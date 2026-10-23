# human-writer

An agent skill that makes AI write like one specific person: grounded in real facts, in the author's own voice, with nothing invented and nothing copied. It is built from 2026 research on why AI writing reads as AI. It installs in Claude Code, the Claude apps and the Claude API, in other tools that read the Agent Skills format (Codex, Cursor, Gemini CLI, GitHub Copilot), and as a single Markdown file in ChatGPT, Gemini or any model's system prompt.

[![check](https://github.com/shri-ram07/human-writer/actions/workflows/check.yml/badge.svg)](https://github.com/shri-ram07/human-writer/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills format](https://img.shields.io/badge/format-Agent%20Skills-6b4fbb.svg)](https://agentskills.io)

AI text is easy to spot for reasons that have little to do with the word "delve". Preference training rewards familiar answers: for 79% of open-ended prompts, a model's own answers are more than 80% alike, and answers from different companies' models are 71–82% alike. A model also has no first-hand knowledge, so professional authors score 66% higher than models on how much of their text cannot be rebuilt from what is already on the web. Banning words, raising the temperature and running drafts through a "humanizer" treat the symptoms. Detectors now train on humanizer output, and in one study a panel of expert readers caught every humanized article. This skill changes how the draft is made instead.

## What it makes the model do

1. Collect the author's real material first: experiences, numbers, names, opinions. When something is missing, it asks, or marks the gap as `[NEEDS: ...]`. It never invents a statistic, client, quote or anecdote.
2. List what every article on the topic already says, and leave it.
3. Propose four or five angles, drop the most predictable ones and pick the best of the rest.
4. Take the voice from about five samples of the author's own writing, and keep their English. Indian English stays Indian English.
5. Draft once, then make one repair pass on the seven faults professional editors fix most often in model prose.
6. Trace every specific to a source, copy nothing from the sources, and compare the piece with earlier outputs so two customers never get the same article.

It ships with `check.py`, a dependency-free script that reports the measurable habits of a draft: overused vocabulary, flat rhythm, synonym cycling, template structure, open placeholders and verbatim overlap with any file or folder.

## Example

One of the test cases hands the model a typical ChatGPT-style blog draft (written for this repo) with the request "the client says it sounds like AI, rewrite it". Full texts: [before](examples/rewrite-before.md) and [after](examples/rewrite-after.md).

Before:

> In today's digital age, online reviews have become a crucial factor in the success of local restaurants. Whether it's Google, Zomato, or TripAdvisor, potential diners are increasingly turning to reviews before deciding where to eat. It's not just about reputation—it's about survival in a competitive landscape.

After:

> The time to ask for a review is when a guest has just said something nice. If a table tells the server the mutton was the best they've had this year, that is the moment for "would you mind saying that on Google?" Asking at the bill is too late, because people are tired and already reaching for their phones to pay.

What `check.py` measured on the two texts:

| | Before | After |
|---|---|---|
| Overused words (crucial, landscape, fosters, ever-evolving) | 4 | 0 |
| Wrap-up openers ("Ultimately", "In conclusion") | 2 | 0 |
| "Moreover / Furthermore" sentence openers | 3 | 0 |
| "It's not just X, it's Y" frames | 1 | 0 |
| Evaluative words per 1,000 | 13.3 | 0 |
| Headers | 6 | 1 (the title) |
| Sentences between 8 and 20 words | 80% | 50% |
| Facts marked for the client to supply | 0 | 3 |

The last row matters most. The draft contained no real facts about the restaurant, so the rewrite keeps the useful advice and marks three places where the owner's own numbers belong instead of making them up. When the model does have material, the result looks like [this essay](examples/essay-forty-per-cent-of-what.md): every number in it traces to a source, and it carries about 10 numbers and names per 100 words against 2 in the draft.

## Install

### Claude Code

As a plugin, inside a session:

```
/plugin marketplace add shri-ram07/human-writer
/plugin install human-writer@human-writer
```

Or copy the skill folder:

```bash
git clone https://github.com/shri-ram07/human-writer
cp -r human-writer/skills/human-writer ~/.claude/skills/      # every project
cp -r human-writer/skills/human-writer .claude/skills/        # or just this project
```

The skill loads on its own for writing requests. To call it directly, type `/human-writer`, or `/human-writer:human-writer` for the plugin install.

### Claude apps (claude.ai and desktop)

Download `human-writer.zip` from the [latest release](https://github.com/shri-ram07/human-writer/releases/latest), or zip the `skills/human-writer` folder yourself. Upload it in the Skills section of your settings; the menu is Customize > Skills on newer layouts and Settings > Capabilities on older ones. Custom skills need code execution turned on. Anthropic's guide: [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude).

### Claude API

Upload the same folder through the Skills API. See [Agent Skills](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) in the Claude docs.

### Codex, Cursor, Gemini CLI, GitHub Copilot and other Agent Skills tools

`skills/human-writer/` follows the [Agent Skills](https://agentskills.io) `SKILL.md` format. Copy the folder into the tool's skills directory; each tool's docs give the path.

### ChatGPT, Gemini Gems, editor rules or any system prompt

Use [`portable/human-writer-compact.md`](portable/human-writer-compact.md). It is one file of about 5,500 characters, so it fits a custom GPT's 8,000-character instructions box. Paste it into the instructions of a custom GPT, ChatGPT Project or Gemini Gem, into your editor's rules (for example Cursor project rules or `.github/copilot-instructions.md`), or send it as the system prompt of an API call. Where the tool accepts knowledge files, upload `skills/human-writer/SKILL.md` and the `references/` files too.

## The check script

```bash
python skills/human-writer/scripts/check.py draft.md                     # the mirror
python skills/human-writer/scripts/check.py draft.md --source notes.md   # verbatim runs of 8+ words shared with a source
python skills/human-writer/scripts/check.py draft.md --source outputs/   # compare with every earlier output in a folder
python skills/human-writer/scripts/check.py draft.md --json              # numbers for a pipeline
python skills/human-writer/scripts/check.py new.py --code --baseline old.py
python skills/human-writer/scripts/check.py --selftest
```

It needs Python 3.10 or newer and nothing outside the standard library. Read its flags as a description of the writing, then fix sentences, not numbers. It is not an AI detector, and its output says nothing about how any detector will score a text.

## Why it works

The research behind the skill traced the recognizable habits of model prose to ten causes in how models are trained and used. The ones that matter most:

| Cause | What readers notice | What the skill does |
|---|---|---|
| Preference training rewards the typical | The same angle, outline and metaphor as every other AI article | Maps the consensus and leaves it; picks a less typical angle the material can support |
| No first-hand knowledge | Generic claims, and invented specifics when the model is pushed | Collects the author's material first and marks gaps instead of filling them |
| Reward proxies: length, formatting, agreement, positivity | Previews and recaps, bold-label bullets, upbeat endings, "pivotal" | Genre-normal length and format, a real stance, plain verbs |
| Decoding stays in the probability head | Even, predictable phrasing | Real specifics in context and one targeted repair pass |
| Training data shared across vendors | Stock names: Elara, Elias, Mara and lighthouses fill 88% of model stories | Names, places and images from the author's world |
| Patch-and-shift | "Delve" fades and new defaults replace it, such as uniform 8–20-word sentences | Rules aimed at mechanisms, with word lists treated as dated |

The evidence, with sources:

- [root-causes.md](skills/human-writer/references/root-causes.md): all ten causes, with mechanisms and numbers.
- [The research report](skills/human-writer/references/research-root-causes-and-fixes.md): about 10,500 words with 200+ citations, covering detection, the root causes, the fixes that measurably work, the market and the law.
- [how-detectors-work.md](skills/human-writer/references/how-detectors-work.md): how AI detectors, watermarks and plagiarism checkers work.
- [originality.md](skills/human-writer/references/originality.md): plagiarism fingerprinting and memorization.
- [ai-text-tells.md](skills/human-writer/references/ai-text-tells.md): the catalogue of tells by model era.

## What it will not do

- Promise that no detector will flag the text. Detectors retrain every few months. Claude, OpenAI and Google now watermark generated text in ways only the key holder can test, and no change of style touches those marks. "Undetectable" is a claim nobody can back.
- Strip watermarks, add typos or swap in look-alike characters.
- Write graded coursework or other assessed work for someone to submit as their own. It will explain, outline from the person's notes and critique their draft instead.
- Write fake reviews or testimonials, or impersonate a real person.

These limits follow the model vendors' usage policies, the EU AI Act's marking rules and contract-cheating laws in England, Australia, Ireland and New Zealand. [for-builders.md](skills/human-writer/references/for-builders.md) has the details.

## For people building a writing product

[for-builders.md](skills/human-writer/references/for-builders.md) covers:

- which sampling controls the current Claude, GPT and Gemini APIs still allow;
- the workflow split into separate calls;
- the levers ranked by evidence;
- how to stop two customers getting the same piece;
- voice profiles and consent;
- honest measurement;
- the legal and platform rules in each market.

## Tests

[`skills/human-writer/evals/`](skills/human-writer/evals) holds 10 test cases in the format Claude Code's `claude plugin eval` reads. They cover a blog post from a bare topic, a LinkedIn post, a product description, an op-ed, a short story, a rewrite of an AI draft, an email and a code task. No benchmark results are published yet.

## Contributing

Model habits change with every generation, so the lists of tells go stale quickly. Pull requests are welcome, especially:

- new tells with evidence: a study, or outputs from a named model with the date;
- test cases from real writing jobs;
- benchmark runs of the test cases.

Every rule in the skill traces to a source; please keep it that way. Before opening a pull request, run `python skills/human-writer/scripts/check.py --selftest` and `python tools/validate.py`.

## License and citation

MIT. The research files quote and cite their sources, and quoted material belongs to its authors. To cite this work, use [CITATION.cff](CITATION.cff).
