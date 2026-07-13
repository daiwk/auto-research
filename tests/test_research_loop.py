import json

from auto_research.research_loop import (
    IterativeResearchLoop,
    ResearchJournal,
    ResearchStage,
    TrialCache,
)


def test_iterative_loop_reuses_completed_trial(tmp_path):
    calls = []

    def evaluate(params):
        calls.append(params)
        return params["score"]

    cache = TrialCache(tmp_path / "cache")
    context = {"track": "recommendation", "experiment": "unit", "seed": 42}
    proposals = [{"score": 2.0}, {"score": 1.0}]
    first = IterativeResearchLoop(evaluate, "minimize", cache, context)
    first_trials, first_best = first.run(proposals)
    second = IterativeResearchLoop(evaluate, "minimize", cache, context)
    second_trials, second_best = second.run(proposals)

    assert len(calls) == 2
    assert [trial.status for trial in first_trials] == ["completed", "completed"]
    assert [trial.status for trial in second_trials] == ["cached", "cached"]
    assert first_best.metric == second_best.metric == 1.0


def test_failed_trial_is_not_cached(tmp_path):
    calls = 0

    def evaluate(_params):
        nonlocal calls
        calls += 1
        raise RuntimeError("expected")

    cache = TrialCache(tmp_path / "cache")
    loop = IterativeResearchLoop(evaluate, "maximize", cache, {"experiment": "bad"})
    first, _ = loop.run([{"x": 1}])
    second, _ = loop.run([{"x": 1}])

    assert calls == 2
    assert first[0].status == second[0].status == "failed"


def test_research_journal_is_append_only_jsonl(tmp_path):
    journal = ResearchJournal(tmp_path / "events.jsonl", "run-1")
    journal.record(ResearchStage.DISCOVERY, "started", topic="ranking")
    journal.record(ResearchStage.COMPLETE, "completed")

    entries = [json.loads(line) for line in journal.path.read_text().splitlines()]
    assert [entry["event"] for entry in entries] == ["started", "completed"]
    assert entries[0]["payload"]["topic"] == "ranking"


def test_adaptive_proposer_can_use_prior_result():
    class Proposer:
        def propose(self, history):
            if not history:
                return {"value": 4.0}
            if len(history) == 1:
                return {"value": history[-1].metric / 2}
            return None

    trials, best = IterativeResearchLoop(
        lambda params: params["value"], "minimize"
    ).run(Proposer())

    assert [trial.metric for trial in trials] == [4.0, 2.0]
    assert best.metric == 2.0
