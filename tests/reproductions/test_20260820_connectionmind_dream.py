from pathlib import Path

import numpy as np
import pytest

from auto_research.reproductions.connectionmind.model import (
    PathPolicy,
    typed_path_features,
)
from auto_research.reproductions.dream.model import (
    StrategyBundle,
    StrategyMemory,
    compile_strategy,
    infer_intent,
)


class _Graph:
    train = ((0, 1, 2), (1, 3, 4))
    friends = ((1,), (0,))
    transition = np.eye(5)
    item_tags = np.eye(5)
    popularity = np.linspace(0.1, 1.0, 5)
    item_count = 5


class _Sequences:
    train = ((0, 1, 2),)
    validation = (3,)
    test = (4,)


class _Industrial:
    sequences = _Sequences()
    transition = np.eye(5)
    cosine = np.eye(5)
    popularity = np.linspace(0.1, 1.0, 5)
    domains = np.asarray((0, 0, 1, 1, 2))
    item_count = 5


def test_connectionmind_scores_every_typed_path_and_terminal_item():
    features = typed_path_features(_Graph(), 0, (0, 1, 2))
    policy = PathPolicy.initialize()
    assert features.shape == (5, 4)
    assert policy.action_logits(features).shape == (5, 4)
    assert policy.item_scores(features).shape == (5,)


def test_dream_compiler_is_guarded_and_preserves_full_catalog():
    data = _Industrial()
    intent = infer_intent(data, (0, 1, 2))
    scores, trace = compile_strategy(
        data, (0, 1, 2), intent,
        StrategyBundle(relevance=1, affinity=2, novelty=1, scatter=1),
    )
    assert scores.shape == (data.item_count,)
    assert np.isfinite(scores).all()
    assert trace["schema_valid"] is True
    with pytest.raises(ValueError):
        compile_strategy(data, (0, 1, 2), intent, StrategyBundle(relevance=3))


def test_dream_memory_only_deposits_positive_conclusions():
    memory = StrategyMemory()
    positive, negative = StrategyBundle(affinity=1), StrategyBundle(novelty=1)
    memory.deposit("global", positive, 0.01)
    memory.deposit("global", negative, -0.01)
    assert memory.retrieve("global") == positive
    assert (memory.accepted, memory.rejected) == (1, 1)


def test_new_adapters_run_on_cached_public_data():
    from auto_research.reproductions.registry import get_adapter

    root = Path("data")
    for key in ("connectionmind", "dream"):
        adapter = get_adapter(key)
        assert adapter.device_capabilities == ("cpu",)
        result = adapter.run(root, 42)
        assert result["method"]
        assert result["baseline"]
        assert all(result["stages"][stage] for stage in (
            ("typed_heterogeneous_graph", "shortest_path_sft", "rule_reward_grpo")
            if key == "connectionmind"
            else ("l0_l1_l2_intent_engine", "m3_schema_guarded_compiler", "offline_online_reward_dual_loop")
        ))
