"""Hierarchy consensus/recognition and information utility, fixed-v1 §3.

Parsing and Wikidata grounding are external; gold is used only by utility.
"""

from collections import Counter
import math
from ._nov18_contracts import receipt, scalar

REQUIRES_GPU_VALIDATION = False


def consensus_target(paths, *, required=16, expected_samples=20):
    """Paths are normalized fine-to-coarse tuples, or None for unusable parses."""
    if (
        type(required) is not int
        or type(expected_samples) is not int
        or not 1 <= required <= expected_samples
        or len(paths) != expected_samples
    ):
        raise ValueError("declared sample count and consensus threshold required")
    usable = [tuple(p) for p in paths if p is not None]
    if len(usable) < required:
        return {"status": "exclude", "level": None, "value": None}
    if not usable[0] or any(len(p) != len(usable[0]) for p in usable):
        raise ValueError("fixed hierarchy depth required")
    for level in range(len(usable[0])):
        votes = Counter(p[level] for p in usable if p[level] is not None)
        passing = [value for value, count in votes.items() if count >= required]
        if passing:
            return {"status": "answer", "level": level, "value": passing[0]}
    return {"status": "abstain", "level": None, "value": None}


def recognition_target(answer_scores, distractor_scores):
    a = tuple(answer_scores)
    ds = tuple(tuple(x) for x in distractor_scores)
    if (
        not a
        or len(a) != len(ds)
        or any(not d for d in ds)
        or any(not math.isfinite(v) for v in a + tuple(v for d in ds for v in d))
    ):
        raise ValueError("finite answer and level-matched distractor scores required")
    passed = [x > max(d) for x, d in zip(a, ds)]
    for level in range(len(a)):
        if all(passed[level:]):
            return level
    return None


def information_utility(
    *, prior_uncertainty, level_uncertainty, finest_uncertainty, correct=None, abstain=False
):
    prior = scalar(prior_uncertainty, "prior", lower=0, strict_lower=True)
    level = scalar(level_uncertainty, "level", lower=0, strict_lower=True)
    finest = scalar(finest_uncertainty, "finest", lower=0, strict_lower=True)
    if (
        not finest <= level <= prior
        or finest >= prior
        or type(abstain) is not bool
        or (correct is not None and type(correct) is not bool)
    ):
        raise ValueError("ordered uncertainties and explicit correctness required")
    if abstain:
        return 0.0
    if correct is None:
        raise ValueError("unobserved correctness is not an incorrect answer")
    return math.log(prior / level) / math.log(prior / finest) if correct else -1.0


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or device != "cpu":
        raise ValueError("CPU hierarchy protocol requires integer seed")
    paths = [(f"day-{i}", "2020", "21st-century") for i in range(20)]
    target = consensus_target(paths)
    recognition = recognition_target([3.0, 1.0, 3.0], [[2.0], [2.0], [2.0]])
    u = information_utility(
        prior_uncertainty=1000, level_uncertainty=1, finest_uncertainty=1 / 365, correct=True
    )
    return receipt(
        seed,
        "l0_interface",
        {
            "shared_coarse_value_selected_without_gold": target
            == {"status": "answer", "level": 1, "value": "2020"},
            "too_few_parses_excluded": consensus_target(paths[:15] + [None] * 5)["status"]
            == "exclude",
            "all_coarser_recognition_required": recognition == 2,
            "abstention_differs_from_error": information_utility(
                prior_uncertainty=1000,
                level_uncertainty=1,
                finest_uncertainty=1 / 365,
                abstain=True,
            )
            == 0
            and information_utility(
                prior_uncertainty=1000,
                level_uncertainty=1,
                finest_uncertainty=1 / 365,
                correct=False,
            )
            == -1,
        },
        {
            "year_information_utility": u,
            "selected_level": target["level"],
            "recognition_level": recognition,
        },
    )
