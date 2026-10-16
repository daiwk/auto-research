#!/usr/bin/env python3
"""Reconcile exactly the accepted twelve components and one review-only report.

No search/exhaustiveness or watermark is inferred from implementing this list.
Full experiments are terminal high-cost decisions; component evidence is checked
separately against the current executed source hashes.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402

BATCH = "2026-10-17-twelve-components-and-meta-system-reference"
COSTS = {
    "drop-kv": "7B/8B 多模型、4K–128K、多 KV 预算完整评测。",
    "mirror-moe": "2–4 H100、4.4B–12.8B tokens、多模型预训练。",
    "bit-sparse": "原文 RTX3090 步时乘3350步估算单臂约七小时；不是A100实测。",
    "lct": "原文 RTX3090 步时乘3400步估算单臂约8.5小时；完整fused kernel/optimizer另需工程验证。",
    "roleq": "原文8B配置3–4 A100小时，二平面阶段不足十小时。",
    "shared-residual-distillation": "1.7/4/8B、100步、每步32题×4rollouts、多冻结教师评分和20K/32K长度。",
    "progress-reward": "4 RTX3090、128CPU/256GB、五种子；原文模拟训练每任务约1–10小时。",
    "elite-replay": "4 A100-80GB、4B全参、长rollout、每题128次评测。",
    "clean-rm": "8–70B两阶段reward model、最多600epochs/早停30，另有策略RL与外部judge。",
    "shortcut-sensitivity": "只接受固定公开历史记录复算；完整新模型/守卫和干预采集预算未可靠确定，不启动探跑。",
    "disagreement-routing": "8B、多样本、多模型BFCL/WebShop训练和长rollout。",
    "tracer": "六环境×四模型×五折×多预算和自由rollout，原文未发布artifacts。",
    "hardware-diversity": "8–128 AMD MI350X/NVIDIA B200和私有生产推荐任务；当前单A100/A30硬件不匹配。",
}


def source_hashes_current(hashes):
    if not hashes or not any(name.startswith("src/") for name in hashes) or not any(name.startswith("scripts/") for name in hashes):
        raise ValueError("executed source coverage missing")
    for name, expected in hashes.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            raise ValueError(f"invalid executed source path: {name}")
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"stale executed source: {name}")


def finalize():
    rows = {row["key"]: row for row in catalog_records() if row["key"] in COSTS}
    if set(rows) != set(COSTS):
        raise ValueError("accepted thirteen-record scope incomplete")
    candidates = []
    counts = {"gpu_receipt_and_source_hashes_validated": 0, "cpu_metrics_sources_validated": 0,
              "review_only_not_reproduced": 0}
    for key, row in sorted(rows.items()):
        page = ROOT / "docs" / row["detail_path"]
        if not page.is_file() or row.get("full_experiment_status") != "not_reproduced_high_cost":
            raise ValueError(f"{key}: detail/cost boundary missing")
        component = key != "hardware-diversity"
        if row.get("promotion_eligible") is not False or row.get("evolve_integrated") is not False:
            raise ValueError(f"{key}: unearned promotion")
        validation = {"requires_gpu_validation": bool(row.get("requires_gpu_validation")),
                      "gpu_validation_passed": False, "status": "review_only_not_reproduced"}
        if row.get("requires_gpu_validation"):
            artifact = row["gpu_validation_artifact"]
            receipt = load_gpu_receipt(ROOT / artifact)
            if receipt["adapter_key"] != key:
                raise ValueError(f"{key}: wrong GPU receipt")
            source_hashes_current(receipt["executed_source_sha256"])
            validation.update(status="gpu_receipt_and_source_hashes_validated", gpu_validation_passed=True,
                              gpu_validation_artifact=artifact, code_commit=receipt["provenance"]["commit"])
            counts["gpu_receipt_and_source_hashes_validated"] += 1
        elif component:
            metric = page.parent / "metrics/component-cpu-seeds42-44.json"
            payload = json.loads(metric.read_text())
            if payload.get("method") != key or payload.get("diagnostic_only") is not True or payload.get("promotion_eligible") is not False:
                raise ValueError(f"{key}: CPU artifact identity/boundary differs")
            source_hashes_current(payload["provenance"]["executed_source_sha256"])
            validation.update(status="cpu_metrics_sources_validated", metrics=[str(metric.relative_to(ROOT))],
                              code_commit=payload["provenance"]["commit"])
            counts["cpu_metrics_sources_validated"] += 1
        else:
            counts["review_only_not_reproduced"] += 1
        candidates.append({
            "id": re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group(), "key": key, "title": row["title"],
            "priority": row.get("priority", "P1"),
            "track": {"foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent"}[row["domain"]],
            "intake_class": "historical-work-new-arxiv" if key == "progress-reward" else "announcement-overlap-new-to-review",
            "status": "deferred", "status_scope": "full_paper_reproduction", "resolution": "not_reproduced_high_cost",
            "full_experiment_status": "not_reproduced_high_cost", "review_done": True, "terminal": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "reason": "成本过高，不复现（审查 DONE）。" + COSTS[key],
            "cost_assessment": {"source_url": row["paper_url"], "basis": COSTS[key],
                                "available_resource": "单张A100或A30，或本地Mac；不假设多卡/并发可用",
                                "cost_type": "published_configuration_or_budget_not_local_measurement"},
            "doc": row["detail_path"], "publication_date": row["published"],
            "implementation_status": row["implementation_status"],
            "bounded_implementation_scope": row["summary"], "local_operator": row.get("local_operator"),
            "local_command": row.get("local_command"), "component_validation": validation,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
            "source_provenance": [{"source_kind": "original-paper", "source_url": row["paper_url"]}],
        })
    expected = {"gpu_receipt_and_source_hashes_validated": 9, "cpu_metrics_sources_validated": 3,
                "review_only_not_reproduced": 1}
    if counts != expected:
        raise ValueError(f"acceptance counts differ: {counts}")
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-17", "scope_kind": "selected-paper-implementation",
             "window": "Twelve user-approved bounded components plus one Meta/AMD review-only system report; not a complete bulletin review.",
             "required_tracks": ["foundation-model", "post-training", "agent"], "review_watermark_advanced": False,
             "coverage_complete": False, "review_snapshot_modified": False,
             "scope_artifact": "research-audits/oct17-components/README.md",
             "accepted_scope_counts": {"bounded_components": 12, "review_only_system_report": 1},
             "component_validation_counts": counts,
             "full_reproduction_policy": "Terminal not_reproduced_high_cost/review DONE; bounded diagnostics accepted separately, no automatic retry or capability promotion.",
             "candidates": candidates}
    ledger["batches"] = [item for item in ledger["batches"] if item["batch"] != BATCH] + [batch]
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(counts))


if __name__ == "__main__":
    finalize()
