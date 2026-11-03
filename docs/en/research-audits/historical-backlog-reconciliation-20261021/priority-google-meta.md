# Confirmed Google/Meta priority shortlist (9)

<!-- source-sha256: 98974d3f5e30392eb4fae54ef8fb3ad4aa52772f6e6f84111efe94208912eb41 -->

[简体中文](../../../research-audits/historical-backlog-reconciliation-20261021/priority-google-meta.md)

These nine priorities have author, affiliation, or participation evidence from the original papers. They do not exhaust affiliations across all candidates.
No matching runnable implementation or metrics were found. Full-experiment costs and possible low-cost components are listed separately.
This round verified only: no implementation, training, or changes to the original ledger. This report records terminal full-experiment cost/source decisions for all nine.
Later synchronization of the original ledger and classifier is data repair, not a restart of these full experiments.
Cost closure applies only to the full experiment and does not implement an unfinished low-cost component.

## 2610.07289 · Catching Developers in the Flow: Low-Latency Agentic Program Repair at Google Scale

- Affiliation/role: The official HTML author block identifies the first author and all coauthors as Google (New York).
- Author code: Data Availability explicitly says the reproduction package and data cannot be released; no author source was found.
- Affordable scope: Define a faithful bounded public APR core separately: pre/post abstention filters, actual LLM ReAct generate-and-validate, real patch application and test execution, and latency logs. Do not claim internal production reproduction. The cost of this separate small run is not established.
- Full experiment: Production verification uses private source, internal CI/developer tools and models, and millions of changes. Close unavailable original-environment reproduction rather than keeping an indefinite implementation debt.
- Final full-experiment disposition: Private production environment cannot be reproduced publicly; review DONE.
- Recommended low-cost scope: Keep the accepted status but separately scope and assess a public core. The full Google production experiment is not reproduced because resources are private; it is not a pending GPU task.
- Evidence: [Paper](https://arxiv.org/html/2610.07289v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2610.06616 · Video Encoders Built on Image Representations

- Affiliation/role: First author at Stanford; the DeepMind coauthor participated only in an advisory capacity. Do not call this a Google first-author paper.
- Author code: No author source repository was located in the official HTML reviewed; this does not prove nonrelease everywhere.
- Affordable scope: Appendix C.1 specifies a separate training-free selection-only variant. Preserve source positions in actual frozen image-encoder features, then select under a fixed token budget using question relevance, DPP diversity, and cross-frame correspondence, without the learned refiner. CPU checks can cover equivalence, budget, and positions. A small real 7B/8B checkpoint run needs separate resource and GPU checks; random features are not capability evidence.
- Full experiment: Appendix C.3: 65K Video-ChatGPT subset, two epochs, 8×A100×12h = 96 GPU hours for the refiner alone, plus three backbones and 13 benchmarks. Full experiments are too costly (review DONE); that figure does not rule out selection-only.
- Final full-experiment disposition: Too costly, not reproduced (review DONE).
- Recommended low-cost scope: Close full-refiner and all-table experiments. Keep selection-only as an affordable core candidate with clear fidelity boundaries; not implemented.
- Evidence: [Paper](https://arxiv.org/html/2610.06616v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2610.00497 · Gumbel Straight Flow: Distilling Autoregressive Models into One-step Flow Maps

- Affiliation/role: The author footnote says the first author's work was done as a Google DeepMind Amsterdam Student Researcher.
- Author code: The reviewed official HTML has no author implementation link; no exhaustive nonrelease claim.
- Affordable scope: A bounded L1 version could use a small vocabulary, short sequences, real autoregressive teacher and flow-map student, posterior Gumbel sampling, monotonic Gaussianization, diagonal CE, off-diagonal semigroup self-consistency, actual gradients, and one-step sampling. Keep both trained models and core losses; straight-line fixtures do not suffice. The scaled run is not costed or implemented.
- Full experiment: Appendix C uses batch 512 and up to 1M steps for teacher/GSF-FM/GSF. The main student is 167.8M, with additional data/conditional tasks and teacher training. A fair full campaign exceeds a short single-A100/A30 run; too costly, not reproduced (review DONE).
- Final full-experiment disposition: Too costly, not reproduced (review DONE).
- Recommended low-cost scope: Close the full experiment for cost. Cheap formula and training-mechanism checks remain bounded candidates, not a GPU delivery commitment.
- Evidence: [Paper](https://arxiv.org/html/2610.00497v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2602.16490 · From Growing to Looping: A Unified View of Iterative Computation in LLMs

- Affiliation/role: Collaboration among TUM, Helmholtz AI, and Google Paradigms of Intelligence; not verified as Google-led alone.
- Author code: Neither the prior review nor the official HTML read this round located an author repository.
- Affordable scope: Scope a small Transformer that actually trains: copy intermediate layers and AdamW states for depth growth, and reuse that block in real forward passes for inference looping. Record parameter, training, and inference budgets and select loop settings on validation only. Copy/loop mechanics do not establish inference gains; a full reduced run still needs cost review.
- Full experiment: §4.1: SmolLM 360M/1.7B uses about 200B/400B tokens, with 22 benchmarks, growing/looping recipes, and further-training controls. Full training exceeds current single-GPU/local budgets and is not reproduced (review DONE).
- Final full-experiment disposition: Too costly, not reproduced (review DONE).
- Recommended low-cost scope: Close original-scale training. Small real-model mechanics require separate acceptance; do not keep 200B pretraining as implementation debt.
- Evidence: [Paper](https://arxiv.org/html/2602.16490v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2510.15831 · VISTA: A Test-Time Self-Improving Video Generation Agent

- Affiliation/role: Official project lists the first author as a Google Student Researcher/NUS and other authors at Google.
- Author code: The official project links paper, demos, and prompts but no author code; this is not exhaustive.
- Affordable scope: Affordable checks cover tournament/champion state, three critique dimensions, and DTPA prompt revision orchestration only. Without actual video generation and multimodal judging, this is L0 diagnostic, not core reproduction. The defining method regenerates video each round, so no immediately actionable low-cost capability implementation was established.
- Full experiment: §4 uses 100 MovieGen prompts and 161 private prompts with Gemini 2.5 Flash and Veo 3. §4.3 reports about 0.7M tokens and 28 videos per round, excluding video-generation tokens. Multiple rounds/baselines are costly and private data unavailable. Full reproduction not run (review DONE).
- Final full-experiment disposition: Too costly, not reproduced (review DONE).
- Recommended low-cost scope: Close full VISTA on cost and retain documentation; fixed videos or scores are not implementation or evolve capability.
- Evidence: [Paper](https://arxiv.org/html/2510.15831v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2610.09159 · SpecGuard: Proving a Task Is Broken Before the Agent Cheats

- Affiliation/role: First author Param Biyani is at MATS; Krishnamurthy Dvijotham coauthored from Google DeepMind. Not Google first author.
- Author code: Public author repository under Apache 2.0: https://github.com/prmbiy/specguard, including src/conflict_certifier, configs, data, scripts, tests, and RESULTS.
- Affordable scope: Highest-priority bounded faithful path: an actual model sees D+C but not T and generates spec.lean; independent TestAgent writes tests.lean; the real Certifier connects them and calls the Lean kernel. Keep conflict/no-conflict/inconclusive and semantic fidelity audit. A few public or custom tasks may need no model training. No handwritten gold to bypass autoformalization, and Lean passing is not semantic correctness.
- Full experiment: §5 uses three agents with one model, SpecAgent 120 Bash turns, ten Lean feedback rounds per agent, and one-hour task timeouts. 349 SWE tasks plus models/repeats/baselines, 187 VERINA, and 95 LiveCodeBench among others. At the reported USD 0.26/task, 349 tasks are USD 90.74 for one arm and about USD 272.22 for three repeats (inferred, not local spend). Close the full multi-hour campaign without ruling out a real small sample.
- Final full-experiment disposition: Too costly, not reproduced (review DONE).
- Recommended low-cost scope: Keep real small-sample Lean as the highest-priority affordable candidate, still unimplemented. No promise to reproduce all models and benchmarks.
- Evidence: [Paper](https://arxiv.org/html/2610.09159v1); see [Google reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/google-review.json) for passage locations.

## 2610.06064 · TrustMI: Causally controlling how assistants trust their users

- Affiliation: Meta authorship or collaboration verified from the original.
- Paper resources: Official original §4, Appendix C/D.2/D.4: six 7B-70B models; learned steering matrices trained 10 epochs, 120B judge on H100, multiple agent and capability benchmarks, mostly three repetitions. Full campaign should not be treated as an affordable automatic TODO; smaller faithful scope requires explicit cost assessment.
- Missing deliverables: Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- Final full-experiment disposition: Too costly, not reproduced (review DONE). Define a separate scope before attempting affordable faithful components; fixed simulators or graph answers are not substitutes for the core algorithm.
- Evidence: [Paper](https://arxiv.org/html/2610.06064v1); §4; Appendix C; Appendix D.2-D.4 (web lines 164-170, 763-802); see [Meta reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/meta-review.json) for repository locations.

## 2610.04721 · Knossos and Ariadne: Benchmarking and Learning Complete Diagram Topology Extraction with Vision-Language Models

- Affiliation: Meta authorship or collaboration verified from the original.
- Paper resources: Official original Appendix E.1/Table10: NODE1125, EDGE5960, TRACE5801 steps for each 8B/9B backbone; 4 A100 GPUs, QLoRA. Full original reproduction exceeds single A100/A30 campaign budget; ledger has not recorded terminal cost closure.
- Missing deliverables: Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- Final full-experiment disposition: Too costly, not reproduced (review DONE). Define a separate scope before attempting affordable faithful components; fixed simulators or graph answers are not substitutes for the core algorithm.
- Evidence: [Paper](https://arxiv.org/html/2610.04721v1); Appendix E.1 Table10 (web lines 681-693); see [Meta reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/meta-review.json) for repository locations.

## 2610.09484 · MIMESIS: Learning User Simulators as Training Environments for Interactive Agents

- Affiliation: Meta authorship or collaboration verified from the original.
- Paper resources: Official original A.1/Table4: mid-training32 A100 for about4.8days, 9.51B tokens; SFT8 A100; A.3/Table7 simulator RL16 A100/500steps/512rollouts; D.1/Table13 actor RL16 A100. No repository cost terminal is recorded.
- Missing deliverables: Exact ID/title/name search in docs/src/tests found review artifacts only, no reproduction directory, adapter, runnable paper implementation or local metrics for this identity.
- Final full-experiment disposition: Too costly, not reproduced (review DONE). Define a separate scope before attempting affordable faithful components; fixed simulators or graph answers are not substitutes for the core algorithm.
- Evidence: [Paper](https://arxiv.org/html/2610.09484v1); Appendix A.1 Table4, A.3 Table7, D.1 Table13 (web lines 304-328, 382-427, 658-678); see [Meta reconciliation](../../../research-audits/historical-backlog-reconciliation-20261021/data/meta-review.json) for repository locations.

## Coverage limits

Most old candidates lack independently verifiable complete author-affiliation blocks.
We cross-checked 45 cached author fields and specifically read official author blocks for priority papers. Some cached fields were incomplete.
We therefore cannot rule out Google/Meta coauthors elsewhere. Using Gemini or Llama is not affiliation evidence.
