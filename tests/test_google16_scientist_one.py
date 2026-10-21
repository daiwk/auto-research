import json

import pytest

from auto_research.agent_research.google16_scientist_one import (
    Artifact,
    AuditVote,
    Claim,
    Measurement,
    majority_audit,
    numerical_cpr,
    reference_verification,
    score_verification,
    verify_bundle,
)


def fixture():
    record = {"metric": "accuracy", "value": 0.7, "stage": "validation", "unit": "fraction", "direction": "max"}
    payload = json.dumps({"measurements": [record]}).encode()
    artifact = Artifact.from_bytes("log", payload, "execution_log")
    claim = Claim("claim", "numerical", ("log",), metric="accuracy", value=0.7, stage="validation", unit="fraction", direction="max")
    measurement = Measurement("log", **record)
    return artifact, claim, measurement, payload


def test_hash_chains_dangling_support_and_cycles_are_detected():
    artifact, claim, _, payload = fixture()
    result = verify_bundle([artifact], [claim], {"log": payload})
    assert result["structurally_grounded"]["claim"]
    assert result["semantic_entailment"] == "unverified"
    assert not verify_bundle([artifact], [claim], {"log": b"tampered"})["structurally_grounded"]["claim"]
    cyclic = [Claim("a", "conclusion", ("b",)), Claim("b", "conclusion", ("a",))]
    assert not any(verify_bundle([], cyclic, {})["structurally_grounded"].values())
    assert not verify_bundle([], [Claim("missing", "citation", ("absent",))], {})["structurally_grounded"]["missing"]


def test_numerical_cpr_requires_actual_log_record_and_stage_metric_matching():
    artifact, claim, measurement, payload = fixture()
    assert numerical_cpr([claim], [measurement], [artifact], {"log": payload})["cpr"] == 1
    wrong = Claim("wrong", "numerical", ("log",), metric="accuracy", value=0.7, stage="test", unit="fraction", direction="max")
    assert numerical_cpr([wrong], [measurement], [artifact], {"log": payload})["cpr"] == 0
    fabricated = Measurement("log", "accuracy", 0.99, "validation", "fraction", "max")
    with pytest.raises(ValueError, match="not present"):
        numerical_cpr([claim], [fabricated], [artifact], {"log": payload})
    assert numerical_cpr([], [], [], {})["cpr"] is None


def test_score_verification_really_calls_canonical_evaluator_five_times():
    solution, evaluator = b"public solver", b"canonical evaluator"
    calls = []

    def evaluate(source, judge, index):
        calls.append((source, judge, index))
        return Measurement("rerun", "cost", 100 + (index - 2), "test", "seconds", "min")

    result = score_verification(Measurement("paper", "cost", 102, "test", "seconds", "min"), solution=Artifact.from_bytes("code", solution, "code"), solution_bytes=solution, evaluator=Artifact.from_bytes("eval", evaluator, "evaluator"), evaluator_bytes=evaluator, evaluate=evaluate)
    assert len(calls) == 5 and all(call[:2] == (solution, evaluator) for call in calls)
    assert result["canonical_mean"] == 100
    assert result["absolute_tolerance"] == pytest.approx(3 * 2 ** 0.5)
    assert result["status"] == "match"


def test_wrong_direction_and_deterministic_zero_do_not_gain_false_pass():
    code, evaluator = b"x", b"y"
    kwargs = {"solution": Artifact.from_bytes("code", code, "code"), "solution_bytes": code, "evaluator": Artifact.from_bytes("eval", evaluator, "evaluator"), "evaluator_bytes": evaluator}
    reported = Measurement("p", "score", 0.0001, "test", "fraction", "max")
    result = score_verification(reported, **kwargs, evaluate=lambda *args: Measurement("e", "score", 0, "test", "fraction", "max"))
    assert result["status"] == "mismatch" and result["absolute_tolerance"] == 0
    result = score_verification(reported, **kwargs, evaluate=lambda *args: Measurement("e", "score", 0, "test", "fraction", "min"))
    assert result["reason"] == "metric_stage_unit_or_direction_mismatch"


def test_unavailable_semantic_and_reference_audits_stay_unverified():
    assert majority_audit([], pass_verdict="clean", fail_verdict="flagged")["status"] == "unverified"
    votes = [AuditVote("clean", "audit:1", "j1"), AuditVote("unverified", "audit:2", "j2")]
    assert majority_audit(votes, pass_verdict="clean", fail_verdict="flagged")["status"] == "unverified"
    assert reference_verification(reference_id="unknown", resolve=None, disambiguate=None)["status"] == "unverified"
    assert reference_verification(reference_id="unknown", resolve=lambda key: [], disambiguate=lambda *args: None)["status"] == "unverified"
    with pytest.raises(ValueError, match="distinct"):
        majority_audit([votes[0], votes[0]], pass_verdict="clean", fail_verdict="flagged")
