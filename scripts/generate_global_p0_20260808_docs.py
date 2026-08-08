#!/usr/bin/env python3
"""Generate detail pages for the global P0 audit completed on 2026-08-08."""

from __future__ import annotations

import json
from pathlib import Path

from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[1]
RUN = json.loads((ROOT / "docs/experiments/global-p0-20260808-seed42.json").read_text())
FIGURE_START = "<!-- paper-figure:start -->"
FIGURE_END = "<!-- paper-figure:end -->"


REPRO = {
    "glorank": ("全局 Semantic ID 空间把局部候选重排改写为全库生成；先做 listwise SFT，再用组相对奖励优化列表效用与长尾覆盖。", r"J(\theta)=\mathbb E_{\pi_\theta(Y|h)}[R_{list}(Y)],\quad R=R_{rel}+\lambda R_{global}.", "快手 7.8% 流量、14 天：Watch Time +0.095%，Effective View +0.111%，Like +0.286%。"),
    "dual-rerank": ("AR 教师学习物品间顺序依赖，NAR 学生并行估计名次；效用蒸馏把效果与延迟共同写入训练目标。", r"\mathcal L=\mathcal L_{rank}+\lambda\,D_{KL}(p_{AR}\Vert p_{NAR})+\gamma\mathcal L_{utility}.", "快手搜索 5% 流量一个月：Long View +1.107%，并降低平均与 P99 延迟。"),
    "oneranker": ("用 fake item token 统一生成、点击价值估计和广告排序，并通过分布一致性约束让生成概率与 value head 保持同一偏好。", r"\mathcal L=\mathcal L_{gen}+\lambda_v\mathcal L_{value}+\lambda_cD_{KL}(p_{gen}\Vert p_{rank}).", "微信视频号广告全量部署：GMV +1.34%。"),
    "radar": ("将完整排序模型在本次请求后异步运行，把高价值结果缓存为下一次请求的召回补充，再与实时召回合并。", r"C_{t+1}=R_{live}(h_{t+1})\cup\operatorname{TopK}(f_{rank}(h_t,\mathcal I)).", "线上 Recall@200 约翻倍，engagement +0.8%。"),
    "dualgr": ("短期兴趣与长期兴趣使用双路由器，约束 Semantic ID 前缀有效性，并以曝光感知项抑制头部坍缩。", r"p(i|h)=g(h)p_s(i|h)+(1-g(h))p_l(i|h),\quad\mathcal L=\mathcal L_{SID}+\lambda\mathcal L_{expo}.", "快手线上 Video Views +0.527%，Watch Time +0.432%。"),
    "mpformer": ("以 objective token 驱动同一序列检索器完成多种行为目标，并按任务难度动态分配容量和候选配额。", r"z_m=F([e_m;h]),\quad\mathcal L=\sum_m q_m(h)\mathcal L_m,\quad\sum_mq_m=1.", "快手 Watch Time +0.426%；训练资源 -60%，serving 资源 -66.7%。"),
    "hap": ("按候选难度把样本路由到轻量或强预排分支，再以跨分支 harmonization 约束不同计算预算下的排序尺度。", r"s_i=g_i f_{strong}(x_i)+(1-g_i)f_{light}(x_i),\quad\mathcal L=\mathcal L_{rank}+\lambda\mathcal L_{harm}.", "今日头条部署九个月：使用时长 +0.4%，活跃天数 +0.05%。"),
    "onepiece": ("把上下文 token、块级 latent reasoning 与递进多任务目标合并到级联排序器，让召回、点击和价值任务共享表示但分阶段收敛。", r"H^{k+1}=H^k+F_k(H^k,c),\quad\mathcal L=\sum_t\alpha_t(k)\mathcal L_t.", "Shopee GMV/UU 超过 +2%，广告收入 +2.90%。"),
    "intsr": ("用显式查询和隐式会话意图共同生成 POI/物品，统一搜索与推荐词表，并加入时间上下文刻画意图漂移。", r"p(i|q,h,t)=\sum_zp(i|z,t)p(z|q,h),\quad\mathcal L=-\log p(i^+|q,h,t).", "高德 GMV +9.34%，POI CTR +2.76%。"),
    "cdm": ("先用可控 MMR 教师产生兼顾相关性与多样性的列表，再把上下文边际收益蒸馏到可低延迟服务的学生。", r"y_t=\arg\max_i[s(i)-\lambda\max_{j<t}\operatorname{sim}(i,j)],\quad\mathcal L=\|f_\theta-y_{teacher}\|^2.", "快手主端 Watch Time +0.406%，聚类系数 -0.957%。"),
    "cwm": ("以反事实观看时长估计消除视频时长偏置：区分观察到的 watch time 与在统一时长干预下的潜在收益。", r"\hat y(d_0)=\mathbb E[Y\mid X,do(D=d_0)],\quad s=\hat y(d_0)-\lambda\,\operatorname{bias}(D).", "快手 Mean Watch Time +2.9%、Video Views +2.5%、CTR +0.3%。"),
    "rope": ("对每个 attention head 的 Q/K 二维子空间施加随位置旋转，使点积天然只依赖相对位移。", r"q_m=R_mW_qx_m,\ k_n=R_nW_kx_n,\quad q_m^\top k_n=x_m^\top W_q^\top R_{n-m}W_kx_n.", "原文在多项长文本分类与语言建模任务上优于绝对位置编码。"),
    "alibi": ("不学习位置向量，而是在每个 head 的注意力 logits 上加入线性距离惩罚，实现 train-short/test-long 外推。", r"\operatorname{softmax}(QK^\top-m_h|i-j|).", "原文在 1024 token 训练、2048 token 测试时匹配或超过正弦/旋转位置基线。"),
    "gqa": ("多个 query head 共享较少的 K/V head，在 MHA 质量与 MQA 解码带宽之间取得可控折中。", r"Q_h=XW_h^Q,\quad K_h=XW_{g(h)}^K,\ V_h=XW_{g(h)}^V,\quad N_{KV}<N_Q.", "原文通过少量 uptraining 将 MHA checkpoint 转为 GQA，质量接近 MHA、速度接近 MQA。"),
    "hymba": ("同一层并行执行 attention 与状态空间分支，再用输入相关 gate 融合局部精确检索和线性长程状态。", r"H'=H+g(X)\odot A(X)+(1-g(X))\odot SSM(X).", "Hymba-1.5B 在同尺寸模型中报告更优 accuracy、cache 与吞吐折中。"),
    "moba": ("把序列切成 block，以可微 router 为每个 query 选择少量相关块，同时保留当前因果块。", r"A(q)=\operatorname{softmax}(qK_{\mathcal B(q)}^\top)V_{\mathcal B(q)},\quad\mathcal B(q)=\operatorname{TopK}_b r(q,b).", "原文在长上下文训练中以稀疏计算逼近 full attention，并扩展到百万 token。"),
    "doremi": ("用小型 proxy model 的 excess loss 做 group DRO，动态提升欠拟合域权重，再按所得配比训练目标模型。", r"\alpha_d\leftarrow\frac{\alpha_d\exp(\eta[L_d-L_d^{ref}])}{\sum_j\alpha_j\exp(\eta[L_j-L_j^{ref}])}.", "原文在 The Pile 上以更少训练步达到 baseline 8B 模型的平均性能。"),
    "data-mixing-laws": ("先训练多组小预算 domain mixture，拟合各评测域的混合缩放律，再搜索未训练过的最优配比。", r"L_i(\mathbf p,N)=c_i+\sum_j a_{ij}p_j^{-\beta_{ij}}N^{-\gamma_i},\quad\mathbf p^*=\arg\min_{\Delta} \sum_iw_iL_i.", "原文用小模型曲线预测更大预算的 RedPajama 配比，并优于人工与均匀混合。"),
    "blt": ("直接处理 byte，并依据 next-byte entropy 动态形成 patch；全局 Transformer 在 patch 级计算，局部编码器/解码器恢复 byte。", r"b_t=\mathbf1[H(x_{t+1}|x_{\le t})>\tau],\quad z_k=E(x_{s_k:e_k}),\quad p(x)=D(T(z),x_{<t}).", "原文显示 byte patch 在固定 FLOPs 下具有更好的 scaling，并提升噪声与多语鲁棒性。"),
}


