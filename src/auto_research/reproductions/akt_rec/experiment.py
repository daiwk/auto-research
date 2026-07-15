from __future__ import annotations

import os
from pathlib import Path

from ..rec_utils import summarize_runs
from .data import load_akt_data
from .model import AKTConfig, evaluate, train_model
from .semantic import train_llm_semantics


def reproduce_akt_rec(dataset_dir: Path, seed: int = 42) -> dict:
    maximum_users = int(os.environ.get("AUTO_RESEARCH_AKT_USERS", "320"))
    data = load_akt_data(dataset_dir, seed, maximum_users=maximum_users)
    model_name = os.environ.get("AUTO_RESEARCH_AKT_MODEL", "HuggingFaceTB/SmolLM2-135M")
    item_steps = int(os.environ.get("AUTO_RESEARCH_AKT_ITEM_STEPS", "30"))
    user_steps = int(os.environ.get("AUTO_RESEARCH_AKT_USER_STEPS", "30"))
    _, _, item_codes, user_codes, semantic_training = train_llm_semantics(
        data, model_name, item_steps, user_steps, seed
    )
    config = AKTConfig(steps=int(os.environ.get("AUTO_RESEARCH_AKT_STEPS", "400")))
    seed_count = int(os.environ.get("AUTO_RESEARCH_AKT_SEEDS", "3"))
    seeds = tuple(seed + index for index in range(seed_count))
    validation = {name: [] for name in ("online_base", "akt_rec")}
    test = {name: [] for name in validation}
    training = {name: [] for name in validation}
    for run_seed in seeds:
        for name in validation:
            model, metrics = train_model(name, data, item_codes, user_codes, config, run_seed)
            training[name].append(metrics)
            validation[name].append(evaluate(model, data.validation, data, config))
            test[name].append(evaluate(model, data.test, data, config))
    validation_summary = {name: summarize_runs(values) for name, values in validation.items()}
    test_summary = {name: summarize_runs(values) for name, values in test.items()}
    baseline, proposed = test_summary["online_base"], test_summary["akt_rec"]
    return {
        "paper": {
            "arxiv_id": "2605.23310",
            "title": "From Head to Tail: Asymmetric Knowledge Transfer in Long-tail Recommendation with Generative Semantic IDs",
            "url": "https://arxiv.org/abs/2605.23310",
            "organization": "Alibaba Group / Peking University",
        },
        "dataset": {
            "name": "MovieLens 100K",
            "users": data.user_count,
            "items": data.item_count,
            "train_ctr_rows": len(data.train),
            "validation_ctr_rows": len(data.validation),
            "test_ctr_rows": len(data.test),
            "tail_definition": "fewer than 10 positive train interactions",
        },
        "setup": {
            "model": model_name,
            "item_contrastive_steps": item_steps,
            "user_supervision_steps": user_steps,
            "ctr_steps_per_variant_seed": config.steps,
            "seeds": list(seeds),
            "semantic_codebooks": [16, 16, 16],
            "transfer_weights": [config.transfer_weight_head, config.transfer_weight_tail],
        },
        "semantic_training": semantic_training,
        "training": training,
        "validation": validation_summary,
        "test": test_summary,
        "relative": {
            "auc_percent": _gain(proposed["auc"], baseline["auc"]),
            "gauc_percent": _gain(proposed["gauc"], baseline["gauc"]),
            "tail_auc_percent": _gain(proposed["tail_auc"], baseline["tail_auc"]),
        },
        "paper_results": {
            "offline_auc_base": 0.7510,
            "offline_auc_akt_rec": 0.7536,
            "offline_gauc_base": 0.6385,
            "offline_gauc_akt_rec": 0.6483,
            "online_clicks_percent": 2.73,
            "online_ctr_percent": 2.76,
            "online_ctcvr_percent": 1.70,
            "online_gmv_percent": 3.47,
        },
        "scope": (
            "Fine-tunes a real open causal LM with item co-occurrence InfoNCE and supervised "
            "user interest/category objectives, trains item/user RQ-VAEs into three/two-level "
            "semantic IDs, then executes cluster/individual decoupling, asymmetric "
            "stop-gradient transfer, orthogonality, target-aware history retrieval and two activity "
            "gates. MovieLens text/genres replace images, industrial statistics and private Tmall logs."
        ),
    }


def _gain(value: float, baseline: float) -> float:
    return 100.0 * (value - baseline) / max(abs(baseline), 1e-12)
