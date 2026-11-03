# 2026-09-08: Fidelity corrections for the September 7 batch

<!-- source-sha256: b0e7797318907f9144460d73cf0b6ad3816190f0af814ed55711f03c69a6c197 -->

[简体中文](../../design/sep7-fidelity-review.md)

This correction withdraws unsupported evidence. Core operator tests are not full-paper reproduction results.

| Scope | Corrected implementation | Verification | Still outside scope |
| --- | --- | --- | --- |
| BeaconKV / KVMEM | Query normalization, actual model RoPE, GQA per query head; removed fabricated storage-tier counts | A100, pinned Qwen3 revision, 96 head-layers, zero maximum error in full attention outputs, and three CPU regressions | 32K/million-token contexts, real serving throughput, CPU/NVMe tiered scheduling |
| AlleCompanion | Shared dual towers, category-conditioned adapters, mixed negatives, category reconstruction loss, and real optimizer updates | Three CPU MovieLens seeds with same-budget no-adapter control and gradient tests per component | ComCat multi-source mapping, product-complementarity datasets, online GMV |
| AutoLR | Separate candidate review input, real training callbacks, validation decisions, separate guardrails, durable recovery, fixed reference, and human release boundary | Three-seed offline control, gate rejection, recovery, and privilege-boundary tests | Autonomous LLM research/code generation, production multi-expert debate, online experiment permissions |
| AtomRec | Atomic nodes, links, revisions, multihop paths, and capacity eviction | Graph-path, revision, dangling-edge regressions, and public observation parsing diagnostic | LLM semantic editor and recommendation outcomes |
| CoSkill | Private skill edits, subtree retrieval, promotion after execution checks, lineage, GiGPO group logic, and shared-parameter joint loss | Invalid-promotion rejection, role gradients, and state grouping | Full VERL / ALFWorld / WebShop LLM training |
| SiLR | Simulator deep copies, per-branch severity admission, and rejected candidates do not mutate live state | Scalar-trap counterexample and SAFE_PROGRESS / PASS tests | Large-scale Gym-ANM / CityLearn recovery rates, LLM GRPO training |
| Multi-Harness RL | Within- and cross-harness relative credit from one rollout batch, with differentiable clipped objective | Grouping counterexample and real parameter-update tests | Real multi-harness training on SWE-bench and transfer to unseen harnesses |

## Evidence rules

- Four legacy agent policies receive only public `task_id / intent / context`. Tests make gold answers, gold plans, and hidden required tools raise on access.
- The legacy mini-suite parses public text formats; a perfect score is not tool capability. Without a simulator or rollout, do not fabricate admission counts, held-out counts, or policy updates.
- Operators require explicit simulator, execution verification, and rollout-return inputs. Real-environment integration needs separate validation, not a registered name.
- Corrected GPU evidence keeps its original path to avoid broken links and states the correction date and why old results are invalid.
- Regenerate with `PYTHONPATH=src python scripts/regenerate_sep7_fidelity.py`. Artifacts record code commit and data fingerprints. The user's `rl_papers_summary.md` was not edited.

## Local verification

```bash
python -m pytest tests/test_sep7_fidelity.py tests/reproductions/test_sep_7_2026_batch.py tests/reproductions/test_kv_attention_fidelity.py -q
python scripts/validate_gpu_evidence.py
PYTHONPATH=src python scripts/manage_paper_specs.py check
PYTHONPATH=src python scripts/manage_paper_specs.py validate
python scripts/migrate_metric_schema_v2.py
python -m mkdocs build --strict
```
