from auto_research.evolution.models import EvolutionTrial, Genome
from auto_research.evolution.research_memory import (
    methodology_order,
    update_research_memory,
    verify_trial,
)
from auto_research.reproductions.registry import get_adapter


def _trial(trial_id, architecture, fitness, generation=1, status="completed"):
    return EvolutionTrial(
        trial_id, generation, "g0-t0", Genome(architecture=architecture),
        {"fitness": fitness, "ndcg_at_10": fitness},
        {"parameters": 10}, (), "test", 0.1, status,
        None if status == "completed" else "failed",
    )


def test_nova_verification_and_evorec_memory_change_next_generation():
    parent = _trial("g0-t0", "rankmixer_dense", 0.10, generation=0)
    winner = _trial("g1-t1", "rankmixer_unimixer", 0.12)
    failed = _trial("g1-t2", "rankmixer_longer", -1e9, status="failed")
    records = [verify_trial(winner, parent), verify_trial(failed, parent)]

    assert records[0]["passed"]
    assert not records[1]["passed"]
    memory = update_research_memory({}, parent, [winner, failed], winner, records)
    assert memory["successful_skills"][0]["architecture"] == "rankmixer_unimixer"
    assert memory["forbidden_directions"][0]["architecture"] == "rankmixer_longer"
    assert methodology_order(
        ["rankmixer_dense", "rankmixer_longer", "rankmixer_unimixer"], memory
    ) == ["rankmixer_unimixer", "rankmixer_dense"]


def test_p0_recommendation_adapters_keep_online_evidence():
    for key in (
        "nova", "evorec", "tokenmixer-large", "msn", "idproxy",
        "glide", "genrec", "rankgraph2", "solaris",
    ):
        assert get_adapter(key).paper.has_online_ab


def test_minimax_sparse_attention_is_trainable_sparse_gqa():
    import torch

    from auto_research.reproductions.minimax_sparse_attention.model import build_tiny_lm

    model = build_tiny_lm(
        vocab_size=32, dimensions=32, heads=4, kv_heads=2,
        block_size=4, top_blocks=1, sparse=True,
    )
    output = model(torch.randint(0, 32, (2, 16)))
    (output.mean() + model.attention.index_loss).backward()
    assert output.shape == (2, 16, 32)
    assert 0.0 < model.attention.last_pair_ratio < 0.5
    assert model.attention.index_q.weight.grad is not None
