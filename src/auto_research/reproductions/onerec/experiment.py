from __future__ import annotations

import copy
import os
from pathlib import Path
from typing import Any

from ..plum.model import build_semantic_ids, load_movie_metadata
from ..rec_utils import load_movielens_1m_sequences
from .model import (
    OneRecConfig,
    build_generator,
    evaluate_generator,
    preference_pairs,
    require_backend,
    save_checkpoint,
    session_examples,
    train_dpo,
    train_generator,
    train_reward_model,
)


def reproduce_onerec(dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    torch, _ = require_backend()
    data = load_movielens_1m_sequences(dataset_dir)
    metadata = load_movie_metadata(dataset_dir)
    output = Path(os.environ.get("AUTO_RESEARCH_ONEREC_CHECKPOINTS", "runs/onerec-checkpoints"))
    config = OneRecConfig(
        sft_steps=int(os.environ.get("AUTO_RESEARCH_ONEREC_SFT_STEPS", "240")),
        reward_steps=int(os.environ.get("AUTO_RESEARCH_ONEREC_REWARD_STEPS", "120")),
        dpo_steps=int(os.environ.get("AUTO_RESEARCH_ONEREC_DPO_STEPS", "80")),
        dpo_pairs=int(os.environ.get("AUTO_RESEARCH_ONEREC_DPO_PAIRS", "96")),
        evaluation_users=int(os.environ.get("AUTO_RESEARCH_ONEREC_EVAL_USERS", "200")),
    )
    index = build_semantic_ids(
        data, metadata, cardinalities=(256, 128, 64), seed=seed,
        checkpoint_dir=output / "sid",
    )
    rows = session_examples(data.train, index, config)
    torch.manual_seed(seed)
    generator, layout = build_generator(index, config)
    sft_training = train_generator(generator, layout, rows, config, seed)
    torch.manual_seed(seed + 1)
    reward, reward_training = train_reward_model(
        rows, data.item_count, config, seed + 1
    )
    sft_model = copy.deepcopy(generator)
    baseline = evaluate_generator(
        sft_model, data, index, layout, config, seed + 2
    )
    pairs = preference_pairs(
        generator, reward, rows, index, layout, data.popularity, config, seed + 3
    )
    if not pairs:
        raise RuntimeError("OneRec self-sampling produced no valid preference pairs")
    dpo_training = train_dpo(generator, pairs, layout, config)
    aligned = evaluate_generator(
        generator, data, index, layout, config, seed + 2
    )
    save_checkpoint(generator, reward, output / f"seed-{seed}", torch)
    results = {
        "session_generator_sft": baseline,
        "onerec_iterative_preference_alignment": aligned,
    }
    return {
        "paper": {"arxiv_id": "2502.18965", "title": "OneRec: Unifying Retrieve and Rank with Generative Recommender and Iterative Preference Alignment", "url": "https://arxiv.org/abs/2502.18965", "track": "recommendation"},
        "dataset": "MovieLens 1M (public replacement for private Kuaishou logs)",
        "setup": {
            "users": len(data.train), "items": data.item_count, "seed": seed,
            "sid_cardinalities": list(index.cardinalities),
            "sid_uniqueness": index.uniqueness,
            "session_items": config.session_items,
            "experts": config.experts,
            "sft_steps": config.sft_steps,
            "reward_steps": config.reward_steps,
            "dpo_steps": config.dpo_steps,
            "evaluation_users": min(config.evaluation_users, len(data.train)),
        },
        "training": {
            "sid": index.training_metrics,
            "session_sft": sft_training,
            "reward_model": reward_training,
            "dpo": dpo_training,
        },
        "results": results,
        "ndcg_gain_percent": 100 * (aligned["ndcg_at_10"] - baseline["ndcg_at_10"]) / max(baseline["ndcg_at_10"], 1e-12),
        "paper_online_ab": {"traffic_percent": 1.0, "total_watch_time_percent": 1.68, "average_view_duration_percent": 6.56},
        "scope": "Runs RQ semantic-ID training, a session-wise encoder-decoder with sparse MoE, personalized reward-model training, model self-sampling, self-hard winner/loser selection, DPO, and constrained multi-item generation. A 96d local model and MovieLens replace OneRec-1B and private Kuaishou feedback labels.",
    }
