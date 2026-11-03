# Reproduction and implementation overview

<!-- source-sha256: c1a228bfb7e22b44b97d6ab0bd6659b67aec06778f19df9a052b618f4a05f87c -->

[简体中文](../../reproductions/README.md)

This is the **underlying unified inventory** of reproduction adapters, implementation status, and experiment conclusions. Updates to papers and reruns go here and in the individual paper README rather than new milestone audit or batch summary pages.

Browse industrial search, ads, and recommendation [by company](catalog/by-company.md), [by topic](catalog/by-topic.md), or [by month](catalog/by-month.md). Architecture, pretraining, multimodality, and inference efficiency are in [foundation models](../foundation-models/README.md); post-training algorithms are in [LLM post-training](../post-training/README.md). Paper detail and physical paths stay unchanged.

Each new batch builds a candidate set first and records an explicit terminal disposition per candidate. See the [discovery and coverage audit](../paper-discovery-audit.md) for rules, the machine ledger, and mandatory checks.

## Key original figures

Each write-up shows a key original figure between background/main changes and core formulas. Prefer architecture, model structure, or training/inference flow. Store the image in the paper directory as `assets/paper-figure-01.png`, link the original, and retain its copyright note. Without an architecture figure, choose the original flow, algorithm, or experimental screenshot that best explains the method. Explicitly state when public full text is inaccessible; local Mermaid drawings are not original screenshots.

Add or refresh paper figures:

```bash
python -m pip install -e '.[paper-figures]'
python scripts/sync_paper_figures.py --only <arXiv ID or paper directory keyword>
```

Check the collection:

```bash
python scripts/sync_paper_figures.py --workers 3
pytest tests/test_research_module_docs.py
```

Extraction uses arXiv HTML caption relations first, falling back to PDF caption localization and cropping. Some non-arXiv papers use manually verified public PDF mappings. Stable comment markers let repeated refreshes replace figures without duplicate sections.

## Admission and reporting rules {#selection-policy}

- **Industrial threshold:** Full text must report quantitative production online A/B, or the user must explicitly accept statistically significant full rollout, business gains, and guardrails. Deployment alone, offline SOTA, and simulator results do not count. Label unquantified full traffic without inventing percentages.
- **Foundation models:** No online A/B required; need a public benchmark, matched-budget controls, and a core method trainable on public data such as WikiText. Formulas or fixed scores alone do not enter the table.
- **Named exceptions:** SASRec, TIGER, Wide & Deep, DCN-V2, DIEN, BST, DeepFM, YouTube DNN, ESMM, MMoE, and PLE fill classic lineages at user request. Missing quantitative A/B is disclosed per item and does not lower the bar later.
- **Local results:** Every README states baselines, experimental groups, data, main metrics, and relative changes. Separate paper online results, local cross-model comparisons, component ablations, and efficiency controls.
- **Fidelity:** Public substitutes and scaling down are allowed. Replacing a defining architecture, training objective, or inference path with a heuristic is a concept demo. Default batch runs exclude concept demos.
- **Paper information:** At the top of each README list the paper, organization, exact first release and source, upstream code status, adapter, and local code path. Explicitly say no when original author code is not found. Use official proceedings or institution pages if a conference paper lacks arXiv; do not invent IDs.

The common DIN experiment uses MovieLens-100K, chronological leave-two-out, full-item ranking, and seeds 42/43/44. SERAL, LEADRE, COBRA, ARGUS, GR4AD, and MM-LLM use DIN NDCG@10 `0.02167`. Cross-domain KD uses DIN `0.05518` on its independent target split. These are public small-data results, not the papers' private industrial evidence.

## Current progress

- `oob-regularization` · [OOB Regularization](../../reproductions/2610.20158-oob-regularization/README-en.md): Full-dataset Gaussian quantiles and spherical anchors, CPU caches, and periodic refresh. A four-arm short run on public CIFAR used three A100 seeds. Negative results are retained; the full multi-dataset study is not reproduced.
- `forte` · [FORTE](../../reproductions/2610.13806-forte/README-en.md): Pinterest's paired feature-retirement funnel. All three real A100 MovieLens runs retained the original features; no pruning gains are claimed.
- `evo2` · [Evo²](../../reproductions/2610.13025-evo2/README-en.md): Fixed executor alternates harness edits with Proposer/Reflector training, retaining actual execution feedback, SFT, and role-specific GRPO. Local concept diagnostic.
- `rsi-anything` · [RSI-Anything](../../reproductions/2610.13912-rsi-anything/README-en.md): Recursive improvement and policy training driven by isolated program execution feedback. No gold candidates are injected; not evidence of general capability.
- `branch-opd` · [BranchOPD](../../reproductions/2610.13481-branch-opd/README-en.md): Selects branch points on real student rollouts, samples continuations independently, scores them with a teacher, and applies branch distillation and answer formatting constraints.
- `cast-opd` · [CAST](../../reproductions/2610.13257-cast-opd/README-en.md): Aligns credit across tokenizers to pass trainable token-level supervision between heterogeneous teacher and student. Its key is distinct from the older agent CAST.
- `road-mopd` · [Road-MOPD](../../reproductions/2610.13521-road-mopd/README-en.md): Adds cross-teacher safeguards to domain routing, recording conflicts and protected student updates.
- `boundary-evo` · [BoundaryEvo](../../reproductions/2610.13285-boundary-evo/README-en.md): Collects teacher trajectories near the student's capability frontier and maintains replay, iterating data and model together.
- `msar` · [MSAR](../../reproductions/2610.13630-msar/README-en.md): Expands a single residual stream into multi-stream depth-attention residuals and compares real language-model training and resource overhead.
- `orthros` · [Orthros](../../reproductions/2610.13735-orthros/README-en.md): Separates a sliding-window backbone from an independent full-context output stream and checks prefill/decode KV-cache equivalence.
- `dualquant` · [DualQuant](../../reproductions/2610.13767-dualquant/README-en.md): Quantizes real weights and activations with calibration-free dual scaling. Software INT4 does not imply native A100 low-bit acceleration.
- `janus` · [JANUS](../../reproductions/2610.13194-janus/README-en.md): Predicts relative program gains and uncertainty, then tests actual candidates, retaining errors and zero gains.
- `t2mem` · [T2Mem](../../reproductions/2610.13348-t2mem/README-en.md): Manages long conversations using staged summaries, time information, and retrieval. Only the independent scorer sees answers.
- `rated` · [RATED](../../reproductions/2610.13889-rated/README-en.md): Trains a real query/tool dual encoder and updates tool selection from feedback. Semantic retrieval diagnosis is not backend task success.
- `jev-workflow` · [Jev workflow evaluation](../../reproductions/2610.13092-jev-workflow/README-en.md): Compares workflow efficiency, quality, and cost with paired traces. An evaluation facility, not a training algorithm.
- `woven` · [WOVEN](../../reproductions/2610.12417-woven/README-en.md): Uses visual state transitions as a shared training primitive. Official validation and test data were unavailable; local experiments use a labeled split of the training set.
- `umrm` · [UMRM](../../reproductions/2610.12707-umrm/README-en.md): Trains a reward head from frozen VLM intermediate layers. Object verification with public captions does not reproduce official CHAIR.

- `rptune` · [RPTune](../../reproductions/2610.00964-rptune/README-en.md): Google's joint query–product scoring, pruning, and suffix scheduling. No quantitative online A/B; academic/evolve diagnostic only, not industrial evidence.
- `agent-web-rec` · [AgentWebRec](../../reproductions/2610.01705-agent-web-rec/README-en.md): Combines platform semantics, private user sequence memory, and low-confidence neighbor patterns without exposing private records. No online A/B; academic/evolve diagnostic.
- `gear` · [GEAR](../../reproductions/2609.39327-gear/README-en.md): Orthogonal-basis BasisVQ/BasisRQ and contextual reranking of collided items. The paper reports seven days of Douyin Ads A/B at 5% per arm; local work covers the L1 mechanism only.
- `effective-training-time` · [Effective Training Time](../../reproductions/2610.02057-effective-training-time/README-en.md): Separates training on new data from initialization, compilation, checkpointing, publishing, and recovery. User-approved production infrastructure exception, not recommender A/B evidence.
- `gris` · [GrIS](../../reproductions/2610.01533-gris/README-en.md): Combines collaborative graphs and content semantics in hierarchical Semantic IDs. User-approved academic/evolve exception with no online A/B.
- `repair-state` · [REPAIR](../../reproductions/2610.01270-repair-state/README-en.md): Selects corrective evidence from frozen encoder caches to repair a lossy preference state via residuals. User-approved academic/evolve exception with no online A/B.
- `cohortmix-ts` · [CohortMix-TS](../../reproductions/2609.37800-cohortmix-ts/README-en.md): Builds fixed-strength mixed Beta priors from historical cohorts, selects slates by Thompson sampling, and updates from feedback. The 25-day randomized deployment's significant result is from a restricted full-window subgroup; local work diagnoses state updates.
- `recap-ctr` · [RECAP CTR](../../reproductions/2609.37905-recap-ctr/README-en.md): Multiple estimator routes in a weight-shared recurrent backbone, route averaging, and EMA over training. Executable evolve operator: rankmixer_recap. No online A/B; not industrial evidence.
- `evoskillrec` · [EvoSkillRec](../../reproductions/2609.34552-evoskillrec/README-en.md): Runs typed skill genomes, validation, promotion, and reuse via rankmixer_evoskill in unified evolve. L1 mechanism diagnostic, not a claim about large search gains.
- `promptshift` · [PromptShift](../../reproductions/2609.34229-promptshift/README-en.md): Computes Drift, SliceShift, difficulty-weighted hits, and adaptive inverse-popularity reranking on fixed relevance and identity-slice fixtures. No real identity profiles are generated or inferred.
- `grp` · [Snap GRP v0.1](../../reproductions/2609.36688-grp/README-en.md): Separate SID blocks, isolated generation/ranking gradients, and mGRPO with one-sided recall safeguards phase a shared model into retrieval and ranking. L1 public tensors, not Snap's online results.
- `helix` · [TikTok HELIX](../../reproductions/2609.37183-helix/README-en.md): Interleaves feature interactions and sequence modeling while preserving user-state reuse with one-way information flow. L1 public-tensor mechanism, not full-rollout A/B replication.
- `flvm` · [Google/YouTube FLVM](../../reproductions/2609.32839-flvm/README-en.md): Three latent factors, a restricted confound baseline, and sparse feedback routing with three positive/negative-feedback seeds on public KuaiRand. Sparse negatives and unstable semantics make this a concept diagnostic.
- `recursive-opsd` · [Meta DCE+SRCL](../../reproductions/2609.30652-recursive-opsd/README-en.md): Qwen3-4B on A100 runs a dynamic privileged teacher, token forward KL, and answer-validated concise self-rewrites. Two rounds on public GSM8K gave no accuracy gain evidence; concept diagnostic.
- `kuafu` · [Tencent KuaFu](../../reproductions/2609.31045-kuafu/README-en.md): A100 ran itemwise compression, dual-axis projection, and small public MRQA supervision. Dev F1 did not beat same-token head truncation; hallucination RL had zero within-group advantage. Concept diagnostic.
- `onetrans-v2` · [ByteDance OneTrans-V2](../../reproductions/2609.28589-onetrans-v2/README-en.md): Shared causal user backbone, three-level SID retrieval, and joint pre/fine ranking plus distillation ran with three MovieLens-1M proxy-label seeds. No real conversions, ads, or impression funnel; concept diagnostic.
- `xrec` · [TikTok X-Rec](../../reproductions/2609.29180-xrec/README-en.md): Anchor-conditioned spherical flow matching, final-layer interactions, and multi-trigger full-catalog retrieval on MovieLens-1M. Three small-budget seeds underperformed same-budget U2I.
- `music-rationales` · [Google YouTube Music](../../reproductions/2609.23877-music-rationales/README-en.md): A real 7B model creates discovery profiles offline; a public artist catalog filters cached reasons, with CF fallback. Concept diagnostic only.
- `light-heads` · [Google Light Heads](../../reproductions/2609.25433-light-heads/README-en.md): Dynamically adds gradient-free shallow heads above shared ranking towers, comparing window reset and removing stop-gradient.
- `unique` · [UNIQUE](../../reproductions/2609.23718-unique/README-en.md): Flat single-level quantization and early fusion for joint retrieval and ranking. Retains low recall and no ranking improvement on KuaiRand-Pure.
- `muser` · [MuSeR](../../reproductions/2609.23677-muser/README-en.md): Hierarchical temporal compression and multi-query interests. Public labels replace private multimodal semantics; concept diagnostic.
- `evopilot` · [EvoPilot](../../reproductions/2609.21257-evopilot/README-en.md): Constrains long-running online research with artifact attestation, a fail-closed pair verifier, and human review.
- `angle` · [ANGLE](../../reproductions/2609.18296-angle/README-en.md): Hierarchical text identifiers, joint generation/classification/ranking, and dynamic constrained retrieval.
- `sas-attention` · [SAS](../../reproductions/2609.13141-sas-attention/README-en.md): Uses continuous log gates in softmax to train sparse context ranking end to end with language-model loss.
- `mima` · [MIMA](../../reproductions/2609.12842-mima/README-en.md): Uses same-request multiple positives, exclusive matching, and calibrated interest activation to reduce interest collapse.
- `chronicle-rec` · [ChronicleRec](../../reproductions/2609.12375-chronicle-rec/README-en.md): Recent-dense and older-sparse compression, causal time anchors, multiple horizons, and alignment pretraining.
- `pindco` · [PinDCO](../../reproductions/2609.11943-pindco/README-en.md): Incrementally fuses component towers with a page-pixel penalty, prescreening, and feedback from exploration.
- `gese` · [GESE](../../reproductions/2609.15094-gese/README-en.md): Set-level title exploration, fidelity constraints, and personalized contextual selection.
- `lazformer` · [LazFormer](../../reproductions/2609.14978-lazformer/README-en.md): Transferable generative pretraining, ranking residual adaptation, and recent-dense/older-sparse attention.
- `sirf` · [SIRF](../../reproductions/2609.11752-sirf/README-en.md): Internalizes policy rules as trainable interaction features and validates decisions with separate high-quantile error constraints.
- `unirec` · [UniRec](../../reproductions/2609.11052-unirec/README-en.md): The paper fuses pre-ranking and fine ranking. The old NumPy scorer is a concept demo; v3 CPPA/CAPP and AGRR KL are separate A100 mechanism components, not full reproduction.
- `sequenceo1` · [SequenceO1](../../reproductions/2609.08443-sequenceo1/README-en.md): Fixed-budget Sketch Attention, a recent-history branch, and a cache for extremely long sequences.
- `baff` · [BAFF](../../reproductions/2609.08725-baff/README-en.md): Two-axis ranking/bidding interference filtering on shared RTB logs.
- `allecompanion` · [AlleCompanion](../../reproductions/2609.05063-allecompanion/README-en.md): Category-constrained dual towers, ComCat complementary graph, and controlled Category Adapter.
- `autolr` · [AutoLR](../../reproductions/2609.04871-autolr/README-en.md): Multi-expert review, evidence-weighted experiment budgets, and deterministic release gates.
- `beaconkv` · [BeaconKV](../../reproductions/2609.04971-beaconkv/README-en.md): Query-cluster beacons predict distant KV revisits in long reasoning.
- `kvmem` · [KVMEM](../../reproductions/2609.04852-kvmem/README-en.md): Paged KV virtualization and query-dependent agent workspace materialization.
- `coral` · [CORAL](../../reproductions/2609.02730-coral/README-en.md): Meta's constrained configuration, short-term experiment memory, and production feedback loop.
- `recevolve` · [RecEvolve](../../reproductions/2609.01622-recevolve/README-en.md): Google's knowledge-driven proposals, isolated experiments, rollback, and anti-reward-hacking controller.
- `random-attention` · [Random Attention](../../reproductions/2609.03430-random-attention/README-en.md): Prompt protection, random per-head KV eviction, and real Qwen/A100 verification.
- `lngram-v2` · [Lngram v2](../../reproductions/2609.03426-lngram-v2/README-en.md): Discrete latent n-gram memory, GQA zero sink, and real VLM/A100 verification.
- `rest` · [ReST](../../reproductions/2609.01240-rest/README-en.md): Dual-gated temporal encoding and reusable user prefixes for industrial ranking.
- `tgr` · [TGR](../../reproductions/2609.00986-tgr/README-en.md): Unified generative ranking, semantic IDs, and offline reason tokens.
- `camie` · [CAMIE](../../reproductions/2608.30255-camie/README-en.md): Aligns multimodal product representations using shared engagement.
- `setmir` · [SetMIR](../../reproductions/2608.30251-setmir/README-en.md): Predicts sets of interests, gates presence, and dispatches dynamically to ANN.

