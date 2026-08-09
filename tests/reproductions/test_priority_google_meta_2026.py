import numpy as np

from auto_research.reproductions.agentic_rec_tune.model import actor_critic_search
from auto_research.reproductions.dual_sid.model import train_dual_sid
from auto_research.reproductions.ha_moe.model import build_ha_moe, score_ha_moe
from auto_research.reproductions.kunlun.model import score_kunlun
from auto_research.reproductions.mfli.model import build_mfli, score_mfli
from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.ultra_hstu.model import score_ultra_hstu


class Sequences:
    item_count = 16
    features = np.eye(16, 8, dtype=np.float32)
    train = (tuple(range(12)), tuple(range(3, 15)))
    validation = (12, 15)
    test = (13, 0)


class Data:
    sequences = Sequences()
    item_count = 16
    transition = np.full((16, 16), 1 / 16, dtype=float)
    cosine = Sequences.features @ Sequences.features.T
    popularity = np.linspace(0, 1, 16)
    domains = np.arange(16) % 4


def test_priority_adapters_have_full_text_online_evidence():
    for key in ("ha-moe", "dual-sid", "agentic-rec-tune", "mfli", "kunlun", "ultra-hstu"):
        adapter = get_adapter(key)
        assert adapter.fidelity.value == "core_mechanism"
        assert adapter.paper.organization
        assert adapter.paper.published.startswith("2026-")
        assert adapter.paper.has_online_ab
        assert all(evidence.source_url for evidence in adapter.paper.online_ab)
        assert all(evidence.source_location for evidence in adapter.paper.online_ab)


def test_ha_moe_executes_heterogeneous_experts():
    state = build_ha_moe(Data)
    score = score_ha_moe(Data, state, tuple(range(10)))
    assert score.shape == (16,)
    assert len(state["domain_pop"]) == 4


def test_dual_sid_trains_codes_and_semantic_decoder():
    state = train_dual_sid(Data, levels=2, width=4)
    assert state["codes"].shape == (16, 2)
    assert state["reconstructed"].shape == Sequences.features.shape
    assert len(state["transition"]) == 2


def test_mfli_builds_multiple_learned_facets():
    state = build_mfli(Data)
    assert state["facets"].shape == (16, 4)
    assert score_mfli(Data, state, tuple(range(10))).shape == (16,)


def test_kunlun_and_ultra_hstu_execute_deep_routes():
    kunlun, kunlun_trace = score_kunlun(Data, tuple(range(12)), layers=3)
    ultra, ultra_trace = score_ultra_hstu(Data, tuple(range(12)), layers=3, window=4)
    assert kunlun.shape == ultra.shape == (16,)
    assert len(kunlun_trace) == len(ultra_trace) == 3
    assert all(np.isclose(sum(route), 1.0) for route in kunlun_trace + ultra_trace)


def test_agentic_rec_tune_keeps_multiround_skillhub():
    champion, trace = actor_critic_search(Data, generations=3)
    assert len(trace) == 3
    assert all(row["actor_candidates"] > 1 for row in trace)
    assert np.isclose(sum(champion), 1.0)
