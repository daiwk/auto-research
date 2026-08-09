"""Generate detailed Chinese documentation for the 2026-08-09 P0/P1 batch."""

from __future__ import annotations

from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[2]
CHECKED = "2026-08-09"

# id, slug, title, organization, date, upstream URL or None, adapter, topic,
# background/change, flow nodes, formula, paper result, local description
PAPERS = [
 ("2608.02738","kgd","Knowledge–Geometry Decoupling: Refreshable Pretrained Transfer for Streaming Recommendation","Xiamen University / Shopee","2026-08-03","https://github.com/FuCongResearchSquad/KGD4REC","kgd","流式推荐预训练与迁移","相邻点击并不总是有效依赖。KGD 用 BMTP 筛出协同或语义相关的未来物品；迁移时冻结可刷新知识编码器，用只读 cross-attention 读取知识，并以与锚点正交的 ACR 写入任务几何。",("行为序列","BMTP 多步监督","可刷新知识编码器","只读迁移 + ACR","排序任务"),r"$\mathcal L_{BMTP}=-\sum_{j\in\mathcal R_t}\log p(i_{t+j}\mid i_{\le t}),\quad r_{ACR}=r-\operatorname{proj}_{e}(r)$","8 个公开基准相对强预训练迁移基线提升 4%–12%；Shopee 首页搜索线上 GMV/user +1.75%、广告收入 +1.53%，并已全量部署。","MovieLens-1M 上比较相邻 NTP 与 BMTP+冻结知识+正交 ACR，执行全库排序。"),
 ("2608.04455","twitch-mor","Multi-Objective Ranking for Live-Streaming: Balancing Fresh and Delayed Signals with Segment-Aware Targeting","Twitch Interactive","2026-08-05",None,"twitch-mor","直播多目标排序","直播观看、互动、关注和付费的反馈延迟不同，且生命周期分群差异明显。论文组合即时/延迟模型、分群目标权重与 MMoE，在共享专家的同时保留目标专属 gate。",("即时行为","延迟窗口","生命周期分群","MMoE 多任务 gate","融合排序"),r"$y_k=\sum_e g_{k,e}(x)f_e(x),\qquad \mathcal L=\sum_k\lambda_k(s)\mathcal L_k$","线上 DAV +0.09%、高参与用户 capped ARPU +0.56%；MMoE 另带来 DAV +0.08%、新关注 +0.27%，移动 live feed 正向互动 +1.12%。","MovieLens-1M 构造五个即时/延迟目标，比较单目标 DNN 与三专家生命周期 MMoE。"),
 ("2608.00750","hrpo","Hierarchical Residual Policy Optimization for Generative Recommendations","City University of Hong Kong / Kuaishou Technology","2026-08-01","https://github.com/Applied-Machine-Learning-Lab/KDD2026-HRPO","hrpo","生成式推荐后训练","最终物品回报直接广播给所有 SID token 会造成稀疏且高方差的信用。HRPO 在用户簇内平滑 prefix utility，再分解 residual token credit 并累积 credit-to-go，最后用 RRPO 做保守更新。",("用户与历史","层级 SID","prefix utility","residual credit-to-go","RRPO"),r"$\delta_t=U(s_{\le t})-U(s_{<t}),\quad G_t=\sum_{j=t}^{T}\delta_j$","快手三个 IAA 场景 Target Cost 分别提升 +0.168%、+0.186% 和 +3.490%；论文同时报告公开数据离线增益。","MovieLens-1M 上构造二进制层级 SID，实际计算 prefix smoothing、residual credit 与 credit-to-go。"),
 ("2608.03382","llm-ts-prior","LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation","NAVER WEBTOON","2026-08-04",None,"llm-ts-prior","LLM 语义先验与冷启动 bandit","新评论缺少交互反馈，但文本已含性别/内容偏好线索。论文把 LLM 语义判断转为 Beta 伪计数，并按性别年龄分群维护 Thompson posterior。",("评论文本","LLM 语义信号","分群 Beta 先验","Thompson sampling","在线反馈更新"),r"$\theta_a\sim\operatorname{Beta}(\alpha_a,\beta_a),\quad \alpha_a=1+\kappa p_a,\ \beta_a=1+\kappa(1-p_a)$","每臂约 59.5 万用户的四周 A/B/C：Gender Prior 总体 CTR +1.48%（p=0.144，不显著），10–49 曝光冷启动段 +9.51%；Content Prior 总体 CTR -5.68%。","以 MovieLens genre 代理文本语义，运行分群 Beta prior 与 40 轮 Thompson 在线更新；明确保留负向及不显著结果。"),
 ("2608.05872","macro","MACRO: Markov Chain Routing of Transformer Layers","Heinrich Heine University Düsseldorf","2026-08-06","https://github.com/Batorskq/MACRO","macro","动态层路由","固定顺序执行所有 Transformer 层并非总是最优。MACRO 用上下文条件 Markov policy 表示 skip、repeat、residual-add 等操作，再用反馈更新路由分布和 top-k Viterbi 解码候选程序，不修改底座权重。",("任务上下文","Markov 路由策略","skip / repeat / add","top-k Viterbi","冻结 LLM"),r"$p(\rho\mid x)=\prod_t\pi(a_t\mid \ell_t,b_t,d_t,x)$","平均准确率相对顺序执行 +5.0%，相对 Dr. LLM +7.2 个点；搜索时间由 14.8 小时降至 1.6 小时（9.4×）。","在确定性分类 mini-suite 搜索 81 条 skip/repeat/residual 路由；同时作为 micro-LLM evolve 的可选结构。"),
 ("2608.05806","hilp","Hierarchical Latent Prediction for Language Models","University of Texas at Austin / Microsoft Research","2026-08-06",None,"hilp","分层 latent 预训练","NextLat 的逐步 latent rollout 会累积误差。HiLP 增加更粗粒度的抽象 latent 目标，让局部状态同时受长时间尺度结构约束。",("token hidden states","局部 latent predictor","时间池化","高层 abstract latent","联合预训练"),r"$\mathcal L=\mathcal L_{NTP}+\lambda_1\lVert\hat z_{t+1}-z_{t+1}\rVert^2+\lambda_H\lVert\hat h_{k+1}-h_{k+1}\rVert^2$","论文在代码与多步推理基准展示更连贯的长时程 belief state，并提高 speculative decoding 效率；摘要未给统一单一提升值。","合成多尺度序列上比较 next-latent 与加入块级 abstract latent 的预测误差；结构也接入 micro-LLM evolve。"),
 ("2608.05326","qevict","QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding","Indian Institute of Technology Roorkee","2026-08-05",None,"qevict","长上下文 KV cache","二元保留/删除无法应对注意力漂移：今天不重要的窗口可能稍后重新活跃。QEvict 设置全精度、量化可恢复、删除三层，累计注意力变化时可将窗口解量化晋升。",("累计注意力","全精度层","量化可恢复层","动态晋升/降级","最低置信删除"),r"$s_i^{(t)}=\gamma s_i^{(t-1)}+a_i^{(t)},\quad q_i\rightarrow f_i\ \text{if }s_i^{(t)}>\tau$","长上下文理解、检索和推理基准持续优于代表性 eviction/quantization 基线；论文摘要未提供统一百分比。","在固定槽位预算的向量 attention 流上执行三层缓存、量化恢复与晋升，比较不可恢复 eviction recall。"),
 ("2608.06291","bakron","BaKron: Efficient Quantization with Kronecker-Factored Hessians","University of California, San Diego","2026-08-06",None,"bakron","二阶量化","GPTQ 通常只利用输入侧曲率；双侧 Kronecker Hessian 更丰富但直接向量化求解昂贵。BaKron 以反对角并行和递归分治实现双侧自适应 rounding。",("权重矩阵","Kronecker Hessian A⊗B","反对角调度","分治 rounding","低比特权重"),r"$\min_{\hat W}\operatorname{vec}(W-\hat W)^\top(A\otimes B)\operatorname{vec}(W-\hat W)$","顺序步数为 O(m+n)，总工作量由 O(m²n²) 降到 O(mn(m+n))，达到 GPTQ 同阶复杂度同时使用双侧曲率。","对随机权重执行 Kronecker 加权 4-bit rounding 与逐行尺度搜索，和全局 GPTQ-style rounding 比较加权误差。"),
 ("2608.05448","dblast","DBLast: Dependent Block Drafting for Stochastic Speculative Decoding","Huawei Technologies Canada","2026-08-05",None,"dblast","推测解码","并行 block drafter 常把位置条件独立化，在高熵采样时难以匹配联合分布。DBLast 用跨位置共享的低秩 latent mixture 建模依赖，并以期望验证长度为训练目标。",("目标模型","低秩 dependent drafter","block proposal","exact verifier","接受前缀"),r"$q(y_{1:B}\mid x)=\int p(z)\prod_{b=1}^{B}q(y_b\mid x,z)\,dz$","Qwen3-4B/8B 上覆盖 GSM8K、MT-Bench、HumanEval 与创作任务，高熵区间持续提高 accepted draft length；摘要未列统一值。","用 32-token Markov target 比较 unigram 独立 proposal 与 rank-4 条件 proposal，并按精确 speculative acceptance 估计接受长度。"),
]