- Audited 94 main entries and 138 arXiv links in two industrial-deployment blog sections.
- See this page and the domain indexes for adapters. Recommendation requires online A/B or full rollout; foundation models need public benchmarks and real training. Generated manifest counts are authoritative.
- Deferred: AIGQ lacks equivalent query/CTR rewards; RaG needs video generation and quality feedback; RoleGen needs conversion trajectories and online feedback; LCU data require an NDA.
- Skipped EGA-V1. Offline-only or unverified quantitative A/B papers do not enter the implementation queue.
- Remaining qualifying 2026 papers entered core-mechanism reproduction. The 2026-07-27 P1 batch added eight industrial papers and executable Engram, Looped Latent Attention, and GaugeQuant operators to LLM evolve. GRACE, DLMRec, LO-FAR, and PRL lacked quantitative online evidence and were not included.
- The 2026-07-28 batch added Meta Mosaic, Kuaishou UniR², Meituan CORE, and DataOrchestra. The first three passed quantitative online A/B; DataOrchestra has official code and public pretraining benchmarks.
- The 2026-07-30 batch added Tencent CCFormer, Teads Open Web UFM, Meta ROCS, and WIDE. The first three disclose A/B, full traffic, or quantitative deployment, respectively. WIDE provides code and public pruning and throughput experiments.
- The 2025 industrial backfill added MIM, FilterLLM, FuXi-α, RecGPT-V2, HiGR, DRL-PUT, AdaF²M², MGOE, and Click A Buy B. All nine report production A/B and ran independent core mechanisms on MovieLens-1M.
- 2025 LLM evolve P0 added DeepSeek NSA, Qwen Gated Attention, and Moonshot Muon. Structures and optimizers compose; ran matched WikiText-2 controls and four evolve rounds.

## Google / Meta full-text evidence backfill (10 P0 adapters)

- `memory-layer` · [Meta Memory Layer](../../reproductions/2607.25110-memory-layer/README-en.md): Training-time eta=1 writeback makes item cache model state. Always-on attributes cover cold start and missing IDs.
- `scalr` · [Meta SCALR](../../reproductions/2606.00282-scalr/README-en.md): Learns cross-domain event conditionals and samples probabilistically instead of copying top-k to cover more training events.
- `hill-index` · [Meta HILL](../../reproductions/2604.12965-hill-index/README-en.md): Coarse-to-fine residual quantization learns hierarchical indexes and reduces online candidate scoring.
- `semantic-native-longseq` · [Google Semantic-Native Long Sequence Modeling](../../reproductions/2606.07546-semantic-native-longseq/README-en.md): Hierarchical SIDs, bigrams, temporal folding, and global-local pooling extend video histories.

- `ha-moe` · [Google Discover HA-MoE](../../reproductions/2607.27577-ha-moe/README-en.md): Heterogeneity-gated experts; 7-day A/B on 1% traffic.
- `dual-sid` · [YouTube Dual-purpose Semantic IDs](../../reproductions/2607.24865-dual-sid/README-en.md): Semantic IDs encode collaborative identity and reconstruct content embeddings.
- `agentic-rec-tune` · [Google Discover AgenticRecTune](../../reproductions/2604.26969-agentic-rec-tune/README-en.md): Actor–Critic–SkillHub multi-round recommendation optimization.
- `mfli` · [Meta MFLI](../../reproductions/2602.16124-mfli/README-en.md): Learnable real-time retrieval indexes with multiple slices.
- `kunlun` · [Meta Kunlun](../../reproductions/2602.10016-kunlun/README-en.md): Unified deep architecture with GDPA, hierarchical seed pooling, and CompSkip.
- `ultra-hstu` · [Meta ULTRA-HSTU](../../reproductions/2602.16986-ultra-hstu/README-en.md): Semi-local attention, LBSL, and Mixture of Transducers.

Candidates were retrieved by affiliation and topic, then checked in full text and tables without requiring A/B in the abstract. All six had public-data runs, stable metrics, an original key figure, and executable evolve mappings (AgenticRecTune maps to a controller regression, not an invented architecture).

## 2026 historical P0 · H02 (8 adapters)

- `drem` · [DrEM](../../reproductions/2608.12778-drem/README-en.md): Stabilizes multi-channel pxtr ranking with preference-preserving noise filtering, pair-label flip-risk inversion, and consistency fusion.
- `incrementality` · [From Prediction to Incrementality](../../reproductions/2608.10182-incrementality/README-en.md): Uses potential-outcome differences and uncertainty for matched-budget causal targeting instead of ranking treated outcomes.
- `tm20k` · [TM20K](../../reproductions/2608.07055-tm20k/README-en.md): The teacher retains full history; contiguous token merging and attention distillation compress the student's long sequence.
- `transx` · [TransX](../../reproductions/2607.28940-transx/README-en.md): Separates cacheable behavioral and per-request serving streams with cross-attention to reduce repeated work.
- `snaplgr` · [SnapLGR](../../reproductions/2607.28895-snaplgr/README-en.md): Co-engagement propagation, hierarchical residual SIDs, token grounding, and SID sequence SFT.
- `psg` · [PSG](../../reproductions/2607.26427-psg/README-en.md): Generates ordered pairs and expands them into a slate, reducing six-item decoding to three steps.
- `director` · [DIRECTOR](../../reproductions/2607.26418-director/README-en.md): Uses Sinkhorn transport and global matching for parallel duplicate-free dynamic-index slates.
- `reward-guided-decoding` · [Reward Guided Decoding](../../reproductions/2607.25344-reward-guided-decoding/README-en.md): A KL-regularized closed-form policy adds business rewards without retraining the generator.

All eight retain public-data results for seeds 42/43/44, original key figures, online evidence, and reproduction limits. The structures are executable genrec evolve mutations.

## 2026 historical P0 · H03 (9 adapters)

- `specformer` · [SpecFormer](../../reproductions/2607.24025-specformer/README-en.md): Spectrally softened attention and spectral residual position encoding.
- `egr` · [EGR](../../reproductions/2607.23038-egr/README-en.md): A shared encoder jointly learns item index vectors and user query vectors.
- `zorro` · [ZoRRO](../../reproductions/2607.10910-zorro/README-en.md): Training-free ranking over recency, semantics, and category relations.
- `elise` · [Apple Music ELISE](../../reproductions/2607.10239-elise/README-en.md): Dense/lexical quantile calibration and hybrid retrieval.
- `poem` · [POEM](../../reproductions/2606.29946-poem/README-en.md): Partially ordered behavior sequences from real-time multi-objective ranking signals.
- `uniformer` · [UniFormer](../../reproductions/2606.27058-uniformer/README-en.md): Unified token interactions in feature and task spaces.
- `rag-generation` · [Recommendation as Generation](../../reproductions/2606.25496-rag-generation/README-en.md): Disentangled SIDs connect recommendation and content generation.
- `onerank` · [OneRank](../../reproductions/2606.16838-onerank/README-en.md): Transformer-native private task channels and gradient isolation.
- `piano` · [PIANO](../../reproductions/2606.16641-piano/README-en.md): Query-driven interest refinement and a listwise information node.

All nine execute independent core computation, retain three-seed public results and original key figures, and are executable genrec evolve operators. Local results establish mechanisms, not production lift.

## 2026 historical P0 · H04 (9 adapters)

- `atomic-intent` · [Atomic Intent Reasoning](../../reproductions/2606.10357-atomic-intent/README-en.md): Decomposes queries with hierarchical atomic intent trees, then reranks by candidate alignment with intent paths.
- `toolrec` · [ToolRec](../../reproductions/2606.08466-toolrec/README-en.md): Joint relevance, confidence calibration, and business cost filter over-triggered tool recommendations.
- `ssrlive` · [SSRLive](../../reproductions/2606.06970-ssrlive/README-en.md): Static and dynamic SIDs plus user–live-room crosses unify content identity and real-time state.
- `taiji` · [Taiji](../../reproductions/2606.03866-taiji/README-en.md): Adaptively selects Pareto operating points between semantic and collaborative matching.
- `primal-dual-decoding` · [Stochastic Primal-Dual Decoding](../../reproductions/2607.19357-primal-dual-decoding/README-en.md): Updates decoding-time constraint multipliers to balance relevance and business constraints.
- `muchator` · [MuChator](../../reproductions/2605.27103-muchator/README-en.md): Discovers latent intents in multi-turn conversations and ranks candidates using explicit and implicit feedback.
- `causal-representation` · [Causal Representation Learning for Generalisable Recommendation](../../reproductions/2605.27043-causal-representation/README-en.md): Residualizes environment confounders for more stable causal preferences across environments.
- `policy-facet` · [Policy-Grounded Dynamic Facet Suggestions](../../reproductions/2605.16479-policy-facet/README-en.md): Offline taxonomy, online retrieval, and policy-constrained ranking generate dynamic facets.
- `pa-bridge` · [PA-Bridge](../../reproductions/2605.05855-pa-bridge/README-en.md): Aligns representation distributions between active search and passive recommendation.

All nine retain production evidence and public-data limits, execute independent mechanisms with three MovieLens seeds, and register runnable genrec evolve mutations. Negative local results are neither hidden nor rewritten as improvements.

## 2026 historical P0 · H05 (10 adapters)

- `marc` · [MARC](../../reproductions/2604.18146-marc/README-en.md): Extracts task-relevant intermediate representations, decoupling recommendation adaptation from compression.
- `rankup` · [RankUp](../../reproductions/2604.17878-rankup/README-en.md): Randomly permuted multiple embeddings, global tokens, and task decoupling improve effective rank.
- `sid-coord` · [SID-Coord](../../reproductions/2604.10471-sid-coord/README-en.md): Hierarchical SIDs, target-aware HID–SID gating, and interest alignment support long-tail generalization.
- `rclrec` · [RCLRec](../../reproductions/2603.28124-rclrec/README-en.md): Builds short backward curricula from conversion-related behaviors for intermediate supervision.
- `tagllm` · [TagLLM](../../reproductions/2603.21481-tagllm/README-en.md): A user-interest handbook constrains fine multimodal labels, then distills tagging into a small model.
- `genfacet` · [GenFacet](../../reproductions/2603.19665-genfacet/README-en.md): Jointly generates facets and rewrites queries, aligning preferences with retrieval satisfaction.
- `cgr` · [CGR](../../reproductions/2603.04227-cgr/README-en.md): Constraint-aware reward pruning directly within autoregressive reranking.
- `hpgr` · [HPGR](../../reproductions/2603.00980-hpgr/README-en.md): Session-level pretraining and preference-guided sparse attention restructure flat behavior sequences.
- `climber-pilot` · [Climber-Pilot](../../reproductions/2602.13581-climber-pilot/README-en.md): Distills multi-step consumption look-ahead into one-step retrieval with business instructions in attention.
- `rolegen` · [RoleGen](../../reproductions/2602.13134-rolegen/README-en.md): Finds bridge items for dormant users via functional roles and counterfactual conversion paths.

All ten have independent core computation, public seed 42/43/44 artifacts, original key figures, and executable genrec evolve operators. Paper online numbers and local mechanism results remain separate.

## 2026 historical P0 · H06/H07 (15 adapters)

