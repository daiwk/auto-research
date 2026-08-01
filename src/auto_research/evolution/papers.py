from __future__ import annotations

from ..models import Paper
from ..papers import ArxivClient
from .models import PaperInspiration


INSTALLED_MUTATIONS = {
    "2507.15551": ("rankmixer_smoe", "RankMixer per-token FFN 与 dense-training/sparse-serving ReLU MoE"),
    "2602.06563": ("tokenmixer_large", "Mixing-Reverting、per-token SwiGLU、interval residual 与辅助头"),
    "2601.21285": ("zenith", "Prime Token Fusion 与 tokenwise SwiGLU Token Boost"),
    "2108.07505": ("moi_mixer", "显式一阶与二阶 Multi-Order Interaction channel mixing"),
    "2505.04421": ("longer", "LONGER 的分块 token merge、全局兴趣与 recent token 保留"),
    "2604.00590": ("unimixer", "UniMixer 的可学习参数化 token mixing，解除固定 head-token 对齐"),
    "2607.17017": ("rankmixer_whale", "WHALE 的 Wukong 乘性交互、门控 HSTU 与逐层信息交换"),
    "2607.13398": ("rankmixer_tmallgs", "TMallGS 的 field-wise QKV、噪声门控与 progressive supervision"),
    "2607.14331": ("rankmixer_long_history", "异步长历史编码、固定缓存状态与轻量在线近期序列融合"),
    "2607.17473": ("rankmixer_ramp", "RAMP 的个性化/公共双路径、特征可用性 masking 与 prediction alignment"),
}

LLM_MUTATIONS = {
    "2204.02311": ("parallel_block", "PaLM 的 parallel attention/FFN block 与 SwiGLU 路径"),
    "2302.13971": ("llama_modern", "LLaMA 风格 RMSNorm、RoPE、SwiGLU 与 pre-normalization"),
    "2305.13245": ("gqa", "Grouped-Query Attention：多 query heads 共享更少的 key/value heads"),
    "2305.10429": ("data_mixture", "DoReMi 的数据域混合与动态配比思想，本地使用可审计的固定/课程配比"),
    "2310.05914": ("neftune", "NEFTune 在 instruction tuning 时向 embedding 注入缩放均匀噪声"),
    "2401.02385": ("small_llm", "TinyLlama 展示 LLaMA 架构的小模型预训练与 staged data mixture"),
    "2512.24880": ("mhc", "mHC 的多 residual streams、动态映射与 Sinkhorn 双随机流形约束"),
    "2607.18413": ("qkv_depthwise_conv", "在 Q/K/V 投影后加入 k=3 residual depthwise Conv1D，补充短程局部归纳偏置"),
    "2607.20083": ("dynamic_rubric", "按回答集合动态生成 rubric 权重，并以区分性和 anchor 约束协同更新策略"),
    "2607.19313": ("off_context_grpo", "用特权解题信息提高有效 rollout，再以 importance ratio 校正无提示目标策略"),
    "2607.21405": ("mobius_rope", "将 25% attention heads 替换为 anti-periodic Möbius RoPE 频率梯度"),
    "2607.21000": ("naju", "独立 retain/write gates 的 native-discrete selective state-space sequence mixer"),
    "2607.21291": ("adadsf", "按层输入/输出相似度分配 token budget，以轻量 Top-K router 执行动态深度稀疏"),
    "2601.07372": ("engram", "确定性 hashed n-gram O(1) 条件记忆查表，并以门控注入早期层"),
    "2607.15456": ("looped_latent_attention", "跨循环共享低维 K/V latent，并按 loop 重建注意力缓存"),
    "2607.20757": ("gaugequant", "训练中学习等价正交基，以 LogSumExp outlier 目标执行 W4A4 fake quantization"),
    "2607.25915": ("penelope", "只在选定 decoder 区间执行带时间门控的 latent recurrence，避免完整 decoder 重跑"),
    "2101.03961": ("switch_transformer", "top-1 sparse expert routing 与 auxiliary load balancing"),
    "2312.00752": ("mamba", "输入依赖 selective state-space scan 与线性序列复杂度"),
    "2603.26380": ("switch_attention", "逐 token、逐层在 full attention 与 sliding-window attention 间动态路由"),
    "2502.11089": ("native_sparse_attention", "NSA 的压缩、选择与滑窗三分支可训练稀疏注意力"),
    "2505.06708": ("gated_attention", "在每个 attention head 的 SDPA 输出后加入 query-dependent sigmoid gate"),
    "2502.16982": ("optimizer:muon", "Muon 对隐藏矩阵梯度做 Newton-Schulz 正交化，其余参数使用 AdamW"),
    "2607.28418": ("wide_dynamic_width", "WIDE 逐 token 选择 attention-head group 与 FFN-channel group，执行可学习动态宽度剪枝"),
    "2607.28627": ("retoken", "单个可学习 retrieval target 在 value-projection 空间打分，并稀疏选择已缓存 token"),
}

