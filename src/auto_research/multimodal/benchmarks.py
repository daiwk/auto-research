from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import random
import statistics
from typing import Any, Iterable


BENCHMARKS = (
    "cifar10-qa",
    "scienceqa",
    "pope",
    "coco-retrieval",
    "flickr30k-retrieval",
)


@dataclass(frozen=True)
class BenchmarkResult:
    benchmark: str
    evaluation_tier: str
    seeds: tuple[int, ...]
    seed_results: tuple[dict[str, float], ...]
    aggregate_metrics: dict[str, dict[str, float | int | None]]
    evaluated_examples: int
    prediction_source: str
    metadata: dict[str, Any]

    @property
    def formal_comparison(self) -> bool:
        return len(self.seeds) >= 3 and self.prediction_source != "random baseline"

    def to_dict(self) -> dict[str, Any]:
        created_at = datetime.now(timezone.utc).isoformat()
        formal = self.formal_comparison
        if self.prediction_source == "random baseline":
            claim_policy = "random pipeline baseline; not a model capability result"
        elif formal:
            claim_policy = "multi-seed benchmark result"
        else:
            claim_policy = "fewer than three seeds; treat as a smoke result"
        return {
            "schema_version": 2,
            "manifest_ref": f"multimodal-models:{self.benchmark}",
            "benchmark": self.benchmark,
            "evaluation_tier": self.evaluation_tier,
            "seeds": list(self.seeds),
            "evaluated_examples": self.evaluated_examples,
            "prediction_source": self.prediction_source,
            "metadata": self.metadata,
            "seed_results": list(self.seed_results),
            "aggregate_metrics": self.aggregate_metrics,
            "formal_comparison": formal,
            "claim_policy": claim_policy,
            "evaluation_protocol": {
                "tier": self.evaluation_tier,
                "seeds": list(self.seeds),
                "formal_comparison": formal,
                "claim_policy": claim_policy,
            },
            "provenance": {"created_at": created_at},
        }


def run_public_benchmark(
    benchmark: str,
    annotations: Path,
    seeds: tuple[int, ...],
    predictions: str | None = None,
    baseline: str | None = None,
    split: str = "test",
) -> BenchmarkResult:
    """Score public benchmark predictions without coupling to a model framework.

    ``predictions`` may contain ``{seed}``; this makes independently generated
    model outputs auditable. The random baseline is deliberately explicit and
    can never be mistaken for a model result in the generated report.
    """
    if benchmark not in BENCHMARKS or benchmark == "cifar10-qa":
        raise ValueError(f"unknown multimodal benchmark: {benchmark}")
    if bool(predictions) == bool(baseline):
        raise ValueError("provide exactly one of predictions or baseline")
    if baseline and baseline != "random":
        raise ValueError("only the explicit random baseline is supported")
    if not seeds:
        raise ValueError("at least one seed is required")
    if predictions and len(seeds) > 1 and "{seed}" not in predictions:
        raise ValueError(
            "multi-seed model evaluation requires {seed} in --predictions; "
            "reusing one prediction file is not an independent comparison"
        )

    annotations_payload = _read_payload(annotations)
    rows = []
    evaluated_examples = 0
    for seed in seeds:
        if predictions:
            path = Path(predictions.format(seed=seed))
            prediction_payload = _read_payload(path)
        else:
            prediction_payload = _random_predictions(
                benchmark, annotations_payload, seed, split
            )
        metrics, count = score_benchmark(
            benchmark, annotations_payload, prediction_payload, split=split
        )
        rows.append({"seed": seed, **metrics})
        evaluated_examples = count
    return BenchmarkResult(
        benchmark=benchmark,
        evaluation_tier="l2_public_benchmark",
        seeds=seeds,
        seed_results=tuple(rows),
        aggregate_metrics=_aggregate(rows),
        evaluated_examples=evaluated_examples,
        prediction_source=(predictions or "random baseline"),
        metadata={
            "annotations": str(annotations.resolve()),
            "annotations_sha256": _path_sha256(annotations),
            "split": split,
        },
    )


