# Systematic all-domain gap audit (2026-08-08)

<!-- source-sha256: e9651aebd73a5a609b0ed41643925abd3d4ad1d65037bcb34500b9ce2894b0e7 -->

[简体中文](../full-domain-gap-review-20260808.md)

This fixed two-dimensional review covers search, ads, recommendation, and LLM applications; foundation models; LLM post-training; and agents, including each domain's second-level subtopics. The [machine ledger](../paper-discovery-ledger.json) records every candidate as implemented, deferred, or rejected so discoveries are not lost between batches.

## Audit method and limits

1. Build the covered set from adapters, detail pages, and method indexes. A name mention is not an implementation.
2. Search classic lineages, 2025, and 2026 through August 8 separately, then verify via institutions, citation chains, and official repositories.
3. Industrial papers require quantitative online A/B, explicit full-rollout evidence, or a named classic exception approved by the user. Offline metrics and unquantified deployment do not qualify automatically.
4. Foundation models, post-training, and agents need trainable or executable core mechanisms and public benchmarks. Pure analysis can be indexed without placeholder adapters.
5. Deferred means verified but not implemented or awaiting evidence/environment. Rejected means below the current bar, not missed.

Earlier `2026-08-08-p0-p1-closed-audit` closed only its 15 selected papers and did not claim subtopic coverage. It did not establish no omissions. Tests now require audit records for 24 second-level subtopics in all-domain batches.

## Findings and completion

> All **38 P0 and 15 P1 items** identified here were implemented. P0 consists of 19 reproduction adapters, 11 post-training objectives, and eight agent methods ([fixed-seed metrics](../experiments/global-p0-20260808-seed42.json)). P1 consists of eight reproduction adapters, three post-training objectives, and four agent methods ([fixed-seed metrics](../experiments/global-p1-20260808-seed42.json)).

| Domain | Main gaps | P0 | P1 and limits |
|---|---|---:|---|
| Search, ads, recommendation, and LLM applications | Recent generative recommendation, reranking, long histories, heterogeneous coarse ranking, and content relevance | 11 | Classic long sequences and candidates awaiting evidence; no qualifying new moderation or risk candidate |
| Foundation models | Position encoding, GQA and hybrid models, data mixtures, tokenizer-free models, multimodality, and inference decoding | 8 | Five local or single-GPU P1 methods implemented |
| LLM post-training | RLAIF, process rewards, test-time RL, self-play curricula, and off-policy stability | 11 | Three P1 methods; no duplicate adapters for theory equivalent to existing objectives |
| Agents | Tool RL, deep research, skill consolidation, self-evolving RL, and public benchmarks | 8 | Four P1 methods or evaluators implemented |

Counts refer to the explicit priority queue, not arXiv hits. The ledger remains authoritative for candidates, rejection rationale, and priority.

## Search, ads, recommendation, and LLM applications

### Implemented P0 items

