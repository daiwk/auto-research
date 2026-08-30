# 2026-08-29 四领域增量扫描

本轮从上一水位线向前重叠一天，覆盖推荐与 LLM 应用、基础模型/多模态、LLM 后训练和
Agent。自动任务的 arXiv API 一度返回 429，因此复用最近一次成功的 GitHub Actions
候选 artifact，并对 8 月 28 日公告、Google 和 Meta 机构词做定向补查。**本增量没有
新的 Google / Meta 论文通过范围与证据门槛**；机构优先级没有被下调。

## 已实现的九篇 P0

| 领域 | 论文 | 核心机制 | 本地公开实验 |
|---|---|---|---|
| 工业推荐 | [VK Friend-GNN](reproductions/2608.27413-friend-gnn/README.md) | 多哈希共享 embedding、时序邻接与 cutoff | MovieLens-1M 全候选排序；Hit@10 0.0656→0.2281，不能外推为 VK 收益 |
| 后训练 | [TTPO](post-training/2608.27448-ttpo/README.md) | 多数票路由的 OPSD + grouped RL | arithmetic mini-suite 0.1953→0.6328 |
| 后训练 | [Weak-Model Guidance](post-training/2608.27420-weak-guide-rlvr/README.md) | 弱模型前缀探索与混合 RLVR | 0.1953→0.6797 |
| 后训练 | [Uncertainty-Calibrated MOPD](post-training/2608.26735-uc-mopd/README.md) | 双温轨迹、正优势密度和 CLL 门控 | 0.1953→0.1953；负结果保留 |
| 后训练 | [SPEAR](post-training/2608.26550-spear/README.md) | 符号 milestone 与 LCS-F1 过程奖励 | 0.1953→0.2812 |
| Agent | [SWE-Prime](agent-research/2608.27449-swe-prime/README.md) | 轨迹/语义段两级筛选与 loss mask | ToolRoute L2.1 三 seed，joint success 0.7708 |
| Agent | [HarnessLens](agent-research/2608.27311-harnesslens/README.md) | 行为相关任务选择和可归因验证 | joint success 0.8194 |
| Agent | [CoVeMem](agent-research/2608.26895-covemem/README.md) | 协同向量记忆和候选相关读取 | joint success 0.7708 |
| Agent | [SPT](agent-research/2608.26563-spt/README.md) | 多文件 SkillCorpus 与 Reference Insert | joint success 0.8056 |

Agent 数字来自无 guide/oracle 的 ToolRoute L2.1 隔离协议，不是早期会饱和到 1.0 的
确定性 smoke test。后训练 mini-suite 用于验证更新目标和训练动态，不等同论文的大模型
benchmark。

## P1 checkpoint 复现

- [PACE（2608.27206）](reproductions/2608.27206-pace-vlm/README.md)：已实现 APC/DDAE、真实 Qwen2.5-VL + RealWorldQA 路径、Evolve operator，并在 A30 记录质量、token、延迟和显存。
- [TwinKV（2608.27128）](reproductions/2608.27128-twinkv/README.md)：已实现 fixed-budget repair、真实 Qwen3 KV + WikiText-2 长上下文路径、Evolve operator，并在 A30 记录等预算 reconstruction、延迟与显存。

两项均明确保留 checkpoint smoke 与论文完整 benchmark 的边界，不再处于 deferred 队列。

## 全文复核后未进入 P0/P1

- 2608.27006、2608.26579、2608.25381 等推荐候选没有量化生产 A/B 或用户认可的
  全流量证据，因此不进入工业实现队列。
- 本轮其他高召回结果以 benchmark、综述、安全审计或垂直应用为主，不满足“重要新算法
  且存在可信公开复现路径”的 P0 定义。

所有终态写入 [`paper-discovery-ledger.json`](paper-discovery-ledger.json)。下一次扫描从
**2026-08-28** 水位线继续，并保留一天重叠去重，避免 arXiv 公告日与 UTC published
时间错位。

## Evolve 与运行边界

TTPO、Weak-Guide、UC-MOPD、SPEAR 已映射到后训练 genome；SWE-Prime、HarnessLens、
CoVeMem、SPT 已映射到 Agent genome。Friend-GNN 是好友图排序结构，当前 RankMixer
genome 没有同构图槽位，故只保留 adapter，不强行拼接。

这九项新增路径均为 CPU 可运行核心机制，没有新增“必须 CUDA”能力，因此不触发 A100/A30
验证门槛；未来若加入真实 checkpoint CUDA 训练，会按仓库 GPU receipt 合同在 A100/A30
执行后再提交。
