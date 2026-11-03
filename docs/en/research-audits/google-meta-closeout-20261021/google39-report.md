# 39 Google/DeepMind leads: bounded primary-source review

<!-- source-sha256: 377f1daf89050ea1448c089468183a030dab25e00ce9b6395ebdce87fd47e497 -->

[简体中文](../../../research-audits/google-meta-closeout-20261021/google39-report.md)

The frozen list covers **39 unique arXiv IDs**: 16 affordable core/evaluation candidates (all unimplemented at this snapshot), 14 full reproduction closures for cost/private resources, and nine scope closures. **No new implementation, training, model download, automatic implementation/retry, or Evolve integration.** SpecGuard and Video Encoder Selection are independently accepted by the parent batch.

Review DONE means the listed method, experiment, resource, and public-code sections were examined. It does not mean full sequential reading, latest revision coverage, or reproduction. All have `full_article_read=false`. No paper was wholly inaccessible: terminal arXiv DNS failures remain recorded, but browser access to official HTML succeeded. No source exception was invented, no global watermark advanced, and the scope did not expand to all 497 historical opportunities.

## Evidence and time boundaries

- [Machine-readable table](../../../research-audits/google-meta-closeout-20261021/google39-reviews.json) records dispositions, methods, experiments, costs, checked sections, and hashes. [Code-source receipts](../../../research-audits/google-meta-closeout-20261021/evidence/google39-code-primary-receipts.json) verify access, not execution.
- Official arXiv excerpt window: 2026-10-20 18:48:00–18:56:04 UTC. Code review: 18:56:34–18:57:03 UTC. These are bounded session windows, not exact per-request timestamps.
- Frozen ID-order SHA-256, one ID per line with final newline: `8623baeb7c2e1132ce70ede629aef201b24ab6cbdfa5038e9848acb7beae6f3b`.
- `source_sha256` hashes public URL/location/UTC and Chinese paraphrase receipts; `original_capture_sha256` binds raw browsing captures. **Long captures remained private temporary files, not committed; neither hash represents complete HTTP responses or the full papers.** Public receipts contain neither internal browsing references nor lengthy verbatim text. DeepXiv, Superpowers, and secondary summaries did not replace original sources.
- Review targeted v1 sections. Known revisions, such as Cogeneration and ME-POIs v3, were not falsely marked rechecked.

## Key judgments

- AI-Propeller §5.4 reports production Search +0.23% versus deployed Ext-TSP. Retain this even without A/B in the abstract. The body does not identify traffic allocation/scale or explicit full traffic, so the strict gate remains unconfirmed.
- GroundSet used eight A100s for 72h; PointDiT-B training totals 352 H100 GPU-hours; Live-kBench needs at least 30 minutes per patch. These are reported setups, not local measurements.
- VIPE generated 18,160 videos in one experiment. At paper rates of USD 3.20 each, roughly USD 58,112. No current-price verification or paid calls.
- AMS's reported 10–40-second scan excludes model retrieval/loading. Affordable core only; the full 14-configuration matrix was not reproduced.
- TFRBench gold feedback builds benchmark traces and must not be advertised as a leakage-free forecasting agent. Keep mild synthetic experts separate from real routing.
- The v1 header corrected historical audit date 2026-07-10 to **2026-05-29** for 2606.00369.

## Individual decisions

Google coauthors may confer priority without Google first authorship. When official listing is the only affiliation evidence, preserve the unverified author-institution boundary.

### 2601.00372 · LLM-Powered Analysis of IoT User Reviews: Tracking and Ranking Security and Privacy Concerns

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2601.00372v1); v1 date 2026-01-01; author/organization role: North Carolina State University.
- Method: GPT-3.5-Turbo two-stage SFT: CRC classification, explanation, and subtyping; TM topic mapping and dynamic few-shot. This is an IoT review security/privacy study, not a general recommendation, agent, or foundation-model mechanism.
- Experiments/resources: 91,149 unlabeled Amazon reviews, 2,454 human-converted labels, three SFT epochs; Linux with 16GB RAM and RTX 3070M for BERT embeddings. Offline classification and topic statistics.
- Public code: The anonymous repository supplies product information/data; algorithm training code was not verified. [Primary code/project link](https://anonymous.4open.science/r/IoT-Products-SecurityAndPrivacy-5F5D/README.md). Status: `project_or_data_link_only_no_algorithm_code_confirmed`.
- Cost decision: Do not run batch API and SFT on 91K reviews. Scope closure is not a substitute for method review.
- Production evidence: No production A/B or full traffic; offline Amazon reviews are not online experiments.
- Sections actually checked: §3 Methodology, §4 results navigation/summary metrics, authors and date. Source lines L119-L145. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2601.00372.json); SHA-256 `144665c0eee9b8eca2f7554bc52ef4d8a4de6c1a76d08feabc8e7549a8ce0f3e`。

### 2601.19066 · Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2601.19066v1); v1 date 2026-01-27; author/organization role: Google.
- Method: Passerine TDD/TLD/Freeform jointly generate fixes and bug reproduction tests. Tests must fail before and pass after; test-aware selection combines reviewer filtering, normalized groups, and majority vote.
- Experiments/resources: 120 private Google bugs, six languages, five configurations, 20 trajectories per bug, up to 25 steps, Gemini 2.5 Pro. Internal deployment and human review are described, but comparison is offline replay.
- Public code: No public Passerine or private bug implementation found in the reviewed body. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 5×120×20=12,000 trajectories, up to 300,000 steps and private monorepo tests exceed a bounded single-card/Mac run. This is an upper-bound calculation, not a measurement. A small real patch/BRT selector is affordable but not authorized here.
- Production evidence: Passerine is deployed internally; no quantified production A/B or explicit full-traffic adoption for the method was found.
- Sections actually checked: §2.1 Our Agentic APR System, §3 Dynamic Cogeneration, §4.2 configuration, §5 results summary. Source lines L88-L139;L256;L329. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2601.19066.json); SHA-256 `a3556e9374f3ded4cf6da3efccb95d34c58491866202094acc694d6d4df316d5`。

