"""Meta MaD-RL reward identities and executable small-model contract."""

from __future__ import annotations

import json
import math

import numpy as np
import pytest

from auto_research.post_training.mad_rl import (
    distribution_rewards, jensen_shannon, run_choice_experiment,
    validate_target,
)


@pytest.mark.parametrize("divergence", ["l2", "forward-kl", "reverse-kl", "jsd"])
def test_rewards_are_zero_when_frequencies_match_target(divergence):
    target = [0.2] * 5
    rewards, frequencies = distribution_rewards(list(range(5)), target, divergence)
    assert frequencies == pytest.approx(target)
    assert rewards == pytest.approx([0.0] * 5)


def test_table_one_rewards_and_off_support_denominator():
    target = [0.0, 0.0, 1 / 3, 1 / 3, 1 / 3]
    rewards, frequencies = distribution_rewards([0, 2, 2, None], target, "l2")
    assert frequencies.tolist() == pytest.approx([0.25, 0.0, 0.5, 0.0, 0.0])
    assert rewards.tolist() == pytest.approx([-0.25, -1 / 6, -1 / 6, -1.0])
    fkl, _ = distribution_rewards([2, 2, 3, 4], target, "forward-kl")
    assert fkl[0] == pytest.approx((1 / 3) / 0.5 - 1)
    rkl, _ = distribution_rewards([0, 2, 2, 4], target, "reverse-kl")
    assert np.isfinite(rkl).all()  # paper's epsilon floor for zero target mass
    jsd, _ = distribution_rewards([2, 2, 3, 4], target, "jsd")
    assert jsd[0] == pytest.approx(0.5 * math.log(((1 / 3 + 0.5) / 2) / 0.5))


def test_target_validation_and_jsd_units():
    with pytest.raises(ValueError, match="sum to one"):
        validate_target([0.1] * 5)
    with pytest.raises(ValueError, match="nonnegative"):
        validate_target([-0.1, 0.3, 0.3, 0.3, 0.2])
    assert jensen_shannon([0.2] * 5, [0.2] * 5) == pytest.approx(0.0)
    assert jensen_shannon([1, 0, 0, 0, 0], [0, 1, 0, 0, 0]) == pytest.approx(math.log(2))


def test_cli_runner_executes_real_rollouts_and_isolates_topics(tmp_path):
    pytest.importorskip("torch")
    result, directory = run_choice_experiment(
        seeds=(42,), divergences=("correctness", "jsd"),
        steps=2, group_size=8, output_dir=tmp_path,
    )
    assert len(result["runs"]) == 2
    assert result["diagnostic_only"] is True
    assert (directory / "report.md").is_file()
    assert json.loads((directory / "metrics.json").read_text())["method"] == "mad-rl"
    for run in result["runs"]:
        protocol = run["protocol"]
        assert not set(protocol["train_topics"]) & set(protocol["test_topics"])
        assert run["final_test"]["valid_samples"] > 0
        assert run["history"][0]["group_frequencies_full_denominator"]
