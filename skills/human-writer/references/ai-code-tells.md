# AI-code tells: what is measured, how detectors work, what similarity tools see

Evidence base: detector papers and benchmarks 2023 to 2026 (Caliskan-Islam 2015; DetectCodeGPT 2024; Whodunit 2024; GPTSniffer 2023; CodeGPTSensor 2024; Suh et al. 2024; Oedingen 2024; Pan et al. 2024; CoDet-M4 and Droid 2025; CodeMirage 2025; AICD Bench and SemEval-2026 Task 13; Cotroneo 2025; Improta 2026; Readability Spectrum 2026; Wang 2024; GitClear 2024/2025; repository census studies 2026). URLs at the end.

Contents: 1 the one-line finding; 2 measured characteristics; 3 human-side traits; 4 how AI-code detectors work and fail; 5 what similarity tools normalize away; 6 practical state in 2026; 7 sources.

## 1. The one-line finding

LLM code is more statistically regular than human code: higher likelihood under a code model, narrower vocabulary, more uniform line lengths, tidier whitespace, more and longer comments, spec-derived names, compact template-shaped functions. Detectors are, in effect, variance detectors. The second finding is that none of them generalizes: in-distribution F1 of 0.9 to 0.99 falls to near chance under new languages, domains, generators or human-edited hybrid code.

## 2. Measured characteristics of AI-written code

Token predictability and vocabulary:
- CodeLlama-7B mean log-likelihood -0.83 (machine) vs -1.66 (human); log-rank 0.32 vs 0.81. Machines prefer "a limited spectrum of frequently-used tokens" (DetectCodeGPT).
- After identifiers and literals are replaced by placeholders, human code still has the highest cross-entropy in every language (Python human ~0.95 bits/token vs GPT ~0.82, DeepSeek ~0.75): the structure is regular, not just the names (Improta 2026, 787k function pairs).
- AI corpora have ~7,800 fewer unique tokens and ~64 fewer tokens per function; "simpler and more repetitive" (Cotroneo 2025).
- Over 70% of code tokens have entropy below 1, so raw perplexity is weak; the signal lives in the high-entropy choices: naming, comments, layout (Ye 2024).
- Practitioner bands (Codequiry, Java method bodies, comments stripped, mean negative log-likelihood): human with natural comments 0.48 to 0.72; compact competitive human 0.31 to 0.47; GPT-4o 0.22 to 0.34. Human code is "bursty": ordinary runs punctuated by a jarring choice.

Formatting, whitespace, line structure:
- Whitespace tokens show the largest machine-vs-human naturalness gap of any token class (delta log-likelihood 1.61), comments next (1.53), keywords smallest (0.43). Perturbing only spaces and newlines gives AUROC 0.885 vs 0.544 for content perturbation (DetectCodeGPT).
- Whodunit (Python, GPT-4 vs CodeChef): average line length is the top feature, higher means GPT-4; lower line-length standard deviation points to GPT-4; empty-line density and whitespace ratio informative but "gameable".
- CoDet-M4 SHAP: "LLMs try to make the code more structured, separating its parts with empty lines, while people often do not"; more assignment operations; slightly less complex.
- Droid attribution: "consecutive empty lines and extra spaces" and punctuation drive decisions.
- Seven whitespace-only features give 88.5% accuracy; still 80.5% after Black formatting; TF-IDF of tokens 98.3% / 94.0% (Oedingen). Formatting explains only part of the gap.
- Blank-line inconsistencies in 99.2% of model samples vs ground truth; comment-formatting inconsistencies in 86.8% (Wang 2024).
- "Overblanking" (excess meaningless blank lines) is a novel LLM-specific readability pattern; LLM code scores higher mean readability but human code is more internally consistent (Readability Spectrum 2026).
- ChatGPT Java never emits a package declaration (GPTSniffer).
- Indentation cues are informative in Python, much less in C#, JavaScript, C++ (SemEval-2026).

Comments and documentation:
- Redundant comments 24 (LLM) vs 3 (human); deficient comments 60 (human) vs 10 (LLM) (Readability Spectrum).
- Comment ratio and verb-comment ratio were the two best features of one top-15% stylometric SemEval-2026 system; "text-like ratio" 0.07 human vs 0.17 LLM.
- Removing comments is the largest single ablation drop for Suh et al.'s best detector (F1 82.6 to 78.7) and costs commercial detectors far more than fine-tuned ones.
- Comments are the strongest cue for telling LLMs apart from each other (-7.2 points when removed).
- Counter-evidence: AI code is not reliably more docstring-complete (85% of GPT-4 outputs lacked complete docstrings vs 78% human on complex tasks); comment-ratio difference vs human in one Jira-issue study was statistically significant but negligible in size.

