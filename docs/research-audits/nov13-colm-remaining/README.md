# 2026-11-13：24 条 COLM 历史线索核查收口

[English](../../en/research-audits/nov13-colm-remaining/README.md)

本轮逐条处理上轮真实来源快照中的 **24 条待核身份**：收录 23 篇，交付 20 个 L1 机制核及 3 个 L0 接口；另外 1 篇按原文贡献范围明确不纳入。它们不是今天新发表的 24 篇论文，也不是 Google/Meta 全历史穷尽。

## 交付内容

| 领域 | 本地组件 / 接口 |
| --- | --- |
| 基础模型 | Rosetta 表征统一度、LIDAS 层/AdamW 状态生长、Thinking-to-Recall 离线条件分析、Latent Generalization 集合指标、LLM 随机性检验、ECG 联合表示/损失、ContinuousBench 固定评测协议、QE 长度单位、CuE 文化方向、受限 beam 提取概率、StoryScope 特征门控 |
| Agent | Blocksworld 最优性核、SGP 澄清成本与选择、MT-PingEval 私有视图、PolicyBank 结构记忆、Co-Director 分解 UCB、Instruct-to-Act 标注与损失 |
| 后训练 | Social Meta-Learning 成功学生 token SFT、MAPLE 非私有捐赠样例选择、Behavioral Canaries 配对 logprob 审计、RLMF 元认知反馈与优势 |
| 多模态 | AVMeme Exam 反捷径多选评测协议、MMEB-V3 排序与 OmniSET 混合池协议 |

逐篇元数据、原文方法/成本位置、代码来源及最终处置见[完整固定范围](task-scope.json)。[基础模型](foundation-review.json)、[Agent](agent-review.json)、[评测与后训练](evaluation-review.json)保留实际来源 SHA 与核查位置。按一作第一机构聚合，与 Google/Meta 合作作者优先是两个独立字段。

`2601.16355` **Identity, Cooperation and Framing Effects within Groups of Real and Simulated Humans** 是美国政治群体行为的实证模拟研究；本次核查未建立新增可独立实现算法或公开基准的贡献，因此给出有来源的范围排除，不是因 GPU 数量多就否认研究价值，也不伪造一个通用 Agent 实现。

## 真实验证及证据边界

源码先冻结于 `1b7fe8699efd48e6421b01f6df756d6e4086eb52`，再执行 42/43/44：

- 23 个 CPU 组件：实际总耗时约 4.13 秒。
- 7 个 CUDA 组件：单张 **NVIDIA A100-SXM4-80GB**，实际总耗时约 1.47 秒。
- CUDA 范围仅 LIDAS、ECG、CuE、Social Meta-Learning、Instruct-to-Act、Behavioral Canaries、RLMF；没有大模型、公开集全量推理或长训练。

[冻结源码证明](frozen-sources.json)、[原始 CPU 结果](raw-cpu.json)、[原始 CUDA 结果](raw-cuda.json)、单篇旁的三种子指标，以及 7 份脱敏 GPU 回执构成可离线核对的链条：

```bash
PYTHONPATH=src:scripts python scripts/curate_nov13_colm_evidence.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
```

这些命令只核证据，不重跑 GPU。小张量或明确夹具的三种子不是正式模型比较，控制/计分通过不等于文化理解、推理、工具使用、隐私或模型效果提高。所有条目都保留 `diagnostic_only=true`、`promotion_eligible=false`、`evolve_integrated=false`。PolicyBank 和两项多模态基准接口是 **L0**，不升级为能力实现。

完整模型实验均未运行。22 篇有原文模型/数据/实验矩阵依据，明确**成本过高，不复现（审查 DONE）**；Latent Generalization 的私有 Gemini SFT/教师/RL 链路单独标记 `not_reproduced_private_dependency`，不编造公开 GPU 卡时。AVMeme 数据访问条件、未确认发布的源码以及不同媒体许可均逐项保留，不绕过访问门槛。没有为了测成本而加载权重或试训，亦不进入自动重试队列。

## 学习区与双语

23 篇均补中文解读、逐页校对英文和原论文关键图；每篇基础/机制/比较/实现四层问答，共 **92 道独立问答及对应英文**。专题卡片增加 23 份有明确比较对象、方法边界和源指纹的精读更新。计分接口、论文原文结果和本地诊断在学习区与看板中分开，不以满分夹具伪装能力。

## 历史对账和覆盖范围

[当前对账](historical-source-reconciliation.json)显示原先捕获的 28 个身份现在是 **27 个已收录、1 个实质审查排除、0 个待核**。这关闭的是固定来源中的身份，不等于所有官方页面都抓取成功；其余 **4 项来源例外**保留，不能用零待核掩盖未覆盖页面。

上轮[28 身份快照](../nov13-history-repair/historical-source-reconciliation.json)保持原样，展示当时 24 条待核的真实状态，不重写为“早已审过”。本轮没有做新的日期窗口扫描，审查水位仍为 **2026-11-09**。

用户指定的 #250 在本轮开始时已合并，无法继续追加提交。用户随后确认将这24条全部成果放进一个关联 #250 的统一后续 PR，目标仍为 #250 原目标分支 `codex/nov06-priority-papers`，避免把未合入 main 的既有 #244 内容重复带入本轮差异。此处不执行合并或部署。
