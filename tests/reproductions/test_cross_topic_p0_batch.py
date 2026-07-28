from pathlib import Path

import numpy as np
import pytest

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm
from auto_research.evolution.planner import allowed_architectures
from auto_research.reproductions.foundational_ranking import (
    FoundationalConfig,
    build_foundational_model,
)
from auto_research.reproductions.registry import get_adapter


REC_KEYS = ("wide-deep", "dcn-v2", "dien", "bst", "cq-sid", "cs3")
LLM_KEYS = ("switch-transformer", "mamba", "switch-attention")


def test_cross_topic_batch_is_registered_with_complete_metadata():
    for key in REC_KEYS + LLM_KEYS:
        adapter = get_adapter(key)
        assert adapter.paper.organization
        assert adapter.paper.published
        assert adapter.paper.topics
        if adapter.paper.track == "recommendation":
            assert adapter.paper.online_ab or adapter.paper.selection_exception


@pytest.mark.parametrize(
    "kind", ["deep", "wide-deep", "dcn-v2", "din", "dien", "bst", "two-tower", "cs3"]
)
def test_foundational_rankers_execute_real_candidate_conditioned_paths(kind):
    torch = pytest.importorskip("torch")
    features = np.eye(12, 4, dtype=np.float32)
    model = build_foundational_model(
        kind, 12, features,
        FoundationalConfig(dimensions=16, history_length=6, batch_size=4, steps=1),
    )
    histories = torch.randint(0, 12, (4, 6))
    candidates = torch.randint(0, 12, (4,))
    logits = model(histories, candidates)
    loss = logits.square().mean() + model.auxiliary_loss(histories, candidates)
    loss.backward()
    assert logits.shape == (4,)
    assert any(parameter.grad is not None for parameter in model.parameters())


@pytest.mark.parametrize(
    ("architecture", "stat"),
    [
        ("switch_transformer", "active_experts_per_token"),
        ("mamba", "selective_scan"),
        ("switch_attention", "full_attention_rate"),
    ],
)
def test_new_llm_architectures_train_and_expose_mechanism_stats(
    architecture, stat
):
    torch = pytest.importorskip("torch")
    model = build_micro_lm(
        architecture,
        MicroLMConfig(vocab_size=64, dimensions=32, layers=2, heads=4),
    )
    tokens = torch.randint(0, 64, (2, 16))
    loss = model(tokens).square().mean() + model.auxiliary_loss()
    loss.backward()
    assert stat in model.architecture_stats()


def test_direction_can_prioritize_new_llm_mutations():
    assert allowed_architectures("micro-llm", "Mamba selective SSM", [])[0] == "mamba"
    assert (
        allowed_architectures("micro-llm", "Switch Attention 动态注意力路由", [])[0]
        == "switch_attention"
    )
