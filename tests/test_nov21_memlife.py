"""MemOpt input-array arithmetic and declared causal access, not VLM capability."""
import math

import numpy as np
import pytest

from auto_research.agent_research.memlife import (
    MemoryEntry, diagnostic, eligible_memories, faithfulness_from_probabilities,
    fetch_memory, firm_reward, group_relative_advantage, memopt_loss, search_memory,
)


def test_faithfulness_probability_margin_and_multiplicative_reward():
    mask = np.array([[True, True, False]])
    faith = faithfulness_from_probabilities([[.5, .2, 0]], [[.5, .8, 0]], mask)
    assert faith == pytest.approx(np.array([[1, .4, 0]]))
    assert firm_reward(faith, [.5], [.2], mask) == pytest.approx(np.array([[.1, .04, 0]]))
    assert np.all(firm_reward(faith, [0], [1], mask) == 0)
    with pytest.raises(ValueError):
        faithfulness_from_probabilities([[.6]], [[.5]], np.array([[True]]))


def test_candidate_macro_mean_and_group_centered_not_within_variance():
    values = np.array([[1., 0., 0.], [0., 0., 0.]])
    mask = np.array([[True, False, False], [True, True, True]])
    result = group_relative_advantage(values, mask, ["a", "a"])
    assert result["group_means"]["a"] == .5  # Pooled tokens would give .25.
    assert result["group_variances"]["a"] == .25  # Within-candidate deviations would give0.
    assert result["raw"][0, 0] == pytest.approx(1 / (1 + 2e-6))
    assert np.all(result["advantages"][~mask] == 0)
    assert result["centered"][mask].sum() == pytest.approx(0, abs=1e-12)


def test_clip_then_per_group_token_recenter_then_global_whiten():
    x = np.zeros((4, 40))
    x[0, 0] = 1
    x[2] = .8
    x[3] = .2
    mask = np.ones(x.shape, dtype=bool)
    mask[2, 3:] = False
    out = group_relative_advantage(x, mask, ["a", "a", "b", "b"])
    assert out["clipped"].max() == 3
    for rows in ([0, 1], [2, 3]):
        assert out["centered"][rows][mask[rows]].mean() == pytest.approx(0, abs=1e-12)
    valid = out["advantages"][mask]
    assert valid.mean() == pytest.approx(0, abs=1e-12)
    assert valid.var(ddof=1) == pytest.approx(1, abs=1e-6)
    assert out["global_variance_correction"] == 1


def test_flat_groups_and_empty_candidates_do_not_create_signal():
    mask = np.array([[True, True], [False, False], [True, True], [False, False]])
    values = np.array([[.4, .4], [9, 9], [.4, .4], [9, 9]])
    result = group_relative_advantage(values, mask, ["a", "a", "a", "empty"])
    assert result["group_means"] == {"a": .4, "empty": 0}
    assert np.all(result["advantages"] == 0)


def test_clipped_objective_keeps_kl_outside_reward_normalization():
    mask = np.array([[True, True]])
    loss = memopt_loss([[1.5, .5]], [[1, -1]], [[.2, .4]], mask)
    assert loss == pytest.approx(-.197)
    assert memopt_loss([[1.5, .5]], [[1, -1]], [[.2, .4]], mask, beta=0) == pytest.approx(-.2)
    with pytest.raises(ValueError):
        memopt_loss([[0, .5]], [[1, -1]], [[.2, .4]], mask)


def test_malformed_fields_and_undefined_whitening_are_rejected():
    with pytest.raises(ValueError):
        group_relative_advantage([[1]], np.array([[True]]), ["a"])
    with pytest.raises(ValueError):
        group_relative_advantage([[1, math.nan]], np.array([[True, False]]), ["a"])
    with pytest.raises(ValueError):
        firm_reward([[.5, .5]], [.5, .5], [.5], np.array([[True, True]]))
    with pytest.raises(ValueError):
        firm_reward([[1.1, .5]], [.5], [.5], np.array([[True, True]]))
    with pytest.raises(ValueError):
        group_relative_advantage([[1, 0]], [[1., 0.]], ["a"])


def test_finite_inputs_cannot_silently_overflow_statistics_or_loss():
    mask = np.array([[True, True]])
    with pytest.raises(ValueError, match="FIRM"):
        group_relative_advantage([[1e200, -1e200]], mask, ["g"])
    with pytest.raises(ValueError, match="intermediate"):
        memopt_loss([[1e308, 1]], [[-10, 1]], [[0, 0]], mask)
    with pytest.raises(ValueError):
        memopt_loss([[1, 1]], [[1, 1]], [[1e308, 1e308]], mask, beta=10)
    # Large finite padding is not a valid token and must not overflow moments.
    out = group_relative_advantage([[1, 1e200], [0, -1e200]], np.array([[True, False], [True, False]]), ["g", "g"])
    assert np.isfinite(out["advantages"]).all()


@pytest.fixture
def entries():
    return (MemoryEntry("early", "a", 0, 4, "public old event", (1., 0.)),
            MemoryEntry("boundary", "a", 4, 5, "at cutoff", (.6, .8)),
            MemoryEntry("future", "a", 5, 6, "later event", (1., 0.)),
            MemoryEntry("private", "b", 0, 4, "different subject", (1., 0.)))


def test_future_and_other_subject_filtered_before_rank(entries):
    visible = search_memory(entries, (1., 0.), subject="a", query_time=5, limit=2)
    assert [e.entry_id for e in visible] == ["early", "boundary"]
    assert [e.entry_id for e in search_memory(entries, (1., 0.), subject="a", query_time=5, limit=1)] == ["early"]
    assert [e.entry_id for e in eligible_memories(entries, subject="b", query_time=5)] == ["private"]


def test_fetch_clips_request_and_requires_full_segment_containment(entries):
    assert [e.entry_id for e in fetch_memory(entries, subject="a", query_time=5, interval=(4, 100))] == ["boundary"]
    assert fetch_memory(entries, subject="a", query_time=5, interval=(4.5, 5)) == ()
    assert fetch_memory(entries, subject="a", query_time=5, interval=(10, 100)) == ()


def test_vectors_and_explicit_access_contract(entries):
    with pytest.raises(ValueError):
        MemoryEntry("bad", "a", 0, 1, "text", (2., 0.))
    with pytest.raises(ValueError):
        search_memory(entries, (1.,), subject="a", query_time=5)
    with pytest.raises(ValueError):
        eligible_memories(entries + (entries[0],), subject="a", query_time=5)
    with pytest.raises(ValueError):
        fetch_memory(entries, subject="a", query_time=5, interval=(0, 5), limit=65)


def test_diagnostic_all_controls_and_no_cuda():
    for seed in (42, 43, 44):
        out = diagnostic(seed)
        assert out["diagnostic_only"] is True and out["evaluation_tier"] == "l1_mechanism"
        assert all(out["checks"].values())
    with pytest.raises(ValueError):
        diagnostic(42, "cuda")
