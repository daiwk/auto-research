from pathlib import Path

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.reproductions.registry import get_adapter


def test_retoken_is_registered_and_searchable():
    adapter = get_adapter("retoken")
    assert adapter.paper.published == "2026-07-30"
    assert adapter.paper.code_url == "https://github.com/avaxiao/ReToken"
    assert adapter.paper.track == "llm"


def test_retoken_executes_sparse_value_cache_selection():
    import torch

    model = build_micro_lm(
        "retoken",
        MicroLMConfig(
            vocab_size=64,
            dimensions=32,
            layers=2,
            heads=4,
            sequence_length=16,
        ),
    )
    output = model(torch.randint(0, 64, (2, 16)))
    stats = model.architecture_stats()
    assert output.shape == (2, 16, 64)
    assert stats["retrieval_target_tokens"] == 1
    assert 0 < stats["causal_cache_keep_rate"] <= 1


def test_latest_cross_domain_docs_exist():
    root = Path(__file__).resolve().parents[2]
    assert (root / "docs/post-training/2607.28590-vad/README.md").exists()
    assert (root / "docs/agent-research/2607.28609-osreward/README.md").exists()
