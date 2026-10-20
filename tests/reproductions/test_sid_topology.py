import math

import pytest

from auto_research.reproductions.sid_topology import (
    Item, insert_preserving, ranked_assignment, remapped_fraction, resolve_paths,
)


def row(key, value, prefix=(1, 2)):
    return Item(key, prefix, 0., 0., value, 0.)


def test_exact_business_value_and_hybrid_buckets():
    assert Item("x", (0, 0), 10, 5, 2, 20).value == (1 + 1.5 + 2) / 30
    values = [row(str(i), 10-i) for i in range(6)]
    assignment = ranked_assignment(values, head=2, tail_buckets=2, tail_group_size=2)
    assert [assignment[str(i)][2] for i in range(6)] == [1, 2, 3, 3, 4, 4]


def test_head_collision_and_missing_old_item_are_preserved_without_mutation():
    old = {"a": (1, 2, 1), "b": (1, 2, 2), "absent": (3, 4, 7)}
    new = insert_preserving(old, [row("a", 2), row("b", 1), row("new", 9)],
                            head=2, tail_buckets=1, tail_group_size=2)
    assert new["new"] == old["a"] and remapped_fraction(old, new) == 0
    assert new["absent"] == old["absent"] and len(old) == 3
    assert resolve_paths(new, [(1, 2, 1), (1, 2, 1)]) == ("a", "new")


def test_full_remap_negative_control_breaks_learned_path():
    items = [row("a", 2), row("b", 1)]
    old = ranked_assignment(items, head=2, tail_buckets=1, tail_group_size=2)
    current = ranked_assignment([*items, row("new", 9)], head=2, tail_buckets=1, tail_group_size=2)
    assert remapped_fraction(old, current) == 1
    assert "a" not in resolve_paths(current, [old["a"]])


def test_insertion_permutation_independence_and_ties():
    items = [row("b", 2), row("a", 2), row("c", 1)]
    a = ranked_assignment(items, head=2, tail_buckets=1, tail_group_size=2)
    b = ranked_assignment(items[::-1], head=2, tail_buckets=1, tail_group_size=2)
    assert a == b and a["a"] == (1, 2, 1)


def test_invalid_or_exhausted_requests_fail_closed():
    with pytest.raises(ValueError):
        ranked_assignment([row("a", 1), row("a", 2)], tail_group_size=1)
    with pytest.raises(ValueError):
        ranked_assignment([row(str(i), i) for i in range(4)], head=1, tail_buckets=1, tail_group_size=2)
    with pytest.raises(ValueError):
        insert_preserving({"a": (1, 2, 1)}, [row("a", 1, (2, 3))], tail_group_size=1)
    with pytest.raises(ValueError):
        remapped_fraction({}, {})
    for count in (-1, math.nan, math.inf, True):
        with pytest.raises(ValueError):
            row("a", count)