### 2601.21149 · Mobility-Embedded POIs: Learning What a Place Is and How It’s Used from Human Movement

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_private_data`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2601.21149v1); v1 date 2026-01-29; author/organization role: University of Southern California.
- Method: Contrastive visit Transformer and POI prototypes, multiscale Gaussian-anchor transfer with KL, direct anchor supervision and text cosine alignment, then frozen representations with small heads.
- Experiments/resources: Private Veraset mobility: one year in LA and 20 days in Houston. 53.7M parameters, four layers, eight heads, d=512, 20 pretraining epochs and 100 fine-tuning epochs with early stopping, 16GB V100, five map probes.
- Public code: No training repository found in reviewed body/appendix. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: The model fits one card, but paid/private mobility data and SafeGraph, original training and embedding API costs are not available. Bounded component opportunity only. V100 use alone is not cost evidence.
- Production evidence: Five offline map tasks, no A/B or explicit full traffic.
- Sections actually checked: §3.3–3.6, §4.1, Appendix A.1.4–A.3. Source lines L125-L177;L406-L418. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2601.21149.json); SHA-256 `bf0a285cb148b3b6ea24f6da6d5d7f25e595293085374a35faad4c1dea9ee2a4`。

### 2602.02164 · Co-RedTeam: Orchestrated Security Discovery and Exploitation with LLM Agents

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.02164v1); v1 date 2026-02-02; author/organization role: Michigan State University / Google collaboration.
- Method: Docker-isolated multi-agent security discovery with Planner/Validation/Execution/Evaluation and pattern, strategy, and technical memory; uses code and actual execution feedback.
- Experiments/resources: CyBench/BountyBench/CyberGym with multiple models, controls, and iterations; Gemini, GPT-5-mini, o4-mini, Claude 4.5, open 20B/32B. Security benchmarks rather than user A/B.
- Public code: No author Co-RedTeam implementation found; OpenHands is a baseline. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Three benchmarks, multiple models and controls, long traces, isolated Docker, paid APIs/20B–32B, and repeated discovery/exploitation exceed bounded cost by configuration, not local measurement.
- Production evidence: Isolated security evaluation; no production A/B or full traffic.
- Sections actually checked: §3.2–3.4, §4 Experiments, Appendix A.5/C. Source lines L104-L131;L329-L370. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.02164.json); SHA-256 `1fd8770e975ee9a8bcbdfacb2bae88cbd49113399f32f27ec29f091749ef735e`。

### 2602.02690 · Outrunning LLM Cutoffs: A Live Kernel Crash Resolution Benchmark for All,

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.02690v1); v1 date 2026-02-02; author/organization role: Columbia University.
- Method: Live-kBench continually collects time-ordered kernel bugs; kEnv separates agent from compilation/execution, using crash feedback and patch-equivalence judging.
- Experiments/resources: 534 Linux bugs, three scaffolds, Gemini 3 Pro/Flash and Claude Opus 4.5, nine judge votes per patch, at least 30 minutes to compile/test one patch.
- Public code: No named author repository found; public dashboard/benchmark announcement is not verified source code. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: One 30-minute run for 534 bugs implies at least 267 serial hours before models and repeats, extrapolated rather than measured. Kernel VMs/cloud execution cannot be faithfully substituted with Mac or one A100.
- Production evidence: Public offline benchmark, not production A/B.
- Sections actually checked: §3 kEnv navigation, §4 Live-kBench, §5.1, introduction cost. Source lines L45-L59;L140-L190. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.02690.json); SHA-256 `4e68b191ee36a17f566160667907aa2a2afc368109dd61a83100d4823440b1b5`。

### 2602.06276 · Statistical Learning from Attribution Sets

Google’s official list used the short title “Learning from Attribution Sets”; the heading preserves the paper title.

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.06276v1); v1 date 2026-02-06; author/organization role: Google Research.
- Method: Builds unbiased population-loss estimators from anonymous attribution sets and priors for ERM, comparing random assignment and max-prior pseudolabels.
- Experiments/resources: MNIST/CIFAR10/Higgs, MLP/CNN, k=2^0…2^8, ten learning rates × ten repeats, 200 MNIST epochs and 100 otherwise. Preliminary offline simulations.
- Public code: No author implementation repository found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Full grid about (9+9+8)×3×10×10=7,800 runs of 100–200 epochs. The small CPU loss mechanism is affordable but not authorized for implementation here.
- Production evidence: No production ads A/B or full traffic; industry heuristic baselines are not online controls.
- Sections actually checked: §3–4 navigation, §5 Experiments. Source lines L235-L253. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.06276.json); SHA-256 `dde635f3f538fead75f4540ef5ac3c6605c8ce64640f5bfeb333609bec728354`。

### 2602.07266 · ADCanvas: Accessible and Conversational Audio Description Authoring for Blind and Low Vision Creators

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.07266v1); v1 date 2026-02-06; author/organization role: Carnegie Mellon University / Google Research.
- Method: Screen-reader/keyboard WebVTT editor with video QA and collaborative audio description scripts. Accessible interface design and user research, not a standalone comparable agent algorithm.
- Experiments/resources: Formative authoring study with 12 blind or low-vision creators, three video tasks, qualitative observations and usability.
- Public code: No public system implementation verified in methods/user-study sections. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure; an API prototype would not reproduce the user study. No participant recruitment.
- Production evidence: A small user study is not production A/B or full traffic.
- Sections actually checked: §3.2 Design Rationale, §3.3 implementation locations, §4 task/procedure. Source lines L227-L247;L273;L316-L328. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.07266.json); SHA-256 `48461145d250e77c956113131a1275558986abd7a9585b4d06ca2b053fd7f108`。

### 2602.07918 · Causal Armor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.07918v1); v1 date 2026-02-08; author/organization role: Seoul National University / Google collaboration.
- Method: LOO causal ablation at privileged actions compares user versus untrusted spans to trigger selective sanitization. Clears post-injection assistant CoT and regenerates actions.
- Experiments/resources: AgentDojo 1.2.2 four environments/three attack templates and DoomArena TauBench 115 scenarios × five seeds; Vertex AI backbones/sanitizers and eight A100s.
- Public code: No author CausalArmor repo verified; AgentDojo is a benchmark. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Eight A100s and full model/attack/seed grid are too costly. No download/run. A bounded LOO/masking component can use CPU/single-card models but was not approved here.
- Production evidence: Isolated agent security; no A/B or full traffic.
- Sections actually checked: §3–4 mechanism navigation, Algorithm 1, Appendix C/D.1. Source lines L545-L608;L632-L634. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.07918.json); SHA-256 `5eca3db81e91f363b5eb4da5a10247f56796693890f579788561287c00bb17f6`。

### 2602.12481 · Online Advertising with Spatial Interactions

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.12481v1); v1 date 2026-02-12; author/organization role: Google Research.
- Method: Models ad slots as metric points; maps nearest-neighbor externalities to grouped pseudo-disks and uses LP rounding for an 18-approximation and truthfulness, plus a simple logarithmic approximation and 2D PTAS.
- Experiments/resources: Theoretical algorithms/proofs, hardness and appendices. No experimental section or experiment keyword match; not an ad deployment study.
- Public code: No author code link found in reviewed original. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Small geometric/LP CPU instances are affordable without models/data, but not authorized here. Absence of A/B does not invalidate the theory.
- Production evidence: No production A/B/full traffic; does not meet industrial deployment evidence.
- Sections actually checked: §2.1–2.3, simple slot-selection algorithm, section and experiment search. Source lines L178-L246;L308-L354. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.12481.json); SHA-256 `205f87ef58138591d91b3919a3d20e4d9c6d8478ae81ff64fa24efd18b51315c`。

### 2602.16938 · ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.16938v1); v1 date 2026-02-18; author/organization role: Google.
- Method: Collects good/bad recommender interactions and uses PLSA statistics, discriminator HLS, and cross-policy counterfactual checks for prompt/ICL (k=3)/SFT simulators.
- Experiments/resources: 4,146 human plus 3,549 simulated conversations train Gemini 2.5 Flash-Lite discriminator; each simulator generates 300 good and 300 bad. KS/MWU and HLS show realism gaps. A 1990s Turing analogy is not production evidence.
- Public code: No code repository found; announcing data is not releasing code. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Bounded statistics/validation are affordable. Human collection, multiple Gemini SFTs, and thousands of multi-turn rollouts exceed budget; full experiment not reproduced.
- Production evidence: Collected good/bad participant interactions are not production traffic A/B or full rollout.
- Sections actually checked: §4–6, §6.1 discriminator configuration, §6.2 results. Source lines L120-L153;L169-L202. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.16938.json); SHA-256 `9c5a79260f66684ce72cb66467b78de5b39b3b1416de333862dbc41d3853b9c7`。

### 2602.17554 · A Theoretical Framework for Modular Learning of Robust Generative Models

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_implemented`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2602.17554v1); v1 date 2026-02-19; author/organization role: Google Research.
- Method: A normalized robust gate minimizes worst-mixture KL. Stochastic primal-dual training, SIR/rejection sampling, and cached-logit structural distillation give a causal router, not expert averaging.
- Experiments/resources: Synthetic vocab 100, length 10, one layer/two heads/FF 32, embeddings 6/8/16/20, 800 steps for experts/baselines/gates and five repeats; 5K distillation sequences. A CPU core is feasible.
- Public code: No author repository found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: The small Transformer is affordable on Mac/one card, regardless of LLM title; not authorized. Real-data §8.4–8.5 not read paragraph by paragraph; no claim about full affordability.
- Production evidence: Synthetic/offline, no A/B or full traffic.
- Sections actually checked: §7.3 Algorithm 5 and §8.1–8.3. Source lines L827-L915. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2602.17554.json); SHA-256 `eef22aa59cc164eccd4f7baf425753daa5c87bafa48c74103d4a94d33b269d03`。

