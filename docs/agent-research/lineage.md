# Agent 论文谱系与缺口

本页维护 Agent 论文系统审计。覆盖范围从推理-行动、反思、规划搜索、工具学习，
延伸到多 Agent 编排、终身学习和 2026 年规划强化学习；最新边界检查至
**2026-07-30**。

## 谱系覆盖

| 谱系 | 代表方法 | 状态 | 本仓库覆盖 |
|---|---|---|---|
| 推理与行动 | ReAct、ReWOO | 已实现 | 逐步交互；Planner/Worker/Solver 解耦 |
| 自我改进 | Self-Refine、Reflexion | 已实现 | episode 内迭代；跨 trial 语言反思 |
| 显式搜索 | Tree of Thoughts、LATS | 已实现 | BFS thought tree；MCTS + environment feedback |
| 工具学习 | Toolformer、PEARL | 已实现 | 自监督工具标注；工具探索 + Planner RL |
| 多 Agent 编排 | AutoGen、MetaGPT | 已实现 | 角色消息、交接、终止；软件 SOP 与角色 artifact |
| 终身学习与记忆 | Voyager、U-Mem、LEGOMem、MemTool、HiSkill、UniMem、SkillRise | 已实现 | 技能、知识、过程、工具、层次图、跨任务 skill document 与 episodic→parametric 记忆 |
| 外部反馈 | CRITIC | 已实现 | 真实失败 patch、测试反馈和修订 |
| Agent RL / OPD | Agent Lightning、Search-R1、RAGEN、LOOP、WebAgent-R1、MUA-RL、SEED、CAST、TurnOPD | 已实现 | 搜索/网页/长时程/多轮用户 RL、轨迹稳定化、hindsight skill、turn credit、动态 rollout budget |
| 软件工程 Agent | SWE-agent、OpenHands | 已实现（local） | 真实临时仓库、编辑、命令和回归测试 |
| CUA reward 评测 | OSReward / OS-Shepherd | 已实现（protocol mini-suite） | success/fail recall、balanced accuracy 与 leniency 审计 |
| 模块化专家系统 | MRKL、HuggingGPT | 已实现 | 神经符号 router；模型能力匹配与依赖图执行 |
| 经典长期状态 | Generative Agents、MemGPT | 已实现 | 记忆打分/反思；虚拟上下文换入换出 |
| 浏览与引用 | WebGPT | 已实现（deterministic） | 浏览动作、证据引用与轨迹拒绝采样 |
| 具身技能 grounding | SayCan | 已实现（simulation） | 语言相关性乘以技能 affordance |
| 程序与自动工具推理 | PAL、ART | 已实现 | 符号解释器；task-library 检索与工具暂停 |

## 下一阶段缺口

| 环境 | 当前状态 | 下一步 |
|---|---|---|
| `swebench-local` | 真实文件与 subprocess；仓库自带受控 fixture | 接官方 SWE-bench Lite 数据、repository snapshot 与容器 |
| ToolHop | 尚未接入 | 增加公开数据下载、真实工具 runtime 与多跳 verifier |
| Browser | WebGPT 控制流已实现；仍是确定性工具环境 | 增加隔离浏览器、网页快照与网络策略 |
| Agent Lightning LLM RL | transition/credit 机制已实现 | 连接可训练 LLM policy 与统一多轮 controller |

## 当前结论

经典主干已覆盖思考/行动、搜索、反思、神经符号与专家模型编排、多 Agent、长期记忆、
虚拟上下文、Planner RL 和真实代码执行。`swebench-local` 不冒充官方数据；下一优先级
仍是用户已暂缓的外部公开环境 adapter 与可训练 LLM executor。

本轮系统复查补齐了三个互补分支：LOOP 的长时程 leave-one-out PPO 与旧轨迹复用、
WebAgent-R1 的上下文压缩和并行完整轨迹 M-GRPO、MUA-RL 的模拟用户澄清与真实工具
交互。它们均已作为 `critic`、`planner` 或 `tool` genome 算子进入统一 evolve。
