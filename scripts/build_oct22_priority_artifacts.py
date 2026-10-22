"""Bind two CPU component diagnostics, source delta and terminal cost decisions."""
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
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_oct22_priority_components import MODULES, RUNNER, SEEDS  # noqa: E402
from auto_research.foundation_models.deepsea import (  # noqa: E402
    ALL_LANGS, MGSM_ARCHIVE_SHA256, MGSM_JSON_SHA256, UPSTREAM_REVISION,
)

AUDIT = ROOT/"docs/research-audits/oct22-priority-backfill"
COSTS = {
    "deepsea": "13 languages, five tasks and the paper's full model/API evaluation matrix; MetricX-24 requires a separate learned evaluator. Only CPU scorer/schema contracts are run.",
    "logact": "Full semantic LLM voters, AgentDojo/swarm experiments and distributed backends require model calls and a larger campaign. Only local SQLite protocol contracts are run.",
}
CATEGORIES = {"cs.AI", "cs.CL", "cs.CV", "cs.IR", "cs.LG", "cs.RO", "cs.SD", "eess.AS"}
CHECKS = {
    "deepsea": {"five_task_reference_scores", "subject_macro_not_micro", "first_qa_reference_not_oracle",
        "prediction_coverage_rejected", "public_input_excludes_gold", "metricx_not_substituted", "unicode_chrf_and_whitespace"},
    "logact": {"uncommitted_blocked", "incomplete_quorum_blocked", "commit_before_real_effect",
        "uncertain_effect_requires_explicit_recovery", "idempotent_retry_and_cached_result", "durable_reopen_result",
        "rejected_action_never_executed"},
}
METRICS = {"deepsea": {"scorer_contract_cases", "reference_score_error", "coverage_rejection_count", "model_calls"},
           "logact": {"actual_llm_calls", "executor_invocations", "distinct_effects", "recovery_entries", "log_entries"}}


def expected_inspection():
    return {"upstream_revision": UPSTREAM_REVISION, "archive_sha256": MGSM_ARCHIVE_SHA256,
        "json_sha256": MGSM_JSON_SHA256, "json_bytes": 1954503, "test_rows": 3250,
        "language_test_counts": {language: 250 for language in ALL_LANGS}, "projected_prefix_rows": 26,
        "projected_prefix_sha256": "75d25cca098cf2d29d206f47ac98ddc15c86f0bf4beb2806f3cb131ae1948df8",
        "public_field_names": ["question"], "gold_fields_excluded": ["answer", "answer_with_cot"],
        "split": "test", "model_calls": 0, "used_for_training_or_selection": False,
        "benchmark_text_exported": False, "diagnostic_only": True}


def validate_official_inspection(row):
    require(row == expected_inspection(), "fixed official schema/hash/isolation contract differs")


def validate_capture(arxiv):
    require(len(arxiv) == 8 and {p["source"] for p in arxiv} == CATEGORIES,
            "exact eight distinct categories required")
    require(all(p.get("parse_complete") is True and p.get("status") == "retrieved"
        and p.get("announced_on") == "2026-10-21"
        and p.get("parsed_entries") == p.get("expected_entries") == len(p["records"])
        for p in arxiv), "complete same-bulletin capture receipts required")


def records():
    index = {row["key"]: row for row in catalog_records()}
    require(MODULES.keys() <= index.keys(), "missing fixed-scope catalog record")
    return index


def metric_path(row):
    return Path("docs")/Path(row["detail_path"]).parent/"metrics/component-cpu-seeds42-44.json"


def dataset(key, hashes):
    return {"id": f"synthetic:oct22-{key}-contracts-v1", "revision": "sha256:"+digest(hashes),
            "recipe": "source-frozen-generated-contract-inputs", "capability_benchmark": False}


