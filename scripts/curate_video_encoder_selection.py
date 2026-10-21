#!/usr/bin/env python3
"""Curate only successful, source-bound real-feature L1 selection receipts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.gpu_validation import validate_gpu_receipt  # noqa: E402

KEY = "video-encoder-selection"
ARTIFACT = "docs/gpu-validations/video-encoder-selection-a100-20261021.json"
SOURCES = ["scripts/run_video_encoder_selection.py",
           "src/auto_research/foundation_models/video_encoder_selection.py"]


def summarize(report: dict) -> dict:
    if (report.get("adapter_key") != KEY or report.get("status") != "passed"
            or report.get("protocol_id") != "video-encoder-conditional-selection-smolvlm-l1-v1"
            or report.get("evaluation_tier") != "l1_mechanism" or report.get("diagnostic_only") is not True
            or report.get("promotion_eligible") is not False or report.get("evolve_integrated") is not False):
        raise ValueError("only successful non-promotable L1 real-feature runs may be curated")
    protocol = report.get("protocol", {})
    required = {"frozen_real_image_encoder": True, "independent_frame_encoding": True,
                "question_input_embedding_mean": True, "inference_gold_read": False,
                "test_read": False, "training_steps": 0, "refiner_enabled": False,
                "quota_source": "external_uniform_not_SITE",
                "scene_statistic": "explicit_mean_pooled_visual_cosine_proxy",
                "full_SITE_selection_reproduced": False, "video_QA_capability_evaluated": False}
    if any(protocol.get(name) != value for name, value in required.items()):
        raise ValueError("missing frozen-feature/no-gold/no-refiner and external-input scope contracts")
    checkpoint = report.get("checkpoint", {})
    if (not checkpoint.get("id") or not re.fullmatch(r"[0-9a-f]{40}", checkpoint.get("revision", ""))
            or not re.fullmatch(r"[0-9a-f]{64}", checkpoint.get("content_sha256", ""))
            or not checkpoint.get("files_sha256")):
        raise ValueError("real immutable public checkpoint and content hashes required")
    rows = report.get("rows", [])
    expected = report.get("dataset", {}).get("examples")
    if not rows or len(rows) != expected or len({row.get("id") for row in rows}) != expected:
        raise ValueError("every manifest case must be present exactly once")
    for row in rows:
        if row.get("status") != "passed" or "error" in row:
            raise ValueError("failed/partial runs remain evidence, but cannot receive a passing receipt")
        metrics = row.get("metrics", {})
        if any(not isinstance(value, (int, float)) or not math.isfinite(value) for value in metrics.values()):
            raise ValueError("all metrics must be finite scalars")
        if any(metrics.get(name) != 0 for name in (
            "source_embedding_max_error", "source_position_max_error", "source_stream_max_error"
        )) or not 0 <= metrics.get("objective_trace_absolute_error", math.inf) <= 1e-7:
            raise ValueError("source alignment or independent objective identity failed")
        selected = row.get("selected_source_indices", [])
        frame_indices = row.get("source_frame_indices", [])
        timestamps = row.get("source_timestamps", [])
        tokens = metrics.get("tokens_per_frame", 0)
        if (len(selected) != protocol["budget"] or len(set(selected)) != len(selected)
                or metrics.get("selected_tokens") != len(selected)
                or row.get("quotas") != row.get("actual_quotas")
                or sum(row.get("quotas", [])) != len(selected)
                or not re.fullmatch(r"[0-9a-f]{64}", row.get("video_sha256", ""))
                or len(set(frame_indices)) != protocol["frames"]
                or frame_indices != sorted(frame_indices)
                or len(timestamps) != protocol["frames"]
                or any(not math.isfinite(value) for value in timestamps)
                or any(second <= first for first, second in zip(timestamps, timestamps[1:]))
                or not isinstance(tokens, int) or tokens < 1
                or metrics.get("source_frames") != protocol["frames"]
                or metrics.get("candidate_tokens") != tokens * protocol["frames"]
                or any(not isinstance(index, int) or not 0 <= index < tokens * protocol["frames"]
                       for index in selected)):
            raise ValueError("fixed budget/source identity/video provenance mismatch")
        actual = [sum(index // tokens == frame for index in selected) for frame in range(protocol["frames"])]
        positions = row.get("selected_source_positions", [])
        width = math.isqrt(tokens)
        expected_positions = [[timestamps[index // tokens], ((index % tokens) // width + .5) / width,
                               ((index % tokens) % width + .5) / width] for index in selected]
        if (actual != row["actual_quotas"] or width * width != tokens or positions != expected_positions
                or len({tuple(position) for position in positions}) != len(selected)):
            raise ValueError("selected indices, quotas and original time/spatial identities differ")
    names = set(rows[0]["metrics"])
    if any(set(row["metrics"]) != names for row in rows):
        raise ValueError("case metric schemas differ")
    return {"examples": len(rows), **{
        name + ("_max" if "error" in name else "_mean"):
        (max(row["metrics"][name] for row in rows) if "error" in name
         else sum(row["metrics"][name] for row in rows) / len(rows)) for name in sorted(names)
    }}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = json.loads(args.input.read_text())
    metrics = summarize(report)
    if report.get("device") != "cuda" or not re.search(r"\bA(?:100|30)\b", report.get("accelerator", {}).get("model", "")):
        raise ValueError("passing receipt requires actual NVIDIA A100/A30 execution")
    if report.get("accelerator", {}).get("vendor") != "NVIDIA":
        raise ValueError("NVIDIA device required")
    if not re.fullmatch(r"[0-9a-f]{40}", args.source_commit) or report.get("code_revision") != args.source_commit:
        raise ValueError("executed immutable source commit must match the declared source commit")
    executed = report.get("executed_source_sha256", {})
    if set(executed) != set(SOURCES):
        raise ValueError("complete frozen source inventory required")
    for source in SOURCES:
        content = subprocess.check_output(["git", "show", f"{args.source_commit}:{source}"], cwd=ROOT)
        if hashlib.sha256(content).hexdigest() != executed[source]:
            raise ValueError(f"executed source differs from frozen commit: {source}")
    dataset = {**report["dataset"], "split": "public_unlabelled_runtime_sample_not_benchmark_test",
               "video_sha256": {row["id"]: row["video_sha256"] for row in report["rows"]}}
    command = ["python", "scripts/run_video_encoder_selection.py", "--checkpoint", "<cached-public-checkpoint>",
               "--checkpoint-id", report["checkpoint"]["id"], "--checkpoint-revision", report["checkpoint"]["revision"],
               "--manifest", "<public-video-manifest>", "--output-dir", "<new-run>", "--device", "cuda",
               "--frames", str(report["protocol"]["frames"]), "--budget", str(report["protocol"]["budget"]),
               "--seed", str(report["seed"])]
    receipt = {"schema_version": 1, "adapter_key": KEY,
               "validated_at": datetime.now(timezone.utc).isoformat(), "accelerator": report["accelerator"],
               "command": command, "dataset": dataset, "checkpoint": report["checkpoint"],
               "seed": report["seed"], "result": "passed", "metrics": metrics,
               "diagnostic_only": True, "promotion_eligible": False,
               "evaluation_tier": "l1_mechanism", "executed_source_sha256": executed,
               "protocol": report["protocol"],
               "provenance": {"commit": args.source_commit, "artifact_path": ARTIFACT,
                              "raw_result_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest()}}
    errors = validate_gpu_receipt(receipt)
    if errors:
        raise ValueError("; ".join(errors))
    args.output_dir.mkdir(parents=True, exist_ok=False)
    summary = {"schema_version": 2, "manifest_ref": "foundation-models:video-encoder-selection",
               "adapter_key": KEY, "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
               "promotion_eligible": False, "evolve_integrated": False, "seed": report["seed"],
               "dataset": dataset, "checkpoint": {name: report["checkpoint"][name] for name in ("id", "revision", "content_sha256")},
               "metrics": metrics, "protocol": report["protocol"], "code_revision": args.source_commit,
               "gpu_validation_artifact": ARTIFACT,
               "evaluation_protocol": {"tier": "l1_mechanism", "seeds": [report["seed"]],
                   "formal_comparison": False, "claim_policy": "fixed-budget real-feature runtime; not video QA capability"},
               "provenance": {"artifact_path": "docs/foundation-models/2610.06616-video-encoder-selection/metrics/component-a100-seed42.json",
                   "dataset_fingerprint": dataset["manifest_sha256"], "code_commit": args.source_commit,
                   "raw_result_sha256": hashlib.sha256(args.input.read_bytes()).hexdigest()}}
    for name, payload in (("gpu-receipt.json", receipt), ("component-metrics.json", summary)):
        (args.output_dir / name).write_text(json.dumps(payload, indent=2, ensure_ascii=False, allow_nan=False) + "\n")
    print(json.dumps({"status": "passed", "examples": metrics["examples"], "output_dir": str(args.output_dir)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
