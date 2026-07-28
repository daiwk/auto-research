# 自动进化的领域适配

Auto Research 的核心不是某个推荐模型，而是一套开放的研究协议。任意领域只要提供
研究对象、数据、可搜索改动和评测器，就能复用论文检索、并行实验、选择与多轮迭代。

## 统一 adapter 合同

```mermaid
flowchart LR
    I["Topic / current system"] --> P["Paper evidence"]
    P --> H["Hypothesis + mutation"]
    H --> T["Trainer / executor"]
    T --> V["Validation evaluator"]
    V --> S["Selection + research memory"]
    S --> H
    S --> O["Isolated test + report"]
```

一个领域 adapter 需要声明：

| 接口 | 作用 |
|---|---|
| Research object | 当前模型、Agent policy、训练 recipe 或其他待优化系统 |
| Evidence source | 论文检索范围、可采用的结构和训练方法 |
| Mutation space | 结构、数据、后训练、工具策略及超参数改动 |
| Trainer / executor | 可隔离运行的训练或 episode 执行入口 |
| Validation evaluator | 决定晋级的公平指标，禁止读取最终 test |
| Artifact contract | 配置、父子关系、trace、指标和中文报告 |

## 内置领域状态

| 领域 | 已实现的自动进化 | 可复用论文组件 | 当前状态 |
|---|---|---|---|
| 搜广推与 LLM 应用 | RankMixer、HyFormer；MovieLens 与公共推荐评测 | LONGER、UniMixer、RankMixer 等结构及工业论文 adapter | **可运行** |
| 纯 LLM | micro‑LLM；架构 → 数据配方 → SFT/后训练的分轮搜索 | 纯 LLM 架构、Lightning OPD、GPRL、TCR 等 | **可运行** |
| LLM 后训练 | 论文检索约束的 objective genome；多轮搜索算法、学习率、组大小与训练步数 | PPO/DPO/IPO/SimPO/GRPO/LUSPO/CoBA-RL、OPD、GPRL、TCR | **可运行** |
| Agent | 论文检索约束的组合式 genome；逐轮搜索 memory、planner、tool、critic 与容量 | ReAct、LATS、U-Mem、MetaGPT、CRITIC、Agent Lightning、SWE-agent、OpenHands | **可运行** |

!!! note "Agent 状态"
    Agent evolve 可使用确定性 episode evaluator，也可在 `swebench-local` 创建临时
    仓库并真实编辑/测试。论文检索只映射到已审计算子；无安全映射的论文保持 evidence-only。

## 组合式研究

领域与方法不必一一绑定。例如：

- 在推荐 evolve 中把 LLM 语义特征、生成式召回或后训练目标作为 mutation；
- 在纯 LLM evolve 中同时搜索网络结构、预训练数据配方和后训练算法；
- 在 Agent evolve 中组合记忆策略、规划器、工具上下文和 critic；
- 为新领域实现相同 adapter 合同，而不修改研究循环的选择和报告逻辑。

[查看完整进化协议和运行命令 →](model-evolution.md)
