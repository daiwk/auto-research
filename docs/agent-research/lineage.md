# Agent 论文谱系与缺口

本页维护 Agent 论文系统审计。覆盖范围从推理-行动、反思、规划搜索、工具学习，
延伸到多 Agent 编排、终身学习和 2026 年规划强化学习；最新边界检查至
**2026-07-28**。

## 谱系覆盖

| 谱系 | 代表方法 | 状态 | 本仓库覆盖 |
|---|---|---|---|
| 推理与行动 | ReAct、ReWOO | 已实现 | 逐步交互；Planner/Worker/Solver 解耦 |
| 自我改进 | Self-Refine、Reflexion | 已实现 | episode 内迭代；跨 trial 语言反思 |
| 显式搜索 | Tree of Thoughts、LATS | 已实现 | BFS thought tree；MCTS + environment feedback |
| 工具学习 | Toolformer、PEARL | 已实现 | 自监督工具标注；工具探索 + Planner RL |
| 多 Agent 编排 | AutoGen | 已实现 | 角色消息、交接与终止 |
| 终身学习与记忆 | Voyager、U-Mem、LEGOMem、MemTool | 已实现 | 技能、知识、过程与工具记忆 |

## 仍缺失但值得补的 P1

| 方法 | 为什么仍有价值 | 未在本批实现的原因 |
|---|---|---|
| MetaGPT | 经典 SOP 驱动软件多 Agent，补齐结构化协作 | 需要代码仓库级任务和 artifact evaluator，PlanBench mini 不足 |
| CRITIC | 用外部工具验证并修正生成，连接 tool use 与 self-correction | 需要真实搜索/代码执行沙箱与可追踪错误注入 |
| Agent Lightning | 把任意 Agent 轨迹与 RL 训练解耦，适合接 evolve | 需要统一真实 LLM executor 和训练 backend 后才能公平实现 |
| SWE-agent / OpenHands 系谱 | 代码 Agent 的重要工程分支 | 应接 SWE-bench Lite 与隔离容器，不能用确定性规划题代替 |

## 当前结论

经典主干已从“单 Agent 思考/行动”覆盖到“搜索、反思、工具、多 Agent、记忆和 Planner
RL”。下一优先级不是继续增加演示型状态机，而是接入 ToolHop、SWE-bench Lite 等真实
环境，让成本、错误恢复、消息轨迹和跨 episode 复用可被统一比较。
