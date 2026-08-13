# 全域论文谱系与缺口

本页是跨领域的长期审计入口，覆盖**搜广推、基础模型、LLM 后训练和 Agent**。单篇实现与指标仍以各论文 README 为准；这里回答“主干是否齐全、下一步缺什么”。

> 2026-08-08 的二级主题复查确认仍有一批真实缺口；此前“P0/P1 已完成”只指一个局部
> 15 篇批次，不能解释为全库无遗漏。完整证据、优先级和拒绝项见
> [全主题系统缺口审计](full-domain-gap-review-20260808.md)。

## 统一收录原则

| 领域 | 进入实现队列的证据门槛 | 默认公共评测 |
| --- | --- | --- |
| 工业搜广推 | 量化线上 A/B 或用户明确认可的全流量证据；经典基线仅作具名例外 | MovieLens / Amazon / KuaiRand，全库排序 |
| 基础模型 | 公开 benchmark、同预算对照，核心算子可真实训练 | WikiText-2、Tiny Shakespeare、多模态/效率任务 suite |
| LLM 后训练 | 明确可执行的 preference/RL objective 与公开评测 | GSM8K candidate、偏好对、过程 trace |
| Agent | 可审计的规划、工具、记忆或反思轨迹 | 确定性工具与跨 episode mini-suite |

## 搜广推：从经典精排到生成式推荐

```mermaid
flowchart LR
  W["Wide & Deep"] --> F["特征交互<br/>DeepFM / DCN-V2"]
  W --> I["兴趣建模<br/>DIN / DIEN"]
  F --> M["多任务与现代排序<br/>ESMM / MMoE / PLE"]
  I --> S["序列建模<br/>BST / SASRec"]
  M --> H["长序列与大规模排序<br/>HSTU / RankMixer / HyFormer"]
  S --> H
  H --> G["TIGER / OneRec / CQ-SID"]
  G --> R["RL / value-aware generation"]
```

当前主干已经覆盖经典特征交互、序列兴趣、长序列排序、双塔召回、Semantic ID 生成、
LLM 内容/知识增强、采样蒸馏、RL、长期价值和 serving；主题索引进一步拆成召回、
粗排/精排、重排与混排、内容理解、审核风控及广告商业决策。

| 已补齐的经典例外 | 价值 | 当前状态 |
| --- | --- | --- |
| DeepFM | FM 与 deep 共享 embedding 的常用 CTR 基线 | 已按用户批准的经典例外实现 |
| YouTube DNN | 两阶段工业召回代表 | 已按用户批准的经典例外实现召回与 sampled-softmax 路径 |
| ESMM / MMoE / PLE | 多任务 CVR 与 shared-bottom 演进主线 | 已建立公开多任务协议并分别实现 |

RecoChain / DIG（2026）仍未核验到满足工业论文硬门槛的量化线上 A/B，因此不创建占位 adapter。
2026-08-08 复查发现的 GloRank、Dual-Rerank、OneRanker、RADAR、DualGR、MPFormer、
HAP、OnePiece、IntSR、CDM 和 CWM 均已实现；2026-08-13 又补齐 Netflix GenRec，
并保留了原有京东同名 GenRec。

## 基础模型：架构、预训练、多模态与效率

```mermaid
flowchart LR
  T["Dense Transformer"] --> M["Switch Transformer MoE"]
  T --> S["Sparse / Switch Attention"]
  T --> A["Mamba selective SSM"]
  T --> E["Engram / Memory Grafting"]
  T --> P["RoPE / long context / MTP"]
```

当前覆盖 dense 基线、稀疏 MoE、Mamba、动态/稀疏注意力、条件记忆、长上下文位置编码、MTP、
量化、RoPE/ALiBi、GQA、Hymba、MoBA、DoReMi/数据配比、BLT 和多模态经典锚点；
可训练算子已进入 LLM/VLM evolve 搜索空间。

独立浏览入口、分类和评测口径见[基础模型研究](foundation-models/README.md)。

