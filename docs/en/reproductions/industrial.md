# Search, ads, recommendation, and LLM applications

<!-- source-sha256: ed3f2b38b172bdd2e8fd280bbff36ad83fb22e7b7d035d9fd73b84d9c0892653 -->

[简体中文](../../reproductions/industrial.md)

This domain covers industrial recommendation, search, advertising, and their applications with LLMs. New industrial papers need quantified online A/B evidence or full-traffic or production deployment evidence explicitly accepted by the user. Classic baselines are included only as named exceptions.

## Subfields

| Stage or direction | Scope | Representative methods |
|---|---|---|
| Retrieval | Two-tower models, graph retrieval, semantic IDs, generative retrieval | YouTube DNN, TIGER, OneRec, PinRec |
| Coarse and fine ranking | Feature interactions, sequential interests, multitask learning, long sequences | DIN, DIEN, RankMixer, HyFormer, HSTU |
| Reranking and blending | List value, multi-objective constraints, source quotas, long-term value | SORT-Gen, Memento, DeGRe, DRL-PUT |
| Content understanding | Text/image/video representations, content–collaborative alignment, cold start | MM-LLM, PinCLIP, MIM, PRECISE |
| Moderation and risk control | Relevance quality, data review, privacy, anomalies, policy constraints | CORE, ASARL, RAMP, Proximity Features |
| Advertising and business decisions | CVR, delayed feedback, bidding, value-aware generation | ESMM, TWICE, SWAG, UniVA |

## Browse and evaluate

- [Methods index](catalog/README.md)
- [Browse by company](catalog/by-company.md)
- [Browse by topic](catalog/by-topic.md)
- [Browse by month](catalog/by-month.md)
- [Paper lineage and gaps](lineage.md)
- [Shared evaluation protocol](benchmark.md)
- [Adapter and experiment overview](README.md)

Moderation and risk control currently focus on relevance, training-data quality, privacy-constrained features, and policy constraints. This does not imply coverage of content safety, fraud detection, or advertising compliance. New work in these areas still requires real production evidence and should also report precision/recall, false positives, and business guardrails.
