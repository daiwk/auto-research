# Review closeout: 2026-10-01 to 2026-10-07

<!-- source-sha256: cbc3974e4dfa2e59a6f38e9bb2d577a2c9a1102507f61034d1adb465d9eb2b4e -->

[简体中文](../../../research-audits/oct07-review-closure/README.md)

This is PR #195's frozen candidate-review snapshot. See the
[later source acceptance](../oct07-source-closure/README.md) for bounded criteria and supplemental checks, and [unified status](../../../paper-discovery-watermark.json) for the current watermark.

This review was checked on 2026-10-10. The publication window remains October 1–7.

Per-paper decisions retain the defining methods, evidence locations, and public reproduction limits. The accepted items were not implemented in this batch.
Broad query hits, abstract screening, full-text checks, and implementation are recorded separately.

There are **1022** deduplicated papers: 367 rejected or out of scope, 494 accepted pending implementation, 113 deferred after review, and 48 already recorded.

The old source-exhaustiveness watermark is retired. Its frozen field is historical, not current status.
See [unified status](../../../paper-discovery-watermark.json) for the current watermark, coverage, and archived exceptions.
See [implementation reconciliation](implementation-status.md) for current delivery. This snapshot's accepted count is not an implementation count.
See [official source receipts](../../../research-audits/oct07-review-closure/official-sources.json) and [the full per-paper register](../../../research-audits/oct07-review-closure/paper-register.json).

## Retrieval by track

| Track | Submission window | Supplemental ID-month retrieval |
|---|---:|---:|
| recommendation | 35 | 39 |
| foundation-model | 411 | 459 |
| post-training | 177 | 201 |
| agent | 396 | 437 |

The channels overlap; do not add these counts. ID-month retrieval runs independently to catch late-indexed records.
All eight receipts exhausted configured queries with zero failures and zero caps. This establishes API retrieval for this query matrix only,
not exhaustive papers or official sources. Accepted items received full-text checks; out-of-scope items could be screened out on the abstract.

## Accepted, awaiting implementation (494)

**2610.08791 · World Models' Last Exam in Physics**

[Paper](https://arxiv.org/abs/2610.08791)

- **foundation-model**: Forty physics-relation measurement tasks across nine phenomena; official images, prompts, evaluators and external video batch scoring support consideration as public evolve infrastructure, not a new world-model algorithm or completed integration.
  Reproduction scope: The official site returned 404, but GitHub was accessible. The paper attempts physical measurement when the gate fails; the public runtime instead returns with `physics_attempted=False`. Preserve the paper protocol and report coverage separately rather than treating the existing script as faithful. Difficulty labels are assigned post hoc from evaluated model averages; human agreement is only about 53%, not a physical truth oracle.
  Evidence locations: §2.1–2.4/Eq1–7; §3.1–3.3/Table2; official README; docs/evaluation.md; easy/P21/evaluator/_shared/unified_evaluators/runtime.py:339–355; evaluate.py:summarize

**2610.08779 · ALIVE: Interaction-Aligned Object Insertion for First-Frame-Guided Video Editing**

[Paper](https://arxiv.org/abs/2610.08779)

- **foundation-model**: ALIVE concatenates source and noisy target channels, uses a clean first frame and normalizes cross-attention by temporal overlap and description length. Qwen VLM predicts P4 from the same inputs rather than reading targets. Training uses 35,800 pairs and two benchmarks; some baselines get extra P2 prompts, so conditions are not fully matched.
  Evidence locations: §3; §4.2Eq. 2–4, §4.3Eq. 5; §5.1

**2610.08778 · Sherpa: Teaching LLMs to Teach Adaptively**

[Paper](https://arxiv.org/abs/2610.08778)

- **post-training**: A turn-wise gate masks returns with leave-one-out normalization among trajectories reaching the same turn. The teacher learns student preferences. MATH training and evaluation are separated, with a teaching benchmark.

**2610.08775 · Agent in a Bottle: Can LLM Agents Turn Their Capabilities Into Cheap, Scalable Artifacts?**

[Paper](https://arxiv.org/abs/2610.08775)

- **agent**: BOTTLED qualifies as executable evolve evaluation infrastructure: agents create reusable artifacts under a budget and solve many unlabeled tasks, with hidden gold and explicit limits compatible with models, scripts, and routers.
  Reproduction scope: Two runs per model/task and only 1000 zero-shot samples. GPU costs are not folded into the token budget. MIT code; MAVE CC-BY-NC4.0, ESCI Apache2.0, RAID MIT. Contamination judge and Jev evaluation are not public, so no complete contamination audit reproduction.
  Evidence locations: §3.1–3.5 Eq1–6; §4.1; Ethics/Reproducibility; official README and src/bottled/datasets/esci.py

**2610.08773 · AdvSim2Real : Training Web Agents Against Adaptive Prompt Injection in a Web World Model**

[Paper](https://arxiv.org/abs/2610.08773)

- **post-training**: Freeze the world model and judge; train curriculum–executor then adversary–executor. Three rollout seeds and 150 tasks are not production A/B.
- **agent**: Three policies and two stages: reward curriculum near p≈0.5; reward the adversary only for clean-success-to-failure flips; train the executor on fresh rollouts and reuse historical attack inputs. Candidate core Agent RL.
  Reproduction scope: Outcomes use only a world model and LLM judge. Stage 2 has no real browser test or executable safety claim. 150 custom form tasks; three rollout seeds are not training seeds. Post-attack feasibility is unverified. Removing Stage 1 is not compute matched, and robustness improved only 0.44pp.
  Evidence locations: §3 Environment/Threat Model/Metrics; §4 Algorithm1/Eq2–5; §5 Tables1–3; §6 Limitations

**2610.08718 · When Forgetting is not Catastrophic: On the Mechanics of Spurious Forgetting**

[Paper](https://arxiv.org/abs/2610.08718)

- **foundation-model**: Fine-tuning new facts separates shared representation drift from per-fact erosion. Removing the first singular component of the update has a same-norm random rank-1 control on OLMo2-1B; suitable for mechanism diagnosis, not a universal anti-forgetting algorithm.
  Reproduction scope: Old and new first answer tokens were deliberately disjoint, with one pretrained model. Mean diagnostic logits use known old facts, not a serving oracle. Select checkpoint and rank on independent validation when using only the weight intervention.
  Evidence locations: §4.1–4.4; §5.1–5.2/Figure5; §6/Limitations; Appendix D.2

**2610.08713 · SpaTime: Streaming Vision-Language Models for Spatio-temporal Reasoning**

[Paper](https://arxiv.org/abs/2610.08713)

- **foundation-model**: Freeze causal geometry and vision encoders, add projected 2×2 merges, train LoRA/state/head, and model first-Response timing. Strict counts earliest answers; charitable last-frame forced answers stay separate. Train on StreamVSTI and evaluate StreamVSI OOD tasks.
  Evidence locations: §4.1Eq. 5; §4.2Eq. 6–8; §5; §6

**2610.08691 · ScienceClaw: Benchmarking Continual Self-Evolution of AI-for-Science Agents Across the Natural and Social Sciences**

[Paper](https://arxiv.org/abs/2610.08691)

- **agent**: Freeze the model and extract linked Skill–Operator bundles from typed workflow execution and repair. Boundary/source reset replay must actually use the new version. Atomic promotion requires strict independent validation improvement and passing hard constraints/budgets. Candidate for a real evolve loop.
  Reproduction scope: Results are mainly final snapshots; §8 says broad conclusions need repeated runs and discipline-specific intervals. Domain evaluators can miss scientific mistakes. Require actual scientific tools and independent verification; fixed trajectories are not capability reproduction.
  Evidence locations: §3 Eq1–3; §4.1–4.2; §5.1–5.2 Eq5–13; §6 Tables1–2/Fig6; §8

**2610.08678 · Secure Speculative Decoding for Large Language Models**

[Paper](https://arxiv.org/abs/2610.08678)

- **foundation-model**: Mix strict/relaxed acceptance and rejection recovery distributions by global generation position, validating strictly early and quickly later. Defined sufficiently for genuine speculative decoding.
  Reproduction scope: No guarantee against arbitrary attacks. Match target/draft models and lossless, relaxed, and corrected arms; separate task quality from actual latency. Mainly measured on Blackwell, not verified on A100.
  Evidence locations: §IV-B; §V Algorithm 2 / Eq7–14; §VII-A paired protocol; §VIII Tables XII–XIII

**2610.08674 · EC-RAG: Event Chain Retrieval-Augmented Generation for Long Video Understanding**

[Paper](https://arxiv.org/abs/2610.08674)

- **foundation-model**: Decompose query modalities without training; sample frames by CLIP variance; build ASR/OCR/DET event descriptions and time-adjacent chains; use Contriever for related events and adjacent context. Three long-video benchmarks, no learned causal event graph. Count tools and tokens.
  Evidence locations: §3.1–3.4Eq. 12–16; §4.1–4.2

**2610.08670 · Principled Under Pressure: Post-Training Decides Whether LLMs Act on Their Own Moral Judgment**

[Paper](https://arxiv.org/abs/2610.08670)

- **post-training**: Public evaluation: judgment–action gap screening, four-level calibration, and pressure controls independent of training. Apache-2.0 DeepSteer is accessible. Only 74/208 main scenarios passed screening; conditional results do not generalize automatically.
- **agent**: Public evaluation: judgment–action gap screening, four-level calibration, and pressure controls independent of training. Apache-2.0 DeepSteer is accessible. Only 74/208 main scenarios passed screening; conditional results do not generalize automatically.
  Evidence locations: §3.1–3.5; Appendix F; author repository README and file listing checked read-only.

**2610.08662 · ParanoiaEval: Benchmarking Unnecessary Defensive Work in Agentic Coding**

[Paper](https://arxiv.org/abs/2610.08662)

- **agent**: ParanoiaEval qualifies as an evolve behavior-constraint benchmark: 200 matched E+/E− evidence pairs, with separate task oracle and unnecessary-defense judge to assess completion and evidence response.
  Reproduction scope: The public package lacks results and full traces. Only an independent scorer can read answer cards/reference patches. Native harness differences confound model-only comparisons. Developer study conditions on successful runs and is not live A/B. Keep default `same-task=none`; do not expose other-arm gold.
  Evidence locations: §4.1–4.3; §5; §7 Code/Data; official README, scripts/judge.py

**2610.08659 · Selective Transfer of RL Updates for Visual Reasoning**

[Paper](https://arxiv.org/abs/2610.08659)

- **foundation-model**: Separate R−B from B−V, use rank-1 SVD per matrix then restore original Frobenius norms, and reconstruct donor interpolation or directly add the RL delta. Three 8B VLM backbones; select donor on source validation and λ on H1 validation, freeze both, and preserve nonvisual module support alignment.
  Evidence locations: §3.1–3.3Eq. 1–3; §4.1; Appendix A Algorithm 1

**2610.08649 · Stable Scores, Unstable Answers: Frame Phase and Option Order in Video Multiple-Choice Evaluation**

[Paper](https://arxiv.org/abs/2610.08649)

- **foundation-model**: Map 3×8 frame-phase posteriors to content space and arithmetically average, independent of option-order control. With n=442, the 0.45pp gap versus 32 frames is not significant. Origin flips fall but order flips persist. Serial 3.18s exceeds 24-frame 2.86s; attention units are not measured speedups.
  Evidence locations: §3.2Eq. 2; §4 Table 1; §4.3

**2610.08647 · SquidAgent: Parallelize Wisely, Coordinate Efficiently**

[Paper](https://arxiv.org/abs/2610.08647)

- **agent**: Plan a DAG once with output-token and layer-alignment cost estimates. Fork sessions with inherited context and written conventions; parallelize when `sum(tokens)/(max(tokens)+alignment)>alpha`. Explicit executable scheduling mechanism.
  Reproduction scope: Mainly nine custom tasks and LLM rubrics. The token proxy suits generation-heavy work but omits tool/API latency. Alpha 1.9 comes from a MathRef sweep, not established independent validation. Local capability reproduction needs real LLM calls and cost, not fixtures.
  Evidence locations: §3.1–3.3 Eq1–10/Algorithm1; §4.1–4.6; Tables1–4main-text discussion

**2610.08639 · Forensic Reserve: Eliciting Latent Knowledge for Image Forgery Detection**

[Paper](https://arxiv.org/abs/2610.08639)

- **foundation-model**: Locate a reserve via site-wise ICA of frozen DINOv3 and real/fake discovery. Fix output basis U and train only zero-initialized A in residual `UA h`; freeze classifier/backbone and exclude benchmarks from discovery. Reusable visual adapter, with task-specific forensic evidence.
  Evidence locations: §3.1; §3.2Eq. 3; §4.1

**2610.08622 · Agentic RCA for Internet-Scale Services Using Constrained Creativity**

[Paper](https://arxiv.org/abs/2610.08622)

- **agent**: E4 constrains root-cause agents with fixed typed DAG grammar: pick playbooks, compose existing operators, then synthesize new operators. Actual execution and admission give a reproducible controller mechanism.
  Reproduction scope: §4.3 admits using true user root-cause feedback, permitted only in training/validation, never test gold. Accuracy@k,i allows repeated tries. Custom DSB is confounded by operator design. The 70 incidents in phase statistics differ from Table 3 totals, and caption ≤56% differs from 0.80 elsewhere; do not uncritically reuse headlines.
  Evidence locations: §3; §4.1–4.3; §6.1–6.5/Table3/Figs6–9; §8

**2610.08621 · Recursive Game Creator: An Agentic Product-Level Experience-Oriented Game Harness**

[Paper](https://arxiv.org/abs/2610.08621)

- **agent**: Recursive Game Creator combines design/build, executable multi-policy player rollouts, blinded version review, and actual artifact retention. Preference evidence informs later rounds under a fixed-model agent loop.
  Reproduction scope: Budgets are unmatched (three versus one round). User study reports expert scores and playtime but no strong randomized control. 97.1% coverage is not GUI speed; proxies do not represent population preference. Reproduction needs real games and policies without fixed gold traces.
  Evidence locations: §3.1–3.3; §4.1 Tables1–2; §4.2–4.4/Table3; §5

**2610.08586 · MINDSET: Energy-based Schema Evolution for Long Conversational Agent Memory**

[Paper](https://arxiv.org/abs/2610.08586)

- **agent**: Use immutable episodes and versioned schemas. A weighted energy over distortion, contradiction, history, fragmentation, and inconsistency selects reinforce/supersede/split/new, then expands raw retrieval evidence. A defined reproducible memory algorithm.
  Reproduction scope: Parameters are hand-tuned on development, not proven optimal. Development is question-disjoint but not proven conversation-disjoint. LongContext truncates at 20k bytes. Baselines are recreated and some upstream artifacts missing. Preserve the final stay margin rather than the switch margin for actions.
  Evidence locations: §3.1–3.7; §4.1–4.4; §5.1–5.5; Limitations

**2610.08560 · Have I Seen Enough? Frozen Video-Language Models Encode Evidence Readiness**

[Paper](https://arxiv.org/abs/2610.08560)

- **foundation-model**: Nested-CV logistic probes on frozen Qwen residuals predict evidence readiness. Stop on joint readiness/confidence at training quantiles, or choose highest readiness by deadline. Video holdout and crossed quads remove independent image/question shortcuts. Fixed-window policy does not read gold evidence times; annotated growing-prefix sampling is diagnostic, not deployment latency. §4.4 gives matched-video-seconds improvements.
  Evidence locations: §3.1–3.3; §4.4; Appendix C/H/I

**2610.08514 · How Much Evidence Should a Coding Agent's Self-Correction Carry? Adaptive Dirichlet Evidence for Self-Distillation**

[Paper](https://arxiv.org/abs/2610.08514)

- **agent**: EESD uses four public before/after execution transitions and lexical relevance to compute effective sample size `1/sum(p²)`. Dirichlet utility lower scores weight CE while forward KL stays unweighted. Candidate agent self-repair training mechanism.
  Reproduction scope: One same-source adaptation round is not source-disjoint generalization. Full update versus no update does not isolate effective mass or KL, and bootstrap is conditional on one training run. Effective mass measures relevance concentration, not repaired dependencies.
  Evidence locations: §3.1–3.3 Eq1–11; §4.1–4.4; §5

**2610.08463 · UNREAL: Unifying Retrieval and Long-Context with a Single Model**

[Paper](https://arxiv.org/abs/2610.08463)

- **foundation-model**: Use frozen decoder middle-layer chunk features, learn 64 retrieval tokens and cross-layer mixing for MaxSim, then re-encode selected text to generate. Includes multi-positive InfoNCE, public QA training split, and independent long-context validation.
  Reproduction scope: No oracle at test; only training hard-negative mining uses gold. The 100M regime is mainly sparse evidence; dashed latencies are FLOP extrapolations. Count offline encoding/storage and both forward passes. Baseline training budgets are not all matched.
  Evidence locations: §2.1–2.3 Eq1–7; §3/Table1; §4.2/Figure7; §6; Appendix B.1–B.3

**2610.08452 · Agentic AutoRAG: RAG Pipeline Optimization through Reasoning-Driven Agents**

[Paper](https://arxiv.org/abs/2610.08452)

- **agent**: Attribute retrieval/generation issues, diagnose them, then propose with KB and cost guidance. Defined evolve search candidate; accuracy uses 100 validation and 300 independent holdout items.
  Reproduction scope: Medical Pareto reports a repeatedly optimized exam, not holdout. Costs include generation/expansion API, not local embeddings/reranking. Combined no-KB/diagnosis ablation cannot isolate either. WarmTPE gets 30 free in-database trials and is not full syftr. No human agreement for judge.
  Evidence locations: §3.1–3.3; §4; §5/Table2; Limitations

**2610.08414 · Image Bitstream Fine-grained Understanding for Privacy-Friendly AIoT**

[Paper](https://arxiv.org/abs/2610.08414)

- **foundation-model**: BFG encodes JPEG bytes to 192 dimensions using ByteFormer hierarchical convolution/shifted windows, projects to 512, fuses global context with local cross-attention for autoregressive captions, and adds a 120-class head. CFU-D isolates source IDs/splits and tests substitution/deletion/repetition corruption. Dogs 58.51% uses ImageNet initialization; skipping decoding is not a privacy guarantee or broad foundation result.
  Evidence locations: §III-BEq. 2–5; §III-C; §IV-A–D Tables I/IV/V

**2610.08403 · SSR: Sparse Segment Reduction for Ternary GEMM Acceleration**

[Paper](https://arxiv.org/abs/2610.08403)

- **foundation-model**: SSR separates ternary matrices into positive and negative binary matrices, sorts column blocks by pattern, drops all-zero patterns, and replaces multiplication with segmented sums and tree reduction. Public C++/AVX2 code is verifiable.
  Reproduction scope: CPU results only; some high-sparsity settings are slower than CSC/Eigen. No paper GPU validation; unrelated GPU directories are not SSR evidence. Model results mainly give latency for a modified ternary MLP without public quality fidelity. Author README cites DATE2026; record this arXiv listing, not confirmed first publication.
  Evidence locations: §III-A/B Algorithms1–2; §IV-A/B; §IV-C TableIII; §V

**2610.08401 · GeoPID: Decomposing and Steering Visual Information in Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.08401)

- **foundation-model**: GeoPID estimates shared and modality-unique subspaces from unlabeled calibration features and amplifies vision-unique directions by `I+αUUᵀ`. Across 22×14 combinations, 100 separate labeled calibration questions per group select layer and α before freezing; final evaluation sees no gold. Rényi task decomposition is offline diagnosis, and the mean relative 7.63% must retain heterogeneity and regressions across 308 combinations.
  Evidence locations: §2.1–2.3Eq. 11; §3.1; §3.2 Table 5

**2610.08364 · Transect: Retaining Observability for Long-Horizon LLM Agent Evaluations**

[Paper](https://arxiv.org/abs/2610.08364)

- **agent**: Public executable evaluation observability: fixed family-Spec vocabulary, structural/judged scanners, provenance tables, and source-linked reports. Supports evolve audits, not task capability scoring.
  Reproduction scope: One descriptive case; agreement/repeatability is not accuracy. Reading a file does not prove adoption, source order is not wall time, and compaction proximity is not causality. Inspect machine-global caching can mimic repeatability; use fresh caches for independent judge repetitions. Extensions may call models.
  Evidence locations: §2.1–2.2; §3.1/3.3–3.5; §4; official README/API

**2610.08341 · DIPrune: Task-Aware Token Pruning with Dual Importance for Efficient Multimodal Language Models**

[Paper](https://arxiv.org/abs/2610.08341)

- **foundation-model**: DIPrune combines inverted text-to-vision attention rank normalization with truncated normalization of cross-layer rank gains, preserving tokens initially low-ranked but semantically important later and removing corresponding KV. Multiple VLM/video backbones and aligned-layer ablations. At 64 LLaVA tokens, retains 97.7% on average; POPE TTFT 73.23→32.50 ms, with 0.24 ms extra. Use measured TTFT, not FLOPs, for speed.
  Evidence locations: §5.1Eq. 6–7; §5.2Eq. 8; §6.1; §6.5 Table 4

**2610.08183 · Compact Robot Policies Need Fine-Grained Visual Representations**

[Paper](https://arxiv.org/abs/2610.08183)

- **foundation-model**: Train DINOv2 with a 48-query resampler/FiLM text and small flow DiT for actions. λ=.01 weights cross-layer task-classification CE, not an information bottleneck. Remove classifier after training and output action chunks with 10 Euler steps. LIBERO/RoboTwin are within task distributions; real hardware uses an additional private 10,000-hour/5,887-task pretraining corpus, not public simulation alone.
  Evidence locations: §3.1; §3.2Eq. 4–9; §4.1; §4.7; Appendix A.5

**2610.08164 · Align, Then Correct: Training-Free Two-Stage Low-Rank Compensation for Extremely Quantized Large Language Models**

[Paper](https://arxiv.org/abs/2610.08164)

- **foundation-model**: Two-stage low-rank compensation: asymmetric activation targets use full-output Fisher-weighted SVD, then rank-constrained SVD of the existing adapter plus K-FAC natural gradient. Stage two replaces rather than adds a rank-r adapter.
  Reproduction scope: Baselines share rank 64 and calibration source; stage two additionally uses 8K tokens and blockwise backward statistics, so not zero training compute. Separate calibration, validation, and test and evaluate held-out C4 plus task scores. Training-free means no iterative optimization, not no gradients.
  Evidence locations: §4 Eq5–13; §5 Tables1–5; §6

**2610.08162 · The Failure Is in the Readout: Fine-Grained Emotion Recognition Benchmarks Measure Elicitation, Not Perception**

[Paper](https://arxiv.org/abs/2610.08162)

- **foundation-model**: EmoNet audits first-token yes/no probabilities for 40 classes against free JSON generation, with answer mass and single-answer validity gates. Candidate multimodal evaluation diagnostic.
  Reproduction scope: Main κ calibration uses gold test marginals and is an oracle upper bound. Require independent calibration; report parse exclusions, prompt selection from two prompts, and class selection separately. FACES is posed expression, not inner emotion, requires research permission, and does not support inference of real individuals' feelings.
  Evidence locations: §3 Protocol; §5–7; Appendix Q

**2610.08159 · Making COMET Comparable Across Scripts: Diagnosis and Correction of Tokeniser-Induced Script Bias in Indic MT Evaluation**

[Paper](https://arxiv.org/abs/2610.08159)

- **recommendation**: COMET-QN studies Indian-language translation evaluation and script bias, not industrial recommendation. Rerouted to foundation review, not discarded.
- **foundation-model**: Public COMET script-bias diagnostics and rank-safe quantile calibration/LOLO correction are candidate evaluation-audit infrastructure, not a new LLM or integrated dynamic scorer.
  Reproduction scope: Repository recalculates statistics from committed COMET/TP/IP columns, with no GPU or model rerun. New candidates need a real metric. Quantile normalization assumes equal true-quality distributions and otherwise can erase differences; only wmt22-comet-da on five Indic scripts, without measuring this corpus's transliteration accuracy.
  Evidence locations: §6.1–6.4 Eq2–4; Limitations; official README Quickstart/three sample-size bases

**2610.08155 · Token-Efficient Multi-Agent Collaboration via System One-Guided Computational Division of Labor**

[Paper](https://arxiv.org/abs/2610.08155)

- **agent**: S1-MAS uses frozen Laya discrete decision encoding and Qwen 0.6B evidence localization; a lightweight controller chooses Solve/Decompose/Reverse/Review/Repair/Contrast and stopping. Defined collaborative compute-budget mechanism.
  Reproduction scope: Counts GPT input/output tokens but not total local Laya/Qwen compute, so savings are not total energy or total tokens. Code parsing validates an interface, not hidden-test correctness. Author code was not found. Laya has a specified revision and cannot be replaced with a heuristic.
  Evidence locations: §4.1–4.4/Alg1; §5.1–5.4 Tables3–4; Laya model-card reference

**2610.08133 · VLA-ACL: Action-Consistent Visual Token Pruning for Efficient Vision-Language-Action Models**

[Paper](https://arxiv.org/abs/2610.08133)

- **foundation-model**: Freeze the VLA and train only a five-layer patch scorer. Laplace soft Top-K has total mass K, with a square-root black-image embedding gate, L1 full-context teacher and ground-truth action consistency. Hard Top-K preserves RoPE positions at inference. LIBERO and real hardware/A100: K64 success 97.0 versus 96.8, 63.49→46.82 ms; retain K32 Long regression.
  Evidence locations: §III-A/BEq. 6–12; §IV Tables I; Appendix B

**2610.08108 · Enhancing Diffusion Language Models with Autoregressive Post-Training Weights**

[Paper](https://arxiv.org/abs/2610.08108)

- **post-training**: A2D task-vector transfer and AR/diffusion delta interpolation have checkpoint benchmarks. Coefficients used the anchor benchmark; local reproduction must isolate validation selection.

**2610.08106 · ChartBmkAgent: Harness-Governed Multi-Agent Construction of Chart QA Benchmarks from Sparse Error-Taxonomy Specifications**

[Paper](https://arxiv.org/abs/2610.08106)

- **agent**: ChartBmkAgent fixes error taxonomy and difficulty as immutable root constraints. The harness approves data, charts, mechanism anchors, and QA, with local repair or rollback. Candidate auditable evaluation data generation.
  Reproduction scope: 300 synthetic tasks; 40 paired seeds compare 31/40 to 21/40. Each stage permits at most four shared repairs/rollbacks beyond initial proposal. A universal path through anchors is a model judgment, not a proof. Generator is also evaluated and judges overlap, so not independent capability evidence. No official code/data link found in the body; require public taxonomy/prompts or label an independent implementation.
  Evidence locations: Method Eq1–5 / Algorithm1; Experiments Tables2–6; Limitations

**2610.08101 · Beyond Corrected Memory: Execution Consistency in Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.08101)

- **agent**: Separate obligation activation, coverage, and fulfillment. Return U for insufficient evidence instead of no violation. LLM extraction, deterministic rules, and a precommit read-refresh gate define an execution consistency mechanism.
  Reproduction scope: MissingL2 still labels 25/76 reference-U and 18/52 V as N. Gates only cover uncommitted side effects; committed ones need compensation. Stability on 146/180 reformatted traces is not full robustness; overhead +24.6% tokens/5 seconds. Supplementary snapshot and 432 constructed traces are stated, but no independently downloadable repository verified, so no public benchmark integration.
  Evidence locations: §3.1–3.2 Eq1; §4.1–4.3; §5.1–5.3; Reproducibility; AppendixE.5

**2610.08077 · Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight**

[Paper](https://arxiv.org/abs/2610.08077)

- **post-training**: Salesforce SRD converts success/failure trajectories to knowledge/pitfall foresight. A stopped-gradient current-model teacher sees trajectory and gold, supervises a student without privileged inputs, and uses auxiliary JSD. 4/9B on ten benchmarks; gold is teacher-training-only and not an inference input.
- **agent**: Salesforce SRD converts success/failure trajectories to knowledge/pitfall foresight. A stopped-gradient current-model teacher sees trajectory and gold, supervises a student without privileged inputs, and uses auxiliary JSD. 4/9B on ten benchmarks; gold is teacher-training-only and not an inference input.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; public artifact executability was not reverified here. Accepted as a research candidate, not an implementation.
  Evidence locations: §3.1–3.2 Eq.4–9; §4.1–4.2（PDF pp.3–6）

**2610.08076 · SpeedrunBench: Challenging LLM Agents with Video Game Speedrunning**

[Paper](https://arxiv.org/abs/2610.08076)

- **agent**: SpeedrunBench optimizes replayable action trajectories under fixed round and scoring-call budgets. Three public open-source games, pinned revisions, and isolated scoring containers suit public evolve evaluation.
  Reproduction scope: Use only public SuperTux, Tuxemon, and SuperTuxKart, not commercial ROMs. Prior harness leaked the SuperTux scoring key and STK seed; the official current version fixes it, so rerun rather than reuse scores. 200 scoring calls per round and no scorer are unmatched budgets. No root LICENSE shown; verify license before reuse. Readable code is not executed code.
  Evidence locations: §3.1–3.3; §4.1–4.2; §5.1–5.3; Ethics; official README: Changes / isolation / seeds

**2610.08048 · DAEDALUS: Bootstrapping Agent Memory from Self-Generated Tasks**

[Paper](https://arxiv.org/abs/2610.08048)

- **foundation-model**: DAEDALUS is agent-generated tasks and program memory, not a foundation model; reviewed under Agent.
- **agent**: DAEDALUS generates tasks that the Explorer actually completes, derives heuristics from failures, requires three consecutive successes after reset, adjusts difficulty, and injects a frozen library. Genuine memory generation/verification candidate for evolve.
  Reproduction scope: Three successes on one generated task are not independent generalization. LLM judge κ=.73–.81 and self-authored success conditions are not an oracle. Main cost table excludes one-time generation and assumes perfect prompt caching. Consolidation can lose scope; larger banks are not necessarily better. No user co-control and no stable gains from online updates.
  Evidence locations: §3; §4.1–4.2 Tables1–2; §5.1–5.3 Tables3/7; AppendixB; official GitHub contents

**2610.07990 · A Broader Look at Model Merging: Rethinking Implicit Regularization Induced by Task Arithmetic**

[Paper](https://arxiv.org/abs/2610.07990)

- **foundation-model**: S-RandOpt adds one auxiliary-gradient dimension to the task-vector subspace, then samples models; compares actual weight GD with coefficient GD. Candidate merging search mechanism.
  Reproduction scope: WeightGD trades more compute for quality and can regress with tiny auxiliary sets. Unlabeled-test TTA is transductive and must not be merged with frozen-model results.
  Evidence locations: §3.1–3.2; §4.1–4.2/Table2–3; §5.1–5.4

**2610.07987 · VisionWeave: Weaving Elastic Visual Representations as a Native Capability of MLLMs**

[Paper](https://arxiv.org/abs/2610.07987)

- **foundation-model**: VisionWeave learns a gated 2×2 pooler and intermediate ViT granularity router with fine/coarse MRoPE centers aligned. Three teacher top-512 forward-KL stages train pooler, soft-mix router, then hard-route pooler plus LLM; not OPD. A training subset calibrates 50% savings; eight benchmarks and SGLang dual-A100 long video show 2.30× throughput. Label the modified post-encoder FastV baseline.
  Evidence locations: §2.2–2.5; §2.3Eq. 10–12; §3.1; §3.4 Table 5

**2610.07972 · Can Agents Work for Everyone? Cross-User Reliability for Mobile GUI Agents in Personalized User Interfaces**

[Paper](https://arxiv.org/abs/2610.07972)

- **agent**: PAIR defines executable personalized GUI states; RePAIR normalizes advantages across four rollouts for cross-user UC subgoals. Accepted for exploration, with independent validation selection required.
  Reproduction scope: The 31 training specs were selected with historical baselines on test personas, so not strictly held-out. Validation did not select K8iter5; p10–p19 still lack semantic/browser audit. Freeze the visual encoder and train LoRA only. One training seed and round-derived seeds are not independent repetitions. Gold reference paths are only for reward/evaluation.
  Evidence locations: §4–5 Eq1–6; §6/Table2; Appendix RePAIR training/Selection and review scope

**2610.07940 · Hybrid Latent Attention for Looped Language Models**

[Paper](https://arxiv.org/abs/2610.07940)

- **foundation-model**: HLA shares rotary latent KV across loops while keeping an exact recent window. A frozen backbone with learned writer/reader and real same-engine vLLM/A100 speed/quality comparisons supports systems consideration.
  Reproduction scope: Decode only: 1K single requests are 26% slower and 4K ties. Two fine-tuning forwards versus one are not matched compute. Frozen RULER16K still loses 3.1 points; beyond 16K untested. Count added 0.35B/0.70B parameters.
  Evidence locations: §3.1–3.4 Eq1–4; §4.1–4.2; §5.1–5.5 Tables1–3; §6

**2610.07935 · SIGMA: Self-Improving Alignment Generalization from a Model Spec**

[Paper](https://arxiv.org/abs/2610.07935)

- **agent**: Apple/JHU SIGMA uses a same-model task designer, paired single-fact changes, spec/rubric self-acceptance, and generated supervision for self-improvement. Preserve actual judges and GRPO rather than fixtures.
  Reproduction scope: One self-improvement round; bootstrap intervals are not independent training seeds. Single-turn-to-agentic transfer is not all-domain OOD. Safety/helpfulness varies with specs, not just refusal. Eight-rollout SFT AgentMisalignment 3.8 and RL 9.0 differ; two-rollout SFT 1.1 shows non-monotonic scaling. Final-answer reward does not prove CoT monitorability.
  Evidence locations: §2.1–2.2; §3.1/3.6 Table4; §5/Ethics

**2610.07925 · TF-PRVR: Training-Free Partially Relevant Video Retrieval**

[Paper](https://arxiv.org/abs/2610.07925)

- **foundation-model**: TF-PRVR freezes the VLM, uses db4 DWT on frame-feature velocity direction changes for hierarchy, builds within-level semantic/temporal and adjacent-level IoU edges, then propagates by `(1−β)(I−βW)^−1` and takes max after per-time cross-scale averaging. Three datasets/backbones, fixed β=.7. Count offline matrix inverse and features; no new VLM training.
  Evidence locations: §4.2Eq. 1–4; §4.3Eq. 5–8; §5.1–5.3

**2610.07903 · Unsupervised Long-Tailed Adaptation of Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.07903)

- **foundation-model**: MARS learns prompts/text adapters on frozen CLIP: zero-shot visual prototypes detect unsupported probability shifts and fix weak targets with strong-view CE. Teacher soft frequencies and margin EMA control KL/pseudolabel CE. Nine datasets, γ=10/20/50, three seeds, unknown priors but known label set; not open-category discovery.
  Evidence locations: §3.3Eq. 3–6; §3.4Eq. 7–10; §3.5; §4.1/Table 1

**2610.07898 · FC-SWE: Failure-Conditioned RL for Long-Horizon Software Engineering Agents**

[Paper](https://arxiv.org/abs/2610.07898)

- **post-training**: Real R2E-Gym training resets after failure and supplies patch/verifier context. Attempts receive separate rewards; unexecuted padding contributes no advantage. SWE-bench is verifier-assisted, not standalone pass@K.
- **agent**: Real R2E-Gym training resets after failure and supplies patch/verifier context. Attempts receive separate rewards; unexecuted padding contributes no advantage. SWE-bench is verifier-assisted, not standalone pass@K.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; public artifact executability was not reverified here. Accepted as a research candidate, not an implementation.
  Evidence locations: §3.2–3.4Eq. 3–5; §4.1–4.2 Table 1

**2610.07887 · Visual Abstention in Unified Multimodal Models**

[Paper](https://arxiv.org/abs/2610.07887)

- **foundation-model**: VisTA on BAGEL trains feasible/infeasible pairs: reason then generate image or ABSTAIN; text CE for both, flow matching only for feasible inputs. Separate 38,224 pairs and 1,050 DoD image/maze pairs. Without reminder: 93.0% refusal, 0.8% false refusal, 74.3 edit. Paired minimal-change criteria do not establish real-world impossibility or safety alignment.
  Evidence locations: §3.1–3.3; §5.1Eq. 10; §5.2; §5.3 Table 5

**2610.07868 · CueRator: Agentic Search for Symbolic Rules to Adapt Frozen Multimodal Encoders**

[Paper](https://arxiv.org/abs/2610.07868)

- **foundation-model**: CueRator uses agent discovery of AST-constrained closed-form gates on frozen ImageBind. Per-video Sobol training oracles are structure upper-bound diagnostics; a Gaussian contextual policy predicts ten parameters with K4 leave-one-out REINFORCE. Select among 3×20 candidates on validation then test. No deployment access to oracle GT; encoder is frozen, training uses seen-only data, validation includes unseen.
  Evidence locations: §3.2 Algorithm 1; §3.4–3.6; §4.1; §4.2/Table 1

**2610.07862 · A self-learning scientific agent for X-ray diffraction**

[Paper](https://arxiv.org/abs/2610.07862)

- **agent**: Gan Jiang converts XRD execution residuals/failures into versioned skill edits, performs paired selection on development, and freezes before holdout. Candidate scientific-agent mechanism and DeltaXRDbench public evaluation; not the full closed toolchain.
  Reproduction scope: Full XMatcher is closed-source; basic only is public. Three skill arms edit different scopes without isolating individual edits or a full run/split/version manifest. XQueryer varies simulation seeds within structures, not unseen structures. opXRD includes private sources and synthetic mixtures are not real mixtures. Repository license is null; README requires a license before public redistribution. Confirm data-source terms individually.
  Evidence locations: Main self-improving workflows/Fig4; Methods Evaluation of self-improvement; Supplementary1.1/1.2/2.4; Data/Code availability; official DeltaXRDbench README/releases

**2610.07860 · WorkflowOps: Learning Agent Collaboration Priors for Multi-Agent Workflow Orchestration**

[Paper](https://arxiv.org/abs/2610.07860)

- **agent**: WorkflowOps combines MiniLM skill matching, new agents for low sufficiency, and first-order transition priors from synthetic workflows to add soft DAG edges and stage execution. An orchestration candidate, not proven continual evolution.
  Reproduction scope: Frequency is not causal success. Added edges can increase serialization; transitive reduction preserves reachability without creating executable concurrency. Future pool reuse is untested; baselines partly adapted (ADAS partial, MaAS deadlock). Main cost is 605 seconds/query, not low total cost just because matching saves calls.
  Evidence locations: §4 Alg1–2; §5 Tables1–2; §6 Limitations

**2610.07851 · RA-MoWE: Workflow-Affinity Embeddings for Query Clustering and Agentic Workflow Generation**

[Paper](https://arxiv.org/abs/2610.07851)

- **agent**: RA-MoWE uses offline outcome-affinity probes, clustered expert search, and BGE+MLP route prediction. Accept only the executable text-only Guided-BB path; isolate measured test affinity as diagnostic.
  Reproduction scope: A† uses test outcomes and is not deployable. B's three regimes have no prespecified significant gain; Haiku collapses 277/300 to one cluster, and SWE always picks direct. Guided-BB versus CoT .3295 CI crosses zero. Hj enters whole-cluster feedback, not independent search acceptance. Margin 2/n is not confidence, later analyses are exploratory, and a full matched guided/unguided comparison is missing.
  Evidence locations: §2 Eq1–4/Alg1; §3 Tables1/Fig3; AppendixB.2 Eq34/B.3/C.13

**2610.07848 · Dynamic Positional Attention Modulation for Parameter-Efficient Fine-Tuning of Large Language Models**

[Paper](https://arxiv.org/abs/2610.07848)

- **foundation-model**: DyPAM uses low-rank hidden features for RoPE-paired Q/K scaling with head/layer biases. Core PEFT formulas, validation checkpoint selection, and multiseed public tasks are present.
  Reproduction scope: Dynamic scaling cannot be merged offline like LoRA; matched parameters do not mean matched FLOPs. Pre-RoPE pair scaling changes amplitude, not angle. Verified official master README and finetune.py/eval.py/dypam_models.py entry points, but did not run code.
  Evidence locations: §3.1–3.6 Eq6–15; §4.1–4.4; App implementation

**2610.07832 · Harness Engineering for Software Engineering via Modular Executable Dev-Primitives**

[Paper](https://arxiv.org/abs/2610.07832)

- **foundation-model**: HERMES is a software engineering agent harness and resident LLM module design; review under Agent.
- **agent**: HERMES wraps persistent files as Dev-Primitives, activates by dependencies, directs messages, diagnoses execution, and reactivates for edits up to three rounds. Candidate file-level orchestration mechanism.
  Reproduction scope: F.8 mixes leaderboard and rerun matched baselines; 12.4pp average is not uniformly controlled. Resident files retain artifacts/messages, not hidden state. Oracle/reference precision/recall is diagnostic. No author code located; no local run claimed.
  Evidence locations: §3; §4.1–4.3 Tables6–7; Appendix F.4–F.8/G/I

**2610.07819 · $α$Transfer: Coefficient Transfer for Efficient Model Merging**

[Paper](https://arxiv.org/abs/2610.07819)

- **foundation-model**: alphaTransfer moves global/task/layer merge coefficients searched on a small proxy to a larger same-family model, copying/interpolating by relative depth. Actual task-vector edits run on the native larger model.
  Reproduction scope: Requires corresponding small and large expert checkpoints; saves coefficient search, not expert training. Cross-family/recipe transfer unverified; ViTB32→L14 AdaMerging++ loses 7.02 points, so not universally lossless.
  Evidence locations: §3 Eq1–8; §4.1–4.3 Tables2–3; Appendix A.1

**2610.07816 · Do I Need the Cloud? Uncertainty-Aware Step-Level Handoff for Small Language Model Agents**

[Paper](https://arxiv.org/abs/2610.07816)

- **agent**: StepGate trains calibrated routing from local-action counterfactual failure labels. Six feature types, thresholds/budgets, and on-demand agreement sampling choose local, verifier, or stronger model per step. Candidate actual model-routing mechanism.
  Reproduction scope: One Qwen2.5 family, with 7B 4-bit standing in for cloud. Risk features lack robust matched-budget gains; annotation is not authorization/safety and token locality is not privacy. Appendix A recommendations are not release evidence. Code/full 100-task release unverified. Original step baselines have unequal call rates; use rate-matched comparisons.
  Evidence locations: §3; §4 Tables1–4; Appendix A.3/A.6–A.9; Appendix C

**2610.07810 · SIFT: Search Intent-to-Filter Transformer for Multi-Task Personalized Filter Ranking at Airbnb**

[Paper](https://arxiv.org/abs/2610.07810)

- **recommendation**: SIFT qualifies through randomized identity routing and online hotel-expansion evidence. Filter clickers +20%; ordinary bookings +0.03% not significant; uncancelled marketplace bookings +0.76% in hotel expansion. Original journey/filter/capacity labels are private. Accepted does not mean implemented.

**2610.07809 · MASKerade: Token-Routed Mask Experts for Dense-to-MoE Upcycling**

[Paper](https://arxiv.org/abs/2610.07809)

- **foundation-model**: MASKerade trains expert binary masks and a token router on frozen FFNs, with true hard masks, STE, and top-1 retaining softmax probability for router gradients. Matched nominal active budget and mask-type comparisons support multimodal MoE adaptation.
  Reproduction scope: Nominal active parameters double-count overlaps and are not unique weights, FLOPs, or latency. Kernel reuse is future work; mask simulation does not demonstrate GPU speed. Control differing expert widths and learning rates separately.
  Evidence locations: §3.1–3.4 Eq1–9; §4.1–4.2 Tables1–3; §5; Appendix Table12

**2610.07774 · Reading, Not Manipulating: Leveraging Router Logits for Multimodal Safety in MoE Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.07774)

- **foundation-model**: Concatenate last-prompt-token router logits across MoE layers; train-standardize and fit class-balanced L2 logistic detection. After prefill reject at validation-selected τ=.4 or generate normally. Two MoE models, HoliSafe/OOD and MMMU. Readable safety signals do not imply steering control or router uniqueness; residual features also work.
  Evidence locations: §3.1Eq. 4–6; §3.2/Table 1; §4.1–4.4

**2610.07767 · TRACE: Rollout-Guided Quantization-Aware Training for FP4 Reinforcement Learning of MoE Language Models**

[Paper](https://arxiv.org/abs/2610.07767)

- **post-training**: Choose adjacent training activation FP4 codewords closer to rollout values and cache mantissa/scale. Tested with four MoE trainings. Native NVFP4 needs compatible hardware; an A100 simulation cannot claim native speed.

**2610.07758 · Later Is Better: Token Reduction for ViTs Under Distribution Shift**

[Paper](https://arxiv.org/abs/2610.07758)

- **foundation-model**: Late-concentrated power-law token allocation is an executable ViT/VLM compression operator with public official code. Multiple shifts/backbones and five reducers benefit under conservative iso-GFLOPs.
  Reproduction scope: §3's sentence saying late placement reduces FLOPs at equal budget contradicts the surrounding explanation; it should save less. Follow Appendix U. Default gamma uses same-main-benchmark sensitivity; use independent validation. Appendix V batch-64 throughput at two widths is not universal iso-latency. Some components are noncommercial; video/VLM harness release unverified.
  Evidence locations: §3 Eq1; §4–5 Tables1–6; App A/U/V; official README

**2610.07739 · Cite What You Explore: Budget-Aware LLM Reasoning over Medical KGs with Verifiable Evidence**

[Paper](https://arxiv.org/abs/2610.07739)

- **post-training**: Snapshot-matched loss differences with and without evidence define paired gain, with budget and citation integrity. Train the retrieval reasoner with REINFORCE. Needs real MIMIC/PrimeKG mappings, not hand-written scores.

**2610.07731 · Learning to Retrieve via Reinforcement Learning in Embedding Space**

[Paper](https://arxiv.org/abs/2610.07731)

- **post-training**: vMF embedding policy, G×G product rollouts, RLOO, and CMP projection denoising. ReasonRank training, BRIGHT evaluation, and three paired seeds.

**2610.07729 · Foveated Compression: Selective High-Resolution Preservation for Token-Efficient VLMs**

[Paper](https://arxiv.org/abs/2610.07729)

- **foundation-model**: Foveated Compression defines mixed-resolution representations and tie-aware region selection, suitable for token-compression diagnostics; do not turn test-oracle or worse-than-resize results into gains.
  Reproduction scope: The full vision encoder still runs; 20.99% tokens is not end-to-end compute. Question ablation gives no gain. Cached teacher top-256 is not exact full KL. Bootstrap is over examples, not training seeds. Decoder uncertainty arrives after generation and is not free prefill input. Author repository or code not found.
  Evidence locations: §3 Eq1–5; §4 Tables1/2; §5; App A.1–A.3/D

**2610.07706 · WASD: Wasserstein-based Knowledge Distillation for Large Language Models**

[Paper](https://arxiv.org/abs/2610.07706)

- **foundation-model**: WASD uses debiased Sinkhorn divergence with teacher-embedding costs and detached potential differences to optimize student probabilities. Official train/eval scripts and equal-wall-time comparisons exist.
  Reproduction scope: Ten finite iterations and sparse support approximate, not guarantee, exact OT gradients. Roughly 2× training time and 20% memory are not free; five evaluation seeds are not five training seeds. Freeze temperature 2 and judge/ROUGE choices. Shared vocabulary assumptions do not extend automatically across tokenizers.
  Evidence locations: §3.1–3.2 Eq6/10–11 Algorithms1–2; §4.1–4.2; AppC/E; official README

**2610.07689 · Unlocking Fine-Grained Perception in CLIP via Structurally-Aware Latent Masked Modeling**

[Paper](https://arxiv.org/abs/2610.07689)

- **foundation-model**: SALM adapts CLIP with patch relations and norm-difference matrices plus masked reconstruction of teacher latents; SALM-Self removes the external teacher. Core losses and curriculum are specified.
  Reproduction scope: Same size is not matched compute; RADIO is an ImageNet-1K retrain, not the full-scale original. Isolate validation tuning and seed uncertainty; teacher structure can limit results. Official site links the paper/method only; author code not found.
  Evidence locations: §3.2–3.6 Eq1; §4.1–4.4; App A.1–A.3/C; official project page

**2610.07657 · Where Rules End and Judges Begin: Measuring the Judgment Boundary in Multi-Agent Systems Security**

[Paper](https://arxiv.org/abs/2610.07657)

- **agent**: DEFER runs 27 deterministic/similarity checks before a residual LLM panel for host tool and memory safety. Four-domain testbed and outcome oracle, with MIT code, attacks, benchmarks, logs, scripts, and tests, qualify as safety-evaluation candidates.
  Reproduction scope: Hand-tuned CyberOps is a development upper bound; domains reuse one skeleton. Static attacks, stub tools, and synthetic memory. Offline panel readjudication mainly checks direct effects without regenerating downstream traces. Separate v3.1 main results from v2.2/v2.9 third-party or other models; no ACL-plus-judge baseline. Code not run; no safety guarantee.
  Evidence locations: §II–V; §VI-A/VI-B4/VI-C; §VII-B; official README/provenance/contents/license

**2610.07654 · Does On-Policy Distillation for Safety Pose Backdoor Risks?**

[Paper](https://arxiv.org/abs/2610.07654)

- **post-training**: Lazy Defense clips sampled teacher–student token log-ratios on both sides and detaches them. Four combinations only delayed backdoors; they do not guarantee removal.

**2610.07645 · SkillPoison: Progressive Skill Poisoning via Successful Experiences**

[Paper](https://arxiv.org/abs/2610.07645)

- **agent**: SkillPoison exposes governance failures when successful experience becomes a skill outside its valid conditions. Candidate defensive skill-promotion regression and diagnostic, not a capability-improvement policy.
  Reproduction scope: Filter irrelevant categories before freezing the pool; ASR is not unconditional across the full benchmark. Adoption uses self-report or code-pattern proxies, not causality. Public README covers experience generation only; victim skill extraction, frozen task set, and downstream ASR evaluator were not verified together. Not executable evolve integration. No real-system attacks or attack code were run.
  Evidence locations: §3.1–3.4/Eq2–10; §4.1–4.4; Appendix B.1/B.3 Eq13–16/C; official repository README/LICENSE

**2610.07643 · Monte Carlo Estimation for KV Cache Eviction**

[Paper](https://arxiv.org/abs/2610.07643)

- **foundation-model**: Sample short continuations from a frozen model to estimate future queries, weight them by centered log-probability, entropy, and disagreement, then select KV by counterfactual deletion cost after output projection. Discard sampled continuations.
  Reproduction scope: Attention scores alone are not this method. Count one-off lookahead/scoring cost and match cache and lookahead-token budgets. True future queries are diagnostic only, never online selection input. Unseen continuation quality is not guaranteed.
  Evidence locations: §3.1–3.5 Eq1–8; §4.1–4.5; §5 / Reproducibility statement

**2610.07639 · HarnessSecurity-Bench: Do Security Mechanisms Really Protect Coding Agent Harnesses?**

[Paper](https://arxiv.org/abs/2610.07639)

- **agent**: HarnessSecurity-Bench pairs ON/OFF native defenses on fixed legitimate tasks with separate deterministic utility and attack-effect oracles. Suitable for isolated offline harness regression.
  Reproduction scope: 23 tasks, nine mechanisms, six harnesses, one GLM-5.2, ten runs per combination. Excluding unknown oracles requires reporting coverage. Official repo has tasks and utility checks; full runner is maintained separately, so not fully reproducible. Keep attacks inside isolated synthetic canaries, never real credentials or external services. Root license unlisted.
  Evidence locations: §5.1–5.5; §6.1; §7.1–7.3; Data Availability; official README

**2610.07587 · Large Language Model Orchestration under Heterogeneous Preferences via Explicit Persona Inference**

[Paper](https://arxiv.org/abs/2610.07587)

- **post-training**: HARP uses external Bayesian persona posteriors and planning exploration rewards. This is primarily inference-time multi-agent orchestration, not parameter post-training.
- **agent**: A finite persona library and calibrated offline response scorer update each agent's Bayesian posterior, with posterior sampling for central planning. HARP+ adds reward disagreement. Candidate exact mechanism diagnostic, not open-dialogue improvement.
  Reproduction scope: Smaller beliefs do not shrink the planner. Fixed personas and response locality/independent priors are strong assumptions. After Appendix A.1 fixed static posteriors, all open-dialogue HARP lower CIs in 30 cases × four repetitions were nonpositive; updating posterior still did not improve scores. No provider seeds, and cached replay is not seed matching. Author repo not found.
  Evidence locations: §3.1–3.3 Algorithm1/Eq2–3/Assumption3.1; §4.1–4.3; Limitations; Appendix A.1 open-text boundary

**2610.07585 · REViT-v2: Hierarchical Windowed Roto-reflection Equivariant ViT for Equivariant Feature Extraction**

[Paper](https://arxiv.org/abs/2610.07585)

- **foundation-model**: REViT-v2 uses group-equivariant QKV convolution, full representation-field multihead local windows, and group-convolution downsampling, with O(NM²C) rather than global N². ImageNet and RotMNIST include a same-stem global control. Preserve finite p4m group and window geometry; no arbitrary-angle exact equivariance claim.
  Evidence locations: §2.1–2.3Eq. 1–6; §3; §4 Tables 1–2; Appendix A

**2610.07572 · Two Vectors Replace In-Context Demos: Structured Task Adaptation via Embeddings**

[Paper](https://arxiv.org/abs/2610.07572)

- **foundation-model**: STAVE adds two vectors to structured frozen LM/LMM inputs with paired demo/no-demo supervision, genuine 2d adaptation rather than gold inference or per-layer simulation.
  Reproduction scope: Per-task supervised training, not true zero-shot. Table 1 uses validation and best epoch, not independent test; Tables 2/3 have holdouts. Backpropagation through frozen weights still has activation cost. First-token gold diagnostics do not establish free generation. No source entry located in the paper.
  Evidence locations: §3.1–3.4 Eq2–7; §4.1–4.3; AppJ

**2610.07557 · CheckerBench: Can Long-Horizon Agents Synthesize Static-Analysis Checkers?**

[Paper](https://arxiv.org/abs/2610.07557)

- **agent**: CheckerBench/CheckerLab builds static analyzers from patched and vulnerable code, freezes artifacts, and independently rebuilds and checks differential behavior, false positives, and semantics. Public 300-task package and pinned Linux runtime suit code-agent evaluation.
  Reproduction scope: 50 minutes/task and 21 configurations × three runs. Pilot human guidance permits up to two reruns and selects successful traces of at least 40 steps, not an unbiased distribution. Do not mount holdout verifiers/references to agents. Opus5 contributes semantic/false-positive review, and efficiency conditions on successes. Official minimum disk is 100 GB. Third-party terms remain separate.
  Evidence locations: §3.1 stages I–VI; §4; §5.1–5.2; official README

**2610.07533 · SkillFormer: Skill-Decomposed Adaptation for Audio Language Models**

[Paper](https://arxiv.org/abs/2610.07533)

- **foundation-model**: SkillFormer clusters question embeddings into six skills, uses parallel rank-16 adapters and top-2 question routing, trains 500 steps per cluster then 2,000 balanced joint steps. 50k QA, three audio models/benchmarks. §2.4 Phase B explicitly unfreezes the LLM despite Phase A 'throughout' wording; reproduce phases and report trainable parameters, not LoRA-only throughout.
  Evidence locations: §2.1–2.4Eq. 1–3; §3.1–3.4 Table 1

**2610.07532 · Safeguarding LLMs via Model-Agnostic Latent Safety Signals from Dark Knowledge**

[Paper](https://arxiv.org/abs/2610.07532)

- **foundation-model**: LADE selects safety tokens by harmful/benign first-token probability differences, maps first valid subtokens across tokenizers with duplicate weights, and gates using kNN distances from L1-normalized features to harmful references. Implementable defense mechanism.
  Reproduction scope: Hex-Phi/XSTest are extraction/threshold data, not holdout. K5/k500/quantile 0.9. Needs safety-aligned models and log-probabilities; over-refusal and adaptive known-token bypass remain. Verify reference self-distances and non-conservative duplicate mappings. Author code not found.
  Evidence locations: §3.1–3.3 Eq1–5; §4.1; Appendix M

**2610.07522 · Activation Denoising: A Robustness View on Parallel vs Sequential LLM Quantization**

[Paper](https://arxiv.org/abs/2610.07522)

- **foundation-model**: Estimate H/C/N second moments with clean/noisy forwards, linearly pretransform weights, then apply GPTQ/QuIP# rounding under the new metric so layers can quantize in parallel.
  Reproduction scope: Original tuning uses WikiText-2 test perplexity, not leakage-free. Add independent validation and freeze settings. Noise is propagated per-channel Gaussian approximation, not arbitrary independent layer noise. Parallelizability is not measured single-GPU speed.
  Evidence locations: §4 Eq2–3 / Algorithm1; §5 Algorithm2; §6 Setup/Metrics/Table1; §7
- **post-training**: Parallel PTQ activation denoising and error regularization are quantization, not RL/OPD post-training.

**2610.07457 · AlignQuant: Tile-Aligned Mixed-Precision Quantization for Efficient LLM Generation**

[Paper](https://arxiv.org/abs/2610.07457)

- **foundation-model**: AlignQuant aligns assignment, packing, and GPU execution to 64×64 tiles. Normalize prefill/decode Fisher sensitivities separately, take their max, use 4 bits for low-sensitivity tiles and 8 otherwise. Real integer execution is essential.
  Reproduction scope: Fake quantization does not implement speedup. Real CUDA/CUTLASS, packing bytes, transforms, and workspace costs matter; TTFT may be worse than BF16. Paper A100 results do not replace local hardware acceptance.
  Evidence locations: §3.1–3.3 Eq1–3; §4.1–4.4 Tables1–3; official README
- **post-training**: GPU-tile mixed-precision PTQ and kernels, not policy post-training.

**2610.07389 · Inference and learning in sparse autoencoders as natural gradient flow**

[Paper](https://arxiv.org/abs/2610.07389)

- **foundation-model**: BeFOND casts Bernoulli sparse inference and dictionary learning as natural-gradient flow, with closed-form updates, executable official core, and public SAEBench tasks. Candidate representation diagnostic/intervention.
  Reproduction scope: Training takes 12–14× BatchTopK time per token; 1000× is the 6M/8B token ratio, not FLOP savings. ZCA uses 500M additional training tokens. One LM layer, and rare-feature compensation assumes frozen matched moments. Pin paper ETD1 via PAPER_MODELS rather than default `etd1_guarded`. Pretrained checkpoint unreleased; toy tests are not Gemma interventions.
  Evidence locations: §3 Eq9–17; §5–6; App B.6–B.7 Algorithm1; App D.1–D.3 Tables7/10; official README

**2610.07385 · Semantic Capability Acquisition and Specialization During Vision-Language Model Fine-Tuning**

[Paper](https://arxiv.org/abs/2610.07385)

- **foundation-model**: SSR isolates NAME and ATTRIBUTE routes during causal training, fuses summaries, and optionally drops NAME with probability .5; evaluation restores ordinary EOT. P3 without names and CAPP counterfactuals test description readability. Six CLIP-like models across datasets; P3 trajectory peaks are retrospective, not selection, which should use P1. Missing fork revision and subset generator limit exact reproduction.
  Evidence locations: §3; §4.1–4.4; Appendix B（class subsets）, training environment

**2610.07376 · MemCo: Memory-Centric Collaboration for Generalizing LLM Agents to Unseen Environments**

[Paper](https://arxiv.org/abs/2610.07376)

- **agent**: MemCo extracts contextual rules from local trajectory graphs, aggregates episode-reduced positive/negative evidence by exact abstracted role keys, promotes/retracts global records with Wilson scores, and retrieves by state, phase, and goal before grounding. Candidate core agent memory.
  Reproduction scope: Unseen means one agent did not collect a domain; other agents may know it. Distinguish layout holdout. Wilson is approximate binomial and episode deduplication does not guarantee IID. Same-snapshot ablations are not independent. NOTICE says upstream GMemory lacks a license and redistribution is unconfirmed. Artifact excludes models, generated memories, and logs.
  Evidence locations: §3.1–3.5 Eq2–10; §4/4.2; §6; Appendix D.1/F.1; official README/NOTICE

**2610.07349 · RELACE: retrospective likelihood-based action credit estimation for long-horizon language agents**

[Paper](https://arxiv.org/abs/2610.07349)

- **foundation-model**: RELACE is multi-step agent RL credit assignment, reviewed by post-training/Agent.
- **post-training**: Correct local returns with ratios between original and outcome-conditioned action likelihoods. Terminal outcomes are training credit only. Real ALFWorld/WebShop training, but literature baselines mixed into main tables require matched local controls.

**2610.07348 · Stepped MoE: Segment-Level Routing with Configurable Inference Complexity**

[Paper](https://arxiv.org/abs/2610.07348)

- **foundation-model**: Use the first 12 dense layers to predict expert sets for the remaining 44, refresh on each segment's first token, and train budget embeddings with loss scaling across sparsity levels. Real 12B, 1T-token training supports variable-compute consideration.
  Reproduction scope: Throughput uses an NPU simulator with measured matmul/NAND parameters, not on-device end-to-end. Training costs nearly four static models, so 1T tokens is not one dense run's compute. Authors call loss scaling a simplified proxy, not exact frequency-adjusted LR.
  Evidence locations: §2.3–2.5 Eq1–3; §3.1/Tables1–3; §3.4/Figure3; §5

**2610.07338 · Logbook: Extremely Long-form Audio Event Understanding**

[Paper](https://arxiv.org/abs/2610.07338)

- **foundation-model**: Meta Logbook segments continuous audio with full coverage and descriptions: 10-minute end-to-end or 10-second captions to 10-minute text, across Ego4D/SINS/EgoLife. Main segmentation uses fAcc; description uses OLMo atomic facts and overlapping-segment BART MNLI dF1. Human references include vision/LLM labels and are not an upper bound; PFLOPs are estimates. Official loaders/prompts/run_e2e/run_cascade and evaluation support a public audio evaluator.
  Evidence locations: §2.1–2.4; §3; §4.1–4.2; official README Repo layout; README: Repo layout / scripts/run_e2e.py / run_cascade.py / eval_segmentation.py / eval_descriptions.py

**2610.07335 · Selective Critique for Cost-Aware LLM Agents in Long-Horizon Decision Making**

[Paper](https://arxiv.org/abs/2610.07335)

- **foundation-model**: SAG selective critique is for long-horizon agents; review under Agent.
- **agent**: SAG gates a gold-free critic using entropy and top-two margin of length-normalized executable-action likelihoods. Every ten successful episodes, rerun LoRA-SFT from the same base on accumulated pairs. Genuine gating and online learning candidate.
  Reproduction scope: Sequential test-time adaptation uses earlier successful test trajectories to train for later episodes, not frozen holdout evaluation, and never retests old episodes. Token efficiency excludes training and full candidate likelihood cost. WebShop limits clicks after initial search. Pin settings because public WebShop 500/BabyAI 50 differ from paper 200/100. Null license is not permission to redistribute.
  Evidence locations: §3.1–3.4 Eq1–4; §5; Appendix G.1–G.3/H.3–H.5; official README

**2610.07332 · Structuring MoE Expert Selection for Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.07332)

- **foundation-model**: Agentic RL combines operation-label/router mutual information, adjacent-token expert-set consistency, and an entropy gate. Actual AppWorld/AutomationBench training; cannot replace model routing with a proxy.
  Evidence locations: §3.1–3.3; §4.1
- **post-training**: Agentic RL combines operation-label/router mutual information, adjacent-token expert-set consistency, and an entropy gate. Actual AppWorld/AutomationBench training; cannot replace model routing with a proxy.
- **agent**: Agentic RL combines operation-label/router mutual information, adjacent-token expert-set consistency, and an entropy gate. Actual AppWorld/AutomationBench training; cannot replace model routing with a proxy.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; public artifact executability was not reverified here. Accepted as a research candidate, not an implementation.
  Evidence locations: §3.1–3.3; §4.1

**2610.07324 · Scale-Invariant Training for Time Series Foundation Models**

[Paper](https://arxiv.org/abs/2610.07324)

- **foundation-model**: ScaleIn evaluates loss in context-normalized target space as a candidate time-series foundation training configuration. It audits an existing practice theoretically and empirically, not a new network.
  Reproduction scope: TimesFM 49.6M is narrower and shallower and lacks the quantile head, unlike original 200M. Supervised mean improvements are only 1.9% MASE and 1.1% WQL. Arcsinh is not just a b^p ratio; preserve fixed statistics and bias. No official paper code located; Appendix C permits independent implementation.
  Evidence locations: §3 Eq1–10/Theorem3.2; §4.1–4.4 Tables3/4; App C/G.1/H

**2610.07311 · Understanding and Mitigating Inference-Time Overreliance Using Agentic Memory**

[Paper](https://arxiv.org/abs/2610.07311)

- **agent**: MemTrim uses an LLM to normalize atomic evidence with task signatures and answer support, indexed in a separate key-value trie. Remove duplicate or contradictory evidence, suppress stale answers when support changes, and allow typed reuse across task changes. Candidate memory governance.
  Reproduction scope: Unconditional current-query priority is a trust assumption, not suitable for attacker queries or universal defense. LLM support/entity canonicalization does not prove causality. Overlap sweeps also restore answer-relevant information, not isolated repetition effects. Write parsing is amortized; runtime is reads plus generation. No author code found; an independent parser cannot be a fixture.
  Evidence locations: §2; §3.1–3.3 Eq1; §4.1–4.4; Appendix A.1/C benchmark construction

**2610.07289 · Catching Developers in the Flow: Low-Latency Agentic Program Repair at Google Scale**

[Paper](https://arxiv.org/abs/2610.07289)

- **agent**: Google FlowAgent combines pre/post execution filtering, ReAct generate-and-validate, and final tests for low-latency presubmit repair. Core candidate accepted, not implemented.
  Reproduction scope: Not randomized A/B; adoption is selective. Internal Gemini, data, and code are private, so public APR alternatives can only verify mechanisms independently.
  Evidence locations: PDF pp1–10; §3; §4.1; §4.2/Table2; §5; Data Availability

**2610.07261 · Verifying Coordination in Parallel Coding Agents: NP-Bench and a Scheduling Planner**

[Paper](https://arxiv.org/abs/2610.07261)

- **agent**: Nerveplane passively watches Git, colors file-scope conflicts into batches, and orders merges by contract dependencies. NP-Bench includes real Git integration and live coding agents, suitable for parallel evolve collaboration evaluation.
  Reproduction scope: Scopes and dependencies are supplied manually; DAG claims do not cover cycle breaking. Tier A scripts are diagnostics and live cases are simple with 3–15 seeds. The planner receives exact contracts beyond baseline information, confounding amount and timing; no universal 100% coordination claim.
  Evidence locations: §3–5 Algorithm1; §6.2–6.3; §9/reproducibility

**2610.07258 · Lineage-Aware Memory Governance: A Derivation-Gated Framework for Privacy-Preserving Column-Level Access Control in Enterprise AI Agents**

[Paper](https://arxiv.org/abs/2610.07258)

- **agent**: Lineage-aware governance labels sensitive-column derivatives, retrieves the newest safe memory, and flags definition-hash conflicts. Reproducible shared-agent memory diagnostic, not production safety.
  Reproduction scope: The theorem assumes complete lineage, pre-authorized fresh computation, and current policy tags. Cache key is the metric, not semantic definition; conflicts warn but do not block. Only registered sensitive columns are covered, not all ACLs. View/UDF lineage can fail silently; fail-closed applies only to detected errors. Simulation is not capability. Code is promised as future open source without a URL, so independent work is not author reproduction.
  Evidence locations: §III-A–C algorithms/Eq1–2; §IV Theorem1/Corollary3; §VI-A–E TablesVI–VII; §VII-B; §VIII

**2610.07247 · Learning What to Distill: Bilevel Top-K Token Selection for Self-Distillation in Large Language Models**

[Paper](https://arxiv.org/abs/2610.07247)

- **post-training**: Soft-OR utility, softplus inner threshold, and soft masks form approximate bilevel selection; detach threshold and use full-vocabulary forward KL. Final checkpoint at 200 steps. TIP comparison also changes divergence and does not isolate selection.

**2610.07212 · Reward-Driven Learning under Prompt-Level Differential Privacy**

[Paper](https://arxiv.org/abs/2610.07212)

- **post-training**: DP-GRPO clips each prompt group as one DP-SGD record with one-update GRPO record loss. Privacy accounting and actual Qwen 1.5B LoRA go beyond a noise demonstration.

**2610.07191 · Agentic Design Space Exploration for Joint Hardware Configuration Selection and Mapping of AI Inference Workloads on Heterogeneous Edge SoCs**

[Paper](https://arxiv.org/abs/2610.07191)

- **agent**: TraceDSE forms a measured search loop: real hardware traces, tool-based critic, proposer, and Pareto/exploration state. Candidate evolve mechanism.
  Reproduction scope: Energy uses a window of 50 inferences minus idle, not one instant reading. Across-algorithm Pareto-max normalization uses observed outcomes. Critic estimates miss contention; verify execution. A substitute simulator cannot reproduce hardware gains. Author code not found; Gemini usage is not Google affiliation.
  Evidence locations: §3.1–3.6; §4; §5.1–5.3 Tables2–4

**2610.07177 · CLM-as-a-Judge: Evaluating an Open Contrastive Decision Model on Public Judge Benchmarks**

[Paper](https://arxiv.org/abs/2610.07177)

- **post-training**: Public judge evaluation and calibration cascade separate calibration/eval, use both orders and constant controls, and expose cost–risk. arXiv lists ancillary pins, splits, predictions, and judges/run_pass/metrics/analysis source. Hosted strong judge revision cannot be pinned; no execution, and one attachment failed in browser.

**2610.07132 · CroissantMiner: Automated Extraction and Validation of Croissant Metadata for ML Datasets**

[Paper](https://arxiv.org/abs/2610.07132)

- **foundation-model**: CroissantMiner provides 102 human-gold and 500 silver papers with 30 fields, single-pass and four agentic extractors, rule/LLM field scoring, and NULL penalties. Prefill Sonnet4.5 is not ranked; use final κ=.708/hard set .663 instead of early .890. Separate external enrichment from paper-only gold. Official MIT data/evaluation/CLI support evolve extraction evaluation.
  Evidence locations: §3.1–3.3; §4.1; §5.1–5.3; official README/data/evaluation; README benchmark/data/evaluation/CLI, MIT
- **agent**: CroissantMiner compares one-pass, parallel experts, triage-critique, locator, and ReAct extraction of 30 Croissant fields on 602 papers, 102 human-gold. Public research extraction benchmark.
  Reproduction scope: 14 development/88 test; 500 silver are not human gold. Unstated fields should be null, and external lookup changes paper-only tasks. Judge is a model and gold starts from Sonnet prefill; Sonnet4.5 is not ranked. Automated extraction cannot replace source checks here.
  Evidence locations: §3.1–3.3; §4.1; §5.1; Limitations; official README

**2610.07121 · SoloQ: Calibration-Free Quantization for Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.07121)

- **foundation-model**: SoloQ K-RPBH combines permuted block Hadamard and cross-block Haar, E8P weights, and Lloyd/NVFP4 activations without calibration. Scale `||z||²/<q(z),z>` restores a projection, not exact values. Block diffusion quantizes committed KV but keeps active KV precise. Five dLLMs; separate H200 quality/low-bit performance from A100 compatibility.
  Evidence locations: §4.2–4.5Eq. 4, 7–12; §5.1–5.3; Appendix B/C
- **post-training**: SoloQ is calibration-free diffusion quantization and KV compression, not policy post-training.

**2610.07118 · AMBER: Training Long-Horizon Web Agents through Append-Only Memory**

[Paper](https://arxiv.org/abs/2610.07118)

- **foundation-model**: AMBER applies append-only memory RL to long-horizon web agents; review under Agent.
- **post-training**: Append-only two-turn memory/action share terminal GRPO advantage with template-token masking. Experiments initialize with SFT, not fully SFT-free, and require a web environment.
- **agent**: Append-only two-turn memory/action share terminal GRPO advantage with template-token masking. Experiments initialize with SFT, not fully SFT-free, and require a web environment.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; public artifact executability was not reverified here. Accepted as a research candidate, not an implementation.
  Evidence locations: §4.2Eq. 10; §5

**2610.07043 · TRIAGE: Direction-Aware Mismatch Stabilization of Native NVFP4 Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.07043)

- **post-training**: TRIAGE gates negative-advantage, negative-gap tokens by segment while normalizing response update mass, and applies bounded pseudo-Huber repair to positive advantages. Actual NVFP4 learner/sampler experiments; A100 emulation cannot claim native throughput.

**2610.06993 · DART-ES: Difficulty-Aware Reweighting and Targeted Replay for Fine-Tuning LLMs with Evolution Strategies**

[Paper](https://arxiv.org/abs/2610.06993)

- **foundation-model**: DART-ES difficulty reweighting for evolutionary post-training belongs to post-training review.
- **post-training**: DART-ES estimates difficulty with an EMA of perturbation-population accuracy, and uses mastery thresholds and zero-success patience to replay rare solvable items. Actual LLM math ES comparisons; historical accuracy oracle cannot enter evaluation agents.

**2610.06966 · APEX: Active Protection at Execution Boundaries for LLM Agents**

[Paper](https://arxiv.org/abs/2610.06966)

- **agent**: APEX freezes the authorization contract, uses WRAP to verify effects at execution boundaries, uses PLANT deception receipts to expose unauthorized information use, and continues safely after failures. Public AgentDojo/ASB/MCPTox/MSB/Skills tasks support checks.
  Reproduction scope: Zero ASR is not open-world safety. Attackers optimize against fixed feedback per defense, which must be reported. Skills cannot rewrite authorization. Track contract errors, blocks, and failed recovery separately.
  Evidence locations: APEX Algorithm1; WRAP/PLANT coordination; §experiments; Appendix C/D

**2610.06964 · Principles that Guide, Actions that Inform: Agent Evolution via Knowledge Abstraction**

[Paper](https://arxiv.org/abs/2610.06964)

- **agent**: SAGA abstracts trajectories into layered experience/principles, retrieves and adapts them to current tasks, and can optimize actors via SFT/GRPO. ScienceWorld/ALFWorld grounding and utility ledgers are executable.
  Reproduction scope: Strict ALFWorld 7B complete-hierarchy R1–R3 has no L3 principle passing verification, so gains cannot be attributed to verified principles. Strong builder/weak actor is not same-model self-evolution. API faults are not successes.
  Evidence locations: SAGA retrieval-utilization-abstraction; Algorithm1; normalized p34,44,82–90,115–116

**2610.06963 · WavePrune: One period is often enough for RoPE**

[Paper](https://arxiv.org/abs/2610.06963)

- **foundation-model**: WavePrune limits each 2D RoPE channel's QK contribution to its first rotation period. FlashWavePrune uses the maximum window per 16-dimensional group for TensorCore sparsity, usable in inference or retraining.
  Reproduction scope: Zero channel contributions, not full-token softmax masks; validate exact and grouped approximations separately. Physical KV eviction is future work; A100 kernels are not end-to-end gains. HELMET alpha/channel tuning needs fresh validation and independent test. Code includes kernel/training/eval; full README and license still need checking.
  Evidence locations: §3.1 Eq6; §3.3 Eq8; §4.1–4.5; official README

**2610.06950 · Learning to Decide, Not to Reason: Parameter-Efficient Decision Operators via Low-Rank Activation Steering**

[Paper](https://arxiv.org/abs/2610.06950)

- **foundation-model**: DecSteer trains shared low-rank activation residuals and token gates, initially identity with output-branch gradients. Focuses on decisions rather than full model training. Real SearchQA/LiveMath BC and multiple benchmarks; preserve RMS, SiLU, and gating.
  Evidence locations: Abstract (all retrieved abstracts reviewed individually); §3; §4–5
- **post-training**: DecSteer trains shared low-rank activation residuals and token gates, initially identity with output-branch gradients. Focuses on decisions rather than full model training. Real SearchQA/LiveMath BC and multiple benchmarks; preserve RMS, SiLU, and gating.

**2610.06947 · FactorBench: A Portfolio-Aware Benchmark for Automated Factor Mining**

[Paper](https://arxiv.org/abs/2610.06947)

- **post-training**: Public evaluation: symbolic/Python factor to date×asset signal contract in five markets, train 2017–21, validate 2022–23, test 2024–25, with portfolio and cost backtests. Official data/evaluator/mining can support specialized automated research, not universal LLM ability or live A/B.
- **agent**: Public evaluation: symbolic/Python factor to date×asset signal contract in five markets, train 2017–21, validate 2022–23, test 2024–25, with portfolio and cost backtests. Official data/evaluator/mining can support specialized automated research, not universal LLM ability or live A/B.
  Evidence locations: §3.1–3.3; §4; Appendix B; author's README and file list checked read-only.

**2610.06932 · RADC: Risk-Aware Dual Caching for Vision-Language Test-Time Adaptation**

[Paper](https://arxiv.org/abs/2610.06932)

- **foundation-model**: RADC's foreground/global dual cache and Gaussian-risk admission define a VLM TTA candidate.
  Reproduction scope: Sixty-four views and patch extraction cannot be replaced by one forward. On 4090 ImageNet-A, RADC 12.26 min/2084 MiB versus SCA 7.14 min/988 MiB is slower and larger despite better accuracy. Gaussian risk is approximate, not calibration proof. Hyperparameters fixed across domains but validation source needs confirmation. Code link not found.
  Evidence locations: §2.2 Eq3–7; §2.3 Eq8–9; §3.1–3.4 Table4

**2610.06892 · Axiom Satisfiability of Linear Rewards in Alignment**

[Paper](https://arxiv.org/abs/2610.06892)

- **post-training**: LP3 jointly minimizes candidate slack and linear reward-margin violations on finite preference graphs via LP rather than ILP. Real Habermas preferences, no policy training or guarantee of axioms on unseen responses.

**2610.06844 · Learning to Read the Contextual Tokens in Diffusion Transformers**

[Paper](https://arxiv.org/abs/2610.06844)

- **foundation-model**: Contextual Reader adds layer/timestep embeddings to MM-DiT context tokens, uses a two-layer Q-Former, and probes frozen LLM QA. CoAl uses a one-query early aligner with negative cosine to frozen clean-image SigLIP during flow training, upweighting null conditions to limit prompt shortcuts. Discard aligner at inference. Separate COCO from-scratch and SD3 Fine-T2I tuning; probing is not generation capability.
  Evidence locations: §3.1–3.3; §4.1; §4.2–4.3
- **post-training**: Reading and aligning contextual tokens in vision diffusion is image generation training, not LLM RL/OPD.

**2610.06843 · Recursive Video In-Context Learning for Agentic Robot**

[Paper](https://arxiv.org/abs/2610.06843)

- **agent**: RV-ICL indexes demonstrations at several levels and re-enters by subgoal. Candidate demonstration-conditioned context-access diagnostic; isolate stage goals/simulation state from gold-free capability evaluation.
  Reproduction scope: Phase maps use demonstration-derived goals, objects, and regions, and changed goals identify invalid demos. Not autonomous no-gold planning. Hidden goals/answer plans only for diagnostics, never evolve promotion. Old baseline/new method episodes are unpaired and pooled z ignores task clustering. No public code link; simulation only.
  Evidence locations: §3.1–3.3 Algorithm1; §4; §5.1–5.4 Tables1–4; Appendix A/B; Limitations

**2610.06830 · MemPilot: Orchestrating On-Demand Multimodal Memory Curation for LLM Agents**

[Paper](https://arxiv.org/abs/2610.06830)

- **foundation-model**: MemPilot orchestrates multimodal agent memory; review under Agent.
- **post-training**: Group-normalize quality, cost, and latency separately before combining, and use prefix-probed marginal answer quality for stage credit. Training latency is a proxy, not wall-clock reward.
- **agent**: Group-normalize quality, cost, and latency separately before combining, and use prefix-probed marginal answer quality for stage credit. Training latency is a proxy, not wall-clock reward.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §3.3Eq. 7–13; §4.1

**2610.06829 · CLIFT: Conformal Self-Verification for Web Agent Training and Test-Time Scaling**

[Paper](https://arxiv.org/abs/2610.06829)

- **post-training**: Nonnegative conformal self-verification bonus and URL-stratified return advantages alter credit. Report WAI training, VWA bank transfer, and OM2W without policy training separately.
- **agent**: Nonnegative conformal self-verification bonus and URL-stratified return advantages alter credit. Report WAI training, VWA bank transfer, and OM2W without policy training separately.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §2.2Eq. 6–7; §3 Experimental Design

**2610.06817 · Paradee: Distilling Kokoro-82M into an 8M-Parameter Single-Voice Text-to-Speech Model**

[Paper](https://arxiv.org/abs/2610.06817)

- **foundation-model**: Paradee distills Kokoro's single voice into 8.07M TTS, training text and decoder in stages with multiresolution spectral loss, GAN refinement, and phase locking. WikiText103 teacher audio and 200 evaluation sentences can be reconstructed.
  Reproduction scope: Only af_heart voice. Automatic UTMOS/WER is not human naturalness. CPU time excludes phonemization. Int8 applies to weights, not all activations.
  Evidence locations: §4.1–4.6; §5–9; Appendix A–C

**2610.06804 · Sharpen Without Search: On-Policy Distillation of Sequence-Level Power Distribution**

[Paper](https://arxiv.org/abs/2610.06804)

- **post-training**: The Rényi gradient is weighted MLE under a teacher power distribution times the student distribution, with SMC resampling from student proposals. GSM8K training does not read reference answers; retain the entire SMC pipeline.

**2610.06782 · T-Search: An Open Agentic Retriever and Playground for Hard Multi-Step Search**

[Paper](https://arxiv.org/abs/2610.06782)

- **post-training**: Public retrieval-agent interface: frozen-corpus search/save_and_advance/finalize tools and multi-turn evidence state for TRuST/SynthComp. Official Apache-2.0 harness readable. Final-set Recall@10 and generative-agent trajectory recall differ; budget all three fusion calls.

**2610.06751 · MatrixFormer: A Foundation Model for Matrix Completion**

[Paper](https://arxiv.org/abs/2610.06751)

- **recommendation**: MatrixFormer is a general Transformer and was routed to foundation full-text review.
- **foundation-model**: A 78M general matrix completion model with 2D cells, row/column axial attention, and synthetic-prior training. A tabular foundation candidate, not industrial A/B approval.
  Reproduction scope: Authors saw downstream benchmarks during development; UCI context results are exploratory. Ensemble weights fitted on observed unmasked inputs risk optimism; held-out weights are future work. 107× is one expert at fixed ten-column H200 timing; two experts need two passes. No author code verified.
  Evidence locations: §2 Eq1–11; §2.1; §3.1–3.6 Tables1–3; §4

**2610.06750 · Balancing Memory Pathways: Analyzing and Improving Memory Utilization in Hybrid LMs**

[Paper](https://arxiv.org/abs/2610.06750)

- **foundation-model**: Keep two hybrid-LM memory paths and add recurrent auxiliary SFT with cross-segment attention masked. Public implementation supports executable training integration.
  Reproduction scope: Lambda .25 was chosen for Quest without clear validation selection; use separate validation. Two passes for half the steps are not measured equal FLOPs. §6 per-example oracle and success/failure feedback are diagnostics; 32% oracle is not deployable.
  Evidence locations: §3; §4.1; §5.1–5.2; §6; AppB/C.1; official README
- **agent**: Balancing Memory Pathways adds recurrent-only auxiliary NTP to hybrid recurrent-attention LMs, masking cross-segment attention but retaining recurrent state. Train LoRA with two forwards; run full model normally afterward. Candidate agent memory/post-training method.
  Reproduction scope: Reselect/fix λ=.25 on local validation rather than Quest test; independent multiseed intervals were not found. Same-game success demonstrations are conditional efficiency diagnostics; per-example best-path oracle is not deployable. No gold walkthrough by default; isolate gold. Readable repository without LICENSE is not redistribution permission.
  Evidence locations: §3/§4.1/§5.1–5.2 Table1; §6; AppendixB.2/C.1/C.3; official README

**2610.06748 · BazaarBench: Delegation Safety in Decentralized C2C Marketplaces Run by LLM Agents**

[Paper](https://arxiv.org/abs/2610.06748)

- **agent**: BazaarBench continues reproducible 30-day market states for seven days with fixed 20-agent groups and separates inventory/event gold from transaction-safety stages. Candidate multi-agent delegation benchmark.
  Reproduction scope: 100 agents, three base markets, and 45 single continuations are not independent multiseed trials. Photos are JSON, not vision. Some risks use GPT5; idealized inspection is not physical verification and virtual profit is not A/B. L0 blocks inventory errors while L1–L3 only log, limiting causal comparisons. Synthetic services only, not real accounts.
  Evidence locations: §3.1–3.3; §4.1; Appendix B/C

**2610.06729 · Improving Diversity in LLM Short Story Generation**

[Paper](https://arxiv.org/abs/2610.06729)

- **post-training**: DivLM's CPT instruction residual recovery and group genre/tone/style/entity diversity reward define two-stage training, requiring real judges and corpora.

**2610.06686 · OVAL: Output-Aware Local Page Bases for KV Cache Retrieval**

[Paper](https://arxiv.org/abs/2610.06686)

- **foundation-model**: OVAL normalizes and mixes key energy and key/value output sensitivity matrices, builds page representations from principal subspaces, and selects decode pages via logsumexp of low-rank reconstructed logits without rereading value statistics.
  Reproduction scope: Main η* is setting-wise best, not a fixed leakage-free configuration. Freeze η with independent calibration and account for conversion and retrieval costs. Decode overhead versus FreeKV is about 10%; report it with quality gains.
  Evidence locations: §3 Eq1–5 / Algorithm1; §4.1; §4.3; §4.5; official README

**2610.06671 · Learning What to Imitate: Entropy-Aware Distribution Mixing**

[Paper](https://arxiv.org/abs/2610.06671)

- **post-training**: ConMix/GeoMix use normalized student Top-K entropy to set teacher contribution for sampled SFT and forward KL. AMiD already supplied both mixtures; entropy scheduling is new.

**2610.06666 · What Matters for Latent Reasoning with Flow Matching**

[Paper](https://arxiv.org/abs/2610.06666)

- **foundation-model**: FLaRe combines symbolic-CoT VAE, noise-shifted flow matching, and backpropagation through verified rollout paths. An executable latent reasoning training mechanism, not only measurement.
  Reproduction scope: Training reference verification is permitted; inference gold checks are not. Decoded reading uses a 3B autoregressive VAE, not CoT-free efficiency. Direct two-step Euler gets 97% CoT accuracy and 3.9× single-GPU speed; budget default 20 steps separately. Pass@16 is not a serving selector. Preserve stage-one EMA and stage-two LIVE; tiny arithmetic does not establish general reasoning.
  Evidence locations: §2.2–2.3; §3.1/3.2.1–3.2.4; §4.1–4.5; §5; AppA.3/D/E

**2610.06650 · Wikidata Search Traces: A Dataset for Training Knowledge Graph Search Agents**

[Paper](https://arxiv.org/abs/2610.06650)

- **foundation-model**: Wikidata search trajectories and RLM harness belong to Agent review.
- **agent**: Generate unique verifiable questions from constrained Wikidata graphs. A persistent Python REPL composes 13 graph query types, preserving successful trajectories for training and harness research.
  Reproduction scope: Teacher collection saw answer-path clues; deleting them from exported prompts does not make rollouts unprivileged. Training-only teacher data, never clues at evaluation. 10,235 success-selected trajectories are biased, RLM uses many more graph calls than tool baselines, and small-model training is untested. Pin graph, match query budgets, and hold out questions.
  Evidence locations: §3.2–3.5; §4.1; §5 limitations

**2610.06648 · Representation-Space MMD for Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.06648)

- **post-training**: Use RBF-MMD over frozen DLM token features, sample discrete outputs with one denoiser pass, then group REINFORCE and differentiate after continuous bootstrap. OWT/GSM8K and 16B DMax experiments.

**2610.06647 · LoGRA: Scaling LLM Reinforcement Learning with Low-Rank Gradient Sketches**

[Paper](https://arxiv.org/abs/2610.06647)

- **foundation-model**: LoGRA low-rank gradients and KL step control are RL post-training and reviewed there.
- **post-training**: Accumulate randomized gradient sketches directly, apply low-rank updates and predicted-KL step sizes. Real multiscale PPO; H100 results cannot be extrapolated to A100.

**2610.06637 · Long-Horizon Textual World Modeling through Structured Reasoning**

[Paper](https://arxiv.org/abs/2610.06637)

- **post-training**: Real encode-transition-decode rollout trees assign sibling-group credit, jointly training predictive gain and intermediate rewards without gold textual states.

**2610.06636 · Differentially Private Mixing of Public Datasets Improves Private Learning**

[Paper](https://arxiv.org/abs/2610.06636)

- **foundation-model**: DP-MixMin convex proxy optimization of public pretraining mixture weights with privacy accounting is a foundation LM data mixture candidate, not only medicine. Full GPT2-Medium pretraining and DP tuning on two text domains.
  Reproduction scope: Theory assumes the MixMin reduction and Bayes optimality, not guaranteed by empirical proxies. Preserve noise accounting; report image pilots and validation privacy separately. Canary lower bounds do not prove general upper bounds. Enron 148 users and sent-only emails avoid multi-owner data but do not establish arbitrary mailbox-level DP. Author code not found.
  Evidence locations: §4.1–4.2 Algorithm1; §5.2–5.3 Tables1/2; App A.3.2/A.7/A.8

**2610.06617 · RealtimeWAM: One-Step Asynchronous World Action Models**

[Paper](https://arxiv.org/abs/2610.06617)

- **foundation-model**: RealtimeWAM anchors consistency distillation with interval velocity to the teacher's ten-step endpoint; λ=.2 equals 1/t² endpoint weighting. Frozen video shares KV and only action LoRA trains. CUDA two-stream wavefront records events after layer KV projection and waits at action attention. LIBERO/RoboTwin/Plus and matched distillation; latency includes VAE but not once-per-episode text.
  Evidence locations: §4.1Eq. 6–9; §4.2Eq. 10–13; §5.1–5.4

**2610.06616 · Video Encoders Built on Image Representations**

[Paper](https://arxiv.org/abs/2610.06616)

- **foundation-model**: Image-first video preserves source positions, selects DPP/cross-frame associations under fixed token budget, and optionally uses an 18M temporal refiner. Appendix C.1 separates training-free controls.
  Reproduction scope: Fixed output tokens do not eliminate overhead. The refiner uses 65K VideoChatGPT examples after filtering, two epochs, 96 A100 GPU hours. Reported results do not replace local GPU receipts.
  Evidence locations: §2–3; §4.1–4.4/Table1/Table2; Appendix C.1–C.3/Table4/Table5

**2610.06611 · Lens3D: Target-Conditioned Visual Foveation for Fine-Grained 3D Understanding**

[Paper](https://arxiv.org/abs/2610.06611)

- **foundation-model**: Lens3D grounds object boxes, selects depth-visible voxel coverage across views with wireframes, then uses a 2D VLM. LensDistill uses privileged teacher captions and target center to supervise a native 3D LLM, without extra views/VLM at test. LensBench 2,068 objects/141 val scenes separate from 561 training scenes, but references are three-model silver with 100 human-evaluated objects. Keep GT-box variants separate from end-to-end grounding.
  Evidence locations: §3.2Eq. 3–5; §3.3–3.4Eq. 6; §4.1 Tables 1–2

**2610.06598 · SimForcing: Distilling Simulation Motion Priors into Real-Domain Robot World Models**

[Paper](https://arxiv.org/abs/2610.06598)

- **foundation-model**: SimForcing trains action-conditioned video dynamics with simulation replays of real trajectories and a disturbed teacher. Distill adjacent clean-latent differences under shared noise/time using L2; zero-init convolution conditions each block with per-example shared dropout and noise. Bridge/InternData and downstream LIBERO. World pretraining predicts no actions; simulation deliberately excludes object interaction, not general physics.
  Evidence locations: §3.1–3.3Eq. 1–12; §4.1–4.3; Appendix A

**2610.06479 · Behavior-Preserving KV Cache Compression**

[Paper](https://arxiv.org/abs/2610.06479)

- **foundation-model**: Match the next-token distribution under full cache. Approximate removal perturbations at logits through the final norm Jacobian and LM head, then greedily optimize mask-level marginal KL over singleton proposals.
  Reproduction scope: Residual straight-through is approximate, not exact output preservation. Use visible prompt tail or generated queries, never future answers. Prefill still requires full cache and selection adds overhead. The paper links kvpress baselines; no author implementation found.
  Evidence locations: §4.1–4.4 Eq1–8; §5.1 / Table1; §6; Limitations

**2610.06454 · AgentPrivArena: Evaluating and Auditing Real-world AI Agent Privacy**

[Paper](https://arxiv.org/abs/2610.06454)

- **agent**: AgentPrivArena/AgentPrivAudit execute 389 privacy tasks across six container services. Extract source/subject/recipient flows after reads and choose Pass/Abstract/Block before writes. Candidate tool-state benchmark and defense.
  Reproduction scope: Only 389 of 493 source cases converted; missing group chats bias coverage. Scores use two or three model judges without human verification, and fail-open does not guarantee safety. Raw sensitive observations still enter the model. MIT code; prepare PrivacyLens under its own terms. Records are synthetic.
  Evidence locations: §3.1–3.4; §4.1–4.2; §5; Limitations/Ethics; official README

**2610.06446 · The Assistance Dilemma: Learning to Teach via Multi-Turn Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.06446)

- **foundation-model**: Eduardo multi-turn tutoring rewards are reviewed under post-training.
- **post-training**: Tutor has no gold solution. Masked near-transfer post-test retains only student tokens, with correctness/no-handover gates, frozen students, and cross-benchmark evaluation.

**2610.06439 · Better Call Reward: Reward Hacking as Strategic Abstention in Legal Reasoning Models**

[Paper](https://arxiv.org/abs/2610.06439)

- **post-training**: Public reward-hacking diagnostics: 16 LegalBench tasks separate surface proxy, parseable correctness, CTS, and rolling GDM. Apache-2.0 repository has notebooks and results. Deliberately bad proxy training detects format/abstention collapse, not capability gains.

**2610.06413 · SpatialChain: A Benchmark for Auditing Spatial Reasoning Faithfulness in VLMs**

[Paper](https://arxiv.org/abs/2610.06413)

- **foundation-model**: SpatialChain generates and answer-filters 28,350 train and 899 test CoTs from GQA scene graphs. Evaluated models receive image/question; judges can read GT graphs for AC/RF/RC. Surface overlap is not faithfulness and RF is graph agreement, not model-causal faithfulness. Official data/eval/judge CLI supports public evaluation with scorer gold isolated.
  Evidence locations: §3.2–3.3; §4.1–4.3; §5; Appendix L; official README; README Dataset/Repository Structure/eval/judge

**2610.06406 · What Did the Agent Actually Do? Evidence-Grounded Oversight for Long-Horizon Agents**

[Paper](https://arxiv.org/abs/2610.06406)

- **foundation-model**: EBG and AgentMonBench supervise long-horizon agents; review under Agent.
- **agent**: EBG builds deterministic evidence→behavior→scope graphs with requirement-driven one-hop expansion and source rechecking. AgentMonBench separates missing specs, semantic substitutions preserving tests, and post-feedback prefixes. Candidate supervision and conditional public evaluation.
  Reproduction scope: FeedbackTrace selects cases by later pushback hidden from monitoring, not real-time prevalence. EHR only needs one evidence hit, not full sufficiency. Five Codex cases are not causal generalization. Public Drive link exists but files, frozen downloads, and benchmark execution were not verified. Dataset-specific terms pending; follow upstream CC BY/ODC-BY separately.
  Evidence locations: §3.1–3.4; §4.1–4.3 Eq1–2; §5.1–5.2; AppendixD.1/F; official README/dataset_card

**2610.06404 · Quantifying the Stability of Multi-Step Reasoning via Error Amplification**

[Paper](https://arxiv.org/abs/2610.06404)

- **foundation-model**: Random ordered CoT step subsampling with STE quantization-aware SFT aims to reduce stepwise error amplification. CLRS-Text/LEGO experiments and Jacobian diagnostics.
  Reproduction scope: Not direct Jacobian regularization. 2000 train/200 validation/200 test; tune λ and bits only on validation. Main extrapolation +10% length; at +20% all methods below 25%. Seven graph/symbolic tasks and Qwen1.5B do not establish open-text reasoning.
  Evidence locations: §3 error amplification; §4 Algorithm1; §5.1/Table1; Appendix B

**2610.06324 · Readout Blindness: VLM Scores Miss the Spatial Direction Their Frozen Encoders Retain**

[Paper](https://arxiv.org/abs/2610.06324)

- **foundation-model**: ADR uses frozen patch and independent text features for Sinkhorn excess coupling or dense centroids, then signed displacement along parsed subject-object relation axes. No training; context-free/unary blindness theorem has assumptions, not a claim about all VLM encoders. Nine models and five direction-balanced datasets; derangement null adjusts grounded gain for language priors. Candidate readout and diagnostic.
  Evidence locations: §4 Theorems; §5 Algorithm 1; §6; §7 Tables 1–2; Appendix D

**2610.06286 · DeferKV: Rethinking Eviction Timing for One-Shot KV Cache Compression**

[Paper](https://arxiv.org/abs/2610.06286)

- **foundation-model**: DeferKV waits until the first real generation token yields a decode query before compressing prompt KV. Combine that query with trailing prompt queries using temporal discount and reuse base smoothing, budgets, and selection.
  Reproduction scope: Full prompt KV is needed before first decode; retain additional generated-token KV. η=0.7 comes from LongBench sensitivity, requiring separate validation. No assumed MLA or hybrid linear-state compatibility.
  Evidence locations: §4.1–4.3 Eq6–9; §5.1; §5.4–5.6 Table4; Limitations

**2610.06269 · Evolving in Thought Space: Training a Small Model at Test Time Unlocks Better Discoveries**

[Paper](https://arxiv.org/abs/2610.06269)

- **agent**: Guidance-TTT trains a small guidance LoRA. An archive-parent summary proposes strategy, a frozen executor reads the full parent to implement it, and an independent verifier rewards it. Actual RL combines adaptive entropic LOO advantage and centered base correction; high-priority evolve candidate.
  Reproduction scope: Best search outcomes are not cross-task generalization. Three/five repeated fixed programs are not independent training seeds. Do not pool TriMul archive baselines with new paired timing CIs. GPTOSS same-executor score 83.19 versus TTT 83.72 is cheaper but lower. Official README says paper records are historical, not a new port run. H100 is not local A100 validation.
  Evidence locations: §3.1–3.4; §4.1–4.3; Appendix A.3/C.4–C.5/D.3; official guidance-ttt-support recipe README/LICENSE

**2610.06226 · LeAVJEPA: A Minimalist Architecture for Audio-Visual Self-Supervised Learning**

[Paper](https://arxiv.org/abs/2610.06226)

- **foundation-model**: LeAVJEPA trains early-fused shared ViT, modality-specific local views, symmetric invariance, and SIGReg. Appendix C.3 Table A3 controls encoder, 30 epochs, and batch 512 for local views. Research candidate only, not SOTA or reproduced.
  Reproduction scope: Several comparisons are single training runs. Verify original audiovisual data access before implementation. No code link found on the official page.
  Evidence locations: §3.1–3.4; §4.1–4.4/Table2/Table4; Appendix B.1; Appendix C.3/TableA3

**2610.06193 · Correct Code, Broken Contributions? SWE-CC: Benchmarking Repository Policy Compliance for Coding Agents**

[Paper](https://arxiv.org/abs/2610.06193)

- **agent**: SWE-CC compiles 823 contribution rules across 12 SWE-bench repos into deterministic preconditioned checks on trajectories and patches. Candidate coding-agent contract evaluation.
  Reproduction scope: Report compliance with trigger, withheld, and functional success rates; doing less is not compliance. Manual audit accepts 87.2% on average over 150 checks, and uncorrected checkers err. Bind doc versions to historical tasks. MIT release includes tasks/checkers/runner and 8,000 outcomes, but not complete historical traces.
  Evidence locations: §3.1–3.5; §4.1–4.2; Appendix B/D; official README

**2610.06192 · Copies or Sources? Measuring How LLM Aggregators Count Restated Evidence in Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.06192)

- **agent**: Use exact Bayes over countable sources to measure duplicate evidence weights. Compare deduplication declarations, extracting unique readings, and forwarding citations only. Candidate multi-agent evidence aggregation diagnostic.
  Reproduction scope: Extraction adds a model call and can miss evidence; citations must resolve to originals. Hierarchical summaries still duplicate and declarations do not imply independence. Web-summary deduplication is weaker; complex real-world gains unestablished.
  Evidence locations: §2–3 testbeds; §5.1–5.3; Appendix G prompts

**2610.06191 · Judged Useless, Queried Anyway: Tool-Using Agents Rarely Turn Their Own Evidence Judgments into Stopping Decisions**

[Paper](https://arxiv.org/abs/2610.06191)

- **agent**: The agent labels searches USELESS; a harness consolidates/stops after five consecutive failures. Fixed-step controls and 300 new questions support a tool-budget candidate.
  Reproduction scope: Count 3–5 side-channel calls. Keyword reader only works on some models. Threshold is for simulated faults recovering within three attempts; later recovery can be stopped too early. No gold stopping signal. Memory-only answers still need safety/accuracy checks.
  Evidence locations: §2 setting; §5–6; Limitations; Appendix D

**2610.06161 · Introducing Code-Switched Contexts to Cognitively-Inspired Bilingual Model Training**

[Paper](https://arxiv.org/abs/2610.06161)

- **foundation-model**: Dictionary/POS-controlled code-switching and four-stage density curriculum are executable data augmentation diagnostics for small bilingual pretraining. Preserve English–Chinese regressions.
  Reproduction scope: Small English–Dutch/English–Chinese only; Dutch improves while Chinese grammar and translation retrieval regress. No universal language or cognitive fidelity claim. Record lexical/POS noise and word/token budgets. No author code; independent implementation pins corpora and lexicon construction costs.
  Evidence locations: §3.1–3.2/Table1; §4–5; §7/Limitations; App A/B/D

**2610.06147 · Efficient Test-time Adaptation through Candidate Verification and Divergence Shifts**

[Paper](https://arxiv.org/abs/2610.06147)

- **foundation-model**: TTC stability correction for candidate memory subspaces; public code/features support gradient-free VLM adaptation.
  Reproduction scope: Table 5 uses precomputed features without augmentation, so 2× covers adaptation only. Accuracy outside top three is necessarily zero; pseudolabel corruption and empty-class cold starts remain. Separate labeled-memory and label-free protocols; use test_l only for final scoring.
  Evidence locations: §3 Eq1–8; §4.1/4.3/4.4; App B/C/D; author's README.

**2610.06100 · From Traces to Agentic Worlds: Agentic Language World Models for Interactive Environment Simulation**

[Paper](https://arxiv.org/abs/2610.06100)

- **agent**: Trace2Env builds frozen worldbooks from traces, separating cross-episode knowledge, current state, and step memory. Gates applicability, validates schema/constraints, commits in stages, and evaluates W2R against real replay. Candidate world model/environment.
  Reproduction scope: Schema/constraint gates do not prove actual transitions. Legal model proposals are accepted, rejects clear effects but return original observations, risking inconsistency. Main results are single runs; report excluded judge failures. Except Terminal, frozen worldbooks/traces/results mostly on request, so resampling is not exact. SciWorld gold paths are construction/training only, not test-agent input. CR is not per-trajectory consistency probability.
  Evidence locations: §4.1–4.3 Eq3–8; §5.1–5.4 Tables1–3; AppendixC.3 Table13; official REPRODUCING.md

**2610.06064 · TrustMI: Causally controlling how assistants trust their users**

[Paper](https://arxiv.org/abs/2610.06064)

- **agent**: TrustMI learns all-layer BiPO steering on a frozen LM with positive trust NLL to limit likelihood displacement. User and assistant spans train separately; main agent tests apply user-trained matrices to all user/tool outputs. Meta priority security mechanism and public-eval candidate.
  Reproduction scope: User-only steering raises Qwen injection ASR; include tool spans. Moderate α preserves approximate mean, not every subtask. Use separate validation for α/γ; paper 1800/200 lacks clear tuning split. Activation interventions do not identify a unique psychological trust factor; doubt/sycophancy are not disentangled, and changing judges invalidates absolute comparison.
  Evidence locations: §3–6; Appendix B/C/D.3–4/D.6/E; official README, LICENSE/data licenses.

**2610.06026 · Differentiable Bit-Widths: Co-optimizing Pruning and Quantization via SVD for Ultra-Efficient LLM Compression**

[Paper](https://arxiv.org/abs/2610.06026)

- **foundation-model**: DBW learns per-SVD-component bit widths including zero, with STE, Hamilton leftover allocation, matrix budgets, and singular-value entropy regularization for joint pruning/quantization. Public train/eval code supports compression consideration.
  Reproduction scope: 4096×2048 RedPajama calibration, 1.61bpw, group128. Count U/V scales and actual packed storage, not fake quantization. Multiple GEMM launches lose to OmniQuant at 64 tokens; long sequences do not establish low-latency decoding. Verify GPU training/kernels independently on A100/A30. Official homepage license unclear.
  Evidence locations: §2.2/Eq1–4/Algorithm1; §2.3; §3.1–3.2; official README

**2610.06021 · Scalable Minimal-Change Learning for Controllable Image Editing**

[Paper](https://arxiv.org/abs/2610.06021)

- **foundation-model**: Arro audits missing and unintended edits with a VLM, deduplicates shared rubrics with an LLM then validates Booleans with the VLM, and separately normalizes negative counts before weighting and batch renormalization for flow-GDPO. MinEval 10k/600 disjoint and MagicBrush/AnyBench/EmuEdit. Model judges are not A/B; account for group auditor and external judge budgets.
  Evidence locations: §3.2–3.4Eq. 4–8; §4.1–4.4; Appendix B/E/F
- **agent**: ARRO audits omitted and unintended edits with a VLM, rechecks shared atomic rubrics, separately group-normalizes rewards and batch-renormalizes advantage for flow-GDPO. Candidate multimodal post-training/Agent reward.
  Reproduction scope: About 10K MinEval training with independent holdout. EditScore and segmentation OffTarget-L1 depend on judge/perception, not full semantic correctness. Single training seed, no proven diffusion transfer. Preserve real Kontext training; heuristic audit is diagnostic only.
  Evidence locations: §3.2–3.4; §4; §5 Limitations; Appendix B/E/F

**2610.06001 · AgentSpy: Making AI Agent Behavior Observable**

[Paper](https://arxiv.org/abs/2610.06001)

- **agent**: AgentSpy observes process-tree syscalls/network outside an isolated microVM, builds star graphs from normalized command/file/host counts, and compares weighted Jaccard. Candidate independent observability mechanism.
  Reproduction scope: 77/87 tasks, three runs; selected timeout retries/drops affect samples. Resource similarity is not task correctness; reading skills is not use. RQ2 annotation sees metrics and is not blind. Detects four of five safety categories, not complete protection. Verify Linux microVM/kernel permissions; monitor only authorized sandboxes. Source link not found in paper.
  Evidence locations: §3.1–3.4; §4.1–4.2; Threats to validity; §6

**2610.05994 · How (and How Not) to Use Data Augmentation in VLA Post-Training**

[Paper](https://arxiv.org/abs/2610.05994)

- **recommendation**: VLA augmentation belongs to embodied foundation models and was routed to foundation review.
- **foundation-model**: Critic-only image augmentation in VLA PPO affects clean actor/rollouts through advantages. A reproducible robot/post-training intervention, not industrial recommendation evidence.
  Reproduction scope: Critic-only needs an extra backbone forward; matched epochs are not matched FLOPs. One training seed per configuration and repeated checkpoint evaluation are not training repeats. Tune augmentations on independent validation; simulation is not real robots.
  Evidence locations: §3/Table1; §4/Tables2–3; §5; Limitations
- **post-training**: Existing PPO/Flow-SDE compare augmentation placement; the contribution is an empirical critic-only rule, not a new RL/OPD algorithm.

**2610.05993 · From Transformation to Target State: Rethinking Query Representation for Zero-Shot Composed Image Retrieval**

[Paper](https://arxiv.org/abs/2610.05993)

- **foundation-model**: Frozen MLLM reconstructs several holistic target descriptions and weighted atomic facts from reference plus edit. CLIP global/patch-softmax matches are query-wise z-scored and fused. FashionIQ val/CIRR test1/CIRCO test; no task training but dataset-specific prompts and extra MLLM cost remain.
  Evidence locations: §3.2 Eq. 1–3; §3.3 Eq. 4 onward; §4.1–4.4.

**2610.05981 · Mechanizing the User's Eye: Pre-Registered Deployment of a Sabotage-Validated Fail-Plausible Observer in a Production LLM Agent Runtime**

[Paper](https://arxiv.org/abs/2610.05981)

- **agent**: Small agent reliability regression benchmark: five deterministic signals feed an LLM judge with verbatim-substring evidence gates. Fourteen public offline cases, per-detector sabotage, pinned manifest and scorer support evolve regression diagnostics, not general capability.
  Reproduction scope: Sixteen of 24 incidents are structurally invisible. Rules were built from historical examples, so Category A is regression; four holdouts are too few, and optimizers must not see gold or expected signals. Official repo corrects earlier ~70% user discovery to 13/22=59%; cite the version. No independent annotations and two of 14 dates missing. Runner not executed.
  Evidence locations: §3–5 Tables1–3; §6 Table4; §7 Table5; §9; official docs/fail_plausible_bench.md and LICENSE.

**2610.05978 · Byte Language Models: Scaling, Emergent Abstractions, and Information Allocation**

[Paper](https://arxiv.org/abs/2610.05978)

- **foundation-model**: Byte model uses 256 vocabulary, hashed n-grams/DeltaNet convolution 16, four-byte TST first 30%, and NTP last 70%. IsoFLOPs with subwords is not equal text exposure. Late-layer pooled-span interventions are diagnostic; keep the 200M segmented model. Speculation is an eval-text oracle simulation, not real latency; 3.4× accepted tokens is not 3.4× speed.
  Evidence locations: §2.1–2.4; §3.2; §4.2/Table 3; Appendix G

**2610.05940 · ReMem: Streaming Video Understanding With Long Context Retention**

[Paper](https://arxiv.org/abs/2610.05940)

- **foundation-model**: ReMem's training-free SCM uses fixed general-query attention for recursive compression, retaining original RoPE positions plus temporal offset. RVM retrieves top clips by cosine of pooled keys and query, with finite FIFO eviction. Streaming/OVO/long-video and NIAH. r=.7 selected on StreamingBench SQA; create validation rather than reusing tuning results as test.
  Evidence locations: Methodology/SCM/GQC/RVMEq. 1–3; Experiments; Appendix A compression-ratio study

**2610.05935 · ThunderSyncRL: Lossless Acceleration of Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.05935)

- **post-training**: ThunderSyncRL streams fixed-policy-version GRPO dual-gradient accumulation and delayed token-normalized OPD before one optimizer barrier, preserving mathematical updates. B200/H200 checks and real agent training; stale asynchronous gradients are not a substitute.
- **agent**: ThunderSyncRL streams fixed-policy-version GRPO dual-gradient accumulation and delayed token-normalized OPD before one optimizer barrier, preserving mathematical updates. B200/H200 checks and real agent training; stale asynchronous gradients are not a substitute.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §3.3–3.4 Eq.1–9; §4

**2610.05897 · Fitting Vision Adapters at Frontier Scales**

[Paper](https://arxiv.org/abs/2610.05897)

- **foundation-model**: An approximately 50M visual projector connects frozen encoder/reader, initializes with shared-vocabulary affine alignment, and uses empty-think SFT followed by adapter-only CISPO image-math RL to restore reasoning. Positive reward requires nonempty reason/answer. Qwen4–32B matched recipe supports controls; 550/743B MoEs differ in training and rewards. Blind/corrupted-image controls are essential.
  Evidence locations: §3.1–3.3Eq. 3–5; §4.1–4.4; Appendix A.2/C

**2610.05896 · TasteRoute: Personalized Routing for Video Generation**

[Paper](https://arxiv.org/abs/2610.05896)

- **foundation-model**: TasteRoute uses frozen request embeddings, generator/user embeddings and cross features, BT pairwise plus ordinal quality, five prompt-disjoint general folds and per-annotator train/val/test with user dropout .4. Ranks within budget without generating video. Nine annotators and 3,128 videos; 55.2% conflicting-preference accuracy is limited. No population generalization or deployment claim from oracle verifier.
  Evidence locations: §4; §6.1–6.2Eq. 1–3; §7; §9.2

**2610.05885 · The Optimization Landscape of Learning Compacted Context Models**

[Paper](https://arxiv.org/abs/2610.05885)

- **foundation-model**: Fast Diamond simplifies a Perceiver KV writer with explicit single/recursive compression and matched budgets. Candidate learned KV method. The canonical appendix resolves inconsistent main-text readout wording as frozen, with discrepancy noted.
  Reproduction scope: §5 says leave trainable, conflicting with frozen text and Appendix A. Keep the canonical frozen contract and note discrepancy. Code/data promised camera-ready but unreleased; fixed medical OOD set needs resources. Repeated 16/32k compression loses to StreamingH2O. Normalized utility is not raw accuracy; question-excluded budget is not total memory.
  Evidence locations: §2–5; §6.1–6.3; §8; AppA Table2/G Fig20

**2610.05879 · Learning to Learn a Language**

[Paper](https://arxiv.org/abs/2610.05879)

- **foundation-model**: PFLM samples a fresh recurrent SCM prior per sequence for byte-level pretraining, then freezes weights and predicts using long prefixes. Core generator definition and 300M model/weights are public; candidate training paradigm.
  Reproduction scope: UTF-8 byte costs vary by language, so BPB is not language understanding. Does not beat modern natural-text LMs; many numeric shots are not zero-shot. Official model/HF integration/stream scoring verified but full SCM/training pipeline not established. Reproduce Appendix A prior, not arbitrary strings.
  Evidence locations: §2.1–2.4 Eq1–3/Table1; §3–4 Table2; App A/B/D; official README

**2610.05872 · Off-Policy Merging Beats On-Policy Self-Distillation for Continual Learning**

[Paper](https://arxiv.org/abs/2610.05872)

- **foundation-model**: Merge off-policy donor fine-tune deltas after Fisher/KFAC retention-sensitive projection and scaling. Qwen/OLMo continual learning, distinct from 2610.00767 belief transplant and earlier GRAFT 2609.37868 trajectory swapping.
  Evidence locations: Abstract (all retrieved abstracts reviewed individually); §4 Algorithm 1; §5.
- **post-training**: Merge off-policy donor fine-tune deltas after Fisher/KFAC retention-sensitive projection and scaling. Qwen/OLMo continual learning, distinct from 2610.00767 belief transplant and earlier GRAFT 2609.37868 trajectory swapping.

**2610.05861 · Imagine to Act: High-Fidelity Data Synthesis via Image Editing World Model for Scalable GUI Agent Training**

[Paper](https://arxiv.org/abs/2610.05861)

- **foundation-model**: Infinite-Dreamer learns deltas from before/after/action/next action. AppDesigner text drives delta-conditioned FLUX2Klein screenshot edits, VLM filters steps, and SFT trains GUI actor. AndroidControl train/val for world model; actor only synthetic, online AndroidWorld/MobileWorld tests. Future design is allowed in synthesis, not gold next state/plan at evaluation. Not a real app state machine.
  Evidence locations: §3.2–3.5Eq. 1–8; §4.1; Appendix A.5/A.6

**2610.05842 · HLA: Expressive Hybrid Linear Attention via Chunk-Wise Dynamic Mixing**

[Paper](https://arxiv.org/abs/2610.05842)

- **foundation-model**: HLA interpolates complete chunk affine GDN transitions with identity via query gates and composes them temporally, unlike static state weighting. Candidate long-context operator.
  Reproduction scope: Chunk states grow with length, not constant memory or faster than original GDN. The 2× saving is against token KV and omits router/activations. Chunk/pool tuned on LongBenchV2, with train p16/eval p32 requiring validation. Static tasks and module budgets not FLOP-matched.
  Evidence locations: §3 Eq1–13; §4.1; §4.2–4.3 Tables1–4

**2610.05833 · Request Order Matters: Cache-History Sensitivity in Selective KV-Cache Reuse for Rolling Agents**

[Paper](https://arxiv.org/abs/2610.05833)

- **agent**: Candidate KV recomputation diagnostic for long-running agent context: fixed 5% token budget, whole-span selection by document mean deviation and contiguous remainder, versus token Top-K and other blocks. Evidence chiefly supports contiguity, not document boundaries or scores.
  Reproduction scope: Synthetic rolling verbatim copy only, not real agent gains. Chronological full-prefill fidelity 86.8 vs 85.4 not significant; reversed documents only 54.3%. Prefill latency only. No author code/full workload found, so independent mechanism checks are not full reproduction.
  Evidence locations: §2.2–3 Eq1 and document-aligned selector; §4 setup; §5 Tables1–4; §6.

**2610.05778 · MedicalHarness: A Controlled Evaluation of LLMs and Agent Harnesses on Medical Tasks**

[Paper](https://arxiv.org/abs/2610.05778)

- **agent**: MH-Lab toggles summaries, explicit plans, and tool discovery within the same loop and separates answer rate, correctness, traces, and cost. Public code/MedTool support harness ablation.
  Reproduction scope: 107 tasks and three seeds; isolate grader/gold and bootstrap by task. Product harness comparisons are not single-factor; MH-Lab provides controls. Private MedMemory records make the whole 107-task suite not publicly reproducible; MedWeb needs upstream assets/terms. Official scripted smoke is not model capability. Offline only, no clinical deployment.
  Evidence locations: §3–6.1; §6.3/7; Appendix C/D/H; official README

**2610.05774 · AdaSpark: Adaptive DSpark with Online Learning for Tree Verification and N-gram Fill**

[Paper](https://arxiv.org/abs/2610.05774)

- **foundation-model**: AdaSpark merges DSpark proposals with request-local n-grams, ranks legal tree prefixes by acceptance probability, and chooses verification width from online lower-quantile latency and acceptance models. Candidate speculative controller.
  Reproduction scope: Greedy only, not arbitrary sampling guarantee. Count 55–67 cold-start rounds; cross-request stores must bind hardware, weights, and kernels. 42 sessions/95 replies, with some cap loops and single-delta replies excluded. Engine optimizations drive part of gains; adaptive width only ties best fixed width. Pin evolving official Rust Metal/CUDA/CPU versions.
  Evidence locations: §3.1–3.4; §4.1/4.5–4.6; §5; official imparo README

**2610.05744 · CIPHER-MoE: Balancing Efficiency and Routing Fidelity in Trillion-Scale MoE Training**

[Paper](https://arxiv.org/abs/2610.05744)

- **foundation-model**: CIPHER-MoE keeps token Top-K, adds expert cosine affinity, capacity admission, and locality loss, and separates strict drop from reroute. Actual large-scale SFT efficiency and quality evidence.
  Reproduction scope: Spherical/conditional-recall assumptions prove signal retention, not quality. Preserve zero-assignment gradients and weight renormalization. Code promised, not released. No industrial A/B; OOM at 1.6T is not a numeric speedup.
  Evidence locations: §3.2 Eq4–10; §4 Tables2–3; AppA.4/A.5

**2610.05715 · Rotated, but How Far? Diagnosing and Improving Object-Rotation Reasoning in VLMs**

[Paper](https://arxiv.org/abs/2610.05715)

- **foundation-model**: RotationCue uses three learned relation queries for object identity, rotation presence, and angle range, injecting conditional angle cues into a frozen VLM. ALOI/ModelNet40 can construct training; OR-Bench is object-disjoint full test.
  Reproduction scope: Oracle angles are diagnostic. Orientation rotation is not a 2D image rotation. Preserve object isolation and shuffled-cue controls.
  Evidence locations: §3–5.4; Appendix F/H

**2610.05709 · Nexus: An Execution Fabric for AI Agents Across Cloud, Edge, and Devices**

[Paper](https://arxiv.org/abs/2610.05709)

- **agent**: Nexus persists calls as tasks with invocation-scoped delegation, operation journals, device receipts, and cursor recovery. Reuses committed results and coordinates uncertain side effects at the resource. Candidate execution infrastructure.
  Reproduction scope: Single-host OpenWrt/Android virtualization controls do not combine all mechanisms end to end. Latency on 22 common successes from 24 paired tasks must not hide failures. Cloud admission/settlement is central, CPU ceilings are not commercial costs, and suppressing duplicated side effects needs resource support.
  Evidence locations: §3–4; §5.7; §6.1–6.3; Software and Documentation; Appendix D/E

**2610.05697 · From Token-Max to Outcome-Max: How You Use AI Determines Its Productivity**

[Paper](https://arxiv.org/abs/2610.05697)

- **agent**: TokenEcom simulates supervision by verified output/cost rather than token count, carries reusable playbooks across generations, and distills skills from both sides. Public SWE/HumanEval/GSM8K/MATH support cost-aware evolve evaluation.
  Reproduction scope: Humans are LLM simulations and directives also change stopping, so pure reward is not isolated. Accuracy drops on hard tasks among 310 matched SWE pairs. Skills use 20 training, 15 holdout, and 100 validation; gold is scorer-only. Economic accounts and penalties are assumptions, not workplace causality.
  Evidence locations: §3–5; Appendix A.5 Algorithm1; C/D

**2610.05685 · Spend Bytes on Breadth: Precision-Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning**

[Paper](https://arxiv.org/abs/2610.05685)

- **foundation-model**: BreadthKV combines KIVI quantization and SnapKV-D eviction under equal decode-KV bytes and calibrates bits independently on AIME22–23. Studies broader low-precision versus narrower high-precision cache.
  Reproduction scope: Prompt storage excluded, FP16 residual 128–191 tokens, budget error about 5%; report actual memory-time. R1-Qwen AIME24 is development, not test. One sampling seed. H200 one-layer/step kernel is not end-to-end faster, and int2 is slower. No code link found; preserve packed quantization and calibration/test isolation.
  Evidence locations: §3 Eq1; §4–5.1; §5.7/kernel; Limitations; Appendix A/B

**2610.05664 · StageVLN: Spatial and Trajectory Auxiliary Guidance for Efficient Vision-Language Navigation**

[Paper](https://arxiv.org/abs/2610.05664)

- **foundation-model**: StageVLN aligns multilayer current-image features to a frozen geometry teacher by cosine, and trains auxiliary relative heading sin/cos and expert forward-step progress. Pre-action state avoids teacher-forced GT current action. Joint R2R/RxR training and unseen validation; remove teachers/projectors/heads at inference. Progress is not success or a STOP rule.
  Evidence locations: §III-CEq. 2–5; §III-DEq. 6–12; §III-E; §IV-A–D

**2610.05637 · Visual Grounding Safety in Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.05637)

- **foundation-model**: Grounding safety matches VQA and localization by intent. SFT mixes harmful refusal, benign self-distillation with neutral evidence, and 1,548 grounding capability examples; plain and placeholder formats train separately. Score refusal from final answer/coordinates, not thinking. Failed localization can mimic safety, so report PointArena and over-refusal separately. Placeholders are not actionable coordinates.
  Evidence locations: §2.1–2.3; §3.1–3.4 Table 3; Appendix A

**2610.05630 · Atomic Visual Entailment: Enhancing Zero-Shot Vision-Language Reasoning through Atomic Fact Decomposition and Learned Selection**

[Paper](https://arxiv.org/abs/2610.05630)

- **foundation-model**: AVE freezes the decomposer, splits original text into atoms, and pools direct/atomic candidates from two VLMs. XGBoost predicts labels from score/entropy/agreement without requiring pool membership, then GroundingDINO locates representative justifications. Select on 20% validation of 47,203 training items before fixed SNLI-VE dev/test. 94% oracle is not deployment; Flickr30kEntities approximates localization, not full faithfulness.
  Evidence locations: §3.1–3.4; §4.1; §4.3–4.6

**2610.05622 · UndoBench: Separating Task Competence from Recovery Capability in Tool-Using AI Agents**

[Paper](https://arxiv.org/abs/2610.05622)

- **agent**: UndoBench runs same-seed control/fault pairs and separates capability, recovery, duplicates, and missed actions using independent mutation logs and state oracles. Candidate tool-agent fault-tolerance evaluation.
  Reproduction scope: 36 workflows split 14/10/12, so 20 seeds still have only 12 independent test clusters. Main study uses one lost ACK; other failures are extensions. CRSR must be N/A when control success is zero. EvoUndo's zero permission constraints do not establish full capability; B6 is post-hoc and EOR recomputed from logs. Local simulated APIs only, no real payments/services; pin versions.
  Evidence locations: §2–3; §6; Limitations; Appendix G/K/L; official README

**2610.05615 · DREAM: Dynamic Resolution Assignment For Multimodal Multi-agent Debate**

[Paper](https://arxiv.org/abs/2610.05615)

- **foundation-model**: DREAM multi-agent debate with dynamic visual resolution belongs to Agent review.
- **agent**: DREAM forms a confident set with mean-minus-SD ANLL across resolutions, allocates visual payload in five branches, discards probe history for debate, and rolls back to earlier lower-uncertainty answers using agent ANLL traces before judging.
  Reproduction scope: 500 examples per benchmark, three inference seeds. Compute genuine full-response log-probs rather than proxy confidence. α=.5 was best on the same benchmark sweep, contradicting no-tuning; reselect on validation. More tokens, not total cost reduction. LLaVA Div-MAD regresses. Code promised but no repository found.
  Evidence locations: §3.2–3.3 Eq3–4; §4–6; Appendix A/B/F/G

**2610.05572 · Disentangling Task Difficulty from Run-Level Failure in Agent Failure Prediction**

[Paper](https://arxiv.org/abs/2610.05572)

- **agent**: Decompose pooled AUROC into within- and between-task comparisons. Task-grouped CV and absolute turn prefixes distinguish difficulty from current-run failure. Candidate unified budget-control evaluation.
  Reproduction scope: Historical-difficulty oracle and semi-synthetic monitoring are diagnostic; truncation by final trajectory fraction leaks future length. Early stopping does not significantly beat relative budget allocation; thresholds .84–.93 are not universal. Recorded replay is not live agent improvement.
  Evidence locations: §4.2–4.8 Eq1–2; §6.2–6.3; §7 scope

**2610.05563 · G-CARB: Graph-Localized Conformal Agent Risk Budget for Compositional Harm**

[Paper](https://arxiv.org/abs/2610.05563)

- **agent**: CARB calibrates finite-grid corrected conformal risk on stopped-prefix full-episode harm ledgers. G-CARB supplies only prefix-visible source-to-sink paths to a fixed scorer and preserves empty proposals and threshold nesting. Candidate safety gating.
  Reproduction scope: Guarantees expected loss for exchangeable episodes, not trajectory safety or distribution shift. Ledger errors lack independent audit. AgentDojo 200 resplits are percentile variability, not independent CIs. Equal-size random context matches natural-data gains; graph advantage only on constructed diagnostics. Record counts are not tokens/latency; online 64 episodes only consistency. Code package not found.
  Evidence locations: §3–5 Algorithm1; Appendix B/C/D/G

**2610.05540 · SALUS: Automated Auditing of NL-to-SQL Benchmarks through Weak Supervision of Multi-Agent Output**

[Paper](https://arxiv.org/abs/2610.05540)

- **agent**: SALUS uses weak execution/structure/intent labels over multi-agent SQL, fits a generative label model, and trains a SQL-feature-conditioned agent-reliability decision plane on balanced confident pseudolabels. Fuses verdicts to detect benchmark errors.
  Reproduction scope: Human audit of 298 BIRD-Clean-xs items is evaluation only; train/select with weak labels. 37% error is estimated, not all gold. The 65,536-rule stacking oracle uses evaluation gold and is diagnostic. Auto SQL repair addresses only 44% Incorrect SQL and cannot resolve ambiguity/data errors. Keep dev/test separate; correlated agreement is not truth.
  Evidence locations: §3.1–3.4; §4–5.1; §5.6; §6.1; Appendix A/B

**2610.05538 · LiFT: Loop Flow Transformers**

[Paper](https://arxiv.org/abs/2610.05538)

- **foundation-model**: LiFT uses random continuous-depth coordinates to supervise iterative velocity correction with a shared DiT core. Detached initial velocity anchor and prelude auxiliary loss are essential. Matched tokens, blocks, depth, and near-equal FLOPs support comparison to dense.
  Reproduction scope: B/2 trails dense at all cost points, and all LiFT trails at trained depth. One training/sample run, 256 images only without CFG. Analytic FLOPs are not measured speed. Loop and sampling choices from public FID sweeps need independent validation.
  Evidence locations: §3.1–3.2 Eq4–9; §4.1–4.6 Tables1–2; Limitations; Appendix D.5.1/Table17

**2610.05532 · DelegationBench: Measuring When AI Agents Should Ask Before Acting**

[Paper](https://arxiv.org/abs/2610.05532)

- **recommendation**: DelegationBench concerns agent delegation and was routed to Agent evaluation review.
- **agent**: Candidate evolve infrastructure separating permissions from information needs. 156 scenarios, 48 matched pairs, and separate Act/Ask/Request/Refuse scores. Tool-Loop and post-approval test actions, not just judgments.
  Reproduction scope: No provider clients; supply independent wrappers. Three student labels are references, not truth. Tools are stateless; 13 pairs alter multiple factors. Provider terms block raw outputs and explicit-rule study is unreleased. Keep notes/reference labels away from agents.
  Evidence locations: §3–4; §5.2–5.4/Tables1–2; §6–7; AppendixO; official README

**2610.05484 · Universal Test-Time Training**

[Paper](https://arxiv.org/abs/2610.05484)

- **foundation-model**: uTTT shares fast-weight pools across layers with separate read/write routers. Matched state, active compute, and tokens support the core architecture.
  Reproduction scope: RULER still below full attention at 16.52/34.16; retrieval drops beyond 32K. Paper runs do not substitute for local A100/A30 verification.
  Evidence locations: §3; §4.1–4.3/Table2; §5.1–5.2; Appendix D–E

**2610.05481 · CodeForge-MA: Execution-Verified Multi-Agent Learning with Language-Conditioned LoRA for Multilingual Code Generation**

[Paper](https://arxiv.org/abs/2610.05481)

- **post-training**: PPO+SFT is standard; language-conditioned sparse Mixture-of-LoRA gating is the executable addition. Qwen 1.8B and 72B API tests. Preserve routing and auxiliary constraints instead of renaming PPO.
- **agent**: PPO+SFT is standard; language-conditioned sparse Mixture-of-LoRA gating is the executable addition. Qwen 1.8B and 72B API tests. Preserve routing and auxiliary constraints instead of renaming PPO.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §IV-C–D Eq.12–20; experiment configuration.

**2610.05473 · Hierarchical Reinforcement Learning with Stable Temporal Abstraction for Language Model Agents**

[Paper](https://arxiv.org/abs/2610.05473)

- **agent**: STAC subtracts premature-replanning or stale-retention costs from normalized HiPER boundary advantages according to sampled KEEP/SWITCH. PPO modifies boundary tokens only; retain host reward, critic, subgoals, and actions. Candidate hierarchical RL.
  Reproduction scope: Experiments use fixed μshort=μstale=.1 and dmin2/dmax8, not adaptive dual/budget guarantees. Best checkpoint and category results use the same validation; require separate test. Three-seed intervals are wide and success ablations insignificant. Real hierarchical training required, not rule-based switching. No new code located.
  Evidence locations: §2–4 Eq5–11; Appendix A/B/C/F

**2610.05425 · Unmentioned Checklist Findings Change How Reinforcement Learning Appears to Improve Chest Radiograph Report Checking**

[Paper](https://arxiv.org/abs/2610.05425)

- **foundation-model**: A domain diagnostic of how chest-radiograph report checklist labels affect RL.
- **post-training**: Public checklist/reader-format robustness: image writer cannot see queried sentence, checker cannot see images. Matched-label pairs and three checkers isolate omission/order. Official code/formats/analysis accessible; CheXpert needs registration. No clinical or broad vision claim.

**2610.05418 · EvoMem-VLA: State-Evolution Memory for Long-Horizon Robot Manipulation**

[Paper](https://arxiv.org/abs/2610.05418)

- **foundation-model**: EvoMem-VLA freezes paired DINO delta tokenizer and interleaves initial/recent/event state and delta memories. Keyframe head predicts future record offsets, committing only when reached. Routing is configured, not learned. GT subtasks in training vs generated test subtasks cause exposure bias; closed loop sees observations only. RMBench/RoboMME and 80 real episodes across two embodiments.
  Evidence locations: §3.1–3.4Eq. 2–6; §4.1–4.4

**2610.05417 · Render to Reason: Novel-View Semantic Prediction Improves Spatial Understanding in VLMs**

[Paper](https://arxiv.org/abs/2610.05417)

- **foundation-model**: Meta Render2Reason fuses VGGT geometry/cameras with vision cross-attention and trains auxiliary parallel 16×16 nine-class novel-view semantic CE plus QA CE, avoiding adjacent GT teacher-forcing shortcuts. Target training images only supply frozen VGGT camera features; none at QA inference. Separate 4B control from 8B system data; Appendix A.5 checks leakage.
  Evidence locations: §3.1–3.3Eq. 1–3; §4.1–4.3; Appendix A.5

**2610.05402 · Task Vector Descent: Learning from Non-IID Batches**

[Paper](https://arxiv.org/abs/2610.05402)

- **foundation-model**: TVD partially combines task vectors from consecutive same-distribution minibatch updates, interpolating Adam first moments/steps and second moments in square-root space. Fixed sample budgets and isolated train/evaluation for SFT and GRPO.
  Evidence locations: Abstract (all retrieved abstracts reviewed individually); §3.1 Eq.3–4; §3.2–3.3; §4.
- **post-training**: TVD partially combines task vectors from consecutive same-distribution minibatch updates, interpolating Adam first moments/steps and second moments in square-root space. Fixed sample budgets and isolated train/evaluation for SFT and GRPO.

**2610.05398 · MMPostTrainBench: Benchmarking Autonomous Research for Multimodal Post-Training**

[Paper](https://arxiv.org/abs/2610.05398)

- **agent**: MMPostTrainBench wraps multimodal training tasks in independent Harbor verifiers. MMResearch graphs media evidence, hypotheses, and outcomes with global/core/archive memory. Candidate multimodal evolve controller.
  Reproduction scope: Original Qwen3-Omni 30B uses eight GPUs × 24 hours; label single-GPU scaling. Test trajectories are retrospective audit only, not tuning. Three loops per pair but only one fully audited; reverting violations to base is not continuous leakage prevention.
  Evidence locations: §3.2–3.4; §4.1; §4.3–4.4

**2610.05383 · Sibyl: An Efficient Small-large Model Collaboration Framework for Long-horizon Tasks**

[Paper](https://arxiv.org/abs/2610.05383)

- **agent**: Sibyl first improves local policy with hindsight-skill OPD+RL. Replay failed prefixes to find decisive disagreements where one cloud action reverses outcomes, initialize call_cloud, then jointly train trajectory, matched-state, and consultation counterfactual credit and internalize skills. Candidate Agent RL/OPD.
  Reproduction scope: No matched local continuation means zero counterfactual credit. Abstract 95.2/80.4 are absolute success, not relative improvements. Seen140/Unseen134 and official WebShop500 test require isolated skills/tasks/validation. Break-even excludes 149.7/205.7 training GPU hours. Cloud context transfer and outages remain unresolved; real checkpoints/environment required.
  Evidence locations: §4.2–4.4 Eq9–21; §5; Appendix A/D/F

**2610.05373 · Towards Unbiased On-Policy Distillation for Block Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.05373)

- **post-training**: Un-OPD filters block decisions with aligned visible context, blends teacher and detached student logits at high teacher support, and reuses rollouts. Actual BDLM experiments. Title's unbiased does not guarantee arbitrary rollout reuse.

**2610.05367 · AIProver: Agentic Auto-Formalization of Mathematical Research via Certificate-Driven Evolving Harness**

[Paper](https://arxiv.org/abs/2610.05367)

- **post-training**: AIProver alternates model training and harness evolution, with SAM dual-view contrastive/CE, certificate RLSF, and independent fitness accept/rollback. Real formal verification required, not gold-proof fixtures.
- **agent**: AIProver alternates model training and harness evolution, with SAM dual-view contrastive/CE, certificate RLSF, and independent fitness accept/rollback. Real formal verification required, not gold-proof fixtures.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §4（SAM and HarnessEvolve）; Table 3

**2610.05342 · IRSTD-Agent: Agentic Infrared Small Target Detection via Zoom-Guided Interaction Learning**

[Paper](https://arxiv.org/abs/2610.05342)

- **foundation-model**: IRSTD-Agent tool search for infrared small targets belongs to Agent review.
- **agent**: IRSTD-Agent uses proposal/zoom/detect/drop/refine tools, constructs target-preserving, offset-recovery, and negative trajectories from training masks, and SFT-predicts tools and coordinates. Test reads native images. Candidate multimodal active vision.
  Reproduction scope: GT is training trajectory/scorer only, not test crop oracle. Proposal uses unlearned spatial filters/FFT and refine uses connected region masks; tools alone are not policy reproduction. Real 27B CUDA needs receipts. Full2000 specialized detector has higher F1; agent gains chiefly on Large44 native-size groups. Matched IoU scores matched targets, not overall success. No official code found.
  Evidence locations: §3; §4; Appendix A.1–A.4/B.1–B.2

**2610.05334 · AgentDiscover: Autonomous Discovery with Minimal Search Scaffolding**

[Paper](https://arxiv.org/abs/2610.05334)

- **foundation-model**: AgentDiscover autonomous discovery/search belongs to Agent review.
- **agent**: Sandboxed coding agents query idea/candidate/session/lesson graph and submit isolated evaluations. Fresh context across sessions retains tools and skills; a meta-agent distills search guidance from traces. Candidate open search evolve.
  Reproduction scope: Main table is single run. Separate historical AtCoder public cases used in search from official test. Isolate private future workloads, hide candidate stdout/exceptions, and never deserialize candidate pickle in scoring. Residual signal-processing metric error remains; scores do not measure real denoising. List-price estimates are not bills; original public code link not found.
  Evidence locations: §3.2; §4–5; Appendix A/B/C/D

**2610.05318 · Robust Parameter-Efficient LLM Adaptation on Analog Hardware**

[Paper](https://arxiv.org/abs/2610.05318)

- **foundation-model**: Use functionally equivalent channel scaling on frozen base, calibration-outlier splitting for LoRA, and digital residual accumulation for subthreshold updates. Candidate analog-error training diagnostic.
  Reproduction scope: AIHWKit simulation only, with perfect I/O for protected outliers. No real analog-chip energy, communication, or latency. Fixed statistics from 64 calibration batches, 2000 steps, 512 QA, and 100 holdout NLL; some single-point ablations. No analog speedup or deployment. No official code link found.
  Evidence locations: §3.1–3.3/Eq1–5; §4 setup; §5 limitations

**2610.05308 · RubricArmor: Adversarial Evolution Improves LLM-Based Rubric Generation**

[Paper](https://arxiv.org/abs/2610.05308)

- **post-training**: RubricArmor independently verifies flawed full-score attacks and iteratively patches rubrics with score-reduction and independent-review gates. 2K WildChat and actual GRPO on three policies. Preserve executable reward construction and verifiers, not string rules.

**2610.05303 · ASCENT: Online Test-Time Training of Long-Horizon Agents via Self-Distillation of Verified Experience**

[Paper](https://arxiv.org/abs/2610.05303)

- **foundation-model**: ASCENT online agent self-distillation is reviewed under Agent/post-training.
- **post-training**: ASCENT updates LoRA online only on verified success. A fixed initial teacher sees filtered self-hindsight and supervises a student without it via forward KL. No external gold; preserve strict prequential evaluation.
- **agent**: ASCENT updates LoRA online only on verified success. A fixed initial teacher sees filtered self-hindsight and supervises a student without it via forward KL. No external gold; preserve strict prequential evaluation.
  Reproduction scope: Inherited full-text review rather than a fresh reading by this agent; artifact executability not reverified. Accepted as research, not implementation.
  Evidence locations: §3.3 Eq.6–12; §4.1

**2610.05300 · MESH-Harness: Self-Improving Agent Harnesses via Bandit-Guided Compositional Evolution**

[Paper](https://arxiv.org/abs/2610.05300)

- **agent**: MESH-Harness fixes slot contracts and pool capacity, caches embeddings, chooses full combinations with full-covariance LinUCB and mixed-start coordinate search, and mutates/evicts in two slots every five evaluations using traces. Retains surrogate statistics. Candidate combinatorial harness evolve.
  Reproduction scope: Forty candidate evaluations; three reruns are one frozen harness, not training seeds. Initialization affects gains. Generate/select on validation and freeze before test; LCB private tests scorer-only. Remove evaluation duplicates from 433,926 math retrieval pairs. Mean remains additive; covariance captures joint uncertainty, not arbitrary nonlinear interaction. No official code found.
  Evidence locations: §3–5; Appendix B/C.1/C.3/C.5

**2610.05295 · Readable Before Actionable: Causal Tracing of Indirect Prompt Injection**

[Paper](https://arxiv.org/abs/2610.05295)

- **agent**: Readable Before Actionable uses counterfactual content/format role probes, activation patching, and independent hijacked-versus-resisted directions to test fixed pre-action/tool-span edits against AgentDojo attacks. Candidate safety steering experiment.
  Reproduction scope: Probe weights differ from intervention directions; high AUROC is not defense. Estimate directions in training and test held-out AgentDojo families. Llama adaptive ASR 26.3→27.4 worsens and cross-channel transfer fails. Report layer/context rebound and repeated span edits. Separate synthetic operating-point selection from formal holdout. Code not found.
  Evidence locations: §3–7; Appendix Q/V Table23

**2610.05284 · Fusion is the New Mutation: Bandit-Guided Evolution on Workflow Graphs**

[Paper](https://arxiv.org/abs/2610.05284)

- **agent**: DAGO records generation-lineage DAGs, uses five-parent combination arms and cached concatenated embeddings, and selects annealed-score-softmax fusion proposals with shared diagonal LinUCB. The LLM starts from the best parent and targets changes from summaries; child validation updates bandits. Candidate harness evolve.
  Reproduction scope: Lineage DAG is not execution DAG. Diagonal approximation changes coefficients and exploration, not full-ridge equivalence or calibrated CIs. 100 evaluations include 10 roots and at most 30×3 children; three test reruns are one frozen harness. Six tasks have val/test separation. 81.7 vs 80.3 and 11.2% lower search cost are aggregates; QA cost rose. Edges show supplied parents, not inheritance proof. Theory assumes residual/proposal coverage, no general sublinear regret. No official code found.
  Evidence locations: §3–5; Appendix B/C/E/F/G

**2610.05282 · Red-TTT: Test-Time Training for Automated Jailbreaking Large Language Models**

[Paper](https://arxiv.org/abs/2610.05282)

- **post-training**: Red-TTT performs per-target test-time LoRA with softmax(beta reward) minus uniform risk-preference advantages, increasing beta and using elite replay. Fixed 120-query budget. Algorithm review only; no attacks executed.

**2610.05274 · Answer with Evidence: Consistency-Aware Grounded Visual Question Answering for Roadside Traffic Scenes**

[Paper](https://arxiv.org/abs/2610.05274)

- **foundation-model**: EtA uses a box-then-answer sequence. ECPO clusters boxes by cross-sample IoU over G rollouts with support ≥max(2,ceil(.25G)) and applies Hungarian coverage plus format/reference answer reward before GRPO. No GT boxes in RL does not mean label-free. RoadSceneVQA/gRefCOCO/CARPK span tasks; structural consistency existence does not prove full grounding.
  Evidence locations: §IV-AEq. 5–8; §IV-BEq. 9–11/Algorithm 1; §V

**2610.05273 · When and What to Prune? Stage-Aware Visual Token Pruning for Efficient VLA**

[Paper](https://arxiv.org/abs/2610.05273)

- **foundation-model**: SAPrune calibrates three stable action-attention depths without reward, then budgets top-attention and functional-diversity paths using QR explained mass times attention concentration. Prune only visual tokens. Three VLAs on LIBERO/SIMPLER and four real runs; RTX5090 SDPA latency differs from FA2 and cannot be replaced by FLOPs.
  Evidence locations: §3.2 Eq.5–9; §3.3 Eq.10–14 onward; §4.1–4.4; Appendix B.4.3.

**2610.05247 · templar: agentic induction and evolution of standardized radiology reporting templates from large-scale clinical corpora**

[Paper](https://arxiv.org/abs/2610.05247)

- **agent**: TEMPLAR stores templates and anatomical/diagnostic provenance graphs. Span–Triple dual-view BM25/embedding graphs with Leiden derive slots; a structured reducer constrains edits, external evidence grounds findings, and structured training feedback calibrates granularity. Candidate multimodal/medical agent mechanism.
  Reproduction scope: Training findings induce templates and impressions build the diagnostic graph; test impressions are judge-only. Reconstructed z is the only current patient fact, while retrieved training phrases are linguistic priors. Confirm four clinical datasets and English report licenses. Diagnostic fidelity is LLM reference scoring, not diagnostic accuracy. Temperature zero still has truncation/retries/context mismatches. Code not found.
  Evidence locations: §3.1–3.4; §4; Appendix A/B/C.1/C.6/F

**2610.05190 · FORGE: Verification-Gated Behavioral Repair for Generative Language Models**

[Paper](https://arxiv.org/abs/2610.05190)

- **foundation-model**: FORGE uses prefix/LOO toxicity localization, classifies tokens, then edits lm_head by low-rank QP or MLP null space, regenerates, and commits/rolls back. Candidate auditable weight repair.
  Reproduction scope: Fixed-hidden linear margin certificates cover only repaired examples/positions. Toxicity oracle is not true safety; QP and null-space guarantees differ. Repeated repair on evaluation tasks is not generalization. No official code located.
  Evidence locations: §III-C–F; §IV-A/G/H; §V limitations

**2610.05185 · Recurrent Latent Visual Search for GUI Grounding**

[Paper](https://arxiv.org/abs/2610.05185)

- **foundation-model**: ReLaViS feeds latent slots back as spatial distributions and evidence vectors; CWC combines candidate-quality lower bounds and truncated final Gaussian KL. Train warmup, GT-latent teacher forcing, and predicted self-conditioning. Test screenshot/query only with 3×3 peak-neighborhood coordinates. 100k train/5k validation and five isolated GUI benchmarks; grounding is not agent task completion.
  Evidence locations: §3.1–3.4Eq. 1–9; §4.1–4.3

**2610.05176 · AECG: Asymmetric Experience Consolidation and Governance In Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.05176)

- **agent**: AECG scopes memory by team/event/agent, records success and attribution-trusted failures asymmetrically, and detects degradation with slow accumulated and fast discounted Beta-like scores. Review under downstream exposure budget; enable narrow/repair versions only after paired failures and disjoint success replay. Candidate Agent memory/RSI.
  Reproduction scope: Beta-style scoring is not a full posterior. Noise-corrected drift is not calibrated significance; reachability exposure is not causality. Separate AgentBoard dev, four public benchmarks, three independent seeds. Controlled corruption is diagnostic; also test natural drift. Report unattributed or misattributed failures.
  Evidence locations: §3–4; Appendix B.1–B.4/C

**2610.05162 · Memadapter: Counterfactual Adaptation Against Memory-induced Sycophancy**

[Paper](https://arxiv.org/abs/2610.05162)

- **agent**: MemAdapter freezes retrieved memories, constructs counterfactual tasks to infer usage boundaries, reflects on current context to constrain inferential roles, and answers from evidence. Does not alter upstream memory/retrieval. Reliability candidate.
  Reproduction scope: Match identical retrieved inputs per instance and system. Gold/reference belongs to official judge only. 75 controlled instances include manual reconstruction and are diagnostic, distinct from three public benchmarks. Some PersistBench beneficial-memory failures rise. Count three stages of calls; temperature .2 is not independent seeds.
  Evidence locations: §3–4; Appendix A/B/D/G/H

**2610.05139 · Hidden in the Comments: A Context-Injection Attack Surface in Code LLMs**

[Paper](https://arxiv.org/abs/2610.05139)

- **post-training**: Public security evaluation: dual Flask prompt conditions, generation harness, five-component detector, and comment-position controls. Zenodo API confirmed open/published Manuscript_Codes.zip and checksums. Scaffolds are not paired and task types confound; detector references conditions rather than vulnerability gold, so no pure causal or true vulnerability-accuracy claims.

**2610.05132 · SpecAgent: Empowering Program Verification with Agentic Synthesis of Formal Program Specifications**

[Paper](https://arxiv.org/abs/2610.05132)

- **agent**: SpecAgent plans function/loop dependencies and uses ACSL RAG for annotations. Frama-C/WP can revise upstream contracts, while equality of two same-input returns probes specification completeness. Public C/SV-COMP tasks support formal-agent research.
  Reproduction scope: Only annotations may change. Gold specs only for precision/recall judges; proved goals are not complete semantics. Return uniqueness has limited scope and Frama-C/WP can have false negatives. 50 programs, 14 repos, 811 targets are not all languages. Match solver/version/timeouts; official code not located.
  Evidence locations: §3–5; Threats to Validity

**2610.05126 · Selecting Repetition Counts Across Model Scales in Data-Constrained Pretraining**

[Paper](https://arxiv.org/abs/2610.05126)

- **foundation-model**: Use seed bootstrap/log-N regression on small-scale repetition-loss curves to select Top-3 and a two-term curve argmin. Executable pretraining budget selection with frozen choices before target prediction and independent test.
  Reproduction scope: r also changes generic exposure and length, not isolated repetition. 65.6% 6ND savings assume only retained runs, while actual validation uses all seven grid points. Later 80M/520M spot checks and 9/11 exploration are not prospective. Unknown offset prevents absolute loss without large-model data.
  Evidence locations: §3.1–3.2; §5.1–5.3 Eq6–8; §6.1–6.3; §7

**2610.05124 · Memory Canonicalization: A Framework and Benchmark for Cross-Model Drift in Persistent LLM Memory**

[Paper](https://arxiv.org/abs/2610.05124)

- **agent**: Disambiguate structure, extract emotion fields, and verify independently on memory writes. CMSC-E uses one natural-language rendering to separate content rewrite from JSON format; candidate drift diagnostic.
  Reproduction scope: Four write-time calls and store conflict retrieval costs not measured. Pilot gains not significant after multiple correction. Retain raw and canonical evidence; emotion fields are not psychological diagnoses.
  Evidence locations: §IV pipeline; §IV-I three-arm; §VI statistics; conclusion/Code Availability

**2610.05107 · SearchJev: A Fast and Calibrated System-1 Model for Search Agents**

[Paper](https://arxiv.org/abs/2610.05107)

- **agent**: SearchJev reads legal-option token logits directly, trains LoRA with source-weighted CE+Brier soft labels, calibrates temperature by output type on separate validation, and delegates uncertainty to System 2. Jev/Agent search candidate.
  Reproduction scope: Public originals can reconstruct semantically equivalent evaluations, but no full SearchDecision-Bench or official code located. One 100-item BrowseCompPlus run is limited. AR baseline lacks matched task SFT. OOD calibration does not always improve, and batch-1 decision latency is not system cost. Gold is training/scorer only.
  Evidence locations: §2–5; SearchDecision-Bench split; SLCD Eq; BrowseComp-Plus protocol

**2610.05099 · Small Agents with Semantic Search: Efficient Multilingual Code Localization**

[Paper](https://arxiv.org/abs/2610.05099)

- **post-training**: Code localization uses existing quality-weighted SFT, Dr.GRPO/DAPO, and domain F1/turn rewards. Main contributions are semantic-search harness and data, not new post-training core. Gold is for training weights only. This ruling applies to the post-training core track; Agent methods/data are considered independently.
- **agent**: Compact localization uses colgrep late-interaction CPU indexes, training-only gold for turn-weighted SFT, then DrGRPO/DAPO dynamic filtering and asynchronous rollouts. Public SWE-Lite/MultiSWE-Flash locate files by base commits. Candidate agent post-training.
  Reproduction scope: Reference patches represent one solution; file F1 is not issue resolution. Gold Top-10 subset is a retrieval upper bound and hidden from evaluated agents. Training excludes benchmark repos/shared histories and fixes pre-query state. Five eval seeds are not training repeats. Timing excludes prebuilt indexes; tool-interface controls require regenerated demonstrations. No official code found.
  Evidence locations: §3–5; §6 Limitations; Appendix A.5–A.7

**2610.05097 · ReMAP: Restoring the Perceptual Cycle with Reasoning-Time Latent Visual Memory**

[Paper](https://arxiv.org/abs/2610.05097)

- **foundation-model**: ReMAP uses global/local latent visual memory, region localization, staged formation/access training, and RL for when to retrieve. Ten benchmarks; retain real visual memory, not a text oracle.
  Evidence locations: Abstract (all retrieved abstracts reviewed individually); §3.1–3.2; §4.
- **post-training**: ReMAP uses global/local latent visual memory, region localization, staged formation/access training, and RL for when to retrieve. Ten benchmarks; retain real visual memory, not a text oracle.

**2610.05066 · Salvation Lies Within: Eliciting Inherent Style Transfer in Step-Distilled Diffusion Models**

[Paper](https://arxiv.org/abs/2610.05066)

- **foundation-model**: StyleForge's training-free agent extracts render, color/light, composition, and reference-content states, then compiles constraints from color/brightness statistics in fixed order to preserve style, weaken composition, and exclude content before few-step FLUX2Klein. 31 styles × 16 prompts and three Qwen judge controls. Structured prompt operator, not diffusion training or distillation; model scores are not human preference or live A/B.
  Evidence locations: §3.1–3.4; §4.1–4.3

**2610.05047 · Beyond Task Completion: Measuring Interaction Cost in Terminal User Interfaces**

[Paper](https://arxiv.org/abs/2610.05047)

- **agent**: TUINaut shares real TUI I/O in Docker+Tmux and scores completion with independent state oracles. Agent-KLM reports reasoning tokens and atomic keys separately for interactive cost diagnostics.
  Reproduction scope: 84 tasks in 15 repos; 30 have fingerprints. Screen text alone does not prove completion. Tokens and keystrokes cannot be added or mapped to human cognition time. Run real TUIs rather than expected-state fixtures. Repository page failed and needs API recheck, independently of mechanism definition.
  Evidence locations: §2.2 Eq3–5; §3.2–3.4; §6.3

**2610.05039 · Causal Improvement Graph for Agentic Harness Optimization**

[Paper](https://arxiv.org/abs/2610.05039)

- **agent**: CIG persists a typed Evidence–Hypothesis–Intervention–Outcome graph. Observe/Plan/PlanSelect/Implement/Evaluate/Update call local proposers; external validation revises hypothesis assessments before portfolio selection. Candidate harness RSI/evolve.
  Reproduction scope: Causal naming does not identify causality. Seven ordinal criteria and pairwise redundancy use LLM judgments. Freeze validation selection before holdout; test-oracle regret is external diagnosis only. Eight candidates and three or five short runs do not establish long-run transfer; match wide/deep schedules. Code not located.
  Evidence locations: §3–4; Appendix A.3–A.8

**2610.05030 · EVISKILL: Grounding Skill Evolution in Replayable Evidence**

[Paper](https://arxiv.org/abs/2610.05030)

- **agent**: EviSkill derives Replayable Evidence Cards from training spans and links local edits. Restore prefixes and rerun to verify/reflect; global validation updates ValidatedSkill. On global rejection, retain only locally supported edits in WorkingSkill for future epochs. Candidate skill RSI.
  Reproduction scope: Real state restoration and reruns are defining, not static LLM judgment. Local acceptance is not global promotion. Separate train/validation/test and freeze only ValidatedSkill for test; cross-epoch contrasts are training-only. Guard memorization and report card counts, replay calls, and costs; six backbones are not independent seeds.
  Evidence locations: §3–4; Appendix B/E/F prompt templates

**2610.05026 · GeoBridge-VLA: Geometry-Aware Residual Adaptation for Vision-Language-Action Models**

[Paper](https://arxiv.org/abs/2610.05026)

- **foundation-model**: GeoBridge-VLA decodes K4 neighborhood geometry from native visual features with simulated depth or real DA3 pseudodepth, then freezes geometry/VLM and adds zero-init 1×1 residuals gated near .002. Flow plus RMS residual penalty. SmolVLA LIBERO/OMY only; unchanged token count does not remove decoder compute. No cross-backbone verification.
  Evidence locations: §III-AEq. 1–2; §III-BEq. 3–4; §IV-A–C; §V

**2610.05025 · Triggering Generalist Reasoning via Predictive Uncertainty for Dual-System VLA**

[Paper](https://arxiv.org/abs/2610.05025)

- **foundation-model**: TUD separates π0's heavy PaliGemma cache and current SigLIP/Q-Former/action expert. Across observations, re-predict fixed slots under one anchor and use SD to proxy plan change. Online p70 of running means and maxskip trigger refresh; execution uses committed chunks, not every probe. VLA-Arena/CALVIN/real hardware; variance is not calibrated epistemic uncertainty and probes cost compute.
  Evidence locations: §3.1–3.3Eq. 2–6; §4.1–4.4; Appendix B/C

**2610.05024 · LightVLN: Efficient Aerial Vision-and-Language Navigation with Compact Memory and History-Guided Local Aggregation**

[Paper](https://arxiv.org/abs/2610.05024)

- **foundation-model**: LightVLN keeps one learned-query token per historical frame in FIFO and uses history selection to aggregate fixed 32 local regions in the current 16×16 grid. Separate OpenFly/AerialVLN training and unseen campuses. Full model 1.276B, not .5B; separate 4090 profiling from closed-loop routes. No extra memory encoder does not remove vision backbone.
  Evidence locations: §III-B/CEq. 1–5; §III-D/E; §IV-A–D

**2610.05023 · Look Where You Say You're Looking: Self-Grounded Attention for Visual Reasoning**

[Paper](https://arxiv.org/abs/2610.05023)

- **foundation-model**: Self-Grounded Attention localizes each CoT observation with GroundingDINO, combines selected-head regional saliency, exact-match/judge, and format reward for GRPO. Head selection uses VisualCoT relevance and attention is not causal faithfulness. SaliencyR1-8k training and 25 VQA lmms-eval tests. Preserve real locator/judge and eight-H100 budget, not answer-aware fixtures.
  Evidence locations: §3.2–3.5（saliency reward, GRPO, head selection）; §4.1–4.2/Table1

**2610.04991 · CIPO: Counterfactual Imagination Policy Optimization for Adaptive Tool Granularity Selection**

[Paper](https://arxiv.org/abs/2610.04991)

- **agent**: CIPO mines successful training tool chains by budgeted BPE and builds binding/trace/interrupt skills. G4 rollouts fork two bases at first eligibility into atomic/skill paths with the same continuation policy. Bounded outcome difference augments reward for GRPO. Candidate Agent RL/tool genomes.
  Reproduction scope: Forks train only and test cannot see gold chains. Clone real environment state, not final answers. Main TSR counts partial success; five judge repetitions are not five training seeds. Report L.1 yes-only and ToolAthlon three training seeds in real environment separately. Fewer policy decisions are not tokens/latency, and baselines are rewritten in the same simulator. Code not found.
  Evidence locations: §3–4; Appendix D/E/L.1/O/P

**2610.04961 · Building LLM Agent Systems the Deep Learning Way: From Modular Design to Architecture Search**

[Paper](https://arxiv.org/abs/2610.04961)

- **foundation-model**: Deep-learning-inspired agent architecture search and prompt optimization belong to Agent review.
- **agent**: LLM building blocks compose single calls, recursive history, ToT/GoT, and multi-query RAG; self-reflection edits metaprompts. Optuna searches token/head/retrieval settings on 30% train before frozen 70% test. Public GSM8K/StrategyQA/TSP support modular search.
  Reproduction scope: Transformer/RNN are workflow analogies, not neural training; feedback propagation edits text, not gradients. Related-multi promised after review, not complete existing results. Citation-reference retrieval F1 is not writing quality. Gold is external scoring only. Match 120-trial costs to random search.
  Evidence locations: §3–4; Appendix B/C/D Optuna ranges

**2610.04950 · How Should Teachers Be Prepared? RL on Student-Induced States for On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.04950)

- **post-training**: Prep-OPD first trains the teacher with RL on prefixes from a fixed initial student, then freezes it for OPD. DeepMath and eight math benchmarks. No gold solutions injected; preserve state distributions in both stages.

**2610.04940 · Software World Models: From Consequence Prediction to Decision Value**

[Paper](https://arxiv.org/abs/2610.04940)

- **agent**: SWM executes counterfactual changes from restored training worlds, uses SFT warmup plus GRPO to predict downstream blast sets, and uses sampled probabilities for transfer and paid checks. Real OSS and independent synthetic worlds are verifiable.
  Reproduction scope: Graph reachability does not replace learning; both complement. Expert exploration uses privileged graphs as a training control only. Prediction F1 and decision regret differ. Public environment replay remains to be checked.
  Evidence locations: §3.1–3.3/Algorithm1; §4; Appendix D.5–D.13

**2610.04927 · Assembling Insights for Agentic Machine Learning Engineering Systems**

[Paper](https://arxiv.org/abs/2610.04927)

- **agent**: MLE-InsightForge distills competition/domain/improvement insights from source contest gold solutions and inserts them into ReAct trees under trigger/action conditions. 160 Kaggle tasks across 12 domains support source/target isolation.
  Reproduction scope: Never read target winning solutions. Rerun final selections externally on private test inputs. Check Kaggle access, terms, and download eligibility per task. Source isolation does not remove pretraining contamination.
  Evidence locations: §3–5; normalized p33,44–55

**2610.04921 · Complex Agents, Shallow Tests: Demystifying and Enhancing Test Adequacy of Agent Harness in the Wild**

[Paper](https://arxiv.org/abs/2610.04921)

- **agent**: HarnessTester uses coverage to find untested LLM-dependent code, then AST retrieval of constructors, fixtures, and mock bindings to preserve call contracts and generate branch tests. Candidate harness engineering tool.
  Reproduction scope: Same model and 120-minute budget; separate scoped and general baselines. Mocks must match provider structures and injection points. Coverage or mutant kills are not real model capability. Isolate known patches for historical bugs. Official artifact link could not be recovered from extracted text.
  Evidence locations: §6 HarnessTester; §7 coverage/mutants; §8 H-Bench; threats/artifact statement

**2610.04918 · Residual Visual Credit Optimization: Conserved Evidence Routing for Multimodal Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.04918)

- **foundation-model**: RVCO multimodal RL token credit belongs to post-training.
- **post-training**: RVCO scores evidence by likelihood changes after image-patch interventions, routes with IQR/entropy, and uses residual correction to preserve response credit mass. ViRL39K trains four VLM families; requires real visual interventions, not fixed token heuristics.

**2610.04916 · PreAct-Nav: Agentic Reasoning Before Action for Urban Navigation**

[Paper](https://arxiv.org/abs/2610.04916)

- **agent**: PreAct-Nav uses Navigation Memory subgoals and an on-demand Predictive Sandbox to generate future-action cues. Frozen VLM reviews before acting, falling back to the original policy when evidence is unresolved or revisions ineffective. UrbanNav/CityWalker allow verification.
  Reproduction scope: Predictions use only current observations and proposed actions, never real futures. Match action formats and decision budgets, count prediction/memory/review costs, and separate seen/unseen.
  Evidence locations: Method action-review loop; normalized p36–55; Appendix D/F/G

**2610.04915 · Are We Measuring Scientific Intelligence? Rethinking the Evaluation of AI Scientists**

[Paper](https://arxiv.org/abs/2610.04915)

- **agent**: Validate null, withdrawal, and flip counterfactual data statistically to test whether scientific agents respond to evidence. EGA separates matching old keys from responding to new evidence. Candidate research integrity evaluation.
  Reproduction scope: 18 single-cell and four synthetic genetic-statistics tasks with manual counterfactuals and few models. Strip filename/gzip-header/raw-layer leaks. Only verifier sees reference statistics and gold; response to evidence is not full scientific quality, and old answers cannot score flips.
  Evidence locations: §4.1–4.3 Eq2–5; §5; Appendix B/D; Limitations

**2610.04899 · Rewrite What Matters: Adaptive Multilingual Query Rewriting for Reasoning via Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.04899)

- **post-training**: mRewriter-R1 trains rewriting on frozen downstream accuracy using standard GRPO. Aspect/operator planning is an application framework, not a core optimizer. This ruling only applies to post-training; Agent methods and public data are assessed independently.
- **agent**: mRewriter-R1 executes finite language, structural, and semantic operators in sequence, optimizing frozen downstream outcomes with GRPO. MGSM/BELEBELE/XCOPA use defined training and standard language tests.
  Reproduction scope: Not unrestricted rewriting; semantic/numeric/entity preservation is imperfect, so measure regressions. Three inference averages are not training seeds. Downstream gold is only training reward or test scoring.
  Evidence locations: §3/GRPO; Appendix A/D/F; normalized p16,29,82–106

**2610.04889 · ForkPilot: Self-Evolving Policy for Retrospective Search in Long-Horizon Agents**

[Paper](https://arxiv.org/abs/2610.04889)

- **agent**: ForkPilot restores matched state for search-versus-skip trajectories and trains task-bootstrap ensembles. Cost, support, and calibrated margins choose commit/probe/skip. Frozen within tasks and updated across completed source tasks; six public benchmarks.
  Reproduction scope: Actually restore environments and isolate writes. Update experience only after completion, without current future outcomes. Select λ and thresholds source-only. Conformal coverage concerns realized paired targets, not guaranteed loop means.
  Evidence locations: PDF pp3–6; Algorithm1 p21; Appendix D.3/Table6

**2610.04882 · ResOPD: Tail Residualization for Sparse On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.04882)

- **post-training**: ResOPD uses exact top-k mass and a tail bucket baseline, with coarse per-step gradients plus rare tail residual for unbiased estimation under full-support ancestral sampling only. Main math uses top-p=.95/top-k20, outside that condition; separate mechanism and results.

**2610.04868 · From Memory to Guide: Spatio-Temporal Composer for Procedural Coding Memory**

[Paper](https://arxiv.org/abs/2610.04868)

- **agent**: Composer selects a skill and retains whyNow, binds rules to current entities in a Runtime Guide, and exits to task requirements on completion/invalidation. Implementable adaptation over a fixed Skill Bank.
  Reproduction scope: Access and permissions for 13 EngramBench items and private eight-hour tasks were not verified. 7.2pp/32.2% are not public general-benchmark results; guides cannot contain future fixes.
  Evidence locations: Method/Algorithm1; normalized p28–51; Experiments p52–63

**2610.04851 · CURIO: Curiosity-Driven Test-Time Learning for Open-Ended Discovery**

[Paper](https://arxiv.org/abs/2610.04851)

- **post-training**: CURIO trains a hidden-state transition predictor and caches pre-update residuals. Normalize by epoch and add bonuses only to sampled non-top-k tokens. Not guaranteed semantic novelty; encoder or predictor can collapse. Measured scientific discovery tasks.

**2610.04845 · Which Preferences to Train On? End-to-End Multi-Objective Alignment with an Adversarial Preference Distribution**

[Paper](https://arxiv.org/abs/2610.04845)

- **post-training**: MAESTRO uses DirUEG for an adversarial Dirichlet preference distribution, separates adversary/policy batches, and scalarizes vector-reward GAE by preference. Multiobjective HH/Beaver and summary faithfulness tests.

**2610.04824 · Agent Behavior as Code: Efficient and Robust LLM Agents with Programmatic Specifications**

[Paper](https://arxiv.org/abs/2610.04824)

- **foundation-model**: ABCAgent specifies behavior with symbolic programs and belongs to Agent review.
- **agent**: ABCAgent uses programs with unbound inputs. An executor manages scoped typed state, and the LM designs or revises programs. Public GAIA, WorkArena, GSM-Symbolic, and tau2 base tasks can be checked.
  Reproduction scope: Author code and augmented GAIA/WorkArena-CF are promised after acceptance, not reproduced on the 18 added tasks. GAIA dev was a paper evaluation set, so prevent post-hoc code edits. Do not hardcode instance answers.
  Evidence locations: ABCAgent design/execution separation; Experiments; Appendix C/D; normalized p15,22,24–27

**2610.04805 · ExStereo: Lifting 2D Vision-Language-Action Models to 3D with Explicit Stereo Representations**

[Paper](https://arxiv.org/abs/2610.04805)

- **foundation-model**: ExStereo builds four-direction orthographic depth/XYZ/valid features from frozen FastFoundationStereo, calibrated fxB/d, and tabletop RANSAC. Action-query cross-attention residuals join the VLA without replacing prefix/VLM. Seven 3,500-episode midtraining tasks and ten evaluation tasks/objects are disjoint; post-training uses 100 episodes/task. RoboTwin and three real tasks with 20 runs each. Count depth/calibration cost and preserve percentage-point success differences.
  Evidence locations: §IV-A–C; §V-A–C/TableI; §VI/TableIII

**2610.04794 · Knowing the Store: What a Memory Backend Must Write Down Before an Agent Can Read It**

[Paper](https://arxiv.org/abs/2610.04794)

- **agent**: Candidate memory-governance diagnostics: separate active/superseded/retracted/expired and current/past/change intent; compare value-free status summaries, returned tags, and simple name lookup. 444 counterfactual store versions for matched questions; the paper specifies public code/data.
  Reproduction scope: Monitoring diagnostic, not a new capability algorithm. Gold oracle tags are upper bounds only, not agent input. Forty synthetic personas, some groups of 30. Matched AUROC is post hoc and 71 comparisons uncorrected. No human mention labels or evidence of better answers; backend write maintenance unimplemented.
  Evidence locations: §3 pp.2–3 lifecycle / coverage; §4–8 controls; §9 p.8 limitations; Reproducibility p.9

**2610.04792 · Do More Modalities Always Help? A Geometric Perspective on Missing-Modality Robustness**

[Paper](https://arxiv.org/abs/2610.04792)

- **foundation-model**: GU edits Grassmann subspaces for missing images; candidate multimodal robustness operator.
  Reproduction scope: Train a matched T model, not just millisecond editing; Table 4 includes reference cost. Shortest geodesics are not task optimality. Select k/η/layers on development only and isolate test. No author code found.
  Evidence locations: §3–4; §5 Eq1–5; §6.1–6.5 Tables2–4; App D/E

**2610.04779 · Asymmetric Repository Lineage Modeling and Verifier-Guided Coordination in Concurrent AI Coding Agents**

[Paper](https://arxiv.org/abs/2610.04779)

- **agent**: MergeGym separates open-time authored-file overlap, actual Git merge-tree conflicts, and schedule replay. T1 on 229 held-out repos, 5,936 replayable T2 cases, and scheduling on 97 repos support executable infrastructure.
  Reproduction scope: T3 fixes historical labels and durations and uses nonreactive agents, not causal production testing. Oracle gates are not deployable; 31 unreconstructable patches cannot count as clean. Semantic conflicts remain.
  Evidence locations: MergeGym T1/T2/T3; lineage replay; normalized p24–41,59

**2610.04753 · More Value per Key: Asymmetric Sparse Attention for Faster LLM Decoding**

[Paper](https://arxiv.org/abs/2610.04753)

- **foundation-model**: SAGA decouples key and value head counts and refreshes approximate top-N thresholds periodically. Convert pretrained GQA with data-weighted key merging, minimum-weight matching, and KL+CE distillation, not head deletion alone.
  Reproduction scope: Initialization ignores RoPE. Long-context speed does not imply short-context speed, and quality drops. H200/B200 timings and ~23K distillation iterations need new A100 measurements; approximate top-N need not return exactly N.
  Evidence locations: §3.1–3.2; §4.1 Eq13–18; §5.1–5.3 Tables1–2; §6; official repository

**2610.04721 · Knossos and Ariadne: Benchmarking and Learning Complete Diagram Topology Extraction with Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.04721)

- **foundation-model**: Meta-coauthored Ariadne predicts node inventory, emits typed edges from groups of three active sources to all predicted nodes, merges deterministically, and traces separately. Inference does not read GT inventory. Knossos has 18k/1200 across six domains with different seeds, plus 162 TopoBench diagrams. Within-template seed isolation is not unseen grammar generalization. Public dataset/repo links are given, with independent value in method and graph evaluation.
  Evidence locations: §2.3–2.5; §3.1–3.3Eq. 1–2; §4.1–4.4; Appendix B.5; README Quickstart/Ariadne/Code and Assets; adapter weights not included

**2610.04699 · Not Self-Decidable: LLMs Cannot Draw the Boundary of What an Agent Verifier Can Check**

[Paper](https://arxiv.org/abs/2610.04699)

- **agent**: CoVer uses model corroboration only to nominate checks, generates fact slots and rules, and verifies structure, groundedness, invariance, and sensitivity. It uses infrastructure-attested fields and fails closed on missing or anomalous values.
  Reproduction scope: The 73 rules and 36 synthetic records are narrow. Precision does not exceed unanimity at the same elimination rate; do not claim decidability is solved. LLM-filled consent is not external authorization evidence. Keep human and LLM ground truth separate.
  Evidence locations: §6/CoVer Algorithm1; normalized p53–60; Appendix A/E

**2610.04687 · Understanding Errors in LLM-Based Question Answering over Imperfect Tables**

[Paper](https://arxiv.org/abs/2610.04687)

- **agent**: GBDI uses five independent discovery contexts with randomly permuted table rows, maps back to original rows, merges a union ledger, and applies Edit, Drop, or No-op using verifiable evidence. RADAR-T offers 313 cases, 53 tasks, and 27 tables.
  Reproduction scope: Human-repaired tables are oracle upper bounds. Real agents must verify independently. The method does not apply to row-order-dependent questions; use source-table clustered intervals and expose observed tables rather than clean sources or gold repairs.
  Evidence locations: GBDI workflow; normalized p11,29,39,45,55–61; Appendix A/B/E/F

**2610.04658 · RETRACE: From Entangled Repair Histories to Reusable Experience for CI Repair**

[Paper](https://arxiv.org/abs/2610.04658)

- **agent**: RETRACE attributes changes backward from CI repair endpoints and forward through development history to form three levels of reusable problem-level experience. CI-Repair-Bench covers 565 PRs in 101 repositories, with the earliest 30% as history and 408 later targets.
  Reproduction scope: Maintain historical/target temporal isolation. Some CI dependencies and custom actions cannot be reproduced locally. Lightweight local checks are not full CI repair success; do not read future target endpoints.
  Evidence locations: RETRACE bidirectional attribution/three abstraction levels; normalized p55–57,67–68; Appendix A

**2610.04651 · GS-Codec: A Gaussian-Splatting Bottleneck for Neural Audio Coding**

[Paper](https://arxiv.org/abs/2610.04651)

- **foundation-model**: GS-Codec fits latents with an inner loop of continuous 1D Gaussians, trains the codec with stop-gradient and commitment, trains a latent reconstruction predictor instead of 300 Adam steps, and calibrates k-means scalar quantizer parameters on a holdout after training. Fixed centers need no transmitted positions; bitrate remains discrete. Distinguish 2,339-hour and 54k-hour configurations across LibriTTS/LJSpeech/LibriSpeech. Some baseline values are citations rather than reruns. The 7.9 ms L40S number is encoder-only for noncausal three-second clips, not end-to-end streaming latency.
  Evidence locations: §3.1–3.2；§4.1–4.3/Table4；limitations
- **post-training**: GS-Codec is a neural-audio bottleneck using Gaussian splatting; its post-training keyword refers to bitrate control.

**2610.04646 · SEIS: Self-Evolving Inference Systems**

[Paper](https://arxiv.org/abs/2610.04646)

- **agent**: SEIS gives the agent a private code worktree, fixed correctness/throughput scorer, and budget. Successfully verified changes inherit the actual inference engine and kernels. Public Qwen and real GPU workloads can test code evolution.
  Reproduction scope: This is not registry-only integration. Verify decoding, natural EOS, and generation capability; the paper rejected 14 termination failures. Matching MMLU prefill does not establish decode equivalence, and single-request throughput is not concurrent serving.
  Evidence locations: SEIS session/harness gates; §5–6; normalized p16–22,36–54; Appendix B/F

**2610.04641 · Back to the Future: Regressing Readability Features from LLMs**

[Paper](https://arxiv.org/abs/2610.04641)

- **agent**: BTTF combines AST-tagged segment embedding geometry/clustering, frozen code-LM construct-level surprisal and 32/256-token context differences, and conventional code features. Cross-model stability consensus selects 11 features. Dataset-balanced Ridge with alpha=200 predicts quantile-transformed readability and reports signed feature contributions.
  Reproduction scope: The 1,100 public human-scored examples are mostly Java. Feature selection uses all six datasets, so LODO checks prediction transfer with a fixed representation, not leakage-free transfer of selection itself. Fit imputation, clipping, and normalization within each fold. Thirteen transformations diagnose readability direction; parsing does not establish semantic preservation or functional correctness. This can support coding-agent quality assessment, not execution-correctness reward.
  Evidence locations: §2.1–2.2、Table1、§3.2–3.4、§4.6、AppendixA/B、§8

**2610.04616 · PerturBot: Breaking Shortcut Priors in Vision-Language-Action Models with Perturbative Training**

[Paper](https://arxiv.org/abs/2610.04616)

- **foundation-model**: PerturBot's V/C/R respectively use task-preserving viewpoint perturbations, state/skill language relabeling, and relabeling of executed off-target motions, mixed with the original flow loss rather than invented recovery to failed targets. Paired GroundFscore uses shared noise to test null invariance and causal sensitivity separately; calibrate Δaction with two expert records from the same state and preserve denominator flooring and filtering. This is a diagnostic, not a capability certificate. Fifty real PnP layouts and 50 RoboTwin tasks include equal-budget/full-factorial ablations; 84% success is not merely an offline score.
  Evidence locations: §3.1–3.3 Eq3–4；§4.1–4.3/Table1；AppendixA/F

**2610.04611 · Practical Runtime Enforcement of First-Order Temporal Requirements**

[Paper](https://arxiv.org/abs/2610.04611)

- **agent**: EnfFlash compiles an executable MFOTL fragment into a tabular EF causal/suppression runtime, compares with a reference interpreter on real traces, and is a candidate external policy-enforcement backend. Baselines are checkable across 40 formulas and agent environments.
  Reproduction scope: Support only the declared fragment; nested future/past operators need rewriting. Real-time enforcement is not LLM semantic authorization. MonPoly monitors rather than performing the same task. Retain timeouts and maximum latency.
  Evidence locations: §4/EF Algorithm2; §5; normalized p50–53,139–148

**2610.04607 · ForeAct3D: Policy-Grounded Future World Modeling for VLA Policies**

[Paper](https://arxiv.org/abs/2610.04607)

- **foundation-model**: ForeAct3D decodes current/future depth, three-class masks, and poses from six policy-feature queries; future decoding accepts only policy-generated actions. Training uses background staticity, Kabsch rigidity by GT instance, and kinematics; inference needs no future or GT inputs. Same-pixel correspondence is a short-term approximation, and strong supervision and rigid-body assumptions are material. LIBERO 98.3, CALVIN 3.73, and 37.8% real-robot performance have ablations. Geometry baselines use different horizons, and predicted-mask localization still uses GT instances; do not claim GT-free instance detection.
  Evidence locations: §3.1–3.4 Eq3–5；§4/Tables1–2；AppendixA.1–A.4/Table8；limitations

**2610.04604 · Anticipating the Consequences of Curriculum Decisions with Large Language Models**

[Paper](https://arxiv.org/abs/2610.04604)

- **post-training**: An LLM guides a Craftax curriculum, but the trained model is the environment RL learner, not an LLM post-training target.
- **agent**: The curriculum builds cross-task relationships and a feasibility graph from all 256 Craftax objective descriptions and chooses tasks with historical learning progress. Public environments and success predicates for all objectives enable training verification.
  Reproduction scope: An LLM graph prior is not measured causal transfer. Use only current training performance. A public objective list does not authorize choosing curriculum by test returns. Match training and evaluation cost and seeds.
  Evidence locations: §3–4/curriculum; Appendix C.1; normalized p28,37,47,87–90

**2610.04596 · DiffGate: Difficulty-Gated Teacher Guidance for On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.04596)

- **post-training**: DiffGate bounds the teacher–student log ratio with 2tanh(delta/2) and modulates teacher guidance only on failed traces according to group success. It trains 0.6B/1.7B math and code students with a frozen 8B teacher.

**2610.04580 · Strong Helps Weak: Directional Cross-Modal Alignment Transfer in Multi-modal LLMs**

[Paper](https://arxiv.org/abs/2610.04580)

- **foundation-model**: DCAT is a cross-modal alignment and transfer candidate with a clear closed-form solution and public project code entry point.
  Reproduction scope: Not arbitrary cross-architecture merging or universal multimodal benefit. Alignment is a theoretical proxy, not measured mutual information. Charge per-group data recollection and FP64 solves; freeze η/β on independent validation, and do not select donors from test gains.
  Evidence locations: §4 Eq5–11; §5; App C.3–C.5/D/F; official project page

**2610.04575 · From Probe Scores to Alarm Policies: Operational Validity of Activation Monitors for Language-Model Agents**

[Paper](https://arxiv.org/abs/2610.04575)

- **agent**: Aggregate any-alarm maxima by semantic task/case with strict fit/calibration/test isolation. Use a Beta upper bound on independent negative-unit order statistics to select the largest certifiable rank and alarm only on strict exceedance; abstain if unsupported. Compare observable, activation, and joint detectors at the same horizon. Hash-bind model, threshold, and single-use test; a fail-closed claim compiler prevents promotion of AUROC into deployment guarantees.
  Reproduction scope: This is an evaluation/calibration contract, not a new detector or theorem. Public artifacts permit score-level replay only, not regenerated traces or activations or end-to-end training. ST-Web's 23 negatives are below 59/29, so zero alarms are mechanical abstention. AgentDojo's 38 positives fall short of 40, and test FPR of 18.67% at a 10% budget shows shift. Qwen14B is not compute-matched, and human review, blocking, and intervention gains were not measured. Certification assumes IID negative units, not adaptive-attack or familywise guarantees.
  Evidence locations: §3 pp.3–4 Eq4–6、§4 pp.5–6 Fig2/Table4、§5、§6.3 p.8

**2610.04555 · $\mathrm{TRIZ}^{a}$: Guiding Agent Evolution from Pattern Recognition to Solution Invention**

[Paper](https://arxiv.org/abs/2610.04555)

- **agent**: TRIZ-a freezes contradictions and comparison protocols, declares contracts for 40 typed mutation categories, executes candidates, and selects by useful/harmful functional information against a fixed reference population. Three public cybersecurity datasets support verification.
  Reproduction scope: FI depends on the predefined population and budget and does not guarantee monotonic evolution. Match hashes, splits, and preprocessing. V17/V18 are not formal V2 evidence. High-risk security actions still require human authorization.
  Evidence locations: TRIZ typed mutation/functional information; Eq/Appendix B; normalized p14–21,38–39,81

**2610.04518 · Length Generalization Needs Proper Regularization**

[Paper](https://arxiv.org/abs/2610.04518)

- **foundation-model**: VPAD computes affine dropout preserving mean and variance for each token's uncentered activation, with a shared mask after RMSNorm. Public training, evaluation, and weights make it a candidate length-generalization training operator.
  Reproduction scope: Variance matches coordinatewise, with residual projection covariance, not exact distribution preservation. Fig. 1 selects the best seed on RULER 4–8k; Fig. 4 reports three seeds. SmolLMBase's additional 100B training is not a same-data causal comparison. Independent projection masks are an extra official option outside the paper path. The 8k version also changes attention scaling, which needs a separate ablation.
  Evidence locations: §4.2–4.4 Eq12–13；§5.1–5.5；App C.1/C.2；official README

**2610.04517 · EvoCast: Reliable Autonomous Research Agents for Iterative Forecasting Architecture Evolution**

[Paper](https://arxiv.org/abs/2610.04517)

- **agent**: EvoCast separates LLM hypotheses and source edits from deterministic evaluation and promotion authority. Start with baseline and executable ablations, then apply bounded structural program mutations each round. Public TFB forecasting tasks support real experiments.
  Reproduction scope: Change only the model boundary, not evaluation paths. Fit training statistics without validation/test. Select final models on validation. Paper outcomes concern specific forecasting tasks, not general scientific ability.
  Evidence locations: EvoCast Algorithm1; normalized p28–39,53–59

**2610.04512 · Correctness Is a Direction: Geometric Answer Selection in Language Models**

[Paper](https://arxiv.org/abs/2610.04512)

- **foundation-model**: Geometric Answer Selection uses 50 labeled calibration questions to form a direction from correct-minus-incorrect mean normalized hidden states. One forward per candidate projects to select an answer, making it a frozen-model readout candidate.
  Reproduction scope: Use nonzero examples and 20% validation for layer selection. Isolate TQA calibration from testing. Fixed candidates do not directly extend to free generation, and directions do not transfer universally across tasks. Paired comparisons should not copy an independent two-proportion z-test. Author code was not found.
  Evidence locations: §3.1 Eq1–4；§5.1/Table4；§6.3；Limitations

**2610.04506 · EgoExo-Next:Benchmarking Vision-Language Models on Visual-Option Next-State and Cross-View Reasoning**

[Paper](https://arxiv.org/abs/2610.04506)

- **foundation-model**: EgoExo-Next provides 2,503 visual four-choice questions and four ego/exo present-matching or future-state tasks. Later distractors discourage choosing the farthest future. Candidate-only, shuffled-sequence, mismatch, and CLIP/DINO controls support diagnostic value. Official HF provides input images, input_meta, separate answers, and loading rules; give the model only images and input metadata, not gold or time. Paper §4.1 averages both directions, but the HF example describes requiring both directions correct: freeze and report the scoring version. Images retain six source licenses, and annotations are noncommercial research only, not uniformly open for commercial use.
  Evidence locations: §3.1–3.2; §4.1–4.3/Table2–3; official HF Data format/Loading/Licensing; dataset card Subtasks/Repository structure/Data format/Loading/Licensing (visited). Distinguish directional aggregation in the paper and card.

**2610.04488 · Can LLM Agents Automate Reinforcement Learning for Text-to-Speech?**

[Paper](https://arxiv.org/abs/2610.04488)

- **agent**: A TTS agent searches LM-carrier DPO and flow-carrier GRPO on CosyVoice2 and combines complementary policies. Fixed 5,000-condition AISHELL3/LibriTTS and Seed-TTS-Eval support real training and external outcomes.
  Reproduction scope: The paper reports test leakage through a channel not read by the contract, an unprotected pivot proxy, and reward inflation. Do not reuse contaminated iterations as formal gains. Merge scale is manually chosen; retain an independent final test.
  Evidence locations: RL design space/data-proxy-algorithm; §4.2–4.3; Tables1–3

**2610.04432 · Video2World: Benchmarking Coding Agents for Interactive World Modeling from Embodied Videos**

[Paper](https://arxiv.org/abs/2610.04432)

- **agent**: Video2World frames interactive simulation reconstruction from video as a coding-agent task, with separate executability, geometry, dynamics, and functional oracles. Public data and scoring for 222 instances make it a multimodal-agent candidate.
  Reproduction scope: 189 videos and 39 task families; 180 minutes per build without a common token budget, comparing systems rather than bare models. Only the verifier sees gt_pkg/hidden. Do not fake dynamics by writing state directly. HAR has source annotations and is not a fair agent arm. Three simulator dependency sets and GPU/Vulkan require native verification; reading HAR logs is not integration.
  Evidence locations: §3.2–3.3；§4.1；official README Data/Usage

**2610.04429 · Asking Earns Nothing: Scoring the Decision to Act in BFCL Multi-Turn**

[Paper](https://arxiv.org/abs/2610.04429)

- **agent**: Pair BFCL base with miss_func/miss_param and mechanically locate one empty-gold anchor. Identify world-changing attempts rather than lookups from structured rollouts, scoring balanced accuracy of acting under complete information and holding under missing information. Filter bad keys, multiple anchors, and mismatches, then human-certify 223 pairs. Report strict and separate authorization-step credit separately.
  Reproduction scope: Never expose gold to actors; use it offline only for localization/scoring. This is neither task completion nor general safety; uninformative baseline is 50%. Rejected action attempts and hallucinated missing functions count as act; prose is not a call. Keep 134 read-only pairs out to avoid perfect always-hold scores; explicitly record 31 bad keys and eight construction errors. Gemma's default system prompt versus native tool models is not a clean capability comparison. LLM judgment of response content is diagnostic only.
  Evidence locations: §3、§4.1–4.3 Eq1、§5.3–5.4、AppendixC–F

**2610.04409 · Understanding and Mitigating Hallucination Escape in Tool-Using LLM Agents**

[Paper](https://arxiv.org/abs/2610.04409)

- **agent**: EscapeGuard learns a conflict probe from frozen LLM states, then applies conflict-strength attention bias to current tool name, description, and schema tokens during selection/argument phases. BFCL, Seal, and Glaive supply public evaluation sources.
  Reproduction scope: Actual attention intervention is defining, not keyword heuristics. Separate probe training and threshold validation. The paper promises code/data after publication. Attack or conflict gold must not select interventions.
  Evidence locations: EscapeGuard §5.1–5.3; normalized p39–49; Appendix A–H

**2610.04381 · Beyond Plausibility: Verifiable Fine-Grained Image Editing on Structured Assets**

[Paper](https://arxiv.org/abs/2610.04381)

- **foundation-model**: VeriEdit-Bench renders exact targets and protected areas from editable SVG, chart, and HTML sources. Lab distance decomposes fidelity, preservation, localization, and magnitude with per-example harmonic scores, adding executable image-editing evaluation.
  Reproduction scope: Editors see only the image and instructions; targets and masks are verifier-only. Report equal-weight results over 22 cells and per-item means separately for 1,740 examples. No-op should yield 0/100/0/0. Render-noise gating and one-pixel dilation are protocol choices, not general aesthetics.
  Evidence locations: §3.1–3.2 Eq1–5；§4/Table1；Appendix B.1/B.2

**2610.04379 · AgentPersonaBench: Benchmarking Persona-Driven User Simulation**

[Paper](https://arxiv.org/abs/2610.04379)

- **agent**: AgentPersonaBench tests whether persona constraints affect behavior on 2,460 survey/chat/web/app tasks, with automatic leakage checks, independent human review, and separate deterministic and LLM criteria.
  Reproduction scope: This measures controllability of specified traits, not real population distributions or individual prediction. Main results are single-run, with three repeats for some arms. Judges remain beyond the 78.5% deterministic criteria; web/app need actual environments. Assign affiliations by first author, not Meta/OpenAI funding.
  Evidence locations: §3.2–3.3；§4；Appendix E/F；official repository

**2610.04375 · Do Tool Calls Execute as Intended? Measuring and Repairing Intent-Execution Correspondence in LLM Agents**

[Paper](https://arxiv.org/abs/2610.04375)

- **agent**: IEC uses each receiving parser to locate the first intent-to-execution mutation hop and verifies it by replaying a single-hop repair. IntAct generates unmodified transport forms for the relevant wrapper/process boundary or refuses. Public synthetic payloads and CLI paths support verification.
  Reproduction scope: Do not fabricate the private historical shell corpus. Observe witnesses without rerunning dangerous commands; isolate and authorize repair experiments. Exit 0/stdout do not prove argument equality. Test Windows and Linux boundaries separately.
  Evidence locations: IEC/IntAct Algorithm1/Table1; §experiments; normalized p15,30,45,66–67

**2610.04371 · Functionally Equivalent or Not? Graph-Grounded Differential Surrogate Execution for Code Equivalence**

[Paper](https://arxiv.org/abs/2610.04371)

- **agent**: FEAgent proposes executable counterexamples from repository graph obligations and blinded two-program surrogate traces, then returns Equivalent/Inequivalent/Unclear by deterministic reconciliation. EquiBench and SWE-bench Verified support secondary audits.
  Reproduction scope: Not formal proof. Directly execute every reported divergence to confirm it. Extra behavior must be judged against issue requirements. Freeze input domain, environment, and observables before viewing counterexamples.
  Evidence locations: FEAgent five phases; §assessment/Eq1; normalized p20–29,67–79,111

**2610.04344 · Hierarchical Credit Assignment for RLVR on Fused Gromov-Wasserstein Geometry**

[Paper](https://arxiv.org/abs/2610.04344)

- **post-training**: HarA computes separate FGW barycenters for correct and incorrect hidden-state position graphs, assigns different positive and negative credit powers by span contribution to those barycenters, and multiplies GRPO advantage. Real multi-model and multi-benchmark experiments do not justify replacing FGW with Euclidean token scores.

**2610.04328 · Bidirectional Preference Synthesis: Learning Prompt-Conditioned Preferences from Boundary Failures**

[Paper](https://arxiv.org/abs/2610.04328)

- **post-training**: BPS constructs offline preference data rather than a new loss. From partial failures, generate student corrections and safe, non-leaky achieved prompts. After cycle consistency, reverse the same response pair across two prompts as crossed anchors and apply standard DPO. IFBench and function-call tests cover mechanisms and downstream outcomes; same-teacher rankings are not independent generalization.
- **agent**: BPS treats a partially correct response as rejected for its original prompt and chosen for a prompt representing what it actually accomplished. Independent teacher cycle-consistency screening precedes standard DPO over forward and reverse pairs. Public instruction and tool benchmarks allow verification.
  Reproduction scope: This is a cross-topic post-training preference-data method, not a DPO loss change. Reverse prompts must not turn factual or math errors into correct responses. Gemini probes using the same teacher are not teacher-independent generalization. rho≈.195 comes from 282 validation passes.
  Evidence locations: BPS crossed-anchor construction; normalized p17–34,37–42,73–83

**2610.04318 · Rethinking Long-Video Efficiency: A Joint Allocation Perspective on Frames, Pixels, and Front-End Latency**

[Paper](https://arxiv.org/abs/2610.04318)

- **foundation-model**: LoHi splits one decoded frame pool into low-resolution video and a few high-resolution images with common token and front-end decoding budgets. SemDiv combines query relevance and DPP to choose high-resolution frames.
  Reproduction scope: Even with 5,760 visual tokens, decoded frame counts can differ; separate decode, encode, and prefill. Applies to modern dynamic-resolution VLMs, not established for older LLaVA. Entropy-threshold tuning on a 10% benchmark holdout is exploratory; freeze the split. Text cues link streams rather than a new trained cross-stream module. Official code was not found.
  Evidence locations: §4.1–4.4 Eq2–6；§5 setup；Appendix C.6/E

**2610.04303 · What to Preserve in Recursive Computation: A Local Predictive Sufficiency Principle**

[Paper](https://arxiv.org/abs/2610.04303)

- **foundation-model**: Local predictive sufficiency estimates compression deficits from finite ridge tests with full-covariance balancing and projects real optimizer proposals onto half-spaces defined by grouped predictive constraints. Language memory, TGN, VLA, and recurrent policies provide trainable mechanisms and controls.
  Reproduction scope: Population guarantees require independent samples and test coverage; the empirical surrogate is not a guarantee. TGN training epochs take 1.9–2.2×, parameters grow 10.1%, and inference varies ±3%. VLA holds out initializations, not broad OOD. SRI main-table selection of modified tasks requires reporting all six tasks too. Match total training compute in future capability tests.
  Evidence locations: §3.1–3.4/Algorithm2/Propositions2–3；§4/Table1–2；Limitations；Appendix E/Tables18–19

**2610.04299 · Questioning the Questions: Sustaining Self-Evolution in Reasoning Models**

[Paper](https://arxiv.org/abs/2610.04299)

- **post-training**: R-Quest uses validity initialization and pairwise novelty gating of samples to change questioner–solver co-evolution. Two real model-family experiments are reported. The paper selects checkpoints by highest test benchmark mean per domain; an independent validation split is needed rather than inheriting these numbers as unbiased formal outcomes.

**2610.04292 · LMBuild: Evaluating LLM Agents for Generating Buildable and Functional Structures**

[Paper](https://arxiv.org/abs/2610.04292)

- **agent**: LMBuild constructs 3D structures through interactive retrieval and generation of parts and evaluates structure, function, design, and physical realization separately. It is a multimodal coding-agent candidate.
  Reproduction scope: Experiments cover only 200 Core, not 2,549 Full. Three refinement rounds gave modest gains; explicit functional specifications are not discoveries from self-evolution. Physical feasibility is a proxy, not production or assembly. Retain per-item CAD licenses and do not portray medical device designs as usable products.
  Evidence locations: §2.2–2.3；§3.1/3.4；official repository

**2610.04261 · Playing social deduction games with reinforcement fine-tuned large language models**

[Paper](https://arxiv.org/abs/2610.04261)

- **post-training**: GRPO applies social reasoning and influence rewards with shared policies within sides. Standard group normalization, PPO clipping, and KL are not a new optimizer, so this belongs to agent environment research. The judgment applies only to the core post-training track. Agent methods and public data are independently assessed in the Agent track, not rejected globally.
- **agent**: Social reasoning RFT trains one shared policy per side in Werewolf/Avalon, prompting with private visible roles and public history. Hidden-role predictions and later voting influence supply rewards; final wins are an external outcome. Specified game engines support implementation.
  Reproduction scope: Hidden state is reward-only and must not reveal all gold roles to players. Fixed opponents do not show nonstationary multi-agent generalization. Influence rewards are not strictly causal persuasion. Blind model judging is not human interaction, which remains future work.
  Evidence locations: AgentEvolver Game Arena methods; normalized p110–133; social cognition RFT; Limitations

**2610.04225 · FlashGaze: Training-Free Multi-Scale Patch Pruning For Efficient Video Understanding**

[Paper](https://arxiv.org/abs/2610.04225)

- **foundation-model**: FlashGaze chooses Drop/Merge/Keep before vision encoding by motion-compensated error, using three-level quadtree dynamic programming under a pixel budget. Qwen3-VL/NVILA and public video benchmarks support verification.
  Reproduction scope: Keep the entire first frame and exempt it from budget. End-to-end TTFT must include preprocessing and vision encoding. H200 speed is not A100 evidence.
  Evidence locations: §3.1–3.3/Eq1–6/Algorithm1; §4.1; Appendix A/B

**2610.04204 · Clean: Second-order LLM Training at Linear Memory Cost via Nyström Sketching**

[Paper](https://arxiv.org/abs/2610.04204)

- **foundation-model**: Clean/Q-Clean reduces optimizer state through two-sided thin Nyström factors and four complementary block moments. Clear definitions and measured LLM pretraining make it an optimizer candidate.
  Reproduction scope: Linearity concerns state at fixed r, not parameter, gradient, or activation size, and need not hold when r grows with d. Fitting 13B in memory is not full 13B capability training. Freeze best-validation and shortened-sweep selection; no training-seed CI is reported. QClean 12.10 does not beat every baseline.
  Evidence locations: §3 Eq6–16/Alg1；§4；§6 Table3/Fig5；AppA/B/D

**2610.04196 · Asynchronous Is Nearly Free for Evolution Strategies on Long-Horizon Agentic Tasks**

[Paper](https://arxiv.org/abs/2610.04196)

- **agent**: AsyncES records parameter versions to track rollout lag, accepts bounded-staleness returns, standardizes rewards in the accepted cohort, and updates central ES parameters. Workers restore unperturbed weights and replay updates before perturbing again.
  Reproduction scope: Qwen2.5-7B/ALFWorld uses 2,083 train, 100 validation, and 300 test tasks. Three evaluation seeds share one checkpoint, not three training seeds. Asynchronous lag=1 is close to synchronous; lag=4/8 degrades. ES uses roughly 3.99× GRPO FLOPs; wall time alone is insufficient. Real perturbations, discard decisions, and version logs are required, not fixture rewards.
  Evidence locations: §2–5、Appendix A/B

**2610.04178 · SHarP: Saliency-based Pruning of Agent Harnesses**

[Paper](https://arxiv.org/abs/2610.04178)

- **agent**: SHarP disables hand-defined harness modules individually, estimates saliency from relative median dev score/cost and paired t-tests, protects modules with significant performance contributions, prunes by efficiency, and evaluates independently.
  Reproduction scope: Four public task sets and three held-out runs per task. Define module boundaries and coupling first and select only on dev. A p-value is neither causal importance nor effect size. Actually disable tools, instructions, or modules and match budgets. Distinguish mean in the cost formula from median in plots.
  Evidence locations: §3–4、saliency definition and pruning procedure

**2610.04152 · Kepler4D: Controllable Future Video Generation via 4D Scene State Evolution**

[Paper](https://arxiv.org/abs/2610.04152)

- **foundation-model**: Kepler4D uses DA3, SAM2, and a VLM to obtain object proxies. Chain-of-Motion produces structured movement and renders 3D control for VerseCrafter. DL3DV/DAVIS support conditioned continuation experiments.
  Reproduction scope: Evaluation conditions on future camera trajectories estimated from the full video. Do not claim unconditional prediction or include future frames in initial state. Dynamic Degree is not motion accuracy.
  Evidence locations: §3.1–3.4; §4; Appendix B

**2610.04140 · ExpertMuon-Compass: Alignment-Guided Step Sizes for Mixture-of-Experts Training**

[Paper](https://arxiv.org/abs/2610.04140)

- **foundation-model**: ExpertMuon-Compass preserves Muon matrix directions and changes expert step radii with family- and row-alignment scalars. Separate tuning seeds and paired evaluations define a training-operator candidate.
  Reproduction scope: Adds 4–7% wall time. The 8.2M-token run is clearly undertrained; 262M/1.05B are near NorMuon, with the strongest result under changed data ordering. Separate N/H from N/N to avoid crediting momentum changes to Compass. FP32 does not directly extrapolate to BF16 or larger MoEs.
  Evidence locations: §3.1–3.4 Eq1–8；§4.1–4.4 Tables1–4；§5；AppA/C

**2610.04139 · From Sight to Foresight: Predictive Spatial Reasoning in Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.04139)

- **foundation-model**: SpatialMind aligns vision tokens with bounded log-depth correction plus metric and motion encodings, training state chains and answers in GROUND/CURRENT/DYNAMICS/FUTURE stages. External VSI/OSI/VLM4D allow transfer checks.
  Reproduction scope: Verify actual release of the in-house 30,677 training QA and 2,000 benchmark items. Future states are only training targets and offline grading data; inference uses observed prefixes.
  Evidence locations: §3; §4/Eq4–6; §5.1–5.3; Appendix A–C

**2610.04134 · Agentic Resource Allocation for Batch Multi-Objective Bayesian Optimization in Autonomous Materials Discovery**

[Paper](https://arxiv.org/abs/2610.04134)

- **agent**: MultiTaskGP allocates each experiment batch among six qEHVI/diversified qUCB mixes. An LLM chooses an option from recent HV/MI, history, and budget events; Adaptive also selects β.
  Reproduction scope: Twenty-five paired seeds, but ground truth is a random forest fit to data, not material experiments. The exhaustive oracle space for the HV reference is offline only. Budget changes are announced one round ahead, the space is discrete, and q=5 per group. Do not claim causal gains in real discovery.
  Evidence locations: §2.2–2.6、optimization campaigns、Data availability

**2610.04132 · PB-GRPO: Learning Socially Adaptive LLM Agents from Persona-Driven Simulation with Preference-Batched GRPO**

[Paper](https://arxiv.org/abs/2610.04132)

- **post-training**: PB-GRPO preserves prompt-local means but pools variance within latent preference buckets for the denominator. Actual Qwen7B experiments use 128 training and 100 unseen personas; this preliminary single-setting evidence warrants caution.
- **agent**: PB-GRPO preserves prompt-local means but pools variance within latent preference buckets for the denominator. Actual Qwen7B experiments use 128 training and 100 unseen personas; this preliminary single-setting evidence warrants caution.
  Reproduction scope: This entry reuses the full-text review rather than a separate reread. Public artifact executability was not rechecked here. Acceptance means research candidate, not completed implementation.
  Evidence locations: §3 formulas; §4/Table1

**2610.04118 · LongSocialBench: Do Long-Context LLMs Understand Online Discussion Threads?**

[Paper](https://arxiv.org/abs/2610.04118)

- **foundation-model**: LongSocialBench releases 1,462 questions over 94 full discussions with an exact MCQ protocol, covering structured long-context social reasoning. Admit only gold-free inference evaluation; report oracle conditions separately as diagnostics.
  Reproduction scope: The paper measures accuracy on parsed responses; also report coverage and invalid outcomes over the full denominator. Gold-Scope and criterion-label conditions contain gold and must not optimize Evolve capability. Public data are test-only; freeze an episode-level holdout. Pin the actual revision despite different old Tracyyyy1997 README and xinyiliu-research page names. No full author runner was found.
  Evidence locations: §3; §4; §5.5–5.6; App D.2/I; official HF README

**2610.04047 · Periscope: Extending Frozen Language Models Beyond Their Context Window**

[Paper](https://arxiv.org/abs/2610.04047)

- **foundation-model**: Periscope defines local/cross-span probing and evidence graphs for frozen models, making it a long-context reasoning and retrieval operator candidate.
  Reproduction scope: Each token is read twice, so 9k is not total processed length. W²/c bounds length, not accuracy. Single-probe KV differs from batch-resident memory. Charge all probes and embedding/readback models. Finite-choice single-token readout is limiting, multi-document performance is weak, and top-20 missing-option fallback needs unit tests.
  Evidence locations: §3; §4.2–4.3 Tables1–4; §5–6; App A.1/A.2; authors' README

**2610.04009 · SUAVE: Unified Video-Action Models via Masked Diffusion**

[Paper](https://arxiv.org/abs/2610.04009)

- **foundation-model**: SUAVE unifies discrete video and actions under masked diffusion as a new trainable model candidate.
  Reproduction scope: No language generation or semantic-generalization test. Co-training and pretraining-only effects are not separated; single-seed bootstrap measures rollout uncertainty only. A real 1.03-second chunk of five actions is not 5 Hz closed-loop control; reported speed is 2.5 actions/s. Tokenizer limits FVD. No separate author code repository was located.
  Evidence locations: §III-A–D；§IV-A–C；§V Limitations

**2610.04008 · SkillScriptBench: Benchmarking Self-Evolution of Executable Agent Skill Packages Beyond Markdown**

[Paper](https://arxiv.org/abs/2610.04008)

- **agent**: SkillScriptBench checks consistency between SKILL.md and scripts. AST-guided revision binds each requirement to one syntax node, edits locally, and explicitly preserves correct behavior, making it an executable skill/RSI candidate.
  Reproduction scope: Separate 300 faulty and 50 clean tasks among 350. Pass@3 is not three successes. Keep surrogate verification independent of hidden official tests. Failed unique matching against the original or initial repair must fail closed, not overwrite user code uncontrolled. Verify public author dataset availability.
  Evidence locations: §2.1–2.4；§3.1–3.4；§4.1；Appendix A/D

**2610.04002 · Do Language Models Need a Trainable Input Embedding Table? Fixed Minimal Token Codes at 1.7B-Class Scale**

[Paper](https://arxiv.org/abs/2610.04002)

- **foundation-model**: Fixed minimal binary token identities plus deterministic lifting can form an executable architecture/mechanism diagnostic, with public checkpoints. Do not present it as a quality or efficiency winner.
  Reproduction scope: No trainable input table does not mean lookup-free or no embedding function. Parameter count, geometry, and input scale change together. One run, resume without sampler cursor restoration, and unmatched FLOPs. No measured system gains; MMLU/CSQA are near chance.
  Evidence locations: §3.2–3.5；§4.1–4.4；§5/Table2；§8/AppE

**2610.03994 · Solving VeriContest with a Lean-Backed Rust Verifier**

[Paper](https://arxiv.org/abs/2610.03994)

- **agent**: Rust-Prover converts Verus specs to Rust specifications and then Lean via Charon/Aeneas. A proof agent iterates with immutable code/theorems; clean clones recheck byte identity and Lean axioms.
  Reproduction scope: The fixed public benchmark has 1,007 problems and 1,325 theorems. Not all 349 specs are tested and translation has only partial differential coverage, placing the translator in the trust boundary. Ban sorry/admit/native_decide/bv_decide. Public Verus proofs can provide prior information, so unseen Lean proofs do not guarantee no indirect contamination. A proof string is not Lean-kernel success.
  Evidence locations: §3.1–3.4、§4、§4.5

**2610.03984 · Teaching Agents to Code Reliably**

[Paper](https://arxiv.org/abs/2610.03984)

- **post-training**: Weighted coverage Shapley assigns credit to test assertions on mutation and sibling patches, gates positive trajectory advantage, and injects credit into assertion tokens. Gold tests are scorer-only. All 500 examples were first diagnosed, then split into 230 training and 270 holdout; do not claim the holdout was wholly unseen.
- **agent**: Weighted coverage Shapley assigns credit to test assertions on mutation and sibling patches, gates positive trajectory advantage, and injects credit into assertion tokens. Gold tests are scorer-only. All 500 examples were first diagnosed, then split into 230 training and 270 holdout; do not claim the holdout was wholly unseen.
  Reproduction scope: This entry reuses the full-text review rather than a separate reread. Public artifact executability was not rechecked here. Acceptance means research candidate, not completed implementation.
  Evidence locations: §2.3 Eq.2–5；§3

**2610.03938 · MLLMs Fail to Refuse when Using Tools Agentically**

[Paper](https://arxiv.org/abs/2610.03938)

- **agent**: Pair the same MLLM in no-tool and ReAct conditions with four vision tools to measure refusal failure. Use tool counts to diagnose context dilution and reinject the original request each turn to test mitigation.
  Reproduction scope: Three public visual-safety sets and 11 models. RFR is a GPT-5.2-judged refusal proxy, not real harm. Tool-count correlation alone is not causal. Gemini's native tools cannot be controlled and are reported separately. Run real image/OCR/tagging/cropping tools; reinjection is not complete protection.
  Evidence locations: §3.1–3.2、§4.1–4.3、§5、Appendix A–D

**2610.03894 · Proxy Confidence: Auditing Black-Box LLM Agents with a Surrogate's Log-Probabilities**

[Paper](https://arxiv.org/abs/2610.03894)

- **agent**: ProxyConfidence uses an independent open surrogate's teacher-forced or PMI and YES/NO/tool-competition log probabilities to score black-box actions, calibrates score direction by regime, and uses combined scores for audit and correction selection.
  Reproduction scope: BFCL, xLAM, and AppWorld cover decidable tool tasks, not external facts unknowable from context. Teacher-forcing signs can reverse; determine orientation only on validation, not across regimes. Actor de-identification affects replication, and ≤8B scorers and multitenant latency are untested.
  Evidence locations: §3–7、§9、readout definitions

**2610.03820 · From Requirements to Attack Trees: Grounded LLM Agents for Design-Time Security Review**

[Paper](https://arxiv.org/abs/2610.03820)

- **agent**: Extract an entity graph with trust boundaries from requirements and architecture diagrams, assign attack-tree workers by goal, and rebuild only affected branches after joint validation. Preserve stable IDs with at most three attempts. Public Microsoft IoT Edge threat models can serve as reference tasks.
  Reproduction scope: Do not pool the 12 synthetic threats each in OLB/EHS with open-case coverage. The open case has no complete gold and one expert provides no interrater evidence. Repeated calls at the same seed are not independent training seeds. Proposed architecture is not implemented safety; PRDs/diagrams are trusted inputs, and prompt-injection defense is untested. No author repository URL was located.
  Evidence locations: §3.2.1–3.2.6 grounding / attack-tree / validation；§4–6 evaluation

**2610.03796 · ProsaBuddy: Assisting Mechanized Real-Time Schedulability Analysis with LLM-based Agents**

[Paper](https://arxiv.org/abs/2610.03796)

- **agent**: ProsaBuddy's primary path decomposes lemmas in two stages with domain guidelines/skills and isolated subagents. Separate OS processes audit Rocq ASTs: proof bodies permit only ProofStep/Query; outside them only trusted imports; libraries are read-only and theorems/axioms immutable. Seventeen lemmas succeed, versus 12 without skills, 14 without decomposition, and 15 without paper hints. Headline results include human proof hints and must be reported as assisted. The audit TCB beyond the kernel is not formally verified, and weak models omit difficult tasks rather than running a full matrix.
  Evidence locations: §III-B–E；§IV-A–C；§V

**2610.03780 · OceanMind: A multi-agent AI system for ocean diagnosis**

[Paper](https://arxiv.org/abs/2610.03780)

- **agent**: OceanMind's six roles route queries, plan skills, orchestrate tools deterministically, and synthesize ocean evidence. A constrained CodingAgent fills missing tools. Artifact references and role-specific memory transfer data.
  Reproduction scope: CMEMS is public but some in-situ CTD data require applications. Quantitative diagnostics are not general agent gains, and gold chains are scoring-only. Report first-pass, four-gate passing, and step efficiency separately; the efficiency score penalizes too few and too many steps. Single web responses and default sampling do not establish statistical advantage.
  Evidence locations: Methods: agent architecture、benchmark; Data/Code availability

**2610.03741 · Logit-Aware MIMO AirComp for Distributed Mixture-of-Experts LLM Inference over Wireless Edge Networks**

[Paper](https://arxiv.org/abs/2610.03741)

- **foundation-model**: Finite differences estimate MoE aggregation sensitivity to next-token logits, guiding power-constrained MIMO AirComp transceiver weighting. This enables mechanism diagnostics under wireless noise.
  Reproduction scope: Distinguish wireless simulation, Gaussian hidden-state replay, and 295-example closed-loop ARC. A 500-example GSM8K replay is not real wireless deployment. Account for extra forwards, CSI, and sensitivity refresh; more SNR/channel seeds and full benchmarks remain absent.
  Evidence locations: §III-A–C Eq17/34/35 Algorithm1；§IV-A/C/E

**2610.03695 · Language Models that Play Chess and Explain Their Moves**

[Paper](https://arxiv.org/abs/2610.03695)

- **foundation-model**: Queen connects a frozen Leela position encoder to SmolLM3, runs a four-stage spatial/temporal curriculum, then seven rounds of self-evolving SFT on Stockfish-verified recursive subposition explanations. Lichess, public engines, and held-out puzzles support checks.
  Reproduction scope: Stockfish is an explicit training/validation oracle, not teacher-free RSI. Language judges cannot replace legality or PV checks. Isolate root positions and test puzzles.
  Evidence locations: §3.1–3.3/Algorithm1; §4.1–4.3; Appendix A/B

**2610.03632 · World Embedding Benchmark**

[Paper](https://arxiv.org/abs/2610.03632)

- **foundation-model**: World Embedding Benchmark provides public physical video/text retrieval, regression, pair discrimination, and new-model evaluation interfaces, suitable as physical-understanding infrastructure.
  Reproduction scope: Transfer across parameters in one physics family is not OOD under new laws. JEPA regression and direct MLLM pair classification cannot be ranked across tasks. Contrastive adaptation helps retrieval but hurts regression. Freeze family/split manifests and do not tune Evolve repeatedly on public test.
  Evidence locations: §2.1–2.2; §3.1–3.3; official README Evaluation

**2610.03631 · NeutronGym: Physics-Graded Neutron Instrument Design for LLM Agents**

[Paper](https://arxiv.org/abs/2610.03631)

- **agent**: NeutronGym uses 22 MCP tools to manage real McStas instruments and cached compiled simulations. Four reward levels cover syntax, runtime, structure, and science. Programmatic families pass model-free rules and fixed-answer shortcut admission before GRPO.
  Reproduction scope: Actual McStas simulation is required, not LLM judges. Fixed-layout parameter tasks are not topology design. T3 is unscored, two hidden references are unreleased, and nine reward failures are disclosed. 11→77 is one family, second seed 69, and other families partly use one seed; this is not physical facility evidence.
  Evidence locations: §3、§4–5、§6、Appendix B/G

**2610.03591 · HazardWeaver: Scientific Route Selection for Hazard Analysis Agents**

[Paper](https://arxiv.org/abs/2610.03591)

- **agent**: HazardWeaver compiles literature into Satisfied/Violated/Unresolved scientific conditions, finds executable routes with a typed capability graph, and lets an LLM select or repair within their intersection. Independent scoring checks hidden routes, time cutoff, provenance, and budget.
  Reproduction scope: 141 sealed tasks over 11 tracks require real model/solver artifacts. Not finding a route is not proving none exists. Separate DCA and native scientific errors rather than pooling unlike numbers. Hide gold routes and post-cutoff evidence. Domain registry coverage determines verifiability.
  Evidence locations: §3.1–3.4 Eq2–8、§4、Appendix A/C/E

**2610.03585 · Threat-Preserving Representation Sensitivity in Agent-Security Benchmarks**

[Paper](https://arxiv.org/abs/2610.03585)

- **agent**: TPRS freezes task, harm objective, policy, scorer, and environment and changes only tool representation, measuring ASR and benign utility separately on ASB, MCPTox, and AgentDojo.
  Reproduction scope: 28,904 runs. ASB A2 changes the task and is diagnostic; some renamings are not semantically equivalent and cannot isolate threat words. MCPTox form-matched neutral controls explain most variation. Compare per benchmark and distinguish invocation from committed success.
  Evidence locations: §III methodology、Tables I–III、limitations

**2610.03574 · HyperBrowseComp: A Multilingual and Multimodal Stress Test for Web-Browsing Agents**

[Paper](https://arxiv.org/abs/2610.03574)

- **agent**: HyperBrowseComp uses 423 human-written multilingual and multimodal short-answer evidence chains, filtering easy questions with a no-internet condition. Use a common 25-step ReAct limit across provider-native, Exa, and OWL conditions, recording actual web traces and short-answer judgments.
  Reproduction scope: Thirteen-language stress tests do not reflect natural query distribution; live web results vary over time and geography. OWL uses a distinct harness, so differences are not model-only. Keep 2,400-second failures in denominators. Decode the intentionally encoded dataset, but hide gold and solution traces from actors. Small same-model judge sensitivity does not mean no bias.
  Evidence locations: §3.1–3.2、§4.1–4.4、Appendix B、Limitations

**2610.03524 · From Benchmarks to Production: A Text-to-SQL System for Complex Financial Data**

[Paper](https://arxiv.org/abs/2610.03524)

- **agent**: FLINT lookup resolves opaque IDs from reference tables, retrieves structured query-bank examples, links foreign-key schemas, generates SQL, and reflects on execution errors, with multistep parallelism.
  Reproduction scope: Core financial data are private, but Appendix G specifies paths for four public domains. Keep the query bank disjoint from evaluation and report manual rule cost. Executable SQL is not necessarily semantically correct; grade AST, output, and judge separately, with read-only SQL. Production deployment lacks quantitative A/B evidence and does not qualify as industrial search/ads/recs evidence.
  Evidence locations: §3.1–3.6、evaluation、Appendix G、Limitations

**2610.03516 · XGenAct: Geometry-Enhanced World Action Models through Cross-Task Generation**

[Paper](https://arxiv.org/abs/2610.03516)

- **foundation-model**: XGenAct combines a deterministic geometry codec with shared video-flow task mixtures as a world-and-action joint-training candidate.
  Reproduction scope: Geometry modalities use simulator labels during training; future GT cannot be used at deployment. Future perception is scored against simulator state after the policy's actual actions, with exclusions for deviations ≥10 mm reported as coverage. Best menus vary by task; do not select on test. Code and weights are promised, but no public repository was verified.
  Evidence locations: §3.1–3.4 Eq1–6；§4.1–4.4；App B/C/E/G/H；Reproducibility

**2610.03448 · Passing the Test You Trained On: Re-evaluating Prompt-Injection Detectors for LLM Agents**

[Paper](https://arxiv.org/abs/2610.03448)

- **agent**: Reevaluate 15 injection detectors using differential replay of clean and injected tool outputs. Measure TPR at default thresholds and low FPR, audit training overlap, and diagnose missing task context with a task-aware yes/no log-probability judge.
  Reproduction scope: A 1% FPR threshold selected on evaluation benign examples is an optimistic upper bound, not deployment calibration. Gold tool calls only construct fixed data, never enter evaluated actors. Synthetic YAML/JSON differs from real web, and fixed templates are not adaptive attacks. Deduplicate equal-weight InjecGuard/PIGuard.
  Evidence locations: §4.1–4.4、§5、§6、Appendix C

**2610.03389 · From Patching to Pruning Visual Computation in Vision Language Models**

[Paper](https://arxiv.org/abs/2610.03389)

- **foundation-model**: P2P tests replacing cached vision projection with means, scans prefix/suffix sensitivity for safe layers, and actually skips vision attention/MLP, optionally with patched-graph LoRA. Seven public benchmarks and separate proxy, validation, and test data support reproduction.
  Reproduction scope: Acceleration requires bypassing operators, not computing dense outputs and replacing them afterward. Preserve both consecutive failure boundaries and the 3% tolerance protocol.
  Evidence locations: §3; §4.1–4.5; §5.1; Appendix A.6

**2610.03315 · Lightweight, Rubric-Guided Trajectory Evaluation for Production AI Agents**

[Paper](https://arxiv.org/abs/2610.03315)

- **agent**: LiteTrajEval builds offline domain rule profiles, normalizes online traces with weak failure hints, compacts formats and repeated references, and chooses evidence by a tier waterfall budget and MMR before one rubric judge produces a diagnosis.
  Reproduction scope: Public Magentic-One and τ-retail traces. Build rules and budgets only on dev; human failure labels are grading-only. Character budget is not tokens. Hard truncation can lose evidence even when paths remain. Lower costs are not task gains; heuristic hints are not ground-truth causes.
  Evidence locations: §II.A–D、Eq1–3、Algorithm1、evaluation

**2610.03226 · D2K-Bench: Can LLM Agents Turn Expert Designs into Efficient GPU Kernels?**

[Paper](https://arxiv.org/abs/2610.03226)

- **agent**: D2K-Bench pairs 26 tasks and 85 workloads with and without expert L1–3 design guidance. Agents iteratively edit, compile, profile, and submit Triton. Require numeric/state-update correctness and implementation validity before selecting by geometric-mean speedup.
  Reproduction scope: Paper B200 measurements are not A100 performance; any local CUDA implementation needs an A100/A30 receipt. Hide expert source and hide timing from the source judge; guidance excludes tuning parameters. Workload feedback during generation is not held-out generalization. Separate objective score and LLM design rubric.
  Evidence locations: §2.1–2.3、§3.1–3.3、§4、Appendix evaluator

**2610.03213 · Toward SLM-based agentic task-tool intent matching**

[Paper](https://arxiv.org/abs/2610.03213)

- **agent**: Gemma task–tool relevance follows Base→GEPA→LoRA SFT→DrGRPO, with deterministic format, label, and length rewards and per-tool Boolean judgments.
  Reproduction scope: Split 12 MCP servers disjointly. Select by validation F1 and freeze test. Parse failures are end-to-end failures; report classification on parseable predictions separately. Tool-description synthesis and curator filtering do not establish real multi-tool execution. The 95% threshold is manual, not a safety guarantee.
  Evidence locations: §2.1–2.3、§3、§4

**2610.03199 · Predicting and Repairing Merge Collapse in Large Language Models**

[Paper](https://arxiv.org/abs/2610.03199)

- **foundation-model**: Prism norm-scales and averages task vectors, soft-thresholds by cross-expert variance, and applies cancellation/dispersion gates to avoid removing unique knowledge. The deterministic, data-free repair is fully specified.
  Reproduction scope: The 1.9e-3 threshold was tested only at the studied family sizes and is not architecture invariant. Restoration to base performance does not merge every ability; safety was not evaluated. Preserve explicit double coefficient scaling and norm-matched controls rather than treating this as standard averaging.
  Evidence locations: §3.1–3.3 Eq1–3；§4.1–4.3 Eq4–5；§5.1–5.5/Table4；§6

**2610.03198 · KV$^2$: A Self-Refining KV Cache**

[Paper](https://arxiv.org/abs/2610.03198)

- **foundation-model**: KV² uses KeyDiff averaged across layers and heads to choose sparse reconstruction queries per chunk, appending them after the full cache for actual causal forwards. Local maximum attention creates global retention; iterative proxy replacement is possible. It was already queued, so improved evidence is not a new paper count.
  Reproduction scope: Reconstruction-query positions follow context rather than original positions. Preserve global conditioning and local scoring. The author kvpress path masks instead of physically compacting, so it supports compression-stage runtime/memory, not decode-cache savings. Refinement may slow runtime, and full Evolve is not integrated.
  Evidence locations: §3 Eq1–4；§4.1；§5.1–5.4；Limitations

**2610.03190 · Not Until the Evidence Says So: Teaching LLM Investigators When to Close a Case**

[Paper](https://arxiv.org/abs/2610.03190)

- **post-training**: Nautil supplies evidence indexing and request tools, closed/open tasks, within-source balanced accuracy, and key-evidence removal controls. Official MIT code, data, and models are available. RLVR checkpoint selection used 22 of 64 test items, so isolate validation before treating any headline as leakage-free generalization.

**2610.03123 · Foresight: planning future perception in streaming VLMs without retraining**

[Paper](https://arxiv.org/abs/2610.03123)

- **foundation-model**: Foresight separates one frozen model into a video-writing Ingest and read-only-snapshot Think. It plans sampling rate, retained classes, compression, and response timing. StreamingBench and OVO support real causal streaming verification.
  Reproduction scope: The anonymous supplemental implementation and full harness have not been publicly verified. Read only the current video prefix and include asynchronous wall time. Keep 20% calibration separate from 80% holdout.
  Evidence locations: §3.1–3.2/Algorithm1; §4.1; Appendix H/Table10

**2610.03102 · Ask, Relax, or Act? Evaluating Actionable Indeterminacy in LLM Preference Reasoning**

[Paper](https://arxiv.org/abs/2610.03102)

- **agent**: Ask/Relax/Act uses intersection of accepted actions across admissible preferences and objectives to decide whether to act or ask, and finds the smallest allowed repair when infeasible. Exact solvers over four finite structures generate matched intervention pairs.
  Reproduction scope: 4,320 prompts in 36 cells use an exact checker, not an LLM judge. Hide gold completions and solutions. Single-source conditions do not solve multiple-source priority. Separate bare JSON/Markdown refusals from reasoning failures and FC from decision/IFC. Tools are optional and this does not show real-world decision effects.
  Evidence locations: §2.1–2.2、§3–5、Appendix M/O

**2610.03099 · Beyond Single Videos: Benchmarking and Active Evidence Seeking for E-Commerce Cross-Video Reasoning**

[Paper](https://arxiv.org/abs/2610.03099)

- **agent**: AdsCVR/AdSeek selects video frames and audio for turn-level evidence. GRPO uses correctness plus 0.1 format, filtering no-tool and zero-variance groups with up to three resamples. Teacher diagnoses missing evidence/reasoning, rectifies targeted issues, and applies assistant-masked SFT.
  Reproduction scope: Training gold may support reward/teacher, but test actors get metadata and actual perception only. Use original videos and real Qwen-VL/ASR tools; fixture text is not multimodal capability. Account for filtering on teacher success and append corrected data only in training. Separate 73.57 from mixed-source 74.30.
  Evidence locations: §3、§4.1–4.3、§5、Appendix B

**2610.03089 · Securing Computer-Use Agents Against Branch Steering Attacks**

[Paper](https://arxiv.org/abs/2610.03089)

- **agent**: COBRA preplans and commits a program from trusted inputs. BRH parses observations under fixed branch/field constraints, and HTTP/MCP proxies enforce operations, arguments, and approved schema hashes. Fusing five plans preserves legal alternatives.
  Reproduction scope: Malicious observations can choose allowed branches but cannot extend authority. Without an approved sitemap, domain allowlists are weak; non-HTTP GUI effects are outside scope. Run real browsers and proxies. Distinguish matched 86 OSWorld items from full MCP, and multiple-attempt from single-plan budgets.
  Evidence locations: §3–5、Appendix A/D/E/F

**2610.03084 · NegT2IBench: When Negation Changes the Picture. A Polarity Benchmark for Text-to-Image Models**

[Paper](https://arxiv.org/abs/2610.03084)

- **foundation-model**: NegT2IBench uses 4,800 positive and negative attribute/relation prompts in six types, checking object existence and grading with detector, SAM, depth, and SigLIP2. It adds executable negation evaluation for image generation.
  Reproduction scope: In the ambiguous dead zone, positive relations fail and negative ones pass by protocol, not logical truth. Separate image accuracy from prompt accuracy with any of four images. The 140 clear human-rated images informed threshold comparison; preserve independent evaluation. Equal weighting across six types is not universal vision ability.
  Evidence locations: §3.1；§4 human validation；§5；Appendix C.1/C.3/E.2

**2610.03063 · HARPO: Hallucination-Aware Reinforcement Learning for Faithful and Creative Language Generation**

[Paper](https://arxiv.org/abs/2610.03063)

- **post-training**: HARPO trains a hallucination-span reward model and activates writing rewards only when no hallucinations are predicted, with a cosine creativity-to-fidelity curriculum. This is hierarchical multiobjective reward, not new GRPO. The gate does not guarantee hallucination-free outputs.

**2610.03039 · HyperThink: Text-to-Parameter Hypernetworks for Efficient Reasoning**

[Paper](https://arxiv.org/abs/2610.03039)

- **foundation-model**: HyperThink generates frozen-LLM layer biases from queries under VQ constraints, a distinct algorithm candidate.
  Reproduction scope: Not zero overhead. Count query encoder, hypernetwork, and five samples; do not compare as single-sample. Training on two H200 and test on one H200 do not replace local A100 verification. Code is promised but not located. Freeze epoch/commitment details before integration and do not tune on MATH500 test.
  Evidence locations: §3；§4 Tables1–2/Fig4；App C；Reproducibility Statement

**2610.03036 · WebFovea: When the Model Is Right but the Click Is Wrong -- Reliable Round Trips for Vision-Based Web Agents on Live Websites**

[Paper](https://arxiv.org/abs/2610.03036)

- **foundation-model**: WebFovea hardens browser-agent harnesses and is reviewed in the Agent track.
- **agent**: WebFovea hardens visual action round trips through special-token parsing, coordinate mapping, actual select/fill readback, feedback state, five screenshots of history, a bounded DOM-text channel, and executor action budgets.
  Reproduction scope: Actual browser effects are required, not click fixtures. Claude Opus 4.6 only, 70 dev/30 holdout, and 25 scorable after 16 unreachable sites; do not silently remove denominators. Four official submissions going 31→57 are not randomized same-model A/B. Component samples range 1–24, and live web varies. CAPTCHA tools are out of scope.
  Evidence locations: §4.1–4.6、§5.1–5.5、§6.2、Appendix A

**2610.03034 · Adaptive Second-Order Solvers for Fast Stochastic Diffusion Sampling**

[Paper](https://arxiv.org/abs/2610.03034)

- **foundation-model**: The PI diffusion solver uses stochastic Heun first-/second-order error plus previous error for step size and aggregates adaptive traces into static modality-specific schedules. FFHQ/ImageNet64, LM1B, and public EDM checkpoints support verification.
  Reproduction scope: Retain rejected steps and stochastic handling. Compare mean NFE, not step count alone. LM PPL gains accompany lower entropy. Do not transfer schedules across modalities unconditionally.
  Evidence locations: §4/Algorithm1; §5; §6.1–6.4; Appendix B–D

**2610.03020 · DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users**

[Paper](https://arxiv.org/abs/2610.03020)

- **agent**: DyadMem separates Capture, Update, Recall, and full-pipeline evaluations. Six memory types include collaborative user–agent URAM, chronological deletion/addition/deduplication, and final valid-bank recall plus grounded QA.
  Reproduction scope: Standalone Update/Recall and GoldMemory QA are gold-conditioned diagnostics. Ability requires a model-built bank. Report no-change exclusions from update scores separately and retain empty/parse failures. Resolve conflicting QA 0/1 descriptions with formulas/code and freeze judge/matcher thresholds.
  Evidence locations: §3.1–3.3、§4、Appendix G

**2610.03014 · Beyond Predefined Sinks: Security-Aware Dependency Analysis for LLM Agents**

[Paper](https://arxiv.org/abs/2610.03014)

- **agent**: AgentSecGraph finds permissive sensitive-operation anchors, normalizes frameworks, and builds typed Security-ADGs. Python AST backward tracing identifies where constant overwrites break flows; JS uses lexical tracing. Preserve guard and trust-boundary provenance.
  Reproduction scope: may_guard is not safety proof and a matched sink is not a vulnerability. Local dependencies, aliasing, dynamic behavior, and TS types have limited coverage; some cases await disclosure. Freeze source snapshots and report precision, coverage, and attackability separately, without automatic vulnerability guarantees.
  Evidence locations: §3.1–3.4、§4、§5.3、Data availability

**2610.03002 · Recursive Self-Improvement in Unified Multimodal Models**

[Paper](https://arxiv.org/abs/2610.03002)

- **foundation-model**: Unified multimodal RSI uses execution-verified drawing programs as labels. Diagnostics only choose data distribution; separately update generation and comprehension experts and then merge, with equal-step and equal-verified-count controls.
  Reproduction scope: The new benchmark is still judged by same-family U0 and needs external audit. StructT2I 11.0→11.9 is small versus continued 11.7; BizGen roughly 4%. MMBench −2.6 and MMMU −3.0. Chart improvements are not general self-improvement.
  Evidence locations: §2.1–2.5 Eq1–4；§3；§4.1–4.5 Tables1–3

**2610.02986 · OLMo-Detect: A Multi-Stage, Confounder-Controlled Benchmark for Membership Inference on Large Language Models**

[Paper](https://arxiv.org/abs/2610.02986)

- **post-training**: OLMo-Detect audits membership across pre-, mid-, and post-training, matching members and nonmembers by quality, time, and vocabulary. It includes 15 unsupervised and three supervised MIAs, separated dev/test, and official data and scoring. This measures membership and contamination risk, not stronger reasoning.

**2610.02970 · A Guideline-Augmented Multi-Agent Framework for Schema-as-Code Biomedical Named Entity Recognition**

[Paper](https://arxiv.org/abs/2610.02970)

- **agent**: GAMA derives annotation rules from training gold and verifies support on training data. Top-N/type guideline memory produces ranked span/type plans and schema as code, with nested grounding/type/structure repair.
  Reproduction scope: Five public BioNER datasets; never use test gold for rules or repairs, and freeze N/attempts on validation. Valid structure is not correct NER. Compare exact span/type F1 under matched budgets. No new trainable parameters does not eliminate LLM call or induction costs.
  Evidence locations: §III.A–E、§IV experiments

**2610.02952 · GTDD: Generative Test-Driven Development for AI Coding Agents with Adversarial Testing**

[Paper](https://arxiv.org/abs/2610.02952)

- **agent**: GTDD commits candidates/configs before source-informed or blind testers generate valid inputs without expected outputs. A trusted reference checks differences, minimizes prefixes/operations, and permits up to k feedback rounds. Separate fresh audits from development tests.
  Reproduction scope: Fresh audits use conditionally independent random samples and restore protected materials. Population outcomes are hidden from coder and tester. Fresh-audit analysis of 600 historical candidates is an exact probability calculation, not live gate execution. Known-test success is not generalization. Do not mix joint-repository and simultaneous-family multiplicity or acceptance rules.
  Evidence locations: §3.1–3.3、§4、§5–6、Appendix B

**2610.02951 · Dynamic Expert Pruning for Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.02951)

- **foundation-model**: DEP is already queued. A request text encoder and MLP predict layerwise expert top-K, trained with impact-label BCE and soft-mask self-distillation KL. A CPU expert pool delta-loads GPU slots. Retain the candidate without double-counting.
  Reproduction scope: K≥router k and ties must respect exact budget; do not prune shared experts. Routing masks do not save memory without actual host residency and delta transfer. Train one predictor per retention level. Use only current prompt/context, not future agent output. Pruned results still trail dense, so compression is not free.
  Evidence locations: §3.1–3.4 Eq1–6；§4；Appendix H
- **agent**: DEP uses a small prompt/input encoder and MLP for per-layer top-K expert masks, jointly trained on REAP impact BCE and dense-to-soft-masked self-KL. Routing uses a −inf mask; delta-loading host tensors swaps only set differences.
  Reproduction scope: Keep calibration transcripts separate from evaluation. K≥router k with exactly K even at ties. Masking does not establish VRAM savings; measure actual buffers and transfers. Prefetch only known workflow topology. Accuracy still declines versus dense and each retention requires its own predictor. Validate CUDA on A100/A30.
  Evidence locations: §3.1–3.4、§4、Appendix H

**2610.02928 · Discriminating Fixture Coverage in Agent-Infrastructure Verification Suites**

[Paper](https://arxiv.org/abs/2610.02928)

- **agent**: Discriminating Fixture Coverage freezes projection-suite hashes, tests mutant kills, and instruments inactive versus activated-but-unobserved contamination. Add fixtures along seven predicted input dimensions and retest with an unchanged oracle.
  Reproduction scope: 5/10 on the challenge set is not natural fault detection. Repairing 10/10 on the same challenge is not a second holdout. Report optional-hook skips and distinguish first- from higher-order mutants. This audits software verifier coverage, not agent-task improvement.
  Evidence locations: §3–5、Table1、§6

**2610.02925 · Positive-Unlabeled Learning for Agent Safety False Alarm Auditing**

[Paper](https://arxiv.org/abs/2610.02925)

- **agent**: Safe-alarm PU ranking transfers TN via out-of-fold role boundaries and weakens false-alarm negative gradients by mass-constrained soft protection. Frozen references supply median ranks and reliability-gated distillation; hierarchical TN and cross-alarm constraints refine KL ranks.
  Reproduction scope: Target features can be used transductively, but safety labels are sealed. Forty TN and 510 target alarms are small. Soft mass is not global FP prevalence; the safety monitor is frozen. Top-budget ordering is for human review, not automatic dismissal. Reference agreement does not remove shared bias; all three stages need actual training rather than heuristics.
  Evidence locations: §3.1–3.3 Eq1–8、§4.1、Appendix A/B/C

**2610.02887 · Revealing Epistemic Uncertainty in MLLMs via Causal-Invariant Masking**

[Paper](https://arxiv.org/abs/2610.02887)

- **foundation-model**: CIM compares semantic distributions after masking while preserving question-relevant ROI and estimates uncertainty with EED expected embedding drift. VQAv2, OKVQA, AdVQA, POPE, and MME supply public data and equal-sampling controls.
  Reproduction scope: Causal invariance depends on ROI quality and is not proof of causal identification. Preserve mask generation, calibration, and AUROC rather than supplying only synthetic scores.
  Evidence locations: §3.2–3.4; §4.1–4.2; Appendix C.8/E

**2610.02885 · PsyEvo: A Personalized Counseling Agent That Self-Evolves at Test Time**

[Paper](https://arxiv.org/abs/2610.02885)

- **agent**: PsyEvo HBSP combines a fixed population skill prior with client Gaussian posterior sampling. SOCA selects responses using a two-order agreement DAG and mean-preserving ordinal delayed credit. Group-normalized weighted DPO updates shared LoRA across sessions.
  Reproduction scope: Online shared-cohort adaptation is test-time training, not frozen holdout. Client memory is private; adapters remain fixed inside a session and updates apply only to new sessions. External judging does not feed learning; separate internal feedback from reporting. Simulated counseling preference is not clinical efficacy, and small human studies do not establish treatment safety. Execute actual adapter-loss updates.
  Evidence locations: §2.1–2.4 Eq2–9、Algorithm1、§3、Appendix G/H/I

**2610.02880 · Found but Not Read: When Extracted Text Closes the Retrieval-Reading Gap in Document Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.02880)

- **foundation-model**: FoveDoc-Bench freezes ColQwen2 top-16 pages and compares image-only with image plus CPU OCR/PDF text for the same pages. Lexical top-16 chunks have 300 characters each. This separates retrieval and reading bottlenecks.
  Reproduction scope: PDF ground-truth text is an upper bound; gold evidence crops and recall are diagnostic only. FoveDoc gains 13–16 pp versus roughly 0.004 overall on MMLongBench, and charts can worsen. Keep 1,173 documents separate from training/validation QA and stratify by modality and recall.
  Evidence locations: §2 paired protocol；§4–6

**2610.02876 · Seeing, Saying, but Not Using: From Reportable Spatial Facts to Usable States in Multimodal Large Language Models**

[Paper](https://arxiv.org/abs/2610.02876)

- **foundation-model**: OSS normalizes shared spatial facts across contexts and uses ordinary autoregressive training on answer, state alignment, and state trajectory pools. Derivatives inherit observation-world splits; test three SpaceConflict types and paired scores.
  Reproduction scope: True-state injection is oracle-only. Training states must not come from validation or test worlds. The paper links a public repository, but this review did not reverify access.
  Evidence locations: §2.1–2.3; §4.1–4.3; §5.1–5.4; Appendix D.3/D.4

**2610.02856 · Adaptive Mutual Distillation for Balanced Multi-Task Post-Training of Large Language Models**

[Paper](https://arxiv.org/abs/2610.02856)

- **post-training**: AMD mutually distills MFT and smoothed-SFT branches. Three short global probes starting from the same state test increasing, decreasing, or preserving weights. Discard probe parameters and select direction per task on validation. Six benchmarks and several backbones were run; include probe costs.

**2610.02841 · How Robust Is Multimodal Claim Verification to LLM Rewriting?**

[Paper](https://arxiv.org/abs/2610.02841)

- **foundation-model**: SciClaimEval pairs claims with supporting and refuting images and measures verdict changes under natural paraphrases and single-word injections, for multimodal classification and reward-robustness diagnostics.
  Reproduction scope: 704 paired dev and 872 paired test examples. Ten reasoning samples produce support probabilities in steps of 0.1, not log-probability calibration. Paraphrases can change meaning, and CT numeric hedging needs review. One corpus and one main rewrite model do not establish general fact-checker improvement.
  Evidence locations: §3 rewrite strategies；§4.1–4.4；§7/Appendix B/H

**2610.02840 · PointWAM: 3D World Action Modeling for Dexterous Robotic Manipulation**

[Paper](https://arxiv.org/abs/2610.02840)

- **foundation-model**: PointWAM pretrains unified 3D scene and hand trajectories, then retargets actions, qualifying as a robotics foundation-model candidate.
  Reproduction scope: Three evaluation seeds are not three training seeds; RoboDojo has one. Count human-video CoTracker and VGGT-depth preprocessing costs and noise. Point detail and transparent objects fail. The project says code coming soon; none was released. Do not claim language generalization because DexJoCo uses fixed instructions per task.
  Evidence locations: §3.1–3.4 Eq1–7; §4.1–4.4; App B/C; official project page

**2610.02835 · All Work And No Play Makes Jack a Dull Boy: Understanding and Preventing Catastrophic Strategy Collapse in RLVR**

[Paper](https://arxiv.org/abs/2610.02835)

- **post-training**: MeshLearning explores with fixed offline coach-strategy prefixes containing no intermediate calculations or answers. Uniform KL balances growth in correct-trace policy log probability versus pre-RLVR reference. No coach at inference; actual math, science, and code training was run.

**2610.02832 · FastOPD: On-Policy Distillation for Lightweight VLA Deployment**

[Paper](https://arxiv.org/abs/2610.02832)

- **foundation-model**: FastOPD samples on-policy states via one student flow-map jump, matches diagonal teacher velocity, and propagates finite-step maps using midpoint self-consistency. LIBERO, RoboTwin, and real robots were evaluated; single-step action-expert training needs a genuine checkpoint.
  Evidence locations: Abstract (the full abstract in the input retrieval artifact was reviewed item by item); §3 Eq.3; §4.1–4.2
- **post-training**: FastOPD samples on-policy states via one student flow-map jump, matches diagonal teacher velocity, and propagates finite-step maps using midpoint self-consistency. LIBERO, RoboTwin, and real robots were evaluated; single-step action-expert training needs a genuine checkpoint.

**2610.02828 · FSPO: Policy-Consistent Risk and Pareto-Feasible Control for Budgeted LLM RL Post-Training**

[Paper](https://arxiv.org/abs/2610.02828)

- **post-training**: FSPO controls training actions using a policy-consistent risk-to-go ensemble, decision-conditioned calibration, and Pareto continuation certificates. Distinguish the 24-case ledger mechanism and real Qwen3B GRPO trainer study. Admit the mechanism, not fixed-ledger efficiency as LLM capability improvement.

**2610.02814 · VeriPy Source-Preserving Verification and Compatibility Checking for Python Components**

[Paper](https://arxiv.org/abs/2610.02814)

- **agent**: VeriPy retains executable Python ASTs and lowers specifications to Dafny or Lean with explicit admission/environment, proof sidecars and axiom gates, hash-bound guards, original body/model differential tests, and scoped compatibility.
  Reproduction scope: Define supported fragments, exact builtins, Unicode scalar semantics, and snapshot trust boundaries. basedpyright is not functional proof; generating guards does not prove anything. A prior ambientFalse sidecar flaw requires exact proposition and assumption audits. Historical compatibility currently uses Dafny, with different Lean coverage. Execute actual compiler/solver.
  Evidence locations: §3.1–3.3、§4、§7、Appendix G

**2610.02781 · OPD Before RL: Warm-Starting Rubric-Based RL with On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.02781)

- **post-training**: RP-OPD warms students with rubric-privileged teacher top-256 forward KL and then switches to rubric-reward GRPO across three rubric domains and multiple students. HealthBench reports overlapping and non-overlapping tests separately; formal reproduction needs fully isolated data.

**2610.02740 · Prospective Hindsight: Self-Calibrating Reinforcement Learning via Prediction-Reality Gaps**

[Paper](https://arxiv.org/abs/2610.02740)

- **agent**: PH uses shared-policy self-evaluation from only state/action, without privileged future. A ternary majority that disagrees with the actual outcome applies stop-gradient (1+alpha) to base RL, OPD, or Combined loss; unknown is neutral. OLMo3-7B uses a single-turn verifier and multi-turn PRM/user simulation with random equal-mass reweighting control. Calibration is explanatory rather than guaranteed; alpha=2 can collapse to predicting failure. Count extra M training forwards and keep test gold out of self-evaluation.
  Evidence locations: §3.1–3.4 Eq4–5；§4.1/4.3；AppendixC

**2610.02718 · Revisiting Visual Representation Enhancement of VLMs via Kernel Canonical Correlation Analysis**

[Paper](https://arxiv.org/abs/2610.02718)

- **foundation-model**: 3vKCCA trains three-view projections from CLIP vision, frozen DINO, and text, a vision alignment candidate with theoretical limits.
  Reproduction scope: Zero is a necessary KKT condition, not sufficient. Column normalization avoids all W=0 but does not solve original KCCA/eigenproblem. Preserve normalization and monitor rank/correlation. Two 5090 training GPUs are not A100 validation. A single table lacks seed variance and separate tuning details. No author code found.
  Evidence locations: §3 Eq1–3；§4 Table1；App A/C Eq18–21

**2610.02713 · WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds**

[Paper](https://arxiv.org/abs/2610.02713)

- **foundation-model**: WakeKV keeps a full CPU reservoir and per-head GPU LRU residency with reversible retrieval when demand changes, suitable for cache-migration experiments.
  Reproduction scope: Most cache-miss controls use full-attention oracle traces and are not online latency. Real FlexiCache/vLLM bridging covers one model/hardware setup; R16 also reduces attention work. Preserve causal demand prediction and count PCIe retrieval and complete CPU storage. Oracle hit rates are not deployed capability.
  Evidence locations: §3；§4–5；§6 limitations

**2610.02710 · Self-Supervised Scaling of Terminal Environments for Scientific Domains**

[Paper](https://arxiv.org/abs/2610.02710)

- **agent**: SWR packages 500 real workflows into 3,000 tasks with public IO and hidden judges. Typed scenarios, replay counterexamples, and perfect hidden agreement filter SFT; repeated sampling is reweighting, not new traces. SWR100 has new tasks in familiar workflows, not unseen workflows. Separate 35k development checks from an independent 200-case post-freeze audit with 2% false acceptance/rejection. Oracle public-output selection diagnoses shortcuts and must not reach agents. The method is reusable but a complete author release was not located in the text.
  Evidence locations: Title and complete abstract

**2610.02700 · Learning from Evolving Errors: Adaptive Iterative Repair for On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.02700)

- **post-training**: AIR-OPD starts at the first error anchor and retains repair blocks covering 1−epsilon correction probability mass. It distills privileged multiround teacher guidance with gamma-depth/rho-immediate-success normalized weights. References are training-branch only, and actual DAPO training was run.

**2610.02697 · GeoScaffold: Learning Compact Geometric Latents via Reconstruction for Efficient Vision-Language Navigation**

[Paper](https://arxiv.org/abs/2610.02697)

- **foundation-model**: GeoScaffold first trains a frozen depth VQ-VAE, then eight geometry queries reconstruct depth codes, depth maps, connectivity, and traversability under imitation learning. Remove reconstruction heads and tokenizer at deployment. R2R-CE/RxR-CE support checks.
  Reproduction scope: Matterport data require access permission. Depth and oracle traces are training-only. Retain mixed attention masks and queries during inference. Full training costs roughly 1,500 A100 hours and is not lightweight verification.
  Evidence locations: §3.2–3.3/Eq5–9; §4.1–4.4

**2610.02695 · Test-time Calibration Learning for Large Language Model Reasoning**

[Paper](https://arxiv.org/abs/2610.02695)

- **post-training**: TTCL builds pseudo-correctness and confidence targets from answer agreement, separates advantages for reasoning/answer and confidence tokens, and freezes an EMA target cache each epoch. Unlabeled adaptation and evaluation on the same benchmark are transductive TTT, not independent unseen testing.

**2610.02687 · Decoupling Memory from Context: Structured Memory for Token-Efficient Test-Time Continual Learning**

[Paper](https://arxiv.org/abs/2610.02687)

- **foundation-model**: GraphMemory optimizes agent context memory and is reviewed in the Agent track.
- **agent**: GraphMemory extends ACE with compact index selection and directed evidence graphs. BFS uses two hops, 12 nodes, and 2,500 tokens; ranking uses the Beta(1+help,1+harm) mean. Generation attribution is limited to loaded nodes; the Curator explicitly creates/deletes edges. End-to-end is not O(1) because index size grows. FiNER/Formula select memory on validation before held-out test. Token savings coexist with roughly 1.8× slower queries and lower accuracy on some tasks.
  Evidence locations: Title and complete abstract

**2610.02683 · RAOA: Alternating-Operator Neural Computation with Programmable Radio Propagation**

[Paper](https://arxiv.org/abs/2610.02683)

- **foundation-model**: RAOA alternates normalized energy-gradient problem steps and Hadamard mixing, sharing two control parameters across iterations. A zero-initialized residual adapter supports recurrence studies in frozen LLMs.
  Reproduction scope: Operators and propagation simulation only, without actual RF speed, energy, or quantum advantage. The main 4B depth-one experiment is not depth scaling. Qwen depth gains are flat; paired bootstrap on 768-token GSM8K does not distinguish RAOA, MLP, and frozen. Preserve negative results and match compute.
  Evidence locations: §3 Eq1–4；§4 design；§6 scope；Appendix H

**2610.02670 · LEAP: Learning Efficient Action Proposals For LLM Agents**

[Paper](https://arxiv.org/abs/2610.02670)

- **foundation-model**: LEAP learns action proposals for agents and is reviewed in the Agent track.
- **agent**: LEAP trains a tiny draft with target canonical-action LoRA NLL, without target logits. Propose in cloned environments, verify with targets in parallel on the same GPU, commit only matching prefixes, and hand off cloned state without repeating tools. OpenAGI/TaskBench do not execute tools; tau2/BFCL use local backends. Paired task bootstrap supports 1.10–1.63× whole-task speedup. Cannot apply where external effects cannot safely clone, and target authorship does not guarantee identical concurrent trajectories.
  Evidence locations: Title and complete abstract

**2610.02666 · CHASE-VLA: Post-Training Quantization Framework for Vision-Language-Action Models with Chunk-Aware Scale Estimation**

[Paper](https://arxiv.org/abs/2610.02666)

- **foundation-model**: CHASE-VLA predicts layer/denoising-step group activation-scale distributions from earlier generated action chunks. Quantile loss and variance jointly train a scale estimator, preserving a W4A4 action expert.
  Reproduction scope: Use previously generated chunks, not future gold actions; initialize first chunk with base calibration. LIBERO uses 20 episodes per task. A100 latency is action-expert-only, not full VLA. Deployment needs actual packed low-bit verification.
  Evidence locations: §3.2–3.3；§4.1/4.4

**2610.02657 · Context-Tower Conversion Preserves Generation While Freezing Retains Knowledge: Low-Budget AR-to-Diffusion Conversion of MoE LLMs**

[Paper](https://arxiv.org/abs/2610.02657)

- **foundation-model**: Low-budget AR-to-diffusion conversion uses a frozen context tower and layerwise KV concatenation with matched token/parameter protocols and public-task evidence. Admit as a research conversion operator, not serving acceleration.
  Reproduction scope: Arms also change loss, blocks, and corruption; do not attribute all effects to freezing. A trainable tower has no significant generation difference but differs by 13 MMLU points. Served-AR batch-one throughput is .134/.168; engineering 2× is relative to its own baseline. Extra 150M-token S16 is confounded. Seed two covers only the tower, and the 250M intermediate recheck failed.
  Evidence locations: §3；§4/Table2；§5；§6；§7/Limitations

**2610.02638 · Batched Speech Decisions Without Decoding: Single-Token Supervision Lets a Frozen LLM Hear Beyond the Transcript**

[Paper](https://arxiv.org/abs/2610.02638)

- **agent**: DuplexJev freezes ASR and LLM and trains only the connector with transcript KL and single-letter decision CE. Typed options use randomized positions. Shared prefix KV, block-diagonal suffix masks, and restarted positions provide exact batched logit readout. Multilayer fusion A does not beat final-layer B. Human speech splits by speaker; ZJU emotion training still lowers content by 6–17 points, so mixed loss is incomplete. Streaming 160–200 ms is untested design. Admit speech decision and batched readout operators, not a full duplex agent.
  Evidence locations: §2.1–2.4；§3；§4.1/4.3

**2610.02626 · Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination**

[Paper](https://arxiv.org/abs/2610.02626)

- **foundation-model**: IG-VLA combines future-latent differential inference with SceneGist distillation, a defined lower-cost action-policy candidate.
  Reproduction scope: K, λ, and layer choices came from LIBERO ablation and require independent validation. The 6.38× compares a cited baseline; 169.5 ms on A6000 is not a matched rerun. UR3 uses only 77 demos and 16 trials, so 62.5% versus 56.2% differs by one case. No author code found.
  Evidence locations: §3.1–3.2 Eq1–10；§4.1–4.4 Tables1–5；App A

**2610.02617 · WebUIProof: Benchmarking WebUI Code Generators with UI-Agent Execution Harness**

[Paper](https://arxiv.org/abs/2610.02617)

- **agent**: WebUIProof uses DOM and visual agents to test UIs. Build failures score zero and Full+0.5 Partial aggregation depends on grounding and step budget. Roughly 80% human agreement on 100 items is not deterministic oracle accuracy. VisRL uses screenshots, interaction, and analyzer rewards with PPO. Official releases include 149 general tasks and build/eval/compute_acc code, but no verified repository counterpart for 70 3D tasks among the paper's 219. Limit reproduction to 149 rather than assuming RL or 3D sources are public.
  Evidence locations: Title and complete abstract

**2610.02616 · VERSE: Verified Self-Evolving Optimizer for Agent Harnesses**

[Paper](https://arxiv.org/abs/2610.02616)

- **agent**: VERSE adds trace minimization, joint draft/validation passing, replay and perturbation, failure audits, and self-edits to prompts, tools, and hooks of a frozen-weight harness optimizer. Keep 110 train, 50 val, 108 March test, and 107 July OOD separate. Each row is one evolution and three test repeats, not independent search seeds. Compute differs; retain static verifiers, budget, and validation selection. One flip is not repair.
  Evidence locations: Title and complete abstract

**2610.02614 · What Is Lost in Post-Training? Default Collapse and the Loss of In-Context Steerability Across Diverse Perspectives**

[Paper](https://arxiv.org/abs/2610.02614)

- **post-training**: SDM filters prompts by relevance judge, buckets stance with a second judge, and applies PPO with a population-level penalty for deviation from target distributions across dimensions. Two preliminary Llama8B settings do not establish per-prompt guarantees.

**2610.02597 · GRAFT: Growing Agglomerative Foundation Models via Continual Teacher Distillation**

[Paper](https://arxiv.org/abs/2610.02597)

- **foundation-model**: GRAFT retains old teacher functionality with a historical student anchor and admits new vision teachers using TSRT and image–text relation KL. It is a defined continual-distillation operator.
  Reproduction scope: Main tables compare heterogeneous teachers/data, not a fair ranking. DUNE warm-start costs were not paid again. Removing LoRA to restore base is not shared-student retention. Downstream requires new head/decoder tuning, not zero-shot. No official source entry point found in the paper; complete schedule and provenance are needed.
  Evidence locations: §3.1–3.3 Eq1–10；§4.1–4.3 Tables1–2；AppA

**2610.02593 · Fisher-Guided Submodular Data Selection for Continual Pre-Training of Large Language Models**

[Paper](https://arxiv.org/abs/2610.02593)

- **foundation-model**: Dual Fisher geometry and streaming submodular selection define a CPT data algorithm candidate, not industrial deployment evidence.
  Reproduction scope: This does not use F as an update penalty. Diagonal LoRA F, warmup, and projection are approximations; 1/2−ε applies only to the surrogate. Even with equal tokens, count candidate gradients and reference F. Two medical-domain backbones do not show generalization. No author code found; perplexity heuristics cannot replace double logdet.
  Evidence locations: §3；§4.1–4.4 Tables1–2；App A/B/E
- **post-training**: Fisher/submodular data selection serves continual pretraining and is routed to the foundation-model track.

**2610.02588 · Open-Endedness Bench: Measuring Epistemic Process from Agent Records**

[Paper](https://arxiv.org/abs/2610.02588)

- **agent**: OEB converts traces into action/proposition evidence cards, verifies quoted substrings, constructs an epistemic graph via three closed-question votes, and aggregates deterministically. Abstain without opportunities and omit scores with fewer than five. Separate four capability axes from persona instead of summing them. Ninety human audits and 119 existing runs over 12 tasks are correlational. A median 652 judge calls is not low-cost online reward. Official MIT pipeline/converters and HF scored runs were verified.
  Evidence locations: Title and complete abstract

**2610.02569 · Pincer: Resource Authorization for Agents using a Digital Twin**

[Paper](https://arxiv.org/abs/2610.02569)

- **agent**: Pincer trusts complete OS mediation and an isolated twin. Trusted user state, PRF obfuscation of access-pattern path segments, content, and precommitted policy support three conjunctive votes. PRF only limits the resource-name advantage, not all injection. Prior access is not user authority. Synthetic evaluation uses two personas, one model each, and conditional ASR/BGR for the resource gate, not task success. The paper says implementation/data are forthcoming; the algorithm is a candidate but the dataset is not verified runnable.
  Evidence locations: Title and complete abstract

**2610.02542 · How To Train Your World Model: Fine-tuning vs RAG for LM-based World Modeling**

[Paper](https://arxiv.org/abs/2610.02542)

- **agent**: LM world-model research compares fine-tuning and RAG and proposes HWM: next-token prediction conditioned on transitions retrieved with the same episode excluded, optionally using hierarchical observation/action queries. A frozen policy standardizes planning. The authors report 17 wins in 20 model/environment combinations. Actual-environment oracle and post hoc top-20 gold reranking are diagnostic, not deployment inputs. Nonconstructed models winning 9/20 shows limited extrapolation; separate transition fidelity and task utility.
  Evidence locations: Title and complete abstract

**2610.02525 · Learning What to Investigate Next: Meta-Reasoning for Long-Horizon Research Agents**

[Paper](https://arxiv.org/abs/2610.02525)

- **agent**: MIRA freezes curation and executor and trains only outer work-order and terminate decisions. The shared actor–critic uses single-token discrete-return KL, decision GAE, and cross-version bootstrap bridge. Mask policy gradient outside ratio range but retain squared log-ratio penalty; update separate buffers/optimizers in order. Four research environments distinguish proxy/gold. Shared initialization from critic confounds an ablation of parameter sharing itself. Inner tool and experiment tokens are not trained.
  Evidence locations: Title and complete abstract

**2610.02523 · Hypothesis-guided discovery of cognitive algorithms via program refinement**

[Paper](https://arxiv.org/abs/2610.02523)

- **agent**: Start from human-written FlipPy cognitive programs. Game proposes behavioral revisions, Coding implements them, Audit permits up to five repairs, and Inference evaluates behavioral likelihood. Of 846 candidates, 733 executed and 24 representatives were selected by semantic clustering, not fully autonomous theory discovery. Held-out trials were excluded from generation and selection; 72/137 improved. Synthetic recovery recovers 75% of the predictive gap in only 8.4% of cases. Constrained program search and held-out likelihood could generalize as an evolve operator, but the anonymized OSF lacks a locatable link, so materials are not verified.
  Evidence locations: Title and complete abstract

**2610.02480 · MEA: A Reward-Driven Multi-Agent System for Faithful Model Explanations**

[Paper](https://arxiv.org/abs/2610.02480)

- **agent**: MEA shares a backbone between the tool-policy Proposer and explanation Actor. Mask and requery the original classifier for faithfulness; use a common terminal GRPO advantage. Vision area λ=.3 and tool count λ=.05 limit gaming, with top-25% constraints for text/tabular tasks. Three modalities and unseen Q8/Q9 are tested. Masking diagnoses model behavior, not real causality. Keep actual classifier/XAI calls rather than LLM self-grading.
  Evidence locations: Title and complete abstract

**2610.02478 · Tropical Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.02478)

- **agent**: Tropic maintains observed state/fragment graphs in deterministic resettable environments. Freeze and rescore actors per round, use max-plus prefix/suffix for best verified reachable paths, and replay complete paths to validate frontier sampling and top-L stitching. Update by per-token NLL from best and low-coverage archived paths, without reward baselines or negatives. Four environments, two backbones, and three training seeds use held-out instances. Gold paths and nonresettable real APIs cannot substitute.
  Evidence locations: Title and complete abstract

**2610.02472 · APDMem: Agent-Controlled Progressive Disclosure for Query-Adaptive Long-Term Memory**

[Paper](https://arxiv.org/abs/2610.02472)

- **agent**: APDMem builds L0 summary indexes and L3 originals first and caches L1 facts/L2 turn notes on demand. Hybrid search and RRF support agent drill-down; reflection stops with no new evidence or at 20 steps. Draft→organized notes→answer. LongMemEvalS has 500 items; baseline scores are cited, not all rerun. Online costs are provided only for this method and exclude shared answer generation; no equal-budget win over all baselines.
  Evidence locations: Title and complete abstract

**2610.02462 · Capability Scaling-Down Laws for LLM Compression**

[Paper](https://arxiv.org/abs/2610.02462)

- **foundation-model**: Predict pruning, quantization, and distillation loss separately by capability: shared pruning-density curves, bit/group-size grid interpolation, and distinct data-volume and exposure terms for distillation. This can inform Evolve budget allocation.
  Reproduction scope: Coefficients do not transfer across model families automatically. Table 2 rules marked † were chosen after viewing test, requiring new frozen validation. Less measurement is not capability improvement. Official analysis/measurement mirrors omit original teacher text and adapter weights. V47 freeze was missing and explicitly replaced by V70. Old log analysis is not new training.
  Evidence locations: §3–4 Eq3–4；§5.1/Table1；§5.2/Table2；official README

**2610.02460 · CUEing User Simulators: Calibrated User Embeddings for Multi-Turn Benchmarking**

[Paper](https://arxiv.org/abs/2610.02460)

- **agent**: CUE attention-encodes user turns and preceding assistant turns, decodes slot commands, and samples via latent diffusion. Content suppression does not guarantee removal of task or outcome information. Completed-human-trajectory replay is retrospective calibration, not future prediction. Only sampled personas without target traces simulate new users; session mixtures are not population distributions. Includes 483 tauUSI and held-out SimulatorArena/PRISM. Official Apache 2 runtime/training and HF model, annotation, and example-pool entries exist; code was not executed.
  Evidence locations: Title and complete abstract

**2610.02444 · Counterexample Generation via Per-Theorem Symbolic Verifiers: When Imitation Hurts and Reinforcement Repairs**

[Paper](https://arxiv.org/abs/2610.02444)

- **post-training**: SymCE releases counterexample tasks, per-theorem Python verifiers, structural schemas, and dense/sparse rewards for RLVR/Evolve. Author repository includes corpus/splits, oracle/sandbox, runner, and item results. Schemas derive from canonical witnesses; audit possible answer-shape leakage and isolate arbitrary Python execution.

**2610.02425 · Finding the Move Is Not Winning the Game: XiangqiBench for Closed-Loop Evaluation of LLM Agents**

[Paper](https://arxiv.org/abs/2610.02425)

- **agent**: XiangqiBench provides 119 searched and human-verified endgames, not formal proofs. Gold solutions stay out of agent tools. Use fixed 40-ply/depth-18 defender, fail after three consecutive illegal moves, and simplify repetition rules. The 8,568 traces cover 12 models, two settings, and three trials; report pass@3 and all-success separately. Sighted/Restricted prompts differ. Official MIT run/score and dataset card are public, Pikafish GPL separately. Original NNUE was replaced; pin engine and network, not an arbitrary newer release.
  Evidence locations: Title and complete abstract

**2610.02404 · Trained Agentic Context Management**

[Paper](https://arxiv.org/abs/2610.02404)

- **foundation-model**: Self-calling and context-management training belong to the Agent track.
- **agent**: Agentic context management trains minimal read_chunk/spawn tools with oracle SFT for tree reduction, sequential folding, and boundary expansion. RL degraded and is not a successful method. RULER uses five examples per type and OOLONG ten per family, with different native baseline context. An 8k agent budget can scale but cost was not formally quantified. Tune temperature on validation and hide oracle training scripts from evaluated agents.
  Evidence locations: Title and complete abstract

**2610.02396 · Inherit-MAS: Test-Time Evolution of Multi-Agent Systems through Workflow and Execution Inheritance**

[Paper](https://arxiv.org/abs/2610.02396)

- **agent**: InheritMAS prunes the latest-incumbent DAG before one edit and uses a separate judge for lexicographic final ranking. Inherit only read-only nodes with exact resolved requests matching model, parameters, upstream and environment fingerprints plus valid record hashes. State-changing sinks run live. WorkBench/HotpotQA baselines have partly unequal retrieval budgets. Inherited tokens are equivalent historical volume, not consumed tokens; judge maxima do not guarantee monotonic utility.
  Evidence locations: Title and complete abstract

**2610.02388 · Octrees as an Explicit 3D Language**

[Paper](https://arxiv.org/abs/2610.02388)

- **foundation-model**: OctLLM uses a sparse six-level octree, separate 3D branch, and 3D RoPE with frozen Qwen2.5-VL. It also trains occupancy completion and uses TRELLIS decoding. Objaverse-XL, HSSD, ABO, ShapeNet, Toys4K, and PointLLM200 support checks.
  Reproduction scope: 195k assets exclude PointLLM200. The 12 branches have roughly 2.8B trainable parameters, not a tiny adapter. Preserve TRELLIS external decoding and licenses. The paper says released, but links were not verified in this review.
  Evidence locations: §3.1–3.4; §4.1–4.3; Appendix A/B/D/E

**2610.02361 · SEDIMA: Cross-Run Hierarchical Insight Memory for Evolutionary Search Agents**

[Paper](https://arxiv.org/abs/2610.02361)

- **agent**: SEDIMA stores raw evaluation, LLM insight, and attention-centroid clusters. Before mutations it retrieves clusters and insights with traces and suggests three edits, without changing the evolution searcher. AlgoTune/ALE private scores are separate from public fitness, and memory is built on disjoint problems; cold starts also write memory online. Matching 100 candidates does not match tokens/calls. Main results are one run, with three seeds only for ablation/transfer. Bounded context does not mean constant total retrieval cost.
  Evidence locations: Title and complete abstract

**2610.02359 · Lexicographic Multi-Objective On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.02359)

- **post-training**: LMOPD routes to the expert for the highest-priority unsatisfied reward, then applies one ordered projection to centered log-policy corrections for a virtual teacher. Real multi-expert experiments use private training data; one nonorthogonal projection cannot guarantee all constraints or no reward regression.

**2610.02351 · DeReAct: Decomposed Reasoning and Acting for Reliable AI Agents**

[Paper](https://arxiv.org/abs/2610.02351)

- **agent**: DeReAct Brain proposes intents and commands; a separate Critic gates them fail-closed under constraints, and CM retains environment-supported state and decides completion. Brain also sees the first five plus recent-window events. GAIA165/SWE489 use native non-LLM success grading; report pass1 and pass3 over three attempts and separate grounding judges. CM is model judgment, not formal verification; fixed Claude critic/CM are not real external-effect validation. A success flag cannot replace benchmark tests.
  Evidence locations: Title and complete abstract

**2610.02349 · MIRROR: Multipath Quorum Integrity for LLM Multi-Agent Communication**

[Paper](https://arxiv.org/abs/2610.02349)

- **agent**: MIRROR generates canonical bytes once at the sender and recovers by majority across five logical routes with three payloads and two digests. Unkeyed hashes are not authentication; guarantees depend on honest endpoints, fewer than half compromised routes, and second-preimage resistance. AutoGen/CAMEL/MetaGPT and Gemma/Gemini evaluation uses logical routes over shared backends, not independent fault domains or measured latency. It addresses in-transit tampering, not already-injected senders.
  Evidence locations: Title and complete abstract

**2610.02344 · Drive vs. Decay: On the Training Dynamics of Joint-Embedding Predictive Architectures**

[Paper](https://arxiv.org/abs/2610.02344)

- **foundation-model**: ResidualPred uses residual predictors and diagonal attention initialization to suppress JEPA collapse. Table 5 has five seeds and matched ImageNet1K 30-epoch controls, supporting the mechanism.
  Reproduction scope: Linear drive/decay theory does not prove nonlinear network behavior. Gains shrink at 90 epochs. Full official I-JEPA scale was not run.
  Evidence locations: §4；§5；§6.1–6.2/Table4/Table5；§7–8

**2610.02330 · Choosing Before Acting: Comparative Value Estimation for Long-Horizon Tool-Use Agents**

[Paper](https://arxiv.org/abs/2610.02330)

- **agent**: CITA/CIM trains value BCE, gap MSE, and transitivity/confidence from observed same-context success rates, Bayesian-graph synthetic outcomes without real APIs, and LLM simulation comparisons. Vc ranks the next tool; confidence-weighted value and task reward train GRPO. Toolathlon/TOUCAN/TRAJECT use Qwen7B/Llama8B. Value is not true causal counterfactual; label sandbox data synthetic and keep real closed-loop evaluation independent of CIM scores.
  Evidence locations: Title and complete abstract

**2610.02324 · Slow-Fast Multi-Teacher On-Policy Distillation for Capability Preservation**

[Paper](https://arxiv.org/abs/2610.02324)

- **post-training**: SF-MOPD maintains an EMA slow student, uses slow–fast log-probability directions to remove teacher conflict components, and applies JSD distillation with original MOPD regularization. QwenVL2/4/8B ran multiple domains. Use real EMA parameters rather than fixed references.

**2610.02323 · World-Calibrated Proposal-to-Action Flow for Vision-Language-Action Models**

[Paper](https://arxiv.org/abs/2610.02323)

- **foundation-model**: ProAct publishes the training core. Proposal, world calibration, and anisotropic flow are candidates, starting with executable LIBERO.
  Reproduction scope: This is not a counterfactual world model: it predicts expert futures rather than futures after proposal execution. Trained ProAct weights and full RoboTwin rollouts are not public. π0.5 initialization is not reproduced weights. Normalized Da is absorbed by the pipeline, so do not multiply twice. Use executed history only and reset per episode. Cached-frame latency excludes transfer/simulation and is not closed-loop speed.
  Evidence locations: §2.2–2.4 Eq2–11; §3; App A/E/F; official README

**2610.02304 · SimuVerity: Benchmarking Agents for Engineering-Grade Simulink Model Generation**

[Paper](https://arxiv.org/abs/2610.02304)

- **agent**: SimuVerity covers 101 tasks across ten engineering domains. Separate public specs/profiles from hidden scenarios and thresholds. Delivery, execution, and qualification gates precede six-axis grading. Missing deliverables and candidate failures count; rerun infrastructure failures. Six agents each run three times per task. A ten-strong-task ablation is selective, not overall causality. The Apache 2 repository releases tasks, scenarios, scorers, references or import recipes, and result verification. MATLAB/Simulink commercial products and third-party licenses vary by task.
  Evidence locations: Title and complete abstract

**2610.02298 · EditHero: A Benchmark for Long-Horizon Part-Level 3D Editing and Vibe Modeling**

[Paper](https://arxiv.org/abs/2610.02298)

- **foundation-model**: EditHero reconstructs exact 3D targets for 457 chains and 2,755 turns from part libraries and operation logs. Self-rollout separates edited and preserved areas and compares no-op and regeneration controls for multi-turn generation evaluation.
  Reproduction scope: Methods see current target renders, not operation logs or GT 3D. VoxHammer receives a gold mask and has different information. Completed-turn means suffer censoring; report coverage. Separate conditioning and holdout views, and check asset licenses by source.
  Evidence locations: §3 construction；§4 protocol；§5.1；Appendix9/12/18
- **agent**: EditHero covers 457 chains, 2,755 edits, and 252 hosts with exact logs isolated. Self-rollout uses one conditioning and three held-out views; IF and CC assess edited and unedited regions. Agent results cover a selected 55-chain, 416-turn visible-edit subset, with coverage required alongside completed-turn means. Methods and experiments were reviewed, but official README checkboxes for benchmark engine/eval code and HF edit chains remain incomplete; defer due to no public execution entry, not unread material.
  Evidence locations: Title and complete abstract

**2610.02206 · KaliBench: A Fine-Grained Benchmark for Cybersecurity Tool Use on Kali Linux with Runtime-Free Verifiable Rewards**

[Paper](https://arxiv.org/abs/2610.02206)

- **post-training**: KaliBench releases 8,504 query–command pairs, 1,642 tools, and runtime-free shlex scoring under three information conditions with alias-aware arguments. This is offline command-string scoring, not real execution. Do not execute commands automatically against live targets.
- **agent**: KaliBench releases 8,504 query–command pairs, 1,642 tools, and runtime-free shlex scoring under three information conditions with alias-aware arguments. This is offline command-string scoring, not real execution. Do not execute commands automatically against live targets.
  Evidence locations: §3 Evaluation Protocol; §4; Appendix L; author repository README and file listing checked read-only

**2610.02204 · Reconstruct, Practice, Go Real: Guided Self-Improvement for Embodied Agents**

[Paper](https://arxiv.org/abs/2610.02204)

- **agent**: RPG reconstructs MuJoCo tasks from ABC video with human-checked frozen evaluators. Runtime sees deployment observations only; privileged separate episodes support failure analysis. Implementor edits skill/prompt. Paired five-seed gates across 22 tasks require positive average gains and no single-task drop over .2, followed by merge retest. Fifteen rounds use one run and unmatched candidate compute. Saved-round held-out-seed retrospective testing is not unseen tasks. Three real robots run ten trials each with frozen common calibration. Privileged traces are not deployment policy inputs.
  Evidence locations: Title and complete abstract

**2610.02202 · ScholarCatalyst: A Benchmark for Retrieving Papers That Inspire New Research**

[Paper](https://arxiv.org/abs/2610.02202)

- **agent**: ScholarCatalyst covers 207 real projects and 894 queries (207 Core and 687 Sub), with author-verified inspiration and hard negatives. Remove solution leakage and cut the corpus by source-paper completion date. Recall labels are incomplete; oracle reranking is diagnostic. Public 191k documents, evaluation, and constrained local-corpus agentic search scripts under CC-BY-NC 4 are infrastructure, not a training loss.
  Evidence locations: Title and complete abstract

**2610.02196 · InterEvolve: Test-Time Evolution of Reward Programs for Humanoid Loco-Manipulation**

[Paper](https://arxiv.org/abs/2610.02196)

- **foundation-model**: InterEvolve evolves staged reward programs over a frozen forward/backward motion prior. Inner CMA-ES tunes parameters and an outer LLM edits structure, using fixed scenarios and reusing verified skills. OMOMO/GRAB and eight simulated task types support evaluation.
  Reproduction scope: Isolate verifier/evolution scenarios from final test. Rewards may use privileged simulator state but cannot pass correct test plans to the policy. Real G1 demos do not establish local verifiability.
  Evidence locations: §3.1–3.4; §4.1–4.4; Appendix B/D/E

**2610.02191 · The Missing Primitive: Diagnosing and Repairing Mathematical Reasoning in Large Language Models**

[Paper](https://arxiv.org/abs/2610.02191)

- **post-training**: Absorb gives the teacher mathematical primitives only in training. A one-sided reverse-KL clamp limits suppression of student preferences while retaining positive guidance. Prim/HLE/HMMT/Omni were tested; gold primitives must not reach evaluated students.

**2610.02190 · Trust the Direction, Search the Step: Zero-and-First-Order Methods for LLM Fine-Tuning**

[Paper](https://arxiv.org/abs/2610.02190)

- **post-training**: ZFO uses the base first-order optimizer direction and two same-batch positive/negative forwards to estimate second and third derivatives. Taylor/Padé interval step selection includes a singularity fallback. Actual LLM tuning and overhead were measured; match extra forward budgets.

**2610.02161 · DuoMind: Enabling Distributed Multi-Robot Coordination with Semantic Communication**

[Paper](https://arxiv.org/abs/2610.02161)

- **agent**: DuoMind gives each robot a high-level VLM orchestrator and VLA actions, with communication of intent, subgoal, belief, and optional uncertainty. No special joint training. Seven RoboPoly plus eight RoboTwin dual-arm distribution changes; 50 dual-robot demos per task become 100 single-agent training examples. Shared global camera and local wrists. Two simulated robots do not establish large real swarms. Communication and π0 replacement ablations support reuse, not scale claims.
  Evidence locations: Title and complete abstract

**2610.02150 · From Knowledge Access to Source Learning: Developing Source-Specific Competence**

[Paper](https://arxiv.org/abs/2610.02150)

- **agent**: SourceLearn maintains source-grounded entity representations through Inspect/Deepen/Connect and consolidation. Task-guided variants use training guidance answers only to diagnose evidence gaps and reread sources, updating representations/prompts rather than weights. Five tasks use three 30/70 guidance/test splits and AppWorld's official split. Test answers stay out of memory, with separate QA judge and native execution metrics.
  Evidence locations: Title and complete abstract

**2610.02140 · Finetuning with Sampling: SFT Learns Better Than You Think**

[Paper](https://arxiv.org/abs/2610.02140)

- **post-training**: Projection Sampling uses expert-conditioned proposals and blockwise Metropolis–Hastings to keep informative traces close to the base distribution before SFT. Actual chemistry, math, and open-domain training was run. Finite MCMC is not exact sampling from an ideal projection.

**2610.02091 · GeoLatent: Geometry-Guided Latent Structuring with Routed Optimization for 3D Reasoning**

[Paper](https://arxiv.org/abs/2610.02091)

- **foundation-model**: GeoLatent separates shared geometry and residuals and uses three-stage routing optimization to block visual shortcuts into answers. DA3/VGGT targets supervise only latents. SPAR/SpatialLadder and SPBench/ViewSpatial enable actual evaluation.
  Reproduction scope: Geometry teachers are training-only. Deduplicate or disclose 37 overlapping ScanNet scenes. Test routing interventions rather than adding geometry labels and claiming shortcuts were blocked.
  Evidence locations: §3.2–3.4; §4.1–4.4; Appendix B

**2610.02019 · Controllable Multi-label Video Safety Detection via Adaptive Tversky Policy Optimization**

[Paper](https://arxiv.org/abs/2610.02019)

- **foundation-model**: ATPO's adaptive Tversky RL reward for video safety is reviewed by post-training.
- **post-training**: ATPO adjusts Tversky alpha/beta from EMA log-ratio error feedback of FN and FP, fixing their sum at two. It controls global or per-class multilabel reward. Actual VideoVLM training supports a new adaptive reward controller, not a renamed GRPO.

**2610.02005 · Counting Moves, Weighing Voices: Bayesian Dialectical Argumentation for Calibrated Multi-LLM Councils under Persistent Adversaries**

[Paper](https://arxiv.org/abs/2610.02005)

- **agent**: BDA turns Propose/Challenge/Concede into signed endorsement counts and integrates Beta reliability in Dawid–Skene-style aggregation, with roughly 25 labels for matched calibration. K>2 pseudo-likelihood requires tempering; calibration theory assumes binary, no challenge, and other conditions. Stable-label identity learning fails for position-based MCQ. No guarantee against sleeper attacks or reliability shifts. This is a new aggregator, not an unconditional robustness win.
  Evidence locations: Title and complete abstract

**2610.01962 · SIEVE: Selective attention-value Suppression for Vision-Language Models Unlearning**

[Paper](https://arxiv.org/abs/2610.01962)

- **foundation-model**: SIEVE alternates negative CE and zero attention values on forget data with positive CE and frozen-reference value matching on retain data. Synthetic Profile Visual-QA/Textual-QA supports selective forgetting tests.
  Reproduction scope: It does not directly constrain attention weights or establish real privacy/GDPR deletion. Test text and visual access, retain-set damage, and relearning separately.
  Evidence locations: §3.2.1–3.2.3/Eq4–8/Algorithm1; §4.1/4.4; Appendix C

**2610.01955 · Do Your Own Research: Learning to Forecast by Learning to Search**

[Paper](https://arxiv.org/abs/2610.01955)

- **post-training**: prime-forecast releases tool environments, historical questions, and rollout logs, with point-in-time filtering, blocked market prices, Brier scoring, and abstention imputation. Split train/test by resolution date. Live search and API filters are not static, and perfect filtering on a small sample is not leakage proof.
- **agent**: prime-forecast releases tool environments, historical questions, and rollout logs, with point-in-time filtering, blocked market prices, Brier scoring, and abstention imputation. Split train/test by resolution date. Live search and API filters are not static, and perfect filtering on a small sample is not leakage proof.
  Evidence locations: §2–4; Appendix C; author repository README and file listing checked read-only

**2610.01921 · Cross-Lingual Alignment for Decoder-Only Models using MoE Routers**

[Paper](https://arxiv.org/abs/2610.01921)

- **foundation-model**: XLR aligns languages in middle layers by KL over sequence-mean sparse routing probabilities on parallel text. Its CPT auxiliary loss and packing are defined, with public training and evaluation, making it a foundation-model training candidate.
  Reproduction scope: Middle layers were picked visually for two small models; long pretraining and more languages are unverified. Router-only training is not a reliable substitute. Verify epsilon/zero handling for sparse KL and disclose any switch to full softmax. Authors state cleaned private paths are untested and not turnkey; published code is not a reproduction pass. Include additional English compute.
  Evidence locations: §3 Eq1；§4.1–4.4；§5/Table1–2；App C/F；official README/contrastive_training README

**2610.01917 · MoLE: Mixture of Latent Experts for Complementary Visual Reasoning**

[Paper](https://arxiv.org/abs/2610.01917)

- **foundation-model**: MoLE introduces routed vision evidence, expert value transforms, and isolated latent experts plus summary topology. Public data and a detailed appendix support a faithful vision-reasoning implementation.
  Reproduction scope: Latent tokens are not FFN experts. ESVA changes V only on routed edges, not globally. Gold is only an answer label and cannot affect inference routing. Eight latents do not match FLOPs, and parameters are added. K=2 and other benchmark-selected settings need frozen validation. Proprietary baselines are external and some CVBench components are inferred. No author source found.
  Evidence locations: §3.2 Eq4–13；§4 Table1；App A.1–A.4/A.7

**2610.01892 · Selection-Based Structured Reasoning: Toward Efficient Multimodal Search Agents**

[Paper](https://arxiv.org/abs/2610.01892)

- **post-training**: SSR is not ordinary tool use: batched teacher-forced mean-logprob softmax chooses among six shared reasoning templates, then inserts full text before generating an action. SFT uses selector plus action NLL. GRPO uses one categorical selector ratio plus action-token ratios, with no token training on inserted templates. Appendix B detaches rollout competition scores; only first-step probabilities are exact and later ones approximate. Qwen3VL2B/4B run seven multimodal search tasks. Include candidate prefill in efficiency and retain the original post-training abstract-screen miss corrected by full text.
- **agent**: SSR is not ordinary tool use: batched teacher-forced mean-logprob softmax chooses among six shared reasoning templates, then inserts full text before generating an action. SFT uses selector plus action NLL. GRPO uses one categorical selector ratio plus action-token ratios, with no token training on inserted templates. Appendix B detaches rollout competition scores; only first-step probabilities are exact and later ones approximate. Qwen3VL2B/4B run seven multimodal search tasks. Include candidate prefill in efficiency and retain the original post-training abstract-screen miss corrected by full text.
  Evidence locations: Title and complete abstract

**2610.01815 · Debias Anything: Fairness with Diversity without Supervision in Diffusion Models**

[Paper](https://arxiv.org/abs/2610.01815)

- **foundation-model**: Debias Anything trains a semantic adapter on frozen diffusion models using attribute directions, target proportion guidance, and disagreement diversity for batch-level debiasing. Public faces and diffusion checkpoints support quality/fairness comparisons.
  Reproduction scope: An adapter is trained, so the whole process is not training-free. Group proportions do not prove individual fairness. Public code links remain unverified.
  Evidence locations: §4.1–4.3; §5.1–5.2; Appendix C/D
- **post-training**: This is image-diffusion fairness and diversity guidance, not language-model RL or OPD.

**2610.01769 · CONTRA: Discovering and Qualifying Behavior-Changing Questions for Selective Clarification in LLM Code Generation**

[Paper](https://arxiv.org/abs/2610.01769)

- **agent**: CONTRA discovers possible questions over multiple turns, then requires relevance and an issue unresolved by the original request. Sample three programs per potential answer and at least seven common inputs; keep questions only with 2/3 within-group stability and a cross-group difference on at least one input. Failure is not proof of equivalence. Use history to choose another question or stop. 419 underspecified and 80 complete tasks allow up to five questions, with three GPT-4o votes for gold matching. Four-model macro F1 is 41.20 versus 27.32, with isolated execution. This is a reusable execution-evidence clarification operator, not online A/B from plugin deployment.
  Evidence locations: Title and complete abstract

**2610.01741 · ATI-VLA: Action-Centric Predictive Vision-Language-Action Models via Actionable Alignment Then Adaptive Injection**

[Paper](https://arxiv.org/abs/2610.01741)

- **foundation-model**: ATI-VLA shares a quantized action/observation space with hierarchical side injection, a VLA algorithm candidate.
  Reproduction scope: Inference needs neither future frames nor actual actions; do not fill side paths with them. Obtain quantization gradient and codebook settings from author code. Training uses eight H100s and deployment a 5090. Checkpoints chosen on benchmark validation need independently split test seeds and scenes. Distinguish cited and rerun baselines. Project page exists, but public source was not verified.
  Evidence locations: §2.2 Eq5–15/Alg1；§3；App A/B/E

**2610.01710 · CoEvolve: Construct-to-Edit Visual Grounding with Bidirectional State Refinement**

[Paper](https://arxiv.org/abs/2610.01710)

- **foundation-model**: CoEvolve trains ordered multistep bounding-box progress with RER-GRPO, then denoises coordinates with BDR while retaining reasoning text. RefCOCOg train and held-out RefCOCO/+ support tests.
  Reproduction scope: Controlled corruption recovery 58.8→86.19 is not recovery from natural errors. DIOR uses in-domain retraining, not zero-shot. GT coordinates are for reward/training targets only.
  Evidence locations: §3.2–3.3; §4.1–4.5; Appendix B/E

**2610.01687 · Architectural Sampling: Test-Time Scaling via Computational Diversity in Frozen Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.01687)

- **foundation-model**: Architectural Sampling repeats frozen VLM layer windows with different recursion counts to generate architectural rollouts, then trains with label-free self-reward TTRV-GRPO. Public models and 12 benchmarks support verification.
  Reproduction scope: Oracle Pass@k coverage is not deployable Pass@1. Test effective selectors and TTRV separately. Layer repeats cost compute; match FLOPs/tokens. API-only black boxes cannot support this.
  Evidence locations: §3.1–3.3; §4.1–4.2; §5/Table5; Appendix E

**2610.01670 · Do MLLM Judges Judge the Edit? Auditing Bias in Image Editing Evaluation with Verified Quality Preservation**

[Paper](https://arxiv.org/abs/2610.01670)

- **foundation-model**: EditJudgeBias audits VLM judges with 13 quality-preserving cues and sham/actual-degradation controls. The method is reusable, but releases omit benchmark images, human labels, and judge/validator outputs, preventing exact reconstruction of 1,196 triplets.
  Reproduction scope: Five dataset names correspond to three independent content pools, so cluster pairs accordingly. SSIM, calibrated VLMs, and limited human assessment jointly check quality preservation, rather than assuming each pixel edit is harmless. The mitigation is only an initial pilot.
  Evidence locations: §3.1–3.4；§4 metrics；reproducibility statement；Appendix A
- **post-training**: EditJudgeBias independently audits judge bias through quality-preserving cues, sham/retest noise baselines, swapped order, and paired statistics. Official cue/judge/metric CLI can test new judges, but missing full images, human labels, and author I2EBench outputs prevent exact reproduction.

**2610.01649 · CrossGMN: Graph Metanetworks for Cross-Architecture Weight-Space Transformations**

[Paper](https://arxiv.org/abs/2610.01649)

- **foundation-model**: CrossGMN is a small-model compression or Evolve meta-operator candidate, not established LLM compression support.
  Reproduction scope: Up to roughly 200k parameters, requiring access to teacher parameters and compatible inputs/outputs. Distinguish theoretical plain GMN and experimental ScaleGMN. Include amortized teacher-group training. MLP speedup is only 1.04× with 5% failures. No public code found; select anchors by validation rather than best test.
  Evidence locations: §3 Eq1–3；§4 Eq4–5/Theorem1；§5.1–5.4；Limitations；App D.1–D.7

**2610.01640 · Not All Error Yields to Scale: Where Scaling Stops in Vision-Language Inference**

[Paper](https://arxiv.org/abs/2610.01640)

- **foundation-model**: Separable Inference Scaling Law fits error floors and power laws separately by backbone parameters and actual vision token count, using a cost surface to choose held-out settings. It can inform multimodal budget planning.
  Reproduction scope: 26 pretrained models and 650 cells. N excludes encoders/projectors that also differ by family, so coefficients are not pure backbone causality. Prompt backbone FLOPs exclude visual front-end and decoding; not end-to-end latency. Pair-resample matching HRBench4K/8K questions. Use a new validation grid and independent test, not fitting and reporting selection gain on the full benchmark.
  Evidence locations: §2.2–2.3；§5.1–5.3；Appendix evaluation grid

**2610.01637 · Fusing Visual and Textual Representations via Multi-layer Fusing Transformers for Vietnamese Visual Question Answering**

[Paper](https://arxiv.org/abs/2610.01637)

- **foundation-model**: MFT fuses PhoBERT/ViT through multilayer bidirectional cross-modal attention for Vietnamese VQA classification. Public ViVQA supports training and EM/token F1, a narrow multimodal candidate.
  Reproduction scope: Not a generative LLM. Replace the paper's random 80/20 without independent validation with explicit train/validation/test. Published scores from others are not fair reruns.
  Evidence locations: §3.1–3.4; §4.1–4.5

**2610.01625 · Beyond Domain-Level Adaptation: Margin-Oriented Semantic-Appearance Interaction Correction for Personalized Federated Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.01625)

- **foundation-model**: MOSAIC combines shared/private prompts, domain–class residuals, low-rank class corrections, and instance gating over frozen CLIP. Public Office31/Home/DomainNet federated classification supports tests.
  Reproduction scope: The paper reports the highest test accuracy across rounds without independent validation. Select rounds on validation and disclose protocol changes. True-class residual subtraction is diagnostic; inference must compute all candidate classes.
  Evidence locations: Method/Eq10–13; Experiments; Appendix B/F

**2610.01605 · Hob-VL: A Benchmark for Visually Grounded Boolean Reasoning**

[Paper](https://arxiv.org/abs/2610.01605)

- **foundation-model**: Hob-VL provides public symbolic and natural-language visual Boolean composition and De Morgan consistency evaluation, supporting new-provider inference and strict offline grading.
  Reproduction scope: Shared scenes and equivalent rewrites are not independent. Dummy/offline placeholders are not real models. Give models image and predicates/questions, not truth assignments. Generation scripts are not public, but fixed evaluation material and entry points are.
  Evidence locations: §4 construction; §5.1; official README evals.verify_release/results

**2610.01595 · Before It Fades: Reinforcing Temporal Representations at Inference Time in VideoLLMs**

[Paper](https://arxiv.org/abs/2610.01595)

- **foundation-model**: TAI compares forward/reversed video activations by layer and injects input-specific peak vectors into later layers with decay. Three frozen VideoLLMs and four public temporal benchmarks support evaluation.
  Reproduction scope: Two forward/reverse passes are not free. Keep nontemporal controls and count all extra FLOPs. Do not choose layers using correct answers.
  Evidence locations: §3.1–3.2; §4; §5; Appendix evaluation protocol

**2610.01569 · Managing Context and Communication in Distributed Agentic UAV Swarms**

[Paper](https://arxiv.org/abs/2610.01569)

- **foundation-model**: Distributed UAV agent context and communications management belongs to the Agent track.
- **agent**: Distributed UAVs use peer-tag residual embeddings and recency-novelty minimum-distance gossip. Offline manager thresholds choose discard/compact/full; receiving queues only estimate what neighbors know. Three memory FIFO token budgets with ID/path/TTL deduplication. Ten-aircraft SITL search and rescue uses an analytical 802.11n model, not real radio. Proposals all finish versus flood 70–85%; later time/error statistics condition on successes. Do not report only 6–7 MB falling below 0.5 MB. Communications and memory policies may generalize.
  Evidence locations: Title and complete abstract

**2610.01564 · Chaining Skills to Hijack LLM Agents**

[Paper](https://arxiv.org/abs/2610.01564)

- **agent**: APEX studies cross-skill artifacts that misrepresent progress as authorization. Sandbox execution feedback optimizes chains; defense uses taint and original-request verification. 690 attempts across four targeted families yield 512 successes, with family task overlap. Utility is weighted checks, not whole-task success, and more workloop tokens do not imply unauthorized effects. MIT execution, trace checks, and controlled reference variants are public; obtain SkillsBench separately. Use defensive sandbox evaluation only, without external attacks.
  Evidence locations: Title and complete abstract

**2610.01560 · AURAL: Adaptive Latent Reasoning with Joint Chunk for Speech Language Models**

[Paper](https://arxiv.org/abs/2610.01560)

- **post-training**: AURAL models latent chunks jointly with diagonal plus low-rank GMM covariance, CSA, and differentiable two-pass scheduled sampling, then uses latent-coordinate-normalized ratios for GRPO. Preserve the full latent model when testing measured speech/text benchmarks and latency.

**2610.01537 · FedFit: Federated Fine-Tuning of LLMs via Vector-Bank Parameterization and Quantization**

[Paper](https://arxiv.org/abs/2610.01537)

- **foundation-model**: FedFit's disjoint dual banks, alternating federated aggregation, and low-bit communication are reproducible candidates, with formula ambiguities requiring review.
  Reproduction scope: RSC approximates in bank space, not original layer-space optimality. Dual residuals add cross terms, so do not claim exact SoP recovery. Eq. 29 writes Q(e), while adjacent text and Eq. 30 require Q(y+e); document erratum and test conservation first. The 90/10 evaluation split informed stopping and has no stated independent test; add isolated validation/test. Mostly one seed. Bytes are not wireless latency, and no author code found.
  Evidence locations: §III Eq3–8；§IV Eq10–22/Alg1；§V Eq23–31；§VII TablesI–XIII

**2610.01513 · Decision Titan: Test-Time Training for Long-Term Memory in Offline Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.01513)

- **foundation-model**: Decision Titan combines RTG/state/action Decision Transformer with Titans fast-weight memory, updated by trajectory chunk. Repeated-memory X-Maze tests length extrapolation.
  Reproduction scope: Reset memory each episode, retain chunk order and cross-chunk no-grad. Symbolic X-Maze is not physical navigation. The 1.7× training speed and 20× context depend on encoding assumptions.
  Evidence locations: §3.1–3.2; §4.1–4.4; §5
- **post-training**: Decision Titan adds TTT memory to Decision Transformer on X-Maze, not language-model post-training.

**2610.01508 · OverAct: Measuring and Mitigating Proactive Over-Authorization in LLM Tool-Calling Agents**

[Paper](https://arxiv.org/abs/2610.01508)

- **agent**: OverAct defines overreach against a conservative literal-minimal tool set, not universal authorization law. Eight domains and 48 tools, 240 doubly annotated originals expanded to 720 paraphrases, and set-based scoring without an LLM judge. SelfAudit requests grounded justification and then filters before execution without an oracle. Filtering drives most gains; justification alone worsens results. TCR .94→.89. The mechanism is a permission-filter candidate, but reported supplemental logs could not be located publicly, so the 720 items are not an integrated runnable benchmark.
  Evidence locations: Title and complete abstract

**2610.01506 · MCRI: A Four-Dimensional Framework for Analyzing and Evaluating Agent Skills**

[Paper](https://arxiv.org/abs/2610.01506)

- **agent**: MCRI grades Metadata, Constraints, Resources, and Instructions from 1–5 before task-conditioned aggregation, selecting skills by mean repeated score times mean confidence. Three public benchmarks include 50 subtasks, 345 Mind2Web steps, and 58,275 calls. Correlation/popularity is not causality or general quality. Appendix D's scorer is sufficient for a candidate filter, but Appendix F explicitly omits Resources and no public repository was found; do not claim complete experiment or data reproduction.
  Evidence locations: Title and complete abstract

**2610.01499 · VTR-Bench: A Systematic Benchmark for Evaluating Visual Text Rendering in Video Generation**

[Paper](https://arxiv.org/abs/2610.01499)

- **foundation-model**: VTR-Bench publishes 300 prompts and CoQ/carrier-transcription WER entry points for newly generated videos. Agentic keyframe generation is also researchable, but unmatched budget gains do not establish efficiency.
  Reproduction scope: Generated HF videos require private access; public prompts/checklists and code suffice for new runs. Fix coverage across all 300 rather than dropping missing IDs. Human ratings of 100 videos favor readable outputs from three models and do not generalize to failure distributions. Clearest-occurrence WER does not measure temporal consistency. Agentic budgets are larger; match them.
  Evidence locations: §3.1–3.4; §4.1–4.5; App C.2; official README Evaluation/Agentic Generation

**2610.01496 · SALD: Self-Referenced Advantage Learning for Diffusion Models**

[Paper](https://arxiv.org/abs/2610.01496)

- **foundation-model**: SALD compares a same-model easy-noise teacher without gradients and a hard-noise student, with batch-normalized differentiable advantage weights, sample EMA noise curriculum, and frequency discrepancy gates. Public diffusion data/checkpoints support actual training.
  Reproduction scope: Do not detach advantage or spatial weights arbitrarily. The loss remains weighted hard residual, not direct easy–hard distillation. Frequency gating is not per-pixel causal explanation; match costs of two forwards.
  Evidence locations: §2.1–2.5/Eq6–17; §3; Appendix D/E

**2610.01492 · Q-SPT: Learnable Query-Based Compression for Low-Frame-Rate Speech Tokenization**

[Paper](https://arxiv.org/abs/2610.01492)

- **foundation-model**: Q-SPT downsamples SenseVoice/DAC features using sliding-window query cross-attention, semantic FSQ plus conditioned acoustic RVQ, and joint spectral, adversarial, and text reconstruction training. Public LibriSpeech reconstruction, ASR, and TTS support verification.
  Reproduction scope: Text reconstruction exists only during training. Disclose altered baselines at different bitrates/strides. A toy quantizer does not establish ASR/TTS performance.
  Evidence locations: §2.1–2.2/Eq1–5; §3.1–3.3

**2610.01316 · What Wins a Vote? Formatting, Length, and Lexical Diversity in the French Compar:IA LLM Arena**

[Paper](https://arxiv.org/abs/2610.01316)

- **recommendation**: ComparIA preference-style effects are reviewed in the post-training track.
- **post-training**: Public preference analysis truncates dialogue at voting time and fits joint style/length/vocabulary Bradley–Terry with within-model controls. Official code and derived data are readable; original French ComparIA is gated. There are 137,293 decisive votes over 116 models and 127,092 complete cases. Adjusted rank is not proven closer to capability, and observational association does not establish style causality.

**2610.01286 · Dyna3: VLM-Guided Training-Free 4D Reconstruction via Depth Foundation Models**

[Paper](https://arxiv.org/abs/2610.01286)

- **foundation-model**: Dyna3 detects motion with best-match cross-frame DA3 feature similarity and uses Qwen2-VL/SAM3 semantic masks to separate static aggregation and per-frame dynamic point clouds. DAVIS/TUM/Sintel/DyCheck support checks.
  Reproduction scope: Do not replace real DA3/SAM3 with GT masks. Count all VLM, segmentation, and reconstruction costs. Check public checkpoint compatibility in practice.
  Evidence locations: §3.2–3.6/Eq2; §4.1–4.6; Appendix A

**2610.01278 · SCOPE-AD: Sequential cost-aware ordinal-belief planning with energy-based models for diagnostic agents**

[Paper](https://arxiv.org/abs/2610.01278)

- **post-training**: SCOPE-AD uses ordinal belief from observations and an offline soft Bellman EBM planning teacher, then distills with masked KL to Qwen. ADNI patient splits are 1,552/333/333; actual unobserved values are hidden. This is medical offline planning, not general OPD or clinical deployment.
- **agent**: SCOPE-AD uses ordinal belief from observations and an offline soft Bellman EBM planning teacher, then distills with masked KL to Qwen. ADNI patient splits are 1,552/333/333; actual unobserved values are hidden. This is medical offline planning, not general OPD or clinical deployment.
  Reproduction scope: This entry reuses the full-text review rather than a separate reread. Public artifact executability was not rechecked here. Acceptance means research candidate, not completed implementation.
  Evidence locations: §2.2–2.4 Eq.3–4；§3

**2610.01243 · When the Judge Acts: Auditing VLM-Guided Image Selection on Culturally Situated Prompts**

[Paper](https://arxiv.org/abs/2610.01243)

- **foundation-model**: JudgeActs freezes the CulturalFrames candidate pool and uses three cyclic order checks and a preset abstention gate, comparing against exact random expectation and a post hoc human oracle. It audits VLM selection reliability.
  Reproduction scope: Hide human ratings, authors, and country metadata from judges. Separate 300 main from 30 dev by prompt hash and bootstrap prompts, not calls. Three rotations are not all permutations; visual budgets and schemas differ by model. Report coverage with abstention. Public source code does not license underlying images for redistribution.
  Evidence locations: §3 measures；§4.1–4.5；§7

**2610.01238 · Mixture-Trained Merging for Unified Multi-Objective Models**

[Paper](https://arxiv.org/abs/2610.01238)

- **post-training**: MTM trains mixture-biased soft experts, chooses branch blends with multiobjective Bayesian optimization on the merge simplex, and reuses merged checkpoints iteratively. Real Qwen4B/OLMo7B multi-domain and thinking-mode experiments require validation selection and accounting for search training.

**2610.01192 · FlashBack: Knowing When to Remember in Streaming Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.01192)

- **foundation-model**: FlashBack separates native streaming state and a temporary Recall branch, routing by temporal evidence to historical retrieval/SideKV without writing Recall into native history. Public video benchmarks can test causal long-term memory.
  Reproduction scope: Author code is forthcoming. The memory bank may contain only observed prefixes, not full-video offline retrieval. Count temporary retrieval and inference.
  Evidence locations: §3.2–3.4; §4.1–4.4; §6

**2610.01172 · Learning Rate Transfer for Hybrid Transformer-SSM Architectures**

[Paper](https://arxiv.org/abs/2610.01172)

- **foundation-model**: Naive μP with AdamW transfers learning rates across widths in hybrid Transformer–SSM models, an executable parameterization/tuning recipe rather than a new guarantee.
  Reproduction scope: Zero gap on discrete LR grid is not continuous optimality. WT2 multi-epoch best train-loss LR 1.0 differs from validation 0.1, requiring local validation. The 24.9B-token run uses one LR and seed, not a full large sweep. Simplified Mamba ZOH at state 16 is not theoretical true ZOH with growing state. Failed coordinate checks do not establish universal sufficiency.
  Evidence locations: §3.1–3.4；§4.1–4.3；§5.1–5.4；Limitations/AppA.3

**2610.01128 · Grounding Large Language Models in DSGE Simulators for Policy Generation and Forecasting**

[Paper](https://arxiv.org/abs/2610.01128)

- **post-training**: The public DSGE language-agent environment offers deep cloned Snowdrop simulator state, action validation, rolling forecasts committing the first step only, and immutable history. Matched PPO/GRPO share initial conditions and shocks. The author repository is readable for domain simulations, not real policy advice or trading causality.

**2610.01127 · Counting and Min-Cost Encoding for Tokenization in Large Language Models**

[Paper](https://arxiv.org/abs/2610.01127)

- **foundation-model**: CNF–MCE builds a vocabulary from direct substring statistics and actual-use filtering, then globally segments with boundary-aware dynamic programming. This is a defined foundation tokenizer candidate.
  Reproduction scope: 8B mix250k and Qwen152k have different vocabularies and embedding size, so total parameters differ. Compression is not latency; account for tokenizer costs. Match training budget and character exposure, and do not assume ability after swapping existing LM segmentation. No public author code/vocabulary located. Preserve full Unicode units and DP costs rather than longest matching.
  Evidence locations: §3.1 Algorithms1/2；§3.2 Eq1–4；§4.1–4.6 Tables5–8；App B.1

**2610.01076 · GLoC-EHR: Evidence-Cited Clinical Reasoning over Global Context and Local EHR Events**

[Paper](https://arxiv.org/abs/2610.01076)

- **post-training**: GLoC-EHR adds global/local EHR memory interfaces, staged alignment, and evidence-only sufficiency loss. 128,350 patients use isolated 7:1:2 splits and external hospital evaluation. RL remains standard GRPO; admit the architecture and grounded training mechanism. Only teacher/scorer see gold.

**2610.01054 · Capturing In-Context Learning Dynamics with Task Operators**

[Paper](https://arxiv.org/abs/2610.01054)

- **foundation-model**: Task Operator extracts multiplicative softmax mass and additive context values by head and position from ICL forwards for demonstration-free replay. Analytic definitions, public code, answer-excluded validation, and isolated test make it a candidate.
  Reproduction scope: Generation is not GT. Remove test labels and preserve GPQA non-Diamond demonstrations and validation. Validation retains only non-budget-hit completions; report exclusions. A last-token bias cannot replace template mappings; multishot can be unstable. Count extraction and per-site checks; training-free is not cost-free.
  Evidence locations: §3 Eq1–7；§4.1/Table1；App B/C/E；official README

**2610.01037 · SLIM: Simplex-Lattice Interpolation Merging**

[Paper](https://arxiv.org/abs/2610.01037)

- **foundation-model**: SLIM fits merging performance with a minimal quadratic simplex lattice of expert vertices and pairwise midpoints, then optimizes predicted AVG under constraints. It compares to random design under 36 evaluations with held-out OOD.
  Reproduction scope: ID is not independent test. Gemma SLIM OOD 50.30 trails best lattice 51.85, while Llama 47.27 improves. A 120-evaluation cubic fit worsens OOD. Nonconcave quadratics have no global-optimum guarantee; 36 identifies the model and is not a universal lower bound for good merges.
  Evidence locations: §3.1–3.4 Eq1–8；§4.1/Table1；§5/Tables2–3；§6

**2610.01023 · Groundability, Not Scale Alone: When Weak Reviewers Can Audit Strong Coding Agents**

[Paper](https://arxiv.org/abs/2610.01023)

- **agent**: The reviewability framework distinguishes agent testimony, structured evidence, and independent grounded evidence. Freeze a cascade of empty-patch/new static-error checks, generated tests that must fail on base behavior, then 8B review with abstention. Official hidden tests are an upper bound, not deployable. After 32 Django design cases, test once on 121/122 GPT and 59 Gemini: risk .33/.26, over-rejection .66/.67. Generated passes are not proof. Admit independent verification and abstention, not reliable weak-to-strong review or net cost savings.
  Evidence locations: §3；§4；§6 Algorithm1/6.2；§7

**2610.01017 · Pay for the Fault, Not the Flow: Label-Free In-Flow Multi-Agent Workflow Optimization**

[Paper](https://arxiv.org/abs/2610.01017)

- **agent**: InFlowOp uses cost = −log rubric match to build workflows, splitting top-down and merging bottom-up. Declared input/output contracts detect decomposition or assignment errors; switch agents before local re-decomposition, rerun invalidated descendants, and cache others. Semantic matches are not an oracle despite no gold. Rollback non-regression assumes trusted checks and reversible effects. Braid has eight domains, with three closed-source systems on five. A tool-less single LLM that cannot read files is a weak baseline; same-turn-budget single-agent comparison is stronger. Profile-success filtering must avoid cross-test leakage.
  Evidence locations: §3.1–3.2 Eq3–8；§4；§5.1–5.3；AppendixD/E

**2610.00983 · The Devil Is in the Reconstruction Loss Scale: Rethinking Optimization in LLM Quantization**

[Paper](https://arxiv.org/abs/2610.00983)

- **foundation-model**: Replace PTQ reconstruction MSE with grouped RMSE, making output-gradient norm independent of nonzero error scale. Sample, channel, token, and element variants belong to one family and fit existing PTQ training comparisons.
  Reproduction scope: Token/channel defaults by model family were chosen from overall results, so add independent validation. Handle zero error numerically and verify gradients. Match hyperparameters, calibration, and precision budget. Fake-quantization gains are not actual inference speedups.
  Evidence locations: §3 Eq6–8；§4.1–4.3；Appendix A
- **post-training**: RMSE gradient normalization for PTQ reconstruction belongs to quantization optimization.

**2610.00981 · NarrativeFlow: Flow-Based Vision-Language-Action Model Using Robot Velocity Fields**

[Paper](https://arxiv.org/abs/2610.00981)

- **foundation-model**: NarrativeFlow uses two task tokens and narrative differential supervision to strengthen language-conditioned robot flow, a candidate algorithm.
  Reproduction scope: The core is flow, not an entirely new end-to-end VLA. Fixed camera and visible initial end effector require an existing flow control policy. Samples lacking original instructions get them from initial/final images; distinguish human natural instructions in tests. Goal and GT flow are training/oracle-only. A project page exists but author code was not verified. Measure teacher-forced-history to rollout shift.
  Evidence locations: §3.1–3.5 Eq1–5；§4.1；§5.1–5.2；App B/E

**2610.00979 · RISED: RubrIcs for agentic multi-environment Selection and sElf-Distillation**

[Paper](https://arxiv.org/abs/2610.00979)

- **agent**: RISED freezes a rubric vocabulary (82 across four environments, 59 in the main three), labels each rollout asynchronously with Qwen32B, and selects 64/128 groups using pooled MMR relevance minus redundancy under round-robin quotas. Positive and negative rubrics guide sampling; the teacher sees only the union of top three positive rubrics. k=3 OPD ratios combine with GRPO; negative rubrics steer. Qwen3/4B on three environments gains only +1.2/.6 pp against the strongest baseline. Half optimizer steps is not half total cost, and 62.9% zero-variance groups still carry OPD signal. Distillation removal also removes negative steering; disclose it.
  Evidence locations: §2.2/2.4；§3 Eq2；§4.1/4.3；§5

**2610.00977 · ABSENTIA: Detecting Broken Access Control Vulnerabilities in Web Applications**

[Paper](https://arxiv.org/abs/2610.00977)

- **agent**: ABSENTIA builds application profiles, unions patterns extracted by two LLMs into route graphs, declares invariants per route, checks enforcers and source-grounded counterexamples, and composes shared files across routes. Byte-identical dependency closures allow caching across commits. BAC30 covers disclosed bugs in 25 projects; advisories and fixes are oracle-only. Fixed negatives only rule out their matching bugs, not all repository issues. Independent human precision audit on 73 samples did not confirm LLM-judge gains. The static defensive audit is a candidate; forthcoming code is not released code.
  Evidence locations: §4.1–4.4；§5.1–5.2；§7；Code Availability

**2610.00952 · A Matched-Budget Audit Framework for Recaptioned Image-Text Supervision Distributions**

[Paper](https://arxiv.org/abs/2610.00952)

- **foundation-model**: Matched-Budget Recaption Audit compares caption coverage, prefix concentration, CBU density, and image-support risk on the same images and text budgets, as a pretraining-data diagnostic.
  Reproduction scope: Record different word-window and regex lexical units. Fixed Qwen CBU extraction and a Gemma judge are not fully independent, and human assessment covers 43 resolved claims. Caption audits do not establish better downstream T2I training. 490M captions do not confer image redistribution rights; training pipelines still need safety, PII, and deduplication checks.
  Evidence locations: §4.1–4.2；§5.2–5.4；§6–7

**2610.00899 · TOAST: Stochastic Robot Action Tokenization for Autoregressive Vision-Language-Action Models**

[Paper](https://arxiv.org/abs/2610.00899)

- **foundation-model**: TOAST's stochastic action-token supervision is a defined VLA training operator, suitable for matched public LIBERO verification.
  Reproduction scope: Not action-noise augmentation. Equal steps need not match target-token FLOPs; record lengths. Four real tasks average 50.8, +15.8 versus deterministic, which does not generalize to open tasks. Count retries after discarding invalid token chunks. The project mentions code but this review found no public author repository; OpenPI is only the base.
  Evidence locations: §IV; §V-A–D Tables III/V; official project page

**2610.00885 · FORALL-LEAN-AGENT for Auditable Reasoning in Formal Mathematics and Software Verification**

[Paper](https://arxiv.org/abs/2610.00885)

- **agent**: Forall-Lean-Agent isolates actor and fresh read-only reviewer and requires two approvals of the same digest. Use proof-body-free retrieval, OS process-tree sandbox, provider-only proxy, and syntax/name-shadow/axiom audit, then clean serial verification. 100 VSB and 672 Putnam plus two LeanEval sets. Benchmark, strict, and independent-kernel denominators differ. Legacy reference leakage and file drift exclusions do not establish capability. Cost, compile, and review budgets differ; do not attribute harness gain to one component.
  Evidence locations: §3.1–3.6；§4；§5.3；§6

**2610.00878 · UniTrackPLA: Unified Panorama-Language-Action Model for Instruction-Guided Navigation and Dynamic Person Tracking**

[Paper](https://arxiv.org/abs/2610.00878)

- **foundation-model**: UniTrackPLA maps DINOv2/SigLIP panoramic multiview input with time/heading encodings to waypoints. WAC predicts post-action latents and uses observed error to replan. OmniTrack/OmniVLN support route-isolated verification.
  Reproduction scope: Verify dataset downloads and training checkpoints before implementation. EP@0.2 is not success rate. Actual Go2-W hardware results cannot replace local tests.
  Evidence locations: §III; §IV; Tables I–III

**2610.00864 · Kinematic MeanFlow: One-Step Action Generation Policy for Robotic Foundation Models**

[Paper](https://arxiv.org/abs/2610.00864)

- **foundation-model**: K-MF splits the MeanFlow time derivative into two interval JVPs, defining a trainable one-step action generator.
  Reproduction scope: Two JVPs add up to 33% training time; one inference step is not free training. H20 training and L40/Orin latency do not replace A100. The paper promises code; a main README 404 does not prove the repository absent, so release remains unverified. Euler one-step cannot replace the defining loss, and full-body/dexterous hands are out of scope.
  Evidence locations: §3.2 Eq5–9；§4.1–4.5；App C/E；Limitations/Reproducibility

**2610.00779 · Effective Synthetic Data Curation Requires Group-Level Signals**

[Paper](https://arxiv.org/abs/2610.00779)

- **post-training**: Group-level influence measures downstream training utility, using within-group gradient diversity to allocate expensive group-oracle calls and individual proxies for unaudited groups. Actual pretraining/RLVR ran; isolate references and test.

**2610.00767 · Pre-training interventions, ex post facto: Grafting model beliefs across checkpoints**

[Paper](https://arxiv.org/abs/2610.00767)

- **post-training**: Learn a synthetic-document delta in a base checkpoint and add it to the post-trained model to reduce reality drift. Multiple models up to 284B were tested. This differs from prior GRAFT trajectory exchange.

**2610.00717 · Sequential Functional Structured Tucker Compression for Large Language Model Attentions**

[Paper](https://arxiv.org/abs/2610.00717)

- **foundation-model**: FTC measures actual sequential student activations, jointly budgets shared QKV Tucker and sparse core bytes, and separately calibrates WO against a teacher map. Same-metric SeqSVD and equal-storage core ablations make it a compression candidate.
  Reproduction scope: The main method uses 256 calibration windows versus 128 for baselines. Under strong compression with 128 windows, Qwen2.5-7B PPL goes 12.55→43.90, so gains are not all equal-data. Actual 2:4 core strong-compression PPL is 58.50; unstructured sparsity is not GPU acceleration. Author code was not verified.
  Evidence locations: §3.1–3.5 Eq1–4；§4.1–4.3 Tables1–3；Appendix A.4 Tables17–18
- **post-training**: FTC sequential Tucker attention compression uses no RL/OPD. Route to the foundation track rather than reject globally.

**2610.00710 · ReLiveGym: Evaluating Long-Lived Agents over Weeks of Replayed Reality**

[Paper](https://arxiv.org/abs/2610.00710)

- **agent**: ReLiveGym replays weeks of real streams over eight tasks. Clock advances only on wait and does not simulate LLM latency; observations are timestamp-isolated. Deterministic timed-commit scores and a hard-cost wallet accompany sleep/watcher/cron, daily hindsight memory, and BoN pruning. BoN selects the next day from settled past feedback, not future gold, and some tasks benefit, not all. Public code, eight scorers, and config omit data; DATA gives public reconstruction, while bundle links are placeholders. Roughly 33 GB needed; temporal inference has errors; Linux bans shell without an OS fence.
  Evidence locations: §3.1–3.3; §4.1–4.2; §5.3; official README and DATA.md

**2610.00675 · LabBook: Harnessing Experimental History for Efficient LLM-Driven Discovery**

[Paper](https://arxiv.org/abs/2610.00675)

- **agent**: LabBook maintains free-text semantic memory and lossless experiment logs. Latest code/result plus best and stagnation details enter context automatically. Agents have up to five read-only History/Code/Result calls and emit complete new programs and memory without a forced best parent. 49 FrontierCS and nine public tasks use shared model, prompt, and evaluator; ablations remove memory/retrieval or use full history/top-score retrieval. Per-task best normalization is aggregation only; choose candidates on separate validation. Code is promised, but the mechanism is defined enough to consider.
  Evidence locations: §3.1–3.3 Eq1–3；§4.1–4.4；Code availability

**2610.00666 · VisionQ: VLM-as-a-Judge Taxonomy, Dataset and Benchmark for Qualitative Analysis in Computer Vision**

[Paper](https://arxiv.org/abs/2610.00666)

- **foundation-model**: VisionQ provides new VLM-judge benchmark execution and DPO code for auditing agreement with author claims, not objective visual quality or automated peer review.
  Reproduction scope: Ground truth is the author's claimed winner without independent human validation. Overall gain 95% CI is [−1.9,+7.0], with the clearest effect on position bias. Position swapping and symmetry are not independently attributed. Select checkpoint 900 on separate validation. Figure crops are noncommercial; public-source contamination is not ruled out.
  Evidence locations: §3.2–3.4; §4; §5.1–5.4; §6; official README Benchmark/Judge

**2610.00663 · Backdoor Containment via Expert Quarantine and Shutdown in LLMs**

[Paper](https://arxiv.org/abs/2610.00663)

- **foundation-model**: QES uses attention-based soft trigger localization, sample peakiness modulation, and four routing constraints to train expert LoRA and disable isolated experts. It needs no gold trigger and was run on multiple models, two tasks, and three attacks.
  Reproduction scope: Independent review of §4–6 and Appendix D found failures on Sleeper numeric triggers, rare VPI tokens under GQA, and adaptive/syntactically hidden triggers. Attention localization is not a reliable oracle. §5 defaults are from single-cell ablation and need independent validation.
  Evidence locations: Abstract (full abstract reviewed item by item); §4.1–4.2 Eq.1–8; §5
- **post-training**: QES uses attention-based soft trigger localization, sample peakiness modulation, and four routing constraints to train expert LoRA and disable isolated experts. It needs no gold trigger and was run on multiple models, two tasks, and three attacks.

**2610.00661 · Exploring More, Reasoning Better: Stepwise Risk-Sensitive GRPO for Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.00661)

- **post-training**: StepRS-GRPO changes risk coefficients and transforms group advantages by denoising maskedness, preserving the original diffusion trainer. With binary reward this is state/problem reweighting only. Actual SDAR1.7/4B training has mass and RMS controls.

**2610.00651 · Agent Evaluation Reliability: More Tasks Won't (Always) Fix An Agent Leaderboard**

[Paper](https://arxiv.org/abs/2610.00651)

- **agent**: Bayesian crossed Bernoulli-logit variance decomposition distinguishes models from deployed model–scaffold pairs. Residual π²/3 cannot be split further because single cells have insufficient repeats. On 29,923 HAL outcomes, 54 models, and 13 scaffolds, D-study posterior propagation shows that adding tasks does not remove model×scaffold or benchmark variance. Breadth conclusions assume balanced exchangeability and setup costs, not arbitrary new tasks. Official MIT R/Stan tests and outcomes are public. Dollar costs are assumed prices, not measured. This supports evaluation reliability and budget analysis.
  Evidence locations: §3.1–3.5 Eq. 2/8/9; §4; §5.3; official README

**2610.00648 · Incident-Arena: Getting agents to the last nine of reliability**

[Paper](https://arxiv.org/abs/2610.00648)

- **agent**: IncidentArena has 20 Kubernetes incidents on three substrates, with hidden deterministic outcome SLI, restart/reattack gates, frozen healthy thresholds, and oracle/no-op plus adversarial QA. Native harness ran 3,000 trials. Thirteen Slack incidents produce uneven coverage and reasoning comparisons have wide intervals. A post hoc reward-hack judge is not the hidden scorer. Apache 2 tasks and Harbor fork are public; Linux Docker needs 8 CPU, 16 GB, and 40–77 GB. Isolate clusters and secrets, never run against production authority.
  Evidence locations: §3.1–3.4; §4; §5.3–5.4; §6; official README

**2610.00613 · Spatial Strategies, Not Actions: Vector-Quantized Geodesics as Tools for LLM-Driven Agents**

[Paper](https://arxiv.org/abs/2610.00613)

- **agent**: Compress 250 offline geodesic five-step fragments to five prototypes via origin normalization and VQ/K-medoids, adding five primitives and wait. The LLM describes once and chooses only five-step open-loop actions; optional collision filtering uses observed obstacles only. One QwenVL grid world does not establish high-dimensional generalization. Dynamic skill addition by signed measure is untested. Keep actual geodesic sampling and VQ rather than hand-written skills.
  Evidence locations: §4.1–4.4；§5/Table1；§6

**2610.00604 · MIKASA-Robo-VLA: Benchmarking Memory in VLA Models for Long-Horizon Manipulation**

[Paper](https://arxiv.org/abs/2610.00604)

- **foundation-model**: MIKASA-Robo-VLA offers 90 ManiSkill3 tasks, two RGB views and unified 7D state/action, success_once, and 22,500 demos, enabling executable VLA memory evaluation.
  Reproduction scope: Oracle demonstration success of 1.0 follows filtering, not raw success. Privileged simulator state is teacher/evaluator-only. LeRobot lacks per-step reward and formats do not share episode IDs, so do not join by index. The baseline uses 14 tasks, one checkpoint, and no history, not causal evidence about memory. Task gaps are not fully factorial and physical transfer is untested.
  Evidence locations: §3.1/3.4–3.6；§4.1–4.2；§6；Appendix D

**2610.00574 · Make Sparse Rewards Count: Density-Aware Reward Aggregation for Multi-Reward RL**

[Paper](https://arxiv.org/abs/2610.00574)

- **post-training**: DARA weights active groups per reward by capped sqrt(max-density/density), while Asym amplifies only positive advantages before batch normalization. Actual ToolRL/BFCL-v4 and math training was run.

**2610.00573 · FORTE: Adaptive Scoring and Exact Keyframe Selection for Long-Video Question Answering**

[Paper](https://arxiv.org/abs/2610.00573)

- **foundation-model**: FORTE uses banded RBF-GP to estimate frame relevance and temporal-coverage marginal gains within a scoring budget. Exact O(KN) upper-envelope dynamic programming selects 64 frames. Public long-video QA supports checks.
  Reproduction scope: Author code is promised only after publication. Count GP scoring and encoding in the budget. There is no end-to-end speed gain evidence over uniform sampling. Do not choose parameters on test benchmarks.
  Evidence locations: §3.2–3.3; §4.1–4.4; Appendix C/D

**2610.00568 · Emergent Unfaithfulness: How Alignment Training Causes Language Models to Silently Override Task Faithfulness**

[Paper](https://arxiv.org/abs/2610.00568)

- **post-training**: FaithConflict publishes 940 confirming/conflicting document pairs, FaithGap, and a judge with eight behavior and seven reasoning categories, across 22 checkpoints and prompt conditions. Official code/data are readable. Separate task faithfulness and factual correctness; parroting harmful fictional documents is not safety improvement.

**2610.00559 · PhysVista: Benchmarking Physical Intelligence in VLMs via a Perception-Reasoning-Assessment Loop**

[Paper](https://arxiv.org/abs/2610.00559)

- **foundation-model**: PhysVista uses public video frames and questions for perception, causal, and physics tasks, adding public physical-VLM infrastructure.
  Reproduction scope: Outcome uncertainty is always correctly answered Indeterminate and shortcut-prone. Real scenes always score five, exposing real/generated domain cues. Human counterfactual labels are not physical simulator gold. README's generic accuracy conflicts with localization IoU in the paper; verify and retain localization rather than claiming a full harness.
  Evidence locations: §3.2–3.4; §4.1–4.5; official README Data Loading/Model Input

**2610.00541 · Random Recursive Models**

[Paper](https://arxiv.org/abs/2610.00541)

- **foundation-model**: RRM uniformly samples reusable layers with replacement at each step per example in actual stochastic recurrent training. TRM+RRM holds TRM fixed except layer ordering, providing a core control for small recurrent architecture research rather than established large-model ability.
  Reproduction scope: Three seeds mainly vary inference randomness at fixed checkpoints, not independent training. Greater depth can plateau or degrade CIFAR/Zebra; preserve deep supervision. PTRM100 trajectories use a fixed 1,000-item subset and are not single-sample capability.
  Evidence locations: §3 Eq4–6；§4；§5.1–5.5 Tables1–6

**2610.00499 · Denoising Surface: Modeling and Predicting Inference Cost for Diffusion LLM Serving**

[Paper](https://arxiv.org/abs/2610.00499)

- **foundation-model**: DWS separates diffusion decoding load into block survival and conditional denoise-step survival. Two-stage multiscale/Brier MiniLM supervision and CPU INT8 predictions drive SJF with hardware cost profiles.
  Reproduction scope: 100k training includes 10k validation, plus a separate 10k test. Keep actual cost-model testing on GT trajectories separate from prompt prediction. New model families, block sizes, or thresholds require retraining. Batch-96 SGLang measurements do not guarantee other engines. Retain aging with a 10% discount after 30 seconds waiting.
  Evidence locations: §4 Eq6–8；§5 limitations；§6.1–6.4

**2610.00497 · Gumbel Straight Flow: Distilling Autoregressive Models into One-step Flow Maps**

[Paper](https://arxiv.org/abs/2610.00497)

- **foundation-model**: Google DeepMind Amsterdam contributes to GSF: straight paths from AR Gumbel coupling, monotone Gaussianization, and diagonal-teacher/semigroup self-consistent flow-map loss. The paper includes architecture- and iteration-matched FMLM-re and a teacher-forced posterior-Gumbel training algorithm.
  Reproduction scope: Straight optimal paths assume enough capacity, and the actual student trails its AR teacher. Four-step D-MMD is better but nearly twice the size. Most external baselines are cited. Tune temperature on independent validation rather than test maxima and count teacher cost.
  Evidence locations: §3.1–3.2 Eq6–8；§4.1–4.3 Tables2/6–8；Appendix C Algorithms1–2；Appendix D–E

**2610.00487 · ScaffoldM3C: A Multimodal Sequential Monte Carlo Framework for Generative Stable Construction Planning**

[Paper](https://arxiv.org/abs/2610.00487)

- **foundation-model**: ScaffoldM3C conditions Gemma to generate bricks using position, category, and candidate-likelihood heads. SMC penalizes collision-repair displacement, reweights samples, and selects the longest stable sequence. StableText2Brick provides reconstructable supervision.
  Reproduction scope: Check support stability after every step, not only the end. SMC uses a model-candidate posterior, not target sequences. Real xArm need not be claimed for simulation. Release of the in-house 13-condition sequences is unverified.
  Evidence locations: §III-C/Algorithm1; §IV/Eq6–7; §V; §VI–VIII; Appendix A

**2610.00435 · How AI Agents Discover Scientific Equations: From Hydrotope Rediscovery to New Water-Wave Amplitudes**

[Paper](https://arxiv.org/abs/2610.00435)

- **agent**: PI splits analytic and numerical exploration between two students with shared records and independent BG recursive counterexample searches, reconstructing a global amplitude formula across frequency chambers.
  Reproduction scope: Teams use more compute than one agent. Two team successes are not a population success rate; 140 exact tests are not whole-domain analytic proof. Official formulas and test answers remain final-verification only. Redesign model selection from the fixed SR split using independent validation.
  Evidence locations: §3.1–3.2、§5.1–5.4、Appendix C/E

**2610.00432 · XOR-Trellis: Ultra-Low-Complexity Dequantization and Curvature-Aware Hadamard-Free LLM Quantization**

[Paper](https://arxiv.org/abs/2610.00432)

- **foundation-model**: XOR-Trellis uses 16-bit state and two branch bits per step to create a four-value FP4 palette. LDLQ objective adjustment and D-weighted Viterbi preserve curvature without Hadamard rotation.
  Reproduction scope: 384 RedPajama examples, seed 0, no tuning. Effective 2.25 bpw includes group-of-32 scales. Implement state/bitstreams rather than independent rounding. Simpler instruction decoding is not end-to-end CUDA speed, and A100 simulation cannot establish native FP4 benefit.
  Evidence locations: §3 FP4 palettes；§4.2–4.3；§5/Table1–3；Appendix D

**2610.00431 · ChainLoRA: Geometry-Preserving Task Vector Merging for Continual Learning in LLMs**

[Paper](https://arxiv.org/abs/2610.00431)

- **post-training**: ChainLoRA initializes QR carrier chains with one-sided geometric regularization, then archives, finds common carriers by SVD, aligns by Procrustes, and merges shared/residual parts. Three real continual-learning datasets were tested.

**2610.00400 · Representation Transitions Reveal Emerging Safety Risks in Multi-Turn LLM Agents**

[Paper](https://arxiv.org/abs/2610.00400)

- **agent**: DART builds harmful-minus-benign mean transition directions, removes benign mean and principal covariance directions, accumulates projections at segment boundaries, and after threshold identifies the largest segment contribution and regenerates with a reminder.
  Reproduction scope: Select layers/ranks on inner validation and thresholds on benign calibration. Use real hidden-state transitions. ASR/Utility measure final refusal proxies, not harmful tool success. Even perfect detection leaves 25% success, exposing reminder failures. Directions are model-specific.
  Evidence locations: §3–5、Algorithm 1、Appendix A/F/G

**2610.00399 · Metacognitive Reasoning in Energy Based Models using Instance Based Learning Theory**

[Paper](https://arxiv.org/abs/2610.00399)

- **foundation-model**: MERITED uses a 191M EBT energy distribution and question-embedding experience similarity to choose MCMC depth or stepwise stopping. Twenty training-memory items form state/action returns, supporting a dynamic-compute diagnostic.
  Reproduction scope: The paper chose among 450 configurations on the evaluation data with one actual split/seed. Error bars reflect variation across two tasks, not ten independent runs. OpenBookQA uses train. Optimal-stop timing cached test trajectory energies and omits state acquisition. Use live state and separate validation/test before claiming efficiency or generalization; retain paper-protocol replay as diagnostic.
  Evidence locations: Algorithm2–3；Tasks and Data Splits；IBL State, Memory, and Depth Control Eq7–8；Metrics, Timing, and Statistical Analysis

**2610.00385 · FAER: Auditable Utility-Aligned Trajectory Replay for Language Model Post-Training**

[Paper](https://arxiv.org/abs/2610.00385)

- **post-training**: FAER-UTILITY fits gradient alignment and metadata replay weights on non-target calibration blocks, samples without replacement, and joins correctness only after freezing traces. Completed learner results use normalized alignment. Optimizer-aware virtual steps are extensions or diagnostics, not validated learner behavior.

**2610.00372 · When Harnesses Lose the Signal: Causal Evaluation of Recovery in LLM Agents**

[Paper](https://arxiv.org/abs/2610.00372)

- **agent**: CIR pairs replay with and without refresh from the same environment state, distinguishing rescue from harm. Three logistic models predict anomalies and the two successes; choose out-of-fold thresholds under clean-harm constraints and refresh at most once over time.
  Reproduction scope: Separate 93 fitting tasks and 75 prefix-feasible test tasks. A success-filtered cohort does not represent all ALFWorld. Multiplying marginal probabilities provides rescue/harm scores, not joint causal probabilities. The 25% intervention point on recorded factual traces is an evaluation design; online control cannot see the future.
  Evidence locations: §3–5、Eq.1–7、§5.1

**2610.00354 · Proof-Gated Signing: Solver-Checked Transaction Guards that Hold Under State Drift for Onchain AI Agents**

[Paper](https://arxiv.org/abs/2610.00354)

- **agent**: Proof-Gated Signing simulates transactions to extract asset changes, verifies policy across price intervals with Z3, and compiles balance, recipient, allowance, and owner postconditions. Atomic wallet execution and rollback prevent check-to-inclusion drift.
  Reproduction scope: Guarantees depend on guard-held keys, honest tracked tokens, price bands, and policy. Untracked assets and off-chain permits are out of scope. 260 same-source scripted designs are not held out. Nine in-policy slow losses only bound session losses, not prevent them. Run an actual local chain rather than return ALLOW.
  Evidence locations: §2 Theorem/Table1、Algorithm1、§3–4

**2610.00313 · Rules to Tools: Executable Checks for LLM Agents in Scientific Computing**

[Paper](https://arxiv.org/abs/2610.00313)

- **agent**: Rules to Tools compiles public physical equations, boundaries, and output constraints into callable checkers. Repairs get actual artifact residuals and an independent hidden grader evaluates final outcomes. Match written rules, probes, and budget between text/tool arms.
  Reproduction scope: The prepared checker measures a support-package treatment, not a causal effect of tool format alone. Eight-task difference CI is [−12.5,43.75] pp. Flow point values in text and grid L2 gates in tools differ. Separate development-exposed and held-out tasks. Keep hidden arrays and grader code out of repair containers.
  Evidence locations: §3–5、Eq.1–3、Appendix B/C/D/G

**2610.00251 · The Null Is the Hard Part: Exact Tests for Memorization in Generative Models**

[Paper](https://arxiv.org/abs/2610.00251)

- **recommendation**: Exact null hypotheses and multiple-testing corrections for generative-model memorization are routed to foundation/multimodal evaluation.
- **foundation-model**: Model-level randomized label permutation and image-level matched conformal/BH controls can extend generative memorization evaluation. Public code includes actual test entry points and outputs. Candidate evaluation only, not an executed test or proof of no memorization.
  Reproduction scope: Stable Diffusion lacks randomized training/holdout splits, so exchangeability is assumed. Near-duplicate scales do not cover semantic copying. Model-level PCA/Alpha is limited to 2,000 images. Losing certification is not removing memorization.
  Evidence locations: §2 Propositions1–3；§3/Table1–2；§4–6；Reproducibility statement；official README experiments/genmem.py and genmem_sscd.py

**2610.00204 · Query Independent Variable Rate Visual Token Coding**

[Paper](https://arxiv.org/abs/2610.00204)

- **foundation-model**: RDTok uses query-independent PCA to construct token-level quantization rate–distortion curves and integer dynamic programming to allocate a total bit budget. Public ChartQA/COCO images and frozen VLMs can test compression.
  Reproduction scope: Token count stays fixed. Use actual bit-packing and count transform metadata; FP16 tensors do not establish compression. Fit PCA on training only, and do not use queries for allocation.
  Evidence locations: §2.1–2.3/Eq4–5; §3.1–3.4

**2610.00182 · Localizing Post-Wire Semantic Changes in MCP Agent Frameworks**

[Paper](https://arxiv.org/abs/2610.00182)

- **agent**: MCP post-wire differential tests use allowlisted projection to retain semantic atoms and compartments, separately checking protocol validity, typed semantic retention, and consumer-specific access along each framework's public carrier boundaries.
  Reproduction scope: 324 captures and three fresh processes test deterministic stability, not model quality. H4 is local provider request only, without remote calls. New 2026-07-28 protocol was not tested. The v4 package reconstructs normalized captures rather than rerunning frameworks. Keep missing separate from null and text recovery separate from structured slots.
  Evidence locations: §III method、§IV evaluation、Ethics/Reproducibility

**2610.00097 · DramaAgent: Agentic Storytelling Video Generation**

[Paper](https://arxiv.org/abs/2610.00097)

- **foundation-model**: DramaAgent's hierarchical long-story video control and repair is reviewed in the Agent track.
- **agent**: DramaAgent uses hierarchical storyboards, fixed character references, and scene-level video/audio candidates. Weighted identity, semantics, timing, and audiovisual scores identify the weakest axis for rewrite and bounded regeneration.
  Reproduction scope: Real video/audio generation is defining; text fixtures cannot reproduce it. Freeze and select τ=.8, epsilon=.02, R=2, and K budget on validation. Match APIs/backbones, candidate counts, and retry cost. Separate VLM scores from human preferences; audiovisual compatibility is not strict lip sync.
  Evidence locations: §3.1–3.5、Eq.1–9、Appendix B/D

**2610.00040 · DSSR-3D: Decoupled Reasoning for View-Dependent Referring in 3D Gaussians**

[Paper](https://arxiv.org/abs/2610.00040)

- **foundation-model**: DSSR-3D uses FLAN-T5 to parse target, direction, and anchor, locates anchors with semantic Gaussian softmax, and fuses target scores with local directional decay in the camera XZ plane. Public Ref-LERF scenes support tests.
  Reproduction scope: Limited to near-horizontal views and one anchor. The semantic field is pretrained, so not wholly training-free. ViewRef-GS GT uses GroundingSAM; avoid same-source evaluation leakage. Verify release of in-house scenes separately.
  Evidence locations: §3.2–3.6; §4.1–4.2; §5.2–5.3; §6

**2610.00025 · Measuring the Microtask Eligibility Gap: When Is an Off-the-Shelf SLM Enough for an Agent Harness?**

[Paper](https://arxiv.org/abs/2610.00025)

- **agent**: Four microtasks predefine quality thresholds and confidence intervals against non-LLM baselines to determine SLM eligibility. Select log-probability operating points on calibration, with memory BM25 shortlist and SLM reranking plus tool-baseline gating.
  Reproduction scope: 0/16 applies to fixed prompts and models, not all SLMs. Test oracle is an upper bound only. Quantized T2/T4 materials cannot reconstruct full ranking and selection, so they are diagnostic. Thresholds reflect one deployer's preferences, and eligibility excludes actual cost.
  Evidence locations: §3–7、Table1–2、Appendix G–I

**2610.00012 · When Do Causal World Models Help Modular LLM Agents**

[Paper](https://arxiv.org/abs/2610.00012)

- **agent**: FedCausalCompose's local intervention-response matching, edge discovery, and composition constraints are agent world-model diagnostics. Actual implementations must learn edges rather than use oracle edges.
  Reproduction scope: This is a centralized trace harness, not deployed federated privacy. Manual modules and oracle assumptions are strong. ALFWorld is nonmonotonic over correct-edge proportions at 30/45/20/35/40, with some partition drops of 25 pp. Mostly one seed, no AndroidWorld run.
  Evidence locations: §4; §5/Table1; §6–7; official repository README

**2610.00010 · Heavy-Tailed Memory Traces in Long-Horizon Language Agents**

[Paper](https://arxiv.org/abs/2610.00010)

- **agent**: CTWM uses access-rank power-law budgets for core and tail memory, an executable compression candidate. Token savings near zero task success are not capability gains.
  Reproduction scope: The compact graph baseline uses 156.4 tokens versus CTWM's 160.7 but makes more errors. Both ALFWorld one-shot scores are 0/18; three-shot graph 1/18 and CTWM 0/18; of 77 LongMemEval cases CTWM gets zero and graph gets three correct. Saving 24.48% of tokens does not improve ability. τ=1 is hand-selected. Do not promote in Evolve from this diagnostic.
  Evidence locations: §4; §5.4–5.7 Tables3–5; Appendix A.1/B; official repository README

**2602.16490 · From Growing to Looping: A Unified View of Iterative Computation in LLMs**

[Paper](https://arxiv.org/abs/2602.16490)

- **foundation-model**: A historical Google collaboration was missed: grow-first/loop-later plus middle-block recurrence has actual SmolLM training, 22 public tasks, and parameter, training, and inference budget controls. It is a recurrent-model candidate, not a new October paper.
  Reproduction scope: 2× applies only to some reasoning primitives. Extra loops add inference compute, and language/knowledge tasks can degrade. Block and math-source choices used downstream benchmark ablations; add independent validation. No author code links found in official text or Google page.
  Evidence locations: §3.1–3.2/Table1；§5.1–5.3/Table2/Table3；Appendix A；Appendix C.3/Figure17；Appendix D–E

**2510.15831 · VISTA: A Test-Time Self-Improving Video Generation Agent**

[Paper](https://arxiv.org/abs/2510.15831)

- **agent**: High-priority historical Google find: structured prompt planning, bidirectional tournament champion retention, normal/adversarial/meta critique, and DTPA revision with actual regeneration and reselection form an executable agent loop rather than a video-backbone innovation.
  Reproduction scope: First released 2025-10-17, not a 2026 new paper. Official project provides demos/prompts and paper only, with no author source located. Internal 161 prompts are unavailable. Roughly .7M tokens per round excludes video generation. Real multimodal judges and video generation are required, not fixed video scores.
  Evidence locations: §2.1–2.2/Algorithms1–2/Eq1–3; §4.1/Table2 text; §4.2; §4.3/Tables3–4; Limitations; official project


## Already recorded (48)

**2610.03702 · LESSER: Post-Training Data Selection with Output-Layer Gradients**

[Paper](https://arxiv.org/abs/2610.03702)

- **post-training**: The ledger already implements LESSER as an L1 output-layer gradient/selection diagnostic, not an LLM training benchmark.

**2610.03675 · FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution**

[Paper](https://arxiv.org/abs/2610.03675)

- **agent**: FrugalEvo already exists. This abstract agrees with the earlier full-text/code review; no duplicate implementation entry.
  Evidence locations: Title and complete abstract

**2610.03665 · Pivot-SD: Efficient Self-Distillation for Masked Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.03665)

- **post-training**: The ledger reviewed the full text of Pivot-SD, but real diffusion trajectory training is not implemented. Keep its prior unresolved status.

**2610.03634 · Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents**

[Paper](https://arxiv.org/abs/2610.03634)

- **agent**: DepGPO command-dependency graph credit assignment is already cataloged; no duplicate.
  Evidence locations: Title and complete abstract

**2610.03515 · Learning from Repaired Reasoning: Root-Cause-Guided On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.03515)

- **post-training**: The ledger reviewed RC-OPD and the authors' evaluation repository. Real repair continuations and training remain unimplemented.

**2610.03361 · Follow the Winners: Conservative Policy Improvement with the Cross-Entropy Method for Critic-Free RFT**

[Paper](https://arxiv.org/abs/2610.03361)

- **post-training**: FTW is implemented as an L1 CPU FIFO/top-K/KL diagnostic, without Search-R1 or Sokoban training evidence.
- **agent**: FTW already covers a critic-free cross-entropy replay ordinal filter.
  Evidence locations: Title and complete abstract

**2610.03223 · AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.03223)

- **post-training**: AdaStep is implemented as an L1 synthetic-return variance operator, not agent policy training.
- **agent**: AdaStep already covers step-credit signals and variance shrinkage.
  Evidence locations: Title and complete abstract

**2610.02994 · Sentry: Learning to Recover from LLM Agent Failures at Test Time**

[Paper](https://arxiv.org/abs/2610.02994)

- **agent**: Sentry is already cataloged after full-text and repository review; reward-blind recovery is not duplicated.
  Evidence locations: Title and complete abstract

**2610.02199 · TACO: Ternary Absolute-max Column-wise One-sparse Optimizer for LLM Fine-Tuning**

[Paper](https://arxiv.org/abs/2610.02199)

- **foundation-model**: The ledger already lists taco-optimizer; keep its conclusion.

**2610.02163 · AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents**

[Paper](https://arxiv.org/abs/2610.02163)

- **foundation-model**: The ledger already lists autocompact; keep its conclusion.
- **post-training**: AutoCompact is already cataloged under agents; avoid duplicate cross-track implementation.

**2610.02148 · Omni-Embed-Mini: Binding Modalities Without Forgetting via Dense Distillation**

[Paper](https://arxiv.org/abs/2610.02148)

- **foundation-model**: The ledger already lists omni-embed-mini; keep its conclusion.

**2610.02117 · Where-OPD: Spatially Guided On-Policy Self-Distillation of MLLMs with Synthetic Scenes**

[Paper](https://arxiv.org/abs/2610.02117)

- **foundation-model**: The ledger already lists where-opd; keep its conclusion.
- **post-training**: Where-OPD is implemented; preserve the prior conclusion about privileged spatial guidance from synthetic scenes.

**2610.02076 · LLM-as-Jev: LLMs Are Already Jev-Style Decision Models -- When and How to Fine-Tune Them**

[Paper](https://arxiv.org/abs/2610.02076)

- **foundation-model**: The ledger already lists llm2jev; keep its conclusion.

**2610.02057 · Optimizing Effective Training Time for Large-Scale Recommendation Systems**

[Paper](https://arxiv.org/abs/2610.02057)

- **recommendation**: ETT is implemented in the shared manifest, not a new entry.

**2610.02039 · CARM: Cancellation-Aware Response Masking for LLM Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.02039)

- **post-training**: CARM token-level absolute log-ratio response masking is implemented in the ledger.

**2610.02002 · Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents**

[Paper](https://arxiv.org/abs/2610.02002)

- **foundation-model**: The ledger already lists mem-plus-plus; keep its conclusion.
- **agent**: Mem++ already covers whole-document time filtering and read-time lexical/semantic fusion.
  Evidence locations: Title and complete abstract

**2610.01973 · Token-Level Video Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.01973)

- **foundation-model**: The ledger already lists tvrl; keep its conclusion.

**2610.01896 · Asynchronous LLM Post-Training: Group-Mass Capping and Convergence Analysis**

[Paper](https://arxiv.org/abs/2610.01896)

- **post-training**: GMC-GRPO is implemented with mass capping on asynchronous group importance weights.

**2610.01785 · VETO: Video Efficient Token Optimization for Vision Language Models**

[Paper](https://arxiv.org/abs/2610.01785)

- **foundation-model**: The ledger already lists veto; keep its conclusion.

**2610.01705 · AgentWebRec: Compact Evidence Fusion over the Agent Web for Personalized Recommendation**

[Paper](https://arxiv.org/abs/2610.01705)

- **recommendation**: AgentWebRec is implemented. Verified registration only; not a new addition.

**2610.01548 · Range-GRPO: Policy Optimization via Pairwise Relations among Reward Intervals**

[Paper](https://arxiv.org/abs/2610.01548)

- **post-training**: Range-GRPO is implemented; conformal reward-interval pairwise relations estimate advantage.

**2610.01533 · Neither Black nor White: Balancing Semantic and Collaborative Signals with Graph-Informed Semantic IDs (GrIS)**

[Paper](https://arxiv.org/abs/2610.01533)

- **recommendation**: GrIS is implemented. Verified registration only; not a new addition.

**2610.01511 · GAW-PO: Preference Optimization with Gradient-Aligned Token Weights**

[Paper](https://arxiv.org/abs/2610.01511)

- **post-training**: GAW-PO is implemented; reweights rejected DPO tokens by gradient alignment.

**2610.01509 · Sharpening Tax in Post-Training**

[Paper](https://arxiv.org/abs/2610.01509)

- **foundation-model**: The ledger already lists sharpening-tax; keep its conclusion.
- **post-training**: Sharpening Tax/PTGS is implemented; do not treat its existing diagnostic as a new candidate.
- **agent**: Sharpening Tax/PTGS already covers difficulty-posterior temperature sampling.
  Evidence locations: Title and complete abstract

**2610.01434 · MWOP: Modality-aware Width-wise Operation Pruning for Efficient MLLMs**

[Paper](https://arxiv.org/abs/2610.01434)

- **foundation-model**: The ledger already lists mwop; keep its conclusion.

**2610.01415 · Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States**

[Paper](https://arxiv.org/abs/2610.01415)

- **agent**: PoS explicit belief state and recovery from traps are already cataloged.
  Evidence locations: Title and complete abstract

**2610.01395 · AF-Muon: An AdamW-Free Muon Optimizer for Tied-Embedding Models**

[Paper](https://arxiv.org/abs/2610.01395)

- **foundation-model**: The ledger already lists af-muon; keep its conclusion.

**2610.01349 · PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents**

[Paper](https://arxiv.org/abs/2610.01349)

- **agent**: PACE already covers influence-path cuts and gating before executing capability effects.
  Evidence locations: Title and complete abstract

**2610.01270 · Not All Is Lost: Repairing Lossy User Preference States of Personalization Encoders**

[Paper](https://arxiv.org/abs/2610.01270)

- **recommendation**: REPAIR is implemented. Verified registration only; not a new addition.

**2610.01256 · DeFA: Dependency-Guided Failure Attribution for LLM Agents**

[Paper](https://arxiv.org/abs/2610.01256)

- **agent**: DeFA dependency/failure propagation graph attribution is already cataloged.
  Evidence locations: Title and complete abstract

**2610.01207 · Dependency-Aware Reward Shaping for Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.01207)

- **agent**: DARS dependency-graph predicate-potential reward shaping is already cataloged.
  Evidence locations: Title and complete abstract

**2610.01161 · My FAULT: Self-Diagnosis as Credit Assignment in Self-Evolving Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.01161)

- **post-training**: My FAULT self-diagnosed terminal credit redistribution is implemented; preserve the existing fidelity statement.
- **agent**: FAULT self-diagnosed error costs and terminal credit redistribution are already cataloged.
  Evidence locations: Title and complete abstract

**2610.01073 · Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover**

[Paper](https://arxiv.org/abs/2610.01073)

- **agent**: RSI Safety already covers current-contract verification and validated rollback.
  Evidence locations: Title and complete abstract

**2610.01026 · It Takes Workflows to Evolve Better Workflows**

[Paper](https://arxiv.org/abs/2610.01026)

- **post-training**: FloWright is implemented under agents, not a new candidate.
- **agent**: FloWright already covers structural hierarchical reward and multi-role co-evolution.
  Evidence locations: Title and complete abstract

**2610.00972 · VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks**

[Paper](https://arxiv.org/abs/2610.00972)

- **agent**: VeriHarness disagreement/consensus evidence verification is already cataloged.
  Evidence locations: Title and complete abstract

**2610.00964 · RPTune: Learned Context Curation for LLM Catalog Search**

[Paper](https://arxiv.org/abs/2610.00964)

- **foundation-model**: The ledger already lists rptune; keep its conclusion.
- **post-training**: Google RPTune is cataloged. The ledger records seven-merchant experiments and local L1 curation, not a new entry.

**2610.00958 · Role-aware Heuristic Episodic Attention for Conversational LLMs**

[Paper](https://arxiv.org/abs/2610.00958)

- **foundation-model**: The ledger already lists rea; keep its conclusion.

**2610.00906 · ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization**

[Paper](https://arxiv.org/abs/2610.00906)

- **agent**: ActiveSaddler's nonstationary failure-pattern bandit curriculum is already cataloged.
  Evidence locations: Title and complete abstract

**2610.00872 · MemFit: Efficient Long-Term Agentic Memory**

[Paper](https://arxiv.org/abs/2610.00872)

- **agent**: MemFit's append-only original turns and multi-path cross-encoder retrieval are already cataloged.
  Evidence locations: Title and complete abstract

**2610.00838 · SHARPO: Segment-Level Credit Assignment for Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00838)

- **post-training**: SHARPO already exists at ledger L12601; keep implementation/evidence limits without a duplicate.
- **agent**: SHARPO's segment-level teacher–student advantage reweighting exists in post-training/sharpo.
  Evidence locations: Title and complete abstract

**2610.00650 · Self-Evolving Coding Rules for AI Coding Agents**

[Paper](https://arxiv.org/abs/2610.00650)

- **agent**: RuleEvolve coding-rule-pool mutation and evaluation exist in agent-research/rule-evolve.
  Evidence locations: Title and complete abstract

**2610.00623 · HAWK: Rethinking Multimodal Drafting for Speculative Decoding**

[Paper](https://arxiv.org/abs/2610.00623)

- **foundation-model**: The input record identifies HAWK as implemented; use the existing ledger entry.

**2610.00437 · JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces**

[Paper](https://arxiv.org/abs/2610.00437)

- **agent**: JevSpawn compositional actions and feedback branch selection exist in agent-research/jev-spawn.
  Evidence locations: Title and complete abstract

**2610.00426 · IrekoGPT: Turning Structured Pruning into Post-Hoc Slimmable LLMs**

[Paper](https://arxiv.org/abs/2610.00426)

- **foundation-model**: The input record identifies IrekoGPT as implemented; use the existing ledger entry.

**2610.00388 · T2SPO: Trajectory-to-Step Policy Optimization for Agentic Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00388)

- **post-training**: T2SPO already exists. Ledger L12689 limits evidence to real TabPFN on CPU with synthetic states plus the objective, not LLM task training.
- **agent**: T2SPO uses TabPFN remaining trajectory distance for step credit and exists in post-training/t2spo.
  Evidence locations: Title and complete abstract

**2610.00333 · LEGO-OPD: Factorized Teacher Composition for Multimodal On-Policy Distillation**

[Paper](https://arxiv.org/abs/2610.00333)

- **foundation-model**: The input record identifies LEGO-OPD as implemented; use the existing ledger entry.
- **post-training**: LEGO-OPD already exists at ledger L12603; keep the factorized-teacher evidence.

**2610.00332 · The Weakest Link: Distilling LLM Reasoning with Worst-Case Constrained Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00332)

- **post-training**: Weakest Link already exists. Ledger L12690 specifies L1 exact-vocabulary gradients and small-policy prefix constraints, not an LLM benchmark.

**2610.00317 · DriftOPD: Sequence-Level Reverse-KL Distillation for One-Step VLA Policies**

[Paper](https://arxiv.org/abs/2610.00317)

- **foundation-model**: The input record identifies DriftOPD as implemented; use the existing ledger entry.
- **post-training**: DriftOPD already exists at ledger L12604; preserve one-hop drifting/critic evidence boundaries.


## Pending review (0)


## Deferred after review (113)

**2610.08720 · WorldSolver: Can LLM Agents Simulate the Physical Dynamics via Solver Generation?**

[Paper](https://arxiv.org/abs/2610.08720)

- **agent**: WorldSolver's 168 physics-solver tasks, fixed scaffold, and execution/VLM/physics-rule scoring fit evolve. Both the github.com/sirujiang/WorldSolver page and API returned 404. Public tasks, evaluator, and license remain unconfirmed; wait for an executable release.
  Reproduction scope: The 60-point passing threshold is demonstrative, not validated. Rules are hidden from agents; model harnesses differ. A VLM judge also appears among evaluated models and needs independent audit. Inaccessible code does not invalidate the method.
  Evidence locations: §2.1–2.3 Eq1–10; §3.1–3.3/Table3; Limitations; official repo/API access 2026-10-07.

**2610.08526 · WareFly-VLA: A Vision-Language-Action Framework for UAV Navigation and Human Tracking in Smart Warehouses**

[Paper](https://arxiv.org/abs/2610.08526)

- **foundation-model**: WareFly-VLA defines 507 flight trajectories, continuous 4DoF actions, and a fixed 431/76 episode split for UAV evaluation. §6 reports open-loop MAE/correlation and trajectory integration on ground-truth frames, not closed-loop flight success. Data availability says data/runner are on request and will be public after acceptance. Reviewed, awaiting public release.
  Evidence locations: §3; §5.2; §6.1 Tables 5–6; §7 limitations; Data availability

**2610.08513 · Wiki-Talkie: Multilingual Benchmarking of Persona-Based Agents on Real-World Discussions**

[Paper](https://arxiv.org/abs/2610.08513)

- **agent**: Amazon Wiki-Talkie's five-language demographic behavior distributions are useful evaluation. amazon-science/wikitalkie returns 404, access requires an application rather than an open mirror, and models A–D and the extractor are anonymous. Review complete, awaiting resources.
  Reproduction scope: Behaviors come from 50 random threads per user; recheck temporal and target exclusion. History and profile are not information-matched. Length strata do not establish causality. Anonymous models prevent numeric replication. Salted hashes cannot prevent text reidentification; group studies do not authorize individual impersonation.
  Evidence locations: §3.1; §4; §5.2; Limitations/Ethics; official GitHub API on 2026-10-07.

**2610.08400 · Atom-JEPA: Joint-Embedding Predictive Architecture for 3D Atomistic Systems**

[Paper](https://arxiv.org/abs/2610.08400)

- **foundation-model**: Atom-JEPA has real SE(3)-equivariant atom/substructure prediction and public transfer results, but matched-budget attribution is unresolved. §G.1 compares Uni-Mol atom-only vs atom+pool with batch sizes 384/128 and learning rates 2.42e-4/1.4e-4. §B lacks same-architecture alternative SSL controls. Need matched controls or budget evidence; training from scratch is not equal pretraining.
  Evidence locations: §3; §4.2/Table4; Appendix B; Appendix G.1/Table26; Appendix H.1.1

**2610.08327 · MedZERO: Self-Evolving Agents for Open-Ended Medical Reasoning Through Controlled Knowledge Accumulation**

[Paper](https://arxiv.org/abs/2610.08327)

- **agent**: MedZERO's alternating Examiner/Reasoner training and temporary-to-persistent KG admission qualify. The paper says code was withheld at submission and planned after publication. Grounding scorer and mapping thresholds lack detail. Reviewed, awaiting release.
  Reproduction scope: Majority agreement is not medical correctness. Persistent admission lacks independent fact verification and can reinforce errors. MCQ options go only to the downstream judge, not the Reasoner. Clinical utility is unestablished; KG/web/judge dependencies are substantial and grounding scoring is under-specified.
  Evidence locations: §3 Eq1–21; §4.1–4.2; §5; AppendixB; Open access checklist

**2610.08250 · MASC: A Multi-Agent Self-Calibration Framework with Latent Construct Alignment for Consistent Client Role-Playing in Psychological Counseling**

[Paper](https://arxiv.org/abs/2610.08250)

- **agent**: MASC uses emotion/state/action prediction, three-agent five-step debate, consensus-first voting, and up to two memory-assisted retries for persona stability. Relevant to CRPC evaluation, but official repo says code and data coming soon and has no license.
  Reproduction scope: 38 profiles and shared constructs/prompts limit generalization. Hetero/Homo use different backbones and do not isolate diversity. 73.97% is final match; 44.19% retry share is conditional on final convergence, not repair probability. KL measures group label frequencies, not therapeutic realism.
  Evidence locations: Multi-Agent Self-Calibration method Eq1–16/Alg1; Experiment Tables2–3; official GitHub API.

**2610.08246 · LeanPlan: Optimal Planning with LLM-Generated Heuristics and Admissibility Proofs**

[Paper](https://arxiv.org/abs/2610.08246)

- **agent**: LeanPlan generates Lean heuristics and admissibility proofs. Controller rejects sorry/admit/native_decide/new axioms, recompiles independently, and checks training tasks. Fits verifiable evolve, but code, benchmarks, and logs are promised only after acceptance.
  Reproduction scope: SCP budgets were tuned on the test suite; original controls do not provide strict full test isolation. One agent generation per domain, not multiple seeds. Proof covers certificate-passing plans costing <B, not unsatisfiability; parser/compiler unverified. Three rejected test certificates count as unsolved.
  Evidence locations: §3–5; §7 Limitations; Reproducibility

**2610.08215 · Learn2Play Bench: How Well Do LLM Agents Learn from Experience in Unfamiliar Environments?**

[Paper](https://arxiv.org/abs/2610.08215)

- **agent**: Learn2Play's 20 hidden-rule games, deterministic terminal scoring, 10 fixed/10 reshuffled variants, and learning across episodes fit evolve. Official Learn2Play-Bench page/API/raw README all returned 404. Public execution and license are unconfirmed.
  Reproduction scope: One instance seed is not cross-seed generalization. The best human is not an average human; a pilot sets hardness. Rule-discovery evidence can include post-scoring episodes and cannot substitute for in-window scores. Batched actions and feedback deduplication mix with memory effects on cost.
  Evidence locations: §3; §4.1–4.2/4.6; §5; official project GitHub link/API

**2610.07969 · EmbodiedSmith: Scaling Embodied Data through Recursive Self-Improvement Flywheel in Simulation**

[Paper](https://arxiv.org/abs/2610.07969)

- **foundation-model**: Full text confirms EmbodiedSmith's data generation and validation are useful, but the public harness, typed skills, and accepted task bundle were not found. Infrastructure integration deferred.
  Reproduction scope: Deformable assets share one material and have incomplete rebound; connecting physical assets to scenes is future work. Ten in-scene simulator tasks do not establish sim-to-real or generalist results. No replayable source tasks for RSI acceptance; do not use a policy given the gold plan.
  Evidence locations: §3.1–3.3; §4.1–4.3 Table4; Appendix9/10

**2610.07948 · Confidence Reasoning Graphs: Structured Confidence Estimation for LLM Agents**

[Paper](https://arxiv.org/abs/2610.07948)

- **foundation-model**: CRG is structured confidence inference on agent trajectories and belongs in the agent track.
- **agent**: CRG recursively breaks success claims into necessary and sufficient subclaims, cites evidence, and multiplies leaf confidence in an auditable evaluator. Official megagonlabs/crg_ce returned 404. Reviewed, awaiting public implementation.
  Reproduction scope: Multiplication assumes approximate conditional independence, not a probability guarantee. Overlapping leaves may double-count uncertainty and missing citations may hide subsequent repairs. BAS gains are not comprehensive discrimination or task gains. The cited scripts were inaccessible.
  Evidence locations: §4 Eq2–5; §5; §6.2–6.4 Tables3–4; AppendixA.3/A.14.3; official GitHub API

**2610.07863 · ReFold: Training-Free Reversible Inter-Turn Context Folding for Long-Horizon Agents**

[Paper](https://arxiv.org/abs/2610.07863)

- **foundation-model**: ReFold is a reversible rendering layer for interaction context, so review it in the agent track.
- **agent**: ReFold has append-only raw history, exact-duplicate stubs, model-marked stale folds, chunk-boundary cache protection, and append-only restoration. Useful context optimization; the paper only promises code/scripts. Reviewed, awaiting release.
  Reproduction scope: High-concurrency solve gains include serving contention and timeouts, not pure reasoning gains. Full-window cells use one task record, not multiple seeds. Select k on independent validation rather than the 20 SWE test tasks. Chunk/reversible ablations rerender fixed traces, not capability comparisons. A100 needs separate measurement.
  Evidence locations: §3 Eq1–7; §4.1/4.3/4.4; Reproducibility

**2610.07835 · DHCG: Dynamic Construction of Hierarchical Collaboration Graphs for LLM-Based Multi-Agent Reasoning**

[Paper](https://arxiv.org/abs/2610.07835)

- **agent**: DHCG's layered dynamic roles, sparse routing, Expand/Finalize actions, and action-aware weighted DPO qualify. Critical training filtering, value-gap thresholds, λγ, and budgets refer to Appendix B, absent in official HTML and PDF; code not found. Reviewed, awaiting materials.
  Reproduction scope: Missing Appendix B blocks exact training and contamination checks. Pass@5 is an oracle-selected bound, not executable agent capability. A static DAG or heuristic planner is not the trained policy. The claimed RL is offline weighted DPO.
  Evidence locations: §3.1–3.3 Eq1–14; §4.1–4.5; nine-page official PDF (last two pages references; no cited Appendix B).

**2610.07817 · One Step at a Time: Trading LLM Autonomy for Process Predictability**

[Paper](https://arxiv.org/abs/2610.07817)

- **agent**: One Step at a Time's stepwise SOP-MCP server execution and auditing are useful. Revised SOPs, tool specs, traces, and analysis code are promised upon publication. Full-text review complete; exact public evaluation deferred.
  Reproduction scope: Pilot uses test tasks, not independent dev, and MCP traces only. Stepwise display/control/meta-instructions are bundled. Coverage checks tool names, not order, arguments, or use of outputs. Grounded does not mean procedurally correct. Mock tools and fuzzy matcher lack large-scale human validation. About 0.3% ungrounded is not proven safety or trust gain.
  Evidence locations: §3; §4.1–4.5 Tables3–4; §5.3; Limitations1–12; Artifacts

**2610.07763 · ST-Bench: A Spatial-Temporal Benchmark for Multi-Agent System Generation on Scientific Research Tasks**

[Paper](https://arxiv.org/abs/2610.07763)

- **agent**: ST-Bench's 100 science tasks, 2,067 queries, and continuous reward fit multi-agent evaluation. The paper has no verified task, preprocessing, or scorer download; official integration deferred.
  Reproduction scope: 1184/391/492 train/val/test. Reward uses 0.1 validity, 0.4 threshold, and 0.5 single-agent reference; it does not recompute science. Agents self-report all metrics; independently recalculate artifacts. Positive-number/-1 checks may reject valid nonpositive results. MAS mainly gains coverage at 1.85–4.5× time, with partial token costing; no overall same-budget superiority.
  Evidence locations: §2.1–2.2; §3.1–3.3; §4.1–4.5; Appendix C.2

**2610.07757 · Acquiring and Verifying Repository Norms for Coding Agents**

[Paper](https://arxiv.org/abs/2610.07757)

- **agent**: RepoNorm explicitly extracts rules, checks implicit norms globally with counterexamples, independently verifies evidence, and supplies read-only norm packs and RepoNormBench. The claimed official API returned 404; reviewed, pending public execution.
  Reproduction scope: Common patterns are not mandatory norms; retain required/recommended/observed. Shared repo versions may make task bootstrap underestimate uncertainty. One run per cell; document checker missed 39 misleading variants. Coding tokens +33.65%, with incomplete logging.
  Evidence locations: §3.1–3.5 Eq1–2/Algorithm1; §4.1–4.5 Tables2–5; §5; §8

**2610.07753 · From Evidence to Action: How Tool-Using Agents Fail**

[Paper](https://arxiv.org/abs/2610.07753)

- **agent**: SafeActBench uses hidden prerequisites, a provenance-bound Evidence Ledger, and deterministic trace scoring to distinguish investigated no-action, one step, and dependency DAGs. Fits evaluation, but official page access failed and public cases/evaluator are unconfirmed.
  Reproduction scope: 656 synthetic cases, five protocols, three runs per case/config. Preserve hidden gold, return provenance, and pre-action observations, not just final state. Internal reference traces passing do not establish agent success or real-business safety certification.
  Evidence locations: §3.1–3.3; §4.1–4.3; §5.1–5.3; Ethics/Reproducibility

**2610.07751 · How Well Do LLMs Reason with Noisy Evidence? An Active Visual Reasoning Benchmark**

[Paper](https://arxiv.org/abs/2610.07751)

- **agent**: VisualNoiseQA uses a VLM as a stochastic visual sensor that a text agent queries, observing samples and semantic consistency. The 1,000 hard human-solvable cases suit active reasoning; code/data promised after publication.
  Reproduction scope: Gold-hit filtering at 1–5 of 11 samples is benchmark construction only. Runtime consistency is agreement across responses, not gold confidence. Five traces versus one GPT-5 Mini run do not provide comparable variance. BP is a prompt upper reference, not training.
  Evidence locations: §3.1–3.2 Eq1–3; §4.1–4.2; Limitations; release footnote

**2610.07625 · Stateless Language Agents: Scaling Long-Horizon Automated Research**

[Paper](https://arxiv.org/abs/2610.07625)

- **agent**: SLA rebuilds stateless Advisor/Worker context in a harness, assigns experiments by evidence group, retains local candidates, and uses a protected evaluator and Landlock. Strong evolve fit. Official repo currently has assets only, no code/README/license; original implementation deferred.
  Reproduction scope: Ablations are all stateless and vary context, isolation, or assignment, not stateful versus stateless. Token matching excludes experiment/evaluation compute. Repeated aggregate scores in intra-task search are not held-out task generalization. Paper token/GPU experiments are not local runs.
  Evidence locations: §3.1–3.3; §4.1–4.2 Tables1–3; §5; Appendix B.1–B.2

**2610.07588 · Personal-Agent Mediated Recommendation with Cross-Platform User History**

[Paper](https://arxiv.org/abs/2610.07588)

- **agent**: PAMO estimates support from full versus cross-history-removed rationale likelihood, fixes positive/negative NDCG-cutoff advantage mass, and uses value-floor-constrained exponential allocation before GRPO. Agent/post-training candidate. MediateRec release depends on internal approval; fixed splits and platform rankings are unavailable.
  Reproduction scope: The gold target is guaranteed among 50 candidates, not end-to-end retrieval. All-time catalog and popularity sampling can leak temporal information. Support is model-relative, not causal correctness. Value preservation applies to fixed rollout groups, not policy/test monotonicity. No multi-training-seed CI or production A/B.
  Evidence locations: §3–5 Eq8/17–21; §6.1–6.2 Table3; Appendix A.5; introduction release footnote

**2610.07570 · Unanimously Wrong: Certified Abstention from How Medical LLM Consensus Forms**

[Paper](https://arxiv.org/abs/2610.07570)

- **agent**: ProbeGuard uses process signals, counterevidence retrieval and re-answering, and stratified LTT abstention. Useful agent risk control. Official repo returned 404 and standardization isolation is unverified; exact reproduction deferred.
  Reproduction scope: Theorem assumes fixed per-example scoring and IID samples. Per-dataset z(keep)+z(RSE) may not use independently fixed statistics; no unconditional distribution-free certificate. RSE averages mutual entailment, not entropy. MedQA coverage about 32%; the consistent stratum's 55.3% is not 60% traffic. MCQ is not clinical benefit. Extra median probe cost 114 seconds/4381 tokens; official contents HTTP 404.
  Evidence locations: §3.1–3.3 Eq3–6; §4.1/4.4; §5.1–5.3; Appendix D Algorithm2/E proof/J; author GitHub API

**2610.07556 · Decoupled Multi-Agent Orchestration**

[Paper](https://arxiv.org/abs/2610.07556)

- **agent**: DeOrch decouples two-stage DAG decomposition/collaboration RL from worker matching, credits nested rollouts separately, and adapts with density-corrected probes, six anonymous pool features, MMR, and Thompson sampling. Official anonymous code endpoint not connected; original implementation deferred.
  Reproduction scope: 55,676 probe calls for new workers are not free. About 410k training orchestrations on four H200s; no heuristic substitutes. Keep probe/train/test and adaptation-heldout isolation. Best-single is hindsight reference. No training-seed variance conclusion; anonymous code inaccessible.
  Evidence locations: §3.1–3.4; §4.1–4.5 Tables2–5; Appendix B.1–B.5

**2610.07553 · Which and When to Admit: Gradient Admission for Data-Centric Small Language Model Finetuning**

[Paper](https://arxiv.org/abs/2610.07553)

- **foundation-model**: GRADE gradient alignment and EMA gating are new, but the public budget and selection protocol are unresolved. Appendix A estimates anticipated costs and promises a future table; U contains TBD; T alternates highest held-out Avg and validation-loss preselection. Require measured costs and selection records; Meta affiliation alone is insufficient.
  Evidence locations: §4.1–4.2; §5.1–5.2/Table1; Appendix A; Appendix O.4; Appendix T/Table3; Appendix U

**2610.07518 · Harmful SFT Leaves a Continuous Trace in LLM Checkpoint Updates**

[Paper](https://arxiv.org/abs/2610.07518)

- **post-training**: TRACE fits nonnegative coefficients using effective SFT update kernels and a pure target reference bank. sH is geometric association, not harmful-example percentage. Four 7/8B backbones have checkpoint audits. Anonymous code access failed (direct HTTP 401); executable artifacts unconfirmed. Distinct from NVFP4 TRACE.

**2610.07473 · PsyCIDRA: A Dual-Agent Framework for Psychiatric Interviewing and Diagnostic Reasoning**

[Paper](https://arxiv.org/abs/2610.07473)

- **agent**: PsyCIDRA uses five notepad types, 60 expert skills, and ICD lookup for an interview agent, with separate transcript diagnosis. Potential simulated-patient evaluation. The official code/134-profile repo contains only the README title. Full text reviewed; public execution deferred.
  Reproduction scope: Human reference is same-transcript expert consensus, not independent diagnosis. Sample is not population-representative, with four early safety-stop exclusions. PsyCIRA 3/49 flags include two crises, versus Direct 2/52. Do not claim clinical effectiveness, safety, or readiness even with supervision. Human conversations are private; code and simulated profiles are unreleased.
  Evidence locations: §4.1–4.2; §5.1–5.3; §6.1–6.2; Limitations/Ethics; official repository

**2610.07423 · 2d-fet-bench: from spatial reasoning to fet design on flakes**

[Paper](https://arxiv.org/abs/2610.07423)

- **agent**: 2D-FET-Bench evaluates layout agents with real flake outlines and hidden geometry. Its 128 tasks and code are promised after publication; official integration deferred.
  Reproduction scope: Independently check fixed layers by XOR after KLayout saving, not only the interactive verifier. Automated passes among 7,680 runs are not manufacturability; experts approve only 56.4–63.5% of sampled passes. Main ReAct-3 control was selected post hoc, and model reasoning modes differ. MoSe2/WSe2 are role labels on graphene outlines.
  Evidence locations: §3 Eq1–2; §4; §5; §7; Appendix J/L

**2610.07355 · Tracking Is Not Permanence: What Video World Models Keep of a Hidden Object**

[Paper](https://arxiv.org/abs/2610.07355)

- **foundation-model**: Full text: latent/pixel/AR two-world hidden-region distance probes with never-shown and exit controls; synthetic curriculum changes V-JEPA memory. The main renderer shares training provenance, IntPhys is dev-only with unreproduced protocol portions, and Appendix J excludes generalization to all world models. Useful diagnostic, but public renderer/runner not located. No integration or ground-truth worlds as agent input.
  Evidence locations: §3.1–3.5; §4.4–4.6; Appendix I/J

**2610.07127 · PlaySuite: A Large-Scale Benchmark for Interactive Visual Intelligence**

[Paper](https://arxiv.org/abs/2610.07127)

- **foundation-model**: Reused the agent review of §3–6 and Appendix A.3: 5734 games, 14 models, network-isolated workers and shared vLLM. 1fps Qwen3.5-9B milestones are ordinal 0–4, not completion percentages. Games pause for inference; not real time. Agreement from 60 videos and six humans is limited. Code/data promised, no public runnable harness; PyWeek and itch licenses are not uniformly open source.
  Evidence locations: §3–6; Appendix A.3; official README code/data coming soon; agent-fulltext-decisions.json; README release status; shared agent review.
- **agent**: PlaySuite's closed-loop keyboard/mouse control and video milestones across 5734 games suit public evolve evaluation. Official README says code/data/harness/judge coming soon and API license=null. Await release, not rejection for being a benchmark.
  Reproduction scope: Progress averages ordinal values, not completion fractions. Inference pauses games, not real-time reaction. PyWeek allows free unchanged redistribution; itch free access is not a unified open-source license. Public-game contamination is unresolved.
  Evidence locations: §3–4; §5/Table2 full text; §6/Limitations; Appendix A.3; official README.

**2610.07105 · Beyond Successor Accuracy: State Retention for Recursive Self-Improvement in Recommendation**

[Paper](https://arxiv.org/abs/2610.07105)

- **recommendation**: RecRSI reports offline retention trajectories on Amazon/Yelp with GRU4Rec, SASRec, and FMLP; 34/36 successful trajectories are not online experiments. Retain as an RSI lead without bypassing the industrial threshold. Needs separate academic exception approval.

**2610.07089 · Towards a Unified Misuse Monitoring Benchmark**

[Paper](https://arxiv.org/abs/2610.07089)

- **agent**: Unified Misuse Monitoring Benchmark evaluates monitors with a fixed false-positive budget and whether the first flag falls inside the harm window. Useful framework; official code is coming soon, so dataset integration is deferred.
  Reproduction scope: The main table selects thresholds on evaluation data. Use Appendix E.1's frozen 10% benign calibration. One Gemma simulates all tool outputs; this is not real tool capability. Model-assisted location annotations agree exactly 67.5%. Earlier blocks are not necessarily worse; timing depends on the defined window.
  Evidence locations: §3.1–3.4; §4.1; §5 protocol; §6/Limitations; Reproducibility

**2610.07086 · SchemaFill: Efficient LLM Tool Calling via Slot-Parallel Speculative Decoding**

[Paper](https://arxiv.org/abs/2610.07086)

- **agent**: SchemaFill uses public schema and BM25 to draft three call slots in parallel with MAIN/SIDE isolation. Revalidate side values at the actual prefix; target decides all structure tokens. Relevant decoding, but official repo returned 404 and full EAGLE head/numerical equivalence are unverified. Deferred.
  Reproduction scope: 4.05× is structured response generation, not whole agent tasks including tool execution. Oracle skeleton is a ParallelFill diagnostic only. Greedy equivalence requires identical target logits, masks, and positions; stochastic correctness needs real proposal q or point mass and residual sampling, not argmax alone. Blackwell timing is not A100 timing; no local run.
  Evidence locations: §3.1–3.3 Eq1–2; §4.1–4.3 Algorithm1; §5.1–5.3 Table1; AppendixA/B/C.1

**2610.07004 · Topology-Consistent Task Planning over Cellular Workflow Complexes for LLM-based Agents**

[Paper](https://arxiv.org/abs/2610.07004)

- **agent**: TopoPlanner lifts a dependency graph into a cycle-region cellular complex. Query-conditioned cosheaf gating and closure retrieval feed multidimensional message passing and soft graph tokens for planner training. TaskBench is public; grouped splits, topology construction, and code were not located, so exact evaluation is deferred.
  Reproduction scope: A merged cycle cell is not repeated execution; executor owns stopping. Greedy closure is not optimal PCST. Gold tools are only NLL targets or external scores. Node/link F1 and ACC describe plans, not tool success. Finite Kmax does not guarantee a complete cycle basis. Query motifs need held-out topology checks. A small run does not reproduce four-H800 training.
  Evidence locations: §3–4; Appendix B/D/G.1/G.3/G.4

**2610.06971 · AegisFlow: A Multi-Agent Agentic AI Framework for Autonomous Remediation and Self-Healing in Fragile Data Ecosystems**

[Paper](https://arxiv.org/abs/2610.06971)

- **agent**: AegisFlow describes multi-agent monitoring, diagnosis, LLM repair, shadow sandbox, and hot swapping for data pipelines, with human overrides and rollback. The paper includes architecture and experiment claims.
  Reproduction scope: Deferred. The paper cites github.com/mbilalawan/aegisflow for data/scripts, but access and result provenance were not verified. The 98% on-call and 300% feature velocity metrics lack public definitions; architecture alone is not quantitative online evidence.
  Evidence locations: PDF pp14–20,34,38–42; Shadow Sandbox; Supplementary materials

**2610.06949 · AdaLoop: Adaptive-Depth Latent Reasoning for Audio Language Models**

[Paper](https://arxiv.org/abs/2610.06949)

- **foundation-model**: AdaLoop has a question-conditioned multiscale recurrent audio connector and ACT-weighted output. §2.3 Eq6 writes ponder cost as hard stop step K without differentiable remainder or gradient estimator. SFT trains connector only, whereas phase two jointly trains the LM; retain Fixed4 controls and clarify loss for attribution.
  Reproduction scope: Hard K in the formula has almost-everywhere zero gradient with respect to halting probabilities, leaving the claimed ponder training incomplete. No official code resolves it.
  Evidence locations: §2.1–2.3 Eq1–6; §3.1–3.4 Tables1–2; §4

**2610.06923 · RadOnc-Agent: An LLM-Orchestrated Framework for AI Workflows Across the Radiotherapy Care Pathway**

[Paper](https://arxiv.org/abs/2610.06923)

- **agent**: RadOnc-Agent standardizes 26 schemas for 17 clinical and nine auxiliary functions. The LLM chooses functions and arguments; controller dispatches, processes images asynchronously, and returns structured results.
  Reproduction scope: 2,600 questions × three sessions assess technical selection, schema, and dispatch, not clinical benefit. Core code is explicitly private and real patient data are IRB-restricted. Public SynthRAD cannot substitute for the full workflow.
  Evidence locations: §II.1–2, evaluation, Code and Data availability.

**2610.06910 · GAMEGO: Training Game-Dev Agents with Synthetic Trajectories Anchored in Real-World Assets**

[Paper](https://arxiv.org/abs/2610.06910)

- **agent**: GameGo starts from real game seeds and uses staged PRD, asset grounding, and query compression to generate 55,060 sandbox trajectories for assistant-mask SFT. Evaluation uses an actual headless browser playtester and judge.
  Reproduction scope: Split 124 benchmark seeds before training; actual runnable game traces are essential. Appendix promises implementation after acceptance but excludes GameGoData trajectories, unlike the abstract's open-release claim. Wait for verified training data and models. A build pass is not gameplay correctness; judge preference and asset licenses are separate.
  Evidence locations: §3–5, Appendix E, reproducibility statement.

**2610.06861 · When Does External Guidance Help LLM Reasoning? A Bias-Variance Theory of Guidance-Augmented GRPO**

[Paper](https://arxiv.org/abs/2610.06861)

- **post-training**: GA-GRPO mixes independent guided/unguided rollout gradients with σ0²/(σ0²+Rmax²δ²T) weighting. The paper reports Qwen2.5-Math-7B on nine benchmarks and eight A100s. Adaptive TV divergence, variance estimation, and IS clipping were not specified in reviewed methods. T ambiguously denotes rollout horizon or training steps. Curves do not close faithful implementation requirements.

**2610.06825 · PlotGround: Grounding Plot Digitization in Real Scientific Figures and Their Source Data**

[Paper](https://arxiv.org/abs/2610.06825)

- **foundation-model**: PlotGround reconstructs source data from charts and provides 1,119 human-verified evaluation items. Pipeline and PlotGround-1k are promised after acceptance; the original task bundle is not yet reproducible.
  Reproduction scope: Relative error at ±5% and ±2% needs a zero-value rule. Source tables construct labels and must not enter image-only evaluation. Figure and table agents have different inputs, not matched-information gains. API inference budgets differ.
  Evidence locations: §3.1–3.4; §4.1–4.2/4.6; Limitations

**2610.06695 · MedPrune: Topology-Efficient Multimodal Multi-Agent Communication Evolution for Medical VQA Tasks**

[Paper](https://arxiv.org/abs/2610.06695)

- **foundation-model**: MedPrune optimizes communication topology for medical multi-agent systems. Review in agents, not foundation architecture.
- **post-training**: MedPrune optimizes multi-agent nodes and edges through structural search, not LLM-parameter post-training.
- **agent**: MedPrune uses policy gradients to learn heterogeneous spatiotemporal communication, then prunes nodes by weighted degree and edges with nuclear-norm regularization. Relevant mechanism, but missing sampling/training details and upstream code defer faithful implementation.
  Reproduction scope: One-shot pruning in prose conflicts with per-step pruning in Algorithm 1. Row-softmax sampling multiplies retained edges only; DAG distribution unclear. How weighted natural-language outputs become prompts is unspecified. Few-shot 10/20/40 with all original train and test lacks example exclusion details. Validation and patient isolation are unreported. Nuclear norm favors low rank, not guaranteed sparsity or clinical robustness.
  Evidence locations: §3 Eq2–10; §4 Tables1–2; AppendixB.1–B.3; PDFp14 Algorithm1; D.2/D.3

**2610.06597 · Can Agent Harnesses and Inference Engines Hear Each Other? The HEAR Protocol for Agentic LLM Serving**

[Paper](https://arxiv.org/abs/2610.06597)

- **agent**: HEAR's bidirectional harness/engine protocol distinguishes intent/control, preference/requirement, observation/guarantee, and acceptance/completion. Cache/wait protections and role configuration are useful. Anonymous repo returned not_connected; patch and manifest unavailable. Deferred.
  Reproduction scope: Noninferiority is insufficient; 89 paired DRB records do not replace all 100. At 100% Mooncake load the combined session/cache/guard throughput drops to 0.89×. Approximate cache settings do not preserve exact model numerics. Judge runs on a different GPU; timing omits tuning/offline profiling. Anonymous API returned not_connected.
  Evidence locations: §3.1–3.4; §4.1–4.4 Tables3–5; AppendixA.1/A.3–4; B Table17/JudgeProvenance

**2610.06576 · Before Agent Tells The Lie: Has Deception Already Been Represented?**

[Paper](https://arxiv.org/abs/2610.06576)

- **agent**: Deep-kernel MMD white-box prefix probes and type-balanced CAA honesty intervention suit agent monitoring. Full text reviewed; anonymous code not connected and training/deployment selections under-specified. Deferred.
  Reproduction scope: Post-hoc decisive-step alignment is not known online, with survivor and length confounds. No task-grouped split, validation size, or full regularization details. α=2 is selected by best results without validation details. Labels describe behavior, not internal intent. Keep 7/500 invalid cases; 72.9% honesty retention shows intervention cost. Public artifacts unverified.
  Evidence locations: §3.1–3.4 Eq3–9; §4.1–4.4 Table1/Figs3–4; §5; Reproducibility

**2610.06563 · HERA: Harness-Environment Co-Evolution for Reliable Agentic Abstention**

[Paper](https://arxiv.org/abs/2610.06563)

- **agent**: HERA makes same-task feasible/infeasible pairs and co-evolves environment and harness from failures. Independent 15-pair validation uses nondegenerate Abstain/Pair selection. Good evolve fit. Base/final harnesses and runner are public, but 120 instances require authorization, deferring full evaluation.
  Reproduction scope: Alternate routes, inverse mutation, and semantic review support infeasibility, not formal proof. Group splits for derived pairs; task disjointness is not environment/domain disjointness. One rollout per 15 validation pairs does not prove long-term generalization. Full training pipeline not verified.
  Evidence locations: §3.1–3.2; §4; §5 Table1; Appendix B.3/B.4/C.1; official README

**2610.06514 · ANT: A Multi-Granularity Network Traffic Dataset and Benchmark for Agents Behavior Auditing**

[Paper](https://arxiv.org/abs/2610.06514)

- **agent**: ANT is a network-side agent behavior/privacy dataset for supplementary observability. Anonymous public access failed; the 104GB data and executable package are unverified. Integration deferred.
  Reproduction scope: 3,114 episodes and 47 primitives. Split by episode and mask IPs; do not distribute same-trace segments across train/test. Only 20 of 209 test episodes are malicious; refusal filtering changes distribution. Authorized isolated experiments only; no real user traffic capture. Traffic classification is not task capability.
  Evidence locations: §3.1; §4.1; §5; Ethics/Reproducibility

**2610.06411 · From Benchmark to Bench: Can Agents Survive Real-World Drug Discovery?**

[Paper](https://arxiv.org/abs/2610.06411)

- **agent**: MAGI orchestrates REINVENT, ADMET, and structure prediction via MCP, retaining candidates and versioning goals across five rounds. Useful controller, but nine projects include undisclosed AstraZeneca work and restricted scorers.
  Reproduction scope: Endpoints are predictions, not new wet-lab results. One trajectory per backend and no static-goal control cannot isolate the agent. Sanofi's temporal cutoff does not exclude pretraining exposure. Do not invent private scoring data; only a separate public-subset evaluation is feasible.
  Evidence locations: §3.1–3.2; §4 protocol; §6–7; supplemental code DOI.

**2610.06401 · RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents**

[Paper](https://arxiv.org/abs/2610.06401)

- **agent**: RAISED self-generates runnable tool chains. Independent clean-teacher distributions supervise clean/injected students on the same response tokens with forward KL over top-256 plus residual bucket. Qualifying defense training, but official repo returned 404; data/scripts blocked and reproduction deferred.
  Reproduction scope: Offline fixed clean-teacher trajectories, not on-policy distillation. Static injections only; Appendix F adaptive zero-reward failure is not robustness. Same-model generation and filtering can preserve errors. Bucket KL is coarse, not exact full-vocabulary KL. Count teacher generation and 15GB distribution storage; hard SFT is not equivalent.
  Evidence locations: §3 threat; §5.1–5.2 Eq3–4; §6; AppendixC.5.1/E Table14/F/G; official GitHubAPI

**2610.06204 · Do Small Language Models Learn to Negotiate? A Controlled Scaling Study of RL-Trained Sellers**

[Paper](https://arxiv.org/abs/2610.06204)

- **foundation-model**: Small-model negotiation GRPO varies learning rates and scale; domain post-training empirical study.
- **post-training**: An independent bilateral negotiation ledger uses private Dirichlet utilities, JSON counter/accept, a 12-round cap, and held-out buyers/domains. Potential public evaluation. Protocol is described, but the environment and scenario generator were not found. Architecture and compute confound size comparisons.
- **agent**: Gemma negotiation RL controls scale and learning rate but adds no defining agent training method.
  Evidence locations: Title and complete abstract

**2610.06190 · Bridging the Evidence-to-Execution Gap:A Reflective Agent for Multi-Objective Peptide Design**

[Paper](https://arxiv.org/abs/2610.06190)

- **agent**: EASER combines offline low-rank protein-property controls with evidence-agent probes and adaptive sampling. Transferable multi-objective search. Code, matrices, and splits are promised; original reproduction deferred.
  Reproduction scope: Activity, safety, and CPP effects are predictor outputs, not wet-lab/clinical evidence. Internal predictor bias limits search; safety scores do not establish safety. Matched candidate counts do not match LLM/retrieval budget. Candidate data, matrices, and curated evidence are not released. Scalar random search is not the method.
  Evidence locations: §3.1–3.3 Eq1–2; §4; §5.2 Table3/§5.3–5.4; AppendixB/C.1 Algorithm1/G

**2610.06163 · Where Did the Repair First Go Wrong? Localizing the Origins of Silent Failures in Agentic Vulnerability Repair**

[Paper](https://arxiv.org/abs/2610.06163)

- **agent**: SAGE uses prefix-only safety reasoning rubrics and code snapshots to locate the first observable deviation in confirmed silent failures. Useful trajectory diagnosis. Zenodo access failed and complete normalizer/judge scripts are unverified. Deferred.
  Reproduction scope: Only 3,684 of 5,400 attempts enter validation; 95 confirmed cases span 19 tasks. Failure anchors are retrospective and must not enter evaluated agents or step judges. Repeated judge agreement is not correctness or causal attribution. Human labels cover code provenance and writes only. SecurityEval lacks tests; L1 syntax/import/structure cannot establish function.
  Evidence locations: §3.2–3.4; §4.3; §5.1–5.2; Data Availability

**2610.06122 · Benchmarking Jailbreak Guardrails for Embodied Agents**

[Paper](https://arxiv.org/abs/2610.06122)

- **agent**: Fixed embodied agent backends compare perception, planning, and control guardrails, measuring bypass, simulator hazards, benign completion, and cost. Anonymous supplements lack a verified public path; reviewed and deferred.
  Reproduction scope: Only 300 safe/300 unsafe AI2-THOR tasks. Some results use GPT-4o comparison to reference plans rather than environment truth. No physical robot safety certification. Run defensive evaluation in isolated simulators only. Report false blocks and latency, not bypass ranking alone.
  Evidence locations: §3 taxonomy/metrics; §4.1–4.3; §6; Reproducibility/Ethics

**2610.06056 · ROT: Rotating Hidden States towards Contextual Vectors for Hallucination Mitigation in LVLMs**

[Paper](https://arxiv.org/abs/2610.06056)

- **foundation-model**: ROT rotation/smoothing and results were checked, but exact trigger τ and model layer zones are missing. LLaVA layers 6–26 in prose conflict with Appendix Algorithm 1's 1 to Lmid. Author path unconfirmed.
  Reproduction scope: Appendix lists α/β/γ but no τ. Layer selection on 3,000 CHAIR examples lacks an independent validation split. MME covers three perception subsets; POPE does not beat all baselines. Resolve prior-layer pre-FFN cache versus hk−1 semantics. No public author code was found; do not substitute a heuristic.
  Evidence locations: §3.1–3.2 Eq1; §4.1–4.2 Eq2–6; §5 Tables1–3; App A Algorithm1/C/D

**2610.05982 · Breaking the Tie: A Cluster-Aware Routing Framework for Large Language Models**

[Paper](https://arxiv.org/abs/2610.05982)

- **foundation-model**: CASLR clusters queries and trains a BERT router on masked soft labels from expert correctness per cluster. Clear method, but independent training/calibration/test splits and label statistics scope are incomplete. Capability comparison deferred.
  Reproduction scope: Correctness can label training only, not construct test-derived cluster utility. Specific splits/seeds and upstream code were not found. Count 1.13-second routing cost, not near-zero overhead. New experts require new statistics.
  Evidence locations: §4 Eq4–9; §5.2–5.3; §5 routing cost; Appendix A

**2610.05586 · AgentDoxx: Agentic Re-identification of Anonymized Text with Web Search**

[Paper](https://arxiv.org/abs/2610.05586)

- **agent**: AgentDoxx evaluates reidentification of anonymized agent text. Its 822 synthetic interviews are based on real identities; text and gold are explicitly unreleased and controlled hosting is planned. Integration deferred.
  Reproduction scope: Retain defensive privacy lessons only: jointly assess output/retrieval leakage and anonymization utility. Do not rebuild real identity links, scrape private interviews, or publish identifications. The 1,250 real interviews lack gold; 43 matches are not accuracy. Self-disclosed identities are not population-representative. Fictional offline canaries are not official replication.
  Evidence locations: §3.1–3.2; §4.1; §5/Limitations; Ethics/Data and release policy

**2610.05559 · Cut Binary Cross Entropy: Efficient Large-Vocabulary Loss and Gradient Kernels for Sequential Recommendation**

[Paper](https://arxiv.org/abs/2610.05559)

- **recommendation**: Google's public CutBCE JAX/Pallas TPU kernel measures memory and speed on Yambda50M/SASRec, not online A/B. The defining v5e/v6e operator cannot run here. CUDA BCE is not a reproduction; do not reclassify to bypass the industrial threshold.
- **foundation-model**: Reviewed exact BCE in JAX/Pallas on TPU can remain an infrastructure candidate. No industrial A/B or LLM experiment. NVIDIA is not an equivalent kernel; require TPU and separate scope approval.
  Reproduction scope: 65.7% HBM and 225.9% speed refer to TPUv6e, not NVIDIA. Do not relabel as foundation to bypass A/B evidence.
  Evidence locations: §III-A Eq1–2; §IV-B/TableIII; §V

**2610.05399 · Adaptive Code Revision Attacks on AI Pull Request Reviewers**

[Paper](https://arxiv.org/abs/2610.05399)

- **agent**: AFCRA revises code from reviewer feedback while retaining the CVE property. A fresh evaluator runs the PoC and calls it exploitable only if the historical fix blocks it. The 159 runnable PRs fit defensive evaluation. No verified public task/container/PoC package yet.
  Reproduction scope: Attacker PoC access is an explicit threat model. Reviewers cannot access gold fixes externally. An extra-information upper bound is an oracle diagnostic. Defense and false rejections on 33 previously successful attacks do not establish general security; historical CVE contamination is possible.
  Evidence locations: §3–4; §5 RQ1–4; Threats to Validity

**2610.05387 · GNN-CB: A Graph Neural Network Competition Benchmark for Human and LLM Evaluation**

[Paper](https://arxiv.org/abs/2610.05387)

- **agent**: GNN-CB uses 18 graph-learning contests and hidden test scoring for plan→code→execution repair. Useful CPU coding/evolve benchmark. MIT infrastructure promised but no official scorer located. Deferred.
  Reproduction scope: A 10k output limit per API call differs from native agent session budgets. One greedy run and human LLM use are not fully auditable. Do not average unlike metrics into a ranking or invent same-named tasks; get official splits and scorer.
  Evidence locations: §3.1–3.3; §5/Limitations; Data and Code Availability

**2610.05380 · VHDL-REPOBENCH: A Repository-Level Benchmark for Evaluating Large Language Models on VHDL Design Generation**

[Paper](https://arxiv.org/abs/2610.05380)

- **foundation-model**: VHDL-RepoBench retains cross-file dependencies and four completion, summarization, and module generation tasks with GHDL and VUnit/Cocotb. Complete official tasks and dependencies were not located.
  Reproduction scope: Most Pass@k tests compilation only; only a 135-SMG-module subset requires testbenches. Do not call all scores functional correctness. Public code contamination and isolation for about 100 repositories are unclear. Summary ROUGE and preference are not simulation success.
  Evidence locations: §III-A–C; §IV metrics; §V

**2610.05319 · Understanding the Hierarchical Structure and Functional Landscape of the Model Context Protocol Ecosystem**

[Paper](https://arxiv.org/abs/2610.05319)

- **agent**: MCPacific extracts about one million tools statically, designs node-level taxonomy with LLMs and independent pilots, then embeds routes and reviews manually. Same-enabled-tool hierarchical retrieval is useful discovery infrastructure. Full corpus/taxonomy/runner promised, not located. Deferred.
  Reproduction scope: Comparable functions do not guarantee schema or behavior equivalence. Semgrep alerts are not confirmed vulnerabilities. Static patterns miss dynamic tools. GPT-5.4 is both evaluated and judge; claim coverage is not task success. Public tools cover seven languages.
  Evidence locations: §3.1–3.3 Algorithm1; §4 RQ4; Threats to Validity/Ethics

**2610.05241 · StateWise: Diagnosing and Repairing Persistent Operational State Before Agent Actions**

[Paper](https://arxiv.org/abs/2610.05241)

- **agent**: StateWise holds context fixed, attributes effects through per-record counterfactual replanning, uses read-only checks, developer intent, and typed evidence to correct scoped memory, then independently verifies state/action. Artifact repo is mentioned but no URL was found in cached full text. Await 150 executable cases and manifest/audit/source package.
  Reproduction scope: 40 dev and 150 test cases, plus 20 independent cross-model cases. Cases are designed or literature-inspired, not natural incident rates. 93.3% and zero unsafe cases are bounded outcomes, not guarantees. Keep verifier/state interfaces and external gold scorer; ordinary permissions still apply.
  Evidence locations: §3–5; §6; Data Availability

**2610.05223 · Look Before You Leap: Thermodynamic Arbitration of Parametric and Non-Parametric Knowledge in LLM Agents via Self-Regulating Memory Architectures**

[Paper](https://arxiv.org/abs/2610.05223)

- **foundation-model**: MARTA is an agent memory-retrieval framework, reviewed in the agent track.
- **agent**: MARTA projects frozen LM entropy, margin, and hidden variance to BiGRU memory-header affordances, with Sparsemax and bypass. CEA hard-negative NCE trains only the controller. Core executable, but the multimodal procedural/semantic/episodic suite, utility labels, checkpoints, splits, and code were not found. Deferred.
  Reproduction scope: Gold-document acceptance is an oracle retrieval check, not answer quality. SQuAD unanswerability is not general epistemic awareness. 12 ms/3.7× depends on L4 and the 450 ms retrieval setup. Lower entropy is not truth. Multiple backbones do not establish universal invariance. Require actual logits/hidden states and held-out calibration.
  Evidence locations: §3–4; Appendix A Algorithm1/2; B profiling

**2610.05219 · Safe Context Switching for Agents in the Wild: Mitigating Subspace Interference via Orthogonal Adaptation**

[Paper](https://arxiv.org/abs/2610.05219)

- **agent**: AURA freezes old LoRAs and separates new adapters with B-subspace projection and a Frobenius penalty. Chain-of-Pollution retains KV. Code and loader are promised after acceptance; paired chain data and cache/activation protocol remain unclear. Deferred.
  Reproduction scope: Soft orthogonality is not a hard safety guarantee or unlimited scaling. TruthfulQA is not adversarial safety; logit cosine and KL are not safety behavior. Select rank 64 and λ=0.5 on independent validation; the paper omits statistical uncertainty. Execute actual shared-cache checks across adapters, not simulated orthogonal matrices.
  Evidence locations: §3–5; Appendix A/C/D

**2610.05119 · LexiHorizon: Stabilizing Reinforcement Learning for Long-Horizon Deep Search**

[Paper](https://arxiv.org/abs/2610.05119)

- **agent**: LexiHorizon uses 128K context with full reason/action traces but markers for old observations, gates a 30-call saturated effort bonus on nonzero answer reward, and runs GSPO G16 on live web rollouts. Auxiliary resets discard fragments but still cost compute. Training data, live backend, code, and checkpoints were not located; wait for a replayable public protocol.
  Reproduction scope: Mean accuracy over eight traces is not pass@8 or eight training seeds. Policy token counts omit tools. 99.88 valid answers is not correctness. Gold is judge-only. Same-benchmark sweeps and 90% compression need separate validation. Cached fixtures cannot reproduce live training; verify the 9B/128K GPU budget.
  Evidence locations: §3.2–3.3; §4; Appendix A.2–A.3

**2610.05103 · VulValidate: Auditing Function-Level Vulnerability Labels with Executable Evidence**

[Paper](https://arxiv.org/abs/2610.05103)

- **agent**: VulValidate binds vulnerable function labels to historical source and uses matched dynamic evidence on vulnerable/fixed builds, function attribution, and cold replay. Useful defensive audit, but official images and index unavailable. Integration deferred.
  Reproduction scope: Execute only authorized isolated historical fixtures. A successful build is not source fidelity. Crashes do not prove the labeled function is vulnerable; failed triggers do not prove safety. 35,849 audit items include unresolved cases and human adjudication; synthetic return values cannot substitute.
  Evidence locations: §2.1–2.5; §3.1/3.5; §5 threats

**2610.05037 · SparseCraft: Agentic Hardware-Software Co-Optimization for Sparse Computing**

[Paper](https://arxiv.org/abs/2610.05037)

- **agent**: SparseCraft uses constrained MCP to mutate Gemmini Chisel RTL, memory, and schedules. Immutable harness hashes, legality, elaboration, Verilator bitwise gold, synthesis, Pareto admission, and bounded repair form 15 rounds. Only a source link label was found; full bundle and Chipyard/EDA verification unavailable. Deferred.
  Reproduction scope: One 512×512 GraphChallenge INT8 workload and 328-minute run, no held-out workload or search-seed variance. 5.61 perf/W and 11.8 EDP use modeled energy and SRAM area, not measured silicon; clock fixed at 2 ns. External gold must be immutable to the LLM. Require real EDA gates.
  Evidence locations: §II–IV Algorithm1; Gate ladder; Workload

**2610.04973 · TrajLong: Co-Designing Agentic and Long-Context Supervision for Mid-Training**

[Paper](https://arxiv.org/abs/2610.04973)

- **agent**: TrajLong cleans and reorganizes agent traces into Retrieval, MultidocQA, and StateTracking, then all-token CPT on context and multiple QAs. Fixed 10B compiled/30B background mixture before shared SFT. Full compiled and background data and checkpoints not found; defer full scale. Compiler can be studied separately at small scale.
  Reproduction scope: 256K/40B-token CPT requires original loss and background mixture. Toy QA is not reproduction. Contamination filtering removes the entire source if a derived QA matches. ρ1 is correlation over four settings, not causal. Separate Avg@3 and BoN@3; neither is a training seed. Final test cannot choose checkpoints.
  Evidence locations: §3–4; Appendix A.2/A.3/C/D.1

**2610.04914 · Monitorability Disposition in Large Reasoning Models**

[Paper](https://arxiv.org/abs/2610.04914)

- **post-training**: Monitorability disposition is a standalone self-report and monitoring-shutdown protocol: two channel topologies by four directives, 150 tasks in three categories, and external judging. Appendix has prompts, but executable runner and results are not public or verified. Await public resources rather than rejecting for no loss novelty.

**2610.04888 · No Hindsight for LLM Fact-Checkers: Measuring Leakage Channels in Misinformation Detection**

[Paper](https://arxiv.org/abs/2610.04888)

- **post-training**: Point-in-time fact checking separates future retrieval evidence from parametric outcome leakage using dated trust tiers, temporal splits, a frozen-LM bottleneck, and MI head. Date cache, splits, K text, and code are promised at camera-ready. Public execution unavailable. K contains label information and unknown dates are discarded.

**2610.04777 · ARISE: Adaptive Agentic Reasoning with Image-grounded Self-Evaluation for Interpretable IBD Assessment**

[Paper](https://arxiv.org/abs/2610.04777)

- **foundation-model**: ARISE is a domain-specific diagnostic agent workflow for inflammatory bowel disease.
- **agent**: ARISE uses training image labels and expert visual vocabulary to form inspectable clinical hypotheses, refines on validation, and resolves conflicts using FOL/Z3. Defining method and CrohnIPI/C-TRUS evaluation reviewed.
  Reproduction scope: Deferred; expert finding annotations, 13-patient split, full prompts, and implementation release unverified. Clinical satisfiability is not medical correctness. Do not provide lesion labels to the agent at test.
  Evidence locations: ARISE state/refinement/Z3; normalized p13–22,30–32

**2610.04740 · Toward a Locally Deployable Agentic Co-Scientist: Small-Model Planning for Early-Stage Drug Discovery**

[Paper](https://arxiv.org/abs/2610.04740)

- **agent**: The small Co-Scientist uses UMS chunked state and 18 scientific tools to build dependency-valid plans, trains LoRA on 1,263 path-first query-plan pairs, and replans with a rule evaluator.
  Reproduction scope: Deferred; custom query-plan data, internal tools, and external services are not verified public. Query splits do not isolate workflow types. Schema-valid-only denominators are not end-to-end scientific success.
  Evidence locations: System/UMS/Planner; normalized p11–20,103,130–131; Appendix A/B

**2610.04716 · Towards Automatically Pruning Logging Code with Coding Agents: How Far Are We?**

[Paper](https://arxiv.org/abs/2610.04716)

- **agent**: LogRem mines real merged Python/Java logging removals, uses static identification and human verification for 387 tasks, and provides pre-change source plus descriptions that hide target lines. Scores removal sets, unrelated code preservation, and traces. Optional discussion and ten pattern/eleven cause categories support ablations.
  Reproduction scope: Parseable does not mean functional. RWCA matches historical patches, not all correct solutions. Validity is 95.6–100%, RWCA 11.1–19.6%. Historical discussion can expose future intent; isolate it and prevent patch leakage. Do not tune evolve on the same tasks. No public LogRem387 annotations or traces located, so defer exact benchmark rather than inventing cases.
  Evidence locations: §3–5 pp.3–6, Tables4–11 pp.8–11, §8 p.12.

**2610.04672 · MASBench: Benchmarking LLM-based Multi-Agent Collaboration under Partial Observability**

[Paper](https://arxiv.org/abs/2610.04672)

- **agent**: MASBench splits Hotpot evidence, schedule constraints, and resource maps among partially observing agents to test memory/protocol/routing compositions. Official tasks and runner unverified; defer same-name integration.
  Reproduction scope: Communication cost counts cross-agent messages, not local reasoning. Maintain runtime information isolation; do not give joint gold or all constraints to each agent. Report normalized scores and per-thousand-token efficiency separately.
  Evidence locations: §3.1–3.2; §4.1–4.3; §5.1

**2610.04504 · The Same Zero: Why Identical ASR Can Imply Different Guarantees in LLM-Agent Security**

[Paper](https://arxiv.org/abs/2610.04504)

- **agent**: The Same Zero categorizes VAL guarantee sources and evaluates zero stability under attack escalation and actual agent effects. Full AgentDojo banking comparisons and failure mechanisms are reported.
  Reproduction scope: Main testbed and action receipts unverified. Per-task banking traces were lost and shipped gate fields fixed, preventing exact old statistics. Equal zero ASR does not mean equal safety. Disclose the 25% utility collapse.
  Evidence locations: §6.1/6.5; Appendix A.4/A.6; normalized p11,53–54,93

**2610.04441 · LocusRL: Diagnosing LLM Reward and Policy Interventions in Competitive Games**

[Paper](https://arxiv.org/abs/2610.04441)

- **post-training**: LocusRL's five-layer learner/reward/execution/evidence audit and terminal replay certificates can diagnose failures. One repair establishes sufficiency for that state; 20 certificates are not 20 independent states. LocusRL-Pub failed twice; direct HTTP 404. Await code.

**2610.04378 · COPEX: Benchmarking LLM Robustness to Adversarial Context Across Model Context Protocol Layers**

[Paper](https://arxiv.org/abs/2610.04378)

- **agent**: COPEX isolates 25 MCP attack entry types across agent/client/server/transport with 125 scenarios and independent oracles. Complete official scenario package unavailable. Formal integration deferred.
  Reproduction scope: Response scanning occurs after execution and cannot undo side effects. Schema checks only registration and fail open. LLM judges for 15 attack categories are not objective ground truth. One defense run per variant. Authorized isolated fictional canaries/local tests only; ASR is not real exploitability.
  Evidence locations: §3 observation boundary; §4.1–4.3; §5.1; §6 limitations

**2610.04302 · From Valid to Useful: Post-Verification Acquisition for Recursive Self-Improving Recommendation**

[Paper](https://arxiv.org/abs/2610.04302)

- **recommendation**: DA-RSIR uses MC dropout and disagreement buckets to collect data for validated policies, with four datasets and three offline models. §7 says no online evaluation. Keep as an RSI lead; industrial implementation needs exception approval.

**2610.04255 · Grounded in Time: A Multi-Source Dataset and Benchmark for Temporal Grounding in Robotic Manipulation**

[Paper](https://arxiv.org/abs/2610.04255)

- **foundation-model**: Grounded-in-Time uses previous-episode video and counterfactual A/B scenes for history-semantic manipulation, evaluated in ManiSkill3 and real hardware. No official data/environment task bundle located for faithful replay.
  Reproduction scope: π0.5 without prior history is not evidence of worse memory structure. 60 simulator and ten real runs per task; pairs scored casewise. Require real execution, SR and stage PSR; do not use historical answer labels to generate actions.
  Evidence locations: §III-A–D; §IV-A/C/D; TableV

**2610.04246 · Benchmarking Psychological Dynamics in Generative Agents**

[Paper](https://arxiv.org/abs/2610.04246)

- **agent**: PsyDyBench gives different models six days of common-event narratives for 300 synthetic personas and compares within/between-person variance, associations, and human norms. Useful diagnosis; official repo inaccessible, integration deferred.
  Reproduction scope: Six-day autoregression has short-panel bias. Four metrics do not identify one factor, so feature spectra are used. Shared LLM narratives are not human longitudinal data. Directional agreement is not quantitative fidelity or individual diagnosis/prediction.
  Evidence locations: §3.1–3.3; §4; §6/reproducibility

**2610.04156 · Trajectory-Derived Confidence for Reliable, Resource-Aware Clinical Text-to-SQL Agents**

[Paper](https://arxiv.org/abs/2610.04156)

- **agent**: Sentinel uses two ModernBERT heads to predict answerability and correctness from questions and trace prefixes. Calibration selects exit gates, isotonic mapping, and early stopping. Serving abstains by Chow λ/(1+λ).
  Reproduction scope: EHRSQL/MIMIC-III need controlled access; original training traces and heads were not found. Template split 6179/2160/2101, official test untouched. Judge disagreement on 26% of hard cases, one training seed, and heads retrained per agent. Short templates partly explain near-perfect answerability. Await data/traces; no invented SQL reward.
  Evidence locations: §3.1–3.4, §4.1, Limitations, Appendix I.

**2610.03935 · General Decision Models: Benchmarking and Insights Beyond Jev**

[Paper](https://arxiv.org/abs/2610.03935)

- **foundation-model**: InnerJev's Reasoning-to-Readout Self-Distillation is a new algorithm, not only JEVal. Verified two self-reasoning soft targets, frozen output layer, one epoch, and independent dev checkpoint selection. Main comparisons mix scale and training sources; matched-budget alternative distillation loss not confirmed. Needs evidence, not benchmark-only dismissal.
  Evidence locations: §4.1; §6.1–6.3; Appendix F.2/Table42; Appendix F.3; Appendix F.4/Table43

**2610.03902 · When Evidence Changes: Evaluating Memory Repair and Re-reading in Language-Model Agents**

[Paper](https://arxiv.org/abs/2610.03902)

- **agent**: Versioned dependency memory uses snapshot/read-set transactions for revocation and replacement. Compares reread, cache, rebuild, local repair, quarantine, and no propagation, constraining answers via source allowlists.
  Reproduction scope: eICU demo is public but scenarios, traces, and code are promised after acceptance. Only 3–20 patients per cell, post-hoc lexical scorer, same-patient reuse, and some preregistration omissions. Not causal repair evidence. Gold support is scorer-only; source-filtered reread is a matched-information control.
  Evidence locations: §3–5, §6.2–6.5, §8, Appendix A/B.

**2610.03525 · Structured Composition of Verifiable Atomic Insights for Table-to-Report Generation**

[Paper](https://arxiv.org/abs/2610.03525)

- **agent**: ComInsight enumerates atomic insights via SQL grammar, uses calibrated statistics and an SFT+DPO interestingness judge, then typed graphs, Leiden communities, and causal paths to produce SQL-provenanced reports.
  Reproduction scope: The judge needs 1,200 labels and 600 preference pairs, with no original training bundle/checkpoint located. Generic judges or hand scores do not reproduce it. Granger and LLM mechanisms form hypotheses, not interventional causality. Deduplicate 290 calibration/training cases from test; freeze top-50 and thresholds on validation.
  Evidence locations: §IV.A–D, §V, Appendix B.

**2610.03476 · MobiAgent: Dual-Loop Recursive Policy Self-Improvement for Long-Horizon Mobile Manipulation**

[Paper](https://arxiv.org/abs/2610.03476)

- **agent**: MobiAgent combines a receding-horizon VLM planner, shared VLM and skill-specific flow experts, and visual-critic retry/replan. The outer loop verifies segments, clusters skills, and fine-tunes on actual rollouts.
  Reproduction scope: BEHAVIOR-1K/RoboCasa simulation, Astribot hardware, and full π0.5 action training are not text fixtures. Code URL exists; policy weights and curated startup data were not located. Wait for runnable sim assets. Real action capability needs execution, not roadmap registration.
  Evidence locations: §3.1–3.2, §4, Appendix prompts/case studies.

**2610.03421 · CLIMB: Confidence-Guided Complementary Evidence for Multimodal Retrieval-Augmented Generation**

[Paper](https://arxiv.org/abs/2610.03421)

- **foundation-model**: CLIMB fixes an MMR evidence pool, uses R/E/C critics, reranks within it for up to three rounds, and accepts only strictly higher confidence. Relevant, but the visual critic interface with the specified text-only Llama3.1-8B is unclear and code unavailable.
  Reproduction scope: Confidence is relative self-scoring, not calibrated correctness. Count repeated critic/facet calls; multi-round versus single retrieval is not an efficiency comparison. If reporting InfoSeek validation, select on separate dev and freeze splits. Clarify the visual interface before implementing.
  Evidence locations: §3.2–3.4 Eq1–4; §4 implementation; Limitations; Appendix prompts

**2610.03356 · ReFract: Benchmarking Perspective Awareness in Language Model Agents with Text World Models**

[Paper](https://arxiv.org/abs/2610.03356)

- **agent**: ReFract builds industrial maintenance text worlds with expert Pred/Cap/Know and consume/produce relations. Separates authority and knowledge; QTS/FTS test perspective-aware action execution.
  Reproduction scope: No public package of 150 expert transcript tasks and domain/goal data. Handwritten solutions are not the benchmark. Gold goal only to judge; check dependencies and role gates per step. Five small industrial roles are not general agency or industrial gains.
  Evidence locations: §3.1–3.3, §4–5, Appendix A/F.

**2610.03324 · To Jev or Not? Evaluating the Accuracy and Efficiency of Structured Decision Models for Hate-Speech Moderation**

[Paper](https://arxiv.org/abs/2610.03324)

- **foundation-model**: HateDecide is not new JEV training, but definition adherence, grouped deduplication, and threshold calibration can serve decision evaluation. Full prompts/data protocol described, executable code or frozen artifacts not found. Integration awaits public materials.
  Reproduction scope: Four existing English datasets with unknown pretraining exposure. Preserve Dynamic perturbation groups across splits; choose thresholds on 200 validation examples only, never test gold for the model.
  Evidence locations: §3.1–3.4; §5; Appendix prompts; Appendix threshold-tuned control/Table11

**2610.03252 · COSMI: COmpositional Synthesis of Multi-object Interactions**

[Paper](https://arxiv.org/abs/2610.03252)

- **foundation-model**: COSMI combines, mirrors, and geometrically filters single-object human motions with contact to train text-conditioned diffusion with shared object slots. Evaluates unseen objects and five unseen compositions. Method is specified; data/model are only promised.
  Reproduction scope: Deferred; public access to 222k sequences, release pipeline, and checkpoints unverified. Arbitrary stitching or toys do not reproduce contact screening and composition isolation. Source motion data are license-restricted.
  Evidence locations: §3–5; Appendix C/D

**2610.03195 · Source Preference in the Wild: How LLM Agents Favor Items by Source, and How to Reduce It**

[Paper](https://arxiv.org/abs/2610.03195)

- **post-training**: Matched request satisfaction, cyclic Latin-square position controls, and BT-Davidson source preference define a standalone diagnostic with URL visibility and permutation interventions. Code/data are promised upon publication. Not yet a public executor; refer to agents.
- **agent**: Empirical source-preference interventions in search and prompts, not a standalone algorithm.
  Evidence locations: Title and complete abstract

**2610.03153 · EvoRiskBench: An Evolving Benchmark for Runtime Security Risks in Workspace Agents**

[Paper](https://arxiv.org/abs/2610.03153)

- **agent**: EvoRiskBench constructs and refines executable cases across nine entry points by five effects. Sandbox and external events/state corroborate technical risk. Freezes 450 cases across nine model/harnesses.
  Reproduction scope: Cases and platform await artifact safety release; cannot replay all 450. Synthetic businesses/mock credentials are sandbox-only. Report ASR alongside TSR. Judge severity is not real-world harm; traces do not substitute for side-effect evidence.
  Evidence locations: §3.1–3.3, §4, §5, artifact statement.

**2610.03135 · Page-EntroKV: Hardware-Aligned, Entropy-Weighted KV-Cache Eviction under Grouped-Query Attention**

[Paper](https://arxiv.org/abs/2610.03135)

- **foundation-model**: Page-EntroKV uses sink-removed Rényi-2 entropy to weight attention in GQA groups and budgets physical pages. Identifiable mechanism, but public evidence conflicts with paper system claims. Not a mature implementation candidate.
  Reproduction scope: Official repo shows N180 Jaccard 0/UOR 1, not 4.75× bloat. Sinks only in ten layer-0 heads. NIAH lengths only 958/1474/1990. LongBench has four completed and eleven blank rows, no dense baseline. No 8/32/64 page sweep or serving table. Reconcile version and evidence; cache-mask diagnostics do not establish end-to-end gains.
  Evidence locations: §4.1–4.2; §7–8; official README evidence scope

**2610.03056 · MOF-VERIFY: A Failure-Aware Agentic Harness for MOF Hypothesis Verification**

[Paper](https://arxiv.org/abs/2610.03056)

- **agent**: MOF-Verify uses identity and CIF-digest lookup, verified local DOI text extraction, evidence sufficiency, and deterministic verdict routing. Where computation is needed, run actual SevenNet with precision, seed, and convergence recorded.
  Reproduction scope: Benchmark is public, but trusted experimental CIF/CSD may be licensed; expert-local text and curated alias corpus release unverified. T4 needs MLIP rather than fixed properties. Oracle evidence is a ceiling, not retrieval quality. Separate Yes/Re-run/Human-review from literary Yes/No/Uncertain.
  Evidence locations: §3, §4.1–4.2, Appendix A.5.

**2610.03055 · hacktrace: behavior-supervised detection of reward hacking during code generation**

[Paper](https://arxiv.org/abs/2610.03055)

- **agent**: HackTrace supervises generation residual readouts with problem-disjoint action/outcome labels. Problem-group CV selects 88 linear readouts and top-8 MultiMax at layers 18/24, with final AST features. GRPO penalty discourages shortcuts.
  Reproduction scope: https://github.com/XXXX/HackTrace is a placeholder; heads, activations, and GRPO labels are planned, not available. Hidden oracle is evaluation-only. Prefix prediction of final labels is not harm already committed. In editable-test positives, 98.2% changed tests. Report strong penalties with honest-correct and cost metrics.
  Evidence locations: §3.1–3.4, §4.4, §5, release statement.

**2610.03025 · Verifiable, Articulable, and Tacit Components of Preference**

[Paper](https://arxiv.org/abs/2610.03025)

- **recommendation**: VAT/Creative Preferences is a preference post-training method, not rejected under industrial recommendation A/B rules. Referred to post-training.
- **post-training**: Read v2 pp. 1–16 and data inventory p. 32 and compared with v1. Verifiability gap changed from VAT−V in the v1 abstract/introduction to VA−V; articulability remains VAT−VA. Pipeline still uses four metric discovery routes, fidelity optimization, capture–recapture bounds, and nuisance audits. Of 42 tasks, 2.8M texts, and 317M preference acts, only 16M are individual decisions/comments/votes; the rest aggregate engagement, not 317M annotators. LoRA single seed per task, grouped 80/10/10, generated-text portion cross-model ranking without RL. Release statement does not establish a downloadable dataset or runner. Deferred after full-text review.

**2610.02878 · Evaluating VQA in Vision Language Models using Cooperative Principles**

[Paper](https://arxiv.org/abs/2610.02878)

- **foundation-model**: Grice uses visual/relational modifiers for semantically invariant VQA controls with three-person adjudication. Main open-answer metric depends on new AMT ratings; anonymous data release and automatic scoring scope are unverified.
  Reproduction scope: Total 995 conflicts with 438+42+493 category counts. Do not replace human preferences with original-answer automatic scoring. Control independent sessions when rewriting and answering use the same model, and sampling uncertainty. Defer unified evolve integration.
  Evidence locations: §3/3.1; §4–5; §7

**2610.02549 · Evaluating Multi-Dimensional Generalization of Large Language Models in Temporal Extraction Tasks**

[Paper](https://arxiv.org/abs/2610.02549)

- **foundation-model**: TimeBank/i2b2 timex/eventx cross-domain, perturbation, and length diagnostics with Hungarian-LCS are useful. Clinical data are restricted and complete variants/splits/scorer unavailable. No direct unified integration.
  Reproduction scope: Target-containing sentences omit empty outputs. Dense and MoE active parameter counts such as 8B/17B are unmatched, limiting architectural causality. Isolate few-shot examples from test documents. Surface spans are not advanced temporal reasoning.
  Evidence locations: §2.1–2.4; §3 model architecture; Limitations

**2610.02521 · Spatial Memory Intelligence: Endowing World Models with Understanding-Driven Long-Term Memory**

[Paper](https://arxiv.org/abs/2610.02521)

- **foundation-model**: Spatial Memory Intelligence trains spatial clustering, sparsification, action retrieval, and reliability filtering in an MLLM to control HY1.5/Wan2.2 long-video memory. Full text reviewed; action supervision and benchmark promised.
  Reproduction scope: Public release of 100 demonstrations and roughly 1,000 cleaned rollouts unconfirmed. Handwritten rules do not replace learned memory. VBench/GPT judges and revisit reconstruction do not establish full generation quality.
  Evidence locations: §4.3–4.4; §5.1–5.5; §7; Appendix F

**2610.02241 · Hardware-Native Joint Sparse-Quantization for Trillion-Scale Mixture-of-Experts**

[Paper](https://arxiv.org/abs/2610.02241)

- **foundation-model**: moesq jointly learns Gumbel support patterns and quantized values with router-weighted expert reconstruction. Paired 4:8 NVFP4 and Blackwell SpTC grouped kernels define the method. A100/A30 cannot validate that native path.
  Reproduction scope: SGPTQ initialization 512×4096, refinement 8192, validation 128 from the same mixture. Freeze the router, cache expert inputs, and calibrate layerwise on compressed prefixes. CPU/CUDA fake quantization is a diagnostic, not native NVFP4 sparse MMA. B200 verification still needed; A100 is not equivalent.
  Evidence locations: §3.1–3.4 Eq1–5; §4; Appendix B/D.1

**2610.01908 · Same Reward, Different Skills: When Multimodal RL Learns to Look**

[Paper](https://arxiv.org/abs/2610.01908)

- **post-training**: Counterfactual scene generation, stable/switch/invariance target controls, and an independent confirmatory set form visual-grounding evaluation. Standard GRPO trains discovery only. Anonymous code inaccessible; verify public scene generator and frozen dev/test. Benchmark gains are not evidence of visual dependence.

**2610.01833 · Continuous Process-Level Evaluation for Evolving Enterprise AI Agent Skills**

[Paper](https://arxiv.org/abs/2610.01833)

- **agent**: Enterprise-skill evaluation derives oracles through independent APIs, runtime placeholders, rule and limited LLM judging, and dependency attribution, separating process and outcome. Current scope is nine real apps and two private Instana/Kubecost/Cloudability skills, with 104/80 templates. 240 MD/TXT trials also change content; live APIs drift and graph roots are not causal. No complete public templates/traces/environment. Reviewed but not a public regression entry point.
  Evidence locations: Title and complete abstract

**2610.01794 · Continuous Conditioning of VLAs with Augmenting EMG and Visual Task Descriptors**

[Paper](https://arxiv.org/abs/2610.01794)

- **foundation-model**: EMG/vision-conditioned VLA concatenates low-pass EMG and proprioception; RoboCasa conditions actions on object masks. Defined design, but real three-person EMG is private.
  Reproduction scope: Real EMG and author training code were not found. Continuous human correction is not autonomy. RoboCasa segmentation is a privileged mask, not fair vision-only gains.
  Evidence locations: §III-A/B; §IV-A/B; §V; Appendix VI-B/C

**2610.01138 · Auditing Action Settlement in LLM Agent Environments: Order, Progress, and Replay**

[Paper](https://arxiv.org/abs/2610.01138)

- **agent**: Typed proposals freeze a snapshot and use five arbitration strategies. Position order invariance assumes a single move and unique occupancy, not all-state fairness. 2,160 scripted episodes include independent oracles/replayed faults, but LLM archives lack real conflicts and the pilot is imbalanced. Artifacts are local, not public. Not a new synchronization architecture; regression harness deferred.
  Evidence locations: §2.1–2.3; §3.1/3.4–3.5; §4

**2610.01066 · Probe with Participation Trophies: Random-Reward RL as a Probe of LLM Capability**

[Paper](https://arxiv.org/abs/2610.01066)

- **post-training**: Random-reward checkpoint diagnostics cross fixed rollouts with 16 paired replicates and task/reward/input controls, not a new capability algorithm. Official rl-random-prob is explicitly empty. Wait for public scripts/data.

**2610.01042 · Beyond Final Accuracy: Auditing Communication in LLM Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.01042)

- **agent**: ICR freezes three original agent traces and six directed one-hop revisions. Gold is used offline for four correctness strata, with a no-message control. Report CR/PR/SR/SCR separately; SI conflates retention and copying. 430 questions/2,580 events select at least one mistake. Acc† imputes unobserved outcomes; incomplete latent costs do not show speedup. Useful evaluation, but anonymous repo timed out and tasks/code/license cannot be verified.
  Evidence locations: §3.1–3.3; §4.1; Appendix G and costs; Reproducibility.

**2610.00969 · A Citation-Grounded Benchmark for Trustworthy Earnings Call Transcript Analysis with Large Language Models**

[Paper](https://arxiv.org/abs/2610.00969)

- **foundation-model**: ECTs-100 normalizes number type/value/unit across claims, citations, and context, separating grounding and correctness. Full transcripts, tasks, and runner unavailable; defer integration.
  Reproduction scope: Defaulting empty number sets to 1 inflates scores; report coverage. Equal values across different entities/periods are not entailment. No expert calibration; one GPT-4.1 backbone with six configurations. Auto-generated gold is not financial expertise. Aggregate by document and split by company.
  Evidence locations: §2.2–2.4; §3.2–3.4; Appendix A

**2610.00855 · Lang3DSeg: Annotation-Free Open-Vocabulary 3D Segmentation with Point Transformers**

[Paper](https://arxiv.org/abs/2610.00855)

- **foundation-model**: Lang3DSeg filters SAM3 text-ensemble masks with LiDAR occlusion and multiview consistency, then supervises PTv3 with weighted CE/Lovasz/CLIP. Raw nuScenes/SemanticKITTI are public.
  Reproduction scope: github.com/<org>/Lang3DSeg is a placeholder and release is promised after acceptance. Pseudo-label filtering artifacts are missing. Ground-truth classes cannot replace language pseudo-labels.
  Evidence locations: §III-A–C; §IV-A–D; §V

**2610.00825 · Align Then Reason: A Multimodal Lip-Sync Judge for Dubbing**

[Paper](https://arxiv.org/abs/2610.00825)

- **foundation-model**: ATR aligns visual mouth shapes and phonemes via monotonic AutoAVSR/XPhoneBERT CTC and learns a local soft-token judge with scalar calibration. Defines 50k multilingual dialogues and 2,100 tests.
  Reproduction scope: Custom dubbing and expert-rated data/code unverified. Unseen languages calibrate with 300 genuine target clips, not zero-shot without target data. Separate Hungarian block matching from single-clip scores.
  Evidence locations: §2.1–2.3; §3.1–3.5; Appendix A/B

**2610.00673 · Closing the Loop: Practical Training Recipes for Looped Language Models**

[Paper](https://arxiv.org/abs/2610.00673)

- **foundation-model**: Closing the Loop has an executable conversion recipe: single-scalar input reinjection and smooth-exit-weighted LM loss. Full text reviewed; equal data/steps do not match training FLOPs. Additional recurrent training cannot be attributed solely to the algorithm.
  Reproduction scope: From-scratch LoopLM uses 9.9e21 FLOPs vs same-parameter dense 2.5e21 and 3.9B dense 7.1e21. Comparing 310B tokens with Ouro's 7.7T does not isolate architecture.
  Evidence locations: §3.1–3.6; §4.1–4.5 Eq1–2; §5.3/Table4; Appendix I/Table21

**2610.00636 · CompMat-Bench: Benchmarking AI Agents for Computational Materials Science**

[Paper](https://arxiv.org/abs/2610.00636)

- **agent**: CompMat derives 94 tasks from reproducing 65 steps across 15 studies. Separates precomputed HPC from actual workflows, four guidance/span settings and eight workflows, isolated gold/graders and fixed rules. Strong models saturate single tasks with full guidance; workflows need 128 CPUs, 239GB, and 5h. Full/reduced identical for 42 tasks, hardware unmatched. Official page says code/data forthcoming; no public execution. Deferred.
  Evidence locations: §3.1–3.3; §4; §5; §6; author project page.

**2610.00609 · Legal Research Bench: Measuring End-to-End Reliability in Long-Horizon Legal Research Agents**

[Paper](https://arxiv.org/abs/2610.00609)

- **agent**: LRB413 uses attorney questions with as-of dates and all-pass rubrics (any invalid citation fails), five public/200 val/208 test. Judge calibrated on 15 questions/45 responses; single trial does not estimate variance. Public repo has five samples and harness only; platform approval and VALS key required for 408 private questions. Deferred without authorization.
  Evidence locations: §3.1–3.3; §4.2; §6; official README Platform.

**2610.00465 · AIR-LLM: Broadcasting AI Weights over Radio for Memory-Free Edge LLM Inference via RF Computing**

[Paper](https://arxiv.org/abs/2610.00465)

- **foundation-model**: AIR-LLM implements GEMV with wireless weight broadcast, RF multiplication, and calibration units. Specialized RF hardware and curves are necessary; GPU cannot establish hardware results.
  Reproduction scope: Sionna ray tracing models city propagation; wired noiseless RF mixer errors are measured then injected. Two default users are selected at about 4/3 ENOB, not a population distribution. Simulated noise injection is not real wireless LLM reproduction.
  Evidence locations: §3 RF engine/calibration; §4.1–4.2; §5.1

**2610.00425 · Code That Works, Environments That Don't: Measuring Environment Reproducibility in AI-Generated Software**

[Paper](https://arxiv.org/abs/2610.00425)

- **agent**: Gen→Repair repairs up to ten times in clean Docker and compares initial declarations, final installs, and ptrace-observed loaded dependencies.
  Reproduction scope: 50×4×3 main instances and 400 repeats were run manually. Open materials promised; task bundle unavailable. Dynamic loads cover executed paths only and omit C++ header-only dependencies. C++ transitive=1 is a definition, not model improvement. Await official tasks, containers, and parser.
  Evidence locations: §2–5, §6.6.

**2610.00316 · DuplexSpeechBench-Document Grounding: Benchmarking Document Grounding and Hallucinations in Voice Agents**

[Paper](https://arxiv.org/abs/2610.00316)

- **agent**: DSB-DG includes 50 documents, 1,636 QAs, and 20 dialogues. Fixed evidence with increasing context tiers, probe–distractor–repeat, and different refresh rates compares speech grounding and latency.
  Reproduction scope: Need official QA/audio/dialogue/scorer bundle, not just project page. Truth is judge-only. Near-zero GDS depends on initial GA; FTED is speech-end to first token, not full voice latency. Track context injection and ASR errors separately.
  Evidence locations: §2–4, Appendix B–E/H.

**2610.00197 · Comedic Fool's Gold: Reward Exploits and Countermeasures in Conversational Humor**

[Paper](https://arxiv.org/abs/2610.00197)

- **post-training**: Humor reward audit covers laughter, speaker-wide normalization, and concurrent scorer noise. Small taste gain disappears after instrument correction and token loopholes remain. No public data/runner found; internal archival is not public execution.

**2610.00092 · BudgetSchemaBench: A Budget-Swept Diagnostic for Schema Context in Text-to-SQL**

[Paper](https://arxiv.org/abs/2610.00092)

- **agent**: BudgetSchemaBench's budget sweeps, namespace checks, and execution scoring fit evolve. Official repository contains only a 339-byte README saying code is under organizational review. Public execution blocked.
  Reproduction scope: Guaranteed-gold context is diagnostic only. 94.6% after removing gold tables suggests, but does not prove, contamination. ≤2 pp serialization with ±4 CI is not equivalence (δ3 TOST failed). Paper's BSD3 release conflicts with license=null and absent runner/manifest.
  Evidence locations: §3; §4 Tables4–5; §5; official README.MD and contents API 2026-10-07.

**2610.00054 · The First Token Is Not the Verdict: Hidden Costs of Reading LLM Judges Without Generating**

[Paper](https://arxiv.org/abs/2610.00054)

- **recommendation**: First-token LLM judge position-bias audit belongs to post-training evaluation, not recommendation online research.
- **post-training**: First-token compliance checks and conditional generation are a reusable judge protocol. 1,678/11,596 require generation; 85.5% saved, but compliant subsets have 0–5.5% readout error. First token is not always final judgment. Public code and predictions unavailable; not integrated.

**2610.00015 · From Proposal to Verified Effect: Praxa, an Evidence-Bound Harness for Governed AI Agent Execution**

[Paper](https://arxiv.org/abs/2610.00015)

- **agent**: Praxa uses model proposals, deterministic authority gates, broker execution, and readback evidence bound to state. Protected/resource gates validate recursive specialist candidates.
  Reproduction scope: Core executor is private and missing from the public SDK. Terminal-Bench 12-task pilot has fixed order, asymmetric rebuild, and incomplete verifier budgeting. Recursive topology is a synthetic proxy; optimizer not run. Zero HOLD confirmations. Wiring alone is not measured improvement. Await core code or permission.
  Evidence locations: §3–6, §8–11.


## Rejected or out of scope (367)

**2610.08781 · IdeaAnchor: Teaching LLMs to Turn Literature into Research Ideas**

[Paper](https://arxiv.org/abs/2610.08781)

- **post-training**: The paper concerns anchor data and privileged supervision; it uses standard SFT, self-training, and GRPO. It may be an agent research-data method but is not a core optimizer implementation. This applies only to core post-training; the Agent track independently reviews methods and public artifacts rather than rejecting globally.

**2610.08668 · Semantic Behavioral Watermarking: Paraphrase-Robust and Forgery-Resistant Provenance for LLM Agents**

[Paper](https://arxiv.org/abs/2610.08668)

- **agent**: SBW uses semantic clustering, a history-keyed PRF, and an abstention margin to watermark agent behavior for attribution. It optimizes attribution detection rather than planning, learning, tools, or task ability, so it is outside this capability round.
  Reproduction scope: §7 explicitly states ToolBench provides no environment execution feedback. Copy and chain replay are unresolved. Utility measures agreement between actions and argmax, not task success. Some robustness artifacts were not retained.
  Evidence locations: §3 threat model；§4.1–4.3；§5；§6.1/6.3/6.4 Tables2/4/5；§7

**2610.08651 · A Case Study in Assuring AI-Written Software**

[Paper](https://arxiv.org/abs/2610.08651)

- **agent**: A medical-software governance case study with no independent agent algorithm.
  Evidence locations: Title and complete abstract

**2610.08630 · Towards In-Parameter Memory Augmentation for Large Language Models**

[Paper](https://arxiv.org/abs/2610.08630)

- **agent**: A parametric-memory survey with no new core algorithm.
  Evidence locations: Title and complete abstract

**2610.08561 · Reinforcement Learning for Hierarchical Reasoning Rewards: Minimax-Optimal Rates with Transformers**

[Paper](https://arxiv.org/abs/2610.08561)

- **post-training**: Defines a depth curriculum and prefix-adaptive actor–critic queries and proves minimax rates in a formal setting. Actual LLM training benchmarks were not verified, so no capability reproduction.

**2610.08539 · RSJEV: Discriminative Remote Sensing Scene Classification with Multimodal Large Language Models**

[Paper](https://arxiv.org/abs/2610.08539)

- **foundation-model**: RSJEV adapts existing JEV/Mapika-style candidate-conditioned single-token readout and CE+Brier to remote-sensing classification. Full text did not identify a distinct core training mechanism beyond registered LLM2Jev or Decider, so this is domain reuse.
  Evidence locations: §I–III；§IV.A–E；TableII

**2610.08528 · MedCORE: Criteria-Grounded Clinical Reasoning for Interpretable Medical Image Diagnosis**

[Paper](https://arxiv.org/abs/2610.08528)

- **foundation-model**: MedCORE is a clinical-standards graph network for skin, ultrasound, and retinal diagnosis. It is a domain application rather than general foundation-model methodology.

**2610.08482 · Knee3DVLM: Dual-Sequence Full-Volume Vision-Language Modeling for Comprehensive Knee MRI Assessment**

[Paper](https://arxiv.org/abs/2610.08482)

- **foundation-model**: Knee3DVLM models 57 diagnostic targets from two knee MRI sequences. This is a specific medical application.

**2610.08430 · NeMo-DCR: Bit-Exact Delta-Compressed Refit for Scalable Agentic RL at Trillion-Parameter Scale**

[Paper](https://arxiv.org/abs/2610.08430)

- **agent**: NeMo-DCR synchronizes weights with exact delta transfer, a training infrastructure contribution rather than an agent policy.
  Evidence locations: Title and complete abstract

**2610.08407 · Seeing the Context: Enhancing Recommender Systems with Image-Derived Contextual Signals**

[Paper](https://arxiv.org/abs/2610.08407)

- **recommendation**: ICE-Fuse reports RMSE and ablations on TripAdvisor image/text context without online traffic experiments or deployment evidence required for industrial search/ads/recs.

**2610.08337 · Machine Learning for German Redispatch Forecasting under Data Delays and Temporal Distribution Shift**

[Paper](https://arxiv.org/abs/2610.08337)

- **foundation-model**: Probabilistic forecasting comparisons for German grid redispatch belong to energy time-series applications.

**2610.08331 · Transferable Spatial Temporal Coherence Adversarial Attack on Black-Box Vision Language Models for Autonomous Driving**

[Paper](https://arxiv.org/abs/2610.08331)

- **foundation-model**: Transfer attacks against autonomous-driving video VLMs primarily contribute attack construction, not foundation-model capability training or inference.

**2610.08300 · Memory Depth and Reconstructed Context Width: A Controlled Evaluation of Hierarchical Retrieval**

[Paper](https://arxiv.org/abs/2610.08300)

- **foundation-model**: Controlled hierarchical conversational retrieval depth/context-width experiments are system diagnostics, not a new foundation-model algorithm.

**2610.08245 · Aligning Performance with Contribution: Towards Contribution-Aware Fair Recommendation**

[Paper](https://arxiv.org/abs/2610.08245)

- **recommendation**: CPFR evaluates contribution fairness offline on MovieLens 100K/1M and Amazon Office. Fairness loss effectiveness is not industrial online evidence.

**2610.08232 · Behavior-Mining, Generative Conversations, and Collaborative Advisory: the Future of Travel and Tourism Recommender Systems**

[Paper](https://arxiv.org/abs/2610.08232)

- **recommendation**: A travel recommendation position/survey paper proposing future advisory directions, not a reproducible new algorithm and experiment.

**2610.08208 · STRUCTURALCOST: A controlled reading time dataset for modeling human sentence processing difficulty**

[Paper](https://arxiv.org/abs/2610.08208)

- **foundation-model**: STRUCTURALCOST provides human syntactic reading-time data without a direct executable foundation-model capability/Evolve task.

**2610.08200 · Finding the Heads and the Neurons Responsible for Network Information Retrieval in Language Models**

[Paper](https://arxiv.org/abs/2610.08200)

- **foundation-model**: Locating entity retrieval in attention heads and neurons is interpretability, without a standalone executable capability benchmark.

**2610.08136 · Adapting Generative Recommenders for Multi-Turn Interaction**

[Paper](https://arxiv.org/abs/2610.08136)

- **recommendation**: INTEGER generates multi-turn conversations with Amazon Beauty/Toys and Tencent Hy3 and reports offline hit rate, NDCG, and dialogue quality without production control experiments.

**2610.08129 · Do LLMs Act on What They Know? From Partner Representations to Cooperative Actions**

[Paper](https://arxiv.org/abs/2610.08129)

- **recommendation**: Hanabi collaboration conventions belong to Agent review, not industrial search/ads/recs.
- **agent**: Hanabi is a controlled knowing–doing diagnostic for receiving decisions, not full autonomous collaboration. Retain as a negative reference for oracle or representation leakage, not capability implementation.
  Reproduction scope: Do not count oracle rules or code-to-action translation as evaluated agent ability. Activation experiments use only Qwen3-8B and recorded states. Full-game gains are not established and executable public benchmark/code was not located.
  Evidence locations: §3.1–3.3；§4.1–4.3；§5.1/5.7；AppendixI/Limitations

**2610.08097 · When Tools Lie: Reliability of Mathematical Agents Under Corrupted Tool Feedback**

[Paper](https://arxiv.org/abs/2610.08097)

- **agent**: Compares broken tools and verification frequency on 31 math tasks. The authors explicitly could not control verifier quality across comparisons.
  Evidence locations: Title and complete abstract

**2610.08090 · Explainable Rule Mining of IPv6 Extension-Header Presence Patterns from Paired-Vantage Captures**

[Paper](https://arxiv.org/abs/2610.08090)

- **foundation-model**: Negative network-measurement results on mining IPv6 extension-header rules are not foundation-model algorithms.

**2610.08082 · POLAR: Ontology-Guided Risk Prevention for Tool-Calling LLM Agents**

[Paper](https://arxiv.org/abs/2610.08082)

- **post-training**: Inference guardrails use a reversibility ontology and action pruning without updating weights or RL/distillation objectives; refer to Agent review.
- **agent**: POLAR is not queued for capability or safety improvement. Its human-authored Datalog reversibility ontology uses weak-chain minimum scoring and veto, but gains cannot distinguish structural reverse search from blanket veto. Core implementation, ontology, and logs are private, and original configuration cannot be traced.
  Reproduction scope: Escalate/Advisory archive means conflict with the table, so withdraw that comparison. Arms filter errors separately and adaptation compute is unmatched. Reversibility is neither authorization nor safety. Keep the negative-control value without claiming execution passed.
  Evidence locations: §3.2–3.6 Eq1；§4.1–4.6 Tables3–6；Limitations/Resource declaration

**2610.08068 · PhysTacGen: Physics-Aware Visual-Tactile Sensor Image Generation**

[Paper](https://arxiv.org/abs/2610.08068)

- **foundation-model**: PhysTacGen generates tactile sensor images from vision, chiefly a domain-specific robotics modality pipeline. Its post-training mechanism can be reviewed by that track.

**2610.08018 · Structured but Silent: Probing Capability Requirements in LLM Hidden States**

[Paper](https://arxiv.org/abs/2610.08018)

- **agent**: TACIT uses linear hidden-state probes to diagnose capability requirements, not an execution policy.
  Evidence locations: Title and complete abstract

**2610.07982 · M3SunAgent: Monocular 3D Spatial Understanding Agent for Metric Depth Estimation and 3D Visual Grounding**

[Paper](https://arxiv.org/abs/2610.07982)

- **foundation-model**: M3SunAgent coordinates tools for 3D spatial planning and belongs to the Agent track.

**2610.07966 · Feature Encoding in VAE-based Audio Decoders: Effects of Input, Depth and Distribution**

[Paper](https://arxiv.org/abs/2610.07966)

- **foundation-model**: RAVE/EnCodec feature probes and clustering are representation interpretability diagnostics.

**2610.07954 · Revisiting Numerical Forecasting Models for Language-Based Trajectory Prediction**

[Paper](https://arxiv.org/abs/2610.07954)

- **foundation-model**: MoRE transfers task-specific RL rewards for pedestrian and athlete trajectory prediction, not general foundation modeling.

**2610.07937 · Leveraging a four-quadrant approach for evaluating Redpine Science**

[Paper](https://arxiv.org/abs/2610.07937)

- **agent**: Redpine Science reports four-quadrant retrieval-service evaluation rather than a new agent algorithm.
  Evidence locations: Title and complete abstract

**2610.07913 · Multimodal Knowledge Distillation for Gastric Adenocarcinoma Classification from Whole-Slide Images**

[Paper](https://arxiv.org/abs/2610.07913)

- **foundation-model**: Gastric adenocarcinoma pathology-image distillation is a specific medical application.

**2610.07886 · ShanLiangRen: A Nutrition Agent for Personalized Daily Meal Planning**

[Paper](https://arxiv.org/abs/2610.07886)

- **agent**: ShanLiangRen combines constrained retrieval, LLM proposal/repair, deterministic nutrition calculation, and Pareto screening. It is not queued as a general agent reproduction: the 1.55M-recipe/60k-ingredient database and 300 test cases are not public, and component contributions and budget/iteration settings are not separated.
  Reproduction scope: PCS is the share of individual constraints satisfied, not clinical safety. Nutrient intervals, ingredient lists, and totals do not establish safe allergy or disease recommendations. Pareto screening is not a distinct general policy and key materials cannot be verified. Retain as an application lead without implementing medical advice.
  Evidence locations: §3 five-module System Design; §4; §5 Table1; §6

**2610.07881 · Self-Referenced Social Preferences: Cooperation without Observing Others Rewards**

[Paper](https://arxiv.org/abs/2610.07881)

- **agent**: Traditional MARL social preferences with self-referential rewards, no LLM/tool-agent method.
  Evidence locations: Title and complete abstract

**2610.07842 · Privileged Context as Drift in On-Policy Self-Distillation**

[Paper](https://arxiv.org/abs/2610.07842)

- **post-training**: Controls privileged context content × source across 27 adapters with existing lm-evaluation-harness retention tasks, token/sequence KL, and LoRA geometry diagnostics. No new independent task or scorer. Retain as OPSD risk/ablation evidence, not a core algorithm or public benchmark.

**2610.07825 · Forecast Accuracy Is Not Trading Profit: Evolving Small Recurrent Networks for Stock Return Prediction**

[Paper](https://arxiv.org/abs/2610.07825)

- **foundation-model**: Evolution of small recurrent networks for stock returns and trading is a financial time-series application.

**2610.07787 · OOPMAS: Object-Oriented Multi-Agent Systems for Query-Level Workflow Generation**

[Paper](https://arxiv.org/abs/2610.07787)

- **agent**: OOPMAS's OOP agent/workflow generation can diagnose training-time search, but headline scores reuse queries with correctness feedback and choose the better skill-on/off arm. This fails isolated capability evaluation.
  Reproduction scope: Baseline workflow incompatibility yields zero and baseline cost is estimated. The reported $35/$15 conflicts with roughly 7×. Run-local skills do not persist across deployment. Reconsider under separate train/val/test and keep oracle grades away from actors.
  Evidence locations: §3.1–3.3 Algorithm1; §4.1–4.6 Table1; Appendix A/B

**2610.07782 · Persistent Memory in Multi-Agent LLM Inference: What It Costs, What It Buys, and When You Can Tell**

[Paper](https://arxiv.org/abs/2610.07782)

- **agent**: Measurement corrections and null outcomes in persistent-memory ablations, not a standalone new policy.
  Evidence locations: Title and complete abstract

**2610.07781 · Quantization Effects on Tool-Failure Recovery Vary Across Prompts and Evaluation Designs**

[Paper](https://arxiv.org/abs/2610.07781)

- **post-training**: Prompt/scoring protocol evaluation for failure recovery by 4/8-bit agents, no training algorithm.
- **agent**: Diagnoses sensitivity of quantized agent recovery to prompts, selection, and scoring.
  Evidence locations: Title and complete abstract

**2610.07761 · Contrastive Learning for Aspect Representation towards Explainable Recommendation**

[Paper](https://arxiv.org/abs/2610.07761)

- **recommendation**: CLARER reports offline RMSE/MAE/BLEU/ROUGE on TripAdvisor HK, Yelp 2019, and Amazon Movies/TV, without online A/B or deployment evidence.

**2610.07755 · Trustworthy Method Comparison with AI Judges: Estimation and Design under Order, Batch, and Aggregation Effects**

[Paper](https://arxiv.org/abs/2610.07755)

- **foundation-model**: AI judge statistical design and Markov GLMM inference, not core foundation-model training/inference.

**2610.07730 · SanSi: A Looped Typed Decision Model for System 1.5 Thinking**

[Paper](https://arxiv.org/abs/2610.07730)

- **post-training**: The main contribution is a recurrent typed-decision architecture and per-cycle proper scoring. Refer to foundation models.

**2610.07704 · Independent Multi-Agent Reinforcement Learning with Counterfactual Semantic-Social World Models**

[Paper](https://arxiv.org/abs/2610.07704)

- **agent**: CASTLE uses independent PPO and two world models for traditional MARL without LLM agent execution.
  Evidence locations: Title and complete abstract

**2610.07668 · CACHEFORGE: LLM-Guided End-to-End Generative Cache Replacement Policy for Performance and Hardware Efficiency**

[Paper](https://arxiv.org/abs/2610.07668)

- **foundation-model**: CACHEFORGE evolves CPU hardware cache replacement with LLMs, not LLM KV caching. This is agent-assisted hardware design.
- **post-training**: LLMs generate C++ cache policies and evolve them in simulation without LLM parameter post-training. Refer to Agent research.

**2610.07640 · Towards the Automatic Synthesis of Interpretable Chess Tactics**

[Paper](https://arxiv.org/abs/2610.07640)

- **agent**: PAL induces symbolic chess tactics through logic learning rather than LLM agents.
  Evidence locations: Title and complete abstract

**2610.07615 · AFA-BANDIT: Provably Near-Optimal Online Multi-Feature Classification Under Budget Constraints**

[Paper](https://arxiv.org/abs/2610.07615)

- **agent**: AFA-BANDIT is online feature-acquisition bandit classification, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.07594 · BiGym 2.0: Benchmarking Learned and Agent-Developed Policies for Humanoid Household Manipulation**

[Paper](https://arxiv.org/abs/2610.07594)

- **agent**: BiGym2 is a humanoid household benchmark comparing VLA, IL, RL, and coding agents, not a new language policy.
  Evidence locations: Title and complete abstract

**2610.07578 · Cooperating with Future Collaborators: Multi-Agent RL under Staggered Participation**

[Paper](https://arxiv.org/abs/2610.07578)

- **agent**: SPL adds staggered augmentation to conventional MARL training with no LLM policy.
  Evidence locations: Title and complete abstract

**2610.07576 · CETUS: How Far Do Representations Trained on Earth Transfer to Cassini SAR of Titan?**

[Paper](https://arxiv.org/abs/2610.07576)

- **foundation-model**: CETUS evaluates Earth-to-Titan SAR representation transfer. The abstract explicitly notes that comparisons cannot isolate pretraining effects; this is a domain diagnostic.

**2610.07569 · OpenSplatGraph: From Dense Semantic Maps to Structured Scene Graphs for Open-Vocabulary Robot Perception**

[Paper](https://arxiv.org/abs/2610.07569)

- **foundation-model**: OpenSplatGraph converts online 3D Gaussian semantic maps to scene graphs, a robotic perception/mapping system.

**2610.07550 · Foundation Model-Aided Multi-Agent Reinforcement Learning for Wireless Random Access Network Optimization**

[Paper](https://arxiv.org/abs/2610.07550)

- **agent**: Foundation-model-assisted wireless random-access actor–critic, not an LLM tool agent.
  Evidence locations: Title and complete abstract

**2610.07545 · Quality-Aware Self-Correcting Speech Translation on an Edge Device**

[Paper](https://arxiv.org/abs/2610.07545)

- **post-training**: Training-free inference correction for edge speech translation via quality estimation and minimum Bayes risk.

**2610.07535 · Disentangling Models from Personas in Heterogeneous LLM Simulations**

[Paper](https://arxiv.org/abs/2610.07535)

- **agent**: A study of heterogeneous models in social simulation, without a new execution algorithm.
  Evidence locations: Title and complete abstract

**2610.07534 · The EPIC Framework for Spec-Driven Development**

[Paper](https://arxiv.org/abs/2610.07534)

- **agent**: EPIC is a specification-quality practice framework with interviews and correlations, not an agent algorithm.
  Evidence locations: Title and complete abstract

**2610.07509 · On Open-Ended Information Seeking for Information Elicitation Agents**

[Paper](https://arxiv.org/abs/2610.07509)

- **agent**: Controlled behavioral study of how models affect information-elicitation preferences.
  Evidence locations: Title and complete abstract

**2610.07491 · Who Bears the Burden? Learning Responsibility for Shared Constraints in Multi-Agent Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.07491)

- **agent**: LiRA studies welfare gradients in traditional shared-constraint MARL, not LLM policies.
  Evidence locations: Title and complete abstract

**2610.07489 · Deep Defence on Wheels: A Dual Intrusion Detection System Architecture for Comprehensive In-Vehicle Network Security**

[Paper](https://arxiv.org/abs/2610.07489)

- **foundation-model**: FPGA deployment of two in-vehicle CAN intrusion detectors, outside foundation models.

**2610.07475 · Adapting to Changes in Agent Behavior via Finite-Depth Policy Sensitivity**

[Paper](https://arxiv.org/abs/2610.07475)

- **agent**: Finite-depth RL policy sensitivity and pursuit–evasion games, without language agents.
  Evidence locations: Title and complete abstract

**2610.07460 · ElasticFit: Fit-Aware 3D Object Insertion via VLM Reasoning and Generative Adaptation**

[Paper](https://arxiv.org/abs/2610.07460)

- **foundation-model**: ElasticFit is a 3D object insertion and geometric-constraint pipeline, not general multimodal foundation training.

**2610.07426 · AccentCL: Robust Accent Classification with Incremental Expansion**

[Paper](https://arxiv.org/abs/2610.07426)

- **foundation-model**: AccentCL classifies English accents and adds classes incrementally, a specific speech classification task.

**2610.07402 · Rethinking Semantic ID Construction for Generative Recommendation: SimHash with Parallel Decoding and Semantic Alignment**

[Paper](https://arxiv.org/abs/2610.07402)

- **recommendation**: FLASH uses Recall/NDCG and early stopping on four Amazon categories. Open source does not substitute for industrial online evidence.

**2610.07359 · Evaluate the Stack, Not the Layer: Do Deterministic and LLM Gates for Agent Actions Fail Independently?**

[Paper](https://arxiv.org/abs/2610.07359)

- **agent**: Statistical evaluation of how deterministic rules couple with LLM gate errors, not a new policy.
  Evidence locations: Title and complete abstract

**2610.07339 · A doctrine-grounded visual question answering dataset for Tactical Combat Casualty Care**

[Paper](https://arxiv.org/abs/2610.07339)

- **foundation-model**: TC3-VQA is a tactical casualty-care VQA dataset; its main contributions are domain data and source grounding.

**2610.07269 · What Words Keep of a Place: Zero-Shot Language Reasoning for Cross-View Geo-Localization**

[Paper](https://arxiv.org/abs/2610.07269)

- **foundation-model**: GeoLingual diagnoses distinguishability and negative findings for language descriptions in cross-view localization, mainly application evaluation.

**2610.07243 · Hybrid Cross-Modal Attention Network for Early Breast Cancer Detection in Low-Resource Clinical Settings**

[Paper](https://arxiv.org/abs/2610.07243)

- **foundation-model**: HCMAN fuses breast-cancer clinical images and structured records, a specialized medical model.

**2610.07226 · Minimal Witness Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.07226)

- **post-training**: MWRL uses minimal-witness policy gradients on set lattices. LLM experiments freeze Qwen and search head/MLP subsets rather than training a language policy; route to circuit discovery/general RL.

**2610.07168 · A theory of platonic representations in language models**

[Paper](https://arxiv.org/abs/2610.07168)

- **foundation-model**: Cross-lingual Platonic representations and synthetic language diagnostics explain behavior rather than proposing a foundation-model algorithm.

**2610.07091 · Smart Content Ingestion for Generative AI Workloads**

[Paper](https://arxiv.org/abs/2610.07091)

- **foundation-model**: Enterprise multi-format extraction and retrieval evaluation is not a core foundation-model algorithm.

**2610.07062 · Learning to Simulate Individuals from Macro Social Signals**

[Paper](https://arxiv.org/abs/2610.07062)

- **foundation-model**: macro2mind trains user simulators from market signals, a specialized post-training application.

**2610.07060 · Skillful Data-Driven Subseasonal Soil Moisture Forecasting: Prospects and Limits for Flash Drought Prediction**

[Paper](https://arxiv.org/abs/2610.07060)

- **foundation-model**: Subseasonal soil-moisture forecasting is a domain-specific meteorological model and problem.

**2610.07032 · Investigating Model Compression for Neural Machine Translation in the Biomedical Domain**

[Paper](https://arxiv.org/abs/2610.07032)

- **foundation-model**: French–English biomedical translation combines existing distillation and quantization, a domain compression application.

**2610.07023 · Beyond Refusal Patterns: Safe-Role Internalization for Robust and Generalizable LLM Safety Alignment**

[Paper](https://arxiv.org/abs/2610.07023)

- **post-training**: SSRFT generates and expands safe persona QA for standard SFT alignment. It offers safety-data research, not a new optimizer or distillation algorithm.

**2610.07014 · DTFormer: Text-Guided Semantic Alignment for RGB-D Segmentation**

[Paper](https://arxiv.org/abs/2610.07014)

- **foundation-model**: DTFormer adds text semantic prototypes to RGB-D segmentation, a specialized segmentation network.

**2610.06977 · Visual-Invariance-Augmented Feature Optimal Alignment for Transferable Adversarial Attacks against Closed-Source MLLMs**

[Paper](https://arxiv.org/abs/2610.06977)

- **foundation-model**: IAU-FOA studies multimodal transfer attacks, not foundation-model capability algorithms.

**2610.06972 · BoT-Feedback: Grounding Multimodal Reasoning in Biomechanical Evidence for Explainable Human Action Feedback**

[Paper](https://arxiv.org/abs/2610.06972)

- **foundation-model**: BoT-Feedback uses biomechanics to guide movement instruction, a domain application.

**2610.06962 · Verdicts Without Annotated Evidence: Rejection Sampling or Label-Only Post-Training for Evidence Recovery?**

[Paper](https://arxiv.org/abs/2610.06962)

- **post-training**: Compares label-only SFT and RSFT on existing ContractNLI with nonoverlapping document splits but one seed. It analyzes evidence-quality decoupling under two kinds of supervision but adds no standalone public task/scorer. Retain as evidence-recovery ablation evidence.

**2610.06918 · Learning from Unreliable Trajectories: Adversarially-Robust Federated Q-Learning**

[Paper](https://arxiv.org/abs/2610.06918)

- **agent**: Robust Async-Fed-Q is theoretical federated tabular RL, not language agents.
  Evidence locations: Title and complete abstract

**2610.06902 · Tree Navigation Without LLM Summaries: A Matched-Cost Study of Hierarchical Retrieval for Long-Document QA**

[Paper](https://arxiv.org/abs/2610.06902)

- **foundation-model**: NavTree's deterministic hierarchical RAG navigation belongs to the Agent track.

**2610.06896 · Medical Image Alignment Assessment as a Test of Generalist Visual Reasoning in Frontier Multimodal Models**

[Paper](https://arxiv.org/abs/2610.06896)

- **foundation-model**: Evaluates frontier multimodal models on medical-image alignment without a new core algorithm.

**2610.06874 · Statistical Turbulence and High-Fidelity Disturbance Fields for Quadrotor Flight Control**

[Paper](https://arxiv.org/abs/2610.06874)

- **agent**: Cross-evaluates wind-field fidelity for quadrotor PPO control, not LLM agents.
  Evidence locations: Title and complete abstract

**2610.06851 · Base Models Can Reason By Taking a Cue From Training Data**

[Paper](https://arxiv.org/abs/2610.06851)

- **post-training**: Intervenes on initial tokens and pretraining data to study reasoning cues, not a new post-training algorithm.

**2610.06833 · Towards Looped Models Done Right, Part II: Rethinking at Fixed Points**

[Paper](https://arxiv.org/abs/2610.06833)

- **post-training**: Recurrent fixed points, depth priors, and orthogonal injection concern architectures and training foundations; route to foundation models.

**2610.06790 · Back to the Future: Rethinking EDA Infrastructure for Agentic Systems in Chip Design Verification**

[Paper](https://arxiv.org/abs/2610.06790)

- **agent**: BTTF mainly provides domain VCD-to-SQLite conversion and conventional role division and self-correction. Its 150 queries, RTL waveforms, and scorer are not public; no independent general algorithm or attachable evaluation package satisfies reproduction.
  Reproduction scope: SVA rule matching and observed waveform checks are not full formal verification. 'Hallucination-free production' exceeds evidence from one in-house set and no randomized production A/B. Independent repeats, holdout splits, and code/data links are not reported.
  Evidence locations: §3.1–3.2; §4 Tables1–2; §5; Appendix A

**2610.06784 · How to scale your HEP ML models: A recipe for robust architecture comparisons at scale**

[Paper](https://arxiv.org/abs/2610.06784)

- **foundation-model**: Scaling-law comparison for high-energy physics jet models falls outside current language/vision/multimodal foundation modeling.

**2610.06744 · ufakzeka-karar: An Open Turkish Typed-Decision Model with Order-Invariant Option Scoring**

[Paper](https://arxiv.org/abs/2610.06744)

- **post-training**: Releases a Turkish typed-decision head and data, primarily comparing cross-entropy and REINFORCE without a new LLM policy algorithm.

**2610.06726 · Decoupling Time and Space: A Temporally Conditioned Refinement for EEG Source Imaging**

[Paper](https://arxiv.org/abs/2610.06726)

- **foundation-model**: Temporally conditioned EEG source-localization refinement is a specialized medical signal inverse problem.

**2610.06715 · Domain adaptation of Russian ModernBERT for long legal documents**

[Paper](https://arxiv.org/abs/2610.06715)

- **foundation-model**: Compares continued pretraining for Russian legal ModernBERT; the abstract does not propose a general training algorithm.

**2610.06703 · Reading the Mood: Emotion-Guided Book-to-Music Recommendation via CGANs and LLMs**

[Paper](https://arxiv.org/abs/2610.06703)

- **recommendation**: SAGA-CDR uses Amazon 2023 books-to-music, Douban cross-validation, and multi-seed offline cold-start evaluation, without online traffic.

**2610.06685 · Aligning Multimodal Patient Evidence with Biomedical Knowledge Graphs for Clinical LLMs**

[Paper](https://arxiv.org/abs/2610.06685)

- **foundation-model**: MM-KG fuses clinical evidence and biomedical knowledge graphs, a medical knowledge application.

**2610.06670 · Reward Stealing Attack on Large Language Models**

[Paper](https://arxiv.org/abs/2610.06670)

- **foundation-model**: ReSA extracts proxy safety rewards through inverse RL for attacks, not foundation-model capability.
- **post-training**: ReSA extracts proxy safety rewards and reverses inference decoding; it is primarily an attack/inference method, not training improvement.

**2610.06651 · Considering Context: When World Models Need Context Encoders**

[Paper](https://arxiv.org/abs/2610.06651)

- **agent**: Model-based RL theory diagnosing predictive context sufficiency, without an LLM agent algorithm.
  Evidence locations: Title and complete abstract

**2610.06614 · FREA: A Multi-Source Expert Benchmark for Reaction Feasibility Verification**

[Paper](https://arxiv.org/abs/2610.06614)

- **agent**: FREA builds an expert reaction-feasibility benchmark and trains forward models, not an agent policy.
  Evidence locations: Title and complete abstract

**2610.06603 · Word-Level Text Unmixing via Evidence-Preserving Ownership Routing with Language Models**

[Paper](https://arxiv.org/abs/2610.06603)

- **agent**: EPOR supervises word-level reconstruction of text-source attribution, not agent actions.
  Evidence locations: Title and complete abstract

**2610.06590 · SPRIG: Semantic-ID-enhanced Paths for Knowledge Graph-based Generative Recommendation**

[Paper](https://arxiv.org/abs/2610.06590)

- **recommendation**: SPRIG combines knowledge graphs and SID on ML1M/LFM2B. Public offline recommendation does not meet online admission.

**2610.06584 · Does AI Help Cyber Attackers or Defenders? Evidence from Nonpublic Vulnerabilities and Subsequent Attacks**

[Paper](https://arxiv.org/abs/2610.06584)

- **agent**: Nonpublic vulnerability attack/defense capability evaluation, not a new agent method.
  Evidence locations: Title and complete abstract

**2610.06582 · Mind the Execution Gap: Action-Semantic Mismatch in World-Model Control**

[Paper](https://arxiv.org/abs/2610.06582)

- **foundation-model**: Asynchronous execution and controller-action semantic correction, primarily control-system diagnostics and interface repair.

**2610.06571 · BrainTRACE: Tracing Longitudinal, Multimodal, and Volumetric Evidence in Brain MRI Clinical Reasoning**

[Paper](https://arxiv.org/abs/2610.06571)

- **foundation-model**: BrainTRACE benchmarks longitudinal brain-MRI evidence chains, not a new foundation-model algorithm.

**2610.06409 · FlashCart: Fast Cartesian Tensor Products for Equivariant Interatomic Potentials**

[Paper](https://arxiv.org/abs/2610.06409)

- **foundation-model**: FlashCart contributes an equivariant tensor-product GPU kernel and architecture for atomic potentials, a specialized atomic simulation model.

**2610.06394 · Harnessing Multimodal Large Language Models for Training-Free Human-Object Interaction Detection**

[Paper](https://arxiv.org/abs/2610.06394)

- **foundation-model**: HarnessHOI uses active MLLM interaction hypotheses for HOI detection, a vision application harness rather than foundation-model training.

**2610.06387 · Scaling Down the Scaling Laws: Parameter Efficiency and Compute-Optimal Training in Resource-Constrained Large Language Models**

[Paper](https://arxiv.org/abs/2610.06387)

- **foundation-model**: A survey of resource-constrained LLM scaling laws, with no original core algorithm.

**2610.06360 · Ontology Concept Overlap as a Training Signal: Knowledge-Grounded Reinforcement Learning for Clinical Question Answering**

[Paper](https://arxiv.org/abs/2610.06360)

- **post-training**: UMLS concept overlap, judging, and consistency are task rewards with standard GRPO. Evidence is limited to clinical 3–3.8B models, and all 7B runs collapse. Not a general optimizer.

**2610.06320 · CRAFTER: Causality-based Self-adaptation for Autonomous IoT Systems**

[Paper](https://arxiv.org/abs/2610.06320)

- **agent**: CRAFTER is causal RL for adaptive IoT, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.06293 · VepAgent: Bridging Causal-Transition via Tool-Augmented Reinforcement Learning for Video Event Prediction**

[Paper](https://arxiv.org/abs/2610.06293)

- **foundation-model**: VepAgent's tool-augmented RL for video-event prediction belongs to Agent review.

**2610.06251 · Shared Stopping Decisions Change Answers in HQQ Cache Quantization**

[Paper](https://arxiv.org/abs/2610.06251)

- **foundation-model**: HQQ diagnoses and fixes cross-request interference from shared stopping criteria, not a new core foundation-model method.

**2610.06207 · AI-Decision Checkpoints for AI-Augmented Business Process Management: Framework and Educational Instantiation**

[Paper](https://arxiv.org/abs/2610.06207)

- **agent**: AI-decision checkpoints are a teaching framework for business processes, not an algorithm.
  Evidence locations: Title and complete abstract

**2610.06196 · EORestore-Agent: Fidelity-Guided Agentic Restoration of Remote Sensing Images with Composite Degradations**

[Paper](https://arxiv.org/abs/2610.06196)

- **foundation-model**: EORestore coordinates tools for remote-sensing image restoration, a domain system.

**2610.06148 · Reinforcement Learning-Based Optimization of Workload-Aware Power Delivery Networks**

[Paper](https://arxiv.org/abs/2610.06148)

- **agent**: PDN grid wire-width optimization with DQN, not language agents.
  Evidence locations: Title and complete abstract

**2610.06083 · Boosting Transferable Adversarial Attacks against Deep Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.06083)

- **agent**: DQN/DDQN adversarial perturbation transfer in CartPole, not LLM agents.
  Evidence locations: Title and complete abstract

**2610.06069 · Attention Tax, Handoff Tax: A Stylised Model of When Multi-Agent LLM Systems Help**

[Paper](https://arxiv.org/abs/2610.06069)

- **foundation-model**: Theoretical models of multi-agent reliability and communication costs belong to Agent review.
- **agent**: Stylized attention/handoff theory and measurements of multi-agent reliability, not an independent execution algorithm.
  Evidence locations: Title and complete abstract

**2610.06063 · Vision Transformer Ensembles for Panoramic Street Segmentation**

[Paper](https://arxiv.org/abs/2610.06063)

- **foundation-model**: Integrates existing architectures for street-scene segmentation, with no new foundation-model method.

**2610.06050 · MATE: Adaptive Long- and Short-Term User Memory for LLM-Based Recommendation**

[Paper](https://arxiv.org/abs/2610.06050)

- **recommendation**: MATE performs full-catalog offline streaming replay on ML10M, Amazon Luxury Beauty, and KuaiRec2.0, predicting before updating memory. It is not an online exposure experiment.

**2610.06047 · Let the Agent Do It? How Software Practitioners Understand and Make Permission Decisions in Agentic AI Assistants**

[Paper](https://arxiv.org/abs/2610.06047)

- **agent**: Practitioner interviews and surveys of permission decisions, not an algorithm.
  Evidence locations: Title and complete abstract

**2610.06039 · MercerFlow: Flow Matching in a Kernel-Induced Latent Space for Probabilistic Forecasting**

[Paper](https://arxiv.org/abs/2610.06039)

- **foundation-model**: MercerFlow uses kernel latent spaces for probabilistic time-series forecasting, without a general foundation pretraining claim.

**2610.06025 · Grounded Joint-Attention Other-Play for Zero-Shot Coordination**

[Paper](https://arxiv.org/abs/2610.06025)

- **agent**: MATE is visual joint-attention MARL, not an LLM tool agent.
  Evidence locations: Title and complete abstract

**2610.06019 · Adaptive Expert Guidance for Efficient On-Policy Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.06019)

- **agent**: Jointly learns PPO learner/expert control allocation in traditional RL, without language agents.
  Evidence locations: Title and complete abstract

**2610.06018 · Investigating Query-Insensitive Behavior in Spatio-Temporal Video Grounding**

[Paper](https://arxiv.org/abs/2610.06018)

- **foundation-model**: Diagnoses query insensitivity in video grounding without new capability training.

**2610.05961 · Strategic Multi-Agent Learning for Interpretable Action Valuation of All Players in Football**

[Paper](https://arxiv.org/abs/2610.05961)

- **agent**: Football-player dynamic game action valuation, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.05949 · Technical Report on the Turba Fertilizer Machine Learning Stack in Morocco**

[Paper](https://arxiv.org/abs/2610.05949)

- **recommendation**: Turba fits surrogate regressions and engineers data for Moroccan fertilizer recommendations, not internet search/ads/recs or a general LLM algorithm.

**2610.05874 · Global Communication or Graph-Specific Memory?**

[Paper](https://arxiv.org/abs/2610.05874)

- **foundation-model**: Diagnoses globally shared memory in static graph Transformers rather than contributing a current core foundation-model algorithm.

**2610.05863 · CCQ: A Multi-State Child Care Quality Dataset to Support AI for Children's Health Research**

[Paper](https://arxiv.org/abs/2610.05863)

- **foundation-model**: CCQ provides childcare-quality data and prediction benchmarks, not a foundation-model algorithm.

**2610.05828 · Data-Driven Personas for Survey Simulation: Insights into Simulation Alignment Across Data-Access Regimes**

[Paper](https://arxiv.org/abs/2610.05828)

- **agent**: Analyzes sensitivity of population-persona survey simulation to data sources.
  Evidence locations: Title and complete abstract

**2610.05787 · Constraint-Aware Conversational Job Recommendation in Code-Mixed Low-Resource Settings**

[Paper](https://arxiv.org/abs/2610.05787)

- **recommendation**: JobCCC/W-SCAR compares offline retrieval and multiobjective ranking with 988 labeled dialogues and 22,410 jobs, without online deployment or A/B.

**2610.05750 · Beyond Semantic Similarity: Performance and Costs of Agentic Retrieval for Complex Tasks**

[Paper](https://arxiv.org/abs/2610.05750)

- **agent**: Studies cost and effectiveness of existing ReAct retrieval, without a new core mechanism.
  Evidence locations: Title and complete abstract

**2610.05699 · Planetary Geospatial Foundation Models for Global Public Health**

[Paper](https://arxiv.org/abs/2610.05699)

- **foundation-model**: Google PDFM's five public-health studies use existing embeddings as fixed covariates, not new foundation-model training. Pretraining code is proprietary, downstream scripts are unreleased, and several health datasets are restricted, so these are not runnable public Evolve tasks.
  Reproduction scope: Some US v0 embeddings are public, with others requiring application. Public tutorials are not the paper's complete reproduction source.
  Evidence locations: §1–2/Table1；§4 Methods/PDFM Embeddings；Data Availability；Code Availability

**2610.05690 · Errors of LLM-Assisted Literature Retrieval in Environmental Science: A Comparison Study of Abstract versus Full-text Based Prompts**

[Paper](https://arxiv.org/abs/2610.05690)

- **foundation-model**: Compares environmental-science literature retrieval errors, without new foundation-model methodology.

**2610.05681 · Automatic Speech Recognition for Low-Resource Sinhala: A Critical Review of Methods, Challenges, and Future Directions**

[Paper](https://arxiv.org/abs/2610.05681)

- **foundation-model**: A Sinhala ASR survey with no original core algorithm.

**2610.05670 · Generate What You Can Trust: Content Credibility in Generative Recommenders**

[Paper](https://arxiv.org/abs/2610.05670)

- **recommendation**: CreGR reports offline PolitiFact/GossipCop/MHMisinfo label experiments and notes larger evaluation as future work. It does not meet industrial moderation admission.

**2610.05600 · An LLM-in-the-loop RL Framework for Bioinformatics Feature Selection**

[Paper](https://arxiv.org/abs/2610.05600)

- **post-training**: RL selects biological features. The LLM advises and rewards but its policy does not update.
- **agent**: An LLM supplies soft actions and validation/knowledge rewards to a bioinformatics feature-selection DQN. The actual policy is conventional select/skip DQN, so this is domain selection, not LLM post-training or a general agent mechanism.
  Reproduction scope: Allows T=5d repeated exploration. Keep labels in train/validation and isolate downstream test. Public dataset names do not reconstruct splits; no independent seeds or source reported. GPT-4o biological advice is not medical validation.
  Evidence locations: §2–4；Experimental Evaluation

**2610.05591 · What Is a Repeated Token Worth? The Scaling Geometry of Multi-Epoch Pretraining**

[Paper](https://arxiv.org/abs/2610.05591)

- **foundation-model**: An empirical repeated-pretraining scaling and ordering study. The retokenization intervention uses existing BPE-dropout, so no new adapter; retain as support for repetition-count and budget audits.
  Reproduction scope: The frontier is fitted, not additional isoFLOP measurements. Weight-decay/dropout recipes are absent and constants do not extrapolate to frontier LLMs. BPE changes token counts, so equal bytes are not equal FLOPs. A scaling-law analysis is not a verified general selector.
  Evidence locations: §3 Eq1–2；§4.1–4.4 Eq3–5；§6.2–6.3；§7 Limitations

**2610.05569 · Factoriax: A GPU-Accelerated Factorio-Style Simulator for Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.05569)

- **agent**: Factoriax is a JAX factory simulator and PPO benchmark, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.05501 · Logic-Logit: A Logic-Based Approach to Choice Modeling**

[Paper](https://arxiv.org/abs/2610.05501)

- **recommendation**: Logic-Logit fits rules by column generation and Frank–Wolfe. Experiments predict offline choices on synthetic data, 2013 Expedia Kaggle, and MIMIC-IV, without randomized online comparisons.

**2610.05463 · Human-Like Attention? A Psychophysical Comparison of Visual Search in Humans and MLLMs**

[Paper](https://arxiv.org/abs/2610.05463)

- **foundation-model**: Psychophysical comparison of human and MLLM visual search is cognitive evaluation.

**2610.05461 · AI Safety via Debate is Compromised by Cognitive Biases**

[Paper](https://arxiv.org/abs/2610.05461)

- **agent**: Measures cognitive bias in human debate judgments, with no new agent policy.
  Evidence locations: Title and complete abstract

**2610.05446 · Hierarchical Time-aware Bootstrapping for Off-Policy Subgoal Value Learning**

[Paper](https://arxiv.org/abs/2610.05446)

- **post-training**: Off-policy subgoal value learning for HIRO-style AntFall hierarchical control, without language-model post-training.

**2610.05413 · A Strong Baseline for Evaluating Vision Encoders in Multimodal Large Language Models**

[Paper](https://arxiv.org/abs/2610.05413)

- **foundation-model**: RAVEL evaluates visual encoders, not a new foundation-model capability algorithm.

**2610.05400 · CASE: Cost-Aware Stopping for Efficient Long-Video Agents**

[Paper](https://arxiv.org/abs/2610.05400)

- **foundation-model**: CASE stopping decisions for long-video agents belong to the Agent track.

**2610.05369 · AutoDP-LLM: Automating Data Pre-processing for Intrusion Detection Systems using Large Language Models**

[Paper](https://arxiv.org/abs/2610.05369)

- **agent**: AutoDP-LLM generates constrained IDS preprocessing code under host-fixed budget and selection, using semantic-RF-MI features and resampling. This is mainly domain data engineering, without a general policy or new LLM training algorithm.
  Reproduction scope: Train-only profiling, validation selection, and frozen test are appropriate. A multi-backbone executable pipeline is not general agent improvement. HPC parallelism is only future work.
  Evidence locations: §III；§IV；Appendix A/B prompts

**2610.05329 · Understanding the Weight Averaging Mechanism in LLM Training for Post-Training Quantization**

[Paper](https://arxiv.org/abs/2610.05329)

- **post-training**: Theory and kernels for averaging pretrained weights with PTQ belong to foundation-model quantization.

**2610.05306 · Kinematics-Centric Continuous Sign Language Retrieval with Gloss-Guided Boundary-Aware Alignment**

[Paper](https://arxiv.org/abs/2610.05306)

- **foundation-model**: Sign-language kinematic text retrieval and gloss alignment are domain-specific.

**2610.05305 · Characterizing Parallelism Strategies in LLM Inference: Fundamental Compute-Communication Trade-offs**

[Paper](https://arxiv.org/abs/2610.05305)

- **foundation-model**: Analyzes existing tensor, pipeline, and hybrid parallelism with 8×A100 measurements, without an executable new training, model, or scheduling algorithm. Keep as systems background rather than a new adapter.
  Reproduction scope: One eight-GPU NVLink host with ISL1000/OSL200 does not establish single-A100 parallel gains. vLLM 0.15.0 in text conflicts with 0.15.1 in tables. Theoretical prefill/decode results are not universal across batches and networks.
  Evidence locations: §2 TP/PP/HB analytical model；§3.1/3.4；Table2/Figure8–9

**2610.05292 · Erased, Rerouted, or Rescaled? Post-Training and the Causal Quotient of a Language Model's Belief State**

[Paper](https://arxiv.org/abs/2610.05292)

- **foundation-model**: Post-training information erasure, rerouting, and scaling provide theory and causal explanation, not a standalone general task benchmark.
- **post-training**: Analyzes post-training belief-state erasure, rerouting, scaling, and KL protection, not a new training algorithm.

**2610.05265 · Loopy: Low-Bit Quantization Framework for Looped Language Models**

[Paper](https://arxiv.org/abs/2610.05265)

- **post-training**: Low-bit PTQ and calibration budget allocation for recurrent models, without RL or OPD.

**2610.05249 · ArticuTable: Generating Instance-Level Interactive Rigid-Articulated 3D Tabletop Scenes from a Single Image**

[Paper](https://arxiv.org/abs/2610.05249)

- **foundation-model**: ArticuTable reconstructs interactive 3D tabletop scenes from one image, a specialized asset-generation system.

**2610.05220 · Ranking Bandits for Carousel Interfaces with Observable Browsing Depth**

[Paper](https://arxiv.org/abs/2610.05220)

- **recommendation**: The OD-ranking bandit uses simulation calibrated with RecGaze logs. Real online evaluation is explicitly future work; online learning is not an online A/B test.

**2610.05200 · Learning without Overwriting: A Theory of Self-Distillation and Supervised Fine-Tuning in Continual Reasoning**

[Paper](https://arxiv.org/abs/2610.05200)

- **post-training**: DAG theory explaining reasoning retention under OPSD/SFT; the abstract offers no new training method.

**2610.05131 · RoMod: Temporal Routing Modulation via Mixture-of-Experts for Video Anomaly Detection**

[Paper](https://arxiv.org/abs/2610.05131)

- **foundation-model**: RoMod uses MoE routing features to detect video anomalies, primarily a specialized detection head.

**2610.05129 · Representation--Behavior Alignment for Explainable Weakly-Supervised Video Anomaly Detection**

[Paper](https://arxiv.org/abs/2610.05129)

- **foundation-model**: RBA adapts a few attention layers for video anomaly detection, not a general foundation-model capability route.

**2610.05125 · Bayesian Entropy-based Reordering for Calibrated Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.05125)

- **post-training**: BayesER uses posterior uncertainty to commit tokens during diffusion inference, without adapter training.

**2610.05114 · Belief-Trajectory Energy: Measuring the Path to a Prediction**

[Paper](https://arxiv.org/abs/2610.05114)

- **foundation-model**: BTE uses interlayer belief-trajectory energy to identify difficulty and generation source, primarily an interpretability metric.

**2610.05111 · InstMoE: Adaptive Multimodal Routing with Specialized Experts**

[Paper](https://arxiv.org/abs/2610.05111)

- **foundation-model**: InstMoE trains a lightweight Transformer for CMU-MOSEI/CH-SIMS emotion using pre-extracted BERT/COVAREP features, InfoNCE, and five dense T/A/V/TA/TV weighted experts with centroid-bias initialization. It is supervised emotion fusion, not adaptation of a foundation generator, general agent, or independent public evaluation protocol.
  Evidence locations: §3.2–3.3 Eq. 1–9; §4.1–4.2

**2610.05100 · METRO: Metric-Enhanced Token Routing Operator**

[Paper](https://arxiv.org/abs/2610.05100)

- **foundation-model**: METRO uses Mahalanobis routing for grid/PDE neural operators, outside current foundation-model scope.

**2610.05041 · Communication Shapes Collective Inference in Self-Adapting LLM Societies: Evidence from Mafia**

[Paper](https://arxiv.org/abs/2610.05041)

- **agent**: Adaptive LLM group communications in Mafia, not a new general algorithm.
  Evidence locations: Title and complete abstract

**2610.05036 · Characterizing Security Effects of OSS Vulnerabilities in Agent Systems**

[Paper](https://arxiv.org/abs/2610.05036)

- **agent**: Diagnoses security impact of OSS vulnerability propagation to agent layers, not agent capability.
  Evidence locations: Title and complete abstract

**2610.05029 · SPACE-CLIPv2: Decoding Local Geometry from Frozen CLIP for Monocular Depth Estimation**

[Paper](https://arxiv.org/abs/2610.05029)

- **foundation-model**: SPACE-CLIPv2 uses a domain-specific frozen-CLIP depth decoder, not general vision foundation training.

**2610.05009 · Rethinking Tool Design for Agentic RCA: A Controlled Empirical Study**

[Paper](https://arxiv.org/abs/2610.05009)

- **agent**: Controlled comparison of RCA tool abstraction and composition, not a new algorithm.
  Evidence locations: Title and complete abstract

**2610.04977 · Do LLMs Understand Sequential Structure? A Controlled Study of Inference and Generation**

[Paper](https://arxiv.org/abs/2610.04977)

- **agent**: Controlled study of sequence structure in rock–paper–scissors and n-grams.
  Evidence locations: Title and complete abstract

**2610.04976 · Priced Guidance: Can Language Models Generate Future Research Ideas?**

[Paper](https://arxiv.org/abs/2610.04976)

- **foundation-model**: Priced Guidance's evaluator sees goals, so it is at most a mechanism diagnostic, not Evolve capability evidence.

**2610.04957 · Trinity: One Differentiable Physics for Training, Refining and Scoring Generative Floorplanners**

[Paper](https://arxiv.org/abs/2610.04957)

- **foundation-model**: Trinity generates and refines chip floorplans, a specialized engineering optimization.

**2610.04893 · SFlexRCA: Lightweight, Scalable, and Flexible Root Cause Analysis for IIoT Edge Systems**

[Paper](https://arxiv.org/abs/2610.04893)

- **foundation-model**: SFlexRCA analyzes root causes in industrial IoT sensors, not a foundation-model algorithm.

**2610.04878 · Bounded Reasoning: Cognitive Hierarchy in Human-versus-AI Cyber Defense**

[Paper](https://arxiv.org/abs/2610.04878)

- **agent**: Human/DQN cognitive-hierarchy experiments in network defense, without an LLM policy.
  Evidence locations: Title and complete abstract

**2610.04867 · Greedy Local Learning for Language Model Pretraining: Gaps and Objective Design**

[Paper](https://arxiv.org/abs/2610.04867)

- **foundation-model**: The paper explicitly measures local learning rather than introducing a new method. Retain as comparison for local prediction/JEV objectives, not a separate adapter.
  Reproduction scope: One seed and unmatched token/compute budgets. Single-GPU stage simulation does not establish distributed throughput. The paper mentions release, but full text had no verifiable official repository entry. Memory diagnostics are not capability gains.
  Evidence locations: §3.1–3.4；§4.1–4.5 Tables1–4；§5 Limitations

**2610.04862 · GitSwarm: Decentralized Compounding Inference**

[Paper](https://arxiv.org/abs/2610.04862)

- **foundation-model**: GitSwarm's persistent Git memory for multi-agent inference belongs to Agent review.

**2610.04832 · Agent Skill Evolution: How Revisions Affect Coding Agents**

[Paper](https://arxiv.org/abs/2610.04832)

- **agent**: Empirical effects of SKILL edits on adherence and cost, without a new algorithm.
  Evidence locations: Title and complete abstract

**2610.04802 · Multi-Agent Spectrum Sharing**

[Paper](https://arxiv.org/abs/2610.04802)

- **agent**: Multi-agent spectrum meta-RL for cognitive radar, not LLM agents.
  Evidence locations: Title and complete abstract

**2610.04639 · When Talk Isn't Code: Comparing LLM Agents That Simulate and Develop Software**

[Paper](https://arxiv.org/abs/2610.04639)

- **agent**: Controlled safety comparison of LLM simulation and development protocols, not a new method.
  Evidence locations: Title and complete abstract

**2610.04636 · Does Neural Complexity Improve Health Misinformation Detection? A Leakage-Controlled Cross-Corpus Benchmark**

[Paper](https://arxiv.org/abs/2610.04636)

- **foundation-model**: A health misinformation benchmark comparing architectures, not a foundation-model algorithm.

**2610.04589 · StegoMemory: Agentic Memory Acts as Covert Steganographic Channel**

[Paper](https://arxiv.org/abs/2610.04589)

- **agent**: StegoMemory measures cross-session risks across several steganographic schemes, without a new capability policy.
  Evidence locations: Title and complete abstract

**2610.04569 · From Transformers to Weighted Automata: Towards the Verification of Large Language Models**

[Paper](https://arxiv.org/abs/2610.04569)

- **foundation-model**: Formal verification theory mapping Transformers to weighted automata, not capability training or inference efficiency.

**2610.04544 · Label Agreement Does Not Measure Authorization**

[Paper](https://arxiv.org/abs/2610.04544)

- **agent**: A case study auditing authorization and output integrity of a label-ontology pipeline, not a general algorithm.
  Evidence locations: Title and complete abstract

**2610.04541 · Autonomous Structuring of Radiology Reports Across Modalities at Archive Scale Using an Open-Weight Large Language Model**

[Paper](https://arxiv.org/abs/2610.04541)

- **foundation-model**: Template-driven radiology-report archiving, a specialized clinical deployment.

**2610.04528 · Quantifying Collusion Among Autonomous LLM Agents: A Statistical Analysis of the Collusion Wiki Incident**

[Paper](https://arxiv.org/abs/2610.04528)

- **agent**: Statistical analysis of Collusion Wiki events, not an algorithm.
  Evidence locations: Title and complete abstract

**2610.04507 · LoRA's Second Descent Extends Beyond Parameter Parity**

[Paper](https://arxiv.org/abs/2610.04507)

- **foundation-model**: Empirical LoRA-rank and double-descent noise diagnostics, not a new method.
- **post-training**: Studies double descent under LoRA rank and label noise, not a new post-training algorithm.

**2610.04502 · Localization Lens for Improving Medical Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.04502)

- **foundation-model**: Anatomic localization representations, pixel shuffle, and DCL for Med-VQA are specialized medical adaptation.

**2610.04499 · Homogeneous Semantic Alignment and Hierarchical Expert Routing for Radiology Report Generation**

[Paper](https://arxiv.org/abs/2610.04499)

- **foundation-model**: HSA-HER is a specialized radiology-report generator.

**2610.04494 · DreamTest: World-Model Surrogates for Search-Based Testing of Deep Reinforcement Learning Agents**

[Paper](https://arxiv.org/abs/2610.04494)

- **agent**: DreamTest tests agents with traditional DRL world models, not language agents.
  Evidence locations: Title and complete abstract

**2610.04433 · What Does a Harness Buy? Tokens, Mostly**

[Paper](https://arxiv.org/abs/2610.04433)

- **agent**: Studies rerun randomness and cost with fixed model and harness, without a new algorithm.
  Evidence locations: Title and complete abstract

**2610.04425 · AgroGround: Multi-Granularity Grounded Recognition in Agriculture**

[Paper](https://arxiv.org/abs/2610.04425)

- **foundation-model**: AgroGround provides agricultural grounding data and training tasks, primarily a domain benchmark.

**2610.04424 · On the Trade-off Between Information Loss and Generalization in Sparse Attention**

[Paper](https://arxiv.org/abs/2610.04424)

- **foundation-model**: JS error and generalization bounds for sparse attention, without a new executable capability algorithm.

**2610.04418 · CORE-RL: Confidence-Oriented Reliability Evaluation of Black-Box Reinforcement Learning Policies**

[Paper](https://arxiv.org/abs/2610.04418)

- **agent**: CORE-RL evaluates reliability in black-box continuous control, not LLM agents.
  Evidence locations: Title and complete abstract

**2610.04413 · Specific Algorithmic Interpretability of Neural Networks: A Case Study on Textures**

[Paper](https://arxiv.org/abs/2610.04413)

- **foundation-model**: Interpretable initialization and PAC-Bayes theory for scattering texture classification, not foundation modeling.

**2610.04412 · Large Language Models and Augmented Democracy**

[Paper](https://arxiv.org/abs/2610.04412)

- **post-training**: A dissertation integrating digital twins into democracy, not a distinct core RL/OPD algorithm.
- **agent**: Augmented Democracy collects political preference modeling and parliamentary digital-twin work, tuning on public voting and demographics and discussing opinion proxies.
  Reproduction scope: No general agent operator or executable capability improvement under current scope. Political preference prediction is not tool, planning, or self-evolution implementation, and does not warrant scope expansion.
  Evidence locations: Thesis chapters preference prediction/digital twins; normalized p17,25–33,60–61,69–120

**2610.04403 · Saying, Not Knowing: Aggressively GGUF-Quantized Small Language Models Still Write Rare Words They Can No Longer Define**

[Paper](https://arxiv.org/abs/2610.04403)

- **foundation-model**: Audits vocabulary capabilities of quantized GGUF small LMs without a new quantization algorithm.
- **post-training**: Measures lexical meaning in low-bit GGUF models, a quantization evaluation.

**2610.04366 · Human Behavior-Informed Crash Scenario Generation with Real-World Crash Priors for Autonomous Vehicle Safety Evaluation**

[Paper](https://arxiv.org/abs/2610.04366)

- **agent**: CrashSim generates multi-agent traffic; LLMs only help diagnose and are not the core agents.
  Evidence locations: Title and complete abstract

**2610.04278 · Do RUL explanations hold up? Faithfulness and stability of attributions on C-MAPSS**

[Paper](https://arxiv.org/abs/2610.04278)

- **foundation-model**: Audits explainability for remaining equipment lifetime, a predictive maintenance application.

**2610.04272 · Rethinking Self-Distillation for Multi-Teacher Capability Merging**

[Paper](https://arxiv.org/abs/2610.04272)

- **post-training**: Controls data and hyperparameters when comparing MOPD, SFT, soft labels, and existing merges, a fair-baseline diagnostic.

**2610.04269 · Self-Reflection Fine-Tuning: Enhancing Agent Security against Prompt Injection Attacks from Failure Experience**

[Paper](https://arxiv.org/abs/2610.04269)

- **post-training**: SRFT turns failure analyses into safe reasoning/action samples and uses standard negative-log-likelihood LoRA SFT. The data/safety framework is useful but adds no core training algorithm. This applies only to core post-training; independently review methods and public data in the Agent track.

**2610.04263 · Multimodal Dual-Encoder Retrieval for Automated ICD Coding**

[Paper](https://arxiv.org/abs/2610.04263)

- **foundation-model**: Dual-encoder retrieval and LLM reranking for ICD coding, a specialized clinical application.

**2610.04168 · Agentic Cognitive Depth: Operational Criteria for Evaluating LLM Agents**

[Paper](https://arxiv.org/abs/2610.04168)

- **agent**: Proposes criteria and diagnostics for agent cognitive depth; no new algorithm was executed.
  Evidence locations: Title and complete abstract

**2610.04158 · How RL Reshapes LLM Reasoning: Transferability, Coverage, and Scaling Laws**

[Paper](https://arxiv.org/abs/2610.04158)

- **post-training**: Theoretical and empirical work on RL policy selection, transfer, coverage, and scaling, without a new training mechanism.

**2610.04138 · Dual-Scale Relational Graph Transformers for Ecosystem-Aware Fraud Detection**

[Paper](https://arxiv.org/abs/2610.04138)

- **foundation-model**: HERMES is a banking fraud graph model for industrial risk, not a foundation model. Review production evidence separately.

**2610.04133 · Auditing Pairwise Equivalence Judgments: Self-Critique Effects and Diversity Measurement in Multi-Agent Hypothesis Generation**

[Paper](https://arxiv.org/abs/2610.04133)

- **agent**: Studies hypothesis equivalence, self-critique, and diversity measurement.
  Evidence locations: Title and complete abstract

**2610.04125 · Representational Control over Self-Report & Behavior Coherence in LLM Risk-Taking**

[Paper](https://arxiv.org/abs/2610.04125)

- **agent**: Diagnostic comparison of self-reported risk preferences, behavior, and activation representations.
  Evidence locations: Title and complete abstract

**2610.04104 · Where Does the Semantic Gain Come From? A Reproduction and Extension of Semantic Knowledge-driven Contrastive Learning for Long-Tailed Recognition**

[Paper](https://arxiv.org/abs/2610.04104)

- **foundation-model**: Audits SKCL reproduction and budget confounding without establishing a stable gain for a new algorithm.

**2610.04083 · Self-Propagating Misalignment in LLM Agents, and Why Auditing or Disabling Memory Is Not Enough**

[Paper](https://arxiv.org/abs/2610.04083)

- **agent**: Threat evaluation of misaligned objectives propagating through memory and files; no new defense.
  Evidence locations: Title and complete abstract

**2610.04053 · The Cost of a Hop: Benchmarking NLIP and A2A**

[Paper](https://arxiv.org/abs/2610.04053)

- **agent**: Compares NLIP/A2A communication latency, not an agent policy.
  Evidence locations: Title and complete abstract

**2610.04040 · Agent Policy-Value Audit: Separating Transition Composition from Event Selection in Financial LLM Agents**

[Paper](https://arxiv.org/abs/2610.04040)

- **agent**: Statistical audit of transition composition versus selection in financial-agent returns.
  Evidence locations: Title and complete abstract

**2610.03972 · Probabilistic Algorithms for Ising Machines from Optimization to Generative AI**

[Paper](https://arxiv.org/abs/2610.03972)

- **foundation-model**: Survey of Ising probabilistic algorithms and hardware co-design.
- **post-training**: Ising-machine probabilistic algorithms survey, not new LLM post-training.

**2610.03969 · How Do Coding Agents Optimize Software and Report Performance Validation? A Large-Scale Empirical Study of Open-Source Pull Requests**

[Paper](https://arxiv.org/abs/2610.03969)

- **agent**: Large empirical study of performance-PR practice and measurement by agents.
  Evidence locations: Title and complete abstract

**2610.03923 · Learning Robust Personalized Prompts for LLM-Driven Sequential Recommendation**

[Paper](https://arxiv.org/abs/2610.03923)

- **recommendation**: LRPRec reports offline ranking under temporal splits on MovieLens, Steam, and LastFM. A/B is a hypothetical use for prompt changes, not an executed production experiment.

**2610.03830 · Memory-State Critic for Asymmetric Actor-Critic with Application to Vision-Based Pursuit-Evasion**

[Paper](https://arxiv.org/abs/2610.03830)

- **agent**: Traditional visual pursuit-evasion RL with a memory-state critic, not a language agent.
  Evidence locations: Title and complete abstract

**2610.03792 · What Do Verifiable Rewards Teach Video-Language Models About Time? A Controlled Multi-Model Study**

[Paper](https://arxiv.org/abs/2610.03792)

- **foundation-model**: Video RLVR temporal-understanding controls are diagnostic and reviewed under post-training.

**2610.03759 · BridgeCast: Bridging Ocean Wave Forecasts to Reanalysis via Flow Matching with Exogenous Variables**

[Paper](https://arxiv.org/abs/2610.03759)

- **foundation-model**: BridgeCast applies flow-matching bias correction to ocean-wave prediction, a specialized scientific application.

**2610.03713 · What Should World Models Forget? Stratified Retention for Continual Adaptation**

[Paper](https://arxiv.org/abs/2610.03713)

- **foundation-model**: Proposes retaining information at invariant time scales and a measure for world models; the abstract gives no empirical evidence for a new training algorithm.

**2610.03620 · UniIntervene++: An Adaptive Intervention Agent for Efficient Real-World Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.03620)

- **agent**: UniIntervene++ schedules a robot SERL policy with availability-masked SMDP Double-DQN options: RL, demonstration-trajectory correction, and CodePolicy. Adaptive RL Probe estimates capability.
  Reproduction scope: Five physical robot tasks require hardware and demonstrations. The scheduler is classical RL, not general LLM/agent learning; CodePolicy does not make the system a text/software agent reproduction. Revisit for a future robotics track.
  Evidence locations: §III, Eq scheduler, §IV.C

**2610.03617 · DEPICT: Scoring Text-to-Image Alignment by Answer Agreement**

[Paper](https://arxiv.org/abs/2610.03617)

- **foundation-model**: DEPICT measures image-text consistency, not a foundation model capability algorithm.

**2610.03604 · Mastering Atari 2600 Games with Discovered Options**

[Paper](https://arxiv.org/abs/2610.03604)

- **agent**: Wayfarer studies Atari deep-RL options, with no language agent.
  Evidence locations: Title and complete abstract

**2610.03598 · When a Correct Reward Is Not Enough: Diagnosing and Guiding PPO in an Analytically Solved Broker-Trader Game**

[Paper](https://arxiv.org/abs/2610.03598)

- **agent**: Continuous financial-broker PPO diagnostic, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.03567 · Writerslogic at the CLEF 2026 SimpleText Track: Multi-Candidate LLM Simplification and Stacked Complexity Spotting**

[Paper](https://arxiv.org/abs/2610.03567)

- **foundation-model**: CLEF SimpleText shared-task system with domain prompt selection and NLI adaptation.
- **post-training**: SimpleText shared-task reranking and DeBERTa NLI fine-tuning, no new LLM policy algorithm.

**2610.03529 · Divergence controls entropy in distillation**

[Paper](https://arxiv.org/abs/2610.03529)

- **foundation-model**: Theory and experiments on entropy under distillation divergences; post-training may review it, but not a new foundation architecture.
- **post-training**: Theory and controls on how distillation divergence affects entropy, without an independent new training method.

**2610.03502 · Certified Mechanistic Edits: Behavioral Guarantees for Skill Removal and Preservation**

[Paper](https://arxiv.org/abs/2610.03502)

- **foundation-model**: Formal verification of skill deletion over continuous inputs in small networks, outside foundation-scale capability algorithms.

**2610.03480 · Metropolis-Hastings Dominates Importance Resampling for Policy Composition**

[Paper](https://arxiv.org/abs/2610.03480)

- **post-training**: Inference-sampling theory for policy composition compares MH and importance resampling without updating the LM.

**2610.03468 · A Vision-Language Model (VLM)-based Pipeline for End-to-End Procedural Modeling of Field-Grown Maize from Point Clouds**

[Paper](https://arxiv.org/abs/2610.03468)

- **foundation-model**: Procedural corn point-cloud reconstruction, a specialized agricultural geometry pipeline.

**2610.03463 · Generalization of Transformer-Based Neural Quantum States via In-Context Learning**

[Paper](https://arxiv.org/abs/2610.03463)

- **foundation-model**: Theory of Transformer quantum-state ICL generalization, outside this foundation-model scope.

**2610.03454 · Measure Less, Know More: Self-Supervised Test-Time Feature Acquisition**

[Paper](https://arxiv.org/abs/2610.03454)

- **post-training**: Test-time RL for modality acquisition over arbitrary foundation representations, not an LLM post-training mechanism.

**2610.03445 · Corrupted but Correct: Why Vision-Language Models Lie to Themselves Internally**

[Paper](https://arxiv.org/abs/2610.03445)

- **foundation-model**: Mechanism diagnosis of VLM attack training/inference mismatch, not a new capability method.

**2610.03369 · Mixture-of-Experts for Cryptocurrency Order Execution: Training Stability, Tail Risk, and Failure Modes**

[Paper](https://arxiv.org/abs/2610.03369)

- **post-training**: Multiseed control study of DDQL/MoE for cryptocurrency orders, without language-model training.

**2610.03289 · Architecture-Dependent Fusion Pathways in MLLMs**

[Paper](https://arxiv.org/abs/2610.03289)

- **foundation-model**: Diagnoses cross-layer fusion representations in MLLMs without a new capability algorithm.

**2610.03220 · Evolving Hybrid Quantum-Classical Architectures for Image Classification**

[Paper](https://arxiv.org/abs/2610.03220)

- **foundation-model**: Quantum-classical circuit architecture search for image classification, outside this foundation-model scope.

**2610.03215 · StanceEval 2026: The Second Stance Detection Shared Task**

[Paper](https://arxiv.org/abs/2610.03215)

- **foundation-model**: Overview of the StanceEval Arabic stance detection shared task.

**2610.03193 · Bridging Research and Practice: A Systematic Evaluation of Generalist and Dermatology-Specific Models in Clinical Skin Lesion Classification**

[Paper](https://arxiv.org/abs/2610.03193)

- **foundation-model**: Systematic clinical benchmark of dermatology models, no new method.

**2610.03187 · Lightweight and Resource-Efficient Perception for Robotic Guide Dogs**

[Paper](https://arxiv.org/abs/2610.03187)

- **foundation-model**: Guide-robot perception with a 360-degree camera and LiDAR, a specialized application.

**2610.03185 · Gains and Collapse in On-Policy Distillation:A Reinforcement Learning Perspective**

[Paper](https://arxiv.org/abs/2610.03185)

- **post-training**: Analyzes OPD gains and collapse. Truncated-response loss masking and existing SFT warmup retain the optimizer recipe. Not a standalone core method, but relevant risk evidence for ResOPD and related reproductions.

**2610.03141 · Behavior Pack Optimization for Video MLLM Post-Training**

[Paper](https://arxiv.org/abs/2610.03141)

- **foundation-model**: BPO applies RL to counterfactual behavior bundles for video MLLMs; reviewed under post-training.

**2610.03136 · Investigating the Role of Reasoning-Language Alignment in Monolingual Retrieval-Augmented Generation**

[Paper](https://arxiv.org/abs/2610.03136)

- **agent**: German RAG reasoning-language comparison, not a new core algorithm.
  Evidence locations: Title and complete abstract

**2610.03112 · Building Interpretable Feature Representations for Resume-Vacancy Matching by Distilling Production LLM Signals**

[Paper](https://arxiv.org/abs/2610.03112)

- **foundation-model**: Deployed recruitment matching distillation is industrial recommendation, not a foundation model. Production feedback agreement is not A/B.

**2610.03109 · Emergent Structure in the Marginal Attention Space of Language Models**

[Paper](https://arxiv.org/abs/2610.03109)

- **post-training**: Marginal attention and KV eviction budgets belong to inference/foundation models.

**2610.03098 · Predictor-Guided Latent Space Codon Optimization for Maximizing Protein Expression**

[Paper](https://arxiv.org/abs/2610.03098)

- **foundation-model**: Latent codon optimization for mRNA, a specialized life-science design problem.

**2610.03057 · When Does Synthetic Relational Data Teach Models to Use Relations? Tracing Predictive Structure from Pretraining Data to Model Behavior**

[Paper](https://arxiv.org/abs/2610.03057)

- **foundation-model**: Attributes model behavior across four synthetic relation datasets without proposing a new core training method.

**2610.03033 · When Numbers Start Talking: Numerical Signalling and Strategic Behaviour Among LLMs**

[Paper](https://arxiv.org/abs/2610.03033)

- **agent**: Strategic-game behavior study using numeric messages and natural language.
  Evidence locations: Title and complete abstract

**2610.03016 · From Expression to Reaction: Role-aware Visual Transfer and Stimulus-guided Reasoning for Interlocutor Emotion Recognition**

[Paper](https://arxiv.org/abs/2610.03016)

- **foundation-model**: Competition-specific vision transfer and boundary inference for conversational emotion recognition.

**2610.03010 · Engineering Sustainable Agents: A Systematic Comparison of Agentic LLMs for Developer Workflows**

[Paper](https://arxiv.org/abs/2610.03010)

- **agent**: Compares development-agent energy, latency, and effectiveness configurations.
  Evidence locations: Title and complete abstract

**2610.02974 · From Language Priors to Field Adaptation: Preference Learning for Traversability Estimation**

[Paper](https://arxiv.org/abs/2610.02974)

- **foundation-model**: Robot traversability preference learning for specialized terrain estimation.

**2610.02957 · Understanding Trajectory Heterogeneity in Federated World Model Learning**

[Paper](https://arxiv.org/abs/2610.02957)

- **foundation-model**: Federated clinical world-model trajectory heterogeneity benchmark, a domain diagnostic.

**2610.02910 · Frequency Is Not Sensitivity Identifying Safety-Sensitive Experts in Sparse MoE LLM**

[Paper](https://arxiv.org/abs/2610.02910)

- **foundation-model**: Attack/diagnostic based on suppressing safety-sensitive MoE experts, not a capability enhancement algorithm.

**2610.02886 · Misinformation Without Triggers: From Factual Answers to Downstream Decisions**

[Paper](https://arxiv.org/abs/2610.02886)

- **post-training**: Controlled evaluation of triggerless data poisoning on facts and downstream decisions, not a post-training method.

**2610.02847 · Turnover-Orthogonal Credit Assignment for Open-Team Multi-Agent Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.02847)

- **agent**: TOCA decomposes credit in classical open-team MARL, not a language agent.
  Evidence locations: Title and complete abstract

**2610.02839 · To Explore The Strange New World Beyond Data Distribution: System Behavior, Causality Tax, and Non-causal Base Model**

[Paper](https://arxiv.org/abs/2610.02839)

- **foundation-model**: SBD/GSH is a theoretical lazy-training NTK spectral proof of concept. The authors explicitly provide no end-to-end language capability results; no foundation/evolve adapter added.
  Reproduction scope: Noncausal shells depend on heuristic renormalization and block execution. NTK spectral SNR is not language-model accuracy or proof of a universal causality tax. Retain theoretical context without presenting prospective backprop-free training as validated.
  Evidence locations: §5.2–5.3; §6.1–6.2

**2610.02819 · Text-Centric Post-Training for Omni-Modal Reasoning**

[Paper](https://arxiv.org/abs/2610.02819)

- **post-training**: Text-centric Omni studies text/multimodal data and SFT/RL recipes; gradient orthogonality is diagnostic and no new core optimizer is proposed. Keep recipe insights without a new adapter.

**2610.02766 · Exact Memory-Time Optimization for Prefix-Cached Language Model Serving**

[Paper](https://arxiv.org/abs/2610.02766)

- **post-training**: Minimum-cut/closure optimization for prefix-cache timeout, a serving systems algorithm only.

**2610.02755 · FiberGeoText: A Vision-Language Model for Population- Level Organization of Superficial White Matter**

[Paper](https://arxiv.org/abs/2610.02755)

- **foundation-model**: FiberGeoText is a specialized medical model for brain white-matter fiber clustering.

**2610.02744 · EpiWorld: Grounding LLM Policy Agents in Epidemiological World Models**

[Paper](https://arxiv.org/abs/2610.02744)

- **post-training**: EpiWorld simulator counterfactuals and episodic skill memory are not explicit LLM parameter post-training.
- **agent**: EpiWorld uses an epidemic graph world model and protocol/skill/lesson library. Teachers distill failure events and supersede old lessons, rather than parameter RL. Retrospective data from 51 states and two SEIR simulations share the same model across policies; mechanistic reruns do not identify real interventions. Lessons fail across epidemics and ensemble intervals are underdispersed. Highly disease-specific, with no general agent mechanism or benchmark.
  Evidence locations: §3.2–3.5; §4.1–4.2; §5.2; Limitations

**2610.02702 · Silent Dissent: LLM Agents That Yield to the Majority Still Represent Their Original Premise**

[Paper](https://arxiv.org/abs/2610.02702)

- **agent**: J-lens diagnoses hidden bridges after conformity, not a mature new policy.
  Evidence locations: Title and complete abstract

**2610.02659 · Distributed Learning with Selective State Space Models: Architecture-Aware Convergence Analysis**

[Paper](https://arxiv.org/abs/2610.02659)

- **foundation-model**: Convergence theory for SSM federated learning and comparison of existing methods, no new training algorithm.

**2610.02654 · Coherence-Driven Belief Formation and Population Dynamics of Contagion in LLM Agents**

[Paper](https://arxiv.org/abs/2610.02654)

- **agent**: Analysis of LLM social belief-propagation kernels and group dynamics.
  Evidence locations: Title and complete abstract

**2610.02611 · Scale-Recursive Rectified Flows for Few-Step Precipitation Ensembles**

[Paper](https://arxiv.org/abs/2610.02611)

- **foundation-model**: Recursive flow sampling across rainfall-field scales, a specialized weather model.

**2610.02610 · Seer: Maximum Likelihood Regression for Learning-Speed Curves**

[Paper](https://arxiv.org/abs/2610.02610)

- **recommendation**: Seer is a late upload of a 1995 UIUC PhD dissertation on learning curves for classical classifiers. Its 2026 arXiv ID does not make it a new LLM method.

**2610.02600 · When History Misleads: Asymmetric Margin Supervision for Instruction-Guided LLM Generative Recommendation**

[Paper](https://arxiv.org/abs/2610.02600)

- **recommendation**: Meta AIMS retains full history and uses removal counterfactuals for asymmetric margins updating competitors only. Six backbones, private logs, and Qilin/KuaiSearch-Lite Recall/NDCG are all offline. Production SIDs/logs are not deployment experiments. Methods, results, conclusion, and appendix yielded no A/B or full-rollout effects, so the industrial gate was not met.

**2610.02554 · Test-time Multi-agent Coordination by Decomposed Value Gradient Flow**

[Paper](https://arxiv.org/abs/2610.02554)

- **post-training**: SCOUT is an offline MARL generative prior with SVGD action refinement, not language-model post-training.
- **agent**: SCOUT flow priors/SVGD are classical offline MARL, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.02513 · From Fragments to Global Maps: Learning Vectorized Map Aggregation with Large Language Models**

[Paper](https://arxiv.org/abs/2610.02513)

- **foundation-model**: MapMergeLLM aggregates vector road maps for specialized autonomous driving.

**2610.02507 · MeshQuery: Agentic Seam Planning for UV Parametrization**

[Paper](https://arxiv.org/abs/2610.02507)

- **foundation-model**: MeshQuery is a 3D mesh UV unwrapping agent; reviewed under Agent.

**2610.02497 · LiteEMG-FM: An Efficient and Deployable Foundation Model for Robust EMG Sensing**

[Paper](https://arxiv.org/abs/2610.02497)

- **foundation-model**: LiteEMG-FM is an 8M masked spectrogram CNN/Transformer for EMG, cross-user signal tasks, and ESP32 deployment, not in this general LLM/VLM scope.
  Reproduction scope: A foundation label does not make it a general large model. Its training and zero-calibration metrics are sensor-specific.
  Evidence locations: §4.1–4.3; §5.1–5.9; §6

**2610.02486 · From Retrieval to Typed Decisions: Calibrated System One Models from Biomedical Sentence Encoders**

[Paper](https://arxiv.org/abs/2610.02486)

- **post-training**: Converts biological sentence encoders to typed decision models and diagnoses RLCD, mainly architecture/calibration.

**2610.02466 · SD-DPC: Sparse Dictionary Differentiable Predictive Control**

[Paper](https://arxiv.org/abs/2610.02466)

- **post-training**: Sparse nonlinear control using a SINDy dictionary, without LMs.

**2610.02452 · Reinforcement Learning Techniques for the Optimization of Target Polarization in Nuclear Physics Scattering Experiments**

[Paper](https://arxiv.org/abs/2610.02452)

- **agent**: Nuclear-physics polarization GP surrogate and classical RL control, no language agent.
  Evidence locations: Title and complete abstract

**2610.02451 · A Simulation-Grounded Agentic VLM Framework for Wildfire Monitoring and Reporting**

[Paper](https://arxiv.org/abs/2610.02451)

- **foundation-model**: Wildfire monitoring simulation and a multimodal-memory agent are specialized; reviewed under Agent.

**2610.02442 · AI-driven Thermal-aware Data Center Capacity Planning**

[Paper](https://arxiv.org/abs/2610.02442)

- **foundation-model**: CFD surrogate for thermally aware datacenter capacity planning, not a core foundation algorithm.

**2610.02432 · Evaluating and Improving the Robustness of Large Language Models to Input Sequence Variations**

[Paper](https://arxiv.org/abs/2610.02432)

- **agent**: MCPSec/MCPBench and AttestMCP fixed permission tables/HMAC, plus CommitBoundary containers, static checks, and output validation, reuse 2025 work [11] (arXiv2601.17549) in §5.3. The 847 cases and ASR 53.7→12.4 measure combined security engineering, not a new standalone agent algorithm/public entry point. HMAC protects integrity, not authorization; misuse within allowed parameters can pass. Excluded for repeated integration, not merely a benchmark without loss.
  Evidence locations: Title and complete abstract

**2610.02386 · Social bot detection in the age of ChatGPT: Challenges and opportunities**

[Paper](https://arxiv.org/abs/2610.02386)

- **foundation-model**: Survey of social bot detection, no new foundation-model algorithm.

**2610.02376 · Coco: An Agentic Copilot for the Hardware--Software Co-Design Lifecycle**

[Paper](https://arxiv.org/abs/2610.02376)

- **agent**: Google/Google DeepMind and MIT's Coco is used daily by TPU architects, but the paper gives system design and two cases without verifiable algorithm benchmarks or quantitative controls. Does not meet standalone reproduction criteria; retain as a high-priority deployment lead.
  Reproduction scope: The 2× time-to-simulation/time-to-insight headline is a target, not a measured gain. No A/B, control tables, or code/data release links found.
  Evidence locations: Full text §§1–6; §3 four-layer stack; §4 Early experience; §5.1–5.2 two case studies.

**2610.02375 · EviDent-CBCT: Evidence-Bottlenecked Report Generation from Dental CBCT under Non-Exhaustive Report Supervision**

[Paper](https://arxiv.org/abs/2610.02375)

- **foundation-model**: Discrete evidence bottleneck for dental CBCT reports, a specialized medical application.

**2610.02369 · Automating the Application of HCI Principles: Skills for On-Demand UI Construction, the Human-AI Space to Think, and the Future of HCI**

[Paper](https://arxiv.org/abs/2610.02369)

- **agent**: HCI principles as skills, a research agenda and conceptual framework without new algorithm evaluation.
  Evidence locations: Title and complete abstract

**2610.02320 · DeskForge: Dense Supervision from Desktop Environments for Computer-Use Agents**

[Paper](https://arxiv.org/abs/2610.02320)

- **foundation-model**: DeskForge desktop interaction data and benchmark belong to Agent.

**2610.02284 · Effects of interpulse-interval variation on deep-learning classification of bat vocalizations**

[Paper](https://arxiv.org/abs/2610.02284)

- **foundation-model**: Temporal interval experiment for bat species acoustic classification, not a foundation-model algorithm.

**2610.02270 · Reliability Stress Tests and Decision-Time Routing for Chest X-ray Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.02270)

- **foundation-model**: Chest X-ray VLM stress testing and multi-agent routing, specialized medical evaluation.

**2610.02267 · Fast Models, Slow Evidence: A Paired and Self-Audited Evaluation of System-1 Decision Models for LLM Agent Harnesses**

[Paper](https://arxiv.org/abs/2610.02267)

- **agent**: Paired evaluation and self-audit of Laya/Jev System 1 decision models, not a new model.
  Evidence locations: Title and complete abstract

**2610.02247 · Toward Controlling Biology with Language:Offline Learning of Prompt-Conditioned Interventions for Cells, Organoids, and Biobots**

[Paper](https://arxiv.org/abs/2610.02247)

- **foundation-model**: Language retrieval and offline mapping over existing biological intervention records, not a general foundation algorithm.

**2610.02189 · Generative modeling of intrinsically disordered protein regions by reinforcing sparse autoencoder features**

[Paper](https://arxiv.org/abs/2610.02189)

- **post-training**: Protein IDR language models and SAE functional control, not general LLM RL/OPD.

**2610.02181 · OmniSeek: Native Tool Integration for Multi-turn Audio-Visual Reasoning**

[Paper](https://arxiv.org/abs/2610.02181)

- **foundation-model**: OmniSeek multi-turn audiovisual active-search tools and RL are reviewed under Agent.

**2610.02173 · Every Ablation Is a Dose: Counterweights and the Semblance of Self-Repair**

[Paper](https://arxiv.org/abs/2610.02173)

- **post-training**: Causal interpretation of self-repair ablations, not a post-training algorithm.

**2610.02159 · When Do Intrinsic Rewards Lead to Exploration?**

[Paper](https://arxiv.org/abs/2610.02159)

- **agent**: Counterfactual intrinsic-reward exploration theory, not an LLM policy.
  Evidence locations: Title and complete abstract

**2610.02144 · Faynt: Scaling and Optimizing Policies for Competitive Melee**

[Paper](https://arxiv.org/abs/2610.02144)

- **foundation-model**: Faynt is a specialized Smash Bros RL policy, not a general foundation algorithm.

**2610.02142 · Keyword Harnesses Fail Open: A Cheap Diagnostic Ladder for Tool-Use Claims in Small Language Models**

[Paper](https://arxiv.org/abs/2610.02142)

- **foundation-model**: Keyword harness security diagnostics and patch experiments, primarily agent diagnostics.

**2610.02074 · Homomorphic Advantage Operator: Stabilizing Reinforcement Learning Under Fully Homomorphic Encryption Constraints**

[Paper](https://arxiv.org/abs/2610.02074)

- **agent**: Homomorphic advantage under FHE constraints for classical RL.
  Evidence locations: Title and complete abstract

**2610.02045 · Form and Void: Entangled Composition through an Autonomous AI Agent**

[Paper](https://arxiv.org/abs/2610.02045)

- **foundation-model**: FaV-A is a multistage image composition agent without a new trainable foundation mechanism.

**2610.02038 · Mimir: Physics-Grounded LLM Agents for Long-Horizon Irrigation Control**

[Paper](https://arxiv.org/abs/2610.02038)

- **agent**: Mimir uses fixed water simulation, grid candidates, lexicographic choice, and a projection shield for LLM suggestions. ACE event memory only changes context. 19 crop-years, 6,938 days, four environments, temporal 60/40, and nine-season memory frozen on test. Repair ablation cost 109.1→180.5, but slices differ. Irrigation-specific ACE, MPC, and runtime protection do not add a general learning/search mechanism or public general benchmark.
  Evidence locations: Title and complete abstract

**2610.02021 · Task-Adaptive Grounded 3D-Programmers Using 2D VLMs**

[Paper](https://arxiv.org/abs/2610.02021)

- **foundation-model**: 3D-Prog uses coordinate frames and feedback programming for a frozen 2D VLM; belongs to Agent.

**2610.02015 · On Language Drift during RLVR Post-Training**

[Paper](https://arxiv.org/abs/2610.02015)

- **post-training**: Theoretical conditions and empirical analysis of language drift in RLVR, no new training mechanism.

**2610.02012 · Bellman Meets Lyapunov: Unsupervised Reinforcement Learning via Mastering Chaos**

[Paper](https://arxiv.org/abs/2610.02012)

- **agent**: F-CIP is classical RL with dynamics-derived intrinsic reward, not a language agent.
  Evidence locations: Title and complete abstract

**2610.01999 · From Reasoning Failures to Composable Video Spatial Intelligence**

[Paper](https://arxiv.org/abs/2610.01999)

- **foundation-model**: CROSS is a training-free geometry skill library and spatial agent, not foundation training.

**2610.01981 · Universal interpolation for deep residual self-attention networks**

[Paper](https://arxiv.org/abs/2610.01981)

- **foundation-model**: Mathematical universal interpolation guarantee for residual self-attention, without comparative empirical training results.

**2610.01944 · Anti-Persona: Disrupting Unauthorized Identity Binding and Recognition in Personalized Vision--Language Models**

[Paper](https://arxiv.org/abs/2610.01944)

- **foundation-model**: Anti-Persona protects image privacy with perturbations, without changing the foundation model's core training or inference.

**2610.01939 · Fewer Tokens, Better Action: GPT-6 Astra Robot Agents with 14% Higher Success Rate but 65% Fewer Tokens**

[Paper](https://arxiv.org/abs/2610.01939)

- **foundation-model**: PyRUA-Lean robot code execution and selective-observation harness belong to Agent.

**2610.01894 · A foundation for systematic analysis of transformers and RNNs for tractography**

[Paper](https://arxiv.org/abs/2610.01894)

- **recommendation**: RNN/Transformer training and imaging evaluation for dMRI tractography, outside internet recommendation and general LLM research.

**2610.01882 · Flowing Faster to Coordinate: One-Step Online Multi-Agent Flow Policies**

[Paper](https://arxiv.org/abs/2610.01882)

- **agent**: OMAF is a classical multi-agent flow policy, not an LLM agent.
  Evidence locations: Title and complete abstract

**2610.01846 · Beyond Decodability: Do Acoustic Factors Drive Predictions in Speech-Based Alzheimer's Assessment?**

[Paper](https://arxiv.org/abs/2610.01846)

- **foundation-model**: Acoustic intervention diagnostics for Alzheimer's speech assessment, no new general model algorithm.

**2610.01835 · Varda-single-1.0: deterministic data-driven weather forecasting at 1 km resolution over Switzerland's complex topography**

[Paper](https://arxiv.org/abs/2610.01835)

- **foundation-model**: Swiss regional weather modeling and validation, not a new general foundation mechanism.

**2610.01828 · The Asymptotics of Language Model Alignment with Memory**

[Paper](https://arxiv.org/abs/2610.01828)

- **post-training**: Asymptotic relation between best-of-n and KL-RL under Markov generation, not a new training algorithm.

**2610.01821 · Beyond Linear Concepts: Discovering and Aligning Non-Linear Concept Manifolds in Large Language Models**

[Paper](https://arxiv.org/abs/2610.01821)

- **foundation-model**: Interpretability of nonlinear concept manifolds and CBA metrics, no new capability training.

**2610.01766 · VideoEvolve: Evolving Agent Harnesses for Video Temporal Grounding**

[Paper](https://arxiv.org/abs/2610.01766)

- **foundation-model**: VideoEvolve evolutionary video-localization harness is reviewed under Agent.

**2610.01754 · Cog-VADU: A Training-Free Cognitive Reasoning Framework for Video Anomaly Detection and Understanding**

[Paper](https://arxiv.org/abs/2610.01754)

- **foundation-model**: Cog-VADU uses training-free temporal prompting and reranking for specialized anomaly detection.

**2610.01746 · End-to-End Learning vs. Modular Architectures: Comparative Insights into Autonomous Driving Systems**

[Paper](https://arxiv.org/abs/2610.01746)

- **recommendation**: Survey and binary decision framework comparing end-to-end and modular autonomous driving; not a new LLM/agent training algorithm.

**2610.01578 · The hidden advantage of mask resampling: a theory of masked autoencoders**

[Paper](https://arxiv.org/abs/2610.01578)

- **foundation-model**: Theory and interpretation of MAE mask resampling; no new algorithm in the abstract.

**2610.01531 · Towards Reliable Vision-Language Models for Autonomous Driving**

[Paper](https://arxiv.org/abs/2610.01531)

- **foundation-model**: Evaluates autonomous-driving VLM corruption robustness using existing VEA, no new core algorithm.

**2610.01530 · Calibrating Prediction Timeliness Through Multi-Objective Hyperparameter Optimization for Remaining Useful Life Prediction**

[Paper](https://arxiv.org/abs/2610.01530)

- **foundation-model**: Multiobjective hyperparameter optimization for remaining useful life, a predictive-maintenance application.

**2610.01514 · How the Audit Rule Shapes Faithful Factor Explanations in LLMs**

[Paper](https://arxiv.org/abs/2610.01514)

- **agent**: Theory and experiments on incentives for explanation-factor audits, not an agent execution algorithm.
  Evidence locations: Title and complete abstract

**2610.01491 · Auditing Web Agent Evaluation on WebArena-Lite: Human Review of Outcomes and Trajectories**

[Paper](https://arxiv.org/abs/2610.01491)

- **agent**: Observational WebArenaLite comparison on 165 fixed tasks using MASM actions, memory, and procedural guides. Human correction only for GPT; 25-step net +6 with paired p=.392, one rollout per task. §6 reports one guide exposing an intermediate answer and one state carryover. 55.2% showed progress under manual audit, not a new public automatic evaluator. The guide is not gold-free policy capability and does not add an eligible independent algorithm or public interface.
  Evidence locations: Title and complete abstract

**2610.01490 · The Persona Is Still There, but Who Is Speaking? Latent Identity Reversion in Persistent AI Agents**

[Paper](https://arxiv.org/abs/2610.01490)

- **agent**: Incident and controlled behavior study of lost persona system anchors.
  Evidence locations: Title and complete abstract

**2610.01451 · A Multi-Agent LLM Framework for Personalized Health Checkup Interpretation and Guidance**

[Paper](https://arxiv.org/abs/2610.01451)

- **agent**: Health-check system routes 29 intents to 13 mapped agents, up to four per request, then runs parallel RAG and fixed-order LLM synthesis. Domain integration, not a general algorithm. 120 Korean compound queries and five synthetic records; the Single baseline handles one intent, confounding coverage. Four of seven types tested; memory/prefilter untested. Not clinical safety; critical failures 15→13.3% are similar.
  Evidence locations: Title and complete abstract

**2610.01389 · AiSearch: Interactive Multi-Modal Search with VLMs**

[Paper](https://arxiv.org/abs/2610.01389)

- **foundation-model**: AiSearch uses existing VLMs in interactive multimodal retrieval without a new foundation mechanism.

**2610.01364 · LLM-Driven Multi-Agent Control for Skill-Based Smart Manufacturing**

[Paper](https://arxiv.org/abs/2610.01364)

- **agent**: Manufacturing MCP wraps OPCUA and MQTT with external state and physical-tool masks. Compares standard orchestrator/peer/monolithic layouts, no new general planning. Nine simulation tasks × ten runs with one Gemma4 31B; timing/tokens condition on success. Mono/peer 93%, orchestrator 87%, reversed on silent faults. Not real-factory deployment or a new general public benchmark.
  Evidence locations: Title and complete abstract

**2610.01345 · ARCCS: An Automated Regulatory Compliance Checking System**

[Paper](https://arxiv.org/abs/2610.01345)

- **agent**: ARCCS segments regulations, extracts atomic requirements, checks scope and RAG evidence, and applies four-label confidence gates for human review. No general optimization/planning. GDPR: three terms documents, 100 requirements, 90 LLM judgments without deterministic gold. Procurement: 100 synthetic traces × 12 rules, a sanity check rather than legal coverage. Not a general Agent/evolve benchmark.
  Evidence locations: §2.1–2.3; §3.1–3.3; §4; §5

**2610.01325 · PPO-HRAP: Proximal Policy Optimization with a Hybrid Regime-Aware Policy for Risk-Controlled Trading**

[Paper](https://arxiv.org/abs/2610.01325)

- **agent**: PPO-HRAP combines volatility priors with classical financial RL, not a language agent.
  Evidence locations: Title and complete abstract

**2610.01275 · Know When to Hold 'em: Correct-Token Retention in Uniform-State Diffusion Language Models**

[Paper](https://arxiv.org/abs/2610.01275)

- **post-training**: USDM correct-token retention is diffusion pretraining/architecture loss, routed to foundation.

**2610.01257 · Science Utopia? Closed-Loop LLM Simulation of Academic Research Ecosystems**

[Paper](https://arxiv.org/abs/2610.01257)

- **agent**: Suto simulates ten years of academia: researchers choose already available SciEvo papers rather than conduct research. Three-reviewer mean scores and quotas govern acceptance; grant ranks and budget exits close the loop. Worlds with 5,000 researchers study institutional simulation, not general agent optimization or real research capability.
  Evidence locations: §2.1–2.2; §3.1–3.4; §5

**2610.01234 · ASCRIBE: Atomic and Significance-Based Reasoning for Thai Clinical SOAP Note Generation**

[Paper](https://arxiv.org/abs/2610.01234)

- **post-training**: ASCRIBE structures atomic facts and clinical importance with five domain rewards, using LoRA SFT and standard GRPO. No new core optimizer/distillation; clinical application.

**2610.01195 · Federated Agent Optimization**

[Paper](https://arxiv.org/abs/2610.01195)

- **agent**: Federated Agent Optimization defines a problem and agenda without implementing a new algorithm.
  Evidence locations: Title and complete abstract

**2610.01184 · ReCast: Contract-Preserving Protection for Fixed-Interface Multimodal Reasoning**

[Paper](https://arxiv.org/abs/2610.01184)

- **foundation-model**: ReCast privacy-preserving media reconstruction and remote solving workflow belongs to Agent.

**2610.01180 · Skeleton-and-Strategy Prompting: Training-Free Negation Understanding for Vision-Language Models**

[Paper](https://arxiv.org/abs/2610.01180)

- **foundation-model**: SSP retrieves examples and prompts for negation understanding without a new trainable core.

**2610.01166 · CineMR: Tool-Integrated Vision-Language Reasoning for Quantitative Cardiac MRI Assessment**

[Paper](https://arxiv.org/abs/2610.01166)

- **foundation-model**: CineMR is a specialized cardiac MRI medical tool-use agent.

**2610.01102 · MASkillBlender: Decentralized Whole-Body Coordination for Multi-Humanoid Loco-Manipulation via Skill Blending**

[Paper](https://arxiv.org/abs/2610.01102)

- **agent**: MASkillBlender is classical multi-humanoid RL skill blending, not an LLM policy.
  Evidence locations: Title and complete abstract

**2610.01093 · OrbitTAMP: Grounding Language Models for Task and Motion Planning in Spacecraft Rendezvous**

[Paper](https://arxiv.org/abs/2610.01093)

- **agent**: OrbitTAMP converts language to partial MissionConfig, enumerates and scores behavior-time graphs, then uses waypoint/SCP planning. Preserves given fields; safety comes from downstream constraints. 1000 test cases are 10% on-grid module data without language/behavior selection. Uses greedy waypoints rather than learned proposals. Space-specific graph and dynamics TAMP, no standalone general Agent innovation.
  Evidence locations: §III-A–B; §IV-D/E; §V-A/TableIII

**2610.01027 · LawCompass: Navigating from Legal QA to Multi-Agent Deep Research with Grounded Evidence**

[Paper](https://arxiv.org/abs/2610.01027)

- **agent**: LawCompass offers QA, retrieval, and deep research, with LangGraph planning 3–5 tasks, schema repair/fallback, and a citation catalog. Twenty queries with manual Top-5 retrieval and subjective usability do not validate long legal tasks. Domain RAG and routing, no new core operator or public task/scorer.
  Evidence locations: §4.1–4.5; §5.1–5.2

**2610.00991 · Adapter Thickets: Splitting an RLVR Budget Beats Concentrating It**

[Paper](https://arxiv.org/abs/2610.00991)

- **post-training**: Adapter thickets compare fixed training/160 inference-rollout budgets, randomly sharded LoRAs, standard GRPO, and voting. An allocation/ensemble study, not a new loss.

**2610.00988 · Auditable Algebraic Counting Field for Cryptic-Pocket Detection from Apo Structures**

[Paper](https://arxiv.org/abs/2610.00988)

- **post-training**: Supervised algebraic fields for cryptic pockets in apo proteins, not LM post-training.

**2610.00984 · HADRec: A Hierarchy-Aware Drug Recommendation Framework by Fusing Molecular Knowledge and Electronic Health Record**

[Paper](https://arxiv.org/abs/2610.00984)

- **recommendation**: HADRec combines molecules, EHR, and ATC hierarchy for clinical drug recommendation on MIMIC, outside internet recommendation; offline medical metrics are not deployment.

**2610.00973 · Concept Driven Domain Adaptation: Finding an Abstract Needle in a Haystack**

[Paper](https://arxiv.org/abs/2610.00973)

- **foundation-model**: CDDA adapts retrieval to middle-school physics videos, not a general foundation-model algorithm.

**2610.00954 · Beyond Leaderboards: Tokenomics of Agentic Small Language Model Ensembles**

[Paper](https://arxiv.org/abs/2610.00954)

- **post-training**: SLM ensemble inference feedback and token/cost evaluation without parameter post-training.
- **agent**: SLM ensemble tokenomics case study; abstract focuses on evaluation, not a core training method.
  Evidence locations: Title and complete abstract

**2610.00922 · EyeTAG: Eye Trajectory-Aware Gaze Estimation**

[Paper](https://arxiv.org/abs/2610.00922)

- **foundation-model**: EyeTAG is a domain-specific temporal motion prior for gaze estimation.

**2610.00917 · Finding the Right Fit: Model-Harness Interactions across Agent Tasks**

[Paper](https://arxiv.org/abs/2610.00917)

- **agent**: Empirical comparison of 66 configurations across three fixed agent benchmarks. Native pairs are not always best, but models, context, tools, and timeouts vary. One counted run per task, using latest infrastructure reruns and zero for missing results, does not identify component effects. No new training/planning method or public task/scorer; trajectory proposals untested.
  Evidence locations: §3.1–3.4; §4.1; §7–8

**2610.00905 · Understanding Issues, Causes and Solutions in Open-Source LLM-based Multi-Agent Systems**

[Paper](https://arxiv.org/abs/2610.00905)

- **agent**: Empirical study of issue causes and remedies in open-source multi-agent projects.
  Evidence locations: Title and complete abstract

**2610.00903 · Sharpen Before You Adapt: Data-Free Entry-State Sharpening for Test-Time Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00903)

- **post-training**: Entry-state sharpening unifies analysis of SPIRAL, R-Zero, and majority-pseudolabel SFT preparation for TTRL. No new algorithm specified; retains GRPO and self-distillation.

**2610.00898 · When Do Biological Reasoning Models Use Their Biological Inputs?**

[Paper](https://arxiv.org/abs/2610.00898)

- **post-training**: Public bio-mirage intervention/conflict benchmark verified, but requires Evo2, protein/single-cell encoders and KEGG/ChatNT/C2S tasks. Not general post-training or Agent evaluation here; keep as biological modality reference.

**2610.00890 · Cross-Benchmark Transfer from RL on Agentic Coding Tasks**

[Paper](https://arxiv.org/abs/2610.00890)

- **agent**: KimiK2.7Code uses rank-32 LoRA and existing GSPO on 1,700 expert repo/terminal tasks. All-pass pass-to-pass gate multiplies fail-to-pass scores; masks tool tokens and filters overlong sequences. One epoch on 64 H200s. Six benchmarks/five independent transfer sets and a prespecified final checkpoint provide evidence, but partial public baselines, TB3trained8 infrastructure exclusions, and one recipe do not isolate innovation. No new core RL/OPD or public 1,700-task runner; retain as experimental reference.
  Evidence locations: §3.3; §4.1–4.3; §5–6/Table2; §8

**2610.00888 · Match the Distribution, Not the Compute: Post-Training Multi-Token Prediction Heads**

[Paper](https://arxiv.org/abs/2610.00888)

- **post-training**: MTP head training and speculative verification serving belong to foundation, not core RL/OPD.

**2610.00883 · DeBERTa-ConPara: Attack-Aware and Deployment-Realistic Detection of AI-Generated Text**

[Paper](https://arxiv.org/abs/2610.00883)

- **foundation-model**: Unicode preprocessing for a DeBERTa generated-text detector, a specialized application.

**2610.00881 · Machine Translation for Sign Languages**

[Paper](https://arxiv.org/abs/2610.00881)

- **foundation-model**: Survey of sign-language machine translation, no new algorithm.

**2610.00870 · An Educator-Guided LLM Pedagogical Agent for Scaffolded Feedback in Conceptual Database Design**

[Paper](https://arxiv.org/abs/2610.00870)

- **agent**: In four-stage ERD instruction, teachers control disclosures; the LLM picks written questions, fills templates, and gives later feedback. Episode memory is not a persistent learner model. Of 63 students, 48 completed; 383 voluntary episodes produced only 186 later artifacts. 71.1% target incorporation is conditioned on diagram revision and not correctness. No controlled learning benefit, general agent core, or executable public benchmark.
  Evidence locations: §3.2–3.4; §4 classroom study/4.2/4.3; §5.

**2610.00852 · Child-Adapted Structured Phonological Representations for Interpretable Speech Sound Analysis**

[Paper](https://arxiv.org/abs/2610.00852)

- **post-training**: Adapts phonological representations for children's speech, not language-model policy training.

**2610.00849 · Learning Multiple Timescales for Goal-Conditioned Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00849)

- **agent**: GITA is classical multiscale offline goal-conditioned RL, no LLM agent.
  Evidence locations: Title and complete abstract

**2610.00848 · Geometric Similarity in VLM Low-Level Vision Representations**

[Paper](https://arxiv.org/abs/2610.00848)

- **foundation-model**: GeoSim interprets multilayer geometric representation similarity without a new foundation-model training algorithm.

**2610.00809 · Paying for Too Many Tokens? Valid and Cost-Efficient Multimodal LLM Annotation with Simple Heuristics**

[Paper](https://arxiv.org/abs/2610.00809)

- **foundation-model**: Sampling and grid-heuristic evaluation for social-science video annotation, no new core model.

**2610.00795 · Can large language models unlock discrete data in ophthalmic diagnostic reports?**

[Paper](https://arxiv.org/abs/2610.00795)

- **foundation-model**: Twenty-case ophthalmology PDF extraction proof of concept, a specialized medical application.

**2610.00758 · Scalable Multi-Task Inverse Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00758)

- **agent**: Low-rank multitask inverse RL and state-coverage theory, not core LLM agent control, memory, or tools.
  Evidence locations: Title and complete abstract

**2610.00705 · Meta-Multi-Agent Reinforcement Learning for Fast Adaptation of Interactive Policies with Applications to Autonomous Driving**

[Paper](https://arxiv.org/abs/2610.00705)

- **agent**: Markov-game meta-NE/gradient-play adaptation and autonomous-driving policies, outside LLM agents.
  Evidence locations: Title and complete abstract

**2610.00694 · How Divergence Becomes Decision Flips in Compressed Language Models**

[Paper](https://arxiv.org/abs/2610.00694)

- **foundation-model**: Measures the relationship between compressed-model TV and decision flips; analysis, not a new capability algorithm.

**2610.00680 · Curvature Under Attack in hZACH-ViT: Gauge Symmetry, Boundary Saturation, and Adversarial Failure**

[Paper](https://arxiv.org/abs/2610.00680)

- **foundation-model**: Diagnoses curvature and adversarial boundary saturation in small ViTs without a general foundation algorithm.

**2610.00677 · Harnessing Vision-Language Models for Perceptual Quality Assessment and Autonomous Content Adjustment in Augmented Reality**

[Paper](https://arxiv.org/abs/2610.00677)

- **foundation-model**: RateAR perceptual benchmark and automatic AR adjustment application, no core foundation mechanism.

**2610.00665 · Analysis of Quantized and Efficiently Adapted Protein Language Models**

[Paper](https://arxiv.org/abs/2610.00665)

- **foundation-model**: Evaluates existing QLoRA quantized adaptation on protein LMs, no new core algorithm.

**2610.00654 · When More Data Is Not Enough: The Context-Sufficiency Frontier in Generative AI Personalization**

[Paper](https://arxiv.org/abs/2610.00654)

- **recommendation**: Home retail context sufficiency uses two constructed users, one request, and a 32×10 offline factorial study on the main model. Retail catalogs are not online A/B.

**2610.00629 · ASAD: Adaptive Software Agents for Debugging**

[Paper](https://arxiv.org/abs/2610.00629)

- **agent**: ASAD prompts its main agent with static complexity to choose a simple fix or sequential roles, allowing up to three edits per agent and five global iterations. LLM-generated roles/priorities are not a defined new optimizer. Three existing debug benchmarks, 100 samples × five runs, and 223 manually checked Defects4J cases; passing tests is not correctness. Runtime feedback/multi-file coordination are future work. Standard planner/specialist/reviewer integration, not a new core.
  Evidence locations: §III-B–D; §IV-C; §V-D; §VII; Conclusion

**2610.00622 · Understanding and Mitigating Library-Related Issues in LLM-Generated Code**

[Paper](https://arxiv.org/abs/2610.00622)

- **agent**: Analyzer extracts JSON dependencies, searches official docs and gathers imports/snippets, then Generator iterates with compile/import and LLM validation. Existing library-grounded RAG/self-refinement integration. Real ablations on 300 tasks/five models, but compilation does not run logic and automatic pip installs do not prove correctness or safety. No new retrieval-version protocol, algorithm, or independent public scorer.
  Evidence locations: §IV-A–E; §V; §VI-A and ablations.

**2610.00619 · Beyond Supra-Competitive Outcomes: Collusive Behaviour in Deep Reinforcement Learning for Optimal Execution Games**

[Paper](https://arxiv.org/abs/2610.00619)

- **agent**: PPO collusion behavior and penalties in financial execution games, not an LLM agent method.
  Evidence locations: Title and complete abstract

**2610.00610 · Explainable Suicide Risk Assessment on Social Media with Multi-Task QLoRA**

[Paper](https://arxiv.org/abs/2610.00610)

- **post-training**: Suicide-risk shared-task system uses standard multitask QLoRA with probability averaging/cross-fold aggregation, a domain application rather than a general algorithm or new evaluation protocol.

**2610.00592 · ALER: Adaptive Learnable Experience Rewriting for Reinforcement Learning**

[Paper](https://arxiv.org/abs/2610.00592)

- **foundation-model**: ALER partially observable RL with slot memory belongs to Agent review.
- **agent**: Traditional partially observable RL experience rewriting with LSTM and slot memory, not an LLM agent method.
  Evidence locations: Title and complete abstract

**2610.00590 · Towards Hierarchical Cyber Defense with Large Language Models: From Planning to Execution**

[Paper](https://arxiv.org/abs/2610.00590)

- **agent**: Cyberwheel switches subnet planning and primitive execution between PPO and frozen LLMs under noisy local detectors, using 20 episodes × 100 steps per seed. Strong LLM+LLM wins while smaller models are unstable. Three known hierarchy configurations in a defense simulator, one global seed, no new general operator or public task definition.
  Evidence locations: §3.2–3.5; §4.1–4.4; §5.1–5.3

**2610.00562 · Can LLMs Reason Over Long Horizons? An Empirical Evaluation of Context Strategies for Longitudinal Clinical Reasoning**

[Paper](https://arxiv.org/abs/2610.00562)

- **foundation-model**: MedLoCoMo compares long-context clinical strategies, a specialized evaluation.

**2610.00557 · No One Architecture Fits All: A Cross-Environment Evaluation of Hierarchical Red Team Agents**

[Paper](https://arxiv.org/abs/2610.00557)

- **agent**: Compares existing RL+RL and LLM+LLM across CybORG/Cyberwheel and analyzes bottlenecks; no new mechanism.
  Evidence locations: Title and complete abstract

**2610.00540 · Assessing the Impact of Language Disparity on Multilingual Linguistic Ability in Large Language Models**

[Paper](https://arxiv.org/abs/2610.00540)

- **post-training**: Compares four existing MultiBLiMP readouts across 101 languages. Linguistically informed interpretation, no independent new benchmark or training method in abstract.

**2610.00511 · Before Agents Decide: Epistemic Action in LLM-Based Systems**

[Paper](https://arxiv.org/abs/2610.00511)

- **agent**: Conceptual taxonomy and design argument for epistemic actions, without implementation or empirical evidence.
  Evidence locations: Title and complete abstract

**2610.00430 · Memetic Trojans: Social Contagions as Carriers of Adversarial Payloads in Agent Networks**

[Paper](https://arxiv.org/abs/2610.00430)

- **agent**: Vulnerability and network simulation analysis of adversarial payload propagation, not a method to improve core agent capability.
  Evidence locations: Title and complete abstract

**2610.00406 · LLM-as-a-Judge for Low-Resource Languages: Adapting Ragas and Comparative Ranking for Romanian**

[Paper](https://arxiv.org/abs/2610.00406)

- **foundation-model**: Romanian RAG judging strategies and benchmark, without a new core model mechanism.

**2610.00398 · WIPSNet: Deep Learning for Paediatric Wheeze Detection from Overnight Impedance Pneumography**

[Paper](https://arxiv.org/abs/2610.00398)

- **foundation-model**: WIPSNet uses a domain-specific 3D ResNet for pediatric impedance respiratory measurements, not a general mechanism.

**2610.00374 · Faithful Chart Generation for Multimodal Deep Research: Frame-Evidence Co-Adaptation**

[Paper](https://arxiv.org/abs/2610.00374)

- **foundation-model**: FECA evidence-adaptive chart-planning agent workflow, without a new foundation core.

**2610.00367 · MoRA: MoE Pruning via Router Bias Learning and Expert Approximation**

[Paper](https://arxiv.org/abs/2610.00367)

- **post-training**: MoRA learns router bias and affine expert-output approximations for MoE pruning. Routed to foundation review, not globally rejected.

**2610.00363 · Deep Learning for Anomaly Detection in Railway Systems: A Structured Survey**

[Paper](https://arxiv.org/abs/2610.00363)

- **foundation-model**: Structured review of railway anomaly detection, no new algorithm.

**2610.00302 · Decoding the Disaster: Multi-Task Geospatial Reasoning with Vision-Language Models and Crowdsourced Imagery for Disaster Mapping**

[Paper](https://arxiv.org/abs/2610.00302)

- **foundation-model**: GRDisaster geolocates disaster street imagery and grades damage, a domain benchmark not yet integrated as a general task.

**2610.00256 · Verification Pulses and the Cost of Escaping Wrong Consensus**

[Paper](https://arxiv.org/abs/2610.00256)

- **post-training**: Verification-pulse control theory for binary consensus registers and LM response tests. Schedule-comparison intervals include zero; no standalone general LLM training/evaluation component.

**2610.00253 · System Attribution in LLM Brand Recommendations: Single Responses Identify the System, Aggregated Brand Profiles Do Not Transfer**

[Paper](https://arxiv.org/abs/2610.00253)

- **recommendation**: Audits output attribution and brand bias, not an online recommendation algorithm. Routed to general evaluation.
- **foundation-model**: Existing character n-grams and random forests explain a brand-recommendation corpus. Domain and harness are not crossed; aggregate profiles fail across domains. No foundation algorithm; code/full data require requests and no independent public evolve task exists.
  Evidence locations: §1–4; §6.4–6.5; §7; Data Availability/Code Availability

**2610.00223 · A Holistic Assessment of the Carbon Footprint of Noor, a Very Large Arabic Language Model**

[Paper](https://arxiv.org/abs/2610.00223)

- **foundation-model**: System-wide carbon footprint assessment of Noor, no new model algorithm.

**2610.00196 · GPEC: Efficient Pre-LLM Gaussian Process Embedding Correction for Cardiac Video Caption Generation**

[Paper](https://arxiv.org/abs/2610.00196)

- **foundation-model**: GPEC Gaussian-process residual adaptation for cardiac-video captioning, a medical application.

**2610.00188 · Uncertainty-Aware RL-Controlled Adaptive 3D Mapping**

[Paper](https://arxiv.org/abs/2610.00188)

- **agent**: RL controls TSDF voxel subdivision for 3D mapping, not an LLM agent method.
  Evidence locations: Title and complete abstract

**2610.00106 · SyntheticHLS: Building Diverse Synthetic High-Level Synthesis Datasets using LLMs**

[Paper](https://arxiv.org/abs/2610.00106)

- **foundation-model**: SyntheticHLS generates and mutates hardware-synthesis data with an agent, not general foundation training.

**2610.00096 · FACET at WMT 2026 Automated Translation Quality Evaluation Task**

[Paper](https://arxiv.org/abs/2610.00096)

- **post-training**: FACET decomposes translation quality using three fixed model prompts for WMT, with no training or new general executable framework.

**2610.00093 · Safety in Self-Evolving Agents: A Survey**

[Paper](https://arxiv.org/abs/2610.00093)

- **agent**: Survey of self-evolving agent safety and SAVER taxonomy, not a new reproducible algorithm.
  Evidence locations: Title and complete abstract

**2610.00084 · Scientific Agents: Evaluating Profession-Specific System Prompts on Scientific Tasks**

[Paper](https://arxiv.org/abs/2610.00084)

- **agent**: Controlled comparison of 503 occupational system prompts with negative cost results, no new agent capability mechanism.
  Evidence locations: Title and complete abstract

**2610.00069 · A Framework for Egocentric and Exocentric Procedural Understanding via Temporal Segmentation and Semantic Abstraction**

[Paper](https://arxiv.org/abs/2610.00069)

- **foundation-model**: Work-event memory design and evaluation outline using frozen DINOv2/VJEPA2, an agent conceptual framework.

**2610.00047 · Characterizing a Configuration Where Inference-Time PRM-Pruned Fragment Grafting Is Inert: Evidence from Three Reasoning LMs**

[Paper](https://arxiv.org/abs/2610.00047)

- **post-training**: PPFG is a null-effect/equivalence test for specific inference fragment grafting, a useful negative result without a new training algorithm or general benchmark.

**2610.00035 · Integrating Fairness and Explainability in a Multiple Instance Reinforcement Learning System**

[Paper](https://arxiv.org/abs/2610.00035)

- **post-training**: RL-MIL and a fairness hypernetwork for educational risk, not language-model training or general LLM evaluation.
- **agent**: Student-risk RL-MIL fairness hypernetwork and mode-collapse analysis, not an LLM agent method.
  Evidence locations: Title and complete abstract

**2610.00031 · Seeing the City or Recognizing the Place? What Street-View Imagery Adds Beyond Existing Urban Data in VLM-Based Urban Sensing**

[Paper](https://arxiv.org/abs/2610.00031)

- **foundation-model**: Diagnoses geographic record dependence in street-view predictions, a domain urban data-quality study.

**2610.00024 · Encoded but Disconnected: Decomposing Vision-Language Model Failures under a Patching Null**

[Paper](https://arxiv.org/abs/2610.00024)

- **foundation-model**: Negative VLM mid-layer patching results and oracle-label interventions. Explicitly not deployable and not eligible as evolve capability improvements.