- `unimvt` · [UniMVT](../../reproductions/2602.12972-unimvt/README-en.md): Jointly learns debiased CTR and causal uplift with explicit treatment and counterfactual estimates.
- `rq-gmm` · [RQ-GMM](../../reproductions/2602.12593-rq-gmm/README-en.md): Replaces hard clustering with residual Gaussian-mixture quantization for probabilistic SIDs in multimodal CTR.
- `capts` · [CAPTS](../../reproductions/2602.12564-capts/README-en.md): Value-aware matching and adaptive cross-channel routing select I2I retrieval triggers.
- `mlcc` · [MLCC](../../reproductions/2602.12041-mlcc/README-en.md): Hierarchical compression and low-dimensional feature crossing grow capacity within a controlled compute budget.
- `ug-sep` · [UG-Sep](../../reproductions/2602.10455-ug-sep/README-en.md): Separates user-side and general computation to reuse representations computed once.
- `smes` · [SMES](../../reproductions/2602.09386-smes/README-en.md): Progressive sparse routing and deduplicated execution allocate expert capacity dynamically by task.
- `pit` · [PIT](../../reproductions/2602.08530-pit/README-en.md): Combines item tokens dynamically by user so SIDs encode personal preferences.
- `zenith` · [Zenith](../../reproductions/2601.21285-zenith/README-en.md): Prime Token Fusion and Boost scale live-stream ranking.
- `easq` · [EASQ](../../reproductions/2601.20215-easq/README-en.md): Separate LoRA and multitask paths incorporate sparse survey satisfaction into online learning.
- `s2gr` · [S2GR](../../reproductions/2601.18664-s2gr/README-en.md): Injects semantic guidance in stages into latent reasoning for intermediate decisions.
- `sparsectr` · [SparseCTR](../../reproductions/2601.17836-sparsectr/README-en.md): Combines global, transition, and local sparse attention over thousand-event histories.
- `hcub` · [HCUB](../../reproductions/2601.14333-hcub/README-en.md): Hierarchical contextual uplift bandits learn catalog personalization incrementality.
- `airbnb-ebr` · [Airbnb EBR](../../reproductions/2601.06873-airbnb-ebr/README-en.md): Journey-level retrieval and multi-stage ranking unify experience recommendations.
- `promise` · [PROMISE](../../reproductions/2601.04674-promise/README-en.md): Process rewards supervise intermediate reasoning in generative recommendation.
- `harmonrank` · [HarmonRank](../../reproductions/2601.02955-harmonrank/README-en.md): Relation-aware attention and consistency constraints coordinate multi-stage ranking.

All fifteen have independent mechanisms, public results at seeds 42/43/44, original key figures, and executable evolve operators. H06/H07 close the fixed 55-paper 2026 historical P0 queue.

## 2026-08-24 cross-domain additions

- `oneshot-index` · [OneShot](../../reproductions/2607.27475-oneshot-index/README-en.md): Meta/Instagram jointly trains a hierarchical index and ranking, replacing pure dot-product retrieval with neural scoring. Deployed to all global traffic.
- `clockrope` · [ClockRoPE](../../reproductions/2607.26369-clockrope/README-en.md): YouTube/Google DeepMind samples rotary frequencies from a periodic kernel's Fourier spectrum to model daily and weekly routines.
- `next-vlm` · [NEXT](../../reproductions/2607.24789-next-vlm/README-en.md): Meta uses an 8B VLM to build a directed item→intent→item NKG; reasoning is offline and only verified edges are injected online.
- `onemodel` · [OneModel](../../reproductions/2608.18606-onemodel/README-en.md): Xiaohongshu uses a shared long-sequence backbone, scenario gates, and hierarchical user representations for recommendation, ads, and merchant ranking. Reports quantitative A/B in three production settings.
- `rare` · [RARE](../../reproductions/2608.21236-rare/README-en.md): Projects editing directions into the MoE router null space and corrects drift at downstream guard layers to preserve expert paths.

## 2026-08-26 additions

- `tagr` · [TAGR](../../reproductions/2608.24034-tagr/README-en.md): Kuaishou livestream ads use stable two-level semantic/collaborative IDs, multiscale interests, and behavior-value gates. Production A/B: LRE +8.5%, SCC +7.4%, revenue +16.1%.
- `wemm-embedding` · [WeMM-Embedding](../../reproductions/2608.24053-wemm-embedding/README-en.md): WeChat combines multimodal alignment, cross-scale teacher refinement, and Matryoshka embeddings. Reports full rollout of 14 online A/B gains and releases code and weights.

## 2026-08-27 additions

- `dceo` · [DCEO](../../reproductions/2608.25635-dceo/README-en.md): Taobao Search uses a context-conditioned actor to optimize relative causal long-term user value. A 41-day production A/B reported GMV +0.36%.
- `transretrieval` · [TransRetrieval](../../reproductions/2608.25528-transretrieval/README-en.md): Cross-domain ad retrieval with norm-aware aggregation, target-token compression, and positional domain embeddings. One-month 5%-traffic A/B revenue +2.53%.
- `vbvr-pro` · [VBVR-Pro](../../reproductions/2608.26105-vbvr-pro/README-en.md): Task-specific executable scoring replaces generic VLM judging for state-level verifiable reward in native visual reasoning.
- `mllmclip` · [MLLMCLIP](../../reproductions/2608.25575-mllmclip/README-en.md): Selects teacher tokens by attention across MLLM layers and aligns small CLIP visual/text features via CKA.

## 2026-08-29 additions

- `friend-gnn` · [VK Friend-GNN](../../reproductions/2608.27413-friend-gnn/README-en.md): Multi-hash sharing compresses massive user embeddings, while time-sorted adjacency and binary cutoffs prevent future leakage. VK production A/B: friend adds +16.0%, unique friend-adding users +11.5%.
- `pace-vlm` · [PACE](../../reproductions/2608.27206-pace-vlm/README-en.md): A shallow visual preview adapts token budgets with fused LLM/ViT attention. Verified real Qwen2.5-VL and RealWorldQA on A30.
- `twinkv` · [TwinKV](../../reproductions/2608.27128-twinkv/README-en.md): Pairs orphan and donor entries to repair arbitrary KV eviction policies at a fixed cache budget. Real Qwen3 KV and WikiText-2 long context verified on A30.

## 2026 historical scan B01–B03 (18 adapters)

- `dynamic-codebook` · [Dynamic Single-Level Large Semantic Codebook](../../reproductions/2608.21012-dynamic-codebook/README-en.md): Exposure-weighted dynamic large codebook, independent collision codes, and short SID decoding.
- `netflix-mediafm` · [Netflix Multimedia Asset Personalization](../../reproductions/2608.18322-netflix-mediafm/README-en.md): Frozen multimodal features, a unified asset dual encoder, and query-aware scoring.
- `ogr` · [Once Generated, Ranked](../../reproductions/2608.17613-ogr/README-en.md): Unified semantic–collaborative IDs, slate planning, and conservative policy alignment.
- `inthq` · [IntHQ](../../reproductions/2608.09634-inthq/README-en.md): Hierarchical task-interactive queries over short and long streams.
- `pushdualgen` · [PushDualGen](../../reproductions/2608.07989-pushdualgen/README-en.md): Generate SIDs first and interpretable copy on demand.
- `recharness` · [RecHarness](../../reproductions/2607.29241-recharness/README-en.md): Bandit routing over multi-round architecture experiments under a limited budget.
- `gala` · [GALA](../../reproductions/2607.29213-gala/README-en.md): Multimodal triplet pretraining, GRPO behavioral alignment, and gated ID fusion.
- `feedback-policy` · [Feedback-Grounded Policy Discovery](../../reproductions/2607.27789-feedback-policy/README-en.md): Discovers generative policies from feedback and distills to a lightweight online ranker.
- `real-estate-rerank` · [LLM-Based Re-Ranking for Real Estate Search](../../reproductions/2607.14835-real-estate-rerank/README-en.md): Reranks using conversational intent, property text, and candidate-set statistics.
- `adaptive-ad-load` · [Adaptive Ad Load Design](../../reproductions/2607.14418-adaptive-ad-load/README-en.md): Chooses ad count dynamically under revenue and conversion constraints.
- `guess-where-you-go` · [Guess Where You Go](../../reproductions/2607.26073-guess-where-you-go/README-en.md): Spatiotemporal SIDs, curriculum learning, and long-term feedback policy optimization.
- `genpage` · [GenPage](../../reproductions/2606.31031-genpage/README-en.md): One model generates whole pages and is post-trained with long-term rewards.
- `journeyformer` · [JourneyFormer](../../reproductions/2606.19108-journeyformer/README-en.md): Jointly encodes Airbnb guest journeys at short and long timescales.
- `l2rec` · [L2Rec](../../reproductions/2605.26717-l2rec/README-en.md): Personalized dual-view LoRA-MoE and cross-view fusion.
- `qgs` · [QGS](../../reproductions/2605.25514-qgs/README-en.md): Joint query–item sequences, Linear HSTU, and generative search.
- `tubifm` · [TubiFM](../../reproductions/2605.23702-tubifm/README-en.md): A shared user-story foundation model unifies three ranking tasks.
- `pearl-percentile` · [PEARL](../../reproductions/2605.21752-pearl-percentile/README-en.md): Multi-sample contrastive learning estimates behavior percentiles with low bias and variance.
- `dadf` · [DADF](../../reproductions/2605.17863-dadf/README-en.md): Freezes the base model and learns distribution-aware multiplicative residual corrections.

## All-domain P0 gap closeout (19 adapters)

- `glorank` · [GloRank](../../reproductions/2604.25291-glorank/README-en.md)
- `dual-rerank` · [Dual-Rerank](../../reproductions/2604.07420-dual-rerank/README-en.md)
- `oneranker` · [OneRanker](../../reproductions/2603.02999-oneranker/README-en.md)
- `radar` · [RADAR](../../reproductions/2506.07261-radar/README-en.md)
- `dualgr` · [DualGR](../../reproductions/2511.12518-dualgr/README-en.md)
- `mpformer` · [MPFormer](../../reproductions/2508.20400-mpformer/README-en.md)
- `hap` · [HAP](../../reproductions/2603.03770-hap/README-en.md)
- `onepiece` · [OnePiece](../../reproductions/2509.18091-onepiece/README-en.md)
- `intsr` · [IntSR](../../reproductions/2509.21179-intsr/README-en.md)
- `cdm` · [CDM](../../reproductions/2406.09021-cdm/README-en.md)
- `cwm` · [CWM](../../reproductions/2406.07932-cwm/README-en.md)
- `rope` · [RoPE / RoFormer](../../reproductions/2104.09864-rope/README-en.md)
- `alibi` · [ALiBi](../../reproductions/2108.12409-alibi/README-en.md)
- `gqa` · [GQA](../../reproductions/2305.13245-gqa/README-en.md)
- `hymba` · [Hymba](../../reproductions/2411.13676-hymba/README-en.md)
- `moba` · [MoBA](../../reproductions/2502.13189-moba/README-en.md)
- `blt` · [Byte Latent Transformer](../../reproductions/2412.09871-blt/README-en.md)
- `doremi` · [DoReMi](../../reproductions/2305.10429-doremi/README-en.md)
- `data-mixing-laws` · [Data Mixing Laws](../../reproductions/2403.16952-data-mixing-laws/README-en.md)

Each write-up has upstream code status, core formulas, original figures, paper results, fair local baselines, stable metrics, and executable commands. Negative local results are retained.

## All-domain P1 gap closeout (8 adapters)

- Industrial recommendation: [TWIN-V2](../../reproductions/2407.16357-twin-v2/README-en.md), [SIM](../../reproductions/2006.05639-sim/README-en.md), [CRSD](../../reproductions/2510.11056-crsd/README-en.md).
- Multimodal: [CLIP](../../reproductions/2103.00020-clip/README-en.md), [BLIP-2](../../reproductions/2301.12597-blip2/README-en.md), [LLaVA](../../reproductions/2304.08485-llava/README-en.md), [SigLIP 2](../../reproductions/2502.14786-siglip2/README-en.md), [SmolVLM](../../reproductions/2504.05299-smolvlm/README-en.md).
- Inference and deployment: [Speculative Decoding](../../reproductions/2211.17192-speculative-decoding/README-en.md), [AWQ](../../reproductions/2306.00978-awq/README-en.md), [Medusa](../../reproductions/2401.10774-medusa/README-en.md).

## 2026-08-09 P0/P1 additions (9 adapters)

- `twitch-mor` · [Twitch Multi-Objective Ranking](../../reproductions/2608.04455-twitch-mor/README-en.md)
- `llm-ts-prior` · [LLM-Derived Thompson Priors](../../reproductions/2608.03382-llm-ts-prior/README-en.md)
- `kgd` · [KGD](../../reproductions/2608.02738-kgd/README-en.md)
- `hrpo` · [HRPO](../../reproductions/2608.00750-hrpo/README-en.md)
- `bakron` · [BaKron](../../reproductions/2608.06291-bakron/README-en.md)
- `macro` · [MACRO](../../reproductions/2608.05872-macro/README-en.md)
- `hilp` · [HiLP](../../reproductions/2608.05806-hilp/README-en.md)
- `dblast` · [DBLast](../../reproductions/2608.05448-dblast/README-en.md)
- `qevict` · [QEvict](../../reproductions/2608.05326-qevict/README-en.md)

The first four industrial papers met quantitative online A/B or rollout criteria; the other five belong to foundation models. Core mechanisms ran and preserve seed 42 metrics, including negative and nonsignificant results.

## 2026-08-13 MR7 additions (3 adapters)

- `sona` · [Sona](../../reproductions/2608.11015-sona/README-en.md): Compressed history, autoregressive Semantic IDs, and an item ranker in one model replace a music recommendation cascade.
- `metastrategy` · [MetaStrategy](../../reproductions/2608.09440-metastrategy/README-en.md): An LLM writes typed strategies compiled deterministically for multi-objective ranking.
- `gas` · [GAS](../../reproductions/2608.12209-gas/README-en.md): A removable MoT generation branch performs continuous next-embedding prediction for multimodal understanding without deployment overhead.

Both industrial papers report quantitative real-traffic A/B in the full text. MovieLens-1M experiments retain negative results rather than importing online lifts. GAS is foundation/multimodal and does not require online A/B; public-pixel runs and paper numbers are separate.

