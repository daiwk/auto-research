from auto_research.reproductions.lum.model import _condition


def test_lum_condition_precedes_item_and_has_three_levels():
    assert [_condition(value) for value in (1, 3, 5)] == [0, 1, 2]


def test_group_query_returns_one_isolated_vector_per_condition():
    import pytest
    torch = pytest.importorskip("torch")
    import numpy as np
    from auto_research.reproductions.lum.model import LUMConfig, LUMData, build_lum

    data = LUMData((), (), (), np.eye(4, dtype=np.float32), users=1, items=4)
    config = LUMConfig(dimensions=8, heads=2, layers=1, history_length=2)
    model = build_lum(data, config)
    output = model.query(torch.tensor([[0, 1]]), torch.tensor([[2, 1]]), torch.tensor([[0, 1, 2]]))
    assert output.shape == (1, 3, 8)
    assert torch.isfinite(output).all()
