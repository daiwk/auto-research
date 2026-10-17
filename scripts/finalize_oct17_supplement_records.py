#!/usr/bin/env python3
"""Close the selected 9-component/2-interface/3-reference scope, not source coverage."""
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
from curate_oct17_supplement_evidence import CATALOG_KEYS, GROUPS, validate_curated  # noqa: E402

BATCH = "2026-10-17-nine-components-two-interfaces-three-high-cost-references"
INTERFACES = {"gacc-bench", "muon-paired-budget"}
REFERENCES = {"gemini-minecraft", "hy-memory", "athanor"}
COSTS = {
    "prism-1": "8B/12B、多臂多种子；作者H100单次50–85分钟。",
    "langdit": "约334M、七组×250K更新，每步512×1024 tokens。",
    "oprd-reminder": "16 H20、131072 context、三epochs和在线仓库rollout。",
    "opcredit": "八张RTX5880、约2500 GPU小时和Freebase服务。",
    "structural-signal-retriever": "全量8.84M passages、约124 GiB RAM和API编排。",
    "rsiflow": "4B/8B分布式训练、多轮多候选、3000训练及744报告任务。",
    "leash": "OSWorld 262任务、多弱模型/商业强模型、每任务最多50动作。",
    "probe": "4B auditor/30B target、双A100、多优化器多臂训练。",
    "terminal-rsi": "27B、256K、多阶段分布式PPO、3000任务。",
    "gacc-bench": "十模型、多预算、281 contexts/500 goals/2571 questions的长上下文API扫评。",
    "muon-paired-budget": "四workloads、23候选、五匹配种子的完整LM/ViT训练。",
    "gemini-minecraft": "四执行Agent加Observer，单次约27小时和24000调用。",
    "hy-memory": "30B-A3B、128 H20，每批64 windows×8 rollouts。",
    "athanor": "四商业研究Agent各占八卡节点、104小时、作者合计费用约12000美元。",
}


def current_sources(hashes):
    if not hashes or not any(p.startswith("src/") for p in hashes) or not any(p.startswith("scripts/") for p in hashes):
        raise ValueError("executed algorithm/runner coverage missing")
    for name, expected in hashes.items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f"stale or invalid source: {name}")


