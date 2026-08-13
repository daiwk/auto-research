"""Budget-matched, resumable evaluation matrices for public checkpoints."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
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
    max_new_tokens: int = 16
    prompt_style: str = "direct"
    use_hint: bool = True
    image_size: int = 0

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

        cell = cls(
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
            max_new_tokens=int(row.get("max_new_tokens", 16)),
            prompt_style=str(row.get("prompt_style", "direct")),
            use_hint=bool(row.get("use_hint", True)),
            image_size=int(row.get("image_size", 0)),
        )
        if cell.max_new_tokens < 1 or cell.image_size < 0:
            raise ValueError("matrix max_new_tokens must be positive and image_size non-negative")
        return cell

    def comparison_budget(self) -> dict[str, Any]:
        """Fields that must match before two checkpoints can share a ranking."""
        common = {
            "annotations": str(self.annotations),
            "image_root": str(self.image_root),
            "split": self.split,
            "maximum_examples": self.maximum_examples,
        }
        if self.family == "generative":
            common.update({
                "max_new_tokens": self.max_new_tokens,
                "prompt_style": self.prompt_style,
                "use_hint": self.use_hint,
                "image_size": self.image_size,
            })
        return common


def load_matrix(path: Path) -> tuple[MatrixCell, ...]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    rows = payload.get("cells", payload) if isinstance(payload, dict) else payload
    if not isinstance(rows, list) or not rows:
        raise ValueError("matrix config must contain a non-empty cells list")
    cells = tuple(MatrixCell.from_dict(row, path.parent) for row in rows)
    names = [cell.name for cell in cells]
    if len(names) != len(set(names)):
        raise ValueError("matrix cell names must be unique")
    _validate_comparison_groups(cells)
    return cells


def _validate_comparison_groups(cells: tuple[MatrixCell, ...]) -> None:
    budgets: dict[tuple[str, str], tuple[str, dict[str, Any]]] = {}
    for cell in cells:
        group = (cell.family, cell.benchmark)
        budget = cell.comparison_budget()
        if group not in budgets:
            budgets[group] = (cell.name, budget)
            continue
        reference_name, reference = budgets[group]
        if budget != reference:
            changed = sorted(key for key in budget if budget[key] != reference[key])
            raise ValueError(
                f"matrix group {cell.family}/{cell.benchmark} is not budget-matched: "
                f"{cell.name} differs from {reference_name} in {', '.join(changed)}"
            )


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
    config_digest = _matrix_digest(cells, seed)
    state = _read_state(state_path, config_digest=config_digest, seed=seed)
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
                    max_new_tokens=cell.max_new_tokens,
                    prompt_style=cell.prompt_style, use_hint=cell.use_hint,
                    image_size=cell.image_size, seed=seed, offline=offline,
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
                "selected_examples": metadata.get(
                    "selected_examples", metadata.get("images")
                ),
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


def _matrix_digest(cells: tuple[MatrixCell, ...], seed: int) -> str:
    payload = {
        "seed": seed,
        "cells": [
            {
                **asdict(cell),
                "annotations": str(cell.annotations),
                "image_root": str(cell.image_root),
                "checkpoint_path": str(cell.checkpoint_path) if cell.checkpoint_path else None,
            }
            for cell in cells
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_state(path: Path, *, config_digest: str, seed: int) -> dict[str, Any]:
    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError("unsupported checkpoint matrix schema")
        recorded = payload.get("config_sha256")
        if recorded is None and payload.get("cells"):
            raise ValueError(
                "legacy checkpoint matrix state has no config digest; use a new output directory"
            )
        if recorded is not None and recorded != config_digest:
            raise ValueError(
                "checkpoint matrix config/seed changed; use a new output directory"
            )
        return payload
    return {
        "schema_version": 1,
        "config_sha256": config_digest,
        "seed": seed,
        "cells": {},
        "updated_at": None,
    }


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
        lines += [
            f"## {family} / {benchmark}", "",
            "| checkpoint | revision | 样本 | 状态 | 指标 | sec/example | 峰值显存 MiB | batch |",
            "|---|---|---:|---|---|---:|---:|---:|",
        ]
        for name, row in rows:
            metrics = ", ".join(
                f"{key}={value:.4f}" for key, value in row.get("metrics", {}).items()
                if key != "seed" and isinstance(value, (int, float))
            ) or "—"
            efficiency = row.get("efficiency") or {}
            latency = efficiency.get("seconds_per_new_prediction")
            if latency is None and row.get("family") == "retrieval":
                selected = row.get("selected_examples") or 0
                total = efficiency.get("inference_seconds")
                latency = total / selected if total is not None and selected else None
            memory = efficiency.get("peak_gpu_memory_mb")
            revision = str(row.get("resolved_revision") or "—")[:12]
            latency_text = f"{latency:.4f}" if latency is not None else "—"
            memory_text = f"{memory:.1f}" if memory is not None else "—"
            lines.append(
                f"| `{name}` | `{revision}` | {row.get('selected_examples', '—')} | "
                f"{row['status']} | {metrics} | {latency_text} | {memory_text} | "
                f"{row.get('batch_size', '—')} |"
            )
        lines.append("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
