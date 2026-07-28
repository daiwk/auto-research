from pathlib import Path
from typing import Any

from ..learn.model import LEARNConfig, content_embeddings
from ..llm_rec_data import load_text_ctr_data
from ..rec_utils import load_movielens_sequences, summarize_runs
from ..trainable_sequence_core import SequenceTrainConfig, evaluate_pairwise, train_pairwise
from .model import build_llatte_model


def reproduce_llatte(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    data = load_movielens_sequences(dataset_dir)
    titles = load_text_ctr_data(dataset_dir).titles
    content = content_embeddings(titles, dataset_dir, LEARNConfig())
    config = SequenceTrainConfig(steps=75, evaluation_batch_size=16)
    baseline_runs, llatte_runs, training = [], [], []
    for run_seed in (seed, seed + 1, seed + 2):
        baseline, baseline_trace = train_pairwise(
            build_llatte_model(content, config.dimensions, method="short"),
            data, config, run_seed,
        )
        llatte, llatte_trace = train_pairwise(
            build_llatte_model(content, config.dimensions, method="llatte"),
            data, config, run_seed,
        )
        baseline_runs.append(evaluate_pairwise(baseline, data, config))
        llatte_runs.append(evaluate_pairwise(llatte, data, config))
        training.append({"seed": run_seed, "short": baseline_trace, "llatte": llatte_trace})
    results = {
        "short_online_sequence": summarize_runs(baseline_runs),
        "llatte_mla_dhen": summarize_runs(llatte_runs),
    }
    return {
        "paper": {"arxiv_id": "2601.20083", "title": "LLaTTE: Scaling Laws for Multi-Stage Sequence Modeling in Large-Scale Ads Recommendation", "url": "https://arxiv.org/abs/2601.20083", "track": "recommendation"},
        "dataset": "MovieLens 100K with BERT-tiny title embeddings (full public interactions)",
        "setup": {"users": len(data.train), "items": data.item_count, "seeds": [seed, seed + 1, seed + 2], "semantic_encoder": "prajjwal1/bert-tiny", "mla_latents": 4, "online_window": 12, "training": training},
        "results": results,
        "ndcg_gain_percent": 100 * (results["llatte_mla_dhen"]["ndcg_at_10"] - results["short_online_sequence"]["ndcg_at_10"]) / max(results["short_online_sequence"]["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"conversion_lift_percent": 4.3, "normalized_entropy_reduction_percent": 0.25},
        "scope": "Core-mechanism reproduction: BERT semantic features, latent upstream attention, target-aware online attention and DHEN gating are trained end to end. Meta private ads features, asynchronous serving and production scale are not reproduced.",
    }
