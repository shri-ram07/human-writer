# For builders: running human-writer inside a product

For whoever runs this skill as the writing engine of a content product or pipeline. Tags follow `root-causes.md`: untagged findings are peer-reviewed or replicated; [LIMITED], [VENDOR CLAIM], [HYPOTHESIS] and [UNKNOWN] mark weaker ground. Verified against research through 23 October 2026.

## 1. What the model APIs allow (October 2026)

Check the current API documentation before relying on any cell: this is what the vendors' pages said on 23 October 2026.

| Control | Anthropic (Messages API) | OpenAI (GPT-6 family) | Google (Gemini 3, Vertex AI) |
|---|---|---|---|
| temperature, top_p, top_k | "Removed - 400" on Fable 5/5.1, Opus 5.5, Opus 5, Opus 4.8/4.7 and Sonnet 5; "Non-default values - 400" on Sonnet 5.5 and Haiku 5.5 (Haiku 5.5 accepts only `temperature = 1` and `top_p = 0.99`); allowed on Opus 4.6, Sonnet 4.6 and Haiku 4.5, one of the two at most | removed whenever reasoning effort is not `none`; GPT-6 Astra and GPT-6.1 Sol do not support `none`, GPT-6 Sol and GPT-6 Luna do | Gemini 3: keep temperature at 1.0, since lowering it "may lead to unexpected behavior, such as looping or degraded performance"; Gemini 3.6 Flash and later: custom values "aren't supported and are ignored if set" |
| Prefill | 400 on the whole 4.6+ family | not covered | not covered |
| Several samples | repeated calls | `n` | multiple candidates (Preview) |
| Log-probabilities | none documented | removed above effort `none` | `avgLogprobs`, `logprobsResult` |
| Logit bias, penalties | none documented | `logit_bias` (−100 to 100) and penalties (−2.0 to 2.0) remain in the schema; honoured by GPT-6 reasoning models? [UNKNOWN] | penalties unsupported from Gemini 3.6 Flash; no logit bias |
| Text watermark on API output | yes, worldwide, no opt-out mentioned [VENDOR CLAIM] | off by default, opt-in for select models [VENDOR CLAIM] | not stated; Google names only "the Gemini app and web experience" [UNKNOWN] |

