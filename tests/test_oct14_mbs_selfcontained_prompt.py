"""Generic construction prompt contracts; CPU fixtures are not GPU evidence."""
import json

from auto_research.post_training.oct13_common import CostLedger
from auto_research.post_training.response_policy import GeneratedResponse
from auto_research.reproductions.magicbeanstalk.algorithm import Problem
from auto_research.reproductions.magicbeanstalk.checkpoint import CheckpointConstruction


class RecordingPolicy:
    def __init__(self, texts):
        self.texts = iter(texts)
        self.calls = []

    def generate(self, messages, **kwargs):
        self.calls.append((messages, kwargs))
        return [GeneratedResponse((1,), next(self.texts), False)] * kwargs["samples"]


def test_child_contract_is_generic_and_explicit_without_extra_sampling():
    teacher = RecordingPolicy(["[]"])
    ledger = CostLedger()
    backend = CheckpointConstruction(teacher, None, ledger, max_tokens=1024, teacher_attempts=2)
    assert backend.propose_children(Problem("ABSTRACT_PARENT", "SECRET_ANSWER", "SECRET_TRACE"), []) == []
    text = teacher.calls[0][0][0]["content"]
    instruction, context = text.split("\nOutput JSON only, without prose or code fences.\n")
    assert "quantity, unit, time interval, relation and assumption" in instruction
    assert "without the parent, other children, or the answer/trace fields" in instruction
    assert "complete step-by-step trace using only that question" in instruction
    assert "exactly one concise numerical final answer" in instruction
    assert "Do not disclose the parent final answer" in instruction
    assert "array of objects, not an array of strings" in instruction
    assert "Escape newlines and backslashes" in instruction
    assert not any(x in instruction for x in ("ABSTRACT_PARENT", "SECRET_ANSWER", "SECRET_TRACE", "James", "624"))
    assert json.loads(context)["parent"]["answer"] == "SECRET_ANSWER"  # train construction role only
    assert teacher.calls[0][1] == {"samples": 1, "max_tokens": 1024, "sample": True}
    assert ledger.calls == {"construction_teacher": 1}


def test_complete_children_keep_existing_schema_and_worked_trace():
    children = [{"question": "A machine makes four units each hour for two hours. How many units?",
                 "answer": "8", "trace": "Multiply four units per hour by two hours to obtain eight units."},
                {"question": "A worker produces five units each day for three days. How many units?",
                 "answer": "15", "trace": "Multiply five units per day by three days to obtain fifteen units."}]
    teacher = RecordingPolicy([json.dumps(children)])
    backend = CheckpointConstruction(teacher, None, CostLedger())
    actual = backend.propose_children(Problem("parent", "PRIVATE", "PLAN"), [])
    assert [vars(p) for p in actual] == children


def test_missing_facts_are_not_repaired_with_parent_gold_or_autoaccepted():
    teacher = RecordingPolicy([json.dumps([{"question": "How many units in a year?", "answer": "999",
                                           "trace": "SECRET_PARENT_TRACE"}]), "\\boxed{1}", "\\boxed{2}"])
    ledger = CostLedger()
    backend = CheckpointConstruction(teacher, None, ledger, max_tokens=1024, teacher_attempts=2)
    child = backend.propose_children(Problem("SECRET_PARENT_FACTS", "999", "SECRET_PARENT_TRACE"), [])[0]
    assert backend.verify(child) is None
    assert len(teacher.calls) == 3
    for messages, kwargs in teacher.calls[1:]:
        content = str(messages)
        assert "How many units in a year?" in content
        assert not any(x in content for x in ("SECRET_PARENT_FACTS", "SECRET_PARENT_TRACE", "999"))
        assert kwargs["max_tokens"] == 1024 and kwargs["samples"] == 1
    assert ledger.calls == {"construction_teacher": 1, "construction_verification": 2}
    assert all(not a["accepted"] for a in backend.response_audits[1:])


def test_malformed_array_is_not_repaired_or_promoted_from_partial_objects():
    text = '[{"question":"child","answer":"8","trace":"first\nsecond"}]'
    teacher = RecordingPolicy([text])
    ledger = CostLedger()
    backend = CheckpointConstruction(teacher, None, ledger)
    assert backend.propose_children(Problem("parent", "PRIVATE", "TRACE"), []) == []
    assert backend.response_audits[0]["response_text"] == text
    assert backend.response_audits[0]["schema_valid_problem_count"] == 0
    assert ledger.calls == {"construction_teacher": 1}
