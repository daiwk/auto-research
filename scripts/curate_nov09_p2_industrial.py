"""Reconcile 18 industrial-route candidates and four preserved production leads.

This is an original-source selection review, not an implementation delivery.
Every disposition has a pinned source witness; high cost is assessed only for
the complete experiment and does not make an unimplemented cheap core done.
"""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup
import fitz

from build_nov09_review_inventory import ledger_row
from route_nov09_title_abstract import load_observations


ARTIFACT = "research-audits/nov09-review-closure/p2-industrial-primary-reviews.json"
INDUSTRIAL_IDS = (
    "2610.27850", "2610.29228", "2610.30769", "2610.34402", "2610.35765",
    "2610.37281", "2610.40182", "2610.41674", "2610.41911", "2611.01647",
    "2611.01786", "2611.02019", "2611.02040", "2611.03113", "2611.04459",
    "2611.06610", "2611.07851", "2611.08572",
)
ADDITIONAL_PRODUCTION_IDS = ("2610.36287", "2611.01695", "2611.04515", "2611.06123")
AVAILABLE = "one A100 or A30, or local Mac; no experiment was started by this review"


SPECS = (
    {
        "id": "2610.27850", "organization": "University of Copenhagen / LUT University",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "DPFR 有独立的新公平性/相关性联合评测方法：按 Pareto 前沿弧长选参考点，再计算二维距离，并提供均匀抽取替换进度的近似前沿。原文实验为六个公开推荐数据集上的四种推荐器与三种公平重排器离线比较，不是生产线上 A/B 或全流量部署。本轮仍按工业推荐门槛不选，而不是声称无原创算法；低成本指标核心未实现，也不贴高成本标签。",
        "locations": ["author block", "§3.3–3.4", "§4 experimental setup and public datasets"],
        "algorithm_assessment": "new DPFR arc-length reference and approximate Pareto-front evaluator; low-cost arithmetic core not implemented",
        "production_evidence": {"kind": "six_public_datasets_offline_evaluation", "online_ab": False, "details": "Amazon Luxury Beauty、MovieLens10M/20M、Last.fm、QK-video、Jester；按时间或随机6:2:2切分。"},
        "upstream_artifact": "https://github.com/theresiavr/robustness-DPFR-recsys-evaluation",
        "checks": [("S3.SS3.SSS0.Px1.p3.1", "not computed based on a percentile"), ("S3.SS4.p1.1", "Oracle2Fair"), ("S4.SS0.SSSx1.p1.1", "six publicly available")],
    },
    {
        "id": "2610.29228", "organization": "Optum",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "论文定义了真实的精确 MILP 药物集合解码器，在冻结 FLAME 分数上联合约束药物数量和 DDI 边预算，不是无方法的临床报告。但验证仅为 MIMIC-III 单一回顾性 EHR 基准，原文明确尚不能建立临床安全性/效用、临床部署需进一步验证。没有本方法真实生产 A/B 或认可的全量部署证据，本轮不作为工业推荐例外；MILP 低成本核心未实现，不将其误标高成本。",
        "locations": ["author block", "MILP formulation", "§6 frozen scorer and split", "§9 limitations"],
        "algorithm_assessment": "new exact safety-constrained set decoder with a frozen scorer; core not implemented",
        "production_evidence": {"kind": "retrospective_clinical_benchmark_only", "online_ab": False, "details": "MIMIC-IIIv1.4约14000次就诊、151药物/1425DDI边，患者不交叉的4:1:1切分；临床部署仍为未来验证。"},
        "checks": [("S6.SS0.SSS0.Px1.p1.1", "frozen drug-level classifier"), ("S6.SS0.SSS0.Px2.p1.1", "no shared patient identifiers"), ("S9.p1.1", "does not establish the clinical safety")],
    },
    {
        "id": "2610.30769", "organization": "Cornell University / Stanford University",
        "track": "agent", "priority": "P1", "decision": "reviewed_deferred", "resolution": "not_reproduced_high_cost",
        "reason": "这是多 Agent 社会反馈/羊群效应的受控研究，不是生产推荐部署：将每个 Agent 的歌曲推荐累积为后续 Agent 可见的社会信号，比较独立、弱影响和强影响世界。完整原文实验为13个模型、每模型12960名Agent、合计168480名Agent且每人两阶段调用，含闭源模型、27B/80B和DeepSeek-R1等；逐世界顺序反馈还限制并行。按用户成本规则不运行完整矩阵。小规模反馈环境/统计组件仍未实现，未把测量研究误称训练算法或已复现能力。",
        "locations": ["author block", "§2.1–2.5", "§3 outcomes", "§4 limitations"],
        "algorithm_assessment": "controlled sequential social-feedback protocol and herding/cascade measurements; small protocol components not implemented",
        "production_evidence": {"kind": "controlled_llm_population_simulation", "online_ab": False, "details": "48首新生成歌词；17个独立演化世界/模型；人类MusicLab只作定性参照，并非严格同任务人机对照。"},
        "cost_assessment": {"source_url": "https://arxiv.org/html/2610.30769v1", "basis": "§2.1两阶段任务、§2.2精确Agent规模、§2.3完整模型列表；原始规模判断，非本地运行估时", "scale": "13模型×12960Agent=168480Agent，每Agent两阶段，独立世界1440、16个影响世界各720；包含多个闭源API及27B/80B模型，影响世界逐Agent顺序反馈。", "available_resource": AVAILABLE, "cost_type": "大规模异构模型推理/API与顺序反馈实验矩阵"},
        "checks": [("S2.SS1", "two stages"), ("S2.SS2", "168,480"), ("S2.SS3", "Qwen3-Next 80B"), ("S2.SS5", "qualitative")],
    },
    {
        "id": "2610.34402", "organization": "University of Antwerp / Froomle",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "论文从 Bernoulli/多项式朴素贝叶斯推导 item similarity，并分析平滑、偏置和已有 cosine 方法的优化解释，属于新相似度方法而非复述。原文用 Amazon Books、MIND、MovieLens25M 离线数据和用户训练/验证/测试划分评估，无本方法生产 A/B 或全量上线证据。保留工业推荐门槛，不因方法便宜而虚构经典例外；算子核心未实现、不标高成本。",
        "locations": ["author block", "Naive Bayes similarity derivations", "§7.1 datasets and evaluation protocol", "conclusion"],
        "algorithm_assessment": "new probabilistically derived item-similarity estimators; core not implemented",
        "production_evidence": {"kind": "offline_public_recommendation_datasets", "online_ab": False, "details": "三公开数据集；MIND只使用点击并忽略impressions，非现网实验。"},
        "checks": [("S7.SS1", "Three datasets"), ("S7.I1.i2.p1.1", "ignoring the impression data")],
    },
    {
        "id": "2610.35765", "organization": "University of Antwerp",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "原文有新 Rasch/activity 零假设与 EM 拟合和共现偏差检验，解释用户活跃度如何造成 phantom correlation，不是无原创分析。MovieLens1M/20M、Last.fm、Amazon Books 上的拟合和模拟属于离线推荐分析，没有本方法生产 A/B 或全量部署。本轮工业推荐门槛不通过；分析组件仍未实现，未用低优先级或数据量大替代该判断。",
        "locations": ["author block", "activity baseline and EM fitting", "§7.1 evaluation datasets", "conclusion"],
        "algorithm_assessment": "new activity-conditioned null model, EM fit and co-occurrence diagnostics; core not implemented",
        "production_evidence": {"kind": "offline_fit_and_simulation_on_four_public_datasets", "online_ab": False, "details": "四公开推荐数据集；Last.fm为假设失败的反例，不是线上系统。"},
        "checks": [("S7.SS1.p1.1", "four datasets"), ("S7.SS1.p2.1", "assumptions fail")],
    },
    {
        "id": "2610.37281", "organization": "Nagoya University / Shenzhen University / Sichuan Agricultural University / Guangdong AI Economy Laboratory / Tongji University",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "RPSD 有明确新 OPD 方法：检索相似用户窗口，用时间感知非平衡OT和MMR筛选特权证据；同一策略作为特权教师，只评分学生已采样completion，以中心化token对数概率差调整credit，教师不另生成答案、推理时不读特权。原文仅为 MovieLens1M/Netflix/MicroLens 离线推荐实验，未证明本方法生产A/B。不能为绕过工业推荐门槛改归后训练；OT/credit低成本核心未实现，也不以4B训练的潜在成本代替资格判断。",
        "locations": ["author block", "RPSD objective and retrieval", "Appendix C implementation and split"],
        "algorithm_assessment": "new retrieval-privileged on-policy self-distillation for recommendation; low-cost OT/token-credit operators not implemented",
        "production_evidence": {"kind": "three_offline_recommendation_datasets", "online_ab": False, "details": "Qwen3-4B LoRA，7:1:2实例切分，每题1目标+9负例，8次学生rollout；教师证据仅训练可见。"},
        "checks": [("A3.p1.1", "student sees only"), ("A3.p2.1", "unbalanced OT"), ("A3.p3.1", "does not generate a separate response")],
    },
    {
        "id": "2610.40182", "organization": "LTCI, Télécom Paris / Institut Polytechnique de Paris",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "CUP 提出条件utility parity的分布稳定性解释，并对ranking-policy混合求解SOCP且给泛化界，确有新且低成本的公平排序核心。原文验证仅为MovieLens1M离线10次切分，估计集求混合权重后在test用户评估；没有本方法生产A/B或全量部署。按工业推荐门槛不选，不能以‘无原创’排除；HTML漏作者栏，已另核固定PDF第一页机构。",
        "locations": ["PDF p1 byline", "conditional utility parity formulation and bounds", "§6.2 setup, results and runtime"],
        "algorithm_assessment": "new conditional utility parity and second-order-cone mixture optimization; low-cost core not implemented",
        "production_evidence": {"kind": "movielens1m_offline_split_evaluation", "online_ab": False, "details": "训练/估计/test用户50/25/25，10次随机划分；19-ranker字典，单前沿点毫秒级。"},
        "checks": [("S6.SS2.p1.1", "MovieLens-1M"), ("S6.SS2.p2.1", "19"), ("S6.SS2.p4.1", "milliseconds")],
        "pdf_checks": [(1, "Institut Polytechnique de Paris")],
    },
    {
        "id": "2610.41674", "organization": "Kempelen Institute of Intelligent Technologies / Comenius University",
        "decision": "rejected", "resolution": "not_selected_this_window_position_and_research_agenda",
        "reason": "已读原文讨论trustworthy multi-stakeholder RS的利益相关方价值、法规与研究议程。贡献是问题梳理和未来技术方向，而非交付一个新独立算法或公共能力基准，本轮不选。Facebook/YouTube等为讨论案例，不是作者Meta/Google归属；未将这类背景词或无A/B关键词自动当成机构/生产证据。",
        "locations": ["author block", "§1–3 position, legal requirements and future research directions"],
        "algorithm_assessment": "position and future research agenda, not a delivered new independent algorithm or public benchmark",
        "production_evidence": {"kind": "position_discussion", "online_ab": False, "details": "平台案例说明治理问题，不是作者新方法的生产实验。"},
        "checks": [("S1", "trustworthy"), ("S3", "future")],
    },
    {
        "id": "2610.41911", "organization": "Northeastern University / Fondazione Bruno Kessler / University of Trento / ISTI-CNR / New York University / Scuola Normale Superiore",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "论文有新的城市推荐反馈仿真框架及tail-boost重排干预，但‘部署后’指三年仿真中的周级重训，不是真平台上线。数据来自2016–2017 Cuebiq轨迹，模拟四座城市/20000居民，原始日程重复并施加容量与距离约束；作者结论明确要求部署前仿真评估且承认计算密集。没有本方法现网A/B或全量部署，本轮按工业推荐门槛不选，不把新仿真方法说成没有算法或将私有轨迹替换成伪造公开数据。",
        "locations": ["author block", "§3.1–3.3", "§4.3 replication", "§5.4 tail-boost", "§6 discussion and limitations"],
        "algorithm_assessment": "new capacity/distance-constrained feedback simulation and tail-boost intervention; components not implemented",
        "production_evidence": {"kind": "mobility_driven_simulation_not_online_deployment", "online_ab": False, "details": "Boston/SanFrancisco/Detroit各4000居民、Chicago8000；四个月训练/两个月离线留出，仿真约三年，每配置五种子。"},
        "checks": [("S3.SS1", "October 2016 to March 2017"), ("S3.SS2", "simulation runs for about three years"), ("S6", "before an algorithm is deployed")],
    },
    {
        "id": "2611.01647", "organization": "Meta Platforms",
        "verified_priority_organizations": ["Meta"], "priority": "P0",
        "verified_priority_authors": ["Ami Tavory", "Yaniv Sheena", "Shaked Bar", "Yair Zagdansky"],
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "Meta作者原文已核。W-BCE确有新低成本核心：对每条已实现value A与loss B，权重A+B、标签B/(A+B)，学习的是条件期望比而不是已实现比值的期望；另有账户异议与组约束定价。原文Ethics明确所有实验为公开回顾性数据，既无生产部署也无新增个人数据。依既定工业推荐证据门槛，本轮拒绝选入，尽管代码已公开且组件便宜；不是无原创/高成本、没有实现。须未来用户具名批准经典/离线例外才重开，不能改归foundation/post-training绕门槛。",
        "locations": ["author block", "§2–4 mechanism", "§5.1 and §6 evaluation", "Ethical Considerations", "Appendix A public artifact"],
        "algorithm_assessment": "new weighted BCE ratio-ranking, account objections and group pricing; low-cost core not implemented",
        "production_evidence": {"kind": "explicitly_no_production_deployment", "online_ab": False, "details": "Ethical Considerations直接声明公开回顾性实验无生产部署；扩大的policy-bank组比较不能声称显著收益。"},
        "upstream_artifact": "https://github.com/atavory/yielding_fairness",
        "reopen_condition": "explicit user-approved classic/offline industrial exception, or new qualifying production evidence",
        "checks": [("Sx1.p1.1", "no production deployment"), ("A1", "github.com/atavory/yielding_fairness")],
    },
    {
        "id": "2611.01786", "organization": "Xi’an Jiaotong University",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "IncVNM有新交互式VNM效用增量学习算法，用有序点击反馈更新随机结果产品的效用并加入熵正则探索。原文§5股票推荐评估明确是有response error的模拟用户、oracle效用驱动点击；§6将真实用户线上实验列为未来研究。不是已有工业A/B，也不能把股票应用标题当成部署证据。本轮工业推荐门槛不通过；低成本效用更新核心未实现、不标高成本。",
        "locations": ["author block", "incremental VNM utility update and exploration", "§5 stock simulation", "§6 future online experiments"],
        "algorithm_assessment": "new incremental VNM utility elicitation from ordinal clicks; core not implemented",
        "production_evidence": {"kind": "simulated_user_with_response_error", "online_ab": False, "details": "风险厌恶模拟用户根据oracle expected utility点击；真实用户线上实验是未来事项。"},
        "checks": [("S5.p2.1", "simulated risk-averse user"), ("S6.p1.1", "Future research may evaluate IncVNM through online experiments")],
    },
    {
        "id": "2611.02019", "organization": "Toronto Metropolitan University / University of Calabria",
        "decision": "out_of_scope", "resolution": "historical_republication_not_new_2026_research",
        "reason": "固定原文版权/出版说明明确这是IEEE Big Data 2022论文的accepted version（pp5494–5503，DOI 10.1109/BigData55660.2022.10020741）。2026年arXiv上传不是2026新研究。MRRRec确有implicit/explicit criteria双路评分再聚合的新方法，原实验为TripAdvisor离线80:10:10与P100/25epochs；本轮按历史重刊出窗结案，不伪称方法无原创或生产未通过是唯一理由，也不自动批准经典例外。",
        "locations": ["front-matter 2022 publication notice", "§III MRRRec", "§IV-B", "§VI conclusion"],
        "algorithm_assessment": "original 2022 multi-criteria/review recommendation model, not a new 2026 method",
        "original_publication": {"year": 2022, "doi": "10.1109/BigData55660.2022.10020741"},
        "production_evidence": {"kind": "historical_offline_experiment", "online_ab": False, "details": "当前上传为2022工作重刊；没有据此把2026水位回退。"},
        "checks": [("@article", "published in the 2022 IEEE International Conference"), ("S4.SS2", "NVIDIA Tesla P100")],
    },
    {
        "id": "2611.02040", "organization": "Toronto Metropolitan University",
        "decision": "out_of_scope", "resolution": "historical_republication_not_new_2026_research",
        "reason": "原文front-matter明确Version of Record为ASONAM 2024 / Springer LNCS、DOI 10.1007/978-3-031-78538-2_6；2026 arXiv日期不等于新方法发表日期。论文确有predefined/implicit/undefined criteria抽取、情感评分与聚合，TripAdvisor/BeerAdvocate各30000评论、80:10:10离线评测；按历史重刊出窗结案，而不是无原创或高成本。",
        "locations": ["front-matter ASONAM2024 notice", "§III mechanism", "§IV-A/IV-C", "§VI conclusion"],
        "algorithm_assessment": "original ASONAM2024 multi-criteria method, not new 2026 research",
        "original_publication": {"year": 2024, "doi": "10.1007/978-3-031-78538-2_6"},
        "production_evidence": {"kind": "historical_offline_experiment", "online_ab": False, "details": "Google Colab是计算工具，不是Google作者机构。"},
        "checks": [("@article", "ASONAM 2024"), ("S4.SS3", "80, 10, 10")],
    },
    {
        "id": "2611.03113", "organization": "Istanbul Technical University",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "这是受控的LLM推荐微调数据预处理研究，含catalog前缀树约束、标题表面形式、prompt多样化和人口平衡/知识增强对照；不是因为提到Meta Llama就成为Meta论文。原文仅MovieLens1M按用户时间留出验证/test、4995用户与Llama3-8B QLoRA单次微调，结论明确需扩展到更多数据和群体。没有本方法线上A/B或全量部署，不绕过工业推荐门槛；可重用预处理组件未实现、未按模型名称武断高成本。",
        "locations": ["author block", "§3 controlled pipeline", "§4.1–4.2", "§6 conclusion"],
        "algorithm_assessment": "controlled recommendation fine-tuning/preprocessing comparisons and constrained output pipeline; components not implemented",
        "production_evidence": {"kind": "single_public_dataset_offline_finetuning", "online_ab": False, "details": "4995用户、119056基础训练样本；validation/test目标按时间隔离；Llama是基础模型引用非作者机构。"},
        "checks": [("S4.SS1.p1.1", "4,995"), ("S4.SS2.p1.1", "Llama-3-8B-Instruct"), ("S6", "beyond one dataset")],
    },
    {
        "id": "2611.04459", "organization": "Independent Researcher / Princeton University",
        "track": "agent", "priority": "P1", "decision": "accepted", "resolution": "accepted_low_cost_public_agent_benchmark_interface_not_implemented",
        "reason": "原文是新公开Agent需求澄清/工具协议基准，而非工业推荐训练模型，可正当归Agent。450任务属于150个固定请求族，volunteer/mixed/hidden只变披露时机；20000册Wikidata目录、LLM-free用户/判分、两个检索接口、冻结快照与全部32976轨迹公开。低成本接口可接入但本轮只审查，未实现/未跑分；原文单Agent结构化panel每prompt约$1–4.4，不给它虚贴高成本。后续接入必须把隐藏条件和gold留在环境/判分端，不暴露给受测Agent。",
        "locations": ["author block", "§3 resource and disclosure protocol", "§4 controlled setup", "§5 validators and scripted agents", "§7 availability/cost", "§8 limitations"],
        "algorithm_assessment": "new public matched-disclosure Agent benchmark and deterministic replay/validator interface; accepted but not implemented",
        "production_evidence": {"kind": "public_agent_benchmark_not_industrial_deployment_claim", "online_ab": False, "details": "判分基于catalog metadata和协议检查，无LLM judge；规则用户不是经人类验证的完整真实用户模型。"},
        "upstream_artifact": "https://github.com/nbharaths/tau-rec/tree/main/data/tracks/books-wikidata-v2",
        "cost_assessment": {"source_url": "https://arxiv.org/html/2611.04459v1", "basis": "§7每Agent结构化panel的实际报告成本", "scale": "450任务/150族，20000册；单Agent结构化运行每prompt约US$1.0–4.4。完整32976轨迹矩阵未重跑。", "available_resource": AVAILABLE, "cost_type": "low-cost deterministic interface/replay; not a high-cost waiver"},
        "gold_access_contract": "Task facts, answer sets and hidden predicate values remain environment/judge-only; agent receives only permitted user/tool replies.",
        "checks": [("S3.p2.1", "450 tasks"), ("S5", "byte for byte"), ("S7.p1.1", "code MIT"), ("S7.p2.1", "1.0–4.4")],
    },
    {
        "id": "2611.06610", "organization": "Universitat Politècnica de Catalunya",
        "source_format": "pdf", "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "HTML固定版本不可用后已改核原始PDF。u-EASE和u-EASE-i是有定义的新闭式协同过滤方法，公开代码可见，不能按标题粗暴当重复评测。原文是Gowalla/Yelp2018/MovieLens1M的80/10/10离线实验；16vCPU实验的各模型/数据集耗时约0.1–24.5分钟，ML1M秒级，闭式组件也不应按标题误贴高成本。没有本方法生产A/B或认可全量部署，本轮工业推荐门槛不通过，低成本闭式核心未实现。",
        "locations": ["PDF p1 byline", "PDF pp6–8 u-EASE/u-EASE-i and protocol", "PDF p10 computation"],
        "algorithm_assessment": "new closed-form user-side EASE and user-item composition; low-cost core not implemented",
        "production_evidence": {"kind": "offline_public_recommender_benchmarks", "online_ab": False, "details": "原文CPU计算数分钟，非生产实验；代码https://github.com/MariodotR/Alternatives_EASE.git。"},
        "upstream_artifact": "https://github.com/MariodotR/Alternatives_EASE.git",
        "pdf_checks": [(1, "Catalunya"), (7, "u-EASE"), (10, "minutes"), (13, "24.5")],
    },
    {
        "id": "2611.07851", "organization": "KAIST / Salesforce AI Research",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "Tasteply是有具体Gaussian attractor加权与global残差偏好场/cosine混合公式的新推荐交互原型，不能说完全没有新机制。原文实证是5名HCI研究者各15分钟探索+25分钟访谈，属于可用性试探，不是生产A/B/全流量证据；context-gated RLHF还是参与者提议的未来扩展。按工业推荐门槛不选；低成本混合算子未实现，不把未来RLHF当成已做后训练。",
        "locations": ["author block", "§2.1–2.3 preference space and scoring", "§3 exploratory evaluation and future work"],
        "algorithm_assessment": "new preference-space UI and explicit attractor/global-field scoring; core not implemented",
        "production_evidence": {"kind": "five_participant_hci_exploratory_study", "online_ab": False, "details": "N=5，无现网随机试验；context-gated反馈学习为未来方向。"},
        "checks": [("S2.SS3", "Gaussian kernel"), ("S3", "5 HCI researchers"), ("S3", "suggest extending")],
    },
    {
        "id": "2611.08572", "organization": "RMIT University",
        "source_format": "pdf", "decision": "out_of_scope", "resolution": "historical_republication_not_new_2026_research",
        "reason": "HTML固定版本404后核原始PDF封面、数字版说明及方法/结论。封面明确RMIT Master of Engineering论文August2003，2026阅读版只做转录/校对/图形重建且不重新验证原研究。因其是2003案例推理学业建议原型的数字重刊，而非2026新算法/评测，按历史重刊出窗结案。保留原型研究存在的事实，不把144页数字版或2003日期误当本轮昂贵新实验。",
        "locations": ["PDF p1 2003 thesis cover and AI disclosure", "PDF p2 digital reading edition scope", "PDF pp108/115 prototype and future production system"],
        "algorithm_assessment": "2003 case-based-reasoning advisement thesis, digitized in2026 without new scientific validation",
        "original_publication": {"year": 2003, "doi": "10.25439/rmt.34846194"},
        "production_evidence": {"kind": "historical_research_prototype_republication", "online_ab": False, "details": "2003历史研究；2026数字化不新增效果验证。"},
        "pdf_checks": [(1, "2003"), (1, "digital"), (2, "2026")],
    },
    {
        "id": "2610.36287", "organization": "Airbnb Inc.", "priority": "P1",
        "decision": "out_of_scope", "resolution": "historical_republication_not_new_2026_research",
        "reason": "这篇有真实全局流量A/B且本方法已生产部署，不能因不是Google/Meta而漏审或误说无线上证据。双目标优化以DCG代理，随机walk+专家重启筛选instant-book阈值，原文A/B报告instant booking+8.20%、booking0.00%、host adoption+0.96%。但固定原文页首明确2018年2月Workshop on Two-sided Marketplace Optimization、版权2018；2026arXiv上传不是新研究。本轮按历史重刊出窗，未自动批准具名经典例外、未实现。",
        "locations": ["front-matter Feb2018 workshop and copyright", "§2.3", "§3.1–3.2", "§4 Table1 real global traffic A/B"],
        "algorithm_assessment": "original2018 constrained dual-objective random-walk threshold optimization; core not implemented",
        "original_publication": {"year": 2018, "venue": "Workshop on Two-sided Marketplace Optimization, Feb2018"},
        "production_evidence": {"kind": "historical_real_global_traffic_ab_and_deployment", "online_ab": True, "details": "learned参数instant bookings+8.20%、总bookings0.00%；host adoption+0.96%；原文明确服务百万用户。"},
        "production_gate_passed": True,
        "checks": [("@article", "Feb 2018"), ("S3.SS1", "10,000"), ("S4", "real global traffic"), ("S4", "8.20%")],
    },
    {
        "id": "2611.01695", "organization": "South China University of Technology / Alibaba Group",
        "track": "agent", "priority": "P1", "decision": "reviewed_deferred", "resolution": "not_reproduced_high_cost",
        "reason": "SPAR定义了可复现的双环自进化机制：商家内episodic memory与跨商家策略假设；LLM归因只让strategy-driven证据进入Beta-Bernoulli置信度，七种最小修订动作/生命周期阈值进化playbook，非普通销售报告。原文真1688线上A/B每组>30000商家，转化+15.8%、高意向+35.8%，不能漏掉。完整实验依赖1642业务真实对话、51603笔记/3637案例设计、GPT-4o多臂多轮与真实生产商家；原文未提供可核验的业务数据公开获取路径、本轮也没有这些资源，按用户成本/资源规则不跑。本轮审查完成，低成本假设账本/归因门控核心仍未实现，未以生产效果替代本地验证。",
        "locations": ["author block", "§3.3–3.5", "§4.1", "§4.3 online A/B", "Appendix B Algorithm1", "limitations"],
        "algorithm_assessment": "new double-loop merchant memory and causal-attribution-gated hypothesis lifecycle/evolution; cheap core not implemented",
        "production_evidence": {"kind": "live_1688_ab_test", "online_ab": True, "details": "每组>30000商家；7日成交定义；对DirectPrompting相对转化+15.8%、M1+35.8%、outreach sessions-9.2%，bootstrap CI和双比例检验p<.001。未把LLM自报causal attribution视为随机因果识别。"},
        "production_gate_passed": True,
        "cost_assessment": {"source_url": "https://arxiv.org/html/2611.01695v1", "basis": "§4.1业务对话/笔记规模与GPT-4o、§4.3生产商家A/B，原始完整评测要求而非本地实测；数据未找到可核验公开路径不等于断言永不公开", "scale": "1642标注真实对话与300回放校验、51603session notes/3637sales cases、GPT-4o多轮多baseline/ablation；真实A/B每组>30000商家。", "available_resource": AVAILABLE, "cost_type": "需原始业务/生产商家资源的大型多轮闭源API与线上实验矩阵，不能在单卡本地重放完整实验"},
        "checks": [("S3.SS3", "Beta-Bernoulli"), ("S3.SS5", "Only outcomes"), ("S4.SS1", "51,603"), ("S4.SS3", "30,000 merchants per group")],
    },
    {
        "id": "2611.04515", "organization": "Meta", "verified_priority_organizations": ["Meta"], "priority": "P0", "track": "agent",
        "verified_priority_authors": ["Brett Daley", "Ilya Gorbachev", "Anubhav Natani", "Nicholas Brown", "Athena Dai", "Rachel Song", "Marcin Pekalski", "Josip Domazet", "Anchal Choubey", "Daniel Ting"],
        "decision": "rejected", "resolution": "not_selected_this_window_industrial_experience_report",
        "reason": "Meta原始作者栏与全文§1–5已核。文章自称conventional Agent设计，报告97skills、固定CLI参数校验、专家知识库、模板typed provenance门禁与防p-hacking经验。它辅助既有A/B结果分析，并非把Agent自身放进随机线上A/B；三类报告模板的受控对照和使用占比不等于新独立算法/公共基准。按获批应用经验报告口径本轮不选，不把Meta优先误解成无条件收录；可借鉴低成本审计/报告门禁但本次未实现。",
        "locations": ["complete author block", "§1–5 original main text", "Tables1–2 and Figure1"],
        "algorithm_assessment": "conventional Agent architecture and industrial lessons, not a newly delivered independent algorithm or public benchmark",
        "production_evidence": {"kind": "production_experimentation_assistant_usage_and_controlled_report_checks", "online_ab": False, "details": "97技能；45%请求为结果分析；Agent计算数字由确定性工具产生。正文无Agent自身随机流量提升实验，不能把被分析的A/B实验当本方法A/B。"},
        "checks": [("S2", "follows a conventional design"), ("S2", "97 skills"), ("S3", "ground-truth answers"), ("S4", "p-hacking")],
    },
    {
        "id": "2611.06123", "organization": "University of Southern California / Amazon Alexa",
        "track": "post-training", "priority": "P1", "decision": "reviewed_deferred", "resolution": "not_reproduced_high_cost",
        "reason": "Alexicon确有真实生产pipeline，新CPU几何crowding verifier与防reward hacking的concept-gated奖励，训练FLUX.2-klein4B的Flow-GRPO LoRA。15.7%→58.7%是1000概念上的独立VLM离线成对判分，不是用户A/B；原文另明确训练模型/verifier已生产部署。附录A原配置8×H200、5000优化步、每步128张512²图且每样本VLM语义调用，显著超单A100/A30低成本范围，因此完整实验不复现。低成本形态学测量/计数reward核心仍未实现，不能把完整高成本豁免冒充组件交付。",
        "locations": ["PDF p1 author affiliations and Amazon internship", "System Overview", "Method verifier/reward", "Experimental Setup", "Results Tables2–3", "Appendix A TableA.1"],
        "algorithm_assessment": "new morphology-plus-GBDT verifier and concept-gated count-based RLVR reward for a flow policy; cheap core not implemented",
        "production_evidence": {"kind": "explicit_production_deployment_and_offline_paired_eval", "online_ab": False, "details": "模型与verifier在Alexa+生产pipeline；1000概念base/finetuned独立VLM判分15.7%→58.7%、McNemar p=3.3e-94，非线上用户A/B。"},
        "cost_assessment": {"source_url": "https://arxiv.org/html/2611.06123v1", "basis": "Appendix A TableA.1直接报告8H200与batch/steps；Method每样本语义VLM；原始配置非本地估计", "scale": "4B DiT+4B Qwen3 encoder，8×H200/ZeRO2，5000steps×128张512×512图、每张10步denoising和VLM概念判断；两LoRA rank轨迹与1000概念成对eval。", "available_resource": AVAILABLE, "cost_type": "明确多GPU大图像flow-policy RL训练与逐样本VLM调用"},
        "checks": [("Sx4.SSx3", "runs on CPU"), ("Sx4.SSx4", "30 %"), ("S1.SSx1", "H200"), ("Sx8", "deployed in production")],
        "pdf_checks": [(1, "University of Southern California"), (1, "Amazon Alexa")],
    },
)