## 2026-08-20 industrial additions (2 adapters)

- `connectionmind` · [ConnectionMind](../../reproductions/2608.10187-connectionmind/README-en.md): Meta and Michigan State University combine temporal heterogeneous graphs, shortest-path SFT, rule-reward GRPO, and path distillation for social recommendation. Multi-week A/B with tens of millions of users reports quantified impression, watch-time, and session gains.
- `dream` · [DREAM](../../reproductions/2608.09408-dream/README-en.md): Taobao adds three-level intent, strategy memory, typed parameter compilation, and offline/online Reward Dual Loop to existing retrieval and ranking. Fine ranking plus reranking: IPV +2.71%, Core IPV +3.06%, GMV +1.31%.

Both run their core training or control loops. ConnectionMind uses Delicious as in the paper and retains NDCG@10 −7.44%. DREAM's positive local correlation comes with pronounced head bias.

## 2026 historical scan B04–B06 (19 adapters)

Full text verifies production A/B for all 19. Independent mechanisms run on identical MovieLens-100K splits, candidates, and seed 42. Online and local results are reported separately.

### B04

- `prl-puts` · [PRL-PUTS](../../reproductions/2605.16344-prl-puts/README-en.md): Two-head Q network and Pareto utility sweeps.
- `ektm` · [Effective Knowledge Transfer for Multi-Task Recommendation Models](../../reproductions/2605.05730-ektm/README-en.md): Transfers knowledge across tasks based on task similarity.
- `adasid` · [AdaSID](../../reproductions/2604.23522-adasid/README-en.md): Dynamic SIDs from collision load and semantic compatibility.
- `unirec-coa` · [UniRec](../../reproductions/2604.12234-unirec-coa/README-en.md): Generates attribute chains and aligns business preferences.
- `uniscale` · [UniScale](../../reproductions/2603.24226-uniscale/README-en.md): Joint Entire-Space data and model scaling.
- `gatesid` · [GateSID](../../reproductions/2603.22916-gatesid/README-en.md): Cold-start-aware semantic/collaborative gates.

### B05

- `aigq` · [AIGQ](../../reproductions/2603.19710-aigq/README-en.md): Hybrid query generation and IL-GRPO.
- `safro` · [SaFRO](../../reproductions/2603.19585-safro/README-en.md): Satisfaction-aware dual relative policy optimization.
- `sort-ranking` · [SORT](../../reproductions/2603.03988-sort-ranking/README-en.md): System optimizations for an industrial Ranking Transformer.
- `quasid` · [QuaSID](../../reproductions/2603.00632-quasid/README-en.md): Qualification-aware SID collision constraints.
- `gpl-prerank` · [Generative Pseudo-Labeling](../../reproductions/2602.20995-gpl-prerank/README-en.md): LLM pseudo-labels improve online pre-ranking.
- `ltv-video-ranking` · [Long-term Value Prediction](../../reproductions/2602.17058-ltv-video-ranking/README-en.md): Position debiasing and long-term value prediction.

### B06

- `rgalign-rec` · [RGAlign-Rec](../../reproductions/2602.12968-rgalign-rec/README-en.md): Ranker-guided latent query alignment.
- `linkedin-feed-sr` · [LinkedIn Feed SR](../../reproductions/2602.12354-linkedin-feed-sr/README-en.md): Industrial long-sequence feed ranking.
- `cadet` · [CADET](../../reproductions/2602.11410-cadet/README-en.md): Ad CTR conditioned on post-candidate context.
- `diffureason` · [DiffuReason](../../reproductions/2602.09744-diffureason/README-en.md): Diffusion latent reasoning and GRPO.
- `sarm` · [SARM](../../reproductions/2602.09401-sarm/README-en.md): MLLM semantic anchors for livestream ranking.
- `ml-dcn` · [ML-DCN](../../reproductions/2602.09194-ml-dcn/README-en.md): Masked low-rank DCN feature crosses.
- `rag-qac` · [RAG-QAC](../../reproductions/2602.01023-rag-qac/README-en.md): Retrieval augmentation and multi-objective alignment for query completion.

<!-- historical-b07:start -->
## 2026 historical scan B07 (9 foundation and infrastructure adapters)

- `tcab` · [Fast A/B/n Testing: Exact Multi-Policy Comparison via Tree-Coupled Feedback Sharing](../../reproductions/2608.12831-tcab/README-en.md): Shares same-decision feedback through maximal coupling and a minimum spanning tree while preserving each adaptive policy's marginal trajectory distribution.
- `olmpool-long-context` · [Cracks in the Foundation: Seemingly Minor Architectural Choices Impact Long Context Extension](../../reproductions/2608.10296-olmpool-long-context/README-en.md): A controlled 7B pool isolates compound effects of normalization, GQA, pretraining length, and sliding-window attention on long-context extension.
- `distillcache` · [DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference](../../reproductions/2608.08878-distillcache/README-en.md): Treats KV eviction as sequential decisions and trains a lightweight policy with stepwise KL rewards to preserve future predictive distributions.
- `autonomy-heads` · [Autonomy-of-Heads: Data-Free Sparse Attention from Frozen Query-Key Geometry](../../reproductions/2608.06849-autonomy-heads/README-en.md): Separates retrieval and streaming heads through spectral effective rank of frozen Q/K projections, without calibration or runtime gating.
- `physics-mm-pretraining` · [Towards Physics of Multimodal Pretraining: Knowledge Flow, Modality Synergy, Early Unification, and Recipes](../../reproductions/2608.05000-physics-mm-pretraining/README-en.md): Controlled experiments study cross-modal knowledge flow, synergy and competition, early unification, and shared attention/norm with modality-specific FFNs.
- `ttcd` · [Learning What to Remember: Test-Time Training via Context Distillation](../../reproductions/2608.01672-ttcd/README-en.md): A long-window teacher uses hidden-state differences to supervise a short-window student's fast weights so limited memory retains useful information.
- `dart` · [DART: Decoded Attention over Recurrent States for Efficient Long-Context Sequence Modeling](../../reproductions/2608.02032-dart/README-en.md): Keeps Mamba-2 chunk-state contributions, decodes token-conditioned keys/values, and attends over state memory.
- `transmem` · [TransMem: Transforming Hidden States into Memory for Large Language Models](../../reproductions/2607.29032-transmem/README-en.md): Transforms sparse frozen-backbone historical states into reusable parametric memory and learns gates with evidence-conditioned self-distillation.
- `c2kv` · [C²KV: Compressed and Composable KV Cache Reuse for Efficient LLM Inference](../../reproductions/2607.17715-c2kv/README-en.md): Compression tokens and structured attention learn position-independent, composable compressed KV representations while jointly training compression and reuse.

<!-- historical-b07:end -->

## Full reproduction and implementation status