def run_cifar10_benchmark(
    dataset_dir: Path,
    seeds: tuple[int, ...],
    *,
    architecture: str = "micro_vlm_query",
    steps: int = 300,
    maximum_examples: int = 5000,
    dimensions: int = 192,
    batch_size: int = 32,
    learning_rate: float = 3e-4,
    objective: str = "cross_entropy",
    allow_network: bool = True,
) -> BenchmarkResult:
    """Train one fixed micro-VLM recipe and report isolated validation/test metrics."""
    from ..evolution.models import Genome
    from ..runtime import runtime_summary
    from .data import CIFAR10_MD5
    from .evaluator import MicroVLMEvaluator
    import torch

    if len(seeds) < 1:
        raise ValueError("at least one seed is required")
    evaluator = MicroVLMEvaluator(
        dataset_dir, "cifar10-qa", steps, seeds,
        allow_network=allow_network, maximum_examples=maximum_examples,
    )
    genome = Genome(
        architecture=architecture,
        dimensions=dimensions,
        batch_size=batch_size,
        learning_rate=learning_rate,
        multimodal_objective=objective,
    )
    rows = []
    training_metadata = None
    for seed in seeds:
        model, training = evaluator._train(genome, seed)
        training_metadata = training_metadata or training
        validation = evaluator._metrics(model, evaluator.data.validation)
        test = evaluator._metrics(model, evaluator.data.test)
        rows.append({
            "seed": seed,
            **{f"validation_{key}": value for key, value in validation.items()},
            **{f"test_{key}": value for key, value in test.items()},
            "parameters": float(training["parameters"]),
        })
    return BenchmarkResult(
        benchmark="cifar10-qa",
        evaluation_tier="l1_public_images",
        seeds=seeds,
        seed_results=tuple(rows),
        aggregate_metrics=_aggregate(rows),
        evaluated_examples=(
            len(evaluator.data.validation.answers) + len(evaluator.data.test.answers)
        ),
        prediction_source=(
            f"{architecture}; objective={objective}; steps={steps}; "
            f"train_examples={len(evaluator.data.train.answers)}"
        ),
        metadata={
            "dataset_source": evaluator.data.source,
            "dataset_checksum_md5": CIFAR10_MD5,
            "dataset_license": evaluator.data.license,
            "train_examples": len(evaluator.data.train.answers),
            "validation_examples": len(evaluator.data.validation.answers),
            "test_examples": len(evaluator.data.test.answers),
            "architecture": architecture,
            "objective": objective,
            "steps": steps,
            "dimensions": dimensions,
            "batch_size": batch_size,
            "learning_rate": learning_rate,
            "device": training_metadata["device"],
            "runtime": runtime_summary(torch),
            "architecture_stats": training_metadata["architecture_stats"],
        },
    )


def score_benchmark(
    benchmark: str,
    annotations: Any,
    predictions: Any,
    split: str = "test",
) -> tuple[dict[str, float], int]:
    if benchmark == "scienceqa":
        return _score_scienceqa(annotations, predictions, split)
    if benchmark == "pope":
        return _score_pope(annotations, predictions)
    if benchmark in {"coco-retrieval", "flickr30k-retrieval"}:
        return _score_retrieval(annotations, predictions, split)
    raise ValueError(f"unknown multimodal benchmark: {benchmark}")


def write_benchmark_report(result: BenchmarkResult, output_dir: Path) -> Path:
    run_dir = Path(output_dir) / (
        f"{result.benchmark}-{datetime.now().strftime('%Y%m%d-%H%M%S-%f')}"
    )
    run_dir.mkdir(parents=True, exist_ok=False)
    payload = result.to_dict()
    payload["provenance"]["artifact_path"] = str(run_dir / "metrics.json")
    (run_dir / "metrics.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    metric_rows = "\n".join(
        f"| `{name}` | {values['mean']:.6f} | {values['std']:.6f} | "
        f"{_format_ci(values['ci95'])} | {values['n']} |"
        for name, values in result.aggregate_metrics.items()
    )
    boundary = (
        "本报告来自固定训练配方；test 仅用于最终隔离报告，不能反向选择结构或超参数。"
        if result.benchmark == "cifar10-qa" else
        "本报告只评价传入预测文件。若预测来源为 `random baseline`，结果仅用于验证数据和"
        "指标管线，不代表任何 VLM 能力。"
    )
    report = f"""# {result.benchmark} 多模态评测

- 评测层级：`{result.evaluation_tier}`
- seed：{', '.join(str(seed) for seed in result.seeds)}
- 样本数：{result.evaluated_examples}
- 预测来源：`{result.prediction_source}`
- 正式多 seed：{'是' if result.formal_comparison else '否'}

| 指标 | mean | std | 95% CI 半径 | n |
|---|---:|---:|---:|---:|
{metric_rows}

## 运行元数据

```json
{json.dumps(result.metadata, ensure_ascii=False, indent=2)}
```

## 结论边界

{boundary}少于三个 seed 的结果不得声明为稳定提升。
"""
    (run_dir / "report.md").write_text(report, encoding="utf-8")
    return run_dir


