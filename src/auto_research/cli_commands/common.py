from __future__ import annotations

from auto_research.reproductions.manifest import PaperManifest
from pathlib import Path
from auto_research.config import ResearchConfig
from auto_research.reproductions.schema import aggregate_seed_metrics
import argparse
import datetime as dt
from auto_research.reproductions.schema import enrich_result
import json
from auto_research.runtime import runtime_summary


def _add_runtime_arguments(command: argparse.ArgumentParser) -> None:
    command.add_argument(
        "--device",
        help="execution device: auto, cpu, mps, cuda or cuda:<index> (default: env or auto)",
    )
    command.add_argument(
        "--cpu-threads",
        type=int,
        help="PyTorch intra-op threads when running on Linux/CPU",
    )


def _format_agent_evolution_summary(validation: dict[str, float]) -> str:
    labels = (
        ("Joint success", "joint_success"),
        ("average cost", "average_cost"),
        ("reuse", "reuse_rate"),
    )
    return "; ".join(
        f"{label}: {validation[key]:.4f}" for label, key in labels if key in validation
    )


def _run_reproduction(
    adapter,
    dataset_dir,
    seed,
    seeds,
    budget,
    budget_seconds=None,
):
    from auto_research.reproductions.execution import run_with_budget

    result = run_with_budget(
        adapter,
        dataset_dir,
        seed,
        budget,
        timeout_override=budget_seconds,
    )
    try:
        import torch

        result["runtime"] = runtime_summary(torch)
    except ImportError:
        result["runtime"] = runtime_summary()
    result["seed"] = seed
    return enrich_result(
        adapter,
        result,
        seeds=seeds,
        dataset_dir=dataset_dir,
        budget=budget,
    )


def _load_batch_state(path: Path | None) -> dict:
    if path and path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError(f"unsupported reproduction state schema in {path}")
        return payload
    return {"schema_version": 1, "completed": {}}


def _write_batch_state(path: Path | None, state: dict) -> None:
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _write_reproduction_batch_summary(entries, output_dir, seeds_by_adapter, budget):
    grouped = {}
    for adapter, result in entries:
        grouped.setdefault(adapter.key, {"adapter": adapter, "results": []})["results"].append(
            result
        )
    payload = {
        "schema_version": 2,
        "seeds_by_adapter": {key: list(values) for key, values in seeds_by_adapter.items()},
        "budget": budget,
        "papers": {},
    }
    for key, group in grouped.items():
        raw = group["results"]
        payload["papers"][key] = {
            "manifest": PaperManifest.from_adapter(group["adapter"]).to_dict(),
            "seed_results": raw,
            "aggregate_metrics": aggregate_seed_metrics(raw),
            "formal_comparison": len(raw) >= 3,
        }
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"batch-summary-{dt.datetime.now().strftime('%Y%m%d-%H%M%S-%f')}.json"
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path


def _run_config(args: argparse.Namespace) -> ResearchConfig:
    if args.config:
        return ResearchConfig.from_file(args.config)
    if not args.topic or not args.track:
        raise ValueError("--topic and --track are required without --config")
    return ResearchConfig(
        topic=args.topic,
        track=args.track,
        max_trials=args.trials,
        max_papers=args.papers,
        output_dir=args.output_dir,
        allow_network=not args.offline,
        force_rerun=args.force_rerun,
    )


def _init_config(path: Path, track: str) -> None:
    if path.exists():
        raise ValueError(f"refusing to overwrite {path}")
    payload = {
        "topic": "efficient post-training"
        if track == "llm"
        else "ranking loss and negative sampling",
        "track": track,
        "max_papers": 8,
        "max_trials": 8,
        "seed": 42,
        "output_dir": "runs",
        "dataset_dir": "data",
        "allow_network": True,
        "proposal_command": None,
        "proposal_timeout_seconds": 300,
        "cache_dir": ".auto-research/cache",
        "force_rerun": False,
        "experiment_revision": None,
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
