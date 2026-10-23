#!/usr/bin/env python3
"""check.py - a mirror for drafts, not a target to game.

Prose : python check.py draft.md [--source notes.txt --source paper.txt] [--ngram 8]
Code  : python check.py new_module.py --code [--baseline existing_module.py]
Self  : python check.py --selftest

Prints the measurable things AI-text detectors and plagiarism checkers key on
(sentence-length flatness, marker vocabulary, evaluative density, participial
tails, negative parallelism, synonym cycling, verbatim overlap with sources,
Unicode artifacts) and, for code, the house-style drift against a baseline
file from the same repo. Numbers are a mirror: fix the writing, do not tune
the numbers. Stdlib only.
"""
import argparse
import json
import re
import statistics
import sys
import unicodedata
from collections import Counter
from pathlib import Path

# Words whose frequency rose 3x-170x in LLM-era corpora (Liang 2024, Kobak 2025,
# Gray 2024, Juzek & Ward 2025, Reinhart 2025, Wikipedia era lists). The list
# rotates every model generation; the register (evaluative, Latinate, flowery)
# is the durable thing. See references/ai-text-tells.md.
MARKERS = set("""
delve delves delving delved tapestry testament underscore underscores underscoring showcase
showcases showcasing pivotal meticulous meticulously intricate intricacies commendable
landscape realm realms leverage leverages leveraging foster fosters fostering robust
seamless seamlessly crucial vibrant multifaceted nuanced navigate navigating embark embarking
unlock unlocking elevate elevates elevating harness harnessing ever-evolving game-changer
transformative groundbreaking cutting-edge holistic paramount synergy streamline streamlined
empower empowering insightful invaluable noteworthy comprehensive innovative beacon whimsical
bustling captivating enigmatic indelible unwavering paradigm camaraderie palpable garner
garnered garnering boast boasts boasting bolster bolstered bolstering interplay surpass
surpassing surpasses emphasizing highlighting advancements resonate resonates nestled
renowned exemplifies exemplify profound enduring intriguing versatile laudable methodical
""".split())

PHRASES = [
    "it's important to note", "it is important to note", "it's worth noting", "it is worth noting",
    "in today's fast-paced", "in the realm of", "at the end of the day", "a testament to",
    "plays a crucial role", "plays a pivotal role", "plays a vital role", "in conclusion",
    "in summary", "to sum up", "that being said", "with that in mind", "dive into", "deep dive",
    "shed light on", "a wide range of", "a plethora of", "when it comes to", "great question",
    "i hope this helps", "feel free to", "let's explore", "let's dive", "navigating the",
    "the world of", "stands as a", "serves as a", "marks a", "rich tapestry", "whether you're",
    "look no further", "game changer", "elevate your", "unlock the", "embark on", "key takeaways",
    "it goes without saying", "needless to say", "as an ai", "as a language model", "in the ever-",
    "a beacon of", "in the heart of", "diverse array", "indelible mark", "setting the stage",
    "evolving landscape", "key turning point", "deeply rooted", "reflects broader",
    "underscores its importance", "valuable insights", "align with", "aligns with", "resonate with",
    "boasts a", "commitment to", "should be treated as", "should not be confused with",
    "does not establish that", "not widely documented", "maintains a low profile", "below is a",
    "here's a", "here is a", "let me know if", "would you like", "i've got you", "let's be honest",
    "here's the thing", "the result?", "the bottom line", "serving as a reminder",
]

TRANSITIONS = set("""moreover furthermore additionally consequently thus hence notably
importantly interestingly ultimately overall firstly secondly thirdly lastly finally""".split())

CLOSERS = ["in conclusion", "in summary", "to sum up", "ultimately,", "overall,", "all in all"]

# Evaluative qualifiers: models stack these (whole synonym groups rise together).
EVALUATIVE = set("""crucial critical essential vital key pivotal significant important notable
remarkable fundamental paramount integral invaluable indispensable profound powerful compelling
meaningful impactful substantial""".split())

# Stock people and props that expert detectors and corpus studies flag
# (Russell et al. 2025; Hamilton & Mimno 2026).
STOCK_NAMES = [
    "sarah thompson", "emily carter", "john smith", "jane doe", "john doe", "sarah johnson",
    "michael thompson", "emily johnson", "alex johnson", "david miller", "jane smith", "sarah chen",
    "mark johnson", "lisa thompson", "james anderson", "maria garcia", "robert johnson",
    "sarah mitchell", "emma thompson", "dr. smith", "dr. johnson", "elara", "elias", "mara",
    "the lighthouse keeper", "the old clockmaker", "the clockmaker",
]