POST = {
    "rlaif": ("2309.00267", "RLAIF：用 AI 偏好替代昂贵人工标注", "2023-09-01", "Google Research / Google DeepMind", "未发现/未发布原作者独立训练仓库", "AI labeler 对候选做顺序交换评判，去除位置偏差后训练 preference policy；本地落实双顺序标签与成对更新。", r"\hat r=\tfrac12[r_{AI}(a,b)+r_{AI}^{swap}(b,a)],\quad\mathcal L=-\log\sigma(\log\pi(y^+)-\log\pi(y^-)).", "RLAIF 在摘要、helpful 与 harmless 对话上达到与 RLHF 相当表现，direct-RLAIF 更强。"),
    "process-supervision": ("2305.20050", "Let's Verify Step by Step：过程监督与主动标注", "2023-05-31", "OpenAI", "[已开源 PRM800K 数据](https://github.com/openai/prm800k)", "逐步奖励模型判断每个推理步骤，并优先标注不确定步骤；本地与 outcome-only 奖励使用同一候选和预算。", r"\mathcal L_{PRM}=-\sum_t[y_t\log r_t+(1-y_t)\log(1-r_t)],\quad t^*=\arg\max_tH(r_t).", "过程监督模型在代表性 MATH 子集解出 78%，并优于 outcome supervision。"),
    "math-shepherd": ("2312.08935", "Math-Shepherd：无需人工逐步标签的过程奖励", "2023-12-14", "Peking University / Alibaba Group", "未发现/未发布原作者独立代码仓库", "从中间步骤采样多条 continuation，以最终答案正确率构造自动 step label，再训练 verifier 和重排器。", r"v(s_t)=K^{-1}\sum_{k=1}^K\mathbf1[\operatorname{Ans}(\tau_k)=y^*],\quad\mathcal L=-\sum_t\operatorname{BCE}(r(s_t),v(s_t)).", "原文在 GSM8K/MATH 上提升多种 7B/13B 模型的生成与 reranking。"),
    "self-rewarding": ("2401.10020", "Self-Rewarding LM：模型既生成回答也充当裁判", "2024-01-18", "Meta AI / New York University", "未发现/未发布原作者官方训练仓库", "每轮由当前模型生成候选并以 LLM-as-a-Judge 打分，形成新的偏好对继续 DPO，构成自举闭环。", r"D_{t+1}=D_t\cup\{(x,y^+,y^-):J_{\theta_t}(x,y^+)>J_{\theta_t}(x,y^-)\},\quad\theta_{t+1}=\operatorname{DPO}(D_{t+1}).", "三轮自奖励持续提升 instruction following 与 judge 能力；无生产 A/B。"),
    "luffy": ("2504.14945", "LUFFY：离策略示范与 on-policy reasoning 的统一更新", "2025-04-21", "University of Washington / SimpleReasoning", "[已开源](https://github.com/Simplified-Reasoning/LUFFY)", "把离线高质量推理与在线 rollout 放进同一 support，通过正则化 importance ratio 保留 on-policy 行为。", r"\rho=\pi_\theta(y|x)/\mu(y|x),\quad\mathcal L=-\mathbb E[\operatorname{clip}(\rho)A\log\pi_\theta]+\beta D_{KL}(\pi_\theta\Vert\pi_{ref}).", "论文在数学推理基准上超过纯 SFT、纯离策略和纯 on-policy 基线。"),
    "ttrl": ("2504.16084", "TTRL：无标签测试集上的在线强化学习", "2025-04-22", "PRIME-RL author team", "[已开源](https://github.com/PRIME-RL/TTRL)", "同一测试题多次采样，以多数一致答案作为伪标签并即时更新模型，不访问 gold label。", r"\hat y=\operatorname{mode}\{y_k\}_{k=1}^K,\quad r_k=\mathbf1[y_k=\hat y],\quad\theta' = \theta+\eta\nabla J_{GRPO}(r).", "论文在多个 reasoning benchmark 与模型规模上报告 test-time 提升；无生产 A/B。"),
    "absolute-zero": ("2505.03335", "Absolute Zero：零人工数据的自生成课程", "2025-05-06", "Tsinghua University / LeapLab", "[已开源](https://github.com/LeapLabTHU/Absolute-Zero-Reasoner)", "proposer 自己生成可验证任务，solver 求解，程序 verifier 提供奖励；按当前能力边界组织课程。", r"x\sim\pi_P,\ y\sim\pi_S(\cdot|x),\ r=V(x,y),\quad\max_{P,S}\mathbb E[r+\lambda H_{curriculum}(x)].", "Absolute Zero Reasoner 在代码与数学推理上从零数据自举并超过多种人工数据 RLVR 基线。"),
    "intuitor": ("2505.19590", "INTUITOR：以自置信度替代外部 verifier", "2025-05-26", "University of California, Berkeley", "[已开源](https://github.com/sunblaze-ucb/Intuitor)", "把答案分布相对均匀分布的 KL 作为 intrinsic self-certainty reward，在没有答案和 verifier 时优化。", r"r_{int}(y)=D_{KL}(\pi_\theta(\cdot|x,y_{<t})\Vert U),\quad\max_\theta\mathbb E[r_{int}].", "论文在无外部奖励条件下提升多项推理任务；本地 mini-suite 不具测试分布漂移，因此可能不提升。"),
    "cispo": ("2506.13585", "CISPO / MiniMax-M1：裁剪 importance weight 而非优势", "2025-06-16", "MiniMax", "[已开源](https://github.com/MiniMax-AI/MiniMax-M1)", "固定 rollout policy 采样，token 级计算 importance ratio，只裁剪比率以保留优势方向和有效梯度。", r"\mathcal L=-\mathbb E[\operatorname{clip}(\pi_\theta/\pi_{old},1-\epsilon,1+\epsilon)A\log\pi_\theta].", "MiniMax-M1 技术报告展示长上下文 RL 的效率与 reasoning/agent benchmark 结果；无生产 A/B。"),
    "spiral": ("2506.24119", "SPIRAL：零和语言游戏驱动的自博弈推理", "2025-06-30", "Apple / academic collaborators", "[已开源](https://github.com/spiral-rl/spiral)", "同一模型扮演出题者和解题者，在可自动判定的零和多轮语言游戏中形成逐步变难的课程。", r"\max_{\pi_A}\min_{\pi_B}\mathbb E_{\tau\sim(\pi_A,\pi_B)}[R(\tau)],\quad A_A=-A_B.", "论文显示仅依赖自博弈即可提升多项 reasoning benchmark，并在小模型上产生迁移。"),
    "conspo": ("2605.12969", "ConSPO：对比式序列策略优化", "2026-05-13", "Feng Zhang 等（按一作归档）", "未发现/未发布原作者官方代码", "将同组序列的优劣关系写成长度归一化 InfoNCE，避免 token 求和造成长度和组内尺度偏差。", r"s(y)=|y|^{-1}\sum_t\log\pi_\theta(y_t|y_{<t}),\quad\mathcal L=-\log\frac{e^{s(y^+)/\tau}}{\sum_{y\in G}e^{s(y)/\tau}}.", "论文在多项 RLVR reasoning benchmark 上报告稳定优于 group-policy baselines；无生产 A/B。"),
}


