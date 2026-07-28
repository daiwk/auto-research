# 论文实现与评测库

论文实现是研究工作流，不是单一业务领域。仓库用统一的论文信息、实现、数据和指标
合同承载搜广推、纯 LLM 与 Agent；实现成熟后，还可以作为 mutation、训练目标或
evaluator 接入[自动研究与进化](auto-research.md)。

## 三个内置领域

### 搜广推与 LLM 应用

面向互联网公司的推荐、搜索、广告、生成式推荐以及 LLM 与这些系统的结合应用。
该领域坚持真实线上 A/B 硬门槛，并在本地使用公开数据、公平基线和统一对照口径。

- [进入工业论文实现库](reproductions/README.md)
- [按公司](reproductions/catalog/by-company.md) ·
  [按主题](reproductions/catalog/by-topic.md) ·
  [按年月](reproductions/catalog/by-month.md)

### 纯 LLM

覆盖网络结构、预训练、数据配方和后训练。纯 LLM 论文不强制生产 A/B，而是要求论文
给出可信公共 benchmark、明确训练预算和可核验方法；本地结果必须说明模型规模折损。

- [LLM 后训练研究总览](post-training/README.md)
- [后训练方法索引](post-training/catalog.md)
- [后训练统一评测协议](post-training/benchmark.md)
- 纯 LLM 架构与预训练实现可从[按主题目录](reproductions/catalog/by-topic.md)中的
  “纯 LLM”章节进入

### Agent

覆盖长期记忆、规划与反思、工具使用、多 Agent 协作和自我进化。当前优先实现可在
本地重复执行的机制与 mini-suite，再逐步接真实 LLM executor 和完整 benchmark。

- [Agent 论文研究总览](agent-research/README.md)
- [Agent 方法索引](agent-research/catalog.md)
- [Agent 统一评测协议](agent-research/benchmark.md)

## 统一论文合同

每篇论文页都必须包含：

1. 论文链接、公司/机构、首次公开日期和原作者代码；
2. 本地 adapter 与实现目录；
3. 背景、主要改动、架构图和核心公式；
4. 原论文离线/线上结果与真实对比基线；
5. 本地公开数据协议、稳定指标、运行命令和失败结果；
6. 相对原论文的保真边界。

不同领域可以有不同筛选门槛，但不能混用结果口径：工业 A/B、公共 benchmark 和
本地机制验证会分别标注。

## 与自动进化的关系

```mermaid
flowchart LR
    P["论文实现"] --> C["可复用组件"]
    C --> M["Mutation / training objective"]
    C --> E["Evaluator / benchmark"]
    M --> A["Auto Research"]
    E --> A
    A --> X["并行实验与多轮进化"]
    X --> R["稳定结论回写论文库"]
```

论文实现先回答“方法是否被正确理解并能运行”，自动进化再回答“将这些方法组合到
当前系统后，什么配置在给定数据和预算下更优”。
