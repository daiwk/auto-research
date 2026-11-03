# October 29: New announcements, Google/Meta sources, and learning materials

<!-- source-sha256: 464a92a4b78007b66e71cf8fbf9f8cfbf4dee47d1e0db31005d77d956648cf69 -->

[简体中文](../../../research-audits/oct29-components/README.md)

This batch delivers **eight low-cost L1 components and one high-cost reference**, plus the formal EmbeddingGemma 2 paper and official code for existing Meta RPL. These are not nine just-published models or full capability reproductions.

## Scope and final cost decisions

| Item | Source type | Local delivery | Full experiment |
| --- | --- | --- | --- |
| [Google Sleep](../../../foundation-models/2606.03979-sleep-lti/README-en.md) · P0 | October 27 official introduction triggered backfill; arXiv v1 in June, with an earlier 2025 version claimed by the paper | CPU LTI reward combining token edits and external semantics | Too costly, not reproduced, review DONE |
| [DeepMind HOPE](../../../foundation-models/2607.21366-hope-hilbert/README-en.md) · P0 | October 27 official code release triggered July backfill; distinct from Sleep's Hope architecture | CPU Hilbert/ReLU kernel, pruning rates, BN mean correction, and single-step recovery | Too costly, not reproduced, review DONE |
| [ResCom](../../../foundation-models/2610.35955-rescom/README-en.md) | Recent announcement; October 25 v1 predates prior capture | CUDA centered streaming moments, ridge whitening/SVD, and intercept | Too costly, not reproduced, review DONE |
| [Select-TTT](../../../foundation-models/2610.36794-select-ttt/README-en.md) | October 27 v1 | CUDA query-CE chunk selection, clipped write multipliers without renormalization, and actual fast-weight updates | Too costly, not reproduced, review DONE |
| [GUI-JEPA](../../../foundation-models/2610.36877-gui-jepa/README-en.md) | October 27 v1 | CUDA actual three-layer candidate-conditioned predictor, structure head, and listwise loss | Too costly, not reproduced, review DONE |
| [KL-MOPD](../../../recommendation-components/2610.36973-kl-mopd/README-en.md) | October 27 v1; real five-day A/B in body met industrial gate | CUDA single initial calibration, fixed position weights, and student-to-teacher KL | Too costly, not reproduced, review DONE |
| [DiscernMem](../../../agent-research/2610.36652-discernmem/README-en.md) | October 27 v1 | CPU paired replay, dual-reference repair gates, and version-evidence reset | Too costly, not reproduced, review DONE |
| [RuHarness](../../../agent-research/2610.36826-ruharness/README-en.md) | October 27 v1 | CPU six-cell joint posterior, conservative criterion frontier, and validation admission | Too costly, not reproduced, review DONE |
| [PailitaoMMSearch2.0](../../../recommendation-components/2610.36958-pailitao-mmsearch2/README-en.md) | October 27 v1; 14-day A/B and full deployment evidence in body | Reference only; no placeholder model, operator, or metrics | Too costly, not reproduced, review DONE |

Six of nine arXiv first publications postdate the prior capture. ResCom was submitted earlier but in a recent announcement; two historical papers came from official sources. Guided-RLVR is separately recorded as too costly, with formula ambiguities retained and no invented controller.

## Actual execution and limits

Frozen commit `4fd3d0c5845f7f88b9a68333c33c9035f47b3983` binds 12 source/contract files through portable Git proof. CPU ran eight components × three seeds in about 3.30 seconds; real **NVIDIA A100-SXM4-80GB** ran four CUDA components × three seeds in about 1.52 seconds, excluding network/startup. No checkpoints, public capability datasets, LLM/API calls, or full training.

Each seed must pass 59 fixed CPU mechanism checks, with 31 in the CUDA subset. These are numerical, gradient, state, or statistical contracts, not GUI success, forgetting, ImageNet accuracy, recommendation revenue, or unified evolve evidence.

- [Execution spec](../../../research-audits/oct29-components/execution-spec.json), [raw CPU](../../../research-audits/oct29-components/raw-cpu.json), [raw CUDA](../../../research-audits/oct29-components/raw-cuda.json)
- [Frozen source](../../../research-audits/oct29-components/frozen-sources.json), [paper scopes and costs](../../../research-audits/oct29-components/task-scope.json)
- Four GPU receipts: [ResCom](../../../gpu-validations/rescom-a100-20261029.json), [Select-TTT](../../../gpu-validations/select-ttt-a100-20261029.json), [GUI-JEPA](../../../gpu-validations/gui-jepa-a100-20261029.json), [KL-MOPD](../../../gpu-validations/kl-mopd-a100-20261029.json)

An incorrect commit argument was rejected before torch import or component execution. The real frozen commit was then rerun without a fabricated artifact. Review fixed KL normalization overflow for huge finite gaps, non-native RuHarness boolean serialization, asymmetric ResCom moment input, and HOPE extreme-mean cancellation without weakening gates or replacing core operators.

## Source coverage

[Coverage](../../../research-audits/oct29-components/source-coverage.json) retains eight latest and eight recent fetch receipts. The newest announcement was **October 28**, not the 29th capture date; recent pages include October 27 and overlap. Cross-listings and replacements are not new-paper counts. Not every recalled full text was read.

[Google/Meta/DeepMind snapshot](../../../research-audits/oct29-components/official-source-inventory.json): 44/44 pages, Google 435, Meta 144, DeepMind 266 URLs. The reconstructed Google baseline yields seven previously unseen URLs and two removed URLs; net five is not five new papers. Abstract-only triage, unconfirmed dates, and unavailable original environments are separately recorded. Six Meta pages do not establish exhaustion.

Meta sixthview has a release record but no verified paper identity. Genie4/Gemini4 Carbon did not establish canonical papers or reproducible public models. Existing [RPL](../../../agent-research/2610.24854-rpl/README-en.md) received only official source/license; existing [EmbeddingGemma 2](../../../multimodal-models/embeddinggemma2/README-en.md) received the formal paper and figure without a duplicate key or GPU result change.

The watermark remains **2026-10-15**; this fixed delivery does not close all October 16–29 full texts or sources. High-cost decisions are terminal and not queued.

## Learning materials

Four QA levels for each of nine papers plus one each for existing EmbeddingGemma 2 and RPL made **38 new questions**. Nine deep dives updated mechanism comparisons, trade-offs, cross-paper self-tests, and fingerprints. Recent, topic, and all-question views were generated. Teaching numbers are not measurements.

[Learning home](../../learning/index.md) · [Recent additions](../../learning/recent.md) · [Deep dives](../../learning/deep-dives/index.md)

## Delivery checks

- First local full test run: 6,267 passes, two skips, and three metadata integration failures fixed (terminal cost fields/reasons and stale RPL release assertion). All 69 affected regressions passed. Joint scope/ledger reason tampering was added as a negative control; no algorithm/evidence checks weakened.
- `compileall`, Ruff, minimal wheel install, strict docs, catalog/learning generation, paper coverage, GPU evidence, and platform contracts passed. None of 1,001 metric files required migration. Document corrections did not rewrite execution or frozen source.
- PR CI is judged by actual checks; local layered verification does not imply cloud CI completion.