AGENT = {
    "deepresearcher": ("2504.03160", "DeepResearcher：真实搜索环境中的长轨迹 RL", "2025-04-04", "HKU / GAIR", "[已开源](https://github.com/GAIR-NLP/DeepResearcher)", "把 search、browse、证据收集和带引用回答作为一条轨迹，用答案与引用联合奖励训练研究策略。", r"R=R_{answer}+\lambda_cR_{citation}-\lambda_qN_{query},\quad\max_\pi\mathbb E_{\tau\sim\pi}R(\tau).", "论文在 GAIA、WebWalkerQA 等 deep-research 任务上超过 prompting 和 SFT 基线。"),
    "retool": ("2504.11536", "ReTool：在推理链中学习何时调用工具", "2025-04-15", "Jiazhan Feng 等（按一作归档）", "未发现/未发布原作者官方代码仓库", "策略在自然语言 reasoning 与工具执行之间交替，并由可执行反馈学习调用、纠错和停止。", r"\tau=(z_1,a_1,o_1,\ldots),\quad R=R_{answer}-c\sum_t\mathbf1[a_t=tool],\quad\max_\pi\mathbb E[R].", "论文在数学推理和工具增强任务上超过无工具与固定调用基线。"),
    "toolrl": ("2504.13958", "ToolRL：以执行奖励统一多工具学习", "2025-04-16", "Cheng Qian 等（按一作归档）", "未发现/未发布原作者官方代码仓库", "联合优化工具选择、参数生成和执行结果；动态 reward scaling 让不同工具难度进入同一 RL batch。", r"R=R_{select}+R_{args}+R_{exec}+R_{answer},\quad\hat A=(R-\mu_{tool})/(\sigma_{tool}+\epsilon).", "论文在多工具 benchmark 上改善选择准确率、参数正确率与最终任务成功率。"),
    "sage": ("2512.17102", "SAGE：RL 驱动的自改进技能库", "2025-12-18", "Jiongxiao Wang 等（按一作归档）", "未发现/未发布原作者官方代码仓库", "从成功轨迹抽象技能，失败时修订或淘汰，并以任务回报学习技能检索与复用。", r"s^*=\arg\max_{s\in\mathcal S}q_\phi(s|x),\quad\mathcal S\leftarrow\operatorname{Update}(\mathcal S,\tau,R),\quad\max_\phi\mathbb E[R].", "论文在连续任务上报告技能复用带来的成功率与样本效率提升。"),
    "memskill": ("2602.02474", "MemSkill：把 episodic memory 固化成可执行技能", "2026-02-02", "Haozhen Zhang 等（按一作归档）", "[已开源](https://github.com/ViktorAxelsen/MemSkill)", "controller 从历史 episode 选择记忆，designer 将重复成功模式编译为技能，并随新反馈升级技能版本。", r"m^*=q_\phi(x,M),\quad s=G(\tau,m^*),\quad M,S\leftarrow\operatorname{Consolidate}(M,S,R).", "论文在长程与跨任务 agent benchmark 上提升成功率并减少上下文开销。"),
    "memento-skills": ("2603.18743", "Memento-Skills：让 Agent 设计可迁移 Agent 技能", "2026-03-19", "Memento Team", "[已开源](https://github.com/Memento-Teams/Memento-Skills)", "从执行日志反思出结构化技能说明，按任务检索并写回版本化技能，而不是原样堆叠轨迹。", r"s=\operatorname{Reflect}(\tau,R),\quad k^*=\arg\max_k\operatorname{sim}(x,k),\quad k\leftarrow\operatorname{Merge}(k,s).", "技术报告在多任务 agent suite 上展示技能抽取与跨任务迁移收益。"),
    "searl": ("2604.07791", "SEARL：策略与工具图记忆联合自进化", "2026-04-09", "Xinshun Feng 等（按一作归档）", "未发现/未发布原作者官方代码仓库", "把工具和成功转移维护为图记忆；新 rollout 同时更新 policy 与图边权，形成经验池—检索—改进闭环。", r"a_t\sim\pi_\theta(\cdot|x,G),\quad G\leftarrow G+\Delta(\tau,R),\quad\theta\leftarrow\theta+\eta\nabla J(\theta;G).", "论文在多种工具 agent 任务上报告策略与图记忆联合优化优于单独更新。"),
    "agent0": ("2511.16043", "Agent0：零人工数据的自进化多 Agent 课程", "2025-11-20", "Peng Xia 等（按一作归档）", "未发现/未发布原作者官方代码仓库", "任务生成 Agent 提议可验证工具任务，多个执行 Agent 产生候选并多数投票，课程按当前能力边界升级。", r"x\sim\pi_{task},\ y_{1:K}\sim\pi_{agent},\ \hat y=\operatorname{mode}(y_{1:K}),\quad R=V(x,\hat y).", "论文从零种子数据构建 tool-integrated reasoning curriculum，并提升多项 agent benchmark。"),
}