| Fidelity | Adapter / paper | Reported paper evidence | Local conclusion |
|---|---|---|---|
| Core mechanism | `state-opd` · [State-OPD](../../reproductions/2610.13238-state-opd/README-en.md) | No industrial A/B; offline interactive-task results | Three arms × three seeds made actual A100 updates with receipts. Accuracy was zero on all eight questions, not a capability gain. |
| Deferred research material | [MagicBeanStalk](../../reproductions/2610.12659-magicbeanstalk/README-en.md) (historical key `magicbeanstalk`, not registered) | No industrial A/B; synthetic math and finance training | Too costly; not reproduced. Full-method acceptance is pending. Code and real failures are retained, with no executable entry point. |
| Core mechanism | `gppo-framework` · [GPPO framework](../../reproductions/2610.13015-gppo-framework/README-en.md) | No industrial A/B; offline proximal optimization | A100 three-seed mechanism diagnosis on eight questions with a separate GRPO control. No stable-improvement claim. |
| Core mechanism | `tapo-trajectory` · [TAPO trajectory](../../reproductions/2610.13020-tapo-trajectory/README-en.md) | No industrial A/B; offline long-trajectory results | Three A100 seeds did not beat GRPO at this budget. Negative results retained. |
| Core mechanism | `cv-opd` · [CV-OPD](../../reproductions/2610.13264-cv-opd/README-en.md) | No industrial A/B; offline visual-dependence results | Actual updates for method and ablation at three A100 seeds each; test means 4.17%/12.5%. Negative results retained. |
| Core mechanism | `oal` · [OAL](../../reproductions/2610.13674-oal/README-en.md) | No industrial A/B; offline attention replacement | A100 three-seed Q/K grouping, calibration, and LoRA conversion. Seed 44 was not better; not an original-scale capability or efficiency comparison. |
| Core mechanism | `replayssm` · [ReplaySSM](../../reproductions/2610.13778-replayssm/README-en.md) | No industrial A/B; state precision and system experiments | Actual low-bit kernels and rollback ran on A100 for three seeds. JIT compatibility limits retained; no quality or HBM gains claimed. |
| Core mechanism | `lewam` · [LeWAM](../../reproductions/2610.12818-lewam/README-en.md) | No industrial A/B; robotics and planning experiments | A100 native joint training and a three-arm new-candidate loop at three seeds; no planning advantage. Single-task scaling diagnostic only. |
| Core mechanism | `smolwam` · [SmolWAM](../../reproductions/2610.13740-smolwam/README-en.md) | No industrial A/B; LIBERO experiments | A100 three-seed teacher KD, curriculum, and new-student loop. Student and no-op both had zero success, not capability improvement. |
| Core mechanism | `near` · [NEAR](../../reproductions/2610.13314-near/README-en.md) | No industrial A/B; offline memory retrieval | A30 shared-bank three-seed run and strict bank-disjoint single-seed run completed. Three seeds on the same data are not independent replications. |
| Core mechanism | `beyond-final-embedding` · [Beyond the Final Embedding](../../reproductions/2610.13277-beyond-final-embedding/README-en.md) | No industrial A/B; offline sparse-memory retrieval | A30 token matching, ID fusion, and query adapter completed. Strict protocol has only two test queries, not the official benchmark. |
| Core mechanism | `skilldreamer` · [SkillDreamer](../../reproductions/2609.01642-skilldreamer/README-en.md) | No industrial A/B; skill and tool tasks | Complete A100 mechanism receipt for three arms × three seeds. CSI, loading, and tools executed but produced zero submissions. Negative result retained. |
| Core mechanism | `synthself` · [SynthSelf](../../reproductions/2610.13113-synthself/README-en.md) | No industrial A/B; multidomain post-training | A100 three-seed aligner and SFT with acquisition and retention evaluation. Did not beat gold-SFT. |
| Core mechanism | `upturn` · [UPTURN](../../reproductions/2610.13672-upturn/README-en.md) | No industrial A/B; inference interventions | All three A100 seeds ran. 42/43 had rescue; 44 did not and the failure is retained. Only one seed has a valid receipt; no all-seed pass claim. |
| Core mechanism | `doublecat-semicat` · [DoubleCat/SemiCat](../../reproductions/2610.13834-doublecat-semicat/README-en.md) | No industrial A/B; diffusion LM results | Corrected core without an extra forward pass passed on A30 at three seeds. One-hot and DoubleCat generation collapse retained. |
| Core mechanism | `soar` · [SOAR](../../reproductions/2610.13157-soar/README-en.md) | No industrial A/B; provenance-consistent reasoning | Actual updates in six A100 method/ablation runs across three seeds. Ablation seed 43 had zero accuracy; four validation items are diagnostic only. |
| Core mechanism | `grpo-difficulty-curriculum` · [GRPO difficulty curriculum](../../reproductions/2610.13669-grpo-difficulty-curriculum/README-en.md) | No industrial A/B; difficulty curricula | Fifteen A30 runs, five arms × three seeds; 151 real updates and 38 exactly skipped equal-value groups. Negative results and previous numerical errors retained. |
| Core mechanism | `progressive-contraction` · [Progressive Contraction](../../reproductions/2610.12933-progressive-contraction/README-en.md) | No industrial A/B; offline teacher-pool contraction | A100 three-seed real Monte Carlo trees, student routing, and updates. Matches full-SFT per seed; no total-cost savings claim. |
| Core mechanism | `uxsid` · [UxSID](../../reproductions/2605.09040-uxsid/README-en.md) | Version 4 full text reports industrial A/B; see detail page | Four MovieLens-100K structures with three A100 seeds passed cache consistency. No stable improvement or substitute for industrial reproduction. |
| Core mechanism | `wegr` · [WeGR](../../reproductions/2610.16979-wegr/README-en.md) | WeChat Search production A/B: orders +2.539%, CTR +1.508% | A100 three-seed MovieLens-100K diagnostic of CoCo-VAE, DHPO, and MSFT. Low performance and no gains over control retained. |
| Core mechanism | `casi` · [CASI](../../reproductions/2610.20293-casi/README-en.md) | Xiaohongshu seven-day randomized production A/B: Advv +3.51% | CPU component with frozen snapshots, exact and permutation credit, and bounded zero-sum advantages. No LLM policy training; high-cost full experiment not reproduced. |
| Core mechanism | `pn-mix` · [PN-Mix](../../reproductions/2610.19605-pn-mix/README-en.md) | No industrial A/B; offline cache quantization | L1 reference with actual bit packing and attention consumption, not pretrained-LM quality or fused-kernel throughput. |
| Core mechanism | `smrc-pmrc` · [SMRC / PMRC](../../reproductions/2610.19844-smrc-pmrc/README-en.md) | No industrial A/B; optimizer training experiments | Real parameter and optimizer-state updates, paper quadratic counterexample, and small MLP control. Full pretraining not reproduced. |
| Core mechanism | `oob-regularization` · [OOB Regularization](../../reproductions/2610.20158-oob-regularization/README-en.md) | No industrial A/B; self-supervised representation experiments | Real Gaussian/spherical anchors and periodic refresh; four arms, three A100 seeds on official CIFAR training subset. No paper-scale or stable capability gain. |
| Core mechanism | `pace-vlm` · [PACE](../../reproductions/2608.27206-pace-vlm/README-en.md) | No industrial A/B; 10% visual tokens retained 93.8% average performance and up to 3.1× TTFT speedup | Auditable APC/DDAE formulas, matched-checkpoint RealWorldQA quality/tokens/latency/memory, and evolve recipes. |
| Core mechanism | `twinkv` · [TwinKV](../../reproductions/2608.27128-twinkv/README-en.md) | No industrial A/B; offline LongBench/LooGLE/RULER/MMLU-Pro including failures | Auditable fixed-budget repair, real Qwen3 KV reconstruction/latency/memory, and evolve attention operator. |
| Core mechanism | `prl-puts` · [PRL-PUTS](../../reproductions/2605.16344-prl-puts/README-en.md) | P2P impressions +0.30% | Two-head Q and Pareto utility sweep; NDCG@10 +39.64%. |
| Core mechanism | `ektm` · [Effective Knowledge Transfer for Multi-Task Recommendation Models](../../reproductions/2605.05730-ektm/README-en.md) | eCPM +3.93% | Task-similarity-driven transfer; NDCG@10 +10.98%. |
| Core mechanism | `adasid` · [AdaSID](../../reproductions/2604.23522-adasid/README-en.md) | GPM +1.16% | Dynamic SID from collision load and semantic compatibility; NDCG@10 -6.30%. |
| Core mechanism | `unirec-coa` · [UniRec](../../reproductions/2604.12234-unirec-coa/README-en.md) | GMV +5.60% | Attribute chains and business preference alignment; NDCG@10 -4.93%. |
| Core mechanism | `uniscale` · [UniScale](../../reproductions/2603.24226-uniscale/README-en.md) | GMV +2.04% | Joint Entire-Space scaling; NDCG@10 -2.20%. |
| Core mechanism | `gatesid` · [GateSID](../../reproductions/2603.22916-gatesid/README-en.md) | GMV +2.60% | Cold-start-aware semantic/collaborative gating; NDCG@10 +34.95%. |
| Core mechanism | `aigq` · [AIGQ](../../reproductions/2603.19710-aigq/README-en.md) | GMV +10.68% | Hybrid query generation and IL-GRPO; NDCG@10 +8.09%. |
| Core mechanism | `safro` · [SaFRO](../../reproductions/2603.19585-safro/README-en.md) | Watch time +0.61% | Satisfaction-aware dual relative policy optimization; NDCG@10 +81.86%. |
| Core mechanism | `sort-ranking` · [SORT](../../reproductions/2603.03988-sort-ranking/README-en.md) | Orders +6.35% | Industrial Ranking Transformer system optimization; NDCG@10 -13.11%. |
| Core mechanism | `quasid` · [QuaSID](../../reproductions/2603.00632-quasid/README-en.md) | GMV-S2 +2.38% | Qualification-aware SID collision constraint; NDCG@10 -0.55%. |
| Core mechanism | `gpl-prerank` · [Generative Pseudo-Labeling](../../reproductions/2602.20995-gpl-prerank/README-en.md) | CTR +3.07% | LLM pseudo-labels for online pre-ranking; NDCG@10 +12.84%. |
| Core mechanism | `ltv-video-ranking` · [Long-term Value Prediction](../../reproductions/2602.17058-ltv-video-ranking/README-en.md) | VV +2.49% | Position debiasing and long-term value; NDCG@10 +9.73%. |
| Core mechanism | `rgalign-rec` · [RGAlign-Rec](../../reproductions/2602.12968-rgalign-rec/README-en.md) | CTR@3 incremental over QE-Rec +0.13% | Ranker-guided latent query alignment; NDCG@10 -14.03%. |
| Core mechanism | `linkedin-feed-sr` · [LinkedIn Feed SR](../../reproductions/2602.12354-linkedin-feed-sr/README-en.md) | Time spent +2.10% | Industrial long-sequence feed ranking; NDCG@10 -0.12%. |
| Core mechanism | `cadet` · [CADET](../../reproductions/2602.11410-cadet/README-en.md) | CTR +11.04% | Post-candidate-context-conditioned ad CTR; NDCG@10 -6.20%. |
| Core mechanism | `diffureason` · [DiffuReason](../../reproductions/2602.09744-diffureason/README-en.md) | Ad consumption +1.15% | Diffusion latent reasoning and GRPO; NDCG@10 -6.50%. |
| Core mechanism | `sarm` · [SARM](../../reproductions/2602.09401-sarm/README-en.md) | Watch count +1.19% | MLLM semantic anchors for livestream ranking; NDCG@10 +44.74%. |
| Core mechanism | `ml-dcn` · [ML-DCN](../../reproductions/2602.09194-ml-dcn/README-en.md) | Platform-wide CTR +1.89% | Masked low-rank DCN feature crossing; NDCG@10 -2.08%. |
| Core mechanism | `rag-qac` · [RAG-QAC](../../reproductions/2602.01023-rag-qac/README-en.md) | Suggestions taken +3.46% | RAG and multi-objective query completion; NDCG@10 -4.48%. |
| Core mechanism | `dynamic-codebook` · [Dynamic Codebook](../../reproductions/2608.21012-dynamic-codebook/README-en.md) | Consumption +0.792%; decoding FLOPs about -48% | Dynamic codebook and collision code; NDCG@10 -18.73%, negative result retained. |
| Core mechanism | `netflix-mediafm` · [Netflix MediaFM](../../reproductions/2608.18322-netflix-mediafm/README-en.md) | Search playthrough +0.36% | Frozen multimodal features and query scoring; NDCG@10 -9.52%. |
| Core mechanism | `ogr` · [OGR](../../reproductions/2608.17613-ogr/README-en.md) | Effective Views +1.120% | Unified SID, slate planning, and conservative alignment; NDCG@10 +13.25%. |
| Core mechanism | `inthq` · [IntHQ](../../reproductions/2608.09634-inthq/README-en.md) | UVCTR +1.60% | Hierarchical task queries; NDCG@10 -7.38%. |
| Core mechanism | `pushdualgen` · [PushDualGen](../../reproductions/2608.07989-pushdualgen/README-en.md) | Effective play rate +8.50%, dissatisfaction -37.70% | SID then optional copy; NDCG@10 +1.19%. |
| Core mechanism | `recharness` · [RecHarness](../../reproductions/2607.29241-recharness/README-en.md) | ADVV +2.084%, revenue +0.534% | UCB budget routing; NDCG@10 -9.02%. |
| Core mechanism | `gala` · [GALA](../../reproductions/2607.29213-gala/README-en.md) | Orders +0.55% | Gated multimodal behavior alignment; NDCG@10 -5.60%. |
| Core mechanism | `feedback-policy` · [Feedback Policy](../../reproductions/2607.27789-feedback-policy/README-en.md) | Revenue +4.506%, ADVV +4.621% | Feedback policy and conservative increments; NDCG@10 +2.76%. |
| Core mechanism | `real-estate-rerank` · [Real Estate Re-ranker](../../reproductions/2607.14835-real-estate-rerank/README-en.md) | CTR +5.3%, property tour bookings +4.8% | Text/attribute set reranking; NDCG@10 -8.21%. |
| Core mechanism | `adaptive-ad-load` · [Adaptive Ad Load](../../reproductions/2607.14418-adaptive-ad-load/README-en.md) | Revenue +36.8%, conversion -1.1% | Constrained ad load; unchanged NDCG@10. |
| Core mechanism | `guess-where-you-go` · [Gwhere](../../reproductions/2607.26073-guess-where-you-go/README-en.md) | P-CTR +5.83%, U-CTR +6.20% | Spatiotemporal SID next POI; NDCG@10 +9.38%. |
| Core mechanism | `genpage` · [GenPage](../../reproductions/2606.31031-genpage/README-en.md) | Core engagement +0.24%, latency -20% | Joint page utility; NDCG@10 -3.98%. |
| Core mechanism | `journeyformer` · [JourneyFormer](../../reproductions/2606.19108-journeyformer/README-en.md) | Bookers +0.55%, booked nights +0.82% | Long and short journey encoding; NDCG@10 -2.77%. |
| Core mechanism | `l2rec` · [L2Rec](../../reproductions/2605.26717-l2rec/README-en.md) | CTR +9.24%, reply rate +3.15% | Personalized dual-view adaptation; NDCG@10 -5.04%. |
| Core mechanism | `qgs` · [QGS](../../reproductions/2605.25514-qgs/README-en.md) | CTR +0.62%, PV duration +3.55% | Query-conditioned SID scoring; NDCG@10 +0.73%. |
| Core mechanism | `tubifm` · [TubiFM](../../reproductions/2605.23702-tubifm/README-en.md) | Search TVT +3.9%, carousel TVT +0.30% | Unified three-task model; NDCG@10 +0.45%. |
| Core mechanism | `pearl-percentile` · [PEARL](../../reproductions/2605.21752-pearl-percentile/README-en.md) | Watch duration +2.10%, report rate -6.91% | Multi-sample percentile; NDCG@10 -10.65%. |
| Core mechanism | `dadf` · [DADF](../../reproductions/2605.17863-dadf/README-en.md) | Time spent +0.649%, production MAE -12.57% | Frozen-base multiplicative residual; unchanged NDCG@10. |
| Core mechanism | `connectionmind` · [ConnectionMind](../../reproductions/2608.10187-connectionmind/README-en.md) | Meta multi-week A/B with tens of millions of users: impressions +0.33%, watch time +0.43%, video sessions +0.22% | Delicious-2K path SFT, GRPO, and distilled mixed inference. NDCG@10 -7.44%, negative result retained. |
| Core mechanism | `dream` · [DREAM](../../reproductions/2608.09408-dream/README-en.md) | Taobao fine ranking and reranking: IPV +2.71%, Core IPV +3.06%, GMV +1.31% | Intent, strategy memory, safe compilation, and dual-loop gates. NDCG@10 +39.36% but head share +94.37%. |
| Core mechanism | `gas` · [GAS](../../reproductions/2608.12209-gas/README-en.md) | Multimodal: from-scratch overall 47.25→48.25; inference overhead 0% | MoT, NEP, and EMA; Fashion-MNIST QA 61.1%→63.5%, deployment parameter overhead 0%. |
| Core mechanism | `sona` · [Sona](../../reproductions/2608.11015-sona/README-en.md) | Yandex Music active users +4.53%, duration +6.30%, likes +11.42% | History compression, SID decoder, and ranker. NDCG@10 -92.05%, negative transfer retained. |
| Core mechanism | `metastrategy` · [MetaStrategy](../../reproductions/2608.09440-metastrategy/README-en.md) | Taobao click PV +2.11%, IPV +3.12%, transaction value +2.83% | Typed bundles and deterministic compiler. NDCG@10 -8.51%, head share -42.94%. |
| Core mechanism | `crsd` · [CRSD](../../reproductions/2510.11056-crsd/README-en.md) | Meituan AdCTR +0.91%, AdCVR +1.06%, GTV +0.40% | Two-stage reasoning distillation; MovieLens-100K NDCG@10 -2.14%, negative transfer retained. |
| Core mechanism | `twin-v2` · [TWIN-V2](../../reproductions/2407.16357-twin-v2/README-en.md) | Kuaishou watch time in three settings +0.672%/+0.800%/+0.728%, main traffic | Hierarchical compression with GSU/ESU; NDCG@10 +22.45%. |
| Core mechanism | `medusa` · [Medusa](../../reproductions/2401.10774-medusa/README-en.md) | LLM: Medusa-1 2.2×, Medusa-2 2.3–3.6× | Three future heads on WikiText-2; backbone calls -50%, identical outputs. |
| Core mechanism | `awq` · [AWQ](../../reproductions/2306.00978-awq/README-en.md) | LLM: TinyChat more than 3× over FP16 | Activation-aware W4; output MSE -4.22%. |
| Core mechanism | `smolvlm` · [SmolVLM](../../reproductions/2504.05299-smolvlm/README-en.md) | Multimodal: competitive at lower visual token cost | Pixel-shuffle reduces visual tokens 16→4; Fashion-MNIST QA +19.0 points. |
| Core mechanism | `siglip2` · [SigLIP 2](../../reproductions/2502.14786-siglip2/README-en.md) | Multimodal: improved semantics and localization on several image–text benchmarks | Sigmoid contrastive loss and masked-view self-distillation; Fashion-MNIST QA +56.9 points. |
| Core mechanism | `llava` · [LLaVA](../../reproductions/2304.08485-llava/README-en.md) | Multimodal: ScienceQA 92.53% | MLP projector versus linear connector -3.4 points; negative small-data result retained. |
| Core mechanism | `blip2` · [BLIP-2](../../reproductions/2301.12597-blip2/README-en.md) | Multimodal: zero-shot VQAv2 +8.7 points over Flamingo-80B | Four-query Q-Former reduces tokens 16→4; accuracy -5.3 points, negative result retained. |
| Core mechanism | `speculative-decoding` · [Speculative Decoding](../../reproductions/2211.17192-speculative-decoding/README-en.md) | LLM: T5-XXL 2–3× with unchanged distribution | Low-rank draft and exact verification; target calls -75%, identical outputs. |
| Core mechanism | `clip` · [CLIP](../../reproductions/2103.00020-clip/README-en.md) | Multimodal: zero-shot ImageNet matches supervised ResNet-50 | Bidirectional contrastive learning; Fashion-MNIST image–text accuracy 72.0%, shuffled images 10.3%. |
| Core mechanism | `sim` · [SIM](../../reproductions/2006.05639-sim/README-en.md) | Alibaba CTR +7.1%, RPM +4.4%, main traffic | GSU/ESU long-history retrieval; NDCG@10 +32.97%. |
| Core mechanism | `dme` · [DME](../../reproductions/2608.02148-dme/README-en.md) | Douyin Search Lifetime +0.1%, internal offline +2.92% | Typed latent and cross-reconstruction; MovieLens-100K NDCG@10 -8.84%, negative result retained. |
| Core mechanism | `steps` · [STEPS](../../reproductions/2608.01949-steps/README-en.md) | Active days +0.2843%, permission disablement -1.9089%; fully rolled out | Planning/execution/filtering loop; MovieLens-100K NDCG@10 +66.05% |
| Core mechanism | `spear` · [SPEAR](../../reproductions/2608.01738-spear/README-en.md) | Query-view CTR +0.259 and reading depth +0.733; fully rolled out | Dual embeddings and multiplicative gate; MovieLens-100K NDCG@10 +26.95% |
| Core mechanism | `open-language-model` · [OpenLanguageModel](../../reproductions/2607.16669-open-language-model/README-en.md) | Standalone LLM: 90.6% weak scaling on four GPUs; no online A/B | `olm_composable` genome; essentially equivalent WikiText-2 PPL at matched budget, verifying compositional semantics |
| Core mechanism | `gryphon-v2` · [Gryphon-v2](../../reproductions/2608.06213-gryphon-v2/README-en.md) | Yandex Music active users +1.41% | Dual rollout/impression teacher distillation; NDCG@10 -26.84%, retaining negative transfer |
| Core mechanism | `degr` · [DEGR](../../reproductions/2608.04809-degr/README-en.md) | JD.com UCTR +1.22%, PV +0.20% | Diversity and adaptive-reward ORPO; NDCG unchanged, head share -1.21% |
| Core mechanism | `rd-attnres` · [RD-AttnRes](../../reproductions/2608.01075-rd-attnres/README-en.md) | Standalone LLM: 120M/343M PPL -2.97%/-2.43% | PPL +0.61% versus Block AttnRes (worse); QK/V routing JS=0.00489 |
| Core mechanism | `retoken` · [ReToken](../../reproductions/2607.28627-retoken/README-en.md) | Visual Haystacks: Qwen3-VL-8B +13.4 points; no online A/B | One retrieval target and value-cache Top-K; WikiText-2 PPL +3.70% (worse) |
| Core mechanism | `ccformer` · [CCFormer](../../reproductions/2607.28070-ccformer/README-en.md) | Tencent Video CTR +3.57%, ad revenue +1.71%; full rollout after the experiment | Field-specific ID/content gates and hierarchical history compression; MovieLens-1M NDCG@10 +22.44%, tokens 24→12 |
| Core mechanism | `open-web-ufm` · [Open Web UFM](../../reproductions/2607.28019-open-web-ufm/README-en.md) | Teads 50/50 A/B: CTR +2.13%, eCPC -1.13%, visit rate +2.37% | Two-crop contrastive pretraining and next-item proxy; MovieLens-1M NDCG@10 +0.00%, preserving the null result |
| Core mechanism | `rocs` · [ROCS](../../reproductions/2607.27744-rocs/README-en.md) | Meta retrieval up to 3× QPS; short-video ranking LogLoss -0.5%, QPS +50% | Request-once/candidate-late interaction; MovieLens-1M NDCG@10 +8.19%, in-process candidate scoring 129.58× |
| Core mechanism | `wide` · [WIDE](../../reproductions/2607.28418-wide/README-en.md) | Standalone LLM: at 50% sparsity, kernel prefill 1.98× and decode 4.95× | Per-token head/FFN group Top-K; WikiText-2 PPL +0.81% (worse), no kernel speedup in dense PyTorch |
| Core mechanism | `asarl` · [ASARL](../../reproductions/2607.26593-asarl/README-en.md) | QQ Channels CTR +2.69%, group GSB +16.66%, 12 million DAU | Reason/Critic/Gen plus SCT/PGO/SD; NDCG@10 -72.72%, preserving negative transfer on the proxy |
| Core mechanism | `oxygenrec-v2` · [OxygenREC-v2](../../reproductions/2607.24255-oxygenrec-v2/README-en.md) | JD.com UCTCVR +1.61%–+4.44%, homepage GMV +21.21% | Behavioral instructions and privileged distillation; NDCG@10 -54.09%, preserving negative transfer on the proxy |
| Core mechanism | `reco-reward` · [RecoReward](../../reproductions/2607.25901-reco-reward/README-en.md) | Kuaishou effective-user penetration +0.265%, outbound exposure +0.791% | RAS target/non-target reward; Hit@10 -16.00%, retaining the negative result |
| Core mechanism | `twice` · [TWICE](../../reproductions/2607.25404-twice/README-en.md) | Expected revenue +2.486%, conversion +2.061%; full rollout | Dual clocks and delay CDF; NDCG@10 +14.31% |
| Core mechanism | `swag-bid` · [SWAG](../../reproductions/2607.25233-swag-bid/README-en.md) | GMV +3.42%, ROAS +5.65% | Sliding-window masked planner; NDCG@10 +0.00% |
| Core mechanism | `youtube-freshness` · [YouTube Freshness](../../reproductions/2607.23749-youtube-freshness/README-en.md) | 1-day new-release engagement +4.33% | IPS, bias tower, and uncertainty; head share -28.72% |
| Core mechanism | `melo` · [Melo](../../reproductions/2607.23718-melo/README-en.md) | System-level A/B retention >2pp | Grounding and retries; fresh Hit@10 +50.00%, with system attribution reported separately |
| Core mechanism | `penelope` · [Penelope](../../reproductions/2607.25915-penelope/README-en.md) | Standalone LLM: improved structured-reasoning accuracy and compute | Two-step localized recurrence; composite loss -0.63% |
| Core mechanism | `mim` · [MIM](../../reproductions/2502.00321-mim/README-en.md) | Taobao CTR +14.14%, RPM +4.12% | Masked multimodal alignment and CiUBM; NDCG@10 +0.94%, Hit@10 declined |
| Core mechanism | `filterllm` · [FilterLLM](../../reproductions/2502.16924-filterllm/README-en.md) | Cold-PV +5.13%, GMV +10.86% | Text-to-user distribution; NDCG@10 -9.82%, retaining the negative result |
| Core mechanism | `fuxi-alpha` · [FuXi-α](../../reproductions/2502.03036-fuxi-alpha/README-en.md) | Songs played +4.67%, play duration +5.10% | Three-channel interaction; Hit@10 slightly higher, NDCG@10 -4.25% |
| Core mechanism | `recgpt-v2` · [RecGPT-V2](../../reproductions/2512.14503-recgpt-v2/README-en.md) | Taobao CTR +2.98%, IPV +3.71%, NER +11.46% | Hierarchical agents and constrained routing; NDCG@10 +18.52% |
| Core mechanism | `higr` · [HiGR](../../reproductions/2512.24787-higr/README-en.md) | Tencent plays +1.73%, watch time +1.22% | Hierarchical SID slate and ORPO; NDCG@10 -12.32% |
| Core mechanism | `drl-put` · [DRL-PUT](../../reproductions/2509.05292-drl-put/README-en.md) | Pinterest revenue +0.27%, CTR +1.62% | Logged-bandit policy weight adjustment; NDCG@10 +19.13% |
| Core mechanism | `adaf2m2` · [AdaF²M²](../../reproductions/2501.15816-adaf2m2/README-en.md) | Douyin active days +1.37%, duration +1.89% | Feature-mask multi-forward with adapter; NDCG@10 +2.42% |
| Core mechanism | `mgoe` · [MGOE](../../reproductions/2506.10520-mgoe/README-en.md) | Alibaba GMV +16.46%, CVR +5.88% | Macro task graph experts; NDCG@10 +7.03% |
| Core mechanism | `click-a-buy-b` · [Click A Buy B](../../reproductions/2507.15113-click-a-buy-b/README-en.md) | Pinterest primary business metric +0.25% | CABA/CABB with taxonomy; NDCG@10 +33.70% |
| Core mechanism | `mosaic` · [Mosaic](../../reproductions/2607.24015-mosaic/README-en.md) | Meta three surfaces: +0.10%/+0.15%/+0.28% | Four specialists with MRM and CRL; NDCG@10 +3.49%, Hit@10 -7.69% |
| Core mechanism | `unir2` · [UniR²](../../reproductions/2607.24439-unir2/README-en.md) | Kuaishou plays +1.177%, like rate +2.560%; Lite gift spending +2.569% | DQ-PCA and ranking LoRA; SID code accuracy +34.04%, NDCG@10 -13.19% |
| Core mechanism | `core-relevance` · [CORE](../../reproductions/2607.24417-core-relevance/README-en.md) | Meituan NDCG@5 +0.20%, Badcase@5 -15.9% | Cascaded heads, step-GRPO, and PostCoT; NDCG@5 +0.98%, Badcase@5 -50.00%, accuracy -0.52 points |
| Core mechanism | `data-orchestra` · [DataOrchestra](../../reproductions/2607.24717-data-orchestra/README-en.md) | Standalone LLM: consistent average benchmark gains at 0.5B/1.5B/7B | Per-example routing; PPL -1.03% versus fixed cleaning, +8.60% versus raw (worse) |
| Core mechanism | `native-sparse-attention` · [NSA](../../reproductions/2502.11089-native-sparse-attention/README-en.md) | Standalone LLM: quality at least as good as full attention, with significant speedups in three stages at 64K | Three-path sparse attention; attention edges -43.65%, PPL -3.17% |
| Core mechanism | `gated-attention` · [Gated Attention](../../reproductions/2505.06708-gated-attention/README-en.md) | Standalone LLM: improved scaling, stability, and long-context extrapolation | Per-head post-SDPA gate; PPL -0.72% |
| Core mechanism | `muon` · [Muon](../../reproductions/2502.16982-muon/README-en.md) | Standalone LLM: about 2× compute efficiency | Orthogonal matrix updates ran; PPL +5.61% (worse) |
| Core mechanism | `wide-deep` · [Wide & Deep](../../reproductions/1606.07792-wide-deep/README-en.md) | Google Play acquisition +3.9% | Wide feature crosses and deep tower; NDCG@10 +5.45% |
| Core mechanism | `deepfm` · [DeepFM](../../reproductions/1703.04247-deepfm/README-en.md) | User-approved classic exception | Shared embeddings across FM and deep paths; NDCG@10 +23.58% |
| Core mechanism | `youtube-dnn` · [YouTube DNN](../../reproductions/recsys2016-youtube-dnn-youtube-dnn/README-en.md) | User-approved classic exception; no quantified lift disclosed | Nonlinear user tower; NDCG@10 -6.61%, retaining the negative result |
| Core mechanism | `esmm` · [ESMM](../../reproductions/1804.07931-esmm/README-en.md) | User-approved classic exception | Entire-space CTR×CVR; mean AUC +1.69% |
| Core mechanism | `mmoe` · [MMoE](../../reproductions/kdd2018-mmoe-mmoe/README-en.md) | User-approved classic exception | Shared experts and task-specific gates; mean AUC +1.30% |
| Core mechanism | `ple` · [PLE](../../reproductions/recsys2020-ple-ple/README-en.md) | User-approved classic exception | Shared and task-specific experts; mean AUC +1.34% |
| Core mechanism | `dcn-v2` · [DCN-V2](../../reproductions/2008.13535-dcn-v2/README-en.md) | Classic exception: significant online result without disclosed lift | Low-rank cross experts; NDCG@10 +22.87% |
| Core mechanism | `dien` · [DIEN](../../reproductions/1809.03672-dien/README-en.md) | CTR +20.7%, eCPM +17.1% | GRU, auxiliary objective, and interest evolution; NDCG@10 -1.98% |
| Core mechanism | `bst` · [BST](../../reproductions/1905.06874-bst/README-en.md) | CTR +7.57% | Target-token Transformer; NDCG@10 +20.29% |
| Core mechanism | `cs3` · [CS3](../../reproductions/2604.19269-cs3/README-en.md) | Revenue +8.356%/+1.366%/+2.177% | Cycle/sync/cascade; NDCG@10 -16.06% |
| Core mechanism | `cq-sid` · [CQ-SID](../../reproductions/2605.14434-cq-sid/README-en.md) | GMV +1.15%, UCTCVR +0.40% | Category SID and EG-GRPO; NDCG@10 +1.66% |
| Core mechanism | `switch-transformer` · [Switch Transformer](../../reproductions/2101.03961-switch-transformer/README-en.md) | Standalone LLM: about 7× faster pretraining | Top-1 MoE; 30-step PPL -3.29% |
| Core mechanism | `mamba` · [Mamba](../../reproductions/2312.00752-mamba/README-en.md) | Standalone LLM: up to about 5× faster inference | Selective scan; 30-step PPL +48.82% (worse) |
| Core mechanism | `switch-attention` · [Switch Attention](../../reproductions/2603.26380-switch-attention/README-en.md) | Standalone LLM: >4× decoding at 32K | Dynamic full/local router; 30-step PPL +0.19% (slightly worse) |
| Core mechanism | `onemall` · [OneMall](../../reproductions/2601.21770-onemall/README-en.md) | Product-card GMV +13.01%, short-video orders +15.32%, livestream orders +2.78% | Surface prompts, SID, and cross-behavior fusion; NDCG@10 +4.33% |
| Core mechanism | `dos` · [DOS](../../reproductions/2602.04460-dos/README-en.md) | Meituan revenue +1.15% | Dual-stream ORQ; NDCG@10 +11.26% |
| Core mechanism | `mdl` · [MDL](../../reproductions/2602.07520-mdl/README-en.md) | Douyin LT30 +0.0626%, rewrite -0.3267% | Three token types and domain attention; NDCG@10 +13.34%, head share +73.43% |
| Core mechanism | `hisac` · [HiSAC](../../reproductions/2602.21009-hisac/README-en.md) | Taobao CTR +1.65% | Hierarchical interest agents; NDCG@10 +1.31% |
| Core mechanism | `pinclip` · [PinCLIP](../../reproductions/2603.03544-pinclip/README-en.md) | Fresh Repin +15%, new ads click +8.7% | Neighbor alignment NDCG@10 -1.41%; reported gains did not transfer |
| Core mechanism | `pin-scale` · [Pin-SCALE](../../reproductions/sigir2026-pin-scale-pin-scale/README-en.md) | Repin +3.67%, DAU +0.05% | Engagement-aware SID; NDCG@10 +13.61%, fresh Hit +50.00% |
| Core mechanism | `causal-retrieval` · [Causal Retrieval](../../reproductions/2607.14161-causal-retrieval/README-en.md) | Triggering -85%, sessions +0.26%, Save +1.10% | DR uplift triggering; synthetic-treatment NDCG@10 +80.77% |
| Core mechanism | `podcast-mtl` · [Podcast MTL](../../reproductions/2601.02306-podcast-mtl/README-en.md) | eCPS -22%, streams +18%–24% | Shared MTL NDCG@10 -20.63%, showing negative transfer |
| Core mechanism | `engram` · [Engram](../../reproductions/2601.07372-engram/README-en.md) | Standalone LLM: MMLU +3.4, BBH +5.0, HumanEval +3.0 | O(1) memory integrated into evolve; 30-step PPL +50.12% (worse) |
| Core mechanism | `looped-latent-attention` · [Looped Latent Attention](../../reproductions/2607.15456-looped-latent-attention/README-en.md) | Standalone LLM: up to 32× KV compression | Integrated into evolve; parameters -42.28%, PPL +5.56% |
| Core mechanism | `gaugequant` · [GaugeQuant](../../reproductions/2607.20757-gaugequant/README-en.md) | Standalone LLM: LLaMA-2 7B W4A4 PPL 8.22→6.73 | Integrated into evolve; local W4A4 STE PPL -1.56% |
| Core mechanism | `nova` · [NOVA](../../reproductions/2606.27243-nova/README-en.md) | Tencent GMV +1.25%/+1.70%/+2.02% for three pCVR objectives | Four-level verification cascade, failure direction, and architecture gradient actually integrated into evolve |
| Core mechanism | `evorec` · [EvoRec](../../reproductions/2606.28368-evorec/README-en.md) | Revenue +1.85%, CTR +1.02% | Three generations of dual-track model and method evolution with persistent skill memory |
| Complete core pipeline | `tokenmixer-large` · [TokenMixer-Large](../../reproductions/2602.06563-tokenmixer-large/README-en.md) | Orders +1.66%, payment GMV +2.98% | Mixing/reverting, two SwiGLUs, interval residuals, and auxiliary losses actually trained |
| Core mechanism | `msn` · [MSN](../../reproductions/2602.07526-msn/README-en.md) | Watch time +0.2958%, finish rate +0.2071% | Product-Key Memory, sparse top-k reads, and gate |
| Core mechanism | `idproxy` · [IDProxy](../../reproductions/2603.01590-idproxy/README-en.md) | Content interactions +0.50%, ad ADVV +1.93% | Contrastive loss 6.073→5.358; NDCG@10 +5.32% |
| Core mechanism | `glide` · [GLIDE](../../reproductions/2603.17540-glide/README-en.md) | Non-habitual streaming +5.4%, new-show discovery +14.3% | Residual Semantic ID generation and separate long/short-term prompts |
| Core mechanism | `genrec` · [GenRec](../../reproductions/2604.14878-genrec/README-en.md) | Clicks +9.5%, transactions +8.7% | Page-wise NTP, Token Merger, and GRPO-SR/NLL |
| Core mechanism | `genrec-netflix` · [Netflix GenRec](../../reproductions/2608.10257-genrec-netflix/README-en.md) | 10% of traffic for 4 weeks; short-term homepage engagement +0.115%, long-term primary metric +0.006% | SmolLM2 LoRA, catalog head, and reward weighting; NDCG@10 +35.07% (one seed) |
| Core mechanism | `rankgraph2` · [RankGraph-2](../../reproductions/2606.18379-rankgraph2/README-en.md) | CTR +0.96%, CVR +2.75% | Debiased edges, multi-hop PPR, and two-level residual index; NDCG@10 +109.65% |
| Core mechanism | `solaris` · [SOLARIS](../../reproductions/2604.12110-solaris/README-en.md) | Full-traffic top-line revenue +0.67% | Future-pair predictor, asynchronous latent cache, and fallback |
| Core mechanism | `minimax-sparse-attention` · [MiniMax Sparse Attention](../../reproductions/2606.13392-minimax-sparse-attention/README-en.md) | Standalone LLM: 1M-context attention compute -28.4× (reduction, as reported) | Attention pairs -79.95%, PPL +0.41% (worse), unfused MPS runtime +67.58% |
| Core mechanism | `pinequalizer` · [PinEqualizer](../../reproductions/2607.22518-pinequalizer/README-en.md) | Related Pins ranking architecture: all-fresh +8.63%, underexplored +6.57% | MovieLens-1M fresh NDCG +448.62%, underexplored exposure +471.02%, but overall NDCG -16.44% |
| Core mechanism | `gzip-sparse-attention` · [Gzip-guided Sparse Attention](../../reproductions/2607.21752-gzip-sparse-attention/README-en.md) | Standalone LLM: PG-19 BPB 2.34→1.71 versus BigBird | At matched parameter count and 256-token context, BPB +1.02% versus BigBird (worse), attention edges -70.82% |
| Core mechanism | `windowed-mtp` · [Windowed-MTP](../../reproductions/2607.21535-windowed-mtp/README-en.md) | Standalone LLM serving: 1M step latency metric +28.3%–+44.3% as reported | 16K KV reads -99.56%, MPS draft latency -50.25%; exactly identical outputs, acceptance 41.67%→25.00% |
| Core mechanism | `adadsf` · [AdaDSF](../../reproductions/2607.21291-adadsf/README-en.md) | Standalone LLM: at 80% retention, PPL 21.6→18.9 versus MoD | Matched teacher and budget: PPL +0.30% versus Uniform MoD (worse) |
| Core mechanism | `barge` · [BARGE](../../reproductions/2607.21028-barge/README-en.md) | Tencent CTR +0.60%, unique clicking users +1.34%, reading time +1.70% | OSQ+ICA+HPR+DPD; NDCG@10 +85.77%, but head share +165.02% |
| Core mechanism | `mobius-rope` · [Möbius RoPE](../../reproductions/2607.21405-mobius-rope/README-en.md) | Standalone LLM: needle score 63.3%→90.3%, PPL flat | PPL -0.03%, single-seed needle -2.08 points; paper gains did not transfer |
| Core mechanism | `naju` · [Naju](../../reproductions/2607.21000-naju/README-en.md) | Standalone LLM: WikiText-103 PPL 28.31→26.20 | Preserve-first gates correct; WikiText-2 PPL +25.67% (worse) |
| Core mechanism | `dynamic-rubric` · [DynamicRubric](../../reproductions/2607.20083-dynamic-rubric/README-en.md) | WeChat Search: statistically significant at full AI traffic; exact lift undisclosed | Alpaca preference accuracy 83.89%→87.78%, relative +4.64% |
| Core mechanism | `tsgr` · [TSGR](../../reproductions/2607.18796-tsgr/README-en.md) | Taobao IPV +0.43%, transactions +1.12%, GMV +1.64% | Parallel value SID and joint VRM; NDCG@10 +115.73% |
| Core mechanism | `off-context-grpo` · [Off-Context GRPO](../../reproductions/2607.19313-off-context-grpo/README-en.md) | Pure LLM: Qwen2.5-7B +13.8% over GRPO | Official GSM8K Pass@1 2.67%→3.33%, +25.00% relative |
| Core mechanism | `ramp` · [RAMP](../../reproductions/2607.17473-ramp/README-en.md) | Industrial CVR Total Advertiser Value >+3% | Traffic with restricted personalized fields: NDCG@10 +417.23% |
| Core mechanism | `whale` · [WHALE](../../reproductions/2607.17017-whale/README-en.md) | Meta primary metric +0.113%, Metric 1 +0.824% | Progressive Wukong–HSTU exchange; NDCG@10 -83.20%, gains did not transfer |
| Core mechanism | `tmallgs` · [TMallGS](../../reproductions/2607.13398-tmallgs/README-en.md) | Tmall UCTCVR +1.38%, GMV +1.52% | Field-adaptive gated Transformer; NDCG@10 +310.42% |
| Core mechanism | `long-history-transformer` · [Long-History User Transformers](../../reproductions/2607.14331-long-history-transformer/README-en.md) | Yandex Search primary metric +2.77%, Revenue +2.26% | Cached full history plus recent online encoder; NDCG@10 +57.08% |
| Core mechanism | `downstream-rewards` · [Downstream Rewards](../../reproductions/2607.14192-downstream-rewards/README-en.md) | Across surfaces +0.11%–+0.36% | Selected long-term reward head; NDCG@10 -5.10%, gains did not transfer |
| Core mechanism | `recgpt-mobile` · [RecGPT-Mobile](../../reproductions/2605.04726-recgpt-mobile/README-en.md) | Taobao CLICK +1.8%, PAY +2.7%, GMV +2.5% | Real 135M LoRA semantic intent accuracy +100.00%; INT8 relative -6.25%, size -53.68%, trigger skipped 96.21% of inference calls |
| Core mechanism | `sort-gen` · [SORT-Gen](../../reproductions/2505.07197-sort-gen/README-en.md) | Versus deployed baseline: CLICK +4.13%, GMV +8.10% | Ordered regression plus single-pass mask-driven queue generation; Click +5.10%, Pay +8.46%, GMV proxy +9.00%, ILAD +2.89% |
| Core mechanism | `recgpt-v3` · [RecGPT-V3](../../reproductions/2607.15591-recgpt-v3/README-en.md) | Taobao Feed IPV +1.28%, CTR +1.00%, GMV +3.97%; resources -52.4% | After two-stage teacher distillation: NDCG@10 +36.96%, memory tokens -65%, latent slots -90%, but head share +71.43% |
| Core mechanism | `slimper` · [SlimPer](../../reproductions/2607.12281-slimper/README-en.md) | Statistically significant full-traffic lift on Instagram Reels/Feed; exact lift undisclosed | Parameter-matched NDCG@10 +1.29%; attention-score elements -94.12% |
| Core mechanism | `tokenminds` · [TokenMinds](../../reproductions/2606.25147-tokenminds/README-en.md) | YouTube SFV Engaged Users +0.11%, Satisfied Engagement +0.62%, full traffic across multiple surfaces | Actual dense + SID user-token dual-output training; one-seed NDCG@10 -0.35%, no stable improvement claim |
| Core mechanism | `recap` · [RECAP](../../reproductions/2607.15730-recap/README-en.md) | Kuaishou usage time per user +0.139% | GRPO reward 0.5245→0.7096, but NDCG@10 -6.77% and head share -20.27% |
| Core mechanism | `uame` · [UAME](../../reproductions/2607.17092-uame/README-en.md) | LongView up to +1.614%, Forward up to +1.598% | Three public proxy inputs: NDCG@10 -62.28%; online gains did not transfer |
| Core mechanism | `conv-llm` · [Convolution for LLMs](../../reproductions/2607.18413-conv-llm/README-en.md) | Pure LLM: Qwen3-1.7B PPL 13.42→12.79 | Matched-budget WikiText-2 test PPL 305.664→304.787 (-0.29%) |
| Core mechanism | `ppl-factory` · [PPL-Factory](../../reproductions/2607.18199-ppl-factory/README-en.md) | Pure LLM with 10% of data: GSM8K +0.9 and MATH +4.8 points | 20% middle selection had 1.79% worse PPL than random; easy selection was best |
| Core mechanism | `fluid` · [FLUID](../../reproductions/2605.21832-fluid/README-en.md) | QWD +0.55%, cold-start room plays +2.05% | Without candidate IDs: NDCG -20.63%, fresh Hit +100.00%, head share -58.32% |
| Core mechanism | `memory-grafting` · [Memory Grafting](../../reproductions/2605.20948-memory-grafting/README-en.md) | Pure LLM: benchmark average 53.86 | PPL -3.59% versus Transformer, but +0.03% versus Engram; did not beat directly trainable memory |
| Core mechanism | `mhc` · [mHC](../../reproductions/2512.24880-mhc/README-en.md) | Pure LLM: benchmark +2.1%–2.3% | No PPL improvement; residual row/column errors reached zero, spectral norm 1.089→1.000 |
| Core mechanism | `degre` · [DeGRe](../../reproductions/2605.25749-degre/README-en.md) | Taobao Flash CTR +2.85%, GMV +3.75% | Evaluator→beam→dense distillation; NDCG@10 +3.31% |
| Core mechanism | `harness-lm` · [HARNESS-LM](../../reproductions/2605.23572-harness-lm/README-en.md) | Bing Ads Revenue +1.0%, Clicks +0.4% | Three stages converged but test NDCG -28.05% |
| Core mechanism | `grc` · [GRC](../../reproductions/2602.23639-grc/README-en.md) | Revenue +1.79%, CTR +2.11%, GMV +2.04% | Structured SFT→GRPO→EGRS; NDCG -11.12% |
| Core mechanism | `mbgr` · [MBGR](../../reproductions/2604.02684-mbgr/README-en.md) | Meituan CTCVR +3.98% | BID/MBP/LDR; NDCG -5.92% |
| Core mechanism | `growthgr` · [GrowthGR](../../reproductions/2605.17994-growthgr/README-en.md) | New-item GMV +5.3%, site-wide GMV +0.3% | ItemLTV→SID→MoPO; NDCG +2.05% |
| Core mechanism | `mesh` · [MESH](../../reproductions/2607.12392-mesh/README-en.md) | Fresh repins +5.5%, retention +0.46% | Three towers and RGBC; NDCG -3.54% |
| Core mechanism | `sam` · [SAM](../../reproductions/2607.12714-sam/README-en.md) | CTR +1.1%, GMV +0.9%, bad cases -74.5% | ASGU/TTNP; NDCG -6.60% |
| Core mechanism | `danet` · [DANet](../../reproductions/2607.12578-danet/README-en.md) | pCVR +3.63%, GMV +2.23% | TFTM/DCM; NDCG -1.46%, fresh Hit +50.00% |
| Core mechanism | `proximity-features` · [Proximity Features](../../reproductions/2607.12246-proximity-features/README-en.md) | First-time bookers +2.0%, bookings +0.16% | Adaptive ZIP buckets; Hit@10 +16.67%, NDCG +22.91% |
| Core mechanism | `nontp` · [NONTP](../../reproductions/2607.12277-nontp/README-en.md) | Meituan DSP CTR +1.8%, GMV +2.1% | EMA-teacher TCL, cross-domain TDL, and zero additional inference executed; Hit@10 -4.93%, NDCG -8.62% |
| Core mechanism | `akt-rec` · [AKT-Rec](../../reproductions/2605.23310-akt-rec/README-en.md) | Tmall CTR +2.76%, GMV +3.47% | Actual small LLM, RQ-VAE, and asymmetric transfer; AUC +3.44%, GAUC +5.53%, tail AUC +2.15% |
| Complete core pipeline | `s-grec` · [S-GRec](../../reproductions/2602.10606-s-grec/README-en.md) | WeChat GMV +1.19%, CTR +1.16%, dislike -2.02% | Actual LLM PSJ, SID generator, and 5% A2PO. Validation promoted A2PO; test HR@10 +0%, NDCG -4.53%, no constraint violations |
| Complete core pipeline | `pinterest-ads-llm` · [Complementary LLM Predictor](../../reproductions/2605.27856-pinterest-ads-llm/README-en.md) | US Shopping RoAS +4.94%, opt-in +6.69% | SFT selected; GRPO Recall@20 +0%, LLM ranking feature AUC +2.59%, retrieval quota=0 |
| Complete core pipeline | `lwgr` · [LWGR](../../reproductions/2605.18771-lwgr/README-en.md) | Ads revenue +1.35%, CTR +1.17% | Reference selected; LWGR Recall@10 +0%, NDCG -4.29%; dual update ran without improving the constraint |
| Complete core pipeline | `sigma` · [SIGMA](../../reproductions/2602.22913-sigma/README-en.md) | AliExpress Order +2.80%, GMV +7.84% | Top-1 prefix HR@20 1/128→9/128; APF -11.11% relative to top-1 |
| Complete core pipeline | `univa` · [UniVA](../../reproductions/2605.05803-univa/README-en.md) | WeChat Channels GMV +1.50%, GMV(normal) +1.42% | Public Office proxy; HR@100 +4.76%, ValueHR +6.56%, but wNDCG -8.43%; 50/50 trie paths valid |
| Core mechanism | `prompt-generation` · [Prompt Generation](../../reproductions/2607.11326-prompt-generation/README-en.md) | Taobao Search transactions +0.47%, GMV +0.51%; Shop Search +4.01% | Same-source Amazon Office plus Qwen2.5-0.5B; selected Title HR@10 -11.11%, mean merger -90.38% versus raw Title scoring |
| Complete core pipeline | `precise` · [PRECISE](../../reproductions/2412.06308-precise/README-en.md) | WeChat ranking Clicks +1.961%, Shares +1.433% | SmolLM tokens, MoE, and UT/TT; Recall@10 +40.0%, Cold Recall -50.0% |
| Complete core pipeline | `lum` · [LUM](../../reproductions/2502.08309-lum/README-en.md) | Taobao CTR +2.9%, RPM +1.2% | Next-condition-item, grouped queries, and DLRM; AUC +14.60%, positive in 3/3 seeds |
| Complete core pipeline | `lsvcr` · [LSVCR](../../reproductions/2403.13574-lsvcr/README-en.md) | Kuaishou comment watch time +4.1264% | q/v-LoRA + SSC/VCC; comment NDCG +50.40%, item NDCG -56.42% |
| Complete core pipeline | `msd` · [MSD](../../reproductions/2412.06860-msd/README-en.md) | Meituan CTR +2.12%, CPM +2.59% | Teacher→T5 distillation plus LoRA/cache fusion; mean AUC +1.55%, positive in 2/3 seeds |
| Core mechanism | `sessionrec` · [SessionRec](../../reproductions/2502.10157-sessionrec/README-en.md) | Meituan Pay PV +0.603%, PVCTCVR +0.564% | Real KuaiRand sessions and exposed negatives; NDCG@20 -22.05%, positive in only 1/3 seeds |
| Core mechanism | `saviorrec` · [SaviorRec](../../reproductions/2508.01375-saviorrec/README-en.md) | Taobao Clicks +13.31%, Orders +13.44%, CTR +12.80% | Behavior encoder + RQ-SID + MBA + BiTargetAttn; mean cold AUC +6.92%, positive in only 1/3 seeds |
| Complete core pipeline | `pinrec` · [PinRec](../../reproductions/2504.10507-pinrec/README-en.md) | Grid Clicks +4.01%, Time Spent +0.55% | Actual OC + unordered MT training; Recall@10 -27.78% |
| Complete core pipeline | `genrank` · [GenRank](../../reproductions/2505.04180-genrank/README-en.md) | Engagements +1.2474% | Action-oriented latency -25.66%, AUC -0.46% |
| Complete core pipeline | `learn` · [LEARN](../../reproductions/2405.03988-learn/README-en.md) | Cold-item Revenue +8.77% | NDCG +233.10%, but head share 69.50% |
| Complete core pipeline | `notellm` · [NoteLLM](../../reproductions/2403.01744-notellm/README-en.md) | I2I CTR +16.20% | GCL+CSFT; NDCG +7.15%, positive in 3/3 seeds |
| Complete core pipeline | `kar` · [KAR](../../reproductions/2306.10933-kar/README-en.md) | Huawei news Recall +7%; music plays +1.70% | Actual LLM knowledge generation and hybrid experts; mean AUC +0.81%, positive in 2/3 seeds |
| Complete core pipeline | `bahe` · [BAHE](../../reproductions/2403.19347-bahe/README-en.md) | Ads CTR +9.65%, CPM +2.41% | Atomic behavior caching plus upper-layer aggregation; runtime -53.61%, AUC -2.94% |
| Complete core pipeline | `beque` · [BEQUE](../../reproductions/2311.03758-beque/README-en.md) | Taobao GMV +0.40%, transactions +0.34% | SFT, leakage-free self-sampling, offline feedback, and PRO; feedback +30.03%, increment -66.02% |
| Complete core pipeline | `onerec-v2` · [OneRec-V2](../../reproductions/2508.20900-onerec-v2/README-en.md) | Kuaishou stay +0.467%, Lite +0.741% | Actual KuaiRand duration feedback; Lazy latency -54.78%, mean GBPO +21.66% with only 2/3 positive seeds |
| Complete core pipeline | `plum` · [PLUM](../../reproductions/2510.07784-plum/README-en.md) | YouTube Panel CTR +0.76%/+4.96% | CPT lowered loss; Recall@10 R1/CR1 0.5%, R2/CR2 0; no verified retrieval gain |
| Complete core pipeline | `onerec` · [OneRec](../../reproductions/2502.18965-onerec/README-en.md) | Kuaishou watch time +1.68% | Core paths executed; DPO reduced local NDCG@10 from 0.0157 to 0 |
| Complete core pipeline | `g2rec` · [G2Rec](../../reproductions/2606.20554-g2rec/README-en.md) | Meta +0.06%–+0.19% | Soft graph and generative dual loss on Beauty; NDCG@10 +11.92% |
| Complete core pipeline | `mixformer` · [MixFormer](../../reproductions/2602.14110-mixformer/README-en.md) | Douyin duration +0.2799% | Matched-budget trainable blocks; NDCG@10 +17.41% |
| Complete core pipeline | `rankmixer` · [RankMixer](../../reproductions/2507.15551-rankmixer/README-en.md) | Active Days +0.3%, duration +1.08% | Dense per-token FFN performed best; sparse MoE did not match dense |
| Complete core pipeline | `hyformer` · [HyFormer](../../reproductions/2601.12681-hyformer/README-en.md) | Watch time +0.293%, finish +1.111% | NDCG@10 +143.77%, with higher head share |
| Complete core pipeline | `onetrans` · [OneTrans](../../reproductions/2510.26104-onetrans/README-en.md) | Feeds GMV/U +5.6848% | NDCG@10 +123.58%, but 92% of recommendations were head items |
| Complete core pipeline | `rec-distill` · [Rec-Distill](../../reproductions/2605.29755-rec-distill/README-en.md) | Ads ADVV +1.00%, Rec Finish/U +1.2725% | After α search, transferability -4.11%; no verified distillation gain |
| Complete core pipeline | `sasrec` · [SASRec](../../reproductions/1808.09781-sasrec/README-en.md) | None; user-designated classic baseline exception | Original BCE and full-catalog inference; NDCG@10 0.02933, -1.24% versus popularity |
| Core mechanism | `hstu` · [HSTU](../../reproductions/2402.17152-hstu/README-en.md) | Meta engagement +12.4%, consumption +4.4% | Matched sampled-softmax SASRec control; NDCG@10 -17.73% |
| Core mechanism | `m6rec` · [M6-Rec](../../reproductions/2205.08084-m6rec/README-en.md) | Alipay mini-app CTR >+1.0% | Real frozen pretrained LM; mean option-adapter AUC +0.12% ± 0.41% |
| Core mechanism | `din` · [DIN](../../reproductions/1706.06978-din/README-en.md) | Alibaba CTR +10.0%, RPM +3.8% | Local activation and Dice actually trained; NDCG@10 -6.97% versus mean pooling |
| Core mechanism | `tiger` · [TIGER](../../reproductions/2305.05065-tiger/README-en.md) | None; user-designated classic paper exception | Actual RQ-VAE and autoregressive retrieval training; NDCG@10 -39.16% versus capacity-matched random IDs |
| Core mechanism | `transact-v2` · [TransAct V2](../../reproductions/2506.02267-transact-v2/README-en.md) | Pinterest Repin +6.35%, Hide -12.80%, Time Spent +1.41% | NDCG@10 +92.65%, but head share rose to 98.99% |
| Core mechanism | `pinfm` · [PinFM](../../reproductions/2507.12704-pinfm/README-en.md) | Pinterest Homefeed Saves +1.20%–+5.70% | Two rounds of pretraining/fine-tuning with validation selection; test -3.57%, head share fell to 20.16% |
| Core mechanism | `sis` · [SIS](../../reproductions/2607.04728-sis/README-en.md) | Not part of this batch's A/B set | SIS formula executed; Qwen3/GRPO not trained |
| Core mechanism | `mdcns` · [MDCNS](../../reproductions/2605.19651-mdcns/README-en.md) | Public offline paper results | Author's Beauty split; three-source sampling and dual-model updates actually ran |
| Core mechanism | `memento` · [Memento](../../reproductions/2605.24051-memento/README-en.md) | Meta CTR +1.0%, CVR +1.2% | Query-conditioned MMR executed; production replay and serving omitted |
| Core mechanism | `llm-ad-retrieval` · [LLM Retrieval](../../reproductions/2605.21969-llm-ad-retrieval/README-en.md) | Meta top-line +0.45%, final recall +1.2% | Domain SFT and LLM attribute graph; Recall@20 +11.90%, score drift -77.36% |
| Complete core pipeline | `seral` · [SERAL](../../reproductions/2502.13539-seral/README-en.md) | Taobao clicks +29.56%, transactions +27.6% | NDCG +50.60% versus DIN; novelty did not improve |
| Complete core pipeline | `leadre` · [LEADRE](../../reproductions/2411.13789-leadre/README-en.md) | WeChat GMV +1.57%/+1.17% | +12.94% versus DIN; DPO ablation -4.53% |
| Complete core pipeline | `cobra` · [COBRA](../../reproductions/2503.02453-cobra/README-en.md) | Conversion +3.60%, ARPU +4.15% | +25.75% versus DIN; higher popularity concentration |
| Core mechanism | `argus` · [ARGUS](../../reproductions/2507.15994-argus/README-en.md) | Listening +2.26%, likes +6.37% | -4.12% versus DIN; no verified gain |
| Core mechanism | `gr4ad` · [GR4AD](../../reproductions/2602.22732-gr4ad/README-en.md) | Kuaishou ad revenue +4.2% | +69.67% versus DIN, head share 0.505 |
| Core mechanism | `cross-domain-kd` · [Cross-domain KD](../../reproductions/2603.28994-cross-domain-kd/README-en.md) | Music discovery +1.12% | Target split -68.46% versus DIN |
| Core mechanism | `mm-llm` · [MM-LLM](../../reproductions/2605.09338-mm-llm/README-en.md) | Meta engagement +0.02% | -13.23% versus DIN; no verified gain |
| Core mechanism | `cluster-goobs` · [Cluster GOOBS](../../reproductions/2607.00448-cluster-goobs/README-en.md) | Meta CTR +53% | Online sampler executed; genre replaced private LLM clusters |
| Core mechanism | `llatte` · [LLaTTE](../../reproductions/2601.20083-llatte/README-en.md) | Meta conversion +4.3% | BERT semantic features, MLA, target-aware online attention, and DHEN all actually trained |
| Core mechanism | `self-evolving-rec` · [Self-Evolving RecSys](../../reproductions/2602.10226-self-evolving-rec/README-en.md) | Google +0.03%–+0.14% | Local instruction LLM reads the journal, proposes changes each round, receives validation feedback, and uses isolated test |
| Core mechanism | `cmsl` · [CMSL](../../reproductions/2606.28533-cmsl/README-en.md) | Meta +0.092%–+0.171% | Learned contextual lenses and HSTU-style backbone actually trained |
| Core mechanism | `longer` · [LONGER](../../reproductions/2505.04421-longer/README-en.md) | Douyin Ads/e-commerce A/B | InnerTrans, global tokens, and hybrid attention trained end to end |

## Running reproductions

```bash
# One paper
auto-research reproduce --paper <adapter> --seed 42

# All papers
auto-research reproduce --paper all --seed 42

# Include explicitly downgraded concept demos
auto-research reproduce --paper all --include-concept-demos --seed 42
```

Raw run artifacts:

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── report.md
└── result.json
```

Git excludes `runs/`. The single-run source is `result.json`. The paper README summarizes reviewed stable conclusions, protocol, and reproduction limits.

## Adapter layout

```text
src/auto_research/reproductions/<adapter>/
├── adapter.py
├── model.py or algorithm.py
├── experiment.py
└── report.py
```

Shared public splits and per-user/matrix full-catalog metrics are in `reproductions/rec_utils.py`, all-position sequence training in `reproductions/sequence_training.py`, and downloads in `datasets.py`. Paper-specific networks, sampling, tuning, and reporting remain in each implementation. Every README contains metadata, original background, main changes, Mermaid architecture, core equations, paper offline/online results, local protocol, and fidelity limits. `scripts/sync_reproduction_metadata.py` synchronizes metadata. See [architecture](../architecture.md) for extension rules.
