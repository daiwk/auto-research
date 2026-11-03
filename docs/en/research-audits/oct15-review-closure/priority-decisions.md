# Individual P0/P1 review decisions

<!-- source-sha256: 1774cbd278482f3d0b4b6887a35f450a5b3f3dde1c43ba228b1115b664178896 -->

[简体中文](../../../research-audits/oct15-review-closure/priority-decisions.md)

This page records review decisions, not implementation. Explicitly declining an unaffordable full experiment closes its review; it is not a pending run.
The domain receipts referenced by the [complete register](../../../research-audits/oct15-review-closure/paper-register.json) preserve reading methods, source locations, fingerprints, and cost evidence.
Dates are first releases. Unknown first releases are explicit, never inferred from catalog dates.

## Affordable review candidates: 14 (not implemented)

- [When Does Momentum Help in Reinforcement Learning with Verifiable Rewards?](https://arxiv.org/html/2610.20413v1) · 2026-10-14 · P1

    Accept only the original ten-arm bandit's bias-corrected EMA, safe η/(1−β), and analytical checks with CPU numerics. Exclude 4B/32B RLVR and the full 50,000-replicate campaign; no LLM improvement claim. Candidate only: not implemented or run, and not queued for execution or Evolve.

- [SpectrumQuant: Spectrum Alignment for LLM Quantization](https://arxiv.org/html/2610.20303v1) · 2026-10-14 · P1

    SpectrumQuant builds a closed-form alignment-plus-mixing orthogonal rotation from calibration activation covariance. The paper's 7B calibration took about 0.26 GPU-hours and 4.51 GiB; retain the 7B path with 128 real examples, not 70B or a full multi-model downstream sweep. Candidate only; not implemented, run, or queued.

- [Which Knowledge Should LLMs Trust? Uncovering a Generalizable Steering Direction Across Knowledge Conflicts](https://arxiv.org/html/2610.20067v1) · 2026-10-14 · P1

    The knowledge-conflict direction is a linear intervention in residual space, using 7B–9B inference on one A100. Accept real-model direction extraction on independent development pairs and isolated test. Accuracy conditional on clean correctness is not unconditional capability; no answers in inference.

- [One Monitor Does Not Fit All: Formalism-Agnostic Runtime Verification for Agentic AI](https://arxiv.org/html/2610.19818v1) · 2026-10-14 · P1

    AgenticRV's canonical events, monitor-specific projection, unified verdicts, and pre-effect blocking are executable on Mac with Python and controlled workflows. Accept only the mechanism; instant-return monitor microbenchmarks are not semantic monitoring or agent capability.

- [Delta Tokenizer: Reference-Identical Tokenization of Session Deltas and Segment-Parallelism for Long Prompts on Multicore CPUs](https://arxiv.org/html/2610.19801v1) · 2026-10-14 · P1

    Delta Tokenizer needs provably safe incremental seams under tokenizer rules, exact segmentation, and chunk scheduling, not token concatenation. Verify with real tokenizer/text on Mac CPU. No 41.8B-document or multi-server rerun and no TTFT measurement claim.

- [Measuring and Reducing Unusable Replies of LLM Agents](https://arxiv.org/html/2610.19659v1) · 2026-10-14 · P1

    Reply usability is bounded by what a reader actually saw. One rewrite or explicit reply instruction needs no training. Accept reader checks and real rewriting on a few replies, not gold substitutes. The paper's 480 replies across eight models are not local results.

- [Beyond Retrieval: Evidence Access and Event Aggregation in Agent Memory](https://arxiv.org/html/2610.19474v1) · 2026-10-14 · P1

    TallyMem keeps raw traces, generates event specifications, and executes aggregates rather than substituting gold events. Accept raw logs→ledger→real compilation/execution. \$1.05 covers only the paper's primary arm, not all AMA/readers. AMA includes development traces; formal comparisons should use 25 development and 99 isolated repositories.

- [When Is Smaller Greener? Right-Sizing Language Models for Agentic AI](https://arxiv.org/html/2610.19345v1) · 2026-10-14 · P1

    The contribution measures energy, money, and time per success and Pareto-filters choices. Accept CPU calculations and crossover lengths using public parameters. The 15-model GPU pilot was not reproduced, and synthetic reliability is not agent capability.

- [Truthful and Expected-Payment-Optimal Model Routing in Graph-Based Agentic Workflows](https://arxiv.org/html/2610.19316v1) · 2026-10-13 · P1

    STAR's allocation, workload monotonicity, and integral payments can run on small synthetic graphs with an exact solver, without LLM calls. Accept the auction/routing mechanism, not synthetic costs or incentive guarantees as agent gains.

- [Online Tokenization with Optimal Delay in Linear Time](https://arxiv.org/html/2610.19139v1) · 2026-10-13 · P1

    Online tokenization formalizes stable output prefixes and delay across special tokens, pretokenization, and BPE, with a lower-delay joint algorithm and impossibility boundaries. Public Morgan Stanley code supports exact CPU token-ID/stream equivalence tests. Candidate only; no implementation or throughput campaign this round.

- [Plant Memory: Technical Language Processing and a Verified Maintenance Ontology for Agent-Accessible Failure Knowledge from SAP PM Work Orders](https://arxiv.org/html/2610.19131v1) · 2026-10-13 · P1

    Plant Memory's rule-first TLP, evidence/review-aware fact graph, and offline SQLite are affordable; a second LLM reader is optional. Accept rules and provenance only. Results on 400 synthetic work orders are not factory deployment, general agent ability, or Evolve gains.

- [BLADE: Auditing Information Use for Failure Attribution in LLM Multi-Agent Systems](https://arxiv.org/html/2610.18780v1) · 2026-10-13 · P1

    BLADE traces source use through decisions, distinguishing introduction, propagation, and repair without reference answers. The paper estimates roughly \$1.9 for Jev inference over 1,228 traces. Accept affordable real-trace review, requiring a real decision model rather than gold blame-step fixtures.

- [Knowing the User Is Not Knowing What We Established: Grounding Awareness in Personal Agents](https://arxiv.org/html/2610.18684v1) · 2026-10-13 · P1

    Grounding Layer separates user facts from accepted, unconfirmed, revised, and scoped agreements. Keep the ledger, pre-action gate, and raw-dialogue lookup. Verify extraction from real dialogues and bounded actions, not oracle +Status/+Policy or gold actions. No full benchmark gain claimed.

- [Fan Out or Relay? Ownership-Aware Routing for LLM Agents Querying Siloed Tables](https://arxiv.org/html/2610.18157v1) · 2026-10-13 · P1

    OAR drafts SQL and computes owner cover using only public schemas, choosing fan-out or relay before reading private rows. Test on a small real database with an actual drafter, not gold SQL or owner labels. The 13 configurations were not reproduced.

## First releases in the window closed as too costly: 369

Expand a domain below. For every entry, the full paper-scale experiment was not reproduced and review is DONE: either the cost exceeded budget or the full cost remained materially uncertain after read-only checks. No local measured results or automatic retries, implementation, or Evolve promotion are claimed. Small fixtures, numerical unit tests, and registry labels do not substitute for capability comparisons.

<details markdown="1"><summary>Search, advertising, recommendation, and LLM applications: 5</summary>

- [How to Evaluate When You Don't Know How to Evaluate? Choosing Reliable Setups for Base Language Model Benchmarking](https://arxiv.org/html/2610.19185v1) · 2026-10-13 · P1

    Selects LLM evaluation setups by monotonicity, non-randomness, and ranking consistency. Appendix A reports about 11,000 GH200 GPU-hours for 2B models and 7,000 for larger models. Five CPU minutes only computes meta-metrics on existing results. Not reproduced; review DONE.

- [Prompt or Policy? Optimizing Physician Slate Presentations with LLM User Simulators](https://arxiv.org/html/2610.18309v1) · 2026-10-13 · P1

    Compares GEPA, GRPO, and their sequence on fixed physician slates with a patient simulator, not production conversion A/B. §2.2 uses full 4B/12B tuning, a 31B judge, 4,000 GEPA calls, and 125×256 rollouts on H200. Too costly; not reproduced, review DONE.

- [Web Scale on a Budget: Tail-Aware Retrieval Evaluation](https://arxiv.org/html/2610.17986v1) · 2026-10-13 · P1

    Estimates gallery-independent per-query difficulty and uses tail estimates to forecast large-gallery metrics. Estimation on 5M samples is not indexing 100M. Original five-backbone comparisons across real large galleries are costly; not reproduced, review DONE. The 200GB full-gallery descriptors are not a per-run requirement.

- [MMTA: Benchmarking Multimodal Temporal Analysis with Time Series, Text, and Vision](https://arxiv.org/html/2610.17856v2) · 2026-10-13 · P1

    MMTA/TimeOmni-v combines temporal encoding, alignment, visual/text layout, and prediction heads. v2 Appendix C.2 specifies 140GB H200s, 1–8 GPUs per dataset, and about 40,000 padded tokens per rank. Full nine-domain trimodal training/evaluation is too costly; not reproduced, review DONE.

- [Many Right Answers, One Training Example: Removing Responder Noise from GRPO for LLM Recommenders](https://arxiv.org/html/2610.17771v1) · 2026-10-13 · P1

    ReMaRk samples uniformly by request and rewards a union of titles across responses once to reduce responder noise. Selected 2B/4B/9B checkpoints still cost 31.5/41.6/49.3 GPU-hours, and controls cost more. Relatively faster is not cheap; not reproduced, review DONE.

</details>

<details markdown="1"><summary>Foundation models, multimodal, and JEPA: 208</summary>

- [Can Learning to Answer Spatial Questions Improve Novel-View Generation?](https://arxiv.org/html/2610.20610v1) · 2026-10-14 · P1

    Ask4NV is a relevant multimodal method, not a title-based exclusion. The official resource search did not establish total joint-training cost; not reproduced.

- [SafeDriveVLA: Navigation-Conditioned World Model Dreaming for Conflict-Aware End-to-End Autonomous Driving](https://arxiv.org/html/2610.20609v1) · 2026-10-14 · P1

    Complete VLA training and closed-loop driving need substantial data and simulation; resource sections did not establish a single-card budget. Not reproduced.

- [VITAL: From Visual Motion to Precise Action](https://arxiv.org/html/2610.20604v1) · 2026-10-14 · P1

    A trajectory heuristic cannot replace visual motion to precise action. Original multi-GPU training was not reproduced.

- [GeoThinker-$F$: Endogenous Predictive World Representations for Fast Spatial Intelligence](https://arxiv.org/html/2610.20592v1) · 2026-10-14 · P1

    Reducing auxiliary FLOPs by 69.99% still entails large-model multimodal training and evaluation. Total budget unresolved; not reproduced.

- [Your Transformer Is Secretly Elastic](https://arxiv.org/html/2610.20588v1) · 2026-10-14 · P1

    Joint neuron/head soft-pruning rankings are relevant, but minutes of construction do not cover 27 models, multiple datasets, six sparsity levels, and controls. Fair full comparison is likely hours; not reproduced.

- [Continuum Attention](https://arxiv.org/html/2610.20586v1) · 2026-10-14 · P1

    Continuum Attention exactly integrates piecewise-linear K/V curves with closed-form exponential moments, half-token boundaries, and analytical gradients. The study spans 80 training runs, 3.84M tokens per model, and five seeds. Full multi-arm Metal cost could not be established cheaply; not reproduced, review DONE. Unit tests cannot substitute.

- [KinoGen: Customizable Humanoid Loco-Manipulation References via Kinematically Grounded Video Generation](https://arxiv.org/html/2610.20552v1) · 2026-10-14 · P1

    KinoGen requires video generation, geometric fitting, and tracking policies. Official sources did not establish a low total cost and physical resources are needed; not reproduced.

- [Generative Representation Learning for Scalable Latent Tokenization](https://arxiv.org/html/2610.20533v1) · 2026-10-14 · P1

    Full generative representation tokenization training and generation evaluation exceed single-card budget; not reproduced.

- [ActiveEvidence: Decision-Focused Evidence Graphs with Verifiable Acquisition Gaps](https://arxiv.org/html/2610.20532v1) · 2026-10-14 · P1

    CEIG decision certificates are relative to fixed learned scores; semantic quality is separate. Full training was 16.4 GPU-hours; not reproduced.

- [EarlyCommit: Calibrated Word-by-Word Commitment for Robots Acting Before You Finish Speaking](https://arxiv.org/html/2610.20531v1) · 2026-10-14 · P1

    EarlyCommit target construction, RLCD, and temperature fitting were verified. Total multi-arm/multi-seed duration is not disclosed and anonymous supplements were not validated; 31–35ms inference does not establish affordability. Not reproduced.

- [Physical Time as a Missing Dimension of Robot Policy Memory Dynamics](https://arxiv.org/html/2610.20524v1) · 2026-10-14 · P1

    TFP advances memory using actual physical time. Full training is too costly; not reproduced.

- [Graph-Reweighted Behavior Cloning with Human Interventions for Precise Robotic Manipulation](https://arxiv.org/html/2610.20504v1) · 2026-10-14 · P1

    Graph-reweighted BC trains multiple base policies at high cost; not reproduced.

- [Decoupled Marginal Sharpening for Training-Free Inference-Time Scaling](https://arxiv.org/html/2610.20483v1) · 2026-10-14 · P1

    Decoupled Marginal Sharpening does not update weights, but total long inference across tasks/seeds remains unpriced. Training-free is not necessarily cheap.

- [AdaRSI: On-Demand Recursive Self-Improvement for Embodied Agents](https://arxiv.org/html/2610.20474v1) · 2026-10-14 · P1

    AdaRSI needs sub-step adaptation and closed-loop execution. A relative 28% GPU saving does not establish low absolute cost; full campaign unresolved and not reproduced.

- [Equal CER, Unequal Damage: Severity-Weighted Character Error Rate for OCR](https://arxiv.org/html/2610.20461v1) · 2026-10-14 · P1

    Severity-weighted CER is relevant to OCR/VLM evaluation, not a title exclusion. Annotation/scorer training and multi-VLM runs are costly; not reproduced.

- [The COUNT: Counting N-grams Unlocks Scaling on Host Memory and Training-Free Adaptation](https://arxiv.org/html/2610.20456v1) · 2026-10-14 · P1

    COUNT maps CPU n-gram counts into unembedding input features. Main table takes about 797GB RAM and even the small table about 17.1GB, before training. No table download or reproduction; review DONE.

- [When Do Discrete Actions Make Good Continuous Controllers?](https://arxiv.org/html/2610.20429v1) · 2026-10-14 · P1

    Replacing continuous controllers with discrete actions needs matched representation and training controls. Multi-arm budget unresolved; not reproduced.

- [OrionMoE-v1.0: A Mixture-of-Experts Foundation Model for Tabular In-Context Learning](https://arxiv.org/html/2610.20418v1) · 2026-10-14 · P1

    Dual-axis table Transformers and dataset-conditioned sparse routing are relevant. §4 releases only inference code/weights, not training or the synthetic generator. Faithful pretraining cost unresolved; not reproduced.

- [Cortex: Consolidating Context into Parametric Memory](https://arxiv.org/pdf/2610.20399v1) · 2026-10-14 · P1

    Cortex writes external context into parametric memory with episodic queries and context-conditioned distillation across 4B–120B models and batch/sequential edits. Too costly; not reproduced, review DONE. Used official PDF after HTML failed and checked designated method/resources, not full reading.

- [STP-GUI: Spatially-Aware Token Pruning for Efficient Web-GUI Agents](https://arxiv.org/html/2610.20390v1) · 2026-10-14 · P1

    STP-GUI's 2M selector alone cannot replace its defining backbone and training. Original setup too costly; not reproduced.

- [Beyond Expert Rankings: Contrast Calibration for Mixed-Precision MoE Quantization](https://arxiv.org/html/2610.20353v1) · 2026-10-14 · P1

    Contrastive calibration links expert sensitivity to memory allocation. Lower inference storage does not imply an affordable quantization campaign. Cost unresolved; not reproduced.

- [ReferFlow: Beyond Final-Target Localization for Complex Referring Expressions](https://arxiv.org/html/2610.20352v1) · 2026-10-14 · P1

    ReferFlow's full multistage grounding and GRPO are costly; not reproduced.

- [Lifted State Policy Optimization: Internalizing Self-Correction through Transition Geometry](https://arxiv.org/html/2610.20350v1) · 2026-10-14 · P1

    LSPO uses lifted-state energy and finite transition credit before internalizing answers. Training is about 372.9 hours per run; full reproduction too costly.

- [Read, Parse, Describe: Unified Document Parsing with Visual Element Description Generation](https://arxiv.org/html/2610.20335v1) · 2026-10-14 · P1

    Unified document parsing and visual descriptions are relevant. Method/resource sections did not establish full VLM training and multi-parser control cost; not reproduced.

- [Are We Overthinking One-Step Generation?](https://arxiv.org/html/2610.20331v1) · 2026-10-14 · P1

    Priming Models needs both reconstruction initialization and distributional post-training. Tenfold relative compute reduction does not establish cheap single-card training; not reproduced.

- [Beyond Static Cues: Unified Dynamic Detection of MLLM Backdoors via Dual-Flow Trajectory Analysis](https://arxiv.org/html/2610.20319v1) · 2026-10-14 · P1

    Dual-flow backdoor detection needs actual poisoned models and controlled training. Total resource budget unresolved; not reproduced.

- [Anuvani-LID: Robust and Calibrated Spoken Language Identification for Indian Languages](https://arxiv.org/html/2610.20263v1) · 2026-10-14 · P1

    Anuvani-LID's full staged speech training is too costly; not reproduced.

- [Harness Policy Distillation: Aligning Agent Policies with Runtime Semantics](https://arxiv.org/html/2610.20261v1) · 2026-10-14 · P1

    HPD explicitly trains runtime semantics and compares cross-model/cross-harness reconstructed replay with control documents. Total multi-arm cost unresolved; not reproduced.

- [Scaling Multilingual Mixture-of-Experts: How Language Coverage Changes Capacity and Compute Allocation](https://arxiv.org/html/2610.20247v1) · 2026-10-14 · P1

    Fitting multilingual MoE joint scaling laws requires large from-scratch pretraining; full experiment too costly.

- [ObjDream: Guiding Vision-Language-Action Models with Object-Level Understanding and Future State Prediction](https://arxiv.org/html/2610.20223v1) · 2026-10-14 · P1

    ObjDream needs object encoding, VLM, and action training. Original multi-GPU setup was not reproduced.

- [Scaling Multilingual Safety and Reasoning Evaluation through Reasoning-Guided Translation](https://arxiv.org/html/2610.20221v1) · 2026-10-14 · P1

    A few examples' monolingual cost/latency do not bound the full multilingual evaluation/synthesis budget. Material API cost unresolved; not reproduced.

- [Atomic-WAM: Execution-Grounded Atomic-Motion Reasoning for World Action Models](https://arxiv.org/html/2610.20157v1) · 2026-10-14 · P1

    The authors already reduced global batch size and it remains expensive. Do not replace the WAM pipeline with a cheap fixture; not reproduced.

- [XViewRank: Overlap-Conditioned Score Fusion for LLM-Augmented Sparse Retrieval](https://arxiv.org/html/2610.20122v1) · 2026-10-14 · P1

    XViewRank selects on development data without test qrels. Full indexing, view generation, and multiple controls lack a settled total budget; not reproduced.

- [AFCS: Atomic-Fact-Conditioned Synthesis for Factual Knowledge Pretraining](https://arxiv.org/html/2610.20086v1) · 2026-10-14 · P1

    Fact-conditioned corpus synthesis and pretraining are both defining; the full campaign is too costly.

- [VisualWorldBench: A Fine-Grained Multi-Task Benchmark for Evaluating Visual World Knowledge in MLLMs](https://arxiv.org/html/2610.20083v1) · 2026-10-14 · P1

    The benchmark's extra VLM training and knowledge controls are too costly; retain protocol and resource details without rerunning.

- [Rethinking Prediction Horizons: Decoupling Model Queries from State Updates in Few-Step MeanFlow](https://arxiv.org/html/2610.20071v1) · 2026-10-14 · P1

    MeanFlow separates query horizon from state updates. No extra query is needed for the change, but full multi-arm calibration and generation evaluation are too large.

- [FoveaVLA: Foveation Actions Replace the Wrist Camera in VLAs](https://arxiv.org/html/2610.20064v1) · 2026-10-14 · P1

    FoveaVLA's full foveation-to-action training is too costly; not reproduced.

- [GeoCloak: An Agentic Framework for Semantics-Preserving Geolocation Privacy via Peripheral Clue Manipulation](https://arxiv.org/html/2610.20055v1) · 2026-10-14 · P1

    GeoCloak protection needs actual models and closed-loop editing. Checked resource sections did not establish full call costs; not reproduced.

- [Weighted Adjoint Matching: Finetuning Flow Matching Models with Time-Dependent Control Cost](https://arxiv.org/html/2610.20035v1) · 2026-10-14 · P1

    Preserve the time-varying control costs in Weighted Adjoint Matching. A small MLP does not make the whole study cheap; not reproduced.

- [LintEval: Benchmarking LLMs on Linter-Guided File Refactoring](https://arxiv.org/html/2610.20027v1) · 2026-10-14 · P1

    The full generation, regression, and retraining loop was not run; the complete multi-arm budget is unresolved.

- [MorphAct: Robot Policies Morphing with the Worlds They Act In](https://arxiv.org/html/2610.20019v1) · 2026-10-14 · P1

    MorphAct needs actual generation of weights/residuals and a closed-loop environment. Formula-level step costs do not establish total cost; not reproduced.

- [Gray-Box Hallucination Detection in LLMs with Token Identities](https://arxiv.org/html/2610.19996v1) · 2026-10-14 · P1

    Gray-box detection needs real traces and cross-task training. The multi-GPU experiments were not reproduced.

- [LatentLoop: Scaling Looped MoE Models with Asymmetric Compute Allocation](https://arxiv.org/html/2610.19975v1) · 2026-10-14 · P1

    Matched FLOPs for asymmetric loop MoE do not establish equal device requirements. Full multi-GPU training was not reproduced.

- [Safe-FCL: Continual Risk Awareness and Fine-Grained Safety Aggregation for Federated Continual Learning of LLMs](https://arxiv.org/html/2610.19968v1) · 2026-10-14 · P1

    Safe-FCL risk awareness and fine-grained aggregation are not one adapter operation. Full federated training cost remains unresolved; not reproduced.

- [Choosing the Number of Attention Heads from Intrinsic Dimension: A Small-Scale Study](https://arxiv.org/html/2610.19966v1) · 2026-10-14 · P1

    Intrinsic-dimension head selection is described as small-scale, but full comparison takes hours even without VAE search; not reproduced.

- [Complementary Future Token Pruning for World Action Models](https://arxiv.org/html/2610.19957v1) · 2026-10-14 · P1

    Complementary future-token pruning cannot skip the original WAM forward. Checked sections did not establish full model/evaluation budget; not reproduced.

- [SAM3RL: Memory Control via Reinforcement Learning for Visual Object Tracking](https://arxiv.org/html/2610.19931v1) · 2026-10-14 · P1

    SAM3RL needs the actual memory-eviction policy rather than rules. Original long multi-GPU training was not reproduced.

- [When Non-Adversarial Noise Hurts Learning: Benchmarking Skill Self-Evolution in Agents](https://arxiv.org/html/2610.19910v1) · 2026-10-14 · P1

    The long loop needs actual environment execution and skill learning. Resource/metric sections did not establish the full multi-arm cost; not reproduced.

- [Frustratingly Easy Majority Voting Using Length Conditioning](https://arxiv.org/pdf/2610.19890v1) · 2026-10-14 · P1

    Length-conditioned majority voting is cheap, but public tasks, multiple models, and repeated sampling were not costed in full. Cached-answer formulas cannot establish capability; not reproduced.

- [Memory-Efficient Subspace Optimization with Residual Correction: From Momentum SGD to Muon](https://arxiv.org/html/2610.19844v1) · 2026-10-14 · P1

    SMRC/PMRC preserves out-of-subspace residuals and corrects basis changes. Original pretraining used two GPUs for 60M/150M, four for 350M, and eight for 1.3B. Full multi-scale work is too costly; review DONE. A single numerical check is not capability validation.

- [What Matters for World Modeling in Vision-Language-Action Models?](https://arxiv.org/html/2610.19825v1) · 2026-10-14 · P1

    Match training resources and DINOv3 feature precomputation. Full multi-arm experiments are too costly.

- [JointServe: Serving Multi-Model Agents on Memory-Constrained GPUs](https://arxiv.org/html/2610.19822v1) · 2026-10-14 · P1

    JointServe requires runtime transfer and residency scheduling. Its reported 1.83s exchange is not total cost; platform port and evaluation cost unresolved.

- [Calibration and Risk-Budgeted Decisions with System One Models](https://arxiv.org/html/2610.19811v1) · 2026-10-14 · P1

    LTT's statistical risk-selection protocol is useful, but full adaptation and multi-dataset comparison are not costed; not reproduced.

- [Efficient contextual partial monitoring with general function approximation](https://arxiv.org/html/2610.19804v1) · 2026-10-14 · P1

    Contextual partial monitoring has public LLM-routing experiments, but total cost of fair experiments and data preparation remains unverified.

- [Asymptotically Exact Negative Guidance of Diffusion Models via Positive-Unlabeled Learning](https://arxiv.org/html/2610.19802v1) · 2026-10-14 · P1

    Keep PU online training and SMC correction for negative guidance. Full-particle, multi-condition generation quality evaluation costs remain unresolved.

- [Learning to Compute Is Not Learning to Retain or Reuse in Looped Transformers](https://arxiv.org/html/2610.19768v1) · 2026-10-14 · P1

    Looped Transformer retention/reuse diagnostics require many matched training runs. MAC proxies are not measured total FLOPs; full campaign too costly.

- [Refine Actions If Needed: Adaptive Action Chunk Refinement for Robot Manipulation](https://arxiv.org/html/2610.19765v1) · 2026-10-14 · P1

    Low latency does not price RAIN dynamic-routing training and physical execution. Official total cost unresolved; not reproduced.

- [CAST: History-Adaptive Spectral Clipping for LLM Pretraining](https://arxiv.org/html/2610.19761v1) · 2026-10-14 · P1

    Spectral clipping's adaptive history scale and threshold need actual pretraining verification. Original multi-device setup is too costly.

- [Coordi-pi: Coordination-Aware Dual-Hand Action Representation for Bimanual Dexterous Manipulation](https://arxiv.org/html/2610.19753v1) · 2026-10-14 · P1

    Full bimanual action representation and control requires multi-GPU training; not reproduced.

- [One-shot Human Video-Guided Adaptation for Vision-Language-Action Models](https://arxiv.org/html/2610.19746v1) · 2026-10-14 · P1

    CapPro one-shot means one human video, not no training. Model, training, and physical resource costs are unresolved; not reproduced.

- [Discriminative Score Function: Turning Pretrained Models into Functional Generative Priors](https://arxiv.org/html/2610.19743v1) · 2026-10-14 · P1

    DSF's training-free generation is not cheap first-order image optimization. High-order sampling evaluation cost is unresolved.

- [Does the Linguistic Register of Thinking Matter? Wenyan as a Compact Reasoning Register for Chinese LLMs](https://arxiv.org/html/2610.19741v1) · 2026-10-14 · P1

    Wenyan register compression needs actual full tuning and quality/length comparisons. GPU topology and full budget unresolved.

- [ProtModernBERT: Compute-Efficient Protein Language Modeling](https://arxiv.org/html/2610.19738v1) · 2026-10-14 · P1

    ProtModernBERT efficiency still requires protein-corpus pretraining and matched controls. Costs are too high, and paper control costs are estimates, not local measurements.

- [Mitigating Video Hallucinations via Attention-Guided Representation Perturbation](https://arxiv.org/html/2610.19728v1) · 2026-10-14 · P1

    ARP-CD needs actual forwards under representation perturbation. Partial timing does not establish full video evaluation costs; not reproduced.

- [TIMERSI: Towards Self-Improved Agentic Deployment for Time-Series Foundation Models](https://arxiv.org/html/2610.19725v1) · 2026-10-14 · P1

    TIMERSI self-improvement at deployment requires actual model/data replay; total search and multi-window costs unresolved.

- [Recognizing Dialogue Ambiguity via Candidate Set Visual Grounding](https://arxiv.org/html/2610.19723v1) · 2026-10-14 · P1

    Full ambiguity evaluation for candidate-set visual grounding takes hours; not reproduced.

- [Learning Individual Scientific Taste with Privileged Hindsight Distillation](https://arxiv.org/html/2610.19719v1) · 2026-10-14 · P1

    Privileged hindsight distillation for scientific taste needs real feedback and repeated LLM calls. Total budget and availability of public replay remain unresolved.

- [ReGRA: Residual-Gradient Adaptation for Complementary Low-Rank Fine-Tuning](https://arxiv.org/html/2610.19700v1) · 2026-10-14 · P1

    ReGRA must keep two-stage residual gradient projection and orthogonalization. Full cross-model/task training and calibration costs unresolved.

- [Share the Symbol, Not the Vector: Training-Free Fact Communication Across Language Models](https://arxiv.org/html/2610.19696v1) · 2026-10-14 · P1

    Symbolic fact communication is not a token dictionary lookup. Training-free does not eliminate J-lens construction and multi-model evaluation; not reproduced.

- [Annealed Lévy Diffusion via Gaussian Surrogate Reverse Dynamics](https://arxiv.org/html/2610.19692v1) · 2026-10-14 · P1

    ALD combines a time-varying stability index, Gaussian scale mixtures, and two reverse samplers for heavy-tailed exploration and Gaussian refinement. The paper obtained via alternative HTTP shows multi-day, multi-GPU image training and sampling; too costly.

- [Beyond Distribution Matching: Selective Margin Preservation for Supervised Fine-Tuning](https://arxiv.org/html/2610.19685v1) · 2026-10-14 · P1

    SRP-SFT top-K non-target margin hinge was checked. Multi-seed, ranking controls, and cross-backbone training are clearly high-cost multi-GPU work.

- [Enhancing Latent World Models with Associative Memory](https://arxiv.org/html/2610.19683v1) · 2026-10-14 · P1

    Associative-memory latent dynamics need end-to-end training and closed-loop planning. Multi-arm total costs unresolved.

- [ACRO: Actor-Critic Rollout Orchestration](https://arxiv.org/html/2610.19677v1) · 2026-10-14 · P1

    ACRO's actor/critic rollout orchestration needs real environments. Full training and closed-loop cost unresolved.

- [Accelerating VLA Inference with Perturbation Informed Execution](https://arxiv.org/html/2610.19656v1) · 2026-10-14 · P1

    Perturbation-aware VLA needs real fully trained policies and perturbation tasks. Original multi-GPU setup not reproduced.

- [HACHIMI-II: From Role-Play to Learner Behavior Modeling for Faithful Student Simulation](https://arxiv.org/html/2610.19654v1) · 2026-10-14 · P1

    Learner simulation's state-compilation harness is an Agent method despite the education setting. Checked full abstract and available resource text; total real-history replay and multi-model call cost unresolved.

- [SPECTRA-VLA: Base-Fine Hyperspectral Token Transfer at Frozen Vision-Language-Action Interfaces](https://arxiv.org/html/2610.19651v1) · 2026-10-14 · P1

    SPECTRA-VLA modality training and sensor loop cannot be replaced by simple tokens. Budget unresolved; not reproduced.

- [Sparse Autoencoders Are a Shared Coordinate System for Symbolic Matching](https://arxiv.org/html/2610.19636v1) · 2026-10-14 · P1

    SAE shared-coordinate semantic matching is relevant, but full multi-model encoding and data comparisons are too costly.

- [Self-Conditioning Enables Deep Sequential Reasoning in Flow Matching](https://arxiv.org/html/2610.19628v1) · 2026-10-14 · P1

    Deep-sequence self-conditioned flow needs real two-pass training, not a fixed heuristic. Original multi-GPU setup not reproduced.

- [DAGFormer: Global Topology Prediction for Transformer Cross-Layer Connections](https://arxiv.org/html/2610.19625v1) · 2026-10-14 · P1

    Full pretraining and controls for global cross-layer topology prediction are too costly.

- [F2A-ObjectNav: An Adaptive Agentic Architecture for Object-Goal Navigation](https://arxiv.org/html/2610.19618v1) · 2026-10-14 · P1

    An advisor used at under 1% of steps does not imply low API cost or wall time. Full navigation budget unresolved.

- [PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference](https://arxiv.org/html/2610.19605v1) · 2026-10-14 · P1

    PN-Mix assigns precision by prefill Q/K RoPE channel-pair norms with 1-bit residuals and sink protection. Full 8B–32B long-output multi-task evaluation cost unresolved; not reproduced, review DONE. Kitty is a baseline link, not author code.

- [Cracking Mobile Manipulation: From Failure Diagnosis to Agentic Robot System](https://arxiv.org/html/2610.19600v1) · 2026-10-14 · P1

    Mobile manipulation needs a real harness and task environment. Full cross-domain evaluation budget unresolved.

- [Who's Behind the Text? Robust Model Authorship Attribution](https://arxiv.org/html/2610.19583v1) · 2026-10-14 · P1

    Branched LoRA training and cross-domain evaluation for model authorship have unresolved total costs; not reproduced.

- [Back on Track: Deployment-time Policy Improvement via World Model Planning](https://arxiv.org/html/2610.19579v1) · 2026-10-14 · P1

    Deployment world-model planning needs rollouts, training, and closed-loop comparisons. Single-GPU execution does not establish affordability; total cost unresolved.

- [TextVerifier: Seeing Beyond Recognition to Verify Chinese Text Rendering](https://arxiv.org/html/2610.19551v1) · 2026-10-14 · P1

    Milliseconds per character do not price full training and quality comparisons. Multi-GPU experiments were not reproduced.

- [GraphRAG-LTM: A Layered Threat Modeling Framework for Attacks on Graph Retrieval-Augmented Generation](https://arxiv.org/html/2610.19549v1) · 2026-10-14 · P1

    Threat modeling requires actual retrieval, graph evidence, and authorization. Source sections did not establish a total budget; no attack implementation or reproduction.

- [VLRLA: Deployment-Time Adaptation of Vision-Language-Action Models through In-Context Reinforcement Learning](https://arxiv.org/html/2610.19517v1) · 2026-10-14 · P1

    VLRLA in-context RL training and deployment adaptation are costly; not reproduced.

- [One Block Ahead: Promoting Sampler State in Diffusion Language Models](https://arxiv.org/html/2610.19510v1) · 2026-10-14 · P1

    One Block Ahead requires a true uniform-state sampler, not fixed block rules. Baseline H100 throughput is not the new method's total cost.

- [Structure-Preserving Document-Level Data Augmentation via Discourse Parsing](https://arxiv.org/html/2610.19497v1) · 2026-10-14 · P1

    Augmented-data training and label-transfer checks are essential; full campaign cost unresolved.

- [Robota-Embed: Unified VLA Embeddings for Robot In-Context Learning and Evolution](https://arxiv.org/html/2610.19495v1) · 2026-10-14 · P1

    Robota-Embed query timing excludes SAM3, reranking, policy, and robot execution. Full training/pipeline budget unresolved.

- [Towards Efficient Simultaneous Inverse Text Normalization with Pretrained Text-to-Text Language Model and Read-Tag-Write Policy](https://arxiv.org/html/2610.19492v1) · 2026-10-14 · P1

    Read-Tag-Write training and streaming controls are expensive multi-GPU work; not reproduced.

- [AdCoEvo: A Co-Evolving Multi-Agent Advertising Delivery System](https://arxiv.org/html/2610.19454v1) · 2026-10-14 · P1

    AdCoEvo co-evolves three ad-policy roles. §5.1 AuctionNet is a simulator, so 14.02% ADV is not production A/B. Agent/RSI, not industrial P0. Three 8B roles, five 50-period sequences and alternating updates are too costly; review DONE.

- [More Than Seeing: Vision as Scalable Anchors in Native Multimodal Pre-Training](https://arxiv.org/html/2610.19443v1) · 2026-10-14 · P1

    Visual-anchor effects need matched pretraining rather than feature fixtures. Resource text did not establish total tokens or duration.

- [Progress-Aware Distillation for Mitigating Stagnation in Small Language Model Agents](https://arxiv.org/html/2610.19439v1) · 2026-10-14 · P1

    ProD preprocesses rollouts once, but full teacher/student, multi-task, and control costs remain unresolved.

- [Paraphrase Consensus Is Not Self-Consistency: Instruction Reliance and Robustness in VLA Policies](https://arxiv.org/html/2610.19438v1) · 2026-10-14 · P1

    Paraphrase consensus is not independent-policy self-consistency. Full post-training and robot evaluation budget unresolved.

- [WinARDet: Compressed Window Auto-Regression for Long-Horizon Vision-Language Grounding](https://arxiv.org/html/2610.19419v1) · 2026-10-14 · P1

    WinARDet history compression, autoregressive training, and detection evaluation costs remain unresolved.

- [Scaling LLM Inference via Parallelism: Throughput-Latency Trade-off](https://arxiv.org/html/2610.19405v1) · 2026-10-14 · P1

    The claim concerns a multi-GPU throughput/latency frontier; one card cannot reproduce the complete result.

- [RCER: Reconstructing Cross-Evidence Relations for Iterative Retrieval-Augmented Generation](https://arxiv.org/html/2610.19398v1) · 2026-10-14 · P1

    RCER requires separate relation acquisition, context reconstruction, and compositional reasoning. Readable source did not settle full model/call costs.

- [RA$^2$: Retain-Anchored Attraction Preserves Forget-Adjacent Utility in LLM Unlearning](https://arxiv.org/html/2610.19385v1) · 2026-10-14 · P1

    Retain-anchor attraction is relevant, but about five minutes for one arm excludes other datasets, methods, and seeds. Full cost unresolved.

- [One-Step Prediction Fidelity Is a Poor Proxy for Planning Performance in JEPA World Models](https://arxiv.org/html/2610.19375v1) · 2026-10-14 · P1

    JEPA prediction versus planning uses frozen physical-state decoders, paired planning seeds, separate representation/prediction errors, and matched continued training. The protocol is useful, but three environments, model ladders, and repeated training remain too expensive or unpriced. No retraining/reproduction; review DONE. Protocol advice is not Evolve integration.

- [MMKG-R1: Constructing Multimodal Knowledge Graphs via Reinforcement Learning](https://arxiv.org/html/2610.19341v1) · 2026-10-14 · P1

    Multimodal KG construction needs actual policy training, not extraction fixtures; original multi-GPU path not reproduced.

- [LLM-jp-4 Technical Report](https://arxiv.org/html/2610.19331v1) · 2026-10-14 · P1

    Full base pretraining and recipe search exceed this round's single A100/A30 budget.

- [Qwenfant: Train Big Character-level BabyLMs on Concise Parallel Text](https://arxiv.org/html/2610.19294v1) · 2026-10-13 · P1

    Character-level modeling and parallel concise corpora are relevant, but full training and scale-sweep costs were unresolved.

- [MIND: Instruction-Conditioned Incremental Grounding for Robots](https://arxiv.org/html/2610.19262v1) · 2026-10-13 · P1

    Dependency compilation, event-footprint intersection, semantic refresh, and selection isolation are essential. 0.58s evaluation and 0.56s compilation cover only local timing over 59 sequences, excluding observation, detection, planning, and motion. Full multi-model perception and execution are unpriced; no exact-predicate oracle substitute.

- [PACER: Process-Aware VLA Policy Learning from Human Corrections for Robotic Disassembly](https://arxiv.org/html/2610.19248v1) · 2026-10-13 · P1

    Process-aware VLA human corrections need real training and robots; original multi-GPU arms too costly.

- [Copy-Paste Language Models](https://arxiv.org/html/2610.19247v1) · 2026-10-13 · P1

    Small CPhead parameter overhead is not cheap pretraining. Untrained 9B/30B speed cannot establish capability; total budget unresolved.

- [LLMs program using Reusable and Composable Abstract Representations](https://arxiv.org/html/2610.19238v1) · 2026-10-13 · P1

    Causal comparison of reusable compositional abstractions needs real training and interventions; costly configurations not reproduced.

- [Spectral-MoE: Heterogeneous Per-Layer Expert Utilization in Dense-to-MoE Conversion](https://arxiv.org/html/2610.19232v1) · 2026-10-13 · P1

    Spectral-MoE's heterogeneous layer expert budgets need actual conversion and recovery training. Original multi-GPU configuration too costly.

- [DUALVIEW: Leveraging Broad and Output-Specific Evidence for LLM-based Multi-Output Text Regression](https://arxiv.org/html/2610.19206v1) · 2026-10-13 · P1

    DUALVIEW requires full supervision of broad and output-specific evidence at a large budget; not reproduced.

- [Weighted Ensemble Sampling for Rare-Event Estimation in Language Models](https://arxiv.org/html/2610.19202v1) · 2026-10-13 · P1

    Rare-event estimates need adequate samples and per-seed costs. Resource sections define metrics but do not settle total costs.

- [Into the LidarVerse: A Real-Time Unified LiDAR World Model Across Tasks and Sensors](https://arxiv.org/html/2610.19201v1) · 2026-10-13 · P1

    LidarVerse teacher/student and multi-sensor data costs are unresolved. Real-time serving does not imply affordable training.

- [Embedding Geometry Shapes LLM Routing: Tracing Failure Modes and Improving Generalization](https://arxiv.org/html/2610.19198v1) · 2026-10-13 · P1

    Embedding interventions and router generalization require full data and training. Allocated resources are not minimum requirements; campaign budget unresolved.

- [HERO: Harnessing Evidence for Test-time Refinement and Prompt Optimization in Program Generation](https://arxiv.org/html/2610.19184v1) · 2026-10-13 · P1

    HERO requires actual program execution and prompt optimization. References stay on the benchmark side. Total agent/API/execution costs unresolved.

- [Into the Unknown: Benchmarking AI agents on open scientific research problems](https://arxiv.org/html/2610.19159v1) · 2026-10-13 · P1

    Retain integrity lessons from open scientific research benchmarks. The complete long research execution is too costly.

- [FACT: A Multimodal Force-Action-Track Foundation Model for Human-to-Robot Dexterity](https://arxiv.org/html/2610.19155v1) · 2026-10-13 · P1

    FACT's human-to-robot dexterity pretraining needs multiple devices at high cost.

- [TRACER: Trace-Regularized Training Against Indirect Prompt Injection](https://arxiv.org/html/2610.19133v1) · 2026-10-13 · P1

    TRACER must retain channel conditioning and trace training; full training/attack matrix cost unresolved.

- [Unlocking Structured Pruning for Reasoning Language Models via Attention-Preserving MLP Trimming](https://arxiv.org/html/2610.19121v1) · 2026-10-13 · P1

    Retain attention and decoder depth while pruning only the MLP. A short 128-step timing is not the quality-evaluation budget; total cost unresolved.

- [Genesis Steering: Better Activation Steering Through Training Data](https://arxiv.org/html/2610.19114v1) · 2026-10-13 · P1

    Vector addition alone cannot replace construction of training references and fair public evaluation. Resource text did not establish total budget.

- [From Copying to Composition: How Language Models Develop In-Context Learning](https://arxiv.org/html/2610.19113v1) · 2026-10-13 · P1

    Controlled ICL copying/composition learning studies are too costly. Preserve diagnostic insights without reproducing.

- [Beyond Aggregate Accuracy: Item-Level Transitions in Prompt Optimization](https://arxiv.org/abs/2610.19084v1) · 2026-10-13 · P1

    RFDPO must use actual item-level feedback in subsequent optimization. Offline churn formulas do not reproduce it, and API budget remains unresolved.

- [How Inner Optimizers Shape Replica Scaling](https://arxiv.org/html/2610.19064v1) · 2026-10-13 · P1

    Replica scaling needs actual multi-replica training. Full cost unresolved; multi-GPU access is not assumed.

- [Tracing Morphology, Semantics, and Divergence in Language Acquisition](https://arxiv.org/html/2610.19041v1) · 2026-10-13 · P1

    Language-acquisition trajectories and checkpoint scans already take hours; full training/evaluation not reproduced.

- [How Many Ranks Does a Token Need? A Noise-Floor Squelch for Rank-One LoRA Experts](https://arxiv.org/html/2610.19033v1) · 2026-10-13 · P1

    Rank-one expert noise gating and SURE thresholds require real LoRA training; full campaign too costly.

- [Joint Subspace Sparse Attention for Efficient Long-Context Decoding](https://arxiv.org/html/2610.19026v1) · 2026-10-13 · P1

    JSSA projection and cache score-scan kernels need real weights and CUDA evaluation. Local milliseconds do not settle total cost.

- [How Far Can Coding Agents Go in Visual Generation?](https://arxiv.org/html/2610.19025v1) · 2026-10-13 · P1

    The source keeps token/call/cost ledgers, but checked material did not price the entire campaign. Drawing primitives are not capability evaluation.

- [Data Density Scaling Laws for Image Self-Distillation](https://arxiv.org/html/2610.19013v1) · 2026-10-13 · P1

    Image self-distillation scaling laws require multiple matched pretraining arms; original multi-GPU work not reproduced.

- [Discovering Undisclosed Concepts in LoRA Adapters for Diffusion-Based AIGC Models](https://arxiv.org/html/2610.18990v1) · 2026-10-13 · P1

    SGES concept discovery needs actual LoRA and a diffusion backbone. Low rank does not establish low cost; total budget unresolved.

- [LoopWAM: Closed-Loop Generalist Policy Improvement from Deployment Rollouts](https://arxiv.org/html/2610.18873v1) · 2026-10-13 · P1

    LoopWAM's full rollout/training/evaluation cost is unresolved. Historical-trajectory fixtures cannot replace closed-loop runs.

- [EmbodiedEvo: Self-Evolving Coding Agent For Physical Intelligence](https://arxiv.org/html/2610.18867v2) · 2026-10-13 · P1

    No parameter updates does not mean no execution or API costs. A 53% relative saving does not establish affordable full search.

- [DoubtLess: Training-Free Contrastive Decoding for Efficient Reasoning](https://arxiv.org/html/2610.18862v1) · 2026-10-13 · P1

    DoubtLess is training-free but uses long multi-model multistream inference and TP. Total resource cost unresolved.

- [Visual Tokens on Demand: Visual Budgeting for Scalable and Efficient Multi-Image Reasoning in Multimodal LLMs](https://arxiv.org/html/2610.18858v1) · 2026-10-13 · P1

    A small budgeter and 2ms overhead do not price full VLM training and quality comparisons. Full cost unresolved.

- [Interaction Latents as Actions for Contact-Rich Manipulation](https://arxiv.org/html/2610.18855v2) · 2026-10-13 · P1

    Latent interaction-action learning and real/simulated loops need complete multi-arm training. Resource sections did not establish total time.

- [ForceWAM: Decoupling Future and Response Learning from Demo and Play Data for Contact-Rich Manipulation](https://arxiv.org/html/2610.18852v1) · 2026-10-13 · P1

    ForceWAM must preserve both future/response decoupling training stages. Full multi-task cost is high or unresolved.

- [The Last Remote Sensing Model Built by Humans? Casting Any Earth Observation Task as Recursive Self-Improvement](https://arxiv.org/html/2610.18845v1) · 2026-10-13 · P1

    Remote sensing is not a title-based exclusion. The actual agent self-improvement run already takes hours; not reproduced.

- [Read the Room Before Your Model Generates](https://arxiv.org/html/2610.18820v2) · 2026-10-13 · P1

    A 32-dimensional module is not a cheap campaign; the paper reports 125 GPU-hours. Not reproduced.

- [Back-Translation Still Matters: Leveraging Monolingual Data for Low-Resource Machine Translation with LLMs](https://arxiv.org/pdf/2610.18818v2) · 2026-10-13 · P1

    Keep back-translated corpora and matched LLM training. PDF resource excerpts did not establish total time/storage.

- [Depth Memory](https://arxiv.org/html/2610.18809v1) · 2026-10-13 · P1

    LDM's recursive least-squares memory and inverse covariance are essential. Full multi-GPU, high-token pretraining was not reproduced.

- [$λ_0$: Scaling Open-World Egocentric Human Data for Humanoid Loco-Manipulation](https://arxiv.org/abs/2610.18950v1) · 2026-10-13 · P1

    Cross-embodiment alignment, offline motion/refinement, and midtraining require substantial data and physical resources; the abstract already exceeds feasible public reproduction scope.

- [GreenWAM: A World Foundation Model for Robotics](https://arxiv.org/pdf/2610.18774v1) · 2026-10-13 · P1

    The official PDF shows complete cross-embodiment data/training. Total budget unresolved; a state codec cannot replace foundation training.

- [Segment Where You Look: Attention as the Interface Between Language Models and Segmenters](https://arxiv.org/html/2610.18729v1) · 2026-10-13 · P1

    Preserve multimodal training and actual segmenter forwards in the attention interface. Original full multi-GPU setup not reproduced.

- [UniW(A)M: A Unified Mixture-of-Experts Framework for World and World-Action Models](https://arxiv.org/html/2610.18697v1) · 2026-10-13 · P1

    Unified MoE world/action training and pipeline costs are unresolved. A lightweight router does not price all experts.

- [GeoReader: Learning Latent Geometry for Spatial Reasoning in Vision-Language Models](https://arxiv.org/html/2610.18694v1) · 2026-10-13 · P1

    GeoReader's actual geometric transfer and VLM training are expensive; not reproduced.

- [Just Respect the Semantics: Image-Token Compression via Pre-LLM Semantic Variable-Resolution Tokenization and In-LLM Relevance Pruning](https://arxiv.org/html/2610.18690v1) · 2026-10-13 · P1

    Semantic variable resolution and in-LLM pruning need real two-stage forwards. Training-free does not eliminate multi-model evaluation costs.

- [Does Pretraining Teach Chemical Language Models Chemistry?](https://arxiv.org/html/2610.18651v2) · 2026-10-13 · P1

    Retain causal controls in chemical-language pretraining. Total multi-arm data and training cost unresolved.

- [Tiny Recursive Message Passing](https://arxiv.org/html/2610.18649v1) · 2026-10-13 · P1

    The abstract's ten minutes cover the smallest lattice arm only. Full ACT/graph/truncation/SAT/N-queens and multi-seed comparisons are expensive.

- [To Align or Not To Align: Check Your COMPASS Before You Train](https://arxiv.org/html/2610.18638v1) · 2026-10-13 · P1

    Cheap kNN compatibility diagnostics do not price supervision and evaluation. Full fair comparison too costly.

- [VideoJev: System One Model for Video Understanding and Interaction](https://arxiv.org/html/2610.18615v1) · 2026-10-13 · P1

    SystemOne video scoring must run a real encoder, not use cached candidates. Joint-forward latency does not establish full training and multi-arm cost.

- [DPOison-VL: Clean Preference Poisoning in Vision-Language Direct Preference Optimization](https://arxiv.org/html/2610.18609v1) · 2026-10-13 · P1

    Retain security risk and defense evaluation as research leads; do not run poisoning training. Full study is too costly.

- [Beyond Answer Voting: Fine-Grained Correction of LLM Reasoning through Graph Alignment across Sampled Traces](https://arxiv.org/html/2610.18606v1) · 2026-10-13 · P1

    Fine-grained graph correction requires real generation and alignment of multiple trajectories; full inference too costly.

- [LLM2R: From Large Language Models to 3D Reassemblers](https://arxiv.org/html/2610.18604v1) · 2026-10-13 · P1

    LLM2R's actual 3D representation training/unfreezing and multi-part pose evaluation costs unresolved.

- [Rethinking Projector Training in Multimodal LLMs](https://arxiv.org/html/2610.18598v1) · 2026-10-13 · P1

    A 30s closed-form projector build cannot replace multi-stage capability evaluation. Full training takes hours.

- [WAVE-0: Bridging VLA Policies and WAMs with Lightweight Latent Future Prediction](https://arxiv.org/pdf/2610.18568v1) · 2026-10-13 · P1

    Checked official PDF methods/resources. WAVE-0 uses real action supervision for a 257M latent world model with future, delta, and counterfactual ranking losses. After freezing, predicted future tokens from VLM latent action plans feed the action expert. Full model about 4.3B, not an isolated 257M prototype. LIBERO used eight 96GB RTX PRO 6000 GPUs for about 10+13 hours; RoboTwin used eight H100s for about 6+78 hours (roughly 670 H100 GPU-hours), plus an eight-A800 physical bimanual experiment. Too costly for one A100/A30 or Mac; no downloads or reproduction, review DONE. Simulation fixtures or partial world-model training do not substitute.

- [Two For The Price Of One: Curvature-Aware Pruning Preserves Influence Functions Too](https://arxiv.org/html/2610.18516v1) · 2026-10-13 · P1

    Sparse/low-rank models need actual pruning and influence-function evaluation. Relative 5–25× speedup does not establish absolute campaign costs.

- [Towards Safe Autonomy for Computer Use](https://arxiv.org/html/2610.18508v1) · 2026-10-13 · P1

    Verify trust boundaries and pixel/AX consistency in practice; a state machine cannot substitute. Full environment/model-call budget unresolved.

- [EgoOmniWorld: Unifying Egocentric Understanding via Ego-Action-World Interactions](https://arxiv.org/html/2610.18499v1) · 2026-10-13 · P1

    EgoOmniWorld interaction/understanding data and complete multi-GPU adaptation are costly.

- [Graph Metanetworks for Transformer Based Language Models](https://arxiv.org/html/2610.18471v1) · 2026-10-13 · P1

    Actual weight-graph learning is required rather than network statistics. Original eight-GPU training not reproduced.

- [Readout Scaling Shapes Sparse Feature Recovery](https://arxiv.org/html/2610.18462v2) · 2026-10-13 · P1

    Small SAE parameter count does not imply an inexpensive campaign. The reported CPU run already takes hours.

- [EmoGenie: Benchmarking and Evaluating Expressed and Evoked Emotion in T2I Generation with MLLMs](https://arxiv.org/html/2610.18455v1) · 2026-10-13 · P1

    Full emotional-generation training, annotation, and evaluation are too costly.

- [FastEEP: Fast Intra-Instance Elastic Scaling for Expert-Parallel MoE Serving](https://arxiv.org/html/2610.18451v1) · 2026-10-13 · P1

    The capability depends on multi-node MoE transfer and communication; one A100 cannot be assumed sufficient.

- [Thinker-WM: A Unified World Model with Shared Multimodal Representations for Embodied Intelligence](https://arxiv.org/html/2610.18447v2) · 2026-10-13 · P1

    Resource sections did not establish full multimodal training costs. Rapid background evaluation setup does not make training affordable.

- [Agaram 2.5B: The First Tamil-First Language Model Trained from Scratch with Tool Calling. A Playbook for Under-Represented Languages](https://arxiv.org/html/2610.18420v1) · 2026-10-13 · P1

    SFT alone takes hours, in addition to pretraining and tool data. Too costly.

- [Multi-Stream Residual Computation in Diffusion Language Models](https://arxiv.org/html/2610.18407v1) · 2026-10-13 · P1

    Core training and behavioral controls for multi-stream write quantities cannot be replaced by residual tensor tests; total cost unresolved.

- [Bifocal: Training-Free Mixed Granularity Visual Token Pruning for Multimodal LLMs](https://arxiv.org/html/2610.18399v1) · 2026-10-13 · P1

    The two-stage mixed-granularity mechanism is relevant, but full training-free evaluation cost is unresolved.

- [ReDiS: Reasoning-Diagnosis Self-Evolution for Multimodal Reasoning in Remote Sensing](https://arxiv.org/html/2610.18388v1) · 2026-10-13 · P1

    Joint reasoning/diagnosis training requires many rollouts. Full multi-arm resources unresolved.

- [Hallucination-aware Faithful Reasoning in Remote Sensing](https://arxiv.org/html/2610.18369v1) · 2026-10-13 · P1

    Faithful cross-modal reasoning post-training uses an expensive multi-GPU configuration.

- [Pin It on Anyone: Certified Targeted Displacement of Multi-Bit LLM Watermarks Without the Key](https://arxiv.org/html/2610.18359v1) · 2026-10-13 · P1

    Use only as authentication-boundary research. Per-context oracle forwards and total sample cost are unresolved; no targeted disruption or reproduction.

- [Omni-RS: Unifying Multi-Task Understanding and Generation in Remote Sensing](https://arxiv.org/html/2610.18323v1) · 2026-10-13 · P1

    Unified remote sensing understanding/generation requires complete two-stage training. Original long multi-GPU runs not reproduced.

- [Beyond Equation Search: Conjecture-Guided Discovery with SCOPE and ClosureBench](https://arxiv.org/html/2610.18938v1) · 2026-10-13 · P1

    SCOPE needs active experiments and an evidence loop, not equation fixtures. Official sources did not establish an affordable total budget.

- [TRACESTEER: Trace Driven Activation Steering for Hallucination Mitigation in Diffusion Language Models](https://arxiv.org/html/2610.18173v1) · 2026-10-13 · P1

    TraceSteer needs actual denoising trace extraction/intervention, not vector fixtures. Resource sections did not establish a low total budget.

- [SparPR: Runtime KV-Cache Recovery for Resource-Constrained LLM Inference on Consumer Hardware](https://arxiv.org/html/2610.18140v1) · 2026-10-13 · P1

    SparPR combines query-aware block selection, dynamic budgets, and local recomputation for KV recovery. An 8K run takes 44 minutes even on the 8GB laptop; multiple lengths, ratios, and ablations add cost. Not reproduced, review DONE; no probe just to prove it slow.

- [A CaLLM Judge is a Better Judge: Mitigating Bias in LLM-as-a-judge](https://arxiv.org/html/2610.18108v1) · 2026-10-13 · P1

    Postprocessing calibration may be affordable, but checked excerpts did not establish the public score matrix or full bias discovery/calibration cost. A method name or cheap regression is insufficient.

- [ResearchFlow-Eval: Tracing the Execution Gap in End-to-End Multi-Claim Autoresearch](https://arxiv.org/html/2610.18088v2) · 2026-10-13 · P1

    ResearchFlow-Eval's multi-claim research execution is inherently expensive; retain audit protocol only.

- [Same Function, Different Trajectory: No Standard Optimizer Is Equivariant to Transformer Reparameterization](https://arxiv.org/html/2610.18085v1) · 2026-10-13 · P1

    Matched multi-scale training for optimizer non-equivariance already takes multiple GPU-hours; not reproduced.

- [inLoRA-MINT: Internal Representations for Auditing Training Data in Domain-adapted LLMs](https://arxiv.org/html/2610.18051v1) · 2026-10-13 · P1

    inLoRA-MINT needs actual internal activations and adaptation training; full public data and run budget unresolved.

- [Data-Free Continual Learning for World Action Model with Rectified Generative Replay](https://arxiv.org/html/2610.18038v2) · 2026-10-13 · P1

    A single 18-minute replay excludes about 108 minutes of fine-tuning and multi-task/multi-arm evaluation.

- [SHELDON: Reasoning through Dual Search over Hypothesis and Observation Spaces](https://arxiv.org/html/2610.18025v1) · 2026-10-13 · P1

    SHELDON's full dual-search and evidence feedback model/execution cost is unresolved. Fixed candidate trees are not RSI capability.

- [Match the Canvas, Not Just the Answer: Predictability-Aware SFT for Diffusion Language Models](https://arxiv.org/html/2610.18001v1) · 2026-10-13 · P1

    Even the minimum complete predictability-aware SFT budget takes hours.

- [ReEnvision: Future-Guided Selective Action Repair for Long-Horizon Manipulation](https://arxiv.org/html/2610.17977v2) · 2026-10-13 · P1

    145ms execution versus a 110ms base does not price training and multi-task comparisons. Full budget unresolved.

- [BELT : BEhavior-Aligned Low-Rank KV Cache Compression with Learned Top-k Rank Allocation](https://arxiv.org/html/2610.17966v1) · 2026-10-13 · P1

    Closed-form key-side surrogates cannot substitute for rank allocation and real long-context quality/throughput evaluation. Total cost unresolved.

- [Virtual Head Attention](https://arxiv.org/html/2610.17959v1) · 2026-10-13 · P1

    Virtual-head architecture requires actual training and forward passes. Resource sections did not establish total tokens and devices.

- [HaloBlock: Faster and Better Decoding for Diffusion Large Language Models](https://arxiv.org/html/2610.17948v1) · 2026-10-13 · P1

    Actual block-decoding inference uses multiple models and GPUs; full evaluation too costly.

- [MERIT: Multimodal Evidence Reasoning over Image Tables](https://arxiv.org/html/2610.17937v1) · 2026-10-13 · P1

    Retain table vision and reasoning training; do not give gold supporting facts to the evaluated agent. Full training/evaluation costs unresolved.

- [Batch-Paced: Fixed-Budget Batch Decoding in Discrete Diffusion Language Models](https://arxiv.org/html/2610.17917v1) · 2026-10-13 · P1

    The paper excludes budget-matched probe decoding from the main table, but its costs still count. Full campaign budget unresolved.

- [DriveWLA: Unifying Future Dynamics and Scene Semantics through World-Language-Action Modeling for Autonomous Driving](https://arxiv.org/html/2610.17903v1) · 2026-10-13 · P1

    Complete world-language-action and RL training is expensive multi-GPU work; not reproduced.

- [FlashMask-3: Efficient and Expressive Mask-Aware Distributed Attention](https://arxiv.org/html/2610.17901v1) · 2026-10-13 · P1

    Hopper-specific kernels and distributed claims cannot be reproduced faithfully on one A100/A30; hardware and cost exclude them.

- [Prefilling-dLLM v2: Learned Chunk Routing for Long-Context Diffusion Language Models](https://arxiv.org/html/2610.17868v1) · 2026-10-13 · P1

    Original chunk-routing continued training uses multiple GPUs. Full training and length sweep remain expensive or unpriced.

- [MicroCLIP: Connecting Text and Microscopy Images via Contrastive Language--Image Pretraining](https://arxiv.org/html/2610.17866v1) · 2026-10-13 · P1

    Full cross-text/microscopy CLIP pretraining is too costly.

- [DVTR-KD: Distilling Vision-Language Models via Intermediate Visual Token Reconstruction](https://arxiv.org/html/2610.17853v1) · 2026-10-13 · P1

    Real visual teachers and token reconstruction training are required; original multi-GPU setup not reproduced.

- [What Makes a Good Visual Representation for Spatial Understanding in MLLMs?](https://arxiv.org/html/2610.17844v1) · 2026-10-13 · P1

    Full visual representation-space understanding transfer trains on 64 GPUs; too costly.

- [Diff Diffusion: Predicting Edit Paths with Diffusion Models for Efficient Code Editing](https://arxiv.org/html/2610.17831v1) · 2026-10-13 · P1

    DiffDiffusion's editing model, SFT/RL, and multilingual evaluation need real large-scale training. This review does not validate industrial A/B details.

- [MHVF: Training-Free GUI Grounding via Verification-Guided Multi-Hypothesis Search](https://arxiv.org/html/2610.17792v1) · 2026-10-13 · P1

    Training-free MHVF still needs many real VLM forwards for multi-hypothesis search. Multi-benchmark cost unresolved.

- [Full-duplex Spoken Language Modeling with Discrete Diffusion](https://arxiv.org/html/2610.17780v1) · 2026-10-13 · P1

    Full speech generator, listening, and policy pipeline is expensive multi-node work.

- [DT-LoRA: Reaching Beyond the Tangent Space of Low-Rank Adaptation](https://arxiv.org/html/2610.17730v1) · 2026-10-13 · P1

    Low rank does not establish a cheap full study. Resource excerpts did not price multi-task training.

- [From Token Correction to Claim Admission: Training-Free Hallucination Mitigation for Large Vision-Language Models](https://arxiv.org/html/2610.17706v1) · 2026-10-13 · P1

    Claim admission requires actual visual evidence, calibration, and multi-task comparisons. Fitting on one GPU does not establish total affordability.

- [OccWAM: Occupancy World-Action Models with Joint Scene-to-Ego Flow Matching](https://arxiv.org/html/2610.17688v1) · 2026-10-13 · P1

    Full occupancy/action model training requires multiple GPUs and is too costly.

- [Encoding Context into LLM Weights: What Makes It Context?](https://arxiv.org/html/2610.17686v1) · 2026-10-13 · P1

    Parametric context requires actual multi-chunk optimization and retention evaluation. One fixed example's speed is supplemental, not the full budget.

- [Code2Worlds-2: Physically Plausible Agent Harness for Embodied World Simulation](https://arxiv.org/html/2610.17651v1) · 2026-10-13 · P1

    Physically executable world generation needs actual geometry, simulation, and agent loops. Full calls, generation, and execution unpriced.

- [MemAct: Streaming Spatial Understanding with Memory and Active Exploration](https://arxiv.org/html/2610.17640v1) · 2026-10-13 · P1

    MemAct memory writes/reads and active exploration need real long-context training and rollouts; original multi-GPU, large-data setup too costly.

- [Acting Through Registers](https://arxiv.org/html/2610.17638v1) · 2026-10-13 · P1

    Acting Through Registers needs real world/action training. Read resource excerpts did not establish a full budget.

- [Mixed Precision Scaling Laws for Quantized Pretraining](https://arxiv.org/html/2610.17637v1) · 2026-10-13 · P1

    Mixed-precision scaling requires multiple complete pretraining arms. Total tokens/time unverified, and low bit width does not establish affordability.

- [The Tokens Strike Back: Safety-Aware Denoising with Directional Embedding-based Revision](https://arxiv.org/html/2610.17636v1) · 2026-10-13 · P1

    SADDER needs actual denoising trajectories and activation signals. Full multi-setting budget unresolved.

- [From Pixels to Executable Physics: Behavior-Grounded World Models for Embodied Action Consequence Prediction](https://arxiv.org/html/2610.17630v1) · 2026-10-13 · P1

    Physical generation and consequence evaluation cannot be replaced by rule placeholders. Total model/data/run budget unresolved.

- [4LC: 4D Latent Cache for Efficient Conditioning in Dynamic World Modeling](https://arxiv.org/html/2610.17625v1) · 2026-10-13 · P1

    Full 4D-latent-cache conditional adapter/control-branch training is too costly.

- [Revisiting the 16x Pretraining Compute Gap between Diffusion and Autoregressive Language Models](https://arxiv.org/html/2610.17590v1) · 2026-10-13 · P1

    Reassessing the 16-fold gap requires a large real pretraining grid. Resource text did not establish the absolute total cost.

- [TwinPrune: Density-Aware Two-Phase Token Pruning for Vision-Language Models](https://arxiv.org/html/2610.17530v1) · 2026-10-13 · P1

    Prefill/decode pruning needs real models and quality, latency, and VRAM measurements. Largest multi-GPU model and total study too costly.

- [ATTUNE: Agentic Throughput Tuning for LLM Training](https://arxiv.org/html/2610.17528v1) · 2026-10-13 · P1

    Throughput tuning targets cluster-scale training. Editing settings cannot establish convergence; too costly.

- [Box-WAM: Box Trajectories as Compact State Representations for World Action Models](https://arxiv.org/html/2610.17526v1) · 2026-10-13 · P1

    Single-step runtime improvements do not price full WAM training, data, and closed-loop evaluation. Resource excerpts lack total budget.

- [Foundation Models for Event Prediction Across Heterogeneous Event Logs](https://arxiv.org/html/2610.17503v1) · 2026-10-13 · P1

    FEP's nonparametric attention is relevant, but complete pretraining and multiple models, six configurations, and five seeds per dataset are a large multi-GPU campaign.

</details>

<details markdown="1"><summary>Post-training, Agentic RL, and OPD: 80</summary>

- [Co-Evolving Acting and Forecasting for Language Agents](https://arxiv.org/html/2610.20597v1) · 2026-10-14 · P1

    CoPE supervises later actions on successful on-policy trajectories with the same backbone, not a fixed success-action table. Full cost remains materially uncertain after official method/resource checks.

- [One Task, Many Interfaces: Simple Cross-Interface Consistency Training Improves LLM Agent Robustness](https://arxiv.org/html/2610.20576v1) · 2026-10-14 · P1

    CIPR enforces KL consistency over de-semanticized tool IDs, twin interfaces, and equivalent action distributions. A numerical KL example cannot replace dual-interface training. Official-source review left total cost unresolved.

- [Recovering Reliable Supervision via Critique-Guided On-Policy Distillation](https://arxiv.org/html/2610.20572v1) · 2026-10-14 · P1

    CriticOPD critiques failed trajectories, asks students to revise, and scores with privileged teacher critiques. Four A100s (two student, two teacher), up to 16,384 response tokens, and 8–32 evaluation samples make the full study costly. Not reproduced, review DONE. Verified author repository kzhao5/CriticOPD.

- [Manacá-1B-Instruct-2: Reproducible Safety Alignment for a Native Brazilian-Portuguese LLM. Negative DPO Results, a Controlled Composition Scan, and a Silent Failure Mode of the LLM Judge](https://arxiv.org/html/2610.20570v1) · 2026-10-14 · P1

    Manacá reports three negative DPO runs, three Safety-SFT rounds, and mixture sweeps. Preserve negative results and effective N under judge refusals; reward margins are not generation capability. Full cost remains unresolved.

- [PrismaCoder: Pushing the Boundaries of Open Multimodal Code Intelligence through Decomposed Rubric Synthesis](https://arxiv.org/html/2610.20538v1) · 2026-10-14 · P1

    PrismaForge applies decomposed rubrics to multimodal code filtering and RL rewards; PrismaCoder includes the whole data/training chain. Original resources exceed the single-card budget.

- [VASPO: Self-Distillation with Privileged Value Estimation](https://arxiv.org/html/2610.20516v1) · 2026-10-14 · P1

    VASPO combines same-privilege critic PPO advantages with bounded self-teacher ratios. Eight H200s, full-parameter training, 200 rollout updates, and eight responses per question are too costly. Not reproduced, review DONE.

- [Hindsight-Privileged RLVR: Single-Rollout Token Credit Without Group Sampling](https://arxiv.org/html/2610.20497v1) · 2026-10-14 · P1

    HP-RLVR constructs single-trajectory token credit from causal versus hindsight JS under a generation snapshot, without reference answers. Three 8B tasks and paired 100-step training still cost substantially despite relative speed versus GRPO. Not reproduced, review DONE.

- [Training Language Models to Fail Gracefully](https://arxiv.org/html/2610.20401v1) · 2026-10-14 · P1

    GracefulRL combines success/fallback/error log barriers with TailRL and smoothing to avoid fallback-only collapse. Rules cannot substitute for policy training. Full cost remains materially uncertain.

- [TreeFlex: Agents Navigating Their Own Search Trees](https://arxiv.org/html/2610.20334v1) · 2026-10-14 · P1

    TreeFlex uses one Reflection/Execution policy and tree-aware GRPO to navigate its own search tree. Preset trees cannot substitute for tools and state restoration. Full cost remains unresolved.

- [CASI: Credit Assignment via Set Intervention for Agentic Retrieval](https://arxiv.org/html/2610.20293v1) · 2026-10-14 · P0

    CASI intervenes over a fixed retrieval snapshot, using Shapley attribution and bounded zero-sum projection for action credit. §4.5 reports randomized seven-day A/B on 10% production traffic, Advv +3.51%; industrial evidence qualifies. Private replay/teacher and full training scale are unavailable, so faithful cost is unresolved. Not reproduced, review DONE.

- [Repairing Speech Access After Text Updates with Frozen Affine Fields](https://arxiv.org/html/2610.20253v1) · 2026-10-14 · P1

    AFFIRM combines frozen-base correction with zero-mean query-conditioned affine correction for speech access. Small operator size does not price acquisition/training. Full cost unresolved.

- [What Makes a Social Agent's Interactions Effective? Learning from Verifiable Outcomes in Paired Worlds](https://arxiv.org/html/2610.20195v1) · 2026-10-14 · P1

    PaCPO assigns credit from tentative plan feasibility across paired worlds. Private constraints remain with the checker; the evaluated agent cannot see gold plans for either world. Full cost unresolved.

- [RM-OPD: On-Policy Distillation for Generative Reward Models](https://arxiv.org/html/2610.20174v1) · 2026-10-14 · P1

    RM-OPD trains domain GRPO teachers, then routes OPD and merges domain weights into a reward model. 74K preferences, training on two nodes × eight H800s, and evaluation on eight H800s are too costly. Not reproduced, review DONE.

- [MemDuet: Learning Dual-Process Memory for Long-Context Reasoning](https://arxiv.org/html/2610.19928v1) · 2026-10-14 · P1

    MemDuet uses parallel small-model evidence selection and large-model verification/update in three stages of SFT, GRPO, and joint training. Original resources exceed the single-card budget.

- [MolHop: Scaffold-Hopping Molecular Design with Agentic Reinforcement Learning](https://arxiv.org/html/2610.19920v1) · 2026-10-14 · P1

    MolHop navigates/edits about 1.6M scaffolds and learns cross-scaffold discovery through Agentic RL. Original resources exceed the single-card budget.

- [Not All Criteria Matter: Importance-Aware Criteria Weighting for Rubric-Based LLM Evaluation](https://arxiv.org/html/2610.19915v1) · 2026-10-14 · P1

    ICW derives rubric weights through LLM pairwise importance comparisons, consistency repair, and a principal eigenvector. Random matrices do not substitute for LLM judgments or demonstrate gains. Full cost unresolved.

- [Rent-Seeking Language Models: Reward Models Set the Prices, Frequent Audits Curb the Rent](https://arxiv.org/html/2610.19832v1) · 2026-10-14 · P1

    Rent-Seeking studies RL overoptimization with proxy/gold rewards and audit frequency. Keep the fixed testbed, equally accurate proxies, and actual training rather than simulating a rent scalar. Original resources exceed budget.

- [Learning Perception to Action Rules through Reinforcement Learning for Theory-of-Mind Reasoning](https://arxiv.org/html/2610.19796v1) · 2026-10-14 · P1

    ToM rule-GRPO trains rules linking perception, belief, and action. Choose checkpoints on development and isolate test; handwritten if-then rules do not replace learning. Full cost unresolved.

- [More Methods, Better Agents? A Reality Check on Self-Distillation in Agentic Reinforcement Learning](https://arxiv.org/pdf/2610.19789v1) · 2026-10-14 · P1

    The self-distillation reality check compares ten methods with GRPO across 132 runs and 12,124.4 H800 GPU-hours. Retain fair-comparison findings without rerunning. Too costly; review DONE.

- [Qwen-MT-Lumen at WMT2026: Instruction-Specialized Translation via Quality-Aware Training and On-Policy Distillation](https://arxiv.org/html/2610.19758v1) · 2026-10-14 · P1

    Qwen-MT-Lumen uses four translation stages: CPT/SFT, online M2PO, teacher OPD, and structural repair, not a lightweight standalone loss. Full cost unresolved.

- [RouteWeaver: Weaving Mode Selection and Execution into Unified LLM Routing](https://arxiv.org/html/2610.19705v1) · 2026-10-14 · P1

    RouteWeaver splits mode and execution credit using COMET-GRPO and learns three routing modes via progressive exploration. Original resources exceed single-card budget.

- [Function-Space Temporal Self-Distillation for Policy Optimization](https://arxiv.org/html/2610.19687v1) · 2026-10-14 · P1

    FSPO keeps sparse historical next-token distributions for temporal function-space consolidation, with privileged correction and reliability adjustment. Original resources exceed budget.

- [Model What Matters: Decision-Guided Selective World Modeling for Language Agents](https://arxiv.org/html/2610.19642v1) · 2026-10-14 · P1

    DGS-WM selects observation units by downstream policy decisions and adjusts world-model auxiliary loss by prediction confidence. Full faithful cost remains unresolved.

- [Divergent Paths: Learning an Outcome-Predictive Representation of LLM Agent Trajectories](https://arxiv.org/html/2610.19614v1) · 2026-10-14 · P1

    Precog-RM learns trajectory representations and predicts outcomes few-shot to stop GRPO early. 47.3% is a relative FLOP saving, not an absolute affordable budget. Official checks left total cost unresolved.

- [PA1-OPD: One-Step Prefix-Augmented On-Policy Distillation for Language Model Pretraining](https://arxiv.org/html/2610.19601v1) · 2026-10-14 · P1

    PA1-OPD adds teacher supervision after one student transition from a corpus prefix, using shared-prefix tree attention rather than offline KD. Original resources exceed single-card budget.

- [INTACT: Inducing Latent Reasoning on a Frozen Backbone](https://arxiv.org/html/2610.19568v1) · 2026-10-14 · P1

    INTACT trains an external latent encoder over a frozen backbone, distilling written reasoning before answer-correctness RL. Few trainable parameters do not imply short training. Original resources exceed budget.

- [$τ$-Emotion-Bench: Exposing the Interaction Fragility of LLM Agents through Real-World User Emotions](https://arxiv.org/html/2610.19560v1) · 2026-10-14 · P1

    τ-Emotion-Bench/Tracer selects demonstrations through interruptible emotional interactions and trains an actual tool-calling policy, not merely relabeled emotions. Original resources exceed budget.

- [Retrieve What Helps, Only When It Helps: Agentic Reinforcement Learning for Selective Retrieval-Augmented Machine Translation](https://arxiv.org/html/2610.19528v1) · 2026-10-14 · P1

    SRAT learns retrieval timing and targets with agentic RL, training a retriever with Plackett–Luce and quality contrast. Original resources exceed budget.

- [Diagnosing and Correcting Reward Hacking in Verifiable Instruction Following](https://arxiv.org/html/2610.19525v1) · 2026-10-14 · P1

    CaLIF adds reward from frozen reference likelihood of the request within a region defined by two offline anchors, limiting hollow constraint satisfaction and likelihood inflation. Original resources exceed budget.

- [ActICL: Post-Training for Agentic Multimodal In-Context Learning](https://arxiv.org/html/2610.19475v1) · 2026-10-14 · P1

    ActICL jointly learns multimodal demonstration acquisition and answering, retaining multi-turn retrieval/filtering and two-stage training. Original resources exceed budget.

- [MIPS: Mitigating Mode Collapse in Reinforcement Learning for Large Outcome Spaces](https://arxiv.org/html/2610.19457v1) · 2026-10-14 · P1

    MIPS uses a learned reverse trajectory model for marginal IPS, not oracle outcome probabilities supplied to the policy. Official checks left full cost unresolved.

- [ForkGRPO: Efficient Exploration and Fine-Grained Credit Assignment for Diffusion Language Models](https://arxiv.org/html/2610.19408v1) · 2026-10-14 · P1

    ForkGRPO branches at high-entropy states and uses continuation groups for within/across-state segment credit. The Fast variant still needs actual rollout training. Original resources exceed budget.

- [Learning What to Keep: Transfer-Aware Personal Skill Learning from User Feedback](https://arxiv.org/html/2610.19380v1) · 2026-10-14 · P1

    SkillGrain jointly optimizes skill induction and conditioned generation with atomic rule transferability, rubric rewards, and fine-grained credit. Original resources exceed budget.

- [Beyond Corrected Actions: Training LLM Agents on Textual Critiques](https://arxiv.org/html/2610.19367v1) · 2026-10-14 · P1

    CAFT generates expert corrections and textual critiques of student errors, actually fine-tunes, and compares RL warm starts. Original resources exceed budget.

- [Where to Start, How to Move: Analyzing Curricula under GRPO for Long-Horizon LLM Agents](https://arxiv.org/html/2610.19349v1) · 2026-10-14 · P1

    Guide-assisted GRPO compares starting points, handoff granularity, and curriculum movement. Successful reference prefixes are training-only, not unassisted evaluation inputs. Original resources exceed budget.

- [DTDD: Divergence-Triggered Dynamic Distillation for Reliable On-Policy Supervision](https://arxiv.org/html/2610.19302v1) · 2026-10-13 · P1

    DTDD triggers teacher takeover by segment disagreement, continuing OPD on student prefixes and cloning teacher suffixes. Original 23 arms took about 22 serial hours and 43M teacher tokens. Not reproduced; review DONE.

- [Verifier-Grounded Agentic RL for Provably Correct Code](https://arxiv.org/html/2610.19298v1) · 2026-10-13 · P1

    Formal-verification RL tracks proof obligations, hidden probes, and prioritized integrity audit with a frozen proof specialist. Unit-test rewards cannot replace formal verification. Original resources exceed budget.

- [Outcome-Routed Distillation and Reinforcement Learning for Diffusion Language Models](https://arxiv.org/html/2610.19271v1) · 2026-10-13 · P1

    Outcome-routed dLLM applies ratio-free REINFORCE to mixed groups and canvas KL when the student fails but the teacher succeeds; anchoring KL preserves ability. Original resources exceed budget.

- [Titan-Llama: Retrofitting Pre-trained LLMs with External Neural Memory Modules](https://arxiv.org/html/2610.19210v1) · 2026-10-13 · P1

    Titan-Llama replaces some attention with test-time updatable neural memory. Keep frozen/adapted layers and real long-context training, not a KV-cache demo. Total cost unresolved.

- [Demystifying On-Policy Distillation: Where Does the Teacher's Advantage Live?](https://arxiv.org/html/2610.19145v1) · 2026-10-13 · P1

    OPD teacher-advantage analysis uses controlled token flips and branched continuations to isolate corrections. Many long continuations per disagreement make full multi-model/branch costs unresolved. No reproduction or automatic rerun; review DONE.

- [Contextual Credit Policy Optimization](https://arxiv.org/html/2610.19103v1) · 2026-10-13 · P1

    CCPO uses context-weighted observation-matched peers and historical/future credit. Appendix reports eight H200s and roughly 19,200 trajectories per run. Too costly; review DONE.

- [GroundGUI: GUI Grounding by High-Quality Data and Distillation-to-Reinforcement Learning](https://arxiv.org/html/2610.19100v1) · 2026-10-13 · P1

    GroundGUI uses actual ScreenRef grounding for SFT, then OPSD→RLOO in D2RL. Point-in-box reward alone cannot replace training. Original resources exceed budget.

- [Backpropagating Verifier Rewards Through Continuous Flow Language Models](https://arxiv.org/html/2610.19080v1) · 2026-10-13 · P1

    Continuous-flow LM uses an intermediate embedding critic to bypass discrete decoding and backpropagate pathwise verifier reward. Keep critic updates alongside policy changes. Original resources exceed budget.

- [Who Should We Listen to More? Welfare-Aware Preference Acquisition for Pluralistic Alignment](https://arxiv.org/html/2610.19035v1) · 2026-10-13 · P1

    WAPA uses an auxiliary reference for individual supervision utility and marginal welfare. Separate label efficiency from full compute; oracle labels provide only an upper bound. Original resources exceed budget.

- [Tev: Scaling Long-Horizon Agentic Environments with Dense Progress Rewards](https://arxiv.org/html/2610.18868v1) · 2026-10-13 · P1

    Tev synthesizes verifiable environments latent-world-first and shapes progress for long-horizon training. Hidden full world specs cannot be read by the evaluated agent. Original resources exceed budget.

- [Hybrid Reasoning Agents](https://arxiv.org/html/2610.18861v1) · 2026-10-13 · P1

    HybridAgent switches between latent reasoning and text tools via HybridLink, keeping HybridSFT/HybridRL and continuous cross-turn memory. Original resources exceed budget.

- [Two Clocks: Why Larger Rollout Batches Learn Slower but Fail on Schedule in Reinforcement Learning with Verifiable Rewards](https://arxiv.org/html/2610.18853v1) · 2026-10-13 · P1

    Two Clocks separates RLVR sampling progress and collapse, testing batch/sqrt-LR scaling and switches. Quadratic toy plots do not replace training. Original resources exceed budget.

- [MFG: Multi-turn Feedback Guided Molecular Optimization](https://arxiv.org/html/2610.18851v1) · 2026-10-13 · P1

    MFG learns molecular optimization from cross-turn property/similarity feedback and aligned rewards. A fixed scorer cannot simulate learning. Original resources exceed budget.

- [SkillScaffold: Scaffolding Agentic Reinforcement Learning with Policy-Adaptive Skill Credit Assignment and Selective Injection](https://arxiv.org/html/2610.18807v1) · 2026-10-13 · P1

    SkillScaffold uses verified trajectory outcome likelihood for skill utility, selection, and abstention, jointly training Generator/Executor. Evaluated agents cannot read gold successful traces. Full cost unresolved.

- [Rubrics from the Task, Verdicts from Evidence: Pointwise Rubric Rewards with Tool-Augmented Judges](https://arxiv.org/html/2610.18766v1) · 2026-10-13 · P1

    ReVeR uses instruction-only rubrics and a tool-augmented pointwise judge for label-blind distillation. Labels filter teacher outputs only. Original resources exceed budget.

- [PreciseCoder: Faithful and Generalizable Debugging Beyond Unit-Test Rewards](https://arxiv.org/html/2610.18755v1) · 2026-10-13 · P1

    PreciseCoder adds semantic local-edit credit to unit-test rewards and measures repository transfer. Fewer diff lines are not correctness. Original resources exceed budget.

- [Enabling Token-wise Importance Sampling in Off-Policy RLVR with Proximal KL Regularization](https://arxiv.org/html/2610.18738v1) · 2026-10-13 · P1

    Proximal KL separates reference and behavior policy and replaces clipping with token-wise IS and future-KL credit. Tabular coverage/expressiveness guarantees do not carry over automatically to Transformers. Full cost unresolved.

- [A Refresh Interval Does Not Fully Specify a Refresh Schedule: Learning-Rate-Dependent Placement in Kronecker-Preconditioned Language Model Training](https://arxiv.org/html/2610.18695v1) · 2026-10-13 · P1

    Kronecker refresh placement studies LR-dependent ranking reversals at a fixed number of refreshes. A single numerical check is not cross-LR training evidence. Original resources exceed budget.

- [ProAS: A Progress-Aware Advantage Shaping Framework for Multi-Turn Agentic Reinforcement Learning](https://arxiv.org/html/2610.18683v1) · 2026-10-13 · P1

    ProAS uses a dynamic Agentic Reference Graph to mask invalid positive credit and redistribute negative credit asymmetrically. Gold plans cannot replace ARG decisions. Original resources exceed budget.

- [MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization](https://arxiv.org/html/2610.18642v1) · 2026-10-13 · P1

    MultiAlloc profiles layer sensitivity and token importance offline, then jointly allocates fidelity under a fixed KV budget. Full cost unresolved.

- [Can an Agent Learn to Predict Its Own Failure? Outcome-Grounded Confidence Calibration in LLM Agents](https://arxiv.org/html/2610.18614v1) · 2026-10-13 · P1

    Outcome-grounded confidence trains per-step confidence against eventual episode outcomes with proper scoring, separating difficulty, depth, and attempt foresight. Original resources exceed budget.

- [Does self-distillation improve reasoning?](https://arxiv.org/html/2610.18613v1) · 2026-10-13 · P1

    The self-distillation reasoning review separates OOD generalization, thinking-mode transfer, and gradient alignment. Retain negatives rather than relabel as general improvement. Original resources exceed budget.

- [LLM Agents for Automated Post-Training via Structured Recipe Optimization](https://arxiv.org/html/2610.18572v1) · 2026-10-13 · P1

    SRO's Recipe-Space Designer defines composable choices, then searches post-training recipes with structured trial evidence and multi-objective BO. Original resources exceed budget.

- [Imprinting: Knowledge Distillation Can Shift Student Behavior](https://arxiv.org/html/2610.18517v1) · 2026-10-13 · P1

    Imprinting studies teacher safety transfer through ordinary task distillation, comparing divergence-token masks/rewrites and later preference tuning. It is a multi-teacher/student causal comparison, not one loss check. Full cost unresolved.

- [How Low Can You Go: Fine-Tuning LLMs with Bayesian Optimization (LlMBO)](https://arxiv.org/html/2610.18504v1) · 2026-10-13 · P1

    LlMBO uses Gaussian-process BO over low-dimensional TinyLoRA and directly optimizes greedy accuracy. Few parameters still require many LLM generations. Original resources exceed budget.

- [ReTerm: Recovery Training for Self-Improving Terminal Agents](https://arxiv.org/html/2610.18484v1) · 2026-10-13 · P1

    ReTerm starts with recovery SFT, then forks own failure states into recovery rollouts for ReTerm-GRPO. Original resources exceed budget.

- [Teacher-Guided Tool Learning for Small Language Models via Bidirectional KL Constraints](https://arxiv.org/html/2610.18459v1) · 2026-10-13 · P1

    SeTPO pairs reverse-KL advantages on low-reward trajectories with continual forward-KL demonstrations. A 0.5B fit on one GPU does not price full controls. Full cost unresolved.

- [Copying Is Not Grounding: Training Faithful Long-Form RAG with Authored-Sentence Credit](https://arxiv.org/html/2610.18442v1) · 2026-10-13 · P1

    ASC moves faithfulness reward/advantage to authored sentences, excluding copied or empty text and comparing sentences from the same query. Original resources exceed budget.

- [Teach Me After You Learn It: Lookahead Self-Distillation for RLVR](https://arxiv.org/html/2610.18256v1) · 2026-10-13 · P1

    LEAD uses disjoint on-policy groups for virtual RL lookahead teachers, cross-group token distillation, and GRPO signal reconciliation. Original resources exceed budget.

- [TextualRL: Textual Reinforcement Learning for Context Management](https://arxiv.org/html/2610.18216v1) · 2026-10-13 · P1

    TextualRL critiques groups of same-task rollouts and checks bounded context patches across groups; held-out validation decides adoption. No gold-script substitute. Full cost unresolved.

- [A Few More Tokens Ahead: Reinforcing Parallelism in Diffusion LLMs](https://arxiv.org/html/2610.18200v1) · 2026-10-13 · P1

    RePara strengthens dLLM parallel generation with group-relative updates on contiguous short token blocks. Changing decode quota is not RL. Original resources exceed budget.

- [Failure Recovery via Belief Updates and World Modeling for Long-Horizon Agents](https://arxiv.org/html/2610.18082v1) · 2026-10-13 · P1

    BELIEFWEAVER uses relational beliefs and an IWM to predict repair across attempts and distills via SFT/OPD into a 9B student, not simple backtracking. Full cost unresolved.

- [WorkRover: Scaling Long-Horizon Cowork Agent Training Via Recursive Environment Evolution](https://arxiv.org/html/2610.18067v1) · 2026-10-13 · P1

    WorkRover selects minimal validated environment revisions using dependency-closed factorial replay and applies VTCA to real workspace progress. Static registry names are not executable evolution. Full cost unresolved.

- [Correcting or Continuing? What On-Policy Distillation Learns from Student Errors](https://arxiv.org/html/2610.18011v1) · 2026-10-13 · P1

    Error-focused OPD compares five mechanisms, eight configurations, and a non-failure-focused positive control. Preserve lower accuracy despite decreasing KL; diagnostics are not gains. Full cost unresolved.

- [Fish Audio Drama 3 Technical Report](https://arxiv.org/html/2610.18010v2) · 2026-10-13 · P1

    Fish Audio Drama 3 v2 reports three stages for a 35B-A3B speech generator: pretraining, SFT, and preference RL. Single-H200 inference does not imply single-card training. Original resources exceed budget.

- [Agent-Reflex: Teaching Language Agents to Act Reflectively](https://arxiv.org/html/2610.17953v1) · 2026-10-13 · P1

    Agent-Reflex uses noise-grounded skill discovery, ReSFT, and reflection-guided on-policy RL. Prompt templates cannot substitute. Full cost unresolved.

- [PaceReasoner: Label-Free Learning to Answer Briefly from Long Reasoning](https://arxiv.org/html/2610.17900v1) · 2026-10-13 · P1

    PaceReasoner uses LONG consensus to supervise SHORT with behavior reward and a ratio controller. Label-free still incurs generation; separate adaptation/test. Original resources exceed budget.

- [Training LLMs for Multi-Agent Collaboration with Verifiable Information Rewards](https://arxiv.org/html/2610.17893v1) · 2026-10-13 · P1

    CoSIR rewards disclosure, requests, and information use by reduced Bayesian team surprisal, transferring cooperation through self-play post-training. Evaluators may know the correct option, agents cannot. Original resources exceed budget.

- [Efficiently Learning To Reason or Not to Reason: Root-token Policy Optimization for Adaptive Thinking](https://arxiv.org/html/2610.17767v1) · 2026-10-13 · P1

    RPO trains only the think/no-think root token but needs real long trajectories from both modes for group-relative advantages. A hand-built difficulty gate is not a reproduction. Original resources exceed budget.

- [Explore with Memory, Learn without It: In-Context Exploration and Self-Distillation for LLM Reasoning](https://arxiv.org/html/2610.17734v1) · 2026-10-13 · P1

    LEAF uses dynamic problem-specific memory for exploration and self-distills to a memory-free policy. Keep memory and validation/test boundaries. Original resources exceed budget.

- [CoCA: Criterion-Aware Credit Assignment for Rubric-Based Reinforcement Learning](https://arxiv.org/html/2610.17733v1) · 2026-10-13 · P1

    CoCA constructs criterion-group relative outcome credit and assigns tokens through criterion-induced distribution shifts, not direct privileged-teacher imitation. Original resources exceed budget.

- [TSRL: Trigger-based Supervised Reinforcement Learning for Continual Agent Training](https://arxiv.org/html/2610.17726v1) · 2026-10-13 · P1

    TSRL triggers SFT on failed hard states during RL and studies continual forgetting. Gold successful paths do not replace expert supervision. Original resources exceed budget.

- [DeltaTTG: Training Multi-Turn Agents with a Token-to-Go Progress Meter](https://arxiv.org/html/2610.17666v1) · 2026-10-13 · P1

    DeltaTTG trains a progress meter on real multi-policy successes, then freezes it to redistribute outcome advantage. Remaining gold plan length cannot replace the meter. Original resources exceed budget.

- [Decouple to Forget: Semantic Mediation for Sensitive Unlearning in Large Language Models](https://arxiv.org/html/2610.17654v1) · 2026-10-13 · P1

    D2F decomposes sensitive fact mediators, generates counterfactuals preserving nonsensitive content, and preference-unlearns. A single 40GB A100 and two epochs fit, but GPT-4o construction/audit and two benchmarks still count. Full cost unresolved.

- [RELAY: Selective Self-Distillation with Adaptive Hand-off for Rubric-Based Reinforcement Learning](https://arxiv.org/html/2610.17623v2) · 2026-10-13 · P1

    RELAY v2 selects positive or low/zero-advantage trajectories for distillation and stops the teacher at a plateau while continuing GRPO. Reviewed v2, not v1. Original resources exceed budget.

</details>

<details markdown="1"><summary>Agent and RSI: 76</summary>

- [Player-1: Learning to Play from Synthetic Experience](https://arxiv.org/html/2610.20584v1) · 2026-10-14 · P1

    Player-1 requires SFT and multi-environment PPO. Official Appendix D.3 specifies about 24h on 32 H200s per SFT model and 36h on 64 H200s for RL, plus 512 concurrent environments. Too costly.

- [Latent Compaction with Test-Time Training](https://arxiv.org/html/2610.20582v1) · 2026-10-14 · P1

    Latent Compaction freezes the model but fits attention and distills caches per document, not training-free compression. Suggested 1,000 updates in each of two stages and 20 documents per RULER task-length. Total preparation and multi-model evaluation cannot be costed cheaply within one card.

- [Beyond LLM Judge: Mechanical Verification for Agentic Autoformalization](https://arxiv.org/html/2610.20573v1) · 2026-10-14 · P1

    The verifier combines LLM semantic review with numerical/vacuity checks. Free vacuity checks alone are incomplete. Appendix F reports 1,539 numerical checks costing about \$314.18 in total and taking 77s per item, plus about \$99.57 back-translation. Full combined study is expensive.

- [Scaling Discovery Requires Forgetting](https://arxiv.org/pdf/2610.20563v1) · 2026-10-14 · P1

    Forgetting clears search sessions/history while retaining the best candidate. The study uses multiple agents, four executable research tasks, 30 continuation proposals, and replicates. PDF costs/figures cover continued search; a constant cache-reset fixture does not reproduce discovery.

- [PhySGA: A Physics-Space Grounded Agentic Framework for Generalizable and Interactive 3D Composition](https://arxiv.org/html/2610.20560v1) · 2026-10-14 · P1

    PhySGA needs Assembly/Critic, physical primitives, skill feedback, and Isaac Sim assets. §4.1 uses GPT-5.5 and Isaac Sim 4.2.0 on 120 prompts. Hardware, asset preparation, and repeated closed-loop cost unresolved.

- [From Relevance to Validity: Zero-Shot Tool Selection via Functional and Contextual Validation](https://arxiv.org/html/2610.20388v1) · 2026-10-14 · P1

    Tool transfer-validity needs representation extraction, training, capability ranking, and actual backbones/judges in cached tool environments. Appendix I.4 uses three 95GB cards, three seeds, and separate remote models. Single-card total unresolved.

- [Reflect After Failure: Brain-Inspired Self-Evolving Agents for Embodied Spatial Intelligence](https://arxiv.org/html/2610.20312v1) · 2026-10-14 · P1

    HiMeco combines PEP, a strategy bank, and executable skills. Eight A6000s/API and 208 fixed episodes account for 1,664 planned executions. Separate four-round adaptation within one episode from independent transfer. A diagnostic may read a reference snapshot; online agents and held-out improvement cannot.

- [P2Patch: Exploit-Guided Vulnerability Repair](https://arxiv.org/html/2610.20245v1) · 2026-10-14 · P1

    P2Patch generates an independent exploit after each repair and accumulates PoV, isolating construction from held-out oracles. 101 real CVEs, multiple attack/repair models, and increased end-to-end cost exceed affordable scope.

- [SWE-Stream: Scaling Executable Training Data for SWE Agents via Progressive Construction and Elastic Streaming](https://arxiv.org/html/2610.20193v1) · 2026-10-14 · P1

    SWE-Stream progressively constructs tasks and streams them while actually rebuilding and validating repositories. 80,874 tasks, 118,688 trajectories, and 30B training. Even the 500-task scheduler control took 23.06h; full study too costly.

- [Why Generate a Click? Plug-in Decision Heads for Web Agents](https://arxiv.org/html/2610.20107v1) · 2026-10-14 · P1

    Plug-in heads require a 4B/8B generator trained on 213K web steps before head and cascade training. Not a small linear-layer add-on. Appendix B uses two GPUs and 96GB cards, with about 11 hours for 4B joint training.

- [EvalBuilder: Can LLMs Build Efficient Benchmarks?](https://arxiv.org/html/2610.20099v1) · 2026-10-14 · P1

    EvalBuilder generates and iterates benchmark proxies with held-out ranking, not just a scorer. Appendix B.1 reports 4h33m, 7h9m, and 13h7m, with a 16h cap. Too costly.

- [Memorizing Who, Knowing How: Benchmarking Personal and Procedural Memory for Persistent Assistants](https://arxiv.org/html/2610.20022v1) · 2026-10-14 · P1

    PraxisMem jointly manages personal and procedural memory with privileged joint-state supervision, location-aware GRPO, and OPSD. Gold-state fixtures cannot replace a deployable manager. Training and 20 long trajectories are not affordably costed.

- [A Strong Harness Narrows the Model Gap: A Comparative Evaluation for Legislative Document-to-XML Conversion](https://arxiv.org/html/2610.19999v1) · 2026-10-14 · P1

    Legislative XML requires real tools, persisted state, and citation authority lookup, not document splitting. The paper did not log tokens, latency, or costs; 153 bills × three harnesses × three models cannot be priced from artifacts. No exploratory run.

- [AtomSearch: Evidence-Grounded Tree Search for Agent Skill Optimization](https://arxiv.org/html/2610.19951v1) · 2026-10-14 · P1

    AtomSearch performs skill-state tree search over evidence-backed atomic edits with regression/repair memory. Roughly 923–17,200 item evaluations per experiment across multiple targets make full search expensive. Review DONE.

- [Explorer-Zero: Improving Self-Play for Long-Horizon Tasks with Decomposable Verifiable Rewards](https://arxiv.org/html/2610.19868v1) · 2026-10-14 · P1

    Explorer-Zero alternates proposer/solver self-play and saves environment checkpoints for reward. Appendix D uses eight H100s and about 15 node-hours per ALFWorld run, 29 for AppWorld. A reward function or fixture is not self-play.

- [Euler: Towards Human-Centered Multi-Agent Mathematical Discovery](https://arxiv.org/html/2610.19864v1) · 2026-10-14 · P1

    Euler uses research graphs, saved team state, and budget reservations for long math investigations. Three cases do not prove affordability. Resource accounting was checked; frontier calls, proof tools, and prolonged continuation remain unpriced.

- [DeltaStreamer: Towards Human-Like Agentic Streaming Video Understanding](https://arxiv.org/html/2610.19849v1) · 2026-10-14 · P1

    DeltaStreamer's change-aware memory, planning, and video replay all require a 27B multimodal model. §4.1 uses eight A100s, BF16, and 1fps. Text summaries cannot replace video observation/replay.

- [LAGO: Language Agents with Reusable Growing Options](https://arxiv.org/html/2610.19843v1) · 2026-10-14 · P1

    LAGO's meta-agent and option library need real decomposition, tool execution, and verification. A 35B-A3B model, 500 SWE tasks, and a 150-task rerun cost substantially. No preset options or gold decomposition substitute.

- [EGCForest: Structured Agent Memory Organization for Enterprise Group Chats](https://arxiv.org/html/2610.19836v1) · 2026-10-14 · P1

    EGCForest needs three forests, Placement Map, structured bridges, summary construction, and embeddings. 206MB/65ms covers storage/online retrieval, not offline construction and answering across three benchmarks. A 0.6B encoder does not bound LLM construction cost.

- [ActionOPD: Distilling Decisions, Not Tokens](https://arxiv.org/html/2610.19820v1) · 2026-10-14 · P1

    ActionOPD samples teacher/student actions on student-visited states and optimizes policy from semantic agreement, not offline imitation. 4B/8B, multiple teachers, four candidates per state, and closed-loop tools remain unpriced.

- [Evolve Together, Fall into Place: How Social Scaffolding Shapes Self-Evolving Multi-Agent Systems](https://arxiv.org/html/2610.19799v1) · 2026-10-14 · P1

    AGORA studies scaffolding in evolving teams using eight 96GB RTX PRO 6000s, 900-second sessions, and repeats. Full evolution and controls are too costly; static role labels are not an implementation.

- [StateCraft: Augmenting Video World Models with Abstract-State Reasoning](https://arxiv.org/html/2610.19795v1) · 2026-10-14 · P1

    StateCraft jointly trains persistent abstract states and video diffusion. Each of two backends uses about 400 H200 GPU-hours; roughly 2,000 trajectories × 300 actions. Full pipeline exceeds budget.

- [PRISMATIC : Prescription Risk Inspection System for Multi-Agent Treatment Interaction in Clinical Decision-Making](https://arxiv.org/html/2610.19762v1) · 2026-10-14 · P1

    PRISMATIC's DSWA/DFPC need multi-specialty agents iterating and updating across cases. MIMIC-IV cases/prescriptions and blackboard checked; restricted records, repeated LLM calls, and medical review remain unpriced. No probe or gold-prescription agent input.

- [New Model, Old Habits: Behavior Transfer under Model Swapping in Multi-Session LLM Agents](https://arxiv.org/html/2610.19712v1) · 2026-10-14 · P1

    DASH selects raw history or summaries by exchange direction and original author, requiring repeated model swaps on real multi-session tasks. Checked setup and limitations; closed loops, visibility of raw reasoning, and full model matrix unpriced.

- [C3: Rethinking Process Supervision via Confidence-Guided Credit Correction in Multi-Turn Reinforcement Learning](https://arxiv.org/html/2610.19695v1) · 2026-10-14 · P1

    C3 adjusts positive credit for bad spans by confidence after RL advantage estimation; actual RL is required. Qwen3-8B search, full-parameter 4B WebShop, critic/critic-free arms, and retrieval make cost high or unresolved.

- [MCAIR: Monitoring and Correcting Agent Unfaithfulness via Internal Representations](https://arxiv.org/html/2610.19679v1) · 2026-10-14 · P1

    MCAIR's CPU probe under 0.2ms assumes pre-extracted hidden states. The paper uses 8B/12B/14B, two RTX A6000s, layer sweeps, and three correction experiments. Sampling and representation extraction remain expensive or unpriced.

- [JevCoder: When Does Decision Delegation Pay Off in Code Repair?](https://arxiv.org/html/2610.19596v1) · 2026-10-14 · P1

    JevCoder's low-price judge does not make the repair agent cheap. Compute section reports two L40S cards, about 200 GPU-hours, and \$1500 API cost. Full work exceeds budget.

- [L3M: A Verifiable Harness and Runtime for Self-Extending and Self-Improving Agents](https://arxiv.org/html/2610.19591v1) · 2026-10-14 · P1

    L3M runtime includes Git state traces, narrowed capabilities, and Lean kernel verification. No fully reusable upstream implementation was established, and Terminal-Bench total calls are unresolved. Not reproduced, review DONE; a Python state machine is not a Lean proof.

- [XferAgent: Cross-Agent Experience Transfer for Self-Improving LLM Agents](https://arxiv.org/html/2610.19581v1) · 2026-10-14 · P1

    XferAgent routes experience from local/shared graphs before execution and updates from results, not static shared prompts. Four domains, heterogeneous frameworks, multi-pass construction, and regressions remain unpriced.

- [Mission (Im)Possible: Towards Autonomous Discovery of Autopilot Logic Flaws in Open-Source Drone Frameworks](https://arxiv.org/pdf/2610.19566v1) · 2026-10-14 · P1

    IMF needs three-agent static slicing, real simulation, and log-oracle validation. 105 new PX4/Ardupilot findings are not a cheap single-script rerun. Official examples checked; build/simulation/frontier budget unresolved.

- [MemCode: Discrete Semantic Representations for Long-Term Agent Memory](https://arxiv.org/html/2610.19472v1) · 2026-10-14 · P1

    MemCode's cheap retrieval cannot omit ISQ learning. Appendix B: 64,935 DailyDialog pairs, T5-base VQ-VAE, ten epochs, 32GB GPU and 90GB RAM. Offline training and LLM atomic writing remain costly or unpriced.

- [PFedMA: Who Should Join Next as Federated Multi-Agent Orchestration Evolves?](https://arxiv.org/html/2610.19458v1) · 2026-10-14 · P1

    PFedMA trains the orchestrator with PPO and evolves privacy rules in both directions across clients, not only agent scoring. Appendix E.3 uses batch 64 and up to 220 steps. Closed-loop client/security cost unresolved.

- [EvoProbe: Evaluation-Driven Benchmark Evolution for LLM Agents](https://arxiv.org/html/2610.19433v1) · 2026-10-14 · P1

    EvoProbe needs task generation, executable subtask validation, multiple judges, and regeneration. 66 cybersecurity tasks, eight models, two rounds, and human quality review leave cost and infrastructure unresolved.

- [VideoHarness-SRSI: Structured Recursive Self-Improvement for Video Understanding Harness](https://arxiv.org/html/2610.19424v1) · 2026-10-14 · P1

    VideoHarness-SRSI requires content-free feedback, probe racing, factorial combinations, and independent validation. More than 4,000 evolved candidates, four video benchmarks, and three seeds make complete search costly.

- [Beyond the Trial-and-Error Loop: Hybrid Projection and Automated Tuning for Distributed Training](https://arxiv.org/html/2610.19423v1) · 2026-10-14 · P1

    Primus Projection has CPU simulation, but claimed tuning gains require GPU microbenchmark calibration and multinode verification. 671B/1,024 GPUs and 235B/256 GPUs exceed budget. Uncalibrated CPU simulation is not throughput or agent-tuning reproduction.

- [AgentSafeEvo: Adversarial Co-Evolution for LLM Agent Safety](https://arxiv.org/html/2610.19422v1) · 2026-10-14 · P1

    AgentSafeEvo requires attacker/defender RL co-evolution and learnability weighting. Appendix D.1 uses four GPUs per role, 120 steps, batch 64, and 16K response; too costly.

- [From Failures to Learnable Worlds: Policy-Conditioned Environment Generation for Navigation Agents](https://arxiv.org/html/2610.19420v1) · 2026-10-14 · P1

    WEDGE derives and verifies weaknesses from failure contrasts, then generates navigation worlds and trains. §4.4 needs about 21K policy rollouts for 4.2K candidates; ten weakness-discovery LLM calls do not price it.

- [SERO: Learning from Executable Oracle Continuations for Long-Horizon Agentic Reinforcement Learning](https://arxiv.org/html/2610.19397v1) · 2026-10-14 · P1

    SERO needs executable oracle continuations, state restore, and policy-reachability weights; oracles are training-only. Appendix E.1 uses 16×8 rollouts per batch, 50-step horizon, 1.5B/7B, and several optimizers. Full cost high or unpriced.

- [STRATA: Self-Maintaining Structured Experience Graphs for Self-Evolving Language Agents](https://arxiv.org/html/2610.19386v1) · 2026-10-14 · P1

    STRATA's typed graph, reflector, community induction, GC, and contrast edges need real online tasks. Four benchmarks, two backbones, seven controls, three seeds, and 812 WebArena tasks are costly.

- [EvoWeave: Composing Reusable Agent Experience through Operation Level Graphs](https://arxiv.org/html/2610.19381v1) · 2026-10-14 · P1

    EvoWeave requires operation contracts, directed connections, and post-execution reflection, not graph registration. Four benchmarks, five settings, and three backbones; Appendix F cannot aggregate cost categories into a total, so budget remains unresolved.

- [DeLoop: Repeated Actions as Self-Supervision for Long-Horizon Agents](https://arxiv.org/html/2610.19376v1) · 2026-10-14 · P1

    DeLoop mines repeat actions as negatives and first later non-loop actions as positives from real rollouts, then runs DPO. No gold substitution. 8B/14B/32B, thousands of episodes, and cross-environment training/sampling are costly or unpriced.

- [Policy-Verified Self-Training: Learning Agent Compliance from Verifiable Policy Rewards](https://arxiv.org/html/2610.19372v1) · 2026-10-14 · P1

    PVST converts deterministic policy gates into RFT/DPO supervision. Verifier scope depends on attack goals and some bindings are weaker than original clauses. 8B/4B multi-arm training and closed-loop AgentDojo costs remain unclear; a compiled gate is not training capability.

- [MemeTrace: A Multimodal LLM-Based Agent for Safety-Aware Meme Provenance Analysis](https://arxiv.org/html/2610.19267v1) · 2026-10-13 · P1

    MemeTrace averages 18.46 steps, 11.54 multimodal calls, and 3.92 searches per meme; about \$0.1259 and 111 seconds. The 100-example main set alone is roughly 3.1 serial hours from paper averages, not local measurement. Multi-model, ablation, and robustness runs add cost.

- [ChunkAct: Action Chunking for Agentic Robotics](https://arxiv.org/html/2610.18874v1) · 2026-10-13 · P1

    ChunkAct must run VLA, segmentation, and replanning after failure exits. The paper uses multiple LIBERO-Pro suites, GPT-5.6-sol high, and up to 100 calls per episode. Total VLA/simulation costs unresolved; fixed action chunks do not demonstrate robotics.

- [SEAR: Self-Evolving Agentic Robotics](https://arxiv.org/html/2610.18792v1) · 2026-10-13 · P1

    SEAR separates experience retention from retries, privileged state, and budgets. 330 simulated and five physical tasks, over four cumulative agent-runtime years, and hours of practice/AR exceed budget.

- [Beyond the Verdict: Agentic Code Judging with Verifiable Feedback](https://arxiv.org/html/2610.18760v1) · 2026-10-13 · P1

    ARBITER uses RL to teach a 35B MoE verifier to generate executable counterexamples. Average per candidate is 35.0K–46.9K output tokens. Training and iterative refinement are costly; paper failures and judge labels cannot replace generation.

- [Kwai Summary Attention V2 Technical Report](https://arxiv.org/html/2610.18654v1) · 2026-10-13 · P1

    KSA V2 combines Summary→Meta KV compression with summary-guided sparse indexing over original chunks. Staged training uses 1.9B/4B, 128K context, and billions of tokens. Too costly; review DONE.

- [Knowledge Graphs as Files: An Agent Harness Where Tool Creation and Tool Use Co-Evolve](https://arxiv.org/html/2610.18616v1) · 2026-10-13 · P1

    DKGI exposes full KGs as files and co-evolves tools and usage. Three graphs and frontier models, up to 300 turns/1,800s per run plus repeats, are costly. Review DONE; verified author repository leopoldwhite/DKGI.

- [The Last Mile of Coding Agents for Long-Document Tasks: An Empirical Study on Clinical Trial Protocol Digitization](https://arxiv.org/html/2610.18507v1) · 2026-10-13 · P1

    TrialScribe uses domain skills and verification for protocol PDF digitization. Gold fields cannot replace 27B inference and real tool execution. §4.2 uses two A100s, 150 long protocols, and multiple models/metrics; exceeds single-card budget.

- [Judges Follow the Reference: The Derivation Gap in Verifying Tool-Call Arguments](https://arxiv.org/html/2610.18497v1) · 2026-10-13 · P1

    DeRef uses an independent deriver that never sees the candidate to generate references from full history, rather than feeding gold to judges. A 27B deriver, large benchmarks, long histories, and seconds per reference make full multi-judge/settings expensive.

- [MemoryVLN: From Ego-Aware Memory Representation to Cross-Context Memory Reuse in Vision-Language Navigation](https://arxiv.org/html/2610.18478v1) · 2026-10-13 · P1

    MemoryVLN needs actual VLN training for compression, ego-aware multimodal features, hierarchical memory, and write-back. Appendix A.3 uses 64 GPUs at global batch 64 plus VGGT/Habitat; too costly.

- [Reliable Memory from Unstable Growth: Curating Self-Written Agent Playbooks with Randomized Experiments](https://arxiv.org/html/2610.18427v1) · 2026-10-13 · P1

    RBC estimates lesson effects with randomized block inclusion and fresh practice to select curated/full/no playbook, with isolated test. Nineteen settings, three growth runs and three evaluation seeds each, hundreds to thousands of episodes per score: too costly.

- [Delegating Earth science model calibration to knowledge-guided LLM agents](https://arxiv.org/pdf/2610.18378v1) · 2026-10-13 · P1

    GCH freezes agent declarations for deterministic numerical search. Six-model calibration takes 80–600 evaluations and three seeds, not just writing config. Official PDF Table B3/Appendix C checked; model, knowledge infrastructure, and full search costs unresolved.

- [Urbex: Agentic Spatial Grounding for City-Scale 3D Scenes](https://arxiv.org/html/2610.18356v1) · 2026-10-13 · P1

    Urbex active spatial search requires rendering, tool interaction, and RL. Hardware section reports 16 H20s for training; about 3.2s/query on one H20 is inference only, excluding offline scene preprocessing.

- [Beyond Answer Sharing: TrueMAD for Targeted Peer Engagement in Multi-Agent Debate](https://arxiv.org/html/2610.18240v1) · 2026-10-13 · P1

    TrueMAD targeted advice must come from real peers, not gold critiques. Main setup uses 30B-A3B, multiple agents and rounds, and three reasoning benchmarks. Full arms remain unpriced.

- [The Agentic Scientist: Orchestrating Coding Agents for Automated Scientific (Co-)Discovery](https://arxiv.org/html/2610.18933v1) · 2026-10-13 · P1

    The Agentic Scientist is end-to-end research orchestration and verification, not just multi-agent dialogue. Appendix settings include 20–60 ideation cycles, up to three hours per candidate, 250 epochs, and up to 1B environment steps.

- [APT: Feedback-Driven Agentic Post-Training for Text-to-Image Generation](https://arxiv.org/html/2610.18097v1) · 2026-10-13 · P1

    APT agents generate evaluations, diagnoses, and training distributions, then actually update image generators with RL. Multiple base generators, benchmarks, and generation/training cycles are high cost or unresolved. Prompt selection alone is not reproduction.

- [AReaL-RSI: Adaptive Scaling and Coordination of Recursive Self-Improvement](https://arxiv.org/html/2610.18083v1) · 2026-10-13 · P1

    AReaL-RSI needs a leader, conditional memory sharing, and post-campaign evidence review. KernelBench gives one hour per researcher, RSIBench two hours, plus four-agent controls and multiple tasks/backbones; expensive.

- [Cost-Efficient Privacy Enforcement for Email-Generating LLM Agents under Strategic Information Requests](https://arxiv.org/html/2610.18007v1) · 2026-10-13 · P1

    The method needs actual Gemma contract-conditioned rewriting and PrivacyChecker. Remote-token savings do not establish total compute reduction. Defender objective and §5.1 checked; local overhead and full multi-policy email costs unresolved.

- [Learning How to Remember: Memory Modality Selection for GUI Agents](https://arxiv.org/html/2610.17928v1) · 2026-10-13 · P1

    SwitchMem compares text and image for the same retrieved demonstration and learns a step router. Preserve real VLM hidden-state probes and both memories. 9B actor, three GUI benchmarks, paired annotation/training, and later loops remain costly or unpriced.

- [Interaction-as-a-Judge](https://arxiv.org/html/2610.17895v2) · 2026-10-13 · P1

    Interaction-as-a-Judge requires real computer interaction to evaluate and repair apps, and training rewards need interaction traces. v2 Appendix G uses Qwen3.5-9B, 384 prompts × eight samples = 3,072 traces per batch. Full inference and RL too costly.

- [ECMR: Evidence-Aware Deliberation Control for Multi-Agent LLM Reasoning](https://arxiv.org/html/2610.17869v1) · 2026-10-13 · P1

    ECMR's state-conditioned controller requires support independence, contradiction, verification, and a role/action loop. 9,000 held-out records and multi-policy/domain runs are costly with unresolved total resources. Gold-state replay and normalized audit costs are not actual dollars/time.

- [State-Aware Generation of Deployable Websites from Visual Prototypes and Requirements](https://arxiv.org/html/2610.17861v1) · 2026-10-13 · P1

    VisStateCoder needs prototype grounding, graph-guided generation, render evidence, and scoped updates, not a static Project State Graph. Official §4.4: five models, up to 16,384 output tokens per call, at most four rounds; controls 7,200s/task. Full website generation/deployment costly and unresolved.

- [Socratic Skill Learning: Interleaving Teaching and Practice for Transferable Agent Skills](https://arxiv.org/html/2610.17860v1) · 2026-10-13 · P1

    SSL alternates Educator and Student coaching, with only Student acting, and verifies transferable skills. 35 families/408 cases, main 22/155, 66 runs per schedule and multiple model pairs make acquisition costly.

- [Agentic-MatriBO: Capability-Compiled Agentic Bayesian Optimization for Materials and Chemical Design](https://arxiv.org/html/2610.17832v1) · 2026-10-13 · P1

    Agentic-MatriBO retains capability compilation, evidence gating, and oracle access only after submission. No advance gold-pool scan. Four pools × five seeds × multiple baselines/agent calls leave full dependencies and costs unresolved.

- [Agentic4PDM: Host-Governed Evidence Admissibility for Industrial Fault Diagnosis](https://arxiv.org/html/2610.17786v1) · 2026-10-13 · P1

    Agentic4PDM host governance does not eliminate retrieval or inference. Appendix F complex investigations and DTW controls exceed 1,000s per sample. Pretrained representations, class references, and real industrial data still required; total unresolved.

- [Beyond Belief Nesting: Rethinking Higher-Order Theory of Mind in Large Language Models](https://arxiv.org/html/2610.17777v1) · 2026-10-13 · P1

    HopTrace encodes perspective once and answers multilevel ToM deterministically; gold belief graphs cannot substitute. Full comparisons use 100 narratives/500 main questions, other benchmarks, multiple models, 4–217s/story and four A800s for larger open models. Faithful total cost unresolved.

- [Coupled Harness--Model Evolution for Scientific Equation Discovery](https://arxiv.org/html/2610.17740v1) · 2026-10-13 · P1

    Coupled Harness–Model Evolution evolves executable tools and LoRA-trains a Qwen controller on successful GPT-5.5 traces, not library registration. Full tool search, teacher trajectories, and student training remain unpriced.

- [SkillScreen: High-Recall Screening of Malicious Agent Skills with Decision Models](https://arxiv.org/html/2610.17727v2) · 2026-10-13 · P1

    SkillScreen uses a 2B decision model's NLI scores with validation-frozen 99% recall threshold. Preserve higher false positives on unseen benign sources and SKILL.md-only scope. v2 reports 3.4–3.9 hours per single epoch on 10GB H100 MIG, before splits/seeds. Too costly; review DONE.

- [Evidence-First Agentic Verification](https://arxiv.org/html/2610.17724v1) · 2026-10-13 · P1

    Sauron bounded queries and faithfulness checks reduce relative costs, not entire evaluation cost. One Sol configuration on 100 episodes costs \$297.69 and TRAIL \$841, before multiple backbones, fault injections, and ablations. Too costly.

- [Adaptive-Group Process Rewards for GUI Agents](https://arxiv.org/html/2610.17710v1) · 2026-10-13 · P1

    Adaptive-Group process reward uses VLM scoring by action/subgoal group and actual GUI-agent GRPO. Two process-reward benchmarks and three OSWorld application groups leave total scoring/rollout/training costs materially uncertain.

- [RALI@iKAT 2026: Retrieval-aware User Profile Denoising via Personalized Conversational Dense Retrieval](https://arxiv.org/html/2610.17673v1) · 2026-10-13 · P1

    PCDR trains a conversation retriever before joint user-profile projection. Base conv-Qwen3 uses four GPUs, batch 480, 20 epochs, and cross-GPU negatives. Fixed embeddings cannot replace denoising learning.

- [Cowork-Gym: Synthesizing Interactive Work Environments at Scale](https://arxiv.org/html/2610.17670v1) · 2026-10-13 · P1

    Cowork-Gym needs build–execute–revise environments and SFT/RL/OPD. 64.9K environments, 14 scenarios, and 9B/27B/35B-A3B training exceed budget; a few synthetic fixtures do not substitute.

- [Executable Prefix Values for Locating Agent Failures](https://arxiv.org/html/2610.17633v1) · 2026-10-13 · P1

    Executable Prefix Values estimates V(h_t) by rebuilding intermediate repository states and actually continuing, not re-scoring judge labels. 150 SWE tasks, 47/60 failure traces, and multiple restart schedules require many continuations.

- [MAS-Gate: Unlocking Multi-Agent System Lifecycle via Node-Centric Quantification](https://arxiv.org/pdf/2610.17613v1) · 2026-10-13 · P1

    MAS-Gate learns utility from reference-answer likelihood changes and trains the Editor with paired traces; gold stays in training/scoring. Official PDF p18: eight H100s, batch 256, group 16, 15K prompt/8,192 response. Gold-based fixtures do not become inference operators.

- [EdgeWise: Bringing Long-Horizon Agents to the Edge via Selective Cloud Delegation](https://arxiv.org/html/2610.17560v1) · 2026-10-13 · P1

    EdgeWise jointly learns solving and delegation with step-level RL, not routing labels alone. 9B local and frontier cloud models, 80-turn tasks, RL sampling and controls remain unpriced. Relative 62% savings do not imply cheap reproduction.

</details>

## Retrospective discoveries, known revisions, and official identities: 13

These are not first releases in the current window. Only the current record's reproduction-cost decision is closed; older implementation evidence is not upgraded.

- [Google Earth AI Geospatial Reasoning Agent: Capabilities and a Systematic Evaluation](https://research.google/pubs/google-earth-ai-geospatial-reasoning-agent-capabilities-and-a-systematic-evaluation/) · 2026-10-11 · P1

    Gemini powers modular geospatial skills and planning. Official development splits are available for two benchmarks. First arXiv publication was 2026-10-11; catalog/blog updates are not first releases. Full Gemini/tool budget unresolved; not reproduced, review DONE.

- [DRanker: A Transformer-Based Multi-Task Ranking Model for the Disney+ Homepage](https://arxiv.org/html/2610.15696v1) · 2026-10-11 · P0

    DRanker combines an approximately 7M encoder-only multitask ranker and causal debiasing. The body documents online A/B and global rollout, not only an abstract claim. Months of private Disney interactions and hundreds of millions of training examples cannot be replicated with public data and one card. First arXiv release 2026-10-11 is a retrospective discovery; review DONE.

- [Vela: User Behavior as Supervision Sparks LLM Intelligence](https://arxiv.org/html/2610.14709v1) · 2026-10-10 · P1

    Vela converts long-term behavior into tasks and trajectories, an LLM data/training method rather than qualifying industrial A/B. 35B-A3B, 131,072 length, 75K trajectories, two epochs; appendix RL uses 48 GPUs (32 train, 16 rollout). Too costly; review DONE.

- [Do LLMs Learn from Rewards in Context? : Rethinking the role of reward in In-Context RL](https://arxiv.org/html/2610.11152v3) · 2026-10-08 · P1

    v3 reward flips/randomization/removal and trajectory shuffling find direct ICRL benefits largely driven by ICL context, not a claim about all inference-time RL. The paper reports roughly 5h for ten ScienceWorld episodes and 3h for code on one A100. Full multi-model controls too costly; review DONE.

- [Self-Retrospection Distillation: Turning Post-hoc Experiences into Prior Foresight](https://arxiv.org/html/2610.08077v3) · 2026-10-06 · P1

    SRD v3 learns pre-action foresight from hindsight traces without generating foresight at inference. Hindsight supervision does not expose future to the evaluated agent. Appendix C.2 uses 4B/9B thinking-on, eight H200s, 128 trajectories per step, and ten agent tasks. Too costly; review DONE.

- [Imagine the Future, Internalize the Gist: Efficient VLA Reasoning via Internalized Spatiotemporal Imagination](https://arxiv.org/html/2610.02626v3) · 2026-10-02 · P1

    IG-VLA v3 predicts future SigLIP states before internalizing spatiotemporal reasoning into a gist, not repeating the current frame. §4.1: eight H100s for reasoning, four A6000s for gist, LIBERO 100K and VLABench 61K steps. Single-card latency does not verify training. Too costly; review DONE.

- [Token Utility for On-Policy Distillation via Local Trust-Region Optimization](https://arxiv.org/html/2610.18883v1) · 2026-10-01 · P1

    FUW/Token Utility uses Fisher-geometric token utility to weight distillation. 1.7B/4B students, 8B/14B/30B teachers, 279 steps × 256 sequences × 8,192 context are too costly. Review DONE. First arXiv release was 2026-10-01, a historical omission rather than October 14 first publication.

- [The Teacher Is a Direction, Not a Destination: Extrapolating RL-Induced Representation Residuals in On-Policy Distillation](https://arxiv.org/html/2609.36484v2) · 2026-09-29 · P1

    RIDE v2 uses layerwise hidden-state residuals of RL teacher versus base for extrapolated regression, requiring extra frozen-base forwards. Output-space probability extrapolation is not equivalent. Full teacher/base/student long rollouts and multi-task budget unresolved. Do not retrain; review DONE. Preserve prior L1 implementation and receipt without upgrading for revised metadata.

- [Rubric Dropout: A Simple Way to Mitigate Reward Hacking in Rubric-as-Reward RL](https://arxiv.org/html/2608.11669v2) · 2026-08-12 · P1

    Rubric Dropout v2 retains same-prompt same-step masks, discusses dropping related criteria in blocks, keeps at least three criteria, and evaluates with the full rubric. Independent gold judging is not absolute truth; most configurations use one run. 1.7B–8B, 16 rollouts, 600 steps, and dual API judges are too costly. Prior adapter does not cover v2 blocks.

- [SPARK: Learning from Verification in Speculative GRPO Rollouts](https://arxiv.org/html/2608.04962v2) · 2026-08-05 · P1

    v2 replaces SpecRoll with SPARK: low-rank logit correction shared in each prompt group and reset per rollout, updated from verifier top-16 plus tail feedback with projections learned across rollouts. Target verifier is unchanged. This is not just renaming fast/slow SpecRoll, and local legacy work is not SPARK. Twenty-one model/data configurations plus GRPO exceed budget; review DONE and old page warns about revisions.

- [UniRec: Bridging the Expressive Gap between Generative and Discriminative Recommendation via Chain-of-Attribute](https://arxiv.org/html/2604.12234v5) · 2026-04-14 · P0

    UniRec v5 confirms Shopee and includes capacity-constrained SID, CoA, CDC, and RFT+DPO. §4.2 production A/B qualifies on PVCTR/orders/GMV; do not mix business and offline token-hit metrics. Billions of private events across nine days and three settings prevent faithful full reproduction. Review DONE; old CoA experiments do not upgrade to v5.

- [AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics](https://github.com/facebookresearch/autoformbench/blob/main/paper.pdf) · First release date unverified · P1

    Meta's Lean AutoformBench is distinct from document understanding paper 2603.29832. Official page 2026-10-13, manuscript 2026-10-05, and CITATION 2026-09-30 mean different things and cannot establish first public release. 341 tasks × nine frontier models and long traces with up to \$200 per task (a cap, not uniform actual spend) exceed budget. Review DONE; retain result-import potential without claiming integration.

- [CATWILD: Compiler Autotuning For TPU workloads in the Wild](https://research.google/pubs/catwild-compiler-autotuning-for-tpu-workloads-in-the-wild/) · First release date unverified · P1

    Official source confirms CATWILD TPU-fleet compiler autotuning and five years of production, but only gives 2026, no downloadable paper or exact date. Exact-title and official checks could not place it in the window. TPU fleet unavailable on one A100/A30; no reproduction. Archive date exception outside accepted count.

## Evaluation references, boundaries, and source exceptions: 3

<details markdown="1"><summary>Other P0/P1 decisions (none are capability implementations from this round)</summary>

- [Hide and Seek: HIDE Concepts to SEEK explanations for black box models](https://arxiv.org/html/2610.13935v3) · 2026-10-09 · P1

    Reviewed v3 abstract, method/evaluation, and Appendix A costs: VLM retrieves real concept images, occludes locations, and queries black-box output differences. Cost varies by images per concept; reusable encoders do not make the full pipeline free. Current-version review only; no semantic diff against missing prior baseline or implementation upgrade.

- [NOMOS: Compiling Written Policies into Statically Verified Tool-Call Gates for LLM Agents](https://arxiv.org/html/2610.11030v2) · 2026-10-08 · P1

    NOMOS v2 compiles statically verifiable tool gates in four stages and compares loose, prompt, and dynamic LLM gates. Schema validation alone is not policy compilation. Banking benign utility was used for policy revision, not held-out utility. Original long agents and 26B/70B judges were not run. Revision review only.

- [The Dice Roll Method: A Standardized Protocol for Repeated-Query Auditing of Large Language Model Brand Recommendations](https://arxiv.org/html/2609.04047v2) · 2026-09-03 · P1

    Dice Roll v2 retracts v1's fixed-run tiers and unreproducible tables arising from notebook synthetic data and a 'Research' count field. Pilot first, then determine repeats from variance components; do not cite fixed 5/10/15 recommendations. No implementation exists. Keep the old review snapshot plus this correction without treating prior acceptance as v2 verification.

</details>

See the domain JSON files and the [complete register](../../../research-audits/oct15-review-closure/paper-register.json) for all P2, out-of-scope, and historical-date dispositions, kept out of the default reading view.
