# KITE/SST：公开小模型等算量诊断

这是 [KITE/SST](https://arxiv.org/abs/2609.27294) 的缩小机制检查，**不是**论文 MoE 规模或原文 benchmark 的复现。运行脚本：`scripts/benchmark_kite_equal_flops.py`。

采用公开 WikiText-2 原始文本，独立 train、validation、test 文件，按 UTF-8 字节做 32-token next-token 任务。固定种子 42、43、44。宽度 32 的 2 层 Prefiller 经两阶段扩成 2+2 层 SST；对照为 4 层 dense 模型。两者初始 embedding、输出头和前两层权重相同，但参数量分别为 64,704 与 68,800。

SST 训练 30+30 步；对照按 PyTorch profiler 可识别的前后向 FLOPs 匹配为 17+28 步。两者阶段边界均重启 AdamW，学习率 0.001。对照 FLOPs / SST FLOPs = 0.9993；计数不含 optimizer、LayerNorm 和内存移动，因而不是严格硬件算量相等。test 不参与方法或超参选择。

| Seed | SST val NLL | Dense val NLL | SST test NLL | Dense test NLL | SST 末 token ms | Dense 末 token ms |
|---:|---:|---:|---:|---:|---:|---:|
| 42 | 3.7512 | 4.0244 | 3.7661 | 4.0508 | 0.279 | 0.346 |
| 43 | 3.5698 | 3.7940 | 3.6004 | 3.8177 | 0.279 | 0.343 |
| 44 | 3.5245 | 3.7784 | 3.5059 | 3.7568 | 0.281 | 0.356 |

```bash
PYTHONPATH=src python scripts/benchmark_kite_equal_flops.py \
  --data-root data --seeds 42,43,44 \
  --source-steps 30 --continuation-steps 30
```

仅能得出：在这个固定小任务和近似 FLOPs 预算下，SST 的 NLL 与本机末 token 延迟优于该 dense 对照。这里的“本机”不是 GPU 延迟，不能外推为论文 67B 扩展性或 GPU 吞吐。

## A100 CUDA 推理微基准

另用 `scripts/benchmark_kite_gpu_latency.py` 测量宽度 32、随机初始化的 2+2 SST 与 4 层 dense 对照，固定种子 42、43、44，每个配置预热后重复 20 次。输入是程序生成的 byte token，**不是** WikiText-2 训练后的权重，也不产生语言质量指标。`decode-one` 是完整前缀之后生成一个 token 的耗时；SST 的 `prefill-last-only` 仅计算与末 token 相关的 prefiller 输出，和全序列 prefill 分列报告。末 token logits 与完整 prefill 的最大绝对误差为 `2.46e-7`。

| 上下文 token | SST 完整 prefill | SST 末 token prefill | SST decode-one | Dense prefill | Dense decode-one |
|---:|---:|---:|---:|---:|---:|
| 32 | 1.421 | 1.417 | 1.435 | 1.374 | 1.447 |
| 128 | 1.423 | 1.422 | 1.438 | 1.378 | 1.454 |
| 256 | 1.441 | 1.431 | 1.455 | 1.406 | 1.457 |

单位为 ms，表中是三种子各自重复测量中位数的再中位数；[脱敏 GPU 运行凭证](../gpu-validations/kite-sst-gpu-latency-a100-20260929.json)记录了固定版本和命令。在此极小模型、短上下文的 launch-bound 微基准中，**没有测出明确的 CUDA 延迟优势**。它只关闭“小模型真实 CUDA prefill/decode 是否能跑”的验证项；原论文规模、长上下文、吞吐和真实训练权重仍待验证，不能据此宣称 KITE 论文效果已复现。
