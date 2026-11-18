"""Pin original-source dispositions for eight residual production/workflow leads."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup
import fitz

from build_nov09_review_inventory import ledger_row
from curate_nov09_p2_industrial import source_receipt
from route_nov09_title_abstract import load_observations


ARTIFACT = "research-audits/nov09-review-closure/p2-residual-industrial-reviews.json"
SPECS = (
    {
        "id": "2610.26369", "organization": "Eramet / Mines Paris PSL", "format": "pdf",
        "decision": "rejected", "resolution": "not_selected_this_window_prototype_and_unevaluated_benchmark_blueprint",
        "reason": "EI2ROC原文明确分开已实现原型、参考设计和未来工作：测试环境在Eramet真实矿场、少量dispatcher、单一模型配置；schema/auth/scope/rate/audit门禁在运行，但HSE独立规则未强制执行，benchmark harness尚未实现、场景库仍建设，明确没有受控任务/安全/运营效果评价。四条示例查询只展示开销和时延，其他行业量化收益是引文，不能当成本系统A/B。按本轮原型/方法蓝图而非交付公共评测的选题口径不选，不否定新架构；低成本编排门禁未实现，也不以工业标题贴高成本。",
        "locations": ["PDF p1 original authors", "PDF pp7–12 architecture and maturity table", "PDF p13 operating observations", "PDF pp16–17 proposed evaluation and future calibration"],
        "algorithm_assessment": "three-tier mining orchestration reference design; new benchmark remains a proposal, not a delivered public capability benchmark",
        "production_evidence": {"kind": "operating_site_testing_prototype_observations", "online_ab": False, "details": "原型12周/31活跃日合计API$19.63；4示例查询$0.28–0.42、70–130秒；无baseline/gold/human adjudication，作者明确不构成评价。"},
        "pdf_checks": [(1, "Eramet"), (12, "not implemented"), (12, "No controlled"), (13, "19.63")],
    },
    {
        "id": "2610.26662", "organization": "Independent Researchers (Tian Zhang / Meng Li)",
        "decision": "rejected", "resolution": "not_selected_this_window_single_case_operational_experience_report",
        "reason": "AllPath有可审计的风险门禁、字节相同base/单调版本/冻结授权的策略修订门禁和无action tools的夜间反思；源码与每日journal公开。但原文自述是单系统、单操作者（也是作者）的7.5周paper-brokerage自然观察，顺序人审/自动两regime受市场变化混杂，不是随机AB，也不报告投资收益或证明更安全。52次反思、119次revision是运行记录而非公共Agent能力基准。本轮按单案例运营经验报告不选，保留真实有用设计事实；未交易、未运行Agent，不能把它说成高成本训练。",
        "locations": ["author block", "§3.6 deployment/artifacts", "§4.1–4.3 verification", "§5.5 sequential comparison", "§6.1/6.5", "§7 limitations"],
        "algorithm_assessment": "layered verification and self-revision system case study; no claim that the study establishes investment performance or a safer regime",
        "production_evidence": {"kind": "live_paper_account_single_operator_sequential_regimes", "online_ab": False, "details": "paper账户用经纪商模拟API；shadow账户只本地账本、不发订单。市场真实但资金不冒险；内部ledger非公开，journal可按日核对。"},
        "upstream_artifact": "https://github.com/dukesky/allpath-trading-agent",
        "checks": [("S3.SS6", "paper-trading API"), ("S4.SS1", "byte-identical"), ("S6.SS5", "52 nightly reflection sessions"), ("S7", "natural experiment, not an experiment")],
    },
    {
        "id": "2610.26817", "organization": "Lyft, Inc.", "track": "recommendation",
        "decision": "rejected", "resolution": "industrial_online_evidence_not_established",
        "reason": "Lyft NBA有独立新低成本核心：multinomial propensity模型与SNIPW因果校正转移/奖励，嵌入CMDP occupancy-measure LP，显式预算/eligibility/fairness等约束并解释shadow prices。原文研究是68周专有历史数据、52周训练+16周holdout的model-based OPE；LTV+19%/+8%为离线估计。§5明确线上A/B是可能的后续验证，不能把公司部署背景或百万活跃用户当该policy已A/B。按工业业务定向决策证据门槛不选，LP/SNIPW核心未实现，不能改归通用RL绕过门槛或武断说核心高成本。",
        "locations": ["complete Lyft byline", "§2.2–2.3 SNIPW and CMDP LP", "§3 temporal holdout", "§4.2 policy OPE", "§5 explicit future online A/B"],
        "algorithm_assessment": "new causal-corrected constrained offline policy optimization for business targeting; cheap core not implemented",
        "production_evidence": {"kind": "proprietary_historical_data_offline_policy_evaluation", "online_ab": False, "details": "8RFM状态×2action；99分位权重裁剪，γ=.9。强可忽略性/positivity是假设；不能用IPW消除未观测混杂。"},
        "checks": [("S2.SS2", "strong ignorability"), ("S3", "68 weeks of proprietary historical data"), ("S4.SS2", "All three are obtained and evaluated offline"), ("S5", "online A/B test")],
    },
    {
        "id": "2610.27859", "organization": "ZJU-UIUC Institute / Zhejiang University / University of Illinois Urbana-Champaign", "format": "pdf",
        "decision": "rejected", "resolution": "not_selected_this_window_laboratory_provenance_experience_report",
        "reason": "已核原文机构与Experience report类型。APS ELN确有七项新工程扩展：每数值绑定file/extractor版本、selection snapshot或server公式，MCP结构化写入、内容hash和只读重放漂移检查；Community desktop/MCP代码公开。生产历史审计与后建两项agent记录演示不是同一口径：后者验证46值的来源链，44值独立精确复算、2个分割依赖值仅量级一致；‘zero drift’不是新Agent能力或测量科学准确性。原文自述新扩展尚未经数月常规人/Agent使用，五平台对比是文档/源码审查非现场试验。本轮按单实验室溯源工程经验报告不选，不将FAIR数据原则当Meta机构、不把可复用便宜重放组件说成高成本。",
        "locations": ["PDF p1 author affiliations and article type", "PDF p4 Community release", "PDF pp8–10 provenance extensions", "PDF pp11–12 validation", "PDF pp15–16 validity limits"],
        "algorithm_assessment": "new database/provenance engineering and deterministic replay safeguards, reported as a single-laboratory experience study rather than a new Agent learning algorithm",
        "production_evidence": {"kind": "production_notebook_audit_and_two_short_demonstrations", "online_ab": False, "details": "7个月生产记录审计覆盖约5年历史项目；新provenance扩展用两项短期演示验证，未有多月纵向新功能效果。"},
        "pdf_checks": [(1, "Experience report"), (4, "open-source software"), (9, "drift check"), (12, "44"), (16, "not yet been evaluated over a multi-")],
    },
    {
        "id": "2610.32110", "organization": "William Jeffries (author affiliation not stated; Pilsudski Institute is the production user, not a verified author affiliation)", "priority": "P1",
        "decision": "accepted", "resolution": "accepted_low_cost_tool_formatter_audit_and_public_evaluation_interface_not_implemented",
        "reason": "这是可独立复用的公开工具语义检查/评测资源：固定同一真实tool内部结果，仅改变formatter披露scope/completeness/uncertainty/provenance；40冻结case中8调试、32holdout，确定性construction checker、claim sheets、模型输出与人工仲裁公开。保留真正生产故障和对照实验事实，但90/90 verifier翻转来自固定答案离线测试，不是用户线上AB；审计prompt演示由已知缺陷作者编写，不能叫穷尽发现。低成本checker/成对渲染协议适合接入，接受但本轮未实现/未跑分；全paper API$74.44只是原始成本，不冒充本地复现或任意高成本豁免。",
        "locations": ["original author block", "§1 public artifacts", "§2 actual formatter failures", "§3 paired protocol and safeguards", "§4.3 cost", "§5–6 audit demonstration and limits"],
        "algorithm_assessment": "public paired tool-formatter evidence protocol, deterministic construction checks and audit prompt; cheap interface/core accepted but not implemented",
        "production_evidence": {"kind": "real_rag_incidents_plus_offline_paired_formatter_experiment", "online_ab": False, "details": "Pilsudski档案RAG已被用户使用；文中3模型5replicates/condition、1200agent输出。固定答案verifier对照不是现网随机流量。"},
        "upstream_artifact": "https://github.com/williamcodes/who-verifies-the-tools",
        "cost_note": "§4.3原始全部pilots+full run API$74.44；本次不发API、不运行模型、不认定所有完整矩阵便宜。",
        "checks": [("S1.p7.1", "github.com/williamcodes/who-verifies-the-tools"), ("S3.p3.1", "32"), ("S3.SS3.p1.1", "deterministic checker"), ("S4.SS3", "$74.44"), ("S6", "unevaluated demonstration")],
    },
    {
        "id": "2610.32851", "organization": "Cognizant",
        "decision": "rejected", "resolution": "not_selected_this_window_single_estate_architecture_report",
        "reason": "PDF作者机构为Cognizant。论文确有先组织后检索的新artifact级方案：保留producer/service/domain/version元数据，catalog+稀疏registry+导航hypergraph先限artifact ID，再做vector search和置信度不足时全库widening，并留context graph。241仓库/18服务、100+生产缺陷和35回归失败是真实开发者复核的案例观察；原文检索accuracy与widening rate仍在评估，未给独立公共基准或随机流量对照。按本轮单企业架构报告不选，不声称无新设计；低成本scoping核心未实现，不能以未测latency或private企业全文规模虚标已验证效果/高成本。",
        "locations": ["PDF p1 Cognizant byline", "Design section and Figures1–3", "Deployment and Evaluation", "Limitations/Path Forward"],
        "algorithm_assessment": "new artifact-provenance scoping architecture and navigation hypergraph, with limited single-estate observational evaluation; core not implemented",
        "production_evidence": {"kind": "developer_adjudicated_production_defect_case_study", "online_ab": False, "details": "100+ live queue缺陷、35release回归；precision/placement/widening实测尚未完成，latency按设计讨论而非报告benchmark。"},
        "checks": [("Sx2", "artifact identifiers"), ("Sx3", "100 defects"), ("Sx3", "measurements are in progress"), ("Sx5", "single estate")],
        "pdf_checks": [(1, "Cognizant")],
    },
    {
        "id": "2610.34679", "organization": "Netflix", "priority": "P1",
        "decision": "accepted", "resolution": "accepted_low_cost_trace_driven_tool_optimizer_core_not_implemented",
        "reason": "AT-AT是新环境侧Agent优化器，不是普通MCP部署报告：固定executor/harness，用train traces与结果让Pi coding Agent只修改允许的tool描述/实现，语法编译+文件allowlist门禁，失败最多5次修正。公开源码与τ²-verified train/test、TerminalBench/TBLite和Netflix三MCP提供验证。生产任务选自过去两周流量，但original/optimized比较在sandbox回放，非用户随机AB；仅一台MCP成功率上升，另两台content score下降，不能把效率改善夸成全面能力提升。廉价trace/edit-validation核心可接受但本轮未实现；优化API原文约$1.34/$6.935/$7.684每server，不能将完整30trial、多基准/闭源矩阵视为已跑或把便宜核心贴高成本。",
        "locations": ["complete Netflix author block", "§3.2 defining method", "§4.1 held-out split and paired30trial significance", "§4.2 public coding benchmarks", "§4.3 production MCP replay and Table4", "§5 limitations/future guarantees"],
        "algorithm_assessment": "new logged-trace-driven, agent-fixed tool optimizer with editable-file and syntax gates; core accepted but not implemented",
        "production_evidence": {"kind": "production_derived_tasks_sandbox_paired_replay", "online_ab": False, "details": "三MCP test10/5/11任务；pass80→80、0→0、54.5→72.7%；成本/错误降但前两content score下降。"},
        "upstream_artifact": "https://github.com/Netflix-Skunkworks/agent-tool-opt-core",
        "cost_note": "原文Table4一轮optimizer分别$1.34/$6.935/$7.684；session cost不含judge。未运行这些API或完整benchmark矩阵。",
        "gold_access_contract": "Optimizer receives train traces/evaluation only; keep held-out task outcomes and test data out of optimization inputs.",
        "checks": [("S3.SS2", "up to five attempts"), ("S4.SS1", "train split only"), ("S4.SS3", "sandbox environment"), ("S4.SS3", "$7.684"), ("S4.SS3", "content score fell")],
    },
    {
        "id": "2610.35509", "organization": "PayPal Inc.", "track": "foundation-model",
        "decision": "rejected", "resolution": "not_selected_this_window_enterprise_gateway_experience_report",
        "reason": "Cosmos确有PayPal大规模真实生产使用，不应被generic deployment过滤：>12000开发者、约200B tokens/day、100+models和99.999%ATB是历史point-in-time数据，不是SLA承诺或新模型效果。论文贡献为Envoy外部Go控制+in-proxy RustWasm翻译/计量、OPA纯决策和versioned rollout的系统架构/经验；五分钟synthetic-upstream基准仅测request-path overhead、排除response-body工作，非线上模型AB。按本轮基础模型算法/公共能力基准重点不选这篇企业gateway工程报告，不否定系统价值；不把200B生产流量冒作必须复现的训练成本，也未实现/跑其CPU压测。",
        "locations": ["complete PayPal author block", "§5 two-tier dataplane", "§9.4 policy function", "§13.1 synthetic CPU benchmark", "§13.2 production counts", "§15–16 limitations"],
        "algorithm_assessment": "enterprise governance gateway architecture and operating lessons, not a new foundation-model algorithm or delivered public model benchmark",
        "production_evidence": {"kind": "real_production_gateway_observation_and_synthetic_load_benchmark", "online_ab": False, "details": "2/4实例、每实例4vCPU/8GiB，110ms synthetic upstream，约1137–2262RPS，p50约4ms/p99约10–11ms；仅request path。"},
        "checks": [("S13.SS1", "synthetic upstream"), ("S13.SS1", "excludes response-body work"), ("S13.SS2", "point-in-time aggregates"), ("S15", "one large organization")],
    },
)


def build(source_dir: Path) -> dict:
    observations, metadata_receipts = load_observations(source_dir)
    rows = []
    for original in SPECS:
        spec = dict(original)
        identity, revision = spec["id"], 1
        metadata = observations[identity, revision]
        if max(v for i, v in observations if i == identity) != revision:
            raise ValueError(f"{identity}: later observed revision is not reviewed")
        fmt = spec.pop("format", "html")
        path = source_dir / "p2-residual-industrial" / f"{identity}v1.{fmt}"
        url = f"https://arxiv.org/{fmt}/{identity}v1"
        receipts = [source_receipt(path, url, source_dir)]
        soup = BeautifulSoup(path.read_text(), "html.parser") if fmt == "html" else None
        witnesses = []
        for location, needle in spec.pop("checks", []):
            node = soup.find(id=location)
            text = " ".join(node.get_text(" ", strip=True).split()) if node else ""
            if needle.casefold() not in text.casefold():
                raise ValueError(f"{identity}: missing original witness {location}: {needle}")
            witnesses.append({"format": "html", "location": location, "match": needle,
                              "paragraph_sha256": sha256(text.encode()).hexdigest()})
        pdf_checks = spec.pop("pdf_checks", [])
        if pdf_checks:
            pdf = path.with_suffix(".pdf")
            if fmt != "pdf":
                receipts.append(source_receipt(pdf, f"https://arxiv.org/pdf/{identity}v1", source_dir))
            with fitz.open(pdf) as doc:
                for page, needle in pdf_checks:
                    text = " ".join(doc[page - 1].get_text().split())
                    if needle.casefold() not in text.casefold():
                        raise ValueError(f"{identity}: missing PDF p{page} witness: {needle}")
                    witnesses.append({"format": "pdf", "page_one_based": page, "match": needle,
                                      "page_text_sha256": sha256(text.encode()).hexdigest()})
        row = {
            "revision": revision, "title": metadata["title"], "published": metadata["published"],
            "updated": metadata["updated"], "metadata_sha256": metadata["metadata_sha256"],
            "capture": metadata["captures"][0], "metadata_capture": metadata["captures"][0],
            "metadata_capture_sha256": metadata_receipts[metadata["captures"][0]],
            "source_url": url, "source_sha256": receipts[0]["source_sha256"],
            "source_capture": receipts[0]["source_capture"], "source_receipts": receipts,
            "source_witnesses": witnesses, "track": "agent", "priority": "P2",
            "verified_priority_organizations": [], "production_gate_passed": False,
            "review_done": True, "fulltext_review_completed": True, "full_article_read": False,
            "source_review_scope": "bounded original byline, defining contribution, production vs offline evidence, costs and limitations; not an implementation or full-article endorsement",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "implementation_status": "not_implemented", "experiments_started": 0, "gpu_runs": 0,
            **spec,
        }
        if fmt == "pdf":
            row["source_access_attempts"] = [
                {"url": f"https://arxiv.org/html/{identity}v1", "outcome": "HTTP404; original HTML unavailable"},
                {"url": url, "outcome": "fixed PDF downloaded; first page visually inspected and relevant sections read"},
            ]
        ledger_row(row, ARTIFACT)
        rows.append(row)
    return {"schema_version": 1,
            "window": {"start": "2026-10-16", "end": "2026-11-09", "timezone": "Asia/Shanghai"},
            "scope": "Eight residual strong production/workflow leads from the frozen365 protection set; original sources, not abstract-only exclusions",
            "counts": dict(Counter(r["decision"] for r in rows)), "all_sources_exhaustive": False,
            "implementations": 0, "gpu_runs": 0, "reviews": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_dir)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"]))


if __name__ == "__main__":
    main()
