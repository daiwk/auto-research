import numpy as np
import pytest

from auto_research.foundation_models.e_means import cosine_step, diagnostic, fit, _revive


def test_one_step_ema_updates_counts_and_sums_not_centroids():
    rows = np.array([[0.0], [2.0], [10.0], [14.0]])
    result = fit(rows, k=2, epochs=1, batch_size=4, alpha0=0.5, seed=42,
                 initial_indices=np.array([0, 2]))
    np.testing.assert_allclose(result.ema_centers[:, 0], [1.0, 12.0], atol=1e-9)
    np.testing.assert_array_equal(result.centers[:, 0], [1.0, 12.0])
    np.testing.assert_array_equal(result.last_assignments, [0, 0, 1, 1])
    assert result.revival_count == 0 and result.steps == 1


def test_revival_perturbs_donor_in_opposite_alternating_directions():
    counts = np.array([8.0, 0.01, 0.02])
    sums = np.array([[16.0, 32.0], [0.0, 0.0], [0.0, 0.0]])
    assert _revive(counts, sums, np.random.default_rng(5)) == 1
    np.testing.assert_array_equal(counts, [4.0, 4.0, 0.02])
    np.testing.assert_allclose(sums[0] / 4.0, [2 * (1 - 1 / 128), 4 * (1 + 1 / 128)])
    np.testing.assert_allclose(sums[1] / 4.0, [2 * (1 + 1 / 128), 4 * (1 - 1 / 128)])
    np.testing.assert_array_equal(sums[:2].sum(axis=0), [16, 32])


def test_empty_last_epoch_slots_and_unit_alpha_stay_finite():
    rows = np.array([[0.0], [0.0], [10.0], [10.0]])
    result = fit(rows, k=2, epochs=1, batch_size=4, alpha0=1.0, seed=0,
                 initial_indices=np.array([0, 1]))
    assert np.isfinite(result.centers).all()
    assert result.centers[0, 0] == 5.0
    assert result.centers[1, 0] == 0.0
    assert cosine_step(0, 1, 1.0) == 1.0


def test_diagnostic_is_seeded_cpu_only():
    for seed in (42, 43, 44):
        first = diagnostic(seed)
        assert first == diagnostic(seed)
        assert all(first["checks"].values())
    with pytest.raises(ValueError, match="CPU-only"):
        diagnostic(42, device="cuda")
    with pytest.raises(ValueError, match="dividing"):
        fit(np.zeros((4, 1)), k=2, epochs=1, batch_size=3, alpha0=0.2, seed=0)
