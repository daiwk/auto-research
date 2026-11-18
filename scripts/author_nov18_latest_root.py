"""Author reviewed paired root paper notes and learning units from fixed sources.

Only small public paper figures are fetched. This is not a translation service
or a model/dataset runner; all prose below is explicitly authored in both languages.
"""

from __future__ import annotations
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen
import fitz
from bs4 import BeautifulSoup
from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov18-latest"
CACHE = ROOT / ".cache/nov18-latest/root"

PAPERS = [
    dict(
        id="2611.22503",
        key="yuanbao-rubric",
        domain="recommendation",
        author="Yu Lu",
        institution="Tencent",
        module="reproductions/yuanbao_rubric_components.py",
        gpu=True,
        topic=["检索与匹配", "大模型与搜索融合"],
        card="recommendation/retrieval-matching",
        compare="recommendation:wesearch",
        figure=2,
        image="overall_framework.png",
        title="From Relevance to Utility: Rubric Alignment in Yuanbao Search",
        name="元宝搜索：Rubric 对齐检索、排序与集合选择",
        cn="传统逐文档相关性不等于给下游推理提供有用证据。元宝先生成查询特定的加权正向标准和扣分标准，用蒸馏标签统一训练召回与四头排序，再用集合奖励训练选择器。低于组均值的轨迹并不接受负优势惩罚，而是按奖励差蒸馏组内最佳轨迹。",
        en="Pointwise relevance need not supply useful evidence for downstream reasoning. Yuanbao builds query-specific weighted positive and negative rubrics, distills labels for retrieval and four-head ranking, and trains subset selection with set-level rewards. Below-mean rollouts imitate the best in-group trajectory with reward-gap weights instead of receiving negative-advantage suppression.",
        formula=r"L_{sel}=L_{GRPO,+}+0.5L_{distill},\quad w_g=r^*-r_g,\quad A_g=(r_g-\bar r)/(\sigma_r+10^{-4}).",
        mechanism_cn="对应§2.1、Eq4–6。正向标准允许多文档共同覆盖，负向标准由任一文档触发扣分；focal pairwise 是标签差减分数差的 hinge，不是普通 CE。两分支分别求均值；较差轨迹的权重作用于同一个最佳轨迹的 token NLL，保留 padding mask、空分支和奖励并列时零更新。参考 KL 由调用者显式提供，不擅自选择估计器。",
        mechanism_en="Sections2.1 and Eqs4–6 are implemented. Positive criteria can be covered collectively and any document can trigger a deduction. Focal pairwise ranking uses a label-gap minus score-gap hinge, not ordinary CE. Each selection branch has its own mean; poor-rollout weights multiply the same best-trajectory token NLL. Padding, empty branches and tied zero updates are preserved. Reference KL is an explicit caller input, not an invented estimator.",
        result_cn="§3.2/Table2：5%生产流量、约280万查询、14天 A/B；单独召回/排序/选择 GSB 相对提升0.40%/3.94%/4.82%，整条链路8.52%。单项和9.16%不可当成全链路效果。这些均为作者线上结果，不是本地实测。",
        result_en="Section3.2/Table2 reports14-day A/B on5% production traffic, approximately2.8M queries: retrieval/ranking/selection individually improve GSB by0.40%/3.94%/4.82%, while the full pipeline improves8.52%. Their9.16% sum is not the end-to-end gain. These are author production measurements, not local results.",
        limits_cn="没有运行 rubric 生成、DeepSeek judge、Qwen 编码器或真实搜索。诊断检查最佳轨迹有蒸馏梯度、失败轨迹没有模仿梯度、奖励不反传、padding 梯度为零；它们不是答案准确率。",
        limits_en="No rubric generator, DeepSeek judge, Qwen encoder or real search is run. Diagnostics check best-trajectory imitation gradients, absent poor-trajectory imitation gradients, detached rewards and zero padding gradients; these are not answer-accuracy scores.",
        contrast_cn="WeSearch用簇和原子文档匹配收缩候选空间；元宝用rubric统一上游标签和最终集合奖励。两者不是同一种SID/召回架构，局部ADC或双分支loss都不能替代端到端搜索验证。",
        contrast_en="WeSearch narrows candidates using clusters and atomic document matching; Yuanbao aligns upstream labels with final subset rewards. They are not the same SID/retrieval architecture, and neither local ADC nor the dual-branch loss replaces end-to-end search validation.",
        qa=[
            (
                "set-utility",
                "为什么逐文档相关性不够？",
                "集合需要覆盖互补信息并避开任一有害证据，单文档高相关不能保证集合效用。",
                "Why is pointwise relevance insufficient?",
                "A set must cover complementary information and avoid any harmful evidence; individually relevant documents need not form a useful set.",
            ),
            (
                "best-imitation",
                "较差轨迹在蒸馏分支学习什么？",
                "按最佳奖励与自身奖励之差，最大化组内最佳轨迹的概率，不是模仿自己的失败轨迹。",
                "What does a poor rollout imitate?",
                "It maximizes the best in-group trajectory likelihood, weighted by its reward gap, rather than imitating its own failure.",
            ),
            (
                "not-wesearch",
                "元宝和WeSearch改动的是同一层吗？",
                "不是。前者统一效用监督并优化集合；后者主要改变簇内原子文档匹配。",
                "Does Yuanbao change the same layer as WeSearch?",
                "No. It aligns utility supervision and subset selection; WeSearch primarily changes atomic matching within cluster-constrained candidates.",
            ),
            (
                "zero-ties",
                "组内奖励全部相同时该怎样？",
                "优势和最佳奖励差都为零；两分支不给虚假策略更新，且padding必须始终无梯度。",
                "What happens when all rewards tie?",
                "Advantages and best-reward gaps are zero, so neither branch fabricates a policy update; padding must still receive no gradient.",
            ),
        ],
    ),
    dict(
        id="2611.22597",
        key="cotti",
        domain="recommendation",
        author="Maolei Huang",
        institution="Alibaba Group",
        module="reproductions/cotti_components.py",
        gpu=True,
        topic=["训练目标与决策优化", "分布漂移与校准"],
        card="recommendation/feedback-multitask-causality",
        compare="recommendation:baff",
        figure=1,
        pdf=(2, [45, 45, 305, 283]),
        title="COTTI: Contrastive Training and Time-Aware Inference for Robust Industrial Recommendation under Promotional Drift",
        name="COTTI：促销漂移中的跨周期对比与时变校准",
        cn="COTTI把训练时历史偏好连续性和上线时促销概率修正分开。CPC比较同一用户常态/促销双视图并用可微门控调节一致性；RW按相对历史距离重加权但截断其梯度；ABA在冻结预测器的logit上添加事件强度与预测头方差决定的有界修正。",
        en="COTTI separates historical preference continuity during training from promotion-time probability correction. CPC uses a differentiable consistency gate on regular/promotion views, RW weights examples by standardized historical distance with stopped gradients, and ABA adds an event- and head-variance-dependent bounded correction to fixed predictor logits.",
        formula=r"\eta_u=1-\sigma(\|z_{reg}-z_{promo}\|^2/(4d)),\quad \omega=\operatorname{sg}\exp[-\gamma(d-\mu_b)/(\sigma_b+\epsilon)],\quad p_{adj}=\sigma(h+\alpha(t)\tanh(\beta U)).",
        mechanism_cn="严格保留Eq6–16：CPC门控用未归一化表示距离并参与反传；RW不裁剪、不均值归一化，权重是正影响量而非可靠性概率；ABA使用预测头多次dropout logit的总体方差，不是全编码器不确定性。事件中心须事先公告、宽度来自历史，幅度只在验证集选；修正只能向上，不能解决过预测。",
        mechanism_en="Eqs6–16 are retained: CPC gates raw representation distances and remains differentiable. RW is neither clipped nor mean-normalized; weights are positive influence factors, not reliability probabilities. ABA uses population variance of repeated head-only dropout logits, not full-encoder uncertainty. The event center is announced beforehand, width comes from history and amplitude is selected on validation. The correction only increases scores and cannot fix overprediction.",
        result_cn="§IV-E：2025-12-01至12-10、25%实时流量、HDR serving control，对照CVR相对+3.14%、RPM+2.68%。12月12日全量轨迹仅描述性；原文未披露分臂比例、随机化单元、分臂计数或权重，不能据此独立判断平衡和干扰。",
        result_en="SectionIV-E reports December1–10,2025 A/B on25% of real-time traffic against serving control HDR: relative CVR+3.14% and RPM+2.68%. The December12 full-rollout trace is descriptive. Arm allocation, randomization unit, arm counts and aggregation weights are not reported, limiting independent balance/interference assessment.",
        limits_cn="本地只运行CPC/RW/ABA张量；没有历史构造、缺失常态视图回退或服务融合策略。保留paid-item新类目召回下降的作者负结果，不能拿整体AUC覆盖探索代价。",
        limits_en="Only CPC/RW/ABA tensors run locally, without history construction, missing-regular-view fallback or serving fusion. The author-reported decline in paid-item recall for novel categories is retained; aggregate AUC does not erase the discovery trade-off.",
        contrast_cn="BAFF按竞价策略干扰过滤日志，COTTI按用户历史距离改变促销样本影响；两种权重/过滤都不自动成为因果无偏估计，COTTI的校准也不能证明A/B日志无污染。",
        contrast_en="BAFF filters logs for bidding-policy interference; COTTI changes promotion-example influence using historical distance. Neither weighting/filtering automatically yields causal unbiasedness, and COTTI calibration does not establish uncontaminated A/B logs.",
        qa=[
            (
                "separate-phases",
                "为什么ABA不直接训练编码器？",
                "它是冻结预测器后的事件logit修正；训练表征由CPC和RW承担，避免把校准与表征学习混在一起。",
                "Why does ABA not retrain the encoder?",
                "It corrects event logits after fixing the predictor; CPC/RW handle representation learning, keeping calibration separate.",
            ),
            (
                "gradient-convention",
                "CPC和RW的门控梯度一样吗？",
                "不同。CPC的eta参与反传，RW的omega只控制监督梯度大小并detach；统一detach会改算法。",
                "Do CPC and RW share the same gradient convention?",
                "No. CPC eta participates in backpropagation; RW omega is detached and only scales supervised gradients. Detaching both changes the algorithm.",
            ),
            (
                "not-causal-filter",
                "COTTI能代替BAFF解决实验干扰吗？",
                "不能。历史距离不是反事实曝光或竞价干扰证据，促销概率修正和实验日志污染是不同问题。",
                "Can COTTI replace BAFF interference handling?",
                "No. Historical distance is not counterfactual exposure/interference evidence; promotion calibration and polluted experiment logs are different problems.",
            ),
            (
                "one-sided",
                "为什么ABA有可能校准更差？",
                "非负事件幅度加tanh方差只能提高概率；某子群已经过预测时会继续推高，应独立看分组校准与新类目召回。",
                "Why can ABA worsen calibration?",
                "A nonnegative event amplitude times tanh variance only raises probabilities. Already-overpredicted groups can worsen, requiring separate subgroup calibration and novel-category recall analysis.",
            ),
        ],
    ),
    dict(
        id="2611.20448",
        key="intentflow",
        domain="recommendation",
        author="Dongjia Zhao",
        institution="Xiaohongshu",
        module="reproductions/intentflow_components.py",
        gpu=True,
        topic=["检索与匹配", "多模态搜索与意图"],
        card="recommendation/retrieval-matching",
        compare="recommendation:wesearch",
        figure=6,
        image="embedding-training.png",
        title="IntentFlow: An Intent-Driven Real-Time Multimodal Search System with Image-Text Queries at Xiaohongshu",
        name="IntentFlow：意图条件多模态搜索与固定索引适配",
        cn="相同图片上的找同款、找搭配和问使用信息需要不同证据，纯视觉相似性不足。IntentFlow将意图层级、可验证三档相关性、agentic数据构造、多模态检索和意图条件重排统一起来。索引固定后只在查询侧进行高层LoRA与六专家残差投影，避免全库重算。",
        en="Finding an exact item, styling an outfit and seeking usage information require different evidence even for the same image. IntentFlow unifies intent hierarchy, verified three-grade relevance, agentic data construction, multimodal retrieval and intent-conditioned reranking. After indexing, query-only upper-layer LoRA and six-expert residual projections avoid recomputing the document corpus.",
        formula=r"f(q)=\operatorname{norm}\left[u_q+0.1\|u_q\|\sum_{j=1}^2\sum_{k=1}^6\alpha_k(q)U_{j,k}V_jh_q\right],\quad L_{KD}=\tfrac12 KL_{q\to d}+\tfrac12 KL_{d\to q}.",
        mechanism_cn="实现Eq16、18–21、24：同一查询门控混合两个共享瓶颈分支（原设置rank8/64），保留冻结基础投影；蒸馏两方向使用相同合法候选并detach教师；CSLS只减去文档对训练query参考库的离线密度项。零初始化up projection是本地稳定初始化约定，原文未明确此初始化，不伪称完整模型配方。",
        mechanism_en="Eqs16,18–21 and24 are implemented: one query gate mixes two shared-bottleneck branches (paper ranks8/64), retaining a frozen base projection. Both distillation directions share valid candidate sets and detach the teacher. CSLS subtracts only offline document density relative to a training-query bank. Zero-initialized up projections are a local stability convention, not an initialization specified by the paper or a complete model recipe.",
        result_cn="Table1为相同生产control的用户级A/B：识别+重排Top4QCTR/QCTR/停留相对+21.65%/+15.12%/+9.66%；加入召回后+28.17%/+18.96%/+12.56%。两配置是累计组合，不等于召回单独贡献。端到端P50为1.07秒，不能将组件分位数直接相加。",
        result_en="Table1 uses the same production control in user-level A/B: recognition+reranking yields relative Top4QCTR/QCTR/dwell lifts21.65%/15.12%/9.66%; adding retrieval yields28.17%/18.96%/12.56%. These cumulative configurations do not isolate retrieval alone. End-to-end P50 is1.07s; component quantiles cannot simply be added.",
        limits_cn="输入仅为外部融合特征和候选分数；没有用规则假装0.8B意图识别器，也未实现完整LoRA/VLM、agentic核验或NDCG权重训练链。文档输入在诊断中保持不变，不意味着语义召回已提升。",
        limits_en="Inputs are externally supplied fused features and candidate scores. No rules impersonate the0.8B recognizer, and the full LoRA/VLM, agentic verification or NDCG-weighted training chain is absent. Unchanged document tensors in diagnostics do not establish improved semantic retrieval.",
        contrast_cn="WeSearch用簇限制候选并原子匹配；IntentFlow先定义请求满足所需证据，再让查询编码适配固定文档空间。一个侧重候选组织，一个侧重意图监督与查询表示，均不能仅凭组件前后向推断线上收益。",
        contrast_en="WeSearch constrains candidates by clusters and atomic matching; IntentFlow defines evidence required by the request and adapts query encoding to a fixed document space. Candidate organization and intent-supervised representations differ, and component gradients prove neither online lift.",
        qa=[
            (
                "intent-not-object",
                "同一块手表图片为什么能改变相关性标签？",
                "找同型号要求实体对应，问表带耐用性允许其他型号提供可迁移的材料/使用证据；标签由完整意图决定。",
                "Why can one watch image yield different relevance labels?",
                "Exact-model search requires entity correspondence, while strap-durability questions can accept transferable material/use evidence from another model.",
            ),
            (
                "shared-bottleneck",
                "残差专家是不是六套独立query encoder？",
                "不是。每个分支共享一个down瓶颈，六套up投影由同一query门控混合；基础投影和文档空间保留。",
                "Are residual experts six independent query encoders?",
                "No. Each branch shares a down bottleneck and mixes six up projections with one query gate, preserving the base projection and document space.",
            ),
            (
                "fixed-index",
                "它和WeSearch的簇约束有什么区别？",
                "固定索引适配改变query如何落入已有文档空间；簇约束改变候选空间组织，两者可组合但不是相互替代。",
                "How does it differ from WeSearch cluster constraints?",
                "Fixed-index adaptation changes how a query maps into existing document space; cluster constraints organize candidates. They can combine but are not substitutes.",
            ),
            (
                "no-test-bank",
                "CSLS参考query能用测试查询吗？",
                "不能用测试分布或标签调参。原文参考库来自训练query，离线密度项随适配模型计算，线上仅校正候选分数。",
                "May the CSLS reference bank use test queries?",
                "Do not tune on test distribution or labels. The paper uses training queries to precompute document density for the adapted model; serving only adjusts candidate scores.",
            ),
        ],
    ),
]

