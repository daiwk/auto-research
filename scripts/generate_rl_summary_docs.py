#!/usr/bin/env python3
"""Generate detail pages for representative missing methods in rl_papers_summary."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FIGURE_START = "<!-- paper-figure:start -->"
FIGURE_END = "<!-- paper-figure:end -->"


PAPERS = (
    {
        "module": "post-training", "slug": "web-2025-tis",
        "title": "TIS：截断重要性采样训推校正", "key": "tis",
        "url": "https://fengyao.notion.site/off-policy-rl",
        "publication_label": "Your Efficient RL Framework Secretly Brings You Off-Policy RL Training",
        "information_heading": "资料信息",
        "summary_heading": "原始资料总结",
        "result_heading": "资料离线与线上效果",
        "scope_note": "本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。",
        "institution": "UC San Diego / Microsoft Research", "date": "2025-08-05",
        "code": "未发布独立算法仓库；资料页列出 OAT、SkyRL、OpenRLHF 后续实现",
        "topic": "训推失配 / 截断重要性采样",
        "summary": "混合训练框架由 rollout 引擎采样、训练引擎重算 log-prob；即使权重相同，数值精度和 kernel 差异也会让行为分布与训练分布偏离。TIS 将训练侧与 rollout 引擎概率比乘入策略梯度，并只对过大的校正权重做单侧上截断，保留小权重样本而控制重尾方差。",
        "mermaid": 'R["rollout-engine probability"] --> W["training / rollout ratio"]\n    T["training-engine probability"] --> W\n    W --> C["one-sided upper truncation"]\n    A["group advantage"] --> U["weighted policy update"]\n    C --> U',
        "formula": r"\rho_t^{\rm TI}=\frac{\pi_{\rm train}(a_t\mid s_t)}{\pi_{\rm rollout}(a_t\mid s_t)},\qquad w_t=\min(\rho_t^{\rm TI},c),\qquad \mathcal L=-\mathbb E[w_t r_t^{\rm policy}A_t].",
        "result": "原始网页在多个 LLM RL 设置中比较 Vanilla IS、PPO-IS 与 TIS，报告截断校正能避免训推概率差异引发的训练崩溃；该资料不是独立论文，也未报告生产线上 A/B。",
        "local": "本地显式维护旧训练策略和带确定性数值/router 扰动的 rollout 引擎分布，以 `c=2` 单侧截断训推 ratio；TIS 不丢弃区间外样本，并继续保留 PPO stale-policy ratio。",
        "boundary": "候选动作分布替代逐 token LLM 概率，确定性引擎扰动替代真实 vLLM/FSDP 数值差异；这里只验证 TIS 权重与梯度路径，不复刻网页中的大模型训练。",
    },
    {
        "module": "post-training", "slug": "2510.18855-icepop", "id": "2510.18855",
        "title": "IcePop：双侧训推失配掩码", "key": "icepop",
        "institution": "Ant Group / Inclusion AI", "date": "2025-10-21",
        "code": "未发现/未发布 IcePop 独立算法源代码",
        "topic": "MoE 训推失配 / 双侧 mask",
        "summary": "MoE router 会放大训练引擎与 rollout 引擎的微小数值差异，单侧 TIS 仍可能保留严重偏小的失配 ratio。IcePop 对训练侧与 rollout 引擎的 token 概率比设置固定双侧区间；区间内保留原始校正权重，区间外 token 的本次策略梯度直接归零。",
        "mermaid": 'R["rollout-engine probability"] --> W["training / rollout ratio"]\n    T["training-engine probability"] --> W\n    W --> M["fixed two-sided mask"]\n    M --> U["in-band weighted policy update"]',
        "formula": r"\rho_t^{\rm TI}=\frac{\pi_{\rm train}(a_t\mid s_t)}{\pi_{\rm rollout}(a_t\mid s_t)},\qquad m_t=\mathbf1[c_{\rm low}\le\rho_t^{\rm TI}\le c_{\rm high}],\qquad \mathcal L=-\mathbb E[m_t\rho_t^{\rm TI}r_t^{\rm policy}A_t].",
        "result": "Ring-1T 技术报告将 IcePop 与 C3PO++、ASystem 共同用于万亿参数 MoE RL，并报告 Ring-1T 在 AIME 2025 等推理基准上的结果；没有隔离 IcePop 的生产线上 A/B。",
        "local": "在与 TIS 相同的候选策略和引擎失配模拟中采用公开实现常用的 `[0.5, 5.0]` 区间，区间外动作真正不产生梯度，同时保留旧 rollout policy 的 PPO ratio/clip。",
        "boundary": "没有真实 MoE expert routing、万亿参数模型或异步集群；本地只隔离复现固定双侧 mask 与原始区间内校正权重。",
    },
    {
        "module": "post-training", "slug": "web-2025-online-icepop",
        "title": "Online IcePop：单次 rollout 更新的纯在线失配掩码",
        "key": "online-icepop",
        "url": "https://zhuanlan.zhihu.com/p/1984379979035850499",
        "publication_label": "Online IcePop 技术说明",
        "information_heading": "资料信息",
        "summary_heading": "原始资料总结",
        "result_heading": "资料离线与线上效果",
        "scope_note": "本页在公开候选策略上复现网页资料中的可隔离 RL 更新机制；不把轻量实验写成来源材料中的大模型效果。",
        "institution": "Jian Hu（技术说明；方法源自 Ant Group Bailing Team）",
        "date": "2025-12-16（作者公开说明页首发）",
        "code": "未发布独立源代码；属于 IcePop 的训练调度变体",
        "topic": "纯在线策略梯度 / 训推失配",
        "summary": "普通 IcePop 同时面对训练/rollout 引擎差异和一次 rollout 被多次更新造成的策略陈旧。Online IcePop 强制每个 rollout batch 只更新一次，使 stale-policy ratio 恒为 1，从目标中移除 PPO ratio 与 clip；训练侧仍用 IcePop 双侧 mask 和区间内原始 ratio 校正引擎失配。",
        "mermaid": 'B["fresh rollout batch"] --> O["exactly one update"]\n    O --> P["policy ratio = 1; no PPO clip"]\n    R["training / rollout-engine ratio"] --> M["IcePop two-sided mask"]\n    P --> U["pure-online update"]\n    M --> U',
        "formula": r"r_t^{\rm policy}=1,\qquad \mathcal L_{\rm online}=-\mathbb E\!\left[\mathbf1[c_{\rm low}\le\rho_t^{\rm TI}\le c_{\rm high}]\,\rho_t^{\rm TI}A_t\right].",
        "result": "原始说明聚焦稳定性设计，主张以 pure-online 单次更新消除 router shift 累积；该资料不是独立论文，没有独立 benchmark 表或生产线上 A/B。",
        "local": "每个训练 step 后立即把当前权重刷新为下一批 rollout 权重，诊断中强制 `policy_staleness_ratio_mean=1`、关闭 PPO clip，同时沿用 IcePop `[0.5, 5.0]` 双侧 mask。",
        "boundary": "本地一个 candidate group 对应一个 rollout batch，不包含真实并行采样和通信；验证的是单次更新调度、stale ratio 消除和训推 mask 的组合语义。",
    },
    {
        "module": "post-training", "slug": "2607.10169-ripo", "id": "2607.10169",
        "title": "RIPO：黎曼等距策略优化", "key": "ripo",
        "institution": "论文作者团队（机构详见原论文）", "date": "2026-07-11",
        "code": "未发现官方代码", "topic": "几何信任域 / 动态 clip",
        "summary": "固定 PPO ratio 区间在低概率区域过于保守、在高概率区域又可能过大。RIPO 以 Fisher–Rao 几何定义策略距离，并按旧策略概率设置等距 clip 半径，使不同概率区域获得更均衡的局部 KL 预算。",
        "mermaid": 'O["old policy probability"] --> R["Fisher–Rao radius"]\n    R --> C["probability-dependent clip"]\n    A["group advantage"] --> C\n    C --> U["policy update"]',
        "formula": r"r_t=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\rm old}(a_t\mid s_t)},\quad \epsilon_t=\epsilon(p_{\rm old}(a_t\mid s_t)),\quad \operatorname{clip}(r_t,1-\epsilon_t,1+\epsilon_t).",
        "result": "论文在七个竞赛级推理 benchmark 上报告优于既有 LLM RL 方法，AIME24 相对 GRPO 的最高增幅为 60%；未报告生产线上 A/B。",
        "local": "在 GSM8K candidate-policy 上实际执行依旧概率相关的 Fisher–Rao clip、组内优势和旧 rollout policy 刷新，并记录各样本动态半径。",
        "boundary": "候选动作概率替代 token 分布，验证动态 clip 与梯度路径，不复刻论文的全参数长 CoT 训练。",
    },
    {
        "module": "post-training", "slug": "2606.15079-kpop", "id": "2606.15079",
        "title": "KPop：二元 KL 自适应训推失配掩码", "key": "kpop",
        "institution": "Ling / Ring 技术报告作者团队", "date": "2026-06-13",
        "code": "未发现独立算法开源仓库", "topic": "异步训推失配 / adaptive mask",
        "summary": "异步 rollout 中的 serving 概率与训练侧概率失配，固定 ratio mask 会误删正常探索或保留错误梯度。KPop 将当前 token 与“其余词表”压缩为二元分布，只有正反两个方向的 binary KL 都低于阈值时才保留该 token 的更新。",
        "mermaid": 'S["serving probability"] --> B["binary token/rest KL"]\n    T["training probability"] --> B\n    B --> M["adaptive keep / mask"]\n    M --> U["policy gradient"]',
        "formula": r"D_{\rm bi}(p\Vert q)=p\log\frac pq+(1-p)\log\frac{1-p}{1-q},\quad m_t=\mathbf1[D_{\rm bi}(p\Vert q),D_{\rm bi}(q\Vert p)\le\tau].",
        "result": "Ling/Ring 2.6 技术报告将 KPop 用于大规模异步 agentic RL，以稳定 coding、search、tool-use 和 workflow 环境训练；未给出生产线上 A/B。",
        "local": "在候选策略的 rollout/训练双分布上计算双向 binary KL，并让 mask 真正决定每个采样动作是否产生 policy gradient。",
        "boundary": "没有真实训推引擎、MoE routing 或万亿参数异步集群；本地只验证 binary-KL mask 的可审计更新语义。",
    },
    {
        "module": "post-training", "slug": "2508.07629-gppo", "id": "2508.07629",
        "title": "GPPO：保留越界梯度的 PPO clip", "key": "gppo",
        "institution": "Klear-Reasoner 作者团队（含 Alibaba Group）", "date": "2025-08-11",
        "code": "未发现独立算法开源仓库", "topic": "梯度保留 clip",
        "summary": "普通 PPO 在正优势高 ratio、负优势低 ratio 的越界象限直接令梯度为零，可能同时压制探索和从负样本学习。GPPO 保持 PPO 的前向 clipped objective，但通过 stop-gradient 边界权重恢复这些越界位置的反向信号。",
        "mermaid": 'R["importance ratio"] --> P["PPO clipped surrogate"]\n    P --> F["same forward objective"]\n    R --> G["stop-gradient boundary weight"]\n    G --> B["preserved backward gradient"]',
        "formula": r"\tilde r_t=\operatorname{sg}(\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)-r_t)+r_t,\quad \mathcal L=-\min(r_tA_t,\operatorname{clip}(r_t)A_t).",
        "result": "Klear-Reasoner 报告 GPPO 改善探索与负样本利用，整体模型在 AIME 2024/2025 与 LiveCodeBench 上取得较强结果；未报告线上 A/B。",
        "local": "在 GSM8K candidate-policy 中区分 PPO 正常和越界样本，前向仍计算 clipped surrogate，反向以 clip 边界权重保留越界梯度。",
        "boundary": "本地不训练 Klear-Reasoner 或长 CoT SFT，只复现 GPPO 的前向/反向分离机制。",
    },
    {
        "module": "post-training", "slug": "2503.20783-dr-grpo", "id": "2503.20783",
        "title": "Dr. GRPO：去长度与组方差偏置的组策略优化", "key": "dr-grpo",
        "institution": "SAIL 研究团队", "date": "2025-03-26",
        "code": "[已开源](https://github.com/sail-sg/understand-r1-zero)", "topic": "GRPO 聚合 / 长度偏置",
        "summary": "原始 GRPO 的 response 内长度平均和组内标准差会引入长度与题目难度偏置。Dr. GRPO 移除这两个归一化项，保留中心化的组相对奖励，让每条轨迹以原始尺度参与更新。",
        "mermaid": 'G["response group"] --> C["mean-center rewards"]\n    C --> N["remove std / length normalization"]\n    N --> P["clipped policy update"]',
        "formula": r"\hat A_i=r_i-\frac1G\sum_{j=1}^G r_j,\qquad \mathcal L_{\rm DrGRPO}=-\frac1G\sum_i\min(r_i(\theta)\hat A_i,\operatorname{clip}(r_i(\theta))\hat A_i).",
        "result": "论文报告在保持推理效果的同时提升 token efficiency，并以极简 R1-Zero recipe 在 7B base 上得到 AIME24 43.3%；未报告线上 A/B。",
        "local": "在相同 GSM8K candidate-policy、步数和 seed 下真实移除组 std 与伪长度归一化，并与 GRPO 的更新统计对比。",
        "boundary": "候选策略没有自由生成 response 长度，伪长度只用于暴露归一化差异，不等同于论文的 token-level 长 CoT 训练。",
    },
    {
        "module": "post-training", "slug": "2607.10481-armor", "id": "2607.10481",
        "title": "ARMOR：reference anchor rollout", "key": "armor",
        "institution": "论文作者团队（机构详见原论文）", "date": "2026-07-11",
        "code": "未发现官方代码", "topic": "reference anchor / 长程稳定性",
        "summary": "单纯 reverse-KL 只能被动惩罚偏离，无法保证 reference 中已有有效解法仍被覆盖。ARMOR 从冻结 reference 主动采样 anchor trajectories，与当前策略 rollout 混合优化，用数据而不是辅助 KL 项稳定长程 RL。",
        "mermaid": 'R["reference policy"] --> A["anchor rollouts"]\n    P["current policy"] --> O["on-policy rollouts"]\n    A --> M["mixed optimization"]\n    O --> M\n    M --> U["stable update"]',
        "formula": r"\mathcal L=\mathbb E_{\tau\sim\pi_\theta}[\ell_{\rm on}(\tau)]+\lambda\mathbb E_{\tau\sim\pi_{\rm ref}}[\ell_{\rm anchor}(\tau)].",
        "result": "论文在推理 benchmark 上报告 anchor rollout 能缓解验证集 collapse、支持更长训练；未报告生产线上 A/B。",
        "local": "每个训练组一半从当前策略采样、一半从冻结 reference 采样，分别记录 anchor 数、权重和最终策略指标。",
        "boundary": "reference 是本地初始化候选策略，不包含论文规模的长程训练或真实轨迹池。",
    },
    {
        "module": "post-training", "slug": "2501.03262-reinforce-plus", "id": "2501.03262",
        "title": "REINFORCE++：全局优势归一化", "key": "reinforce-plus",
        "institution": "论文作者团队（机构详见原论文）", "date": "2025-01-04",
        "code": "未发现官方代码", "topic": "优势估计 / critic-free RL",
        "summary": "GRPO/RLOO 的 prompt-local 标准差会让不同难度组被随机方差重新加权。REINFORCE++ 保留组内中心化，但使用跨 batch 的全局优势尺度归一化，从而在不引入 critic 的前提下降低方差与局部偏置。",
        "mermaid": 'G["prompt group rewards"] --> C["group mean centering"]\n    B["global reward moments"] --> N["global normalization"]\n    C --> N\n    N --> U["critic-free update"]',
        "formula": r"\hat A_i=\frac{r_i-\overline r_{\rm group}}{\sqrt{\operatorname{EMA}_{\rm batch}[(r-\overline r)^2]}+\epsilon}.",
        "result": "论文报告全局优势归一化在通用 RLHF、复杂推理和 agentic 设置中优于 prompt-local critic-free 基线与部分 PPO 对照；未报告线上 A/B。",
        "local": "维护跨训练步的 reward 二阶矩，真实以它而非当前组 std 缩放 group-centered advantage。",
        "boundary": "本地 EMA 是小批候选轨迹统计，不代表论文的大 batch 分布或人类偏好奖励。",
    },
    {
        "module": "post-training", "slug": "2607.07976-taco", "id": "2607.07976",
        "title": "TACO：尾部 token 信用校准", "key": "taco",
        "institution": "论文作者团队（机构详见原论文）", "date": "2026-07-08",
        "code": "[已开源](https://github.com/xiuyilou/TACO)", "topic": "token 信用 / 熵与 surprisal",
        "summary": "整条回答正确时，统一的正 advantage 会把内部不合理的低概率 token 一起强化，形成 positive-credit contamination。TACO 依据局部上下文计算 tail risk，并仅平滑降低高 risk token 的正信用，负信用仍完整保留。",
        "mermaid": 'T["sampled token"] --> S["contextual tail-risk / surprisal"]\n    A["response advantage"] --> W["positive-credit calibration"]\n    S --> W\n    W --> U["token policy update"]',
        "formula": r"\tilde A_t=\begin{cases}w(\operatorname{tailrisk}_t)A,&A>0\\A,&A\le0,\end{cases}\qquad 0<w(\cdot)\le1.",
        "result": "论文在三种 LLM、八个 benchmark 上报告优于 GRPO 类基线，并改善长程 RL 稳定性；未报告线上 A/B。",
        "local": "以 rollout 概率的 surprisal 代理 tail risk，正 advantage 的 tail 样本会被连续降权，负 advantage 不会被 mask。",
        "boundary": "候选动作而非逐 token CoT，无法复刻论文的上下文 tail-risk predictor，只验证信用校准方向。",
    },
    {
        "module": "post-training", "slug": "2508.11408-chord", "id": "2508.11408",
        "title": "CHORD：动态协调 SFT 与 on-policy RL", "key": "chord",
        "institution": "Alibaba Group / ModelScope 作者团队", "date": "2025-08-15",
        "code": "[已开源](https://github.com/modelscope/Trinity-RFT/tree/main/examples/mix_chord)", "topic": "教师轨迹 / SFT-RL 混合",
        "summary": "将 SFT 与 RL 串成两个独立阶段会造成 expert data 的过拟合或过早遗忘。CHORD 把专家 SFT 作为 on-policy RL 中动态退火的辅助目标，并以 token 级不确定性权重平滑从模仿过渡到探索。",
        "mermaid": 'E["off-policy expert trace"] --> S["dynamic SFT weight"]\n    O["on-policy rollout"] --> R["group RL loss"]\n    S --> M["mixed objective"]\n    R --> M\n    M --> U["policy update"]',
        "formula": r"\mathcal L=\lambda_t\mathcal L_{\rm SFT}+(1-\lambda_t)\mathcal L_{\rm RL},\qquad \lambda_t\downarrow\ \text{during training}.",
        "result": "论文在多个实际任务上报告动态混合优于分离式 SFT+RL 与静态混合基线；未报告生产线上 A/B。",
        "local": "把 verified gold candidate 作为 expert trace，真实按训练进度退火 SFT 项并与 on-policy group-RL 梯度相加。",
        "boundary": "本地不训练 LLM token-level uncertainty model，gold candidate 仅是确定性 expert 代理。",
    },
    {
        "module": "post-training", "slug": "2504.05118-vapo", "id": "2504.05118",
        "title": "VAPO：面向长 CoT 的 critic PPO", "key": "vapo",
        "institution": "论文作者团队（机构详见原论文）", "date": "2025-04-07",
        "code": "未发现官方代码", "topic": "critic PPO / 长 CoT",
        "summary": "长 CoT 的 value-based PPO 易受 critic bias、异质 response 长度和稀疏奖励影响。VAPO 预训练 value model，并依 response 长度调节 actor 的 GAE/更新策略，以更稳定地进行 value-based 推理 RL。",
        "mermaid": 'R["sparse outcome reward"] --> C["pretrained value critic"]\n    L["response length"] --> G["length-adaptive GAE"]\n    C --> G\n    G --> P["PPO actor update"]',
        "formula": r"\hat A_t^{\rm VAPO}=\sum_{l\ge0}(\gamma\lambda(L))^l\delta_{t+l},\qquad \mathcal L_{\rm actor}=\min(r_t\hat A_t,\operatorname{clip}(r_t)\hat A_t).",
        "result": "论文在 Qwen-32B / AIME 2024 上报告 60.4，并称相同设置下超过 DeepSeek-R1-Zero-Qwen-32B 与 DAPO 十余分；未报告线上 A/B。",
        "local": "复用可训练线性 critic，按候选伪长度调节 GAE 系数，并真实更新 actor、old policy 和 critic。",
        "boundary": "本地 critic 不是预训练 value model，候选动作与伪长度替代自由生成长 CoT。",
    },
    {
        "module": "agent-research", "slug": "2505.10978-gigpo", "id": "2505.10978",
        "title": "GiGPO：Agent 的组中组相对优势", "key": "gigpo",
        "institution": "论文作者团队（机构详见原论文）", "date": "2025-05-16",
        "code": "未发现官方代码", "topic": "Agent step credit / group RL",
        "summary": "多轮 Agent 的最终奖励稀疏，整条轨迹的 group relative advantage 无法判断哪个 environment step 做对了。GiGPO 先在完整轨迹组上计算 macro advantage，再按跨轨迹重复到达的 anchor state 建立 step group，计算 micro relative advantage。",
        "mermaid": 'T["trajectory group"] --> M["macro relative advantage"]\n    T --> A["shared anchor states"]\n    A --> m["micro step advantage"]\n    M --> U["agent policy update"]\n    m --> U',
        "formula": r"A^{\rm GiGPO}_{t}=A^{\rm macro}(\tau)+A^{\rm micro}(s_t,a_t),\quad A^{\rm micro}=r(s_t,a_t)-\operatorname{mean}_{a\in\mathcal G(s_t)}r(s_t,a).",
        "result": "论文在 ALFWorld、WebShop 与 search-augmented QA 上报告相对 GRPO 的显著提升，ALFWorld 超过 12%、WebShop 超过 9%；未报告线上 A/B。",
        "local": "在 PlanBench mini 中显式生成完整轨迹组与 step group，分别统计组间和组内优势、trajectory rollout 与 turn credit。",
        "boundary": "确定性任务没有跨轨迹真实环境 state 合流，使用共享计划步骤作为可审计 anchor-state 代理。",
    },
    {
        "module": "agent-research", "slug": "2604.18401-steppo", "id": "2604.18401",
        "title": "StepPO：step-aligned Agent 策略优化", "key": "steppo",
        "institution": "University of Science and Technology of China 作者团队", "date": "2026-04-20",
        "code": "未发现官方代码", "topic": "Agent step MDP / step GAE",
        "summary": "Agent 的自然决策单位是“观察—动作”的 environment step，token-level MDP 会让动作粒度和信用粒度错位。StepPO 将交互重写为 step-level MDP，在 step boundary 估值和做 GAE，并把 step 内 token ratio 聚合后再裁剪。",
        "mermaid": 'O["environment observation"] --> S["step action"]\n    S --> V["step critic / GAE"]\n    V --> R["within-step ratio aggregation"]\n    R --> U["step-aligned update"]',
        "formula": r"\hat A_t^{\rm step}=\sum_{l\ge0}(\gamma\lambda)^l\delta_{t+l},\qquad r_t^{\rm step}=\exp\!\left(\frac1{|\mathcal T_t|}\sum_{j\in\mathcal T_t}\log r_j\right).",
        "result": "论文在 multi-hop QA、论文搜索和 text-world action 任务上报告持续超过多种 token-centric RL 基线；未报告线上 A/B。",
        "local": "在 PlanBench mini 的每个环境动作边界执行 step value、step GAE 与 step sequence-ratio clip，并公开对应诊断计数。",
        "boundary": "本地 action 是确定性工具计划，不含真实 LLM token generation；验证的是 step 对齐状态机而非论文规模的 agent 训练。",
    },
)


def render(paper: dict[str, str]) -> str:
    source = f"src/auto_research/{paper['module'].replace('-', '_')}/"
    url = paper["url"] if "url" in paper else f"https://arxiv.org/abs/{paper['id']}"
    publication_label = (
        paper["publication_label"]
        if "publication_label" in paper
        else f"{paper['title']}（arXiv {paper['id']}）"
    )
    information_heading = paper.get("information_heading", "论文信息")
    summary_heading = paper.get("summary_heading", "原始论文总结")
    result_heading = paper.get("result_heading", "论文离线与线上效果")
    scope_note = paper.get(
        "scope_note",
        "本页在公开候选策略或确定性 Agent mini-suite 上复现可隔离的 RL 更新机制；不把轻量实验写成原论文规模模型或 benchmark 结论。",
    )
    command = (
        f"auto-research post-train --algorithm {paper['key']} --dataset gsm8k-candidate "
        "--maximum-examples 256 --steps 120 --seed 42"
        if paper["module"] == "post-training"
        else f"auto-research agent-eval --method {paper['key']} --benchmark planbench-mini --episodes 120 --seed 42"
    )
    return f'''# {paper["title"]}

> {scope_note}

## {information_heading}

| 字段 | 内容 |
|---|---|
| {"资料链接" if information_heading == "资料信息" else "论文链接"} | [{publication_label}]({url}) |
| 公司 / 机构 | {paper["institution"]} |
| 首次公开日期 | {paper["date"]} |
| 原作者代码 | {paper["code"]} |
| 本地 adapter / 算法键 | `{paper["key"]}` |
| 本地复现代码 | [`{source}`](https://github.com/daiwk/auto-research/tree/main/{source}) |

## {summary_heading}

### 背景与主要改动

{paper["summary"]}

```mermaid
flowchart LR
    {paper["mermaid"]}
```

### 核心公式

$$
{paper["formula"]}
$$

### {result_heading}

{paper["result"]}

## 本地复现

{paper["local"]}

```bash
{command}
```

固定 seed 汇总指标见 [`rl-papers-summary-seed42.json`](../../experiments/rl-papers-summary-seed42.json)。

## 复现边界

{paper["boundary"]}
'''


def preserve_figure(rendered: str, existing: str) -> str:
    if FIGURE_START not in existing or FIGURE_END not in existing:
        return rendered
    figure = (
        existing.split(FIGURE_START, 1)[1].split(FIGURE_END, 1)[0]
    )
    block = f"{FIGURE_START}{figure}{FIGURE_END}\n"
    diagram_end = rendered.index("```\n", rendered.index("```mermaid")) + 4
    return rendered[:diagram_end] + "\n" + block + rendered[diagram_end:]


def main() -> None:
    for paper in PAPERS:
        path = DOCS / paper["module"] / paper["slug"] / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        rendered = render(paper)
        if path.exists():
            rendered = preserve_figure(
                rendered, path.read_text(encoding="utf-8")
            )
        path.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
