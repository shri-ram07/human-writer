# Originality: how copy detection works and what it takes to be original

Evidence base: the classical algorithm papers (Schleimer, Wilkerson & Aiken 2003; Broder 1997; Manku, Jain & Das Sarma 2007; Wise 1993; Prechelt 2002), the PAN plagiarism-detection overviews (2013, 2014), Stamatatos 2009, Foltýnek et al. 2020 (TeSToP, 15 commercial tools), vendor documentation (Turnitin, iThenticate, Copyleaks, Copyscape, Unicheck, PlagScan, PlagAware), Lee et al. 2023 and Carlini et al. 2022 on memorization, and the code-similarity tool sources and papers (MOSS, JPlag, Dolos, Compare50, Mossad, Sağlam & Schmid 2025). URLs at the end.

Contents: 1 text fingerprinting in five steps; 2 thresholds by tool; 3 what survives paraphrase; 4 intrinsic detection; 5 technical disguises; 6 LLM memorization; 7 code similarity; 8 practice.

## 1. Text fingerprinting in five steps

Every classical copy detector does this:
1. Normalize: lowercase, strip punctuation and whitespace, often remove stop words and stem; map look-alike Unicode characters back to Latin.
2. Slice into k-grams (k consecutive words or characters). The choice of k is the noise threshold: common idioms must be shorter than k. Broder used 10-word shingles; textbook guidance is ~9 characters for articles; PAN systems seed on 3 to 8 word n-grams; Turnitin surfaces matches of 8 words or more.
3. Hash each k-gram with a rolling (Karp-Rabin) hash so each new k-gram costs one update.
4. Select fingerprints position-independently. Winnowing: slide a window of w consecutive hashes and keep the minimum (rightmost on ties). Guarantee: any shared substring of length t = w + k - 1 is detected; nothing shorter than k can match; density about 2/(w + 1). MOSS uses the robust variant. Alternatives: 0 mod p (unbounded gaps), MinHash and LSH banding (fixed-size sketches, whole-document resemblance), SimHash with Hamming distance 3 on 64 bits (Google's near-duplicate crawl filter).
5. Index fingerprint to (document, position) like a search engine; look up each new document's fingerprints; rank candidate pairs by shared fingerprints; re-align the best pairs with suffix-array, greedy-string-tiling or dynamic-programming passes to find exact passage boundaries; merge adjacent matches; drop passages below a length floor.

Resemblance (Jaccard of shingle sets) versus containment (shared shingles over one document's shingles): plagiarism needs containment, because a stolen paragraph sits inside a long paper. Fixed-size sketches cannot measure containment; winnowing and mod-p selection can.

What Turnitin publicly documents: a crawl of about 70 billion current and archived pages (it keeps historical copies, so deleting a source online does not remove it), 1.9 billion student papers as of June 2025, 47,000 journals and Crossref-gated publisher content. The Similarity Score is the percentage of the submission's words that match any source; Turnitin states it "is not an assessment of whether the paper includes plagiarized material" and that there is no acceptable score. Match Overview partitions the text among best sources (27 + 10 + 2 + 2 + 1 = 41% in its sample report); All Sources lists overlapping ones. The algorithm itself is undisclosed.

## 2. Thresholds by tool

| Tool | Smallest match surfaced | Notes |
|---|---|---|
| Turnitin (current report) | 8 consecutive words, default and minimum | legacy advice: set 10 to 16 for cleaner reports; quotes and bibliography usually excluded |
| iThenticate / Crossref Similarity Check | 9 words | 78M full-text scholarly items |
| Unicheck | 4 words | plus synonym-aware NLP layer (undocumented) |
| PlagScan (now Ouriginal/Turnitin) | about 3 consecutive words (uncited) | Bing index plus prevention pool |
| PlagAware | 50 characters default (10 to 250) | low settings flag 2 to 3 words |
| Copyscape Copysentry | 1 to 4 sentences | queries Google directly |
| Copyleaks | not published | three levels: identical, minor changes, paraphrased ("related meaning"); cross-language from 9 source languages |
| PAN research systems | passages under 150 to 300 characters or 15 to 40 words discarded | seeds on sorted 3 to 5 grams, stop-word 8-grams, sentence cosine > 0.33 |
| Lee et al. 2023 (LLM plagiarism pipeline) | 256 characters of verbatim common substring | paraphrase via RoBERTa classifier 0.5 to 0.99 with matching named entities |
| Carlini et al. 2022 (memorization) | 50 tokens, about 25 words | the unit of "extractable" |

Institutional policies, where they exist, use an overall cap around 15 to 20% with a per-source cap of 1 to 2% and sometimes a 10-word unbroken-string rule; the per-source cap is the operative signal. Testers (TeSToP) say the single percentage "does not carry any information on the actual extent of plagiarism".

Under default Turnitin settings a copied run of 7 words or fewer is invisible; 8 or more appears and is dismissed as a common phrase unless matches cluster; 10 to 16 words is where reviewers start treating a match as copying.

## 3. What survives paraphrase

The PAN text-alignment architecture is seeding, extension, filtering:
- Seeds designed against disguises: sorted word n-grams and skip-grams (defeat reordering), stop-word 8-grams (eight function words in sequence; survive synonym replacement of content words), named-entity n-grams, stemmed n-grams, sentence tf-idf cosine above 0.33 (tolerates about two-thirds of the vocabulary changing).
- Extension merges seeds whose gaps are below 200 to 4,000 characters, or via Smith-Waterman / clustering; filtering drops short passages.
- Results of the best 2014 system by obfuscation type (plagdet): none 0.90, synonym-and-shuffle "random" obfuscation 0.88, cyclic machine translation through three languages 0.89, human summary 0.56. The naive baseline collapses to 0.05 to 0.11 under any obfuscation.

What this means: synonym substitution every few words destroys ordered word 5-grams but not stop-word 8-grams or sorted n-grams; clause reordering destroys ordered n-grams but not sorted ones; back-translation preserves enough skeleton to match. Only rewriting that changes the content words, the function-word sequence and the order at once, which is to say genuine re-expression or summary, escapes, and that is also the only kind that reads well.

Semantic layers: SBERT sentence similarity beats Jaccard for alignment (85.8% vs 78.2%); heavy synonym substitution lands at cosine 0.35 to 0.55; vendor "paraphrase detection" (Copyleaks related meaning, Unicheck NLP, Quetext fuzzy matching) is undocumented, and the last independent multi-tool test (TeSToP 2020, 15 tools, 8 languages) found synonym replacement "only partially satisfactory", manual paraphrase "quite unsatisfactory" for every tool, and translation undetected by all but one; no tool rated "useful".

Cross-language: character 3-gram cosine works for related languages (F1 0.96 on a balanced test); explicit semantic analysis over Wikipedia concepts works for arbitrary pairs; citation-order analysis (longest common citation sequence, citation tiling) found 13 of 16 translated sections in the Guttenberg thesis that text matchers missed entirely.

## 4. Intrinsic detection (style shifts inside one document)

Stamatatos 2009: character 3-gram profiles over a sliding window of 1,000 letters (step 200); each window's dissimilarity to the whole-document profile; flag windows above mean plus two standard deviations. PAN-09 result: recall about 0.46, precision about 0.22. Modern style-change systems (PAN 2023, DeBERTa-based) reach F1 0.98 when topics differ and 0.82 when all paragraphs share a topic. It detects mixtures, never wholesale replacement, and cannot say where text came from; it is triage, not evidence.

## 5. Technical disguises are flags, not disguises

Turnitin maps look-alike characters from other alphabets back to Latin before matching and raises a "replaced characters" flag; it flags white-on-white text and hidden quotation marks (documents of 500+ characters). Unicheck claims homoglyph detection. Research systems normalize case, whitespace, punctuation, stop words and stems. Text embedded as images is still invisible to text matchers but conspicuous to a human and breaks word counts. None of this is writing, and all of it draws attention.

## 6. LLM memorization

- GPT-2 (Lee et al. 2023, 10,000 generations per setting): verbatim training-data spans of 256+ characters in 0.47% (temperature), 0.65% (top-k), 0.70% (top-p) of generations; paraphrase 0.16 to 0.32%; idea 0.05 to 0.38%. Larger models plagiarize more; top-k and top-p more than temperature sampling. A model fine-tuned on a domain corpus reached 5.5% paraphrase reuse of that corpus.
- Carlini et al. 2022: GPT-J 6B reproduces at least 1% of its training set given 50-token prompts; memorization grows log-linearly with model size, duplication count and prompt length (33% extractable at 50 tokens of context vs 65% at 450 for the 6B model); deduplication cuts it about threefold to tenfold.
- Nasr, Carlini et al. 2023: alignment does not eliminate memorization; a divergence attack extracted training data from ChatGPT.
- NYT v. OpenAI Exhibit J: 100 examples of GPT-4 continuing New York Times articles verbatim when prompted with their openings; OpenAI called it "a rare bug" tied to heavily duplicated text.
- Through a commercial checker, ChatGPT essays averaged 22% similarity against 33% for human essays; the exposure is not the headline percentage but occasional sentence-length verbatim fragments of widely duplicated text, which is exactly what web-indexed checkers match.

Practical reading: famous passages, encyclopedic definitions, licenses, lyrics, widely syndicated news and popular tutorials are the high-risk inputs. Prompting a model with the opening of a known text is the worst case. Asking for original prose on a topic is the low-exposure case. Paraphrase-level reuse (0.2 to 0.4% of generations, up to 5% after domain fine-tuning) is what text matchers miss and readers catch.

## 7. Code similarity

How the tools work:
- MOSS: language front end strips whitespace and comments and collapses identifiers to one placeholder; k-grams of the token stream hashed with a rolling hash; robust winnowing; inverted index; passages in more than 10 submissions ignored (-m); anything in the base file ignored (-b); output ranked by matched fingerprints with "Lines Matched" and per-file percentage. Stanford: "the scores are certainly not a proof of plagiarism."
- JPlag: structural tokens (CLASS{, METHOD{, VARDEF, ASSIGN, APPLY, LOOP{, IF{, RETURN...), Greedy String Tiling with Karp-Rabin hashing; similarity = matched tokens over total tokens (average) or the larger one-sided coverage (max); minimum token match per language (Java 9, C/C++/Python 12, C#/Go/Rust 8, text 5); since v5.0.0 (2024) token-sequence normalization and subsequence match merging against insertion and reordering; since v6.3.0 rarity-weighted matches. Compares only within the submitted set, never against the internet.
- Dolos: tree-sitter syntax tree serialized with identifiers, strings and comments masked; k = 23, window 17 (any shared run of 39 syntax tokens is detected); metrics similarity, total overlap, longest fragment; threshold inferred from a two-Gaussian fit of the nearest-neighbour histogram.
- Compare50: winnowing with k = 25, t = 35; identifiers to `v`, literals normalized; idf weighting down-weights snippets common across submissions; relative 1 to 10 scores.
- Clone detectors: Type-1 (whitespace/comments), Type-2 (plus identifiers/literals/types), Type-3 (statements added/changed/removed), Type-4 (same computation, different syntax). Token tools catch Types 1 to 3 (SourcererCC recall T1 100%, T2 98%, strongly similar T3 61%, weak T3/T4 0%); AST hashing and characteristic vectors tolerate scattered edits; PDG matching handles reordering and insertion but does not scale; LLMs reach only 0.15 to 0.33 recall on Type-4 Java clones.

What survives normalization: the ordered sequence of statement kinds, control-structure nesting, the number and order of calls, assignments and declarations, method boundaries. Renaming, reformatting, commenting, splitting declarations, changing constants and modifiers change nothing in any tool (Prechelt found these "futile" in real student attempts). Inserting statements every few lines, reordering independent statements, swapping loop forms and extracting methods break token runs; the automated version (Mossad) drove MOSS from 26% to 15% and JPlag to 1% average similarity while readers found the code as readable as student code; JPlag's 2024 defenses restore 61 to 93 median points on such attacks.

Baselines for honest work: 25 to 30% in MOSS on small C assignments, 44 to 87% on tiny Java exercises, 0 to 6% median in JPlag on larger projects. Simple assignments produce uniform solutions. Reviewers add submission timelines, autograder-score coincidences, shared comments and typos, and whether a disguise looks artificial.

LLM convergence: one model-written submission does not trip these tools (no reference corpus of model output), but many students using the same model on the same small task converge (GPT-4 pairs median 20 to 31% vs 0 to 6% human; 2026 algorithmic tasks more than 75% vs 28%); instructors now generate "pseudo-AI submissions" and compare with Dolos (median 59 to 60% for AI vs 13 to 14% for student code).

GitHub Copilot's filter: compares an accepted, unmodified inline suggestion plus about 150 characters of surrounding code against an index of public GitHub code; under 1% of suggestions match; Block suppresses them; otherwise code referencing lists repositories and licenses. A licensing check, not an originality test.

## 8. Practice

Text:
- Read, close the source, write from understanding. Sentence-by-sentence paraphrase keeps the skeleton the seeds are built to find.
- Quote exact words with marks and attribution; cite ideas too.
- Expect short common phrases to match; worry when matches cluster on one source.
- Never prompt-continue a known text. When a famous passage, definition or license must appear, quote and cite it.
- Run `scripts/check.py draft.md --source <file>` for every document you were given; it reports shared 8-word runs.

Code:
- Decomposition, control flow and data representation are what register as original. Names, comments and formatting do not.
- Write standard algorithms from the spec, in the repo's style, with a comment naming the algorithm.
- Do not reproduce memorized snippets from well-known repositories or tutorials; if a suggestion looks like one, rewrite it from the problem.
- Expect convergence on small, well-specified tasks; the decisions specific to this codebase are the cure.

## Sources

- Schleimer, Wilkerson & Aiken 2003, Winnowing (SIGMOD): https://theory.stanford.edu/~aiken/publications/papers/sigmod03.pdf
- Broder et al. 1997, Syntactic clustering of the web: https://archives.iw3c2.org/www6/proceedings/Technical/Paper205/Paper205.html
- Manku, Jain & Das Sarma 2007, Detecting near-duplicates for web crawling: https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/33026.pdf
- Leskovec, Rajaraman & Ullman, Mining of Massive Datasets ch. 3: http://infolab.stanford.edu/~ullman/mmds/ch3.pdf
- Turnitin, Understanding the Similarity Report (student guide): https://help.turnitin.com/Resources/PDF/understanding_the_turnitin_similarity_report-a_student_guide.pdf
- Turnitin content database (2019): https://www.turnitin.co.uk/blog/how-much-do-you-know-about-turnitins-content
- Turnitin, excluding small matches: https://guides.turnitin.com/hc/en-us/articles/23539146689549
- Turnitin flags (replaced characters, hidden text): https://help.turnitin.com/feedback-studio/flags.htm
- Crossref Similarity Check: https://www.crossref.org/documentation/similarity-check/
- Copyleaks detection levels: https://docs.copyleaks.com/concepts/features/detection-levels.md
- Copyscape FAQ: https://www.copyscape.com/faqs.php
- Foltýnek et al. 2020, Testing of support tools for plagiarism detection (TeSToP): https://link.springer.com/article/10.1007/s40979-020-00061-1
- Potthast et al., PAN 2013 overview: https://ceur-ws.org/Vol-1179/CLEF2013wn-PAN-PotthastEt2013.pdf and PAN 2014 overview: https://ceur-ws.org/Vol-1180/CLEF2014wn-Pan-PotthastEt2014.pdf
- Potthast et al. 2011, Cross-language plagiarism detection: https://webis.de/downloads/publications/papers/potthast_2011a.pdf
- Ferrero et al. 2017, Cross-language plagiarism detection methods: https://arxiv.org/pdf/1705.08828
- Gipp & Meuschke 2011, Citation pattern matching: https://smartlib.umri.ac.id/assets/uploads/files/9af07-gipp11c.pdf
- Stamatatos 2009, Intrinsic plagiarism detection using character n-gram profiles: https://ceur-ws.org/Vol-502/paper8.pdf
- Zangerle et al., PAN 2023 multi-author style analysis: https://dbis-web1.uibk.ac.at/sites/default/files/2023-11/zangerle-pan-2023.pdf
- Lee, Le, Chen & Lee 2023, Do language models plagiarize? (WWW): https://ar5iv.labs.arxiv.org/html/2203.07618
- Carlini et al. 2022, Quantifying memorization across neural language models: https://ar5iv.labs.arxiv.org/html/2202.07646
- Nasr, Carlini et al. 2023, Scalable extraction of training data: https://systems.cs.columbia.edu/private-systems-class/papers/Carlini2023Scalable.pdf
- OpenAI response to NYT (via Fortune): https://fortune.com/2024/01/08/openai-blog-post-new-york-times-lawsuit-not-full-story-copyright
- Prechelt, Malpohl & Philippsen 2002, JPlag (J.UCS): https://www.jucs.org/jucs_8_11/finding_plagiarisms_among_a/Prechelt_L.pdf
- JPlag repository and releases: https://github.com/jplag/JPlag
- Dolos algorithm docs: https://github.com/dodona-edu/dolos/blob/main/docs/about/algorithm.md and Maertens et al. 2024: https://arxiv.org/abs/2402.10853
- MOSS home and reading guide: https://theory.stanford.edu/~aiken/moss/
- Compare50 docs: https://cs50.readthedocs.io/projects/compare50/en/latest/
- Roy & Cordy 2007, clone detection survey: https://research.cs.queensu.ca/TechReports/Reports/2007-541.pdf
- Sajnani et al. 2016, SourcererCC: https://arxiv.org/abs/1512.06448
- Novak, Joy & Kermek 2019, source-code similarity detection survey (ACM TOCE): https://www.dcs.warwick.ac.uk/~msj/publications/fulltext/novak_joy_kermek_toce_2019.pdf
- Cheers, Lin & Smith 2021, robustness of plagiarism tools to obfuscation: https://arxiv.org/abs/2102.03997
- Devore-McDonald & Berger 2020, Mossad: https://arxiv.org/abs/2010.01700
- Sağlam & Schmid 2025, automated plagiarism defenses in JPlag: https://arxiv.org/abs/2505.20158
- Biderman & Raff 2022, GPT-J vs MOSS: https://arxiv.org/abs/2201.07406
- Bashir 2025, pseudo-AI submissions with Dolos (Frontiers): https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1549761/full
- GitHub blog, code referencing for Copilot: https://github.blog/news-insights/product-news/introducing-code-referencing-for-github-copilot