def source_receipt(path: Path, url: str, root: Path) -> dict:
    data = path.read_bytes()
    if not data or (path.suffix == ".pdf" and not data.startswith(b"%PDF")):
        raise ValueError(f"invalid source capture: {path}")
    return {"source_url": url, "source_sha256": sha256(data).hexdigest(),
            "source_capture": path.relative_to(root).as_posix(), "source_bytes": len(data),
            "fetch_result": "success; exact fixed-revision source locally read"}


def build(source_dir: Path) -> tuple[dict, dict]:
    observations, capture_receipts = load_observations(source_dir)
    expected = set(INDUSTRIAL_IDS) | set(ADDITIONAL_PRODUCTION_IDS)
    if {s["id"] for s in SPECS} != expected or len(SPECS) != len(expected):
        raise ValueError("bounded ownership is not covered exactly once")
    rows, protected = [], []
    for original in SPECS:
        spec = dict(original)
        identity, revision = spec["id"], 1
        if max(v for i, v in observations if i == identity) != revision:
            raise ValueError(f"{identity}: a later captured revision needs review")
        metadata = observations[identity, revision]
        fmt = spec.pop("source_format", "html")
        source = source_dir / "p2-industrial" / f"{identity}v{revision}.{fmt}"
        main_url = f"https://arxiv.org/{fmt}/{identity}v{revision}"
        receipts = [source_receipt(source, main_url, source_dir)]
        soup = BeautifulSoup(source.read_text(), "html.parser") if fmt == "html" else None
        witnesses = []
        for location, needle in spec.pop("checks", []):
            node = soup.select_one("article") if location == "@article" else soup.find(id=location)
            text = " ".join(node.get_text(" ", strip=True).split()) if node else ""
            if needle.casefold() not in text.casefold():
                raise ValueError(f"{identity}: missing HTML witness {location}: {needle}")
            witnesses.append({"format": "html", "location": location,
                              "paragraph_sha256": sha256(text.encode()).hexdigest(), "match": needle})
        pdf_checks = spec.pop("pdf_checks", [])
        if pdf_checks:
            pdf = source_dir / "p2-industrial" / f"{identity}v{revision}.pdf"
            if fmt != "pdf":
                receipts.append(source_receipt(pdf, f"https://arxiv.org/pdf/{identity}v{revision}", source_dir))
            with fitz.open(pdf) as document:
                for page, needle in pdf_checks:
                    text = " ".join(document[page - 1].get_text().split())
                    if needle.casefold() not in text.casefold():
                        raise ValueError(f"{identity}: missing PDF witness p{page}: {needle}")
                    witnesses.append({"format": "pdf", "page_one_based": page,
                                      "page_text_sha256": sha256(text.encode()).hexdigest(), "match": needle})
        row = {
            "revision": revision, "title": metadata["title"], "published": metadata["published"],
            "updated": metadata["updated"], "metadata_sha256": metadata["metadata_sha256"],
            "capture": metadata["captures"][0], "metadata_capture": metadata["captures"][0],
            "metadata_capture_sha256": capture_receipts[metadata["captures"][0]],
            "source_url": main_url, "source_sha256": receipts[0]["source_sha256"],
            "source_capture": receipts[0]["source_capture"], "source_receipts": receipts,
            "source_witnesses": witnesses, "track": "recommendation", "priority": "P2",
            "verified_priority_organizations": [], "production_gate_passed": False,
            "review_done": True, "fulltext_review_completed": True, "full_article_read": False,
            "source_review_scope": "bounded original byline, defining contribution, experimental/deployment evidence, original date and relevant cost/limitations; not a whole-article endorsement",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "implementation_status": "not_implemented", "experiments_started": 0, "gpu_runs": 0,
            **spec,
        }
        if fmt == "pdf":
            row["source_access_attempts"] = [
                {"url": f"https://arxiv.org/html/{identity}v1", "outcome": "HTTP404; no HTML original obtained"},
                {"url": main_url, "outcome": "PDF downloaded, first-page byline visually inspected and relevant original pages read"},
            ]
        if row["resolution"] == "not_reproduced_high_cost":
            row.update(full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True,
                       low_cost_core_status="not_implemented; full-experiment waiver does not deliver the component")
        ledger_row(row, ARTIFACT)
        rows.append(row)
        protected.append({"id": identity, "revision": revision, "title": row["title"],
                          "metadata_sha256": row["metadata_sha256"], "metadata_capture": row["metadata_capture"],
                          "source_url": main_url, "source_sha256": row["source_sha256"],
                          "protection_reason": "industrial/production original-source review; never override by P2 title-abstract selection", "review_artifact": ARTIFACT})
    common = {"schema_version": 1,
              "window": {"start": "2026-10-16", "end": "2026-11-09", "timezone": "Asia/Shanghai"},
              "input_inventory_commit": "aedf2d24a996a833c4d8820932a29d5eb04cb04a", "all_sources_exhaustive": False}
    report = common | {
        "scope": "18 industrial-route records plus four preserved production leads; all22 pinned originals checked, zero implementations and zero GPU runs claimed",
        "counts": dict(Counter(row["decision"] for row in rows)),
        "low_cost_core_delivery": "Not part of this review. Acceptance or high-cost complete-experiment closure does not imply an implemented cheap core.",
        "reviews": rows,
    }
    return report, common | {"protected_ids": sorted(expected), "records": protected}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--protected-output", type=Path, required=True)
    args = parser.parse_args()
    report, protected = build(args.source_dir)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.protected_output.write_text(json.dumps(protected, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["counts"]))


if __name__ == "__main__":
    main()
