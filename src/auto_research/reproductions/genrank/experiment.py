import os
from pathlib import Path

from ..action_data import load_action_ctr
from ..industrial_ranking import require_backend
from .model import GenRankConfig, build_model, train_evaluate


def reproduce_genrank(dataset_dir: Path, seed: int = 42):
    torch, _ = require_backend()
    config = GenRankConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_GENRANK_STEPS", "120")),
        maximum_train=int(os.environ.get("AUTO_RESEARCH_GENRANK_TRAIN", "8000")),
        maximum_test=int(os.environ.get("AUTO_RESEARCH_GENRANK_TEST", "2000")),
    )
    train, test, items = load_action_ctr(dataset_dir, config.history)
    train, test = train[:config.maximum_train], test[:config.maximum_test]
    torch.manual_seed(seed)
    baseline = train_evaluate(build_model(items, config, False), train, test, config, seed)
    torch.manual_seed(seed)
    method = train_evaluate(build_model(items, config, True), train, test, config, seed)
    return {
        "paper": {"arxiv_id": "2505.04180", "title": "Towards Large-scale Generative Ranking", "url": "https://arxiv.org/abs/2505.04180", "track": "recommendation"},
        "dataset": "MovieLens 100K explicit action sequence",
        "setup": {"seed": seed, "steps": config.steps, "train_examples": len(train), "test_examples": len(test)},
        "results": {"interleaved_item_action": baseline, "genrank_action_oriented": method},
        "paper_online_ab": {"time_spent_percent": 0.3345, "reads_percent": 0.6325, "engagements_percent": 1.2474, "lt7_percent": 0.1481},
        "scope": "Executes the paper's item-action interleaved baseline and action-oriented organization with position/time bias, causal Transformer action generation, CTR training, and latency comparison.",
    }
