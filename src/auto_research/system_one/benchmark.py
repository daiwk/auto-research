"""Banking77 evaluation for local and online System One decision providers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import csv
import json
import math
import time
from pathlib import Path
from urllib import request

import numpy as np

from .contracts import ChoiceQuestion, SystemOneRequest
from .local import DecisionTrainingExample, LocalDecisionModel, LocalSystemOneProvider
from .nanojev import NANOJEV_REVISION, NanoJevProvider
from .providers import TypeSafeHTTPProvider


BASE_URL = (
    "https://raw.githubusercontent.com/PolyAI-LDN/"
    "task-specific-datasets/master/banking_data"
)


@dataclass(frozen=True)
class SystemOneBenchmarkConfig:
    dataset_dir: Path = Path("data/system-one")
    output_dir: Path = Path("runs/system-one")
    backend: str = "local"
    architecture: str = "rival_attention"
    objective: str = "hybrid"
    dimensions: int = 256
    steps: int = 800
    learning_rate: float = 0.15
    seeds: tuple[int, ...] = (42, 43, 44)
    maximum_train_examples: int | None = 4000
    maximum_eval_examples: int | None = 1000
    allow_network: bool = True
    confidence_threshold: float = 0.8
    checkpoint_dir: Path | None = None
    checkpoint_revision: str = NANOJEV_REVISION
    device: str = "cuda:0"
    precision: str = "bf16"
    temperature: float = 1.0
    batch_questions: int = 0
    disable_native_triton: bool = False

    def validate(self) -> None:
        if self.backend not in {"local", "typesafe", "nanojev"}:
            raise ValueError("backend must be local, typesafe or nanojev")
        if not self.seeds:
            raise ValueError("at least one seed is required")
        if min(self.dimensions, self.steps) < 1 or self.learning_rate <= 0:
            raise ValueError("dimensions, steps and learning_rate must be positive")
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be in [0, 1]")
        if self.precision not in {"fp32", "bf16"}:
            raise ValueError("precision must be fp32 or bf16")
        if not math.isfinite(self.temperature) or self.temperature <= 0.0:
            raise ValueError("temperature must be a finite positive number")
        if self.batch_questions < 0:
            raise ValueError("batch_questions must be non-negative")


def run_system_one_benchmark(
    config: SystemOneBenchmarkConfig,
) -> tuple[dict, Path]:
    config.validate()
    train, validation, test = load_banking77(
        config.dataset_dir,
        allow_network=config.allow_network,
        maximum_train_examples=config.maximum_train_examples,
        maximum_eval_examples=config.maximum_eval_examples,
    )
    run_dir = config.output_dir / time.strftime("%Y%m%d-%H%M%S")
    runs = []
    for seed in config.seeds:
        started = time.monotonic()
        if config.backend == "local":
            model = LocalDecisionModel(
                config.dimensions,
                architecture=config.architecture,
                objective=config.objective,
                seed=seed,
            )
            training = model.fit(
                train,
                steps=config.steps,
                learning_rate=config.learning_rate,
                seed=seed,
            )
            temperature = model.calibrate_temperature(validation)
            provider = LocalSystemOneProvider(model)
        elif config.backend == "typesafe":
            provider = TypeSafeHTTPProvider()
            training = {"initial_loss": None, "final_loss": None, "steps": 0}
            temperature = None
        else:
            provider = NanoJevProvider.from_checkpoint(
                config.checkpoint_dir,
                allow_download=config.allow_network,
                revision=config.checkpoint_revision,
                device=config.device,
                precision=config.precision,
                temperature=config.temperature,
                batch_questions=config.batch_questions,
                disable_native_triton=config.disable_native_triton,
            )
            training = {
                "initial_loss": None,
                "final_loss": None,
                "steps": 0,
                "external_checkpoint": True,
            }
            temperature = config.temperature
        validation_metrics = evaluate_examples(
            provider, validation, config.confidence_threshold
        )
        test_metrics = evaluate_examples(provider, test, config.confidence_threshold)
        runs.append(
            {
                "seed": seed,
                "training": training,
                "temperature": temperature,
                "validation": validation_metrics,
                "test": test_metrics,
                "duration_seconds": time.monotonic() - started,
            }
        )
        if config.backend in {"typesafe", "nanojev"}:
            # Both are fixed checkpoints; repeating the identical model with a
            # nominal seed would misrepresent one run as multi-seed evidence.
            break
    method = (
        f"system-one:{config.architecture}:{config.objective}"
        if config.backend == "local" else f"system-one:{config.backend}"
    )
    result = {
        "schema_version": 2,
        "domain": "system-one",
        "method": method,
        "dataset": "Banking77",
        "config": {
            **asdict(config),
            "dataset_dir": str(config.dataset_dir),
            "output_dir": str(config.output_dir),
            "checkpoint_dir": (
                str(config.checkpoint_dir) if config.checkpoint_dir is not None else None
            ),
            "seeds": list(config.seeds),
        },
        "dataset_summary": {
            "source": "PolyAI Banking77",
            "license": "CC BY 4.0",
            "train_examples": len(train),
            "validation_examples": len(validation),
            "test_examples": len(test),
            "validation_selected_temperature": config.backend == "local",
            "test_isolation": True,
        },
        "runs": runs,
        "aggregate_metrics": _aggregate_runs(runs),
        "claim_policy": (
            "public-dataset checkpoint comparison; no claim about TypeSafe's unpublished "
            "architecture, NanoJev's out-of-domain product quality, or vendor-reported performance"
        ),
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    write_system_one_report(result, run_dir / "report.md")
    return result, run_dir


def load_banking77(
    directory: Path,
    *,
    allow_network: bool,
    maximum_train_examples: int | None = None,
    maximum_eval_examples: int | None = None,
) -> tuple[
    tuple[DecisionTrainingExample, ...],
    tuple[DecisionTrainingExample, ...],
    tuple[DecisionTrainingExample, ...],
]:
    directory.mkdir(parents=True, exist_ok=True)
    train_path, test_path = directory / "train.csv", directory / "test.csv"
    for path in (train_path, test_path):
        if path.exists():
            continue
        if not allow_network:
            raise FileNotFoundError(
                f"Banking77 file missing: {path}; rerun without --offline"
            )
        with request.urlopen(f"{BASE_URL}/{path.name}", timeout=60) as response:
            path.write_bytes(response.read())
    raw_train = _read_banking77(train_path)
    raw_test = _read_banking77(test_path)
    labels = tuple(sorted({label for _, label in (*raw_train, *raw_test)}))
    criteria = {label: label.replace("_", " ") for label in labels}
    instruction = "Which banking intent best describes this customer request?"

    def convert(rows):
        return tuple(
            DecisionTrainingExample(text, instruction, criteria, label)
            for text, label in rows
        )

    train_rows = _balanced_limit(raw_train, maximum_train_examples)
    validation_rows = _balanced_limit(raw_test[::2], maximum_eval_examples)
    test_rows = _balanced_limit(raw_test[1::2], maximum_eval_examples)
    return convert(train_rows), convert(validation_rows), convert(test_rows)


def evaluate_examples(provider, examples, confidence_threshold: float) -> dict[str, float]:
    confidences, correctness, nlls, briers, latencies = [], [], [], [], []
    sum_errors = []
    for row in examples:
        started = time.perf_counter()
        response = provider.decide(
            SystemOneRequest(
                row.state,
                {
                    "intent": ChoiceQuestion(row.instructions, row.criteria),
                },
            )
        )
        latencies.append((time.perf_counter() - started) * 1000.0)
        answer = response.answers["intent"]
        probability = max(float(answer.probabilities[row.target]), 1e-12)
        predicted = str(answer.value)
        correct = float(predicted == row.target)
        confidences.append(float(answer.confidence))
        correctness.append(correct)
        nlls.append(-math.log(probability))
        briers.append(
            sum(
                (float(value) - float(label == row.target)) ** 2
                for label, value in answer.probabilities.items()
            )
        )
        sum_errors.append(abs(sum(answer.probabilities.values()) - 1.0))
    confidence = np.asarray(confidences)
    correct = np.asarray(correctness)
    accepted = confidence >= confidence_threshold
    return {
        "accuracy": float(correct.mean()),
        "nll": float(np.mean(nlls)),
        "brier": float(np.mean(briers)),
        "ece": expected_calibration_error(confidence, correct),
        "coverage": float(accepted.mean()),
        "selective_accuracy": float(correct[accepted].mean()) if accepted.any() else 0.0,
        "latency_ms_mean": float(np.mean(latencies)),
        "schema_validity": float(max(sum_errors, default=1.0) <= 1e-5),
        "probability_sum_error_max": float(max(sum_errors, default=0.0)),
        "evaluated_examples": float(len(examples)),
    }


def expected_calibration_error(
    confidence: np.ndarray, correctness: np.ndarray, bins: int = 10
) -> float:
    if confidence.shape != correctness.shape or not len(confidence):
        raise ValueError("confidence and correctness must be non-empty and aligned")
    error = 0.0
    edges = np.linspace(0.0, 1.0, bins + 1)
    for index in range(bins):
        lower, upper = edges[index], edges[index + 1]
        mask = (confidence >= lower) & (
            confidence <= upper if index == bins - 1 else confidence < upper
        )
        if mask.any():
            error += float(mask.mean()) * abs(
                float(correctness[mask].mean()) - float(confidence[mask].mean())
            )
    return error


def write_system_one_report(result: dict, path: Path) -> Path:
    aggregate = result["aggregate_metrics"]
    summary = result["dataset_summary"]
    lines = [
        "# System One / Jev-compatible benchmark",
        "",
        "> 本报告比较公开契约下的 typed decision 实现；不推断 Jev 的未公开架构。",
        "",
        "## 协议",
        "",
        f"- 数据：Banking77 train `{summary['train_examples']}` / validation "
        f"`{summary['validation_examples']}` / test `{summary['test_examples']}`；",
        "- validation 只用于温度校准，test 仅在选择完成后报告；",
        "- 指标：accuracy、NLL、Brier、ECE、coverage、selective accuracy、schema validity。",
        "",
        "## Test 汇总",
        "",
        "| 指标 | 均值 | 标准差 |",
        "|---|---:|---:|",
    ]
    for name in (
        "accuracy", "nll", "brier", "ece", "coverage", "selective_accuracy",
        "latency_ms_mean", "schema_validity",
    ):
        lines.append(
            f"| {name} | {aggregate.get(name + '_mean', 0.0):.6f} | "
            f"{aggregate.get(name + '_std', 0.0):.6f} |"
        )
    lines.extend([
        "",
        "## 边界",
        "",
        result["claim_policy"],
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _read_banking77(path: Path) -> list[tuple[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    if rows and [value.lower() for value in rows[0][:2]] == ["text", "category"]:
        rows = rows[1:]
    parsed = [(row[0], row[1]) for row in rows if len(row) >= 2 and row[0] and row[1]]
    if not parsed:
        raise ValueError(f"Banking77 file contains no examples: {path}")
    return parsed


def _balanced_limit(
    rows: list[tuple[str, str]], maximum: int | None
) -> list[tuple[str, str]]:
    if maximum is None or len(rows) <= maximum:
        return rows
    groups: dict[str, list[tuple[str, str]]] = {}
    for row in rows:
        groups.setdefault(row[1], []).append(row)
    selected: list[tuple[str, str]] = []
    cursor = 0
    labels = sorted(groups)
    while len(selected) < maximum:
        added = False
        for label in labels:
            if cursor < len(groups[label]) and len(selected) < maximum:
                selected.append(groups[label][cursor])
                added = True
        if not added:
            break
        cursor += 1
    return selected


def _aggregate_runs(runs: list[dict]) -> dict[str, float]:
    keys = sorted(runs[0]["test"]) if runs else []
    result: dict[str, float] = {}
    for key in keys:
        values = np.asarray([row["test"][key] for row in runs], dtype=np.float64)
        result[f"{key}_mean"] = float(values.mean())
        result[f"{key}_std"] = float(values.std())
    return result
