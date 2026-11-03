# Fidelity closeout before returning to incremental paper scans

<!-- source-sha256: 1d6f7c3bbf2073d7b509a2c7d5454a5c1133a4303e2e77d75947b195a3efd9eb -->

[简体中文](../../design/fidelity-closeout.md)

Scope: deliver all four requested items in one MR. Unit tests, fixed candidates, and registry names cannot substitute for actual capability evidence.

## Acceptance checklist

- [x] Repository-wide fidelity audit: inventory gold-label access and counter-only paths by source and method. Diagnostics cannot support capability claims.
- [x] CI regression prevention: reject new leakage and unexecuted operators, isolate legacy diagnostics, and prevent Evolve promotion.
- [x] Real CoSkill loop: checkpoint action generation, environment execution, private skill edits, reset verification, role-isolated credit, and shared-parameter training. Independent validation/test, multiple seeds, A100 evidence, executable Evolve integration, and verified resume.
- [x] Product-data validation: three-seed public-data comparison for AlleCompanion; corrected AtomRec checkpoint rerun on A100 with atomic memory, staged generation, label-free candidate ranking, and strict failures.
- [x] AutoLR loop: actual checkpoint proposals, two reviewers, backward verification, validation selection, ledger resume, and one final test, all run end to end on A100.
- [x] Task-level KV validation: multiple texts, long-context accuracy, latency, and peak VRAM at common budgets; actual A100 run.
- [x] Results, docs, and dashboard synchronized. Full tests, generation contracts, and PR CI passed in PR #152.

## Constraints

- Retain negative results. Never replace a failed model with gold or preset correct actions.
- Commit sanitized reviewable evidence only, not raw data, checkpoints, or remote logs.
- Original paper scale is not required, but defining generation, training, and inference cannot be replaced by proxies.
- Use the designated A100/A30 for GPU runs. Transfers require user authorization and platform approval.
- Merged PR #151 is the baseline, not a new completion in this batch.

## 2026-09-10 closeout

- Isolated legacy Agent Evolve: mini-suites and fixed-patch environments cannot promote. Generic ToolRoute routing is separate from paper implementations, and unknown paper operators fail.
- `scripts/audit_fidelity_boundaries.py` inventories attribute, literal-index, and `get/getattr` label accesses plus state updates in all `src`; CI checks drift. The snapshot has 1,292 review points across 50 files. Role classification follows below; behavioral tests cover dynamic keys and cross-function flow.
- CoSkill used an actual Qwen3-4B checkpoint on A100. The initial two tasks produced all-zero advantages/gradients and remain a failed training-coverage diagnostic. With 12 training tasks, parameters changed for all three seeds and both roles had nonzero gradients, but validation did not improve consistently. A separate one-round real CLI smoke verified unified controller execution, selection among negative results, final test, reporting, and checkpoint resume.
- The Amazon Beauty raw metadata and interactions ran a two-tower comparison over three seeds, capped at 1,000 users and 2,000 products. The category adapter lost on next-product prediction; this is not semantic complementarity evaluation and the negative result remains. AtomRec separately completed a small public product-memory experiment with strict pre-target reconstruction and no gold fallback; test was negative.
- AutoLR added dynamic proposals, independent reviewers, execution verification, and recovery. All three actual proposals on public Amazon Beauty failed to beat baseline; negative outcomes and final test were retained.
- The KV run downloaded and verified WikiText-2 test from a pinned public mirror on A100, evaluating six non-overlapping texts. KVMem quality was close to full, but the Python implementation was 56× slower. The reference backend retains a full backing cache with no peak-memory reduction; no speedup or savings are claimed.
- Implementations, public results, sanitized A100 evidence, local generator contracts, and PR CI were verified. Return to incremental discovery.

## Review categories

| Path family | Permitted label access | Claim boundary |
|---|---|---|
| `datasets.py`, `*data.py` | Data parsing/splitting | Never in policy observations; verified with isolation tests |
| Verifiers in `*benchmark.py`, `*evaluation.py`, and `generation.py` | Environment/evaluator | Score only after actions or text are produced |
| `agent_research/method_families`, `latest_*`, `p0/p1_*` | Legacy fixtures historically read labels | L1 diagnostics; ineligible for Evolve promotion |
| `post_training` candidate policies | Gold may construct candidate sets | Explicit `diagnostic_only`; only free generation can promote |
| `multimodal` and foundation checkpoint evaluation | Evaluator reads public benchmark labels | Checkpoint prompts do not receive labels |
| `evolution/composable.py` | Legacy environment/evaluation aggregation | Mini-suites cannot promote; real ToolRoute exposes public observations only |

A state-update inventory only establishes that a counter or cache changed, not that a model, tool, optimizer, or paper algorithm ran. Capability evidence needs behavioral tests, actual execution traces, and independent splits. The public dashboard gives explicit `diagnostic_only` priority over old `formal_comparison` labels.