POST_TRAINING_MUTATIONS = {
    "2203.02155": ("ppo-rlhf", "PPO-RLHF 的 clipped policy objective、value baseline 与 KL 约束"),
    "2305.18290": ("dpo", "DPO 直接从偏好对优化隐式奖励，无需单独训练 reward model"),
    "2310.10505": ("remax", "ReMax 使用 greedy response baseline 降低 policy-gradient 方差"),
    "2306.13649": ("gkd", "GKD 在学生自身生成轨迹上查询教师，并支持 on/off-policy 混合与可选散度"),
    "2306.08543": ("minillm", "MiniLLM 以 reverse KL、teacher-mixed sampling 和方差缩减蒸馏生成模型"),
    "2601.18734": ("opsd", "OPSD 让同一模型以普通/特权上下文分别作为学生和教师，并裁剪逐 token 散度"),
    "2607.28582": ("beta-opsd", "β-OPSD 把 reference 与 privileged teacher 的几何插值闭式解转成低方差蒸馏目标，并加入 return-to-go credit"),
    "2607.28590": ("vad", "比较同一教师有/无视觉证据的分布，以单侧投影重建 student-anchored 多模态 OPD 目标"),
    "2602.12275": ("opcd", "OPCD 在学生轨迹上以 reverse KL 内化教师上下文中的经验与系统行为"),
    "2607.28022": ("flux-opd", "Flux-OPD 以 context-free teacher 为锚，注入演化上下文的差分信号并按教师冲突自适应降权"),
    "2402.01306": ("kto", "KTO 使用前景理论式效用优化单条 desirable/undesirable 反馈"),
    "2402.03300": ("grpo", "GRPO 用组内相对奖励替代 learned critic"),
    "2607.26862": ("reco-grpo", "ReCo 以响应期望出现次数与 token Bernoulli 方差重加权 GRPO，抑制分布集中"),
    "2402.14740": ("rloo", "RLOO 以 leave-one-out 组均值作为无偏 baseline"),
    "2403.07691": ("orpo", "ORPO 将 SFT 与 odds-ratio preference penalty 合并为单阶段目标"),
    "2503.14476": ("dapo", "DAPO 加入动态采样、token-level loss 与非对称 clipping"),
    "2507.18071": ("gspo", "GSPO 用 sequence-level importance ratio 稳定大模型 RL"),
    "2604.13010": ("lightning-opd", "Lightning OPD 缓存离线教师分布以减少在线 rollout 成本"),
    "2605.18721": ("gprl", "GPRL 联合多维偏好并监控 reward drift"),
    "2607.19824": ("tcr", "TCR 用 thinking checklist reward 与 EMA residual 做过程信用分配"),
    "2607.14777": ("critic:seed", "从 on-policy 轨迹抽取 hindsight skill，并用 skill 引起的 token 概率变化形成稠密 OPD 信号"),
    "2607.26057": ("relay-opd", "检测失败前缀后让教师短暂接管，再把轨迹交还学生继续生成"),
    "2607.25308": ("critic:cast", "用 game solver 相邻状态价值差形成 turn-level advantage，并与稀疏 outcome reward 联合"),
    "2607.05804": ("planner:turn-opd", "按 probe 统计分配 rollout 深度，并逐步转向 turn-normalized KL"),
    "2607.25659": ("cort", "比较 rubric 与 criteria-free 重放的 token likelihood，重分配 GRPO response advantage"),
    "web-tis-2025": ("tis", "TIS 用训练侧与 rollout 引擎概率之比校正梯度，并对过大的失配权重做单侧上截断"),
    "2510.18855": ("icepop", "IcePop 对训练侧与 rollout 引擎概率比做双侧 mask，区间外 token 不参与更新"),
    "web-online-icepop-2025": ("online-icepop", "Online IcePop 每个 rollout batch 只更新一次，移除 stale-policy ratio 并保留训推失配 mask"),
    "2310.12036": ("ipo", "IPO 将偏好 log-ratio gap 回归到有限目标，抑制确定性偏好过拟合"),
    "2405.14734": ("simpo", "SimPO 使用 reference-free、长度归一化的 sequence preference margin"),
    "2602.05261": ("luspo", "LUSPO 校正 sequence policy objective 的响应长度偏差"),
    "2606.22317": ("coba-rl", "边界感知 Curriculum RL 定位 pass@k 能力边界并在边界附近训练"),
    "2212.08073": ("constitutional-ai", "Constitutional AI 先自我批评/修订，再以 AI 偏好执行 RLAIF"),
    "2304.05302": ("rrhf", "RRHF 让响应 log-probability 排序对齐 reward 排序，并保留 best-response SFT"),
    "2304.06767": ("raft", "RAFT 从当前策略采样多个响应、按 reward 选优，再迭代监督微调"),
    "2305.10425": ("slic-hf", "SLiC-HF 用带 margin 的序列概率校准偏好顺序，并以 SFT target 交叉熵防止漂移"),
    "2310.05344": ("steerlm", "SteerLM 将多维质量属性显式标注并作为条件执行可控 SFT"),
    "2401.01335": ("spin", "SPIN 让当前策略区分人类示范与上一轮策略自生成响应，逐轮刷新对手"),
}

