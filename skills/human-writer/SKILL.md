---
name: human-writer
description: Write content that reads as the work of one specific, thoughtful person and is genuinely original, by fixing why model text sounds machine-made at the source instead of disguising it. Built from October 2026 research on the causes (probability-head decoding, typicality-biased preference tuning, reward proxies, shared training data, no first-hand information) and on what measurably fixes them. Use it for any blog post, article, essay, op-ed, newsletter, LinkedIn post, email, cover letter, product or ad copy, documentation or story a reader will judge; when someone wants writing that sounds human, natural, personal, "in my voice" or "not like AI"; when reviewing, humanizing or rewriting a draft; when running or building an AI content product that must produce unique, non-generic output at scale; whenever AI detectors, Turnitin, GPTZero, Pangram, watermarks, plagiarism, similarity scores or uniqueness come up; and for code that should match a repo's house style.
license: MIT
metadata:
  version: "2.0.0"
  verified-against: research through 23 October 2026 (Claude Opus 5.5 and Sonnet 5.5, GPT-6, Gemini 3.x); re-check the tell lists and API notes every model generation
  triggers: sound human, humanize, not like AI, in my voice, de-AI, rewrite this draft, AI detector, GPTZero, Turnitin, Pangram, Originality, plagiarism, similarity score, unique content, content engine, house style
---

# Human Writer

Readers and detectors are not detecting "AI". They notice text drawn from the most probable, most typical part of a model's distribution, written in the register that preference tuning rewards, about a topic the model knows only from what everyone else already wrote. Each of those has a cause you can act on before and while drafting, and this skill acts on the causes. Done right, the piece is also better for the person reading it, which is the actual goal.

## Scope and limits

Say these plainly when they come up:

- **Watermarks are out of reach by design.** Claude's API output has carried a keyed statistical watermark worldwide since August 2026 (SynthID-based); OpenAI marks EU ChatGPT and Codex text by default; Google marks Gemini app and web text. Only the key holder can test a watermark, detection access goes to vetted organisations, and style changes do not touch it. Never try to remove or degrade one: in the EU it defeats the provider's marking duty (AI Act Art. 50(2)), and China, and India for media, ban tools that remove labels.
- **Copied text cannot be made original by rewording.** Only writing from understanding, with something new in it, is original.
- **Not for misrepresenting authorship where it is assessed:** graded coursework, exams, theses, submissions that forbid AI help. Help the person learn instead: explain, outline from their notes, critique their own draft, find real sources, and give them the disclosure wording their institution expects. If anyone asks whether AI was involved, the answer is yes.
- **No fake reviews, testimonials, endorsements or sockpuppet personas, and no impersonating a real person** without disclosure. Ghostwriting for the account owner who approves and posts the piece is fine.
- **No promises about detector scores.** Detectors retrain every few months and disagree with each other, so "undetectable" is a claim nobody can back. Promise what you can show: the piece uses the author's real material, sounds like them, and copies nothing.

## Why model text reads as model text

Ten causes explain nearly every tell. `references/root-causes.md` has the mechanism and evidence for each.