def diagram(label: str) -> str:
    return f'''```mermaid
flowchart LR
 A["公开输入 / 历史"] --> B["{label}"]
 B --> C["论文特有状态或目标"]
 C --> D["同预算评测"]
```'''


def reproduction_page(key: str) -> str:
    adapter = get_adapter(key)
    paper = adapter.paper
    summary, formula, original = REPRO[key]
    slug = f"{paper.arxiv_id}-{key}"
    metric = json.loads((ROOT / "docs/reproductions" / slug / "metrics/public-seed42.json").read_text())
    if paper.track == "recommendation":
        base, method = metric["baseline"], metric["method"]
        local = f'MovieLens-100K、260 users / 420 items、seed 42：NDCG@10 {base["ndcg_at_10"]:.4f} → **{method["ndcg_at_10"]:.4f}（{metric["relative"]["ndcg_at_10_percent"]:+.2f}%）**。基线是共享 transition + content scorer；实验组只加入论文核心路径。'
        comparison = f'基线为共享 transition + content scorer，实验组只加入 `{key}` 核心机制；相对 NDCG@10 {metric["relative"]["ndcg_at_10_percent"]:+.2f}%。'
        dataset = "movielens-100k"
    elif "perplexity" in metric["baseline"]:
        base, method = metric["baseline"], metric["method"]
        local = f'WikiText-2、12 steps、64d/2-layer、seed 42：PPL {base["perplexity"]:.2f} → **{method["perplexity"]:.2f}（{metric["relative"]["perplexity_percent"]:+.2f}%）**；参数、token、优化器和步数相同。'
        comparison = f'基线为同预算 `llama_modern`，实验组为 `{key}`；相对 PPL {metric["relative"]["perplexity_percent"]:+.2f}%。'
        dataset = "wikitext-2"
    else:
        base, method = metric["baseline"], metric["method"]
        local = f'WikiText-2 + public narrative、seed 42：validation loss {base["validation_loss"]:.4f} → **{method["validation_loss"]:.4f}（{metric["relative"]["validation_loss_percent"]:+.2f}%）**；公开 token 与验证口径一致。'
        comparison = f'基线为均匀数据混合，实验组为 `{key}`；相对 validation loss {metric["relative"]["validation_loss_percent"]:+.2f}%。'
        dataset = "wikitext-2"
    code = (
        f"是：[原作者仓库]({paper.code_url})"
        if paper.code_url
        else "否：未发现/未发布原作者官方代码仓库（核查日期：2026-08-08）"
    )
    package = key.replace("-", "_")
    paper_label = paper.publication_label or f"arXiv {paper.arxiv_id}"
    return f'''# {paper.title}

> **保真度：核心机制复现**。原文结论、本地公开数据实验和未复刻部分分开陈述。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{paper_label}]({paper.url}) |
| 公司/机构 | {paper.organization} |
| 首次公开日期 | {paper.published}（arXiv v1） |
| 原文开源代码 | {code} |
| Adapter | `{key}` |
| 本地复现代码 | [`src/auto_research/reproductions/{package}/`](https://github.com/daiwk/auto-research/tree/main/src/auto_research/reproductions/{package}/) |

## 原始论文总结

### 背景与主要改动

{summary}

{diagram(key + " 核心路径")}

### 核心公式

$$
{formula}
$$

### 论文离线与线上效果

{original}

## 本地复现

> **本地对照口径**：{comparison}

{local}

```bash
auto-research reproduce --paper {key} --dataset-dir data --seed 42
auto-research evolve --model {"rankmixer" if paper.track == "recommendation" else "micro-llm"} --dataset {dataset} --direction "组合 {key} 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`metrics/public-seed42.json`](metrics/public-seed42.json)。

## 复现边界

{metric["scope"]} 本地数值不等同于原论文大模型、私有数据、生产流量或专用 kernel；本地相对变化不得与原文提升混写。
'''