POST = [
 ("2608.06310","rrc","RRC: Unlocking Generative Reward Models in LLM Reinforcement Learning via Ranking-Based Reward Construction","Northeastern University","2026-08-06","https://github.com/wangclnlp/RRC","生成式奖励模型","生成式 RM 擅长相对比较，却被传统 RL 强制压成独立标量。RRC 用组内自竞争排序和少量 anchor 排序构造中心化 reward。",("候选回答组","生成式 RM 比较","self-competitive rank","anchor-guided rank","策略更新"),r"$r_i=\frac{\operatorname{rank}(y_i)-\bar r}{K-1}+\lambda r_i^{anchor}$","AlpacaEval2 由 35.8% 提至 41.3%，ArenaHardV2 由 8.0% 提至 11.2%。"),
 ("2608.05080","rail","Optimizing What Policies Learn From: Recoverability-Aware Rollout Intervention Learning","University of Notre Dame / Amazon","2026-08-05",None,"rollout 预算分配","均匀 rollout 浪费预算，静态启发式又跟不上策略变化。RAIL 把干预位置与方式视为 contextual bandit，并通过 shadow-to-live 轨迹学习 recoverability controller。",("策略状态","shadow intervention","recoverability gain","contextual bandit","live rollout allocation"),r"$a^*(s)=\arg\max_a\mathbb E[\Delta R_{recover}(s,a)-\lambda C(a)]$","在约束 rollout 预算下持续优于均匀 GRPO 及自适应基线；论文摘要未给统一单一提升值。"),
 ("2608.04962","specroll","SpecRoll: Fast-Slow Verifier-Feedback Adaptation for Speculative Reinforcement Learning Rollouts","VNU University of Engineering and Technology / Viettel AI","2026-08-05","https://anonymous.4open.science/r/SpecRoll-26062006","RL rollout 加速","RL 中 target policy 持续变化，静态 drafter 很快过时。SpecRoll 用 future-token heads 提议、Reflex 做无反传的快速隐状态纠偏，并只在持续退化时启动慢速 head 更新；exact verifier 保持采样分布不变。",("演化 target policy","future-token heads","Reflex 快路径","触发式慢更新","稀疏树验证"),r"$\alpha=\min(1,p_\theta(y)/q_\phi(y)),\qquad \mathcal L_{GRPO}\ \text{unchanged}$","5 个 1.5B–14B 模型、3 个数学数据集上生成加速 1.26×–2.15×，端到端加速 1.21×–2.04×。"),
]

