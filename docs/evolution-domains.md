# 自动进化的领域适配

## 2026-08-29 新增论文算子

- 后训练：`ttpo`、`weak-guide-rlvr`、`uc-mopd`、`spear` 已成为可继承、可组合的
  objective / rollout / reward 候选。
- Agent：`swe-prime`、`harnesslens`、`covemem`、`spt` 已进入 policy、verifier、memory
  和 data/skill 槽位。
- `friend-gnn` 暂不接入 RankMixer genome：好友图 GNN 与当前序列排序槽位不相容；
  在图模型 genome 建立前，强行映射会制造错误的可组合性声明。

这些名字均来自仓库内已经实现并有公开实验产物的论文，不是运行时临时编造的结构。

Auto Research 的核心不是某个推荐模型，而是一套开放的研究协议。任意领域只要提供
研究对象、数据、可搜索改动和评测器，就能复用论文检索、并行实验、选择与多轮迭代。

!!! info "论文检索不等于自动写实现"
    在线检索负责发现证据；可执行 mutation 必须预先在仓库实现并通过测试。控制器只能
    组合白名单算子和参数，不会直接运行从论文文本或模型生成的任意代码。完整例子见
    [候选来源说明](model-evolution.md#candidate-sources)。

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
| 基础模型 | micro‑LLM；架构 → 数据配方 → 效率算子的分轮搜索 | Mamba、Switch Transformer、稀疏注意力、条件记忆、量化与动态计算等 | **可运行** |
| LLM 后训练 | 论文检索约束的 objective genome；多轮搜索算法、学习率、组大小与训练步数 | 当前全部后训练 adapter：PPO/DPO/GRPO、偏好优化、OPSD/OPCD/Lightning OPD、过程奖励与课程 RL | **可运行** |
| Agent | 论文检索约束的组合式 genome；逐轮搜索 memory、planner、tool、critic 与容量 | ReAct/LATS/ART、Voyager/AutoGen/PEARL、LOOP/WebAgent-R1/MUA-RL、Agentic RL/OPD 与软件 Agent | **可运行** |

!!! note "Agent 状态"
    Agent evolve 可使用确定性 episode evaluator，也可在 `swebench-local` 创建临时
    仓库并真实编辑/测试。论文检索只映射到已审计算子；无安全映射的论文保持 evidence-only。

## 已实现论文到 evolve 的系统审计

- **后训练**：`post_training.models.ALGORITHMS` 中的全部算法均有论文 mutation，
  新增 OPSD 与 OPCD 后由测试强制检查集合覆盖，避免独立复现完成但 genome 漏接。
- **Agent**：除公平对照 `long-context` 外，当前所有论文方法均映射为 memory、
  planner、tool 或 critic 算子。本轮补齐此前遗漏的 Voyager、AutoGen、PEARL，并加入
  LOOP、WebAgent-R1、MUA-RL；Search-R1 也从通用 tool fallback 升级为显式算子。
- **推荐与基础模型**：只接入能由当前 evaluator 公平计分的结构。需要专有数据协议、
  serving 延迟目标或 byte-level backend 的方法继续保留为 evidence-only，避免“能列出
  名字”被误报为“已搜索其核心机制”。

## 组合式研究

领域与方法不必一一绑定。例如：

- 在推荐 evolve 中把 LLM 语义特征、生成式召回或后训练目标作为 mutation；
- 在基础模型 evolve 中搜索网络结构、预训练数据配方和效率算子，并可跨域组合后训练算法；
- 在 Agent evolve 中组合记忆策略、规划器、工具上下文和 critic；
- 为新领域实现相同 adapter 合同，而不修改研究循环的选择和报告逻辑。

[查看完整进化协议和运行命令 →](model-evolution.md)