### 2603.01293 · Theoretical Perspectives on Data Quality and Synergistic Effects in Pre- and Post-Training Reasoning Models

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.01293v1); v1 date 2026-03-01; author/organization role: USC / Google Research.
- Method: Analyzes in-context linear-regression weight prediction, pretraining covariance and SFT/OS data allocation. OS is outcome-supervised regression, not policy-gradient RL.
- Experiments/resources: LSA d=100, 130 epochs; GPT-2-style 9.5M, 12 layers/eight heads/d=256, batch 64, 100 SFT and 12K OS steps, ten repeats, synthetic covariance shift.
- Public code: No author code found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: LSA is CPU-affordable. The complete GPT-2 × B/n/k grid × ten repeats × 12K OS steps likely exceeds short budget. No run or LSA authorization.
- Production evidence: Synthetic theory validation, no A/B or full traffic.
- Sections actually checked: §1 tasks/OS scope, §8 Experiments. Source lines L59-L61;L275-L317. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.01293.json); SHA-256 `b8065a6fd16e805d23e3de4352dc184ad3b6ba1b031fc892f4494946a33bc89c`。

### 2603.06981 · Diffusion Controller: Framework, Algorithms and Parameterization

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.06981v1); v1 date 2026-03-07; author/organization role: CMU / Google Research.
- Method: DiffCon treats reverse diffusion as LS-MDP control with f-divergence-regularized PG/PPO and reward-weighted regression. A lightweight side control alters scores using intermediate outputs from a frozen backbone.
- Experiments/resources: SD 1.4, five parameterizations × SFT/RWL/PPO; side 12M and LoRA 17M; 1,000/2,000/2,400 steps. HPS/CLIP/PickScore and human evaluation.
- Public code: No author repository verified in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 15 training arms, SD 1.4, reward models, image evaluation, and thousands of PPO steps imply hours beyond one A100/A30 short budget. Not measured locally.
- Production evidence: Offline image preferences, not A/B.
- Sections actually checked: §1 definitions, §5.1–5.2 configurations and Table 1. Source lines L77-L81;L319-L354. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.06981.json); SHA-256 `225d3c64ba529e58ca3ebbd26192ef238252266dcfd8ad17198f92ceb70268e9`。

