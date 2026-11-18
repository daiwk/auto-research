"""Build the source-bound, bilingual Nov 18 post-training component bundle.

Only this batch's exclusive files are written. No model/data downloads or runs.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov18-latest/post"

# Descriptions are reviewed against fixed-v1 method sections, not abstract labels.
PAPERS = [
    dict(
        id="2611.23229",
        key="ambient-sft",
        author="Giannis Daras",
        affiliation="Massachusetts Institute of Technology",
        sections=["§3.1 Eq.4 and practical implementation", "§4 Tables2–5"],
        gpu=True,
        tier="l1_mechanism",
        scope="原式CE与同位置温度forward-KL、冻结教师、随机clean/matching分支；不乘T²。",
        scope_en="Exact CE and same-position tempered forward KL, frozen teacher and stochastic clean/matching branches; no T-squared multiplier.",
        cost="§4比较Qwen3 1.7B–14B、OLMo3-7B和Llama3.1-8B，多个域和温度/正则化对照；额外冻结教师前向。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.20687",
        key="sh-opd",
        author="Xinhao Yao",
        affiliation="Renmin University of China",
        sections=["§4 Definition1, Algorithm1, Eq.5–8", "§5", "AppendixA.1"],
        gpu=True,
        tier="l1_mechanism",
        scope="power-survival离散分布、每批共享真实生成cap、标准token-mean OPD及隐式位置权重；不作逆概率去偏。",
        scope_en="Power-survival distribution, one actual generation cap per batch, standard token-mean OPD and implicit position weights; no inverse-probability correction.",
        cost="§3.1/§5用1.5B学生和教师，数学/代码任务，响应上限7168、batch64；数学训练约4500万监督token，多α和多任务扫描。",
        code="https://github.com/chen123CtrlS/SH-OPD",
        license="MIT",
        revision="98467d23930e2197dd0b240af9e37cc7c5c3f505",
    ),
    dict(
        id="2611.20674",
        key="leaf-opd",
        author="Zirui Pang",
        affiliation="The Hong Kong University of Science and Technology (Guangzhou)",
        sections=["§4 Eq.4–7 and teacher criterion", "§5 TOFU/RWKU/MUSE", "AppendixC.2"],
        gpu=True,
        tier="l1_mechanism",
        scope="SS1/SS0.5教师持续监督诊断、teacher-only privileged-context边界、forget/retain分离forward-KL。",
        scope_en="SS1/SS0.5 persistent-supervision diagnostics, teacher-only privileged-context boundary and separate forget/retain forward KL.",
        cost="§5含Llama2-7B、Qwen3-8B及Llama3-8B，TOFU/RWKU/MUSE多基准；需目标模型微调、教师强化SFT、在线采样和保留集对照。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.22298",
        key="streaming-opd",
        author="Yun Zhu",
        affiliation="Independent Researcher, China",
        sections=[
            "§3 Eq.1–6, Table2, Definition1",
            "§4.1 launch resources",
            "§5 stage-wise interventions",
        ],
        gpu=True,
        tier="l1_mechanism",
        scope="保留完整因果prefix的新片段loss mask/version记录、teacher top-k不重归一化截断clip损失、按监督权重归约。",
        scope_en="Full causal prefixes with new-segment loss masks and version tags, unrenormalized teacher-top-k clipped loss and supervision-weighted reduction.",
        cost="§4.1为Qwen3-4B教师/Qwen3-0.6B学生、VERL/vLLM多服务，trainer/generator/teacher分配4/1/1或2/1/1 GPU；响应2048、多预算/陈旧度/续训对照。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.20691",
        key="specal",
        author="Kai Tang",
        affiliation="Zhejiang University / Ant Group",
        sections=["§3 Eq.3–12", "§5 experimental setup"],
        gpu=True,
        tier="l1_mechanism",
        scope="归一化response表示的中心Gram谱、质量×effective-rank带通、LOO去噪SVD条件支持及双层RMS advantage校准。",
        scope_en="Centered Gram spectrum of normalized response representations, mass times effective-rank band-pass, denoised LOO-SVD support and two-level RMS advantage calibration.",
        cost="§5明确8张A100，Qwen3-8B-Base/DeepSeek-R1-Distill-Llama-8B、DeepMath难题、batch128、多数学及OOD评测。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.21791",
        key="regularized-score-centering",
        author="Hao Bai",
        affiliation="University of Illinois Urbana-Champaign",
        sections=["PDFp1 author superscripts", "§3 Eq.3–8", "§5.2 and AppendixA sampling"],
        gpu=True,
        tier="l1_mechanism",
        scope="独立auxiliary actions的加权score center、detached TIS权重、独立KL cap的reverse-KL梯度估计；不是reward减均值。",
        scope_en="Weighted score centers from independent auxiliary actions, detached TIS weights and reverse-KL gradient estimator with an independent KL cap; not reward centering.",
        cost="§5含Qwen3-32B、每题64个rollout、每token32/64/128辅助采样及6个多轮Agent环境；完整异步多任务训练不适合单卡短时验收。",
        code="https://github.com/BiEchi/rsc",
        license=None,
        revision="2fd280c420faa875809d4bb632ad1d2367e229cc",
    ),
    dict(
        id="2611.21766",
        key="margin-dynamics-tpo",
        author="Xingzi Xu",
        affiliation="Amazon",
        sections=["§2.1 Eq.3", "AppendixB Eq.25", "§3 experimental setup"],
        gpu=True,
        tier="l1_mechanism",
        scope="长度归一化分数的TPO-S label-smoothed sigmoid与AppendixB精确归一化Huber TPO-H；验证有限吸引点和有界梯度。",
        scope_en="TPO-S label-smoothed sigmoid on length-normalized scores and Appendix-B normalized-Huber TPO-H; finite-attractor and bounded-gradient checks.",
        cost="§3每个运行Qwen3-8B LoRA rank64、A100-40GB约24GB峰值，seq512；完整实验还有多数据规模/噪声/方法矩阵，并非单次标量loss验证。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.20635",
        key="ca-zodpo",
        author="Weiyun Huang",
        affiliation="Uppsala University",
        sections=["§2 Eq.1–5", "§3 HH-RLHF setup"],
        gpu=True,
        tier="l1_mechanism",
        scope="chosen/rejected activation差的power-iteration子空间、rank归一化双点有限差分、换basis投影的低秩momentum更新。",
        scope_en="Power-iteration subspace of chosen/rejected activation differences, rank-normalized two-point finite differences and basis-transported low-rank momentum.",
        cost="§3 Qwen2.5-1.5B在HH-RLHF先SFT再多种ZO/FO-DPO对照，seq2048；每更新提取basis前向+两次损失前向，完整campaign需真实模型训练/评判。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.20955",
        key="jev-safety-reward",
        author="Eunkyeong Lee",
        affiliation="KT / Sungkyunkwan University",
        sections=["§3.1–3.4", "§4–5", "AppendixC human audit"],
        gpu=False,
        tier="l0_interface",
        scope="固定概率judge的confidence gate、校准集阈值、PHR/GPR分母区分、prompt级bootstrap和judge升级重审规则；不实现商业judge。",
        scope_en="Confidence gate, held-out calibration threshold, distinct PHR/GPR denominators, prompt-level bootstrap and judge-version revalidation; no commercial judge implementation.",
        cost="§3–5每run76800个rollout、11组RL运行、8B策略/8B guard与120B第二参考及商业judge、人类审核；完整安全训练和评判campaign不运行。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.21538",
        key="optimistic-verifier-audit",
        author="Arunkumar V",
        affiliation="University College of Engineering, BIT Campus, Anna University, Tiruchirappalli",
        sections=["§3 Definitions1–2", "§4–5", "AppendixA/B/D"],
        gpu=False,
        tier="l1_mechanism",
        scope="小有限状态域的精确MSR antichain、因果precision/recall/F1、代理selection-error和signed/absolute gap；不伪造LLM训练伤害。",
        scope_en="Exact MSR antichains on small finite state spaces, causal precision/recall/F1 and proxy selection-error/signed/absolute gaps; no simulated LLM damage claims.",
        cost="§3/D完整124416状态、12训练gate/4留出gate、14真实策略、4B/mini多框架精度/adapter/seed训练矩阵；本地只在小枚举域核定义，不跑模型campaign。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.21211",
        key="confidence-adaptive-granularity",
        author="Lukas Ellinger",
        affiliation="Technical University of Munich",
        sections=["§3.1–3.6", "AppendixF/H"],
        gpu=False,
        tier="l0_interface",
        scope="给定已核验hierarchy上的20采样/16共识规则、recognition的逐层全coarser通过规则与归一化information utility；不拿gold选训练共识。",
        scope_en="20-sample/16-vote consensus on externally verified hierarchies, recognition requiring every coarser level to pass and normalized information utility; no gold-driven consensus target selection.",
        cost="§3.6有1.2B/3B/9B/31B四模型，逐实体关系20采样、Wikidata grounding、LoRA及数千题多评判器/人类审核；完整矩阵不运行。",
        code="https://github.com/lukasellinger/teaching-granularity",
        license="MIT",
        revision="5f4b2b53ccd14f30f44257138bcd978b8a6be2f9",
    ),
    dict(
        id="2611.20612",
        key="design-taste-admission",
        author="Sujay Choubey",
        affiliation="固定v1未列一作机构（不由其他作者邮箱推断）",
        sections=["§4 Eq.3–4", "§5–8 training/evaluation"],
        gpu=False,
        tier="l0_interface",
        scope="expert agreement/causal sensitivity/hack resistance/stability四项admission、V0乘性hard gates与已admit分数composite reward；不造浏览器/设计judge能力。",
        scope_en="Four admission tests for expert agreement, causal sensitivity, hack resistance and stability; multiplicative V0 hard gates and admitted-score composite reward, not a browser or design judge.",
        cost="§4–8需Qwen3.5-4B多轮repo编辑/build/Chromium渲染、独立judge ensemble、每维约385专家对和完整RL/消融；人类专家与多模型loop无法以算子单测替代。",
        code="https://github.com/mr-siddy/Tasteful-Designs",
        license=None,
        revision="a3f98e4375df17d3631df9ee9b68762980e30a71",
    ),
    dict(
        id="2611.20755",
        key="gprm",
        author="Zifan Zhang",
        affiliation="Wuhan University",
        sections=["§3.1–3.5", "§4 model and search setup"],
        gpu=False,
        tier="review_only",
        scope="只收录方法和成本；不以字符串parser或固定规则替代4维global PRM。",
        scope_en="Method and cost review only; no string parser or fixed rule replaces the four-dimensional global PRM.",
        cost="§4使用4B/14B PRM、Qwen3-235B-Instruct错误注入/分析教师与7B搜索策略，SFT后GRPO，再Best-of8/逐步续写搜索、多benchmark。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.22210",
        key="mpg-dpo",
        author="Zhen-Yu Zhang",
        affiliation="RIKEN Center for Advanced Intelligence Project",
        sections=["§3 Eq.2–6 and Algorithm1", "§4 models and oracle settings"],
        gpu=False,
        tier="review_only",
        scope="只收录cone+ridge confidence+非支配trade-off主动选对的完整算法；不将一个pair selector宣称完整个性化DPO。",
        scope_en="Review the complete cone, ridge-confidence and nondominated trade-off selection algorithm; a pair selector is not advertised as personalized DPO.",
        cost="§4三个7B系列、每prompt8候选、3seed、86M DeBERTa独立编码器和多个外部LLM偏好oracle，在线score/cone与DPO交替训练；完整多模型campaign高成本。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.23124",
        key="ash-hint-steering",
        author="Khiem Le",
        affiliation="University of Notre Dame",
        sections=["§4 Eq.4–5 and Algorithm1", "§6 experimental settings"],
        gpu=False,
        tier="review_only",
        scope="只收录每步先训练steering再GRPO、hint/plain独立归一化advantage及最后一步不更新model的完整顺序；不把DPO公式当实现。",
        scope_en="Review steering-before-GRPO order, separately normalized hint/plain advantages and final-step no-model-update rule; a DPO formula alone is not an implementation.",
        cost="§6四个1B/1.7B/3B/4B模型、每步hint与plain双组在线生成+steering训练再GRPO，多个竞赛/OOD及pass@8矩阵；完整campaign高成本。",
        code=None,
        license=None,
        revision=None,
    ),
    dict(
        id="2611.22206",
        key="tailroll",
        author="Niloofar Gholipour",
        affiliation="École de technologie supérieure, Canada",
        sections=[
            "§V migration policy and sufficiency termination",
            "§VI–VII Ascend setup and 300-step results",
        ],
        gpu=False,
        tier="review_only",
        scope="只收录多engine真实在途迁移/单次re-prefill与部分输出loss mask机制；不以离线调度模拟声称系统提速。",
        scope_en="Review actual multi-engine in-flight migration, one-time re-prefill and partial-output loss masking; no offline scheduler simulation claims system speedups.",
        cost="§VI–VII在Ascend910C NPU上用Qwen3-14B/32B、多engine/KV迁移、10配置和300step真实RL；现有单卡A100/A30不具同构多engine硬件拓扑。",
        code=None,
        license=None,
        revision=None,
    ),
]

COST_UPDATES = {
    "margin-dynamics-tpo": "§3与Appendix E：每个运行Qwen3-8B LoRA rank64、A100-40GB约24GB峰值，seq512。作者披露完整预算约153 GPU-hours、使用8张A100-40GB，预测/复刻/跨模型/补充实验分别约30/63/18/27小时；标准复刻还含UltraChat-200k一轮SFT、60K偏好对5000步及每方法5种子。不是单次标量loss验证。",
    "ash-hint-steering": "§6及Table4/5明确全部实验使用2张NVIDIA A100 80GB、最大响应4096token；涵盖四个1B/1.7B/3B/4B模型，每步hint与plain双组在线生成、先steering再GRPO，以及多个竞赛/OOD与pass@8矩阵。当前单卡短时预算不覆盖原文双卡完整campaign。",
    "mpg-dpo": "§4明确全部实验在一台4张NVIDIA H100 80GB机器上运行；含三个7B系列、每prompt8候选、3seed、86M DeBERTa独立编码器和多个外部LLM偏好oracle，在线score/cone与DPO交替训练。原文多卡、多模型和外部查询campaign超出本轮单A100/A30短预算。",
}


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def preflight():
    from dataclasses import asdict
    from auto_research.papers import canonical_arxiv_id, parse_arxiv_feed

    metadata = json.loads((ROOT / ".cache/nov18-latest/metadata-pool.json").read_text())
    pool = {p["canonical_id"]: p for p in metadata["papers"]}
    for raw in (CACHE / "arxiv").glob("*.xml"):
        for paper in parse_arxiv_feed(raw.read_bytes()):
            identity = canonical_arxiv_id(paper.arxiv_id)
            pool.setdefault(identity, asdict(paper) | {"repository_status": "new"})
    rows = []
    for row in PAPERS:
        row = row | {"cost": COST_UPDATES.get(row["key"], row["cost"])}
        p = pool[row["id"]]
        source = CACHE / (row["id"] + "v1.html")
        rows.append(
            row
            | {
                "title": p["title"],
                "published_at": p["published"],
                "updated_at": p["updated"],
                "reviewed_version": "v1",
                "source_url": f"https://arxiv.org/html/{row['id']}v1",
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "repository_status_before_batch": p["repository_status"],
                "implementation_status": "review_only"
                if row["tier"] == "review_only"
                else "planned_component_only",
                "review_done": True,
                "full_experiment_status": "not_reproduced_high_cost",
                "automatic_retry": False,
                "automatic_implementation_queue": False,
                "preimplementation_budget": {
                    "checkpoint_download_bytes": 0,
                    "dataset_download_bytes": 0,
                    "paid_api_calls": 0,
                    "local_component_seconds_per_seed_cap": 30,
                    "gpu_component_seconds_per_seed_cap": 30 if row["gpu"] else 0,
                    "cap_scope": "Tiny exact operator/negative-control checks only; not a training campaign.",
                },
            }
        )
    write_json(
        ROOT / "docs/research-audits/nov18-latest/post-review.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-18",
            "owner": "nov18_post_scan",
            "window": {"start": "2026-11-16", "end": "2026-11-18", "whole_end_day_claimed": False},
            "coverage": "Official metadata pool plus fixed-version full-text method/cost review. Source-bound selection, not an all-source exhaustion claim.",
            "google_meta_authorship": "No paper in this fixed post-training list has a verified Google/Meta first-author affiliation. RSC's PDF superscripts map Hao Bai to UIUC; cited Google/Meta models are not affiliations.",
            "accepted": rows,
        },
    )


FIGURES = {
    "ambient-sft": (2, 1, (0.08, 0.50, 0.94, 0.75)),
    "sh-opd": (1, 1, (0.12, 0.23, 0.91, 0.59)),
    "leaf-opd": (2, 1, (0.17, 0.33, 0.49, 0.672)),
    "streaming-opd": (7, 1, (0.115, 0.24, 0.94, 0.65)),
    "specal": (4, 1, (0.08, 0.07, 0.94, 0.42)),
    "regularized-score-centering": (1, 1, (0.115, 0.53, 0.92, 0.88)),
    "margin-dynamics-tpo": (3, 1, (0.1, 0.07, 0.92, 0.32)),
    "ca-zodpo": (4, 1, (0.12, 0.06, 0.92, 0.33)),
    "jev-safety-reward": (2, "Table 1", (0.11, 0.07, 0.89, 0.24)),
    "optimistic-verifier-audit": (4, 1, (0.115, 0.07, 0.92, 0.53)),
    "confidence-adaptive-granularity": (1, 1, (0.51, 0.25, 0.89, 0.54)),
    "design-taste-admission": (3, 1, (0.1, 0.07, 0.92, 0.43)),
    "gprm": (1, 1, (0.1, 0.50, 0.92, 0.88)),
    "mpg-dpo": (2, 1, (0.09, 0.07, 0.94, 0.345)),
    "ash-hint-steering": (5, 2, (0.15, 0.08, 0.9, 0.27)),
    "tailroll": (1, 1, (0.505, 0.43, 0.93, 0.73)),
}

REPRESENTATIVES = {
    "preference-and-alignment": ("post-training:dpo", "post-training/2305.18290-dpo/README.md"),
    "policy-optimization": ("post-training:grpo", "post-training/2402.03300-grpo/README.md"),
    "reward-and-credit": (
        "post-training:bait-reward-defense",
        "post-training/2611.16369-bait-reward-defense/README.md",
    ),
    "teacher-and-context": (
        "post-training:lcs-reference-opd",
        "post-training/2611.13135-lcs-reference-opd/README.md",
    ),
    "student-trajectory-distillation": (
        "post-training:opd-lm",
        "post-training/2606.06712-opd-lm/README.md",
    ),
    "data-and-budget": (
        "post-training:grpo-dropout",
        "post-training/2610.11854-grpo-dropout/README.md",
    ),
}
TOPICS = {
    "ambient-sft": "preference-and-alignment",
    "sh-opd": "data-and-budget",
    "leaf-opd": "teacher-and-context",
    "streaming-opd": "student-trajectory-distillation",
    "specal": "policy-optimization",
    "regularized-score-centering": "policy-optimization",
    "margin-dynamics-tpo": "preference-and-alignment",
    "ca-zodpo": "preference-and-alignment",
    "jev-safety-reward": "reward-and-credit",
    "optimistic-verifier-audit": "reward-and-credit",
    "confidence-adaptive-granularity": "preference-and-alignment",
    "design-taste-admission": "reward-and-credit",
    "gprm": "reward-and-credit",
    "mpg-dpo": "preference-and-alignment",
    "ash-hint-steering": "policy-optimization",
    "tailroll": "data-and-budget",
}
COMPARE_OVERRIDES = {
    "sh-opd": (
        "GRPODropout先完成rollout再按熵贡献筛样本，不能节省同一轮生成；SH-OPD在生成前共享采样cap，改变深度曝光和实际生成预算。现有Dropout真实checkpoint的负结果也说明公式执行不等于能力收益。",
        "GRPODropout filters completed rollouts by entropy contribution and does not save that round's generation. SH-OPD samples a shared cap before generation, changing depth exposure and actual budget. Existing Dropout checkpoint negative results also separate formula execution from capability gains.",
    ),
    "streaming-opd": (
        "OPDLM把AR教师与双向扩散学生的状态/目标对齐；Streaming OPD仍沿因果prefix计分，只改变交付和消费时序。旧OPDLM候选诊断不是实际扩散decoder，当前prefix/损失核也不是异步服务性能证据。",
        "OPDLM aligns AR-teacher targets with bidirectional diffusion-student states. Streaming OPD retains causal prefixes and changes delivery/consumption timing. The existing OPDLM candidate diagnostic is not a real diffusion decoder; the new prefix/loss kernel likewise is not asynchronous-service performance evidence.",
    ),
    "gprm": (
        "Bait对外部reward的probe/policy差做防御变换，不判断推理step；GPRM学习带预测历史和未来trajectory的四维过程模型。二者都要隔离scorer信息，但不能用Bait数值核或标签parser替代PRM。",
        "Bait defensively transforms an external probe/policy reward gap, not reasoning-step correctness. GPRM learns a four-axis process model with predicted history and future trajectories. Both require scorer isolation, but neither Bait algebra nor a label parser substitutes for a PRM.",
    ),
    "ash-hint-steering": (
        "GRPO消除critic但仍依赖同组相对reward；ASH在hint/plain双组上分别标准化，在GRPO之前另训activation steering并在最终步停model更新，防止返回stale向量。旧GRPO候选成功率不能当无hint生成能力。",
        "GRPO removes the critic but still relies on relative rewards within a group. ASH normalizes hinted/plain groups separately, trains activation steering before GRPO and skips the final model update to avoid a stale vector. Existing candidate GRPO success is not hint-free generation capability.",
    ),
}
COMPARE_QUESTIONS = {
    "sh-opd": (
        "SH-OPD与GRPODropout都减少监督，为何不能只比较保留样本数？",
        "Why not compare SH-OPD and GRPODropout only by retained sample count?",
        "教学例：预先cap到4token不同于已生成8token后删除半数响应；生成成本必须分别统计。",
        "Teaching example: capping generation at four tokens differs from generating eight then filtering responses; generation costs require separate accounting.",
    ),
    "streaming-opd": (
        "Streaming OPD与OPDLM都改变蒸馏，为什么不是同一种状态/效率优化？",
        "Why are Streaming OPD and OPDLM not the same state/efficiency optimization?",
        "教学例：一个保留因果prefix改变消费时钟，另一个需双向去噪状态；两种小组件都不直接给出系统吞吐或扩散生成能力。",
        "Teaching example: one retains causal prefixes and changes consumption clocks; the other needs bidirectional denoising states. Neither small component establishes throughput or diffusion-generation capability.",
    ),
    "gprm": (
        "GPRM能否由现有Bait reward防御组件加一个标签parser得到？",
        "Can GPRM be obtained by adding a label parser to the existing Bait reward-defense component?",
        "教学例：Bait翻转reward不识别当前推理step是否与未来推导一致；[CORRECT]可解析也不代表判断正确。",
        "Teaching example: Bait reward flipping does not assess consistency of a reasoning step with later derivation; parsing [CORRECT] is not judging it correctly.",
    ),
    "ash-hint-steering": (
        "已有GRPO实现是否足以宣称ASH无hint行为迁移已接入？",
        "Does an existing GRPO implementation establish ASH hint-free behavior transfer?",
        "教学例：分别归一化hint/plain组后，还需先更新真实activation向量再更新model，并在最后一步停model更新。",
        "Teaching example: separately normalizing hinted/plain groups still requires actual activation-vector training before the model and no model update on the final step.",
    ),
}


def build_bundle():
    import importlib
    import fitz
    from nov18_post_content import CONTENT
    from english_learning_sources import question_units

    audit = ROOT / "docs/research-audits/nov18-latest"
    reviewed = json.loads((audit / "post-review.json").read_text())
    qbank, english, proposals = {}, {}, []
    for row in reviewed["accepted"]:
        key = row["key"]
        content = CONTENT[key]
        identity = "post-training:" + key
        module = key.replace("-", "_")
        detail = Path(f"post-training/{row['id']}-{key}/README.md")
        directory = ROOT / "docs" / detail.parent
        directory.mkdir(parents=True, exist_ok=True)
        assets = directory / "assets"
        assets.mkdir(exist_ok=True)
        pdf = CACHE / (row["id"] + "v1.pdf")
        page_no, figure_no, norm = FIGURES[key]
        document = fitz.open(pdf)
        page = document[page_no - 1]
        w, h = page.rect.width, page.rect.height
        bbox = fitz.Rect(norm[0] * w, norm[1] * h, norm[2] * w, norm[3] * h)
        image = assets / "paper-figure-01.png"
        page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=bbox, alpha=False).save(image)
        source_url = f"https://arxiv.org/pdf/{row['id']}v1#page={page_no}"
        write_json(
            assets / "provenance.json",
            {
                "schema_version": 1,
                "reviewed_on": "2026-11-18",
                "figures": [
                    {
                        "file": image.name,
                        "paper_id": row["id"],
                        "version": "v1",
                        "figure": figure_no,
                        "page_number": page_no,
                        "source_url": source_url,
                        "source_kind": "fixed_v1_pdf_rendered_crop",
                        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
                        "image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                        "crop_pdf_points": list(bbox),
                        "render_scale": 3,
                        "dpi": 216,
                        "caption_included": True,
                        "visual_review_done": False,
                        "scientific_content_modified": False,
                        "attribution": "Copyright belongs to the original authors. Original figure reproduced with caption for research explanation; not a local result.",
                        "license": "Original fixed-version arXiv paper; author copyright retained. Figure reproduced for attributed research commentary, not code relicensing.",
                    }
                ],
            },
        )
        review_only = row["tier"] == "review_only"
        component = (
            None
            if review_only
            else importlib.import_module("auto_research.post_training." + module)
        )
        per_seed = (
            []
            if review_only
            else [component.diagnostic(seed, device="cpu") for seed in [42, 43, 44]]
        )
        if any(not all(x["checks"].values()) for x in per_seed):
            raise ValueError("failed component checks: " + key)
        local_path = None if review_only else f"src/auto_research/post_training/{module}.py"
        if not review_only:
            write_json(
                directory / "metrics/component-cpu-seeds42-44.json",
                {
                    "schema_version": 2,
                    "key": key,
                    "device": "cpu",
                    "diagnostic_only": True,
                    "evaluation_tier": row["tier"],
                    "per_seed": per_seed,
                    "capability_comparison": False,
                    "promotion_eligible": False,
                    "evolve_integrated": False,
                    "checkpoint_calls": 0,
                    "dataset_downloads": 0,
                },
            )
        code_cn = (
            (
                f"[作者仓库]({row['code']})；固定SHA `{row['revision']}`；"
                + (
                    "许可 " + row["license"]
                    if row["license"]
                    else "未找到项目级许可，不复制上游源码"
                )
                + "。仅核对发布证据，未执行上游训练。"
            )
            if row["code"]
            else "固定v1及所核作者入口未找到可验证的本篇方法源码发布；引用的训练器、模型或库不算本篇开源。"
        )
        code_en = (
            (
                f"[Author repository]({row['code']}); verified revision `{row['revision']}`; "
                + (
                    "licence " + row["license"]
                    if row["license"]
                    else "no project-level licence verified; upstream source not copied"
                )
                + ". Release evidence only; upstream training not executed."
            )
            if row["code"]
            else "No verifiable method-source release found in fixed v1 or the bounded author entry points checked. Referenced trainers, models and libraries are not this paper's source release."
        )
        stamp = row["published_at"].replace("T", " ").replace("Z", " UTC")
        tier_cn = (
            "仅方法与成本收录，无本地模型实现"
            if review_only
            else row["tier"] + " 独立组件，diagnostic only"
        )
        status = (
            "> **"
            + tier_cn
            + "。** 完整实验成本过高，不复现（审查 DONE）；不自动重试、不进入Evolve晋级。\n"
        )
        source_note = "；".join(row["sections"])
        lines = [
            f"# {row['title']}",
            "",
            "[English](README-en.md)",
            "",
            status,
            "## 论文信息",
            "",
            "| 字段 | 内容 |",
            "| --- | --- |",
            f"| 论文链接 | [arXiv {row['id']}v1](https://arxiv.org/abs/{row['id']}v1)；[固定v1原文]({row['source_url']}) |",
            f"| 公司 / 作者机构 | 一作 **{row['author']}**：**{row['affiliation']}**；不把所用Google/Meta模型当作者机构 |",
            f"| 首次公开日期 | **{stamp}**，原始arXiv提交，不替换成公告或本次审查日期 |",
            f"| 原作者开源代码 | {code_cn} |",
            f"| 本地 adapter / key | `{key}`；`adapter: null` |",
            f"| 本地复现代码 | {'无；完整实验不复现，不创建占位模型' if review_only else '`' + local_path + '`'} |",
            "",
            "## 原始论文总结",
            "",
            "### 背景与主要改动",
            "",
            content["questions"][0][1],
            "",
            content["questions"][1][1],
            "",
            "<!-- paper-figure:start -->",
            "### 原论文关键图",
            "",
            f"[![原论文 {figure_no if isinstance(figure_no, str) else 'Figure ' + str(figure_no)}](assets/paper-figure-01.png)]({source_url})",
            "",
            f"图片来自[原论文]({source_url})第{page_no}页，版权归原作者所有；完整保留图与原图注，未重绘/改数值。来源、裁剪与SHA见[provenance](assets/provenance.json)。图表中的结果属于作者，不是本地实验。",
            "<!-- paper-figure:end -->",
            "",
            "```mermaid",
            "flowchart TD",
            f'    I["{key}: 外部合法输入"] --> M["论文特有方法与约束"]',
            f'    M --> C["{row["scope"]}"]',
            '    C --> B["组件诊断或仅收录；无能力晋级"]',
            "```",
            "",
            "### 核心公式",
            "",
            f"固定v1位置：{source_note}。",
            "",
            "$$",
            content["formula"],
            "$$",
            "",
            "### 论文离线与线上效果",
            "",
            content["result"],
            "",
            "## 成本决策与本地状态" if review_only else "## 本地复现",
            "",
            "### 数据协议与代码映射",
            "",
            row["scope"],
            "",
            content["questions"][3][1],
            "",
        ]
        if not review_only:
            lines += [
                "```bash",
                f"PYTHONPATH=src python -c 'from auto_research.post_training.{module} import diagnostic; print(diagnostic(42, device=\"cpu\"))'",
                "PYTHONPATH=src python -m pytest -q tests/post_training/test_nov18_latest_post_components.py",
                "```",
                "",
                "### 结果、负控与边界",
                "",
                f"已实际执行CPU seeds42/43/44；[指标](metrics/component-cpu-seeds42-44.json)仅记录算子与负控，不含任务成功率。"
                + (
                    "CUDA验证由统一批次真实A100/A30回执验收，未完成前不得称GPU已通过。"
                    if row["gpu"]
                    else "此协议仅支持CPU，不宣称CUDA路径。"
                ),
                "",
                "、".join(per_seed[0]["checks"]) + "。",
                "",
            ]
        else:
            lines += [
                "### 结果、负控与边界",
                "",
                "没有本地模型运行、checkpoint下载、数据集下载、付费API调用或伪造metrics文件。保留未复现状态，不将审查DONE改称实现完成。",
                "",
            ]
        lines += [
            "### 高成本完整实验",
            "",
            row["cost"],
            "",
            "**完整实验成本过高，不复现（审查 DONE）**。成本依据来自原文配置而非本地测速；只在明确小算子预算内工作，不为证明高成本探跑大模型。单卡A100/A30或Mac不能替代论文完整多模型/多任务/专家与系统对照。",
            "",
        ]
        cn = "\n".join(lines)
        (directory / "README.md").write_text(cn)
        cn_sha = hashlib.sha256(cn.encode()).hexdigest()
        english_cost = (
            "The original configuration is recorded verbatim with source locations in the cost assessment. It involves "
            + {
                "ambient-sft": "Qwen3 1.7B–14B plus OLMo/Llama, multiple domains/temperature baselines and a frozen teacher forward.",
                "sh-opd": "1.5B teacher/student, math/code sweeps, batch 64, 7,168 response tokens and roughly 45 million supervised math tokens.",
                "leaf-opd": "7B/8B models, TOFU/RWKU/MUSE, target-model preparation, teacher SFT, online rollouts and retention controls.",
                "streaming-opd": "Qwen3-4B/0.6B and separate VERL/vLLM services allocating 4/1/1 or 2/1/1 GPUs to trainer/generator/teacher.",
                "specal": "eight A100s, two 8B model families, batch 128, difficult DeepMath and multiple math/OOD evaluations.",
                "regularized-score-centering": "Qwen3-32B, 64 rollouts per prompt, 32/64/128 auxiliary actions per token and six agent environments.",
                "margin-dynamics-tpo": "approximately 153 GPU-hours using eight A100-40GB GPUs, 24GB peak per Qwen3-8B LoRA run, UltraChat-200k SFT and 60K-pair/5,000-step/five-seed preference replication.",
                "ca-zodpo": "Qwen2.5-1.5B HH-RLHF SFT and several ZO/first-order DPO comparisons, with basis extraction and two perturbed forwards each update.",
                "jev-safety-reward": "76,800 rollouts per run, eleven RL runs, 8B policies/guards, a 120B second reference, commercial judges and human audit.",
                "optimistic-verifier-audit": "124,416 contexts, multiple gates/public policies and 4B/mini model, framework, precision, adapter and seed training comparisons.",
                "confidence-adaptive-granularity": "1.2B/3B/9B/31B models, twenty samples per entity-relation, grounding, LoRA, thousands of QA items and human/model judges.",
                "design-taste-admission": "a 4B multi-turn editing policy, real Chromium builds/renders, independent judge ensembles and about 385 expert pairs per dimension.",
                "gprm": "4B/14B PRMs, a Qwen3-235B synthesis teacher, SFT/GRPO and 7B best-of-eight/step-wise completion search.",
                "mpg-dpo": "four NVIDIA H100 80GB GPUs, three 7B families, eight responses per prompt, three seeds, an 86M DeBERTa encoder and several external preference oracles.",
                "ash-hint-steering": "two NVIDIA A100 80GB GPUs, 4,096 response tokens, four 1B–4B policies, hinted/plain online groups and steering-then-GRPO math/OOD sweeps.",
                "tailroll": "Qwen3-14B/32B, multiple Ascend 910Cs and real engine migration/re-prefill across ten configurations and 300-step training.",
            }[key]
        )
        en_status = (
            "Review only; no local model implementation"
            if review_only
            else row["tier"] + " standalone component; diagnostic only"
        )
        en = [
            f"# {row['title']}",
            "",
            f"<!-- source-sha256: {cn_sha} -->",
            "",
            "[简体中文](README.md)",
            "",
            f"> **{en_status}.** Full experiments are not reproduced due to high cost (review DONE). No automatic retries or Evolve promotion.",
            "",
            "## Paper information",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Paper | [arXiv {row['id']}v1](https://arxiv.org/abs/{row['id']}v1); [fixed v1]({row['source_url']}) |",
            f"| First author / institution | {row['author']}; {'The fixed v1 does not state the first author affiliation; not inferred from another author email.' if key == 'design-taste-admission' else row['affiliation']} |",
            f"| Original publication | {stamp}; original submission, not announcement/review date |",
            f"| Original source code | {code_en} |",
            f"| Local adapter / key | `{key}`; `adapter: null` |",
            f"| Local code | {'None; no placeholder model' if review_only else '`' + local_path + '`'} |",
            "",
            "## Original paper summary",
            "",
            "### Background and defining changes",
            "",
            content["questions"][0][4],
            "",
            content["questions"][1][4],
            "",
            "<!-- paper-figure:start -->",
            "### Original paper figure",
            "",
            f"[![Original {figure_no if isinstance(figure_no, str) else 'Figure ' + str(figure_no)}](assets/paper-figure-01.png)]({source_url})",
            "",
            f"From [fixed v1]({source_url}), PDF page {page_no}. Copyright belongs to the original authors. The original panel and caption are preserved without scientific edits; source/crop/SHA are in [provenance](assets/provenance.json). Author results are not local measurements.",
            "<!-- paper-figure:end -->",
            "",
            "### Core equations",
            "",
            f"Read source locations: {source_note}.",
            "",
            "$$",
            content["formula"],
            "$$",
            "",
            "### Paper results and production evidence",
            "",
            content["result_en"],
            "",
            "## Cost decision and local status" if review_only else "## Local component",
            "",
            "### Data contract and code mapping",
            "",
            row["scope_en"],
            "",
            content["questions"][3][4],
            "",
        ]
        if not review_only:
            en += [
                "```bash",
                f"PYTHONPATH=src python -c 'from auto_research.post_training.{module} import diagnostic; print(diagnostic(42, device=\"cpu\"))'",
                "PYTHONPATH=src python -m pytest -q tests/post_training/test_nov18_latest_post_components.py",
                "```",
                "",
                "### Results, negative controls and limits",
                "",
                "CPU seeds 42/43/44 were executed. [Metrics](metrics/component-cpu-seeds42-44.json) contain operator/control results, not task-success rates. "
                + (
                    "A real A100/A30 receipt must pass the batch GPU gate before CUDA validation is claimed."
                    if row["gpu"]
                    else "CPU-only protocol; no CUDA path is advertised."
                ),
                "",
                ", ".join(per_seed[0]["checks"]) + ".",
                "",
            ]
        else:
            en += [
                "### Results and limits",
                "",
                "No local model run, checkpoint/data download, paid API call or invented metric file. Review DONE does not mean implementation completed.",
                "",
            ]
        en += [
            "### High-cost full experiment",
            "",
            english_cost,
            "",
            "**The high-cost full experiment is not reproduced (review DONE).** This is a source-configuration assessment, not a local timing claim. Only declared tiny-operator checks are allowed; no large-model probe is run to prove cost. No capability comparison or Evolve integration is claimed.",
            "",
        ]
        (directory / "README-en.md").write_text("\n".join(en))
        questions = []
        for index, q in enumerate(content["questions"]):
            record = {
                "id": [
                    "defining-problem",
                    "mechanism-boundary",
                    "compare-existing",
                    "implementation-integrity",
                ][index],
                "level": ["basics", "mechanism", "comparison", "implementation"][index],
                "question": q[0],
                "answer": q[1],
                "example": q[2],
                "source_sections": [
                    "背景与主要改动",
                    "核心公式",
                    "结果、负控与边界" if not review_only else "结果、负控与边界",
                ],
                "added": "2026-11-18",
            }
            questions.append(record)
            unit = question_units({identity: [record]})
            unit_id = next(iter(unit))
            english[unit_id] = {
                "source_sha256": unit[unit_id].source_sha256,
                "reviewed": True,
                "fields": {"question": q[3], "answer": q[4], "example": q[5]},
            }
        qbank[identity] = {"questions": questions}
        row["implementation_status"] = "deferred_high_cost" if review_only else "component_only"
        row["local_module"] = local_path
        row["english_source_sha256"] = cn_sha
        cost = {
            "source": row["source_url"],
            "source_sections": row["sections"],
            "basis": row["cost"],
            "available_resource": "Single NVIDIA A100/A30 or local Mac",
            "decision": "Full experiment not reproduced due to high cost; review DONE. No checkpoint/data download or paid API call.",
            "local_budget": row["preimplementation_budget"],
        }
        spec = {
            "domain": "post-training",
            "key": key,
            "title": row["title"],
            "paper_url": f"https://arxiv.org/abs/{row['id']}v1",
            "reviewed_version_url": row["source_url"],
            "reviewed_version": "v1",
            "detail_path": detail.as_posix(),
            "first_author": row["author"],
            "first_author_affiliation": row["affiliation"],
            "published": row["published_at"][:10],
            "published_at": row["published_at"],
            "code": row["code"],
            "code_status": code_cn,
            "code_license": row["license"],
            "upstream_revision": row["revision"],
            "adapter": None,
            "topic": [TOPICS[key], "后训练算法组件"],
            "priority": "P1",
            "intake_class": "new_submission_in_requested_window",
            "implementation_status": row["implementation_status"],
            "diagnostic_only": True,
            "promotion_eligible": False,
            "evolve_integrated": False,
            "requires_gpu_validation": row["gpu"],
            "gpu_validation_passed": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
            "review_done": True,
            "review_resolution": "not_reproduced_high_cost",
            "automatic_retry": False,
            "automatic_implementation_queue": False,
            "cost_assessment": cost,
            "summary": content["questions"][0][1] + " " + row["scope"],
        }
        if not review_only:
            spec.update(
                evaluation_tier=row["tier"],
                local_operator=f"auto_research.post_training.{module}.diagnostic",
                local_command=f"PYTHONPATH=src python -c 'from auto_research.post_training.{module} import diagnostic; print(diagnostic(42))'",
            )
        else:
            spec["deferral_reason"] = (
                row["cost"]
                + " 完整实验成本过高，不复现（审查DONE）；不以固定规则或公式占位冒充模型/系统实现。"
            )
        write_json(ROOT / f"src/auto_research/paper_specs/catalog/post-training/{key}.json", spec)
        topic = TOPICS[key]
        peer, peer_path = REPRESENTATIVES[topic]
        peer_sha = hashlib.sha256((ROOT / "docs" / peer_path).read_bytes()).hexdigest()
        comparison, comparison_en = COMPARE_OVERRIDES.get(
            key, (content["questions"][2][1], content["questions"][2][4])
        )
        body = content["questions"][1][1] + " " + comparison + " 本轮边界：" + row["scope"]
        body_en = (
            content["questions"][1][4] + " " + comparison_en + " Local boundary: " + row["scope_en"]
        )
        q_cn, q_en, ex_cn, ex_en = COMPARE_QUESTIONS.get(
            key,
            (
                content["questions"][2][0],
                content["questions"][2][3],
                content["questions"][2][2],
                content["questions"][2][5],
            ),
        )
        proposed_q = {
            "id": "nov18-" + key,
            "question": q_cn,
            "answer": comparison,
            "example": ex_cn,
            "papers": [identity, peer],
        }
        proposals.append(
            {
                "paper": identity,
                "target_card": "post-training/" + topic,
                "source_revisions": {identity: cn_sha, peer: peer_sha},
                "comparison": {
                    "position": row["scope"],
                    "tradeoff": comparison,
                    "sections": ["背景与主要改动", "核心公式", "论文离线与线上效果"],
                },
                "analysis": {
                    "title": content["questions"][1][0],
                    "body": body,
                    "papers": [identity, peer],
                },
                "question": proposed_q,
                "update": {
                    "date": "2026-11-18",
                    "papers": [identity, peer],
                    "summary": row["scope"] + " 完整实验高成本不复现；组件诊断不等于能力比较。",
                },
                "english": {
                    "comparison": {"position": row["scope_en"], "tradeoff": comparison_en},
                    "analysis": {"title": content["questions"][1][3], "body": body_en},
                    "question": {"question": q_en, "answer": comparison_en, "example": ex_en},
                    "update": row["scope_en"]
                    + " The high-cost full experiment is not reproduced; component diagnostics are not capability comparisons.",
                },
            }
        )
    write_json(
        ROOT / "docs/learning/questions/nov18-latest-post.json",
        {"schema_version": 1, "papers": qbank},
    )
    write_json(
        ROOT / "docs/en/learning/translations/qa-nov18-latest-post.json",
        {"schema_version": 1, "units": english},
    )
    write_json(
        audit / "deep-dive-proposals-post.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-18",
            "integration_owner": "root",
            "proposals": proposals,
        },
    )
    write_json(audit / "post-review.json", reviewed)


def render_reviewed_figures(*, visual_reviewed=False):
    """Only crop/provenance output; never reset accepted GPU or catalog state."""
    import fitz

    for row in PAPERS:
        key = row["key"]
        page_no, figure_no, norm = FIGURES[key]
        assets = ROOT / f"docs/post-training/{row['id']}-{key}/assets"
        provenance = json.loads((assets / "provenance.json").read_text())
        pdf = CACHE / (row["id"] + "v1.pdf")
        document = fitz.open(pdf)
        page = document[page_no - 1]
        w, h = page.rect.width, page.rect.height
        bbox = fitz.Rect(norm[0] * w, norm[1] * h, norm[2] * w, norm[3] * h)
        image = assets / "paper-figure-01.png"
        page.get_pixmap(matrix=fitz.Matrix(3, 3), clip=bbox, alpha=False).save(image)
        fig = provenance["figures"][0]
        fig.update(
            crop_pdf_points=list(bbox),
            image_sha256=hashlib.sha256(image.read_bytes()).hexdigest(),
            visual_review_done=visual_reviewed,
        )
        write_json(assets / "provenance.json", provenance)


def refresh_cost_records():
    """Propagate verified resource disclosures without resetting GPU state."""
    import re

    audit = ROOT / "docs/research-audits/nov18-latest"
    review = json.loads((audit / "post-review.json").read_text())
    proposals = json.loads((audit / "deep-dive-proposals-post.json").read_text())
    for row in review["accepted"]:
        if row["key"] not in COST_UPDATES:
            continue
        row["cost"] = COST_UPDATES[row["key"]]
        spec_path = ROOT / f"src/auto_research/paper_specs/catalog/post-training/{row['key']}.json"
        spec = json.loads(spec_path.read_text())
        spec["cost_assessment"]["basis"] = row["cost"]
        if row["implementation_status"] == "deferred_high_cost":
            spec["deferral_reason"] = (
                row["cost"]
                + " 完整实验成本过高，不复现（审查DONE）；不以固定规则或公式占位冒充模型/系统实现。"
            )
        write_json(spec_path, spec)
        directory = ROOT / f"docs/post-training/{row['id']}-{row['key']}"
        digest = hashlib.sha256((directory / "README.md").read_bytes()).hexdigest()
        en = directory / "README-en.md"
        en.write_text(
            re.sub(
                r"<!-- source-sha256: [a-f0-9]{64} -->",
                f"<!-- source-sha256: {digest} -->",
                en.read_text(),
            )
        )
        row["english_source_sha256"] = digest
        for p in proposals["proposals"]:
            if p["paper"] == "post-training:" + row["key"]:
                p["source_revisions"][p["paper"]] = digest
    write_json(audit / "post-review.json", review)
    write_json(audit / "deep-dive-proposals-post.json", proposals)


if __name__ == "__main__":
    import sys

    if "--refresh-costs" in sys.argv:
        refresh_cost_records()
    elif "--figures-only" in sys.argv:
        render_reviewed_figures(visual_reviewed="--accept-visual-review" in sys.argv)
    else:
        preflight()
    if "--build" in sys.argv:
        build_bundle()
