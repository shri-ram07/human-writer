"""Repo checks that back the README's claims. Run from anywhere: python tools/validate.py"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "human-writer"
errors = []


def check(ok, msg):
    if not ok:
        errors.append(msg)


# SKILL.md frontmatter, per the Agent Skills format: lowercase name matching the folder, description <= 1024 chars
text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
front = re.match(r"---\n(.*?)\n---\n", text, re.S)
check(front, "SKILL.md has no frontmatter")
fields = dict(re.findall(r"^(name|description): (.*)$", front.group(1), re.M)) if front else {}
check(fields.get("name") == SKILL.name, f"frontmatter name {fields.get('name')!r} != folder {SKILL.name!r}")
check(re.fullmatch(r"[a-z0-9-]{1,64}", fields.get("name", "")), "name must be 1-64 lowercase letters, digits, hyphens")
check(0 < len(fields.get("description", "")) <= 1024, f"description is {len(fields.get('description', ''))} chars")
check(len(text.splitlines()) < 500, "SKILL.md should stay under 500 lines")

# every bundled file SKILL.md points at exists
for ref in sorted(set(re.findall(r"`((?:references|scripts)/[\w./-]+\.(?:md|py))`", text))):
    check((SKILL / ref).is_file(), f"SKILL.md mentions missing file {ref}")

# the portable prompt must fit a custom GPT's 8,000-character instructions box
compact = (ROOT / "portable" / "human-writer-compact.md").read_text(encoding="utf-8")
check(len(compact) <= 8000, f"portable prompt is {len(compact)} chars, over 8000")

# plugin and marketplace manifests agree, and the plugin source exists
plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
check(plugin["name"] == fields.get("name"), "plugin.json name differs from the skill name")
check(not re.match(r"(claude|anthropic|anthropics|cc-plugin)-", plugin["name"]), "plugin name uses a reserved prefix")
check(market.get("owner", {}).get("name"), "marketplace.json needs owner.name")
for entry in market["plugins"]:
    check(entry["name"] == plugin["name"], "marketplace entry name differs from plugin.json name")
    check(".." not in entry["source"] and (ROOT / entry["source"]).is_dir(), f"bad source {entry['source']}")

# every eval case loads under claude plugin eval: prompt.md, case.yaml with its name, at least one grader
for case in sorted(p for p in (SKILL / "evals").iterdir() if p.is_dir()):
    check((case / "prompt.md").is_file(), f"{case.name}: no prompt.md")
    yaml = (case / "case.yaml").read_text(encoding="utf-8") if (case / "case.yaml").is_file() else ""
    check(f"name: {case.name}\n" in yaml and 'schema_version: "1.1"' in yaml, f"{case.name}: bad case.yaml")
    check(any((case / "graders").glob("*.md")), f"{case.name}: no graders")

if errors:
    print("\n".join("FAIL " + e for e in errors))
    sys.exit(1)
print("validate ok")