### 2603.10465 · MoXaRt: Audio-Visual Object-Guided Sound Interaction for XR

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.10465v1); v1 date 2026-03-11; author/organization role: Google.
- Method: MoXaRt XR audio uses AudioScopeV2 coarse separation, face/instrument anchors, branch refinement, and teacher–student distillation; chiefly an XR acoustic interaction system.
- Experiments/resources: Thirty one-minute mixed recordings and 22-person study; visual 3.2M/33M, coarse audio 6M, speech 9M/music 7M; about two seconds interactive latency.
- Public code: No complete author system or distillation code verified. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure. No YFCC100M pretraining, specialized teacher distillation, or user recruitment.
- Production evidence: Technical and participant study, not production A/B.
- Sections actually checked: §3.2.1–3.2.4, §5/6 technical and user-study summaries. Source lines L187-L228;L93-L95. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.10465.json); SHA-256 `8101409b163ea7e86c321094f2ab2d0606f66f42ebfb15ba6652bed06f1b8772`。

### 2603.14609 · GroundSet: A Cadastral-Grounded Dataset for Spatial Understanding with Vector Data

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.14609v1); v1 date 2026-03-15; author/organization role: official Google source; see primary source for author affiliation.
- Method: Aligns cadastral vectors to aerial images for automatic spatial tasks. Vanilla VLM LoRA is a data-contribution baseline, not a new spatial network.
- Experiments/resources: 85,864 km² across 20 districts, 20cm imagery; multiple VLMs across captions/VQA/classification/detection/REC/segmentation. One LoRA epoch took ~72h on eight A100s.
- Public code: No author implementation found in reviewed sources. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Eight A100 × 72h = 576 GPU-hours for main training alone, beyond one A100/A30; no data/weight downloads.
- Production evidence: Offline remote sensing benchmark, not A/B.
- Sections actually checked: §3 data construction, §4.2–4.3. Source lines L93;L221-L238. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.14609.json); SHA-256 `0028b9f91234a8ecab28b888a0e14cd2afcd0793e3d6b2057f168a6e182022b7`。

### 2603.14769 · POLCA: Stochastic Generative Optimization with LLM

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.14769v1); v1 date 2026-03-16; author/organization role: University of Wisconsin-Madison.
- Method: POLCA tracks evaluation history in a priority queue, preserves diversity with embedding epsilon-nets, and summarizes local history with an LLM. Noise adjusts exploration/exploitation.
- Experiments/resources: tau-bench/HotpotQA/VeriBench/KernelBench. VeriBench 41 problems, up to 50 compiler calls each × three runs × controls. KernelBench 16 tasks, Claude 3.7 and Gemini embeddings.
- Public code: The paper explicitly links public rlx-lab/POLCA. No download or execution verified runtime requirements. [Primary code/project link](https://github.com/rlx-lab/POLCA). Status: `released_primary_repository_reachable`.
- Cost decision: Full multi-benchmark/control × three/six seeds × 50 iterations with paid APIs is too costly. Bounded epsilon-net/queue is affordable but not authorized here.
- Production evidence: Offline optimization, no A/B or full traffic.
- Sections actually checked: §1 mechanism, Appendix D VeriBench/KernelBench budgets/configuration. Source lines L99-L106;L725-L745;L769-L775. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.14769.json); SHA-256 `936c7c6cc3242b8bf6b04e8aaf2402390e960601bed9d535049e424f3017e4d9`。

### 2603.24591 · Vibe Coding XR: Accelerating AI + XR Prototyping with XR Blocks and Gemini

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.24591v1); v1 date 2026-03-25; author/organization role: Google XR Labs.
- Method: XR Blocks wraps WebXR perception and interaction in semantic primitives and generates runnable XR scripts with Gemini prompts/templates. It is a development workflow.
- Experiments/resources: VCXR60 technical pilot on desktop simulation and Android XR headsets, not a controlled general learning/optimization benchmark.
- Public code: The authors link the official public google/xrblocks repository. [Primary code/project link](https://github.com/google/xrblocks). Status: `released_primary_repository_reachable`.
- Cost decision: Scope closure; an API demo does not justify a new XR implementation. No model training required for review.
- Production evidence: Pilot, not A/B or full traffic.
- Sections actually checked: §1/§3 framework/workflow, §4 preliminary evaluation location. Source lines L55-L85. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.24591.json); SHA-256 `b8e9b1c9aea42b8ee8efd861663ba85b2e1c96caa851943087fbc31d4f73fc40`。

### 2603.28896 · Fisheye3R: Adapting Unified 3D Feed-Forward Foundation Models to Fisheye Lenses

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.28896v1); v1 date 2026-03-30; author/organization role: Yale University / Google XR.
- Method: Freezes VGGT/pi3/MapAnything, adapts with calibration tokens and a camera-type linear classifier controlling masks to retain perspective compatibility; SL/SSL.
- Experiments/resources: ScanNet++/ADT/KITTI360 geometry; K=8 per layer except first 12, AdamW 40K steps, checkpointing, four 48GiB RTX A6000s.
- Public code: No author repository found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Three large backbones × adaptations × 40K steps, four 48GiB GPUs and multiple datasets are too costly. A minute-long CPU camera classifier cannot reproduce adaptation.
- Production evidence: Offline 3D, no A/B.
- Sections actually checked: §3 masked calibration, train/evaluation/hardware settings. Source lines L142-L149;L332-L347. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.28896.json); SHA-256 `c8ba18b1d695e0193276c207d941d884308b370b35bd65f2cae18d53038daabe`。

### 2603.29470 · AI-Simulated Expert Panels for Socio-Technical Scenarios and Decision Guidance

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.29470v1); v1 date 2026-03-31; author/organization role: affiliations not visible in HTML; not independently confirmed.
- Method: One Gemini simulates energy experts using stochastic CIB cross-impact paths, MCDA stakeholder selection, and quantitative scenarios. German energy transition proof of concept, not agent capability.
- Experiments/resources: Five simulated experts, 15×3 descriptor states and over 250K discussion words. CIB consistency does not ensure plausible narratives; no actual expert capability comparator.
- Public code: Accompanying resources/transcripts mentioned, no algorithm release verified. HTML did not show Google affiliation; preserve official listing provenance without claiming Google first author. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure. No need to regenerate 250K words; cost does not resolve unverified affiliation.
- Production evidence: Policy simulation, not A/B.
- Sections actually checked: §2 Methods, §3.1–3.3 Results. Source lines L69-L77;L138-L170. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.29470.json); SHA-256 `a0791bb14f867ae57b07c93c835bf67dd3cc3720924dd8c9f9dbbad749fc9e4f`。

