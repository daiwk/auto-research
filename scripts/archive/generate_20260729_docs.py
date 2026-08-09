#!/usr/bin/env python3
"""Generate the paper pages and scalable catalogs added on 2026-07-29."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


PAPERS = [
    {
        "module": "post-training",
        "slug": "2607.26057-relay-opd",
        "id": "2607.26057",
        "title": "Relay-OPD：轨迹接力式 On-Policy Distillation",
        "key": "relay-opd",
        "institution": "Zhejiang University / Alibaba Group Yuvion Team",
        "date": "2026-07-28",
        "code": "[已开源](https://github.com/ZJU-REAL/Relay-OPD)",
        "topic": "On-policy distillation",
        "summary": "检测学生前缀失效后让教师短暂接管，再把轨迹交还学生；有限接力预算把监督集中到关键早期位置。",
        "mermaid": 'S["学生 rollout"] --> F["前缀失效检测"]\n    F --> T["教师短暂接力"]\n    T --> R["学生恢复生成"]\n    R --> U["整条接力轨迹蒸馏"]',
        "formula": r"\mathcal L_{\mathrm{relay}}=-\sum_t\log p_\theta(y_t\mid y_{<t}),\quad \sum_j L_j\le B_{\mathrm{relay}}.",
        "paper_result": "Qwen3-1.7B 学生在八个数学推理 benchmark 上平均比标准 OPD 高 5.73%，比 FastOPD 高 1.49%，训练轨迹长度减少超过 50%。",
        "local": "GSM8K candidate-policy 上实现失效前缀检测、教师 handoff、有限 relay budget 和学生恢复生成；与同一未训练策略公平比较。",
        "boundary": "本地教师是可复现的候选分布缓存，并非 Qwen3-4B；因此验证接力状态机和监督方向，不冒充论文八卡训练。",
    },
    {
        "module": "post-training",
        "slug": "2607.25659-cort",
        "id": "2607.25659",
        "title": "CoRT：反事实重放的 Token 级 Rubric Credit",
        "key": "cort",
        "institution": "ByteDance internship / academic author team",
        "date": "2026-07-28",
        "code": "截至 2026-07-29 未发现官方公开仓库",
        "topic": "Token-level credit assignment",
        "summary": "对同一响应分别在带 rubric 和去 criteria 的上下文中重放，用 token 似然差重分配 GRPO 的响应级 advantage。",
        "mermaid": 'Y["同一响应"] --> R["rubric 条件重放"]\n    Y --> C["criteria-free 重放"]\n    R --> D["token likelihood contrast"]\n    C --> D\n    D --> U["重加权 GRPO"]',
        "formula": r"w_t=\operatorname{Norm}\!\left(\log\pi_\theta(y_t\mid x,r)-\log\pi_\theta(y_t\mid x)\right),\quad \mathcal L=-\sum_t w_tA\log\pi_\theta(y_t).",
        "paper_result": "跨模型和 reward 粒度的大多数配对实验优于 response-level GRPO，平均提升 4.4 个百分点，且不训练额外 token scorer。",
        "local": "在 GSM8K candidate-policy 上执行 rubric/criteria-free 两次反事实重放、归一化 token 权重和带符号 advantage 更新。",
        "boundary": "候选动作特征代理真实 token 序列；没有开放式生成、rubric judge 或大模型参数更新。",
    },
    {
        "module": "agent-research",
        "slug": "2607.14777-seed",
        "id": "2607.14777",
        "title": "SEED：自进化 On-Policy Distillation",
        "key": "seed",
        "institution": "Tsinghua University / Zhejiang University / CUHK / NTU / Tongji University",
        "date": "2026-07-16",
        "code": "[已开源](https://github.com/jinyangwu/SEED)",
        "topic": "Agentic RL / hindsight skill",
        "summary": "从已完成轨迹中反思出可复用 hindsight skill，再用 skill 条件前后的动作概率变化形成稠密 on-policy 蒸馏信号。",
        "mermaid": 'E["完成的 on-policy 轨迹"] --> A["自分析"]\n    A --> S["hindsight skill"]\n    S --> P["普通/skill 条件重打分"]\n    P --> U["稠密蒸馏 + outcome RL"]',
        "formula": r"r_t^{\mathrm{skill}}=\log\pi_\theta(a_t\mid s_t,z)-\log\pi_\theta(a_t\mid s_t),\quad \mathcal L=\mathcal L_{\mathrm{RL}}+\lambda\mathcal L_{\mathrm{OPD}}.",
        "paper_result": "论文在文本和视觉 Agent 任务上报告一致的性能与样本效率提升，并测试未见场景泛化。",
        "local": "在 PlanBench mini-suite 中把成功/失败轨迹压缩为 hindsight skill，并记录 skill 数量、稠密 credit 更新和跨 episode 复用。",
        "boundary": "使用确定性任务与结构化 skill，不执行视觉模型或大规模策略梯度训练。",
    },
    {
        "module": "agent-research",
        "slug": "2607.25308-cast",
        "id": "2607.25308",
        "title": "CAST：用游戏求解器提供 Turn 级教师信号",
        "key": "cast",
        "institution": "USTC / Nanjing University / Wuhan University",
        "date": "2026-07-28",
        "code": "[已开源](https://github.com/Wloner0809/CAST)",
        "topic": "Agentic RL / turn-level credit",
        "summary": "把求解器状态价值的相邻差分变成 solver advantage，为稀疏结果奖励补充 turn 级 credit。",
        "mermaid": 'S["Agent state"] --> V0["solver value V(s)"]\n    S --> A["执行动作"]\n    A --> V1["solver value V(s′)"]\n    V0 --> D["turn advantage"]\n    V1 --> D\n    D --> U["RLVR update"]',
        "formula": r"A_t^{\mathrm{solver}}=V_{\mathrm{solver}}(s_{t+1})-V_{\mathrm{solver}}(s_t),\quad A_t=A^{\mathrm{outcome}}+\lambda A_t^{\mathrm{solver}}.",
        "paper_result": "在 Sokoban、Minesweeper、Rush Hour 的域内和未见难度上超过训练基线，并在 ALFWorld、WebShop 获得最高平均零样本表现。",
        "local": "PlanBench mini-suite 的确定性最短路充当 solver，逐 turn 查询状态值并统计 credit update。",
        "boundary": "没有复刻论文三类游戏的大规模 LLM RLVR；求解器准确，适合验证 credit assignment 而非模型能力。",
    },
    {
        "module": "agent-research",
        "slug": "2607.05804-turn-opd",
        "id": "2607.05804",
        "title": "TurnOPD：面向长程 Agent 的 Turn-Aware OPD",
        "key": "turn-opd",
        "institution": "Academic author team",
        "date": "2026-07-07",
        "code": "截至 2026-07-29 未发现官方公开仓库",
        "topic": "Agentic OPD / rollout budgeting",
        "summary": "用 probe 统计自适应决定 rollout 深度，并逐步把 token KL 预算迁移为 turn-normalized 监督。",
        "mermaid": 'P["turn probe"] --> B["自适应 rollout 深度"]\n    B --> R["截断轨迹"]\n    R --> N["turn-normalized KL"]\n    N --> U["student update"]',
        "formula": r"L^\star=\operatorname{Budget}(\hat I_1,\ldots,\hat I_T),\quad \mathcal L=\sum_{t\le L^\star}\frac{1}{|y_t|}\mathrm{KL}(\pi_\theta^t\Vert\pi_T^t).",
        "paper_result": "在 ALFWorld、WebShop 和 Multi-Hop Search 的等墙钟预算下提高验证准确率，并推进 accuracy-time 前沿。",
        "local": "ScaleMCP mini-suite 中执行深度 probe、动态截断和 turn 归一化，记录节省的 rollout turns。",
        "boundary": "教师行为由确定性任务 oracle 提供；没有运行任务专用大模型教师。",
    },
    {
        "module": "agent-research",
        "slug": "2607.25853-hiskill",
        "id": "2607.25853",
        "title": "HiSkill：层次化 Skill Graph",
        "key": "hiskill",
        "institution": "Beijing University of Posts and Telecommunications",
        "date": "2026-07-28",
        "code": "[已开源](https://github.com/BUPT-GAMMA/HiSkill)",
        "topic": "Hierarchical skill memory",
        "summary": "用高层 skill、可执行 AtomicOp 和多类有向边组织经验，推理时只检索任务相关子图来落地动作。",
        "mermaid": 'T["交互轨迹"] --> H["高层 Skill"]\n    T --> O["AtomicOp"]\n    H --> G["typed skill graph"]\n    O --> G\n    G --> S["相关子图检索"]\n    S --> A["动作落地"]',
        "formula": r"G=(V_{\mathrm{skill}}\cup V_{\mathrm{op}},E_{\mathrm{decomp}}\cup E_{\mathrm{temporal}}\cup E_{\mathrm{recovery}}),\quad a_t=\operatorname{Ground}(s_t,G_t).",
        "paper_result": "在三个交互环境上超过强基线，同时降低推理 token 消耗。",
        "local": "PlanBench mini-suite 构建高层 skill/AtomicOp 节点及 decomposition、transition、recovery 边，记录子图复用。",
        "boundary": "图节点来自受控轨迹，不由在线 LLM 抽取；主要验证层次和关系是否改善复用。",
    },
    {
        "module": "agent-research",
        "slug": "2607.26017-unimem",
        "id": "2607.26017",
        "title": "UniMem：情景记忆到参数记忆的互补路由",
        "key": "unimem",
        "institution": "CASIA / UCAS / Peking University / University College London",
        "date": "2026-07-28",
        "code": "截至 2026-07-29 未发现官方公开仓库",
        "topic": "Continual agent memory",
        "summary": "新颖任务先进入 episodic buffer；反复出现且可靠的执行模式再被自路由控制器固化到可扩展 parametric memory。",
        "mermaid": 'X["无边界任务流"] --> R["routing token"]\n    R --> E["episodic buffer"]\n    R --> P["parametric memory"]\n    E --> C["可靠模式 consolidation"]\n    C --> P',
        "formula": r"z_t=\operatorname{Route}_\theta(x_t),\quad M_p\leftarrow M_p\oplus\operatorname{Consolidate}(M_e)\ \text{if recurrence}\ge\tau.",
        "paper_result": "在长程流式任务上保持执行 fidelity，三个 backbone 平均提高 4.0 个 EM 点。",
        "local": "EvoMem mini-suite 实现 episodic route、复现频次阈值、parametric route 和 consolidation 统计。",
        "boundary": "参数记忆是结构化模式表，不是扩展 LLM 权重块；验证稳定性/可塑性路由逻辑。",
    },
]

INDUSTRIAL = [
    {
        "slug": "2607.25901-reco-reward", "id": "2607.25901", "key": "reco-reward",
        "title": "RecoReward：用推荐器奖励训练多模态描述", "institution": "Kuaishou / Nankai University / Chinese Academy of Sciences",
        "date": "2026-07-28", "topic": "LLM + 推荐 / 多模态生成",
        "summary": "冻结双塔推荐器，以目标用户与非目标用户的亲和力差作为奖励训练内容描述；线上 serving 只消费描述，不依赖用户画像。",
        "mermaid": 'C["内容特征"] --> G["描述候选"]\n    U["目标/非目标行为塔"] --> R["RAS reward"]\n    G --> R\n    R --> P["策略选择"]\n    P --> S["content-only serving"]',
        "formula": r"R_{\mathrm{RAS}}(d,u)=s(f(d),g(u))-\lambda\,\mathbb E_{u^-}s(f(d),g(u^-)).",
        "paper_result": "离线相对 Qwen 基线的 Recall 提升 31.7%–40.4%；快手一周 A/B 中关键页有效用户渗透 +0.265%、外流曝光 +0.791%、外流用户 +0.740%。",
        "local": "MovieLens-100K 上以历史物品质心代理用户塔，执行目标/非目标扣减、620 个候选打分和 content-only serving。",
        "comparison": "基线为 content-only semantic recall，实验组为 RAS 选择；Hit@10 -16.00%、NDCG@10 -9.68%，head share -24.14%（负结果）。",
        "boundary": "没有微调 Qwen3.5-9B，也没有直播视频和快手私有行为；本地结果只验证 RAS 奖励可执行。",
    },
    {
        "slug": "2607.25404-twice", "id": "2607.25404", "key": "twice",
        "title": "TWICE：双时钟双窗口长延迟转化学习", "institution": "Kuaishou",
        "date": "2026-07-28", "topic": "广告 CVR / 延迟反馈",
        "summary": "把点击时钟的 current-status 标签与转化时钟的 delay CDF 分开学习，再用曝光窗口权重校正长期未成熟标签。",
        "mermaid": 'X["曝光/点击"] --> C["click clock status"]\n    Y["转化延迟"] --> D["conversion clock CDF"]\n    C --> J["two-window likelihood"]\n    D --> J\n    J --> V["CVR"]',
        "formula": r"P(Y=1\mid x,t)=p_{\mathrm{cvr}}(x)\,F_{\mathrm{delay}}(t\mid x),\quad F(t+\Delta)\ge F(t).",
        "paper_result": "Kwai 广告线上 A/B：expected revenue +2.486%、revenue +1.858%、conversions +2.061%，之后部署到全流量。",
        "local": "MovieLens 时间戳构造点击/转化两个时钟，拟合单调 delay CDF 并按 exposure maturity 加权。",
        "comparison": "基线为 mature-label next-item CVR，实验组为双时钟 current-status；Hit@10 +8.00%、NDCG@10 +14.31%。",
        "boundary": "公开交互代理广告延迟，未包含生产聚合记录和真实 revenue；线上数字只引用论文。",
    },
    {
        "slug": "2607.25233-swag-bid", "id": "2607.25233", "key": "swag-bid",
        "title": "SWAG：滑动窗口感知的生成式自动出价", "institution": "Alibaba International Digital Commerce / Dalian University of Technology",
        "date": "2026-07-28", "topic": "广告出价 / 长期决策",
        "summary": "用 masked future plan 建模跨 episode 的七日滑窗目标，并以 per-step gate 将长期 guidance 注入当前 bid 决策。",
        "mermaid": 'H["历史 campaign"] --> M["masked future plan"]\n    W["7-day window objective"] --> M\n    M --> G["state gate"]\n    G --> B["bid/action score"]',
        "formula": r"a_t=\pi_\theta(s_t,\;g_t\odot h_{\mathrm{window}}),\quad g_t=\sigma(W[s_t;h_{\mathrm{window}}]).",
        "paper_result": "AliExpress 21 天 campaign-randomized A/B：cost +1.96%、GMV +3.42%、ROAS +5.65%、目标达成率 +2.02pp。",
        "local": "把 MovieLens 周期行为映射为 campaign window，实际执行 future masking、七日 MPC score 和 state gate。",
        "comparison": "基线为 single-episode Decision Transformer proxy，实验组为 sliding-window planner；同一小数据候选排序下 Hit@10 与 NDCG@10 均为 +0.00%。",
        "boundary": "不是生产 Decision Transformer checkpoint，且公开数据没有 bid、budget、GMV，结果仅是结构消融。",
    },
    {
        "slug": "2607.23749-youtube-freshness", "id": "2607.23749", "key": "youtube-freshness",
        "title": "YouTube Music：打破新颖性与新鲜度反馈环", "institution": "YouTube Music / Google",
        "date": "2026-07-26", "topic": "排序 / 新鲜度 / 探索",
        "summary": "系统比较 recency feature、IPS、可移除 bias tower 与 SNGP 不确定性探索，区分训练去偏和 serving 探索。",
        "mermaid": 'L["连续训练日志"] --> I["IPS debias"]\n    L --> B["bias tower"]\n    X["recency"] --> R["ranker"]\n    I --> R\n    B --> R\n    R --> U["uncertainty exploration"]',
        "formula": r"\mathcal L_{\mathrm{IPS}}=-\frac{y}{\max(p_{\mathrm{log}},\epsilon)}\log\hat y,\quad score=\mu(x)+\beta\sigma(x).",
        "paper_result": "两周、每臂每日数百万用户的六项 A/B；不确定性损失让 1-day new-release engagement +4.33%。",
        "local": "MovieLens 上执行 recency、IPS、训练期 bias tower/serving 移除和距离不确定性加分。",
        "comparison": "基线为 popularity-biased continuous ranker，实验组为四机制组合；Hit@10 +0.00%、NDCG@10 -6.35%，head share -28.72%。",
        "boundary": "没有 YouTube 连续训练基础设施和 SNGP 大模型；本地负结果不推翻论文各干预的在线结论。",
    },
    {
        "slug": "2607.23718-melo", "id": "2607.23718", "key": "melo",
        "title": "Melo：生产级 LLM 音乐推荐 Agent", "institution": "NetEase Cloud Music / Zhejiang University of Technology",
        "date": "2026-07-26", "topic": "LLM + 推荐 / Agent",
        "summary": "用多节点 Agent 编排意图、检索、推荐与解释，以实体目录 grounding 阻止幻觉，并在失败时触发反思重试。",
        "mermaid": 'Q["用户请求"] --> I["意图节点"]\n    I --> R["检索/推荐节点"]\n    R --> G["entity grounding"]\n    G --> V{"有效?"}\n    V -->|否| F["reflective retry"]\n    F --> R\n    V -->|是| O["playlist"]',
        "formula": r"\hat e=\arg\max_{e\in\mathcal E}s(q,e),\quad \text{retry}=\mathbf1[\hat e\notin\mathcal E\ \lor\ score<\tau].",
        "paper_result": "约百万用户、2026-04-02 至 05-10 的系统级 A/B 报告 playlist retention 提升超过 2pp；该数值包含 Muse Mix 产品/UI 整体影响。",
        "local": "MovieLens 目录执行 entity grounding、候选校验和一次 reflective retry，记录错误修复路径。",
        "comparison": "基线为无运行时修复的 catalog recommender，实验组为 grounding + retry；Hit@10 -20.00%、NDCG@10 -8.16%，fresh Hit@10 +50.00%。",
        "boundary": "无法隔离论文系统 A/B 中模型、产品面和 UI 的贡献，论文也未给置信区间；本站明确保留该归因限制。",
    },
    {
        "slug": "2607.25915-penelope", "id": "2607.25915", "key": "penelope",
        "title": "Penelope：局部潜在递归的高效结构化推理", "institution": "Academic author team",
        "date": "2026-07-28", "topic": "纯 LLM / 高效架构",
        "summary": "只在一个 decoder 边界执行共享权重的 latent recurrence，用门控状态反复精炼表示，避免整条 decoder 重跑。",
        "mermaid": 'X["lower decoder"] --> H["localized boundary"]\n    H --> R["shared latent block × K"]\n    R --> G["GRU/time gate"]\n    G --> U["upper decoder"]',
        "formula": r"h^{k+1}=\operatorname{GRU}(h^k,F_\theta(h^k,t_k)),\quad k=1,\ldots,K.",
        "paper_result": "论文报告在结构化推理任务上以局部递归改善 accuracy/compute 权衡；未报告生产线上 A/B。",
        "local": "WikiText-2 同预算 micro-LM 比较 modern decoder 与两步 localized recurrence，并记录实际参数、loss 与 perplexity。",
        "comparison": "基线为 llama_modern，实验组为 penelope；composite loss 从 6.9539 降到 6.9100，相对改善 0.63%。",
        "boundary": "12-step 本地预算不包含论文规模 checkpoint 和 CoT-to-latent curriculum，只验证真实 PyTorch 结构路径。",
    },
]


def research_page(paper: dict[str, str]) -> str:
    module = paper["module"]
    source = f"src/auto_research/{module.replace('-', '_')}/"
    metrics = (
        "post-training-20260729-seed42.json"
        if module == "post-training"
        else "agent-20260729-seed42.json"
    )
    command = (
        f"auto-research post-train --algorithm {paper['key']} --dataset gsm8k-candidate "
        "--maximum-examples 256 --steps 120 --seed 42"
        if module == "post-training"
        else f"auto-research agent-eval --method {paper['key']} --episodes 120 --seed 42"
    )
    return f"""# {paper['title']}

