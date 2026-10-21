from dataclasses import asdict

import pytest

from auto_research.agent_research.spec_driven_tests import (
    Condition, Contract, Execution, FixedSourceView, GeneratedSuite, Specification,
    evaluate, generate, pass_detect_at_k,
)


def specification():
    return Specification((Contract("increment", "Add one", (),
        (Condition("result equals input plus one"),), ("test zero and negative values",)),))


def test_phase_order_public_view_and_optional_curation():
    calls = []
    view = FixedSourceView("def increment(x): return x + 1")
    object.__setattr__(view, "gold_patch", "PRIVATE")

    def extract(public):
        assert set(asdict(public)) == {"source", "requirements", "existing_tests"}
        assert not hasattr(public, "gold_patch")
        calls.append("extract")
        return specification()

    def curate(spec):
        calls.append("curate")
        return spec

    def synthesize(public, spec):
        assert spec.markdown().endswith("test zero and negative values\n")
        calls.append("tests")
        return GeneratedSuite("assert increment(0) == 1")

    spec, suite = generate(view, extract, synthesize, curate)
    assert calls == ["extract", "curate", "tests"]
    assert "[ ] result" in spec.markdown() and suite.code


def test_failed_phase_one_does_not_call_generator():
    with pytest.raises(ValueError, match="phase I"):
        generate(FixedSourceView("fixed"), lambda _: "unstructured", lambda *_: pytest.fail("phase II ran"))


@pytest.mark.parametrize("fixed,buggy,detect", [
    (Execution(True, True), Execution(True, False, ("test_boundary",)), True),
    (Execution(True, True), Execution(False, False), False),
    (Execution(True, True), Execution(True, False), False),
    (Execution(True, False, ("test",)), Execution(True, False, ("test",)), False),
    (Execution(False, False), Execution(True, False, ("test",)), False),
])
def test_same_suite_dual_execution_build_errors_not_detection(fixed, buggy, detect):
    calls = []

    def execute(source, suite):
        calls.append((source, suite))
        return fixed if source == "fixed" else buggy

    result = evaluate(GeneratedSuite("same frozen tests"), "fixed", "buggy", execute)
    assert result.detects_bug is detect
    assert all(code == "same frozen tests" for _, code in calls)
    assert [source for source, _ in calls] == (["fixed", "buggy"] if fixed.passed else ["fixed"])


def test_source_tampering_discarded_without_execution():
    result = evaluate(GeneratedSuite("test", ("source.py",)), "fixed", "buggy",
        lambda *_: pytest.fail("tampered suite executed"), allowed_existing_paths=("test.py", "BUILD"))
    assert not result.valid and not result.detects_bug


def test_allowlisted_test_build_edits_and_observed_k():
    detected = evaluate(GeneratedSuite("tests", ("test.py", "BUILD")), "fixed", "buggy",
        lambda source, _: Execution(True, source == "fixed", () if source == "fixed" else ("boundary",)),
        allowed_existing_paths=("test.py", "BUILD"))
    missed = evaluate(GeneratedSuite("tests"), "fixed", "buggy", lambda *_: Execution(True, True))
    assert pass_detect_at_k(((missed, detected), (missed, missed)), 1) == {"pass_at_k": 1., "detect_at_k": 0.}
    assert pass_detect_at_k(((missed, detected), (missed, missed)), 2) == {"pass_at_k": 1., "detect_at_k": .5}


def test_invalid_contracts_and_outcomes_rejected():
    with pytest.raises(ValueError):
        Condition("condition", True)
    with pytest.raises(ValueError):
        Contract("unit", "description", (), (Condition("untested"),), ())
    with pytest.raises(ValueError):
        Execution(False, True)
    with pytest.raises(ValueError):
        pass_detect_at_k(((evaluate(GeneratedSuite("x"), "f", "b", lambda *_: Execution(True, True)),),), 2)
