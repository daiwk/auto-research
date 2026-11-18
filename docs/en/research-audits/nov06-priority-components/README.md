# November 5–6 papers: Google/Meta collaboration and bounded mechanisms

<!-- source-sha256: 73dfa845b816f26730e81089d427595f8df6cc5772184f8fe571a1a8420b7e4b -->

[简体中文](../../../research-audits/nov06-priority-components/README.md)

This fixed intake contains **eight papers**: seven L1 components and one high-cost reference. Official arXiv bulletin dates are recorded separately from v1 timestamps. Five v1 timestamps are later than the previous capture; three papers came from overlapping announcements. They were not all first published on November 6.

## Delivery

| Paper | Announced | Local delivery | Complete experiment not reproduced |
| --- | --- | --- | --- |
| [PiPNN II](../../../foundation-models/2611.05690-pipnn-ii/README-en.md), Google Research collaboration | Nov 5 | CPU unsigned-to-signed dot correction, scaling and streaming top-k | Large graph construction, terabyte-scale host memory and H100-specific kernels |
| [RAGCompass](../../../post-training/2611.05596-ragcompass/README-en.md), Meta collaboration | Nov 5 | CPU candidate-level distillation KL and offline selection | Multiple datasets and retrievers, trained reranker and real-model generation |
| [URED](../../../recommendation-components/2611.05997-ured/README-en.md) | Nov 5 | CPU session top scores, user recency deduplication and exposure-category filtering | Private Taobao 30-day logs, distributed serving and traffic A/B |
| [ICE](../../../recommendation-components/2611.07591-ice/README-en.md) | Nov 6 | A100 browsing-depth tails, detached gates and impression/click losses | 141.79M private slates, production evaluator and A/B |
| [ConvPE](../../../foundation-models/2611.07749-convpe/README-en.md) | Nov 6 | A100 causal convolutional positional bias | Large-corpus training and configuration search |
| [CoRD](../../../post-training/2611.07959-cord/README-en.md) | Nov 6 | CPU geometric mixing and maximal-coupling rollout kernel, key `cord-rollout` | LLM rollouts, distillation and multi-device training |
| [EnvOpt](../../../agent-research/2611.07372-envopt/README-en.md) | Nov 6 | CPU offline acceptance and rollback protocol | Real model APIs, agents and environment optimization across settings |
| [XStack](../../../agent-research/2611.08472-xstack/README-en.md) | Nov 6 | Reference and method review only, no executable entry | TPU migration matrix of 20 repositories by seven agents, real retraining and judging |

The priority organizations are verified coauthor affiliations, not first-author institutions. All eight complete experiments are **not reproduced due to cost (review DONE)**, with no automatic retry. The new CoRD and existing CORD retain distinct keys, modules and learning history.

## Execution and evidence

[Preflight](../../../research-audits/nov06-priority-components/preflight.json), [frozen source](../../../research-audits/nov06-priority-components/frozen-sources.json), [raw CPU](../../../research-audits/nov06-priority-components/raw-cpu.json), [raw CUDA](../../../research-audits/nov06-priority-components/raw-cuda.json), [paper dispositions](../../../research-audits/nov06-priority-components/task-scope.json).

CPU runs cover seven components; real A100 runs cover ConvPE and ICE. Each uses seeds 42, 43 and 44, with no checkpoint/data downloads or model/API calls. Each paper has its own metrics, and CUDA items have sanitized [GPU receipts](../../gpu-validation.md). The runs validate mechanisms and boundaries on generated inputs, not full model quality, serving speed, production lift or executable Evolve integration.

## Sources and learning

[Capture receipts](../../../research-audits/nov06-priority-components/source-coverage.json) cover eight arXiv categories via two routes each. November 6 new listings contain 1,373 category entries, including 602 replacements; the two recent days contain 1,128 distinct identities. Only the eight selected papers are dispositioned here. Listing counts are not full-text review counts.

[Priority review](../../../research-audits/nov06-priority-components/priority-review.json) separates directories, software releases and blogs about earlier papers from verified publications. Missing full directory coverage is not zero additions. BRIDGE remains a lead because its business-lift control was not verified. The global review watermark stays October 15, 2026.

All eight papers have original figure attribution, reviewed bilingual write-ups, and four levels of questions: 32 total. Related deep dives add comparisons, analyses, checks and dated updates bound to paper-page fingerprints.

[Recent Q&As](../../learning/recent.md) · [Deep dives](../../learning/deep-dives/index.md)
