from auto_research.reproductions.latest_20260921 import (
    ComparisonProtocol,
    make_evopilot_adapter,
    verify_comparison,
)


def test_evopilot_rejects_depth_mismatch_and_admits_exact_contrast():
    protocol = ComparisonProtocol("base", "data", "eval", 10, ("head",))
    common = {
        "status": "succeeded", "base_revision": "base",
        "data_revision": "data", "evaluator_revision": "eval",
        "artifact_digest": "sha256:public",
    }
    control = {**common, "effective_output_depth": 10,
               "configuration": {"head": False}}
    treatment = {**common, "effective_output_depth": 10,
                 "configuration": {"head": True}}
    assert verify_comparison(control, treatment, protocol)["admitted"] is True
    mismatched = {**control, "effective_output_depth": 30}
    result = verify_comparison(mismatched, treatment, protocol)
    assert result["admitted"] is False
    assert "control:effective_output_depth" in result["errors"]


def test_evopilot_has_meta_online_evidence():
    adapter = make_evopilot_adapter()
    assert adapter.paper.organization == "Meta Platforms"
    assert adapter.paper.online_ab[0].lift_percent == 0.66
    assert adapter.evaluation_tier.value == "l2_public_dataset"
