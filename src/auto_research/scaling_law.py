"""Budget-matched empirical scaling curves for the trainable micro LLM."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
from typing import Callable

import numpy as np

from .evolution.llm import MicroLLMEvaluator
from .evolution.models import Genome
from .runtime import exclusive_file_lock, runtime_summary


DEFAULT_SCALING_POINTS = "64x2:12000:6,64x2:24000:12,96x2:24000:12,128x3:48000:18"


@dataclass(frozen=True)
class ScalingBudgetPoint:
    dimensions: int
    layers: int
    train_tokens: int
    steps: int

    @property
    def key(self) -> str:
        return f"d{self.dimensions}-l{self.layers}-t{self.train_tokens}-s{self.steps}"


def parse_scaling_points(value: str) -> tuple[ScalingBudgetPoint, ...]:
    points = []
    for raw in value.split(","):
        raw = raw.strip()
        if not raw:
            continue
        try:
            shape, tokens, steps = raw.split(":")
            dimensions, layers = shape.lower().split("x")
            points.append(ScalingBudgetPoint(
                int(dimensions), int(layers), int(tokens), int(steps)
            ))
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"invalid scaling point {raw!r}; expected DIMxLAYERS:TOKENS:STEPS"
            ) from exc
    return tuple(points)


@dataclass(frozen=True)
class ScalingLawConfig:
    dataset_dir: Path = Path("data")
    output_dir: Path = Path("runs/scaling-law")
    points: tuple[ScalingBudgetPoint, ...] = parse_scaling_points(DEFAULT_SCALING_POINTS)
    seeds: tuple[int, ...] = (42,)
    architecture: str = "gpt_baseline"
    vocab_size: int = 1024
    batch_size: int = 2
    sequence_length: int = 64
    maximum_eval_tokens: int = 8192
    learning_rate: float = 3e-4
    optimizer: str = "adamw"
    allow_network: bool = True
    resume: bool = False

    def validate(self) -> None:
        if len(self.points) < 3:
            raise ValueError("scaling-law requires at least three budget points")
        if not self.seeds:
            raise ValueError("scaling-law requires at least one seed")
        if min(
            self.vocab_size, self.batch_size, self.sequence_length,
            self.maximum_eval_tokens,
        ) < 1 or self.learning_rate <= 0:
            raise ValueError("scaling-law sizes and learning rate must be positive")
        if len(set(self.points)) != len(self.points):
            raise ValueError("scaling-law budget points must be unique")
        for point in self.points:
            if min(point.dimensions, point.layers, point.train_tokens, point.steps) < 1:
                raise ValueError("scaling-law point values must be positive")
            if point.dimensions % 4:
                raise ValueError("scaling-law dimensions must be divisible by four heads")
            if point.train_tokens <= self.sequence_length + 1:
                raise ValueError("each data budget must exceed the sequence length")
        if len({(point.dimensions, point.layers) for point in self.points}) < 2:
            raise ValueError("scaling-law requires at least two model sizes")
        if len({point.train_tokens for point in self.points}) < 2:
            raise ValueError("scaling-law requires at least two data budgets")


EvaluatorFactory = Callable[[ScalingLawConfig, ScalingBudgetPoint], object]


class ScalingLawRunner:
    def __init__(
        self,
        config: ScalingLawConfig,
        evaluator_factory: EvaluatorFactory | None = None,
    ):
        self.config = config
        self.evaluator_factory = evaluator_factory or self._evaluator

    def _evaluator(self, config: ScalingLawConfig, point: ScalingBudgetPoint):
        return MicroLLMEvaluator(
            config.dataset_dir, "wikitext-2", point.steps, config.seeds,
            config.allow_network, point.train_tokens, config.maximum_eval_tokens,
            config.vocab_size, "core", "primary",
        )

    def run(self) -> tuple[dict, Path]:
        config = self.config
        config.validate()
        config.output_dir.mkdir(parents=True, exist_ok=True)
        points_dir = config.output_dir / "points"
        points_dir.mkdir(parents=True, exist_ok=True)
        fingerprint = _config_fingerprint(config)
        rows = []
        with exclusive_file_lock(config.output_dir / "result.json"):
            for index, point in enumerate(config.points):
                point_path = points_dir / f"{index:02d}-{point.key}.json"
                if config.resume and point_path.exists():
                    cached = json.loads(point_path.read_text(encoding="utf-8"))
                    if cached.get("config_fingerprint") != fingerprint:
                        raise ValueError(f"cached point does not match current config: {point_path}")
                    rows.append(cached["point"])
                    continue
                evaluator = self.evaluator_factory(config, point)
                genome = Genome(
                    architecture=config.architecture,
                    dimensions=point.dimensions,
                    layers=point.layers,
                    batch_size=config.batch_size,
                    sequence_length=config.sequence_length,
                    learning_rate=config.learning_rate,
                    optimizer=config.optimizer,
                    post_training="none",
                    post_steps=0,
                )
                trial = evaluator.evaluate(
                    f"scale-{index}", 0, None, genome, (),
                    "fixed architecture and optimizer; only declared compute/data budget changes",
                )
                summary = evaluator.summary()
                parameters = int(trial.training["parameters"])
                tokens_seen = point.steps * config.batch_size * config.sequence_length
                row = {
                    "id": f"scale-{index}",
                    **asdict(point),
                    "parameters": parameters,
                    "available_train_tokens": int(summary["train_tokens"]),
                    "tokens_seen": tokens_seen,
                    "estimated_training_flops": int(6 * parameters * tokens_seen),
                    "validation_lm_loss": float(trial.validation["lm_loss"]),
                    "validation_lm_loss_std": float(
                        trial.validation.get("lm_loss_std", 0.0)
                    ),
                    "validation_perplexity": float(trial.validation["perplexity"]),
                    "initial_training_loss": float(trial.training["initial_loss"]),
                    "final_training_loss": float(trial.training["final_loss"]),
                    "duration_seconds": float(trial.duration_seconds),
                    "device": trial.training["device"],
                }
                _write_json(point_path, {
                    "schema_version": 1,
                    "config_fingerprint": fingerprint,
                    "point": row,
                })
                rows.append(row)
            fit = fit_scaling_curves(rows)
            payload = {
                "schema_version": 2,
                "kind": "empirical_micro_lm_scaling_curve",
                "config": {
                    **asdict(config),
                    "dataset_dir": str(config.dataset_dir),
                    "output_dir": str(config.output_dir),
                    "points": [asdict(point) for point in config.points],
                    "seeds": list(config.seeds),
                },
                "points": rows,
                "fit": fit,
                "protocol": {
                    "dataset": "WikiText-2",
                    "fixed_axes": [
                        "dataset split", "BPE vocabulary", "architecture",
                        "optimizer", "batch size", "sequence length", "seed set",
                    ],
                    "compute_proxy": "6 * total trainable parameters (including embeddings) * tokens_seen approximation",
                    "claim_boundary": (
                        "local descriptive fit; not a Chinchilla compute-optimal frontier "
                        "and not evidence for large-model extrapolation"
                    ),
                },
                "runtime": runtime_summary(),
            }
            _write_json(config.output_dir / "result.json", payload)
            (config.output_dir / "report.md").write_text(
                render_scaling_report(payload), encoding="utf-8"
            )
        return payload, config.output_dir


def fit_scaling_curves(rows: list[dict]) -> dict:
    if len(rows) < 3:
        raise ValueError("at least three completed points are required for a fit")
    compute = np.asarray([row["estimated_training_flops"] for row in rows], dtype=float)
    losses = np.asarray([row["validation_lm_loss"] for row in rows], dtype=float)
    if np.any(compute <= 0) or np.any(losses <= 0):
        raise ValueError("compute and validation loss must be positive")
    if len(np.unique(compute)) < 3:
        raise ValueError("at least three distinct compute budgets are required")
    design = np.column_stack([np.ones(len(rows)), np.log(compute)])
    coefficients, *_ = np.linalg.lstsq(design, np.log(losses), rcond=None)
    predicted_log = design @ coefficients
    predicted = np.exp(predicted_log)
    compute_fit = _fit_metrics(losses, predicted, np.log(losses), predicted_log)
    compute_fit.update({
        "intercept": float(coefficients[0]),
        "log_compute_slope": float(coefficients[1]),
        "descriptive_alpha": float(-coefficients[1]),
    })
    for row, estimate in zip(rows, predicted):
        row["predicted_validation_lm_loss"] = float(estimate)
        row["relative_fit_residual"] = float(
            (row["validation_lm_loss"] - estimate) / row["validation_lm_loss"]
        )

    parameters = np.asarray([row["parameters"] for row in rows], dtype=float)
    data = np.asarray([row["available_train_tokens"] for row in rows], dtype=float)
    surface_design = np.column_stack([
        np.ones(len(rows)), np.log(parameters), np.log(data)
    ])
    surface = {"status": "not_identifiable"}
    if len(rows) >= 4 and np.linalg.matrix_rank(surface_design) == 3:
        surface_coefficients, *_ = np.linalg.lstsq(
            surface_design, np.log(losses), rcond=None
        )
        surface_log = surface_design @ surface_coefficients
        surface_prediction = np.exp(surface_log)
        surface = {
            "status": "descriptive_only",
            "intercept": float(surface_coefficients[0]),
            "log_parameter_slope": float(surface_coefficients[1]),
            "log_data_slope": float(surface_coefficients[2]),
            **_fit_metrics(losses, surface_prediction, np.log(losses), surface_log),
        }
    return {
        "compute_power_law": compute_fit,
        "parameter_data_surface": surface,
        "point_count": len(rows),
    }


def _fit_metrics(losses, predicted, log_losses, predicted_log) -> dict:
    residual = log_losses - predicted_log
    total = float(np.sum((log_losses - log_losses.mean()) ** 2))
    return {
        "log_rmse": float(np.sqrt(np.mean(residual ** 2))),
        "loss_rmse": float(np.sqrt(np.mean((losses - predicted) ** 2))),
        "r_squared": float(1.0 - np.sum(residual ** 2) / total) if total > 0 else 0.0,
        "max_absolute_relative_error": float(
            np.max(np.abs((losses - predicted) / losses))
        ),
    }


def render_scaling_report(payload: dict) -> str:
    fit = payload["fit"]["compute_power_law"]
    lines = [
        "# Micro-LLM 多预算 scaling-law 报告", "",
        "## 结论与边界", "",
        f"- 完成 `{len(payload['points'])}` 个独立 compute/data 预算点；所有点锁定相同架构、tokenizer、optimizer、batch、sequence length 与 seed 集合。",
        f"- 描述性 compute slope：`{fit['log_compute_slope']:.6f}`；log-space RMSE：`{fit['log_rmse']:.6f}`；R²：`{fit['r_squared']:.6f}`。",
        "- 这是 micro-LLM 局部经验拟合，不是 Chinchilla compute-optimal frontier，也不允许外推为大模型规律。", "",
        "## 预算点与拟合残差", "",
        "| 点 | Dim×Layers | 可用数据 tokens | Steps | 参数量 | Tokens seen | 估算 FLOPs | Validation loss | 预测 loss | 相对残差 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in payload["points"]:
        lines.append(
            f"| `{row['id']}` | {row['dimensions']}×{row['layers']} | "
            f"{row['available_train_tokens']} | {row['steps']} | {row['parameters']} | "
            f"{row['tokens_seen']} | {row['estimated_training_flops']:.3e} | "
            f"{row['validation_lm_loss']:.6f} | "
            f"{row['predicted_validation_lm_loss']:.6f} | "
            f"{row['relative_fit_residual']:+.2%} |"
        )
    surface = payload["fit"]["parameter_data_surface"]
    lines += ["", "## 参数量 × 数据量曲面", ""]
    if surface["status"] == "descriptive_only":
        lines += [
            f"独立参数/数据 log-linear 曲面可辨识；log-space RMSE `{surface['log_rmse']:.6f}`，"
            f"R² `{surface['r_squared']:.6f}`。该曲面只描述本次网格，不计算所谓最优参数/数据配比。"
        ]
    else:
        lines += [
            "当前预算网格不足以独立辨识参数量和数据量效应；报告保留该负结论，不强行拟合。"
        ]
    lines += [
        "", "## 复现", "", "```bash",
        "auto-research scaling-law --dataset-dir data --offline --device auto \\",
        f"  --points \"{DEFAULT_SCALING_POINTS}\" --seeds 42",
        "```", "",
        "正式研究应扩大正交模型/数据网格、训练至接近收敛并至少运行 3 seeds；本命令默认值只用于工程 smoke。", "",
    ]
    return "\n".join(lines)


def _config_fingerprint(config: ScalingLawConfig) -> str:
    payload = {
        **asdict(config),
        "dataset_dir": str(config.dataset_dir.resolve()),
        "output_dir": str(config.output_dir.resolve()),
        "points": [asdict(point) for point in config.points],
        "resume": False,
    }
    encoded = json.dumps(payload, sort_keys=True, default=str).encode()
    return hashlib.sha256(encoded).hexdigest()


def _write_json(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)
