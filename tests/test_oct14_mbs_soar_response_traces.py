"""CPU-only diagnostic evidence contracts, never model capability evidence."""
import hashlib
import json
from pathlib import Path
import re
import runpy

import pytest
import torch

from auto_research.post_training.oct13_common import CostLedger, ExecutionFailure
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk import checkpoint as mbs_checkpoint
from auto_research.reproductions.magicbeanstalk.algorithm import MagicBeanStalk, Node, Problem
from auto_research.reproductions.soar.algorithm import LexicalRetriever, parse_step
from auto_research.reproductions.soar.checkpoint import SYSTEM


ROOT = Path(__file__).resolve().parents[1]


def probe(monkeypatch):
    monkeypatch.syspath_prepend(str(ROOT / "scripts"))
    return runpy.run_path(str(ROOT / "scripts/diagnose_oct14_soar_format.py"))


class Policy:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.messages = []
        self.model = torch.nn.Linear(1, 1).requires_grad_(False)
        self.provenance = {"public_id": "cpu-fixture", "revision": "fixture-v1"}

    def generate(self, messages, **kwargs):
        self.messages.append(messages)
        response = next(self.responses)
        if isinstance(response, Exception):
            raise response
        return [response] * kwargs["samples"]


def test_soar_system_has_two_explicit_parser_legal_answer_templates():
    assert "<information_source>internal/external</information_source>" not in SYSTEM
    templates = re.findall(r"<information_source>.*?</answer>", SYSTEM)
    assert len(templates) == 2
    assert {parse_step(x)["source"] for x in templates} == {"internal", "external"}
    assert parse_step("<information_source>internal/external</information_source><answer>x</answer>") == {"kind": "invalid"}
    assert "<think>reasoning</think>" in SYSTEM and "<search>atomic query</search>" in SYSTEM


def test_soar_keeps_complete_actual_invalid_response_and_original_tokens(monkeypatch):
    n = probe(monkeypatch)
    response = GeneratedResponse((7, 8, 9), "literal invalid output", False)
    policy = Policy([response] * 8)
    f = n["diagnose_format"]
    monkeypatch.setitem(f.__globals__, "load_policy", lambda *_args, **_kwargs: policy)
    evidence = {}
    ledger = CostLedger()
    retriever = LexicalRetriever([{"text": "public text", "source_url": "https://example.org"}])
    f({}, [{"question": "public question", "answer": "PRIVATE_GOLD"}] * 4,
      retriever, ledger, evidence)
    assert ledger.calls == {"policy_trajectory": 8}
    for row in evidence["training_episode_audits"]:
        assert row["completed"] is True and row["final_action_kind"] == "invalid"
        turn = row["turns"][0]
        assert turn["response_text"] == response.text
        assert turn["response_token_ids"] == list(response.tokens)
        assert turn["response_text_sha256"] == hashlib.sha256(response.text.encode()).hexdigest()
        assert not turn["truncated"] and turn["generated_tokens"] == 3
    assert "PRIVATE_GOLD" not in json.dumps(evidence) and "PRIVATE_GOLD" not in str(policy.messages)
    assert evidence["optimizer_updates"] == 0 and evidence["assessment_executed"] is False


@pytest.mark.parametrize("next_policy_failure", [False, True])
def test_soar_partial_turn_survives_generation_exception_without_fabricated_completion(monkeypatch, next_policy_failure):
    n = probe(monkeypatch)
    response = GeneratedResponse((5, 6), "<think>lookup</think><search>public query</search>", False)
    responses = [response]
    if next_policy_failure:
        responses.append(GeneratedResponse((9,), "actual internal recall", False))
    responses.append(RuntimeError("fixture generation failure"))
    policy = Policy(responses)
    f = n["diagnose_format"]
    monkeypatch.setitem(f.__globals__, "load_policy", lambda *_args, **_kwargs: policy)
    evidence = {}
    ledger = CostLedger()
    retriever = LexicalRetriever([{"text": "public text", "source_url": "https://example.org"}])
    with pytest.raises(RuntimeError, match="fixture generation failure"):
        f({}, [{"question": "public question", "answer": "PRIVATE_GOLD"}] * 4,
          retriever, ledger, evidence)
    row = evidence["training_episode_audits"][0]
    assert row["completed"] is False and row["turns"][0]["response_text"] == response.text
    assert row["turns"][0]["response_token_ids"] == [5, 6]
    assert "answer" not in row and evidence["optimizer_updates"] == 0
    assert ledger.calls == ({"policy_trajectory": 1, "isolated_internal_recall": 1}
                            if next_policy_failure else {"policy_trajectory": 1})