AGENT_MUTATIONS = {
    "2210.03629": ("planner:react", "ReAct 交替生成推理轨迹与工具动作"),
    "2302.04761": ("tool:toolformer", "Toolformer 通过自监督 API 调用标注学习何时调用工具"),
    "2303.11366": ("critic:reflexion", "Reflexion 将执行反馈写成语言反思并用于下一 episode"),
    "2303.17651": ("critic:self-refine", "Self-Refine 以生成、反馈、修订循环改进输出"),
    "2305.10601": ("planner:tree-of-thoughts", "Tree of Thoughts 显式搜索并评估多条推理分支"),
    "2305.18323": ("planner:rewoo", "ReWOO 先规划工具依赖，再批量执行与汇总证据"),
    "2310.04406": ("planner:lats", "LATS 将语言模型推理与蒙特卡洛树搜索、反思结合"),
    "2507.21428": ("tool:memtool", "MemTool 动态选择记忆工具和上下文写入策略"),
    "2510.04851": ("memory:legomem", "LEGOMem 将过程记忆拆成可组合、可复用的模块"),
    "2602.22406": ("memory:u-mem", "U-Mem 主动判断知识缺口并获取、压缩长期记忆"),
    "2607.14777": ("critic:seed", "SEED 从轨迹抽取 hindsight skill，并把概率变化作为稠密 on-policy credit"),
    "2607.25308": ("critic:cast", "CAST 用 solver 状态价值差为每个交互 turn 分配信用"),
    "2607.27973": ("critic:tapo", "TAPO 交替执行策略优化与 action-conditioned next-observation transition supervision"),
    "2607.28076": ("critic:grsd", "GRSD 对照同组成功/失败轨迹反思，由 stop-gradient self-teacher 形成能力匹配的 turn-level guidance"),
    "2607.28609": ("critic:os-shepherd", "按 success/fail 双类召回、balanced accuracy 与 leniency 检查评估电脑操作轨迹"),
    "2505.10978": ("critic:gigpo", "GiGPO 联合完整轨迹组的 macro advantage 与共享状态 step group 的 micro advantage"),
    "2604.18401": ("critic:steppo", "StepPO 以环境 step 为 MDP 单位执行 GAE，并聚合 step 内 token ratio 后裁剪"),
    "2607.05804": ("planner:turn-opd", "TurnOPD 联合控制 rollout 深度与 turn-normalized 蒸馏权重"),
    "2607.25853": ("memory:hiskill", "HiSkill 用分层 skill graph 连接高层经验与可执行 AtomicOp"),
    "2607.26017": ("memory:unimem", "UniMem 在 episodic retrieval 与可扩展 parametric memory 之间自路由和巩固"),
    "2308.00352": ("planner:metagpt", "MetaGPT 以标准作业流程组织产品、架构、工程与 QA 角色产物"),
    "2305.11738": ("critic:critic", "CRITIC 用外部工具执行结果验证并据反馈修订输出"),
    "2508.03680": ("critic:agent-lightning", "Agent Lightning 将运行轨迹与 RL 训练解耦并做分层信用分配"),
    "2405.15793": ("planner:swe-agent", "SWE-agent 使用面向代码仓库的 Agent-Computer Interface 定位、编辑和测试"),
    "2407.16741": ("planner:openhands", "OpenHands 以事件流统一编辑器、终端和浏览器动作"),
    "2205.00445": ("tool:mrkl", "MRKL 用 router 将请求分发给神经或离散符号专家"),
    "2303.17580": ("planner:hugginggpt", "HuggingGPT 规划子任务、按能力描述选模型、依赖执行并汇总"),
    "2304.03442": ("memory:generative-agents", "Generative Agents 以相关性、近期性、重要性检索记忆并形成反思"),
    "2310.08560": ("memory:memgpt", "MemGPT 以 core/working/archival 分层和 interrupt 管理虚拟上下文"),
    "2112.09332": ("tool:webgpt", "WebGPT 在文本浏览器中搜索、导航、收集引用，并用 reward model 做轨迹拒绝采样"),
    "2204.01691": ("planner:saycan", "SayCan 将语言模型给出的技能相关性与 value-function affordance 相乘"),
    "2211.10435": ("tool:pal", "PAL 让语言模型生成可执行程序，并把精确求解交给符号解释器"),
    "2303.09014": ("planner:art", "ART 从任务库检索多步示例，在工具调用处暂停生成并注入执行结果"),
    "2503.09516": ("tool:search-r1", "Search-R1 交错执行推理与检索，屏蔽环境返回 token，并用结果奖励更新策略"),
    "2504.20073": ("critic:ragen", "RAGEN 的 StarPO-S 过滤退化轨迹、引入 critic baseline 和解耦 clipping"),
    "2502.01600": ("critic:loop", "LOOP 以 leave-one-out baseline、离策略轨迹复用与逐 token clipping 训练长程交互 Agent"),
    "2505.16421": ("planner:webagent-r1", "WebAgent-R1 用动态上下文压缩、并行 trajectory rollout 和多轮 M-GRPO"),
    "2508.18669": ("tool:mua-rl", "MUA-RL 将模拟用户反馈和真实工具响应纳入只使用最终任务奖励的多轮 RL"),
    "2305.16291": ("memory:voyager", "Voyager 将成功程序沉淀为可检索、可组合的终身技能库"),
    "2308.08155": ("planner:autogen", "AutoGen 以可配置角色对话和代码执行组织多 Agent 协作"),
    "2601.20439": ("planner:pearl", "PEARL 探索多条工具计划，并用执行反馈自适应更新计划策略"),
    "2607.27083": ("tool:cam-df", "CAM-DF 将工具排序转成异构成本下的边际收益停止决策"),
    "2607.26784": ("memory:skillrise", "SkillRise 在相关任务序列中交替求解与维护技能文档，并用下游结果分配整理阶段信用"),
}

