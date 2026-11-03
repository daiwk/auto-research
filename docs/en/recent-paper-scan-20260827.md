# Incremental paper scan: 2026-08-27

<!-- source-sha256: 88868534176cb0701c7e636ee954f8c37c2c5baf046ed3496a8f80fe02104588 -->

[简体中文](../recent-paper-scan-20260827.md)

Scan by arXiv announcement date with one day of API overlap: August 27 announcements can carry August 26 API published dates. Recommendation, foundation, post-training and agent tracks returned 6/50/14/38 deduplicated candidates. Full-text review led to 14 implementations. Google/Meta retain top priority but not an exemption from industrial evidence.

| Track | Paper | First-author affiliation | Evidence or local conclusion |
|---|---|---|---|
| Industrial recommendation | [DCEO](../reproductions/2608.25635-dceo/README-en.md) | Alibaba | 41-day A/B GMV +0.36%; proxy Hit up, NDCG slightly down |
| Industrial recommendation | [TransRetrieval](../reproductions/2608.25528-transretrieval/README-en.md) | RUC/Alibaba | Month-long 5%-traffic revenue +2.53%; local Hit@10 +11.76% |
| Foundation/multimodal | [VBVR-Pro](../reproductions/2608.26105-vbvr-pro/README-en.md) | NTU | Executable verifier beats noisy scalar judge analogue |
| Foundation/multimodal | [MLLMCLIP](../reproductions/2608.25575-mllmclip/README-en.md) | KAIST/Sony | Attention selection and CKA runnable; diagnostic proxy |
| Post-training | [V-Rubrics](../post-training/2608.25580-v-rubrics/README-en.md) | NTU | Prefix-localized multidimensional credit |
| Post-training | [Clue-OPSD](../post-training/2608.25356-clue-opsd/README-en.md) | UMD | Training clue teacher; full-video student at inference |
| Post-training | [GRIN](../post-training/2608.25243-grin/README-en.md) | UC Merced | Golden-response injection in failed rollouts and mixed-policy correction |
| Post-training | [GRIP](../post-training/2608.25583-grip/README-en.md) | Peking University | Reward-guided policy interpolation |
| Agent | [JIT-Agent](../agent-research/2608.25593-jit-agent/README-en.md) | LV-NUS Lab | Harness generation, repair and archive distillation; joint success only 0.15 |
| Agent | [TraceML](../agent-research/2608.26086-traceml/README-en.md) | CMU | Four-phase development trajectories and reopening past plans |
| Agent | [AdaVDR](../agent-research/2608.25559-adavdr/README-en.md) | Alibaba | Tool necessity filtering and reliability reflection |
| Agent | [TOPAS](../agent-research/2608.25523-topas/README-en.md) | USTC | Critical-path and prefix-reuse scheduling |
| Agent | [CaSKG](../agent-research/2608.25500-caskg/README-en.md) | Jilin/Ant | Counterfactual probes and Bayesian skill-graph calibration |
| Agent | [ProgRouter](../agent-research/2608.25992-progrouter/README-en.md) | Aston | Online stepwise progress/cost routing |

AMBER (Meta, 2608.25546) remains a priority candidate but fails industrial eligibility: full text lacks quantified production A/B or explicit full traffic, not just abstract wording. HSR/MOTIF are offline recommendation papers. DCEO and TransRetrieval meet full-text evidence; online and local proxy numbers stay separate.

The discovery script now defaults to one day of announcement overlap and records requested and actual query windows. Ledger identity removes duplicates without losing UTC/announcement mismatches.