| Subtopic | Paper | Gap addressed | Reported online evidence |
|---|---|---|---|
| Generative recommendation | [GloRank](https://arxiv.org/abs/2604.25291) | Global Semantic ID action space, SFT and GRPO | Kuaishou, 7.8% of traffic for 14 days; watch time +0.095% and improvements in multiple engagement metrics |
| Reranking and blending | [Dual-Rerank](https://arxiv.org/abs/2604.07420) | Sequential distillation and latency-aware dual reranking | 5% traffic for one month; Long-View +1.107%, significantly lower P99 and mean latency |
| Fine ranking | [OneRanker](https://arxiv.org/abs/2603.02999) | Unifies value-aware generation and ad ranking | WeChat Ads full rollout; GMV +1.34% |
| Retrieval | [RADAR](https://arxiv.org/abs/2506.07261) | Asynchronously uses a full ranker for next-request retrieval | About 2× Recall@200; online engagement +0.8% |
| Retrieval | [DualGR](https://arxiv.org/abs/2511.12518) | Long/short interest routing, constrained SIDs, and exposure-aware loss | Kuaishou views +0.527%, watch time +0.432% |
| Training and serving | [MPFormer](https://arxiv.org/abs/2508.20400) | Multitask retriever and resource sharing | Watch time +0.426%; training resources −60%, serving −66.7% |
| Coarse ranking | [HAP](https://arxiv.org/abs/2603.03770) | Heterogeneous examples and dynamic compute budget | Toutiao for nine months; duration +0.4%, active days +0.05% |
| Generative recommendation | [OnePiece](https://arxiv.org/abs/2509.18091) | Context engineering, blockwise latent reasoning, and progressive MTL | Shopee GMV/UU more than +2%, ad revenue +2.90% |
| Content understanding | [IntSR](https://arxiv.org/abs/2509.21179) | Joint search/recommendation intent and point-of-interest understanding | Amap GMV +9.34%, POI CTR +2.76% |
| Reranking and blending | [CDM](https://arxiv.org/abs/2406.09021) | Diversity as a controllable industrial blending objective | Kuaishou main app watch time +0.406%, clustering coefficient −0.957% |

[CWM](https://arxiv.org/abs/2406.07932) also reports online MWT +2.9%, VV +2.5%, and CTR +0.3%. Its counterfactual long-term-value ranking merits a fair reproduction in the same P0 batch.

### Implemented P1 and evidence threshold

- [SIM](https://arxiv.org/abs/2006.05639), [TWIN-V2](https://arxiv.org/abs/2407.16357), and [CRSD](https://arxiv.org/abs/2510.11056) are implemented. Preserve the online tables rather than treating “significant improvement” in an abstract as numerical evidence. Later candidates must pass the same bar.
- **Moderation and risk:** No public candidate satisfied both industrial scope and quantitative online A/B or full rollout. This is an audited subtopic with no qualifying candidates. Admitting public moderation benchmarks would require a separate change to the criteria.

## Foundation models

### P0: Fair local reproduction and evolve integration

| Subtopic | Paper | Variable to test |
|---|---|---|
| Long context | [RoPE / RoFormer](https://arxiv.org/abs/2104.09864) | Absolute positions versus RoPE length extrapolation at matched parameter count |
| Long context | [ALiBi](https://arxiv.org/abs/2108.12409) | Train-short/test-long attention-bias comparison |
| Architecture | [GQA](https://arxiv.org/abs/2305.13245) | Joint quality, KV cache, and throughput metrics for MHA, MQA, and GQA |
| Architecture | [Hymba](https://arxiv.org/abs/2411.13676) | Parallel attention and SSM heads, not a configuration placeholder |
| Architecture | [MoBA](https://arxiv.org/abs/2502.13189) | Differentiable block routing and real sparse computation |
| Pretraining data | [DoReMi](https://arxiv.org/abs/2305.10429) | Proxy-loss-driven domain-weight updates |
| Pretraining data | [Data Mixing Laws](https://arxiv.org/abs/2403.16952) | Predict data mixtures from multiple low-budget domain curves, not one run |
| Architecture / tokenizer | [Byte Latent Transformer](https://arxiv.org/abs/2412.09871) | Entropy patching, byte encoders and decoders, and same-FLOP comparison |

### Implemented P1

- Multimodal anchors: [CLIP](https://arxiv.org/abs/2103.00020) and [LLaVA](https://arxiv.org/abs/2304.08485).
- Inference: [Speculative Decoding](https://arxiv.org/abs/2211.17192), [AWQ](https://arxiv.org/abs/2306.00978), and [Medusa](https://arxiv.org/abs/2401.10774).

## LLM post-training

Many DPO/GRPO/OPD objective names hid genuine gaps in three lineages.

### Implemented P0

| Lineage | Paper | Missing mechanism |
|---|---|---|
| AI feedback | [RLAIF](https://arxiv.org/abs/2309.00267) | Principles and preference labels, AI preference model, and policy update in one loop |
| Process rewards | [Let's Verify Step by Step](https://arxiv.org/abs/2305.20050) | Fair step-level comparison of outcome and process rewards |
| Process rewards | [Math-Shepherd](https://arxiv.org/abs/2312.08935) | Automatic step supervision and a step verifier |
| Self-rewarding | [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020) | One model judges, generates preferences, and updates iteratively |
| Reasoning RL | [LUFFY](https://arxiv.org/abs/2504.14945) | Correction that preserves on-policy behavior with offline data |
| Test-time RL | [TTRL](https://arxiv.org/abs/2504.16084) | Reward estimation and online adaptation on unlabeled test examples |
| Self-play | [Absolute Zero](https://arxiv.org/abs/2505.03335) | Jointly generated tasks, verifier, and curriculum |
| Self-confidence reward | [INTUITOR](https://arxiv.org/abs/2505.19590) | Self-certainty reward without an external verifier |
| Stability | [CISPO](https://arxiv.org/abs/2506.13585) | Actual gradient path for token importance sampling and clipping |
| Self-play | [SPIRAL](https://arxiv.org/abs/2506.24119) | Language-game curriculum and two-role updates |
| Stability | [ConSPO](https://arxiv.org/abs/2605.12969) | Sequence consistency constraint |

PPO, GAE, and DeepSeek-R1/GRPO are not missing adapters because existing implementations already cover their mechanisms. Technical reports or pure theory without new executable objectives are lineage notes, not additional algorithm counts.

## Agents

### Implemented P0

| Subtopic | Paper | Missing mechanism |
|---|---|---|
| Deep research | [DeepResearcher](https://arxiv.org/abs/2504.03160) | Long search/browse/answer trajectory RL and citation reward |
| Tool RL | [ReTool](https://arxiv.org/abs/2504.11536) | RL curriculum for dynamic tool calls during reasoning |
| Tool RL | [ToolRL](https://arxiv.org/abs/2504.13958) | Multi-tool selection, argument generation, and execution-feedback training |
| Skill library | [SAGE](https://arxiv.org/abs/2512.17102) | RL-driven generation, updating, and reuse of skills |
| Memory and skills | [MemSkill](https://arxiv.org/abs/2602.02474) | Consolidating episodic memories into executable skills |
| Memory and skills | [Memento-Skills](https://arxiv.org/abs/2603.18743) | Experience extraction, skill retrieval, and cross-task transfer |
| Agentic RL | [SEARL](https://arxiv.org/abs/2604.07791) | Self-evolving trajectory pool and policy-improvement loop |
| Multi-agent systems | [Agent0](https://arxiv.org/abs/2511.16043) | Self-generated tasks and a multi-agent curriculum |

P1 Agent-R1, CAMEL, ToolBench/ToolLLM, and GAIA are implemented. Each write-up separately states the deterministic mini-suite limits.

## Executed results

1. Each industrial P0 records quantitative online evidence, upstream code status, fair local baselines, and negative results.
2. RoPE, ALiBi, GQA, Hymba, MoBA, BLT, DoReMi, and Data Mixing Laws are executable adapters; architecture and data-mixture operators entered evolve.
3. Eleven post-training methods use a common reward, KL, length, and seed protocol. TTRL and INTUITOR did not improve in the non-shifted mini-suite; this is a fidelity limit, not a hidden failure.
4. Eight agent methods ran 120 episodes with method-specific telemetry.
5. Future omission checks append a `scope_kind: global` ledger batch or clearly declare bounded scope. CI rejects missing subtopic records in all-domain audits.
