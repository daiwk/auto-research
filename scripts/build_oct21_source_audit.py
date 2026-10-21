#!/usr/bin/env python3
"""Freeze a finite Oct21 source delta and selected-paper dispositions, not global closure."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from curate_oct21_component_evidence import COMPONENTS, REFERENCES, write  # noqa: E402

AUDIT = ROOT / "docs/research-audits/oct21-components"
BATCH = "2026-10-21-new-announcements-and-priority-delta-components"
COSTS = {
    "baseline-incremental": "Millions of private ranking logs, deployed predictions and user-randomized live-traffic four-arm experiments; no public production environment.",
    "spar-prefix-balance": "Qwen3-0.6B/1.7B/4B, months of private Youku logs, daily SFT/DPO and seven-day live A/B.",
    "echo-selector-loss": "100K event histories, K10000/M100 retrieval, concurrent teacher/selector/ranking graphs, large industrial logs and live traffic.",
    "ap-opd": "1.7B student/8B math teacher,17398 training problems,128prompts per batch,200updates,8192-token responses plus teacher GSPO and code/evaluation matrix.",
    "optd": "1.5B/4B/7B students and domain teachers,50–150updates,up to16384-token training responses plus long multi-sample math/code evaluation.",
    "locale-jepa": "ImageNet100epoch multiarchitecture grid, including eight-GPU ViT-L training.",
    "oo-harness": "Closed-source evolution/actor calls, forty evolution iterations per long-horizon benchmark and held-out benchmark campaign.",
    "rpl": "Eight H100 policy-training GPUs plus a separate eight-H100 reranking node, Wikipedia retrieval and full RL/mutation/SFT matrix.",
    "visually-attributable-opd": "Eight H800, 4B/9B full-parameter post-training, group8 and batch48 with full benchmark matrix.",
    "cache-engineering": "Eight A800-80GB split prefill/decode with TP4, 120B/230B models and long-horizon serving evaluation.",
    "esc": "22B active parameters,177K steps,global batch128,6.8e21FLOPs and geometric preprocessing/Best-of-N.",
    "aptamer-lab-loop": "Specialist physical laboratory and sequencing; about4400 constructs and three7–10day feedback cycles.",
}


def finalize(directory):
    capture = directory/"retrieval.json"
    receipts = json.loads(capture.read_text())
    arxiv = [r for r in receipts if r["kind"] == "arxiv"]
    if len(arxiv) != 8 or any(r.get("announced_on") != "2026-10-21" or not r.get("parse_complete") for r in arxiv):
        raise ValueError("eight actual complete Oct21 bulletin captures required")
    records = {r["key"]: r for r in catalog_records()}
    selected = [records[k] for k in sorted(set(COMPONENTS) | REFERENCES)]
    dispositions = []
    for record in selected:
        key = record["key"]
        identity = re.search(r"\d{4}\.\d{4,5}", record["paper_url"]).group()
        component = key in COMPONENTS
        dispositions.append({"id": identity, "key": key, "title": record["title"],
            "original_published_at": record["published_at"],
            "intake_class": "historical-backfill" if key == "esc" else "new-to-repository-recent-first-publication",
            "priority": record["priority"], "domain": record["domain"], "first_author_affiliation": record["first_author_affiliation"],
            "implementation_status": record["implementation_status"], "component_implemented": component,
            "review_done": True, "full_experiment_status": "not_reproduced_high_cost",
            "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": {"source_url": record["paper_url"].replace("/abs/", "/html/"),
                "basis": "Named method/resource/deployment sections in fixed v1 and linked author source; not a local runtime estimate",
                "scale": COSTS[key], "available_resource": "One NVIDIA A100 or A30, or local Mac"},
            "detail_path": record["detail_path"], "paper_url": record["paper_url"]})
    dates = sorted(r["checked_at"] for r in receipts)
    deltas = [json.loads((directory/name).read_text()) for name in
              ("google-delta.json", "meta-delta.json", "google-deepmind-delta.json")]
    for delta in deltas:
        delta["page_receipts"] = [{k:v for k,v in row.items() if k != "records"}
                                   for row in receipts if row["source"] == delta["organization"]]
    coverage = {"schema_version": 1, "checked_on": "2026-10-21", "scope_kind": "selected-components-and-priority-official-delta",
        "source_check_window_utc": {"first_checked_at": dates[0], "last_checked_at": dates[-1]},
        "all_sources_exhaustive": False, "review_watermark_advanced": False,
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"},
        "baseline": "../oct20-components/source-coverage.json",
        "raw_capture_sha256": hashlib.sha256(capture.read_bytes()).hexdigest(),
        "counts": {"selected_papers": len(selected),
                   "new_to_repository_recent_papers": sum(r["intake_class"] != "historical-backfill" for r in dispositions),
                   "historical_backfill": sum(r["intake_class"] == "historical-backfill" for r in dispositions),
                   "components": len(COMPONENTS), "reference_only": len(REFERENCES),
                   "cuda_components_executed_on_a100": sum(device == "cuda" for device in COMPONENTS.values()),
                   "category_entries_including_crosslists_and_replacements": sum(r["parsed_entries"] for r in arxiv),
                   "unique_bulletin_identities": len({r["id"].split("v")[0] for p in arxiv for r in p["records"]}),
                   "directory_new_urls_not_paper_count": sum(len(d["new_directory_urls"]) for d in deltas)},
        "arxiv_sources": [{k:v for k,v in row.items() if k != "records"} for row in arxiv],
        "bulletin_ids_by_category": {row["source"]: [entry["id"] for entry in row["records"]] for row in arxiv},
        "official_directory_deltas": deltas,
        "additional_dispositions": [
            {"id": "2610.26902", "title": "MOSS", "decision": "not_selected_under_industrial_evidence_gate",
             "source_url": "https://arxiv.org/html/2610.26902v1", "reason": "Production monitoring and offline alert-rate fix validation found; no qualifying randomized online business A/B effect established. Deployment alone does not automatically waive the gate."},
            {"title": "Autonomous Semantic Harmonization and Decoupled Staging for Enterprise Cloud CRM and ERP Data Migration",
             "source_url": "https://research.google/pubs/autonomous-semantic-harmonization-and-decoupled-staging-for-enterprise-cloud-crm-and-erp-data-migration-2/",
             "decision": "archived_unconfirmed_not_blocking", "reason": "Official directory/abstract retrieved, but original publication identity/date, author affiliation and defining executable method cannot be confirmed from linked primary resources. No invented paper or implementation."},
            {"id": "2610.28601", "title": "Evolving Agent Interfaces (Agent S4)", "decision": "outside_fixed_batch_not_implemented",
             "source_url": "https://arxiv.org/abs/2610.28601", "reason": "Candidate identity observed, not part of this finite twelve-paper delivery; no global closure claim."},
            {"id": "2608.07418", "title": "ResidencyRL", "decision": "historical_followup_not_part_of_recent_count",
             "source_url": "https://research.google/pubs/residencyrl-reinforcement-learning-in-simulated-clinical-environments/",
             "reason": "Older Google candidate surfaced in cross-check; identity is not a new October publication or a completed implementation. This batch does not claim global historical completeness."}],
        "limitations": ["A full bulletin title/abstract parse is not full-text review of all1126 identities.",
                        "Google listing29pages, Meta bounded6pages and DeepMind9pages; Meta pagination not claimed exhaustive.",
                        "Publication dates are originalv1 dates, not announcement or directory dates. ESC is an explicit10-14 historical backfill.",
                        "High-cost full experiments are terminal reviewDONE, not implementations, not automatic retries.",
                        "Global reviewed-through watermark remains10-15: selected-paper delivery is not whole-window review closure."]}
    write(AUDIT/"source-coverage.json", coverage)
    write(AUDIT/"task-scope.json", {"schema_version": 1, "batch": BATCH, "papers": dispositions,
                                  "fixed_component_keys": sorted(COMPONENTS), "reference_only_keys": sorted(REFERENCES)})
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batch = {"batch": BATCH, "date": "2026-10-21", "scope_kind": "selected-paper-implementation",
             "source_artifact": "research-audits/oct21-components/README.md", "all_sources_exhaustive": False,
             "review_watermark_advanced": False, "counts": coverage["counts"], "candidates": []}
    for row in dispositions:
        batch["candidates"].append({"id": row["id"], "key": row["key"], "doc": row["detail_path"],
            "title": row["title"], "priority": row["priority"],
            "track": {"recommendation": "recommendation", "foundation-models": "foundation-model", "post-training": "post-training", "agent-research": "agent"}[row["domain"]],
            "status": "implemented" if row["component_implemented"] else "deferred",
            "resolution": "bounded_component_implemented_full_experiment_not_reproduced_high_cost" if row["component_implemented"] else "not_reproduced_high_cost",
            "implementation_status": row["implementation_status"], "catalog_key": row["key"], "catalog_detail": row["detail_path"],
            "reason": "低成本组件已验收；完整实验成本过高不复现（审查DONE）。" + COSTS[row["key"]] if row["component_implemented"] else "成本过高，不复现（审查DONE）。" + COSTS[row["key"]],
            "original_published_at": row["original_published_at"], "intake_class": row["intake_class"],
            "review_done": True, "automatic_retry": False, "automatic_implementation_queue": False,
            "cost_assessment": row["cost_assessment"], "review_artifact": "research-audits/oct21-components/task-scope.json",
            "full_text_review": {"scope": "full-text", "read_scope": "Named defining method, experiment/resource and relevant deployment sections", "full_article_read": False},
            "source_provenance": [{"source_url": row["paper_url"], "source_kind": "primary-method-and-cost-review",
                                   "organization": row["first_author_affiliation"]}]})
    indices = [i for i,b in enumerate(ledger["batches"]) if b["batch"] == BATCH]
    if indices:
        ledger["batches"][indices[0]] = batch
    else:
        ledger["batches"].append(batch)
    write(ledger_path, ledger)
    print(json.dumps(coverage["counts"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capture_directory", type=Path)
    finalize(parser.parse_args().capture_directory)