FALLBACK_PAPERS = (
    Paper("RankMixer: Scaling Up Ranking Models in Industrial Recommenders", "Parameter-free token mixing and per-token feed-forward networks for industrial ranking.", [], "2025-07-21", "https://arxiv.org/abs/2507.15551", "2507.15551"),
    Paper("TokenMixer-Large: Scaling Up Large Ranking Models in Industrial Recommenders", "Mixing and reverting, interval residuals, auxiliary losses and sparse per-token MoE.", [], "2026-02-06", "https://arxiv.org/abs/2602.06563", "2602.06563"),
    Paper("Zenith: Scaling up Ranking Models for Billion-scale Livestreaming Recommendation", "Prime Tokens, Token Fusion and Token Boost for scalable ranking.", [], "2026-01-29", "https://arxiv.org/abs/2601.21285", "2601.21285"),
    Paper("MOI-Mixer: Improving MLP-Mixer with Multi Order Interactions in Sequential Recommendation", "Explicit multi-order interactions in mixer channel layers.", [], "2021-08-17", "https://arxiv.org/abs/2108.07505", "2108.07505"),
    Paper("LONGER: Scaling Up Long Sequence Modeling in Industrial Recommenders", "Token merge, global tokens and hybrid attention for ultra-long user sequences.", [], "2025-05-07", "https://arxiv.org/abs/2505.04421", "2505.04421"),
    Paper("UniMixer: A Unified Architecture for Scaling Laws in Recommendation Systems", "Learnable parameterized token mixing for heterogeneous feature interaction.", [], "2026-04-01", "https://arxiv.org/abs/2604.00590", "2604.00590"),
    Paper("TMallGS: Scaling Unified Feature and Sequence Modeling for Generative E-commerce Search", "Field-wise QKV, adaptive gates and progressive supervision for heterogeneous search features.", [], "2026-07-15", "https://arxiv.org/abs/2607.13398", "2607.13398"),
    Paper("Long-History User Transformers for Real-Time Ad Ranking", "Asynchronous long-history state caching plus a lightweight online recent-event encoder.", [], "2026-07-15", "https://arxiv.org/abs/2607.14331", "2607.14331"),
    Paper("WHALE: A Scalable Unified Model for Recommendation with Wukong-HSTU Architecture", "Progressively exchanges Wukong feature interactions and gated HSTU sequence states.", [], "2026-07-19", "https://arxiv.org/abs/2607.17017", "2607.17017"),
    Paper("RAMP: Robust Ad Recommendation Under Limited Personalized-Feature Availability via Masking and Alignment Pathways", "Dual personalized/public paths with availability masks and prediction alignment.", [], "2026-07-20", "https://arxiv.org/abs/2607.17473", "2607.17473"),
)

