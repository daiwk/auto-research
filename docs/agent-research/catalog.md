# Agent 研究方法索引

本页按能力方向维护 Agent 论文实现。每个方法都有独立详情页，避免记忆、规划与工具
管理的指标和复现边界混在同一段文字中。

## 已实现论文

| 方向 | 方法 | 论文信息 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| Agentic RL 基础设施 | [Agent-R1](2511.14460-agent-r1/README.md) | Mingyue Cheng，2025-11-18 | [已开源](https://github.com/AgentR1/Agent-R1) | `agent-r1` |
| 通用 Agent 评测 | [GAIA](2311.12983-gaia/README.md) | Grégoire Mialon，2023-11-21 | [官方 benchmark](https://huggingface.co/gaia-benchmark) | `gaia` |
| 工具指令与评测 | [ToolBench](2305.16504-toolbench/README.md) | Qiantong Xu，2023-05-25 | 未发现该论文官方代码 | `toolbench` |
| 多 Agent 协作 | [CAMEL](2303.17760-camel/README.md) | Guohao Li，2023-03-31 | [已开源](https://github.com/camel-ai/camel) | `camel` |
| 策略—工具图共进化 | [SEARL](2604.07791-searl/README.md) | Xinshun Feng，2026-04-09 | 未发现官方代码 | `searl` |
| 技能设计 | [Memento-Skills](2603.18743-memento-skills/README.md) | Huichi Zhou，2026-03-19 | [已开源](https://github.com/Memento-Teams/Memento-Skills) | `memento-skills` |
| 记忆技能 | [MemSkill](2602.02474-memskill/README.md) | Haozhen Zhang，2026-02-02 | [已开源](https://github.com/ViktorAxelsen/MemSkill) | `memskill` |
| 技能库强化学习 | [SAGE](2512.17102-sage/README.md) | Jiongxiao Wang，2025-12-18 | 未发现官方代码 | `sage` |
| 零数据多 Agent | [Agent0](2511.16043-agent0/README.md) | Peng Xia，2025-11-20 | 未发现官方代码 | `agent0` |
| 工具强化学习 | [ToolRL](2504.13958-toolrl/README.md) | Cheng Qian，2025-04-16 | 未发现官方代码 | `toolrl` |
| 推理中工具调用 | [ReTool](2504.11536-retool/README.md) | Jiazhan Feng，2025-04-15 | 未发现官方代码 | `retool` |
| 深度研究 RL | [DeepResearcher](2504.03160-deepresearcher/README.md) | Yuxiang Zheng，2025-04-04 | [已开源](https://github.com/GAIR-NLP/DeepResearcher) | `deepresearcher` |
| 递归 turn 信用 | [AgentOPSD](2608.05987-agent-opsd/README.md) | Zi-Han Wang 等，2026-08-06 | [仓库公开、完整代码待发布](https://github.com/ZethWang/AgentOPSD) | `agent-opsd` |
| 观测校准蒸馏 | [OCSD](2608.04788-ocsd/README.md) | Yi Yang 等，2026-08-05 | [已开源](https://github.com/yiy1x/OCSD) | `ocsd` |
| 可验证统一记忆 | [VerMem](2608.03137-vermem/README.md) | Sun Yat-sen University，2026-08-04 | [已开源](https://github.com/Sun-SYSU-24/VerMem) | `vermem` |
| 检索—记忆共进化 | [CoEvo-Mem](2608.01739-coevo-mem/README.md) | Bowen Ye 等，2026-08-03 | 未发现官方代码 | `coevo-mem` |
| 环境 rehearsal / Agent RL | [EnvACE](2608.06197-envace/README.md) | SJTU 等 / Tencent，2026-08-06 | [已开源](https://github.com/Within-yao/EnvACE) | `envace` |
| 工具学习 | [Toolformer](2302.04761-toolformer/README.md) | Meta AI / UPF，2023-02-09 | 未发布官方代码 | `toolformer` |
| 自我迭代 | [Self-Refine](2303.17651-self-refine/README.md) | CMU / AI2 / UW / NVIDIA / UCSD / Google，2023-03-30 | [已开源](https://github.com/madaan/self-refine) | `self-refine` |
| 解耦规划 | [ReWOO](2305.18323-rewoo/README.md) | Microsoft / NCSU / Texas A&M，2023-05-29 | [已开源](https://github.com/billxbf/ReWOO) | `rewoo` |
| 多 Agent | [AutoGen](2308.08155-autogen/README.md) | Microsoft Research，2023-08-16 | [已开源](https://github.com/microsoft/autogen) | `autogen` |
| 规划强化学习 | [PEARL](2601.20439-pearl/README.md) | 中科院信工所 / 中国科学院大学，2026-01-28 | 未发现 | `pearl` |
| 成本感知工具停止 | [CAM-DF](2607.27083-cam-df/README.md) | Peking / McGill / SUFE / Tsinghua，2026-07-29 | 论文称发布 artifacts，但未找到仓库链接 | `cam-df` |
| 跨任务技能进化 | [SkillRise](2607.26784-skillrise/README.md) | Zhejiang / NUS / SJTU / Meituan，2026-07-29 | [已开源](https://github.com/Within-yao/SkillRise) | `skillrise` |
| 推理搜索 | [Tree of Thoughts](2305.10601-tree-of-thoughts/README.md) | Princeton / Google DeepMind，2023-05-17 | [已开源](https://github.com/princeton-nlp/tree-of-thought-llm) | `tree-of-thoughts` |
| Agent 搜索 | [LATS](2310.04406-lats/README.md) | UIUC，2023-10-06 | [已开源](https://github.com/lapisrocks/LanguageAgentTreeSearch) | `lats` |
| 推理与行动 | [ReAct](2210.03629-react/README.md) | Princeton / Google Research，2022-10-06 | [已开源](https://github.com/ysymyth/ReAct) | `react` |
| 自我反思 | [Reflexion](2303.11366-reflexion/README.md) | Northeastern / MIT / Princeton，2023-03-20 | [已开源](https://github.com/noahshinn/reflexion) | `reflexion` |
| 终身学习 | [Voyager](2305.16291-voyager/README.md) | NVIDIA / Caltech / UT Austin / Stanford / ASU，2023-05-25 | [已开源](https://github.com/MineDojo/Voyager) | `voyager` |
| 主动记忆 | [U-Mem](2602.22406-u-mem/README.md) | National University of Singapore，2026-02-25 | [匿名仓库](https://anonymous.4open.science/r/code-release-456D/) | `u-mem` |
| 过程记忆 | [LEGOMem](2510.04851-legomem/README.md) | Microsoft Research，2025-10-06 | 未发现 | `legomem` |
| 工具记忆 | [MemTool](2507.21428-memtool/README.md) | PwC CTIO，2025-07-29 | 未发现 | `memtool` |
| 多 Agent 软件工程 | [MetaGPT](2308.00352-metagpt/README.md) | DeepWisdom / Xiamen / KAUST，2023-08-01 | [已开源](https://github.com/FoundationAgents/MetaGPT) | `metagpt` |
| 工具反馈 | [CRITIC](2305.11738-critic/README.md) | Microsoft / Tsinghua，2023-05-19 | [已开源](https://github.com/microsoft/ProphetNet/tree/master/CRITIC) | `critic` |
| Agent RL | [Agent Lightning](2508.03680-agent-lightning/README.md) | Microsoft Research，2025-08-05 | [已开源](https://github.com/microsoft/agent-lightning) | `agent-lightning` |
| Agent group credit | [GiGPO](2505.10978-gigpo/README.md) | 论文作者团队，2025-05-16 | 未发现官方代码 | `gigpo` |
| Step-aligned Agent RL | [StepPO](2604.18401-steppo/README.md) | 中国科学技术大学作者团队，2026-04-20 | 未发现官方代码 | `steppo` |
| Agent RL | [TAPO](2607.27973-tapo/README.md) | Peking University / Pengcheng Laboratory，2026-07-30 | 未发现官方代码 | `tapo` |
| Agent group credit | [Group-Reflective Self-Distillation](2607.28076-grsd/README.md) | Baidu Inc. / collaborating universities，2026-07-30 | [已开源](https://github.com/BinbZheng1/GRSD) | `grsd` |
| CUA Reward 评测 | [OSReward / OS-Shepherd](2607.28609-osreward/README.md) | HKU / Nanjing / NUS / USTC / Xi’an Jiaotong / Oxford / Fudan，2026-07-30 | [项目主页](https://os-copilot.github.io/OSReward-Home/) | `os-shepherd` |
| 搜索 Agent RL | [Search-R1](2503.09516-search-r1/README.md) | UIUC / UMass Amherst / Google Cloud AI Research，2025-03-12 | [已开源](https://github.com/PeterGriffinJin/Search-R1) | `search-r1` |
| 多轮 Agent RL | [RAGEN](2504.20073-ragen/README.md) | Northwestern / Stanford / Microsoft / UW / NYU / UBC / SMU，2025-04-24 | [已开源](https://github.com/RAGEN-AI/RAGEN) | `ragen` |
| 长时程 Agent RL | [LOOP](2502.01600-loop/README.md) | Apple，2025-02-03 | [已开源](https://github.com/apple/ml-loop) | `loop` |
| 网页 Agent RL | [WebAgent-R1](2505.16421-webagent-r1/README.md) | University of Virginia / Amazon / Georgia Tech，2025-05-22 | [已开源](https://github.com/weizhepei/WebAgent-R1) | `webagent-r1` |
| 多轮用户 Agent RL | [MUA-RL](2508.18669-mua-rl/README.md) | Meituan / CAS / Peking University，2025-08-26 | [已开源](https://github.com/zzwkk/MUA-RL) | `mua-rl` |
| 软件工程 ACI | [SWE-agent](2405.15793-swe-agent/README.md) | Princeton，2024-05-06 | [已开源](https://github.com/SWE-agent/SWE-agent) | `swe-agent` |
| 通用软件 Agent | [OpenHands](2407.16741-openhands/README.md) | All-Hands-AI / CMU 等，2024-07-23 | [已开源](https://github.com/All-Hands-AI/OpenHands) | `openhands` |
| 神经符号路由 | [MRKL](2205.00445-mrkl/README.md) | AI21 Labs 等，2022-05-01 | 未发布完整实现 | `mrkl` |
| 专家模型编排 | [HuggingGPT](2303.17580-hugginggpt/README.md) | Zhejiang / Microsoft Research Asia，2023-03-30 | [已开源](https://github.com/microsoft/JARVIS) | `hugginggpt` |
| 记忆与反思 | [Generative Agents](2304.03442-generative-agents/README.md) | Stanford / Google Research，2023-04-07 | [已开源](https://github.com/joonspk-research/generative_agents) | `generative-agents` |
| 虚拟上下文 | [MemGPT](2310.08560-memgpt/README.md) | UC Berkeley，2023-10-12 | [已开源](https://github.com/letta-ai/letta) | `memgpt` |
| 浏览问答 | [WebGPT](2112.09332-webgpt/README.md) | OpenAI，2021-12-17 | 未发布完整训练代码；公开 comparisons 数据 | `webgpt` |
| 具身规划 | [SayCan](2204.01691-saycan/README.md) | Google Robotics / Everyday Robots，2022-04-04 | [模拟实现](https://github.com/google-research/google-research/tree/master/saycan) | `saycan` |
| 程序推理 | [PAL](2211.10435-pal/README.md) | CMU / Inspired Cognition，2022-11-18 | [已开源](https://github.com/reasoning-machines/pal) | `pal` |
| 自动工具推理 | [ART](2303.09014-art/README.md) | UW / UCI / Meta AI，2023-03-16 | [已开源](https://github.com/bhargaviparanjape/language-programmes) | `art` |
| Agentic RL / hindsight skill | [SEED](2607.14777-seed/README.md) | Tsinghua / Zhejiang / CUHK / NTU / Tongji，2026-07-16 | [已开源](https://github.com/jinyangwu/SEED) | `seed` |
| Agentic RL / turn-level credit | [CAST](2607.25308-cast/README.md) | USTC / Nanjing University / Wuhan University，2026-07-28 | [已开源](https://github.com/Wloner0809/CAST) | `cast` |
| Agentic OPD / rollout budgeting | [TurnOPD](2607.05804-turn-opd/README.md) | Academic author team，2026-07-07 | 未发现 | `turn-opd` |
| Hierarchical skill memory | [HiSkill](2607.25853-hiskill/README.md) | BUPT，2026-07-28 | [已开源](https://github.com/BUPT-GAMMA/HiSkill) | `hiskill` |
| Continual agent memory | [UniMem](2607.26017-unimem/README.md) | CASIA / UCAS / Peking University / UCL，2026-07-28 | 未发现 | `unimem` |

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
