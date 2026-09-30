# 2026-09-30 四领域扫描收口

扫描窗口为 2026-09-28 至 2026-09-30，覆盖推荐/搜广推、基础模型、LLM 后训练和 Agent。arXiv 各查询页没有使用缓存回退；Google Research、Google DeepMind、Meta 及 RecSys/SIGIR 官方目录分别记录传输状态与身份对账状态。DeepXiv 未使用。

## 官方来源修复

- 12 个静态官方会议来源建立了 906 个标题的显式快照；快照只表示已经检查过目录库存，不代表论文通过收录或复现门槛。
- 日常扫描只审查静态目录新增标题；不再把整届会议的历史标题误报成“当天新增”。
- 动态官方研究页先打开论文详情解析直接 arXiv 链接，再做精确标题对账；传输健康、分页缺口和身份未解析分别记录。
- 修复后推荐方向本窗口官方身份待核队列从 886 条降为 0；这是对账结果，不是静默过滤。

## 本批实现

| 领域 | 论文 | 本地级别 |
|---|---|---|
| 推荐 / Evolve | EvoSkillRec；PromptShift | typed genome 晋级复用闭环；列表漂移与自适应 rerank |
| 基础模型 | Telescopic Language Models；FRAC | 随机前缀 + full anchor；分数阶有限模态递归 |
| 后训练 | RFPO；OLIVE；ROSS；R²-OPD；MAS-OPD | Critic/GAE、续写监督、选择性历史监督、奖励重加权、多 Agent OPD |
| Agent | Dr.Credit；CCM；SAGE；Certified Selective Automation；Mnemon | 过程信用、有界上下文、安全门、任务簇证书、Jev 记录视图 |

所有条目均提供可执行 reference kernel、三种子诊断 receipt、中文边界说明和原论文关键图。`diagnostic_only=true` 的 mini-suite 只证明机制可执行，不声称复现论文规模效果。

## 已审但本批不实现

- DaRoPE（2609.34556）：与现有 RoPE/长上下文算子重叠，缺少本批可独立验证的真实 checkpoint 增量协议，暂缓。
- Harness Evolution（2609.36892）：定义性贡献依赖可编辑真实 harness 与跨代执行反馈，不能用静态 tensor 替代。
- General Asynchronous Agents（2609.35427）：需要异步工具执行环境和同预算延迟/成功率评测，暂缓。
- Typed memory / Jev（2609.34227）：和已实现 Mnemon 的 raw-record + Jev 路径重叠，保留为后续真实 checkpoint 对照候选。

下一次扫描可从 2026-10-01 开始，并保留至少两天公告重叠窗口；不会再次重扫整届静态会议目录。
