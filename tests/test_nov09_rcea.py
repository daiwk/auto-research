from math import log

import pytest

from auto_research.post_training.rcea import (
    Trajectory, diagnostic, entropy_allocation, local_entropy_change,
)


def test_uniform_support_has_exact_six_way_chain_rule():
    rows = [Trajectory(0.125, False)] * 2 + [Trajectory(0.125, True, False)] * 2 + [
        Trajectory(0.125, True, True, mode) for mode in ("a", "a", "b", "b")
    ]
    result = entropy_allocation(rows)
    assert result.total == pytest.approx(log(8))
    assert result.reconstructed == pytest.approx(result.total)
    assert result.effective_modes == pytest.approx(2)
    assert result.modes == pytest.approx(0.5 * log(2))
    assert result.within_mode == pytest.approx(0.5 * log(2))
    assert result.invalid_success == pytest.approx(0.25 * log(2))
    assert result.failed == pytest.approx(0.25 * log(2))


def test_absent_mode_is_not_one_and_unlabelled_success_rejected():
    result = entropy_allocation([Trajectory(1.0, False), Trajectory(0.0, True, True, "a")])
    assert result.total == result.reconstructed == 0
    assert result.effective_modes is None
    with pytest.raises(ValueError, match="need validity"):
        entropy_allocation([Trajectory(1.0, True)])
    with pytest.raises(ValueError, match="sum to one"):
        entropy_allocation([Trajectory(0.8, False)])


def test_covariance_is_logit_shift_invariant_and_matches_small_finite_step():
    logits = [2.0, 0.0, -2.0]
    small_step = [0.002, 0.0, -0.002]
    prediction, actual = local_entropy_change(logits, small_step)
    assert prediction < 0 and actual == pytest.approx(prediction, rel=0.002)
    assert local_entropy_change(logits, [x + 10 for x in small_step]) == pytest.approx((prediction, actual))
    assert local_entropy_change(logits, [1.0] * 3) == pytest.approx((0.0, 0.0))
    with pytest.raises(ValueError, match="match vocabulary"):
        local_entropy_change(logits, [0.1])


def test_diagnostic_has_no_cuda_path():
    result = diagnostic(42)
    assert all(result["checks"].values())
    assert result["metrics"]["entropy_reconstruction_abs_error"] < 1e-12
    with pytest.raises(ValueError, match="only supports CPU"):
        diagnostic(42, device="cuda")
