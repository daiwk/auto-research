import math

import pytest

from auto_research.agent_research.google16_polca import Candidate, Polca, epsilon_filter


def candidate(key, x):
    return Candidate(key, f"parameter {key}", (float(x),))


def test_farthest_first_net_strict_boundary_and_proposals_filter_each_other():
    base = candidate("base", 0)
    proposals = [candidate("near", .1), candidate("far", 2), candidate("nearfar", 2.1),
                 candidate("boundary", 1)]
    accepted = epsilon_filter(proposals, [base], epsilon=1)
    assert [c.key for c in accepted] == ["nearfar"]
    assert epsilon_filter([candidate("a", 1)], [base], epsilon=1) == ()
    assert len(epsilon_filter(proposals, [base], epsilon=0)) == 4


def test_same_minibatch_history_summary_and_empirical_mean_not_best_score():
    controller = Polca(candidate("base", 0), epsilon=.1, seed=42)
    events = []

    def evaluate(c, value):
        events.append((c.key, value))
        return value + (1 if c.key == "new" else 0), f"observed {value}"

    def summarize(history):
        assert len(history[0].observations) == 2
        return "actual callback result, unit fixture only"

    def propose(history, summary):
        assert history[0].observations and summary.startswith("actual")
        return [candidate("new", 2)]

    trace = controller.round([("v1", 0), ("v2", 4)], evaluator=evaluate,
                             summarizer=summarize, proposer=propose, batch_size=2)
    assert [v for k, v in events if k == "base"] == [v for k, v in events if k == "new"]
    assert trace.admitted == ("new",) and trace.metric_calls == 4
    assert controller.best().candidate.key == "new"
    assert all(x.item_id in {"v1", "v2"} for h in controller.histories() for x in h.observations)


def test_stochastic_feedback_averaged_and_variance_preserved_across_rounds():
    controller = Polca(candidate("base", 0), epsilon=.1)
    values = iter([10., -10.])
    kwargs = dict(evaluator=lambda c, x: (next(values), "noisy"),
                  summarizer=lambda h: "fixture", proposer=lambda h, s: [], batch_size=1)
    controller.round([("v", None)], **kwargs)
    controller.round([("v", None)], **kwargs)
    history = controller.best()
    assert history.mean == 0 and history.sample_variance == 200
    assert len(history.observations) == 2


def test_budget_exhaustion_keeps_deferred_proposal_distinct_from_evaluated():
    controller = Polca(candidate("base", 0), epsilon=.1, max_metric_calls=2)
    trace = controller.round([("v", 0)], evaluator=lambda c, x: (0., "fixture"),
                             summarizer=lambda h: "fixture",
                             proposer=lambda h, s: [candidate("new", 5)], batch_size=2)
    assert trace.deferred_budget == ("new",) and trace.admitted == ()
    assert "new" not in controller.memory and controller.calls == 2
    with pytest.raises(RuntimeError):
        controller.round([("v", 0)], evaluator=None, summarizer=None, proposer=None)


def test_test_split_nonfinite_embeddings_and_duplicate_ids_rejected():
    with pytest.raises(ValueError):
        Candidate("x", "x", (math.nan,))
    with pytest.raises(ValueError):
        epsilon_filter([candidate("x", 1)], [candidate("x", 0)], epsilon=.1)
    controller = Polca(candidate("base", 0), epsilon=.1)
    with pytest.raises(ValueError):
        controller.round([("test", 0)], evaluator=None, summarizer=None, proposer=None, split="test")
