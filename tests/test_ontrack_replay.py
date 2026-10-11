import json

import pytest

from auto_research.agent_research.ontrack_replay import auc, instance_id, paired_auc_interval, parse_trace, partition_instances


def test_instance_partition_is_grouped_reproducible_and_nonoverlapping():
    ids = [f"django__django-{i}" for i in range(20)] * 2
    parts = partition_instances(ids, calibration=4, reference_pool=3)
    assert parts == partition_instances(ids, calibration=4, reference_pool=3)
    assert sum(len(x) for x in parts.values()) == 20
    assert not set(parts["calibration"]) & set(parts["evaluation"])
    assert instance_id("folder/django__django-123.traj") == "django__django-123"


def test_parser_never_uses_resolution_exit_status_submission_or_executes_commands():
    log = [{"action": "open src/model.py", "thought": "inspect file", "observation": "File: src/model.py", "state": "{}"},
           {"action": "edit 1:2\\npass", "observation": "File updated", "state": json.dumps({"open_file": "src/model.py"})}]
    row = {"trajectory": json.dumps(log), "resolved": True, "exit_status": "submitted", "submission": "GOLD"}
    first = parse_trace(row)
    row.update(resolved=False, exit_status="exit_cost", submission="DIFFERENT_GOLD")
    assert parse_trace(row) == first
    assert first[0].produces == ("src/model.py",)
    assert first[1].consumes == ("src/model.py",)
    assert all("GOLD" not in repr(x) for x in first)


def test_auc_orientation_ties_and_bootstrap_recompute_both_on_same_instances():
    assert auc([1, 0], [1, 0]) == 1
    assert auc([1, 0], [0, 0]) == .5
    assert auc([1, 1], [0, 1]) is None
    assert paired_auc_interval([1, 0, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]) == [0., 0.]
    with pytest.raises(ValueError):
        auc([1, 0], [float("nan"), 0])