AGENT = [
 ("2608.05446","evoharness-rl","EvoHarness-RL: Learning Self-Evolving Runtime Harness for Long-Horizon LLM Agents","University of Illinois Urbana–Champaign / Meta AI","2026-08-05",None,"Harness policy RL","把 Belief、Progress、Experience 暴露为策略可操作的外部状态；先 SFT 学会 harness action，再以成本感知 GRPO 学习何时读写和合并。",("交互轨迹","BPE harness state","harness SFT","cost-aware GRPO","选择性读写"),r"$R=R_{task}-\lambda C_{harness}$","Qwen3-8B 在 ALFWorld 达到 96.9% success，并观察到 harness annealing 与 harness evolution。"),
 ("2608.05810","vag","When Self-Evolution Backfires: Pre-Commit Gating against Skill Contamination in LLM Agents","论文未列机构","2026-08-06",None,"技能进化安全","技能一旦进入上下文会污染后代，事后删除无法彻底回滚。VaG 在写入前依次做结构、行为无害性、语义一致性验证，再以边际收益选择可共同使用的 Hot 技能集合。",("新技能 Cold","三类 critic","Warm 候选","边际收益组合筛选","Hot runtime pool"),r"$M_r=M_{r-1}\cup G(S_r),\quad f(H)=\mathbb E[R(agent\oplus H)]$","Terminal-Bench 2 五轮单调升至 72% pass@1；技能池约小 5×，相对 ungated 最佳轮仍高 10pp。"),
 ("2608.06153","gse","Learning Globally Reusable Skills for Coding Agents","Tianjin University","2026-08-06",None,"全局技能进化","GSE 用 Skill Relation Graph 显式维护技能关系，以聚类合并局部经验，并通过 replay verification 防止过拟合与行为回退。",("局部技能更新","Skill Relation Graph","cluster consolidation","replay verification","全局技能库"),r"$\max_{S,G}\;U(S)-\lambda\operatorname{Conflict}(G)-\mu\operatorname{Regression}(S)$","测试生成 precision/recall 提升 6.1%–34.1% / 31.8%–180.0%；内部工业 Agent F1 +61.4%。"),
 ("2608.06128","cipo","Contextual Information Policy Optimization for Search Agents","Beihang University","2026-08-06",None,"搜索 Agent RL","只奖励最终答案会让检索退化成确认偏见。CIPO 识别受外部证据影响的后续动作，给予 dense turn credit，并与全局 outcome reward 联合优化。",("搜索请求","外部证据","evidence influence","turn-level credit","global outcome"),r"$A_t=\lambda A_t^{evidence}+(1-\lambda)A^{outcome}$","7 个域内/域外基准上减少 prior-driven reasoning，并在多数任务取得最佳或有竞争力结果。"),
 ("2608.04934","state2state","State2State: Environment-Derived Mid-Training for LLM Agents","Tsinghua University AIR / Alibaba Group","2026-08-05","https://github.com/THUNLP-MT/State2State","环境派生中训练","从环境探索自动采样起点与目标状态，用规则化状态匹配做 verifier，形成无需人工任务与专家轨迹的可扩展 mid-training。",("环境探索","起始状态","目标状态","规则 verifier","mid-training + RL"),r"$\tau\sim\pi(\cdot\mid s_0),\quad R=\mathbf 1[T(s_T)=T(s^*)]$","ALFWorld 与 ScienceWorld 多数设置提升；作为下游 RL 初始化时继续改善最终效果与样本效率。"),
 ("2608.06301","harnessopt-bench","HarnessOpt-Bench: Evaluating LLMs at Harness Optimization","Scale AI","2026-08-06",None,"Harness 优化评测","在固定 target-evaluation 预算下，让优化器修改 prompt、工具、控制流和记忆；隐藏测试集与可信执行环境隔离搜索反馈，保留候选版本以供审计。",("seed harness","预算化编辑","可见验证反馈","可信执行边界","隐藏测试归一化增益"),r"$Score=(J(h^*)-J(h_0))/\max(|J(h_0)|,\epsilon)$","5 个前沿模型、4 个下游任务、111 次计分运行表明模型差异大于 coding harness 差异，native harness 并非稳定更优。"),
 ("2608.05886","codegrep","CodeGrep: An RL-Trained Retrieval Agent for LLM Coding Agents","NetEase Guangzhou AI Lab","2026-08-06",None,"代码检索 Agent","以 GRPO 训练 14B 检索 Agent 并行发出 grep/glob/read，多轮缩小候选文件，再交给冻结 coding agent；优化的是下游修复收益而非孤立检索分数。",("issue","并行 grep/glob/read","GRPO 检索策略","候选文件","冻结 coding agent"),r"$R=R_{resolve}-\lambda_{tok}C_{tok}-\lambda_{round}C_{round}$","SWE-Bench Verified 500 题 resolve 25.8%→27.0%（+1.2pp），成功样本 rounds -15%、tokens -19%。"),
 ("2608.04843","memorycpt","MemoryCPT: An End-to-End Agent Memory Framework for Cost-Performance Trade-off","Hong Kong University of Science and Technology / Tencent LIGHTSPEED STUDIOS","2026-08-05",None,"端到端 Agent 记忆","QAD 将离线记忆构建链蒸馏为紧凑模型；QAR 用 RRF 检索和 LoRA summarizer 生成查询相关上下文，并以成本感知 GRPO 优化 Quality per Cost。",("长交互历史","QAD 离线蒸馏","RRF 检索","QAR + GRPO","压缩上下文"),r"$QPC=Q(answer)/C_{inference}$","LoCoMo 与 LongMemEval 上改善质量—成本折衷；消融验证 QAD、RRF、QAR 与成本 reward 的贡献。"),
 ("2608.01597","hindsearch","HindSearch: Trajectory-Level Hindsight Critique for Search-Augmented Reinforcement Learning","Santa Clara University","2026-08-03","https://anonymous.4open.science/r/hindsearch-anon-EBDC","搜索轨迹 hindsight","冻结 judge 利用 gold answer 为失败搜索轨迹生成逐轨迹 critique，把只有成败的稀疏信号转成辅助 on-policy distillation 信号，并与 GRPO 联合。",("搜索 rollout","最终 verifier","失败轨迹","gold-aware critique","GRPO + distillation"),r"$\mathcal L=\mathcal L_{GRPO}+\lambda\mathcal L_{distill}(\pi_\theta,\text{critique})$","论文在搜索增强推理任务报告稳定改善，详情页保留原文口径；本地不把 judge 使用 gold answer 伪装成部署时能力。"),
]

