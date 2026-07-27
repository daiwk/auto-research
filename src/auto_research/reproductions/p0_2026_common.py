from __future__ import annotations

from pathlib import Path

import numpy as np

from .industrial_2026 import (
    base_scores,
    evaluate,
    load_industrial_data,
    summary_result,
    tune_blend,
)


def load_data(dataset_dir: Path):
    return load_industrial_data(dataset_dir, maximum_users=260, maximum_items=420)


def normalized(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64)
    scale = np.max(np.abs(values))
    return values / max(float(scale), 1e-12)


def run_scoring_reproduction(
    *,
    key,
    paper,
    dataset_dir,
    build_method,
    baseline_name,
    method_name,
    paper_results,
    scope,
):
    data = load_data(dataset_dir)
    raw_scorer, stages = build_method(data)
    baseline_scorer = lambda history: base_scores(data, history)
    baseline = evaluate(data, baseline_scorer)
    alpha, scorer, validation = tune_blend(data, baseline_scorer, raw_scorer)
    proposed = evaluate(data, scorer)
    stages = {**stages, "validation_selected_blend": alpha, "validation": validation}
    return summary_result(
        key=key,
        paper=paper,
        data=data,
        baseline_name=baseline_name,
        method_name=method_name,
        baseline=baseline,
        proposed=proposed,
        stages=stages,
        paper_results=paper_results,
        scope=scope,
    )
