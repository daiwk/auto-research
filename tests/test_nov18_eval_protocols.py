"""Negative controls for supplied-data protocols, not judge/inference capability."""

from importlib import import_module
import math

import pytest

from auto_research.foundation_models.runway_inference_protocol import cache_key, cost_per_successful_request, evaluate_sla, result_for_cell
from auto_research.foundation_models.smart_model_routing import cascade_cost, cascade_quality, cost_reduction, shadow_price_tier, token_cost, two_stage_breakeven
from auto_research.post_training.calibrated_judges_protocol import Verdict, join_swapped_judgments, qualify
from auto_research.post_training.luce_similarity_audit import corrected_win_probability, heldout_log_loss, menu_log_odds_shift


@pytest.mark.parametrize("module", ["post_training.luce_similarity_audit", "foundation_models.runway_inference_protocol",
                                   "foundation_models.smart_model_routing", "post_training.calibrated_judges_protocol"])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostics(module, seed):
    implementation = import_module(f"auto_research.{module}")
    result = implementation.diagnostic(seed)
    assert implementation.REQUIRES_GPU_VALIDATION is False
    assert result["seed"] == seed and result["diagnostic_only"] is True
    assert result["checks"] and all(type(v) is bool and v for v in result["checks"].values())
    assert all(type(v) in (int, float) and math.isfinite(v) for v in result["metrics"].values())
    with pytest.raises(ValueError):
        implementation.diagnostic(seed, device="cuda")


def test_luce_extremes_and_estimand_boundary():
    assert corrected_win_probability(-1000) == 0
    assert corrected_win_probability(1000) == 1
    assert heldout_log_loss([1, 0], [.8, .2]) == pytest.approx(-math.log(.8))
    assert menu_log_odds_shift(1e300, 1e-300, 1, 1) == pytest.approx(600 * math.log(10))
    assert menu_log_odds_shift(1e-300, 1e300, 1e300, 1e-300) == pytest.approx(-1200 * math.log(10))
    with pytest.raises(ValueError):
        menu_log_odds_shift(0, 2, 3, 4)
    with pytest.raises(ValueError):
        heldout_log_loss([1], [1])


def _configuration():
    return dict(dataset="fixture", dataset_revision="v1", instance="fixture", model="fixture", model_revision="v1",
                engine="fixture", engine_version="v1", input_length=10, output_length=10, concurrency=1,
                streaming=True, aiperf_extra_args=[], benchmark_duration=10, custom_dataset_type="text",
                warmup=0, engine_configuration={})


def test_cache_all_settings_and_copies():
    config, cache, calls = _configuration(), {}, []
    result, hit = result_for_cell(config, cache, lambda c: calls.append(c) or {"data": [1]})
    result["data"].append(2)
    cached, hit = result_for_cell(config, cache, only_cache=True)
    assert hit and cached == {"data": [1]} and len(calls) == 1
    for field, value in [("warmup", 1), ("engine_configuration", {"mtp": True}), ("dataset_revision", "v2")]:
        changed = {**config, field: value}
        assert cache_key(config) != cache_key(changed)
        with pytest.raises(KeyError):
            result_for_cell(changed, cache, only_cache=True)
    result_for_cell(config, cache, lambda c: calls.append(c) or {}, no_cache=True)
    assert len(calls) == 2


def test_sla_missing_and_warning_semantics():
    rules = [{"metric": "p95", "operator": "<=", "value": 2, "unit": "s", "severity": "critical"}]
    assert not evaluate_sla({}, rules)["accepted"]
    assert not evaluate_sla({"p95": (1000, "ms")}, rules)["accepted"]
    assert evaluate_sla({"p95": (1, "s")}, rules)["accepted"]
    assert evaluate_sla({}, [{**rules[0], "severity": "warning"}])["accepted"]


def test_routing_includes_overhead_and_conditional_quality():
    assert shadow_price_tier([.0006, .015], [.949, .950], 1) == 0
    assert shadow_price_tier([.0006, .015], [.949, .950], 15) == 1
    assert cost_reduction(.02, 25, frontier_token_ratio=100) == pytest.approx(2.98 / 2.0392)
    threshold = two_stage_breakeven(1, 10, checker_cost=1, router_cost=.5)
    assert cascade_cost([1, 10], [threshold, 1], checker_costs=[1, 0], router_cost=.5) == pytest.approx(10)
    assert cascade_cost([1, 10], [threshold + .01, 1], checker_costs=[1, 0], router_cost=.5) < 10
    assert cascade_quality([.5, 1], [1, .2]) == pytest.approx(.6)
    with pytest.raises(ValueError):
        cascade_cost([1, 10], [.5, .5])


def test_extreme_cost_arithmetic_never_silently_returns_nan_or_infinity():
    assert token_cost(1_000_000, 0, 1e308, 0) == 1e308
    assert cost_per_successful_request(1e308, 1, 1) == pytest.approx(1e308 / 3600)
    for operation in [
        lambda: cost_reduction(.5, 1e308, frontier_token_ratio=1e308),
        lambda: cost_reduction(1, 1e-300, frontier_token_ratio=1e-300),
        lambda: cascade_cost([1e308, 1e308], [0., 1.]),
        lambda: token_cost(2_000_000, 0, 1e308, 0),
        lambda: cost_per_successful_request(1e308, 1e308, 1),
        lambda: two_stage_breakeven(1e308, 1, checker_cost=1e308),
    ]:
        with pytest.raises(ValueError, match="finite floating-point"):
            operation()


def _qualified(judge):
    return qualify(judge, [(Verdict(judge, f"catch-{i}", "AB", "A" if i < 3 else "B"), "A") for i in range(4)])


def test_judge_gate_swap_disagreement_and_gold_separation():
    qs = (_qualified("j1"), _qualified("j2"))
    assert qs[0].qualified and qs[0].sensitivity == .75
    votes = [Verdict(q.judge, "pair", order, "A" if order == "AB" else "B") for q in qs for order in ("AB", "BA")]
    assert join_swapped_judgments("pair", votes, qs)["winner"] == "A"
    inconsistent = [votes[0], Verdict("j1", "pair", "BA", "A"), *votes[2:]]
    assert join_swapped_judgments("pair", inconsistent, qs)["winner"] == "tie"
    bad = qualify("bad", [(Verdict("bad", "bad-catch", "AB", "B"), "A")])
    assert not bad.qualified
    assert join_swapped_judgments("pair", [*votes[:2], Verdict("bad", "pair", "AB", "A"), Verdict("bad", "pair", "BA", "B")], (qs[0], bad))["winner"] == "tie"
    with pytest.raises(ValueError):
        join_swapped_judgments("catch-0", [], qs)
    with pytest.raises(ValueError):
        join_swapped_judgments("pair", votes, (qs[0], qs[0]))
    with pytest.raises(ValueError):
        join_swapped_judgments("pair", votes + [votes[0]], qs)
