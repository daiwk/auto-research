# 基础模型研究

基础模型研究覆盖模型在后训练之前和推理期间的核心能力：网络架构、预训练数据与
优化、多模态表征、长上下文以及推理效率。论文详情仍保留在原来的稳定 URL 下，
本目录提供新的逻辑入口，因此已有链接不会因重构失效。

## 研究范围

| 方向 | 主要问题 | 当前公共评测 |
|---|---|---|
| 网络架构 | MoE、状态空间、条件记忆、递归与残差路径 | WikiText-2 perplexity、参数量、训练稳定性 |
| 注意力与长上下文 | 稀疏/门控注意力、位置编码、KV 压缩 | perplexity、attention edges、KV 占用、长上下文任务 |
| 预训练与数据 | 数据清洗/选择、配比、优化器 | 同 token/step 预算 perplexity 与任务指标 |
| 多模态基础模型 | 视觉 token、跨模态检索与统一表征 | 公开多模态 benchmark 或可审计的缩小实验 |
| 推理与系统效率 | 动态计算、量化、推测解码 | 质量、延迟、吞吐、峰值内存与压缩率 |

## 浏览入口

- [方法索引](catalog.md)：查看全部基础模型论文、机构、日期、原作者代码与本地入口；
- [按机构/公司/学校](catalog/by-organization.md)：按一作的第一署名单位聚合；
- [按主题](catalog/by-topic.md)：按“研究方向 → 方法簇 → 论文”浏览；
- [按年份](catalog/by-year.md)：同年论文按首次公开日期倒序排列；
- [论文谱系与缺口](lineage.md)：查看已覆盖的技术主干与下一步缺口；
- [统一评测协议](benchmark.md)：明确质量、计算和复现保真度的共同口径。

## 最新实现

- [RD-AttnRes](../reproductions/2608.01075-rd-attnres/README.md)：在 Block AttnRes 的同一组 residual sources 上分别学习 QK 与 V 深度路由；已接入 micro-LLM evolve，并保留 30-step 本地负结果。

## 与后训练和应用的边界

- DPO、GRPO、OPD、reward model 等训练后目标进入[LLM 后训练](../post-training/README.md)；
- 推荐、搜索、广告中的 LLM 特征、生成式召回和多模态内容应用进入
  [搜广推与 LLM 应用](../reproductions/industrial.md)；
- Agent 的规划、工具、记忆和环境交互进入[Agent 研究](../agent-research/README.md)；
- 同一论文确实跨域时可以从多个主题入口访问，但只有一个稳定详情页和一份本地指标。

## 与 Auto Research 的关系

已通过真实训练和测试的网络算子、数据策略与效率方法可以进入 micro-LLM evolve。
检索到但尚未实现的论文只作为 evidence，不会直接生成未经验证的训练代码。

```mermaid
flowchart LR
  P["论文与公开实现"] --> A["可训练 adapter"]
  A --> G["架构 / 数据 / 效率 genome"]
  G --> E["同预算并行实验"]
  E --> V["Validation 选择"]
  V --> G
  V --> T["隔离 Test 与研究报告"]
```
