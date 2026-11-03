# Incremental paper scan: 2026-08-26

<!-- source-sha256: b19aa17e13089d75ea6d409b932bfdf1ce7b49c8c05b00cbc550d13d01753caa -->

[简体中文](../recent-paper-scan-20260826.md)

arXiv's visible August 26 submissions yielded **363 deduplicated papers** across cs.AI/LG/CL/IR/CV. Metadata keyword/semantic recall preceded priority full-text review. Google/Meta were separately checked; missing A/B wording in abstracts was not disqualifying.

| Track | Paper | Institution | Why selected |
|---|---|---|---|
| Industrial recommendation | [TAGR](../reproductions/2608.24034-tagr/README-en.md) | Kuaishou | Production LRE +8.5%, SCC +7.4%, revenue +16.1% |
| Multimodal foundation | [WeMM-Embedding](../reproductions/2608.24053-wemm-embedding/README-en.md) | WeChat/Tencent | Two-stage embeddings; full rollout after 14 online A/B tests; code and weights released |
| Post-training | [OPDSearch+](../post-training/2608.24310-opd-search-plus/README-en.md) | UCAS | Search evidence in OPD plus RL correction |
| Post-training | [OPDVR](../post-training/2608.24696-opdvr/README-en.md) | Tsinghua LeapLab | Verifiable-reward gating for token-level OPD |
| Agent | [SPO++](../agent-research/2608.24870-spo-plus-plus/README-en.md) | Renmin University | Event-time value freezing and token-measure correction for asynchronous RL |
| Agent | [SkillForge](../agent-research/2608.24747-skillforge/README-en.md) | AMAP/Alibaba | Create, verify, reuse and revise skills |
| Agent | [AHEAD](../agent-research/2608.24114-ahead/README-en.md) | AWS AI Labs/Purdue | Dense trajectories from environment feedback and corrective hints |
| Agent | [SMITH](../agent-research/2608.24571-smith/README-en.md) | Appier/NTU | Schema, code and execution verification for tool improvement |

All eight provide method-specific implementation, fixed metrics, original figures, details and Evolve mutations. Public proxies and deterministic mini-suites test mechanisms, not full paper scale.

## Industrial evidence

TAGR §4.3/Table 1 quantifies multi-week A/B in the same production stack. WeMM belongs to foundations: 14 A/B tests preceded full rollout but their effect sizes are not published. RecGPT-Mobile-V2 (2608.24295) discusses deployment/retrieval but lacks quantified A/B or explicit full traffic. Intuit's migration (2608.24132) is an offline fixed-cohort study. Native Multimodal CTR (2608.24091), RetrievalFormer (2608.24079) and Tlow (2608.24176) fail the industrial gate. No new Google/Meta work met both topic and full-text online evidence in this batch; priority remains.

## Local limits

TAGR MovieLens-1M NDCG@10 0.11227→0.08212 (−26.86%), head share 0.7275→0.1303. SID increases tail coverage but not ranking accuracy at this budget. WeMM two-stage alignment raises Recall@10 0.56111→0.83889 and MRR 0.28627→0.50894 on a MovieLens content/collaborative proxy. OPDSearch+ and OPDVR reach 0.66406 on arithmetic-smoke, a candidate-policy check. All four agents reach joint success 1.0 on planbench-mini, which validates control flow and telemetry only. Rejections and reasons remain in the machine-readable ledger for the next batch.