EXAMPLES = {
    "yuanbao-rubric": [
        (
            "教学例：两篇分别覆盖价格与性能仍可共同满足正向标准，但其中任一含过期价格就触发扣分。",
            "Teaching example: separate price/performance documents can cover positive criteria collectively, but either document can trigger an outdated-price penalty.",
        ),
        (
            "教学例：奖励0、1、3时，前两条都向奖励3的token序列蒸馏，权重分别3、2。",
            "Teaching example: with rewards0,1,3, the first two imitate the reward3 token sequence with weights3 and2.",
        ),
        (
            "教学例：ADC距离正确不能证明最终三个证据文档没有重复、缺漏或过期信息。",
            "Teaching example: correct ADC distances do not prove a final evidence set is nonredundant, complete or current.",
        ),
        (
            "教学例：奖励全为2时应为零更新；把padding logp改成极小值也不改变loss。",
            "Teaching example: rewards all equal to2 yield zero update; arbitrarily small padding log probabilities must not change the loss.",
        ),
    ],
    "cotti": [
        (
            "教学例：促销高峰只改ABA的事件幅度，不因此更新历史编码器。",
            "Teaching example: a promotion peak changes the ABA event amplitude without retraining the historical encoder.",
        ),
        (
            "教学例：两视图相同的CPC gate为0.5；RW中低于均值距离的权重可以大于1。",
            "Teaching example: identical views give a CPC gate of0.5; an RW distance below the mean can receive a weight above1.",
        ),
        (
            "教学例：HDR线上control与TEN离线control不能当成同一因果基线。",
            "Teaching example: online HDR and offline TEN are different controls, not interchangeable causal baselines.",
        ),
        (
            "教学例：原概率0.8的过预测样本仍被非负ABA推高，应记录该负结果。",
            "Teaching example: an overpredicted0.8 probability is still raised by nonnegative ABA; retain this adverse result.",
        ),
    ],
    "intentflow": [
        (
            "教学例：同一候选在找同型号时得0/1档，在问皮表带耐用时可得2档。",
            "Teaching example: one candidate can be grade0/1 for an exact-model request but grade2 for a transferable leather-strap durability question.",
        ),
        (
            "教学例：两个分支rank8/64，共享各自down矩阵；gate不是人工意图one-hot。",
            "Teaching example: rank8/64 branches each share a down matrix; their gate is not a hand-written intent one-hot.",
        ),
        (
            "教学例：query残差改变而doc向量逐位不变，只证明固定索引接口成立。",
            "Teaching example: changing query residuals with bitwise-unchanged documents proves only the fixed-index interface.",
        ),
        (
            "教学例：热门文档对训练query平均相似度高，离线密度扣分较大；不能用测试命中率来选k。",
            "Teaching example: a document with high training-query similarity receives a larger density correction; do not choose k using test hit rates.",
        ),
    ],
}

