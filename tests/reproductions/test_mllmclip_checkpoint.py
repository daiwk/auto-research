from __future__ import annotations

from pathlib import Path

import pytest

from auto_research.reproductions.mllmclip.checkpoint import (
    CheckpointConfig,
    fit_projection,
)


def test_checkpoint_projection_optimizes_real_cka_objective():
    torch = pytest.importorskip("torch")
    generator = torch.Generator().manual_seed(42)
    student = torch.randn(48, 8, generator=generator)
    mapping = torch.randn(8, 12, generator=generator)
    teacher = student @ mapping + 0.01 * torch.randn(48, 12, generator=generator)
    result = fit_projection(
        student[:32], teacher[:32], student[32:], teacher[32:],
        torch.arange(32) % 4, torch.arange(16) % 4,
        CheckpointConfig(Path("unused"), steps=80, batch_size=16, learning_rate=1e-2),
        torch, torch.device("cpu"),
    )
    assert result["final_loss"] < result["initial_loss"]
    assert result["method"]["linear_cka"] > result["baseline"]["linear_cka"]
