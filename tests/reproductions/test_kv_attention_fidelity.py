"""Regression checks for the checkpoint probe, independent of GPU access."""

import pytest
import torch

from auto_research.reproductions.beaconkv.model import farthest_point_beacons
from auto_research.reproductions.gpu_checkpoint_20260907 import _attend, run


def test_identical_beacons_do_not_repeat_indices():
    indices = farthest_point_beacons(torch.ones(12, 4), 8)
    assert len(indices.unique()) == 8


def test_attention_keeps_gqa_queries_separate():
    keys = torch.tensor([[3.0, 0.0], [-3.0, 0.0]])
    values = torch.eye(2)
    queries = torch.tensor([[2.0, 0.0], [-2.0, 0.0]])
    indices = torch.arange(2)
    outputs = torch.stack([_attend(q, keys, values, indices, torch) for q in queries])
    expected = torch.nn.functional.scaled_dot_product_attention(
        queries[:, None, :], keys.expand(2, -1, -1), values.expand(2, -1, -1)
    )[:, 0, :]
    torch.testing.assert_close(outputs, expected)
    averaged = _attend(queries.mean(0), keys, values, indices, torch)
    assert not torch.allclose(outputs[0], averaged)


def test_invalid_retention_fails_before_loading_checkpoint(tmp_path):
    with pytest.raises(ValueError, match="retained_tokens"):
        run("beaconkv", output=tmp_path / "result.json", model_id="unused",
            revision="unused", sequence_length=8, retained_tokens=9, seed=42,
            local_files_only=True)
