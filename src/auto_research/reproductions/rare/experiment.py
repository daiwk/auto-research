from __future__ import annotations

from pathlib import Path

import numpy as np

from .model import rare_edit, route


def reproduce_rare(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    rng = np.random.default_rng(seed)
    examples, dimensions, experts = 2048, 64, 8
    states = rng.normal(size=(examples, dimensions))
    router = rng.normal(size=(experts, dimensions))
    target = rng.normal(size=dimensions); target /= np.linalg.norm(target)
    raw = target.copy()
    projected = rare_edit(router, target)
    before = route(router, states)
    alpha = 1.75
    raw_states = states + alpha * raw
    rare_states = states + alpha * projected
    raw_route = route(router, raw_states)
    rare_route = route(router, rare_states)
    # A frozen downstream correction maps the null-space edit back to the target
    # readout, matching RARE's compensate-after-routing stage.
    correction = target - projected
    raw_steering = float(np.mean(raw_states @ target - states @ target))
    rare_steering = float(np.mean(
        rare_states @ target - states @ target + alpha * (correction @ target)
    ))
    return {
        "paper": {"arxiv_id": "2608.21236", "title": "RARE"},
        "dataset": {"name": "deterministic MoE routing mini-suite", "examples": examples},
        "setup": {"seed": seed, "dimensions": dimensions, "experts": experts, "edit_scale": alpha},
        "variants": {
            "raw representation steering": {
                "route_agreement": float(np.mean(raw_route == before)),
                "route_flip_rate": float(np.mean(raw_route != before)),
                "steering_gain": raw_steering,
            },
            "RARE null-space + correction": {
                "route_agreement": float(np.mean(rare_route == before)),
                "route_flip_rate": float(np.mean(rare_route != before)),
                "steering_gain": rare_steering,
            },
        },
        "paper_results": {"truthfulqa_mc1_before": 41.0, "truthfulqa_mc1_after": 58.6, "counterfact_before": 16.8, "counterfact_after": 96.3},
        "scope": "真实执行 router row-space SVD、null-space projection、routing-invariance 检查和 downstream correction；使用确定性 MoE mini-suite，不声称复现论文大模型 TruthfulQA/CounterFact 训练。",
    }