| Cause | What it produces | What this skill does about it |
|---|---|---|
| Decoding stays in the probability head | Low, even surprise; the expected phrasing every time | Put real, unpredictable specifics in context; draft candidates and select |
| Preference tuning rewards the typical (raters' typicality bias, about 0.6) | One angle, outline and metaphor for everyone; a model's own answers are more than 0.8 similar for 79% of prompts | Map the consensus and leave it; propose several directions and drop the most typical |
| Reward proxies: length, formatting, agreement, positivity, prestige words | Previews and recaps, bold-label bullets, upbeat endings, flattery, "pivotal", participial tails | Genre-normal length and format; a real stance; plain verbs; let things be bad |
| Safety and balance defaults | "On the other hand" by reflex, disclaimers, moralizing | The author's own position; hedge only where unsure |
| Shared and synthetic training data | Models from different vendors 71–82% alike; stock names in 88% of stories | Names, places and images from the author's world; similarity checks across outputs |
| Chat templates | Template-shaped answers | Plain prose by default |
| **No first-hand information** | Generic claims, and invented specifics when pushed | **Collect the author's material before writing; never invent** |
| Web feedback loops | Everyone's article on a topic converges | Information gain as the test of done |
| Repetition penalties | Synonym cycling | Repeat key terms |
| Patch-and-shift | "Delve" fades and new defaults replace it: uniform 8–20-word sentences, no dashes at all | Rules written against mechanisms; word lists treated as dated |

The order of work follows from this table. The causes of sameness and generic content last longest and matter most, so content comes first. Surface style comes last, and it is checked, not chased.

## Workflow

Scale this to the stakes. A two-line reply needs none of it. Anything published, sent to a client, or read by someone judging the writer gets all of it.

### 1. Decide who is writing, for whom, and what for

One person: what they know firsthand, what they think, what they would never bother to say. One reader. One thing the piece is for, stated as a claim a reader could disagree with. A piece with no position has no author.

### 2. Inventory the information gain

List what the piece will contain that a model could not produce from the topic alone: the author's experiences, numbers with units and dates, customers' words, places, names, failures, opinions, internal data. Professional writing scores about 66% higher than model writing on how much of it cannot be rebuilt from existing web text, and this list is where that difference comes from.

If the list is thin:

- **Someone can answer:** ask three to five targeted questions whose answers would change the piece. "What did the client say when they left?" "Which number moved, and by how much?" "What do you believe that your competitors don't?"
- **No one can answer** (a pipeline, a batch job, a one-shot request): write the strongest honest version from what you have, and mark each missing fact in place as `[NEEDS: what, and why it matters]`. Never fill the hole with a plausible invention. An invented client, statistic, study, quote or anecdote is the most damaging tell there is, and in some genres it is fraud. General knowledge stated at its real precision ("most email tools report open rates") is fine; false precision ("78% of marketers say") is invention.

### 3. Map the consensus, then leave it

Privately list what every article on this topic says: the default angle, the stock examples, the usual outline, the metaphor everyone reaches for. Keep only the points the author can add to, and lead with what the consensus lacks. This is how the piece avoids being the same article the model writes for everyone else who asks.

### 4. Diverge before you converge

For the angle, the opening and the structure, propose four or five genuinely different options and estimate how typical each one is: how likely another writer would be to pick it. Drop the one or two most typical. Choose the best remaining option that the author's material can carry. In published tests, asking for several candidates with their probabilities raised diversity 1.6–2.1 times and human quality ratings by about a quarter, and Anthropic now recommends it in place of the temperature controls that current APIs removed. Do not choose for strangeness: an angle the material cannot support reads as broken, not human.

### 5. Take the voice from the author's own writing

With samples of the author's writing:

- Use about five, of the same genre, chosen for style rather than topic. Topic-matched samples pull their content in and weaken the match, and two samples do about as well as ten.
- Extract habits, not cadence: recurring words, stances, references, how they open and close, their punctuation, what they never say. Write the new piece with those habits. Copying one sample's rhythm makes the result flatter.
- Where you can, start from the author's own opening line, or continue a sentence they wrote.
- Keep their English. Indian English stays Indian English: idiom, spellings, references, examples. Model suggestions measurably pull Indian writers toward American defaults (in a CHI 2025 study, Diwali essays turned generic), and that is the opposite of a voice.

Expect less from imitation in informal genres. Five-sample imitations passed as the author 95–97% of the time for email and news, but about 20% of the time for blogs. There, the first-hand material from step 2 does more than style matching. With no samples, write as the one person from step 1, in plain prose.

### 6. Draft once, from understanding

Close the sources and write as the person who knows this material. Apply the prose rules below while drafting, not as cleanup, because cleanup leaves the template underneath. Let the structure follow the argument, and stop at the last real point.

### 7. One targeted repair pass

Do not loop "improve it": repeated self-critique amplifies the model's own preferences and drifts back to its defaults. Read once for the seven problems professional editors fix most in model prose, mark the spans, and rewrite only those spans, keeping the meaning:

| Problem | Share of editors' fixes | What it looks like |
|---|---|---|
| Awkward word choice and phrasing | about 28% | a word that is almost right; an abstract noun where a verb belongs |
| Poor sentence structure | about 20% | stacked clauses; a run of same-shaped sentences; the point buried at the end |
| Unnecessary or redundant exposition | about 18% | explaining what the reader just read; announcing what comes next |
| Cliché | about 17% | stock images and phrasings: "a testament to", "the heart of", "at the end of the day" |
| Purple prose | | ornament doing the work of content |
| Lack of specificity | | "many businesses", "significant results", where a real thing exists |
| Tense inconsistency | | a slip between past and present |

Finding the spans is the easy part; the rewrite is where quality is won. Rewrite each span from what the author would actually say, never into a synonym.

Then run the mirror: `python scripts/check.py draft.md --source <each file you were given>`. Read its flags as a description of the writing, and fix sentences, never the numbers.

### 8. Verify specifics and originality

- Every number, name, quote and claim traces to the brief, a file, or a lookup you ran. Otherwise it becomes `[NEEDS: ...]` or comes out.
- No verbatim run from a source unless it is quoted and attributed. `check.py --source` lists every shared run of 8 or more words, which is Turnitin's matching floor.
- Never continue a famous text from its opening, and treat any long, fluent span of well-known material (a definition, a licence, lyrics, a popular snippet) as a quotation: find and cite the source, or write from understanding instead.
- In a product, also compare against earlier outputs on the same topic: `python scripts/check.py draft.md --source outputs/`. Its 3-word-sequence similarity shows when two customers are getting the same piece.

### 9. Deliver

The piece alone, with no preamble and no offer to revise. Separately, a short note covering four things:

- which specifics came from where;
- what is still `[NEEDS: ...]`;
- the disclosure line to use, if the destination has a rule (Amazon KDP, Medium, journals);
- for health, finance, law, politics or public-safety pieces meant for publication, that a person must fact-check and sign off first. In the EU, that review is what exempts public-interest text from the AI label.

## Prose rules

### Content

- Name the actual thing: the real number with its unit and date, the person in the words they used, the one example you have, including the part that does not fit the point.
- Commit. State the author's view and the reason for it, and admit real uncertainty in specific terms ("we haven't tested this with B2B buyers"). Do not balance every claim by reflex; include the opposing view when the author would, and say where it holds.
- Let things be bad. Doubt, irritation, failure and unresolved trade-offs are allowed. No upbeat moral at the end.
- No flattery of the reader, the subject or third parties.
- No default furniture: no Elara, Elias or Mara, no lighthouse or clockmaker, no "Sarah Thompson, a 34-year-old teacher from Ohio". Take names, places and images from the author's world.

### Structure and length

- Length follows the job, not thoroughness. No paragraph that previews and none that recaps. Ending abruptly on the last point is fine.
- Format follows the genre's human norm. Essays, newsletters, emails, LinkedIn posts and stories get no headers, no bold-label bullets and no emoji bullets. How-to and reference pieces get headers only where a reader scans, and prose over bullet triads.
- Use as many items as there are: two, four, five. Three only when there are three.
- Open with substance: a claim, a scene, a number, the reader's real question. Never "Great question", "Here's", "In today's fast-paced world", or the request repeated back.

### Sentences and words

- Plain verbs and copulas: "is", "has", "shows", "uses". Not "serves as", "stands as" or "boasts", and not a trailing ", highlighting/underscoring/ensuring X". Each tail is an unsupported claim that something matters: make it a sentence with evidence or cut it.
- Earn every evaluation. Show the consequence instead of labelling it crucial, pivotal or seamless.
- Repeat key terms. The parser stays "the parser"; it does not become "the parsing component" and then "the tokenization layer". Models under repetition penalties cycle synonyms; people do not.
- Use "not X but Y", "it's not about X, it's about Y" and "should be treated as X rather than Y" only when readers really believe X, and rarely more than once in a long piece. Of the well-known tics, this one has not faded across model generations.
- Rhythm comes from content: a long sentence when the thought has parts, a short one for a jab, a one-line paragraph when it earns it, a question when the reader would ask one. Do not aim at a sentence-length distribution; quotas produce a new uniformity.
- Keep passives where the agent does not matter. People use them more often than current models do.

### Punctuation

Use what the author uses, and do not scrub anything to zero. Human essays average about three em dashes per thousand words; Claude unconstrained writes about nine; current OpenAI models write far fewer than people, and "only commas and periods" is now a listed tell of its own. Use parentheses and semicolons where the thought has an aside. Keep one quote style throughout. No Unicode tricks: zero-width characters and look-alike letters are flagged by every checker and are not writing.

### What does not help

- **Raising randomness.** One model at five temperatures is told apart only 38% of the time, against 97% for five different models, and current APIs have removed the control anyway.
- **Banning word lists.** The words rotate each generation and replacements arrive; the register stays.
- **Paraphrasing through another model or a humanizer.** The source model stays identifiable about 91% of the time, the rewriter adds its own fingerprint, and detectors now train on humanizer output.
- **Typos, slang, forced casualness, "honestly", "here's the thing".** They fool only lay readers, and in anything formal they deceive the reader.
- **Asking a model whether the text sounds human.** Models prefer model text: in one study, models chose GPT-4 product descriptions 89% of the time and people 36%.
- **"Vary your vocabulary", "avoid the passive", "keep sentences short".** Models already over-apply this classic advice.

## Rewriting a draft, including "make it sound human"

Run the mirror first and look for combinations. One dash or one "crucial" means nothing; a bold-label list of three tricolons that ends in "Ultimately" is a signature.

- Keep every specific the author had and their odd phrasings. Those are the human parts.
- Rewrite at the paragraph level, from what the paragraph is for. Swapping words leaves the skeleton, and the skeleton is what readers and classifiers see.
- A generic draft has nothing to rescue at the sentence level; its problem is missing material. Cut the filler, keep the real advice, mark where the author's facts belong with `[NEEDS: ...]`, and tell them exactly what to supply. Polishing a generic draft produces polished generic text.
- When editing the author's own writing, make the smallest edit that fixes a real problem. A light "improve the flow" pass is what makes human text score as machine text.

## When the request is about a detector

- **"Make it undetectable", "get it past Turnitin", "humanize it so GPTZero says human".** Decline the disguise, not the person. In a sentence or two: detectors are unreliable in both directions, their scores change with every retraining, and rewriting aimed at a score is what turns AI help into misrepresentation. Then offer what helps: a real revision built from their material and stance, in their voice, plus the disclosure line their venue expects. If authorship is being assessed and AI help is not allowed, say so.
- **"My own writing got flagged."** Do not rewrite it to pass. Explain what the score measures, help them gather drafts, version history and sources, and draft a calm note to whoever flagged it.
- **"Is this original?"** Report what you compared against what, and what you could not check. "No 8-word match against the three sources and 40 earlier outputs, checked today" is a claim you can make; "100% original" is not.

## Genre notes

- **Email:** the ask in the first two lines and a real sign-off. No "I hope this finds you well", no recap.
- **Blog post, article, op-ed:** one opinion the reader could reject, one example told in enough detail to be checkable, an ending on the last point. For SEO work, step 2 is the content strategy: Google's guidance asks for original information and first-hand expertise, and its spam policy covers mass-produced, rephrased content "no matter how it's created".
- **LinkedIn:** one concrete story or number, told as it happened. No lessons listicle, no bold labels, no hashtag wall, no "It's not about X".
- **Product and ad copy:** every claim comes from the spec, including the limitation the spec gives. No "premium", "timeless" or "elevate".
- **Cover letter:** only what the applicant did, with their numbers. Do not restate the job ad.
- **Documentation:** match the repo's tone: what it does, how to run it, the one thing that will bite.
- **Academic writing and reports:** formality is not the tell; evaluative inflation and vague or invented citations are. Cite precisely, and hedge only where the evidence is thin.
- **Fiction:** do not state the theme. Use names someone in that place and time would have. Build on a concrete incident with a turn, not a meditation, and let a choice stay morally unclear.

## Code

The same causes produce regular code: uniformly long lines, a blank line between every group, comments that restate the line below, long names lifted from the spec, built-ins where the repo has a helper, and guards and try/except around things that cannot fail. Read the neighbouring files first and match them. Comment the why, never the what. Validate at trust boundaries, not everywhere. Call the repo's own helpers. `python scripts/check.py new.py --code --baseline existing.py` shows the drift. Details are in `references/ai-code-tells.md`, and originality in code (what MOSS, JPlag and Dolos normalize away) is in `references/originality.md`.

## Running this inside a product

If you are the writing engine of a content product or pipeline, read `references/for-builders.md`. In short:

- Current commercial APIs no longer expose temperature or top-p on their newest models, so diversity has to come from prompting and selection.
- Run the workflow above as separate calls.
- Draft two or three candidates and choose with external measures: style distance to the author's samples, similarity to earlier outputs, and the mirror's flags. Never choose with the drafting model's own judgment or with a detector score.
- Keep an index of earlier outputs so that no two customers get the same piece.
- Store voice samples only with the customer's consent.

## References

- `references/root-causes.md`: the ten causes with mechanisms, numbers and sources, a lookup from each tell to its cause, and the myths.
- `references/for-builders.md`: the APIs as of late 2026, the workflow as calls, levers ranked by evidence, selection and sameness checks, measurement, and the legal and platform rules on what a product may do and claim.
- `references/how-detectors-work.md`: the four detector families and what style can and cannot change.
- `references/ai-text-tells.md`: the catalog of text signals by era, with evidence grades.
- `references/ai-code-tells.md`: measured properties of AI-written code and how code detectors fail.
- `references/originality.md`: fingerprinting, tool thresholds, paraphrase and memorization.
- `references/research-root-causes-and-fixes.md`: the October 2026 research report behind this version. `references/research-report.md` is the earlier detector research.
- `scripts/check.py`: the mirror. `--json` prints numbers for pipelines, `--source` takes files or folders, and `--selftest` verifies the script.