LLM_FALLBACK_PAPERS = (
    Paper("PaLM: Scaling Language Modeling with Pathways", "Parallel Transformer layers and SwiGLU in a decoder-only language model.", [], "2022-04-05", "https://arxiv.org/abs/2204.02311", "2204.02311"),
    Paper("LLaMA: Open and Efficient Foundation Language Models", "Pre-normalization with RMSNorm, SwiGLU and rotary positional embeddings.", [], "2023-02-27", "https://arxiv.org/abs/2302.13971", "2302.13971"),
    Paper("GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints", "Grouped-query attention shares key/value heads for efficient decoding.", [], "2023-05-22", "https://arxiv.org/abs/2305.13245", "2305.13245"),
    Paper("DoReMi: Optimizing Data Mixtures Speeds Up Language Model Pretraining", "Optimizes domain weights for language-model pretraining data mixtures.", [], "2023-05-17", "https://arxiv.org/abs/2305.10429", "2305.10429"),
    Paper("NEFTune: Noisy Embeddings Improve Instruction Finetuning", "Adds scaled uniform noise to token embeddings during instruction tuning.", [], "2023-10-09", "https://arxiv.org/abs/2310.05914", "2310.05914"),
    Paper("TinyLlama: An Open-Source Small Language Model", "A compact LLaMA-style model trained with staged data mixtures.", [], "2024-01-04", "https://arxiv.org/abs/2401.02385", "2401.02385"),
    Paper("mHC: Manifold-Constrained Hyper-Connections", "Doubly stochastic residual mixing stabilizes multi-stream Hyper-Connections.", [], "2025-12-31", "https://arxiv.org/abs/2512.24880", "2512.24880"),
    Paper("Convolution for Large Language Models", "A residual depthwise Conv1D after QKV projections adds local token interaction with negligible parameters.", [], "2026-07-20", "https://arxiv.org/abs/2607.18413", "2607.18413"),
    Paper("Off-Context GRPO: Learning to Reason on Hard Problems using Privileged Information", "Samples reward-bearing trajectories with privileged context and corrects back to the original policy.", [], "2026-07-21", "https://arxiv.org/abs/2607.19313", "2607.19313"),
    Paper("Co-Evolving LLM Evaluators and Policies via DynamicRubric", "Response-set conditioned rubrics co-evolve an evaluator and policy under discriminability and anchor objectives.", [], "2026-07-22", "https://arxiv.org/abs/2607.20083", "2607.20083"),
    Paper("Naju: A Native Discrete State-Space Model with Independent Retention and Writing for Long-Sequence Memory", "Native-discrete selective recurrence with independent retain and write gates.", [], "2026-07-23", "https://arxiv.org/abs/2607.21000", "2607.21000"),
    Paper("Anti-Periodic Positional Encoding: Möbius Boundary Conditions Make In-Context Retrieval Reliable", "Anti-periodic frequencies on a subset of attention heads improve retrieval reliability.", [], "2026-07-23", "https://arxiv.org/abs/2607.21405", "2607.21405"),
    Paper("Adaptive Depth Sparse Framework: Similarity-Driven Resource Allocation for Pre-Trained LLMs", "Similarity-calibrated layer budgets and lightweight Top-K token routing preserve dense features under sparse execution.", [], "2026-07-23", "https://arxiv.org/abs/2607.21291", "2607.21291"),
    Paper("Windowed-MTP: Removing the Full-Context Draft-KV Tax at Million-Token Context", "A sink plus recent window bounds the built-in MTP draft KV read while full-context target verification preserves outputs.", [], "2026-07-23", "https://arxiv.org/abs/2607.21535", "2607.21535"),
    Paper("Parameter-free Adaptive Sparse Attention via Compression-Based Content Selection", "Per-block gzip ratios select content-adaptive literal-to-literal long-range attention without learned routing parameters.", [], "2026-07-23", "https://arxiv.org/abs/2607.21752", "2607.21752"),
    Paper("Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models", "O(1) hashed n-gram conditional memory complements compute sparsity.", [], "2026-01-12", "https://arxiv.org/abs/2601.07372", "2601.07372"),
    Paper("Looped Latent Attention: Cross-Loop KV Compression for Looped Transformers", "Shared latent K/V codes compress recurrent Transformer caches.", [], "2026-07-16", "https://arxiv.org/abs/2607.15456", "2607.15456"),
    Paper("GaugeQuant: Online Learning of Quantization-Optimal Bases from LLM Symmetries", "Online orthogonal-basis learning suppresses W4A4 outliers.", [], "2026-07-22", "https://arxiv.org/abs/2607.20757", "2607.20757"),
    Paper("Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity", "Top-1 sparse expert routing with a load-balancing auxiliary objective.", [], "2021-01-11", "https://arxiv.org/abs/2101.03961", "2101.03961"),
    Paper("Mamba: Linear-Time Sequence Modeling with Selective State Spaces", "Input-dependent state-space parameters selectively retain and propagate sequence information.", [], "2023-12-01", "https://arxiv.org/abs/2312.00752", "2312.00752"),
    Paper("Switch Attention: Towards Dynamic and Fine-grained Hybrid Transformers", "Per-token per-layer routing between full and sliding-window attention.", [], "2026-03-27", "https://arxiv.org/abs/2603.26380", "2603.26380"),
    Paper("Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention", "Trainable compressed, selected and sliding-window attention branches for long-context language models.", [], "2025-02-16", "https://arxiv.org/abs/2502.11089", "2502.11089"),
    Paper("Gated Attention for Large Language Models: Non-linearity, Sparsity, and Attention-Sink-Free", "A head-specific sigmoid gate after SDPA improves stability and long-context behavior.", [], "2025-05-10", "https://arxiv.org/abs/2505.06708", "2505.06708"),
    Paper("Muon is Scalable for LLM Training", "Orthogonalized matrix updates plus AdamW for the remaining parameters improve training efficiency.", [], "2025-02-24", "https://arxiv.org/abs/2502.16982", "2502.16982"),
)

