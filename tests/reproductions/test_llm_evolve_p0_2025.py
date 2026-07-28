from dataclasses import replace

import pytest

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.evolution.models import Genome, PaperInspiration
from auto_research.evolution.muon import Muon
from auto_research.evolution.planner import allowed_architectures, propose
from auto_research.reproductions.registry import get_adapter


def test_p0_adapters_have_verified_metadata_and_upstream_status():
    expected = {
        "native-sparse-attention": ("2025-02-16", False),
        "gated-attention": ("2025-05-10", True),
        "muon": ("2025-02-24", True),
    }
    for key, (published, has_code) in expected.items():
        adapter = get_adapter(key)
        assert adapter.paper.track == "llm"
        assert adapter.paper.published == published
        assert bool(adapter.paper.code_url) is has_code


@pytest.mark.parametrize(
    "architecture",
    ["native_sparse_attention", "gated_attention", "nsa_gated_attention"],
)
def test_attention_variants_are_causal_and_trainable(architecture):
    torch = pytest.importorskip("torch")
    torch.manual_seed(7)
    config = MicroLMConfig(
        vocab_size=97,
        dimensions=32,
        layers=1,
        heads=4,
        sequence_length=24,
    )
    model = build_micro_lm(architecture, config).eval()
    left = torch.randint(0, config.vocab_size, (2, config.sequence_length))
    right = left.clone()
    right[:, 12:] = torch.randint(
        0, config.vocab_size, right[:, 12:].shape
    )
    left_logits = model(left)
    right_logits = model(right)
    assert torch.allclose(left_logits[:, :12], right_logits[:, :12], atol=1e-6)
    model.train()
    model(left).square().mean().backward()
    assert all(
        parameter.grad is not None
        for parameter in model.parameters()
        if parameter.requires_grad
    )


def test_nsa_executes_all_three_sparse_branches():
    torch = pytest.importorskip("torch")
    config = MicroLMConfig(
        vocab_size=97,
        dimensions=32,
        layers=1,
        heads=4,
        sequence_length=32,
    )
    model = build_micro_lm("native_sparse_attention", config)
    model(torch.randint(0, config.vocab_size, (2, config.sequence_length)))
    stats = model.architecture_stats()
    assert stats["compression_block"] > 0
    assert stats["selected_blocks"] == 1
    assert stats["local_window"] > 0
    assert 0 < stats["attention_edge_fraction"] < 1
    assert stats["reference_kernel"] == "pytorch"


def test_muon_updates_matrix_parameters_with_orthogonalized_direction():
    torch = pytest.importorskip("torch")
    torch.manual_seed(3)
    model = build_micro_lm(
        "llama_modern",
        MicroLMConfig(
            vocab_size=64,
            dimensions=32,
            layers=1,
            heads=4,
            sequence_length=16,
        ),
    )
    optimizer = Muon(
        model.named_parameters(), learning_rate=3e-4, torch=torch
    )
    before = optimizer.muon_parameters[0].detach().clone()
    tokens = torch.randint(0, 64, (2, 16))
    model(tokens).square().mean().backward()
    optimizer.step()
    assert not torch.equal(before, optimizer.muon_parameters[0])
    assert optimizer.last_orthogonality_error < 0.2


def test_evolve_can_compose_sparse_gating_and_muon():
    papers = [
        PaperInspiration(
            "2502.11089",
            "NSA",
            "https://arxiv.org/abs/2502.11089",
            "2025-02-16",
            "native_sparse_attention",
            "NSA",
            "installed evidence",
        ),
        PaperInspiration(
            "2502.16982",
            "Muon",
            "https://arxiv.org/abs/2502.16982",
            "2025-02-24",
            "optimizer:muon",
            "Muon",
            "installed evidence",
        ),
    ]
    architectures = allowed_architectures(
        "micro-llm",
        "组合 Native Sparse Attention、Gated Attention 和 Muon",
        papers,
    )
    assert architectures[0] == "nsa_gated_attention"
    assert "optimizer:muon" in architectures
    parent = replace(
        Genome(), architecture="llama_modern", optimizer="adamw"
    )
    import random

    index = architectures.index("optimizer:muon")
    genome, rationale = propose(
        parent,
        generation=1,
        index=index,
        architectures=architectures,
        rng=random.Random(42),
        model="micro-llm",
    )
    assert genome.architecture == "llama_modern"
    assert genome.optimizer == "muon"
    assert "优化器研究" in rationale
