"""GRAFT credit on an evaluator-isolated public tool environment."""

import json
from pathlib import Path

from auto_research.agent_research.graft_public import run_graft_tool_policy
from scripts.migrate_metric_schema_v2 import migrate_payload


def test_graft_public_policy_is_deterministic_and_preserves_split_contract():
    arguments = dict(seed=42, train_episodes=12, validation_episodes=12,
                     test_episodes=12, epochs=2)
    first = run_graft_tool_policy(**arguments)
    assert first == run_graft_tool_policy(**arguments)
    assert first["protocol"]["oracle_fields_exposed"] is False
    assert first["protocol"]["test_used_for_selection"] is False
    assert first["protocol"]["diagnostic_only"] is True
    for method in ("outcome", "graph_td"):
        result = first["methods"][method]
        assert len(result["history"]) == 2
        assert result["weight_l2_after_training"] > 0
        for split in ("validation", "test"):
            assert 0 <= result[split]["joint_success"] <= 1
            assert 0 <= result[split]["irreversible_error_rate"] <= 1


def test_graft_public_rejects_insufficient_or_invalid_budget():
    import pytest

    with pytest.raises(ValueError):
        run_graft_tool_policy(seed=42, train_episodes=3)
    with pytest.raises(ValueError):
        run_graft_tool_policy(seed=42, learning_rate=0)


def test_committed_graft_metrics_satisfy_schema_v2_without_migration():
    root = Path(__file__).resolve().parents[1]
    path = root / "docs/experiments/metrics/graft-public-toolroute-l21.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert migrate_payload(path, payload) == payload
