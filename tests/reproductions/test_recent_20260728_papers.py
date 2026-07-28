import numpy as np

from auto_research.reproductions.core_relevance.model import (
    COREConfig,
    build_model as build_core,
    step_rewards,
    teacher_binary_logits,
)
from auto_research.reproductions.data_orchestra.model import (
    ACTIONS,
    apply_operation,
    build_orchestrator,
    decide,
    text_features,
)
from auto_research.reproductions.mosaic.model import (
    MosaicConfig,
    build_model as build_mosaic,
    cosine_redundancy,
)
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.unir2.model import (
    UniR2Config,
    build_model as build_unir2,
    dual_query_masks,
)


class _Data:
    item_count = 12
    features = np.eye(12, 6, dtype=np.float32)
    popularity = np.arange(1, 13, dtype=np.float32)


def test_recent_papers_preserve_online_evidence_and_upstream_code_contract():
    for key in ("mosaic", "unir2", "core-relevance"):
        adapter = get_adapter(key)
        assert adapter.paper.published == "2026-07-27"
        assert adapter.paper.has_online_ab
        assert adapter.paper.code_url is None
    orchestra = get_adapter("data-orchestra")
    assert orchestra.paper.track == "llm"
    assert orchestra.paper.code_url == "https://github.com/GAIR-NLP/DataOrchestra"


def test_mosaic_executes_four_specialists_mrm_and_redundancy_loss():
    import torch

    config = MosaicConfig(dimensions=8, maximum_history=5)
    model = build_mosaic(_Data(), config, fleet=True)
    histories = torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])
    logits, specialists, mrm = model(histories, return_specialists=True)
    assert logits.shape == (2, 12)
    assert len(specialists) == 4
    assert mrm.shape == (2, 4)
    assert cosine_redundancy(specialists, torch).ndim == 0


def test_unir2_masks_visibility_and_isolates_ranking_gradients_with_lora():
    import torch

    generation, ranking = dual_query_masks(4, 2, 2, torch)
    assert generation.tolist() == [
        [True, True, True, True, True, False],
        [True, True, True, True, True, True],
    ]
    assert ranking.all()
    ids = np.stack((np.arange(12) % 4, np.arange(12) // 4), -1)
    config = UniR2Config(
        dimensions=8,
        heads=2,
        maximum_history=5,
        codebook_size=4,
        sid_levels=2,
        lora_rank=2,
    )
    model = build_unir2(_Data(), ids, config, unified=True)
    histories = torch.tensor([[0, 1, 2, 3, 4], [1, 2, 3, 4, 5]])
    candidates = torch.tensor([6, 7])
    _, ranking_logits = model(histories, candidates)
    ranking_logits.sum().backward()
    assert model.dq.rank_q.b.weight.grad is not None
    assert model.dq.q.weight.grad is None


def test_core_executes_postcot_aggregation_and_conditional_step_rewards():
    import torch

    class_logits = torch.tensor([[1.0, 2.0, 3.0]])
    binary = teacher_binary_logits(class_logits, torch)
    assert binary.shape == (1, 2)
    actions = torch.tensor([[[1.0, 0.0], [0.0, 1.0]]])
    rewards, active = step_rewards(actions, torch.tensor([2]), torch)
    assert rewards.shape == active.shape == (1, 2, 2)
    assert not active[0, 0, 1]
    model = build_core(6, COREConfig(dimensions=8), cascaded=True)
    assert model(torch.randn(3, 6), torch.randn(3, 6)).shape == (3, 2)


def test_data_orchestra_routes_per_example_and_applies_distinct_operations():
    import torch

    features = text_features("= Heading =\nA sentence.").shape[0]
    model = build_orchestrator(features)
    decision = decide(model, "A complete and reasonably clean sentence.", torch)
    assert decision.action in ACTIONS
    assert apply_operation("x\nx\ny", "deduplicate") == "x\ny"
    assert apply_operation("= Heading =", "wiki") == "Heading."
