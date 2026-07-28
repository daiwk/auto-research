from pathlib import Path

import pytest

from auto_research.post_training import PostTrainingConfig, PostTrainingRunner


@pytest.mark.parametrize(
    "algorithm",
    [
        "dpo", "kto", "orpo", "grpo", "dapo", "gspo",
        "ppo-rlhf", "rloo", "remax", "lightning-opd", "gprl", "tcr",
        "constitutional-ai", "rrhf", "raft",
        "slic-hf", "steerlm", "spin",
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


@pytest.mark.parametrize("algorithm", ["ipo", "simpo", "luspo", "coba-rl"])
def test_free_generation_algorithms_use_token_rollouts_and_verifier(
    tmp_path: Path, algorithm: str
):
    result, run_dir = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            dataset="arithmetic-generate",
            steps=2,
            maximum_examples=12,
            seeds=(7,),
            output_dir=tmp_path,
        )
    ).run()
    run = result.training["runs"][0]
    assert run["free_generation"] is True
    assert run["tokenizer"] == "auditable character tokenizer"
    assert run["model"] == "GRU causal LM"
    assert "exact final numeric answer" in run["verifier"]
    assert 0 <= result.final["accuracy"] <= 1
    assert "format_rate" in result.final
    assert (run_dir / "metrics.json").exists()


def test_candidate_algorithms_reject_free_generation_only_objectives():
    with pytest.raises(ValueError, match="requires a free-generation dataset"):
        PostTrainingConfig(algorithm="simpo", dataset="arithmetic-smoke")


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        (
            "constitutional-ai",
            ("critique_violation", "revision_changed", "ai_preference_margin"),
        ),
        ("rrhf", ("ranking_pairs", "ranking_violations", "sft_best_nll")),
        ("raft", ("sampled_responses", "kept_fraction", "selected_reward_quantile")),
    ],
)
def test_missing_classic_alignment_mechanisms_are_observable(
    tmp_path: Path, algorithm: str, diagnostics: tuple[str, ...]
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=20,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    for diagnostic in diagnostics:
        assert diagnostic in result.training["last_diagnostics"]
    if algorithm == "constitutional-ai":
        assert result.training["last_diagnostics"]["human_preference_labels"] == 0
    if algorithm == "raft":
        assert result.training["last_diagnostics"]["kept_responses"] == 1


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        (
            "slic-hf",
            ("calibration_margin", "margin_violation", "sft_regularization_nll"),
        ),
        (
            "steerlm",
            ("attribute_dimensions", "target_attribute_match", "attribute_conditioned_sft"),
        ),
        (
            "spin",
            ("self_play_logit", "opponent_response_probability", "opponent_iteration"),
        ),
    ],
)
def test_p1_alignment_candidate_mechanisms_are_observable(
    tmp_path: Path, algorithm: str, diagnostics: tuple[str, ...]
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=20,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    for diagnostic in diagnostics:
        assert diagnostic in result.training["last_diagnostics"]
    if algorithm == "spin":
        assert result.training["rollout_policy_refreshes"] == 1
