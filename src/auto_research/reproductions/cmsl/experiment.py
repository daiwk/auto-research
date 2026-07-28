from pathlib import Path
from typing import Any

from ..rec_utils import load_movielens_sequences, summarize_runs
from ..trainable_sequence_core import SequenceTrainConfig, evaluate_pairwise, train_pairwise
from .model import build_cmsl_model


def reproduce_cmsl(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    config = SequenceTrainConfig()
    baseline_runs, cmsl_runs, training = [], [], []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, baseline_trace = train_pairwise(
            build_cmsl_model(data.item_count, config.dimensions, method="single"),
            data, config, run_seed,
        )
        cmsl, cmsl_trace = train_pairwise(
            build_cmsl_model(data.item_count, config.dimensions, method="cmsl"),
            data, config, run_seed,
        )
        baseline_runs.append(evaluate_pairwise(baseline, data, config))
        cmsl_runs.append(evaluate_pairwise(cmsl, data, config))
        training.append({"seed": run_seed, "single": baseline_trace, "cmsl": cmsl_trace})
    results = {"single_sequence_hstu": summarize_runs(baseline_runs), "cmsl": summarize_runs(cmsl_runs)}
    return {
        "paper": {"arxiv_id": "2606.28533", "title": "CMSL: Constructive Multi-Sequence Learning for Recommendation Systems", "url": "https://arxiv.org/abs/2606.28533", "track": "recommendation"},
        "dataset": "MovieLens 100K (full public positive sequences)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "learned_contextual_lenses": 6, "training": training},
        "results": results,
        "ndcg_gain_percent": 100 * (results["cmsl"]["ndcg_at_10"] - results["single_sequence_hstu"]["ndcg_at_10"]) / max(results["single_sequence_hstu"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"metric_1": 0.116, "metric_2": 0.158, "metric_3": 0.171, "metric_4": 0.092},
        "scope": "Core-mechanism reproduction: contextual lenses and an HSTU-style gated attention backbone are learned end to end. Meta private features, scale and serving stack are not reproduced.",
    }
