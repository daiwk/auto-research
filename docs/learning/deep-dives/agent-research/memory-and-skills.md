---
hide:
  - toc
---

<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->

# 经验进入长期系统前，要解决存取、价值与准入

[Agent](../index.md) · 更新 2026-10-27 · 55 篇主题资料 / 6 篇重点对照

MemGPT 管信息放在哪里，MemPrice 管有限窗口里保留何种精度，CMP 管效用如何识别；Voyager 把成功程序变技能，VaG 管技能进入库的风险，SkillRise 用后续任务检验整理价值。存得下、相关、合法和能帮助未来，是四个不同问题。

[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · [更新记录](#updates) · [本主题逐篇问答](../../paths/agent-research/memory-and-skills.md)

!!! note "怎么读这张卡片"

    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。

## 机制对照 {#comparison}

比较维度：对象是原始事件、压缩表示、运行状态还是可执行技能 · 决定发生在写入、读取、淘汰还是持久准入 · 价值来自相似度、当前成功、随机曝光还是下游任务 · 原始细节和错误后代是否可以恢复或撤销

<div class="ar-deep-comparison" markdown="1">

| 论文与来源 | 机制定位 | 得到了什么，付出什么 |
| --- | --- | --- |
| [MemGPT](../../../agent-research/2310.08560-memgpt/README.md) · [原始来源](https://arxiv.org/abs/2310.08560)<br>章节：背景与主要改动、核心公式、复现边界 | 分层管理核心信息、当前上下文和外部归档，以模型函数调用和 heartbeat 控制换入换出。 | 外部容量不等于当前可见，检索仍可能漏证据；本地使用确定性 key 与代理成本，不是语义检索服务。 |
| [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](../../../agent-research/2610.24955-memprice/README.md) · [原始来源](https://arxiv.org/abs/2610.24955)<br>章节：背景与主要改动、核心公式、本地复现与边界 | 每项记忆选 raw/summary/abstraction/keywords/delete 中一版，以背包满足硬预算，队列价格反映长期占用。 | 联合分配依赖效用和token大小输入，窗口已删细节只能经归档刷新恢复；本地只执行DP与状态合同。 |
| [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](../../../agent-research/2610.02070-causal-memory-policy/README.md) · [原始来源](https://arxiv.org/abs/2610.02070)<br>章节：背景与主要改动、核心公式、复现边界 | 在固定候选池预留均衡随机曝光，估计设计下处理/对照净效应及标准误，不确定时保护记忆。 | 处理一条会改变其他槽位分布，效应不能当独立加性系数；本地合成结果不证明真实问答或长期删除策略。 |
| [Voyager](../../../agent-research/2305.16291-voyager/README.md) · [原始来源](https://arxiv.org/abs/2305.16291)<br>章节：背景与主要改动、核心公式、复现边界 | 自动课程产生任务，代码执行和反馈修订后，将验证成功程序作为可检索技能继续组合。 | 一次环境成功仍有适用前提；本地技能是结构化工具计划，没有 Mineflayer/GPT-4 或真实 Minecraft。 |
| [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](../../../agent-research/2608.05810-vag/README.md) · [原始来源](https://arxiv.org/abs/2608.05810)<br>章节：背景与主要改动、核心公式、复现边界 | 在持久写入前检查结构、行为无害与语义一致，再按边际收益选择可兼容 Hot 技能集合。 | 阻止污染早于事后删除，但验证仍受覆盖限制；本地只执行相关核心算子，候选发现不等于完整能力进化。 |
| [SkillRise](../../../agent-research/2607.26784-skillrise/README.md) · [原始来源](https://arxiv.org/abs/2607.26784)<br>章节：背景与主要改动、核心公式、复现边界 | 同一policy交替求解与整理文档，当前结果监督solve，下游折扣结果监督curate。 | 要求任务序列能暴露经验迁移价值；本地仅验证状态和phase信用，未做原文模型RL。 |

</div>

## 取舍分析 {#analysis}

### 资源分配器需要效用，但不会自动产生因果证据

MemGPT 使信息可被移到归档，MemPrice 再在当前窗口联合分配多级表示；两者都需要决定什么值得留下。CMP 处理的是另一层：难题更常检索某条记忆，不能把相关失败都归咎于它，随机曝光才提供可识别的对照。将 CMP 的估计交给分配器也须保留曝光设计和不确定度，不能把固定槽位净效应直接当可随意相加的单项价值。

对照来源：[memgpt](../../../agent-research/2310.08560-memgpt/README.md) · [memprice](../../../agent-research/2610.24955-memprice/README.md) · [causal-memory-policy](../../../agent-research/2610.02070-causal-memory-policy/README.md)

### 当前成功、持久准入与未来受益是三个时点

Voyager 让成功程序进入技能积累链，VaG 更强调新经验会影响后代，需在写入前检查并考虑共同使用的兼容性。SkillRise 又把整理行为交给下游任务结果评价：当前成功主要说明求解，不足以说明留下的文档帮助未来。这不是谁更先进的直线序列，而是不同证据合同：执行通过、库准入和跨任务学习应分别记录。

对照来源：[voyager](../../../agent-research/2305.16291-voyager/README.md) · [vag](../../../agent-research/2608.05810-vag/README.md) · [skillrise](../../../agent-research/2607.26784-skillrise/README.md)

## 跨论文问答 {#questions}

先想自己的答案，再展开；每个问题至少联系两篇论文。

### MemPrice 背包选中一条“高效用”记忆，为什么 CMP 仍会追问这个效用是怎样测出来的？ {#cross-allocation-versus-identification}

??? note "展开答案与例子"

    **答案：** 背包只在给定效用与大小下求联合分配，不证明上游估计可靠。如果记忆常在难题出现，观察到失败多可能只是选择偏差；CMP 用均衡随机曝光和对照估计设计下净作用，并保留标准误。这个净效应又受槽位替代影响，不能不加条件当成独立可加背包收益。

    **教学例子：** 教学例：故障排查记忆总在最难事故被检索，成功率低不说明它有害；先辨别没有它时会怎样，再讨论是否值得占窗口。

    对照来源：[memprice](../../../agent-research/2610.24955-memprice/README.md) · [causal-memory-policy](../../../agent-research/2610.02070-causal-memory-policy/README.md)

### Voyager 一次执行成功的程序，为什么不能不经检查就当成 VaG 里可与所有技能共同使用的长期经验？ {#cross-successful-skill-versus-admission}

??? note "展开答案与例子"

    **答案：** 一次成功支持该环境中的执行路径，未说明程序在其他前提仍无害，也未排除与已有技能冲突。VaG 在写入前分开检查结构、行为和语义，再以集合边际价值选择兼容组合。两种机制可以讨论不同生命周期，但不能把成功、无害和组合收益合并成一张通过票。

    **教学例子：** 教学例：技能在空目录中成功，若暗含删除旧文件的前提，搬到共享目录可能有害；单次成功没有验证这个新作用域。

    对照来源：[voyager](../../../agent-research/2305.16291-voyager/README.md) · [vag](../../../agent-research/2608.05810-vag/README.md)

### 为什么 SkillRise 的整理文档不能直接沿用 Voyager 式当前任务成功信号？ {#cross-current-outcome-versus-future-skill}

??? note "展开答案与例子"

    **答案：** 当前成功主要说明刚才的动作完成目标，文档价值却体现在后续相关任务能否借它行动。SkillRise 将solve与curate分phase，用下游折扣回报监督后者，并只作用于对应生成token。Voyager 的成功程序准入提供执行证据，不能替代这项跨任务信用；漂亮但无用的总结也不应因当前成功自动获奖。

    **教学例子：** 教学例：当前任务靠偶然试错成功，文档若只写具体答案，下一题无法复用；下游评价才会暴露它没有留下可迁移步骤。

    对照来源：[skillrise](../../../agent-research/2607.26784-skillrise/README.md) · [voyager](../../../agent-research/2305.16291-voyager/README.md)

## 更新记录 {#updates}

新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。

**2026-10-27** · 首版：比较分层存储、记忆价格、随机曝光效用、成功程序积累、预提交准入与下游技能信用。

覆盖 55 篇主题资料；目录见下。

<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 55 篇资料</summary>

目录归类覆盖本主题全部资料；重点对照范围以上表为准。

- [Cache Engineering for Agents](../../../agent-research/2610.28577-cache-engineering/README.md)
- [Remembering Has a Price: Learning Memory Worth under Resource Constraints](../../../agent-research/2610.26453-tokenworth/README.md)
- [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](../../../agent-research/2610.24955-memprice/README.md)
- [MemoProAgent: Toward Memory-Driven Proactive Assistance](../../../agent-research/2610.22671-proper-agent/README.md)
- [MemScope: Evolving Agent Memory Architectures through Localized Code Repair](../../../agent-research/2610.21170-memscope/README.md)
- [Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing](../../../agent-research/2610.22196-hy-memory/README.md)
- [Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents](../../../agent-research/2610.20116-transparent-compact/README.md)
- [Recursive Formation and First-Class Reuse of Compositional Capabilities](../../../agent-research/2610.19414-formcraft/README.md)
- [Test-Time Memory Construction](../../../reproductions/2610.13348-t2mem/README.md)
- [NEAR: Neighborhood-Aware Residuals for Memory Retrieval](../../../reproductions/2610.13314-near/README.md)
- [Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence](../../../reproductions/2610.13277-beyond-final-embedding/README.md)
- [Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents](../../../agent-research/2610.12124-hippocam/README.md)
- [Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents](../../../agent-research/2610.02002-mem-plus-plus/README.md)
- [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](../../../agent-research/2610.02070-causal-memory-policy/README.md)
- [Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States](../../../agent-research/2610.01415-belief-state-pos/README.md)
- [AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents](../../../agent-research/2610.02163-autocompact/README.md)
- [MemFit: Efficient Long-Term Agentic Memory](../../../agent-research/2610.00872-memfit/README.md)
- [UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval](../../../agent-research/2609.36805-upliftmem/README.md)
- [ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents](../../../agent-research/2609.37311-remem/README.md)
- [Context Language Models](../../../agent-research/2609.37725-context-lm/README.md)
- [Mnemon: Raw Records, Fast Judgments, Slow Thoughts](../../../agent-research/2609.36059-mnemon/README.md)
- [Continuous Context Management](../../../agent-research/2609.35540-ccm/README.md)
- [Interactive Memory Learning for Long-Term Conversations](../../../agent-research/2609.17088-interactive-memory/README.md)
- [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](../../../agent-research/2609.17653-evoskill-gui/README.md)
- [When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents](../../../agent-research/2609.10750-skill-retention/README.md)
- [Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents](../../../agent-research/2609.11060-grounded-memory/README.md)
- [MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging](../../../agent-research/2609.08273-memforest/README.md)
- [CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution](../../../agent-research/2609.04865-coskill/README.md)
- [AtomRec: Evolving Atomic Memory for Agentic Recommendation](../../../agent-research/2609.04882-atomrec/README.md)
- [Imagine Before Acting: Prospective Skill Identification for LLM Agents](../../../reproductions/2609.01642-skilldreamer/README.md)
- [SPT: Skills as Pre-Training Data for Agentic Language Models](../../../agent-research/2608.26563-spt/README.md)
- [When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems](../../../agent-research/2608.26895-covemem/README.md)
- [SKILL.state: Scalable Long-Horizon Agent Skills](../../../agent-research/2608.26263-skill-state/README.md)
- [CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval](../../../agent-research/2608.25500-caskg/README.md)
- [SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents](../../../agent-research/2608.24747-skillforge/README.md)
- [HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation](../../../agent-research/2608.15703-hymem/README.md)
- [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](../../../agent-research/2608.05810-vag/README.md)
- [Learning Globally Reusable Skills for Coding Agents](../../../agent-research/2608.06153-gse/README.md)
- [MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off](../../../agent-research/2608.04843-memorycpt/README.md)
- [VerMem](../../../agent-research/2608.03137-vermem/README.md)
- [CoEvo-Mem](../../../agent-research/2608.01739-coevo-mem/README.md)
- [SkillRise](../../../agent-research/2607.26784-skillrise/README.md)
- [UniMem](../../../agent-research/2607.26017-unimem/README.md)
- [HiSkill](../../../agent-research/2607.25853-hiskill/README.md)
- [Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents](../../../agent-research/2607.13591-memcon/README.md)
- [Memento-Skills](../../../agent-research/2603.18743-memento-skills/README.md)
- [U-Mem](../../../agent-research/2602.22406-u-mem/README.md)
- [Learning Personalized Agents from Human Feedback](../../../agent-research/2602.16173-pahf/README.md)
- [MemSkill](../../../agent-research/2602.02474-memskill/README.md)
- [SAGE](../../../agent-research/2512.17102-sage/README.md)
- [LEGOMem](../../../agent-research/2510.04851-legomem/README.md)
- [MemTool](../../../agent-research/2507.21428-memtool/README.md)
- [MemGPT](../../../agent-research/2310.08560-memgpt/README.md)
- [Voyager](../../../agent-research/2305.16291-voyager/README.md)
- [Generative Agents](../../../agent-research/2304.03442-generative-agents/README.md)

</details>

[进入本主题逐篇四层问答](../../paths/agent-research/memory-and-skills.md) · [返回全部精读卡片](../index.md)
