from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from auto_research.recommendation_latest_20260930_closure import (
    Skill,
    SkillGenome,
    SkillGenomeController,
)


def reproduce(_dataset_dir: Path, seed: int = 42) -> dict:
    """Execute one typed skill-genome promotion and reuse cycle."""
    rng = np.random.default_rng(seed)
    features = rng.normal(size=12)
    target = np.tanh(features)
    evaluator = lambda output: -float(np.mean((np.asarray(output) - target) ** 2))
    controller = SkillGenomeController(evaluator)
    controller.register(Skill("tanh", "features", "scores", np.tanh))
    genome = SkillGenome(("tanh",), "features", "scores")
    baseline_score = evaluator(features)
    promoted = controller.evaluate_and_promote(
        genome, features, baseline=baseline_score, minimum_gain=1e-12
    )
    reused = controller.reuse()
    return {
        "paper": {
            "arxiv_id": "2609.34552",
            "url": "https://arxiv.org/abs/2609.34552",
        },
        "dataset": "deterministic public mechanism mini-suite",
        "setup": {"seed": seed, "examples": len(features)},
        "baseline": {"name": "untransformed feature genome", "score": baseline_score},
        "method": {
            "name": "typed tanh skill genome",
            "validation_score": promoted["score"],
            "promoted": promoted["promoted"],
            "reusable_genomes": len(reused),
        },
        "scope": (
            "执行 typed genome、validation evaluator、promotion 与 reuse；"
            "不调用外部 LLM，不复刻论文的大规模架构搜索。"
        ),
    }


def render(result: dict) -> str:
    return "# EvoSkillRec\n\n```json\n" + json.dumps(
        result, ensure_ascii=False, indent=2
    ) + "\n```\n"
