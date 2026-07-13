from auto_research.spaces import candidate_params


def test_candidate_params_is_reproducible_and_bounded():
    space = {"a": [1, 2], "b": ["x", "y"]}
    first = list(candidate_params(space, 3, seed=42))
    second = list(candidate_params(space, 3, seed=42))
    assert first == second
    assert len(first) == 3
    assert len({tuple(sorted(item.items())) for item in first}) == 3
