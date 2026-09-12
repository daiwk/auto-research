from __future__ import annotations

import math

import pytest

from auto_research.post_training.models import PostTrainingConfig
from auto_research.post_training.runner import PostTrainingRunner


@pytest.mark.parametrize(
    ("algorithm", "diagnostic"),
    [
        ("oprd", "teacher_shift_abs_mean"),
        ("route-opd", "transported_mass"),
        ("compass-opd", "centered_cross_family_gap"),
        ("probe-erpo", "probe_consensus_mean"),
    ],
)
def test_latest_post_training_mechanisms_execute(tmp_path, algorithm, diagnostic):
    result, run_dir = PostTrainingRunner(
        PostTrainingConfig(
            algorithm=algorithm,
            dataset="arithmetic-smoke",
            output_dir=tmp_path,
            steps=4,
            maximum_examples=32,
            group_size=4,
            allow_network=False,
        )
    ).run()

    assert run_dir.joinpath("metrics.json").is_file()
    assert result.training["diagnostic_only"] is True
    assert result.training["promotion_eligible"] is False
    assert result.training["rollout_policy_refreshes"] == 0
    value = result.training["last_diagnostics"][diagnostic]
    assert math.isfinite(value)
