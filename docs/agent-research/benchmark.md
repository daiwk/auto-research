# Agent 统一评测协议

Agent 方法不仅比较最终成功率，还必须比较上下文、知识获取和工具维护成本。当前
mini-suite 保证 Mac/Linux CPU 可重复运行，后续真实 LLM executor 沿用相同指标接口。

## 评测矩阵

| Benchmark | 主要能力 | 本地任务 | 关键指标 |
|---|---|---|---|
| `evomem-mini` | episode 内/跨 episode 的知识与执行记忆 | EvoMem 四象限任务 | joint success、获取成本、memory size |
| `planbench-mini` | 可验证规划与过程复用 | 结构化动作序列 | plan success、平均成本、reused plans |
| `scalemcp-mini` | 有限上下文中的动态工具集合 | 多轮工具路由 | task success、上下文成本、tool evictions |
| `swebench-local` | 代码定位、编辑、测试与修订 | 临时 Python 仓库 + 真实 unittest | resolved rate、命令/编辑、反馈轮次、复用 |
| `osreward-mini` | CUA reward 判分与宽松偏差 | 四平台完成/未完成证据轨迹 | success/fail recall、balanced accuracy、leniency |
| `toolroute-l2` | 无 oracle 规划、工具反馈与故障恢复 | evaluator 隐藏 labels 的多步工具环境 | answer accuracy、plan F1、recovery、invalid-tool rate、cost |

前三项与 `osreward-mini` 是仓库自带的确定性 mini-suite；`swebench-local` 会真实执行
代码，但任务仍是仓库自带 micro fixtures，不是官方 SWE-bench Lite；`osreward-mini`
复现官方指标与证据核验协议，不是官方 1,019 条截图轨迹。

`toolroute-l2`与上述 L1 mini-suite 分层：policy 接口没有 reference answer/plan，结果可以
在相同 benchmark 版本、预算和 seeds 内公平比较。详细协议和三 seed 结果见
[Agent L2 无 Oracle 能力评测](capability-benchmark.md)。

## 公平口径

- 固定 120 episodes 和 seed 42，方法与基线使用同一任务序列。
- `long-context` 是不压缩历史的对照，成本按保留的上下文单元累计。
- 成功率相同时，比较平均成本和方法特有诊断；不能只用成本推断真实 LLM 效果。
- 新方法必须保存逐步 trace，标明记忆写入、检索、升级、复用和淘汰事件。
- 调用外部模型时必须记录模型、采样参数、token 成本、失败重试和缓存命中。
- 代码 benchmark 的初始仓库必须真实失败；成功只由回归测试退出码判定，并保存命令输出。

## 稳定结果

| 方法与 benchmark | joint success | 平均成本 | 诊断 |
|---|---:|---:|---|
| Long-context · EvoMem mini | 1.0000 | 64.5000 | 历史线性增长 |
| U-Mem · EvoMem mini | 1.0000 | 3.0500 | memory size 12 |
| LEGOMem · PlanBench mini | 1.0000 | 1.1200 | reused plans 108 |
| MemTool · ScaleMCP mini | 1.0000 | 1.9812 | tool evictions 200 |
| ReAct · ScaleMCP mini | 1.0000 | 3.0000 | reasoning/actions 360/360 |
| Reflexion · PlanBench mini | 0.9000 | 1.1000 | reflections 12 |
| Voyager · PlanBench mini | 1.0000 | 1.1200 | skills created/reused 12/108 |
| Tree of Thoughts · PlanBench mini | 1.0000 | 2.5000 | expanded/backtracked 1200/480 |
| LATS · PlanBench mini | 1.0000 | 4.0000 | rollouts/reflections 480/360 |
| Toolformer · ScaleMCP mini | 1.0000 | 3.0000 | accepted/candidate calls 360/540 |
| Self-Refine · PlanBench mini | 1.0000 | 2.0000 | feedback/refinement 120/120 |
| ReWOO · PlanBench mini | 1.0000 | 3.5000 | plans/worker calls 120/360 |
| AutoGen · PlanBench mini | 1.0000 | 3.0000 | agent messages/critic rounds 360/120 |
| PEARL · PlanBench mini | 1.0000 | 1.1200 | explorations/updates/reuse 24/12/108 |
| MRKL · ScaleMCP mini | 1.0000 | 1.2500 | router/symbolic calls 360/170 |
| HuggingGPT · PlanBench mini | 1.0000 | 2.3500 | model matches/edges 360/240 |
| Generative Agents · EvoMem mini | 1.0000 | 1.7900 | retrieved/reflections 354/30 |
| MemGPT · EvoMem mini | 1.0000 | 0.9200 | writes/page-ins/interrupts 108/96/108 |
| WebGPT · ScaleMCP mini | 1.0000 | 3.0000 | references/candidates 600/240 |
| SayCan · PlanBench mini | 1.0000 | 3.3750 | checks/filtered 1350/790 |
| PAL · ScaleMCP mini | 1.0000 | 1.4000 | programs/interpreter calls 120/120 |
| ART · PlanBench mini | 1.0000 | 1.5500 | retrievals/pauses/updates 108/360/12 |
| OS-Shepherd protocol · OSReward mini | 1.0000 BalAcc | 2 evidence checks | sRec/fRec 1.0000/1.0000；leniency 0 |

