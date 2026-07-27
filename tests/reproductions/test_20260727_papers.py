from types import SimpleNamespace

import numpy as np

from auto_research.reproductions.gzip_sparse_attention.model import (
    GzipLMConfig,
    build_attention_mask,
    build_model,
    compression_ratios,
)
from auto_research.reproductions.pinequalizer.model import build_model as build_pinequalizer
from auto_research.reproductions.registry import get_adapter


def test_new_adapters_preserve_evidence_gate_and_metadata():
    pinterest = get_adapter("pinequalizer")
    gzip = get_adapter("gzip-sparse-attention")
    assert pinterest.paper.organization == "Pinterest"
    assert pinterest.paper.has_online_ab
    assert pinterest.paper.online_ab[0].lift_percent == 8.63
    assert gzip.paper.organization == "Pennsylvania State University"
    assert gzip.paper.code_url is None


def test_gzip_mask_is_input_adaptive_and_parameter_free():
    import torch

    repeated = torch.tensor([[65] * 32 + list(range(32))], dtype=torch.long)
    ratios = compression_ratios(repeated, block_size=32)[0]
    assert ratios[0] < ratios[1]
    mask = build_attention_mask(
        repeated, mode="gzip", heads=4, block_size=32, local_blocks=0
    )
    assert mask.shape == (1, 4, 64, 64)
    assert mask[0, 2, 63, 32]
    config = GzipLMConfig(
        dimensions=32, layers=1, heads=4, sequence_length=64, block_size=32
    )
    dense = build_model(config, "dense")
    gzip_model = build_model(config, "gzip")
    assert sum(p.numel() for p in dense.parameters()) == sum(
        p.numel() for p in gzip_model.parameters()
    )
    assert gzip_model(repeated).shape == (1, 64, 256)


def test_pinequalizer_executes_engagement_dropout_and_feature_crossing():
    import torch

    data = SimpleNamespace(
        users=3,
        items=5,
        genres=np.asarray(
            [[1, 0], [0, 1], [1, 1], [1, 0], [0, 1]], dtype=np.float32
        ),
        popularity=np.asarray([20, 10, 2, 1, 0], dtype=np.float32),
        fresh=np.asarray([False, False, True, True, True]),
        underexplored=np.asarray([False, False, False, True, True]),
        user_profiles=np.asarray([[1, 0], [0, 1], [1, 1]], dtype=np.float32),
    )
    baseline = build_pinequalizer(data, debiased=False, dimensions=16)
    proposed = build_pinequalizer(data, debiased=True, dimensions=16)
    users = torch.tensor([0, 1, 2])
    items = torch.tensor([0, 3, 4])
    assert baseline(users, items).shape == proposed(users, items).shape == (3,)
    assert proposed.catalog_scores(users).shape == (3, 5)
    assert proposed.debiased
