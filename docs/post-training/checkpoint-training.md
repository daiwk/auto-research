# 真实 checkpoint 后训练

原有 `post-train` 命令保留轻量、可审计的机制实验。`checkpoint-post-train` 是独立的 L2/L3
路径：直接加载固定 revision 的公开 pretrained causal LM，并在公开数据上执行真实参数更新。

## 固定模型与数据

| 资源 | 固定版本 | 用途与许可 |
| --- | --- | --- |
| `HuggingFaceTB/SmolLM2-135M-Instruct` | `12fd25f77366fa6b3b4b768ec3050bf629380bac` | Apache-2.0；Mac、Linux CPU 和单卡 GPU 可加载 |
| OpenAI GSM8K | 仓库既有官方 JSONL 下载口径 | SFT 与三 seed unrestricted generation |
| `HuggingFaceH4/ultrafeedback_binarized` | `292c16329d921287c4166934cac1a6ad1e13a6c5` | MIT；chosen/rejected 公平比较 DPO 与 ORPO |

## 三条可执行路径

```bash
# GSM8K：真实生成、固定 checkpoint、3 seeds
auto-research checkpoint-post-train \
  --objective sft --dataset gsm8k \
  --steps 20 --maximum-examples 64 --evaluation-examples 16 \
  --seeds 42,43,44 --device cuda

# UltraFeedback：同模型、同数据、同预算 DPO/ORPO
auto-research checkpoint-post-train \
  --objective dpo --dataset ultrafeedback \
  --steps 20 --batch-size 2 --gradient-accumulation 2 \
  --mixed-precision auto --device cuda

auto-research checkpoint-post-train \
  --objective orpo --dataset ultrafeedback \
  --steps 20 --batch-size 2 --gradient-accumulation 2 \
  --mixed-precision auto --device cuda
```

DPO 使用冻结 reference model；ORPO 是 reference-free 的 chosen NLL 加 odds preference 项。
二者都在同一 tokenizer、长度、batch 和 step 预算下报告 held-out preference accuracy。

## GPU 完整性与恢复

- CUDA A30 默认选择 BF16；不支持 BF16 时回退 FP16，CPU/Mac 使用 FP32。
- 支持真实 batch、gradient accumulation、梯度裁剪和 safe-tensors checkpoint。
- `--save-every N` 同时保存模型、tokenizer、optimizer 与精确 step。
- `--resume-from runs/.../checkpoint-N` 从模型权重和 optimizer state 继续，不从头重跑。
- checkpoint 和数据缓存只保留在本地/开发机，MR 只保存指标与复现命令。

输出 `metrics.json` 会记录模型/数据 revision、license、设备类型、混合精度、resume 起点、
三 seed 均值与标准差。缩小步数只能称为工程 smoke，不能写成稳定算法提升。
