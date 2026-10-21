from dataclasses import asdict
import math

import pytest

from auto_research.agent_research.google16_causal_armor import (
    CachedLikelihoodScorer, Turn, attribute, guard, render_context,
)


class Scorer:
    def __init__(self, scores=(-2., -4., -10., -3.)):
        self.scores = scores
        self.contexts = None

    def score_batch(self, contexts, action):
        self.contexts = contexts
        assert action == "write"
        return self.scores, 2


def context():
    return (Turn("system", "policy"), Turn("user", "request"),
            Turn("tool", "injection", True), Turn("assistant", "contaminated"),
            Turn("tool", "fact", True), Turn("assistant", "more reasoning"))


def test_equations_normalize_by_action_not_input_length_and_omit_one_span():
    scorer = Scorer()
    result = attribute(context(), "write", scorer)
    assert result.user_influence == 1
    assert result.span_influences == ((2, 4), (4, .5))
    assert result.flagged_indices == (2,)
    assert result.action_tokens == 2 and result.scoring_contexts == 4
    assert all(Turn("system", "policy") in x for x in scorer.contexts)
    assert not any(t.role == "user" for t in scorer.contexts[1])
    assert Turn("tool", "fact", True) in scorer.contexts[2]
    assert Turn("tool", "injection", True) not in scorer.contexts[2]


def test_tau_sign_strict_boundary_and_low_user_alone_not_sufficient():
    scorer = Scorer((-2., -2., -2., -2.))
    assert not attribute(context(), "write", scorer, tau=0).flagged_indices
    assert attribute(context(), "write", scorer, tau=.1).flagged_indices == (2, 4)
    assert not attribute(context(), "write", Scorer(), tau=-10).flagged_indices


def test_flag_without_actual_callbacks_is_withheld_not_security_success():
    result = guard(context(), "write", Scorer(), privileged=True)
    assert result.status == "intervention_required" and result.action is None
    assert not result.sanitizer_observed and not result.regeneration_observed


def test_sanitizer_is_selective_and_all_post_first_hit_assistant_reasoning_masked():
    calls = []

    def sanitize(user, action, span):
        calls.append((user, action, span))
        return "delivery Friday"

    def regenerate(turns):
        assert turns[2].content == "delivery Friday"
        assert turns[4].content == "fact"
        assert turns[3].content == "[Reasoning redacted for security]"
        assert turns[5].content == "[Reasoning redacted for security]"
        return "read"

    result = guard(context(), "write", Scorer(), privileged=True,
                   sanitizer=sanitize, regenerate=regenerate)
    assert calls == [("request", "write", "injection")]
    assert result.action == "read" and result.status == "regenerated_not_executed"
    assert context()[2].content == "injection"  # immutable input


def test_nonprivileged_path_does_not_invoke_scorer():
    scorer = Scorer()
    assert guard(context(), "write", scorer, privileged=False).status == "not_checked"
    assert scorer.contexts is None


def test_invalid_scores_and_context_fail_closed():
    for scores in [(-2,), (-2, -4, math.nan, -3)]:
        with pytest.raises(ValueError):
            attribute(context(), "write", Scorer(scores))
    with pytest.raises(ValueError):
        attribute((Turn("tool", "x", True),), "write", Scorer())
    with pytest.raises(ValueError):
        Turn("assistant", "x", True)
    with pytest.raises(ValueError):
        CachedLikelihoodScorer("/nonexistent", revision="main")


def test_explicit_context_render_has_no_hidden_gold():
    data = asdict(context()[1])
    assert set(data) == {"role", "content", "untrusted"}
    assert render_context((Turn("user", "request"),)) == "[user]\nrequest\n[assistant action]\n"
