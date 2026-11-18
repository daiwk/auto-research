<!-- source-sha256: 46325e4737fd29ec2cc6b8ec65ce0f50cfe3ecdfa60443a369770f68b1b36b53 -->
# November 18, 2026: fourteen affordable opportunities delivered

[简体中文](../../../research-audits/nov18-components/README.md)

This batch implements the fourteen opportunities from the [closed November 10–15 review](../nov15-review-closure/README.md), with executable components, separate metrics, original figures, Chinese and reviewed English prose, four-level questions and same-topic comparisons. **These are not fourteen new papers published today or fourteen complete model reproductions.** The review watermark remains November 15, 2026; this delivery claims no additional exhaustive source scan.

## Fixed scope

| Area | Component | Local boundary |
| --- | --- | --- |
| System One | [Typed Inbox](../../../system-one/2610.32955-typed-inbox-protocol/README-en.md) | L0: frozen views, thread isolation and validation action costs, not a mail classifier |
| Agents | [AskALCF](../../../agent-research/2611.15700-askalcf-protocol/README-en.md) | L1: two-scope sufficiency, coarse attribution, revision cache and human ship/revert; not its complete 28-rule system |
| Agents | [ProdPilot](../../../agent-research/2611.17381-prodpilot-protocol/README-en.md) | L1: bounded repair, independent checks, rollback and deployment gates; no real cloud |
| Multimodal | [FEND](../../../multimodal-models/2611.18050-fend-protocol/README-en.md) | L0: deadline, detector priority and human FPR; no audio models |
| Foundation | [Stratified Retention](../../../foundation-models/2610.03713-stratified-retention-protocol/README-en.md) | L0: proposed stratified retention/revision evaluation; no invented empirical campaign |
| Foundation | [Tokenization Premium](../../../foundation-models/2611.13441-tokenization-premium/README-en.md) | L1: aligned join-then-tokenize, UNK exclusion, coverage/risk/ECE; no private architecture |
| Multimodal | [RSLiveBench-UAV](../../../multimodal-models/2611.14953-rslivebench-uav-protocol/README-en.md) | L0: rolling windows, four-calendar-month embargo and finite scoring; no full official data or VLM |
| Multimodal | [Library retrieval](../../../multimodal-models/2611.17726-multimodal-library-protocol/README-en.md) | L0: external embeddings, relevance metrics and explicit timing scope; no Qdrant/ColPali |
| Post-training | [Luce audit](../../../post-training/2610.19095-luce-similarity-audit/README-en.md) | L1: similarity odds, menu shifts and transfer uncertainty; no preference-model fitting |
| Foundation | [Runway](../../../foundation-models/2611.12737-runway-inference-protocol/README-en.md) | L1: configuration cache, SLA and unit-consistent costs; no cloud inference |
| Foundation | [Smart Routing](../../../foundation-models/2611.15911-smart-model-routing/README-en.md) | L1: cost/quality and cascade overhead arithmetic; not an online router |
| Post-training | [Calibrated Judges](../../../post-training/2611.19840-calibrated-judges-protocol/README-en.md) | L1: catches, two judges, swapped orders and disagreement ties; no paid judges |
| Foundation | [HVMap](../../../foundation-models/2611.01514-hvmap/README-en.md) | L1: four-layer maps, cross-target fuzzy loss, SCORE2 and hub/spoke paths; no full vector databases |
| Foundation | [Mixed Signals](../../../foundation-models/2611.13758-mixed-signals-weights/README-en.md) | L0: atomic external patches, practice budgets and evaluators; the linear harness is not TinyEEGNet |

The [machine-readable scope](../../../research-audits/nov18-components/task-scope.json) records each definition and cost disposition. Every component has a separate `metrics/component-cpu-seeds42-44.json`; only the two CUDA paths also have CUDA metrics and sanitized receipts. A theoretical proposal or evaluator is not mislabeled as a new training algorithm.

## Actual execution and evidence boundaries

The [preflight](../../../research-audits/nov18-components/preflight.json) fixes one device, 180 seconds and seeds 42/43/44, with zero model/dataset downloads, pretrained-model calls and API calls. [CPU raw evidence](../../../research-audits/nov18-components/raw-cpu.json) contains fourteen components; [real A100 evidence](../../../research-audits/nov18-components/raw-cuda.json) contains HVMap and Mixed Signals. Both bind the same [Git source proof](../../../research-audits/nov18-components/frozen-sources.json). Actual small-operator batch times are roughly 0.12 seconds CPU and 0.39 seconds CUDA, **not paper training/inference benchmarks**. Extreme-value fixes from independent review were refrozen and rerun; [initial records](../../../research-audits/nov18-components/initial-9da5bfcf/disposition.json) are retained but are not final acceptance.

HVMap checks gradients, absolute anchors, native weights and merging. Mixed Signals checks actual parameter writes and changed forward passes, atomic rejection, charged failures and external metrics. It contains no LLM editor, EEG/ECG model or subject trial. Known answers remain in independent scorers, never policies; multiple seeds do not upgrade L0/L1. There is no capability comparison, production A/B, Evolve promotion or safety certification.

Expensive complete campaigns are explicitly **not reproduced; review DONE**. Missing private architecture is recorded as unreconstructable scope, not automatically called expensive. Stratified Retention has no original empirical campaign and retains `no_original_experiment`. Automatic retry and implementation queues are disabled.

## Metadata and learning

Tokenization Premium appeared on official Zenodo v1.0 on September 22, before its November arXiv entry, and includes an author measurement script. HVMap's public source has no declared license, so local formulas are independently implemented. Library database-only timing is separated from its inconsistent end-to-end description rather than calling roughly 22k QPS end-to-end. RA-Eval's distinct length statistics retain their different denominators.

Four authored question bundles provide 56 questions across four levels. Reviewed English translations bind exact Chinese SHA values. Fourteen deep-dive updates compare existing same-topic papers using actual README fingerprints, not catalog labels. Method, institution, topic and date catalogs and bilingual learning pages regenerate together.

## Verification

```bash
PYTHONPATH=src:scripts python -m pytest tests/test_nov18_root_components.py tests/test_nov18_agent_protocols.py tests/test_nov18_data_protocols.py tests/test_nov18_eval_protocols.py tests/test_nov18_delivery.py
PYTHONPATH=src:scripts python scripts/curate_nov18_evidence.py --check
python scripts/validate_gpu_evidence.py
python scripts/english_docs.py --require-complete
```

Raw execution refuses overwrites. Reruns must use new output paths, preserving existing successes and failures.
