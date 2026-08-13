"""Budget-matched, resumable evaluation matrices for public checkpoints."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Callable

from .benchmarks import run_public_benchmark
from .checkpoint import CheckpointPredictionConfig, generate_checkpoint_predictions
from .retrieval import RetrievalPredictionConfig, generate_retrieval_predictions


@dataclass(frozen=True)
class MatrixCell:
    name: str
    family: str
    benchmark: str
    model_id: str
    annotations: Path
    image_root: Path
    checkpoint_path: Path | None = None
    revision: str = "main"
    split: str = "test"
    maximum_examples: int | None = None
    batch_sizes: tuple[int, ...] = (1,)
    score_batch_size: int = 256

    @classmethod
    def from_dict(cls, row: dict[str, Any], root: Path) -> "MatrixCell":
        family = str(row.get("family", "generative"))
        if family not in {"generative", "retrieval"}:
            raise ValueError("matrix family must be generative or retrieval")
        batches = tuple(int(value) for value in row.get("batch_sizes", [1]))
        if not batches or min(batches) < 1:
            raise ValueError("matrix batch_sizes must contain positive integers")
        def resolve_path(value: str | None) -> Path | None:
            return (root / value).resolve() if value else None

        return cls(
            name=str(row["name"]), family=family,
            benchmark=str(row["benchmark"]), model_id=str(row["model_id"]),
            annotations=resolve_path(row["annotations"]),
            image_root=resolve_path(row["image_root"]),
            checkpoint_path=resolve_path(row.get("checkpoint_path")),
            revision=str(row.get("revision", "main")),
            split=str(row.get("split", "test")),
            maximum_examples=row.get("maximum_examples"),
            batch_sizes=batches,
            score_batch_size=int(row.get("score_batch_size", 256)),
        )


def load_matrix(path: Path) -> tuple[MatrixCell, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("cells", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows:
        raise ValueError("matrix config must contain a non-empty cells list")
    cells = tuple(MatrixCell.from_dict(row, path.parent) for row in rows)
    names = [cell.name for cell in cells]
    if len(names) != len(set(names)):
        raise ValueError("matrix cell names must be unique")
    return cells


def run_checkpoint_matrix(
    config: Path,
    output_dir: Path,
    *,
    seed: int = 42,
    offline: bool = False,
    generative_runner: Callable[..., dict[str, Any]] = generate_checkpoint_predictions,
    retrieval_runner: Callable[..., dict[str, Any]] = generate_retrieval_predictions,
) -> Path:
    """Run each compatible cell independently and preserve failures for resume.

    A generative VLM is never ranked against a retrieval encoder: the report
    groups cells by ``family`` and ``benchmark`` and only compares like with like.
    Existing completed rows are reused. CUDA OOM errors retry the explicitly
    configured smaller batch sizes without deleting already written predictions.
    """
    cells = load_matrix(config)
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / "matrix.json"
    state = _read_state(state_path)
    for cell in cells:
        prior = state["cells"].get(cell.name, {})
        if prior.get("status") == "completed":
            continue
        row = _run_cell(
            cell, output_dir, seed=seed, offline=offline,
            generative_runner=generative_runner,
            retrieval_runner=retrieval_runner,
        )
        state["cells"][cell.name] = row
        state["updated_at"] = datetime.now(timezone.utc).isoformat()
        _write_json(state_path, state)
        _write_report(output_dir / "report.md", state)
    return output_dir


def _run_cell(cell, output_dir, *, seed, offline, generative_runner, retrieval_runner):
    cell_dir = output_dir / cell.name
    cell_dir.mkdir(parents=True, exist_ok=True)
    predictions = cell_dir / "predictions.jsonl"
    errors = []
    for batch_size in cell.batch_sizes:
        try:
            if cell.family == "generative":
                metadata = generative_runner(CheckpointPredictionConfig(
                    benchmark=cell.benchmark, annotations=cell.annotations,
                    image_root=cell.image_root, output=predictions,
                    model_id=cell.model_id, checkpoint_path=cell.checkpoint_path,
                    revision=cell.revision, split=cell.split,
                    maximum_examples=cell.maximum_examples, batch_size=batch_size,
                    seed=seed, offline=offline,
                ))
            else:
                metadata = retrieval_runner(RetrievalPredictionConfig(
                    benchmark=cell.benchmark, annotations=cell.annotations,
                    image_root=cell.image_root, output=predictions,
                    model_id=cell.model_id, checkpoint_path=cell.checkpoint_path,
                    revision=cell.revision, split=cell.split,
                    maximum_images=cell.maximum_examples, batch_size=batch_size,
                    score_batch_size=cell.score_batch_size, seed=seed, offline=offline,
                ))
            result = run_public_benchmark(
                cell.benchmark, cell.annotations, (seed,),
                predictions=str(predictions), split=cell.split,
                maximum_examples=cell.maximum_examples,
            )
            return {
                "status": "completed", "family": cell.family,
                "benchmark": cell.benchmark, "model_id": cell.model_id,
                "resolved_revision": metadata.get("resolved_revision"),
                "batch_size": batch_size,
                "metrics": result.seed_results[0],
                "efficiency": {
                    key: metadata.get(key) for key in (
                        "inference_seconds", "seconds_per_new_prediction",
                        "peak_gpu_memory_mb",
                    )
                },
            }
        except (RuntimeError, OSError, ValueError) as exc:
            errors.append({"batch_size": batch_size, "error": str(exc)})
            if not _is_oom(exc):
                break
    return {
        "status": "failed", "family": cell.family,
        "benchmark": cell.benchmark, "model_id": cell.model_id, "errors": errors,
    }


def _is_oom(exc: BaseException) -> bool:
    text = str(exc).lower()
    return "out of memory" in text or "cuda oom" in text


def _read_state(path: Path) -> dict[str, Any]:
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError("unsupported checkpoint matrix schema")
        return payload
    return {"schema_version": 1, "cells": {}, "updated_at": None}


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _write_report(path: Path, payload: dict[str, Any]) -> None:
    lines = [
        "# 多模态 checkpoint 同预算矩阵", "",
        "> 只在相同 family 与 benchmark 内比较；生成式 VLM 与检索编码器不横向排名。", "",
    ]
    groups: dict[tuple[str, str], list[tuple[str, dict[str, Any]]]] = {}
    for name, row in payload["cells"].items():
        groups.setdefault((row["family"], row["benchmark"]), []).append((name, row))
    for (family, benchmark), rows in sorted(groups.items()):
        lines += [f"## {family} / {benchmark}", "", "| checkpoint | 状态 | 指标 | batch |", "|---|---|---|---:|"]
        for name, row in rows:
            metrics = ", ".join(
                f"{key}={value:.4f}" for key, value in row.get("metrics", {}).items()
                if key != "seed" and isinstance(value, (int, float))
            ) or "—"
            lines.append(f"| `{name}` | {row['status']} | {metrics} | {row.get('batch_size', '—')} |")
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
