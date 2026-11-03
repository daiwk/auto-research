# Recent paper scan: 2026-09-27

<!-- source-sha256: 01efcfe2e021ae10c985a70a5f5572e2094c06c1d20cd4cf073e1d68347bd499 -->

[简体中文](../recent-paper-scan-20260927.md)

September 20–27 overlap across four tracks with manifest/ledger deduplication. arXiv paging succeeded without cache; Google Research and Meta AI pages timed out. No cross-source completeness or all-source watermark advance. Month-wide IDs catch delayed indexing; new means not closed here, not published this week. Institution keywords are not affiliations. Per-query paging capped at 100; expansion to 200 stopped because of rate limits.

| Track | Unique hits | Not closed | Interpretation |
|---|---:|---:|---|
| Search/ads/recommendation | 143 | 92 | Includes institution false positives and delayed older work |
| Foundation | 600 | 532 | Broad hits need date and topic review |
| Post-training | 313 | 257 | Meta MaD-RL found on official site, not this arXiv candidate set |
| Agent | 548 | 491 | Unclosed is not implementable |

## Full-text priority queue

| Priority | Paper | Evidence | Recorded status |
|---|---|---|---|
| P0 | [OneTrans-V2](https://arxiv.org/abs/2609.28589) (Sep 23, ByteDance) | §6.3 user-level 50/50 A/B; shared causal context, three-stage training, decision-conditioned retrieval and ranking-to-preranking distillation | [Three-seed public proxy](../reproductions/2609.28589-onetrans-v2/README-en.md); MovieLens lacks transactions, ads and funnel |
| P0 | [X-Rec](https://arxiv.org/abs/2609.29180) (Sep 24, TikTok) | §5 two vertical rollouts, vertical engagement +4.1484%, global +0.0111%; spherical flow matching and late-interaction DiT | [Public mechanism vs SID-AR](../reproductions/2609.29180-xrec/README-en.md); matched 200 steps, 20×1 full-catalog and CPU throughput; negative low-budget result |
| P0 | [CMRec](https://arxiv.org/abs/2609.28972) (Sep 24, Alibaba International) | [§4.2](https://arxiv.org/html/2609.28972v1) May 10–20 2026, 10% traffic: revenue +1.77%, orders +2.64%; shared codebook, dual constraints, contextual weights | Pending; private ads plus public six-region Amazon M2, check author code |
| P0 | [AgentX-Model](https://arxiv.org/abs/2609.30001) (Sep 24, Kuaishou) | §4.3 five A/B tests; dual agents, Reproduce/Follow-up/Composition/Diagnose and dependent replay | [Six-node MovieLens-1M result-blind replay, three seeds](../agent-research/2609.30001-agentx-model/README-en.md); no private 473-node graph, online gate or LLM agent |

## P1 review leads, not implemented

- [MaD-RL (Meta)](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/) (Sep 24): KL/JS distribution matching vs GRPO collapse. Found after source timeout; verify equations, protocol, arXiv and code, not entropy-only substitution.
- [DeltaS](https://arxiv.org/abs/2609.27470): gated linear-attention drift for video KV eviction; author code linked, real hybrid checkpoint and equal-budget video tests needed.
- [KITE](https://arxiv.org/abs/2609.27294): KV-invariant dual tower and prefill/decode cost; verify small trainable model, not just FLOPs arithmetic.
- [PACT](https://arxiv.org/abs/2609.26355), [DCRL](https://arxiv.org/abs/2609.27572): critic alignment and policy–reward coupling; review equations, permissions and matched generative baseline.
- [Trajectory-graph advantages](https://arxiv.org/abs/2609.28963): step credit needs nongold multi-turn trajectories and a trainable policy.
- [IterSynth](https://arxiv.org/abs/2609.29444): role-separated deep search needs real retrieval, independent judge and cost comparison.

[Flexible recommendation for individuals/groups](https://arxiv.org/abs/2609.27998) is IMT Atlantique/Lab-STICC, not Google/Meta, with synthetic experiments. [LLM user profiling](https://arxiv.org/abs/2609.27183) uses production data but compares four strategies offline; no eligible A/B found. [From Interests to Semantic IDs](https://arxiv.org/abs/2609.29983) is Amazon Reviews offline, retained outside industrial. Light Heads, Music Rationales, UNIQUE, MuSeR and Meta layered engagement are overlap duplicates; unfinished private paths remain so.

Complete timed-out sources, paging above 100 and author-code checks. Industrial eligibility is not implementation. Preserve metadata, figures, independent metrics, three seeds and fair split/baselines; run CUDA paths on A100/A30. Promote P1 only after formulas, public data and budget checks; no registry-only or gold-trajectory capability claims.
