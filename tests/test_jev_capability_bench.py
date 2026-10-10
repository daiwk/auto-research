import pytest

from auto_research.system_one.capability_bench import (
    CapabilityItem, evaluate_capability, frontier_comparison,
)
from auto_research.system_one.contracts import DecisionAnswer, SystemOneResponse


class Recorder:
    def __init__(self):
        self.requests = []

    def decide(self, request):
        self.requests.append(request.to_dict())
        return SystemOneResponse(model="fixture", answers={"answer": DecisionAnswer(
            type="choice", value="A", probabilities={"A": 0.6, "B": 0.4}, confidence=0.6,
        )})


def test_reference_is_not_exposed_and_coverage_is_explicit():
    item = CapabilityItem("x", "mathqa", "one plus one?", {"A": "2", "B": "3"}, "A")
    provider = Recorder()
    result = evaluate_capability(provider, [item])
    assert result["results"][0]["accuracy"] == 1
    assert result["results"][0]["accuracy_ci95"][0] < 1
    assert len(result["coverage"]["missing"]) == 12
    assert provider.requests[0]["state"] == {"question": "one plus one?"}
    assert "target" not in str(provider.requests)
    with pytest.raises(ValueError, match="isolated test"):
        evaluate_capability(provider, [CapabilityItem(
            "y", "mathqa", "q", {"A": "a", "B": "b"}, "A", split="calibration",
        )])


def test_published_scores_do_not_change_measured_median():
    result = frontier_comparison([
        {"benchmark": "mathqa", "accuracy": 0.5, "provenance": "measured", "source": "run"},
        {"benchmark": "mathqa", "accuracy": 0.99, "provenance": "published", "source": "paper"},
    ])
    assert result["mathqa"]["measured_median"] == 0.5
    assert result["mathqa"]["published_scores"] == [0.99]
    with pytest.raises(ValueError, match="proportions"):
        frontier_comparison([{"benchmark": "mathqa", "accuracy": 90}])
