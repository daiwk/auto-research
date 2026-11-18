"""Build bounded original-source dispositions for seven production-deployment leads."""
from __future__ import annotations

import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

from bs4 import BeautifulSoup

from build_nov09_review_inventory import ledger_row
from route_nov09_title_abstract import load_observations


REVIEWS = (
    {
        "id": "2610.31351", "revision": 1,
        "organization": "DoorDash, Inc.",
        "locations": ["author block", "§III-A/III-B", "§IV-A/IV-B, Tables I–II", "§V threats to validity"],
        "decision": "rejected", "resolution": "not_selected_this_window_industrial_experience_report",
        "reason": "DoorDash 的系统真实运行在生产仓库，但 50 个 stale flag 的 90% 可用 PR 是单公司工程经验结果，人工清理耗时为内部估计而非随机对照。原文 A/B 指 feature flag 的用途，不是该清理 Agent 的线上效果实验。本轮按工业应用经验报告不选：公开论文描述 ADK 编排、MCP/Jira、worktree 与确定性门禁组合，没有提供可独立复现的新算法或公开清理基准。",
        "production_evidence": {
            "kind": "observational_internal_production_workflow", "online_ab": False,
            "details": "最近 50 个 Kotlin 仓库 flag 清理：31 首次接受、14 修改后接受、5 失败；每项平均 13.8 分钟/$4.79。flag 运行态来自 DoorDash 内部实验平台，目标值先由工程师确认。",
            "interpretation": "生产代码中的 PR 处理，不是用户流量随机 A/B；不将 Google ADK 的工具来源当作 Google 作者机构。",
        },
        "source_checks": [("S3.SS1.p2.1", "orchestrator"), ("S4.SS1.p2.1", "50"), ("S5.p6.1", "rather than precise wall-clock")],
    },
    {
        "id": "2610.23317", "revision": 1,
        "organization": "Beihang University / Omaha AIGC",
        "locations": ["author block", "§3.2–3.3, Equations 2–9", "§4.1–4.5, Tables 1–4", "§5 Enterprise Deployment"],
        "decision": "reviewed_deferred", "resolution": "not_reproduced_high_cost",
        "reason": "AgentOnto 是独立的本体构建—检查分析—反馈更新方法：更新必须同时通过 correction 与 retention 检查，再用自生成任务做两轮准备，不能按普通案例报告排除。论文还报告真实企业上线后观察，但 84%→100% 的非空聚合覆盖来自前测/上线样本，不是随机用户 A/B。完整论文矩阵依赖闭源生成/审查 API、606 分析请求、多组本体与 SQL 基线、44 反馈事件和174更新后请求，以及不可公开重放的企业生产数据；依用户高成本规则不启动完整实验，本次仅完成原文审查，不声称组件实现。",
        "production_evidence": {
            "kind": "post_launch_enterprise_observation_and_controlled_task_checks", "online_ab": False,
            "details": "15 个客户账户一周内完成144分析会话、918操作；消费制造数据含约437M设备报告、96设备型号、333本体对象。聚合非空覆盖前测453/541、上线106/106；另有19/24任务的逐阶段检查。",
            "interpretation": "明确上线与量化使用证据，但非随机流量实验；两公共数据域上的离线准确率与生产覆盖不同口径。",
        },
        "cost_assessment": {
            "source_url": "https://arxiv.org/html/2610.23317v1",
            "basis": "§4.1 固定模型与任务数、§4.2–4.5 完整比较矩阵、§5 企业数据；原始规模评估，不是本地实测",
            "scale": "gpt-5.6-terra 生成及独立 gpt-5.6-sol 审查；606 分析请求与多组基线，44反馈事件、174更新后请求；完整上线部分还有约437M设备报告的私有企业环境。",
            "available_resource": "one A100 or A30, or local Mac; no experiment was started",
            "cost_type": "多阶段闭源 API 实验矩阵和不可公开重放的企业生产环境",
        },
        "source_checks": [("S3.SS2.p13.2", "correction and retention"), ("S4.SS1.p2.1", "606"), ("S4.SS1.p5.1", "gpt-5.6-terra"), ("S5.p2.1", "144")],
    },
    {
        "id": "2610.28432", "revision": 2,
        "organization": "Idealworks / NVIDIA",
        "locations": ["author block", "§1 Scope of This Work", "§2–3, Tables 1–6", "Appendix E, Tables 18/21/25", "Appendix G"],
        "decision": "reviewed_deferred", "resolution": "not_reproduced_high_cost",
        "reason": "固定 v2 原文扩展 COMPASS 的机器人 embodiment、数字孪生和真实机器人基准，并加入控制器与全局规划器集成。65.3%→91.7% 为研发中心机器人试验对照；生产导航栈是基线，不代表学习策略已做客户全流量 A/B。完整实验含世界模型和 IL 两阶段的各6张 Blackwell GPU、8 GPU/32机器人并行残差RL、Cosmos视频增强、物理 iw.hub/Jetson 和研发场地；显著超出单A100/A30或Mac的低成本范围，不启动完整复现。",
        "production_evidence": {
            "kind": "real_robot_research_facility_benchmark_against_production_stack", "online_ab": False,
            "details": "Idealworks 研发中心实机，每场景约30次试验；IW.CE-COMPASS 的 S1–S4 平均成功率91.7%，生产 IW Nav为100%。学习策略使用单RGB相机，IW Nav使用先验地图/LiDAR，不能视为同传感器公平A/B。",
            "interpretation": "真实部署到实验机器人并有生产系统基线，但不是客户现场全流量或随机在线实验。作者归属 NVIDIA/Idealworks，不是 Google/Meta。",
        },
        "cost_assessment": {
            "source_url": "https://arxiv.org/html/2610.28432v2",
            "basis": "Appendix E Tables18/21/25 明列硬件、时长和rollout；§3明列数据和实机要求，原始规模非本地实测",
            "scale": "世界模型17/24epochs和IL29/31epochs均用6×RTX PRO6000 Blackwell（各约44–47分钟）；残差PPO每变体440iterations、8GPU×4robots、450step horizon；605探索+240示范episodes、Cosmos增强和iw.hub实机。",
            "available_resource": "one A100 or A30, or local Mac; no experiment was started",
            "cost_type": "多GPU世界模型/模仿/RL训练、视频增强和专用真实机器人场地",
        },
        "source_checks": [("S3.p1.1", "R&D"), ("A5.T18", "6x"), ("A5.T21", "6x"), ("A5.T25", "440")],
    },
    {
        "id": "2610.33253", "revision": 1,
        "organization": "Zafin",
        "locations": ["author block", "§3 Zafin AIOS Architecture", "§4.3–4.9", "§5.1–5.6 Table1", "§6 limitations"],
        "decision": "rejected", "resolution": "not_selected_this_window_descriptive_customer_case_study",
        "reason": "Zafin AIOS 是两套私有生产代码库的 Customer Zero 案例。原文明确49项增强请求的38%/76%收益来自开发者与主管估算，未为每任务运行平行人类组，不是随机A/B或因果提升证据。贡献是意图、RBAC、审计和人工门禁的工程架构及描述性案例，未交付可独立复现的新算法或公共能力基准；按本轮已批准的应用报告口径不选，不把缺少A/B本身当Agent研究的否决条件。",
        "production_evidence": {
            "kind": "private_production_case_study_with_expert_estimated_baseline", "online_ab": False,
            "details": "30项定价平台和19项交易协商平台增强请求；平均估计节省38%/76%，整体53%；每请求平均2.9次人工介入。",
            "interpretation": "真实生产代码与治理证据成立，努力节省是专家估计而非直接测量的随机对照提升。",
        },
        "source_checks": [("S4.SS5.p1.1", "expert developer estimates"), ("S4.SS9.p2.1", "rather than a fully controlled"), ("S5.SS1.p1.1", "Forty-nine")],
    },
    {
        "id": "2610.33636", "revision": 1,
        "organization": "Chalmers University of Technology / Volvo Group",
        "locations": ["author block", "§III-A/III-B", "§IV-A–IV-D Tables I–III", "§V-A.1", "§VII"],
        "decision": "rejected", "resolution": "not_selected_this_window_existing_harness_comparison",
        "reason": "原文对比 Volvo 既有定制 ReAct harness 与现成 Claude Code/OpenCode，用相同 MCP/工具层和模型在66个内部IVI、56个既有AMEX任务重复执行，并访谈10人。Setup A已生产使用；Setup B在访谈时尚未向测试员发布。论文贡献为既有系统的采用/维护权衡实证，不是新独立算法或新的公开能力基准，本轮不选。Google Maps是被测应用，非Google作者机构或线上A/B。",
        "production_evidence": {
            "kind": "production_baseline_and_offline_rig_phone_comparison", "online_ab": False,
            "details": "IVI每配置2次、AMEX每配置3次；同模型IVI成功率差异不显著。Setup B单任务推理成本2.6–10.7倍，3–66%月总成本节省把估计工程维护人力纳入。",
            "interpretation": "受控任务对照及访谈，不是向真实用户随机分配流量；不把成本模型的总拥有成本估计当模型效果提升。",
        },
        "source_checks": [("S3.SS1.p1.1", "production use at Volvo"), ("S4.SS1.SSS2.p1.1", "66"), ("S5.SS1.SSS1.p1.1", "not yet been released")],
    },
    {
        "id": "2610.36254", "revision": 1,
        "organization": "Socket Inc.",
        "locations": ["author block", "§II", "§III The Bootstrap", "§IV Two Working Factories", "§V–VI"],
        "decision": "rejected", "resolution": "not_selected_this_window_unevaluated_bootstrap_and_observational_report",
        "reason": "两个工业factory观测15/17天，15倍合入增长是随代理逐步上线的相关变化；原文明确没有新增协调机制或优化器。公开1400词bootstrap提示是从手工factory提炼的未验证可行性假设，生产部署与多仓工作亦超出该bootstrap范围；真正随机对照列为未来五个月计划。按应用经验/前瞻研究报告不选本轮算法复现，不声称已完成自进化能力验证。",
        "production_evidence": {
            "kind": "observational_industrial_factories_and_unevaluated_new_prompt", "online_ab": False,
            "details": "CLI factory约30个定时Agent，15日观察；另一个factory17日。样本日69次合入花费$1.2k，至少25/450已标fixed的问题后发现修复逃逸；人工审批保留。",
            "interpretation": "作者明确前后变化不建立因果，bootstrap未受测；未来800+fix/arm等试验不能冒充既有结果。",
        },
        "upstream_artifact": "https://github.com/mikolalysenko/instant-factory",
        "source_checks": [("S2.p2.1", "We add no coordination mechanism"), ("S3.p1.1", "untested feasibility hypothesis"), ("S5.p1.1", "proposes no new optimizer"), ("S4.p10.1", "cannot establish causality")],
    },
    {
        "id": "2611.03774", "revision": 1,
        "organization": "University of North Dakota",
        "locations": ["author block", "§II-C–II-F", "§III-A–III-J", "§IV"],
        "decision": "rejected", "resolution": "not_selected_this_window_specialist_detection_application",
        "reason": "HeteroScan 的检出模型为55维图统计上的既有 RF/ExtraTrees/XGBoost 集成；Claude只在分类后生成证据说明，明确不参与检测分类。8,047样本沙箱后保留2,516图的离线切分和20份说明检查不等于线上流量A/B，公开网页仅表示工具可访问。贡献为恶意软件领域的应用分类与行为实证，非新LLM/Agent算法或通用公开能力基准，本轮不选。未执行、下载或操作恶意样本。",
        "production_evidence": {
            "kind": "web_demo_and_offline_sandbox_classification", "online_ab": False,
            "details": "2,516图按70/15/15分层划分，378测试样本；LLM说明20样本平均4.4/5规则检查。GNN比较使用不同旧数据集，作者标为初步且不可逐样本比较。",
            "interpretation": "网站部署不证明生产流量或随机试验；模型名与API供应商不是作者机构。",
        },
        "source_checks": [("S2.SS6.p1.1", "does not perform classification"), ("S3.SS5.p1.1", "not directly comparable"), ("S3.SS8.p1.1", "20 samples")],
    },
)