Sources: [Opus 5.5 guide](https://platform.claude.com/docs/en/models/opus-5-5/migration-guide), [Anthropic guides](https://platform.claude.com/docs/en/about-claude/models/migration-guide), [OpenAI guide](https://r.jina.ai/https://platform.openai.com/docs/guides/latest-model), [openai-python](https://raw.githubusercontent.com/openai/openai-python/main/src/openai/types/chat/completion_create_params.py), [Gemini 3](https://ai.google.dev/gemini-api/docs/gemini-3), [Vertex parameters](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/multimodal/content-generation-parameters), [Gemini API](https://ai.google.dev/api/generate-content), [Claude marking](https://support.claude.com/en/articles/16266773-how-claude-marks-ai-generated-content), [OpenAI provenance](https://openai.com/index/eu-text-provenance/), [SynthID](https://deepmind.google/models/synthid/). Open weights served with vLLM keep every knob, including `min_p`, `repetition_penalty`, `bad_words` and `logit_bias` ([vLLM](https://docs.vllm.ai/en/latest/api/vllm/sampling_params.html)).

What this means for the pipeline [HYPOTHESIS, from the notes]:
- Variety has to come from the prompt (verbalized sampling) and from selection among candidates. Anthropic documents the same substitute: "If the caller previously relied on `temperature` for design variety, use approach (2) - it produces meaningfully different directions across runs".
- Phrase bans run after the fact (find the hits, rewrite the sentence), since Antislop's API mode needs `top_logprobs` and a draft cannot be resumed without prefill. On Claude, "continue the author's opening" goes in the user turn.
- Surprisal statistics need a local scorer model. Keep penalties low where they exist, and never use temperature or penalties to "humanize": their documented effect is on detector scores (RAID: up to 32 points), with no shown gain in quality.
- Choose the drafting model with the watermark in mind. On Claude the EU-required mark arrives with the text, so the simplest compliant design keeps every word Claude-chosen and documents reliance on that mark. A rewriting stage on a model that does not mark weakens the upstream mark and is itself in-scope rewriting under the Commission's guidelines; an open-weights voice model or an Antislop-style sampler has to carry the product's own mark for EU users, because the Code says logging alone is "not considered sufficient"; the OpenAI API needs marking switched on; Gemini API coverage is unstated. The strongest quality lever (per-author fine-tuning, section 5) and this compliance shortcut pull against each other, so make the choice deliberately (`research-root-causes-and-fixes.md`, the section on the law).

## 2. The workflow as calls

Each SKILL.md step is its own call or script with a fixed input and output, and every check runs outside the drafting model.

| Step | Call | Input | Output |
|---|---|---|---|
| 1. Who, for whom, what for | Brief | customer brief, author profile | author, reader, purpose, a claim a reader could disagree with |
| 2. Information gain | Inventory | brief, customer files, interview answers | first-hand items, each tagged with its source; three to five questions if someone can answer, `[NEEDS: ...]` entries if no one can |
| 3. Consensus | Consensus map, kept private | topic; optionally the top results | default angle, stock examples, usual outline, stock metaphor; the points the author can add to |
| 4. Diverge | Verbalized sampling | steps 1–3 | four or five options with probabilities; the most probable one or two dropped; the best remaining option the inventory supports |
| 5. Voice | Habit extraction, cached per author | about five consented samples, same genre, chosen for style | recurring words, stances, references, openings, closings, punctuation, what the author never says; their opening line if any |
| 6. Draft | Two or three drafting calls, then selection (section 4) | spec, inventory, chosen option, habits, prose rules; extracted facts in place of the source documents | one draft; an outline first for long pieces |
| 7. Repair | Span detection, span rewrite, `scripts/check.py` | draft, seven categories, ban-list hits, expert-edit examples | rewritten spans only; `check.py --json` numbers |
| 8. Verify | Claim trace, originality checks | draft, inventory, sources, archive | every figure, name and quote traced or turned into `[NEEDS: ...]`; overlap numbers |
| 9. Deliver | Delivery note | final piece, inventory, destination | the piece alone, plus the four-part note in SKILL.md step 9 |

**Step 4, verbalized sampling.** The published template asks for k candidates with verbalized probabilities: five `<response>` items, each holding a `<text>` and a `<probability>`, optionally "such that the probability of each response is less than 0.10" ([Zhang et al.](https://arxiv.org/html/2510.01171v3); exact wording in the [code](https://github.com/CHATS-lab/verbalized-sampling)). A skeleton:

```text
Propose 5 different <angles | openings | structures> for the piece below.
Return 5 <response> items: the option in <text>, and in <probability>
how likely a typical writer would be to choose it.
[optional] Keep the probability of each response below 0.10.
Brief: {step 1}   Material: {step 2}   What every article says: {step 3}
```

The customer can make the final choice. On creative writing (100 prompts per task), semantic diversity rose 1.6–2.1x, and human ratings on a 1–4 scale went 1.90 → 2.39 for poems and 2.74 → 3.06 for stories. Quality falls as k grows, and marketing genres are untested.

**Step 7, the repair pass** ([Chakrabarty, Laban & Wu, CHI 2025](https://arxiv.org/html/2409.14509v5)):
1. Detect. In: the draft, the seven categories, regex ban-list hits, about five annotated examples (gains plateau after 5 shots). Out: spans with categories. Precision of 0.46, against 0.57 agreement between experts, is enough: rewrites of writer-chosen and model-chosen spans ranked the same (1.99), so "detection of problematic spans is not the bottleneck".
2. Rewrite. In: the marked draft, the inventory, the habits, few-shot expert edits (LAMP, github.com/salesforce/creativity_eval). Out: replacement text for each span, meaning kept, the rest untouched. Experts ranked writer-edited text 1.50, model-edited 1.99 and unedited 2.51, so the pass closes about half the gap.
3. Mirror. `python scripts/check.py draft.md --source <files or folder> --json`, then one fix of what it flags.

Optional: 20 candidate edits of the draft, scored by an edit-trained writing-quality reward model (WQRM), with any below the draft discarded; experts preferred the top-scored edit 66% of the time ([Chakrabarty et al., COLM 2025](https://arxiv.org/html/2504.07532v3)). Never loop: self-refinement without external feedback raised fluency and each model's bias toward its own text ([Xu et al., ACL 2024](https://aclanthology.org/2024.acl-long.826)), and iterated rewriting drifts toward model-specific attractors ([Perez et al.](https://arxiv.org/html/2407.04503v2)) [LIMITED]. LAMP is about 80% literary fiction; gains on blogs, LinkedIn and email are unmeasured.

## 3. Levers ranked by evidence

Adapted from the fixes notes, whose ordering is a synthesis [HYPOTHESIS]: row 1 leads as the cheap lever that adds information the model lacks, rows 2–5 have the most direct peer-reviewed evidence, and row 6 has the largest effect on the thinnest evidence.

| # | Lever | Evidence | Best measured effect | Cost | Commercial APIs |
|---|---|---|---|---|---|
| 1 | First-hand content (step 2) | mechanism established; detector effect [LIMITED] | content-anchored detector TPR 59.6–63.5% → 5.8%; human key points not homogenised | none | yes, with customer input |
| 2 | Detect-then-rewrite, seven categories (step 7) | CHI 2025 | expert rank 2.51 → 1.99 (writer edits 1.50) | low | yes |
| 3 | Best-of-N edits reranked by WQRM | COLM 2025 | selected edit preferred 66% (72.2% at gap > 1) | N × edit tokens (N = 20) | drafting yes; scorer runs locally |
| 4 | Verbalized sampling (step 4) | ICML 2026; Anthropic's guidance | 1.6–2.1x diversity; human ratings +25.7% | small at k ≤ 5 | yes |
| 5 | About five style-matched samples, completion format (step 5) | EMNLP Findings 2025 | verified as the author: email/news 95–97%, blogs 17–21% | low | yes |
| 6 | Per-author fine-tune | [LIMITED]: one preprint | expert style OR 0.16 → 8.16 | ~$25–276 per author | hard: OpenAI closed to new users |
| 7 | Model-specific slop bans | [LIMITED]: preprint, LLM judges only | 90% slop reduction, about no quality loss (FTPO) | sampler throughput −69% to −96% | rewrite pass only |
| 8 | Plan or research before long drafts | established for organisation | +25% organised, +10% coverage (STORM) | more calls | yes |
| 9 | Humanlike persona prompt | [LIMITED]: chat Turing test | judged human 36% → 73% (GPT-4.5) | none | yes |
| 10 | Base-model draft, instruct revision | [LIMITED] | base wins originality 4/4, loses pleasantness | lower fluency | open weights only |
| 11 | Expert human edit on flagship pieces | CHI 2025, NAACL 2025 | writer-edited ranked first 65% | human time | service add-on |

Weak or counter-productive: temperature, min-p and typical sampling (weak evidence, and removed or ignored on current Claude, GPT-6 above effort `none` and Gemini 3.6 Flash+; see the temperature myth in `root-causes.md`); open-ended self-refinement; generic DPO toward "human text" (Antislop: writing quality 67.8 → 54.6, diversity 100 → 73.9 at 8k pairs; people spotted Llama-DPO text more often, 0.52 → 0.70); token bans past about 2,000 patterns; paraphrase through a second model.

Against-detector family (measured, not recommended): RL with a detector's score as reward (Llama-2-7B: AUROC 0.84 → 0.63 at perplexity 8.7 → 9.0; [Nicks et al., ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/hash/1f9f07df0992ce21698d800eaa891bd8-Abstract-Conference.html)); DPO with human text as "chosen" (detectors lose 5–35 points; fluency never assessed; [Pedrotti et al. 2025](https://arxiv.org/html/2505.24523v1)); tuning against Fast-DetectGPT (0.72 → 0.18), which leaves a stylometric detector at 0.95 ([Rivera Soto et al.](https://arxiv.org/html/2505.14608v2)) [LIMITED]; detector-guided paraphrasers; repetition penalties and high temperature; commercial humanizers (one pushed GPTZero's false-negative rate to about 0.5 while Pangram held, [Jabarian & Imas, NBER 2025](https://www.nber.org/papers/w34223) [LIMITED]). Each buys a lower score on some detector with no shown gain in quality; section 6's ship rule rejects such changes.

## 4. Choosing among candidates and keeping customers' outputs distinct

**Selection.** Score candidates only with measures the drafting model does not control:
- WQRM, a ModernBERT-Large scorer trained on edit-derived preferences, agreed with experts 74.3% of the time on a 4,729-pair benchmark, against GPT-4o zero-shot 40.9%, o3 64.3% and Pangram used as a quality proxy 65.0% ([Chakrabarty et al., COLM 2025](https://arxiv.org/html/2504.07532v3)). Experts agree with it only 55% of the time at score gaps ≤ 0.5, so treat those as ties. Weights are said to be at github.com/salesforce/creativity_eval; it is weaker outside fiction-like text.
- StyleDistance cosine to the author's held-out samples, similarity to earlier outputs, the mirror's flags, and the count of inventory items used. A model may answer narrow, checkable questions ("does paragraph 3 contain a concrete example?").

Never select with the drafting model's own judgment, which favours its own and lower-perplexity text (section 6), or with a detector score, which is the against-detector family and moves whenever the detector retrains.

**Distinct outputs.** AI help raises individual quality and shrinks collective diversity: with five GPT-4 ideas, stories gained 8.1% in novelty and grew more alike ([Doshi & Hauser 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532)). Check every piece against the archive:
- Small archives: `python scripts/check.py draft.md --source outputs/ --json` reads every .md and .txt file under the folder and reports, per file, `longest_run` (the longest shared verbatim run in words; 0 below `--ngram`, default 8) and `jaccard3` (3-word-sequence similarity). It compares against every file, so its cost grows with the archive.
- At scale: `datasketch` `MinHashLSH(threshold=..., num_perm=...)` over word 5-gram shingles of every delivered piece. LSH returns false positives and negatives, so confirm each candidate with `MinHash.jaccard`; Redis or Cassandra holds a large index ([datasketch](https://ekzhu.com/datasketch/lsh.html)). Calibrate the threshold on same-genre human pairs.
- The same article in different words passes both checks, since model text is mostly novel at short n-gram lengths. Compare outlines by embedding similarity with earlier outlines on the topic and with a generic outline from the same brief, and reject above a threshold calibrated on the author's corpus, starting from Hivemind's 0.8 [HYPOTHESIS].
- Web overlap: query infini-gram (`https://api.infini-gram.io/`, index `v4_rpj_llama_s4` or `v4_dolma-v1_7_llama`, `query_type: "count"`) for each output's 5-grams through 12-grams, compare the zero-count share at each n with genre-matched human texts, and review any verbatim match of 50 tokens or more ([infini-gram docs](https://infini-gram.readthedocs.io/en/latest/api.html)). There is no uptime guarantee, so retry; heavy use may need self-hosting.

**Per-model slop profile.** Profile the product's own outputs against genre-matched human text with ρ(p) = f_LLM(p) / f_human(p) for words, bigrams and trigrams, add regexes such as "It's not X, it's Y", and send the hits to the repair pass. Re-profile whenever the underlying model changes: profiles differ between families, and some entries are absurdly model-specific ("elara" at 85,513x in gemma-3-12b) ([Antislop](https://arxiv.org/html/2510.15061v2)) [LIMITED]. Add the family checks in `root-causes.md` (R10).

## 5. Voice profiles

**Samples.** About five of the same genre, chosen for style. Across 400+ authors and six models, five-shot imitations passed authorship verification as the author 94.7–97.5% of the time for news and 95.7–96.6% for email, but 16.7–21.3% for blogs; going from 2 to 10 samples changed the metrics "very little"; topic-similar samples cut attribution ([Wang et al. 2025](https://arxiv.org/html/2509.14543v1)). The notes differ on the count (3–10 in the root-cause notes, about five in the fixes notes); the measured curve is flat from 2 to 10. Continuing the author's own text matched style best (99.9% agreement) yet left perplexity at 15.2 against 29.5 for the humans ([Jemama & Kumar 2025](https://arxiv.org/abs/2509.24930v1)) [LIMITED], so extract habits and let first-hand material carry the piece. Keep the author's English: with GPT-4o suggestions, a classifier separating Indian from American writers fell from 90.6% to 83.5%, and Diwali and biryani essays turned "more generic" ([Agarwal, Naaman & Vashistha, CHI 2025](https://arxiv.org/html/2409.11360v3)).

**Per-author fine-tuning, the strongest single lever.** Fine-tuning GPT-4o on each of 30 living authors' complete works moved MFA-trained readers from a style odds ratio of 0.16 (95% CI 0.08–0.29) for in-context prompting to 8.16 (4.69–14.2), and quality from 0.13 to 1.87; 27 of 30 tuned authors beat parity on style; Pangram flagged 97% of in-context outputs and 3% of tuned ones; cost $25–$276 per author, median $81 ([Chakrabarty, Ginsburg & Dhillon](https://arxiv.org/html/2510.13939v3)) [LIMITED]. Caveats: one preprint with no confirmed venue and reader counts that differ across versions; novelists' whole bodies of work, where customers have far less; untested on open models, non-fiction and less than a book of text. OpenAI's tuning platform is closed to new users, so the route is open weights or Vertex AI's Gemini tuning, per-model support unverified ([Vertex tuning](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/tune-models); [OpenAI](https://r.jina.ai/https://platform.openai.com/docs/guides/model-optimization)). Sell the style and quality result; the lower detector rate is a side effect.

**Consent and data.**
- India's DPDP Act and Rules: core duties apply from about 13–14 May 2027 ([commencement](https://www.meity.gov.in/static/uploads/2025/11/c56ceae6c383460ca69577428d36828b.pdf)). Treat samples and profiles as personal data [HYPOTHESIS]: an itemised notice naming the voice profile as a specified purpose (Rule 3); withdrawal as easy as consent, deleting samples and profile; separate consent for any model training; Rule 6 safeguards (encryption, access control, logs kept one year); breach notice to the Board "within seventy-two hours" (Rule 7); "verifiable consent of the parent" for children (Rule 10) ([DPDP Rules](https://www.meity.gov.in/static/uploads/2025/11/53450e6e5dc0bfa85ebd78686cadad39.pdf)). Penalties reach ₹250 crore for failed security safeguards ([PIB](https://static.pib.gov.in/WriteReadData/specificdocs/documents/2025/nov/doc20251117695301.pdf)).
- Isolate each account's samples and profile, with no pooling across customers.
- Apple apps "must clearly disclose where personal data will be shared with third parties, including with third-party AI, and obtain explicit permission before doing so" (5.1.2(i)), and "AI content creation apps" need filtering, reporting, blocking and published contact details (1.2) ([guidelines](https://developer.apple.com/app-store/review/guidelines/), last updated October 16, 2026).
- GDPR was not researched; EU customers' samples need a lawyer.

## 6. Measuring quality honestly

1. Quality as experts judge it: a blind panel of three to five people who write professionally and use LLMs often, ranking 60 triplets per genre (baseline, current system, a human piece on a matched brief) by quality and labelling each human or AI. Five such experts by majority vote misclassified 1 of 300 articles (99.3% TPR at 0% FPR); individuals averaged 92.7% TPR at 4.0% FPR, non-experts 56.7% at 51.7% ([Russell, Karpinska & Iyyer 2025](https://arxiv.org/abs/2501.15654)) [LIMITED]. WQRM scores every output between panels.
2. Voice: StyleDistance cosine to the author's held-out samples ([model card](https://huggingface.co/StyleDistance/styledistance), MIT) [LIMITED], normalised between other authors (floor) and the author's held-out samples against each other (ceiling). People match their own style model only 69.1–81.9% of the time [LIMITED], and no "same author" threshold has been validated for 300–1,500-word marketing texts.
3. Originality and diversity: compression ratio, long-n-gram self-repetition and Self-BLEU (`pip install diversity`) plus mean pairwise embedding cosine over 10 samples per brief, and the archive and web checks in section 4.

Customers see these results, the share of specifics they supplied and the open `[NEEDS: ...]` items (section 8).

**Ship rule.** On 60 real briefs per genre, run the notes' ablation ladder: a single prompt, then adding first-hand inputs, five samples, verbalized planning, the repair pass with ban list, and 5–10 candidates with external selection. Ship a change only if expert preference is non-inferior and WQRM, voice match and within-brief diversity do not drop; reject any change whose only gain is a lower detector score.

**Why LLM judges fail.** General LLM judges sat near chance on the section 4 benchmark (o1 51.7%). LLMs chose GPT-4-written product descriptions 89% of the time where people chose them 36%, and picked the first option shown 73.18% of the time (Llama-3.1-70B-Instruct) ([Laurito et al., PNAS 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12337326/)); self-recognition rises with self-preference ([Panickssery et al. 2024](https://papers.nips.cc/paper_files/paper/2024/hash/7f1f0218e45f5414c79c0679633e47bc-Abstract-Conference.html)); judges favour lower-perplexity text ([Wataoka et al.](https://arxiv.org/abs/2410.21819)) [LIMITED]; and judges correlate worst with people where annotators disagree ([Hivemind](https://arxiv.org/html/2510.22954)) [LIMITED]. Keep them to narrow, checkable questions.

**Detectors: informational, version-dated.** If you report them at all, use an ensemble (a RAID-trained encoder, a classifier trained elsewhere, a zero-shot statistic), each calibrated at 1% and 5% FPR on same-genre human text (RAID's human rows plus 200 or more texts per genre you control, used with permission). Report TPR with Wilson 95% intervals per detector, never averaged into one "AI %" or read at a default 0.5 threshold; use the single-prompt baseline as the positive control; date each result with detector, version and generating model, and recalibrate when either changes. RAID's near-perfect leaderboard scores come from 2023-era generators and say almost nothing about 2025–26 models. Avoid the non-commercial licences (`Lindarixon/Linda-RAID`, `TrustSafeAI/RADAR-Vicuna-7B`) ([RAID submissions](https://github.com/liamdugan/raid/tree/main/leaderboard/submissions)).

## 7. Legal and platform rules

Research notes, not legal advice.

**The product may:**
- Draft, edit and personalise in the customer's voice (blogs, marketing copy, emails, LinkedIn posts, essays where AI help is permitted), and ghostwrite for an account owner who approves and posts. No vendor bans text that reads as human; they ban deception, plagiarism and academic dishonesty.
- Offer disclosure helpers (KDP, Medium, journal declarations, an EU Art. 50(4) label) and, for public-interest posts, an editorial workflow: a named responsible editor, substantive review with fact-checking, no AI edits after sign-off. The EU exception requires this: "Fact-checking the accuracy of the content is a minimum requirement", and AI intervention after the review voids it ([Article 50 Guidelines](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2026-07/guidelines_on_the_implementation_of_the_transparency_obligations_for_certain_ai_systems_under_article_50_of_the_ai_act_bzptwqhk0ikg1dtlddap41psfy_131215.pdf)).

On Claude, the vendor terms add two duties: notify users "that factual assertions in Outputs should not be relied upon" ([Commercial Terms](https://www.anthropic.com/legal/commercial-terms)), and disclose AI in any consumer-facing chat ([Usage Policy](https://www.anthropic.com/legal/aup)).

**It must not do or claim:**
- Features or marketing such as "bypass Turnitin/GPTZero", "undetectable" or "submit as your own". Anthropic's policy (effective Nov 12, 2026) bars using Claude to "Plagiarize or submit AI-assisted work without proper permission or attribution" or to "circumvent the guardrails or terms of other platforms or services"; OpenAI's (effective November 20, 2026) bars "academic dishonesty" ([Usage Policies](https://openai.com/policies/usage-policies/)); Google Ads bans "essay or thesis generators" ([policy](https://support.google.com/adspolicy/answer/6016086?hl=en)); such claims are the strongest evidence of knowledge under cheating statutes; and efficacy claims need "competent and reliable evidence" when made ([FTC, Workado](https://www.ftc.gov/news-events/news/press-releases/2025/04/ftc-order-requires-workado-back-artificial-intelligence-detection-claims)).
- Fake reviews, testimonials, sockpuppets or bots that claim to be human ([16 CFR §465.2](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-D/part-465)); impersonating a real person without disclosure.
- Output presented as human-made: OpenAI's consumer terms forbid "Represent that Output was human-generated when it was not."; Google forbids "claiming it was created solely by a human, in order to deceive" ([Prohibited Use Policy](https://policies.google.com/terms/generative-ai/use-policy)).
- Watermark or label removal. A stage that rewrites Claude's text with a non-marking model weakens the mark and is itself "paraphrasing or rewriting text that changes style, structure and meaning", which needs marking in the EU [HYPOTHESIS]: keep every word-writing stage on a marking model, or mark again.
- A student-facing product on the Gemini API, whose terms bar clients "likely to be accessed by individuals under the age of 18" ([Gemini API terms](https://ai.google.dev/gemini-api/terms)).

**Platforms.** Google Search treats "Scaled content abuse" as spam "no matter how it's created", naming "Using generative AI tools or other similar tools to generate many pages without adding value for users" ([spam policies](https://developers.google.com/search/docs/essentials/spam-policies)). KDP requires disclosing AI-generated text "even if you applied substantial edits afterwards" ([KDP](https://kdp.amazon.com/en_US/help/topic/G200672390)). On Medium, "Undisclosed AI-generated writing will be given Network Only distribution" ([Medium](https://help.medium.com/hc/en-us/articles/22576852947223)); journals require disclosure ([COPE](https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools)). Google Play bars apps that help users deceive others ([Play](https://support.google.com/googleplay/android-developer/answer/9888077?hl=en)), and Stripe bars businesses that "make outrageous claims" ([Stripe](https://stripe.com/legal/restricted-businesses)).

| Market | Must do | Must not do or claim | Provisions and status |
|---|---|---|---|
| EU | Mark every text output machine-readably; document reliance on the upstream mark (Guidelines para. 74); treat style rewriting and summaries as generation; offer a label and a qualifying review workflow | Strip or degrade marks; as a Code signatory, promote circumvention tools | [AI Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng) Art. 50(2), (4), (5); [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng); [Code of Practice](https://ec.europa.eu/newsroom/dae/redirection/document/129555). In force 2 Aug 2026; systems already on the market by 2 Dec 2026; fines up to EUR 15M or 3%, the lower for SMEs |
| India | Text only: no labelling duty today. Image, audio or video: visible label, permanent metadata with a unique identifier. DPDP design (section 5) | Enable removal of media labels (Rule 3(3)(b)); exaggerated accuracy claims (CCPA guidelines [LIMITED]); theses written for submission | [IT Rules as amended](https://www.meity.gov.in/static/uploads/2026/02/550681ab908f8afb135b0ad42816a1c9.pdf), in force 20 Feb 2026; DPDP core from about May 2027; [UGC 2018](https://www.ugc.gov.in/pdfnews/7771545_academic-integrity-Regulation2018.pdf) |
| US | Hold evidence for every performance claim when it is made; refuse review and testimonial generation | Essays for credit ([CA §66400](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=EDC&sectionNum=66400); [NY §213-b](https://www.nysenate.gov/legislation/laws/EDN/213-B), class B misdemeanor); fake reviews | FTC Act s.5; Rytr order set aside 22 Dec 2025 ([FTC](https://www.ftc.gov/news-events/news/press-releases/2025/12/ftc-reopens-sets-aside-rytr-final-order-response-trump-administrations-ai-action-plan)); California's AI Transparency Act excludes text [LIMITED] |
| UK (England) | Professional positioning; in academic settings, "permitted assistance" only | Paid completion of post-16 assignments; advertising to students; a "not for submission" term is not, of itself, sufficient evidence (s.27(5)); directors exposed (s.29) | [Skills and Post-16 Education Act 2022](https://www.legislation.gov.uk/ukpga/2022/21/section/27/enacted) ss.26–30; no prosecutions found |
| Australia | Block requests for students' assessment work | Strict liability on the "assessment task" circumstance; 2 years or 500 penalty units; advertising offence | [TEQSA Act](https://legislation.gov.au/C2020A00078/asmade/2020-09-03/text/original/pdf) ss.114A, 114B; 615 blocked domains, four on ".ai" essay-writer domains (service type unchecked) |
| Ireland, New Zealand | As for England | Providing or advertising cheating services: Ireland up to €100,000 and/or five years; New Zealand up to NZD 10,000 [LIMITED] | [QQI Act s.43A](https://revisedacts.lawreform.ie/eli/2012/act/28/section/43A/revised/en/html); [NZ s.393](https://www.nzlii.org/nz/legis/consol_act/eata2020204/s393.html) |
| China | Visible and metadata labels, or unlabelled output only under a user agreement shifting the duty, with six-month logs | Tools to delete, alter, forge or conceal labels; ghostwritten theses (degree withheld or revoked) | [CAC Measures](https://www.cac.gov.cn/2025-03/14/c_1743654684782215.htm), in force 1 Sep 2025; separate filing (not researched) |
| South Korea | Notice before use that the service runs on generative AI; for drafting tools, a UI logo; exported files labelled in header or metadata | (third-party removal not currently penalised) | AI Basic Act Art. 31, in force 22 Jan 2026 ([Shin & Kim](https://shinkim.com/eng/media/newsletter/3190)) [LIMITED] |

**Where the notes disagree.** The market notes say the Code requires providers' terms to forbid removing markings; the legal notes, from the Code's text, say the required terms clause covers metadata markings only, while the ban on offering circumvention tools covers all marks and binds only signatories. The market notes date the final Workado order 28 Aug 2025 (3–0, [FTC](https://www.ftc.gov/node/297697)); the legal notes report it finalised around late October 2025, from local news. The market notes put the cheating-advertising offence in England and Wales; the statute the legal notes read covers England.

**Open points for a lawyer:** whether an India-incorporated SaaS selling to EU customers is a provider for every EU user, and whether signing the Code is worth its duties; whether a general-purpose assistant that does not target students can still fall within England s.27 or TEQSA s.114A; whether MeitY can treat an AI writing SaaS as an intermediary; output-ownership and indemnity wording, given that vendors assign rights only "if any"; GDPR for voice samples.

## 8. What to promise customers

Promise what can be shown:
- The piece uses their material, says where each specific came from, invents nothing, and marks gaps as `[NEEDS: ...]`.
- Their voice, measured against their own samples; no competitor in the notes measures it.
- Meaning preserved and readable prose: customers praise "The meaning is preserved" [LIMITED], and since fluent output is what Pangram catches most [VENDOR CLAIM], readability is worth having for its own sake.
- Originality as a dated comparison, such as "No 8-word match against the three sources and 40 earlier outputs, checked today".- Disclosure and provenance support: an editorial log for the EU review exception, declaration text, a process record.
- Rights: "we assign to you all rights we have, and claim none", with the note that the customer's own edits, selection and arrangement create authorship (lawyer needed for the wording).
- Monthly billing with a working cancel button: charges after cancellation and trials that convert to annual plans fill this market's one-star reviews [LIMITED].

Never promise:
- "Undetectable", "bypass Turnitin/GPTZero/Pangram", "0% AI", "100% human score" or "guaranteed": Turnitin and Pangram train on humanizer output, and results conflict by tester and version.
- Refunds if a detector flags the text.
- Watermark removal, or "watermark and future-proof".
- "You own 100% of the copyright": "Copyright does not extend to purely AI-generated material" ([USCO Part 2](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf)), and Thaler is final since cert was denied on 2 Mar 2026.
- "100% original", or uniqueness that is exclusive and legally protected.