稳定数据：
[`agent-mini-suites-seed42.json`](../experiments/agent-mini-suites-seed42.json)。
经典方法结果：
[`classic-agent-mini-suites-seed42.json`](../experiments/classic-agent-mini-suites-seed42.json)。
代码 sandbox 结果：
[`agent-code-sandbox-seed42.json`](../experiments/agent-code-sandbox-seed42.json)。
本批经典缺口：
[`p0-missing-agent-mini-suites-seed42.json`](../experiments/p0-missing-agent-mini-suites-seed42.json)。
P1 候选：
[`p1-agent-candidates-mini-suites-seed42.json`](../experiments/p1-agent-candidates-mini-suites-seed42.json)。

## 运行与产物

```bash
auto-research agent-eval --method voyager \
  --benchmark planbench-mini --episodes 120 --seed 42

auto-research agent-eval --method swe-agent \
  --benchmark swebench-local --episodes 12 --seed 42

auto-research agent-eval --method os-shepherd \
  --benchmark osreward-mini --episodes 120 --seed 42

auto-research agent-capability \
  --methods long-context,react,reflexion,agent-g2,ahead,auso \
  --episodes 60 --seeds 42,43,44
```

产物写入 `runs/agent-research/<method>-<benchmark>-seed<seed>/`，包括逐 episode
trace、`metrics.json` 和中文 `report.md`。

## 新方法验收

新增方法必须通过单元测试、对应 mini-suite/真实 sandbox、稳定指标检查和 MkDocs 严格构建。
若论文依赖私有环境、付费 API 或人工 judge，页面必须说明未覆盖部分，并优先增加
公开 benchmark 适配器，不能用确定性任务分数冒充论文结果。
## Agentic RL 与持续记忆诊断

新增方法除 success/cost 外必须保留机制计数：SEED 的 hindsight skill 和 dense credit、
CAST 的 solver query 和 turn credit、TurnOPD 的 rollout 节省、HiSkill 的图节点/边与
AtomicOp 复用、UniMem 的 episodic/parametric route 和 consolidation。相同 benchmark
内固定 episode、memory budget 与 seed，禁止只比较最终成功率。

CAM-DF 必须报告总候选/实际开放工具、exposure reduction、成本感知停止与
regret-weighted label 数；SkillRise 必须分别报告 skill document 更新、跨任务复用和
下游 credit update，不能把普通 key-value memory 改名为跨任务技能进化。

Search-R1 还必须报告搜索次数、被 loss mask 的检索 token 和 outcome update；RAGEN
必须报告 trajectory rollout/filter、critic baseline、Echo Trap 探针与 gradient clip。
确定性 mini-suite 的 100% 成功率只证明控制流可执行，不等于论文真实搜索或游戏效果。

LOOP 必须报告 leave-one-out update、旧轨迹复用和逐 token clipping；WebAgent-R1
必须报告被压缩的上下文 token、并行完整轨迹组和 M-GRPO update；MUA-RL 必须保留
模拟用户 turn、意图修正、真实工具响应和最终任务奖励计数。固定 seed 快照见
[`omitted-agentic-rl-opd-seed42.json`](../experiments/omitted-agentic-rl-opd-seed42.json)；
mini-suite 不冒充 AppWorld、WebArena-Lite、TAU2 或 BFCL。
