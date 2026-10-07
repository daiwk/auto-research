import json

import pytest

from auto_research.agent_research.frugalevo import (
    Candidate, Completion, FrugalEvo, IslandArchive, SearchConfig, budget_auc,
)
from auto_research.agent_research.program_sandbox import packing_score
from auto_research.agent_research.sentry import Diagnosis, Lesson, PublicStep, Sentry, retrieve


def test_sentry_no_failure_never_exposes_memory():
    calls = []
    def model(role, prompt):
        calls.append((role, prompt))
        return '{"intervene":false}'
    monitor = Sentry(model, playbook=(Lesson("progress", ("repetition",), "TRIGGER", "SECRET_LESSON", 1),))
    monitor.start_task("public objective", "schema")
    assert monitor.observe(PublicStep("inspect", "search", "new result")) is None
    assert len(calls) == 1
    assert "SECRET_LESSON" not in calls[0][1]
    with pytest.raises(TypeError):
        monitor.observe({"answer": "gold"})


def test_sentry_hard_repair_does_not_create_lessons():
    monitor = Sentry(lambda *_: pytest.fail("invalid actions must not invoke soft detector"))
    monitor.start_task("public task", "{tool: str}")
    prompt = monitor.observe(PublicStep("", "{", "malformed call", parsed_ok=False))
    assert "schema" in prompt.lower()
    monitor.finalize()
    assert not monitor.playbook


def test_sentry_only_verified_recovery_updates_and_horizon_is_respected():
    calls = []
    def model(role, prompt):
        calls.append((role, prompt))
        return {
            "detect": '{"intervene":true,"category":"progress","labels":["repetition"],"evidence":"same empty query"}',
            "verify": '{"resolved":true,"evidence":"revised query returned new relevant evidence"}',
            "summarize": '{"trigger":"repeated empty query","principle":"change a query constraint"}',
        }[role]
    monitor = Sentry(model, horizon=2)
    monitor.start_task("find evidence", "schema")
    assert monitor.observe(PublicStep("retry", "search", "empty"))
    monitor.observe(PublicStep("change", "search other", "new evidence"))
    assert not monitor.playbook
    assert [role for role, _ in calls] == ["detect"]
    monitor.observe(PublicStep("inspect", "read", "details"), terminal=True)
    assert len(monitor.playbook) == 1
    assert [role for role, _ in calls] == ["detect", "verify", "summarize"]
    assert all("benchmark_reward" not in prompt and "gold_answer" not in prompt for _, prompt in calls)


@pytest.mark.parametrize("verdict,learning", [('{"resolved":false,"evidence":"still looping"}', True),
                                             ('{"resolved":"true","evidence":"new"}', True),
                                             ('{"resolved":true,"evidence":"new"}', False)])
def test_sentry_no_unverified_or_frozen_writes(verdict, learning):
    def model(role, prompt):
        if role == "detect":
            return '{"intervene":true,"category":"progress","labels":["repetition"],"evidence":"loop"}'
        if role == "verify":
            return verdict
        pytest.fail("summarizer must not run")
    monitor = Sentry(model, horizon=1, learning=learning)
    monitor.observe(PublicStep("r", "a", "o"))
    monitor.observe(PublicStep("r", "a", "o"), terminal=True)
    assert not monitor.playbook


def test_sentry_label_overlap_recency_and_diversity():
    book = [Lesson("progress", ("repetition",), str(i), "vary", i) for i in range(6)]
    book += [Lesson("progress", ("planning_stall", "repetition"), "stall", "act", 9),
             Lesson("grounding", ("hallucination",), "bad claim", "inspect", 10)]
    chosen = retrieve(book, Diagnosis("progress", ("repetition",), "loop"), 3)
    assert [row.insertion_step for row in chosen] == [9, 5, 4]
    assert retrieve(book, Diagnosis("grounding", ("objective_drift",), "drift"))[0].insertion_step == 10


class ScriptedGenerator:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.prompts = []
    def upper_cost(self, prompt, max_tokens):
        return 1
    def generate(self, prompt, max_tokens, seed):
        self.prompts.append(prompt)
        return Completion(next(self.responses), 1, 1, 1)