def finalize():
    rows = {row["key"]: row for row in catalog_records() if row["key"] in COSTS}
    if set(rows) != set(COSTS):
        raise ValueError("accepted fourteen-record scope missing")
    device_by_key = {CATALOG_KEYS.get(key, key): device for device, _, items in GROUPS.values() for key in items}
    counts = {"gpu_receipt_and_source_hashes_validated": 0, "cpu_metrics_sources_validated": 0,
              "review_only_not_reproduced": 0}
    candidates = []
    for key, row in sorted(rows.items()):
        page = ROOT / "docs" / row["detail_path"]
        if not page.is_file() or row.get("full_experiment_status") != "not_reproduced_high_cost":
            raise ValueError(f"{key}: detail/full-cost boundary missing")
        if row.get("promotion_eligible") is not False or row.get("evolve_integrated") is not False:
            raise ValueError(f"{key}: unearned capability/Evolve promotion")
        status = ("deferred_high_cost" if key in REFERENCES else
                  "evaluation_protocol_interface" if key in INTERFACES else "component_only")
        if row.get("implementation_status") != status:
            raise ValueError(f"{key}: accepted implementation type differs")
        validation = {"requires_gpu_validation": False, "gpu_validation_passed": False,
                      "status": "review_only_not_reproduced"}
        if key in REFERENCES:
            if not row.get("review_done") or row.get("local_operator") or row.get("gpu_validation_artifact"):
                raise ValueError(f"{key}: reference must not impersonate executable implementation")
            counts["review_only_not_reproduced"] += 1
        else:
            device = device_by_key[key]
            metric_path = page.parent / f"metrics/component-{device}-seeds42-44.json"
            metric = json.loads(metric_path.read_text())
            validate_curated(metric, key)
            current_sources(metric["provenance"]["executed_source_sha256"])
            if device == "cuda":
                artifact = row["gpu_validation_artifact"]
                receipt = load_gpu_receipt(ROOT / artifact)
                if receipt["adapter_key"] != key or receipt["metrics"] != metric["metrics"]:
                    raise ValueError(f"{key}: receipt/metric differs")
                if (receipt["provenance"]["commit"] != metric["provenance"]["commit"]
                        or receipt["executed_source_sha256"] != metric["provenance"]["executed_source_sha256"]
                        or receipt["dataset"] != metric["dataset"]):
                    raise ValueError(f"{key}: receipt/metric provenance differs")
                current_sources(receipt["executed_source_sha256"])
                validation.update(requires_gpu_validation=True, gpu_validation_passed=True,
                                  status="gpu_receipt_and_source_hashes_validated", gpu_validation_artifact=artifact)
            else:
                if row.get("requires_gpu_validation") or row.get("gpu_validation_artifact"):
                    raise ValueError(f"{key}: CPU interface must not invent GPU evidence")
                validation["status"] = "cpu_metrics_sources_validated"
            validation.update(metrics=[str(metric_path.relative_to(ROOT))], code_commit=metric["provenance"]["commit"])
            counts[validation["status"]] += 1
        candidates.append({
            "id": re.search(r"\d{4}\.\d{4,5}", row["paper_url"]).group(),
            "key": key, "title": row["title"], "priority": row.get("priority", "P1"),
            "track": {"foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent"}[row["domain"]],
            "intake_class": "announcement-overlap-new-to-review",
            "status": "deferred", "status_scope": "full_paper_reproduction", "resolution": "not_reproduced_high_cost",
            "full_experiment_status": "not_reproduced_high_cost", "review_done": True, "terminal": True,
            "automatic_retry": False, "automatic_implementation_queue": False,
            "reason": "成本过高，不复现（审查 DONE）。" + COSTS[key],
            "cost_assessment": {"source_url": row["paper_url"], "basis": COSTS[key],
                                "available_resource": "单张A100或A30，或本地Mac；不假设多卡/并发可用",
                                "cost_type": "published_configuration_or_budget_not_local_measurement"},
            "doc": row["detail_path"], "publication_date": row["published"],
            "implementation_status": status, "bounded_implementation_scope": row["summary"],
            "local_operator": row.get("local_operator"), "local_command": row.get("local_command"),
            "component_validation": validation, "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "source_provenance": [{"source_kind": "original-paper", "source_url": row["paper_url"]}],
        })
    expected = {"gpu_receipt_and_source_hashes_validated": 4, "cpu_metrics_sources_validated": 7,
                "review_only_not_reproduced": 3}
    if counts != expected:
        raise ValueError(f"acceptance counts differ: {counts}")
    path = ROOT / "docs/paper-discovery-ledger.json"
    ledger = json.loads(path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-17", "scope_kind": "selected-paper-implementation",
             "window": "Oct16 announcements/Oct15 v1 overlap supplement; not new Oct17 announcements or full-source closure.",
             "required_tracks": ["foundation-model", "post-training", "agent"],
             "review_watermark_advanced": False, "coverage_complete": False, "review_snapshot_modified": False,
             "scope_artifact": "research-audits/oct17-supplement/README.md",
             "accepted_scope_counts": {"bounded_components": 9, "evaluation_interfaces": 2, "review_only_papers": 3},
             "component_validation_counts": counts,
             "full_reproduction_policy": "High-cost complete experiments terminal/review DONE; bounded diagnostics admitted separately; no auto retry or capability promotion.",
             "candidates": candidates}
    ledger["batches"] = [item for item in ledger["batches"] if item["batch"] != BATCH] + [batch]
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(counts))


if __name__ == "__main__":
    finalize()
