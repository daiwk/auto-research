# 10月22日 Google / Meta 优先补查

本轮8类 arXiv 仍是**10月21日同一公告**，1126个去重论文身份及版本记录与PR219相同，未确认新的首发或更新版本。以下是官方仓库补发现和代码发布更新，不能算成“几小时内又新发了几篇”。

## 固定交付范围

| 项目 | 来源与分类 | 低成本交付与边界 |
| --- | --- | --- |
| [DeepSEA](../../foundation-models/2610.26155-deepsea/README.md) | Google Research，一作 Jiuzhou Han；10月19日，同公告补发现 | 五任务外部预测评分器、仅公开输入投影、覆盖检查；实际核对官方MGSM的13种语言共3250条schema，不生成模型预测 |
| [LogAct](../../agent-research/2604.07988-logact/README.md) | Meta，一作 Mahesh Balakrishnan；4月9日，历史补发现 | 本机SQLite意图→投票→决议→执行/结果协议、崩溃恢复与真实小型文件/数据库副作用；不是LLM Agent或分布式共识 |
| [ProPerAgent](../../agent-research/2610.22671-proper-agent/README.md) | 官方作者仓库新发布，不是论文新版本 | 修正源码链接、固定revision和CC-BY-NC-4.0许可；有推理/评测与GRPO入口，但完整训练数据和后训练checkpoint未发布，不升级本地证据等级 |
| [SWE-sweep](https://swesweep.com/paper) | Meta FAIR；非阻塞归档例外 | 报告页日期与网站日期不同，准确首发日未证实；固定作者仓库LICENSE仍为评审用途限定，不复制或执行其源码，不冒充正式实现条目 |

两项新增组件均为**CPU-only L1机制/接口诊断**，0次模型调用，禁止由evolve据此晋级。本轮没有新增或升级CUDA路径，因此没有虚构A100/A30回执。三seed验证的是实现合同，不代表多语模型或Agent能力。

## 成本与数据边界

- DeepSEA全模型矩阵、13语种五任务推理及MetricX-24评测：成本过高，**完整实验不复现（审查DONE）**。本地WMT24的chrF沿用作者公开评分脚本，不将其称为论文使用的MetricX-24；请求MetricX会明确拒绝。chrF另与固定SacreBLEU2.5.1做边界数值对照。
- 官方DeepSEA评测集只核对固定文件hash、数量和白名单投影，不提交文本/gold，不用于训练、选参或evolve。指标卡只显示评分合同与恢复计数，不将给定正确答案的fixture分数当作模型准确率。
- LogAct完整LLM语义投票、AgentDojo/swarm及多机后端实验：成本过高，**完整实验不复现（审查DONE）**。任意外部动作不能凭日志保证exactly-once；不确定动作默认不重放，显式幂等合同也需要外部执行器真正兑现。
- SWE-sweep全实验涉及100个仓库、4068个缺陷和7个LM；原文表24（物理第39页）四种展示配置的单仓库中位数为0.3–1.6小时，最长5.5小时。**完整实验不复现（审查DONE）**；许可/首发日例外归档，不阻塞审查，也不自动重试。

## 来源覆盖与未证实范围

8类arXiv逐条版本身份差集为0；DeepMind成功读取9页265条，有限目录差集为0。Google年份目录、Meta论文目录本轮超时，记录为不可用、差集未知，**不是0条新论文**。用Google/Meta官方仓库及作者名单补证本轮四项，但不声称穷尽组织全部仓库或所有论文全文。

全局审查水位仍为**2026-10-15**。本轮是有边界的增量/补查，不把两项组件交付冒充全窗口审查完成。见[来源回执](source-coverage.json)、[成本与例外清单](task-scope.json)、[官方MGSM无文本schema回执](deepsea-official-schema.json)。

## 重跑

```bash
PYTHONPATH=src python scripts/run_oct22_priority_components.py \
  --output runs/oct22-cpu-contracts.json
PYTHONPATH=src python scripts/build_oct22_priority_artifacts.py --check
```

运行器要求源码与真实Git提交匹配，拒绝未提交/变动源码；正式记录保留[可移植源码证明](frozen-sources.json)、三seed指标与负对照。官方MGSM archive的hash/schema检查为可选参数`--mgsm-archive`，不会下载资源或打印题目答案。

交付后清理本轮临时依赖、PDF渲染和站点构建目录；保留实验回执、失败记录及可复用公开缓存，不删除用户其他文件。