NOT_JUST_BUT = re.compile(r"\bnot (?:just|only|merely|simply)\b.{1,70}?\bbut\b", re.I | re.S)
ITS_NOT_ITS = re.compile(
    r"\b(?:isn'?t|is not|aren'?t|are not|wasn'?t|was not|it'?s not|this isn'?t|that'?s not)"
    r" (?:about |just |only |merely )?.{1,70}?[,;:—–-]\s*(?:it'?s|it is|this is|that'?s|they'?re|but rather|rather)\b",
    re.I | re.S)
TRICOLON = re.compile(r"\b\w+(?: \w+)?, \w+(?: \w+)?,? (?:and|or) \w+", re.I)
PARTICIPIAL_OPENER = re.compile(
    r"^[\"']?(?!During|Nothing|Something|Everything|Anything|Morning|Evening|Spring|String|Thing|King|Ring|Wing|Bring|Swing)"
    r"(?:[A-Z]\w*ing|Having|Being)\b[^,.;:!?]{0,60},")
VAGUE_TAIL_VERBS = ("highlighting underscoring emphasizing ensuring reflecting symbolizing contributing "
                    "fostering enhancing showcasing demonstrating signaling marking paving cementing "
                    "solidifying reinforcing illustrating revealing suggesting indicating offering providing "
                    "allowing enabling creating leaving adding helping serving shaping driving positioning "
                    "making").split()
VAGUE_TAIL = re.compile(r",\s+(?:" + "|".join(VAGUE_TAIL_VERBS) + r")\b[^.!?]{0,80}[.!?]", re.I)
ANY_TAIL = re.compile(
    r",\s+(?!including|according|during|regarding|following|notwithstanding|concerning|considering|"
    r"pending|excluding|owing|something|nothing|everything|anything|morning|evening)[a-z]+ing\b", re.I)
ZERO_WIDTH = {"\u200b", "\u200c", "\u200d", "\u2060", "\ufeff", "\u00ad"}

# The skill's marker for a fact only the customer can supply; the pipeline must not ship with any left.
PLACEHOLDER = re.compile(r"\[NEEDS:[^\]\n]{1,160}\]")

STOP = set("""that this with from have they their there which were been will would could should
about what when then than them these those into only also more most some such over just like
very much many even well back after before through where while because being does done made
make your you're other another each every both between under again still might must shall""".split())


# ---------- text prep ----------
def strip_markdown(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    headers = len(re.findall(r"^#{1,6} ", text, flags=re.M))
    bullets = len(re.findall(r"^\s*(?:[-*+]|\d+[.)]) ", text, flags=re.M))
    bold_labels = len(re.findall(r"^\s*(?:[-*+]|\d+[.)])\s+\*\*[^*\n]{1,60}\*\*\s*[:—-]", text, flags=re.M))
    text = re.sub(r"^#{1,6} .*$", "", text, flags=re.M)
    text = re.sub(r"^\s*(?:[-*+]|\d+[.)]) ", "", text, flags=re.M)
    text = re.sub(r"(\*{1,3}|_{1,3})(\S.*?\S|\S)\1", r"\2", text)
    return text, headers, bullets, bold_labels


def split_sentences(text):
    # ponytail: regex splitter, swap in a real tokenizer if abbreviations bite
    flat = re.sub(r"\s+", " ", text).strip()
    parts = re.split(r"(?<=[.!?])[\"')\]]*\s+(?=[\"'(\[]?[A-Z0-9])", flat)
    return [p.strip() for p in parts if len(p.split()) >= 2]


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text) if len(p.split()) >= 3]


def words(text):
    return re.findall(r"[A-Za-z][A-Za-z'’-]*", text)


def content_words(s):
    return {w.lower().strip("'’-") for w in words(s) if len(w) >= 4 and w.lower() not in STOP}


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def find_all(text, needle):
    return [m.start() for m in re.finditer(r"\b" + re.escape(needle) + r"\b", text)]


