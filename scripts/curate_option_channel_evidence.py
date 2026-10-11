#!/usr/bin/env python3
"""Archive a real public checkpoint's six-policy security diagnostic."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--source-commit", required=True)
    a = p.parse_args()
    report = json.loads(a.input.read_text())
    if (report["adapter_key"] != "option-channel-attack" or report["labels_selected_on_evaluation"]
            or report["calibration_seed"] == report["evaluation_seed"] or len(report["rows"]) != 6):
        raise ValueError("six-policy calibration/heldout runtime required")
    commit = subprocess.check_output(["git", "rev-parse", a.source_commit], cwd=ROOT, text=True).strip()
    for row in report["rows"]:
        attack = row["option_attack"]
        if (attack["originally_correct_blocks"] == 0) != (attack["asr_open"] is None):
            raise ValueError("empty ASR denominator must remain undefined")
    summaries = {r["policy"]: {**r["option_attack"], "asr_ci95": r["option_asr_ci95"],
                               "irrelevant_text_asr": r["irrelevant_text"]["asr_open"]} for r in report["rows"]}
    artifact = "docs/agent-research/2610.12292-option-channel-attack/metrics/laya-a100.json"
    receipt_path = "docs/gpu-validations/option-channel-attack-a100-20261011.json"
    dataset = {"id": "native-six-policy-guardbench-style", "revision": commit,
               "protocol": report["synthetic_protocol"], "calibration_seed": report["calibration_seed"],
               "evaluation_seed": report["evaluation_seed"]}
    payload = {"schema_version": 2, "manifest_ref": "agent-research:option-channel-attack",
               "method": "option-channel-attack", "dataset": dataset["id"], "seeds": [43],
               "metrics": summaries, "runtime_details": report,
               "evaluation_protocol": {"tier": "l1_mechanism", "diagnostic_only": True,
                                       "formal_comparison": False, "seeds": [43],
                                       "claim_policy": report["claim_scope"],
                                       "qualification": "synthetic guardrail diagnostic, not agent task capability"},
               "provenance": {"original_code_commit": commit, "artifact_path": artifact,
                              "dataset_fingerprint": hashlib.sha256(json.dumps(
                                  [r["evaluated_state_digest"] for r in report["rows"]]).encode()).hexdigest()}}
    sources = ("src/auto_research/system_one/option_channel.py", "scripts/run_option_channel.py")
    receipt = {"schema_version": 1, "adapter_key": "option-channel-attack", "validated_at": "2026-10-11",
               "accelerator": {"vendor": "NVIDIA", "model": "A100-SXM4-80GB"},
               "command": ["python", "scripts/run_option_channel.py", "--checkpoint", "checkpoints/laya",
                           "--output", "runs/option-channel-42-43.json", "--count", "24", "--device", "cuda:0"],
               "dataset": dataset, "checkpoint": report["checkpoint"], "result": "passed",
               "metrics": summaries, "evaluation_tier": "l1_mechanism",
               "executed_source_sha256": {s: hashlib.sha256(subprocess.check_output(
                   ["git", "show", f"{commit}:{s}"], cwd=ROOT)).hexdigest() for s in sources},
               "limitations": [report["claim_scope"], "native synthetic rows, not author's byte-identical benchmark",
                               "four label candidates and one model only; not original full attack sweep"],
               "provenance": {"commit": commit, "artifact_path": receipt_path,
                              "metrics_artifact": artifact, "checkpoint_committed": False}}
    for relative, value in ((artifact, payload), (receipt_path, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
