<!-- source-sha256: 60f0f19ad5419ff9f9747b8b3ad8f98b44678103ea8c9c11789f495250332b7b -->

# November 7: priority-institution paper backfills

On the morning of November 7 in Shanghai, we rechecked the `new` and `recent` listings for eight arXiv categories. All 16 routes parsed successfully. The latest bulletin was still **November 6**, with the same paper identities and versions in each category as the previous capture. The three papers below are **backfills**, not new first publications. We record the first public version, arXiv announcement, and institution listing dates separately.

| Paper | First v1 (UTC) / announcement | Low-cost component | Why we did not reproduce the full experiment |
| --- | --- | --- | --- |
| [GINGER](../../../foundation-models/2611.08306-ginger/README-en.md), Google Research | Nov 5, 17:09:45 / Nov 6 | Nested quantization with a 4-bit navigation code and within-interval refinement | 14 datasets, up to one billion vectors, 2.3 TB of RAM, and SIMD engineering |
| [GSLM2](../../../multimodal-models/2611.01143-gslm2/README-en.md), Meta Superintelligence Labs | Oct 31, 17:31:45 / Nov 3; Meta directory: Nov 4 | Joint deduplication and scoring at each stream's transition positions | Up to 6 million hours of speech, 6.5 billion parameters, and multi-H200 pretraining |
| [EmoReward](../../../post-training/2611.06518-emoreward/README-en.md), with Tencent Hunyuan | Nov 4, 13:43:09 / Nov 5 | Active reward gating and frozen per-regime RewardMemory calibration | Multiple HunyuanVideo 1.5 RL arms, a reference run, multiple reward models, and transfer experiments |

All full experiments are marked **not reproduced due to cost (review complete)** and are excluded from automatic retries. The three CPU numerical mechanism checks each ran with seeds 42, 43, and 44. They did not require large downloads, model or API calls, or GPU validation. No formal capability comparisons or Evolve integrations were performed.

[Bulletin comparison receipts](../../../research-audits/nov07-priority-backfill/source-coverage.json) · [Official priority sources and excluded leads](../../../research-audits/nov07-priority-backfill/priority-review.json) · [Paper dispositions](../../../research-audits/nov07-priority-backfill/task-scope.json) · [Preflight budget](../../../research-audits/nov07-priority-backfill/preflight.json) · [Frozen sources and execution proof](../../../research-audits/nov07-priority-backfill/frozen-sources.json)

Coverage of the Google Research and Meta directories was limited. This does not establish that other sources had no new entries; the overall review watermark is unchanged. Meta's CAP-Mix reports offline evaluation, not the controlled production A/B or full-traffic evidence required for industrial admission. The specialized Muse models were a product update. We did not find a public replayable set of tasks and grading inputs for BioBasicsBench. Neither is presented as implemented.

All three papers have original figures, Chinese and English method pages, and questions at all four learning levels. See [recent questions](../../learning/recent.md) and [topic deep dives](../../learning/deep-dives/index.md).
