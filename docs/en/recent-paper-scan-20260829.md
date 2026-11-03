# Four-track incremental scan: 2026-08-29

<!-- source-sha256: cbf0823f53f350e11e08b429af694e8d36b1eb59d2c19056fa5a228af4523c91 -->

[简体中文](../recent-paper-scan-20260829.md)

Overlap one day across recommendation/LLM applications, foundation/multimodal, post-training and agents. The arXiv API temporarily returned 429; reuse the most recent successful GitHub Actions candidate artifact and check August 28 announcements and Google/Meta affiliations directly. **No new Google/Meta paper passed scope and evidence in this increment**; priority remains.

## Nine implemented P0 papers

| Track | Paper | Mechanism | Local public experiment |
|---|---|---|---|
| Industrial recommendation | [VK Friend-GNN](../reproductions/2608.27413-friend-gnn/README-en.md) | Shared multi-hash embeddings and temporal adjacency/cutoff | MovieLens-1M full catalog Hit@10 0.0656→0.2281; not VK lift |
| Post-training | [TTPO](../post-training/2608.27448-ttpo/README-en.md) | Majority-vote OPSD routing and grouped RL | Arithmetic 0.1953→0.6328 |
| Post-training | [Weak-Model Guidance](../post-training/2608.27420-weak-guide-rlvr/README-en.md) | Weak-model prefix exploration and mixed RLVR | 0.1953→0.6797 |
| Post-training | [Uncertainty-Calibrated MOPD](../post-training/2608.26735-uc-mopd/README-en.md) | Two temperatures, positive-advantage density and CLL gate | 0.1953→0.1953; negative result retained |
| Post-training | [SPEAR](../post-training/2608.26550-spear/README-en.md) | Symbolic milestones and LCS-F1 process reward | 0.1953→0.2812 |
| Agent | [SWE-Prime](../agent-research/2608.27449-swe-prime/README-en.md) | Trajectory/semantic-span selection and loss mask | Three-seed ToolRoute L2.1 joint success 0.7708 |
| Agent | [HarnessLens](../agent-research/2608.27311-harnesslens/README-en.md) | Behavior-related task selection and attribution | Joint success 0.8194 |
| Agent | [CoVeMem](../agent-research/2608.26895-covemem/README-en.md) | Collaborative vector memory and candidate-aware retrieval | Joint success 0.7708 |
| Agent | [SPT](../agent-research/2608.26563-spt/README-en.md) | Multi-file SkillCorpus and Reference Insert | Joint success 0.8056 |

ToolRoute L2.1 excludes guides and oracles, unlike older fixtures that saturate at 1.0. Post-training mini-suites validate updates and training dynamics, not paper-scale LLM benchmarks.

## Two checkpoint P1 paths

- [PACE (2608.27206)](../reproductions/2608.27206-pace-vlm/README.md): APC/DDAE, real Qwen2.5-VL and RealWorldQA, Evolve operator; A30 records quality, tokens, latency and memory.
- [TwinKV (2608.27128)](../reproductions/2608.27128-twinkv/README-en.md): fixed-budget repair, real Qwen3 KV and WikiText-2, Evolve operator; A30 records matched-budget reconstruction, latency and memory.

Both are checkpoint smoke rather than paper benchmark reproductions; neither remains deferred. Recommendation candidates 2608.27006, 2608.26579 and 2608.25381 lacked quantified A/B or accepted full-traffic evidence. Other broad hits were benchmarks, surveys, audits or vertical applications without a qualifying algorithm and reproducible route. Final states are in the [ledger](../paper-discovery-ledger.json). Continue from the **2026-08-28** watermark with one-day overlap.

TTPO, Weak-Guide, UC-MOPD and SPEAR map to post-training genomes; SWE-Prime, HarnessLens, CoVeMem and SPT map to agent genomes. Friend-GNN stays adapter-only because RankMixer has no matching friend-graph slot. The nine P0 paths are CPU-runnable and add no CUDA-required path; future checkpoint training requires the A100/A30 receipt.
