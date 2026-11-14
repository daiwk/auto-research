"""SGP v1 Eq.2–4 offline reward/selection, not a dialogue actor or ReST trainer."""
from dataclasses import dataclass
import math
from numbers import Real

REQUIRES_GPU_VALIDATION = False
_SEQUENCES = {("answer",), ("multi_answer",), ("clarify", "answer"), ("clarify", "multi_answer")}


def _number(value, name, *, unit=False):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value) or value < 0:
        raise ValueError(f"finite nonnegative {name} required")
    if unit and value > 1:
        raise ValueError(f"{name} must be in [0,1]")


@dataclass(frozen=True)
class Rollout:
    identity: str
    interpretation: str
    actions: tuple[str, ...]
    accuracy: float
    final_assistant_words: int
    user_answer_overlap: float

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (self.identity, self.interpretation)):
            raise ValueError("rollout and interpretation identities required")
        if not isinstance(self.actions, tuple) or not all(isinstance(x, str) for x in self.actions) or self.actions not in _SEQUENCES:
            raise ValueError("v1 action sequence with at most one clarification required")
        _number(self.accuracy, "externally evaluated accuracy", unit=True)
        _number(self.user_answer_overlap, "user-answer overlap", unit=True)
        if type(self.final_assistant_words) is not int or self.final_assistant_words < 0:
            raise ValueError("nonnegative final assistant word count required")


def reward(rollout: Rollout, alpha: float, beta: float) -> float:
    """Reward points: normalized F1 becomes100*F1 before paper cost subtraction.

    Filter thresholds remain normalized (e.g.0.1/0.4). Paper Tables2–3 report
    F1/reward on the percentage-point scale and alpha2/20, beta0.1/0.7/5.
    Dividing both reward and coefficients by100 gives an equivalent convention.
    """
    if not isinstance(rollout, Rollout):
        raise ValueError("typed externally evaluated rollout required")
    _number(alpha, "clarification cost")
    _number(beta, "word cost")
    return 100 * rollout.accuracy - alpha * rollout.actions.count("clarify") - beta * rollout.final_assistant_words


def select_rollouts(rollouts, interpretations, *, alpha, beta, minimum_accuracy):
    """Uniform interpretation means, then per-interpretation best compatible row.

    Missing interpretation coverage cannot estimate Eq.3 and excludes that action
    sequence. Ties use lexical sequence/identity order, a local convention. Only
    offline evaluated records enter here; no labels enter an evaluated actor.
    """
    _number(minimum_accuracy, "accuracy threshold", unit=True)
    interpretations = tuple(interpretations)
    if not interpretations or any(not isinstance(i, str) or not i.strip() for i in interpretations) or len(set(interpretations)) != len(interpretations):
        raise ValueError("unique nonempty interpretation set required")
    rows = tuple(rollouts)
    if any(not isinstance(row, Rollout) for row in rows) or len({r.identity for r in rows}) != len(rows):
        raise ValueError("typed uniquely identified rollouts required")
    if any(row.interpretation not in interpretations for row in rows):
        raise ValueError("rollout interpretation outside declared set")
    valid = [r for r in rows if r.accuracy >= minimum_accuracy and r.user_answer_overlap >= .5]
    scores = {}
    for sequence in sorted({r.actions for r in valid}):
        groups = [[r for r in valid if r.actions == sequence and r.interpretation == i] for i in interpretations]
        if all(groups):
            scores[sequence] = sum(sum(reward(r, alpha, beta) for r in g) / len(g) for g in groups) / len(groups)
    if not scores:
        raise ValueError("no valid action sequence covers all interpretations")
    best = min(scores, key=lambda sequence: (-scores[sequence], sequence))
    chosen = tuple(min((r for r in valid if r.actions == best and r.interpretation == i),
                       key=lambda r: (-reward(r, alpha, beta), r.identity)) for i in interpretations)
    return {"action_sequence":best, "expected_reward":scores[best], "selected":chosen,
            "valid_rollouts":len(valid), "sequence_rewards":scores}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only selection required")
    rows = [Rollout("a", "i1", ("answer",), 1., 2, 1.),
            Rollout("b", "i2", ("answer",), 0., 2, 1.),
            Rollout("c", "i1", ("clarify", "answer"), .9, 2, 1.),
            Rollout("d", "i2", ("clarify", "answer"), .9, 2, 1.)]
    low = select_rollouts(rows, ("i1", "i2"), alpha=2., beta=0., minimum_accuracy=0.)
    high = select_rollouts(rows, ("i1", "i2"), alpha=80., beta=0., minimum_accuracy=0.)
    checks = {"cost_changes_selected_sequence":low["action_sequence"] != high["action_sequence"],
              "balanced_not_lucky_max":low["action_sequence"] == ("clarify", "answer"),
              "one_best_per_interpretation":len(low["selected"]) == 2,
              "word_cost_uses_final_assistant_only":math.isclose(reward(rows[0], 0., .1), 99.8),
              "paper_cost_points_not_normalized_f1":low["expected_reward"] == 88.}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "metrics":{"low_cost_expected_reward":low["expected_reward"],"high_cost_expected_reward":high["expected_reward"],"selected_rollouts":2}}
