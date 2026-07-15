from pathlib import Path

import numpy as np
import pytest

from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.univa.data import commercial_sid, path_bid_dispersion


def test_adapter_has_quantified_wechat_ab():
    adapter = get_adapter("univa")
    assert adapter.paper.organization == "Tencent / WeChat Channels"
    assert {entry.lift_percent for entry in adapter.paper.online_ab} == {1.5, 1.42}


def test_classify_then_equal_frequency_respects_budget():
    attributes = np.asarray([[0, 0, 0]] * 8 + [[1, 0, 0]] * 4)
    bids = np.arange(12, dtype=float)
    tokens, stats = commercial_sid(attributes, bids, budget=6)
    assert stats["vocabulary_size"] == 6
    assert len(set(tokens[:8])) == 4
    assert len(set(tokens[8:])) == 2
    assert stats["weighted_entropy"] > 0


def test_commercial_suffix_reduces_within_path_bid_dispersion():
    bids = np.asarray([1.0, 10.0, 2.0, 9.0])
    semantic = np.asarray([[0, 0, 0]] * 4)
    commercial = np.asarray([[0, 0, 0], [0, 0, 1], [0, 0, 0], [0, 0, 1]])
    assert path_bid_dispersion(commercial, bids)["mean_std"] < path_bid_dispersion(semantic, bids)["mean_std"]


def test_dual_head_decoder_shapes_when_torch_available():
    torch = pytest.importorskip("torch")
    from auto_research.reproductions.univa.model import UniVAConfig, build_model

    config = UniVAConfig(dimensions=48, steps=1)
    model = build_model(20, (8, 8, 6), config)
    histories = torch.randint(0, 20, (2, 20))
    codes = torch.stack((torch.randint(0, 8, (2,)), torch.randint(0, 8, (2,)), torch.randint(0, 6, (2,))), 1)
    generation, value = model(histories, codes)
    assert [tuple(tensor.shape) for tensor in generation] == [(2, 8), (2, 8), (2, 6)]
    assert [tuple(tensor.shape) for tensor in value] == [(2, 8), (2, 8), (2, 6)]
