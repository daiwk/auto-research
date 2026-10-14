"""Reporting contracts, not training or capability evidence."""
from auto_research.post_training.oct13_common import CostLedger, render_result, result_payload


class PolicyFixture:
    provenance = {"public_id": "fixture", "revision": "fixture"}


def test_upturn_report_names_same_round_control_not_training_before_after():
    result = {"method": "upturn", "seed": 42, "parameters_changed": True,
              "baseline": {"pass_rate": 1.0}, "method_metrics": {"pass_rate": .75}}
    text = render_result(result)
    assert "匹配预算对照" in text and "训练后干预策略" in text
    assert "训练前 validation" not in text
    assert "0.75" in text and "1.0" in text


def test_synthself_protocol_scopes_gold_exclusion_to_evaluated_inference():
    result = result_payload("synthself", {}, 42, {}, PolicyFixture(), CostLedger(), {}, {}, [])
    protocol = result["protocol"]
    assert protocol["gold_in_student_generation"] is False
    assert protocol["gold_in_student_generation_scope"] == "evaluated_student_inference_only"
    assert protocol["training_construction_roles_with_gold"] == ["offline_aligner", "construction_self_rewrite"]


def test_real_before_after_reports_keep_their_original_labels():
    result = {"method": "soar", "seed": 42, "baseline": {}, "method_metrics": {}}
    text = render_result(result)
    assert "训练前 validation" in text and "训练后 validation" in text