def test_frugalevo_real_evaluator_pilots_ranking_and_fixed_parent():
    weak = ScriptedGenerator(["cold", "pilotA", "pilotB", "bad1", "bad2", "better", "bad3", "bad4"])
    strong = ScriptedGenerator(["analysis", '["A","B"]'])
    scores = dict(initial=1, cold=1, pilotA=2, pilotB=3, bad1=0, bad2=0, better=4, bad3=0, bad4=0)
    evaluated = []
    def evaluator(code):
        evaluated.append(code)
        return Candidate(code, scores[code], "measured:" + code)
    result = FrugalEvo(strong, weak, evaluator, SearchConfig(budget=10, strategies=2)).run("task", "initial")
    assert result["best"]["code"] == "better"
    assert result["spent"] == 10
    assert len(evaluated) == 9  # initial + eight actually executed candidates
    assert "PARENT:\ninitial" in weak.prompts[1] and "PARENT:\ninitial" in weak.prompts[2]
    assert weak.prompts[4].startswith(weak.prompts[3])  # append-only failure feedback
    assert result["candidates"][4]["strategy"] == "B"  # pilot B ranks first
    assert "PARENT:\nbetter" in weak.prompts[-1]


def test_frugalevo_rejects_overbudget_call_and_counts_bad_strategy():
    weak = ScriptedGenerator(["no_gain"])
    strong = ScriptedGenerator(["analysis", "not JSON"])
    result = FrugalEvo(strong, weak, lambda c: Candidate(c, 1, "ok"),
                      SearchConfig(budget=3)).run("task", "initial")
    assert result["spent"] == 3 and len(result["calls"]) == 3
    assert result["best"]["code"] == "initial"
    assert budget_auc([(0, 1), (2, 3), (9, 50)], 5) == 11


def test_archive_keeps_cell_elite_and_distinct_islands():
    archive = IslandArchive(islands=2, bins=1)
    for code, score in [("a", 1), ("b", 2), ("c", 0), ("d", 3)]:
        archive.add(Candidate(code, score, "ok"))
    assert [next(iter(row.values())).score for row in archive.islands] == [1, 3]


def test_packing_score_does_not_trust_claimed_score():
    payload = {"centers": [[(i % 6 + .5) / 6, (i // 6 + .5) / 6] for i in range(26)],
               "radii": [1 / 12] * 26, "score": 1e9}
    assert packing_score(payload) == pytest.approx(26 / 12)
    payload["radii"][0] = float("nan")
    with pytest.raises(ValueError, match="finite"):
        packing_score(payload)
    payload["radii"][0] = 0.3
    with pytest.raises(ValueError):
        packing_score(payload)
    with pytest.raises(ValueError):
        packing_score(json.loads('{"centers":[],"radii":[]}'))


def test_sentry_public_case_strips_labels_and_scorer_stays_outside():
    from auto_research.agent_research.sentry_public import public_case, run_episode
    row = {"id": "task", "question": "Where?", "answer": "SECRET GOLD",
           "supporting_facts": {"title": ["PRIVATE PLAN"]},
           "context": {"title": ["Doc"], "sentences": [["Public evidence."]]}}
    case = public_case(row)
    assert set(case) == {"id", "question", "documents"}
    prompts = []
    def generate(prompt, maximum, seed):
        prompts.append(prompt)
        if len(prompts) == 1:
            return Completion('{"reasoning":"inspect","action":"read","argument":"Doc"}', 1, 1, 1)
        return Completion('{"reasoning":"observed","action":"finish","argument":"guess"}', 1, 1, 1)
    result = run_episode(case, generate, sentry=None, seed=42)
    assert result["prediction"] == "guess"
    assert "exact_match" not in result
    assert all("SECRET GOLD" not in prompt and "PRIVATE PLAN" not in prompt for prompt in prompts)
    with pytest.raises(ValueError, match="public-case"):
        run_episode({**case, "answer": "gold"}, generate, sentry=None, seed=42)


def test_sentry_action_schema_is_real_enum_not_literal_union():
    from auto_research.agent_research.sentry_public import ACTION_SCHEMA
    schema = json.loads(ACTION_SCHEMA)
    assert schema["properties"]["action"]["enum"] == ["search", "read", "finish"]
    assert "search|read|finish" not in ACTION_SCHEMA


@pytest.mark.parametrize("field,value", [("evidence", None), ("category", []), ("labels", [{}])])
def test_sentry_malformed_detector_types_fail_closed(field, value):
    result = {"intervene": True, "category": "progress", "labels": ["repetition"], "evidence": "loop"}
    result[field] = value
    monitor = Sentry(lambda *_: json.dumps(result))
    assert monitor.observe(PublicStep("r", "a", "o")) is None
    assert monitor.events[-1]["event"] == "invalid_detection"
    assert not monitor.playbook


def test_public_tool_requires_observed_evidence_but_never_checks_answer():
    from auto_research.agent_research.sentry_public import RetrievalEnvironment
    env = RetrievalEnvironment({"Doc": "Some public text."})
    assert env.execute("finish", "anything")[1:] == (False, False)
    assert env.execute("read", "Doc")[1:] == (True, False)
    assert env.execute("finish", "not a correct answer")[1:] == (True, True)
