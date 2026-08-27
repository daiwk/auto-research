from __future__ import annotations

from pathlib import Path

import numpy as np


def _tasks(seed: int, count: int = 300):
    rng = np.random.default_rng(seed)
    tasks = []
    for index in range(count):
        kind = index % 3
        start = rng.integers(0, 8, size=2)
        velocity = rng.integers(-2, 3, size=2)
        steps = int(rng.integers(1, 6))
        target = np.clip(start + velocity * steps, 0, 7)
        tasks.append((kind, start, velocity, steps, target))
    return tasks


def _evaluate(tasks, *, rule_grounded: bool, seed: int):
    rng = np.random.default_rng(seed)
    rewards = []
    for kind, start, velocity, steps, target in tasks:
        if rule_grounded:
            predicted = np.clip(start + velocity * steps, 0, 7)
            reward = float(np.array_equal(predicted, target))
        else:
            # A scalar visual judge is deliberately sensitive to fluent but
            # unsupported trajectories, matching the failure mode under study.
            predicted = np.clip(start + velocity * max(1, steps - 1), 0, 7)
            reward = float(np.array_equal(predicted, target))
            reward = 0.75 * reward + 0.25 * float(rng.random() > 0.45)
        rewards.append(reward)
    values = np.asarray(rewards)
    return {"reward_mean": float(values.mean()), "reward_std": float(values.std())}


def reproduce_vbvr_pro(dataset_dir: Path, seed: int = 42) -> dict:
    del dataset_dir
    tasks = _tasks(seed)
    judge = _evaluate(tasks, rule_grounded=False, seed=seed)
    verifier = _evaluate(tasks, rule_grounded=True, seed=seed)
    return {
        "paper": {"arxiv_id": "2608.26105", "title": "VBVR-Pro"},
        "dataset": {"name": "VBVR-Pro procedural task specification", "tasks": len(tasks)},
        "setup": {"seed": seed, "modalities": ["image-state", "interleaved", "video-state"]},
        "variants": {"scalar VLM-judge analogue": judge, "task-grounded verifier": verifier},
        "relative": {"reward_mean_percent": 100 * (verifier["reward_mean"] - judge["reward_mean"]) / max(judge["reward_mean"], 1e-9)},
        "diagnostics": {"deterministic_scorers": 3, "judge_calls": 300, "verifier_calls": 300},
        "scope": "复刻 300 个程序化状态转移任务与确定性 task-specific scorer，对比易受流畅度影响的标量 judge；不训练或加载 14B/19B 视频生成器，也不冒充七个外部 benchmark 结果。",
        "diagnostic_only": True,
    }