def test_mbs_teacher_json_and_question_only_verification_store_actual_responses():
    teacher = Policy([
        GeneratedResponse((1, 2), '[{"question":"child","answer":2,"trace":"trace"}]', False),
        GeneratedResponse((3, 4), "\\boxed{99}", False),
        GeneratedResponse((5,), "\\boxed{7}", True),
    ])
    ledger = CostLedger()
    backend = mbs_checkpoint.CheckpointConstruction(teacher, Policy([]), ledger, teacher_attempts=2)
    parent = Problem("public parent", "7", "PRIVATE_PARENT_PLAN")
    assert len(backend.propose_children(parent, [])) == 1
    assert backend.verify(parent) is None
    assert ledger.calls == {"construction_teacher": 1, "construction_verification": 2}
    traces = backend.response_audits
    assert [x["role"] for x in traces] == ["construction_teacher", "construction_verification", "construction_verification"]
    assert traces[0]["operation"] == "propose_children"
    assert traces[0]["input_gold_scope"] == "training-construction-context"
    assert traces[1]["response_text"] == "\\boxed{99}" and traces[1]["response_token_ids"] == [3, 4]
    assert traces[1]["reject_reason"] == "incorrect_independent_solution"
    assert traces[2]["reject_reason"] == "truncated_independent_solution" and traces[2]["truncated"]
    assert all(x["input_gold_scope"] == "question-only-no-answer-or-trace" for x in traces[1:])
    assert "PRIVATE_PARENT_PLAN" in str(teacher.messages[0])
    assert "PRIVATE_PARENT_PLAN" not in str(teacher.messages[1:])


class Backend:
    def __init__(self, mode="ok"):
        self.mode = mode
        self.calls = []
        self.verify_counts = {}

    def verify(self, p):
        self.calls.append("verify")
        self.verify_counts[p.question] = self.verify_counts.get(p.question, 0) + 1
        if self.mode == "candidate-verify" and p.question.startswith("new"):
            return None
        return None if self.mode == "subtree" and p.question.startswith("child") and self.verify_counts[p.question] % 2 == 0 else p

    def student_rates(self, p, *, worked_examples, through_student=None):
        self.calls.append("rates")
        if self.mode == "threshold" and p.question.startswith("new"):
            return [0.9]
        return [0.5 if worked_examples and self.mode != "effectivity" else 0.]

    def propose_children(self, p, negative):
        self.calls.append("propose")
        if self.mode == "few":
            return [Problem("child-a", "2", "a")]
        return [Problem("child-a", "2", "a"), Problem("child-a" if self.mode == "duplicate" else "child-b", "3", "b")]

    def scaffold_safe(self, p, children):
        self.calls.append("safe")
        return self.mode != "unsafe"

    def harder_leaf(self, p):
        self.calls.append("harder")
        if self.mode == "missing":
            return None
        return p if self.mode == "same" else Problem("new child", "4", "new trace")

    def blueprint_and_novelty(self, original, candidate):
        self.calls.append("novelty")
        return self.mode != "novelty"


@pytest.mark.parametrize("mode,reason", [("few", "fewer_than_two_verified_children"),
    ("duplicate", "duplicate_or_parent_leaking_children"), ("unsafe", "unsafe_scaffold"),
    ("effectivity", "no_effectivity_improvement"), ("subtree", "child_decomposition_failed")])
def test_mbs_each_decomposition_continue_records_reason_without_extra_calls(mode, reason):
    backend = Backend(mode)
    builder = MagicBeanStalk(backend, decomposition_retries=2)
    assert builder.decompose(Problem("parent", "7", "parent trace")) is None
    rejected = [x for x in builder.audit if x.get("reject_reason") == reason]
    assert len(rejected) == 2
    assert backend.calls.count("propose") == 2
    if mode in {"few", "duplicate"}:
        assert "safe" not in backend.calls


@pytest.mark.parametrize("mode,reason", [("missing", "no_schema_valid_candidate"),
    ("same", "candidate_repeats_original_question"), ("novelty", "blueprint_or_novelty_rejected"),
    ("candidate-verify", "independent_verification_failed"), ("threshold", "weakest_success_exceeds_threshold")])
def test_mbs_synthesis_continue_records_specific_reject_reason(mode, reason):
    backend = Backend(mode)
    builder = MagicBeanStalk(backend, synthesis_retries=2)
    assert builder.synthesize(Node(Problem("original", "1", "trace"))) is None
    assert len([x for x in builder.audit if x.get("reject_reason") == reason]) == 2
    assert backend.calls.count("harder") == 2