Naming:
- ChatGPT names functions from docstring keywords ~95% of the time; function names longer (Python 17.6 vs 13.6 chars; Java 18.9 to 19.3 vs 14.0).
- Higher frequency of AST Name nodes (identifier references) and shorter identifiers point to human (Whodunit).
- Not uniformly better: Pylint naming violations 72 (GPT-4) vs 65 (human); "redundant variables" (several names for one purpose) is a novel LLM issue.
- Renaming removes much but not all signal (random at 50% of identifiers replaced in one study; <0.4 F1 change in another).

Size, structure, repetition, defensive code:
- Function size roughly half: Python 12.7 NLOC human vs 6.9 ChatGPT / 5.2 DeepSeek / 4.5 Qwen; cyclomatic complexity 4.0 vs 2.5 / 2.0 / 1.8; Halstead volume 2 to 2.6x lower (Cotroneo; Improta). Maintainability index is "mechanically" higher because it penalizes size.
- Counter-evidence on small tasks: GPT-4 complexity 61% higher than human on 72 tasks; "excessive complexity" is the most frequent LLM readability issue in one study.
- Unused arguments: 33k (ChatGPT), 112k (DeepSeek), 213k (Qwen) findings on ~285k Python functions each; Java System.out.println 10k to 38k. Models replicate signature parameters without using them and leave debug prints.
- Idioms: built-ins where the ground truth calls repository functions; "rarely use Pythonic idioms"; deprecated APIs; humans use more list comprehensions (Wang 2024).
- Repository scale (GitClear): eightfold rise during 2024 in blocks of five or more lines duplicating adjacent code; copy-pasted lines exceeded moved lines for the first time; churn roughly doubled from 2021; "resembles a developer unfamiliar with the project".
- In the wild: near-identical insecure templates recur across unrelated projects; AI code concentrates in glue code, tests, docs and boilerplate.
- Security: Python vulnerable-sample rate 5.6% human vs ~8% ChatGPT; Java 3% human vs 19.6% DeepSeek; CWE-78 injection 2,243 human vs 13,419 ChatGPT findings.
- Agentic PRs: smaller, more localized edits, fewer files, less deletion, three to four times as many commits per PR.
- Model-specific signatures exist (Claude Code commits 1.95 issues per commit vs Devin 0.89; code smells 89% of AI-introduced issues).
- Community "slop" heuristics (deslop, DEV posts; no controlled evidence): docstrings on trivial functions, `total_sum_of_numeric_values_in_list` names, try/except around operations that cannot fail, triple null checks, empty catch blocks that only log, section-divider comments, `=== true`, redundant `return undefined`, "perfectly modular" tiny functions, no env/config/auth handling.

## 3. Human-side traits (what detectors read as human)

- Inconsistent style within a file (58 human vs 15 LLM cases), deficient or absent comments, structural and formatting issues.
- Shorter, more variable line lengths; irregular spacing; missing blank-line separation.
- More identifier references and shorter identifiers; project-specific helper calls; Pythonic shortcuts.
- Larger, more branching functions; protected-member access and generic-exception catching ("issues of mature codebases").
- Token-level burstiness.
- In classroom code: coding and spelling errors, unclosed resources, IDE stubs, use of only-taught methods.
- Not human-exclusive: TODO/FIXME comments (AI agents wrote 525 self-admitted-debt comments in one dataset) and debug prints.
- Hybrid (human-edited) code is where detectors fail: F-score correlates -0.43 with the share of preserved human code; hybrid recall 33% in CoDet-M4.

## 4. How AI-code detectors work and how they fail

Zero-shot:
- DetectCodeGPT: perturb spaces and newlines (Poisson insertions), score with normalized perturbed log-rank; average AUROC 0.83 vs 0.77 for log-rank; Python only, 128-token snippets.
- Yang 2023 (DetectGPT4Code): surrogate code LM scores only the final tokens after a long prefix; AUROC 71 to 80 on GPT-3.5/GPT-4.
- Ye 2024: have an LLM rewrite the code and measure similarity to the original; synthetic code changes less; AUROC 80 to 82 vs 55 to 65 for log-prob baselines.
- ATC 2025: condition token entropy on an inferred task description, exclude comments; AUROC ~93 vs ~56 raw entropy.
- Perplexity works for C/C++ (~91% AUC) but not Python (~64%) or Ruby (~73%); under 20 LOC accuracy ~70%.

