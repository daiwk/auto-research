"""Co-Director factored UCB arithmetic over external video evaluations.

Uses the linked author's UCBBandit formula and recommendation-first unpulled
arms. It supplies no LLM warm-start values, video generation or quality judge.
"""
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = False
AXES = {
    "strategy":("informational", "transformational", "comparative"),
    "narrative":("analytical", "vignette", "narrative_drama"),
    "aesthetic":("clarity_energy", "cinematic_premium", "minimalist_focus", "kinetic_grit"),
}


def _number(value, *, score=False):
    if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value) or value < 0 or (score and value > 100):
        raise ValueError("finite nonnegative value (score in [0,100]) required")


@dataclass(frozen=True)
class VideoEvaluation:
    identity: str
    choices: tuple[str, str, str]
    strategic_rewards: tuple[float, float, float]
    quality: float

    def __post_init__(self):
        if not isinstance(self.identity, str) or not self.identity.strip() or not isinstance(self.choices, tuple) or len(self.choices) != 3:
            raise ValueError("video identity and three selected categorical arms required")
        if not isinstance(self.strategic_rewards, tuple) or len(self.strategic_rewards) != 3:
            raise ValueError("three explicit factored strategic rewards required")
        for value in (*self.strategic_rewards, self.quality):
            _number(value, score=True)
        if any(choice not in arms for choice, arms in zip(self.choices, AXES.values())):
            raise ValueError("selected creative direction outside fixed paper axes")


class FactoredUCB:
    def __init__(self, *, seed: int, exploration=2., recommendations=None):
        if type(seed) is not int:
            raise ValueError("integer seed required")
        _number(exploration)
        recommendations = {} if recommendations is None else dict(recommendations)
        if any(axis not in AXES or arm not in AXES[axis] for axis, arm in recommendations.items()):
            raise ValueError("external recommendation outside fixed axes")
        self.exploration, self.recommendations = exploration, recommendations
        self._random = random.Random(seed)
        self._stats = {axis:{arm:[] for arm in arms} for axis, arms in AXES.items()}
        self._history: list[VideoEvaluation] = []

    def select(self):
        choices = []
        for axis, arms in AXES.items():
            unpulled = [arm for arm in arms if not self._stats[axis][arm]]
            if unpulled:
                recommended = self.recommendations.get(axis)
                choices.append(recommended if recommended in unpulled else self._random.choice(unpulled))
            else:
                total = sum(len(rewards) for rewards in self._stats[axis].values())
                values = {arm:sum(self._stats[axis][arm])/len(self._stats[axis][arm])
                          + self.exploration*math.sqrt(math.log(total)/len(self._stats[axis][arm])) for arm in arms}
                # Paper does not prescribe ties; use fixed categorical order.
                choices.append(max(arms, key=lambda arm:values[arm]))
        return tuple(choices)

    def update(self, result: VideoEvaluation):
        if not isinstance(result, VideoEvaluation) or any(row.identity == result.identity for row in self._history):
            raise ValueError("new typed externally evaluated video required")
        for axis, arm, reward in zip(AXES, result.choices, result.strategic_rewards):
            self._stats[axis][arm].append(reward)
        self._history.append(result)

    def statistics(self):
        return {axis:{arm:{"pulls":len(values),"mean":sum(values)/len(values) if values else None}
                      for arm, values in arms.items()} for axis, arms in self._stats.items()}

    def best_video(self):
        if not self._history:
            raise ValueError("no externally evaluated video exists")
        return max(self._history, key=lambda row:row.quality)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only arithmetic required")
    warm = {axis:arms[0] for axis, arms in AXES.items()}
    bandit = FactoredUCB(seed=seed, recommendations=warm)
    first = bandit.select()
    bandit.update(VideoEvaluation("fixture:first", first, (10.,20.,30.), 90.))
    second = bandit.select()
    bandit.update(VideoEvaluation("fixture:second", second, (90.,80.,70.), 40.))
    stats = bandit.statistics()
    checks = {"recommendation_first_unpulled":first == tuple(warm.values()),
              "unpulled_explored_before_ucb":all(a != b for a,b in zip(first,second)),
              "factor_specific_update":stats["strategy"][first[0]]["mean"] == 10. and stats["aesthetic"][first[2]]["mean"] == 30.,
              "quality_selection_not_strategic_sum":bandit.best_video().identity == "fixture:first",
              "three_axes_not36_joint_paths":sum(len(arms) for arms in AXES.values()) == 10}
    return {"seed":seed,"diagnostic_only":True,"evaluation_tier":"l1_mechanism","checks":checks,
            "metrics":{"external_evaluation_fixtures":2,"factored_arm_count":10,"best_fixture_quality":90.}}