POST_TRAINING_FALLBACK_PAPERS = (
    Paper("Training language models to follow instructions with human feedback", "PPO-based RLHF with a learned reward model.", [], "2022-03-04", "https://arxiv.org/abs/2203.02155", "2203.02155"),
    Paper("Direct Preference Optimization: Your Language Model is Secretly a Reward Model", "A closed-form preference objective without an explicit reward model.", [], "2023-05-29", "https://arxiv.org/abs/2305.18290", "2305.18290"),
    Paper("ReMax: A Simple, Effective, and Efficient Reinforcement Learning Method for Aligning Large Language Models", "A greedy-response baseline for low-variance policy gradients.", [], "2023-10-16", "https://arxiv.org/abs/2310.10505", "2310.10505"),
    Paper("On-Policy Distillation of Language Models: Learning from Self-Generated Mistakes", "Generalized Knowledge Distillation trains on student-generated sequences with teacher token feedback.", [], "2023-06-23", "https://arxiv.org/abs/2306.13649", "2306.13649"),
    Paper("MiniLLM: Knowledge Distillation of Large Language Models", "Reverse-KL distillation with teacher-mixed sampling and variance reduction.", [], "2023-06-14", "https://arxiv.org/abs/2306.08543", "2306.08543"),
    Paper("Self-Distilled Reasoner: On-Policy Self-Distillation for Large Language Models", "A shared model teaches its context-free view from a privileged-solution view on student trajectories.", [], "2026-01-26", "https://arxiv.org/abs/2601.18734", "2601.18734"),
    Paper("On-Policy Context Distillation for Language Models", "Reverse-KL context distillation internalizes transient experience and system prompts on student trajectories.", [], "2026-02-12", "https://arxiv.org/abs/2602.12275", "2602.12275"),
    Paper("KTO: Model Alignment as Prospect Theoretic Optimization", "Alignment from unpaired desirable and undesirable feedback.", [], "2024-02-02", "https://arxiv.org/abs/2402.01306", "2402.01306"),
    Paper("DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models", "Introduces Group Relative Policy Optimization.", [], "2024-02-05", "https://arxiv.org/abs/2402.03300", "2402.03300"),
    Paper("ReCo: Reweighting GRPO Against Distributional Concentration", "Expected-occurrence response weights and token variance ratios preserve rollout diversity.", [], "2026-07-29", "https://arxiv.org/abs/2607.26862", "2607.26862"),
    Paper("Back to Basics: Revisiting REINFORCE Style Optimization for Learning from Human Feedback in LLMs", "RLOO uses leave-one-out baselines for efficient online RLHF.", [], "2024-02-22", "https://arxiv.org/abs/2402.14740", "2402.14740"),
    Paper("ORPO: Monolithic Preference Optimization without Reference Model", "Combines supervised learning and odds-ratio preference optimization.", [], "2024-03-12", "https://arxiv.org/abs/2403.07691", "2403.07691"),
    Paper("DAPO: An Open-Source LLM Reinforcement Learning System at Scale", "Dynamic sampling and token-level policy optimization for reasoning.", [], "2025-03-18", "https://arxiv.org/abs/2503.14476", "2503.14476"),
    Paper("Group Sequence Policy Optimization", "Sequence-level importance ratios stabilize group policy optimization.", [], "2025-07-24", "https://arxiv.org/abs/2507.18071", "2507.18071"),
    Paper("Lightning OPD", "Offline teacher-distribution caching for efficient policy distillation.", [], "2026-04-17", "https://arxiv.org/abs/2604.13010", "2604.13010"),
    Paper("GPRL", "Multi-dimensional preference optimization with reward-drift monitoring.", [], "2026-05-25", "https://arxiv.org/abs/2605.18721", "2605.18721"),
    Paper("TCR", "Checklist rewards and EMA residuals for process-level credit assignment.", [], "2026-07-23", "https://arxiv.org/abs/2607.19824", "2607.19824"),
    Paper("A General Theoretical Paradigm to Understand Learning from Human Preferences", "Introduces Identity Preference Optimization with a finite log-ratio target.", [], "2023-10-18", "https://arxiv.org/abs/2310.12036", "2310.12036"),
    Paper("SimPO: Simple Preference Optimization with a Reference-Free Reward", "Length-normalized reference-free preference optimization.", [], "2024-05-23", "https://arxiv.org/abs/2405.14734", "2405.14734"),
    Paper("Length-Unbiased Sequence Policy Optimization", "Corrects response-length bias in sequence policy optimization.", [], "2026-02-05", "https://arxiv.org/abs/2602.05261", "2602.05261"),
    Paper("Curriculum Reinforcement Learning Can Incentivize Reasoning Capacity in LLMs Beyond the Base Model", "Locates the pass@k capability boundary and trains near it with targeted guidance.", [], "2026-06-21", "https://arxiv.org/abs/2606.22317", "2606.22317"),
    Paper("Constitutional AI: Harmlessness from AI Feedback", "Self-critique and revision followed by reinforcement learning from AI preferences.", [], "2022-12-15", "https://arxiv.org/abs/2212.08073", "2212.08073"),
    Paper("RRHF: Rank Responses to Align Language Models with Human Feedback without tears", "Aligns response likelihood ordering with reward ordering and fine-tunes the best response.", [], "2023-04-11", "https://arxiv.org/abs/2304.05302", "2304.05302"),
    Paper("RAFT: Reward rAnked FineTuning for Generative Foundation Model Alignment", "Samples responses, keeps reward-ranked winners, and iteratively fine-tunes on them.", [], "2023-04-13", "https://arxiv.org/abs/2304.06767", "2304.06767"),
    Paper("SLiC-HF: Sequence Likelihood Calibration with Human Feedback", "Calibrates preferred and rejected sequence likelihoods with a margin plus SFT regularization.", [], "2023-05-17", "https://arxiv.org/abs/2305.10425", "2305.10425"),
    Paper("SteerLM: Attribute Conditioned SFT as an (User-Steerable) Alternative to RLHF", "Annotates responses along multiple quality axes and conditions SFT and inference on requested attributes.", [], "2023-10-09", "https://arxiv.org/abs/2310.05344", "2310.05344"),
    Paper("Self-Play Fine-Tuning Converts Weak Language Models to Strong Language Models", "Uses previous-policy generations as self-play negatives against human demonstrations.", [], "2024-01-02", "https://arxiv.org/abs/2401.01335", "2401.01335"),
    Paper("Your Efficient RL Framework Secretly Brings You Off-Policy RL Training", "Truncated importance sampling corrects training-inference mismatch with a one-sided capped ratio.", [], "2025-08-05", "https://fengyao.notion.site/off-policy-rl", "web-tis-2025"),
    Paper("Every Step Evolves: Scaling Reinforcement Learning for Trillion-Scale Thinking Model", "IcePop masks both tails of the token-level training-inference ratio for stable MoE RL.", [], "2025-10-21", "https://arxiv.org/abs/2510.18855", "2510.18855"),
    Paper("Stabilizing MoE RL Without Router Replay: The Online IcePop Solution", "Pure-online IcePop removes policy staleness by applying one update per rollout batch.", [], "2025-12-16", "https://zhuanlan.zhihu.com/p/1984379979035850499", "web-online-icepop-2025"),
)

