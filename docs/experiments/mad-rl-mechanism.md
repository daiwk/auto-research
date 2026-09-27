# MaD-RL：分布匹配奖励的轻量机制实验

> 这是可运行的**机制诊断**，尚未进入正式论文复现目录。它不使用原文 Qwen3-4B、数学/代码基准，也不代表原论文成绩。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [Meta 官方论文页](https://ai.meta.com/research/publications/mad-rl-matching-distributions-for-calibrating-llms-with-reinforcement-learning/) |
| 公司 / 机构 | Meta Superintelligence Labs |
| 首次公开日期 | 2026-09-24（Meta 官方论文页） |
| 原作者代码 | 截至 2026-09-27 未找到公开源码 |
| 本地 adapter / CLI key | `mad-rl`（独立机制实验，非正式论文 adapter） |
| 本地复现代码 | `src/auto_research/post_training/mad_rl.py` |

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

## 正式收录前还缺什么

- 取得原论文 PDF 中的真实关键图，并按仓库统一论文页合同保存原图；当前 Meta 官方 PDF 下载在本地与 A100 环境均不可达，不能用自绘图冒充原图。
- 使用公开、可核验的数据和语言模型 checkpoint 重做原文级别的数学/代码任务、目标分布及原文基线；不能把本页的单 token GRU 诊断称为论文完整复现。
