# System One / Jev-compatible benchmark

> 本报告比较公开契约下的 typed decision 实现；不推断 Jev 的未公开架构。

## 协议

- 数据：Banking77 train `4000` / validation `1000` / test `1000`；
- validation 只用于温度校准，test 仅在选择完成后报告；
- 指标：accuracy、NLL、Brier、ECE、coverage、selective accuracy、schema validity。

## Test 汇总

| 指标 | 均值 | 标准差 |
|---|---:|---:|
| accuracy | 0.135333 | 0.047542 |
| nll | 3.987024 | 0.015477 |
| brier | 0.974854 | 0.000384 |
| ece | 0.104811 | 0.050786 |
| coverage | 0.000000 | 0.000000 |
| selective_accuracy | 0.000000 | 0.000000 |
| latency_ms_mean | 0.434357 | 0.020418 |
| schema_validity | 1.000000 | 0.000000 |

## 边界

public-dataset local comparison; no claim about TypeSafe's unpublished architecture or vendor-reported performance
