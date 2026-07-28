from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .algorithms import initialize, metrics, update
from .data import load_post_training_data
from .models import PostTrainingConfig, PostTrainingResult


class PostTrainingRunner:
    def __init__(self, config: PostTrainingConfig):
        self.config = config

    def run(self) -> tuple[PostTrainingResult, Path]:
        config = self.config
        data = load_post_training_data(
            config.dataset, config.dataset_dir, config.allow_network,
            config.maximum_examples, config.seed,
        )
        state = initialize(len(data.feature_names), data.train)
        state.teacher_calls = len(data.train) if config.algorithm == "lightning-opd" else 0
        baseline = metrics(state, data.validation)
        rng = np.random.default_rng(config.seed)
        history = []
        last_diagnostics = {}
        for step in range(config.steps):
            index = int(rng.integers(0, len(data.train)))
            loss, last_diagnostics = update(
                config.algorithm, state, data.train[index], config.learning_rate,
                rng, config.group_size, index,
            )
            if step == 0 or (step + 1) % max(1, config.steps // 10) == 0:
                row = {"step": float(step + 1), "loss": loss}
                row.update(metrics(state, data.validation))
                history.append(row)
        final = metrics(state, data.validation)
        training = {
            "steps": config.steps,
            "learning_rate": config.learning_rate,
            "group_size": config.group_size,
            "train_examples": len(data.train),
            "validation_examples": len(data.validation),
            "data_source": data.source,
            "teacher_cache_entries": len(state.teacher_cache)
            if config.algorithm == "lightning-opd" else 0,
            "teacher_prefill_calls": state.teacher_calls,
            "online_teacher_calls": 0,
            "drift_events": state.drift_events,
            "critic_updates": state.critic_updates,
            "rollout_policy_refreshes": state.ppo_updates // 16,
            "last_diagnostics": last_diagnostics,
            "fidelity": "mechanism reproduction on a candidate-policy model",
        }
        result = PostTrainingResult(
            config.algorithm, config.dataset, baseline, final, training, history
        )
        run_dir = config.output_dir / f"{config.algorithm}-{config.dataset}-seed{config.seed}"
        run_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "algorithm": result.algorithm,
            "dataset": result.dataset,
            "baseline": result.baseline,
            "final": result.final,
            "relative_accuracy": result.relative_accuracy,
            "training": result.training,
            "history": result.history,
        }
        (run_dir / "metrics.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        from .report import render_report
        (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")
        return result, run_dir