- RoPE / ALiBi：已有独立同预算长上下文 adapter 和 evolve 算子。
- Chinchilla scaling：需多 compute/data 预算曲线，不适合用单次小模型实验代替。
- 新 MoE routing 与线性序列模型：只有真实算子、梯度和公开 benchmark 都可验证时进入。

## LLM 后训练

经典链路已覆盖 PPO-RLHF、Constitutional AI、RRHF、RAFT、DPO、KTO、ORPO、IPO、
SimPO、GRPO、RLOO、ReMax，以及 DAPO、GSPO、LUSPO、CoBA-RL、Lightning OPD、
Relay-OPD、GPRL、TCR、CoRT。四个 sequence objective 进入
真实 tokenizer 自由生成与多 seed 路径；P1 又补齐 SLiC-HF、SteerLM 和 SPIN 的
序列校准、多属性条件 SFT 与自博弈。方法差异见[后训练谱系](post-training/lineage.md)。

后训练论文检索、可审计 objective 映射和组合式 genome 已进入统一多轮控制器。下一步是扩大
公开 rollout 规模，并继续统一 reward、KL、长度偏差和 group normalization 的报告口径。

## Agent

经典链路已覆盖 ReAct、MRKL、HuggingGPT、Toolformer、Tree of Thoughts、Reflexion、
Self-Refine、LATS、ReWOO、AutoGen、WebGPT、SayCan、PAL、ART、Generative Agents、MemGPT、MetaGPT、CRITIC、
SWE-agent、OpenHands、Agent Lightning、SEED、CAST、TurnOPD、Voyager、HiSkill、
UniMem，以及近期记忆与规划方法；软件 Agent
已有真实文件编辑和回归测试路径。完整谱系见
[Agent 谱系](agent-research/lineage.md)。

memory、planner、tool policy 和 critic 已成为可组合 genome，并在同一任务套件比较成功率、
token/tool 成本、跨 episode 复用与错误恢复。后续仍需增加真实浏览器/代码环境 benchmark，
并区分算法收益和更强 foundation model 的收益。

## 已完成批次与新优先级

1. **既有 P0 批次已完成**：Wide & Deep、DCN-V2、DIEN、BST、CS3、CQ-SID、Switch Transformer、Mamba、Switch Attention；这不代表新审计发现的 P0 已实现。
2. **P1 基础设施已完成**：新 LLM 架构、后训练和 Agent 的论文约束 genome 已接入统一多轮控制器。
3. **P1 经典论文已完成**：DeepFM、YouTube DNN、ESMM、MMoE、PLE 已按用户批准的经典例外实现。
4. **2026-08-08 P0/P1 队列已闭环**：结果和边界见[全主题系统缺口审计](full-domain-gap-review-20260808.md)；新候选不能继续沿用该日的旧队列。

## 当前真实遗留项（2026-08-13）

| 优先级 | 遗留项 | 当前边界 |
| --- | --- | --- |
| 持续门禁 | 新论文召回的稳定性 | 已改为每日多查询分页候选 artifact + 全文复核；仍需人工确认 affiliation 和线上证据，不是未实现 P0 |
| P1 | 基础模型 test-time compute / verifier / 动态 reasoning budget | 需同时报告正确率、token、延迟与调用成本 |
| P1 | 后训练扩大到可下载 pretrained causal LM | 还需真实 teacher、UltraFeedback、batch rollout、混合精度与断点续训 |
| P1 | Agent Lightning 连接可训练 LLM policy | 现有 transition/credit 机制已实现，但 executor 仍不是统一多轮 LLM policy |
| 等待公开证据 | 安全/风控、私有广告日志、RecoChain / DIG 等 | 不用占位 adapter 伪装实现 |
| 用户已延后 | 官方 SWE-bench Lite、ToolHop 和真实浏览器环境 | 依赖外部 sandbox/凭据/长时运行，暂不冒充已接入 |
