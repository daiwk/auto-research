from pathlib import Path

import pytest

from auto_research.post_training import PostTrainingConfig, PostTrainingRunner


@pytest.mark.parametrize(
    "algorithm",
    [
        "dpo", "kto", "orpo", "grpo", "dapo", "gspo",
        "ppo-rlhf", "rloo", "remax", "lightning-opd", "gprl", "tcr",
    ],
)
def test_post_training_algorithms_run_and_report(tmp_path: Path, algorithm: str):
    result, run_dir = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=12,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    assert 0 <= result.final["accuracy"] <= 1
    assert "kl_from_reference" in result.final
    assert (run_dir / "metrics.json").exists()
    assert (run_dir / "report.md").exists()


def test_lightning_opd_has_no_online_teacher_calls(tmp_path: Path):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm="lightning-opd",
            steps=8,
            maximum_examples=32,
            output_dir=tmp_path,
        )
    ).run()
    assert result.training["teacher_cache_entries"] == 32
    assert result.training["teacher_prefill_calls"] == 32
    assert result.training["online_teacher_calls"] == 0


@pytest.mark.parametrize(
    ("algorithm", "diagnostic"),
    [
        ("ppo-rlhf", "value_loss"),
        ("rloo", "leave_one_out_variance"),
        ("remax", "greedy_baseline_reward"),
    ],
)
def test_classic_rlhf_mechanisms_are_exposed(
    tmp_path: Path, algorithm: str, diagnostic: str
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=20,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    assert diagnostic in result.training["last_diagnostics"]
    if algorithm == "ppo-rlhf":
        assert result.training["critic_updates"] == 20
        assert result.training["rollout_policy_refreshes"] == 1
    else:
        assert result.training["last_diagnostics"]["value_model_parameters"] == 0


def test_dpo_exposes_pairwise_reference_margin(tmp_path: Path):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm="dpo", steps=20, maximum_examples=48, output_dir=tmp_path
        )
    ).run()
    diagnostics = result.training["last_diagnostics"]
    assert "preference_margin" in diagnostics
    assert diagnostics["reward_model_parameters"] == 0


def test_grpo_uses_old_policy_clipping_without_critic(tmp_path: Path):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm="grpo", steps=20, maximum_examples=48, output_dir=tmp_path
        )
    ).run()
    diagnostics = result.training["last_diagnostics"]
    assert "importance_ratio" in diagnostics
    assert "clip_fraction" in diagnostics
    assert diagnostics["value_model_parameters"] == 0
    assert result.training["critic_updates"] == 0
    assert result.training["rollout_policy_refreshes"] == 1


@pytest.mark.parametrize(
    ("algorithm", "diagnostic"),
    [
        ("kto", "desirable_utility"),
        ("orpo", "log_odds_margin"),
        ("dapo", "clip_high"),
        ("gspo", "sequence_ratio_mean"),
    ],
)
def test_additional_preference_and_reasoning_rl_mechanisms(
    tmp_path: Path, algorithm: str, diagnostic: str
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=20,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    assert diagnostic in result.training["last_diagnostics"]
    if algorithm in {"dapo", "gspo"}:
        assert result.training["rollout_policy_refreshes"] == 1
