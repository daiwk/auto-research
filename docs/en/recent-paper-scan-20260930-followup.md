# Official-source retry and combined P0/P1 batch: 2026-09-30

<!-- source-sha256: 1ffe8c1521e9f66b0f3aad96210d35d53affc089c61fc2b81e1787de97ae99ad -->

[简体中文](../recent-paper-scan-20260930-followup.md)

September 27–30 overlap. All four arXiv tracks finished with zero cache fallback. Google Research, Google DeepMind, Meta and conference lists recovered, but undated or unmatched identities remain; cross-source status stays partial and watermark stays unchanged. The queue now excludes known out-of-window titles and numeric paging links; undated titles stay reviewable.

| Paper | Track / priority | Implemented mechanism and boundary |
|---|---|---|
| [GRP v0.1](../reproductions/2609.36688-grp/README-en.md) | Industrial recommendation P0 | Snap multi-arm A/B; block SID decoding, detached MHP and mGRPO retrieval protection; no private data/serving |
| [LIFT](../foundation-models/2609.38149-lift-feedback/README-en.md) | Foundation P1 | Top-k latent state, fusion and CE/state KL; no 1B pretraining |
| [Triadic Linear Attention](../foundation-models/2609.36529-triadic-linear-attention/README-en.md) | Foundation P1 | Third-order write, two-query contraction and decay; no dedicated GPU kernel |
| [OASIS](../post-training/2609.37915-oasis/README-en.md) | Post-training P1 | Shortest verified scaffold, separate contexts and clipped OPSD |
| [GRAFT](../post-training/2609.37868-graft/README-en.md) | Post-training P1 | All-fail peer groups, compatibility and token clipping |
| [RIDE](../post-training/2609.36484-ride/README-en.md) | Post-training P1 | Extrapolated RL hidden residuals and masked regression |
| [PR-OPD](../post-training/2609.36642-pr-opd/README-en.md) | Post-training / agentic RL P1 | Multi-layer privileged alignment, teacher stop-gradient |
| [UserProxyBench](../agent-research/2609.38043-userproxybench/README-en.md) | Agent evaluation P1 | Strict UFS and premature disclosure audit separate from agent reward |
| [UpliftMem](../agent-research/2609.36805-upliftmem/README-en.md) | Agent memory P1 | Paired set uplift and Gaussian EVSI |

Nine have original figures, metadata, three-seed L1 metrics and unit tests; no paper-scale reproduction. No new CUDA claims; Triadic kernel unimplemented. S3, FOCUS, Traverse, LatCom, SkillGym, AnyAct, BRIDGE and RLTL;DR are terminal deferred for real checkpoints, large training, browser/MCP/code execution or large environment generation. No placeholder methods. Next keep at least three days of overlap from around September 28, retry official identities and check arXiv after September 30. Advance cross-source watermark only with auditable official outcomes.