def _score_scienceqa(
    annotations: Any, predictions: Any, split: str
) -> tuple[dict[str, float], int]:
    problems = _scienceqa_problems(annotations, split)
    predicted = _prediction_map(predictions)
    correct = 0
    image_correct = image_count = text_correct = text_count = 0
    for identifier, problem in problems.items():
        if identifier not in predicted:
            raise ValueError(f"missing ScienceQA prediction for {identifier}")
        choices = problem.get("choices", [])
        answer = int(problem["answer"])
        guess = _choice_index(predicted[identifier], choices)
        hit = int(guess == answer)
        correct += hit
        if problem.get("image"):
            image_correct += hit
            image_count += 1
        else:
            text_correct += hit
            text_count += 1
    count = len(problems)
    if not count:
        raise ValueError(f"ScienceQA contains no records for split {split!r}")
    return {
        "accuracy": correct / count,
        "image_accuracy": image_correct / image_count if image_count else 0.0,
        "text_accuracy": text_correct / text_count if text_count else 0.0,
        "coverage": len(set(problems) & set(predicted)) / count,
    }, count


def _score_pope(annotations: Any, predictions: Any) -> tuple[dict[str, float], int]:
    records = _records(annotations)
    predicted = _prediction_map(predictions)
    tp = fp = tn = fn = 0
    for row in records:
        identifier = str(row.get("question_id", row.get("id")))
        if identifier not in predicted:
            raise ValueError(f"missing POPE prediction for {identifier}")
        truth = _yes_no(row["answer"])
        guess = _yes_no(predicted[identifier])
        if truth and guess:
            tp += 1
        elif not truth and guess:
            fp += 1
        elif not truth and not guess:
            tn += 1
        else:
            fn += 1
    count = len(records)
    if not count:
        raise ValueError("POPE annotation file is empty")
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return {
        "accuracy": (tp + tn) / count,
        "precision": precision,
        "recall": recall,
        "f1": 2 * precision * recall / (precision + recall) if precision + recall else 0.0,
        "yes_ratio": (tp + fp) / count,
    }, count


def _score_retrieval(
    annotations: Any, predictions: Any, split: str
) -> tuple[dict[str, float], int]:
    images = annotations.get("images", annotations) if isinstance(annotations, dict) else annotations
    images = [row for row in images if row.get("split", split) == split]
    image_to_text: dict[str, set[str]] = {}
    text_to_image: dict[str, str] = {}
    for image_position, row in enumerate(images):
        image_id = str(row.get("cocoid", row.get("imgid", row.get("image_id", image_position))))
        texts = set()
        for sentence_position, sentence in enumerate(row.get("sentences", [])):
            text_id = str(sentence.get("sentid", sentence.get("id", f"{image_id}:{sentence_position}")))
            texts.add(text_id)
            text_to_image[text_id] = image_id
        image_to_text[image_id] = texts
    if not image_to_text or not text_to_image:
        raise ValueError(f"retrieval annotations contain no image-caption pairs for split {split!r}")
    prediction_rows = _records(predictions)
    i2t = {
        str(row["image_id"]): [str(value) for value in row["ranked_text_ids"]]
        for row in prediction_rows if "ranked_text_ids" in row
    }
    t2i = {
        str(row["text_id"]): [str(value) for value in row["ranked_image_ids"]]
        for row in prediction_rows if "ranked_image_ids" in row
    }
    if set(i2t) != set(image_to_text):
        missing = sorted(set(image_to_text) - set(i2t))[:3]
        raise ValueError(f"retrieval predictions miss image queries: {missing}")
    if set(t2i) != set(text_to_image):
        missing = sorted(set(text_to_image) - set(t2i))[:3]
        raise ValueError(f"retrieval predictions miss text queries: {missing}")
    image_ranks = [
        _first_relevant_rank(i2t[query], relevant)
        for query, relevant in image_to_text.items()
    ]
    text_ranks = [
        _first_relevant_rank(t2i[query], {relevant})
        for query, relevant in text_to_image.items()
    ]
    metrics = {}
    for name, ranks in (("i2t", image_ranks), ("t2i", text_ranks)):
        for k in (1, 5, 10):
            metrics[f"{name}_recall_at_{k}"] = sum(rank <= k for rank in ranks) / len(ranks)
        metrics[f"{name}_median_rank"] = float(statistics.median(ranks))
    metrics["mean_recall"] = statistics.fmean(
        metrics[key] for key in metrics if "recall_at" in key
    )
    return metrics, len(image_ranks) + len(text_ranks)


