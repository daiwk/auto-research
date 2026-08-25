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
        if config.dataset.endswith("-generate"):
            return self._run_generation()
        data = load_post_training_data(
            config.dataset, config.dataset_dir, config.allow_network,
            config.maximum_examples, config.seed,
        )
        state = initialize(len(data.feature_names), data.train)
        teacher_cached = {
            "gkd", "minillm", "opsd", "dash", "beta-opsd", "opcd", "flux-opd",
            "lightning-opd", "relay-opd", "turn-opd", "distilled-rl",
            "u-opsd", "rp-opsd", "pcsd", "adrs", "mopd", "opd-lm",
            "r2-opd", "sr-opsd", "opd2", "causal-opd", "smopd", "rstg",
        }
        state.teacher_calls = len(data.train) if config.algorithm in teacher_cached else 0
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
        refresh_updates = {
            "ppo-rlhf": state.ppo_updates,
            "grpo": state.grpo_updates,
            "reco-grpo": state.reco_updates,
            "dapo": state.dapo_updates,
            "gspo": state.gspo_updates,
            "spin": state.spin_updates,
            "ripo": state.variant_updates,
            "tis": state.variant_updates,
            "icepop": state.variant_updates,
            "kpop": state.variant_updates,
            "gppo": state.variant_updates,
            "dr-grpo": state.variant_updates,
            "armor": state.variant_updates,
            "reinforce-plus": state.variant_updates,
            "taco": state.variant_updates,
            "chord": state.variant_updates,
            "vapo": state.variant_updates,
            "vad": state.variant_updates,
            "r2-opd": state.variant_updates,
            "sr-opsd": state.variant_updates,
            "opd2": state.variant_updates,
            "causal-opd": state.variant_updates,
            "smopd": state.variant_updates,
            "rstg": state.variant_updates,
            "sa-mrpo": state.variant_updates,
            "rubric-dropout": state.variant_updates,
            "erils": state.variant_updates,
            "crpo": state.variant_updates,
            "serpo": state.variant_updates,
            "iso-rlvr": state.variant_updates,
            "srpo": state.variant_updates,
            "erpo": state.variant_updates,
        }.get(config.algorithm, 0)
        rollout_policy_refreshes = (
            state.online_rollout_refreshes
            if config.algorithm == "online-icepop"
            else refresh_updates // 16
        )
        training = {
            "steps": config.steps,
            "learning_rate": config.learning_rate,
            "group_size": config.group_size,
            "train_examples": len(data.train),
            "validation_examples": len(data.validation),
            "data_source": data.source,
            "teacher_cache_entries": len(state.teacher_cache)
            if config.algorithm in teacher_cached else 0,
            "teacher_prefill_calls": state.teacher_calls,
            "online_teacher_calls": state.online_teacher_calls,
            "drift_events": state.drift_events,
            "critic_updates": state.critic_updates,
            "rollout_policy_refreshes": rollout_policy_refreshes,
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

    def _run_generation(self):
        from .generation import load_generation_suite, train_free_generation
        from .coba_teacher import HFTeacherGenerator

        config = self.config
        seeds = config.seeds or (config.seed, config.seed + 1, config.seed + 2)
        teacher = (
            HFTeacherGenerator(
                config.teacher_model_id, config.teacher_revision,
                config.teacher_checkpoint_path, config.allow_network,
                config.teacher_max_new_tokens,
            )
            if config.teacher_model_id else None
        )
        baselines, finals, training = [], [], []
        for seed in seeds:
            suite = load_generation_suite(
                config.dataset, config.dataset_dir, config.allow_network,
                config.maximum_examples, seed,
            )
            baseline, final, diagnostics = train_free_generation(
                config.algorithm, suite, config.steps, config.learning_rate,
                config.group_size, seed,
                teacher=teacher,
                teacher_cache_path=(
                    config.teacher_cache
                    or config.output_dir / "coba-cache" / "teacher.json"
                ) if teacher else None,
                boundary_cache_path=(
                    _seed_cache_path(config.boundary_cache, seed)
                    if config.boundary_cache else
                    config.output_dir / "coba-cache" / f"boundary-seed{seed}.json"
                ) if teacher else None,
                boundary_samples=config.boundary_samples,
                teacher_input_cost_per_million=config.teacher_input_cost_per_million,
                teacher_output_cost_per_million=config.teacher_output_cost_per_million,
            )
            baselines.append(baseline)
            finals.append(final)
            training.append(diagnostics)
        baseline = _mean_metrics(baselines)
        final = _mean_metrics(finals)
        teacher_runs = [row["teacher"] for row in training]
        teacher_requests = sum(
            row["actual_calls"] + row["cache_hits"] for row in teacher_runs
        )
        result = PostTrainingResult(
            config.algorithm, config.dataset, baseline, final,
            {
                "seeds": list(seeds),
                "runs": training,
                "data_source": suite.source,
                "fidelity": "token-level causal-LM free generation with executable verifier",
                "teacher_summary": {
                    "enabled": teacher is not None,
                    "actual_calls": sum(row["actual_calls"] for row in teacher_runs),
                    "cache_hits": sum(row["cache_hits"] for row in teacher_runs),
                    "teacher_request_rate": (
                        teacher_requests / max(1, config.steps * len(seeds))
                    ),
                    "input_tokens": sum(row["input_tokens"] for row in teacher_runs),
                    "output_tokens": sum(row["output_tokens"] for row in teacher_runs),
                    "estimated_cost": sum(row["estimated_cost"] for row in teacher_runs),
                    "provenance": teacher.provenance() if teacher else None,
                },
            },
            [
                {"seed": float(row["seed"]), **entry}
                for row in training for entry in row["history"]
            ],
        )
        run_dir = (
            config.output_dir
            / f"{config.algorithm}-{config.dataset}-seeds{'-'.join(map(str, seeds))}"
        )
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
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        from .report import render_report
        (run_dir / "report.md").write_text(render_report(result), encoding="utf-8")
        return result, run_dir


def _mean_metrics(rows):
    return {
        key: float(np.mean([row[key] for row in rows]))
        for key in rows[0]
    } | {
        f"{key}_std": float(np.std([row[key] for row in rows]))
        for key in rows[0]
    }


def _seed_cache_path(path: Path, seed: int) -> Path:
    rendered = str(path)
    if "{seed}" in rendered:
        return Path(rendered.format(seed=seed))
    return path.with_name(f"{path.stem}-seed{seed}{path.suffix}")
