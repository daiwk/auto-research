# Agent 研究论文与资料索引

本页由统一论文规格生成的 `docs/research-manifest.json` 构建；元数据维护入口是
打包的 `paper.yaml` 和按领域保存的 catalog 规格，不直接编辑生成产物。
背景、架构、公式、原文效果和本地实验请进入独立详情页。

## 论文实现与研究资料

<div class="ar-method-index" markdown>

| 方向 | 方法 | 一作机构与日期 | 原作者代码 | 本地入口 |
|---|---|---|---|---|
| Agent 训练与策略优化 | [Asymmetric On-Policy Distillation Learns In-Context Exploration](2610.30105-asteroid/README.md) | University of Washington，2026-10-21 | [原作者入口](https://github.com/WEIRDLabUW/asteroid)；原作者源码可见；固定95eee5ee66488af3aaa0aa55a09ae163b1ca3778未找到LICENSE/COPYING，未确认开放许可。本地根据论文独立实现，不复制作者源码 | `asteroid`：仅低成本组件，完整实验不复现 |
| 公开评测协议 | [PLE: Physical-Engineering's Last Exam](2610.30537-physical-engineering-exam/README.md) | Google Cloud AI Research，2026-10-21 | [原作者入口](https://github.com/google-research/ple)；官方代码已公开；固定70ed96281d87380926a0d7c08e21799fd5edee63为10月23日最终29dev/56hidden协议发布。仅离线配置/产物/外部评分协议，不执行作者runner、容器或模型。 | `physical-engineering-exam`：仅低成本组件，完整实验不复现 |
| Agent运行时 | [Cache Engineering for Agents](2610.28577-cache-engineering/README.md) | Tsinghua University，2026-10-20 | [原作者入口](https://github.com/thu-nics/AKV)；作者正文链接的官方AKV实现已核验；本轮不安装或运行完整serving系统。 | 计划键 `cache-engineering`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 自我进化 | [Evolving Agent Interfaces](2610.28601-agent-s4/README.md) | University of California, Santa Barbara，2026-10-20 | [原作者入口](https://github.com/simular-ai/Agent-S/tree/58187e364e3024076540892f5f69d1efc218b74f/agent_s4)；官方开源，Apache-2.0；固定核对58187e364e3024076540892f5f69d1efc218b74f，主要对照tournament.py、scoring.py及operators/。 | `agent-s4`：仅低成本组件，完整实验不复现 |
| 自我进化 | [Object-Oriented Harness: Evolving Agent Harnesses through Object-Oriented Design](2610.28380-oo-harness/README.md) | University of Illinois Urbana-Champaign，2026-10-20 | 未发现官方代码 | `oo-harness`：仅低成本组件，完整实验不复现 |
| 记忆与长期交互 | [Remembering Has a Price: Learning Memory Worth under Resource Constraints](2610.26453-tokenworth/README.md) | Nanjing University，2026-10-19 | [原作者入口](https://github.com/AIGNLAI/TokenWorth)；官方仓库已有tokenworth_core及三类环境实现；未据此声称本地执行了官方Agent评测 | `tokenworth`：仅低成本组件，完整实验不复现 |
| 记忆与长期交互 | [MemPrice: Online Memory Allocation via Adaptive Pricing for Long-Horizon Agents](2610.24955-memprice/README.md) | Hong Kong University of Science and Technology，2026-10-18 | [原作者入口](https://anonymous.4open.science/r/ICLR2027-MemPrice)；论文提供匿名开源地址，但2026-10-20无法访问核验内容；不声称已核实完整官方实现 | `memprice`：仅低成本组件，完整实验不复现 |
| 科学研究与实验闭环 | [Aptamers as a sandbox for lab-in-the-loop agentic molecular discovery](2610.24806-aptamer-lab-loop/README.md) | Google Research，2026-10-17 | 未发现官方代码 | 计划键 `aptamer-lab-loop`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 检索与工具 | [Learning to Program Retrievals: Composing Search Primitives via Reinforcement Learning](2610.24854-rpl/README.md) | KAIST AI / Meta Superintelligence Labs，2026-10-17 | 未发现官方代码 | `rpl`：仅低成本组件，完整实验不复现 |
| 规划、推理与工具使用 | [SCOPE: Selective Certification of Program Edits for Embodied Heuristic Learning](2610.23128-scope-replay/README.md) | Peking University，2026-10-16 | [原作者入口](https://github.com/VDIGPKU/SCOPE)；官方仓库已有scope源码、脚本与Apache-2.0许可；单任务示例不等于全部论文实验可一键复现 | `scope-replay`：仅低成本组件，完整实验不复现 |
| 多Agent协作 | [World of SWECraft: Agent Collaboration at Scale via Simulated Software Worlds](2610.24061-world-of-swecraft/README.md) | Massachusetts Institute of Technology，2026-10-16 | 未发现官方代码 | 计划键 `world-of-swecraft`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 多 Agent 协作 | [A team of Gemini 4 Argon agents beats Minecraft](2610.22319-gemini-minecraft/README.md) | Google DeepMind，2026-10-15 | 未发现官方代码 | 计划键 `gemini-minecraft`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 公共评测与协议 | [AgentPerturb: Evaluating LLM Agent Robustness under Controlled Interaction Perturbations](2610.21624-agent-perturb/README.md) | The Hong Kong University of Science and Technology (Guangzhou)，2026-10-15 | [原作者入口](https://github.com/xuyj233/AgentPerturb)；论文提供官方地址，但2026-10-19核对该仓库仍为空；方法代码与数据尚未发布 | `agent-perturb`：CPU 评测接口，不执行模型 |
| 递归自改进 | [Athanor: An Agent-Native System for Autonomous Post-Training Research](2610.21055-athanor/README.md) | ByteDance / Duke University，2026-10-15 | 未发现官方代码 | 计划键 `athanor`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 递归自改进 | [AutoSFT: An Agentic System for Automated Data Research in Supervised Fine-Tuning](2610.22194-auto-sft/README.md) | Tsinghua University，2026-10-15 | [原作者入口](https://github.com/Thinking-Space/AutoSFT)；官方仓库目前仅README，写明Source code coming soon；未发布算法源码 | 计划键 `auto-sft`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 专家模型编排 | [Disagreement-Guided Weak-to-Strong Routing](2610.22245-disagreement-routing/README.md) | University of Pennsylvania，2026-10-15 | [原作者入口](https://github.com/nooranisima/disagreement-weak-to-strong-routing)；未发布可运行实现；官方仓库仅README，Code coming soon；未见可核验实现许可证 | `disagreement-routing`：仅低成本组件，完整实验不复现 |
| 工具使用与可靠性 | [Diviner: Agentic RCA with Human-Governed Adaptation for Large-Scale Infrastructure](2610.21281-diviner/README.md) | Meta，2026-10-15 | 未发现官方代码 | `diviner`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [GACC-Bench: Benchmarking Goal-Adaptive Context Compression Ability across Large Language Models](2610.21893-gacc-bench/README.md) | Fudan University，2026-10-15 | [原作者入口](https://github.com/weiting24/GACC-Bench)；官方代码/数据入口可读；本轮未确认完整复用许可证，保留各来源数据许可 | `gacc-bench`：CPU 评测接口，不执行模型 |
| 公共评测与协议 | [Harness-Delta Attribution: Dissecting Gains From Harness Evolution](2610.22466-harness-decomposition/README.md) | Amazon，2026-10-15 | [原作者入口](https://github.com/Wenwen-D/HarnessDeltaAttribution)；已核官方仓库包含HDA_SKILL、paired-bootstrap源码、框架实现与benchmark工件，不是占位地址 | `harness-decomposition`：CPU 评测接口，不执行模型 |
| 长期记忆 | [Hy-Memory-30B-A3B: Attributed Reinforcement Learning for Long-Term Memory Writing](2610.22196-hy-memory/README.md) | Tencent Hunyuan，2026-10-15 | [原作者入口](https://github.com/Tencent-Hunyuan/Hy-Memory)；已找到框架仓库和模型入口；不能据此断言完整训练流水线均已公开 | 计划键 `hy-memory`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 工具使用与可靠性 | [JevAgentHarness: Benchmarking, Deploying and Training Decision Models That Share Control with LLMs](2610.21412-jev-agent-harness/README.md) | University of Illinois Urbana-Champaign，2026-10-15 | [原作者入口](https://github.com/JevAgentHarness/JevAgentHarness)；作者公开仓库可读；本轮未核实完整复用许可证，保留上游独立许可边界 | `jev-agent-harness`：仅低成本组件，完整实验不复现 |
| 专家模型编排 | [LEASH: Uncertainty-Aware Weak-to-Strong Escalation and Oversight for Computer-Use Agents](2610.22280-leash/README.md) | Simular，2026-10-15 | 未找到作者发布的方法代码仓库；许可证未确认 | `leash`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [Librarian Agents: Training LLMs to Curate Long-Context Workspaces that Anticipate Future Queries](2610.22273-librarian-agents/README.md) | Stanford University，2026-10-15 | [已开源](https://github.com/teresaz05/librarian-agents) | `librarian-agents`：CPU 评测接口，不执行模型 |
| 记忆与长期交互 | [MemoProAgent: Toward Memory-Driven Proactive Assistance](2610.22671-proper-agent/README.md) | Michigan State University，2026-10-15 | [原作者入口](https://github.com/facebookresearch/Memo-Pro-Agent)；2026-10-22核对Meta官方作者仓库：MemoProAgent已公开GPM推理/评测harness及GRPO reward/launcher入口；固定commit 8563e58d3106c8e0b3108bff64c04d00e1c8f095。相对先前核对5bf57aed仅机构banner、README图片及合规测试更新，无算法或数据实质新释放。CC-BY-NC-4.0非商用源码许可，非OSI开源许可；eval800历史数据按作者README仍需private资源授权，Ego4D视频另行授权；无完整论文训练数据、后训练checkpoint或完整结果配方。v2首页已直接列出仓库与数据链接，不再仅依v1的将来发布承诺交叉归属。此次不运行、移植或重新验收作者代码。 | `proper-agent`：仅低成本组件，完整实验不复现 |
| 长期记忆 | [MemScope: Evolving Agent Memory Architectures through Localized Code Repair](2610.21170-memscope/README.md) | Institute of Computing Technology, Chinese Academy of Sciences / University of Chinese Academy of Sciences，2026-10-15 | 未发现官方代码 | `memscope`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [PROBE: Learning to Audit Policy Compliance in Tool-Using LLM Agents](2610.22124-probe/README.md) | Mohamed bin Zayed University of Artificial Intelligence，2026-10-15 | [原作者入口](https://github.com/Mishrakshitij/PROBE)；作者实现公开可读；本轮未确认可复用许可证，本地独立实现不复制上游代码 | `probe`：仅低成本组件，完整实验不复现 |
| 规划与搜索 | [Repairing LLM-Generated Specifications with Deterministic Diagnosis](2610.22568-drago/README.md) | University of Oxford，2026-10-15 | 未发现官方代码 | `drago`：仅低成本组件，完整实验不复现 |
| RSI | [RSIFlow: Adaptive Self-Improvement Workflows with an Evolving Meta-Agent](2610.21791-rsiflow/README.md) | Beihang University，2026-10-15 | [原作者入口](https://github.com/1HUAN1/RSI-Flow)；MIT；发布的是skill-memory variant，Meta可执行程序固定 | `rsiflow`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [SciPIvot: Benchmarking Principal-Investigator Judgment at Pivotal Moments of Scientific AutoResearch Agents](2610.21082-scipivot/README.md) | University of Maryland, College Park / The Chinese University of Hong Kong（PDF上标已核），2026-10-15 | [已开源](https://github.com/AutoResearch-Factory/SciPIvot) | `scipivot`：CPU 评测接口，不执行模型 |
| 公共评测与协议 | [Shortcut Sensitivity in Agent-Safety Evaluations](2610.22243-shortcut-sensitivity/README.md) | Kontext，2026-10-15 | [原作者入口](https://github.com/hasandemirkiran/shortcut-sensitivity-agent-safety-evaluations)；作者未授予独立复用许可证；仅研究artifact公开可读，不等于标准许可开源 | `shortcut-sensitivity`：仅低成本组件，完整实验不复现 |
| 工具使用与路由 | [SSR: Structural Signal Retriever for Scalable Agent Discovery in LLM-Orchestrated Multi-Agent Systems](2610.21113-structural-signal-retriever/README.md) | State University of Campinas，2026-10-15 | [原作者入口](https://github.com/gmaldonadoc/sscr-agent-routing)；原作者公开仓库，未见代码许可证；本地只依据论文独立实现，不复制上游代码 | `structural-signal-retriever`：仅低成本组件，完整实验不复现 |
| RSI | [Terminal-RSI: Recursive Self-Improving Terminal Agents via Recursive Self-Rewrite and Policy-Refine](2610.22192-terminal-rsi/README.md) | Tencent Hy Frontier / National University of Singapore，2026-10-15 | 未发布；作者项目页标注Code soon / Model soon，未核验方法代码或许可证 | `terminal-rsi`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [ToolBottleneckBench: Measuring Tool-Agent Performance under Controlled Pressures and Fixed Harness Budgets](2610.21098-tool-bottleneck-bench/README.md) | University of Osaka，2026-10-15 | [已开源](https://github.com/zichuanxu/tool-bottleneck-bench) | `tool-bottleneck-bench`：CPU 评测接口，不执行模型 |
| tool-retrieval | [TRACER: Trajectory-Aware Tool Retrieval for LLM Agents](2610.21267-tracer/README.md) | Microsoft，2026-10-15 | 未发布（论文附录A.13明确We release no artifacts here）；未发现原作者方法代码仓库 | `tracer`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [AlphaDiana: A Measurement System for Agents in Verifiable Reasoning Tasks](2610.20675-alpha-diana/README.md) | Hong Kong Baptist University，2026-10-14 | [原作者入口](https://github.com/tmlr-group/AlphaDiana)；官方仓库已提供 alphadiana 框架、配置、脚本与许可证；不是占位仓库 | `alpha-diana`：CPU 评测接口，不执行模型 |
| 多Agent协作 | [ARIA: Runtime Inspection and Amendment for Multi-Agent Systems](2610.20780-aria/README.md) | Florida State University，2026-10-14 | [原作者入口](https://github.com/LabRAI/ARIA)；MIT；训练与serving要求CUDA，原生框架/benchmark另有环境和授权条件 | `aria`：仅低成本组件，完整实验不复现 |
| 公共评测与协议 | [Evolving Together, Failing Apart: The Skill-Policy Co-evolution Trap in Self-Improving Agents](2610.20845-coda/README.md) | Alibaba Token Hub, Alibaba Group，2026-10-14 | 未发现官方代码 | `coda`：CPU 评测接口，不执行模型 |
| Agent记忆与上下文 | [Maximising Transparency in Context Compaction Improves Retention of Facts and Commitments for Lightweight Coding Agents](2610.20116-transparent-compact/README.md) | Hokkaido University，2026-10-14 | [已开源](https://github.com/felixwoolford/transparent-compact-pi) | `transparent-compact`：仅低成本组件，完整实验不复现 |
| 可验证能力组合 | [Recursive Formation and First-Class Reuse of Compositional Capabilities](2610.19414-formcraft/README.md) | not listed in paper，2026-10-14 | [已开源](https://github.com/lancelot138505-cpu/f-system) | `formcraft`：仅低成本组件，完整实验不复现 |
| RSI | [The World Won't Wait: Evaluating and Teaching Agents Under a Live Clock](2610.20665-torsi/README.md) | Peking University / Samsung Research，2026-10-14 | 未发现官方代码 | `torsi`：CPU 评测接口，不执行模型 |
| 公共评测与协议 | [What Coding Agents Leave Unsaid: Measuring Task-State Gaps Between Execution and Reports](2610.20003-ctxgap/README.md) | Tencent，2026-10-14 | [已开源](https://github.com/Kaguraaaaaa/Ctxgap) | `ctxgap`：CPU 评测接口，不执行模型 |
| 公共评测与协议 | [CLASHarness: Benchmarking Multi-Agent Conflict in Computer Use via a Controllable and Verifiable Generation Pipeline](2610.19128-clasharness/README.md) | Google / Emory University（共同署名），2026-10-13 | [已开源](https://github.com/google-research/CLASHarness) | `clasharness`：CPU 评测接口，不执行模型 |
| agentic-rl | [RSIPO: Recursive Self-Improving Policy Optimization for Agentic Reinforcement Learning via Skill-Policy Co-Evolution](../reproductions/2610.15772-rsipo/README.md) | Chinese University of Hong Kong，2026-10-11 | [已开源](https://github.com/zfkarl/RSIPO) | 计划键 `rsipo`：成本过高，暂不复现；待验收，未注册可执行入口。 |
| 自进化与经验复用 | [Harmony Harness: Multi-Objective Self-Evolution of Agent Harnesses](2610.15150-harmony-harness/README.md) | Google Cloud AI Research / Carnegie Mellon University，2026-10-10 | 未发现官方代码 | 计划键 `harmony-harness`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| memory-retrieval | [Beyond the Final Embedding: Retrieving Memories from Token-Level Evidence](../reproductions/2610.13277-beyond-final-embedding/README.md) | Southeast University，2026-10-09 | 未发现官方代码 | `beyond-final-embedding` |
| agent-evolution | [Evo2: Evolving the Evolver through Weight-Harness Co-Evolution](../reproductions/2610.13025-evo2/README.md) | University of Illinois Urbana-Champaign / Google DeepMind，2026-10-09 | 未发现官方代码 | `evo2` |
| 规划、搜索与反思 | [Harness²: Recursive Agent Harnessing for an Open World](2610.14224-harness2/README.md) | Northwestern University，2026-10-09 | [原作者入口](https://github.com/google-research/harness2)；Google Research官方Apache-2.0源码；已固定1cfe254e8d25b15f37048c3730134686abe60335并核对recursion、selection、library与demo，非Google正式支持产品 | `harness2`：仅低成本组件，完整实验不复现 |
| autonomous-research | [Janus: Enhancing Long-Horizon Autonomous Research with Co-Evolving World Models](../reproductions/2610.13194-janus/README.md) | Institute of Computing Technology, Chinese Academy of Sciences，2026-10-09 | 未发现官方代码 | `janus` |
| memory-retrieval | [NEAR: Neighborhood-Aware Residuals for Memory Retrieval](../reproductions/2610.13314-near/README.md) | Southeast University，2026-10-09 | 未发现官方代码 | `near` |
| tool-retrieval | [RATED: Reliability-Aware AI Agent Tool Retrieval via Execution Dynamics](../reproductions/2610.13889-rated/README.md) | Texas Tech University，2026-10-09 | [已开源](https://github.com/Elliotes/EcoAgent) | `rated` |
| recursive-self-improvement | [RSI-Anything: Unlocking Recursive Self-Improvement with World Models](../reproductions/2610.13912-rsi-anything/README.md) | PhAI Labs / The Chinese University of Hong Kong，2026-10-09 | [已开源](https://github.com/Gen-Verse/RSI-Anything) | `rsi-anything` |
| long-term-memory | [Test-Time Memory Construction](../reproductions/2610.13348-t2mem/README.md) | Northeastern University，2026-10-09 | [已开源](https://github.com/OpenBMB/T2Mem) | `t2mem` |
| agent-evaluation | [When Faster Decisions Do Not Make Better Agents: An Empirical Study of Jev in Agent Workflows](../reproductions/2610.13092-jev-workflow/README.md) | Nanjing University，2026-10-09 | 未发现官方代码 | `jev-workflow` |
| 程序进化 | [EvoAlloc: A Self-Evolving Resource Allocation Agent for Efficient Program Evolution](2610.12086-evoalloc/README.md) | King Abdullah University of Science and Technology，2026-10-08 | 未发现官方代码 | `evoalloc` |
| 世界模型 | [Memento 3: Model-Based Recursive Self-Improvement through Reflective Rulebooks](2610.11794-memento3/README.md) | University College London，2026-10-08 | 未发现官方代码 | `memento3` |
| Agent 安全 | [One Word Opens the Gate: The Option-Channel Attack on Typed Decision Models as Agent Guardrails](2610.12292-option-channel-attack/README.md) | University of Southern California，2026-10-08 | [已开源](https://github.com/ArminAzizi98/option-channel-attack) | `option-channel-attack` |
| Agent 安全 | [OnTrack: Real-Time Monitoring and Intervention in LLM Agent Trajectories via Streaming Structure-Aware Optimal Transport](2610.12375-ontrack/README.md) | Cribl AI，2026-10-08 | 未发现官方代码 | `ontrack` |
| 递归自改进 | [Recursive Self-Improvement through Multi-Agent Self-Supervision](2610.12176-mass/README.md) | UC Berkeley，2026-10-08 | [已开源](https://github.com/SakanaAI/mass) | `mass` |
| 长期记忆 | [Use and Disuse: Intent-Structured Experience Consolidation for Memory and Learning in LLM Agents](2610.12124-hippocam/README.md) | Institute of Information Engineering, Chinese Academy of Sciences，2026-10-08 | 未发现官方代码 | `hippocam` |
| Agentic RL | [When Should Agents Think? Adaptive Reasoning via Cross-Turn Estimation](2610.12061-race/README.md) | Renmin University of China，2026-10-08 | [已开源](https://github.com/HututuAI/RACE) | `race` |
| Agent 安全 | [SpecGuard: Proving a Task Is Broken Before the Agent Cheats](2610.09159-specguard/README.md) | MATS，2026-10-06 | [原作者入口](https://github.com/prmbiy/specguard)；作者Apache-2.0源码；固定15820b5018296f4b131b39788180b6ab370d9cfb。MATS一作、Google DeepMind合作者，不归作Google一作 | `specguard`：仅低成本组件，完整实验不复现 |
| Agentic RL | [AdaStep: Adaptive Step Credit Weighting for Agentic Reinforcement Learning](2610.03223-adastep/README.md) | Tsinghua University，2026-10-02 | 未发现官方代码 | `adastep` |
| Agentic RL | [Credit Where It Matters: Dependency-Aware Policy Optimization for Terminal Agents](2610.03634-depgpo/README.md) | Southeast University，2026-10-02 | 未发现官方代码 | `depgpo` |
| 程序进化 | [FrugalEvo: Towards Cost-Aware LLM-Guided Program Evolution](2610.03675-frugalevo/README.md) | National University of Singapore，2026-10-02 | [已开源](https://github.com/chchenhui/frugalevo) | `frugalevo` |
| 自进化与经验复用 | [SEER: Self-Evolving Event Reasoning and Retrieval for Time Series Forecasting](2610.04109-seer-forecasting/README.md) | Google Cloud AI Research / University of Virginia，2026-10-02 | [原作者入口](https://github.com/BennyTMT/SEER)；作者仓库存在，所读根目录仅 README、assets、paper 和 citation，未确认可执行核心代码 | 计划键 `seer-forecasting`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 失败恢复 | [Sentry: Learning to Recover from LLM Agent Failures at Test Time](2610.02994-sentry/README.md) | Stanford University，2026-10-02 | 未发现官方代码 | `sentry` |
| Harness 优化 | [ActiveSaddler: Automated Curriculum Learning for Agent Harness Optimization](2610.00906-active-saddler/README.md) | POSTECH，2026-10-01 | [已开源](https://github.com/microsoft/AutoSaddler/tree/feat/activesaddler) | `active-saddler` |
| Coding Agent | [AutoCompact: Learning When to Compact Context in Long-Horizon Coding Agents](2610.02163-autocompact/README.md) | 原文首页未列第一作者机构，2026-10-01 | 未发现官方代码 | `autocompact` |
| 长程 Agent | [Beyond Memory: Harnessing Long-Horizon Agents with Explicit Belief States](2610.01415-belief-state-pos/README.md) | 原文首页未列第一作者机构，2026-10-01 | 未发现官方代码 | `belief-state-pos` |
| 因果检索干预 | [Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval](2610.02070-causal-memory-policy/README.md) | Illinois Institute of Technology，2026-10-01 | [已开源](https://anonymous.4open.science/r/cmp-release-D0C3/) | `causal-memory-policy` |
| 模拟前瞻与动作选择 | [Code Owns the Simulation, Jev Owns the Evaluation](2610.01834-jev-lookahead/README.md) | The Chinese University of Hong Kong，2026-10-01 | 未发现官方代码 | `jev-lookahead` |
| 失败归因 | [DeFA: Dependency-Guided Failure Attribution for LLM Agents](2610.01256-defa/README.md) | Qwen DianJin Team, Alibaba Cloud Computing，2026-10-01 | 未发现官方代码 | `defa` |
| 工作流进化 | [It Takes Workflows to Evolve Better Workflows](2610.01026-flowright/README.md) | William & Mary，2026-10-01 | 未发现官方代码 | `flowright` |
| Agent 记忆 | [Mem++: Non-Destructive Memory for Long-Term Organizational LLM Agents](2610.02002-mem-plus-plus/README.md) | The University of Texas at Austin，2026-10-01 | [已开源](https://github.com/AIDAChip-Inc/mem-plus-plus) | `mem-plus-plus` |
| 本地 Agent 运行框架 | [Mingbird: A Local-First Agent Harness Enabling Small Open Models to Complete Real Tasks](2610.02001-mingbird/README.md) | University of Science and Technology Beijing，2026-10-01 | [已开源](https://github.com/Mingbird/Mingbird-agent) | `mingbird` |
| Agent 安全 | [PACE: Provenance-Aware Capability Enforcement for Tool-Using LLM Agents](2610.01349-pace-capability/README.md) | 原文首页未列第一作者机构，2026-10-01 | 未发现官方代码 | `pace-capability` |
| RSI 安全 | [Safety Must Survive Self-Improvement: Why Failures Persist and How Agents Recover](2610.01073-safe-self-improvement/README.md) | 原文首页未列第一作者机构，2026-10-01 | 未发现官方代码 | `safe-self-improvement` |
| Agent 验证 | [VeriHarness: Scaling Agentic Verification for Long-Horizon Tasks](2610.00972-veriharness/README.md) | Google Cloud AI Research，2026-10-01 | 未发现官方代码 | `veriharness` |
| Jev | [JevSpawn: Adaptive Agentic Inference through Compositional Action Spaces](2610.00437-jev-spawn/README.md) | 原文首页未列第一作者机构，2026-09-30 | 未发现官方代码 | `jev-spawn` |
| Agent 记忆 | [MemFit: Efficient Long-Term Agentic Memory](2610.00872-memfit/README.md) | 原文首页未列第一作者机构，2026-09-30 | 未发现官方代码 | `memfit` |
| RSI | [Self-Evolving Coding Rules for AI Coding Agents](2610.00650-rule-evolve/README.md) | 原文首页未列第一作者机构，2026-09-30 | 未发现官方代码 | `rule-evolve` |
| 上下文管理 | [Context Language Models](2609.37725-context-lm/README.md) | University of Washington / Meta Superintelligence Labs，2026-09-29 | [已开源](https://github.com/facebookresearch/context-language-models) | `context-lm` |
| Harness 设计 | [Learning Meta-Skills for Agent Harness Design in Test-Time AI4AI](2609.38143-meta-skills/README.md) | Apodex / University of Illinois Urbana-Champaign，2026-09-29 | [已开源](https://github.com/qiancheng-apodex/MetaSkill-AI4AI) | `meta-skills` |
| Harness 优化 | [Mixture of Self-Improving Branches for Agent Harness Optimization](2609.37834-branch-mixture/README.md) | 原文首页未列机构，2026-09-29 | 未发现官方代码 | `branch-mixture` |
| 长期记忆 | [ReMem: Rethinking Perception and Memory in Long-Context Recommendation Agents](2609.37311-remem/README.md) | The Hong Kong Polytechnic University，2026-09-29 | [已开源](https://github.com/Quhaoh233/ReMem) | `remem` |
| Agent 推理 | [Thinking Before Thinking: Scaling Agentic Inference Through Meta-Reasoning](2609.38147-meta-reasoning/README.md) | Meta Superintelligence Labs，2026-09-29 | 未发现官方代码 | `meta-reasoning` |
| Agent 记忆 | [UpliftMem: Learning Set-Level Uplift for Agent Memory Retrieval](2609.36805-upliftmem/README.md) | Beihang University，2026-09-29 | 未发现官方代码 | `upliftmem` |
| Agent 评测 | [UserProxyBench: Evaluating LLM User Simulators for Agent Benchmarks and Training](2609.38043-userproxybench/README.md) | 原文未列机构，2026-09-29 | 未发现官方代码 | `user-proxy-bench` |
| RSI | [Video-RSI: Recursive Self-Improvement of Video Understanding Agents via Harness Evolution](2609.37950-video-rsi/README.md) | Tsinghua University，2026-09-29 | [已开源](https://github.com/bingjunluo/Video-RSI) | `video-rsi` |
| Agent 评测 | [Certified Selective Automation of LLM Agent Evaluation](2609.34320-certified-selective-eval/README.md) | Independent Researcher，2026-09-28 | 未发现官方代码 | `certified-selective-eval` |
| 上下文管理 | [Continuous Context Management](2609.35540-ccm/README.md) | University of Miami，2026-09-28 | 未发现官方代码 | `ccm` |
| Agent RL | [Dr.Credit: Rubric-Grounded Process Credit Assignment for Deep Research Agents](2609.34296-dr-credit/README.md) | University of Chinese Academy of Sciences，2026-09-28 | 未发现官方代码 | `dr-credit` |
| Agentic RL | [GraphHCA: Closed-Form Hindsight Credit Assignment for Long-Horizon LLM Agents](2609.35084-graphhca/README.md) | Beihang University，2026-09-28 | 未发现官方代码 | `graphhca` |
| Harness 学习 | [Harness Learning Enables Generalizable Test-Time Adaptation](2609.35738-harness-learning/README.md) | Johns Hopkins University，2026-09-28 | 未发现官方代码 | `harness-learning` |
| 长期记忆 | [Mnemon: Raw Records, Fast Judgments, Slow Thoughts](2609.36059-mnemon/README.md) | 原文未列机构，2026-09-28 | 未发现官方代码 | `mnemon` |
| 规划 | [SAGE: Symbolic Action-Gating and Editing for LLM Task Planners](2609.34268-sage/README.md) | 原文首页未列机构，2026-09-28 | [已开源](https://github.com/mtbui2010/sage) | `sage-planner` |
| 研究自动化 | [Advancing Model Research in AgentX: Long-Horizon Autonomy for Industrial Recommender Systems](2609.30001-agentx-model/README.md) | Kuaishou，2026-09-24 | 未发现官方代码 | `agentx-model-replay` |
| 编程 Agent | [An Empirical Study of Harness Design for Coding Agents](2609.20804-harness-design-study/README.md) | University of Massachusetts Amherst，2026-09-17 | 未发现官方代码 | `harness-design-study` |
| 多 Agent | [CERA-MoA: Co-Evolving Router and Agents for Mixture-of-Agents](2609.18779-cera-moa/README.md) | IIIS, Tsinghua University，2026-09-16 | 未发现官方代码 | `cera-moa` |
| 轨迹精炼 | [Dependency-Aware Trajectory Refinement for Efficient Multi-Turn Agent Fine-Tuning](2609.18417-dependency-refinement/README.md) | ShanghaiTech University，2026-09-16 | [已开源](https://github.com/Alibaba-NLP/VLLM-KB) | `dependency-refinement` |
| 长期记忆 | [Interactive Memory Learning for Long-Term Conversations](2609.17088-interactive-memory/README.md) | Harbin Institute of Technology, Shenzhen / Pengcheng Laboratory，2026-09-15 | 未发现官方代码 | `interactive-memory` |
| GUI Agent | [Reflect, Revise, Reuse: Training-Free Skill Evolution for GUI Agents](2609.17653-evoskill-gui/README.md) | Zhejiang University，2026-09-15 | [已开源](https://github.com/ZJU-REAL/EvoSkill-GUI) | `evoskill-gui` |
| 编程 Agent | [RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views](2609.16936-repoatlas/README.md) | Beihang University，2026-09-15 | 未发现官方代码 | `repoatlas` |
| 科学 Agent | [ScienceBuddy: Recursive-in-Recursive Self-Improvement for Interactive Scientific Agents](2609.17523-sciencebuddy/README.md) | Gen-Verse research collaboration，2026-09-15 | [已开源](https://github.com/Gen-Verse/ScienceBuddy) | `sciencebuddy` |
| Agent 评测 | [Verifiable Social Reasoning for LLM Assistants](2609.17496-fuse-evaluator/README.md) | Google Research / Hebrew University of Jerusalem / University of Cambridge，2026-09-15 | 未发现官方代码 | `fuse-evaluator` |
| Agent RL | [HarnessBandit: Joint Learnability-Transferability Scheduling for Multi-Harness Agentic Reinforcement Learning](2609.13739-harness-bandit/README.md) | Harbin Institute of Technology / Alibaba Cloud，2026-09-12 | 未发现官方代码 | `harness-bandit` |
| 代码 Agent | [Beyond Vector Similarity: Hierarchical Context-Aware Graph RAG vs Standard RAG in Enterprise Code Migration](2609.12464-hcrg/README.md) | Google Cloud，2026-09-11 | 未发现官方代码 | `hcrg`：仅低成本组件，完整实验不复现 |
| 技能进化 | [COBRA-Skills: Contextual Bandit-Guided Evolution for Agent Skill Optimization](2609.11682-cobra-skills/README.md) | The Chinese University of Hong Kong, Shenzhen，2026-09-10 | [已开源](https://github.com/Jerry-LuP/COBRA-Skills) | `cobra-skills` |
| Harness 自进化 | [Ecdysis: Efficient and Effective Training of Runtime Harnesses for LLM Agents](2609.11677-ecdysis/README.md) | Chengdu Institute of Computer Applications, Chinese Academy of Sciences，2026-09-10 | [已开源](https://github.com/cuiyu-ai/Ecdysis) | `ecdysis` |
| 持久化优化规划 | [MAPLE: Memory-Augmented Planning with Language and Evolution](2609.11636-maple/README.md) | Harbin Institute of Technology, Shenzhen，2026-09-10 | [已开源](https://github.com/xin8coder/MAPLE) | `maple` |
| Agent 记忆 | [Grounding Agent Memory: Environment-Probing Curation for Enterprise Agents](2609.11060-grounded-memory/README.md) | Microsoft，2026-09-09 | 未发现官方代码 | `grounded-memory` |
| 搜索 Agent | [SearchAtlas: Analyzing Agentic Search Strategies via Evidential Query Graphs](2609.10901-searchatlas/README.md) | Duke University，2026-09-09 | [已开源](https://github.com/DukeNLP/SearchAtlas) | `searchatlas` |
| Agent RL | [T1: Terminal Agent Reinforcement Learning for Long-Horizon Tasks](2609.11042-t1-terminal-rl/README.md) | National University of Singapore / Tencent，2026-09-09 | 未发现官方代码 | `t1-terminal-rl` |
| 技能检索 | [When Synthetic Data Hurts: On Catastrophic Forgetting in Skill Retrieval for LLM Agents](2609.10750-skill-retention/README.md) | Manulife，2026-09-09 | [已开源](https://github.com/manulife-ai/emnlp2026/) | `skill-retention` |
| 环境反馈脚手架 | [Environments as Scaffold: Enriching Feedback to Bootstrap Self-Evolving Agents in Long-Horizon Tasks](2609.08404-feedback-scaffold/README.md) | Fudan University，2026-09-08 | [已开源](https://github.com/HongbangYuan/EnvAsScaffold) | `feedback-scaffold` |
| 事件树记忆压缩 | [MemForest: Efficient Agent Memory Management via EventTree Partitioning and Progressive Merging](2609.08273-memforest/README.md) | Shanghai Jiao Tong University，2026-09-08 | [已开源](https://github.com/Celina-love-sweet/MemForest) | `memforest` |
| 自进化程序图 | [Procedural Graphs: Self-Evolving Execution Structures for LLM Agents](2609.09153-procedural-graphs/README.md) | Google，2026-09-08 | 未发现官方代码 | `procedural-graphs` |
| Agentic recommendation memory | [AtomRec: Evolving Atomic Memory for Agentic Recommendation](2609.04882-atomrec/README.md) | Xi'an Jiaotong-Liverpool University，2026-09-04 | 未发现官方代码 | `atomrec` |
| Hierarchical skill coevolution | [CoSkill: Joint Reinforcement Learning of Reasoning and Meta-Skill Agents for Hierarchical Skill Evolution](2609.04865-coskill/README.md) | Institute of Automation, Chinese Academy of Sciences，2026-09-04 | [已开源](https://github.com/jinyuan-cookie/CoSkill) | `coskill` |
| Structure-preserving verifier and reward | [SiLR: Structure-Preserving Admission and Process Reward for LLM Tool Agents](2609.04629-silr/README.md) | Institute of Science Tokyo，2026-09-03 | 未发现官方代码 | `silr` |
| Multi-harness RL audit | [What Does Multi-Harness RL Learn? Credit Assignment and Portability in Coding Agents](2609.04518-multi-harness-rl/README.md) | New York University，2026-09-03 | 未发现官方代码 | `multi-harness-rl` |
| skill-retrieval | [Imagine Before Acting: Prospective Skill Identification for LLM Agents](../reproductions/2609.01642-skilldreamer/README.md) | Sichuan University，2026-08-28 | 未发现官方代码 | `skilldreamer` |
| 论文到代码状态子规划 | [DeepRepro: State-Aware Subplanning for Paper-to-Code Reproduction in Evolving Repositories](2608.26557-deeprepro/README.md) | Institute of Computing Technology, Chinese Academy of Sciences，2026-08-27 | [已开源](https://github.com/ruyisy/DeepRepro) | `deeprepro` |
| 红队技能进化 | [RedEvoAgent: Automatic Red-Teaming Agent with Experience-Driven Skill Evolution](2608.27439-redevoagent/README.md) | City University of Hong Kong，2026-08-27 | 未发现官方代码 | `redevoagent` |
| Agent 技能预训练 | [SPT: Skills as Pre-Training Data for Agentic Language Models](2608.26563-spt/README.md) | Beijing University of Posts and Telecommunications，2026-08-27 | 未发现官方代码 | `spt` |
| 软件轨迹筛选 | [SWE-Prime: Fewer Trajectories, Better Performance](2608.27449-swe-prime/README.md) | Sun Yat-sen University，2026-08-27 | 未发现官方代码 | `swe-prime` |
| 行为相关 Harness 验证 | [Verify Smarter, Evolve Further: Efficient Harness Evolution through Behavior-Aware Verification](2608.27311-harnesslens/README.md) | Fudan University，2026-08-27 | [已开源](https://github.com/jhxu5214/HarnessLens) | `harnesslens` |
| Agent 数据质量 | [What Makes Good Agentic Data? An ACE Lens on Data Generation for LLM Agents](2608.27260-ace-data/README.md) | Huawei Technologies Co., Ltd，2026-08-27 | 未发现官方代码 | `ace-data` |
| 可训练协同记忆 | [When Memory Takes Gradients: Collaborative Vector Memory for Agentic Recommender Systems](2608.26895-covemem/README.md) | Shenzhen Technology University，2026-08-27 | 未发现官方代码 | `covemem` |
| 视频研究自适应工具与反思 | [AdaVDR: Adaptive Tool Use and Reflection for Video Deep Research](2608.25559-adavdr/README.md) | Accio Team, Alibaba Group，2026-08-26 | [已开源](https://github.com/Accio-Lab/AdaVDR) | `adavdr` |
| 反事实因果技能图 | [CaSKG: Counterfactual-Causal Skill Graphs for Scalable Agent Skill Retrieval](2608.25500-caskg/README.md) | Jilin University / Ant Group，2026-08-26 | [已开源](https://github.com/ZhiyuanLi218/Caskg) | `caskg` |
| Harness 即时生成与进化 | [JIT-Agent: Scaling Harness Intelligence via Just-in-Time Harness Evolution](2608.25593-jit-agent/README.md) | LV-NUS Lab，2026-08-26 | [已开源](https://github.com/bingreeky/JIT) | `jit-agent` |
| 在线进展成本路由 | [ProgRouter: Online Progress-Guided Orchestration for Multi-Agent LLM Workflows under Quality-Cost Tradeoffs](2608.25992-progrouter/README.md) | Aston University，2026-08-26 | 未发现官方代码 | `progrouter` |
| Agent运行时 | [SKILL.state: Scalable Long-Horizon Agent Skills](2608.26263-skill-state/README.md) | Google，2026-08-26 | 未发现官方代码 | `skill-state`：仅低成本组件，完整实验不复现 |
| 工作流 Prefix-State 调度 | [TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving](2608.25523-topas/README.md) | University of Science and Technology of China，2026-08-26 | 未发现官方代码 | `topas` |
| ML 开发轨迹规划 | [TraceML: An Empirical Analysis of Human-Agent Planning in Machine Learning Development](2608.26086-traceml/README.md) | Carnegie Mellon University，2026-08-26 | [已开源](https://huggingface.co/datasets/jerryyan/TraceML) | `traceml` |
| 环境反馈提示训练 | [AHEAD: Agentic Hints for Effective Agent Development](2608.24114-ahead/README.md) | AWS AI Labs / Purdue University，2026-08-25 | 未发现官方代码 | `ahead` |
| 可验证技能锻造 | [SkillForge: Automated Skill Discovery and Refinement for Tool-Using Agents](2608.24747-skillforge/README.md) | AMAP, Alibaba Group，2026-08-25 | 未发现官方代码 | `skillforge` |
| 多维验证工具自进化 | [SMITH: Self-Improving Tool-Using Agents through Multi-Aspect Verification](2608.24571-smith/README.md) | Appier AI Research / National Taiwan University，2026-08-25 | [已开源](https://github.com/appier-research/smith) | `smith` |
| 异步单流 Agent RL | [SPO++: Stabilizing Asynchronous Agentic Reinforcement Learning via Measure-Theoretic Token Correction](2608.24870-spo-plus-plus/README.md) | Renmin University of China，2026-08-25 | 未发现官方代码 | `spo-plus-plus` |
| 高斯 guidance Agent RL | [Agent-G²: Gaussian Guidance for Agentic Reinforcement Learning](2608.23318-agent-g2/README.md) | Baidu，2026-08-24 | [已开源](https://github.com/ZJU-REAL/Agent-G2) | `agent-g2` |
| Harness 自动优化 | [AutoSaddler: Automatic Harness Optimization with Durable Updates from Agent Execution Traces](2608.23041-autosaddler/README.md) | Microsoft / POSTECH，2026-08-24 | 未发现官方代码 | `autosaddler` |
| 动作级技能优化 | [AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization](2608.21292-auso/README.md) | University of Science and Technology of China，2026-08-21 | [已开源](https://github.com/JordanSancholhz/Action-Skill) | `auso` |
| Agentic RL | [SAPO: Single-Rollout Autoregressive Policy Optimization for Agentic Reinforcement Learning](2608.19842-sapo/README.md) | Xiamen University，2026-08-20 | 未发现官方代码 | `sapo` |
| Agentic RL | [RTPO: Reverse-Turn Policy Optimization for Stabilizing Agentic RL Training](2608.18682-rtpo/README.md) | Adelaide University，2026-08-19 | 未发现官方代码 | `rtpo` |
| Agentic RL | [SPADE: Self-Play in Adaptive Synthetic Executable Environments](2608.19197-spade/README.md) | University of Washington，2026-08-19 | [已开源](https://github.com/spade-rl/spade) | `spade` |
| Agentic RL | [PlanPO: Group Planning-Aware Policy Optimization for Multi-Turn Agentic LLMs](2608.17289-planpo/README.md) | Xiamen University，2026-08-18 | 未发现官方代码 | `planpo` |
| 工具使用 | [Grounding AI Agents in Contracts: An Empirical Evaluation of Spec-Driven Test Generation](2608.17177-spec-driven-tests/README.md) | Google，2026-08-17 | 未发现官方代码 | `spec-driven-tests`：仅低成本组件，完整实验不复现 |
| Agentic RL | [TRCA: Transition-wise Rubric Credit Assignment for Long-horizon LLM Agents](2608.16156-trca/README.md) | Authors did not disclose affiliation，2026-08-17 | 未发现官方代码 | `trca` |
| 记忆 | [HyMem: Hierarchical Context Management for Long-Horizon Agents via Information Isolation](2608.15703-hymem/README.md) | Institute of Automation, Chinese Academy of Sciences，2026-08-16 | 未发现官方代码 | `hymem` |
| 反思 | [LoongReflect: Boosting Long-Horizon Reflection in Search Agents via Global Perspective Distillation](2608.11967-loongreflect/README.md) | Authors did not disclose affiliation，2026-08-12 | 未发现官方代码 | `loongreflect` |
| Agentic RL / efficient long context | [Efficient Reinforcement Learning for Long-Horizon Tool-Use Agentic Tasks](2608.10357-sinkflex-rl/README.md) | Capital One AI Foundations，2026-08-11 | 未发现官方代码 | `sinkflex-rl` |
| 自进化 | [OpenLoopEvolve: A Verifiable Self-Evolution Framework for Loop Policies in Long-Horizon Complex Tasks](2608.09380-openloopevolve/README.md) | Tsinghua University，2026-08-10 | [已开源](https://github.com/yoyoshikc/OpenLoopEvolve) | `openloopevolve` |
| 代码 Agent | [Coupling Planning with Episodic Memory in LLM Agents for Software Issue Resolution](2608.06811-pmcoder/README.md) | Vanderbilt University，2026-08-07 | 未发现官方代码 | `pmcoder` |
| 多轮 Agent RL | [ResidencyRL: Reinforcement Learning in Simulated Clinical Environments](2608.07418-residency-rl/README.md) | Google DeepMind，2026-08-07 | 未发现官方代码 | 计划键 `residency-rl`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 递归 turn 信用 | [AgentOPSD](2608.05987-agent-opsd/README.md) | Tsinghua University，2026-08-06 | [已开源](https://github.com/ZethWang/AgentOPSD) | `agent-opsd` |
| 代码检索 Agent | [CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents](2608.05886-codegrep/README.md) | NetEase Guangzhou AI Lab，2026-08-06 | 未发现官方代码 | `codegrep` |
| 搜索 Agent RL | [Contextual Information Policy Optimization for Search Agents](2608.06128-cipo/README.md) | Beihang University，2026-08-06 | 未发现官方代码 | `cipo` |
| 环境 rehearsal / Agent RL | [EnvACE](2608.06197-envace/README.md) | Shanghai Jiao Tong，2026-08-06 | [已开源](https://github.com/Within-yao/EnvACE) | `envace` |
| Harness 优化评测 | [HarnessOpt-Bench: Evaluating LLMs at Harness Optimization](2608.06301-harnessopt-bench/README.md) | Scale AI，2026-08-06 | 未发现官方代码 | `harnessopt-bench` |
| 全局技能进化 | [Learning Globally Reusable Skills for Coding Agents](2608.06153-gse/README.md) | Tianjin University，2026-08-06 | 未发现官方代码 | `gse` |
| 技能进化安全 | [When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents](2608.05810-vag/README.md) | 论文未列机构，2026-08-06 | 未发现官方代码 | `vag` |
| Harness policy RL | [EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents](2608.05446-evoharness-rl/README.md) | University of Illinois Urbana–Champaign / Meta AI，2026-08-05 | 未发现官方代码 | `evoharness-rl` |
| 端到端 Agent 记忆 | [MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off](2608.04843-memorycpt/README.md) | Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS，2026-08-05 | 未发现官方代码 | `memorycpt` |
| 观测校准蒸馏 | [OCSD](2608.04788-ocsd/README.md) | Nanjing University，2026-08-05 | [已开源](https://github.com/yiy1x/OCSD) | `ocsd` |
| 环境派生中训练 | [State2State: Environment-Derived Mid-Training for LLM Agents](2608.04934-state2state/README.md) | Tsinghua University AIR / Alibaba Group，2026-08-05 | [已开源](https://github.com/THUNLP-MT/State2State) | `state2state` |
| 工具规划 | [ToolLIFT: Lifting Tool-Specific Trajectories into Function-Level Graphs for Generalizable Tool Planning](2608.03468-toollift/README.md) | Authors did not disclose affiliation，2026-08-04 | 未发现官方代码 | `toollift` |
| 可验证统一记忆 | [VerMem](2608.03137-vermem/README.md) | Sun Yat-sen University，2026-08-04 | [已开源](https://github.com/Sun-SYSU-24/VerMem) | `vermem` |
| 检索—记忆共进化 | [CoEvo-Mem](2608.01739-coevo-mem/README.md) | 论文未列机构，2026-08-03 | 未发现官方代码 | `coevo-mem` |
| 搜索轨迹 hindsight | [HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning](2608.01597-hindsearch/README.md) | Santa Clara University，2026-08-03 | [已开源](https://anonymous.4open.science/r/hindsearch-anon-EBDC) | `hindsearch` |
| 工具规划 | [HyperAgent: Planning and Acting over Tool-Schema Hypergraphs for Tool-Use LLM Agents](2608.02650-hyperagent/README.md) | University of New South Wales，2026-07-31 | 未发现官方代码 | `hyperagent` |
| Agent group credit | [Group-Reflective Self-Distillation](2607.28076-grsd/README.md) | Baidu Inc.，2026-07-30 | [已开源](https://github.com/BinbZheng1/GRSD) | `grsd` |
| 多 Agent | [MANTA: Multi-Agent Network Topology Adaptation for Self-Evolving Multi-Agent Systems](2607.28527-manta/README.md) | Cornell University，2026-07-30 | 未发现官方代码 | `manta` |
| CUA Reward 评测 | [OSReward / OS-Shepherd](2607.28609-osreward/README.md) | The University of Hong Kong，2026-07-30 | [已开源](https://os-copilot.github.io/OSReward-Home/) | `os-shepherd` |
| Agent RL | [TAPO](2607.27973-tapo/README.md) | Peking University，2026-07-30 | 未发现官方代码 | `tapo` |
| 成本感知工具停止 | [CAM-DF](2607.27083-cam-df/README.md) | Peking University，2026-07-29 | 未发现官方代码 | `cam-df` |
| 跨任务技能进化 | [SkillRise](2607.26784-skillrise/README.md) | Zhejiang University，2026-07-29 | [已开源](https://github.com/Within-yao/SkillRise) | `skillrise` |
| Agentic RL / turn-level credit | [CAST](2607.25308-cast/README.md) | University of Science and Technology of China，2026-07-28 | [已开源](https://github.com/Wloner0809/CAST) | `cast` |
| Hierarchical skill memory | [HiSkill](2607.25853-hiskill/README.md) | Beijing University of Posts and Telecommunications，2026-07-28 | [已开源](https://github.com/BUPT-GAMMA/HiSkill) | `hiskill` |
| Continual agent memory | [UniMem](2607.26017-unimem/README.md) | CASIA，2026-07-28 | 未发现官方代码 | `unimem` |
| Agentic RL / hindsight skill | [SEED](2607.14777-seed/README.md) | Tsinghua University，2026-07-16 | [已开源](https://github.com/jinyangwu/SEED) | `seed` |
| 主动记忆 | [Memory as a Controlled Process: Learned Adaptive Memory Management for LLM Agents](2607.13591-memcon/README.md) | 未明确标注（正文 HTML 未显示一作机构映射），2026-07-15 | [已开源](https://github.com/ericjiang18/MemCon/) | `memcon` |
| Agentic OPD / rollout budgeting | [TurnOPD](2607.05804-turn-opd/README.md) | Academic author team，2026-07-07 | 未发现官方代码 | `turn-opd` |
| 研究自动化 | [AgentX: Towards Agent-Driven Self-Iteration of Industrial Recommender Systems](2606.26859-agentx/README.md) | Kuaishou，2026-06-26 | 未发现官方代码 | `agentx` |
| 多Agent协作 | [Formalizing Mathematics at Scale](2605.29955-autoformbot/README.md) | FAIR at Meta / CERMICS, ENPC, Institut Polytechnique de Paris，2026-05-28 | [原作者入口](https://github.com/facebookresearch/autoform-bot)；官方框架MIT开源；形式化库另见facebookresearch/atlas-lean；本轮只核源码发布和文档，不安装插件或运行Agent | 计划键 `autoformbot`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 科学研究 Agent | [ScientistOne: Towards Human-Level Autonomous Research via Chain-of-Evidence](2605.26340-scientist-one/README.md) | Google Cloud AI Research，2026-05-25 | [原作者入口](https://github.com/scientist-one/generated-artifacts)；作者Apache-2.0仓库仅发布generated-papers与solution-code；未核到ScientistOne编排或CoE审计系统源码，不能混称系统开源 | `scientist-one`：CPU 评测接口，不执行模型 |
| 训练服务优化 | [PROMPTS: Performance Optimization via Multi-Agent Planning for LLM Training and Serving](mlsys2026-prompts/README.md) | University of Maryland / Google，2026-05-18 | 未发现官方代码 | `prompts` |
| Agent 检索 | [Superintelligent Retrieval Agent: The Next Frontier of Agentic Retrieval](2605.06647-sira/README.md) | Meta Superintelligence Labs / Rice University（工作完成于 Meta），2026-05-07 | [已开源](https://github.com/facebookresearch/sira) | `sira` |
| Step-aligned Agent RL | [StepPO](2604.18401-steppo/README.md) | University of Science and Technology of China，2026-04-20 | 未发现官方代码 | `steppo` |
| 工具调用与环境执行 | [LogAct: Enabling Agentic Reliability via Shared Logs](2604.07988-logact/README.md) | Meta，2026-04-09 | [原作者入口](https://github.com/facebookresearch/logact)；原作者MIT仓库已公开；核对固定commit db395449fb2dbb534c8eec848900252ac8324ab2。本地独立实现有界单机SQLite协议，不安装作者插件或下载模型 | `logact`：仅低成本组件，完整实验不复现 |
| 策略—工具图共进化 | [SEARL](2604.07791-searl/README.md) | Shanghai AI Laboratory，2026-04-09 | 未发现官方代码 | `searl` |
| Agent 评测 | [TFRBench: A Reasoning Benchmark for Evaluating Forecasting Systems](2604.05364-tfrbench/README.md) | Google Cloud AI Research / University of Kentucky，2026-04-07 | 未发现官方代码 | `tfrbench`：CPU 评测接口，不执行模型 |
| Agent 数据合成 | [Reasoning-Driven Synthetic Data Generation and Evaluation](2603.29791-simula/README.md) | EPFL，2026-03-31 | 未发现官方代码 | `simula`：CPU 评测接口，不执行模型 |
| AI 研究 Agent | [AIRA2: Overcoming Bottlenecks in AI Research Agents](2603.26499-aira2/README.md) | FAIR at Meta / University College London，2026-03-27 | 未发现官方代码 | `aira2` |
| RSI | [HyperAgents](2603.19461-hyperagents/README.md) | University of British Columbia，2026-03-19 | [已开源](https://github.com/facebookresearch/hyperagents) | `hyperagents` |
| 技能设计 | [Memento-Skills](2603.18743-memento-skills/README.md) | Memento Team，2026-03-19 | [已开源](https://github.com/Memento-Teams/Memento-Skills) | `memento-skills` |
| Agent 自进化 | [POLCA: Stochastic Generative Optimization with LLM](2603.14769-polca/README.md) | University of Wisconsin-Madison，2026-03-16 | [原作者入口](https://github.com/rlx-lab/POLCA)；作者公开入口固定356d0177d034df8c70bf351f5f62c93dbb226b41；其setup脚本指向Trace experimental，核心核对4ee52f12f0bb328dfee2f16b6c1801232c6ccf46 | `polca`：仅低成本组件，完整实验不复现 |
| 主动记忆 | [U-Mem](2602.22406-u-mem/README.md) | National University of Singapore，2026-02-25 | [已开源](https://anonymous.4open.science/r/code-release-456D/) | `u-mem` |
| Agent 评测 | [ConvApparel: A Benchmark Dataset and Validation Framework for User Simulators in Conversational Recommenders](2602.16938-convapparel/README.md) | Google，2026-02-18 | 未发现官方代码 | `convapparel`：CPU 评测接口，不执行模型 |
| 个性化 Agent | [Learning Personalized Agents from Human Feedback](2602.16173-pahf/README.md) | Meta Superintelligence Labs / Princeton University（工作完成于 Meta），2026-02-18 | [已开源](https://github.com/facebookresearch/PAHF) | `pahf` |
| Agent 安全 | [CausalArmor: Efficient Indirect Prompt Injection Guardrails via Causal Attribution](2602.07918-causal-armor/README.md) | Google Cloud AI Research，2026-02-08 | 未发现官方代码 | `causal-armor`：仅低成本组件，完整实验不复现 |
| 自动研究 | [AIRS-Bench: a Suite of Tasks for Frontier AI Research Science Agents](2602.06855-airs-bench/README.md) | FAIR at Meta / University of Oxford，2026-02-06 | [原作者入口](https://github.com/facebookresearch/airs-bench)；官方任务定义与评测代码已发布，CC BY-NC 4.0；本地尚未接入任务运行器 | 计划键 `airs-bench`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 自进化与经验复用 | [MARS: Modular Agent with Reflective Search for Automated AI Research](2602.02660-mars-research/README.md) | Google Cloud AI Research，2026-02-02 | [原作者入口](https://github.com/jfc43/MARS)；MIT 作者仓库存在，根目录为 exp-logs/figures/README/LICENSE；发布生成代码和轨迹，未确认完整 MARS controller | 计划键 `mars-research`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |
| 记忆技能 | [MemSkill](2602.02474-memskill/README.md) | Nanyang Technological University，2026-02-02 | [已开源](https://github.com/ViktorAxelsen/MemSkill) | `memskill` |
| 规划强化学习 | [PEARL](2601.20439-pearl/README.md) | 中国科学院信息工程研究所，2026-01-28 | 未发现官方代码 | `pearl` |
| 代码 Agent | [Dynamic Cogeneration of Bug Reproduction Test in Agentic Program Repair](2601.19066-dynamic-brt/README.md) | Google，2026-01-27 | 未发现官方代码 | `dynamic-brt`：仅低成本组件，完整实验不复现 |
| 技能库强化学习 | [SAGE](2512.17102-sage/README.md) | University of Wisconsin–Madison，2025-12-18 | 未发现官方代码 | `sage` |
| 零数据多 Agent | [Agent0](2511.16043-agent0/README.md) | University of North Carolina at Chapel Hill，2025-11-20 | 未发现官方代码 | `agent0` |
| Agentic RL 基础设施 | [Agent-R1](2511.14460-agent-r1/README.md) | University of Science and Technology of China，2025-11-18 | [已开源](https://github.com/AgentR1/Agent-R1) | `agent-r1` |
| 过程记忆 | [LEGOMem](2510.04851-legomem/README.md) | Microsoft Research，2025-10-06 | 未发现官方代码 | `legomem` |
| 多轮用户 Agent RL | [MUA-RL](2508.18669-mua-rl/README.md) | Meituan，2025-08-26 | [已开源](https://github.com/zzwkk/MUA-RL) | `mua-rl` |
| 工具学习 | [ToolGrad: Efficient Tool-Use Dataset Generation with Textual Gradients](2508.04086-toolgrad/README.md) | Google，2025-08-06 | [已开源](https://github.com/zhongyi-zhou/toolgrad) | `toolgrad` |
| Agent RL | [Agent Lightning](2508.03680-agent-lightning/README.md) | Microsoft Research，2025-08-05 | [已开源](https://github.com/microsoft/agent-lightning) | `agent-lightning` |
| 工具记忆 | [MemTool](2507.21428-memtool/README.md) | PricewaterhouseCoopers Commercial Technology and Innovation Office，2025-07-29 | 未发现官方代码 | `memtool` |
| 网页 Agent RL | [WebAgent-R1](2505.16421-webagent-r1/README.md) | University of Virginia，2025-05-22 | [已开源](https://github.com/weizhepei/WebAgent-R1) | `webagent-r1` |
| Agent group credit | [GiGPO](2505.10978-gigpo/README.md) | Nanyang Technological University，2025-05-16 | 未发现官方代码 | `gigpo` |
| 多轮 Agent RL | [RAGEN](2504.20073-ragen/README.md) | Northwestern，2025-04-24 | [已开源](https://github.com/RAGEN-AI/RAGEN) | `ragen` |
| 工具强化学习 | [ToolRL](2504.13958-toolrl/README.md) | University of Illinois Urbana-Champaign，2025-04-16 | 未发现官方代码 | `toolrl` |
| 推理中工具调用 | [ReTool](2504.11536-retool/README.md) | ByteDance Seed，2025-04-15 | 未发现官方代码 | `retool` |
| 深度研究 RL | [DeepResearcher](2504.03160-deepresearcher/README.md) | HKU，2025-04-04 | [已开源](https://github.com/GAIR-NLP/DeepResearcher) | `deepresearcher` |
| 搜索 Agent RL | [Search-R1](2503.09516-search-r1/README.md) | University of Illinois Urbana-Champaign，2025-03-12 | [已开源](https://github.com/PeterGriffinJin/Search-R1) | `search-r1` |
| 长时程 Agent RL | [LOOP](2502.01600-loop/README.md) | Apple，2025-02-03 | [已开源](https://github.com/apple/ml-loop) | `loop` |
| 通用软件 Agent | [OpenHands](2407.16741-openhands/README.md) | All-Hands-AI，2024-07-23 | [已开源](https://github.com/All-Hands-AI/OpenHands) | `openhands` |
| 软件工程 ACI | [SWE-agent](2405.15793-swe-agent/README.md) | Princeton University，2024-05-06 | [已开源](https://github.com/SWE-agent/SWE-agent) | `swe-agent` |
| 通用 Agent 评测 | [GAIA](2311.12983-gaia/README.md) | Meta AI，2023-11-21 | [已开源](https://huggingface.co/gaia-benchmark) | `gaia` |
| 虚拟上下文 | [MemGPT](2310.08560-memgpt/README.md) | University of California, Berkeley，2023-10-12 | [已开源](https://github.com/letta-ai/letta) | `memgpt` |
| Agent 搜索 | [LATS](2310.04406-lats/README.md) | University of Illinois Urbana-Champaign，2023-10-06 | [已开源](https://github.com/lapisrocks/LanguageAgentTreeSearch) | `lats` |
| 多 Agent | [AutoGen](2308.08155-autogen/README.md) | Microsoft Research，2023-08-16 | [已开源](https://github.com/microsoft/autogen) | `autogen` |
| 多 Agent 软件工程 | [MetaGPT](2308.00352-metagpt/README.md) | DeepWisdom，2023-08-01 | [已开源](https://github.com/FoundationAgents/MetaGPT) | `metagpt` |
| 解耦规划 | [ReWOO](2305.18323-rewoo/README.md) | Microsoft Research，2023-05-29 | [已开源](https://github.com/billxbf/ReWOO) | `rewoo` |
| 工具指令与评测 | [ToolBench](2305.16504-toolbench/README.md) | Tsinghua University，2023-05-25 | 未发现官方代码 | `toolbench` |
| 终身学习 | [Voyager](2305.16291-voyager/README.md) | NVIDIA，2023-05-25 | [已开源](https://github.com/MineDojo/Voyager) | `voyager` |
| 工具反馈 | [CRITIC](2305.11738-critic/README.md) | Microsoft，2023-05-19 | [已开源](https://github.com/microsoft/ProphetNet/tree/master/CRITIC) | `critic` |
| 推理搜索 | [Tree of Thoughts](2305.10601-tree-of-thoughts/README.md) | Princeton University，2023-05-17 | [已开源](https://github.com/princeton-nlp/tree-of-thought-llm) | `tree-of-thoughts` |
| 记忆与反思 | [Generative Agents](2304.03442-generative-agents/README.md) | Stanford University，2023-04-07 | [已开源](https://github.com/joonspk-research/generative_agents) | `generative-agents` |
| 多 Agent 协作 | [CAMEL](2303.17760-camel/README.md) | King Abdullah University of Science and Technology，2023-03-31 | [已开源](https://github.com/camel-ai/camel) | `camel` |
| 专家模型编排 | [HuggingGPT](2303.17580-hugginggpt/README.md) | Zhejiang University，2023-03-30 | [已开源](https://github.com/microsoft/JARVIS) | `hugginggpt` |
| 自我迭代 | [Self-Refine](2303.17651-self-refine/README.md) | Carnegie Mellon University，2023-03-30 | [已开源](https://github.com/madaan/self-refine) | `self-refine` |
| 自我反思 | [Reflexion](2303.11366-reflexion/README.md) | Northeastern University，2023-03-20 | [已开源](https://github.com/noahshinn/reflexion) | `reflexion` |
| 自动工具推理 | [ART](2303.09014-art/README.md) | University of Washington，2023-03-16 | [已开源](https://github.com/bhargaviparanjape/language-programmes) | `art` |
| 工具学习 | [Toolformer](2302.04761-toolformer/README.md) | Meta AI Research，2023-02-09 | 未发现官方代码 | `toolformer` |
| 程序推理 | [PAL](2211.10435-pal/README.md) | Carnegie Mellon University，2022-11-18 | [已开源](https://github.com/reasoning-machines/pal) | `pal` |
| 推理与行动 | [ReAct](2210.03629-react/README.md) | Princeton University，2022-10-06 | [已开源](https://github.com/ysymyth/ReAct) | `react` |
| 神经符号路由 | [MRKL](2205.00445-mrkl/README.md) | AI21 Labs，2022-05-01 | 未发现官方代码 | `mrkl` |
| 具身规划 | [SayCan](2204.01691-saycan/README.md) | Robotics at Google，2022-04-04 | [已开源](https://github.com/google-research/google-research/tree/master/saycan) | `saycan` |
| 浏览问答 | [WebGPT](2112.09332-webgpt/README.md) | OpenAI，2021-12-17 | [已开源](https://huggingface.co/datasets/openai/webgpt_comparisons) | `webgpt` |
| 形式化数学 Agent | [AutoformBench: A Lean Formalization Benchmark for Advanced Mathematics](autoformbench/README.md) | FAIR at Meta，未标注 | [已开源](https://github.com/facebookresearch/autoformbench) | `autoformbench`：CPU 评测接口，不执行模型 |

</div>

分类浏览：

- [按机构/公司/学校](catalog/by-organization.md)
- [按主题](catalog/by-topic.md)
- [按年份](catalog/by-year.md)
