# Google EMNLP 历史25条：逐篇核查与低成本组件

本轮严格覆盖用户批准的 **25条历史线索**，不把会议收录、首次发现或revision日期当作新首发。结论为 **14项独立L1组件、8篇高成本完整实验不复现、3篇不接收**；原会议页另外4条链接例外不在这25条里，没有冒称一并全文审结。

完整方法、精确v1UTC、一作首机构、Google合作证据、原作者代码固定版本/许可证、成本依据与决定保留在[逐篇审查](review-decisions.json)和[固定范围/验收状态](task-scope.json)。保留[最初元数据快照](../oct25-priority-components/google-emnlp-title-identity-audit.json)，不改写当时尚未审查的历史记录。

## 14项低成本组件

这些入口执行真实的数值算子、梯度或离线协议，不是14个完整大模型/Agent。真实SAE、模型输出、teacher scores、verifier和环境等外部输入不能用启发式伪装。所有组件均为 `L1 / diagnostic_only`，不作正式能力对比，也不进入Evolve晋级。

| 论文 / 组件 | 已实现的精确范围 | 未实现的完整路径 |
| --- | --- | --- |
| [SCAR](../../post-training/2505.20417-scar-shapley-credit/README.md) | 小博弈精确Shapley、signed credit、span末尾奖励和alpha插值 | 无真实RM评分、语法分段、Owen近似或RLHF训练 |
| [概率autorater](../../post-training/2510.00263-probabilistic-autorater/README.md) | 分段Brier/clip-log奖励与失败解析惩罚 | 不训练文本autorater，数值梯度不等于对文本解析反传 |
| [RM记忆协议](../../post-training/2607.24484-rm-memorization-protocol/README.md) | 逐run概率的TM/TG/CM及user级切分一致性 | 不生成25个RM，不以合成分数宣称模型记忆能力 |
| [Benchmark self-bias](../../post-training/2509.26600-benchmark-self-bias/README.md) | 逐segment排名、leave-self-out自偏与显式方向/tie约定 | 不运行翻译/LLM judge，不把peer consensus当绝对真值 |
| [DMAST](../../agent-research/2603.04364-dmast/README.md) | 攻击模式隔离、共享role原始组统计、长度罚与clipped GRPO/IS/KL | 不含浏览器、攻击器生成、多阶段SFT或真实自博弈 |
| [SOPBench协议](../../agent-research/2503.08669-sopbench-protocol/README.md) | Single/And/Or/Chain过程检查与三项联合验收 | 只做轨迹后评分，不重建七域工具或Agent |
| [FinanceHarness协议](../../agent-research/2607.27853-finance-harness-protocol/README.md) | PIT search/read双重日期门、失效run拒绝、逐题等权rubric | 不含私有语料、检索ranker、judge或金融研究智能 |
| [Cue2Narrate DRL](../../multimodal-models/2609.01725-cue2narrate-drl/README.md) | masked SFT与当前policy正负caption排序loss | 不含定位器、电影数据、负caption生成或VLM训练 |
| [POLARIS HRI](../../post-training/2606.04095-polaris-hri/README.md) | policy-only统计、human-reference warmup及共同clipped surrogate | 不含人类版权故事、LLM rubric judge或9B训练 |
| [TaskPress](../../foundation-models/2608.03276-taskpress/README.md) | task attention×value量化scale、逐head topk、实际KV gather及原位置 | 不含task-guide生成/演化、GQA策略或量化内核/速度结论 |
| [组合水印](../../foundation-models/2510.01637-combinatorial-watermark/README.md) | pattern logit bias、cyclic匹配、global/local编辑分数 | 不含secret分区生成、真实LLM输出或正式FPR校准 |
| [插值null校准](../../foundation-models/2609.17764-interpolated-null-calibration/README.md) | 对齐三pass分数的插值校准、端点与排序 | 不含attention提取器或真实检索能力比较；权重仅可validation选择 |
| [XLGoBench](../../foundation-models/2605.30788-xlgobench/README.md) | 五类算法题结构生成、exact scorer和gold隔离的callback | 不含官方七语模板、人工翻译验证或LLM能力结果 |
| [Mechanistic ETM](../../foundation-models/2507.23220-mechanistic-etm/README.md) | 冻结SAE encoder的Binomial ELBO、独立decoder的topic steering | 不含真实SAE/LLM、topic judge或完整八数据集矩阵 |

## 8篇完整实验高成本，不复现