def validate_result(key, result):
    require(key in MODULES and result["method"] == key, "wrong component identity")
    require(result["schema_version"] == 2 and result["fixture_demo"] is True
        and result["manifest_ref"] == records()[key]["domain"]+":"+key, "schema/manifest/fixture identity differs")
    require(result["evaluation_tier"] == result["evaluation_protocol"]["tier"] == "l1_mechanism"
        and result["diagnostic_only"] is True and result["formal_comparison"] is False
        and result["evaluation_protocol"]["formal_comparison"] is False
        and result["promotion_eligible"] is False and result["evolve_integrated"] is False
        and result["pretrained_model_calls"] == 0 and result["full_experiment_review_done"] is True
        and result["full_experiment_status"] == "not_reproduced_high_cost", "diagnostic claim boundary")
    p = result["provenance"]
    hashes = p["executed_source_sha256"]
    require(set(hashes) == {RUNNER, *MODULES.values()}, "executed source scope differs")
    require(result["dataset"] == dataset(key, hashes) and result["seeds"] == result["evaluation_protocol"]["seeds"] == SEEDS, "dataset identity/recipe/seeds")
    require(p["accelerator"] == "CPU" and p["artifact_path"] == metric_path(records()[key]).as_posix(), "CPU artifact binding")
    require(re.fullmatch(r"[0-9a-f]{64}", p["raw_runner_artifact_sha256"])
        and p["official_schema_inspection_sha256"] == digest(expected_inspection()), "raw/schema provenance binding")
    require(p["dataset_fingerprint"] == "sha256:"+digest({"dataset": result["dataset"], "source": hashes, "seeds": SEEDS}), "fingerprint")
    rows = result["per_seed"]
    require(result["metrics"] == aggregate(rows), "aggregate differs")
    require(all(set(row["checks"]) == CHECKS[key] and set(row["metrics"]) == METRICS[key]
        and all(v is True for v in row["checks"].values()) for row in rows), "failed or missing defining contract")
    if key == "deepsea":
        require(all(r["metrics"]["scorer_contract_cases"] == 7 and r["metrics"]["reference_score_error"] < 1e-12
            and r["metrics"]["coverage_rejection_count"] == 3 and r["metrics"]["model_calls"] == 0 for r in rows), "scorer reference/isolation failed")
    else:
        require(all(r["metrics"]["executor_invocations"] == 2 and r["metrics"]["distinct_effects"] == 1
            and r["metrics"]["recovery_entries"] == 1 and r["metrics"]["log_entries"] == 12
            and r["metrics"]["actual_llm_calls"] == 0 for r in rows), "durable execution/recovery failed")


def curate(path):
    data = Path(path).read_bytes()
    raw = json.loads(data)
    require(raw["device"] == "cpu" and raw["accelerator"] == "CPU" and raw["seeds"] == SEEDS
        and set(raw["components"]) == set(MODULES) and raw["diagnostic_only"] is True
        and raw["formal_comparison"] is False and raw["promotion_eligible"] is False
        and raw["evolve_integrated"] is False and raw["pretrained_model_calls"] == 0
        and raw["full_experiment_status"] == "not_reproduced_high_cost", "fixed CPU scope required")
    commit, hashes = raw["code_commit"], raw["source_sha256"]
    proof = capture_sources(ROOT, commit, hashes)
    verify_sources(ROOT, commit, hashes, proof)
    inspection = raw.get("official_data_schema_inspection")
    validate_official_inspection(inspection)
    prepared = []
    for key in MODULES:
        row = records()[key]
        target = metric_path(row)
        ds = dataset(key, hashes)
        result = {"schema_version": 2, "method": key, "manifest_ref": row["domain"]+":"+key,
            "seeds": SEEDS, "dataset": ds, "per_seed": raw["components"][key]["per_seed"],
            "metrics": aggregate(raw["components"][key]["per_seed"]), "evaluation_tier": "l1_mechanism",
            "evaluation_protocol": {"tier": "l1_mechanism", "seeds": SEEDS, "formal_comparison": False,
                "claim_policy": "scorer/durability contracts, not model or agent capability results"},
            "provenance": {"commit": commit, "artifact_path": target.as_posix(), "accelerator": "CPU",
                "executed_source_sha256": hashes, "raw_runner_artifact_sha256": hashlib.sha256(data).hexdigest(),
                "official_schema_inspection_sha256": digest(inspection),
                "dataset_fingerprint": "sha256:"+digest({"dataset": ds, "source": hashes, "seeds": SEEDS})},
            "diagnostic_only": True, "fixture_demo": True, "pretrained_model_calls": 0,
            "formal_comparison": False, "promotion_eligible": False, "evolve_integrated": False,
            "full_experiment_status": "not_reproduced_high_cost", "full_experiment_review_done": True}
        validate_result(key, result)
        prepared.append((ROOT/target, result))
    for target, result in prepared:
        write(target, result)
    write(AUDIT/"frozen-sources.json", {"schema_version": 1, "commit": commit, "proof": proof})
    write(AUDIT/"deepsea-official-schema.json", inspection)