COST_CN = {
    "yuanbao-rubric": "610M生产query-document预训练、0.6B/4B/7B链路、外部大模型judge和14天生产A/B超出单卡/本地短预算，私有语料和流量亦不可用。",
    "cotti": "作者训练使用64A100、20worker和20参数服务器并依赖私有飞猪日志；缺失视图回退、历史构造及选定校准网格也未完全披露。",
    "intentflow": "0.8B多模态全参数学生、2B教师、agentic证据采集与百亿条生产索引的完整矩阵超出短预算，不用规则假装模型。",
    "simq": "五个百万级多向量索引的完整Recall/QPS/构建时间矩阵成本高；PLAID基线另需GPU聚类。本地精确小图构建不等于可扩展HNSW。",
    "unigraph": "268万至884万条、1024维dense加高维sparse的索引矩阵超出短预算；本地有限alpha-cover与beam search不宣称生产吞吐。",
    "dealrank": "六模型、数千query、frontier付费调用和27B本地推理的NDCG/延迟全矩阵不执行；确定性一致ranker仅核验调度性质。",
    "efficient-evals-tensor": "原文三基准、30次切分及大量judge评分的完整矩阵不重采集；新仓库公开已存评分使离线分析可行，但其完整CPU notebook估计约1小时，本轮不运行。原始数据可用不等于每个组件都必须跑全campaign。",
    "cutagent": "8B多模态规划器、70K商品各90–120视频片段、教师数据、TTS/BGM/渲染、397B评审与真实广告流量完整矩阵超出单卡/本地预算。",
}


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def original_figure(p, page):
    assets = page.parent / "assets"
    assets.mkdir(exist_ok=True)
    asset = assets / "paper-figure-01.png"
    html = CACHE / (p["id"] + "v1.html")
    if not asset.exists():
        if p.get("image"):
            url = f"https://arxiv.org/html/{p['id']}v1/{p['image']}"
            with urlopen(url, timeout=30) as response:
                asset.write_bytes(response.read())
            extraction = "original HTML image, no redraw"
        else:
            page_number, rect = p["pdf"]
            doc = fitz.open(CACHE / (p["id"] + "v1.pdf"))
            doc[page_number].get_pixmap(
                matrix=fitz.Matrix(2, 2), clip=fitz.Rect(rect), alpha=False
            ).save(asset)
            extraction = f"fixed v1 PDF page{page_number + 1}, crop{rect}; no redraw"
    else:
        url = (
            f"https://arxiv.org/html/{p['id']}v1/{p['image']}"
            if p.get("image")
            else f"https://arxiv.org/pdf/{p['id']}v1"
        )
        extraction = "original source image or fixed PDF crop; no redraw"
    if not p.get("image"):
        url = f"https://arxiv.org/pdf/{p['id']}v1"
    soup = BeautifulSoup(html.read_text(), "html.parser")
    captions = [
        f.find("figcaption").get_text(" ", strip=True)
        for f in soup.select("figure")
        if f.find("figcaption")
        and __import__("re").search(
            r"(?:Figure|Fig\.)\s*" + str(p["figure"]) + r"[.:]",
            f.find("figcaption").get_text(" ", strip=True),
        )
    ]
    dump(
        assets / "provenance.json",
        {
            "figure": p["figure"],
            "caption": captions[0] if captions else p["title"],
            "source_url": url,
            "source_version": "v1",
            "source_sha256": hashlib.sha256(
                (html if p.get("image") else CACHE / (p["id"] + "v1.pdf")).read_bytes()
            ).hexdigest(),
            "extraction": extraction,
            "file": asset.name,
            "asset_sha256": hashlib.sha256(asset.read_bytes()).hexdigest(),
            "copyright": "Original paper authors; no claim of local generation",
        },
    )


