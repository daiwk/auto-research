from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.reproductions.adadsf.model import (
    allocate_retentions,
    sparsify,
)
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.windowed_mtp.model import build_mtp_head


def test_latest_efficiency_adapters_have_complete_upstream_evidence():
    adadsf = get_adapter("adadsf")
    windowed = get_adapter("windowed-mtp")
    assert adadsf.paper.organization.startswith("Huawei")
    assert adadsf.paper.code_url is None
    assert windowed.paper.organization == "NVIDIA"
    assert windowed.paper.code_url.endswith("windowed-mtp-b200")


def test_adadsf_budget_allocation_and_real_sparse_execution():
    import torch

    ratios = allocate_retentions([0.99, 0.90, 0.75, 0.95], target=0.8)
    assert abs(sum(ratios) / len(ratios) - 0.8) < 1e-6
    assert ratios[2] > ratios[0]
    config = MicroLMConfig(
        vocab_size=64, dimensions=32, layers=4, heads=4, sequence_length=20
    )
    dense = build_micro_lm("llama_modern", config)
    sparse = sparsify(dense, ratios)
    tokens = torch.randint(0, 64, (2, 20))
    assert sparse(tokens).shape == (2, 20, 64)
    assert any(block.last_active_fraction < 1 for block in sparse.blocks)
    assert sum(block.last_active_fraction for block in sparse.blocks) / 4 <= 0.8


def test_windowed_mtp_uses_sink_plus_recent_keys():
    import torch

    config = MicroLMConfig(
        vocab_size=64, dimensions=32, layers=1, heads=4, sequence_length=20
    )
    target = build_micro_lm("llama_modern", config)
    draft = build_mtp_head(target)
    tokens = torch.randint(0, 64, (2, 20))
    indices = draft.key_indices(20, window=6, sink=2, device=tokens.device)
    assert indices.tolist() == [0, 1, 14, 15, 16, 17, 18, 19]
    assert draft(tokens).shape == draft(tokens, window=6, sink=2).shape == (2, 64)
