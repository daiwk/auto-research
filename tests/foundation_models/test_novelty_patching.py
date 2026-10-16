import numpy as np
import pytest

from auto_research.foundation_models.novelty_patching import (
    calibrate_threshold, fit_novelty_table, novelty_targets,
)


def brute_force(data, window=128, cap=16):
    return np.array([-max([0] + [length for start in range(max(0, t-window), t)
                                for length in range(1, min(cap, len(data)-t)+1)
                                if data[start:start+length] == data[t:t+length]])
                     for t in range(len(data))])


@pytest.mark.parametrize("data", [b"", b"x", b"aaaaaa", b"abcabcXabcabcY", bytes(range(255))])
def test_training_target_matches_independent_lz_reference(data):
    np.testing.assert_array_equal(novelty_targets(data), brute_force(data))


def test_overlap_cap_and_window_are_not_heuristic_novelty():
    assert novelty_targets(b"a" * 40)[1] == -16  # overlapping LZ copy
    assert novelty_targets(b"a" + b"b" * 128 + b"a")[-1] == 0
    np.testing.assert_array_equal(novelty_targets(b"abcabcabc", window=2), np.zeros(9))
    rng = np.random.default_rng(42)
    for _ in range(12):
        data = bytes(rng.integers(0, 5, 100, dtype=np.uint8))
        np.testing.assert_array_equal(novelty_targets(data, window=17, cap=8),
                                      brute_force(data, window=17, cap=8))


def test_exact_conditional_means_and_two_stage_frequency_backoff():
    documents = [b"abcabcaZ", b"abcaQ", b"xYabc"]
    table = fit_novelty_table(documents, min_count=2)
    pairs, singles, all_labels = {}, {}, []
    for data in documents:
        targets = brute_force(data)
        all_labels.extend(targets)
        for t in range(1, len(data)):
            singles.setdefault(data[t-1], []).append(targets[t])
            if t >= 2:
                pairs.setdefault(tuple(data[t-2:t]), []).append(targets[t])
    assert table.global_mean == np.mean(all_labels)
    for last in range(256):
        expected1 = np.mean(singles[last]) if len(singles.get(last, [])) >= 2 else table.global_mean
        assert table.next_score(bytes([last])) == expected1
        for first in (0, 97, 98, 120):
            labels = pairs.get((first, last), [])
            expected2 = np.mean(labels) if len(labels) >= 2 else expected1
            assert table.next_score(bytes([first, last])) == expected2
    assert table.two_byte_counts[ord("Z") * 256 + ord("a")] == 0  # no cross-document pair


def test_online_boundaries_are_prefix_causal_even_when_future_labels_change():
    table = fit_novelty_table(b"abc abc abc x abc y " * 40)
    prefix = b"unseen prefix abc "
    one, two = prefix + b"abcxyz", prefix + b"zzzzzz"
    np.testing.assert_array_equal(table.scores(one)[:len(prefix)+1],
                                  table.scores(two)[:len(prefix)+1])
    for t, score in enumerate(table.scores(one)):
        assert score == table.next_score(one[:t])
    assert novelty_targets(b"aaba")[1] != novelty_targets(b"abba")[1]


def test_threshold_is_train_only_closest_attainable_and_ties_are_reported():
    train = [b"abc abc def abc " * 50, b"123 123 456 " * 10]
    table = fit_novelty_table(train)
    calibration = calibrate_threshold(table, train, .1)
    scores = np.concatenate([table.scores(doc) for doc in train])
    observed = float((scores > calibration.threshold).mean())
    assert observed == pytest.approx(calibration.achieved_rate)
    all_rates = [1.] + [float((scores > threshold).mean()) for threshold in np.unique(scores)]
    assert abs(observed - .1) == pytest.approx(min(abs(rate - .1) for rate in all_rates))
    assert calibration.training_fingerprint == table.training_fingerprint
    for target in (0., 1.):
        result = calibrate_threshold(table, train, target)
        assert result.achieved_rate == target
    constant = fit_novelty_table(b"abc", min_count=20)
    assert calibrate_threshold(constant, b"abc", .1).achieved_rate == 0.


@pytest.mark.parametrize("kwargs", [{"target_rate": -1}, {"target_rate": float("nan")}])
def test_invalid_calibration_rejected(kwargs):
    with pytest.raises(ValueError):
        calibrate_threshold(fit_novelty_table(b"abc"), b"abc", **kwargs)
