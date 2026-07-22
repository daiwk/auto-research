import numpy as np

from auto_research.reproductions.recgpt_v3.model import RecGPTV3Config, build_models


def test_recgpt_v3_has_hybrid_sid_memory_and_latent_paths():
    features = np.eye(8, dtype=np.float32)
    semantic_ids = np.column_stack((np.arange(8) % 4, np.arange(8) // 4))
    config = RecGPTV3Config(dimensions=16, heads=4, maximum_history=8, recent_events=2, memory_slots=3, latent_tokens=2, codebook_size=4)
    baseline, method = build_models(features, semantic_ids, config)
    import torch
    histories = torch.tensor([[0, 1, 2, 3, 4, 5, 6, 7]])
    assert baseline(histories).shape == (1, 8)
    logits, teacher, latent, segments, weights = method(histories, return_aux=True)
    assert logits.shape == teacher.shape == (1, 8)
    assert latent.shape == segments.shape == (1, 2, 16)
    assert weights.shape == (1, 3, 6)


def test_recgpt_v3_metadata_is_complete():
    from auto_research.reproductions.registry import get_adapter
    adapter = get_adapter("recgpt-v3")
    assert adapter.paper.published == "2026-07-17"
    assert adapter.paper.organization == "Alibaba / Taobao"
    assert len(adapter.paper.online_ab) == 3
