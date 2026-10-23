# Root causes: mechanisms, evidence, durability

The evidence behind the cause table in SKILL.md: for each of the ten causes, the mechanism, the tells, the measurements with their conditions and sources, its durability and the workflow's answer; then a tell-to-cause lookup, the myths and the open questions. Untagged findings are peer-reviewed or replicated. Weaker evidence keeps the research notes' tags: [LIMITED] (one study, small sample, preprint or narrow conditions), [VENDOR CLAIM] (a company on its own product; [BENCHMARK CLAIM] for a leaderboard), [HYPOTHESIS] (an inference), [UNKNOWN] (looked for, not found).

Verified against research through 23 October 2026.

## R1. Decoding stays in the probability head

**Mechanism.** Maximum-likelihood pretraining learns a good average of human text, and every practical decoder (greedy, beam, low temperature, top-k, top-p) cuts off the low-probability tail to avoid incoherence. Tokens therefore come from the head: average surprise is low, and because nothing comes from the tail, its variance is low too. Post-training sharpens the distribution further, so a chat model at temperature 1 already behaves like a cooled base model.

**Tells.** Low, even surprisal (GPTZero's original "low burstiness"); the expected phrasing every time; fewer novel n-grams beyond four words; repeated part-of-speech templates.

**Evidence.**
- GPT-2 Large on WebText (5,000 continuations of up to 200 tokens per method), perplexity / Self-BLEU4: human 12.38 / 0.31, greedy 1.50 / 0.50, nucleus p=0.95 13.13 / 0.32, pure sampling 22.73 / 0.28. The harder the truncation, the lower the perplexity and the more alike the outputs ([Holtzman et al. 2020](https://ar5iv.labs.arxiv.org/html/1904.09751)). Top-k (k=40) "concentrates up to 80% of its mass in the first 500 most common tokens" ([Ippolito et al. 2020](https://arxiv.org/abs/1911.00650)).
- Under a GPT2-XL observer, "the UID scores of human-written text have a higher mean and larger standard deviation than most machine-written text"; the generators tested are older ([GPT-who 2024](https://arxiv.org/html/2310.06202)).
- On Pythia models with the Pile indexed, "for n > 4, LM-generated text is less novel than human-written text", and larger models and more constrained decoding lower novelty further ([Merrill et al. 2024](https://arxiv.org/abs/2406.13069)). About 95% of model summaries repeat part-of-speech 6-gram templates against about 38% of human references; 76% of those templates occur in pretraining data, and they survive alignment ([Shaib et al. 2024](https://arxiv.org/html/2407.00211v2)).
- Token entropy on human text falls from 1.616 in Llama-2 base to 1.051 in Llama-2 chat ([Juzek & Ward 2025](https://arxiv.org/html/2412.11385v1)).

**Durability.** High: inherent to sampling. Nobody has measured surprisal mean and variance for 2025–26 frontier chat models against matched human text.

**What the skill does.** Steps 2 and 4: real specifics in context, then several options and a selection; temperature is left alone. The notes' reasoning [HYPOTHESIS]: most human surprisal spikes carry information (a name, an exact number, a local idiom, a quote) that a truncated decoder cannot reach by chance. Supplied in context, they stay coherent and still surprise the reader; higher temperature puts spikes in the wrong places.

## R2. Preference tuning rewards the typical

**Mechanism.** Annotators systematically favour familiar text (the authors cite mere exposure, availability, processing fluency and schema congruity). With reward r(x,y) = r_true(x,y) + α·log π_ref(y|x) + ε, the KL-regularized RLHF optimum is π* ∝ π_ref^γ · exp(r_true/β) with γ = 1 + α/β > 1. Among equally good answers this "behaves like temperature scaling" toward the most typical, and biased preference data alone can drive collapse "even with a perfect reward model and optimization process".

**Tells.** One answer per prompt; one default angle, outline and metaphor for everyone.

**Evidence.**
- α on HelpSteer (6,874 correctness-matched pairs): 0.57 ± 0.07 with Llama-3.1-405B base as the typicality scorer, 0.65 ± 0.07 with GLM-4.5 (p < 10⁻¹⁴). On human-only preference data, raters picked the response the base model found more probable 51.6–60.8% of the time, and the effect stays significant with length, readability, type-token ratio and sentence length controlled. On Tulu-70B, direct-prompt diversity falls from 45.4% (base) to 20.8% (SFT) to 10.8% (DPO) ([Zhang et al.](https://arxiv.org/html/2510.01171)). The notes grade this paper differently: [LIMITED] in the root-cause notes, peer-reviewed in the fixes notes, which cite its ICML 2026 version ([PMLR](https://proceedings.mlr.press/v306/zhang26hy.html)).
- One model, 100 queries, 50 samples each at top-p 0.9 and temperature 1.0, embedded with text-embedding-3-small: "in 79% of cases, the average similarity exceeds 0.8" ([Artificial Hivemind](https://arxiv.org/html/2510.22954)) [LIMITED: one study].
- RLHF "significantly reduces output diversity compared to SFT" per input (LLaMa 7B on TL;DR, 16 samples on each of 500 inputs) ([Kirk et al. 2024](https://arxiv.org/html/2310.06452v3)), and alignment cuts the Creativity Index by an average of 30.1% ([Lu et al. 2025](https://arxiv.org/abs/2410.04265)).
- Qualifications: part of the drop is aggregation into longer, fuller answers ([Lake et al. 2025](https://arxiv.org/abs/2406.17692)), and "More target data moves model diversity toward the human (or synthetic target) level in all experiments" ([Skobelev et al., Sept 2026](https://arxiv.org/abs/2609.16454)) [LIMITED]. The fault lies in the objective and the preference data.

**Durability.** High while preference data favour the typical. [HYPOTHESIS] R2 multiplies the other causes: a 52–60% per-comparison preference, raised to a power above one, can grow into 10–30x word ratios in corpora and >1,000x phrase ratios in creative writing.

**What the skill does.** Step 3 maps the consensus and leaves it; step 4 drops the one or two most typical of four or five directions (candidates with verbalized probabilities raised creative-writing diversity 1.6–2.1x). In a product, per-author training data goes further (`for-builders.md`, section 5).

## R3. Reward proxies: length, formatting, agreement, positivity, prestige words

**Mechanism.** Raters and reward models respond to measurable stand-ins for quality (length, formatting, agreement, confidence, positive sentiment, frequent and impressive words), and optimisation amplifies each one. Instruction tuning also builds the noun-heavy, participial, evaluative register that base models lack.

**Tells.** Previews, recaps, restated questions; headers, bold-label bullets, triads, emoji; "Great question" and praise; uniform confidence; upbeat endings; "delve", "nuanced", "pivotal"; participial tails, nominalizations, "serves as"; "not X but Y".

**Evidence.**
- Length alone goes far: "a purely length-based reward reproduces most downstream RLHF improvements over supervised fine-tuned models" ([Singhal et al. 2024](https://arxiv.org/abs/2310.03716)). Chatbot Arena style coefficients: answer length 0.249, markdown lists 0.031, headers 0.024, bold 0.019 ([LMSYS, 29 Aug 2024](https://lmsys.org/blog/2024-08-28-style-control/)) [VENDOR/BENCHMARK CLAIM, very large n]. Preference models favour "lists, links, bold text, and emojis", and less than 1% biased data can bias a reward model ([Zhang et al. 2024](https://arxiv.org/abs/2409.11704)) [LIMITED: preprint]; the markdown skeleton alone identifies a chat model 73.1% of the time ([Sun et al. 2025](https://arxiv.org/html/2502.12150)) [LIMITED].
- Five assistants "consistently exhibit sycophancy across four varied free-form text-generation tasks" ([Sharma et al. 2024](https://arxiv.org/abs/2310.13548)); confident answers carry "an average of 47%" error, and preference data penalise stated uncertainty ([Zhou et al. 2024](https://arxiv.org/abs/2401.06730)); "RLHF improves sentiment towards all groups, but does not remove bias" ([Bai et al. 2022](https://arxiv.org/html/2204.05862)); reward models overvalue frequent tokens ([Christian et al. 2025](https://arxiv.org/abs/2506.07326)).
- ChatGPT-3.5 wrote "delves" 183.17 times per million words against 3.20 on arXiv, which rules out pretraining frequency ([Juzek & Ward, COLING 2025](https://arxiv.org/html/2412.11385v1)). Llama 3.2-3B Instruct uses "nuanced" 8342% more than its base, and 400 Prolific raters (4,039 ratings kept) preferred the variant dense in LLM-associated words 52.4% vs 47.6% (χ² = 9.4, p < 0.01) ([Juzek & Ward, BIAS 2025](https://arxiv.org/html/2508.01930v1)) [LIMITED: small effect, Llama only].
- Present participial clauses run at 527% of the human rate in GPT-4o, 224–261% in Llama 3 Instruct and 94–102% in Llama base; nominalizations at ~209–214% in GPT models against 88–91% in base ([Reinhart et al., PNAS 2025](https://arxiv.org/html/2410.16107v1)).
- Between Llama-2-7b and its chat version, 77.7% of token positions keep the base model's top choice, and "Most distribution shifts occur with stylistic tokens" ('However', 'Here (are some)', 'Great (question)'), mostly at the start ([URIAL](https://arxiv.org/html/2312.01552)) [LIMITED: Llama-2 era].
- "Not X but Y" overshoots the human rate about twofold in oratory, undershoots in informal Q&A and matches people in argument, journalism and encyclopedic prose; its attribution to preference tuning is inferential ([Boggia, July 2026](https://arxiv.org/abs/2607.21498)) [LIMITED].

**Durability.** Medium: patched version by version, but the register outlasts any single word (see the R10 ranking), and contrastive framing has lasted into 2026.

**What the skill does.** The prose rules, applied while drafting (step 6) and checked once (step 7): genre-normal length and format; no previews, recaps or default triads; an opening with substance, since alignment works hardest on the first tokens; a stance with specific uncertainty; plain verbs; earned evaluations; no flattery; bad news allowed.

## R4. Safety and balance defaults

**Mechanism.** Harmlessness training, published specifications and character training set defaults for balance, reticence and caveats. Claude's character training has it rank its own responses against traits such as "I like to try to see things from many different perspectives" ([Anthropic, June 2024](https://www.anthropic.com/research/claude-character)) [VENDOR CLAIM].

**Tells.** "On the other hand" by reflex; disclaimers; moralizing; dark topics avoided.

**Evidence.** OpenAI's Model Spec (8 May 2024) said the assistant should "acknowledge and describe significant perspectives" on multi-viewpoint topics ([Model Spec](https://cdn.openai.com/spec/model-spec-2024-05-08.html)) [VENDOR CLAIM]. Anthropic's constitution (January 2026) counts it a failure when a response "Adds excessive warnings, disclaimers, or caveats that aren't necessary or useful" or "Lectures or moralizes about topics when the person hasn't asked for ethical guidance", and still asks for "norms of professional reticence" on hot-button issues ([constitution](https://www.anthropic.com/constitution)) [VENDOR CLAIM]. "An excessive focus on avoiding harm can lead to 'safe' responses that don't actually address the needs of the human" ([Bai et al. 2022](https://arxiv.org/html/2204.05862)).

**Durability.** Medium: it follows policy, and the providers' own specifications now reject much of it.

**What the skill does.** Step 1 requires a claim a reader could disagree with. The prose rules ask for the author's view with its reason, uncertainty in specific terms, the opposing view only where the author would give it, and caveats only where they carry information, such as the human sign-off step 9 requires for health, finance, law, politics and public safety.

## R5. Shared and synthetic training data

**Mechanism.** One model's outputs become another's training data: Stanford Alpaca learned from 52K demonstrations generated with text-davinci-003 ([Stanford CRFM](https://crfm.stanford.edu/2023/03/13/alpaca.html)), and UltraChat's 1.5 million dialogues "do not involve human queries" ([UltraChat](https://arxiv.org/abs/2305.14233)). Preference data are probably shared as well, so models from different vendors land on the same modes and carry each other's fingerprints.

**Tells.** Sameness across vendors; stock names and images (Elara, Elias, Mara, lighthouses, clockmakers); shared phrases ("unspoken", "flickered"); one model's text classified as another's.

**Evidence.**
- Between models, "the average pairwise similarity between responses from different models ranges from 71% to 82%"; qwen-max and qwen-plus produced the identical motto "Empower Your Journey: Unlock Success, Build Wealth, Transform Yourself"; across 25 models a metaphor for time collapsed into "time is a river" and "time is a weaver". The causes "remain unclear due to proprietary training details" ([Artificial Hivemind](https://arxiv.org/html/2510.22954)) [LIMITED].
- "11 words occur in 88.3% of generated stories, with little difference between models" (20,000 stories from four current models); they are rare in published literature and present in preference data "likely used by all current models" ([Hamilton & Mimno 2026](https://arxiv.org/abs/2605.26492)) [LIMITED: preprint].
- Fine-tuning on ChatGPT-generated UltraChat cut the separability of Llama and Gemma outputs from 96.5% to 59.8%, and Grok outputs were classified as ChatGPT 82.8% of the time ([Sun et al. 2025](https://arxiv.org/html/2502.12150)) [LIMITED]. Editors found "unspoken" in ~15% of responses from Claude 3.5 Sonnet, GPT-4o and Llama 3.1 70B alike ([Chakrabarty et al. 2025](https://arxiv.org/html/2409.14509)); "flickered" is on 98.5% of 67 models' slop lists ([Antislop](https://arxiv.org/html/2510.15061)) [LIMITED].

**Durability.** Rising with the share of synthetic data.

**What the skill does.** Names, places and images from the author's world; similarity checks against earlier outputs (step 8); no paraphrase through a second model, which leaves the first one identifiable and adds a second fingerprint.

## R6. Chat templates

**Mechanism.** Every chat request is wrapped in the same role and structure tokens, and those tokens narrow what the model produces whatever the question. The structural tokens "significantly constrain the model's output space", "diversity collapse persists even under high-temperature sampling", and minimal formatting gives the most diverse outputs ([Yun et al. 2025](https://arxiv.org/abs/2505.18949)) [LIMITED: preprint].

**Tells.** The same scaffold whatever the question; sameness that survives high temperature.

**Evidence.** That preprint is the only direct study. Format habits are cheap to instil: 1,000 curated examples taught LLaMa 65B to "follow specific response formats" ([LIMA](https://arxiv.org/abs/2305.11206)).

**Durability.** High in chat products.

**What the skill does.** Plain prose by default, minimal scaffolding, and format set by the genre's human norm.

## R7. No first-hand information

**Mechanism.** A model can only recombine its training data and its prompt, and its knowledge of a topic is the written consensus. Without the author's input it reproduces that consensus; pushed for specifics, it invents them.

**Tells.** Phrases like "many businesses" and "significant results"; few citations; no new data; invented clients, statistics, quotes and anecdotes.

**Evidence.**
- Measured as how much of a text can be rebuilt from verbatim and near-verbatim web snippets, "the CREATIVITY INDEX of professional human authors is on average 66.2% higher than that of LLMs" ([Lu et al. 2025](https://arxiv.org/abs/2410.04265)). "Lack of Specificity and Detail" is one of the seven categories professional editors fix ([Chakrabarty et al. 2025](https://arxiv.org/html/2409.14509)).
- In co-written essays the homogenisation came from the model's key points, and the writers' own points stayed diverse ([Padmakumar & He 2024](https://arxiv.org/html/2309.05196v3)). A content-anchored detector that caught 59.6–63.5% of fully AI-written reviews caught 5.8% (at 0.1% FPR) of GPT-4.1 reviews written from bullet points of real ones ([Yu et al. 2025](https://arxiv.org/html/2502.19614)) [LIMITED].
- Google asks "Does the content provide original information, reporting, research, or analysis?" and says "using generative AI to produce large amounts of text without manual oversight or curation represents little to no effort" ([Search Central, updated 2026-10-05](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)); its information-gain patent is not confirmed in live ranking ([US 11,354,342 B2](https://patents.google.com/patent/US11354342B2/en)).
- Copying is a separate, smaller risk: memorization "significantly grows" with model capacity, duplication of an example and tokens of context ([Carlini et al. 2023](https://arxiv.org/abs/2202.07646)).

**Durability.** Fundamental. [HYPOTHESIS] It is the binding constraint on originality: without new information in the inputs, a model with no surface tells still writes the consensus.

**What the skill does.** Step 2 (the inventory, three to five targeted questions, and `[NEEDS: what, and why it matters]` in place of any invention) and step 8 (every number, name and quote traced to its source); no famous text continued from its opening.

## R8. Web feedback loops

**Mechanism.** About half of new English articles are now primarily AI-written, SEO writers copy the top results, generative search cites predictable sources, and models retrain on generated text, which erodes the tails of the distribution unless real data keeps accumulating. Every article on a topic drifts toward the same article.

**Tells.** Pages for one query growing alike; homogenized search results; the same piece whoever commissions it.

**Evidence.**
- In 55.4k random English Common Crawl articles, the primarily AI-generated share was 35.9% about 12 months after ChatGPT's launch, 48% at 24 months and 49.9% in Q1 2026 (average of Pangram, Copyleaks and GPTZero; FPR 1.36–1.84% on pre-ChatGPT articles) ([Graphite, 15 May 2026](https://graphite.io/five-percent/ai-now-writes-as-many-online-articles-as-humans-do)) [VENDOR CLAIM].
- Scrapes for 388 keywords in 2019 and 2024 showed similarity rising (values unpublished): "Everybody tries to mimic the top 10 performers" ([UNSW BusinessThink](https://businessthink.unsw.edu.au/articles/ai-content-tools-seo-geo-search-visibility)) [LIMITED: secondary report]. Generative engines cite "content characterized by significantly higher predictability for underlying LLMs" ([Ma et al.](https://arxiv.org/abs/2509.14436)) [LIMITED].
- Recursive training makes the "tails of the original content distribution disappear": OPT-125m on wikitext2 lost "from 20 to 28 perplexity points" with no original data, and keeping 10% gave "only minor degradation" ([Shumailov et al., Nature 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11269175/)).
- The loop can be broken: across 44 years of CHI papers, "prose did not homogenize" ([Kosch et al. 2026](https://arxiv.org/abs/2609.23090)) [LIMITED]. Variety survives where people keep control of the content.

**Durability.** Worsening.

**What the skill does.** Information gain is the test of done (step 2), and the consensus map (step 3) names what every other article says so the piece can leave it. In a product, cross-customer checks catch the same loop inside your own archive.

## R9. Repetition penalties

**Mechanism.** Frequency, presence and repetition penalties discount any token already used. They cure loops by creating another artifact: the model swaps a key term for synonyms where a person would repeat it.

**Tells.** Synonym cycling ("the parser", then "the parsing component", then "the tokenization layer"); key terms that never recur.

**Evidence.** OpenAI-style APIs expose `frequency_penalty` and `presence_penalty` (−2.0 to 2.0), per third-party mirrors of the documentation ([Box developer reference](https://developer.box.com/reference/resources/ai-llm-endpoint-params-openai)). Adjacent-sentence content-word overlap has a median of 0.021 in machine text against 0.063 in human text ([Opace 2026](https://opace.agency/tools/ai/content-verification-integrity/research/ai-writing-myths-measured/)) [VENDOR CLAIM], and Wikipedia's editors blame repetition penalties for "elegant variation" [editor observation]. Hosted products do not publish their penalty defaults, so for them the cause is inferred [UNKNOWN], and R3 may reinforce it.

**Durability.** Settings-dependent.

**What the skill does.** "Repeat key terms"; low penalties wherever an API still offers them.

## R10. Patch-and-shift

**Mechanism.** Once a tell is public, providers train it out and users scrub it, and replacement defaults arrive. Fixed lists go stale, over-correction becomes a tell of its own, and human usage moves more slowly than models do, so a human writer in 2026 can carry 2024 tells absorbed from reading model text.

**Tells.** Wikipedia's mid-2026 ("GPT-6 era") list: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally, "with much more period and comma usage and shorter sentences around a strict 8–20 word limit"; new corrective frames such as "should be treated as X rather than Y" ([Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)) [editor observation].

**Evidence.**
- "delve" in rewritten arXiv abstracts: odds ratio >300:1 for GPT-3.5 and GPT-4, ~100:1 for GPT-4-turbo, ~40:1 for GPT-4o ([Yakura et al.](https://arxiv.org/html/2409.01754v3)). It dropped soon after being pointed out in early 2024, while "significant" kept rising ([Geng & Trotta 2025](https://arxiv.org/abs/2502.09606)) [LIMITED].
- Em dashes per 1,000 words: GPT-4.1 10.62, GPT-5.4 1.43 (≈ −85%); Claude Opus 4.6 9.09 unconstrained, 0.19 under a no-markdown instruction ([Freeburg 2026](https://arxiv.org/pdf/2603.27006)) [LIMITED]. From September 2026, Wikipedia reports, newer models "appear hard-coded not to use them", so "commas and periods are more likely now than even human text, and now that has become its own sign". Human use lagged and kept rising: em dashes in medRxiv Discussion sections went from ~4% through 2023 to 8.0% in 2024 and 20.3% in 2025 (N = 69,632) ([Czuma 2026](https://arxiv.org/abs/2606.29540)) [LIMITED].
- "Not X but Y" persisted: its web rate rose from 0.87 to 2.36 per 10k words between 2023 and 2026 (Pew), and The Atlantic (July 2026) wrote that earlier tells "came and went as models improved, but this one has not faded" ([AI Weekly summary](https://aiweekly.co/alerts/atlantic-ais-its-not-x-its-y-tic-proves-hardest-to-shake)).
- Fixed-list slop scores (EQ-Bench Creative Writing, fetched 23 Oct 2026) roughly halve within families, e.g. claude-sonnet-4 2.7 to claude-opus-5 0.9, gemini-2.0-flash 6.5 to gemini-3.8-flash 3.1 ([EQ-Bench](https://eqbench.com/creative_writing.html)) [BENCHMARK CLAIM; LLM-judged]. A fixed list cannot see new tics, so part of the fall measures list-avoidance [HYPOTHESIS].

**Durability.** Cyclical. The notes rank durability, most to least [HYPOTHESIS]: sameness of angle and content (R2, R5, R7); the evaluative, nominal and participial register (R3); contrastive framing; stock names and settings; formatting habits; individual words; individual punctuation marks. Family checks still worth running in late 2026 [HYPOTHESIS]: Claude, em dashes when unconstrained; ChatGPT, bold inside lists, headers, "certainly" and "overall"; Gemini, italics and more slop than its peers; Llama 4, the most slop of the major families.

**What the skill does.** Rules aimed at mechanisms; word lists treated as dated, with the `verified-against` stamp in SKILL.md's metadata; punctuation taken from the author, nothing scrubbed to zero; rhythm from content, with no sentence-length quota.

## Tell-to-cause lookup

| Tell | Cause | Note |
|---|---|---|
| "delve", "underscore", "nuanced", "pivotal", "meticulous" | R3, amplified by R2 | single words retired by R10 |
| Participial tails, nominalizations, "serves as", "stands as" | R3 | instruction-tuning register; base models sit near human rates |
| Headers, bold-label bullets, triads, emoji | R3, R6 | the rule of three alone is near chance (AUROC 0.515, Opace) [VENDOR CLAIM] |
| "Great question", "Certainly", "Here are some", "Of course" | R3 | alignment shifts early stylistic tokens (URIAL) |
| Previews, closing summaries, "a beacon of hope" endings | R3 (length, positivity) | [HYPOTHESIS]: no direct reward-model study |
| Flattery; uniform confidence | R3 | sycophancy; raters penalise stated uncertainty |
| "On the other hand", disclaimers, moralizing | R4 | |
| "It's not X, it's Y" | R3, on raw material from promotional prose (R1) | inferential (Boggia) |
| Corrective frames such as "should be treated as X rather than Y" | R10, R3 | very rare before July 2026, around the GPT-5.6 release |
| Elara, Elias, lighthouses, "time is a river" | R5, R2 | |
| Synonym cycling; key terms never repeated | R9, possibly R3 | |
| Em dashes, too many or none | R3, R10 | origin unresolved |
| Uniform 8–20-word sentences; only commas and periods | R10 | over-correction |
| Flat surprisal, "low burstiness" | R1, R2 | |
| Template-shaped answers | R6 | |
| Generic claims; invented specifics | R7 | |
| The same angle and outline as everyone else | R2, R5, R7, R8 | |

## Myths that are not causes

- **"AI has perfect grammar."** AI text has fewer surface errors (19.6% of human against 14.8% of AI self-presentations flagged for grammar; [Jakesch et al.](https://www.arxiv.org/pdf/2206.07271)), but skilled people write cleanly too, and Wikipedia lists perfect grammar as an ineffective indicator. Editors' commonest fixes to model prose are awkward word choice and phrasing (~28%), poor sentence structure (~20%) and tense slips ([Chakrabarty et al. 2025](https://arxiv.org/html/2409.14509)).
- **"AI never uses contractions."** It depends on the model: GPT-4o and GPT-4o Mini use them at 60–63% of the human rate, Llama 3 Instruct at 139–141% ([Reinhart et al.](https://arxiv.org/html/2410.16107v1)); a 2026 RAID-based replication finds chat models overusing them.
- **"Burstiness = sentence-length variance."** GPTZero defined burstiness as "how much writing patterns and text perplexities vary over the entire document" ([GPTZero](https://gptzero.me/news/perplexity-and-burstiness-what-is-it/)) [VENDOR CLAIM]. Sentence-length variation scored AUROC 0.521 on 5,935 matched pairs (Opace) [VENDOR CLAIM]. With a corrected measure, 32 of 45 family-by-mode cells were flatter than human, and few-shot human exemplars gave the flattest output in 7 of 9 families ([NeurIPS 2026](https://neurips.cc/virtual/2026/164820)) [LIMITED]. The deficit is in surprisal (R1); prompting for rhythm moves flatness unpredictably.
- **"AI text is simply low-perplexity."** That depends on the observer and the prompt. Under GPT-2-small, modern machine text had a higher median log-perplexity than human text (3.68 against 3.31), and surprisal kurtosis (AUROC 0.766) beat log-perplexity (0.715) ([Opace](https://opace.agency/tools/ai/content-verification-integrity/research/ai-writing-myths-measured/)) [VENDOR CLAIM]. An odd prompt can make any completion high-perplexity, which is why Binoculars divides perplexity by cross-perplexity.
- **"Raise the temperature."** In a fixed-model narrative task, temperature was "weakly correlated with novelty" and moderately with incoherence ([Peeperkorn et al. 2024](https://arxiv.org/abs/2405.00492)) [LIMITED]. Five temperatures of one model were told apart 37.9% of the time (chance 20%) against 97.1% for five different models ([Sun et al. 2025](https://arxiv.org/html/2502.12150)) [LIMITED]. Min-p 0.1 at temperature 2.0 still left 61.2% of response pairs above 0.8 similarity (Hivemind), and across 16 models temperature had "no systematic effect" on register ([AI-Brown/AI-Koditex](https://arxiv.org/html/2509.10179)). On re-analysis, min-p's headline human study won 1 of 12 tests after Bonferroni correction ([Schaeffer et al.](https://arxiv.org/html/2506.13681v2)) [LIMITED].
- **"Paraphrase or 'humanize' it."** The source model stays identifiable at 91.4% after GPT-4o-mini paraphrase, 91.8% after translation and 88.9% with the words shuffled, because word choice carries the signal ([Sun et al. 2025](https://arxiv.org/html/2502.12150)), and the rewriter adds its own fingerprint. Humanized o1-pro articles were still caught 100% by an expert majority and at 90.0% TPR by Pangram ([Russell et al. 2025](https://arxiv.org/abs/2501.15654)).
- **"Ban the AI words."** Plain token banning "becomes unusable at just 2,000" patterns, with writing quality at 28/100 at 8,000 bans ([Antislop](https://arxiv.org/html/2510.15061)) [LIMITED]. Replacements rise as old words fall, and the mid-2026 plain style is a tell in its own right (R10).
- **"Hedging is the AI tell."** Hedging density scored AUROC 0.500 (Opace) [VENDOR CLAIM]; GPT-4 essays had fewer epistemic markers than students' (0.00 against 0.06 per sentence, d = 1.53) and 44% fewer modals (Herbold et al.). The model pattern is uniform confidence plus formulaic disclaimers (R3, R4).
- **"AI text is plagiarized."** It is mostly novel at short n-gram lengths; the larger problem is semantic sameness (R2, R5, R7).

## Gaps: what nobody has measured

- Surprisal mean and variance for 2025–26 frontier chat models against matched human text under a modern observer; closed models do not expose full log-probabilities.
- Reward-model preference for previews, closing summaries, the rule of three, "not X but Y" or synonym variation, and base-versus-aligned comparisons for these figures; their attribution to preference tuning is inference.
- The typicality weight α beyond HelpSteer and two scorer models, including the proprietary preference data behind GPT-5.x, Claude 4.x–5.x and Gemini 3; which training stage causes what in frontier models.
- The causes of between-model homogeneity; the origin of the em dash habit; penalty defaults in hosted chat products; how the causes interact and how much of each tell each one explains.
- Per-version corpus studies (Biber-feature style) for GPT-5.x, Claude 4.x–5.x, Gemini 2.5–3, Llama 4, Qwen 3 and DeepSeek V3/V4, and reasoning models against their non-reasoning siblings.
- Peer-reviewed similarity measurements across AI-written SEO articles; whether Google uses information gain in ranking; how rankings and readers respond to information-rich AI-assisted content.
- Whether the skill's rules work as a set against expert readers and detectors. The verbalized-sampling and anti-slop evidence comes from creative writing; transfer to marketing copy, email and LinkedIn posts is untested, and thresholds need calibrating per author and genre.