以下是**审查DONE / 未复现**，不是待算力TODO，不提供伪指标、可执行入口或GPU收据，也不自动重试。上节14项对应的完整模型实验同样未运行。

| 论文 | 原文成本 / 不复现原因 |
| --- | --- |
| [AgentDebugX](../../agent-research/2607.18754-agentdebugx/README.md) | 9B/27B与多API诊断、长时搜索和修复重跑；部分归因协议使用参考答案，不能冒称无gold能力 |
| [LifeAgentBench](../../agent-research/2601.13880-lifeagentbench/README.md) | 作者报告全评测300–500GPU小时、13模型；不把普通scorer替代其LifeAgent |
| [CoReflect](../../agent-research/2601.12208-coreflect/README.md) | 953场景、三轮、多大型模型与reflective analyzer；状态机不能代替语义共演化 |
| [Sparse-to-Dense Principle](../../post-training/2605.12483-sparse-to-dense-reward-principle/README.md) | 作者direct GRPO约50.2H200小时，teacher-first约4–6倍；不重命名已有KL算子冒充整套经验流程 |
| [跨script知识迁移](../../post-training/2603.17070-cross-script-knowledge-transfer/README.md) | 120B/30B、真实LoRA与多语长推理；不以正则音译或手工提示替代 |
| [跨语知识探索](../../foundation-models/2606.24579-cross-lingual-exploration/README.md) | 约234K探索路径和多前沿模型/LLM聚合判定；不以字符串投票替代 |
| [NaijaS2ST](../../multimodal-models/2604.16287-naijas2st/README.md) | 约269小时语音、多方向模型训练、ASR/TTS与人工评审；不以文本exact-match替代 |
| [MVEB](../../multimodal-models/2606.14958-mveb/README.md) | 33checkpoint与23/184任务；作者单H100对一模型报告31.9/302.7小时 |

## 3篇未接收

- [AgenticTagger](https://arxiv.org/abs/2602.05945v1)：正文私有ranking数据为离线实验，未确立量化生产A/B或已授权全流量证据；Google合作优先但不豁免门槛。target-item critique泄漏不能包装为公平能力提升。
- [How Coding Agents Fail Their Users](https://arxiv.org/abs/2605.29442v1)：观察性会话与人工质性研究，不是新可执行coding policy；不造规则分类器冒充论文方法。
- [What Limits Us?](https://arxiv.org/abs/2609.15191v1)：人审codebook的科研元分析，不把人工批准流程冒充自主RSI算法。

## 验收与完整性

14项全部通过成本门槛后才执行小规模诊断；10项有CUDA路径，另4项为纯CPU协议/参考实现。本批没有下载大模型、原始视频/音频、私有数据或大索引，没有试跑昂贵完整实验。

最终源码提交与实测时间见[CPU原始结果](raw-cpu.json)、[A100原始结果](raw-cuda.json)和[portable Git证明](frozen-sources.json)。每篇保留独立 `metrics/component-<device>-seeds42-44.json`；GPU回执只含模型型号、命令、seed、来源commit和数值，不含主机/用户/驱动信息。

最终冻源为 `4cce1ab4d701df8daaed9a8abe8671f3eef9d168`：CPU14组件×3seed约2.00秒，真实A100的10组件×3seed约1.61秒。这里只计组件执行，不含导入、连接、同步或测试；**不是完整模型训练时间**。DMAST新增的零IS/关闭KL极端分支也在这次A100诊断中真实执行，不沿用修复前的结果。

```bash
python scripts/curate_google_emnlp25_evidence.py --check
python -m pytest tests/test_google_emnlp25_closure.py
```

验收检查25个精确输入身份、原题名、日期/机构/catalog别名、每项状态、14组件check/metric集合和数值门槛、三seed、每seed实际设备、CPU/CUDA同冻源、raw→单篇指标→收据一致。缺项、重复、错误身份、CPU冒充GPU、改称能力复现或重开高成本自动队列均失败。

交叉审查修复POLARIS clipped exp的NaN反传、mETM encoder/decoder混用，以及DMAST零IS分支的无用指数。只修数值求值或恢复原公式，不以额外clamp改目标。原图22张均保留固定来源、版本、许可和SHA；方法版本与v1首发时间分开记录，机构按一作首署名单位聚合。

**本批25条已作明确处置，不再是25条未读队列；完整模型实验没有被宣称已实现。全局审查水位仍为2026-10-15**，这不是所有Google论文或全时间窗口的穷尽审查。