### 2603.29791 · Reasoning-Driven Synthetic Data Generation and Evaluation

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2603.29791v1); v1 date 2026-03-31; author/organization role: EPFL / Google internship.
- Method: Simula builds seedless taxonomies, locally meta-prompts and complexifies, samples hierarchy nodes globally, and uses double critics and calibrated complexity/Elo. Requires actual M3 generation and critique.
- Experiments/resources: Gemini 2.5 Flash, multilingual CTI/law/GSM8K/GlobalMMLU, 512K unique points per dataset and five versions. 13-gram/Jaccard decontamination and BS=N5 scoring.
- Public code: No author implementation found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 512K per task × multiple variants, critics, complexity and downstream training risk millions of paid multimodal API calls. Bounded taxonomy/critic core affordable but not authorized.
- Production evidence: Offline synthesis/downstream evaluation, no A/B.
- Sections actually checked: §3 setup, §3.2 data scale, Appendix E cost examples. Source lines L133-L160;L674-L685. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2603.29791.json); SHA-256 `31797910eae4658e36df7db22237fecb2dc4b8ee39d5f0bb22fb719906ef0f8c`。

### 2604.05364 · TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2604.05364v1); v1 date 2026-04-07; author/organization role: University of Kentucky / Google collaboration.
- Method: Reason/search/forecast/verify/summary agents build grounded traces, up to K=3 loops, selected by MASE and consistency. Gold feedback builds a benchmark, not a leakage-free forecasting agent.
- Experiments/resources: Ten datasets in five domains with Gemini/Claude forecasts and LLM judges. Candidate verification sees future truth; forecasting itself does not. External event retrieval includes the future horizon.
- Public code: The author project page is public; independent algorithm source was not verified. [Primary code/project link](https://tfrbench.github.io/). Status: `project_or_data_link_only_no_algorithm_code_confirmed`.
- Cost decision: The full dataset/model/candidate/three-loop retrieval and judge API grid is costly. A bounded protocol and scorer are affordable but not implemented; isolate labels.
- Production evidence: Offline forecasting benchmark, not A/B.
- Sections actually checked: §3 Algorithm 1 and six steps, §4 result excerpts. Source lines L165-L224;L616-L672. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2604.05364.json); SHA-256 `573ddf1fa3c2c4aa17ea4776f708c999a3ac96578e5c952f4b709caa48db9e57`。

### 2604.09803 · MAGE: Modality-Agnostic Music Generation and Editing

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2604.09803v1); v1 date 2026-04-10; author/organization role: Google (internship).
- Method: MAGE uses Controlled Multimodal FluxFormer latent flow matching, audio-visual nexus alignment, multiplicative cross-gates, and dynamic modality masking for generation and mixture editing.
- Experiments/resources: MUSIC; AdamW 1e-4, 1K epochs with data repeated five times each, 70% mixture/20% zero-mixture/10% CFG fallback; Euler with two evaluations and MixWavCodec.
- Public code: No author repository found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 1,000 epochs × five repeats plus audio-video flow, codec resources, and evaluations imply hours/days. Too costly, not measured or downloaded.
- Production evidence: Offline music, no A/B.
- Sections actually checked: Appendix A model/train/inference and evaluation locations. Source lines L315-L343. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2604.09803.json); SHA-256 `dbf1e594ba8530befc001b170937bb1667df54a0c1e1ddda516dfbcaeccebfd7`。

### 2604.20329 · Image Generators are Generalist Vision Learners

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2604.20329v1); v1 date 2026-04-22; author/organization role: Google / Google DeepMind.
- Method: Vision Banana instruction-tunes NanoBananaPro with reversible/parseable RGB encodings of segmentation, depth and normals, retaining original generation data in the mixture.
- Experiments/resources: Multiple 2D/3D and editing benchmarks; depth training only synthetic. Original NanoBananaPro data and trainable checkpoint are not public.
- Public code: Project page available; trainable author code, NBP weights, and original mixture not verified. [Primary code/project link](https://vision-banana.github.io/). Status: `project_or_data_link_only_no_algorithm_code_confirmed`.
- Cost decision: Closed NBP training and original corpus are unavailable on one card. RGB encoding helpers do not reproduce generalist training.
- Production evidence: Offline zero-shot vision/generation, no A/B.
- Sections actually checked: §2 Method, Table 1, §3.2 depth encoding/training. Source lines L61-L85;L219-L244. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2604.20329.json); SHA-256 `832a2b2e678fbed6c8a46ed3980d80d94c0d1976f3b8ffb46f152b84c7f0084d`。

### 2604.23099 · ProEval: Proactive Failure Discovery and Efficient Performance Estimation for Generative AI Evaluation

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2604.23099v1); v1 date 2026-04-25; author/organization role: Google DeepMind.
- Method: ProEval pretrains a GP surrogate, uses Bayesian quadrature for overall performance and superlevel-set failure sampling, transfers TPF/RPF/SF, and applies topic UCB1 plus LLM failure-pattern transfer.
- Experiments/resources: 16 LLMs/VLMs across reasoning, knowledge, safety, text and image; 100 discovery iterations. GP uses historical external scores, not gold in the evaluated agent.
- Public code: The authors explicitly release google-deepmind/proeval. [Primary code/project link](https://github.com/google-deepmind/proeval). Status: `released_primary_repository_reachable`.
- Cost decision: CPU GP/BQ on existing scores is affordable. Full 16-model benchmarks and LLM query synthesis are costly. Not rerun or approved for implementation.
- Production evidence: Offline evaluation; no A/B/full traffic.
- Sections actually checked: §2 Algorithm 2, §3.1 data/model/features, Table 5. Source lines L274-L336;L452-L462. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2604.23099.json); SHA-256 `5704d72b8d22dedb0b0411bc1ed476c103825a93ca54939f2ccec8e8e3907611`。

