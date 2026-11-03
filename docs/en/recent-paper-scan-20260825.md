# Incremental paper scan: 2026-08-25

<!-- source-sha256: 20122aa804cc9a44ea48b507b10bc44ccb3010875f9990e8844a26285dfe6f06 -->

[简体中文](../recent-paper-scan-20260825.md)

## Scope

- Following the January 1–August 24 historical scan, read the arXiv batch visible August 25 (entries dated August 24 UTC).
- Sources: paginated arXiv API submittedDate, DeepXiv semantic search, paper HTML/PDF and official code.
- Tracks: industrial search/ads/recommendation and LLM applications, foundation models, multimodal, post-training and agents. Industrial eligibility needs quantified online A/B or verifiable full traffic, checked in full text.

## Results

Metadata screening covered 329 new cs.IR/cs.LG/cs.CL/cs.AI/cs.CV entries. No new industrial recommendation paper met the online gate; ANR-DiffRec and SST are public-dataset work, not production deployments.

| Track | Paper | Reason | Status |
|---|---|---|---|
| Post-training | [SRPO](../post-training/2608.23493-srpo/README-en.md) | Reflection patches and same-model privileged teacher for token credit | Implemented |
| Post-training | [ERPO](../post-training/2608.23311-erpo/README-en.md) | Alibaba/AMAP Query-KL regularization without directly suppressing answer exploration | Implemented |
| Agent | [Agent-G²](../agent-research/2608.23318-agent-g2/README.md) | Baidu task-level Gaussian guidance without probe rollouts | Implemented |
| Agent | [AutoSaddler](../agent-research/2608.23041-autosaddler/README-en.md) | Microsoft collaboration; failure traces drive durable harness edits | Implemented |

ProxyFormer and Sigmoid Attention KV eviction need a higher-fidelity training budget. E2S-Pruner, FOVEA and WnW need real-checkpoint protocols. ANR-DiffRec/SST lack industrial A/B. Prime Agent, SkillAlchemy, TRACE and GSAR remain candidates below this batch's two agent P0s. The next batch starts after this one and continues Google/Meta full-text checks.
