# System One / Jev-compatible benchmark

<!-- source-sha256: daf1e02adcfeb6e7b17b643d726b602ad8b48db701a38d7c58535c067ccde04f -->

[简体中文](../../system-one/banking77-local-report.md)

> This report compares typed decision implementations under a public contract. It does not infer Jev's unpublished architecture.

## Protocol

- Data: Banking77 train `4000` / validation `1000` / test `1000`.
- Validation is used only for temperature calibration. Test results are reported only after selection.
- Metrics: accuracy, NLL, Brier, ECE, coverage, selective accuracy, and schema validity.

## Test summary

| Metric | Mean | Standard deviation |
|---|---:|---:|
| accuracy | 0.135333 | 0.047542 |
| nll | 3.987024 | 0.015477 |
| brier | 0.974854 | 0.000384 |
| ece | 0.104811 | 0.050786 |
| coverage | 0.000000 | 0.000000 |
| selective_accuracy | 0.000000 | 0.000000 |
| latency_ms_mean | 0.434357 | 0.020418 |
| schema_validity | 1.000000 | 0.000000 |

## Scope

Public-dataset local comparison; no claim about TypeSafe's unpublished architecture or vendor-reported performance.