def source_audit(directory):
    raw_bytes = (directory/"retrieval.json").read_bytes()
    raw = json.loads(raw_bytes)
    baseline = json.loads((ROOT/"docs/research-audits/oct21-priority-backfill/source-coverage.json").read_text())
    arxiv = [p for p in raw if p["kind"] == "arxiv"]
    validate_capture(arxiv)
    ids = {r["id"] for p in arxiv for r in p["records"]}
    old = {identity for values in baseline["bulletin_ids_by_category"].values() for identity in values}
    deltas = []
    for name in ("google", "meta", "google-deepmind"):
        delta = json.loads((directory/f"{name}-delta.json").read_text())
        expected_baseline = (baseline["raw_capture_sha256"] if name == "google-deepmind" else
            "8583e2acbbbbb731444b285ee57a5a12301cea5f8889e78f41e9a164498e3dce")
        require(delta["baseline_sha256"] == expected_baseline, "official directory baseline differs")
        if delta["retrieved_pages"] < delta["attempted_pages"]:
            delta.update(status="source_unavailable_not_zero_delta", new_directory_urls=None, changed_records=None)
        else:
            delta["status"] = "bounded_directory_difference_checked"
        deltas.append(delta)
    counts = {"component_only": 2, "same_bulletin_backfill": 1, "historical_backfill": 1,
              "metadata_updates": 1, "archived_nonblocking": 1,
              "fresh_since_last_scan": len({i.split('v')[0] for i in ids}-{i.split('v')[0] for i in old}),
              "changed_version_identities": len(ids-old), "unique_bulletin_identities": len({i.split('v')[0] for i in ids})}
    write(AUDIT/"source-coverage.json", {"schema_version": 1, "checked_on": "2026-10-22",
        "scope_kind": "bounded-priority-backfill", "raw_capture_sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "baseline": "../oct21-priority-backfill/source-coverage.json", "baseline_raw_sha256": baseline["raw_capture_sha256"],
        "all_sources_exhaustive": False, "review_watermark_advanced": False,
        "review_watermark": {"before": "2026-10-15", "after": "2026-10-15"}, "counts": counts,
        "added_version_identities": sorted(ids-old), "removed_version_identities": sorted(old-ids),
        "bulletin_ids_by_category": {p["source"]: [r["id"] for r in p["records"]] for p in arxiv},
        "bulletin_category_identity_sha256": {p["source"]: digest([r["id"] for r in p["records"]]) for p in arxiv},
        "retrieval_receipts": [{k:v for k,v in p.items() if k != "records"} for p in raw],
        "official_directory_deltas": deltas,
        "supplementary_sources": [{"url": "https://github.com/"+repo, "revision": revision,
            "scope": "bounded official repository/author identity review, not organization exhaustion"}
            for repo, revision in [("google-research/deep-sea", "7c3abc06824c8cb634930ab6049176da30cfa0e7"),
                ("facebookresearch/logact", "db395449fb2dbb534c8eec848900252ac8324ab2"),
                ("facebookresearch/Memo-Pro-Agent", "5bf57aed9a865bc3489e5daa8040e243ec50fa85"),
                ("facebookresearch/swe-sweep", "5968c69a4f6407fc50d3c5e7e0601a46960c4e0d")]],
        "limitations": ["Still the October21 bulletin; no new bulletin/version identity since PR219.",
            "Google/Meta publication directories unavailable: unknown delta, not zero.",
            "Bounded repository supplement and two components do not finish full-window review."]})
    index = records()
    rows = [{"key": key, "domain": index[key]["domain"], "paper_url": index[key]["paper_url"],
        "title": index[key]["title"], "priority": index[key]["priority"],
        "detail_path": index[key]["detail_path"], "published_at": index[key]["published_at"],
        "implementation_status": "component_only", "component_implemented": True, "review_done": True,
        "intake_class": "historical-backfill" if key == "logact" else "same-bulletin-recent-backfill",
        "full_experiment_status": "not_reproduced_high_cost", "automatic_retry": False,
        "automatic_implementation_queue": False, "cost_assessment": {"source_url": index[key]["paper_url"], "scale": COSTS[key]}}
        for key in MODULES]
    exception = {"key": "swe-sweep", "paper_url": "https://swesweep.com/paper",
        "status": "archived_source_exception", "review_done": True, "blocking": False,
        "exact_first_publication_date": None, "report_header_date": "2026-10-01",
        "code": "https://github.com/facebookresearch/swe-sweep", "code_reused": False,
        "upstream_revision": "5968c69a4f6407fc50d3c5e7e0601a46960c4e0d",
        "license_url": "https://github.com/facebookresearch/swe-sweep/blob/5968c69a4f6407fc50d3c5e7e0601a46960c4e0d/LICENSE",
        "reason": "Report header/website/git dates differ and do not prove exact first publication; fixed LICENSE is review-only, not a reusable open-source grant.",
        "full_experiment_status": "not_reproduced_high_cost", "automatic_retry": False,
        "cost_assessment": {"source_url": "https://swesweep.com/paper", "physical_pdf_page": 39,
            "scale": "100 repositories/4068 bugs/22 languages/7 LMs; Table24 median0.3-1.6h per repository, max5.5h in four displayed model campaigns."}}
    updates = [{"key": "proper-agent", "change": "official author code availability/license/revision only; no new paper/version or upgraded fidelity",
                "revision": index["proper-agent"]["upstream_revision"]}]
    write(AUDIT/"task-scope.json", {"schema_version": 1, "batch": "2026-10-22-priority-backfill",
        "papers": rows, "metadata_updates": updates, "archived_exceptions": [exception]})
    ledger_path = ROOT/"docs/paper-discovery-ledger.json"
    ledger = json.loads(ledger_path.read_text())
    batch = {"batch": "2026-10-22-priority-backfill", "date": "2026-10-22", "scope_kind": "bounded-priority-backfill",
        "source_artifact": "research-audits/oct22-priority-backfill/README.md", "counts": counts,
        "review_watermark_advanced": False, "all_sources_exhaustive": False,
        "metadata_updates": updates, "archived_exceptions": [exception],
        "candidates": [{**row, "id": row["paper_url"].split("/abs/")[-1].split("v")[0],
            "doc": row["detail_path"], "catalog_key": row["key"], "catalog_detail": row["detail_path"],
            "status": "implemented", "track": "agent" if row["key"] == "logact" else "foundation-model",
            "full_text_review": {"scope": "full-text", "read_scope": "defining method, public code, cost and key figure", "full_article_read": False},
            "source_provenance": [{"source_url": row["paper_url"], "source_kind": "primary-method-and-cost-review",
                "organization": index[row["key"]]["first_author_affiliation"]}],
            "resolution": "bounded_component_implemented_full_experiment_not_reproduced_high_cost",
            "reason": "CPU低成本接口/协议已验证；完整实验成本过高，不复现（审查DONE）。"} for row in rows]}
    ledger["batches"] = [b for b in ledger["batches"] if b["batch"] != batch["batch"]] + [batch]
    write(ledger_path, ledger)


def check():
    proof = json.loads((AUDIT/"frozen-sources.json").read_text())
    batch_bindings = []
    for key in MODULES:
        result = json.loads((ROOT/metric_path(records()[key])).read_text())
        validate_result(key, result)
        p = result["provenance"]
        verify_sources(ROOT, p["commit"], p["executed_source_sha256"], proof["proof"])
        batch_bindings.append((p["commit"], p["executed_source_sha256"], p["raw_runner_artifact_sha256"]))
    require(all(row == batch_bindings[0] for row in batch_bindings), "two components must bind the same actual run")
    validate_official_inspection(json.loads((AUDIT/"deepsea-official-schema.json").read_text()))
    print("Two frozen CPU component evidence contracts passed; no model/GPU capability claims")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path)
    parser.add_argument("--capture", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.input:
        curate(args.input)
    if args.capture:
        source_audit(args.capture)
    if args.check:
        check()
