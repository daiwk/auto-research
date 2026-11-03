# Shared evaluation protocol for foundation models

<!-- source-sha256: 43b0e5a000dee6cab7ef3ca48543a991bb395054ec4cb4e6d4a0abeba3bf8ec3 -->

[简体中文](../../foundation-models/benchmark.md)

Foundation-model experiments compare **quality, computational cost, and reproduction fidelity**. Fewer parameters, sparser masks, or lower theoretical FLOPs do not by themselves imply faster training or serving.

## Evaluation tiers

| Tier | Environment | Supported claims |
|---|---|---|
| L0 | Tiny Shakespeare / very small configuration | Operator, gradients, and reporting path run |
| L1 | WikiText-2 / small public datasets | Quality and mechanism differences under a matched budget |
| L2 | Standard public benchmarks, multiple seeds | Comparable scaled-down reproduction results |
| L3 | GPU kernels, paper models, and full data | Paper-scale quality and real performance reproduction |

## Required metrics

- Architecture and pretraining: parameters, training tokens and steps, validation and test perplexity, seed.
- Long context: training and test lengths, task quality, and measured attention/KV memory use.
- Multimodal: data sources, encoder and tokenizer, task metrics, and handling of missing modalities.
- Quantization and compression: accuracy, model size, peak memory, measured latency, and hardware.
- Serving: TTFT, TPOT, throughput, concurrency, GPU memory, input/output lengths, and software versions.

## Fair comparisons

The main results must use comparable data splits, token and step budgets, parameter counts, and evaluation code. If an architecture adds parameters, include an equal-parameter or equal-compute control. Without a fused kernel, a dynamic sparsity method may report the selection mechanism and theoretical or tensor sparsity, but not an actual speedup. Retain all negative results.
