import importlib

import pytest
import torch


@pytest.mark.parametrize("module", ["fleet_feature_components", "lser_protocol_components", "dna_components"])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostics(module, seed):
    out = importlib.import_module("auto_research.reproductions." + module).diagnostic(seed)
    assert out["diagnostic_only"] is True
    assert all(value is True for value in out["checks"].values())
    assert out["metrics"]


def test_fronts_preserve_ties_and_task_units():
    from auto_research.reproductions.fleet_feature_components import pareto_fronts

    assert pareto_fronts({"a": [1, 2], "b": [1, 2], "c": [0, 1]}) == [["a", "b"], ["c"]]
    assert pareto_fronts({"a": [100, 1], "b": [1, 2], "c": [0, 0]}) == [["a", "b"], ["c"]]
    with pytest.raises(ValueError):
        pareto_fronts({"a": [float("nan")]})


def test_blending_never_fills_an_undefined_rounding_shortfall():
    from auto_research.reproductions.fleet_feature_components import blend_sources

    assert blend_sources([["a"], ["a", "b"]], [1, 2])["quota_exhausted"]
    assert blend_sources([["a", "b"]], [1], banned=["a"])["selected"] == ["b"]
    with pytest.raises(ValueError):
        blend_sources([["a", "a"]], [1])
    with pytest.raises(ValueError):
        blend_sources([["a"]], [True])


def test_pipeline_cost_is_set_dependent_and_refill_failure_explicit():
    from auto_research.reproductions.fleet_feature_components import pipeline_delta, trim_additions

    def cost(s):
        return len(s) + (100 if {"a", "b"} <= s else 0)

    assert pipeline_delta([], ["a"], [["b"]], cost) == 101
    result = trim_additions(["a"], [], [], {"a": "dense"}, {"dense": []}, ["a"], lambda s: False)
    assert result["feasible"] is False and result["selection"] == ["a"]
    with pytest.raises(ValueError):
        trim_additions(["a"], [], [], {"a": "dense"}, {"dense": []}, [], lambda s: True)


def test_admission_requires_terminal_feasible_and_strict_ne_improvement():
    from auto_research.reproductions.fleet_feature_components import choose_winner

    assert choose_winner([{"status": "failed"}], .7, {"memory": 1.}) is None
    assert choose_winner([{"status": "completed", "validation_ne": .7, "resources": {"memory": 1.}}],
                         .7, {"memory": 1.}) is None
    with pytest.raises(ValueError):
        choose_winner([{"status": "completed", "validation_ne": .6, "resources": {"QPS": 1.}}],
                      .7, {"inverse_qps": 1.})


def test_lser_timestamp_and_cache_boundaries():
    from auto_research.reproductions.lser_protocol_components import point_in_time, cached_payload

    ev = [{"timestamp": x, "session_id": "current"} for x in [1, 5, 10, 11]]
    w = point_in_time(ev, cutoff=10, session_start=5, history_start=0,
                      current_session="current", session_limit=3, history_limit=3)
    assert w == {"session": [ev[1]], "history": [ev[0]]}
    row = {"family": "session", "as_of": 5, "written_at": 8, "values": [1.]}
    old_arrives_late = {**row, "as_of": 4, "written_at": 9, "values": [2.]}
    out = cached_payload([row, old_arrives_late], request_time=10)
    assert out["vectors"]["session"]["values"] == (1.,)
    assert out["missing_required"] == ["history"] and out["requires_external_cold_start"]
    with pytest.raises(ValueError):
        cached_payload([{**row, "as_of": 9}], request_time=10)


def test_lser_lookback_and_logged_session_not_guessed_from_time():
    from auto_research.reproductions.lser_protocol_components import point_in_time

    events = [{"timestamp": t, "session_id": session}
              for t, session in [(0, "old"), (2, "old"), (5, "other"), (6, "current")]]
    result = point_in_time(events, cutoff=10, session_start=5, history_start=1,
                           current_session="current", session_limit=10, history_limit=10)
    assert result == {"session": [events[3]], "history": [events[1]]}


def test_lser_incomplete_llm_pair_is_not_silently_used_as_treatment():
    from auto_research.reproductions.lser_protocol_components import cached_payload

    row = {"family": "llm_session", "as_of": 1, "written_at": 2, "values": [1.]}
    assert cached_payload([row], request_time=5)["vectors"] == {}


def test_dna_shared_request_is_candidate_independent_and_padding_has_no_gradient():
    from auto_research.reproductions.dna_components import DNA

    torch.manual_seed(42)
    model = DNA(depth=2)
    s = torch.randn(1, 3, 8, requires_grad=True)
    u = torch.randn(1, 2, 8, requires_grad=True)
    valid = torch.tensor([[True, True, False]])
    groups = torch.tensor([0, 1, 1])
    cache = model.prepare_request(s, u, groups, valid)
    original = cache.sequence.clone()
    model.score(cache, torch.randn(1, 2, 2, 8)).sum().backward()
    assert torch.equal(cache.sequence, original)
    assert (s.grad[:, -1] == 0).all()
    assert cache.updates == 1 and len(cache.keys_values) == 2
    assert model.layers[0].uk.in_features == 16
    assert model.layers[0].candidate_read.ff[0] is not model.layers[0].candidate_read.ff[1]


def test_dna_depth_one_has_no_unused_update_and_rejects_empty_history():
    from auto_research.reproductions.dna_components import DNA

    model = DNA(depth=1)
    s, u = torch.randn(1, 3, 8), torch.randn(1, 2, 8)
    groups = torch.tensor([0, 1, 1])
    assert not hasattr(model.layers[0], "uk")
    assert model.prepare_request(s, u, groups, torch.ones(1, 3, dtype=torch.bool)).updates == 0
    with pytest.raises(ValueError):
        model.prepare_request(s, u, groups, torch.zeros(1, 3, dtype=torch.bool))
