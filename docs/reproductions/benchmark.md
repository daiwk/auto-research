# 搜广推与 LLM 应用统一评测协议

本页统一数据切分、基线、指标和报告语义。它不要求 145 篇论文都与 DIN 横向排名：
不同任务只在**相同数据、候选集、预算和目标**下公平比较，论文线上 A/B 永远单列。

## 评测分层

| 评测层 | 适用方法 | 默认公开数据 | 主指标 |
|---|---|---|---|
| 全物品召回/排序 | DIN、SASRec、生成式召回、LLM 推荐增强 | MovieLens-100K / 1M、Amazon 5-core | Recall/Hit@K、NDCG@K |
| CTR/CVR 与多任务 | DeepFM、ESMM、MMoE、PLE、TWICE | 公开交互构造的曝光/转化任务 | AUC、logloss、任务平均值 |
| 新鲜度与探索 | PinCLIP、Pinequalizer、YouTube Freshness | 带时间戳的 MovieLens split | fresh Hit/NDCG、head share、总体质量 |
| 长期价值与广告决策 | SWAG、GrowthGR、Causal Retrieval | 可审计的时间窗或 logged-policy proxy | value/uplift proxy、约束满足、排序质量 |
| 纯 LLM 组件 | Penelope、Engram、Mamba、稀疏注意力 | WikiText-2 / Tiny Shakespeare | validation loss、PPL、参数与计算代理 |
| 系统/Agent 机制 | Melo、NOVA、EvoRec | 确定性公开 mini-suite | 成功率、成本、重试/验证/进化诊断 |

## 推荐任务公共口径

### 数据与切分

1. 按用户和时间排序交互；
2. 默认使用 leave-two-out：倒数第二条作为 validation，最后一条作为 test；
3. 训练阶段只读取更早历史，禁止 validation/test 泄漏；
4. 评测对全部有效物品排序，不用只含一个正例的随机负采样夸大指标；
5. 同组基线与实验组共享用户、物品、候选集合、split 和 seed。

统一 DIN 路径使用 MovieLens-100K、全物品排序和 seeds 42/43/44。历史上
SERAL、LEADRE、COBRA、ARGUS、GR4AD、MM-LLM 使用同一 DIN NDCG@10
`0.02167`；Cross-domain KD 使用独立 target split 的 DIN `0.05518`，两者不能
直接横向比较。

### 指标

$$
\operatorname{NDCG@K}
=\frac{1}{|\mathcal U|}
\sum_{u\in\mathcal U}
\frac{\sum_{r=1}^{K}(2^{rel_{u,r}}-1)/\log_2(r+1)}
{\operatorname{IDCG@K}_u}.
$$

- `Hit/Recall@K` 衡量正例是否进入前 K；
- `NDCG@K` 同时考虑命中与位置；
- `fresh Hit/NDCG` 只在新物品子集统计；
- `head share` 是曝光集中度 guardrail，下降不自动等于总体效果提升；
- AUC/logloss 只用于点式 CTR/CVR 任务，不与全物品 NDCG 混排。

## 纯 LLM 公平口径

结构实验必须共享 tokenizer、context length、训练 token、optimizer 预算、seed 和
validation 数据。除主 loss/PPL 外同时报告：

- 参数量和实际 device；
- architecture-specific 诊断，如稀疏边数、递归次数、cache compression；
- 相同 step 数下的初始/最终 loss；
- 负结果和短预算不稳定性。

不能用参数更大、训练 token 更多或不同 tokenizer 的结果宣称结构本身提升。

## 本地基线规则

每篇论文页必须写明：

> **本地对照口径**：基线是什么，实验组改了什么，主指标相对变化是多少。

基线优先顺序为：

1. 论文直接对照且本地可实现的模型；
2. 相同任务最接近的已实现骨架；
3. 机制隔离 baseline。

DIN 不是所有论文的强制基线。广告出价、延迟 CVR、纯 LLM 架构或 Agent 系统若硬套
DIN，会制造不可解释的百分比；这些任务采用各自同目标基线，并在页面明确说明。

## 线上证据与本地实验

| 结果类型 | 可以说明什么 | 不可以说明什么 |
|---|---|---|
| 论文线上 A/B | 原系统在论文流量和产品条件下的业务变化 | 本地复现达到同样收益 |
| 论文离线结果 | 原模型在论文数据/benchmark 的效果 | 替代线上业务效果 |
| 本地公开数据实验 | adapter 核心机制在公开口径下可运行及其方向 | 原论文私有数据已被完整复刻 |
| 本地负结果 | 当前数据、预算和实现下未迁移收益 | 论文结论被普遍否定 |

Melo 等系统级 A/B 还需单列整体产品归因；TWICE 等全流量论文也必须保留原始指标名，
不能把 expected revenue、conversion 和普通排序 NDCG 混为同一效果。

## 可复现产物

每个 adapter 至少保存：

- 独立论文 README；
- `metrics/*.json` 固定 seed 指标；
- 完整论文元数据和原作者代码状态；
- 原论文关键图及来源；
- adapter key、本地代码路径、运行命令和保真边界。

常用验证命令：

```bash
PYTHONPATH=src pytest -q tests/reproductions
PYTHONPATH=src pytest -q tests/reproductions/test_documentation_catalog.py
python -m mkdocs build --strict
```

新增或更新实验后，正向、负向和跨 seed 不稳定结果都必须保留；checkpoint 只保存在
本地，不提交 GitHub。

