from __future__ import annotations

import json
import inspect
import re
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from typing import Any

from .base import EvaluationTier, ReproductionAdapter, ReproductionFidelity


ROOT = Path(__file__).resolve().parents[3]
METRIC_WORDS = (
    "auc", "ndcg", "hit", "recall", "precision", "map", "mrr", "loss",
    "accuracy", "success", "perplexity", "revenue", "gmv", "ctr", "cvr",
    "qps", "latency", "memory", "flops", "reward", "cost",
)


def normalize_adapter_protocol(adapter: ReproductionAdapter) -> ReproductionAdapter:
    inferred = infer_protocol(adapter)
    return replace(
        adapter,
        evaluation_tier=(
            adapter.evaluation_tier
            if adapter.evaluation_tier is not EvaluationTier.PUBLIC_DATASET
            or adapter.fidelity is ReproductionFidelity.CORE_MECHANISM
            else inferred["evaluation_tier"]
        ),
        datasets=adapter.datasets or inferred["datasets"],
        baseline=adapter.baseline or inferred["baseline"],
        metrics=adapter.metrics or inferred["metrics"],
        default_seeds=(
            adapter.default_seeds
            if adapter.default_seeds != (42,)
            else inferred["default_seeds"]
        ),
        budget=(
            adapter.budget if adapter.budget != "paper-specific" else inferred["budget"]
        ),
        device_capabilities=(
            adapter.device_capabilities
            if not adapter.infer_device_capabilities
            or adapter.device_capabilities != ("cpu",)
            else inferred["device_capabilities"]
        ),
    )


@lru_cache(maxsize=None)
def infer_protocol(adapter: ReproductionAdapter) -> dict[str, Any]:
    payloads = _metric_payloads(adapter)
    readme = _readme(adapter)
    datasets = tuple(dict.fromkeys(
        value for payload in payloads
        if (value := _dataset(payload))
    ))
    seeds = sorted({seed for payload in payloads for seed in _seeds(payload)})
    metrics = sorted({
        key for payload in payloads for key in _metric_keys(payload)
    })
    baselines = [value for payload in payloads if (value := _baseline(payload))]
    if readme and (documented := _readme_baseline(readme)):
        baselines.insert(0, documented)
    steps = [value for payload in payloads if (value := _steps(payload)) is not None]
    run_budget = _run_budget(adapter)
    tier = {
        ReproductionFidelity.FULL_PIPELINE: EvaluationTier.PAPER_PIPELINE,
        ReproductionFidelity.CORE_MECHANISM: EvaluationTier.PUBLIC_DATASET,
        ReproductionFidelity.CONCEPT_DEMO: EvaluationTier.MECHANISM,
    }[adapter.fidelity]
    return {
        "datasets": datasets or ("public dataset documented in adapter report",),
        "baseline": (
            baselines[0]
            if baselines and baselines[0] != "baseline"
            else f"matched control without the {adapter.key} mechanism"
        ),
        "metrics": tuple(metrics) or (f"{adapter.key}.reported_objective",),
        "default_seeds": tuple(seeds) or (42,),
        "budget": (
            f"steps={max(steps)}" if steps else run_budget or "adapter-defined fixed budget"
        ),
        "device_capabilities": ("cpu", "mps", "cuda"),
        "evaluation_tier": tier,
    }


def _metric_payloads(adapter: ReproductionAdapter) -> list[dict[str, Any]]:
    docs = ROOT / "docs" / "reproductions"
    paths = sorted(docs.glob(f"{adapter.paper.arxiv_id}-*/metrics/*.json"))
    payloads = []
    for path in paths:
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(payload, dict):
            payload = dict(payload)
            payload["__artifact_stem"] = path.stem
            payloads.append(payload)
    return payloads


def _readme(adapter: ReproductionAdapter) -> str:
    paths = sorted((ROOT / "docs" / "reproductions").glob(
        f"{adapter.paper.arxiv_id}-*/README.md"
    ))
    if not paths:
        return ""
    try:
        return paths[0].read_text(encoding="utf-8")
    except OSError:
        return ""