def test_mbs_failed_run_payload_retains_real_backend_trace(monkeypatch):
    teacher = Policy([GeneratedResponse((8,), "\\boxed{99}", False)] * 2)
    student = Policy([GeneratedResponse((2,), "wrong", False)] * 2)
    monkeypatch.setattr(mbs_checkpoint, "load_split", lambda _c: ([{"question": "public", "answer": "7"}], [], {}))
    monkeypatch.setattr(mbs_checkpoint, "load_policy", lambda _c, role="student", **_kw: teacher if role == "teacher" else student)
    monkeypatch.setattr(mbs_checkpoint, "evaluate", lambda *_args, **_kwargs: {})
    with pytest.raises(ExecutionFailure) as error:
        mbs_checkpoint.run({"group": 2, "hard_root_limit": 1})
    traces = error.value.evidence["construction_response_audits"]
    assert len(traces) == 4  # two actual calibration outputs + two verification outputs
    assert [x["role"] for x in traces] == ["target_calibration"] * 2 + ["construction_verification"] * 2
    assert error.value.evidence["hard_root_selection"]["paired_rl_root_indices"] == []


def test_mbs_interrupted_construction_keeps_only_already_executed_response_trace(monkeypatch):
    teacher = Policy([RuntimeError("fixture generation interrupted")])
    student = Policy([GeneratedResponse((2,), "wrong", False)] * 2)
    monkeypatch.setattr(mbs_checkpoint, "load_split", lambda _c: ([{"question": "public", "answer": "7"}], [], {}))
    monkeypatch.setattr(mbs_checkpoint, "load_policy", lambda _c, role="student", **_kw: teacher if role == "teacher" else student)
    monkeypatch.setattr(mbs_checkpoint, "evaluate", lambda *_args, **_kwargs: {})
    with pytest.raises(ExecutionFailure) as error:
        mbs_checkpoint.run({"group": 2, "hard_root_limit": 1})
    assert error.value.evidence["error_type"] == "RuntimeError"
    assert len(error.value.evidence["construction_response_audits"]) == 2
    assert all(x["role"] == "target_calibration" for x in error.value.evidence["construction_response_audits"])
    assert error.value.evidence["cost"]["generation_calls"] == {"target_calibration": 1}


@pytest.mark.parametrize("text,truncated,reason", [("not JSON", False, "no_json_value"),
    ('[{"question":"child","answer":2,"trace":"trace"}]', True, "truncated_json_response")])
def test_mbs_json_failure_records_actual_output_without_accepting_prefix(text, truncated, reason):
    response = GeneratedResponse((10, 11), text, truncated)
    ledger = CostLedger()
    backend = mbs_checkpoint.CheckpointConstruction(Policy([response]), Policy([]), ledger)
    assert backend.propose_children(Problem("parent", "7", "trace"), []) == []
    audit = backend.response_audits[0]
    assert audit["response_text"] == text and audit["response_token_ids"] == [10, 11]
    assert audit["reject_reason"] == reason and audit["schema_valid_problem_count"] == 0
    assert ledger.calls == {"construction_teacher": 1}


def test_mbs_operation_is_audit_only_and_does_not_change_prompt_or_budget():
    response = GeneratedResponse((1,), '{"ok":true}', False)
    teacher = Policy([response, response])
    ledger = CostLedger()
    backend = mbs_checkpoint.CheckpointConstruction(teacher, Policy([]), ledger, max_tokens=768)
    assert backend.teacher_json("same instruction", {"parent": "training context"}, operation="first") == {"ok": True}
    assert backend.teacher_json("same instruction", {"parent": "training context"}, operation="second") == {"ok": True}
    assert teacher.messages[0] == teacher.messages[1]
    assert [x["operation"] for x in backend.response_audits] == ["first", "second"]
    assert ledger.calls == {"construction_teacher": 2}


def test_mbs_actual_final_goldilocks_rejection_keeps_reason_and_outcomes():
    backend = Backend()
    backend.target_outcomes = lambda _p: ([0, 0], [False, False])
    builder = MagicBeanStalk(backend)
    builder.decompose = lambda p: Node(p)
    builder.synthesize = lambda _node: Problem("new synthetic", "2", "new trace")
    assert builder.construct(Problem("hard", "7", "trace")) is None
    audit = builder.audit[-1]
    assert audit["reject_reason"] == "target_policy_not_goldilocks"
    assert audit["rewards"] == [0, 0] and audit["truncated"] == [False, False]