> 保真度：实现论文可隔离的核心状态与更新机制，并在统一公开数据或确定性
> mini-suite 上运行；不把轻量机制实验写成原规模大模型复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [{paper['title']}（arXiv {paper['id']}）](https://arxiv.org/abs/{paper['id']}) |
| 公司 / 机构 | {paper['institution']} |
| 首次公开日期 | {paper['date']} |
| 原作者代码 | {paper['code']} |
| 本地 adapter / 算法键 | `{paper['key']}` |
| 本地复现代码 | [`{source}`](https://github.com/daiwk/auto-research/tree/main/{source}) |

## 原始论文总结

### 背景与主要改动

{paper['summary']}

```mermaid
flowchart LR
    {paper['mermaid']}
```

### 核心公式

$$
{paper['formula']}
$$

### 论文离线与线上效果

{paper['paper_result']} 论文没有报告生产线上 A/B，因此本站只保留离线/环境评测口径。

## 本地复现

{paper['local']}

```bash
{command}
```

固定 seed 指标见
[`{metrics}`](../../experiments/{metrics})。

## 复现边界

{paper['boundary']}
"""


def industrial_page(paper: dict[str, str]) -> str:
    source = f"src/auto_research/reproductions/{paper['key'].replace('-', '_')}/"
    return f"""# {paper['title']}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {paper['id']}](https://arxiv.org/abs/{paper['id']}) |
| 公司/机构 | {paper['institution']} |
| 首次公开日期 | {paper['date']}（arXiv v1） |
| 原文开源代码 | 否：截至 2026-07-29 未发现官方公开仓库 |
| Adapter | `{paper['key']}` |
| 本地复现代码 | [`{source}`](https://github.com/daiwk/auto-research/tree/main/{source}) |

## 原始论文总结

### 背景与主要改动

{paper['summary']}

```mermaid
flowchart LR
    {paper['mermaid']}
```

### 核心公式

$$
{paper['formula']}
$$

### 论文离线与线上效果

{paper['paper_result']}

## 本地复现

> **本地对照口径**：{paper['comparison']}

{paper['local']}

```bash
auto-research reproduce --paper {paper['key']} --data-root data --seed 42
```

稳定结果见 [`result-seed42.json`](metrics/result-seed42.json)。

## 复现边界

{paper['boundary']}
"""


def main() -> None:
    for paper in PAPERS:
        directory = DOCS / paper["module"] / paper["slug"]
        directory.mkdir(parents=True, exist_ok=True)
        page = directory / "README.md"
        if not page.exists():
            page.write_text(research_page(paper), encoding="utf-8")
    for paper in INDUSTRIAL:
        directory = DOCS / "reproductions" / paper["slug"]
        directory.mkdir(parents=True, exist_ok=True)
        page = directory / "README.md"
        if not page.exists():
            page.write_text(industrial_page(paper), encoding="utf-8")

    from generate_research_catalogs import main as generate_catalogs

    generate_catalogs()


if __name__ == "__main__":
    main()
