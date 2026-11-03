# Recent paper scan: 2026-09-28

<!-- source-sha256: 5c5b21a7415af6aa9e2dd34907cc390823b14d71aed530f7080922b817376ebb -->

[简体中文](../recent-paper-scan-20260928.md)

Requested September 20–28, 2026 with another overlap day, first 50 per query and manifest/ledger diff. HTTP 406 on the same request later returned 200; bounded retries now handle transient 406. No cache fallback. Unreviewed means no terminal repository decision, not newly published or eligible. Delayed arXiv IDs are surfaced separately.

| Track | Unique hits | Unreviewed | Unreviewed first published Sep 20–28 |
|---|---:|---:|---:|
| Industrial/LLM | 134 | 98 | 32 |
| Foundation/multimodal | 334 | 321 | 217 |
| Post-training | 232 | 187 | 90 |
| Agent | 311 | 300 | 201 |

Meta's main source returned 500; Google/Meta GitHub APIs returned 403. Google's source succeeded but does not establish full-text completeness. Targeted official Meta lookup supplemented coverage. Three source failures and 50-result limits prevent an all-source watermark advance.

| Priority | Paper | Verified evidence and boundary |
|---|---|---|
| P0 industrial | [KuaFu](https://arxiv.org/html/2609.31045) (Tencent, Sep 25) | §4.8 visitor-randomized equal-resource A/B; 5% control after 100% rollout, ten-month GMV +1.37%, 95% CI [0.71%, 2.03%]. MRQA/RecBench public, behavior logs private. Need entry compression, dual-axis projector, three-stage training and hallucination-aware DAPO, not a single function. |
| P0 Meta post-training | [Recursive Self-Improvement via OPD](https://arxiv.org/html/2609.30652) (Sep 25, Meta AI/UCR first author) | Refresh privileged teacher from updated student; validated shorter rewrites for SRCL. Authors compare OPSD on Qwen3 AIME/HMMT. Public Qwen3-4B-Instruct-2507 cached on A100, not the training chain. |
| P1 agent systems | [ActKV](https://arxiv.org/html/2609.31395) (USTC, Sep 25) | Action-based KV allocation needs real inference and equal-budget task/throughput comparison |
| P1 agent RL | [ToolSearcher](https://arxiv.org/html/2609.30906) (Zhejiang University/Ant, Sep 25) | Large tool-space retrieval RL; verify AppWorld/data/code and run retriever–policy chain |
| P1 agent skills | [Code-Based Skills](https://arxiv.org/html/2609.31076) (Sep 25) | Mixed primitives/skills and RL in NetHack/MiniHack; existing tool-tag suite is not equivalent |

[MaD-RL](../experiments/mad-rl-mechanism.md) was officially released by Meta Sep 24; paper dated Sep 23. Four divergences and character-policy diagnostic exist, not Qwen3-4B GSM8K/MATH/CodeContests multilingual training. A100 checkpoint and CUDA availability do not substitute for data protocols, LoRA, warm-up or three-seed cost checks.

GRAFT/KITE/DeltaS were prior leads. [GRAFT three-seed tool comparison](../experiments/sep28-three-mechanisms.md) shows zero lift; formal LLM policy, equal-budget scaling and real video model remain outstanding respectively. CMRec Amazon-M2 not supplied; no fabricated cross-region split.

Prioritize KuaFu with public checkpoints/data and no-compression/truncation controls; then Meta OPD/MaD-RL with public math and matched baselines, validation-only selection; then ActKV/ToolSearcher/Code Skills as dependencies permit. Follow the [roadmap](../research-roadmap.md) for earlier gaps. P0/P1 is not implemented status; code, public tasks, three seeds, docs and required A100/A30 receipts gate promotion.
