# October 14 label and execution-boundary review

<!-- source-sha256: 156e183163d5d106551d4d3505fe306ebac3c0db59647d64d7b170c473f7aa08 -->

[简体中文](../../research-audits/oct14-label-role-review.md)

Each new field access and counter in the AST inventory was checked individually. The inventory is a review aid, not proof of capability.

| Source | New access or counter | Allowed scope and behavior evidence |
|---|---|---|
| `agent_research/memcon.py` | Policy update / episode counter | Update only after real memory-backend operations and terminal feedback; counters are not agent capability. Separate 60-episode observable-record retrieval diagnostic and persistence tests for maintenance and feedback. No old Task answer/plan reads. |
| `system_one/regional_transfer.py` | Prediction gold / fallback gold | Input-file consistency, scoring public predictions, and **validation** temperature/route selection only. Test gold does not select. Regression confirms changing test labels does not alter temperature, threshold, or validation route. |
| `system_one/request_audit.py` | Scorer-only `positive_labels` | Request compiler reads displayed evidence and current question only. Independent request bytes do not change with other questions, route labels, or scoring labels. Labels enter metrics, not the model. |
| WeGR | Training SID / logged reward | Fit tokenizer on train items/sessions only; validation selects arm, test only reports. Scores and query logs are public MovieLens proxies, not production labels. |
| EmbeddingGemma 2 | Caption–image pair IDs | Encoder sees actual images/text. IDs reach the multi-positive scorer after encoding. All four preset MRL dimensions are reported without held-out selection. |

No new agent path returns gold answers. MemCon is a memory operator; JEV request audit is a protocol. Neither automatically qualifies for Evolve promotion. Five deferred papers have no executable adapters or metrics.
