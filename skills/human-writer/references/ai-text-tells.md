# AI-text tells: what is measured, how strong, how it has shifted

Evidence base: corpus and perception studies 2021 to 2026 (Liang 2024; Kobak 2025; Gray 2024; Juzek & Ward 2025; Reinhart 2025; Herbold 2023; Muñoz-Ortiz 2024; Shaib 2024; Jakesch 2023; Clark 2021; Russell 2025; Pew 2026; Freeburg 2026; the Opace 2026 vendor benchmark; Wikipedia's "Signs of AI writing" as of October 2026). URLs at the end. Numbers are quoted from the sources; where a source is a vendor benchmark or an editor-maintained list rather than peer-reviewed work, it says so.

Contents: 1 evidence grades; 2 vocabulary; 3 grammar and register; 4 rhythm; 5 discourse and structure; 6 lexical statistics; 7 what readers use and what works; 8 human-side features; 9 advice that backfires; 10 sources.

## 1. Evidence grades

Strong, replicated across studies:
- Density of evaluative "prestige" vocabulary (adjectives, adverbs, style verbs) at 3x to 170x human rates.
- Nominalizations and present-participial clauses far above human rates; "that"-clause subjects; fewer agentless passives.
- Fewer hedges, epistemic markers and modals; impersonal tone; fewer engagement features (questions, asides).
- Less specific content, fewer citations and quotes, convergence toward the average of other texts on the topic.
- Reused stock names and props.
- Positivity drift regardless of content.
- Homogeneity: outputs more similar to each other than human texts are.
- Part-of-speech templating (repeated POS 6-grams).
- Under-repetition: synonym cycling instead of reusing the term (direction flipped from the GPT-2/3 era, when models were less lexically diverse than humans).

Moderate or era-dependent:
- Negative parallelism ("not just X, but Y"; "it's not X, it's Y"): about 3x human rate; still rising on the web in 2026; also common in human listicles.
- Em dashes: strong for GPT-4-era and for Claude; reversed for 2026 OpenAI models, which now use fewer than humans.
- Markdown and formatting uniformity: separates documents but measures "the interface a document passed through".
- Contractions: GPT-4o uses fewer than humans, Llama-instruct more.

Weak or chance-level as single features (AUROC in a 2026 matched-pair vendor benchmark): hedging phrases 0.500, "in conclusion" closers 0.514, rule of three 0.515, discourse markers 0.517, sentence-length coefficient of variation 0.521, intensifiers 0.534.

Inverted (point toward human): passive voice, grammatical errors, rare words and long words, curly quotes (typesetting).

Anecdotal only: "Moreover/Furthermore" as ChatGPT-specific, Claude semicolons, "Here's the thing" openers, question-and-answer pairs.

The practical rule from Wikipedia's editors, which the data supports: look for combinations. Single features are near chance; the register is what separates.

## 2. Vocabulary

Mechanism: every study that could test it traces overuse to instruction tuning and preference training, not to pre-training data. "delves" appears at 183 per million words in ChatGPT-3.5 output against 3.2 on arXiv and 0.3 in PubMed. Base Llama 3 uses "tapestry" and "camaraderie" at roughly human rates; the instruct versions use them 150x more. Words rise as whole synonym groups ("crucial" does not displace "critical"), which means the signature is density of evaluation, not any one lexeme. Named words have a half-life of about one model generation.

Measured ratios (model-era text against pre-2023 human text):
- ICLR 2024 peer reviews (Liang 2024): "meticulous" 34.7x, "intricate" 11.2x, "commendable" 9.8x. Top AI-associated adjectives: commendable, innovative, meticulous, intricate, notable, versatile, noteworthy, invaluable, pivotal, potent, fresh, ingenious, cogent, ongoing, tangible, profound, methodical, laudable, lucid, appreciable, fascinating, adaptable, admirable, refreshing, proficient, intriguing, thoughtful, credible, exceptional, digestible, prevalent, interpretative, remarkable, seamless, economical, proactive, interdisciplinary, sustainable, optimizable, comprehensive, vital, pragmatic, comprehensible, unique, fuller, authentic, foundational, distinctive, pertinent, valuable. Top adverbs: meticulously, reportedly, lucidly, innovatively, aptly, methodically, excellently, compellingly, impressively, undoubtedly, scholarly, strategically, intriguingly, competently, intelligently, hitherto, thoughtfully, profoundly, undeniably, admirably.
- PubMed abstracts 2024 (Kobak 2025, Science Advances): "delves" 28x, "underscores" 13.8x, "showcasing" 10.7x; 66% of excess style words are verbs, 14% adjectives; common markers: across, additionally, comprehensive, crucial, enhancing, exhibited, insights, notably, particularly, within.
- Juzek & Ward 2025, PubMed 2020 to 2024 change: delves +6,697%, showcasing +1,396%, delve +1,375%, underscores +904%, intricacies +773%, surpassing +667%, intricate +611%, underscoring +537%, garnered +437%, emphasizing +397%, underscore +391%, realm +381%, groundbreaking +330%, advancements +278%, aligns +267%.
- Reinhart 2025 (PNAS preprint): GPT-4o Mini "camaraderie" ~171x, "tapestry" ~147x, "palpable" ~145x human rate; GPT models use several profanities more than 100x less than humans.
- Pew Research, August 2026, per 10,000 words on the web, 2023 to 2026: AI vocabulary (delve, interplay, testament, tapestry, pivotal, underscore) 11.9 to 26.0; em dashes 5.8 to 11.2; Oxford commas 34 to 55.5; negative parallelism 0.87 to 2.36.

Era lists (Wikipedia, editor-maintained, October 2026):
- 2023 to mid-2024 (GPT-4 era): Additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate, intricacies, interplay, key, landscape, meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant.
- Mid-2024 to mid-2025 (GPT-4o era): align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- Mid-2025 to mid-2026 (GPT-5 era): emphasizing, enhance, highlighting, showcasing; canned notability phrasing ("independent coverage", "media outlets", "trade publications", "featured in").
- Mid-2026 onward: challenge, clearer, dependable, echoed, foster, leverage, matters, multifaceted, practical, prioritize, quietly, steady, universally; with more periods and commas and shorter sentences in a strict 8 to 20 word band. Plain is becoming a tell.
- Grok: pseudo-scientific words (causal, empirical, correlate), still "underscore".

Copula avoidance: a measured decline of more than 10% in "is/are" in 2023 academic writing; models prefer "serves as", "stands as", "marks", "features", "boasts", "refers to" over "is/was/has".

Phrases expert readers and phrase scanners flag: "a testament to", "complex tapestry", "stands as", "plays a crucial/pivotal/vital role", "underscores its importance", "reflects broader", "setting the stage for", "indelible mark", "deeply rooted", "evolving landscape", "key turning point", "nestled", "in the heart of", "diverse array", "serving as a beacon of hope", "valuable insights", "align/resonate with". Models also replace "says" with "notes" and "explains" and insert honorifics ("Dr.", "Prof.").

## 3. Grammar and register

Reinhart 2025 (Biber features; rates as a percentage of the human rate; GPT-4o Mini / GPT-4o):
- Present participial clauses 481% / 527% (Llama 3 instruct 224% / 261%; Llama base 94% / 102%).
- "That" clauses as subject 331% / 263%.
- Nominalizations 209% / 214%.
- Past-participial postnominal clauses 257% / 235%.
- Phrasal coordination 144% / 194%.
- Agentless passives 51% / 53%.
- Amplifiers 63% / 46%; synthetic negation ("no", "none", "neither") 36% / 51%; contractions 63% / 60% (Llama instruct 141% / 139%); clausal coordination 63% / 59%; downtoners 155% / 118%.
Base models sit at 70 to 130% of human on most features: the register comes from instruction tuning. A 2026 replication on the RAID corpus (11 models, 8 genres) finds the same overuse of nominalizations, "that"-clause subjects and postnominal participial clauses, and underuse of concessive subordinators ("though", "although") and synthetic negation; human-vs-machine AUC about 0.97.

Herbold 2023 (argumentative essays, effect sizes d): nominalizations per sentence 1.06 human vs 1.73 GPT-4 (d = 1.35); modal verbs 10.84 vs 6.12 (d = 1.08); epistemic markers 0.06 vs 0.00 (d = 1.53); discourse markers 0.57 vs 0.36 (d = 0.98); clauses per sentence 1.81 vs 2.08.

Shaib 2024 (POS templates): about 95% of model summaries contain a repeated POS 6-gram template against about 38% of human references; 76% of model templates occur in pre-training data; templates survive fine-tuning; larger models are not less templated.

Muñoz-Ortiz 2024: models use more auxiliaries, pronouns, numbers and symbols and fewer nouns and adjectives than NYT text; human dependency structures are more optimized (shorter dependencies than chance).

Passive voice runs against folk belief: machine text uses less of it (Cliff's delta -0.20); Bard produced zero passive auxiliaries.

## 4. Rhythm and length

- Models concentrate sentences in the 10 to 30 token range while human news sentences scatter more widely with more long sentences ("register leveling").
- Sentence-length coefficient of variation is near chance as a detector (AUROC 0.52, matched pairs); raw SD does slightly better (0.63). A NeurIPS 2026 paper using the Goh-Barabási burstiness coefficient finds 32 of 45 model-by-prompt cells significantly flatter than human, 8 no different, 5 more dispersed. Prompting for rhythm "moves flatness without targeting" it; few-shot human exemplars produced the flattest output in 7 of 9 families.
- Mid-2026 models: "shorter sentences around a strict 8 to 20 word limit" with more periods and commas (Wikipedia). The Economist's 2026 study: blocky paragraphs, uniform structure, few commas, semicolons and parentheses, and "and" as the most overused word.
- Rhythm variety that survives has to come from content: asides, fragments, questions, quotes, a one-sentence paragraph.

## 5. Discourse and structure

What expert detectors cite (Russell, Karpinska & Iyyer, ACL 2025; 300 nonfiction articles; share of explanations naming each clue):
- Vocabulary 53.1%; Sentence structure 35.9% ("not only... but also", lists of three, less varied length); Grammar and punctuation 24.8% (AI clean, humans make minor errors); Originality 23.7% (AI "safe and predictable, with few surprises or humor"); Quotes 22.3% (AI quotes overly formal, mirror the article's style); Clarity 19.5% (over-explains, "telling rather than showing"); Formatting 15.0% (uniform headings, bolded lists, similar paragraph lengths); Conclusions 13.1% (repetitive, optimistic; humans "end more abruptly"); Formality 12.3% (no filler, contractions, slang); Names and titles 11.7% ("Emily Carter", "Sarah Thompson", same title for several people); Tone 9.3% (neutral or positive throughout); Introductions 7.3% (generic or scenic); Factuality 7.2%; Topics 3.1% (avoids darker subjects).
- These five frequent-ChatGPT-user annotators reached 92.7% TPR / 4.0% FPR individually and 99.3% / 0% by majority vote, including 100% on paraphrased GPT-4o and "humanized" o1-pro text, beating GPTZero (85.3% TPR; 46.7% on humanized) and matching Pangram (98.0%).

Peer reviews (Liang 2024): LLM-modified reviews are closer to the centroid of all reviews, carry fewer "et al." citations, lower self-rated confidence, less specific feedback.

Metadiscourse (Jiang & Hyland 2025): ChatGPT essays have significantly fewer hedges, boosters and attitude markers; students use more questions, personal asides and self-mentions. Goulart 2024: AI texts are more informationally dense and less "involved".

Sentiment: student reports became more positive since 2022 regardless of content (Mak & Walasek 2025); human news expresses more fear and disgust, models more joy; hotel reviews by AI are more analytic and affective and less readable.

Fiction (StoryScope 2026; Hamilton & Mimno 2026): AI stories over-explain themes, favor tidy single-track plots and cluster in a narrow region of narrative space; human stories leave choices morally ambiguous. Eleven tokens (names Elias, Mara, Elara; lighthouses; clockmaker, librarian) occur in 88.3% of 20,000 stories across four current models. Claude shows flat escalation, GPT over-indexes on dream sequences, Gemini defaults to external description.

Encyclopedic prose (Wikipedia's content signs): undue emphasis on significance and legacy; superficial analyses via participle tails with vague attributions; promotional register; vague attributions ("experts argue", "observers have cited"); outline-like "challenges and future outlook" closers; "Awards and recognition" sections; canned notability claims; chatbot residue ("I hope this helps", "Would you like", unfilled placeholders, "2025-XX-XX" dates); title-case headings; bold "key takeaways"; inline-header bullet lists; skipped heading levels; small tables that should be prose; citation bugs (`contentReference[oaicite:N]`, `turn0search0`, `[cite: 1]`, `utm_source=chatgpt.com`).

## 6. Lexical statistics

- Direction flip: GPT-3-era text had lower lexical diversity than human (MTLD 75.7 vs 95.7); GPT-4 text higher (108.9). Fine-tuned GPT-2/3 profiles were simpler and more repetitive than human ones (Jakesch: lexical diversity r = -0.20 with AI authorship).
- 2026 (Opace, 670 long-form pairs, vendor benchmark): MATTR-100 AUROC 0.911; adjacent-sentence content-word overlap 0.912 (median machine 0.021 vs human 0.063); TTR over first 400 words 0.876; distinct word triples 0.839; hapax share 0.782. Machines "use synonyms and rephrasing where people repeat a term". A 24-feature classifier without formatting features caught 72% of machine documents at 1% FPR.
- RAID-based 2026 study: type-token ratio is the single most important feature; humans keep a narrow, consistent TTR for a given length while LLM text spreads wider, "sometimes under-varied and sometimes exaggerated".
- Function words and POS profiles separate human from model at 90% plus and attribute text to a specific model (88% for GPT-3.5/4/Bard; 99.8% for seven LLMs in Japanese). Each LLM forms a tight stylometric cluster; humans vary far more (O'Sullivan 2025).
- Perplexity under a small observer model no longer reliably favors machine text: in the 2026 benchmark machine median log-perplexity (3.68) was higher than human (3.31); surprisal kurtosis beat raw perplexity.
- Homogenization: co-writing with InstructGPT lowered unique n-gram fractions and raised key-point homogenization; AI-assisted stories were 10.7% more similar to each other even as raters judged them more creative; across Reddit, local news and arXiv, variance in complexity features fell after November 2022 and LLM rewriting erases demographic and personality signal.

## 7. What readers use and what works

Jakesch, Hancock & Naaman (PNAS 2023; 4,600 participants): accuracy 50 to 52% in every condition; incentives and feedback did not help; agreement above chance (shared flawed heuristics).
- Cues that work: nonsensical content, repetition.
- Cues readers use that are inverted: grammatical errors (read as AI, actually human), rare bigrams and long words (same), contractions (read as human, actually slightly more AI).
- Not diagnostic: first-person pronouns, family words, focus on the past, word count, swear words.
- AI profiles selected to exploit these heuristics were rated human 65.7% of the time against 51.7% for real human profiles ("more human than human").

Clark et al. (ACL 2021): 50% accuracy on GPT-3; 47% of rater comments concerned form (spelling, grammar, style) and only 25% content; brief training with examples shifted comments toward content and gave the only significant gain (55%).

Russell et al. 2025: experts rely first on AI vocabulary (in 88% of explanations for paraphrased text) and then on formality, originality and clarity, which detectors assess poorly. Blind spots are model-specific: the annotator unfamiliar with Claude did worst on Claude; the annotator relying on informality cues was fooled by o1-pro.

## 8. Human-side features

Empirically more common in human writing:
- Plain copulas and plain verbs: "there is a", "it has a"; wrote not authored, moved not relocated, used not utilized, tried not attempted.
- Superlatives and definitive statements ("one of the best", "the only", "the first"); qualifiers and intensifiers ("very", "perhaps", "tends to"); wordy constructions ("as a result of", "in order to", "the fact that").
- More hedges, boosters, attitude markers, questions, personal asides, modals and epistemic markers.
- About twice the agentless passives of GPT-4o, 2 to 3x the synthetic negation ("no one", "nothing"), 1.6x the contractions and clausal coordination, one-fifth the participial clauses.
- Repeating the same content word across adjacent sentences about three times as often.
- More commas, semicolons and parentheses; quoting people.
- More nouns and adjectives, fewer auxiliaries and pronouns; scattered sentence lengths with more long ones.
- Emotional range including fear, disgust and profanity; darker or mature subjects; humor and surprises; abrupt endings; strong hooks.
- Unique, context-specific names; concrete brand, place and habit detail ("lounging on a lake and drinking Bell's beer"); self-deprecation.
- Moral ambiguity in narrative instead of stated themes.
- Inconsistent formatting; occasional minor errors (statistically real, not a lever to pull on purpose).

## 9. Advice that backfires

- "Vary your sentence length" as a target: CV is near chance; aiming at a band produces the 2026 artifact.
- "Avoid the passive": humans use twice as much as GPT-4o.
- "Don't repeat yourself" / "vary your vocabulary": produces synonym cycling, now a listed sign.
- "Cut qualifiers": humans use more "very" and "perhaps" than models.
- "Never use em dashes": the newest OpenAI models already comply and that absence is now itself a sign; Claude text is the one that needs restraint.
- "Sound casual": fools lay readers, not experts or detectors; informality is cheap for a model to add.
- "Add typos": an evasion trick, not writing.
- "Use the first person": not diagnostic.
- "Perfect grammar means AI" and "formal prose means AI": both listed as ineffective indicators.

## 10. Sources

- Liang et al. 2024, Monitoring AI-Modified Content at Scale (ICML): https://arxiv.org/html/2403.07183v1
- Kobak et al. 2024/2025, Delving into LLM-assisted writing in biomedical publications (Science Advances): https://arxiv.org/html/2406.07016v5
- Gray 2024, ChatGPT "contamination": https://arxiv.org/pdf/2403.16887
- Juzek & Ward 2025, Why does ChatGPT "delve" so much? (COLING): https://arxiv.org/html/2412.11385v1
- AI-induced language change in scientific English (2025): https://arxiv.org/html/2506.21817v1
- Yakura et al., Empirical evidence of LLM influence on human spoken communication: https://arxiv.org/html/2409.01754v3
- Mak & Walasek 2025 (Warwick): https://warwick.ac.uk/news/pressreleases/positive-polished-student/
- Pew Research, August 2026, How much of the internet is written with AI: https://www.pewresearch.org/data-labs/2026/08/20/how-much-of-the-internet-is-written-with-ai.md
- Wikipedia:Signs of AI writing (WikiProject AI Cleanup): https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
- Reinhart et al. 2025, Do LLMs write like humans? (PNAS): https://arxiv.org/html/2410.16107v1
- Interpretable stylistic variation on RAID (2026): https://www.alphaxiv.org/abs/2604.14111
- Herbold et al. 2023 (Scientific Reports): https://ar5iv.labs.arxiv.org/html/2304.14276
- Muñoz-Ortiz et al. 2024, Contrasting linguistic patterns: https://arxiv.org/pdf/2308.09067v3
- Shaib et al. 2024, Detection and measurement of syntactic templates (EMNLP): https://arxiv.org/html/2407.00211v2
- Rosenfeld & Lazebnik 2024, Whose LLM is it anyway?: https://arxiv.org/html/2402.14533v1
- Opace 2026, AI writing myths measured (vendor benchmark, not peer-reviewed): https://opace.agency/tools/ai/content-verification-integrity/research/ai-writing-myths-measured/
- NeurIPS 2026, Burstiness Was Measured Wrong: https://neurips.cc/virtual/2026/164820
- Freeburg 2026, The Last Fingerprint (em dashes): https://arxiv.org/pdf/2603.27006
- Russell, Karpinska & Iyyer 2025, People who frequently use ChatGPT... (ACL): https://arxiv.org/html/2501.15654v2
- Jakesch, Hancock & Naaman 2023 (PNAS): https://www.arxiv.org/pdf/2206.07271
- Clark et al. 2021, All That's "Human" Is Not Gold (ACL): https://aclanthology.org/2021.acl-long.565.pdf
- Jiang & Hyland 2025 (English for Specific Purposes): https://ueaeprints.uea.ac.uk/id/eprint/99123
- StoryScope 2026: https://arxiv.org/abs/2604.03136v1
- Hamilton & Mimno 2026 (stock story tokens): https://arxiv.org/pdf/2605.26492
- Padmakumar & He, Does writing with language models reduce content diversity?: https://arxiv.org/html/2309.05196v3
- Doshi & Hauser 2024 (Science Advances): https://pmc.ncbi.nlm.nih.gov/articles/PMC11244532
- Sourati et al. (USC), LLM homogenization of written text: https://arxiv.org/html/2502.11266v1
- Benchmark of stylistic variation in LLMs (aidiolects): https://arxiv.org/html/2509.10179
- Reinhart's annotated bibliography on LLM style: https://www.refsmmat.com/notebooks/llm-style.html
- Stamatatos 2009, A survey of modern authorship attribution methods: https://www.clips.uantwerpen.be/~walter/educational/material/Stamatatos_survey2009.pdf
