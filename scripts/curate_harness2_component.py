"""Validate real Harness² CPU output and publish bounded scalar diagnostics."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re

from auto_research.agent_research.harness2 import PROTOCOL, UPSTREAM_COMMIT

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("scripts/run_harness2_component.py", "src/auto_research/agent_research/harness2.py")
METRICS = {"tasks": 2, "actual_python_rollouts": 16, "improvement_stages": 12,
           "rollout_budget_identity_checks": 2, "stage_budget_identity_checks": 2,
           "script_mechanism_post_run_checks": 2, "second_task_prior_library_entries": 1,
           "retained_evidence_lessons": 2, "failed_rollouts": 0}
ARTIFACT = "docs/agent-research/2610.14224-harness2/metrics/component-cpu-seeds42-44.json"


def dataset_fingerprint(dataset, rows):
    value = {"dataset": dataset, "fixtures": [
        {"seed": row["seed"], "mode": row["mode"], "sha256": row["fixture_sha256"]}
        for row in rows]}
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def validate_raw(raw):
    if (raw.get("protocol_id") != PROTOCOL or raw.get("upstream_commit") != UPSTREAM_COMMIT or
            raw.get("budget") != {"k": 2, "modes": ["parallel", "sequential"], "workers": 2} or
            raw.get("seeds") != [42, 43, 44] or raw.get("device") != "cpu" or
            raw.get("evaluation_tier") != "l1_mechanism" or
            raw.get("diagnostic_only") is not True or raw.get("promotion_eligible") is not False or
            raw.get("evolve_integrated") is not False or
            raw.get("full_experiment_status") != "not_reproduced_high_cost" or
            raw.get("dataset") != {"id": "generated-signed-ledger", "revision": "signed-ledger-decimal-v1", "public_benchmark": False}):
        raise ValueError("incompatible diagnostic protocol")
    sources = {path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCES}
    if raw.get("source_sha256") != sources:
        raise ValueError("current source differs from executed source; rerun, do not relabel")
    rows = raw.get("per_seed_mode", [])
    if [(r.get("seed"), r.get("mode")) for r in rows] != [(s, m) for s in (42, 43, 44) for m in ("parallel", "sequential")]:
        raise ValueError("complete independent seed/mode records required")
    for row in rows:
        if row.get("metrics") != METRICS:
            raise ValueError("defining mechanism checks did not pass")
        if len(row.get("records", [])) != 2:
            raise ValueError("both streamed tasks required")
        for index, record in enumerate(row["records"]):
            summary, evidence, stages = record["summary"], record["evidence"], record["stages"]
            if (len(evidence) != 8 or len(stages) != 6 or summary["library_entries_seen"] != index or
                    summary["lesson_retained"] is not True or summary["selection_error"] or
                    summary["reflection_error"] or summary["diagnostic_only"] is not True or
                    summary["promotion_eligible"] is not False):
                raise ValueError("task execution or persistent library validation failed")
            labels = {e["label"] for e in evidence}
            if len(labels) != 8 or summary["adopted"] not in summary["finals"]:
                raise ValueError("existing final-output adoption required")
            if not all(e["execution"]["ok"] is True and e["execution"]["trajectory"] and
                       e["execution"]["deliverable"].strip() for e in evidence):
                raise ValueError("missing actual executed output")
            if any(s["fell_back"] or s["attempts"] != 1 or not s["edit"]["supports"] for s in stages):
                raise ValueError("unvalidated/fallback edit cannot support this receipt")
    return raw


def curate(raw, raw_sha256):
    validate_raw(raw)
    return {"schema_version": 2, "method": "harness2", "manifest_ref": "agent-research:harness2",
        "evaluation_tier": "l1_mechanism",
        "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost", "protocol_id": PROTOCOL,
        "dataset": raw["dataset"], "device": "cpu", "seeds": raw["seeds"],
        "budget": raw["budget"], "upstream_commit": UPSTREAM_COMMIT,
        "provenance": {"executed_source_sha256": raw["source_sha256"],
                       "raw_runner_artifact_sha256": raw_sha256,
                       "artifact_path": ARTIFACT,
                       "dataset_fingerprint": dataset_fingerprint(raw["dataset"], raw["per_seed_mode"])},
        "per_seed_mode": [{key: row[key] for key in ("seed", "mode", "fixture_sha256", "metrics")}
                          for row in raw["per_seed_mode"]],
        "metrics": {"actual_python_rollouts_total": 96, "streamed_tasks_total": 12,
                    "improvement_stages_total": 72, "retained_evidence_lessons_total": 12,
                    "script_mechanism_post_run_checks_total": 12, "failed_rollouts_total": 0},
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": raw["seeds"], "formal_comparison": False,
            "claim_policy": "Three-seed CPU mechanism checks only; no stable capability improvement claim",
            "actor": "trusted deterministic editor/selector fixture with actual Python subprocess executor",
            "gold_access": False, "test_isolated": False,
            "interpretation": "mechanism assertions only; no held-out capability, transfer gain, model training or official benchmark"}}


def validate_curated(data):
    if (data.get("method") != "harness2" or data.get("manifest_ref") != "agent-research:harness2" or
            data.get("protocol_id") != PROTOCOL or
            data.get("upstream_commit") != UPSTREAM_COMMIT or data.get("evaluation_tier") != "l1_mechanism" or
            data.get("diagnostic_only") is not True or data.get("promotion_eligible") is not False or
            data.get("evolve_integrated") is not False or data.get("device") != "cpu" or
            data.get("full_experiment_status") != "not_reproduced_high_cost" or
            data.get("budget") != {"k": 2, "modes": ["parallel", "sequential"], "workers": 2} or
            data.get("seeds") != [42, 43, 44] or
            data.get("dataset") != {"id": "generated-signed-ledger", "revision": "signed-ledger-decimal-v1", "public_benchmark": False} or
            data.get("evaluation_protocol", {}).get("formal_comparison") is not False):
        raise ValueError("invalid curated mechanism designation")
    provenance = data.get("provenance", {})
    if provenance.get("executed_source_sha256") != {
            path: hashlib.sha256((ROOT/path).read_bytes()).hexdigest() for path in SOURCES}:
        raise ValueError("curated source proof does not match this implementation")
    if re.fullmatch(r"[a-f0-9]{64}", provenance.get("raw_runner_artifact_sha256", "")) is None:
        raise ValueError("raw execution fingerprint required")
    rows = data.get("per_seed_mode", [])
    if [(r.get("seed"), r.get("mode")) for r in rows] != [(s, m) for s in (42, 43, 44) for m in ("parallel", "sequential")]:
        raise ValueError("complete seed/mode pairs required")
    if any(r.get("metrics") != METRICS or
           re.fullmatch(r"[a-f0-9]{64}", r.get("fixture_sha256", "")) is None for r in rows):
        raise ValueError("defining scalar measurements changed")
    protocol = data.get("evaluation_protocol", {})
    if (protocol.get("seeds") != [42, 43, 44] or not protocol.get("claim_policy") or
            provenance.get("artifact_path") != ARTIFACT or
            provenance.get("dataset_fingerprint") != dataset_fingerprint(data["dataset"], rows)):
        raise ValueError("curated manifest, input provenance or protocol is incomplete")
    if (any(rows[i]["fixture_sha256"] != rows[i+1]["fixture_sha256"] for i in (0, 2, 4)) or
            len({r["fixture_sha256"] for r in rows}) != 3):
        raise ValueError("modes must share matched inputs, different seeds distinct generated inputs")
    expected = {"actual_python_rollouts_total": sum(r["metrics"]["actual_python_rollouts"] for r in rows),
        "streamed_tasks_total": sum(r["metrics"]["tasks"] for r in rows),
        "improvement_stages_total": sum(r["metrics"]["improvement_stages"] for r in rows),
        "retained_evidence_lessons_total": sum(r["metrics"]["retained_evidence_lessons"] for r in rows),
        "script_mechanism_post_run_checks_total": sum(r["metrics"]["script_mechanism_post_run_checks"] for r in rows),
        "failed_rollouts_total": sum(r["metrics"]["failed_rollouts"] for r in rows)}
    if data.get("metrics") != expected:
        raise ValueError("aggregate metrics do not match seed/mode records")
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = args.raw.read_bytes()
    result = curate(json.loads(data), hashlib.sha256(data).hexdigest())
    validate_curated(result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "metrics": result["metrics"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