# ---------- prose metrics ----------
def analyze(raw):
    """Measure a draft: (numbers, matches). Numbers feed --json and pipelines; matches feed the flags."""
    body, n_headers, n_bullets, n_bold_labels = strip_markdown(raw)
    sents = split_sentences(body)
    paras = paragraphs(body)
    ws = words(body)
    n_words = len(ws) or 1
    low = raw.lower().replace("’", "'")
    m = {"words": len(ws), "sentences": len(sents), "paragraphs": len(paras),
         "headers": n_headers, "bullets": n_bullets, "bold_label_bullets": n_bold_labels}

    if len(sents) >= 3:
        lens = [len(s.split()) for s in sents]
        mean, sd = statistics.mean(lens), statistics.pstdev(lens)
        run = best = 1
        for a, b in zip(lens, lens[1:]):
            run = run + 1 if abs(a - b) <= 3 else 1
            best = max(best, run)
        m.update(sentence_mean=mean, sentence_sd=sd, sentence_cv=sd / mean,
                 burstiness=(sd - mean) / (sd + mean) if sd + mean else 0.0,
                 sentence_min=min(lens), sentence_max=max(lens),
                 share_8_20_words=sum(8 <= n <= 20 for n in lens) / len(lens), flat_run=best)
        overlaps = []
        for a, b in zip(sents, sents[1:]):
            ca, cb = content_words(a), content_words(b)
            if ca and cb:
                overlaps.append(len(ca & cb) / len(ca | cb))
        if overlaps:
            m["adjacent_overlap"] = statistics.median(overlaps)

    if len(paras) >= 2:
        pl = [len(p.split()) for p in paras]
        m.update(paragraph_mean=statistics.mean(pl), paragraph_sd=statistics.pstdev(pl),
                 paragraph_cv=statistics.pstdev(pl) / statistics.mean(pl))

    hits = {
        "marker_words": Counter(w.lower().strip("'’-") for w in ws if w.lower().strip("'’-") in MARKERS),
        "marker_phrases": [(p, pos) for p in PHRASES if (pos := find_all(low, p))],
        "transitions": [w for w in (s.split()[0].strip(",").lower() for s in sents) if w in TRANSITIONS],
        "negative_parallelism": ([x.group(0) for x in NOT_JUST_BUT.finditer(body)]
                                 + [x.group(0) for x in ITS_NOT_ITS.finditer(body)]),
        "vague_tails": [x.group(0) for x in VAGUE_TAIL.finditer(body)],
        "participial_openers": [s for s in sents if PARTICIPIAL_OPENER.match(s)],
        "tricolons": TRICOLON.findall(body),
        # wrap-up words only count where they open a sentence ("the overall cost" is not a closer)
        "closers": [s for s in sents if s.lower().startswith(tuple(c.rstrip(",") for c in CLOSERS))],
        "stock_names": [(n, pos) for n in STOCK_NAMES if (pos := find_all(low, n))],
        "mixed_script_words": [x.group(0) for x in re.finditer(r"\w+", raw)
                               if len({unicodedata.name(ch, "?")[:5] for ch in x.group(0) if ch.isalpha()}) > 1],
    }
    hits["placeholders"] = PLACEHOLDER.findall(raw)
    # ponytail: numbers + mid-sentence capitalised words as a proxy for first-hand detail; an NER model would be exact
    nums = len(re.findall(r"(?<![\w.])\d[\d,.:%]*", body))
    names = sum(1 for s in sents for w in s.split()[1:] if re.match(r"[\"'(“‘]?[A-Z][a-z]", w))
    dashes = raw.count("—") + len(re.findall(r"\s--\s|\s–\s", raw))
    ev = sum(1 for w in ws if w.lower() in EVALUATIVE)
    m.update(
        placeholders=len(hits["placeholders"]),
        specifics_per_100_words=(nums + names) / n_words * 100,
        em_dashes=dashes, em_dashes_per_1k=dashes / n_words * 1000,
        evaluative_words=ev, evaluative_per_1k=ev / n_words * 1000,
        participial_per_100_sentences=len(ANY_TAIL.findall(body)) / len(sents) * 100 if sents else 0.0,
        marker_words=sum(hits["marker_words"].values()),
        marker_phrases=sum(len(pos) for _, pos in hits["marker_phrases"]),
        transitions=len(hits["transitions"]),
        negative_parallelism=len(hits["negative_parallelism"]),
        vague_tails=len(hits["vague_tails"]),
        participial_openers=len(hits["participial_openers"]),
        tricolons_per_1k=len(hits["tricolons"]) / n_words * 1000,
        closers=len(hits["closers"]),
        rhetorical_questions=sum(1 for s in sents if s.endswith("?")),
        stock_names=len(hits["stock_names"]),
        zero_width_chars=sum(raw.count(ch) for ch in ZERO_WIDTH),
        mixed_script_words=len(hits["mixed_script_words"]),
    )
    return m, hits


