"""FLVM core fidelity, masking and public split controls."""

from __future__ import annotations

import csv

import torch

from auto_research.reproductions.flvm.experiment import average_precision, load_data
from auto_research.reproductions.flvm.model import FLVM, ROUTES


def test_routed_latent_and_stopped_baseline_gradient():
    torch.manual_seed(1)
    model = FLVM(users=4, items=5)
    users = torch.tensor([0, 1, 2, 3])
    items = torch.tensor([1, 2, 3, 4])
    confounders = torch.randn(4, 3)
    labels = torch.randint(0, 2, (4, 4)).float()
    mask = torch.ones_like(labels)
    mask[0, 2] = 0
    logits, baseline, mean, log_variance = model(users, items, confounders)
    main_only = (logits * mask).sum()
    main_only.backward(retain_graph=True)
    assert all(parameter.grad is None for parameter in model.baseline.parameters())
    model.zero_grad(set_to_none=True)
    loss = FLVM.loss(logits, baseline, labels, mask, mean, log_variance)
    loss.backward()
    assert any(parameter.grad is not None for parameter in model.baseline.parameters())
    assert any(parameter.grad is not None for parameter in model.encoder.parameters())
    assert ROUTES.shape == (4, 3)
    assert torch.equal(ROUTES[2], ROUTES[3])
    assert torch.isfinite(FLVM.value_score(mean)).all()


def test_public_split_uses_only_pre_feedback_inputs(tmp_path, monkeypatch):
    directory = tmp_path / "kuairand-pure" / "data"
    directory.mkdir(parents=True)
    path = directory / "log_standard_4_22_to_5_08_pure.csv"
    fields = ("user_id", "video_id", "hourmin", "duration_ms", "time_ms",
              "long_view", "is_click", "is_like", "is_hate")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for index in range(100):
            writer.writerow({"user_id": index % 4, "video_id": index % 6,
                             "hourmin": 1600, "duration_ms": 10000,
                             "time_ms": 1000 - index,
                             "long_view": index % 2, "is_click": index % 2,
                             "is_like": int(index % 3 == 0),
                             "is_hate": int(index % 7 == 0)})
    monkeypatch.setattr(
        "auto_research.reproductions.flvm.experiment.kuairand_pure_files",
        lambda _: directory,
    )
    data = load_data(tmp_path)
    assert (len(data.train), len(data.validation), len(data.test)) == (70, 15, 15)
    assert data.train.confounders.shape == (70, 3)
    assert data.test.labels[0, 0] == 0  # index 14 after chronological reversal
    assert torch.equal(data.test.mask, torch.ones_like(data.test.mask))


def test_average_precision_handles_unobserved_positives():
    import numpy as np

    assert average_precision(np.array([0, 0]), np.array([0.2, 0.5])) is None
    assert average_precision(np.array([1, 0]), np.array([0.7, 0.1])) == 1.0
