import math

import pytest

from auto_research.multimodal.gslm2 import (
    REQUIRES_GPU_VALIDATION,
    cross_stream_deduplicate,
    diagnostic,
    transition_log_score,
)


def test_cross_stream_union_does_not_deduplicate_independently():
    raw = [(1, 2), (1, 2), (1, 3), (4, 3), (4, 3), (1, 2)]
    got = cross_stream_deduplicate(raw)
    assert got.frame_indices == (0, 2, 3, 5)
    assert got.units == ((1, 2), (1, 3), (4, 3), (1, 2))
    assert cross_stream_deduplicate([[8], [8], [8]]).frame_indices == (0,)


def test_stream_macro_average_ignores_persistence_not_first_token():
    units = [(2, 5), (2, 6), (2, 7), (2, 6)]
    logp = [(-4, -1), (-100, -2), (-50, -3), (-40, -4)]
    result = transition_log_score(units, logp)
    assert result.per_stream_transitions == (1, 4)
    assert result.per_stream_log_probability == (-4, -2.5)
    assert result.mean_log_probability == -3.25
    assert result.mean_log_probability != (-4 - 1 - 2 - 3 - 4) / 5
    assert result == transition_log_score(units, [(-4, -1), (0, -2), (0, -3), (0, -4)])


def test_one_retained_frame_and_no_overflow_for_finite_float_values():
    result = transition_log_score([(0, 1)], [(-1e308, -1e308)])
    assert result.per_stream_transitions == (1, 1)
    assert result.mean_log_probability == -1e308
    assert transition_log_score([(0,), (1,), (2,)], [(-1e308,)] * 3).mean_log_probability == -1e308


@pytest.mark.parametrize("frames", [[], [[]], [(1, 2), (3,)], [(-1,)], [(1.0,)], [(True,)]])
def test_dedup_validates_aligned_unit_shape_and_ids(frames):
    with pytest.raises(ValueError):
        cross_stream_deduplicate(frames)


@pytest.mark.parametrize(
    ("units", "scores"),
    [
        ([(1,), (1,)], [(-1,), (-2,)]),
        ([(1, 2)], [(-1,)]),
        ([(1,)], []),
        ([(1,)], [(1.0,)]),
        ([(1,)], [(math.inf,)]),
        ([(1,)], [(-math.inf,)]),
        ([(1,)], [(math.nan,)]),
        ([(1,)], [(False,)]),
    ],
)
def test_score_rejects_unaligned_or_invalid_probability_inputs(units, scores):
    with pytest.raises(ValueError):
        transition_log_score(units, scores)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_is_bounded_reproducible_and_cpu_only(seed):
    result = diagnostic(seed, "cpu")
    assert not REQUIRES_GPU_VALIDATION
    assert result == diagnostic(seed)
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(result["checks"].values())
    assert result["metrics"]["raw_frames"] > result["metrics"]["retained_frames"]
    with pytest.raises(ValueError, match="CPU only"):
        diagnostic(seed, "cuda")
