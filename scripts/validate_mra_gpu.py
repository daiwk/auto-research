#!/usr/bin/env python3
"""Real CUDA execution/timeout checks; not a model-quality benchmark."""
from __future__ import annotations

import argparse
from dataclasses import replace
from datetime import datetime, timezone
import json
import multiprocessing as mp
import os
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from auto_research.evolution.engine import ModelEvolutionEngine, _effective_workers
from auto_research.evolution.models import EvolutionConfig, EvolutionTrial, Genome
from auto_research.experiment_contract import file_manifest, source_revision
from auto_research.runtime import device_for


class CudaProbeEvaluator:
    def evaluate(self, trial_id, generation, parent_id, genome, papers, rationale):
        import torch
        torch.manual_seed(42)
        device = device_for(torch)
        assert device.type == "cuda"
        started = time.time()
        layer = torch.nn.Linear(32, 8, device=device)
        inputs = torch.randn(16, 32, device=device)
        before = layer.weight.detach().clone()
        optimizer = torch.optim.SGD(layer.parameters(), lr=.01)
        loss = layer(inputs).square().mean()
        loss.backward()
        optimizer.step()
        torch.cuda.synchronize()
        delta = float((before - layer.weight).norm())
        assert delta > 0
        time.sleep(1 if rationale != "timeout" else 60)
        return EvolutionTrial(trial_id, generation, parent_id, genome,
                              {"fitness": -float(loss.detach())},
                              {"seeds": [42], "parameter_delta": delta,
                               "started": started, "finished": time.time()}, papers, rationale, 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()
    import torch
    assert torch.cuda.is_available()
    args.output.mkdir(parents=True, exist_ok=True)
    audit_path = args.output / "device-audit.jsonl"
    os.environ["AUTO_RESEARCH_DEVICE_AUDIT_LOG"] = str(audit_path)
    config = EvolutionConfig(
        "rankmixer", "movielens-100k", direction="longer unimixer", dataset_dir=args.data,
        output_dir=args.output / "evolve", generations=1, population=2, steps=3,
        seeds=(42,), workers=4, gpu_slots=1, device="auto", cpu_threads=1,
        maximum_users=128, maximum_items=512, evaluation_users=64,
        benchmark_suite="core", allow_network=False, trial_timeout_seconds=180,
    )
    assert _effective_workers(config) == 1
    result, _ = ModelEvolutionEngine(config, ROOT).run()
    assert len(result.trials) == 3 and all(t.status == "completed" for t in result.trials)
    assert result.baseline_test is not None and result.champion_test is not None
    metrics = {"seed": 42, "public_training_trials_completed": len(result.trials),
               "baseline_validation_ndcg": result.trials[0].validation["ndcg_at_10"],
               "baseline_final_loss": result.trials[0].training["final_loss"],
               "baseline_test_ndcg": result.baseline_test["ndcg_at_10"],
               "champion_test_ndcg": result.champion_test["ndcg_at_10"],
               "auto_effective_workers": _effective_workers(config)}
    for slots in (1, 2):
        probe_config = replace(config, gpu_slots=slots, trial_timeout_seconds=30)
        engine = ModelEvolutionEngine(probe_config, ROOT, CudaProbeEvaluator())
        specs = [(f"probe-{i}", 1, None, Genome(), (), "success") for i in range(2)]
        rows = list(engine._run_generation(engine.evaluator, specs))
        assert all(row.status == "completed" for row in rows), [r.error for r in rows]
        events = sorted([(r.training["started"], 1) for r in rows]
                        + [(r.training["finished"], -1) for r in rows])
        live = maximum = 0
        for _, delta in events:
            live += delta
            maximum = max(maximum, live)
        assert maximum <= slots
        metrics[f"slots_{slots}_maximum_cuda_overlap"] = maximum
        metrics[f"slots_{slots}_minimum_parameter_delta"] = min(r.training["parameter_delta"] for r in rows)
        engine = ModelEvolutionEngine(replace(probe_config, trial_timeout_seconds=12), ROOT, CudaProbeEvaluator())
        before = {p.pid for p in mp.active_children()}
        started = time.monotonic()
        rows = list(engine._run_generation(engine.evaluator, [
            (f"timeout-{i}", 1, None, Genome(), (), "timeout") for i in range(slots)
        ]))
        assert all(r.status == "failed" and "TimeoutError" in r.error for r in rows)
        assert {p.pid for p in mp.active_children()} <= before
        elapsed = time.monotonic() - started
        assert elapsed < 20
        metrics[f"slots_{slots}_timeout_reaped"] = len(rows)
        metrics[f"slots_{slots}_timeout_elapsed_seconds"] = elapsed
    audit = [json.loads(line) for line in audit_path.read_text().splitlines()]
    assert audit and all(row["resolved"].startswith("cuda") for row in audit)
    metrics["verified_cuda_device_resolutions"] = len(audit)
    artifact = "docs/gpu-validations/experiment-integrity-a100-20261007.json"
    receipt = {
        "schema_version": 1, "adapter_key": "experiment-integrity-runtime",
        "validated_at": datetime.now(timezone.utc).isoformat(),
        "accelerator": {"vendor": "NVIDIA", "model": torch.cuda.get_device_name()},
        "command": ["python", "scripts/validate_mra_gpu.py", "--data", "data", "--output", "runs/mra-gpu", "--commit", args.commit],
        "dataset": {"name": "MovieLens-100k", "revision": file_manifest(args.data),
                    "source": "https://files.grouplens.org/datasets/movielens/ml-100k.zip",
                    "maximum_users": 128, "maximum_items": 512, "evaluation_users": 64},
        "checkpoint": {"model_id": "rankmixer-random-initialization", "revision": "seed42"},
        "result": "passed", "metrics": metrics,
        "provenance": {"commit": args.commit, "source_fingerprint": source_revision(), "artifact_path": artifact},
        "boundary": "CUDA runtime and scheduling smoke verification; three training steps and one seed, not a quality comparison",
    }
    (args.output / "receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
