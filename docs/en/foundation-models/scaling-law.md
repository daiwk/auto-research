# Scaling-law experiments across compute budgets

<!-- source-sha256: 71093c1cbbb9cba1806bd7faa69812aa60872c9ae6c8c95639bbb6ce15013d7d -->

[简体中文](../../foundation-models/scaling-law.md)

`auto-research scaling-law` trains the same micro-LLM across model sizes, available data, and step budgets. It tests whether the infrastructure can collect a reliable empirical curve, not whether a few small runs reproduce or prove Chinchilla scaling.

## Protocol

All points fix the WikiText-2 split, BPE vocabulary, architecture family, optimizer, batch size, sequence length, and seeds. Explicitly vary:

- Hidden width and layer count.
- Maximum sampleable training tokens.
- Optimizer steps.

Each point records parameter count $N$, observed training tokens $T_{seen}$, validation loss, and runtime. Compute uses the standard approximate proxy:

$$
C_{proxy} = 6 N T_{seen}.
$$

Default compute-curve fit:

$$
\log L = b + s\log C_{proxy}.
$$

Report log-space RMSE, original-loss RMSE, $R^2$, maximum relative error, and per-point residuals. If there are at least four points and the parameter/data design matrix has full rank, also fit a descriptive surface:

$$
\log L = b + s_N\log N + s_D\log D.
$$

This surface does not infer an optimal model-to-data ratio. An unidentifiable grid returns `not_identifiable` rather than a forced conclusion.

## Run

Install `llm-evolution` as described in the project README and prepare WikiText-2:

```bash
auto-research scaling-law \
  --dataset-dir data \
  --points "64x2:12000:6,64x2:24000:12,96x2:24000:12,128x3:48000:18" \
  --seeds 42 \
  --offline \
  --device auto \
  --output-dir runs/scaling-law-smoke
```

Points use `DIMxLAYERS:TRAIN_TOKENS:STEPS`. At least three distinct compute points, two model sizes, and two data caps are required. The four default points may identify the parameter/data surface. Mac uses MPS when available, Linux GPU uses CUDA, and Linux CPU can use `--device cpu --cpu-threads N`.

After interruption, repeat the exact configuration with `--resume`. The runner checks each point's config fingerprint and reuses only matching JSON. Configuration changes cannot silently mix with old results.

## Outputs

```text
runs/scaling-law-smoke/
├── points/
│   ├── 00-d64-l2-t12000-s6.json
│   └── ...
├── result.json
└── report.md
```

`result.json` stores raw points, fit coefficients, errors, and protocol. `report.md` shows budgets and per-point relative residuals. Checkpoints are not tracked. Formal research should use an orthogonal model/data grid, nearly converged training, and at least 3 seeds. The default command is an engineering smoke test.

The committed [four-point Mac smoke result](../../experiments/fm002-scaling-law-mac-seed42.json) has compute slope `-0.017291`, log-space RMSE `0.002153`, and $R^2=0.982928$. These values verify collection, fitting, and residual reporting, not a stable scaling exponent.

## Relationship to Evolve

The runner uses micro-LLM's real model, tokenizer, trainer, and device selection but does not choose winners across budget points. Calibrate an affordable and identifiable training range first, then let Evolve compare architecture, data, and post-training at fixed budget. More compute alone is not an architectural gain.
