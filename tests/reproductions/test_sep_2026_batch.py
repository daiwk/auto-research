from pathlib import Path

import torch

from auto_research.evolution.compatibility import operator_registry
from auto_research.reproductions.lngram_v2.model import LngramV2
from auto_research.reproductions.random_attention.model import random_retained_indices
from auto_research.reproductions.registry import get_adapter


ROOT = Path(__file__).resolve().parents[2]


def test_four_sep_papers_have_complete_metadata_and_evolve_operators():
    expected = {
        "coral": ("2609.02730", False),
        "recevolve": ("2609.01622", False),
        "random-attention": ("2609.03430", True),
        "lngram-v2": ("2609.03426", True),
    }
    operators = operator_registry()
    for key, (paper_id, gpu) in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.arxiv_id == paper_id
        assert adapter.paper.published.count("-") == 2
        assert adapter.paper.organization
        assert adapter.requires_gpu_validation is gpu
        assert all(operator in operators for operator in adapter.evolve_operators)
        readme = ROOT / "docs" / "reproductions" / f"{paper_id}-{key}" / "README.md"
        text = readme.read_text(encoding="utf-8")
        for label in ("论文链接", "公司/机构", "首次公开日期", "原文开源代码", "Adapter", "本地复现代码"):
            assert label in text


def test_random_attention_protects_prompt_and_samples_heads_independently():
    retained = random_retained_indices(64, 24, prompt_tokens=8, heads=4, seed=42)
    assert retained.shape == (4, 24)
    assert torch.equal(retained[:, :8], torch.arange(8).expand(4, -1))
    assert torch.unique(retained, dim=0).shape[0] == 4


def test_lngram_v2_hard_forward_has_surrogate_route_gradient():
    hidden = torch.randn(2, 16, 64, requires_grad=True)
    model = LngramV2(width=64, routes=8, bits=3, memory_dim=16, heads=4)
    output, diagnostics = model(hidden, return_diagnostics=True)
    output.square().mean().backward()
    assert torch.isfinite(output).all()
    assert torch.unique(diagnostics["route_ids"]).numel() > 1
    assert model.route_projection.weight.grad.norm() > 0