Trained:
- GPTSniffer (CodeBERT, Java textbook exercises) 0.94 to 1.00 in-distribution, 0.62 cross-source; removing comments and package declarations improved accuracy, removing formatting hurt most.
- Whodunit (XGBoost on 140 stylometric features) F1 0.91; 0.89 without gameable whitespace features; style, not errors, carries the signal.
- CodeGPTSensor (UniXcoder contrastive) 0.99 Python / 0.97 Java on paired data; commercial detectors ~0.54 accuracy on the same set.
- Oedingen: whitespace features 88%, TF-IDF 98%; 20 untrained humans 48.7%.
- CoDet-M4 (UniXcoder) 98.7 F1 in-distribution; hybrid code recall 33%; JavaScript hardest.
- DroidDetect (ModernBERT, 1M samples, 43 models) 99.2 weighted F1 binary, 94 to 95 three-class; prior detectors' recall on adversarially prompted code: GPTZero 0.10, Fast-DetectGPT 0.48, GPTSniffer 0.49.
- LLMSniffer 2026 strips comments to force structural learning: 0.95 on Whodunit, 0.78 cross-domain.

Benchmarks:
- Suh 2024: text detectors 47.8 to 50.8% accuracy on code; best AST-embedding detector 82.6 F1 in-distribution, ~43 across settings; comment removal is the largest ablation drop.
- CodeMirage 2025 (10 languages, 10 production LLMs): TPR at 1% FPR generally below 0.3; "impractical for real-world use"; AST embeddings more robust than raw code embeddings.
- AICD Bench 2026 (2M examples, 77 models, 9 languages): best binary macro-F1 ~0.63 seen domain and language, ~0.20 unseen domain; hybrid samples mostly misclassified as fully AI.
- SemEval-2026 Task 13: encoders at 95 to 98 on validation fell to 25 to 49 on the cross-language test split; shallow AST and comment features were more stable.
- Pan et al. 2024 (education): GPTZero flagged 99.3% of all code as AI (TNR 0.0016); DetectGPT called most code human; five general detectors 0.49 to 0.61 accuracy; instructors by hand 69% accuracy with 22% false positives.

Ordering that holds across evaluations: fine-tuned encoders > hand-crafted stylometry > zero-shot perplexity > LLM-as-judge, but only in-distribution; under shift, shallow structural features often win. Detectors overfit to surface artifacts of a specific generator and domain.

## 5. What similarity tools normalize away (and what survives)

MOSS, JPlag, Dolos and Compare50 all reduce code to a structural token stream before matching:
- Normalized away: whitespace and layout, comments, identifier names, literal values and string contents, type names (JPlag, Compare50), access modifiers, `this.`, import order (partly), package names.
- Survives: the ordered sequence of statement kinds, nesting of control structures, the number and order of calls, assignments and declarations, method boundaries, and for MOSS/Dolos the exact k-gram of syntax-tree node types.
- Parameters: JPlag minimum token match Java 9, C/C++/Python/TypeScript 12, C#/Go/Kotlin/Rust/Swift 8; Dolos k = 23, window 17 (any shared run of 39 syntax tokens is guaranteed to match); Compare50 k = 25, t = 35 with identifiers mapped to `v`; MOSS ignores passages in more than 10 submissions by default and anything in the base file.
- Edits that change nothing in any tool: formatting, comments, renaming, splitting declarations, modifiers, constants, output strings.
- Edits that break matches: inserting statements every few lines, reordering independent statements or members, swapping loop forms, extracting or inlining methods, changing data structures. JPlag 5+ (token-sequence normalization, subsequence match merging) undoes much of this; PDG-based comparison is the most robust but not deployed in mainstream tools.
- Honest independent solutions to the same small task score 25 to 30% in MOSS and 44 to 87% on tiny Java exercises; unrelated pairs on larger projects score 0 to 6% in JPlag. Scores are relative to the class distribution, never a probability.
- LLM output converges: GPT-4 solutions to the same task show median JPlag similarity 20 to 31% against 0 to 6% for unrelated human pairs; 2026 algorithmic tasks: more than 75% vs 28%. A single model-written submission does not trip these tools; a cluster of them does.
- GitHub Copilot's duplicate-detection filter compares an accepted, unmodified inline suggestion plus about 150 characters of context against an index of public GitHub code (under 1% of suggestions match, more in empty files); Block suppresses them, otherwise code referencing shows repositories and licenses. It is an exact-match licensing check, not a similarity test.

## 6. Practical state in 2026

