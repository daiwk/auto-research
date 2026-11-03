# Meta official-source historical backfill: 2026-10-04

<!-- source-sha256: 71cdf2107e49c60b407b00d5b3426229b2dfd67589a0e64c94c9712da3a29eb3 -->

[简体中文](../recent-paper-scan-20261004.md)

Weekend arXiv requests repeatedly hit HTTP 429: neither evidence of no new papers nor a watermark advance. Targeted reconciliation against Meta's official research list, arXiv abstracts/HTML and author GitHub recovered four omitted manifest entries, not four October 4 publications. No DeepXiv. All P0 for Meta priority, not industrial evidence; local L1 diagnostics only.

| Paper | v1 | Author code | Local scope |
|---|---|---|---|
| SIRA | 2026-05-07 | facebookresearch/sira | Document-frequency gate and single weighted BM25 query expansion |
| AIRA2 | 2026-03-27 | No public author implementation found | Barrier-free scheduling and search/validation/test isolation |
| PAHF | 2026-02-18 | facebookresearch/PAHF | Explicit preference memory, pre-action clarification and post-action drift correction |
| HyperAgents | 2026-03-19 | facebookresearch/hyperagents | Performance/novelty parent distribution and bounded archive step |

SIRA does not run the frozen LLM or rebuild the 25.58-million-document Wikipedia index. AIRA2 paper uses 8×H200 and Gemini ReAct; local CPU scheduling and HCE are not CUDA or paper throughput. PAHF hides persona and gold action and tests feedback state transitions only. HyperAgents executes no generated code, shell or arbitrary self-modification, so archive selection is not open-ended recursive improvement.

Watermark **2026-10-02** and overlap start **2026-10-01** remain. Retry four tracks and official Google/Meta sources before advancing.
