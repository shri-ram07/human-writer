# human-writer

Make AI write like one specific person: grounded in real facts, in the author's own voice, with nothing invented and nothing copied.

human-writer is an agent skill built from 2026 research on why AI text reads as AI. It installs in Claude Code, the Claude apps and the Claude API, in tools that read the Agent Skills format (Codex, Cursor, Gemini CLI, GitHub Copilot), and as a single Markdown file you can paste into ChatGPT, a Gemini Gem or any system prompt.

[![check](https://github.com/shri-ram07/human-writer/actions/workflows/check.yml/badge.svg)](https://github.com/shri-ram07/human-writer/actions/workflows/check.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Agent Skills format](https://img.shields.io/badge/format-Agent%20Skills-6b4fbb.svg)](https://agentskills.io)

> **Before**, a typical AI draft: "In today's digital age, online reviews have become a crucial factor in the success of local restaurants. Whether it's Google, Zomato, or TripAdvisor, potential diners are increasingly turning to reviews before deciding where to eat. It's not just about reputation—it's about survival in a competitive landscape."
>
> **After**, the same advice rewritten with this skill: "The time to ask for a review is when a guest has just said something nice. If a table tells the server the mutton was the best they've had this year, that is the moment for "would you mind saying that on Google?" Asking at the bill is too late, because people are tired and already reaching for their phones to pay."

## Why AI writing sounds like AI

Most advice blames words like "delve". The research points somewhere deeper, and it explains why word lists and humanizers keep failing.

- **Training rewards the typical.** People who rate model answers prefer familiar text, and preference training amplifies that preference. For 79% of open-ended prompts a model's own answers are more than 80% alike, and answers from different companies' models are 71–82% alike ([Jiang et al. 2025](https://arxiv.org/html/2510.22954); [Zhang et al. 2025](https://arxiv.org/html/2510.01171)).
- **The model has nothing first-hand.** Professional authors score 66% higher than models on how much of their text cannot be rebuilt from what is already on the web ([Lu et al. 2025](https://arxiv.org/abs/2410.04265)).
- **Surface fixes do not hold.** A model's text stays identifiable about 91% of the time after paraphrasing ([Sun et al. 2025](https://arxiv.org/html/2502.12150)). Turnitin trained its 2025 detector on humanizer output ([Plagiarism Today](https://www.plagiarismtoday.com/2025/08/27/turnitin-launches-anti-ai-humanizer-feature/)), and a panel of expert readers caught every humanized article in one study ([Russell, Karpinska & Iyyer 2025](https://arxiv.org/abs/2501.15654)).

So the skill does not disguise finished text. It changes what goes into the draft and how the draft is made.

## What the skill makes the model do

1. Collect the author's real material first: experiences, numbers, names, opinions. When something is missing, it asks, or marks the gap as `[NEEDS: ...]`. It never invents a statistic, client, quote or anecdote.
2. List what every article on the topic already says, and leave it.
3. Propose four or five angles, drop the most predictable ones and pick the best of the rest.
4. Take the voice from about five samples of the author's own writing, and keep their English. Indian English stays Indian English.
5. Draft once, then make one repair pass on the seven faults professional editors fix most often in model prose.
6. Trace every specific to a source, copy nothing from the sources, and compare the piece with earlier outputs so two customers never get the same article.

It ships with `check.py`, a dependency-free script that reports the measurable habits of a draft: overused vocabulary, flat rhythm, synonym cycling, template structure, open placeholders and verbatim overlap with any file or folder.

## Evidence so far

The example at the top is one of the repo's test cases: a typical ChatGPT-style blog draft (written for this repo) and the request "the client says it sounds like AI, rewrite it". Full texts: [before](examples/rewrite-before.md) and [after](examples/rewrite-after.md). `check.py` measured both:

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

The last row matters most. The draft contained no real facts about the restaurant, so the rewrite keeps the useful advice and marks three places where the owner's own numbers belong instead of making them up.

This is what `check.py` printed for the draft, unedited apart from the cut header lines:

```text
== 301 words, 18 sentences, 6 paragraphs, 6 headers, 3 bullet lines, 0 bold-label bullets
-- Flags
  Uniform paragraphs: all within about 11% of the mean length
  Em dashes: 4 in 301 words
  Evaluative qualifiers stacked: 4 in 301 words
  Marker words (4): crucial, landscape, fosters, ever-evolving
  Marker phrases (1): "in conclusion" (L27)
  Sentence-initial transitions (3): Moreover, Furthermore, Ultimately
  Negative parallelism (1): "It's not just about reputation—it's"
  Closers: "Ultimately, reviews are more than just ratings—the..." | "In conclusion, online reviews are a powerful tool ..."
```

When the model does have material, the result looks like [this essay](examples/essay-forty-per-cent-of-what.md). Every number in it traces to a source listed below it, and it carries about 10 numbers and names per 100 words against 2 in the draft.

Not measured yet: a with-and-without benchmark across the [10 test cases](skills/human-writer/evals), and any blind panel of human judges. Until those exist, treat this section as a demonstration, not a result.

## Every rule traces to a study

| Rule in the skill | What the evidence found | Source |
|---|---|---|
| Collect first-hand material and never invent | Professional authors' text is 66% harder to rebuild from the web than model text | [Lu et al. 2025](https://arxiv.org/abs/2410.04265) |
| Propose several angles and drop the most typical | 1.6–2.1x more semantic diversity, and higher ratings from human judges | [Zhang et al. 2025](https://arxiv.org/html/2510.01171v3) |
| One repair pass on seven fault types | Closed about half the gap to edits by professional writers | [Chakrabarty, Laban & Wu 2025](https://arxiv.org/html/2409.14509v5) |
| About five samples of the author, chosen for style | Imitations passed as the author 95–97% of the time for email and news, about 20% for blogs; two samples did about as well as ten | [Wang et al. 2025](https://arxiv.org/html/2509.14543v1) |
| Keep the author's own English | AI suggestions pulled Indian writers toward American style, and Diwali essays turned generic | [Agarwal, Naaman & Vashistha 2025](https://arxiv.org/html/2409.11360v3) |
| Never let the drafting model judge its own text | Models picked GPT-4 product descriptions 89% of the time; people picked them 36% | [Laurito et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12337326/) |
| No stock names or props | Eleven stock words, Elara and lighthouses among them, appear in 88% of model stories | [Hamilton & Mimno 2026](https://arxiv.org/abs/2605.26492) |
| No temperature tricks | One model at five temperatures was told apart 38% of the time; five different models 97% | [Sun et al. 2025](https://arxiv.org/html/2502.12150) |

The full evidence is in the [research report](skills/human-writer/references/research-root-causes-and-fixes.md), about 10,500 words with 200+ citations, and in [root-causes.md](skills/human-writer/references/root-causes.md). How AI detectors, watermarks and plagiarism checkers work is covered in [how-detectors-work.md](skills/human-writer/references/how-detectors-work.md) and [originality.md](skills/human-writer/references/originality.md).

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

## Try it yourself in five minutes

1. Ask the AI you normally use for a 600-word blog post on a topic you know. Save the answer as `before.md`.
2. Give the same AI the portable file as instructions (or install the skill), and ask again with two or three facts from your own experience. Save that as `after.md`.
3. Run `python skills/human-writer/scripts/check.py before.md`, then the same on `after.md`, and compare the flags.
4. Read both aloud to someone who knows the topic.

If the second draft is not better, open an issue with both texts. That is the most useful bug report this repo can get.

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

## Questions people ask

### Will it get my text past Turnitin or GPTZero?

It is not built to, and nobody can honestly promise that. Detectors retrain every few months, and Claude, OpenAI and Google now put statistical watermarks in generated text that only the key holder can test and no change of style removes. What the research does show is that writing built from real material reads differently. In one study, a model trained on an author's own books was flagged by Pangram 3% of the time, against 97% for the same model imitating that author from a prompt ([Chakrabarty, Ginsburg & Dhillon 2025](https://arxiv.org/html/2510.13939v3)). That was model training, not this skill, and it is one preprint.

### Is this an AI humanizer?

No. A humanizer rewrites finished text, and the original model stays identifiable through paraphrase. This skill works earlier: on the facts, the angle and the voice that go into the draft, and on one targeted edit afterwards.

### Why does the output contain `[NEEDS: ...]`?

Because the skill will not invent facts. Each marker names the specific thing only you can supply, such as your own number, your customer's words or the example that happened to you. Fill them in and the piece becomes yours.

### Which AI models does it work with?

Any model that follows long instructions. The rules were checked against Claude, GPT and Gemini as of October 2026. Current Claude and GPT APIs no longer let you set temperature on their newest models, so the skill gets variety from prompting instead.

### Does it work in other languages?

It is written for English and keeps the author's variety of it: Indian, British, American or any other. Other languages are untested.

### Can I use it in a commercial product?

Yes, under the MIT license. If you are building a writing product, read [for-builders.md](skills/human-writer/references/for-builders.md) first. It covers the API controls that still exist, the workflow as separate calls, how to keep two customers from getting the same piece, voice profiles and consent, and the legal rules in each market, including the EU AI Act's marking duty.

## What it will not do

- Promise that no detector will flag the text.
- Strip watermarks, add typos or swap in look-alike characters.
- Write graded coursework or other assessed work for someone to submit as their own. It will explain, outline from the person's notes and critique their draft instead.
- Write fake reviews or testimonials, or impersonate a real person.

These limits follow the model vendors' usage policies, the EU AI Act's marking rules and contract-cheating laws in England, Australia, Ireland and New Zealand.

## Known limits

- No benchmark has been run yet; the evidence above is a demonstration plus published research.
- Much of the research on editing and diversity used creative writing. Marketing copy, email and LinkedIn posts are less studied.
- Imitating a voice from samples works far better for email and news than for blogs.
- `check.py` is a rough mirror. It counts brand names as specifics, and prose with many short sentences can trip its synonym-cycling flag.
- The lists of AI tells are dated October 2026. Models change, and the lists will need updates.

## Tests

[`skills/human-writer/evals/`](skills/human-writer/evals) holds 10 test cases in the format Claude Code's `claude plugin eval` reads. They cover a blog post from a bare topic, a LinkedIn post, a product description, an op-ed, a short story, a rewrite of an AI draft, an email and a code task.

## Contributing

Model habits change with every generation, so the lists of tells go stale quickly. Pull requests are welcome, especially:

- new tells with evidence: a study, or outputs from a named model with the date;
- test cases from real writing jobs;
- benchmark runs of the test cases;
- before-and-after pairs from your own use.

Every rule in the skill traces to a source; please keep it that way. Before opening a pull request, run `python skills/human-writer/scripts/check.py --selftest` and `python tools/validate.py`.

## License, citation and author

MIT. The research files quote and cite their sources, and quoted material belongs to its authors. To cite this work, use [CITATION.cff](CITATION.cff).

Made by Shri Ram Dwivedi ([@shri-ram07](https://github.com/shri-ram07)). Questions, results and disagreements are welcome in the issues.
