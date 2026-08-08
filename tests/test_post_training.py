from pathlib import Path

import numpy as np
import pytest

from auto_research.post_training import PostTrainingConfig, PostTrainingRunner
from auto_research.post_training.rollout_correction import (
    icepop_weights,
    truncated_importance_weights,
)


@pytest.mark.parametrize(
    "algorithm",
    [
        "dpo", "kto", "orpo", "grpo", "dapo", "gspo",
        "ppo-rlhf", "rloo", "remax", "lightning-opd", "gprl", "tcr",
        "gkd", "minillm", "opsd", "dash", "beta-opsd", "opcd", "flux-opd",
        "constitutional-ai", "rrhf", "raft",
        "slic-hf", "steerlm", "spin",
        "ripo", "tis", "icepop", "online-icepop", "kpop", "gppo",
        "dr-grpo", "armor", "reinforce-plus", "taco", "chord", "vapo",
        "vad",
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
    ("algorithm", "diagnostics"),
    [
        (
            "gkd",
            (
                "student_generated_rollouts",
                "on_policy_fraction",
                "teacher_forward_passes",
                "student_support_fraction",
            ),
        ),
        (
            "minillm",
            (
                "reverse_kl",
                "teacher_mixed_sampling",
                "variance_reduction_baseline",
                "length_normalized_objective",
            ),
        ),
    ],
)
def test_classic_on_policy_distillation_mechanisms_are_observable(
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
    assert result.training["online_teacher_calls"] > 0
    assert result.training["teacher_cache_entries"] == 48


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        (
            "opsd",
            (
                "shared_teacher_student_parameters",
                "privileged_solution_conditioning",
                "dense_token_teacher_calls",
                "pointwise_divergence_clip",
                "jsd_beta",
            ),
        ),
        (
            "dash",
            (
                "adaptive_gate_mean",
                "backward_horizon_mean",
                "local_divergence_clip",
                "extra_teacher_forward_passes",
            ),
        ),
        (
            "opcd",
            (
                "context_conditioned_teacher_calls",
                "context_free_student_view",
                "experience_context_fraction",
                "reverse_kl",
                "experience_internalization_updates",
            ),
        ),
        (
            "beta-opsd",
            (
                "beta_reference_anchor",
                "closed_form_geometric_target",
                "return_to_go_min",
                "privileged_teacher_calls",
            ),
        ),
        (
            "flux-opd",
            (
                "context_free_anchor",
                "evolving_context_teachers",
                "context_conflict_jsd",
                "conflict_weighted_correction",
            ),
        ),
        (
            "vad",
            (
                "teacher_views",
                "visual_evidence_norm",
                "teacher_correction_alignment",
                "one_sided_projection",
                "support_budget_share",
                "refutation_budget_share",
                "attribution_anchor_weight",
                "primary_jsd",
                "regularizer_jsd",
            ),
        ),
    ],
)
def test_privileged_and_context_on_policy_distillation_are_observable(
    tmp_path: Path, algorithm: str, diagnostics: tuple[str, ...]
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=24,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()
    for diagnostic in diagnostics:
        assert diagnostic in result.training["last_diagnostics"]
    assert result.training["online_teacher_calls"] > 0
    assert result.final["accuracy"] >= result.baseline["accuracy"]


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


def test_tis_clamps_only_the_upper_training_inference_ratio():
    correction = truncated_importance_weights(
        np.asarray((0.05, 0.45, 0.50)),
        np.asarray((0.50, 0.45, 0.05)),
        maximum=2.0,
    )

    np.testing.assert_allclose(correction.ratios, (0.1, 1.0, 10.0))
    np.testing.assert_allclose(correction.weights, (0.1, 1.0, 2.0))
    assert correction.kept.all()
    assert correction.adjusted.tolist() == [False, False, True]


def test_icepop_masks_both_ratio_tails_without_clamping_in_band():
    correction = icepop_weights(
        np.asarray((0.05, 0.45, 0.50)),
        np.asarray((0.50, 0.45, 0.05)),
        lower=0.5,
        upper=5.0,
    )

    np.testing.assert_allclose(correction.ratios, (0.1, 1.0, 10.0))
    np.testing.assert_allclose(correction.weights, (0.0, 1.0, 0.0))
    assert correction.kept.tolist() == [False, True, False]
    assert correction.adjusted.tolist() == [True, False, True]


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        (
            "tis",
            (
                "tis_upper_bound",
                "tis_clipped_fraction",
                "training_inference_ratio_mean",
            ),
        ),
        (
            "icepop",
            (
                "icepop_lower_bound",
                "icepop_upper_bound",
                "icepop_kept_fraction",
            ),
        ),
        (
            "online-icepop",
            (
                "updates_per_rollout_batch",
                "forced_on_policy_ratio",
                "icepop_kept_fraction",
            ),
        ),
    ],
)
def test_training_inference_corrections_are_observable(
    tmp_path: Path, algorithm: str, diagnostics: tuple[str, ...]
):
    steps = 20
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            steps=steps,
            maximum_examples=48,
            output_dir=tmp_path,
        )
    ).run()

    for name in diagnostics:
        assert name in result.training["last_diagnostics"]
    last = result.training["last_diagnostics"]
    if algorithm == "tis":
        assert last["tis_clipped_fraction"] > 0
        assert last["mismatch_tokens_dropped"] == 0
        assert result.training["rollout_policy_refreshes"] == 1
    elif algorithm == "icepop":
        assert last["ppo_clip_active"] == 1
        assert 0 < last["icepop_kept_fraction"] < 1
        assert last["mismatch_tokens_dropped"] > 0
        assert result.training["rollout_policy_refreshes"] == 1
    else:
        assert last["ppo_clip_active"] == 0
        assert 0 < last["icepop_kept_fraction"] < 1
        assert last["mismatch_tokens_dropped"] > 0
        assert last["policy_staleness_ratio_mean"] == 1
        assert result.training["rollout_policy_refreshes"] == steps


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        ("ripo", ("fisher_rao_radius_mean", "probability_dependent_clip")),
        ("kpop", ("binary_kl_forward_mean", "adaptive_mask_kept_fraction")),
        ("gppo", ("ppo_forward_surrogate", "preserved_boundary_gradients")),
        ("dr-grpo", ("group_std_normalization", "response_length_normalization")),
        ("armor", ("reference_anchor_trajectories", "anchor_loss_weight")),
        ("reinforce-plus", ("global_advantage_std", "prompt_local_std")),
        ("taco", ("mean_token_surprisal", "negative_credit_preserved")),
        ("chord", ("expert_sft_weight", "dynamic_weighting")),
        ("vapo", ("pretrained_value_model", "length_adaptive_gae_lambda")),
    ],
)
def test_rl_summary_algorithm_mechanisms_are_observable(
    tmp_path: Path, algorithm: str, diagnostics: tuple[str, ...]
):
    result, _ = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm, steps=20, maximum_examples=48, output_dir=tmp_path
        )
    ).run()
    for name in diagnostics:
        assert name in result.training["last_diagnostics"]
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


@pytest.mark.parametrize(
    ("algorithm", "diagnostics"),
    [
        (
            "relay-opd",
            (
                "prefix_failure_detected",
                "teacher_handoff_triggered",
                "relay_budget",
                "student_resumes_after_teacher_leg",
            ),
        ),
        (
            "cort",
            (
                "counterfactual_replays",
                "rubric_conditioned_contrast",
                "token_weight_min",
                "token_weight_max",
            ),
        ),
    ],
)
def test_20260729_post_training_mechanisms_are_observable(
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
    if algorithm == "cort":
        assert result.training["last_diagnostics"]["auxiliary_token_scorer_parameters"] == 0