FIRST_AUTHORS = {
    "rrc": "Chenglong Wang", "rail": "Zheyuan Zhang", "specroll": "Nhat Minh Pham",
    "evoharness-rl": "Xuying Ning", "vag": "Linfang Shang", "gse": "Chen Yang",
    "cipo": "Xingyu Guo", "state2state": "Xuanyu Lei",
    "harnessopt-bench": "Varun Ursekar", "codegrep": "Wuya Chen",
    "memorycpt": "Songxin Lei", "hindsearch": "Haowei Liu",
}


def upstream(value: str | None) -> str:
    return f"是：[{value}]({value})" if value else f"否：未发现原作者公开代码（核查日期：{CHECKED}）"


def diagram(nodes) -> str:
    return "flowchart LR\n" + "\n".join(
        f'    N{i}["{node}"]' + (f" --> N{i+1}" if i + 1 < len(nodes) else "")
        for i, node in enumerate(nodes)
    )


def write_reproduction(row) -> None:
    pid, slug, title, org, date, code, adapter, topic, summary, nodes, formula, result, local = row
    code_dir = f"src/auto_research/reproductions/{adapter.replace('-', '_')}/"
    text = f"""# {title}

> **复现级别：核心机制复现。** 论文的中心算子在本地真实执行；生产私有数据、大模型权重或专用服务未复刻，论文结果与本地结果严格分开。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {pid}](https://arxiv.org/abs/{pid}) |
| 公司/机构 | {org} |
| 首次公开日期 | {date}（arXiv v1） |
| 原文开源代码 | {upstream(code)} |
| Adapter | `{adapter}` |
| 本地复现代码 | [`{code_dir}`](https://github.com/daiwk/auto-research/tree/main/{code_dir}) |

## 原始论文总结

### 背景与主要改动

**主题：{topic}。** {summary}

### 主要架构

```mermaid
{diagram(nodes)}
```

### 核心公式

{formula}

### 论文离线与线上效果

{result}

## 本地复现

{local}

运行：

```bash
auto-research reproduce --paper {adapter} --dataset-dir data --seed 42
```

稳定指标保存在 [`metrics/public-seed42.json`](metrics/public-seed42.json)，不提交 checkpoint。

> **本地对照口径**：基线为去掉论文特有机制、其余数据切分与预算相同的 matched control；实验组为 `{adapter}` 核心机制；相对变化见 `public-seed42.json`；跨论文百分比不适用。

## 复现边界

- 本地结果用于验证机制能执行和比较方向，不等价于原论文规模复现。
- 私有特征、线上流量和生产 serving 不可获得；原文线上数值只作为引用。
- 可接入 evolve 的结构已注册为候选；只影响 serving 的系统方法保留为独立可执行 adapter，不冒充可训练 genome。
"""
    target = ROOT / "docs" / "reproductions" / f"{pid}-{slug}" / "README.md"
    target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text)


