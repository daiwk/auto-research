from auto_research.agent_research.toolsearcher_credit import SearchTrace, trajectory_credit


def test_credit_only_first_discovery_and_no_selection_before_complete_search():
    target = frozenset({"a", "b"})
    traces = (
        SearchTrace((frozenset({"a"}), frozenset({"a"}), frozenset({"b"})), target),
        SearchTrace((frozenset({"a"}), frozenset({"x"})), target),
        SearchTrace((frozenset({"x"}),), frozenset()),
    )
    credits = trajectory_credit(traces, target)
    assert credits[0].first_discoveries == (
        frozenset({"a"}), frozenset(), frozenset({"b"}),
    )
    assert credits[0].search_advantages[1] == 0
    assert credits[0].search_advantages[2] > 0
    assert credits[1].selection_advantage == 0
    assert credits[2].selection_advantage == 0
    assert credits[0].selection_advantage > 0


def test_mastered_target_has_no_search_gradient():
    traces = (
        SearchTrace((frozenset({"a"}),), frozenset({"a"})),
        SearchTrace((frozenset({"a"}),), frozenset()),
    )
    credits = trajectory_credit(traces, frozenset({"a"}))
    assert all(row.search_advantages == (0.0,) for row in credits)
    assert credits[0].selection_advantage > 0
    assert credits[1].selection_advantage < 0


def test_invalid_group_rejected():
    import pytest

    with pytest.raises(ValueError):
        trajectory_credit((SearchTrace((frozenset({"a"}),), frozenset()),), frozenset({"a"}))