def _readme_baseline(readme: str) -> str | None:
    for line in readme.splitlines():
        if "本地对照口径" not in line and not re.match(r"^[-*]\s*(?:公平)?基线[：:]", line):
            continue
        match = re.search(r"(?:基线(?:是|为)|基线[：:])\s*([^；;。]+)", line)
        if match:
            value = re.sub(r"[`*_]", "", match.group(1)).strip()
            return value[:240]
    return None


def _run_budget(adapter: ReproductionAdapter) -> str | None:
    try:
        signature = inspect.signature(adapter.run)
    except (TypeError, ValueError):
        return None
    values = []
    for name in ("steps", "epochs", "iterations", "rounds"):
        parameter = signature.parameters.get(name)
        if parameter and isinstance(parameter.default, int):
            values.append(f"{name}={parameter.default}")
    return ", ".join(values) or None


def _dataset(payload: dict[str, Any]) -> str | None:
    value = payload.get("dataset")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return str(value.get("name") or value.get("dataset") or "") or None
    stem = payload.get("__artifact_stem")
    if isinstance(stem, str):
        value = re.sub(r"-seeds?\d+(?:-\d+)?$", "", stem)
        return value.replace("-", " ")
    return None


def _seeds(payload: dict[str, Any]) -> tuple[int, ...]:
    values = payload.get("seeds")
    if values is None:
        values = payload.get("seed")
    if values is None and isinstance(payload.get("setup"), dict):
        values = payload["setup"].get("seeds", payload["setup"].get("seed"))
    if values is None and isinstance(payload.get("protocol"), dict):
        values = payload["protocol"].get("seeds", payload["protocol"].get("seed"))
    if values is None and isinstance(payload.get("__artifact_stem"), str):
        match = re.search(r"-seeds?(\d+)(?:-(\d+))?$", payload["__artifact_stem"])
        if match:
            start, end = int(match.group(1)), int(match.group(2) or match.group(1))
            values = list(range(start, end + 1))
    if isinstance(values, int):
        return (values,)
    if isinstance(values, list):
        return tuple(int(value) for value in values if isinstance(value, int))
    return ()


def _baseline(payload: dict[str, Any]) -> str | None:
    value = payload.get("baseline")
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("name", "method", "model"):
            if isinstance(value.get(key), str):
                return value[key]
        return "baseline"
    flattened = _flatten(payload)
    for marker, label in (
        ("frozen", "frozen representation baseline"),
        ("sft", "SFT baseline"),
        ("teacher", "teacher baseline"),
        ("din", "DIN baseline"),
        ("sasrec", "SASRec baseline"),
        ("full_sequence", "full-sequence baseline"),
        ("mean_pool", "mean-pooling baseline"),
    ):
        if any(marker in key.lower() for key in flattened):
            return label
    results = payload.get("results")
    if isinstance(results, dict) and results:
        return str(next(iter(results))).replace("_", " ")
    return None


def _steps(payload: dict[str, Any]) -> int | None:
    candidates = []
    for key, value in _flatten(payload).items():
        if "step" in key.lower() and isinstance(value, int) and value > 0:
            candidates.append(value)
    return max(candidates, default=None)


def _metric_keys(payload: dict[str, Any]) -> set[str]:
    result = set()
    for key, value in _flatten(payload).items():
        if isinstance(value, (int, float)) and any(word in key.lower() for word in METRIC_WORDS):
            result.add(key.removeprefix("metrics."))
        elif (
            isinstance(value, (int, float))
            and key.split(".", 1)[0] in {"baseline", "method", "proposed", "relative"}
            and not key.lower().endswith(("step", "steps", "seed"))
        ):
            result.add(key)
    return result


def _flatten(payload: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    result = {}
    for key, value in payload.items():
        name = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            result.update(_flatten(value, name))
        else:
            result[name] = value
    return result