AGENT_FALLBACK_PAPERS = (
    Paper("ReAct: Synergizing Reasoning and Acting in Language Models", "Interleaves reasoning traces and environment actions.", [], "2022-10-06", "https://arxiv.org/abs/2210.03629", "2210.03629"),
    Paper("Toolformer: Language Models Can Teach Themselves to Use Tools", "Self-supervised learning of API calls.", [], "2023-02-09", "https://arxiv.org/abs/2302.04761", "2302.04761"),
    Paper("Reflexion: Language Agents with Verbal Reinforcement Learning", "Stores verbal reflections from execution feedback.", [], "2023-03-20", "https://arxiv.org/abs/2303.11366", "2303.11366"),
    Paper("Self-Refine: Iterative Refinement with Self-Feedback", "Iterative generation, critique, and refinement.", [], "2023-03-30", "https://arxiv.org/abs/2303.17651", "2303.17651"),
    Paper("Tree of Thoughts: Deliberate Problem Solving with Large Language Models", "Searches over evaluated reasoning branches.", [], "2023-05-17", "https://arxiv.org/abs/2305.10601", "2305.10601"),
    Paper("ReWOO: Decoupling Reasoning from Observations for Efficient Augmented Language Models", "Plans tool dependencies before execution.", [], "2023-05-29", "https://arxiv.org/abs/2305.18323", "2305.18323"),
    Paper("Language Agent Tree Search Unifies Reasoning, Acting, and Planning in Language Models", "Combines tree search, environment feedback, and reflection.", [], "2023-10-06", "https://arxiv.org/abs/2310.04406", "2310.04406"),
    Paper("MemTool", "Dynamically selects memory tools and context writes.", [], "2025-07-29", "https://arxiv.org/abs/2507.21428", "2507.21428"),
    Paper("LEGOMem", "Composable process-memory modules for agents.", [], "2025-10-06", "https://arxiv.org/abs/2510.04851", "2510.04851"),
    Paper("U-Mem", "Active knowledge acquisition and compressed long-term agent memory.", [], "2026-02-26", "https://arxiv.org/abs/2602.22406", "2602.22406"),
    Paper("MetaGPT: Meta Programming for Multi-Agent Collaborative Framework", "SOP-driven product, architecture, engineering, and QA agent collaboration.", [], "2023-08-01", "https://arxiv.org/abs/2308.00352", "2308.00352"),
    Paper("CRITIC: Large Language Models Can Self-Correct with Tool-Interactive Critiquing", "Uses external tools to verify and iteratively repair model outputs.", [], "2023-05-19", "https://arxiv.org/abs/2305.11738", "2305.11738"),
    Paper("Agent Lightning: Train ANY AI Agents with Reinforcement Learning", "Disaggregates agent execution and training with hierarchical credit assignment.", [], "2025-08-05", "https://arxiv.org/abs/2508.03680", "2508.03680"),
    Paper("SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering", "A repository-oriented interface for localization, editing, and executable testing.", [], "2024-05-06", "https://arxiv.org/abs/2405.15793", "2405.15793"),
    Paper("OpenHands: An Open Platform for AI Software Developers as Generalist Agents", "An event-stream platform combining editor, terminal, and browser actions.", [], "2024-07-23", "https://arxiv.org/abs/2407.16741", "2407.16741"),
    Paper("MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning", "Routes requests to neural and symbolic expert modules.", [], "2022-05-01", "https://arxiv.org/abs/2205.00445", "2205.00445"),
    Paper("HuggingGPT: Solving AI Tasks with ChatGPT and its Friends in Hugging Face", "Uses an LLM controller to plan, select expert models, execute dependencies, and summarize.", [], "2023-03-30", "https://arxiv.org/abs/2303.17580", "2303.17580"),
    Paper("Generative Agents: Interactive Simulacra of Human Behavior", "Combines a scored memory stream, reflection, and planning for persistent agents.", [], "2023-04-07", "https://arxiv.org/abs/2304.03442", "2304.03442"),
    Paper("MemGPT: Towards LLMs as Operating Systems", "Manages virtual context through working and archival memory tiers plus interrupts.", [], "2023-10-12", "https://arxiv.org/abs/2310.08560", "2310.08560"),
    Paper("WebGPT: Browser-assisted question-answering with human feedback", "Browses, collects references, and uses a learned reward model for rejection sampling.", [], "2021-12-17", "https://arxiv.org/abs/2112.09332", "2112.09332"),
    Paper("Do As I Can, Not As I Say: Grounding Language in Robotic Affordances", "Multiplies language-model skill relevance by value-function affordance.", [], "2022-04-04", "https://arxiv.org/abs/2204.01691", "2204.01691"),
    Paper("PAL: Program-aided Language Models", "Generates executable reasoning programs and delegates exact computation to an interpreter.", [], "2022-11-18", "https://arxiv.org/abs/2211.10435", "2211.10435"),
    Paper("ART: Automatic multi-step reasoning and tool-use for large language models", "Retrieves task-library demonstrations and pauses generation around external tool calls.", [], "2023-03-16", "https://arxiv.org/abs/2303.09014", "2303.09014"),
    Paper("Search-R1: Training LLMs to Reason and Leverage Search Engines with Reinforcement Learning", "Interleaves reasoning with search, masks retrieved tokens and optimizes outcome rewards.", [], "2025-03-12", "https://arxiv.org/abs/2503.09516", "2503.09516"),
    Paper("RAGEN: Understanding Self-Evolution in LLM Agents via Multi-Turn Reinforcement Learning", "StarPO-S stabilizes trajectory-level agent RL against the Echo Trap.", [], "2025-04-24", "https://arxiv.org/abs/2504.20073", "2504.20073"),
    Paper("Reinforcement Learning for Long-Horizon Interactive LLM Agents", "LOOP reuses trajectories with leave-one-out advantages and token-level PPO clipping without a value network.", [], "2025-02-03", "https://arxiv.org/abs/2502.01600", "2502.01600"),
    Paper("WebAgent-R1: Training Web Agents via End-to-End Multi-Turn Reinforcement Learning", "Dynamic context compression and parallel M-GRPO trajectories train web agents from binary outcomes.", [], "2025-05-22", "https://arxiv.org/abs/2505.16421", "2505.16421"),
    Paper("MUA-RL: Multi-turn User-interacting Agent Reinforcement Learning for agentic tool use", "Simulated users dynamically refine intent while real tool responses close the end-to-end RL loop.", [], "2025-08-26", "https://arxiv.org/abs/2508.18669", "2508.18669"),
    Paper("Voyager: An Open-Ended Embodied Agent with Large Language Models", "Stores successful executable programs in a lifelong skill library for retrieval and composition.", [], "2023-05-25", "https://arxiv.org/abs/2305.16291", "2305.16291"),
    Paper("AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation", "Configurable conversational roles coordinate reasoning, tool use and code execution.", [], "2023-08-16", "https://arxiv.org/abs/2308.08155", "2308.08155"),
    Paper("PEARL: Plan Exploration and Adaptive Reinforcement Learning for Multihop Tool Use", "Explores alternative tool plans and adapts the policy from execution outcomes.", [], "2026-01-28", "https://arxiv.org/abs/2601.20439", "2601.20439"),
    Paper("Scores Are Not Decisions: Cost-Aware Stopping for Tool Acquisition in LLM Agents", "Regret-weighted marginal stopping chooses a cost-aware prefix from a frozen tool ranking.", [], "2026-07-29", "https://arxiv.org/abs/2607.27083", "2607.27083"),
    Paper("SkillRise: Agentic Reinforcement Learning for Cross-Task Skill Evolution", "Alternates task solving and skill-document curation with discounted downstream credit.", [], "2026-07-29", "https://arxiv.org/abs/2607.26784", "2607.26784"),
)


