# MaD-RL：分布匹配奖励的轻量机制实验

> 这是可运行的**机制诊断**，尚未进入正式论文复现目录。现在既有字符 GRU 多种子对照，也有 Qwen3-4B 真实 checkpoint 的单 token 诊断；两者均不使用原文数学／代码基准，不代表原论文成绩。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Meta 官方论文页](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/) |
| 公司 / 机构 | Meta Superintelligence Labs |
| 首次公开日期 | 2026-09-23（论文 PDF 落款）；Meta 官方论文页发布于 2026-09-24 |
| 原作者代码 | 截至 2026-09-29 未找到公开源码 |
| 本地 adapter / CLI key | `mad-rl`（独立机制实验，非正式论文 adapter） |
| 本地复现代码 | 奖励与字符策略：`src/auto_research/post_training/mad_rl.py`；Qwen3-4B CUDA 诊断：`scripts/mad_rl_qwen_choice.py` |

原文提出在一组输出上估计类别频率，再用目标分布与经验分布的差构造逐样本奖励。这里实现了 L2、forward KL、reverse KL、Jensen–Shannon 四种奖励，并以纯正确性奖励作对照。五个选项均是有效回答；训练期间不会把目标选项作为单条答案提供给策略。无效输出计入频率分母并受固定惩罚。零概率目标类别在对数奖励中使用数值平滑。

本地用 32 维字符 GRU、单 token 自由采样、组相对优势和 clipped policy update。先在训练主题上进行平衡 SFT 预热，然后训练 60 步；8 个训练主题、2 个验证主题、2 个测试主题不重叠。每种奖励从相同 seed 的初始策略出发，以 42、43、44 三个种子独立运行。测试集只在训练结束后读取。

```bash
auto-research mad-rl --target 0,0,0.3333333333333333,0.3333333333333333,0.3333333333333333 \
  --seeds 42,43,44 --steps 60 --group-size 16 --device cpu \
  --output-dir runs/post-training/mad-rl-peaked

auto-research mad-rl --target 0.2,0.2,0.2,0.2,0.2 \
  --seeds 42,43,44 --steps 60 --group-size 16 --device cpu \
  --output-dir runs/post-training/mad-rl-uniform
```

两组本地实验的三种子平均值如下。指标为**有效选项条件下**的 test Jensen–Shannon divergence，越低越好；无效输出率另行记录，不把其从采样分母中隐藏。

| 奖励 | 尖峰目标：训练前 → 训练后 JSD↓ | 均匀目标：训练前 → 训练后 JSD↓ |
|---|---:|---:|
| 纯正确性 | 0.1749 → 0.1521 | 0.0064 → 0.0101 |
| L2 | 0.1749 → 0.0159 | 0.0064 → 0.0048 |
| forward KL | 0.1749 → 0.0048 | 0.0064 → 0.0076 |
| reverse KL | 0.1749 → 0.0064 | 0.0064 → 0.0061 |
| Jensen–Shannon | 0.1749 → 0.0052 | 0.0064 → 0.0072 |

尖峰目标上，分布奖励比纯正确性控制更接近目标；均匀目标的训练前 JSD 已很低，并非所有奖励都会继续改善。这个结果只支持**本地小模型分布匹配机制可执行**，不能推出原文的大模型结论或跨任务泛化。实验 JSON 与 Markdown 报告由上述命令生成，可逐 seed 核查。

## Qwen3-4B 真实 checkpoint 诊断（A100）

另用公开 `Qwen/Qwen3-4B-Instruct-2507`、同一五选项主题任务，执行 rank-8 LoRA 平衡预热 15 步，再以原文 Jensen–Shannon 类别奖励做 8 次组相对更新；每组 16 个**真实模型 next-token 采样**，无效 token 仍计入完整分母。训练、验证、测试主题分别为 8／2／2 个。它验证大模型参数与类别奖励路径可执行，但仍**不是**原论文的多语言 GSM8K／代码自由生成任务。

```bash
PYTHONPATH=src python scripts/mad_rl_qwen_choice.py \
  --checkpoint /path/to/Qwen3-4B-Instruct-2507 \
  --output runs/post-training/mad-rl-qwen-choice.json \
  --seed 42 --warmup-steps 15 --steps 8 --group-size 16 \
  --eval-samples 16 --divergence jsd
```

| 验证指标 | 预热后、RL 前 | 8 步后 |
|---|---:|---:|
| 有效类别内目标 JSD ↓ | 0.4127 | 0.4127 |
| 有效输出率 ↑ | 1.0000 | 1.0000 |
| 类别计数 A/B/C/D/E（32 次） | 16/0/16/0/0 | 16/0/16/0/0 |

可训练 LoRA 参数变化 L2 为 `0.0982`，但这 32 次验证采样没有朝指定 C/D/E 混合目标靠近，不能据此宣称大模型分布匹配成功。独立测试主题在训练后评估，JSD 为 `0.6398`；样本太少，不作泛化结论。GPU、公开 checkpoint 修订与命令见[净化后的验证凭据](../gpu-validations/mad-rl-qwen-choice-a100-20260929.json)。

## 正式收录前还缺什么

- 取得原论文 PDF 中的真实关键图，并按仓库统一论文页合同保存原图；当前 Meta 官方 PDF 下载在本地与 A100 环境均不可达，不能用自绘图冒充原图。
- 使用公开、可核验的数据和语言模型 checkpoint 重做原文级别的数学／代码自由生成任务、目标分布及原文基线；不能把本页的单 token GRU 或 Qwen3-4B 诊断称为论文完整复现。