def _scienceqa_problems(payload: Any, split: str) -> dict[str, dict[str, Any]]:
    if isinstance(payload, dict) and "problems" in payload:
        split_ids = set(str(value) for value in payload.get("splits", {}).get(split, []))
        source = payload["problems"]
    else:
        split_ids = set()
        source = payload
    if isinstance(source, dict):
        return {
            str(key): value for key, value in source.items()
            if (not split_ids and value.get("split", split) == split) or str(key) in split_ids
        }
    return {
        str(row.get("id", position)): row for position, row in enumerate(source)
        if row.get("split", split) == split
    }


def _random_predictions(benchmark: str, annotations: Any, seed: int, split: str) -> list[dict[str, Any]]:
    rng = random.Random(seed)
    if benchmark == "scienceqa":
        return [
            {"id": identifier, "prediction": rng.randrange(len(row["choices"]))}
            for identifier, row in _scienceqa_problems(annotations, split).items()
        ]
    if benchmark == "pope":
        return [
            {"id": str(row.get("question_id", row.get("id"))), "prediction": rng.choice(("yes", "no"))}
            for row in _records(annotations)
        ]
    images = annotations.get("images", annotations) if isinstance(annotations, dict) else annotations
    images = [row for row in images if row.get("split", split) == split]
    image_ids, text_ids = [], []
    for image_position, row in enumerate(images):
        image_id = str(row.get("cocoid", row.get("imgid", row.get("image_id", image_position))))
        image_ids.append(image_id)
        for sentence_position, sentence in enumerate(row.get("sentences", [])):
            text_ids.append(str(sentence.get("sentid", sentence.get("id", f"{image_id}:{sentence_position}"))))
    rows = []
    for image_id in image_ids:
        ranking = text_ids.copy()
        rng.shuffle(ranking)
        rows.append({"image_id": image_id, "ranked_text_ids": ranking})
    for text_id in text_ids:
        ranking = image_ids.copy()
        rng.shuffle(ranking)
        rows.append({"text_id": text_id, "ranked_image_ids": ranking})
    return rows


def _prediction_map(payload: Any) -> dict[str, Any]:
    return {
        str(row.get("id", row.get("question_id"))): row.get("prediction", row.get("answer"))
        for row in _records(payload)
    }


def _choice_index(value: Any, choices: list[str]) -> int:
    if isinstance(value, int):
        return value
    text = str(value).strip()
    if text.isdigit():
        return int(text)
    if len(text) == 1 and text.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        return ord(text.upper()) - ord("A")
    normalized = text.casefold()
    for index, choice in enumerate(choices):
        if normalized == str(choice).strip().casefold():
            return index
    return -1


def _yes_no(value: Any) -> bool:
    text = str(value).strip().casefold().rstrip(".!")
    if text.startswith(("yes", "是")):
        return True
    if text.startswith(("no", "否", "不是")):
        return False
    raise ValueError(f"POPE answer must be yes/no, got {value!r}")


def _first_relevant_rank(ranking: Iterable[str], relevant: set[str]) -> int:
    for index, candidate in enumerate(ranking, start=1):
        if candidate in relevant:
            return index
    return 1_000_000


def _read_payload(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(path)
    if path.is_dir():
        problems = path / "problems.json"
        splits = path / "pid_splits.json"
        if problems.exists() and splits.exists():
            return {
                "problems": json.loads(problems.read_text(encoding="utf-8")),
                "splits": json.loads(splits.read_text(encoding="utf-8")),
            }
        raise ValueError(
            f"unsupported benchmark directory {path}; expected problems.json and pid_splits.json"
        )
    if path.suffix == ".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return json.loads(path.read_text(encoding="utf-8"))


def _records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("predictions", "annotations", "records"):
            if key in payload:
                return payload[key]
    raise ValueError("expected a JSON array/JSONL or an object with a records list")


def _aggregate(rows: list[dict[str, float]]) -> dict[str, dict[str, float | int | None]]:
    aggregate = {}
    for key in rows[0]:
        if key == "seed":
            continue
        values = [row[key] for row in rows]
        mean = statistics.fmean(values)
        std = statistics.stdev(values) if len(values) > 1 else 0.0
        aggregate[key] = {
            "mean": mean,
            "std": std,
            "ci95": 1.96 * std / math.sqrt(len(values)) if len(values) > 1 else None,
            "n": len(values),
        }
    return aggregate


def _format_ci(value: float | None) -> str:
    return "—" if value is None else f"{value:.6f}"


def _path_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    paths = [path] if path.is_file() else sorted(item for item in path.rglob("*") if item.is_file())
    for item in paths:
        if path.is_dir():
            digest.update(str(item.relative_to(path)).encode())
        with item.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()
