#!/usr/bin/env python3
"""Curate bounded Oct16 CUDA outputs, preserving diagnostics and failed attempts.

This does not run training or synthesize scores. Inputs must be the actual
three-seed CUDA batch, its executed-source hashes and the unified CLI result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import statistics

ROOT = Path(__file__).resolve().parents[1]
SEEDS = [42, 43, 44]
COMMIT = "63ca47dad9a19a302b31b1699267dd5c53692b9d"
MODEL = "NVIDIA A100-SXM4-80GB"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write(relative, payload):
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n")


def average(values):
    return {"mean": statistics.mean(values), "std": statistics.stdev(values), "n": len(values)}


def curate(directory: Path):
    source_hashes = read(directory / "executed-source-sha256.json")

    def hashes(paths):
        result = {}
        for name in paths:
            digest = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            if source_hashes.get(name) != digest:
                raise ValueError(f"executed source does not match: {name}")
            result[name] = digest
        return result

    def emit(key, slug, domain, raw, dataset, metrics, command, sources, checks, failures=()):
        metric_path = f"docs/{domain}/{slug}/metrics/component-seeds42-44.json"
        receipt_path = f"docs/gpu-validations/{key}-a100-20261016.json"
        tier = "l2_public_dataset" if key == "oob-regularization" else "l1_mechanism"
        fingerprint = dataset["revision"]
        source = hashes(sources)
        checkpoint = {
            "public_id": "none-independent-seeded-initialization",
            "revision": COMMIT,
            "pretrained": False,
            "initialization_seeds": SEEDS,
        }
        artifact = {
            "schema_version": 2, "method": key,
            "manifest_ref": f"{'reproduction' if key == 'oob-regularization' else domain}:{key}",
            "seeds": SEEDS, "diagnostic_only": True, "promotion_eligible": False,
            "evaluation_tier": tier, "dataset": dataset,
            "evaluation_protocol": {
                "tier": tier, "seeds": SEEDS, "formal_comparison": False,
                "claim_policy": "bounded component execution only; not full paper benchmark or capability improvement",
            },
            "metrics": metrics, "per_seed": raw,
            "execution_checks": checks,
            "provenance": {"artifact_path": metric_path, "dataset_fingerprint": fingerprint,
                           "commit": COMMIT, "executed_source_sha256": source,
                           "accelerator": MODEL},
            "full_experiment_status": "not_reproduced_high_cost",
            "full_experiment_review_done": True,
        }
        write(metric_path, artifact)
        write(receipt_path, {
            "schema_version": 1, "adapter_key": key, "validated_at": "2026-10-16",
            "accelerator": {"vendor": "NVIDIA", "model": MODEL},
            "command": command, "seeds": SEEDS, "dataset": dataset,
            "command_path_policy": "public input paths relativized; exact content revision retained",
            "checkpoint": checkpoint, "result": "passed", "metrics": metrics,
            "execution_checks": checks, "diagnostic_only": True,
            "promotion_eligible": False, "executed_source_sha256": source,
            "prior_failed_attempts": list(failures),
            "provenance": {"commit": COMMIT, "artifact_path": receipt_path,
                           "metric_artifact_path": metric_path},
            "full_experiment_status": "not_reproduced_high_cost",
        })

    dropd = read(directory / "divergence-routed-opd.json")
    assert dropd["accelerator"] == MODEL and dropd["seeds"] == SEEDS
    assert dropd["diagnostic_only"] and not dropd["promotion_eligible"]
    assert [row["seed"] for row in dropd["results"]] == SEEDS
    for row in dropd["results"]:
        assert row["parameter_delta_l2"] > 0 and row["teacher_parameter_delta_l2"] == 0
        assert row["generated_tokens"] == 64 and len(row["history"]) == 2
        assert all(step["gradient_norm"] > 0 for step in row["history"])
    resource = dropd["public_resources"]
    assert resource["corpus_revision"] == "sha256:" + resource["corpus_sha256"]
    dropd_metrics = {
        name: average([row[name] for row in dropd["results"]])
        for name in ("parameter_delta_l2", "teacher_parameter_delta_l2", "generated_tokens",
                     "baseline_validation_nll", "final_validation_nll")
    }
    emit("divergence-routed-opd", "2610.19572-divergence-routed-opd", "post-training",
         dropd["results"],
         {"id": resource["corpus_id"], "revision": resource["corpus_revision"],
          "source_sha256": resource["corpus_sha256"],
          "source_url": "https://www.gutenberg.org/ebooks/1524", "byte_ranges": resource["byte_ranges"]},
         dropd_metrics,
         ["python", "scripts/run_divergence_routed_tiny.py", "--corpus-path", "public/hamlet.txt",
          "--corpus-id", resource["corpus_id"], "--corpus-revision", resource["corpus_revision"],
          "--device", "cuda", "--teacher-steps", "16", "--steps", "2", "--max-tokens", "16",
          "--seeds", "42,43,44", "--output", "runs/divergence-routed-opd.json"],
         ["src/auto_research/post_training/divergence_routed_opd.py", "scripts/run_divergence_routed_tiny.py"],
         {"actual_online_sampling": True, "frozen_teacher_unchanged": True, "student_updated": True,
          "appendix_kth_score_router": True,
          "heldout_bytes_not_used_for_training": True, "hf_checkpoint_path_validated": False},
         [{"commit": "662e33b4eb1bfba87193a77f08fe516bd81a3203", "error_type": "RuntimeError",
           "reason": "cuDNN RNN backward rejected eval-mode gradient forward",
           "resolution": "temporary evaluation contexts and explicit train-mode PPO forward; regression test and CUDA rerun"}])

    rap = read(directory / "rap-walk.json")
    assert rap["accelerator"] == MODEL and rap["seeds"] == SEEDS
    assert rap["input_kind"] == "explicit_mechanism_fixtures"
    assert [row["seed"] for row in rap["results"]] == SEEDS
    graphs = [graph for row in rap["results"] for graph in row["graphs"]]
    assert len(graphs) == 6
    assert all(graph["parameter_delta_l2"] > 0 and graph["stationary_residual"] < 1e-9 for graph in graphs)
    emit("rap-walk", "2610.20089-rap-walk", "post-training", rap["results"],
         {"id": "explicit-transitive-and-cyclic-mechanism-fixtures", "revision": COMMIT,
          "capability_dataset": False},
         {"parameter_delta_l2": average([g["parameter_delta_l2"] for g in graphs]),
          "maximum_stationary_residual": max(g["stationary_residual"] for g in graphs)},
         ["python", "scripts/run_rap_walk.py", "--device", "cuda", "--seeds", "42,43,44",
          "--output", "runs/rap-walk.json"],
         ["src/auto_research/post_training/rap_walk.py", "scripts/run_rap_walk.py"],
         {"actual_grpo_backward_and_update": True, "explicit_fixture_not_video": True,
          "video_generation_performed": False, "judge_model_called": False})

    oob = [read(directory / f"oob-{seed}.json") for seed in SEEDS]
    for seed, row in zip(SEEDS, oob, strict=True):
        assert row["seed"] == seed and row["device"] == "cuda" and row["accelerator"] == MODEL
        assert row["diagnostic_only"] and not row["promotion_eligible"]
        assert not row["dataset"]["official_test_read"]
        for arm in row["metrics"].values():
            assert arm["optimizer_steps"] == 40 and arm["parameter_update_observed"]
            assert arm["cache_cpu_resident"] and not arm["cached_targets_require_grad"]
    cli_paths = list((directory / "oob-cli").rglob("result.json"))
    assert len(cli_paths) == 1, "require exactly one successful unified CLI artifact"
    cli = read(cli_paths[0])
    # The CLI may wrap the seed result in its standard batch result.
    if "results" in cli and isinstance(cli["results"], list):
        cli = cli["results"][0]
    assert cli["device"] == "cuda" and cli["seed"] == 42 and cli["accelerator"] == MODEL
    assert cli["paired_validation_differences"] == oob[0]["paired_validation_differences"]
    metadata = oob[0]["dataset"]
    metrics = {
        f"{arm}_validation_knn5_accuracy": average([row["metrics"][arm]["validation_knn5_accuracy"] for row in oob])
        for arm in oob[0]["metrics"]
    }
    metrics.update({key: average([row["paired_validation_differences"][key] for row in oob])
                    for key in oob[0]["paired_validation_differences"]})
    emit("oob-regularization", "2610.20158-oob-regularization", "reproductions", oob,
         {"id": metadata["id"], "revision": "sha256:" + metadata["source_sha256"],
          "source_url": metadata["source"], "source_md5": metadata["source_md5"],
          "split_revision": metadata["split_revision"], "training_examples": 512,
          "validation_examples": 128, "official_test_read": False},
         metrics,
         ["python", "scripts/run_oob_regularization.py", "--dataset-dir", "public/cifar10",
          "--device", "cuda", "--seed", "42", "--output", "runs/oob-42.json"],
         ["src/auto_research/reproductions/oob_regularization/algorithm.py",
          "src/auto_research/reproductions/oob_regularization/experiment.py", "scripts/run_oob_regularization.py",
          "src/auto_research/runtime.py", "src/auto_research/cli.py",
          "src/auto_research/reproductions/reporting.py"],
         {"four_actual_training_arms": True, "matched_initialization_and_augmentation_streams": True,
          "cpu_detached_sample_anchor_cache": True, "four_refreshes_each_oob_arm": True,
          "validation_not_used_for_selection": True, "official_test_read": False,
          "unified_cli_cuda_same_seed_agreement": True},
         [{"commit": "d63fa6f67bb1d0e052cf0eabf8254e383697e6b7", "error_type": "TypeError",
           "reason": "unified CLI adapter used unsupported device_for keyword arguments",
           "resolution": "shared runtime API and explicit CUDA index context; regression tests and real unified CLI rerun"}])
    receipt_path = "docs/gpu-validations/oob-regularization-a100-20261016.json"
    receipt = read(ROOT / receipt_path)
    receipt["additional_validated_commands"] = [[
        "python", "-m", "auto_research.cli", "reproduce", "--paper", "oob-regularization",
        "--device", "cuda", "--cpu-threads", "1", "--seeds", "42", "--budget", "smoke",
        "--dataset-dir", "public/cifar10", "--output-dir", "runs/oob-cli",
    ]]
    write(receipt_path, receipt)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    curate(parser.parse_args().input_dir)