- No independently validated content-based AI-code detector exists. Vendor claims (Copyleaks 99.8%, Codequiry 90% with 1.3% FPR, Pangram 96.2% with 0.3% FPR on code over 40 lines) have no public test sets; Copyleaks deprecated AI detection for source files in December 2025; GPTZero documents no code mode; Turnitin analyzes prose only.
- Large-scale attribution of AI commits is metadata-based (bot accounts, Co-authored-by trailers, "Generated with Claude Code" lines, CLAUDE.md and .cursorrules files), not content-based; bot-account lookup alone misses 97% of Claude Code commits.
- Education is shifting to process evidence: version history, oral explanation, "pseudo-AI submission" similarity (instructor generates AI solutions and compares with Dolos), assessment redesign.
- Maintainers describe AI pull requests as "confident tone, plausible-looking code, and no awareness of project conventions", from cosmetic changes that add bugs to refactors nobody asked for.

## 7. Sources

- Caliskan-Islam et al. 2015, De-anonymizing programmers via code stylometry (USENIX): https://www.usenix.org/system/files/conference/usenixsecurity15/sec15-paper-caliskan-islam.pdf
- Shi et al. 2024, Between lines of code (DetectCodeGPT): https://arxiv.org/abs/2401.06461
- Yang et al. 2023, Zero-shot detection of machine-generated codes: https://ar5iv.labs.arxiv.org/html/2310.05103
- Ye et al. 2024, Zero-shot synthetic code detector via code rewriting: https://arxiv.org/abs/2405.16133
- Ashkenazi et al. 2025, Approximated task conditioning: https://arxiv.org/abs/2506.06069
- Efficacy of perplexity in detecting LLM-generated code (2024): https://arxiv.org/abs/2412.16525
- Nguyen et al., GPTSniffer: https://arxiv.org/abs/2307.09381
- Idialu et al. 2024, Whodunit (MSR): https://arxiv.org/abs/2403.04013
- Xu et al., CodeGPTSensor: https://arxiv.org/abs/2411.04704
- Suh et al. 2024, How far are we?: https://arxiv.org/abs/2411.04299
- Oedingen et al. 2024, ChatGPT code detection: https://arxiv.org/abs/2405.15512
- Orel et al. 2025, CoDet-M4: https://arxiv.org/abs/2503.13733
- Orel et al. 2025, Droid / DroidDetect: https://arxiv.org/abs/2507.10583
- LLMSniffer 2026: https://arxiv.org/abs/2604.16058
- CodeMirage 2025: https://arxiv.org/abs/2506.11059
- AICD Bench 2026: https://arxiv.org/abs/2602.02079
- SemEval-2026 Task 13 overview: https://aclanthology.org/2026.semeval-1.445/ and stylometric system: https://arxiv.org/abs/2605.04157
- Pan et al. 2024, Assessing AI detectors in identifying AI-generated code (ICSE SEET): https://arxiv.org/abs/2401.03676
- Wang et al. 2023, Student mastery or AI deception?: https://ar5iv.labs.arxiv.org/html/2311.16292
- Cotroneo, Improta, Liguori 2025 (ISSRE): https://arxiv.org/abs/2508.21634
- Improta et al. 2026, naturalness of human vs LLM code: https://arxiv.org/abs/2609.12708
- Readability Spectrum 2026: https://arxiv.org/abs/2605.13280
- Wang et al. 2024, Beyond functional correctness (style inconsistencies): https://arxiv.org/abs/2407.00456
- Jury et al. 2025, GPT-4 vs human code quality on 72 tasks: https://arxiv.org/abs/2501.16857
- GitClear 2025 via LeadDev: https://leaddev.com/software-quality/how-ai-generated-code-accelerates-technical-debt
- AI Code in the Wild 2025: https://arxiv.org/abs/2512.18567
- Agentic PRs vs human PRs 2026: https://arxiv.org/abs/2601.17581
- Census of AI agents in 180M repositories 2026: https://arxiv.org/abs/2606.24429
- Debt behind the AI boom 2026: https://arxiv.org/abs/2603.28592
- Codequiry perplexity bands (vendor): https://codequiry.com/blog/perplexity-thresholds-for-detecting-ai-code
- Pangram AI code detector (vendor): https://www.pangram.com/blog/ai-code-detector
- deslop heuristics: https://github.com/dabit3/deslop
- GitHub Docs, code referencing: https://docs.github.com/en/copilot/concepts/completions/code-referencing
- Sağlam & Schmid 2025, JPlag defenses and GPT-4 convergence: https://arxiv.org/abs/2505.20158
- Gacek et al. 2026 (CSEDU), structural convergence of AI solutions: https://badap.agh.edu.pl/publikacja/169730