def method_page(key: str, item: tuple[str, ...], module: str) -> str:
    pid, title, date, org, code, summary, formula, original = item
    result = RUN["post_training" if module == "post-training" else "agent"][key]
    if module == "post-training":
        before, after = result["baseline"]["accuracy"], result["final"]["accuracy"]
        delta = (after / before - 1) * 100 if before else 0.0
        local = f'Arithmetic candidate suite、120 steps、256 examples、seed 42：accuracy {before:.4f} → **{after:.4f}（{delta:+.2f}%）**；奖励、KL、长度和候选预算一致。'
        command = f"auto-research post-train --algorithm {key} --dataset arithmetic-smoke --maximum-examples 256 --steps 120 --seed 42"
        code_dir = "src/auto_research/post_training/"
    else:
        metrics = result["metrics"]
        local = f'PlanBench mini-suite、120 episodes、seed 42：joint success **{metrics["joint_success"]:.4f}**，average cost {metrics["average_cost"]:.4f}；方法特有操作有非零 telemetry。'
        command = f"auto-research agent-eval --method {key} --benchmark planbench-mini --episodes 120 --seed 42"
        code_dir = "src/auto_research/agent_research/"
    return f'''# {title}

> **保真度：核心机制复现**。本页不把确定性 mini-suite 冒充原论文完整 benchmark。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{title}（arXiv {pid}）](https://arxiv.org/abs/{pid}) |
| 公司 / 机构 | {org} |
| 首次公开日期 | {date}（arXiv v1） |
| 原作者代码 | {code} |
| 本地 adapter / 方法键 | `{key}` |
| 本地复现代码 | [`{code_dir}`](https://github.com/daiwk/auto-research/tree/main/{code_dir}) |

## 原始论文总结

### 背景与主要改动

{summary}

{diagram(key + " 训练 / 执行闭环")}

### 核心公式

$$
{formula}
$$

### 论文离线与线上效果

{original} 论文未报告生产线上 A/B，本页不补造线上数字。

## 本地复现

{local}

```bash
{command}
auto-research evolve --model {"post-training" if module == "post-training" else "agent"} --dataset {"arithmetic-smoke" if module == "post-training" else "planbench-mini"} --direction "组合 {key} 与已安装论文算子" --generations 2 --population 4
```

固定指标见 [`../../experiments/global-p0-20260808-seed42.json`](../../experiments/global-p0-20260808-seed42.json)。

## 复现边界

本地只验证论文特有目标、状态更新和公平预算；没有复刻原论文的大模型、多卡 RL、私有环境、真实网页或完整 benchmark，因而只报告机制验证，不声称数值复现原表。
'''


def write_page(target: Path, content: str) -> None:
    """Keep a previously synchronized original-paper figure on regeneration."""

    if target.exists():
        previous = target.read_text(encoding="utf-8")
        if FIGURE_START in previous and FIGURE_END in previous:
            figure = previous.split(FIGURE_START, 1)[1].split(FIGURE_END, 1)[0]
            block = f"{FIGURE_START}{figure}{FIGURE_END}\n\n"
            content = content.replace("### 核心公式\n", block + "### 核心公式\n", 1)
    target.write_text(content, encoding="utf-8")


def main() -> None:
    for key in REPRO:
        adapter = get_adapter(key)
        target = ROOT / "docs/reproductions" / f"{adapter.paper.arxiv_id}-{key}" / "README.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        write_page(target, reproduction_page(key))
    for module, items in (("post-training", POST), ("agent-research", AGENT)):
        for key, item in items.items():
            target = ROOT / "docs" / module / f"{item[0]}-{key}" / "README.md"
            target.parent.mkdir(parents=True, exist_ok=True)
            write_page(target, method_page(key, item, module))


if __name__ == "__main__":
    main()
