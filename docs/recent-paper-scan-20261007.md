# 2026-10-07：重叠扫描、两篇真实模型实现与未完成队列

## 先看结论

本轮实现 [FrugalEvo](agent-research/2610.03675-frugalevo/README.md) 和 [Sentry](agent-research/2610.02994-sentry/README.md) 的独立控制器与公开 checkpoint 执行路径。它们均首次发表于 **10 月 2 日**，属于前轮候选的实现，不是今天新发表。真实 A100 运行与单篇指标分开记录；没有注册成已经完成统一 Evolve 集成的算子。

另外五篇完成了方法与实现条件复核，**仍未实现**，详见下表。新发现的 Airbnb SIFT 与 Google TEE-FL 也只是证据明确的待实现项，不能计入已实现篇数。

## 扫描覆盖与数字口径

窗口为 **2026-10-01 至 2026-10-07**。四条主轨使用官方 arXiv 查询，查询传输均返回，但每查询上限 400，部分触顶；机构目录还有超时。`coverage_complete=false`，最后完整水位保持 **2026-10-02**，下次仍保留 10-01 重叠窗口。没有使用 DeepXiv。

| 查询轨道 | 标题命中 | 请求窗口内未登记命中 | 触顶查询 / 总查询 |
|---|---:|---:|---:|
| 搜广推与 LLM 应用 | 39 | 31 | 5 / 22 |
| 基础模型（含多模态交叉） | 453 | 398 | 8 / 8 |
| 后训练 | 200 | 164 | 7 / 8 |
| Agent（含 RSI/Jev 交叉） | 434 | 381 | 8 / 8 |

这些是**宽查询候选**，不是满足门槛的新论文数。跨轨去重后为 1,010 条，含已实现、窗口外相关项和未审项；不能把四行相加当作新增论文数。完整标题池和机器回执已落盘，避免下一轮只看到一个大数字：

- [去重标题池](research-audits/oct07-title-pool.json)
- [查询覆盖回执](research-audits/oct07-query-coverage.json)
- [机构/会议来源回执](research-audits/oct07-official-source-coverage.json)
- [上一轮 48 个 Agent 标题的逐项初筛](research-audits/oct07-agent-48-triage.md)

上一轮的“48”指请求窗口 10-02～10-06 内未登记标题；69 条来自额外 10-01 重叠日，另有 28 条更早相关项。48 条已逐项做标题/摘要判断，**不等于 48 篇全部完成全文复核**。

Google Research 三页、Meta 两页自动抓取超时；DeepMind 的 9 页、265 个出版物记录读到，但身份匹配预算有限，状态仍为 partial。手工官方页复核补出下面的 Google 论文，不能用自动待审队列为 0 来断言没有遗漏。

## 优先机构与新增工业证据

| 优先级 | 论文与时间 | 已核验证据 | 当前决定 |
|---|---|---|---|
| P0 · Google | [Toward provably private learning from federated data](https://arxiv.org/abs/2609.31494)，首次 09-25；[官方发布](https://research.google/blog/toward-provably-private-learning-from-federated-data/) 10-02 | 正文 §5.3：每组 350 万设备，隐私预算约降至三分之一，关键输入体验指标持平；训练从两个月降至三周 | **旧文补发现**。符合生产证据门槛；TEE 远程证明、KMS、DP 与可复现构建才是核心，普通 CUDA 模拟不能证明隐私保证；未实现 |
| P0 · Airbnb | [SIFT](https://arxiv.org/abs/2610.07810)，首次 10-06 | PDF 第 7 页 §8.2/表 4，随机身份分流：推荐过滤器点击人数 +20%，普通 booking 护栏 +0.03% 不显著；第 8 页表 6 的酒店扩展实验才有市场总未取消预订 +0.76% | **近期新文**。满足线上门槛；原始旅程/过滤器/数值容量标签尚无公开等价数据，未实现 |

Meta 官方页面补看了近期 AI 辅助数学结果与既有 MaDRL 入口；前者不直接当作模型训练算法，后者不重复登记。该定向检查不代表 Meta 全部官方目录已审完。

## 五篇候选的方法核查与验收缺口

这里的“未完成”不表示论文不可做，也不以作者暂未开放训练代码作为永久拒绝理由；它明确下一步不能省略的执行链。

| 论文 | 不可替代的核心 | 仍需完成的实际工作 |
|---|---|---|
| [Dynamic Expert Pruning](https://arxiv.org/html/2610.02951v1) | 提示条件的逐层专家预测；REAP 校准目标、BCE 和软掩码 KD；真实稀疏专家驻留/差分加载 | 获取真实 MoE 和工作流校准轨迹，训练预测器，测质量/峰值显存/加载成本。不能用稠密层剪枝或理论显存代替 |
| [RC-OPD](https://arxiv.org/html/2610.03515v1) | 首个错误锚点修复、学生在已修前缀后续写、多轮成功链的局部蒸馏与预算回退；附录 B.6 是逐词表项上截断，不是普通 KL | [作者仓库](https://github.com/Starrylay/RC-OPD)当前为评测与 checkpoint，训练未开放。独立实现仍需真实诊断/续写/训练链和无泄漏对照，不能只交一个 loss 函数 |
| [Recursive Harness Self-Improvement](https://arxiv.org/html/2610.03548v1) | 固定 verifier；在线技能与批后候选副本隔离；同 cohort 有效性、难度和成本 gate，最多三次失败回退 | 接真实生成器与可验证任务，记录被拒提案及所有成本；零准确率按附录特殊处理，不能把随机难度分数当验收 |
| [Pivot-SD](https://arxiv.org/html/2610.03665v1) | 冻结 masked-diffusion 去噪轨迹，剩余掩码位置的熵下降选 pivot；成功 CE、失败仅 pivot unlikelihood | LLaDA/Dream 真 checkpoint 的预提交掩码状态采集和训练，独立 benchmark；自回归 Qwen 的 token 熵不能冒充扩散轨迹 |
| [KV²](https://arxiv.org/html/2610.03198v1) | 分块代理选重建 query、在完整 KV 后实际重建、逐头注意力打分和全局压缩；不是只做 top-K | 核对 KeyDiff 实现、实际 KV/位置编码接口，完成 CUDA 重建及长上下文质量/延迟/显存对照；本轮没有实现或 GPU 回执 |

## 后续执行顺序

1. 先处理 Google TEE-FL 的可公开复现边界和 SIFT 数据映射；不能因私有日志而伪造线上标签。
2. RC-OPD、KV² 优先做完整可执行路径；Dynamic Expert Pruning、Pivot-SD、Harness 按上表准备模型/环境和真实验证。
3. 继续标题池的定向全文复核与失败来源补扫。查询触顶、未审项和身份不明项均保留，覆盖完成前不推进水位。

统一待办仍只维护在[路线图](research-roadmap.md)；本页是本次扫描与交付的固定审计快照。
