# Agent 研究方法索引

本页按能力方向维护 Agent 论文实现。每个方法都有独立详情页，避免记忆、规划与工具
管理的指标和复现边界混在同一段文字中。

## 已实现论文

| 方向 | 方法 | 论文信息 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| 工具学习 | [Toolformer](2302.04761-toolformer/README.md) | Meta AI / UPF，2023-02-09 | 未发布官方代码 | `toolformer` |
| 自我迭代 | [Self-Refine](2303.17651-self-refine/README.md) | CMU / AI2 / UW / NVIDIA / UCSD / Google，2023-03-30 | [已开源](https://github.com/madaan/self-refine) | `self-refine` |
| 解耦规划 | [ReWOO](2305.18323-rewoo/README.md) | Microsoft / NCSU / Texas A&M，2023-05-29 | [已开源](https://github.com/billxbf/ReWOO) | `rewoo` |
| 多 Agent | [AutoGen](2308.08155-autogen/README.md) | Microsoft Research，2023-08-16 | [已开源](https://github.com/microsoft/autogen) | `autogen` |
| 规划强化学习 | [PEARL](2601.20439-pearl/README.md) | 中科院信工所 / 中国科学院大学，2026-01-28 | 未发现 | `pearl` |
| 推理搜索 | [Tree of Thoughts](2305.10601-tree-of-thoughts/README.md) | Princeton / Google DeepMind，2023-05-17 | [已开源](https://github.com/princeton-nlp/tree-of-thought-llm) | `tree-of-thoughts` |
| Agent 搜索 | [LATS](2310.04406-lats/README.md) | UIUC，2023-10-06 | [已开源](https://github.com/lapisrocks/LanguageAgentTreeSearch) | `lats` |
| 推理与行动 | [ReAct](2210.03629-react/README.md) | Princeton / Google Research，2022-10-06 | [已开源](https://github.com/ysymyth/ReAct) | `react` |
| 自我反思 | [Reflexion](2303.11366-reflexion/README.md) | Northeastern / MIT / Princeton，2023-03-20 | [已开源](https://github.com/noahshinn/reflexion) | `reflexion` |
| 终身学习 | [Voyager](2305.16291-voyager/README.md) | NVIDIA / Caltech / UT Austin / Stanford / ASU，2023-05-25 | [已开源](https://github.com/MineDojo/Voyager) | `voyager` |
| 主动记忆 | [U-Mem](2602.22406-u-mem/README.md) | National University of Singapore，2026-02-25 | [匿名仓库](https://anonymous.4open.science/r/code-release-456D/) | `u-mem` |
| 过程记忆 | [LEGOMem](2510.04851-legomem/README.md) | Microsoft Research，2025-10-06 | 未发现 | `legomem` |
| 工具记忆 | [MemTool](2507.21428-memtool/README.md) | PwC CTIO，2025-07-29 | 未发现 | `memtool` |

## 公平基线

`long-context` 保留全部历史和工具描述，不做记忆压缩。它在 mini-suite 上可以保持较高
成功率，但上下文成本随 episode 数量线性增长，因此同时报告成功率和成本，不能只比较
单一 success 指标。

## 后续方向

系统谱系、明确的 P1 与暂缓原因见[论文谱系与缺口](lineage.md)。后续论文按
“长期记忆、规划与反思、工具学习、多 Agent 协作、环境模型、自我进化”
归档。一个方法只有在以下内容齐全时才标记为“已实现”：

1. 核心状态更新和决策过程已落到代码；
2. 至少一个确定性 mini-suite 或公开 benchmark 可运行；
3. 与公平基线同时报告成功率、成本和方法特有诊断；
4. 保存逐 episode trace，能够解释复用、升级或淘汰；
5. 有独立论文页、固定命令和明确的保真边界。
