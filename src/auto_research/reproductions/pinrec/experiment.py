import os
from pathlib import Path

from ..action_data import load_action_sequences
from ..industrial_ranking import require_backend
from .model import PinRecConfig, build_model, evaluate, train_model


def reproduce_pinrec(dataset_dir: Path, seed: int = 42):
    torch, _ = require_backend()
    config = PinRecConfig(steps=int(os.environ.get("AUTO_RESEARCH_PINREC_STEPS", "160")))
    data = load_action_sequences(dataset_dir)
    torch.manual_seed(seed); baseline, base_training = train_model(build_model(data.item_count, config, False, False), data, config, seed, False)
    torch.manual_seed(seed); method, method_training = train_model(build_model(data.item_count, config, True, True), data, config, seed, True)
    return {
        "paper": {"arxiv_id": "2504.10507", "title": "PinRec: Outcome-Conditioned, Multi-Token Generative Retrieval for Industry-Scale Recommendation Systems", "url": "https://arxiv.org/abs/2504.10507", "track": "recommendation"},
        "dataset": "MovieLens 100K rating outcomes",
        "setup": {"seed": seed, "steps": config.steps, "future_window": config.future_window, "users": len(data.train_items)},
        "results": {"unconditioned_next_token": evaluate(baseline, data, config), "outcome_conditioned_multi_token": evaluate(method, data, config)},
        "training": {"baseline": base_training, "pinrec": method_training},
        "paper_online_ab": {"fulfilled_sessions_percent": 0.28, "time_spent_percent": 0.55, "homefeed_grid_clicks_percent": 3.33, "best_oc_homefeed_grid_clicks_percent": 4.01},
        "scope": "Executes a causal decoder, desired-outcome embeddings, ANN-compatible normalized outputs, and unordered windowed multi-token contrastive training. MovieLens rating outcomes replace Pinterest actions.",
    }