def prose_report(raw, sources, ngram):
    m, hits = analyze(raw)
    n_words = m["words"] or 1
    out = [f"== {m['words']} words, {m['sentences']} sentences, {m['paragraphs']} paragraphs, "
           f"{m['headers']} headers, {m['bullets']} bullet lines, {m['bold_label_bullets']} bold-label bullets"]
    flags = []

    if "sentence_mean" in m:
        out.append(f"Sentence length   mean {m['sentence_mean']:.1f}  sd {m['sentence_sd']:.1f}  "
                   f"cv {m['sentence_cv']:.2f}  burstiness {m['burstiness']:+.2f}  "
                   f"min {m['sentence_min']}  max {m['sentence_max']}  "
                   f"| in 8-20 word band: {m['share_8_20_words']:.0%}  "
                   f"| longest run of near-equal lengths: {m['flat_run']}")
        out.append("                  (burstiness near 0 or above is human-like; strongly negative is flat. "
                   "Uniform 8-20 word sentences are a 2026 over-correction artifact.)")
        if m["share_8_20_words"] > 0.85 and m["sentences"] >= 8:
            flags.append(f"Sentence lengths clamped: {m['share_8_20_words']:.0%} of sentences are 8-20 words long")
        if m["flat_run"] >= 6:
            flags.append(f"Flat rhythm: {m['flat_run']} consecutive sentences within 3 words of each other")
        if "adjacent_overlap" in m:
            out.append(f"Adjacent overlap  median {m['adjacent_overlap']:.3f} shared content words between "
                       f"neighbouring sentences (one 2026 benchmark: human median ~0.06, machine ~0.02; "
                       f"people repeat the term, models swap synonyms)")
            if m["adjacent_overlap"] < 0.02 and m["sentences"] >= 15 and m["words"] >= 300:
                flags.append("Synonym cycling: neighbouring sentences almost never reuse a content word")

    if "paragraph_mean" in m:
        out.append(f"Paragraph length  mean {m['paragraph_mean']:.0f}  sd {m['paragraph_sd']:.0f}  "
                   f"cv {m['paragraph_cv']:.2f}")
        if m["paragraph_cv"] < 0.25 and m["paragraphs"] >= 4:
            flags.append(f"Uniform paragraphs: all within about {m['paragraph_cv']:.0%} of the mean length")

    out.append(f"Em dashes         {m['em_dashes_per_1k']:.1f} per 1000 words "
               f"(human essays average about 3; zero is fine, one in every paragraph is not)")
    if m["em_dashes_per_1k"] > 8:
        flags.append(f"Em dashes: {m['em_dashes']} in {n_words} words")
    out.append(f"Evaluative words  {m['evaluative_per_1k']:.1f} per 1000 words "
               f"(crucial, key, significant, vital...; models add qualifiers instead of evidence)")
    if m["evaluative_per_1k"] > 8 and n_words > 150:
        flags.append(f"Evaluative qualifiers stacked: {m['evaluative_words']} in {n_words} words")
    if m["sentences"]:
        out.append(f"Participial       {m['participial_per_100_sentences']:.0f} ', ...ing' clauses per 100 "
                   f"sentences (instruction-tuned models use about 5x the human rate)")
    out.append(f"Specifics         {m['specifics_per_100_words']:.1f} numbers and names per 100 words "
               f"(a rough mirror for first-hand detail, not a quota: brand names count too)")
    if m["placeholders"]:
        flags.append(f"Placeholders still open ({m['placeholders']}): " + " | ".join(hits["placeholders"][:5]))

    if hits["marker_words"]:
        detail = ", ".join(f"{w} x{n}" if n > 1 else w for w, n in hits["marker_words"].most_common())
        flags.append(f"Marker words ({m['marker_words']}): {detail}")
    if hits["marker_phrases"]:
        parts = [f'"{p}" (' + ", ".join(f"L{line_of(raw, x)}" for x in pos[:3]) + ")"
                 for p, pos in hits["marker_phrases"]]
        flags.append(f"Marker phrases ({m['marker_phrases']}): " + "; ".join(parts))
    if hits["transitions"]:
        flags.append(f"Sentence-initial transitions ({m['transitions']}): "
                     + ", ".join(w.capitalize() for w in hits["transitions"][:8]))
    if hits["negative_parallelism"]:
        shown = [re.sub(r"\s+", " ", n)[:80] for n in hits["negative_parallelism"][:4]]
        flags.append(f"Negative parallelism ({m['negative_parallelism']}): " + " | ".join(f'"{s}"' for s in shown))
    if hits["vague_tails"]:
        shown = [re.sub(r"\s+", " ", t)[:70] for t in hits["vague_tails"][:3]]
        flags.append(f"Participial tails with vague claims ({m['vague_tails']}): " + " | ".join(f'"{s}"' for s in shown))
    po = hits["participial_openers"]
    if po and len(po) / m["sentences"] > 0.04:
        flags.append(f"Participial openers ({len(po)} = {len(po) / m['sentences']:.0%} of sentences): "
                     + " | ".join(f'"{s[:50]}..."' for s in po[:3]))
    if m["tricolons_per_1k"] > 6:
        flags.append(f"Lists of three ({len(hits['tricolons'])}, {m['tricolons_per_1k']:.1f} per 1000 words): "
                     + " | ".join(f'"{t[:60]}"' for t in hits["tricolons"][:3]))
    if hits["closers"]:
        flags.append("Closers: " + " | ".join(f'"{s[:50]}..."' for s in hits["closers"][:3]))
    rq = m["rhetorical_questions"]
    if rq and m["sentences"] >= 5 and rq / m["sentences"] > 0.12:
        flags.append(f"Rhetorical questions: {rq} of {m['sentences']} sentences")
    if hits["stock_names"]:
        flags.append("Stock names: " + ", ".join(f"{n.title()} (L{line_of(raw, pos[0])})" for n, pos in hits["stock_names"]))
    if m["bold_label_bullets"] >= 3:
        flags.append(f"Inline-header bullets: {m['bold_label_bullets']} bullets start with a bold label and a colon")
    if m["zero_width_chars"] or m["mixed_script_words"]:
        flags.append(f"Unicode artifacts: {m['zero_width_chars']} zero-width/soft-hyphen chars, "
                     f"{m['mixed_script_words']} mixed-script words {hits['mixed_script_words'][:5]} -> remove; "
                     f"plagiarism tools flag these and they are not writing")

    out.append("-- Flags" if flags else "-- Flags: none")
    out.extend("  " + f for f in flags)

    if sources:
        body = strip_markdown(raw)[0]
        dw = norm_words(body)
        for name, src in sources:
            sw = norm_words(src)
            runs = shared_runs(dw, sw, ngram)
            out.append(f"-- Overlap with {name} ({ngram}-word runs; Turnitin's small-match floor is 8 words; "
                       f"3-word-sequence similarity {jaccard3(dw, sw):.3f}, higher = more alike)")
            if not runs:
                out.append("  none")
            for s, e in runs[:20]:
                snippet = " ".join(dw[s:e])
                out.append(f'  {e - s} words: "{snippet}"')
    return "\n".join(out)