def write_module(row, module: str) -> None:
    pid, slug, title, org, date, code, topic, summary, nodes, formula, result = row
    local = "src/auto_research/post_training/latest_20260809.py" if module == "post-training" else "src/auto_research/agent_research/latest_20260809.py"
    text = f"""# {title}

> **复现级别：核心机制 mini-suite。** 本地实现执行论文特有的 {topic} 算子；不把确定性小型评测写成论文完整复现。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文链接 | [arXiv {pid}](https://arxiv.org/abs/{pid}) |
| 公司/机构/学校 | {org} |
| 首次公开日期 | {date}（arXiv v1） |
| 原文开源代码 | {upstream(code)} |
| Adapter | `{slug}` |
| 本地复现代码 | [`{local}`](https://github.com/daiwk/auto-research/blob/main/{local}) |

## 原始论文总结

### 背景与主要改动

**主题：{topic}。** {summary}

### 主要架构

```mermaid
{diagram(nodes)}
```

### 核心公式

{formula}

### 论文离线效果

{result}

## 本地复现

稳定指标保存在本论文目录的 `metrics/` 下，不提交 checkpoint 或原始运行目录。

```bash
auto-research {'post-train' if module == 'post-training' else 'agent-research'} --{'algorithm' if module == 'post-training' else 'method'} {slug} {'--dataset arithmetic-smoke --steps 120' if module == 'post-training' else '--benchmark planbench-mini --episodes 120'} --seed 42
```

> **本地对照口径**：`{slug}` 与同一公开 mini-suite 的无该机制控制组比较；仅报告本地产物中的指标，不把原文大模型/真实环境结果移植为本地提升。

## 复现边界

- 复现论文特有的状态、信用或选择算子，而非只改方法名。
- 未运行原文大模型、专有环境或昂贵 judge；这些缺口不会标注为“已接入”。
- `{slug}` 已加入统一 evolve 候选发现；组合 genome 仍受公共评测与预算约束。
"""
    target = ROOT / "docs" / module / f"{pid}-{slug}" / "README.md"
    target.parent.mkdir(parents=True, exist_ok=True); target.write_text(text)


def main() -> None:
    for row in PAPERS: write_reproduction(row)
    for row in POST: write_module(row, "post-training")
    for row in AGENT: write_module(row, "agent-research")
    path = ROOT / "docs" / "research-manifest.json"
    manifest = json.loads(path.read_text())
    records = {(paper["domain"], paper["key"]): paper for paper in manifest["papers"]}
    for domain, rows in (("post-training", POST), ("agent-research", AGENT)):
        for pid, slug, title, org, date, code, topic, *_ in rows:
            records[(domain, slug)] = {
                "domain": domain, "key": slug, "title": title,
                "paper_url": f"https://arxiv.org/abs/{pid}",
                "detail_path": f"{domain}/{pid}-{slug}/README.md",
                "topic": [topic], "first_author": FIRST_AUTHORS[slug],
                "first_author_affiliation": org, "published": date,
                "code": code, "adapter": slug,
            }
    manifest["papers"] = sorted(records.values(), key=lambda p: (p["domain"], p["key"]))
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__": main()
