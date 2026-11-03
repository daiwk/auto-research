# Sixteen Google-priority items: low-cost component delivery

<!-- source-sha256: 8d6c6bfb8fe9f813a6719e0559692b01467cc32dcae5a8c60ed43b98d859fc56 -->

[简体中文](../../../research-audits/google16-components-20261021/README.md)

This round implements **exactly 16** accepted follow-ups from the [previous 39-item review](../../../research-audits/google-meta-closeout-20261021/google39-report.md), not 16 new publications or full reproductions. The historical review snapshot is unchanged; a new ledger batch records component delivery.

## Delivered scope

| Paper / component | Actual delivery | Verification boundary |
|---|---|---|
| [Dynamic Cogeneration](../../../agent-research/2601.19066-dynamic-brt/README-en.md) | BRT original defect failure, patched pass, and grouped patch selection | Real subprocesses, manual patch; no LLM repair |
| [ME-POIs](../../../foundation-models/2601.21149-me-pois/README-en.md) | Multiscale Gaussian prior and contrastive/KL/text objectives | A100 tensor and gradient fixture; no private mobility data |
| [Attribution Sets](../../../recommendation-components/2602.06276-attribution-sets/README-en.md) | v1 formula-level risk estimation and finite-candidate ERM | Retained finite-sample counterexample to printed formula; unbiasedness not verified |
| [CausalArmor](../../../agent-research/2602.07918-causal-armor/README-en.md) | LOO likelihood attribution and masking/regeneration interface | Real 0.5B likelihood on A100; no safety accuracy |
| [Spatial Ads](../../../recommendation-components/2602.12481-spatial-ads/README-en.md) | Grouped pseudo-disk LP and randomized rounding | CPU math subproblem, not full matching/payment/PTAS |
| [ConvApparel](../../../agent-research/2602.16938-convapparel/README-en.md) | PLSA statistics, HLS, and cross-policy validation | CPU diagnostic classifier is not Gemini; no human data collection |
| [Modular Robust Generative](../../../foundation-models/2602.17554-modular-robust-generative/README-en.md) | Globally constrained primal-dual, SIR, and router objectives | A100 finite support; residual did not converge in 16 steps; not robustness capability |
| [Data Quality LSA](../../../foundation-models/2603.01293-data-quality-lsa/README-en.md) | LSA initialization, rollout, closed-form SFT, and OS objective | A100 formulas and gradients; OS is regression, not policy-gradient RL |
| [POLCA](../../../agent-research/2603.14769-polca/README-en.md) | Epsilon-net and search history containing inputs and outputs | CPU callback fixtures; no LLM program optimization |
| [Simula](../../../agent-research/2603.29791-simula/README-en.md) | Taxonomy, complexity expansion, independent dual critics, and complexity protocol | Injectable model interface with zero model calls; not a data quality result |
| [TFRBench](../../../agent-research/2604.05364-tfrbench/README-en.md) | MASE, reference construction, and isolated held-out predictions | Reference construction reads labels and is not leakage-free capability evidence |
| [ProEval](../../../foundation-models/2604.23099-proeval/README-en.md) | Empirical GP/BQ and failure-set capture | CPU historical score fixture; no rerun of LLM evaluation |
| [mild](../../../foundation-models/2604.27723-mild/README-en.md) | Margin logistic objective, gradients, and router | CPU mathematical training; inference does not read answers/costs |
| [ScientistOne](../../../agent-research/2605.26340-scientist-one/README-en.md) | CoE evidence binding, score rechecks, CPR, and audit interface | Missing semantic/citation evidence stays unverified |
| [Activation Model Scanner](../../../foundation-models/2608.05578-activation-model-scanner/README-en.md) | 48 official input pairs, activation directions, layer scans, and structural comparison | 96 real A100 forward passes; no independent baseline or safety certification |
| [HCRG](../../../agent-research/2609.12464-hcrg/README-en.md) | Python AST graph/skeleton, three hops, dependency order, and static metrics | Not tree-sitter plus Gemini Java migration |

The [scope manifest](../../../research-audits/google16-components-20261021/task-scope.json) records evidence, full-experiment status, and costs. `component_only` and `evaluation_protocol_interface` are not `full_pipeline`. All are `diagnostic_only=true`, with no capability gain or evolve integration.

## Full experiments

Full multi-data, multi-model, paid-API, multi-seed, or private-data experiments are not reproduced (review DONE) and not automatically retried. ME-POIs documents its unavailable private data. Spatial Ads is theoretical, with no full training experiment; do not invent a cost decision to fill the table. These statuses are independent of component delivery.

## Cross-review fixes

- HCRG stops guessing unimported short names across modules and keeps parameter/local shadows unresolved.
- POLCA history includes inputs and program outputs, not just scores and text.
- AMS reads `hidden_states[block+1]` for official zero-indexed blocks, verified by a real small Transformer hook and rerun on A100.
- Robust gating separates theoretical KL from practical adversary NLL; symmetric entropy fixtures must not hide the distinction.
- Attribution Sets keeps the v1 printed formula and independent finite-sample counterexample, without silently rewriting the equation to pass.

Early/intermediate runs stay separate from final acceptance. Receipt status “passed” covers only specified mechanisms, execution, and provenance, not capability, safety, or optimality.

## Checks

```bash
PYTHONPATH=src python scripts/closeout_google16_components.py --check
python -m pytest tests/test_google16_*.py
python scripts/validate_gpu_evidence.py
```

The earlier table saying 16 items were unimplemented remains the review snapshot from that date. This round did not run a new cross-domain scan or advance the 2026-10-15 watermark.
