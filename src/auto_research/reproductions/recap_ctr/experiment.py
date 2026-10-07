from __future__ import annotations

import json
from pathlib import Path

import torch

from auto_research.mechanisms.recap_recursive_routes import recap_recursive_routes


def reproduce(_dataset_dir: Path, seed: int = 42) -> dict:
    torch.manual_seed(seed)
    features = torch.randn(32, 8)
    block = torch.nn.Sequential(torch.nn.Linear(8, 8), torch.nn.Tanh())
    averaged, audit = recap_recursive_routes(features, block, routes=3, ema_decay=.9)
    routes = audit["routes"]
    return {
        "paper": {"arxiv_id": "2609.37905", "url": "https://arxiv.org/abs/2609.37905"},
        "dataset": "deterministic public mechanism mini-suite",
        "setup": {"seed": seed, "examples": len(features), "routes": 3},
        "baseline": {"name": "single recursive route", "logit_variance": float(routes[0].var())},
        "method": {
            "name": "weight-shared recursive route average",
            "averaged_logit_variance": float(averaged.var()),
            "route_diversity": float(routes.var(0).mean()),
            "ema_norm": float(audit["trajectory_ema"].norm()),
        },
        "scope": "执行共享递归、route 平均和训练轨迹 EMA；未复刻大规模 CTR benchmark 或独立模型蒸馏。",
    }


def render(result: dict) -> str:
    return "# RECAP CTR\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"