### 2604.27723 · Optimized Deferral for Imbalanced Settings

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_implemented`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2604.27723v1); v1 date 2026-04-30; author/organization role: Google Research.
- Method: mild casts imbalanced expert deferral as input–expert cost-sensitive classification with margin surrogate and consistency bounds. Real expert outputs train the router; labels are forbidden at inference.
- Experiments/resources: CIFAR synthetic expert coverage such as 7/2/1; real routing with Qwen2.5 0.5B/1.5B and others. Synthetic oracles and actual models remain separate.
- Public code: No author repository found. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Bounded CPU loss/router checks are affordable without downloading LMs, but synthetic gold experts are diagnostics, not routing ability. Not authorized.
- Production evidence: Offline classification/routing; no A/B/full traffic.
- Sections actually checked: §5.3 Deferral loss, Appendix C.1/C.2. Source lines L306-L326;L536-L572. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2604.27723.json); SHA-256 `69f6576ef83d97e8e782bee058a70029f9baa72f9c93b9d18da64a7b1f8c7a0c`。

### 2605.26340 · Scientist-One: Verifiable Autonomous Research via Chain-of-Evidence

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2605.26340v1); v1 date 2026-05-25; author/organization role: Google Cloud AI Research.
- Method: Scientist-One chain of evidence links claims to code, evaluators, and bibliography. I1 recalculates scores, I2 checks specs, I3 queries citations, I4 checks method/code alignment and CPR. Automated research retains provenance.
- Experiments/resources: Five ADRS tasks × five systems × three runs, Gemini 3.1 Pro, up to 20 iterations and two-hour code windows, five evaluator reruns and majority judges.
- Public code: No separate author release verified. Open baselines are not Scientist-One source. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 5×5×3=75 full research runs capped at two hours each and potentially three retries, plus multi-round work over pools of 500 papers/100 notes. Bounded provenance/audit is affordable but not authorized.
- Production evidence: Offline ADRS, not A/B.
- Sections actually checked: §5 Integrity Audit, §6 Experiments, paper-investigation appendix. Source lines L200-L246;L463-L471. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2605.26340.json); SHA-256 `5d965c86619f27647d82ee82b0170bb417e9b1443a13fe40eba517987abb9415`。

### 2605.29729 · Realistic honeypot evaluations for scheming propensity

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_resource_unavailable`. Separate full-experiment status: `not_reproduced_private_environment`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2605.29729v1); v1 date 2026-05-28; author/organization role: Google DeepMind.
- Method: Uses genuine internal alignment-code honeypots for sabotage opportunities in review and agentic coding, varying agency and hidden goals and inspecting thought/action triggers. Evaluation, not training.
- Experiments/resources: Review: 12 honeypots + one baseline over ten commits; coding: 11 honeypots + two baselines with Antigravity on copies of Google code. Multiple Gemini models/prompts.
- Public code: Internal alignment code is not public; no runnable public environment/implementation found. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Internal code unavailable. 26 settings across models/prompts, long coding traces, and human/CoT review have unresolved material cost. No costly external approximation.
- Production evidence: Deployment-like, not in-deployment A/B. No trigger does not establish safety.
- Sections actually checked: §3 Methods, §3.1 prompting, introductory deployment boundary. Source lines L99-L140;L48-L58. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2605.29729.json); SHA-256 `845d4f3e64430e54cbfda1c8adde5b03e2a179a013af3497530fcba52aad7505`。

### 2605.30174 · LiveSVG: Zero-Shot SVG Animation via Video Generation

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2605.30174v1); v1 date 2026-05-28; author/organization role: Google / Hebrew University.
- Method: LiveSVG generates video then fits original SVG with differentiable rasterization, group homographies and Bézier offsets, disambiguated by sphere-packing recoloring without a skeleton prior.
- Experiments/resources: AniClipart/ChallengeSVG; Veo 3.1/Wan/LTX, 10–20 videos per SVG, two-stage Gemini 3.1 Pro reranking, 5.2 GPU minutes per successful fit, and AMT preference study.
- Public code: Project page public; author implementation not verified. [Primary code/project link](https://levymsn.github.io/LiveSVG). Status: `project_or_data_link_only_no_algorithm_code_confirmed`.
- Cost decision: Full benchmarks × 10–20 videos each, reranking, baselines, fits, and study are costly. 5.2 minutes excludes generation and conditions on successful fits.
- Production evidence: AMT pairwise A/B is offline human preference, not production traffic.
- Sections actually checked: §3 mechanism, Appendix F implementation, runtime/user study. Source lines L87-L92;L404;L440-L475. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2605.30174.json); SHA-256 `f819c31e580dbb974239bb2e82076d89ba07c4829462226656c91b573821c351`。