def main():
    from author_nov18_latest_root_extra import PAPERS as EXTRA

    papers = PAPERS + EXTRA
    # Inspected original PDF crops. Avoid clipped diagrams or surrounding prose.
    overrides = {
        "simq": {"figure": 2, "image": "SIMQ-framework.png"},
        "unigraph": {"figure": 3, "pdf": (4, [45, 45, 565, 338])},
        "dealrank": {"figure": 1, "pdf": (0, [48, 490, 612, 647])},
        "efficient-evals-tensor": {"figure": 1, "pdf": (7, [65, 80, 533, 206])},
        "cutagent": {"figure": 2, "pdf": (3, [53, 40, 558, 313])},
    }
    metadata = {
        p["canonical_id"]: p
        for p in json.loads((ROOT / ".cache/nov18-latest/metadata-pool.json").read_text())["papers"]
    }
    metadata["2603.02029"] = {"published": "2026-03-02T16:12:46Z"}
    costs = {p["key"]: p for p in json.loads((AUDIT / "root-preflight.json").read_text())["papers"]}
    catalog = json.loads((ROOT / "docs/research-manifest.json").read_text())
    known = {
        p["domain"] + ":" + p["key"]: ROOT / "docs" / p["detail_path"] for p in catalog["papers"]
    }
    questions, english, proposals = {}, {}, []
    for p in papers:
        p.update(overrides.get(p["key"], {}))
        identity = p["domain"] + ":" + p["key"]
        implemented = bool(p.get("module"))
        gpu = bool(p.get("gpu", False))
        detail = (
            ("recommendation-components" if p["domain"] == "recommendation" else p["domain"])
            + "/"
            + p["id"]
            + "-"
            + p["key"]
            + "/README.md"
        )
        page = ROOT / "docs" / detail
        page.parent.mkdir(parents=True, exist_ok=True)
        published = metadata[p["id"]]["published"]
        url = f"https://arxiv.org/abs/{p['id']}v1"
        code = (
            "https://github.com/google-deepmind/efficient_evals"
            if p["key"] == "efficient-evals-tensor"
            else None
        )
        code_cn = (
            "已验证Google DeepMind官方仓库，Apache-2.0，固定commit `b4421d929d1078631ee890f8e4a776442c816d36`；2026-11-16新开源，不改变3月首发日期。"
            if code
            else "原文给出[作者仓库](https://github.com/mixedbread-ai/dealrank)，本轮公开API返回404，未核验公开代码/许可证，不复制代码。"
            if p["key"] == "dealrank"
            else "原文及其关联链接未找到/未核验公开的本论文专属作者代码。引用依赖或声称集成不等于已核验专属实现。"
        )
        code_en = (
            "Verified official Google DeepMind repository, Apache-2.0, commit `b4421d929d1078631ee890f8e4a776442c816d36`; new code on2026-11-16 does not change the March publication date."
            if code
            else "The paper links [author code](https://github.com/mixedbread-ai/dealrank), but the public API returned404 in this review; public code/license unverified and no code copied."
            if p["key"] == "dealrank"
            else "No publicly verifiable paper-specific author implementation found in the fixed paper and linked sources. Cited dependencies or integration claims are not verified paper-specific code."
        )
        local = (
            "src/auto_research/" + p["module"]
            if implemented
            else "无新增执行代码（review-only；不制造空adapter）"
        )
        command = (
            f"PYTHONPATH=src python -c 'from auto_research.{p['module'][:-3].replace('/', '.')} import diagnostic; print(diagnostic(42, device=\"cpu\"))'"
            if implemented
            else ""
        )
        original_figure(p, page)
        figure_cn = f"![原文 Figure {p['figure']}](assets/paper-figure-01.png)\n\n图片来自[原论文](https://arxiv.org/pdf/{p['id']}v1)，版权归原作者所有；为原图或PDF裁剪，不是本地结果。[出处与SHA256](assets/provenance.json)。"
        figure_en = f"![Original Figure {p['figure']}](assets/paper-figure-01.png)\n\nImage from the [original paper](https://arxiv.org/pdf/{p['id']}v1); copyright belongs to the original authors. Original asset/PDF crop, not local results. [Provenance and SHA256](assets/provenance.json)."
        status_cn = (
            "L1低成本机制组件；不是能力benchmark，未接入Evolve晋级。"
            if implemented
            else "仅收录审查；高成本完整实验不复现，没有本地能力或算法执行结果。"
        )
        status_en = (
            "L1 bounded mechanism component, not a capability benchmark or Evolve promotion."
            if implemented
            else "Review-only admission. High-cost full experiments not reproduced; no local capability or algorithm-execution results."
        )
        formula = ("\n$$\n" + p["formula"] + "\n$$\n") if p.get("formula") else ""
        cn = f"""# {p["name"]}

[English](README-en.md)

> {status_cn}

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [{p["title"]}]({url})；[固定v1全文](https://arxiv.org/html/{p["id"]}v1) |
| 公司 / 作者机构 | 一作 {p["author"]}：{p["institution"]}；按固定v1作者栏核对 |
| 首次公开日期 | {published.replace("T", " ").replace("Z", " UTC")}（arXiv v1） |
| 原作者开源代码 | {code_cn} |
| 本地adapter / 稳定键 | `{p["key"]}`；adapter为null，不冒充完整模型 |
| 本地复现代码目录 | `{local}` |

## 原始论文总结

### 背景与主要改动

{p["cn"]}

<!-- paper-figure:start -->
### 原论文关键图

{figure_cn}
<!-- paper-figure:end -->

### 核心公式
{formula}
{p["mechanism_cn"]}

### 论文离线与线上效果

{p["result_cn"]}

## 本地复现与边界

### 数据协议与代码映射

{p["limits_cn"]}

{("```bash" + chr(10) + command + chr(10) + "```") if command else "本条为review-only，不提供伪训练命令或合成能力指标。"}

### 结果、负控与边界

{status_cn} {("种子42/43/44只验证显式夹具/小张量的数值和梯度，不是三次独立模型能力试验。CPU与实际GPU证据分别保存，不能用作者指标填充本地看板。" if implemented else "不执行外部API、下载模型/私有数据或自动重试；审查DONE不等于论文复现完成。")}

### 高成本完整实验

{COST_CN[p["key"]]} **成本过高，不复现（审查DONE）**；不阻塞已声明的审查闭环，不进入自动训练或补跑队列。

### 同主题对照

{p["contrast_cn"]}
"""
        page.write_text(cn)
        fingerprint = hashlib.sha256(cn.encode()).hexdigest()
        en = f"""<!-- source-sha256: {fingerprint} -->
# {p["title"]}

[简体中文](README.md)

> {status_en}

## Paper information

| Field | Content |
| --- | --- |
| Paper | [{p["title"]}]({url}); [fixed v1](https://arxiv.org/html/{p["id"]}v1) |
| Institution | First author {p["author"]}: {p["institution"]}; fixed-v1 byline checked |
| First publication | {published.replace("T", " ").replace("Z", " UTC")}, arXiv v1 |
| Original source code | {code_en} |
| Local adapter / key | `{p["key"]}`; adapter is null, not a complete model |
| Local implementation | `{local if implemented else "None: review-only, no empty adapter"}` |

## Paper summary

### Motivation and changes

{p["en"]}

<!-- paper-figure:start -->
### Original figure

{figure_en}
<!-- paper-figure:end -->

### Core formulas
{formula}
{p["mechanism_en"]}

### Author results

{p["result_en"]}

## Local implementation and boundaries

### Data protocol and code mapping

{p["limits_en"]}

{("```bash" + chr(10) + command + chr(10) + "```") if command else "Review-only: no pretend training command or synthetic capability metrics."}

### Results, controls and limits

{status_en} {("Seeds42/43/44 check explicit fixtures/small-tensor arithmetic and gradients, not three independent model-capability trials. CPU and actual GPU evidence remain separate. Author scores must not populate local dashboards." if implemented else "No external API, model/private-data download or automatic retry. Review DONE is not complete reproduction.")}

### High-cost full experiments

{costs[p["key"]]["cost_basis"]} **Not reproduced due to high cost; review DONE.** No automatic training/retry queue and no blocking of declared review closure.

### Same-topic comparison

{p["contrast_en"]}
"""
        page.with_name("README-en.md").write_text(en)
        spec = {
            "domain": p["domain"],
            "key": p["key"],
            "title": p["title"],
            "paper_url": url,
            "reviewed_version_url": f"https://arxiv.org/html/{p['id']}v1",
            "reviewed_version": "v1",
            "published": published[:10],
            "published_at": published,
            "detail_path": detail,
            "topic": p["topic"],
            "first_author": p["author"],
            "first_author_affiliation": p["institution"],
            "verified_priority_organizations": ["Google DeepMind"] if code else [],
            "code": code,
            "code_status": code_cn,
            "method_source_sha256": hashlib.sha256(
                (CACHE / (p["id"] + "v1.html")).read_bytes()
            ).hexdigest(),
            "adapter": None,
            "priority": "P0" if code else "P1",
            "intake_class": "new_code_historical_backfill" if code else "new_paper",
            "implementation_status": "component_only" if implemented else "review_only",
            "evaluation_tier": "l1_mechanism" if implemented else None,
            "diagnostic_only": True,
            "promotion_eligible": False,
            "evolve_integrated": False,
            "requires_gpu_validation": gpu,
            "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
            "review_resolution": "not_reproduced_high_cost",
            "review_done": True,
            "automatic_retry": False,
            "automatic_implementation_queue": False,
            "cost_assessment": {
                "source": f"https://arxiv.org/pdf/{p['id']}v1",
                "available_resource": "one A100/A30 or local Mac",
                "paper_configuration": costs[p["key"]]["cost_basis"],
                "decision": COST_CN[p["key"]],
            },
            "summary": p["cn"] + " 本地边界：" + p["limits_cn"],
        }
        if implemented:
            spec.update(
                local_operator="auto_research."
                + p["module"][:-3].replace("/", ".")
                + ".diagnostic",
                local_command=command,
            )
        if code:
            spec.update(
                upstream_revision="b4421d929d1078631ee890f8e4a776442c816d36",
                code_license="Apache-2.0",
            )
        if gpu:
            spec.update(
                gpu_validation_passed=False,
                gpu_validation_artifact=f"docs/gpu-validations/{p['key']}-a100-20261118-latest.json",
            )
        dump(ROOT / f"src/auto_research/paper_specs/catalog/{p['domain']}/{p['key']}.json", spec)
        rows = []
        for index, (qa, level) in enumerate(
            zip(p["qa"], ("basics", "mechanism", "comparison", "implementation"), strict=True)
        ):
            qid, cq, ca, eq, ea = qa[:5]
            ex, enex = (qa[5], qa[6]) if len(qa) == 7 else EXAMPLES[p["key"]][index]
            rows.append(
                {
                    "id": qid,
                    "level": level,
                    "question": cq,
                    "answer": ca,
                    "example": ex,
                    "source_sections": [
                        "背景与主要改动",
                        "核心公式",
                        "数据协议与代码映射",
                        "高成本完整实验",
                        "同主题对照",
                    ],
                    "added": "2026-11-18",
                }
            )
            english[f"qa/{identity}/{qid}"] = {
                "reviewed": True,
                "fields": {"question": eq, "answer": ea, "example": enex},
            }
        questions[identity] = {"questions": rows}
        # Author an integrated contrast, not an index-only membership label.
        other = p["compare"]
        otherpath = known[other]
        revisions = {
            identity: fingerprint,
            other: hashlib.sha256(otherpath.read_bytes()).hexdigest(),
        }
        comparison = {
            "position": p["cn"],
            "tradeoff": p["contrast_cn"],
            "sections": ["背景与主要改动", "核心公式", "同主题对照", "高成本完整实验"],
        }
        question = rows[2]
        proposals.append(
            {
                "paper": identity,
                "target_card": p["card"],
                "source_revisions": revisions,
                "comparison": comparison,
                "analysis": {
                    "title": p["name"] + "：区别机制与能力",
                    "body": p["mechanism_cn"] + " " + p["contrast_cn"],
                    "papers": [identity, other],
                },
                "question": {
                    "id": "cross-nov18-latest-" + p["key"],
                    "question": question["question"],
                    "answer": question["answer"],
                    "example": question["example"],
                    "papers": [identity, other],
                },
                "update": {
                    "date": "2026-11-18",
                    "papers": [identity, other],
                    "summary": p["limits_cn"] + " 完整实验高成本不复现，未作能力或Evolve晋级证据。",
                },
                "english": {
                    "comparison": {"position": p["en"], "tradeoff": p["contrast_en"]},
                    "analysis": {
                        "title": p["key"] + ": distinguish mechanism from capability",
                        "body": p["mechanism_en"] + " " + p["contrast_en"],
                    },
                    "question": english[f"qa/{identity}/{question['id']}"]["fields"],
                    "update": p["limits_en"]
                    + " Full experiments are not reproduced due to high cost; no capability or Evolve-promotion claim.",
                },
            }
        )
    units = question_units({identity: p["questions"] for identity, p in questions.items()})
    for key, value in english.items():
        value["source_sha256"] = units[key].source_sha256
    dump(
        ROOT / "docs/learning/questions/nov18-latest-root.json",
        {"schema_version": 1, "papers": questions},
    )
    dump(
        ROOT / "docs/en/learning/translations/qa-nov18-latest-root.json",
        {"schema_version": 1, "units": english},
    )
    dump(
        AUDIT / "deep-dive-proposals-root.json",
        {
            "schema_version": 1,
            "reviewed_on": "2026-11-18",
            "integration_owner": "root",
            "proposals": proposals,
        },
    )
    print(
        json.dumps(
            {
                "root_papers": len(papers),
                "questions": len(units),
                "deep_dive_proposals": len(proposals),
            }
        )
    )


if __name__ == "__main__":
    main()
