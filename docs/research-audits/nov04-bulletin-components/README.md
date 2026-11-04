# 11月4日公告批：14篇论文与低成本机制组件

本批依据实际获取的 **2026-11-04 arXiv公告**，交付12个低成本组件，并收录2篇高成本论文。这里的“新”指本次公告首次收录，不等于论文今天首发：12篇来自new栏目，RuntimeTickets来自cross-list，RSI-Dojo是10月29日首发的延迟公告补漏。14篇均不是上轮抓取之后才首次公开的论文。

## 固定交付范围

| 方向 | 论文 | 本地交付 | 未复现的完整实验 |
| --- | --- | --- | --- |
| 工业推荐 | [ReuseGR](../../recommendation-components/2611.04259-reusegr/README.md) | CPU：整行留一深度标签、祖先复用判据、路由和组合评分 | 学习型BudgetCut、PathKD与私有广告检索系统 |
| 工业推荐 | [SPADE](../../recommendation-components/2611.04662-spade-local-search/README.md) | CPU：OA-BPE非重叠合并与SDBS单步扩展 | STAR训练、MARS-DPO与生产搜索服务 |
| 工业推荐 | [OneTrans GSR](../../recommendation-components/2611.04720-onetrans-gsr/README.md) | CPU：约束参考算子、奖励与独立优势归一化 | 学习型RM、GMRPO策略训练与线上混排；本地FP64不是原文位级FP32实现 |
| 基础模型 | [Semantic-Block Sparse Attention](../../foundation-models/2611.04313-semantic-block-sparse-attention/README.md) | CUDA：语义块路由、GQA聚合与因果可见性 | 真实长上下文模型和端到端吞吐矩阵 |
| 基础模型 | [Anchor KV](../../foundation-models/2611.04327-anchor-kv/README.md) | CUDA：外部写入状态、逐层读映射与门控 | LaCT动量/Muon完整内循环训练与大模型评测 |
| 后训练 | [Density-Aware Reward Scaling](../../post-training/2611.04792-dars/README.md) | CUDA：含自密度的高斯KDE、奖励缩放与组归一化 | 完整RL训练；稳定键为`dars-density`，不覆盖已有Dependency-Aware DARS |
| 后训练 | [P²-MOPD](../../post-training/2611.03953-p2-mopd/README.md) | CUDA：参数先验优化器与双通道梯度参考 | 多教师LLM与完整on-policy蒸馏 |
| 后训练 | [Shuffled OPSD](../../post-training/2611.04958-shuffled-opsd/README.md) | CUDA：输入变换、固定参考选择与带符号逐词表权重 | 完整教师/学生训练和任务对照 |
| 后训练 | [Targeted Guidance](../../post-training/2611.05266-targeted-guidance/README.md) | CUDA：失败轮次reverse-KL与停止梯度教师目标 | Agent rollout、提示生成与完整GRPO优化 |
| Agent/RSI | [Meta²](../../agent-research/2611.05139-meta-square/README.md) | CPU：冻结meta-skill、任务内编辑生命周期与公共checkpoint隔离合同 | 真实元Agent/LLM与完整环境搜索 |
| Agent/RSI | [Continual Autoresearch](../../agent-research/2611.05108-continual-autoresearch/README.md) | CPU：运行关闭后的首解、最优曲线、最终选择评分与配对协议 | 实际持续训练、模型调用与大规模实验 |
| Agent安全 | [RuntimeTickets](../../agent-research/2611.03772-runtime-tickets/README.md) | CPU：授权收紧、发送门控与本地HMAC审计链 | 多框架真实网络出口部署；本地链不等于全网可信监控 |
| 基础模型 | [Multi-Layer Indexer](../../foundation-models/2611.03768-multi-layer-indexer/README.md) | 仅资料收录与方法审查 | 原文8×H200的完整服务矩阵 |
| Agent/RSI | [RSI-Dojo](../../agent-research/2611.03698-rsi-dojo/README.md) | 仅资料收录与方法审查 | 每任务约5–10小时的模型训练环境与完整轨迹训练 |

14篇完整实验均标为 **成本过高，不复现（审查 DONE）**，不自动重试。12个可运行组件仅提供L1机制诊断，不是完整能力复现、线上收益复现、端到端服务提速或可执行Evolve接入；2篇资料收录没有伪造算子或指标。

## 真实执行与身份隔离

[成本预审](preflight.json) · [冻结源码证明](frozen-sources.json) · [CPU原始结果](raw-cpu.json) · [CUDA原始结果](raw-cuda.json) · [逐篇范围](task-scope.json)

CPU执行12组件×3种子，A100执行6个CUDA组件×3种子；种子为42/43/44。仅使用小张量、算术和状态合同，零预训练模型调用、零数据/权重下载。运行器内部耗时分别为2.900秒、1.689秒，不包含研究、启动与传输，也不是完整训练耗时。每篇独立保存指标，六个CUDA组件各有脱敏[GPU回执](../../gpu-validation.md)。

旧论文Dependency-Aware Reward Shaping的`post-training:dars`及历史学习记录保持不变。新论文使用`post-training:dars-density`；实际执行时的短标签`dars`保留在不可改写的原始结果中，通过显式映射关联新身份，未改数值、种子或冻结源码。

交叉审查补充了奖励非负约束、极端有限logit下零损失的数值稳定性，以及OneTrans约束生成器在多个候选间被消耗的问题；修正均在冻结源码和实际CPU/A100执行之前完成。规范化指标使用`math.fsum`，避免不同Python版本的末位聚合差异。

## 来源、优先机构与覆盖边界

[来源回执](source-coverage.json)与[公告身份清单](bulletin-records.json)覆盖cs.AI、cs.CL、cs.CV、cs.IR、cs.LG、cs.RO、cs.SD和eess.AS。直接`/new`与`?show=2000`两种路径的日期、条目数和身份一致：1472个含交叉分类/替换的分类条目，1094个去重身份。这是召回量，**不是1094篇全文均已审完**。

[Google/Meta优先复核](priority-review.json)：Google目录30页、Meta目录6页本轮超时，增量未知，不记为零；DeepMind9页成功获取，但未宣称所有详情身份审查完成。官方GitHub最近创建仓库查询和检索仅为有界补充。当前选中14篇没有已核实的Google/Meta作者机构，**Meta²是方法名，不是Meta公司论文**。

本批14篇固定范围已交付；未审公告身份和不可用来源不被伪装成审查DONE。统一审查水位仍为 **2026-10-15**，本批不宣称全窗口穷尽或推进水位。

## 学习卡与中英同步

14篇各新增基础、机制、对比、实现四级问答，共56题；更新对应专题归属、代表方法对照、分析、跨论文自测和绑定当前README指纹的日期记录。论文页保留原图及来源，新增正文、问答和专题单位均有逐项校对的英文版。

[最近问答](../../learning/recent.md) · [全部问答](../../learning/all.md) · [专题精读](../../learning/deep-dives/index.md)
