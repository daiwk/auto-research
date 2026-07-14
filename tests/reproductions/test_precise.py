import numpy as np
import pytest


def test_precise_fusion_and_training_paths_have_expected_shapes():
    pytest.importorskip("torch")
    from auto_research.reproductions.precise.model import PreciseConfig, build_precise

    config = PreciseConfig(dimensions=8, heads=2, layers=1, history_length=4, experts=3, active_experts=2)
    tokens = np.random.default_rng(1).normal(size=(7, 3, 12)).astype(np.float32)
    mask = np.ones((7, 3), dtype=np.bool_)
    model = build_precise(7, tokens, mask, config)

    import torch
    items = torch.tensor([[1, 2, 3, 4], [2, 3, 4, 5]])
    padding = torch.zeros_like(items, dtype=torch.bool)
    assert model.fusion(items).shape == (2, 4, 16)
    assert model.encode(items, padding, targeted=False).shape == (2, 4, 16)
    assert model.encode(items, padding, targeted=True).shape == (2, 16)


def test_precise_catalog_has_quantified_online_ab():
    from auto_research.reproductions.registry import get_adapter

    adapter = get_adapter("precise")
    assert adapter.paper.has_online_ab
    assert adapter.fidelity.value == "full_pipeline"


def test_precise_public_split_has_no_unseen_test_items(tmp_path, monkeypatch):
    from auto_research.reproductions.precise import data as module

    rows = []
    for user in range(2):
        for timestamp, item in enumerate((1, 2, 3, 4)):
            rows.append((user, item, 5.0, timestamp))
    # This last target is unique to user 0 and must be removed by the global
    # train-catalog rule; user 1's final target is seen in prior training.
    rows.extend(((0, 99, 5.0, 9), (1, 3, 5.0, 9)))
    monkeypatch.setattr(module, "movielens_1m", lambda _: rows)
    movie_dir = tmp_path / "ml-1m"
    movie_dir.mkdir()
    (movie_dir / "movies.dat").write_text("\n".join(f"{item}::M{item}::Drama" for item in (1, 2, 3, 4, 99)), encoding="latin-1")

    split = module.load_precise_data(tmp_path, 2)
    assert len(split.test_targets) == 1
    assert all(split.train_frequency[target] > 0 for target in split.test_targets)
