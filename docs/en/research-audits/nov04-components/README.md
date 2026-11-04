# November 4 update: Google/Meta priority and low-cost components

<!-- source-sha256: 0f91916b393b35072d9ee68a765a8003a69cb25c89bdf41fc2396d85698bb300 -->

[简体中文](../../../research-audits/nov04-components/README.md)

The latest observed arXiv announcement is **November 3, 2026**. This is a fixed eight-paper delivery, not an exhaustive full-text review of the web or announcement pool. First publication, overlap backfills, official-URL changes and revisions are separate.

## Fixed scope

| Priority | Paper | Local delivery | Complete experiment not run |
| --- | --- | --- | --- |
| P0: Google | [XLA from the Trenches](../../../foundation-models/2611.00624-xla-trenches/README-en.md) | Review only; public tools distinguished from internal TPU systems | Multiple TPU generations, roughly 200,000 private graphs and internal tools; A100 is not a TPU substitute |
| P0: Meta collaboration | [Strategist](../../../agent-research/2611.03618-strategist/README-en.md) | CPU blueprint/AST, retrieval-score kernels, measurement cards and paired selection | No executor/meta-agent search or benchmark matrix |
| P0: industrial A/B | [WeSearch](../../../recommendation-components/2611.00530-wesearch/README-en.md) | CPU cluster union, OPQ/ADC distance and fresh snapshots | No private billion-document retriever, trained FFN or production A/B |
| P1 | [ProLand](../../../foundation-models/2611.00236-proland/README-en.md) | CUDA thin-factor momentum, low-rank polar and Landing | No full LLM/model/rank matrix |
| P1 | [GAVAGAI](../../../foundation-models/2611.00319-gavagai/README-en.md) | CUDA capped OT with Nothing, detached alignment and prior | No full vision-language training; authors report four A100s and about 11 hours |
| P1 | [SpecOPD](../../../post-training/2611.02846-specopd/README-en.md) | CUDA tree masks, predecessor readout and TV-prefix loss | No drafter/teacher checkpoints, rollouts or inference-speed claims |
| P1 | [RLiD](../../../post-training/2611.02455-rlid/README-en.md) | CUDA legal-menu policy, calibration, PPO and credit-variance audit | No diffusion-LLM/environment RL |
| P1: backfill | [AgentHeal](../../../agent-research/2610.39234-agentheal/README-en.md) | CPU external-evidence/provenance/compliance/abstention evaluator | No real browser actor or semantic judge |

All eight full experiments are **not reproduced due to cost (review complete)**, without automatic retry. Seven components are L1 diagnostics; one paper is reference only. No complete capability reproduction or executable Evolve integration is claimed. Strategist's first-author institution remains Princeton despite Meta collaboration. AgentHeal was first published October 29 and is an overlap backfill; the other seven first appeared after the prior October 30 capture.

## Actual execution and review

[Preflight](../../../research-audits/nov04-components/preflight.json), [frozen-source proof](../../../research-audits/nov04-components/frozen-sources.json), [raw CPU](../../../research-audits/nov04-components/raw-cpu.json), [raw CUDA](../../../research-audits/nov04-components/raw-cuda.json), [per-paper scope/cost](../../../research-audits/nov04-components/task-scope.json).

CPU executes seven components across three seeds; the real A100 executes four CUDA components across the same seeds 42/43/44. Only small matrices and state contracts are used: no model/capability-data downloads or LLM/API calls. Each has its own metrics artifact, and four have separate [GPU receipts](../../gpu-validation.md). Runner time excludes research, transfer and startup; it is not full-experiment runtime.

Cross-review found that WeSearch reconstruction could expand individually bounded inputs into an enormous output. Combined output size is now checked before indexing, with a rejection test. CPU/A100 execution was repeated against repaired frozen source; earlier diagnostics are retained, not reused for changed code. GAVAGAI's eight OT iterations can leave row-sum residuals; these are preserved rather than hidden by post-hoc normalization.

## Sources and deduplication

[Source receipts and identities](../../../research-audits/nov04-components/source-coverage.json) cover eight new listings, eight recent listings and 45 bounded institution pages. New listings contain 3,015 category entries and 2,168 distinct identities; recent listings contain 4,796 identities. These are recall counts, not qualified new papers or full-text reviews. **The global review watermark remains October 15, 2026.**

The parsed views contain 439 Google records, 144 Meta records across six pages and 266 distinct DeepMind URLs across nine pages. DeepMind's heading says 267; that discrepancy is explicit, not certified exhaustive. [Priority review](../../../research-audits/nov04-components/priority-review.json) accounts for five added URLs: FabScore is an old title with a newly readable source but an unconfirmed original date; What Limits Us and EmbeddingGemma 2 are known identities. Subscription-entitlement consistency and chiplet manufacturing tests remain outside topic boundaries despite Google priority.

[Primary receipts](../../../research-audits/nov04-components/primary-receipts.json) retain successful and failed fetches. [Ten unfinished review leads](../../../research-audits/nov04-components/unreviewed-leads.json) do not count as this batch's implementations or review-DONE decisions. Unfinished reading is not relabelled high-cost nonreproduction. Future work can continue these leads without calling them another batch of today's new papers.

## Learning and bilingual updates

Eight papers add basics, mechanism, comparison and implementation questions: 32 in total. Seven existing deep dives gain comparisons, analysis, self-tests and README-fingerprint-bound updates. Write-ups, Q&As, deep dives and this audit ship with reviewed English in the same PR.

[Recent Q&As](../../learning/recent.md), [all questions](../../learning/all.md), [deep dives](../../learning/deep-dives/index.md).
