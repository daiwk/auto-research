"""SSR extraction, exact full-scan ranking, failure accounting and no-gold API."""
from collections import Counter
import inspect
import math

import pytest

from auto_research.agent_research.structural_signal_retriever import (
    AgentCard, SelectionOutcome, StructuralSignalIndex, outcome_counts,
    structural_signals, validate_orchestrator_selection,
)


def test_extraction_is_binary_with_deterministic_frequency_overflow():
    assert structural_signals("THE x A1 cat cat dog") == {
        "a1", "cat", "dog", "a1 cat", "cat cat", "cat dog",
    }
    assert structural_signals("bb cc aa aa", limit=2) == {"aa", "bb"}
    assert structural_signals("bb aa", limit=3) == {"aa", "bb", "bb aa"}
    assert structural_signals("the is a x!") == frozenset()
    assert structural_signals("zz " * 100) == {"zz", "zz zz"}
    assert len(structural_signals(" ".join(f"word{i:02d}" for i in range(100)))) == 64


def test_inverted_index_equals_independent_exhaustive_scoring():
    cards = [AgentCard("z", "tax policy filing"), AgentCard("b", "tax policy"),
             AgentCard("a", "tax policy"), AgentCard("c", "image classifier")]
    index = StructuralSignalIndex(cards)
    card_signals = {card.identifier: structural_signals(card.capability_text()) for card in cards}
    counts = Counter(signal for signals in card_signals.values() for signal in signals)
    for text in ["tax policy", "filing", "image tax", "unmatchedxyz", ""]:
        q = structural_signals(text)
        expected = []
        for identifier, signals in card_signals.items():
            common = sorted(q & signals)
            if common:
                score = math.fsum(math.log((len(cards) + 1) / (counts[s] + 1)) + 1 for s in common)
                expected.append((identifier, score, tuple(common)))
        expected.sort(key=lambda row: (-row[1], -len(row[2]), row[0]))
        actual = index.query(text, top_k=99)
        assert [(hit.identifier, hit.score, hit.matched_signals) for hit in actual] == expected
        assert len(actual) <= len(expected)  # no zero-scoring padding
    assert [hit.identifier for hit in index.query("tax policy")] == ["a", "b", "z"]
    # Repeating a term cannot repeatedly contribute IDF to its score.
    one = index.query("filing")[0]
    repeated = index.query("filing " * 40)[0]
    assert one.score == repeated.score


def test_fields_no_gold_and_selection_failures_are_not_dropped():
    card = AgentCard("safe", skills=("database",), tags=("sql",), tools=("query engine",))
    index = StructuralSignalIndex([card])
    pool = index.query("database sql")
    counts = outcome_counts([
        validate_orchestrator_selection(pool, 1), validate_orchestrator_selection(pool, 0),
        validate_orchestrator_selection(pool, 1, api_failed=True),
        validate_orchestrator_selection(index.query("unknown")),
    ])
    assert counts == {"total_attempts": 4, "selected": 1, "empty_pool": 1, "api_failure": 1, "invalid_index": 1}
    assert validate_orchestrator_selection(pool, True).status == "invalid_index"
    assert validate_orchestrator_selection(pool, "1").status == "invalid_index"
    assert validate_orchestrator_selection([]).selected_identifier is None
    assert "answer" not in inspect.signature(StructuralSignalIndex.query).parameters
    assert "gold" not in inspect.signature(StructuralSignalIndex).parameters
    with pytest.raises(ValueError):
        outcome_counts([SelectionOutcome("untracked_failure")])


@pytest.mark.parametrize("limit", [0, 65, True, 1.5])
def test_invalid_signal_limits_rejected_even_empty_registry(limit):
    with pytest.raises(ValueError):
        StructuralSignalIndex([], limit=limit)


def test_duplicate_identifiers_and_invalid_topk():
    with pytest.raises(ValueError):
        StructuralSignalIndex([AgentCard("a", "one"), AgentCard("a", "two")])
    index = StructuralSignalIndex([])
    assert index.query("any query") == []
    for invalid in (0, -1, True, 1.5):
        with pytest.raises(ValueError):
            index.query("query", top_k=invalid)