def build(source_dir: Path) -> dict:
    observations, _ = load_observations(source_dir)
    reviews = []
    for spec in REVIEWS:
        spec = dict(spec)
        identity, revision = spec["id"], spec["revision"]
        metadata = observations[identity, revision]
        source = source_dir / "production-final" / f"{identity}v{revision}.html"
        soup = BeautifulSoup(source.read_text(), "html.parser")
        checks = spec.pop("source_checks")
        for location, needle in checks:
            node = soup.find(id=location)
            if node is None or needle.casefold() not in node.get_text(" ", strip=True).casefold():
                raise ValueError(f"{identity}: original-source witness missing at {location}: {needle}")
        high_cost = spec["resolution"] == "not_reproduced_high_cost"
        row = {
            "title": metadata["title"], "published": metadata["published"], "updated": metadata["updated"],
            "metadata_sha256": metadata["metadata_sha256"], "capture": metadata["captures"][0],
            "source_sha256": sha256(source.read_bytes()).hexdigest(),
            "source_url": f"https://arxiv.org/html/{identity}v{revision}",
            "source_capture": f"production-final/{identity}v{revision}.html",
            "track": "agent", "priority": "P1", "verified_priority_organizations": [],
            "source_review_scope": "fixed original byline, defining system, experimental protocol, deployment outcomes and limitations",
            "review_done": True, "fulltext_review_completed": True, "full_article_read": False,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "implementation_status": "not_implemented", "production_gate_passed": False,
            **spec,
        }
        if high_cost:
            row.update(full_experiment_status="not_reproduced_high_cost", full_experiment_review_done=True)
        ledger_row(row, "research-audits/nov09-review-closure/batch-terminal-production-reviews.json")
        reviews.append(row)
    return {
        "schema_version": 1,
        "window": {"start": "2026-10-16", "end": "2026-11-09", "timezone": "Asia/Shanghai"},
        "scope": "Seven preserved production/deployment leads checked against exact captured revisions; no implementation or experiment claimed.",
        "input_inventory_commit": "a86689a72b42d93fa726972c0ab2ecb42e378a84",
        "all_sources_exhaustive": False,
        "counts": dict(Counter(r["decision"] for r in reviews)), "reviews": reviews,
    }


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
