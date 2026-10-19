import importlib.util
import math
from pathlib import Path

import pytest

from auto_research.system_one.contracts import DecisionAnswer, SystemOneResponse
from auto_research.system_one.portuguese_ir import (
    Document, confusion_agreement, evaluate_rankings, kendall_tau_b, relevance_request, rerank, rerank_requests,
)


def test_protocol_runner_and_published_table_audit():
    spec = importlib.util.spec_from_file_location("portuguese_runner", Path(__file__).resolve().parents[1] / "scripts/run_oct19_evening_system_one.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for seed in (42, 43, 44):
        assert module.diagnostic(seed)["metrics"]["invalid_response_negative_controls_rejected"] == 4
    expected = {"Quati": (1933, .529, .68), "JurisTCU": (2250, .643, .82),
                "NormasTCU": (812, .548, .52), "Ulysses-RFCorpus": (8205, .649, .65)}
    for name, matrix in module.PUBLISHED_TABLES.items():
        result = confusion_agreement(matrix)
        count, accuracy, kappa = expected[name]
        assert result["judgments"] == count
        assert result["exact_agreement"] == pytest.approx(accuracy, abs=.0006)
        assert result["quadratic_weighted_kappa"] == pytest.approx(kappa, abs=.006)


def test_stable_ties_and_tail_and_body_only_limit():
    docs = [Document("a", "  abc  def", "A long title"), Document("b", "x"), Document("c", "tail")]
    def provider(request):
        return SystemOneResponse(request.model, {key: DecisionAnswer("noul", True, {"yes": .5, "no": .5}, .5) for key in request.questions})
    assert rerank("q", docs, provider, depth=2, batch_size=1)[0] == ("a", "b", "c")
    assert rerank("q", docs, provider, depth=2, retain_tail=False)[0] == ("a", "b")
    state = rerank_requests("q", docs, text_limit=3)[0].state
    assert state["documentos"][0] == {"id": "a", "title": "A long title", "text": "abc"}


def test_macro_mrr_and_linear_gains_and_query_coverage():
    result = evaluate_rankings({"a": ["x", "y"], "b": ["x"]}, {"a": {"x": 1, "y": 3}, "b": {"z": 1}})
    assert result["mrr"] == .5
    assert result["ndcg_at_k_linear"] == pytest.approx((1 + 3 / math.log2(3)) / (3 + 1 / math.log2(3)) / 2)
    with pytest.raises(ValueError):
        evaluate_rankings({"a": []}, {"a": {}, "b": {}})
    with pytest.raises(ValueError):
        evaluate_rankings({"a": ["x", "x"]}, {"a": {"x": 1}})


def test_kendall_ties_unknown_and_input_rejection():
    assert kendall_tau_b({"a": 1., "b": 1.}, {"a": 0., "b": 1.}) is None
    assert kendall_tau_b({"a": 1., "b": 2.}, {"a": 2., "b": 1.}) == -1.
    assert confusion_agreement([[1, 0], [0, 0]])["quadratic_weighted_kappa"] is None
    for matrix in ([[0, 0], [0, 0]], [[1, 2]], [[1., 0], [0, 1]]):
        with pytest.raises(ValueError):
            confusion_agreement(matrix)
    with pytest.raises(ValueError):
        rerank_requests("q", [Document("x", "a"), Document("x", "b")])


def test_quati_ordinal_label_does_not_reuse_juris_tcu_related():
    doc = Document("a", "documento")
    quati = relevance_request("q", doc, "Quati").questions["a"].criteria
    juris = relevance_request("q", doc, "JurisTCU").questions["a"].criteria
    assert quati["1"] == "Slightly Relevant"
    assert juris["1"] == "Relacionado"


@pytest.mark.parametrize("yes,no", [(.7, float("nan")), (float("nan"), .3),
                                   (True, 0.), ("0.7", .3)])
def test_rerank_rejects_malformed_complement_even_if_yes_is_finite(yes, no):
    def provider(request):
        return SystemOneResponse(request.model, {"a": DecisionAnswer("noul", True,
            {"yes": yes, "no": no}, .7)})
    with pytest.raises(ValueError):
        rerank("q", [Document("a", "d")], provider)