### 2605.30322 · Gram: Assessing sabotage propensities via automated alignment auditing

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_resource_unavailable`. Separate full-experiment status: `not_reproduced_private_evaluation`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2605.30322v1); v1 date 2026-05-28; author/organization role: Google DeepMind.
- Method: Gram constrains the Petri auditor to reduce leading prompts and uses 17 sabotage seeds. An investigator creates static environments from traces and runs interventions to separate overeagerness and roleplay.
- Experiments/resources: Gemini 2.5 Pro/3.0 Pro/3.1 Pro; only four of 17 seeds public and 13 private holdout. LLM judges and human checks; 2–3% does not generalize to deployment.
- Public code: No complete implementation found; 13/17 seeds explicitly private. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Dynamic auditor/targets, multiple prompts/trajectories and human review plus unavailable seeds. Unresolved cost/resources; no expensive probe.
- Production evidence: Simulated predeployment audit, not real traffic A/B.
- Sections actually checked: §2.1–2.2, §1 evaluation boundary. Source lines L74-L139. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2605.30322.json); SHA-256 `c3cd1ca60b5cd69dd32699f0e65337bc17df1b3c8a37d6c558e57914378156f0`。

### 2606.00131 · AI-PROPELLER: Warehouse-Scale Inter-Procedural Code Layout Optimization with AlphaEvolve

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2606.00131v1); v1 date 2026-05-28; author/organization role: Google.
- Method: AI-Propeller Magellan uses AlphaEvolve to edit Propeller interprocedural layout and Vizier to tune compiler flags. Each candidate is actually built and run with hardware counters.
- Experiments/resources: Clang 100 modules, 12 AlphaEvolve iterations, 1,200 Vizier trials, 2.7 days, ten executions per binary; controlled 48-core/96GB Xeon. Clang/LevelDB/Redis/Search; Search trained separately.
- Public code: No full AI-Propeller/Magellan implementation found; Propeller/LLVM are upstream, not the new policy pipeline. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: 2.7 days, 1,200 trials × ten executions, Clang rebuilds, and private Search binaries. One GPU cannot substitute for controlled CPU and private workloads.
- Production evidence: §5.4 reports production Search +0.23% versus deployed Ext-TSP. No group/traffic scale or explicit full rollout, so strict A/B/full-traffic gate remains unconfirmed.
- Sections actually checked: §4 method, §5 training/evaluation, §5.4 Warehouse Scale. Source lines L88-L115;L124-L156. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2606.00131.json); SHA-256 `08a3e83c916e8107808c35f0df816ffa145cf299a7b50003e30c40a6529499f6`。

### 2606.00369 · Quantifying the Salience of Geo-Cultural Values for Pluralistic Safety Alignment

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2606.00369v1); v1 date 2026-05-29; author/organization role: Columbia University / Google DeepMind internship.
- Method: Meta-analysis of safety annotations with IW cultural zones and demographic multilevel logistic/linear mixed models. Evaluates LLM rater substitutes and triage, not new alignment training or agent algorithms.
- Experiments/resources: Eight safety datasets overview, six significance analyses, item/rater random effects and culture/demographic fixed effects. LLMs did not reliably replace diverse annotators.
- Public code: No author repository verified in reviewed methods/results. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure; statistics are affordable and cost is not the reason. No new participant collection/annotation.
- Production evidence: Annotation and safety meta-analysis, no A/B.
- Sections actually checked: §4.1 culture operationalization, §4.2 mixed models, abstract scope. Source lines L156-L181;L73-L88. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2606.00369.json); SHA-256 `e4c94a79c808f4f0d536874bb36eac7ce830ebe9ba5d68508b1625a89ff4010d`。

### 2607.02515 · PointDiT: Pixel-Space Diffusion for Monocular Geometry Estimation

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2607.02515v1); v1 date 2026-07-02; author/organization role: ETH Zurich / Google.
- Method: PointDiT predicts clean point maps from raw 3D patches conditioned on four frozen DINOv3 feature levels; plain ViT, velocity loss, spherical sky mapping, rectified t0 sampling.
- Experiments/resources: B 223M/L 771M/H 1.807B; 30 pretraining epochs on 16/16/64 H100s ×12/21/22h, then 64/64/128 H100s ×2.5/7/5.5h fine-tuning.
- Public code: No author code verified; baseline links are not releases. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Smallest B: 192 pretraining +160 fine-tuning =352 H100 GPU-hours; L 784/H 2,112. GPU counts × paper wall time, not local measurements. Beyond one A100/A30.
- Production evidence: Offline geometry, no A/B.
- Sections actually checked: §3.2–3.3, appendix Table 6 training costs. Source lines L137-L163;L455-L460. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2607.02515.json); SHA-256 `c9fd2f768b7e39d7ddef8e1bf57016975cb23e06b042a3c7ca28baa9922efe0f`。

### 2607.13614 · VIP-MINGLE: A Corpus for Videoconference and In-Person Multimodal Interaction in Group Language Engagement

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2607.13614v1); v1 date 2026-07-15; author/organization role: New York University / Google collaboration.
- Method: VIP-MINGLE pairs participants across in-person and video meetings and analyzes speech timing, linguistic complexity, faces, and interaction labels. Corpus, not a new general model/agent.
- Experiments/resources: 59 hours, 32 groups, 105 participants, 7,077 ten-second clips and 192 annotators. Mixed effects/Wilcoxon for domain shift.
- Public code: No complete public processing pipeline verified. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure. Do not recollect 59 hours or claim CPU statistics reproduce the corpus.
- Production evidence: Paired participant study, not production A/B.
- Sections actually checked: §2 data design, §3.1–3.3, §4 annotations. Source lines L44-L62;L94-L113. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2607.13614.json); SHA-256 `37be407ed96b5b57907daf687209446b46da9094132ece85df830a4f3b285206`。

### 2607.25537 · Visual prompt engineering for video models

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2607.25537v1); v1 date 2026-07-28; author/organization role: Google DeepMind.
- Method: VIPE ideates visual rewrites, uses an editor to modify the task image, optionally filters semantic drift, and compares freeform open-loop or ACE edits with video test-time scaling.
- Experiments/resources: Six tasks, 20 variants and best five per edit; one experiment generated 18,160 Veo 3.1 720p eight-second videos. Paper API rates were USD 3.20/video and about USD 0.40/VIPE.
- Public code: Project page public; no author execution code verified. [Primary code/project link](https://visual-prompt-engineering.github.io/). Status: `project_or_data_link_only_no_algorithm_code_confirmed`.
- Cost decision: 18,160×USD 3.20=USD 58,112 at paper rates, before editing/filtering/other experiments. Too costly. No current price check or paid call.
- Production evidence: Offline video reasoning, not A/B.
- Sections actually checked: §4 automated VIPE, Appendix B budgets, §5 test-time scaling. Source lines L151-L162;L177-L180;L335-L337. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2607.25537.json); SHA-256 `22c92799af3dea509393aec62c87ab209b72c7513a039cef8a115f52aff8d6e0`。

### 2608.05578 · Detecting Safety Training Modification in Language Models via Activation Analysis

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2608.05578v1); v1 date 2026-08-06; author/organization role: Google Cloud.
- Method: AMS uses 16 contrastive pairs per safety concept across three concepts and scans 40–80% model depth for maximum separation/direction/sigma. Tier 1 thresholds and Tier 2 baseline cosine/drift checks.
- Experiments/resources: 14 configurations/four families; LOO threshold 71% (10/14), 20 JailbreakBench prompts per model. 40GB A100 scan 10–40s excludes loading; wide bootstrap intervals sometimes cross PASS threshold.
- Public code: Authors release Apache 2 GoogleCloudPlatform/activation-model-scanner and a Zenodo archive. [Primary code/project link](https://github.com/GoogleCloudPlatform/activation-model-scanner). Status: `released_primary_repository_reachable`.
- Cost decision: A cached 3B/7B scan is affordable with no training; full 14-configuration download is not. Core candidate only; 71% is not validated production safety.
- Production evidence: Offline tamper detection, no A/B.
- Sections actually checked: §IV-F algorithm, resources, data availability/abstract statistics. Source lines L242-L277;L583-L602;L631-L646. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2608.05578.json); SHA-256 `724cd5f758a0b87229282126e12cddcc3f3e0116203ff551a5fbf874bf06fd53`。

### 2608.11367 · Gaze Target Estimation Anywhere with Concepts

- Disposition: Deferred: full experiment not reproduced; `not_reproduced_high_cost`. Separate full-experiment status: `not_reproduced_high_cost`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2608.11367v1); v1 date 2026-08-11; author/organization role: University of Illinois Urbana-Champaign / Google.
- Method: PGE jointly localizes prompted subjects and gaze with frozen image/text encoders and a detector Transformer predicting localization, in-frame status, and heatmap. 120K Gaze-Co uses MLLM concepts and human verification.
- Experiments/resources: 119,525 training samples, three public tests and private clinical OOD; 25+5 epochs, batch 128, four H100s. L40S inference and DigiLens ARGO glasses.
- Public code: Authors explicitly release IrohXu/GazeAnywhere. [Primary code/project link](https://github.com/IrohXu/GazeAnywhere). Status: `released_primary_repository_reachable`.
- Cost decision: Four H100s ×30 epochs, multi-backbone/baseline comparisons and 120K data creation exceed bounded A100/A30 budget. Private clinical results cannot be substituted.
- Production evidence: AR field demo and clinical OOD are not A/B or full traffic.
- Sections actually checked: §5.1 implementation, appendix data/model details. Source lines L242-L246;L427-L473. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2608.11367.json); SHA-256 `4ca88f4973bfbd30b7b993cc917566f0a0e815d2f4bce90e53e0fffa25b32375`。

### 2609.01588 · Designing Proactive Thought Partners for Writing

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2609.01588v1); v1 date 2026-09-01; author/organization role: Google DeepMind collaboration.
- Method: Configurable proactive writing partners vary role and timing using NextJS/BlockNote and Gemini decision engine. A technology-probe design space.
- Experiments/resources: 16 participants over one week with diaries/interviews. Flash-Lite selects partner in <1s, Flash suggestions about 8s. Authors do not claim product efficacy.
- Public code: No complete probe implementation found; appendix provides prompts. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Scope closure; no participant rerun or cheap API capability substitute.
- Production evidence: Exploratory one-week deployment, not production A/B or full traffic.
- Sections actually checked: §3 design goals, §4.5 implementation, §5 user study. Source lines L114-L119;L189-L207. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2609.01588.json); SHA-256 `e3aa3647a99f4bc82cf95f45f189343c5fa662729ff994dc09c61ee67f770757`。

### 2609.01834 · Architecting Conversational Data Systems for Stateless LLM APIs

- Disposition: Scope closure: not an algorithm reproduction; `out_of_scope`. Separate full-experiment status: `not_applicable_scope`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2609.01834v1); v1 date 2026-09-01; author/organization role: official Google listing; paper affiliations not independently verified.
- Method: Hydration Proxy is a three-layer pattern: UI, secure gateway, relational ledger/object storage, with stable-prefix and full-history hydration.
- Experiments/resources: 153 lines, architecture §2, cache §3, benefits §4, conclusion/references. No Evaluation search match, controlled quantitative study, or distinct algorithm.
- Public code: No author implementation found in reviewed text. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: Conceptual architecture excluded on scope, not cost.
- Production evidence: 'Production-grade' describes requirements, not quantitative traffic evidence.
- Sections actually checked: §2 architecture, §3 cache-aware context, conclusion and section/Evaluation search. Source lines L53-L124;L127-L138. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2609.01834.json); SHA-256 `2e0a42d1801fd8d1e21c610ca4cdfc8c6e8383cf90d5b1d85d5ae085a4d9de2a`。

### 2609.12464 · Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration

- Disposition: Accepted as a core candidate; not implemented; `accepted_core_not_implemented_this_run`. Separate full-experiment status: `not_implemented`; implementation: `not_implemented`.
- Primary source: [arXiv v1](https://arxiv.org/html/2609.12464v1); v1 date 2026-09-11; author/organization role: official Google listing; paper affiliations not independently verified.
- Method: HCRG maps tree-sitter ASTs to a graph, caches architecture skeletons, migrates topologically and retrieves three hops. Vector control uses 800-character chunks/150 overlap/top five; seven AST+pyflakes structural metrics.
- Experiments/resources: One spring-petclinic Java→Python repository, Gemini 2.5 Pro at T=0, Spanner/Vertex one-hour cache. DRQ 34.8→65.9%, PCC 26.7→45.5%, but cyclomatic agreement fell. No multi-seed/repository generalization.
- Public code: Linked input benchmark is not author pipeline; HCRG release not verified. Status: `not_found_in_reviewed_primary_sources`.
- Cost decision: A small public-repo AST/topology and metrics core is affordable. Equivalent local graph can replace paid cloud, but actual LM migration is required. No authorization or measured total cost.
- Production evidence: Offline migration, not enterprise production A/B or full traffic.
- Sections actually checked: §4.2 settings, §5.2 metrics, §6 results. Source lines L128-L175;L212-L225. [Public summary receipt](../../../research-audits/google-meta-closeout-20261021/evidence/google39/2609.12464.json); SHA-256 `1aaf750fa1321128cc804923bf9021b1da88aa8789c97f97c365279ec1151ed6`。

## Integration boundaries

The parent batch may write the 39 rows to the ledger but must preserve separate `accepted/not_implemented/automatic_implementation_queue=false` and full-experiment decisions. Acceptance is a concrete component opportunity, not implementation authorization, automatic industrial A/B eligibility, delivered code, or GPU verification.

Missing author code means only “not found in the primary sources checked,” not an author confirmation of non-release. Preserve source files, failed searches, cost extrapolations, and negative boundaries.
