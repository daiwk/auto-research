# PROBE：工具 Agent 策略审计与确定性重算

> `component_only` / L1 CPU 机制诊断。只实现惰性 trace/verifier/reward 接口和四个独立规则示例；没有训练审计模型，也没有接入完整 SkyAssist 或真实目标服务。

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [PROBE](https://arxiv.org/abs/2610.22124) |
| 公司/机构 | Kshitij Mishra、Abhijith Sharma 共同一作；Mohamed bin Zayed University of Artificial Intelligence |
| 首次公开日期 | 2026-10-15，arXiv v1 16:01:38 UTC；10-16 公告补审 |
| 原文开源代码 | [作者实现](https://github.com/Mishrakshitij/PROBE)公开可读；本轮未确认复用许可证，本地按论文独立实现 |
| 本地 Adapter | 无（`adapter: null`）；组件 key：`probe` |
| 本地复现代码 | `src/auto_research/agent_research/probe_audit.py`；`scripts/run_oct17_supplement_agent.py` |

## 原始论文总结

### 背景与主要改动

任务完成并不等于按业务/隐私政策完成；只测试最终状态或有害文本也可能漏掉多轮工具调用中的违规。PROBE 训练扮演正常客户的 auditor，与冻结 target 交互，私有 verifier 从完整 trace 判断违规；奖励综合违规、可信客户行为、工具流程进展和策略多样性，比较 GRPO、DPO 和 GFlowNet。

```mermaid
flowchart LR
    P[公共客户场景] --> A[auditor消息]
    A --> T[target与私有policy / database]
    T --> H[公共对话]
    H --> A
    T --> X[私有工具trace]
    H --> V[私有verifier]
    X --> V
    V --> R[违规 / 重复命中 / 覆盖统计]
    J[训练judge命中] --> D[独立确定性重算]
    H --> D
```

<!-- paper-figure:start -->
### 原论文关键图

[![PROBE：工具 Agent 策略审计与确定性重算 原论文 Figure 1](assets/paper-figure-01.png)](https://arxiv.org/pdf/2610.22124#page=2)

> **原论文 Figure 1（关键图）**：展示原论文方法的总体设计和关键组成。图片来自[原论文](https://arxiv.org/abs/2610.22124)，版权归原作者所有；点击图片可查看来源。
<!-- paper-figure:end -->

### 核心公式

[原文 §4、附录 D–F](https://arxiv.org/html/2610.22124v1)的 V3 违规项按策略严重度和本 episode 已有命中次数去重：

$$
r_{viol}(t)=\sum_{i\in hits_t}\sigma_i d(n_i),\qquad
d(n)=\begin{cases}1&n=0\\1/2&n=1\\0&n\ge2.\end{cases}
$$

本地只实现这一明确子项；没有冒充完整 composite reward、审计 RL 或语义 judge。Coverage 的分母是声明的策略全集；`violation_yield_per_100_episodes` 按原始 verifier 命中总数计数，保留同一 policy 跨 turn 的重复命中，可能大于 100，不是成功概率。去重 episode–policy 命中另列 `distinct_episode_policy_yield_per_100_episodes`，不能混作原始 yield。无命中 episode 和暂不支持的策略保留在分母中。

### 论文离线与线上效果

原文 SkyAssist 有 20 策略，16 个程序 predicate、4 个训练时混合语义 judge；另有 unseen target 和 τ-bench 迁移。**附录 E/F 的人工核验发现 S5 judge precision 为 0；改用全确定性重算，最佳 coverage 从 60% 降到 55%**，不能把前者当作已核实能力。原文报告多轮 auditor 比静态/零样本测试发现更多策略，但这是作者实验，不是本地结果。未报告生产线上 A/B。

## 本地复现

```bash
PYTHONPATH=src python scripts/run_oct17_supplement_agent.py \
  --methods probe --device cpu --seeds 42,43,44 \
  --output runs/oct17-supplement-agent/probe.json
```

### 数据协议与本轮 CPU 结果

每 seed 构造 12 条惰性 trace，随机化重复轮数，不执行任何工具。四个示例核验 required fields、当前 mutation intent 的确认、限制目的地及人数；它们不是原文完整 20 策略套件。第五个明确 unsupported 的语义策略留在 coverage 分母。结果为 4/5 coverage=0.8、8/12 episode 有命中，4 条无命中没有删除；这些值只是构造 fixture，不说明目标 Agent 的安全性。

首/重复命中奖励与独立手算误差为 0；实际执行 3 轮 auditor/target callbacks，私有评分 marker 暴露次数为 0，训练 auditor 数量为 0。所有值、逐 seed 与来源 hash 见 [CPU 产物](metrics/component-cpu-seeds42-44.json)。

### 代码映射、成本与边界

`deterministic_rescore` 不读取 judge 命中输入；`violation_reward` 维护每 policy 的命中次数；`audit_metrics` 保留 unsupported policies 和全部 episodes。`audit_episode` 只把公共场景/消息传给 auditor，target 的政策可由其私有闭包持有，完整 trace 最后才送独立评分器。可信 callback 是进程内数据隔离合同，不是恶意代码安全沙箱。

未实现原文 4B QLoRA auditor、30B target、GRPO/DPO/GFlowNet 多臂训练、语义审计 judge 或 τ-bench 能力实验。原文每运行需两张 A100-40GB，另有约 300 步和长多轮 target 调用；**成本过高，不复现（审查 DONE）**。不把规则 predicate 冒充学习式 auditor，不进入 Evolve 能力晋级。
