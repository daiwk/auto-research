"""Behavioral checks for the bounded RAGCompass and PiPNN II references."""

import inspect
import math

import pytest

from auto_research.foundation_models import pipnn_ii
from auto_research.post_training import ragcompass


def test_ragcompass_objective_matches_direct_softmax_kl_and_gradient():
    scores = [-0.4, 0.8, 1.2]
    utilities = [0.9, 0.15, 0.45]
    tau = 0.4
    raw_p = [math.exp(x) for x in scores]
    raw_u = [math.exp(x / tau) for x in utilities]
    p = [x / sum(raw_p) for x in raw_p]
    u = [x / sum(raw_u) for x in raw_u]
    expected = sum(a * math.log(a / b) for a, b in zip(u, p, strict=True))
    actual = ragcompass.distillation_objective(scores, utilities, temperature=tau)
    assert actual.loss == pytest.approx(expected)
    assert actual.prediction == pytest.approx(p)
    assert actual.target == pytest.approx(u)
    assert actual.score_gradient == pytest.approx([a - b for a, b in zip(p, u, strict=True)])
    assert sum(actual.score_gradient) == pytest.approx(0.0, abs=1e-15)


def test_ragcompass_stable_large_logits_and_near_hard_target():
    obj = ragcompass.distillation_objective([10000.0, -10000.0], [0.0, 1.0], temperature=1e-300)
    assert obj.loss == pytest.approx(20000.0)
    assert obj.target == (0.0, 1.0)
    assert obj.prediction == (1.0, 0.0)
    assert obj.score_gradient == (1.0, -1.0)


def test_ragcompass_offline_filter_is_not_the_runtime_selector():
    assert ragcompass.eligible_query([0.0, 0.05])
    assert not ragcompass.eligible_query([0.5, 0.5, 0.0])
    assert ragcompass.eligible_query([0.2, 0.0, 0.75, 1.0])
    assert tuple(inspect.signature(ragcompass.select_retriever).parameters) == ("scores",)
    assert ragcompass.select_retriever([-1.0, 5.0, 5.0, 0.0]) == 1
    assert ragcompass.select_retriever([8.0]) == 0


@pytest.mark.parametrize(("scores", "utilities", "tau"), [
    ([], [], 1.0),
    ([0.0], [0.0], 1.0),
    ([0.0, 1.0, 2.0], [0.0, 1.0], 1.0),
    ([0.0, 1.0], [0.0, 1.1], 1.0),
    ([0.0, math.nan], [0.0, 1.0], 1.0),
    ([0.0, 1.0], [0.0, 1.0], 0.0),
    ([0.0, 1.0], [0.0, 1.0], math.inf),
])
def test_ragcompass_rejects_invalid_objective_inputs(scores, utilities, tau):
    with pytest.raises(ValueError):
        ragcompass.distillation_objective(scores, utilities, temperature=tau)


def test_pipnn_offset_is_for_unsigned_database_not_unsigned_query():
    query = [127, -128, 2]
    database = [-128, 127, 3]
    biased = sum((x + 128) * q for x, q in zip(database, query, strict=True))
    expected = sum(x * q for x, q in zip(database, query, strict=True))
    assert biased != expected
    assert pipnn_ii.corrected_dot(query, database) == expected
    assert pipnn_ii.corrected_dot([-7, 2], [3, -4]) == -29


def test_pipnn_paper_figure_2_first_lane():
    query = [5, 1, -3, 2]
    database = [31, -18, -6, 44]
    assert sum((x + 128) * q for x, q in zip(database, query, strict=True)) == 883
    assert 128 * sum(query) == 640
    assert pipnn_ii.corrected_dot(query, database) == 243


def test_pipnn_single_pass_topk_scores_after_per_row_rescale():
    query = [1, 2]
    rows = [([5, 0], 0.25), ([3, 0], 1.0), ([1, 1], 1.0), ([-4, -5], 1.0)]
    seen = []

    def stream():
        for index, pair in enumerate(rows):
            seen.append(index)
            yield pair

    assert pipnn_ii.fused_quantized_topk(query, 2.0, stream(), k=3) == (
        (1, -6.0), (2, -6.0), (0, -2.5),
    )
    assert seen == [0, 1, 2, 3]


@pytest.mark.parametrize(("query", "query_scale", "rows", "k"), [
    ([0], 1.0, [], 1),
    ([0], 1.0, [([0], 1.0)], 2),
    ([0], 1.0, [([0], 1.0)], 0),
    ([0], 1.0, [([0], 1.0)], True),
    ([0], 1.0, [([0], math.nan)], 1),
    ([0], 0.0, [([0], 1.0)], 1),
    ([0], 1.0, [([0, 0], 1.0)], 1),
    ([0], 1.0, [([128], 1.0)], 1),
    ([False], 1.0, [([0], 1.0)], 1),
])
def test_pipnn_rejects_invalid_row_and_budget_contracts(query, query_scale, rows, k):
    with pytest.raises(ValueError):
        pipnn_ii.fused_quantized_topk(query, query_scale, rows, k=k)


@pytest.mark.parametrize("module", [ragcompass, pipnn_ii])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_contract(module, seed):
    row = module.diagnostic(seed, "cpu")
    assert module.REQUIRES_GPU_VALIDATION is False
    assert row["seed"] == seed
    assert row["diagnostic_only"] is True
    assert row["evaluation_tier"] == "l1_mechanism"
    assert row["checks"] and all(value is True for value in row["checks"].values())
    assert all(math.isfinite(value) for value in row["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")
