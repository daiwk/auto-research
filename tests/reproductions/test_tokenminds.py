import numpy as np

from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.tokenminds.model import (
    TokenMindsConfig,
    build_model,
    build_semantic_codes,
)


def test_tokenminds_metadata_and_online_evidence_are_complete():
    adapter = get_adapter("tokenminds")
    assert adapter.paper.arxiv_id == "2606.25147"
    assert adapter.paper.organization == "Google DeepMind / YouTube"
    assert adapter.paper.published == "2026-06-23"
    assert adapter.paper.has_online_ab
    assert adapter.fidelity.value == "core_mechanism"


def test_tokenminds_builds_hierarchical_codes_and_dual_output():
    import torch

    class Data:
        item_count = 24
        features = np.eye(24, 8, dtype="float32")

    config = TokenMindsConfig(
        dimensions=16,
        maximum_history=6,
        sid_levels=2,
        sid_cardinality=4,
    )
    codes = build_semantic_codes(Data.features, config)
    assert codes.shape == (Data.item_count, config.sid_levels)
    assert codes.min() >= 0
    assert codes.max() < config.sid_cardinality

    histories = torch.randint(0, Data.item_count, (3, config.maximum_history))
    model = build_model(Data, codes, config, dual_output=True)
    logits, sid_logits = model(histories)
    assert logits.shape == (3, Data.item_count)
    assert len(sid_logits) == config.sid_levels
    assert all(values.shape == (3, config.sid_cardinality) for values in sid_logits)
    assert model.token_gate.requires_grad
