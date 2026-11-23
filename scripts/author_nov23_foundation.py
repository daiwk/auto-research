"""One-shot DISCO proposals; shared catalog and learning integration belong to root.

The source PDF/HTML and visually reviewed crop already exist. No downloads,
experiments, shared banks or GPU-validation claims are performed here.
"""

from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov23-latest"
DATE = "2026-11-23"
IDENTITY = "foundation-models:disco"
PEER = "foundation-models:e-rwsc"
DETAIL = "foundation-models/2611.27104-disco/README.md"
PAPER = "https://arxiv.org/abs/2611.27104v1"
PDF = "https://arxiv.org/pdf/2611.27104v1"
HTML = "https://arxiv.org/html/2611.27104v1"
TITLE = "Reliable Behavior Discovery via False Discovery Rate Control"
SECTIONS = ["背景与主要改动", "核心公式", "同主题比较与边界", "数据协议与代码映射", "高成本完整实验"]

QA = [
    ("patterns-not-cases", "basics",
     "DISCO为什么不能把几条明显失败案例直接算成可靠的行为发现？",
     "行为发现声称的是可重复的输入—输出规律，不是存在一个失败案例。FDR约束最终被拒绝假设集合中的误发现比例的期望；挑出最惊讶的例子没有给出这个多重检验保证。",
     "教学例：发现集合有10条规律，其中2条其实不存在，则该次FDP为2/10；FDR还要对发现过程的重复运行取期望，不能把这一个比例当已知真值。",
     "Why are salient failure examples not automatically reliable DISCO discoveries?",
     "A behavior discovery claims a repeatable input-output pattern, not the existence of one failure. FDR controls the expected false fraction in the final rejected-hypothesis set; selecting surprising examples alone supplies no such multiple-testing guarantee.",
     "Illustration: two nonexistent patterns among ten discoveries give FDP=2/10 for that run. FDR additionally averages over repeated discovery runs; one fraction is not its known value."),
    ("coarsened-selection", "mechanism",
     "为什么二分箱DISCO的假设选择器不能顺便看精确e值或原始模型输出？",
     "允许按实际K做最终eBH的论证需要分箱历史把某个null假设的财富过程与其余探索选择隔开。额外输出可能改变未来选题和假设池规模，破坏该论证；不能只保留冻结规则而偷偷开放精确证据。",
     "教学例：e_max=50时，财富2和20都只显示A。同样轮数、同样A历史必须产生同一选择器视图；根据20比2更接近门槛而改选题，不属于这里的二分箱接口。",
     "Why must a binary-bin DISCO selector not also inspect exact wealth or model outputs?",
     "The observed-K argument uses bin histories to separate a null hypothesis's wealth from other exploration choices. Extra outputs can alter future hypotheses and pool size, breaking that argument. Freezing alone does not permit an exact-evidence side channel.",
     "Illustration: with e_max=50, wealth 2 and 20 both reveal A. Equal update counts and A histories yield identical selector views; selecting differently because 20 is nearer the boundary violates this binary-bin interface."),
    ("majority-vs-discoveries", "comparison",
     "DISCO和e-RWSC都累积e-process，为什么不能共用一种成功证书？",
     "e-RWSC认证同一题某答案在固定政策iid采样中的多数概率，不保证答案正确。DISCO控制多个行为假设最终集合的误发现比例，并有自适应假设池的分箱、冻结和校正约束。认证对象与错误定义不同。",
     "教学例：某LLM每次都答错同一个答案，e-RWSC仍可能很快发多数证书；这不证明十个新提出的行为规律有九个真的存在，也不能代替DISCO的FDR证书。",
     "Why can DISCO and e-RWSC not share one success certificate despite both using e-processes?",
     "e-RWSC certifies one answer's majority probability under a fixed policy's iid sampling, not correctness. DISCO controls false discoveries across a final collection of behavioral hypotheses and constrains adaptive pool selection through coarsening, freezing and correction. Their certified objects and errors differ.",
     "Illustration: a model that always gives the same wrong answer can quickly obtain an e-RWSC majority certificate. That does not establish that nine of ten proposed behavioral patterns exist or replace DISCO's FDR certificate."),
    ("conditional-certificate", "implementation",
     "实现时怎样避免把DISCO的post-hoc证书误报成无条件FDR保证？",
     "分开输出epsilon、delta与条件标志。Theorem2用alpha/epsilon选择最终level，约束没有null退出时的条件FDR；delta描述该条件失败风险。不能套用Theorem1的(alpha-delta)/epsilon公式，也不能把未经误差校正的Monte Carlo均值当严格null上界。",
     "教学例：alpha=0.1、epsilon=0.5、delta=0.02时，pre-hoc校正level为0.16；post-hoc的level为0.2，但必须保留条件限定和0.02风险项。两者数值相近不代表保证相同。",
     "How do we avoid reporting DISCO's post-hoc certificate as unconditional FDR control?",
     "Output epsilon, delta and the conditional flag separately. Theorem2 uses alpha/epsilon for conditional FDR given no true-null exit; delta quantifies failure of that condition. Do not substitute Theorem1's (alpha-delta)/epsilon or treat uncorrected Monte Carlo means as rigorous null bounds.",
     "Illustration: alpha=0.1, epsilon=0.5 and delta=0.02 give pre-hoc level 0.16. The post-hoc level is 0.2, but its condition and 0.02 risk term remain explicit. Similar values do not make the guarantees identical."),
]


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def main():
    outputs = [AUDIT / f"{name}.json" for name in (
        "foundation-authored-bundle", "deep-dive-proposals-foundation",
        "paper-proposals-foundation", "foundation-review")]
    if any(path.exists() for path in outputs):
        raise ValueError("append-once authored proposals already exist")
    directory = ROOT / "docs" / Path(DETAIL).parent
    cache = ROOT / ".cache/nov23-latest/foundation-primary"
    pdf_hash = sha256((cache / "2611.27104v1.pdf").read_bytes()).hexdigest()
    html_hash = sha256((cache / "2611.27104v1.html").read_bytes()).hexdigest()
    image_hash = sha256((directory / "assets/paper-figure-01.png").read_bytes()).hexdigest()
    cn_hash = sha256((directory / "README.md").read_bytes()).hexdigest()
    if f"<!-- source-sha256: {cn_hash} -->" not in (directory / "README-en.md").read_text():
        raise ValueError("English page not reviewed against final Chinese source")
    dump(directory / "assets/provenance.json", {
        "schema_version": 1, "paper_url": PAPER, "source_url": PDF + "#page=2",
        "source_sha256": pdf_hash, "source_pdf_sha256": pdf_hash,
        "pdf_page": 2, "page": 2, "figure": "Figure 1",
        "caption": "Original Figure 1: DISCO behavior-discovery loop; complete original caption retained.",
        "crop_pdf_points": [58, 85, 298, 423], "crop_box_pdf_points": [58, 85, 298, 423],
        "render_scale": 3, "retrieved_on": DATE, "reviewed_version": "v1",
        "asset_sha256": image_hash, "image_sha256": image_hash,
        "extraction": "Original fixed-v1 PDF crop including the complete original caption",
        "visually_reviewed": True, "scientific_content_modified": False,
        "copyright": "Copyright belongs to the original authors.",
    })
    questions, translations = [], {}
    for qid, level, q, a, example, eq, ea, ee in QA:
        questions.append({"id": qid, "level": level, "question": q, "answer": a,
                          "example": example, "source_sections": SECTIONS, "added": DATE})
        translations[qid] = {"question": eq, "answer": ea, "example": ee}
    units = question_units({IDENTITY: questions})
    english = {f"qa/{IDENTITY}/{q['id']}": {
        "source_sha256": units[f"qa/{IDENTITY}/{q['id']}"].source_sha256,
        "reviewed": True, "fields": translations[q["id"]],
    } for q in questions}
    dump(outputs[0], {"schema_version": 1, "date": DATE,
                      "papers": {IDENTITY: {"questions": questions}},
                      "english_question_units": english})
    overview = "DISCO以冻结e-process与粗分箱选择接口控制行为发现集合的FDR，允许最终使用实际假设数；本地仅有未boosted二分箱统计核心。"
    comparison = ("e-RWSC认证单题某答案的政策多数概率，不等于正确性；DISCO控制多行为假设集合的误发现比例，"
                  "并为自适应假设池施加分箱、冻结与null分布校正约束。相同的e-process工具不使两类错误和证书等价。")
    analysis = (comparison + " DISCO的pre-hoc证书给出无条件epsilon-alpha加delta界；post-hoc证书依赖无null退出条件，"
                "须同时保留delta失败概率。有限null路径穷举只验收本地公式与接口，不验证真实LLM的p值有效性，"
                "也不替代原文三分箱/boosted发现器及独立复验。")
    en_overview = "DISCO freezes e-processes and coarsens hypothesis-selection feedback to control collection-level FDR with observed pool size. Local code covers only the unboosted binary-bin statistical core."
    en_comparison = ("e-RWSC certifies one answer's policy-majority probability, not correctness. DISCO controls false discoveries across behavioral hypotheses and constrains adaptive pool size through coarsening, freezing and null-law correction. Shared e-process machinery does not equate their errors or certificates.")
    en_analysis = (en_comparison + " DISCO's pre-hoc certificate is an unconditional epsilon-alpha-plus-delta bound. Its post-hoc certificate is conditional on no true-null exit and must retain the delta failure term. Finite null-path enumeration checks local formulas and interfaces, not real-LLM p-value validity, the three-bin/boosted discoverer or independent replication.")
    revisions = {IDENTITY: cn_hash, PEER: sha256((ROOT / "docs/foundation-models/2611.26413-e-rwsc/README.md").read_bytes()).hexdigest()}
    peer_question = questions[2]
    proposal = {
        "paper": IDENTITY, "target_card": "foundation-models/evaluation-and-evidence",
        "source_revisions": revisions,
        "comparison": {"position": overview, "tradeoff": comparison, "sections": SECTIONS[:3]},
        "analysis": {"title": "DISCO与e-RWSC：发现集合错误不等于单题多数", "body": analysis, "papers": [IDENTITY, PEER]},
        "question": {"id": "nov23-disco", "question": peer_question["question"], "answer": peer_question["answer"],
                     "example": peer_question["example"], "papers": [IDENTITY, PEER]},
        "update": {"date": DATE, "papers": [IDENTITY, PEER], "summary": analysis + " 完整API发现/复验矩阵成本过高，不复现（审查DONE）；不进入自动重试。"},
        "english": {
            "comparison": {"position": en_overview, "tradeoff": en_comparison},
            "analysis": {"title": "DISCO vs e-RWSC: collection errors are not single-question majorities", "body": en_analysis},
            "question": translations[peer_question["id"]],
            "update": en_analysis + " The complete API discovery/replication campaign is too expensive, not reproduced (review DONE), and excluded from automatic retries.",
        },
    }
    dump(outputs[1], {"schema_version": 1, "reviewed_on": DATE,
                      "integration_owner": "root", "proposals": [proposal]})
    local = ("CPU-only unboosted binary-bin Algorithm2, exact finite-null path enumeration and Theorems1/2; no models, datasets, LLM discovery/judging, three-bin boosting or capability evidence.")
    cost = ("Appendix L Tables12-13: 900/600/400/400/400 discovery queries per method across five tasks, plus100 independent verification queries per candidate, with proprietary text/image models. Appendix K adds200 hyperparameter runs per method and1000 fresh-seed runs. Full multi-model/API campaign not attempted; local three-seed scalar component budget below10seconds is an estimate, no data/checkpoint/API downloads.")
    code_status = "论文声明源码位于google-deepmind/disco，但2026-11-23官方GitHub入口HTTP404；可访问代码及commit未核实，不能据此断言作者未发布。"
    spec = {
        "domain": "foundation-models", "key": "disco", "title": TITLE,
        "paper_url": PAPER, "reviewed_version_url": PDF, "reviewed_version": "v1",
        "published": "2026-11-20", "published_at": "2026-11-20T04:25:13Z",
        "announced_on": None, "detail_path": DETAIL,
        "topic": ["评测与可靠性", "行为发现与错误发现率控制"],
        "first_author": "David Madras", "first_author_affiliation": "Google DeepMind",
        "affiliation_evidence": "Fixed-v1 PDF first-page byline: all six authors have affiliation1, Google DeepMind.",
        "verified_priority_organizations": ["Google DeepMind"],
        "code": "https://github.com/google-deepmind/disco", "code_status": code_status,
        "code_license": None, "upstream_revision": None, "method_source_sha256": pdf_hash,
        "adapter": None, "priority": "P0", "intake_class": "new_first_release_in_window",
        "implementation_status": "component_only", "evaluation_tier": "l1_mechanism",
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "local_operator": "auto_research.foundation_models.disco.diagnostic",
        "local_command": "PYTHONPATH=src python -c 'from auto_research.foundation_models.disco import diagnostic; print(diagnostic(42))'",
        "requires_gpu_validation": False, "gpu_validation_passed": False, "gpu_validation_artifact": None,
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
        "review_done": True, "review_resolution": "not_reproduced_high_cost",
        "automatic_retry": False, "automatic_implementation_queue": False,
        "cost_assessment": {"source": PDF, "sections": ["5", "6", "K", "L.1-L.2"],
                            "available_resource": "one A100 or A30, or local Mac",
                            "paper_configuration": cost,
                            "estimated_cost_basis": "Read-only fixed-v1 configuration; no full-model campaign or API probe attempted.",
                            "decision": "成本过高，不复现（审查 DONE）；仅验收低成本CPU统计组件"},
        "summary": overview + " " + local,
    }
    dump(outputs[2], {"schema_version": 1, "date": DATE, "papers": [spec]})
    accepted = {
        "arxiv_id": "2611.27104", "identity": IDENTITY, "key": "disco", "domain": "foundation-models",
        "title": TITLE, "first_author": "David Madras", "first_author_affiliation": "Google DeepMind",
        "first_published_at": spec["published_at"], "announced_on": None,
        "intake_class": spec["intake_class"], "reviewed_version": "v1",
        "reviewed_source_url": PDF, "source_sha256": pdf_hash, "html_sha256": html_hash,
        "sections_read": ["1-4 Algorithm2, Eq1-8, Theorems1-2", "5-6", "K", "L.1-L.2"],
        "implementation_status": "component_only", "evaluation_tier": "l1_mechanism",
        "scope": local, "cost_basis": cost, "local_detail_path": DETAIL,
        "requires_gpu_validation": False, "gpu_validation_passed": False,
        "code_url": spec["code"], "code_status": code_status, "upstream_revision": None,
        "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True,
        "review_done": True, "automatic_retry": False, "automatic_implementation_queue": False,
    }
    dump(outputs[3], {"schema_version": 1, "reviewed_on": DATE,
                      "scope": "Finite Nov20 first-release selection; no all-source exhaustiveness or Nov15 watermark advancement claimed.",
                      "requested_window": ["2026-11-20", DATE],
                      "preflight_before_implementation": True,
                      "available_resource": "one A100 or A30, or local Mac",
                      "large_downloads_authorized_or_needed": False,
                      "watermark_change_claimed": False, "accepted": [accepted],
                      "selection_notes": ["Google DeepMind prioritized; original submission date verified on official arXiv.",
                                          "Paper-linked code entry is unavailable (HTTP404); no upstream commit invented.",
                                          "No second foundation/JEPA implementation added; bounded scope remains one paper.",
                                          "No paid API, checkpoint/data download, full campaign, CUDA path or Evolve promotion."]})
    print("Authored DISCO proposals, four reviewed bilingual questions and one same-topic deep-dive update; shared files untouched.")


if __name__ == "__main__":
    main()
