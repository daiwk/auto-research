from __future__ import annotations

from pathlib import Path

import torch

from auto_research.reproductions.light_heads import experiment
from auto_research.reproductions.light_heads.model import HeadSpec, LightHeadRanker


def test_light_head_stop_gradient_isolates_shared_tower_and_main_head():
    model = LightHeadRanker(4, 5, 2, dimensions=8)
    model.inject(HeadSpec("new_task"))
    users = torch.tensor([0, 1, 2])
    items = torch.tensor([2, 3, 4])
    genres = torch.ones((3, 2))
    model(users, items, genres)["new_task"].sum().backward()
    assert model.user.weight.grad is None
    assert model.main.weight.grad is None
    assert model.light_heads["new_task"][0].weight.grad is not None

    model.zero_grad(set_to_none=True)
    model(users, items, genres, stop_gradient=False)["new_task"].sum().backward()
    assert model.user.weight.grad is not None
    assert model.main.weight.grad is None


def test_light_head_reset_preserves_backbone_and_main():
    model = LightHeadRanker(4, 5, 2, dimensions=8)
    model.inject(HeadSpec("new_task"))
    model.inject(HeadSpec("persistent", reset_each_run=False))
    before_backbone = model.user.weight.detach().clone()
    before_main = model.main.weight.detach().clone()
    before_head = model.light_heads["new_task"][0].weight.detach().clone()
    before_persistent = model.light_heads["persistent"][0].weight.detach().clone()
    torch.manual_seed(123)
    model.reset_run()
    assert torch.equal(model.user.weight, before_backbone)
    assert torch.equal(model.main.weight, before_main)
    assert not torch.equal(model.light_heads["new_task"][0].weight, before_head)
    assert torch.equal(model.light_heads["persistent"][0].weight, before_persistent)


def test_light_heads_experiment_runs_all_ablations_on_one_split(monkeypatch):
    def tiny(_root):
        rows = 80
        users = torch.arange(rows) % 4
        items = torch.arange(rows) % 5
        genres = torch.nn.functional.one_hot(items % 2, 2).float()
        labels = ((users + items) % 3 > 0).float()
        high = ((users + items) % 4 == 0).float()
        batch = (users, items, genres, labels, high)
        return {"train": batch, "validation": batch, "test": batch}, 4, 5, 2

    monkeypatch.setattr(experiment, "_prepare", tiny)
    result = experiment.reproduce(Path("unused"), 42, base_steps=3, head_steps=4)
    assert set(result["variants"]) == {"light_head", "no_reset", "no_stop_gradient"}
    assert result["setup"]["same_budget_and_split"] is True
    for variant in result["variants"].values():
        assert 0 <= variant["test"]["main_auc"] <= 1