def discover_papers(query: str, limit: int, allow_network: bool, track: str = "recommendation") -> list[PaperInspiration]:
    tracks = {
        "llm": (LLM_MUTATIONS, LLM_FALLBACK_PAPERS, ("cs.CL", "cs.LG")),
        "post-training": (POST_TRAINING_MUTATIONS, POST_TRAINING_FALLBACK_PAPERS, ("cs.CL", "cs.LG")),
        "agent": (AGENT_MUTATIONS, AGENT_FALLBACK_PAPERS, ("cs.AI", "cs.CL")),
    }
    mutations, fallback, categories = tracks.get(
        track, (INSTALLED_MUTATIONS, FALLBACK_PAPERS, ("cs.IR", "cs.LG"))
    )
    papers: list[Paper] = []
    source = "installed evidence"
    if allow_network:
        try:
            papers = ArxivClient().search(query, limit, categories)
            source = "live arXiv search"
        except Exception:
            papers = []
    by_id = {paper.arxiv_id.split("v")[0]: paper for paper in papers}
    # Installed, reviewed mutations remain available even when broad search misses them.
    for paper in fallback:
        by_id.setdefault(paper.arxiv_id, paper)
    ranked = sorted(by_id.values(), key=lambda paper: (paper.arxiv_id not in mutations, paper.published), reverse=False)
    result = []
    for paper in ranked[: max(limit, len(fallback))]:
        paper_id = paper.arxiv_id.split("v")[0]
        architecture, method = mutations.get(paper_id, (None, "检索到相关论文，但尚无经过测试的安全结构算子映射"))
        result.append(PaperInspiration(paper_id, paper.title, paper.url, paper.published[:10], architecture, method, source if paper_id in {p.arxiv_id.split('v')[0] for p in papers} else "installed evidence"))
    return result