def norm_words(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def jaccard3(a, b):
    """Share of distinct 3-word sequences two texts have in common: catches two pieces built the same way
    even where no 8-word run is copied."""
    sa, sb = ({tuple(w[i:i + 3]) for i in range(len(w) - 2)} for w in (a, b))
    return len(sa & sb) / len(sa | sb) if sa | sb else 0.0


def shared_runs(draft, src, n):
    grams = {tuple(src[i:i + n]) for i in range(len(src) - n + 1)}
    runs = []
    for i in range(len(draft) - n + 1):
        if tuple(draft[i:i + n]) in grams:
            if runs and i <= runs[-1][1] + 1:
                runs[-1][1] = i
            else:
                runs.append([i, i])
    return [(s, e + n) for s, e in runs]


# ---------- code metrics ----------
KEYWORDS = set("""if else elif for while return def class import from as with try except finally
raise pass break continue lambda yield async await and or not in is None True False self cls
function const let var new this typeof instanceof switch case default throw catch public private
protected static void int float double string bool char long struct enum interface package
fn pub mut impl use mod match func type map chan go defer range nil""".split())
CODE_STOP = set("""the and for this that with from return def class import self none true false int str
list dict set if else elif while try except function const let var new get value data result
into when then than are was were will can""".split())


def restating_comments(src):
    lines = src.splitlines()
    total = restate = 0
    for i, line in enumerate(lines[:-1]):
        m = re.match(r"\s*(?:#|//)\s*(.+)", line)
        if not m or re.match(r"\s*(?:#|//)", lines[i + 1]):
            continue
        total += 1
        cwords = {w.lower() for w in re.findall(r"[A-Za-z]{3,}", m.group(1))} - CODE_STOP
        spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", lines[i + 1])
        nwords = {w.lower() for w in re.findall(r"[A-Za-z]{3,}", spaced)} - CODE_STOP
        # restating = most of the comment's content words reappear in the code below it;
        # a long why-comment that shares one loop variable is not restating
        if cwords and len(cwords & nwords) / len(cwords) >= 0.5:
            restate += 1
    return (restate / total if total else 0.0), total


def code_stats(src):
    lines = src.splitlines()
    nonblank = [l for l in lines if l.strip()]
    comments = [l for l in nonblank if re.match(r"\s*(#|//|/\*|\*|--|\"\"\"|''')", l)]
    code = max(len(nonblank) - len(comments), 1)
    lens = [len(l) for l in nonblank] or [0]
    idents = [t for t in re.findall(r"[A-Za-z_]\w*", src) if t not in KEYWORDS and len(t) > 1]
    defs = re.findall(r"^\s*(?:(?:async\s+)?def |function |fn |func |(?:public|private|protected)\s[^=\n]*\()", src, re.M)
    docstrings = re.findall(r"^\s*(?:async\s+)?def [^\n]*:\s*\n\s*(?:\"\"\"|''')", src, re.M)
    gaps = [w.count("\n") for w in re.findall(r"\n\s*\n+", src)]
    restate_ratio, n_inline = restating_comments(src)
    return {
        "lines": len(lines),
        "comment lines / code lines": len(comments) / code,
        "comments restating the next line": restate_ratio,
        "blank-line ratio": (len(lines) - len(nonblank)) / max(len(lines), 1),
        "blank-run size sd": statistics.pstdev(gaps) if len(gaps) > 1 else 0.0,
        "line length mean": statistics.mean(lens),
        "line length sd": statistics.pstdev(lens),
        "identifier length mean": statistics.mean(map(len, idents)) if idents else 0.0,
        "functions": len(defs),
        "docstring coverage": len(docstrings) / max(len(defs), 1),
        "try blocks per 100 code lines": len(re.findall(r"^\s*try\b", src, re.M)) / code * 100,
        "None/null guards per 100 code lines": len(re.findall(
            r"\bif\b[^\n]*(?:\bis(?: not)? None\b|[!=]==? ?(?:null|undefined|None)\b)", src)) / code * 100,
        "TODO/FIXME/HACK": len(re.findall(r"\b(?:TODO|FIXME|XXX|HACK)\b", src)),
    }


def code_report(draft_name, draft, baseline_name, baseline):
    a = code_stats(draft)
    b = code_stats(baseline) if baseline is not None else None
    w = max(len(k) for k in a)
    head = f"{'metric':<{w}}  {draft_name[-22:]:>22}" + (f"  {baseline_name[-22:]:>22}" if b else "")
    out = [head, "-" * len(head)]
    for k, v in a.items():
        fmt = (lambda x: f"{x:>22.2f}") if isinstance(v, float) else (lambda x: f"{x:>22}")
        out.append(f"{k:<{w}}  {fmt(v)}" + (f"  {fmt(b[k])}" if b else ""))
    out.append("")
    out.append("Read the columns side by side. Measured AI-code drift: higher comment ratio, comments that restate")
    out.append("the line below, docstrings on trivial functions, very regular blank lines, lower line-length sd,")
    out.append("longer identifiers, guards and try blocks the caller never asked for. Match the repo, not a textbook.")
    return "\n".join(out)


# ---------- self test ----------
AI_SAMPLE = """In today's fast-paced digital landscape, it's important to note that leveraging robust solutions is crucial.
Moreover, organizations must navigate an ever-evolving realm of challenges. Furthermore, a seamless approach fosters
innovation across teams. It's not just about tools, it's about mindset. Additionally, meticulous planning showcases
commitment. The team shipped the feature on time, highlighting their commitment to excellence. Ultimately, this
serves as a testament to resilience. In conclusion, success is not merely possible but inevitable when stakeholders
embark on this transformative journey together with Sarah Thompson."""

HUMAN_SAMPLE = """We shipped the thing on a Tuesday. Nobody noticed for three days, which was the plan, and then
the pager went off at 2 a.m. because one customer in Ohio had a tab name with a slash in it. One slash. I had
written the parser myself and I had, I'm fairly sure, tested slashes. Apparently not that kind. We fixed it in
twenty minutes and then spent the rest of the week arguing about whether tab names should allow slashes at all.
They should. People name things how they name things."""


def selftest():
    ai = prose_report(AI_SAMPLE, [], 8)
    hu = prose_report(HUMAN_SAMPLE, [], 8)
    for needle in ("Marker words", "Negative parallelism", "Sentence-initial transitions", "Stock names",
                   "Closers", "Participial tails"):
        assert needle in ai, (needle, ai)
    assert "Flags: none" in hu, hu
    src = "the pager went off at 2 a.m. because one customer in Ohio had a tab name"
    assert "17 words" in prose_report(HUMAN_SAMPLE, [("src", src)], 8)
    assert "Unicode artifacts" in prose_report("Plain te\u200bxt with a zero width space here.", [], 8)
    assert "Unicode artifacts" in prose_report("Mixed scrіpt word here.", [], 8)  # Cyrillic i
    m, _ = analyze(HUMAN_SAMPLE + " [NEEDS: the customer's churn number]")
    assert m["placeholders"] == 1 and m["specifics_per_100_words"] > 2, m
    assert abs(jaccard3("a b c d".split(), "a b c e".split()) - 1 / 3) < 1e-9
    cs = code_stats("def f(x):\n    \"\"\"Doc.\"\"\"\n    # add one\n    return x + 1\n\n\n"
                    "def g(counter):\n    # increment the counter\n    counter += 1\n    try:\n"
                    "        return counter\n    except Exception:\n        return None\n")
    assert cs["functions"] == 2 and 0.4 < cs["docstring coverage"] < 0.6, cs
    assert abs(cs["comments restating the next line"] - 0.5) < 1e-9, cs
    print("selftest ok")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("draft", nargs="?")
    ap.add_argument("--source", action="append", default=[],
                    help="file (or folder of .md/.txt files, e.g. earlier outputs) the draft must not copy")
    ap.add_argument("--ngram", type=int, default=8)
    ap.add_argument("--json", action="store_true", help="print the prose numbers as JSON, for pipelines")
    ap.add_argument("--code", action="store_true")
    ap.add_argument("--baseline", help="existing file from the same repo (with --code)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.draft:
        ap.error("draft path required")
    draft = open(args.draft, encoding="utf-8", errors="replace").read()
    if args.code:
        base = open(args.baseline, encoding="utf-8", errors="replace").read() if args.baseline else None
        print(code_report(args.draft, draft, args.baseline or "", base))
        return
    paths = []
    for p in args.source:
        paths += sorted(str(f) for f in Path(p).rglob("*") if f.suffix in (".md", ".txt")) if Path(p).is_dir() else [p]
    sources = [(p, open(p, encoding="utf-8", errors="replace").read()) for p in paths
               if Path(p).resolve() != Path(args.draft).resolve()]
    if not args.json:
        print(prose_report(draft, sources, args.ngram))
        return
    m, _ = analyze(draft)
    dw = norm_words(strip_markdown(draft)[0])
    # longest_run: longest verbatim run shared with the source, in words (0 = nothing at or above --ngram)
    m["overlap"] = {name: {"longest_run": max((e - s for s, e in shared_runs(dw, sw, args.ngram)), default=0),
                           "jaccard3": jaccard3(dw, sw)}
                    for name, sw in ((n, norm_words(s)) for n, s in sources)}
    print(json.dumps(m, indent=1))


if __name__ == "__main__":
    sys.exit(main())
