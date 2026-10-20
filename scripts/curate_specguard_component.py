"""Recheck generated SpecGuard certificates and archive bounded, sanitized scalars."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

from auto_research.agent_research.specguard import (
    CONFLICT, HARNESS, NO_CONFLICT, LeanKernel, PROTOCOL, UPSTREAM_COMMIT,
    assemble, axioms_ok, fingerprint, parse_artifact, public_tasks,
)

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ("src/auto_research/agent_research/specguard.py", "scripts/run_specguard_component.py")


def committed_sources(commit):
    """Resolve immutable local Git blobs, never trust a remote --source-commit label."""
    if type(commit) is not str or re.fullmatch(r"[a-f0-9]{40}", commit) is None:
        raise ValueError("exact frozen source commit required")
    kind = subprocess.run(["git", "cat-file", "-t", commit], cwd=ROOT,
                          capture_output=True, text=True, check=False)
    if kind.returncode or kind.stdout.strip() != "commit":
        raise ValueError("frozen source commit is unavailable in local Git")
    result = {}
    for path in SOURCES:
        blob = subprocess.run(["git", "show", f"{commit}:{path}"], cwd=ROOT,
                              capture_output=True, check=False)
        if blob.returncode:
            raise ValueError(f"frozen source commit lacks {path}")
        result[path] = hashlib.sha256(blob.stdout).hexdigest()
    return result


def validate_raw(raw, kernel):
    tasks = public_tasks()
    dataset = {"id": "self-authored-increment-micro-suite", "public_benchmark": False,
               "revision": fingerprint([asdict(t) for t in tasks])}
    if (raw.get("method") != "specguard" or raw.get("protocol_id") != PROTOCOL or
            raw.get("upstream_commit") != UPSTREAM_COMMIT or raw.get("dataset") != dataset or
            raw.get("tasks") != [asdict(t) for t in tasks] or
            raw.get("evaluation_tier") != "l1_mechanism" or raw.get("diagnostic_only") is not True or
            raw.get("promotion_eligible") is not False or raw.get("evolve_integrated") is not False or
            raw.get("full_experiment_status") != "not_reproduced_high_cost"):
        raise ValueError("incompatible SpecGuard component scope")
    sources = {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCES}
    if raw.get("source_sha256") != sources:
        raise ValueError("current source differs from executed source; rerun, never relabel")
    if raw.get("source_sha256") != committed_sources(raw.get("code_commit")):
        raise ValueError("executed source hashes differ from the frozen Git commit")
    seeds, rows, records = raw.get("seeds", []), raw.get("per_seed", []), raw.get("model_records", [])
    if (not seeds or len(set(seeds)) != len(seeds) or len(seeds) > 3 or
            [(r.get("seed"), r.get("task_id")) for r in rows] !=
            [(seed, t.task_id) for seed in seeds for t in tasks]):
        raise ValueError("complete bounded seed/task records required")
    if (raw.get("model", {}).get("local_files_only") is not True or
            re.fullmatch(r"[a-f0-9]{40}", raw.get("model", {}).get("revision", "")) is None or
            raw.get("lean", {}).get("version") != "4.24.0" or
            raw.get("actual_model_calls") != len(records) or
            raw.get("actual_generated_tokens") != sum(r["generated_tokens"] for r in records)):
        raise ValueError("actual fixed-revision model calls and pinned Lean required")
    budget = raw["budget"]
    if (not 1 <= budget["max_attempts_per_role"] <= 2 or len(records) > budget["max_calls"] or
            len(records) > 54 or raw["actual_generated_tokens"] > budget["max_total_new_tokens"] or
            budget["max_total_new_tokens"] > 24000 or budget["wall_seconds"] > 900 or
            any(not 0 <= r["generated_tokens"] <= budget["max_new_tokens_per_call"] for r in records)):
        raise ValueError("model budget exceeded")
    if raw.get("device") == "cuda":
        if (not re.search(r"NVIDIA.*(?:A100|A30)", raw.get("accelerator", "")) or
                any(not r["actual_model_device"].startswith("cuda") for r in records)):
            raise ValueError("real A100/A30 generation evidence required for CUDA run")
    elif raw.get("device") != "cpu":
        raise ValueError("unknown device")
    linked = Counter((r["seed"], r["request_sha256"], r["response_sha256"]) for r in records)
    rechecks = []
    for row in rows:
        task = next(t for t in tasks if t.task_id == row["task_id"])
        if row.get("task_sha256") != fingerprint(asdict(task)):
            raise ValueError("task hash mismatch")
        role_records = row.get("role_records", [])
        for role in ("spec", "test", "connector"):
            attempts = [r for r in role_records if r["role"] == role]
            if [r["attempt"] for r in attempts] != list(range(1, len(attempts)+1)) or len(attempts) > 2:
                raise ValueError("unbounded or discontinuous role attempts")
        for record in role_records:
            view = ({"description": task.description, "codebase": task.codebase} if record["role"] == "spec"
                    else {"tests": task.tests} if record["role"] == "test" else
                    {"description": task.description, "codebase": task.codebase, "tests": task.tests,
                     "spec": row["artifacts"]["spec"], "test_model": row["artifacts"]["test"]})
            if record.get("input_sha256") != fingerprint(view):
                raise ValueError("role information boundary differs")
            if "response" in record:
                key = (row["seed"], record["request_sha256"],
                       hashlib.sha256(record["response"].encode()).hexdigest())
                if linked[key] < 1:
                    raise ValueError("generated role output is not linked to an actual model call")
                linked[key] -= 1
        if row["verdict"] not in {"conflict", "no-conflict", "inconclusive"}:
            raise ValueError("three-way verdict required")
        if row["verdict"] == "inconclusive":
            if row.get("evidence") is not None or row.get("certificate"):
                raise ValueError("inconclusive must not advertise a certificate")
            continue
        if row.get("evidence") != "lean_kernel_proof":
            raise ValueError("model judgment is not a kernel certificate")
        artifacts = row["artifacts"]
        for role in ("spec", "test", "connector"):
            matching = [r for r in role_records if r["role"] == role and
                        r.get("lean_check", {}).get("ok") is True]
            if (len(matching) != 1 or parse_artifact(matching[0]["response"], role) != artifacts[role]):
                raise ValueError("certificate source is not the accepted model-generated source")
        expected = assemble(artifacts["spec"], artifacts["test"], artifacts["connector"], HARNESS,
                            CONFLICT if row["verdict"] == "conflict" else NO_CONFLICT)
        if row.get("certificate") != expected:
            raise ValueError("certificate differs from mechanical existential/agree harness")
        checked = kernel.compile(expected)
        if not checked.ok or not axioms_ok(checked.output):
            raise ValueError("independent real Lean recheck failed")
        rechecks.append({"seed": row["seed"], "task_id": row["task_id"],
                         "certificate_sha256": checked.source_sha256,
                         "kernel_recheck": True})
    if any(linked.values()):
        raise ValueError("orphan model calls not represented in task records")
    metrics = {"task_runs": len(rows), "certified_conflicts": sum(r["verdict"] == "conflict" for r in rows),
               "formal_agreements": sum(r["verdict"] == "no-conflict" for r in rows),
               "inconclusive": sum(r["verdict"] == "inconclusive" for r in rows)}
    if raw.get("metrics") != metrics:
        raise ValueError("aggregate metrics differ from actual task results")
    return rechecks


def curate(raw, kernel, raw_sha256):
    rechecks = validate_raw(raw, kernel)
    return {"schema_version": 2, "method": "specguard", "manifest_ref": "agent-research:specguard",
        "protocol_id": PROTOCOL, "upstream_commit": UPSTREAM_COMMIT,
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True, "promotion_eligible": False,
        "evolve_integrated": False, "full_experiment_status": "not_reproduced_high_cost",
        "dataset": raw["dataset"], "model": raw["model"], "lean": raw["lean"],
        "device": raw["device"], "accelerator": raw["accelerator"], "seeds": raw["seeds"],
        "budget": raw["budget"], "metrics": {**raw["metrics"],
            "actual_model_calls": raw["actual_model_calls"],
            "actual_generated_tokens": raw["actual_generated_tokens"],
            "independent_kernel_rechecks": len(rechecks)},
        "per_task": [{"seed": r["seed"], "task_id": r["task_id"],
            "task_sha256": r["task_sha256"], "verdict": r["verdict"], "evidence": r["evidence"],
            "model_calls": sum("response" in call for call in r["role_records"]),
            "semantic_audit": "not_established_by_kernel_manual_review_required"}
            for r in raw["per_seed"]],
        "executed_model_roles": sorted({record["role"] for record in raw["model_records"]}),
        "end_to_end_certificate_observed": bool(rechecks),
        "kernel_rechecks": rechecks,
        "provenance": {"executed_source_sha256": raw["source_sha256"],
            "code_commit": raw["code_commit"], "raw_runner_artifact_sha256": raw_sha256,
            "dataset_fingerprint": raw["dataset"]["revision"],
            "artifact_path": "docs/agent-research/2610.09159-specguard/metrics/component-a100-seed42.json"},
        "evaluation_protocol": {"tier": "l1_mechanism", "seeds": raw["seeds"],
            "formal_comparison": False, "test_isolated": False,
            "gold_access": False, "claim_policy": "self-authored micro-suite, not agent/benchmark accuracy",
            "semantic_boundary": "Lean proves only generated formalizations; independent semantic audit required"}}


def gpu_receipt(curated, validated_at):
    """Passing denotes completed CUDA execution, never successful formalization."""
    from auto_research.gpu_validation import validate_gpu_receipt
    if curated.get("device") != "cuda" or not re.search(r"NVIDIA.*(?:A100|A30)", curated.get("accelerator", "")):
        raise ValueError("real A100/A30 curated runtime required")
    receipt = {"schema_version": 1, "adapter_key": "specguard", "validated_at": validated_at,
        "accelerator": {"vendor": "NVIDIA", "model": curated["accelerator"].removeprefix("NVIDIA ")},
        "command": ["python", "scripts/run_specguard_component.py", "--checkpoint", "<cached-public-checkpoint>",
            "--model-id", curated["model"]["id"], "--revision", curated["model"]["revision"],
            "--source-commit", curated["provenance"]["code_commit"], "--lean-bin", "<lean-4.24.0-binary>",
            "--device", "cuda", "--seeds", ",".join(map(str, curated["seeds"])),
            "--max-attempts", str(curated["budget"]["max_attempts_per_role"]),
            "--max-calls", str(curated["budget"]["max_calls"]),
            "--max-new-tokens", str(curated["budget"]["max_new_tokens_per_call"]),
            "--max-total-new-tokens", str(curated["budget"]["max_total_new_tokens"]),
            "--wall-seconds", str(curated["budget"]["wall_seconds"]), "--output", "<new-raw-result>"],
        "dataset": curated["dataset"], "checkpoint": curated["model"], "seeds": curated["seeds"],
        "result": "passed", "result_meaning": "bounded_real_cuda_runtime_completed_not_task_or_semantic_success",
        "metrics": curated["metrics"], "lean": curated["lean"], "diagnostic_only": True,
        "executed_model_roles": curated["executed_model_roles"],
        "end_to_end_certificate_observed": curated["end_to_end_certificate_observed"],
        "promotion_eligible": False, "evolve_integrated": False, "evaluation_tier": "l1_mechanism",
        "full_experiment_status": "not_reproduced_high_cost",
        "provenance": {"commit": curated["provenance"]["code_commit"],
            "artifact_path": "docs/gpu-validations/specguard-a100-20261021.json",
            "executed_source_sha256": curated["provenance"]["executed_source_sha256"],
            "raw_runner_artifact_sha256": curated["provenance"]["raw_runner_artifact_sha256"]}}
    if errors := validate_gpu_receipt(receipt):
        raise ValueError("; ".join(errors))
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, required=True)
    parser.add_argument("--lean-bin", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gpu-receipt", type=Path)
    args = parser.parse_args()
    if args.output.exists():
        raise FileExistsError("immutable curated output already exists")
    if args.gpu_receipt and args.gpu_receipt.exists():
        raise FileExistsError("immutable GPU receipt already exists")
    data = args.raw.read_bytes()
    output = curate(json.loads(data), LeanKernel(args.lean_bin), hashlib.sha256(data).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2, allow_nan=False)+"\n",
                           encoding="utf-8")
    if args.gpu_receipt:
        receipt = gpu_receipt(output, datetime.now(timezone.utc).isoformat())
        args.gpu_receipt.parent.mkdir(parents=True, exist_ok=True)
        args.gpu_receipt.write_text(json.dumps(receipt, ensure_ascii=False, indent=2, allow_nan=False)+"\n")
    print(json.dumps(output["metrics"], ensure_ascii=False))


if __name__ == "__main__":
    main()
