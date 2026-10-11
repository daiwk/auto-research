import numpy as np
import pytest

from auto_research.system_one.option_channel import (
    GuardItem, attack_metrics, guard_items, paired_asr_interval, score_items,
)


def test_option_rename_keeps_state_and_bound_definitions_identical():
    items = guard_items("exfil", count=4)
    observed = []

    def gate(state, instructions, criteria):
        assert "prohibited" not in state and "gold" not in state
        observed.append((state, tuple(criteria.values())))
        return dict(zip(criteria, (.5, .5)))

    score_items(gate, "exfil", items)
    score_items(gate, "exfil", items, allow_label="deny")
    assert observed[:4] == observed[4:]
    with pytest.raises(ValueError):
        score_items(gate, "exfil", items, allow_label="block")


def test_conditional_asr_does_not_count_already_wrong_decisions():
    items = (GuardItem("a", True), GuardItem("b", True), GuardItem("c", False))
    result = attack_metrics(items, np.array([.9, .1, .1]), np.array([.1, .1, .9]))
    assert result["originally_correct_blocks"] == 1 and result["asr_open"] == 1
    assert result["attack_fail_closed"] == 1
    undefined = attack_metrics(items, np.array([.1, .1, .1]), np.array([.1, .1, .1]))
    assert undefined["asr_open"] is None
    assert paired_asr_interval(items, [.1, .1, .1], [.1, .1, .1]) is None


def test_balanced_protocol_is_seeded_and_holdout_differs():
    rows = guard_items("exfil_secret", count=24, seed=42)
    assert sum(x.prohibited for x in rows) == 12
    assert rows == guard_items("exfil_secret", count=24, seed=42)
    assert rows != guard_items("exfil_secret", count=24, seed=43)
