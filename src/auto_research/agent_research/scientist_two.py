"""ScientistTwo control contracts, not an autonomous scientist or semantic judge.

All critics, proposals, experiments, comparisons and rebuttals are external.
Callbacks are not sandboxes and this module does not establish their truthfulness.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math
from numbers import Real
import random

REQUIRES_GPU_VALIDATION = False


def _text(value: str, name: str, *, nonempty: bool = True) -> None:
    if not isinstance(value, str) or (nonempty and not value.strip()):
        raise ValueError(f"{name} must be an explicit string")


def _budget(value: int, name: str) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative integer")


@dataclass(frozen=True)
class Artifact:
    idea_id: str
    artifact_id: str
    evidence_ref: str

    def __post_init__(self):
        for name in ("idea_id", "artifact_id", "evidence_ref"):
            _text(getattr(self, name), name)


@dataclass(frozen=True)
class Critique:
    verdict: str
    feedback: str = ""

    def __post_init__(self):
        if self.verdict not in ("accept", "refine", "reject"):
            raise ValueError("explicit accept/refine/reject verdict required")
        _text(self.feedback, "feedback", nonempty=False)


@dataclass(frozen=True)
class StageResult:
    accepted: Artifact | None
    status: str
    observations: tuple[tuple[Artifact, Critique], ...]
    refinement_calls: int


def run_stage(candidate: Artifact, critic: Callable[[Artifact], Critique],
              refine: Callable[[Artifact, str], Artifact], *, max_rounds: int) -> StageResult:
    """Literal Figure4 critic-call budget, including a discarded last refinement.

    The paper's generic pseudocode refines even on its last allowed critic
    iteration, then returns None if no acceptance occurred. This is not a claim
    that its separate engineering-refinement budget has the same counting unit.
    """
    _budget(max_rounds, "critic rounds")
    if not isinstance(candidate, Artifact) or not callable(critic) or not callable(refine):
        raise ValueError("artifact and external critic/refinement callbacks required")
    observations, refinements = [], 0
    for _ in range(max_rounds):
        verdict = critic(candidate)
        if not isinstance(verdict, Critique):
            raise ValueError("critic must return a typed external verdict")
        observations.append((candidate, verdict))
        if verdict.verdict == "accept":
            return StageResult(candidate, "accepted", tuple(observations), refinements)
        if verdict.verdict == "reject":
            return StageResult(None, "rejected", tuple(observations), refinements)
        updated = refine(candidate, verdict.feedback)
        if not isinstance(updated, Artifact) or updated.idea_id != candidate.idea_id:
            raise ValueError("stage refinement must retain the idea identity")
        candidate, refinements = updated, refinements + 1
    return StageResult(None, "exhausted", tuple(observations), refinements)


@dataclass(frozen=True)
class Assessment:
    artifact: Artifact
    stage: str
    decision: str
    feedback: str = ""

    def __post_init__(self):
        if (not isinstance(self.artifact, Artifact) or self.stage not in ("subset", "full")
                or self.decision not in ("Good", "Bad", "Engineer")):
            raise ValueError("typed subset/full assessment with Good/Bad/Engineer required")
        _text(self.feedback, "feedback", nonempty=False)


def promote_subset(assessment: Assessment,
                   full_experiment: Callable[[Artifact], Assessment]) -> Assessment | None:
    """Only an external subset Good unlocks a full-set callback; no invented threshold."""
    if not isinstance(assessment, Assessment) or assessment.stage != "subset" or not callable(full_experiment):
        raise ValueError("subset assessment and external full-set execution required")
    if assessment.decision != "Good":
        return None
    result = full_experiment(assessment.artifact)
    if (not isinstance(result, Assessment) or result.stage != "full"
            or result.artifact.idea_id != assessment.artifact.idea_id):
        raise ValueError("full-set result must retain the promoted idea identity")
    return result  # A full-set Bad/Engineer does not become Good merely by promotion.


@dataclass(frozen=True)
class Idea:
    idea_id: str
    description: str
    novelty: float

    def __post_init__(self):
        _text(self.idea_id, "idea identity")
        _text(self.description, "idea description")
        if isinstance(self.novelty, bool) or not isinstance(self.novelty, Real) or not math.isfinite(self.novelty):
            raise ValueError("finite externally assessed novelty required")


def _history(history: Sequence[Assessment]) -> tuple[Assessment, ...]:
    if (not isinstance(history, Sequence) or isinstance(history, (str, bytes))
            or not all(isinstance(x, Assessment) and (x.decision == "Bad" or
                       (x.stage == "full" and x.decision == "Good")) for x in history)):
        raise ValueError("closed experiment history must retain terminal Good and Bad records")
    if len({x.artifact.idea_id for x in history}) != len(history):
        raise ValueError("closed experiment identities must be unique")
    return tuple(history)


def build_round(seeds: Sequence[Idea], history: Sequence[Assessment],
                evolve: Callable[[tuple[Assessment, ...], int], Sequence[Idea]], *,
                evolved_count: int = 1, exploration_count: int = 1) -> tuple[Idea, ...]:
    """Eq3 pool: external evolved proposals plus highest-novelty untried seeds.

    The evolver receives successes AND diagnostic failures. Scores are inputs,
    not this module's semantic novelty evaluation. ID ties are locally stable.
    """
    _budget(evolved_count, "evolved count")
    _budget(exploration_count, "exploration count")
    archive = _history(history)
    if (not isinstance(seeds, Sequence) or isinstance(seeds, (str, bytes))
            or not all(isinstance(x, Idea) for x in seeds) or not callable(evolve)
            or len({x.idea_id for x in seeds}) != len(seeds)):
        raise ValueError("unique ranked seed identities and external evolver required")
    evolved = evolve(archive, evolved_count) if evolved_count else ()
    if (not isinstance(evolved, Sequence) or isinstance(evolved, (str, bytes))
            or len(evolved) > evolved_count or not all(isinstance(x, Idea) for x in evolved)):
        raise ValueError("external evolved proposals exceed the declared budget or type")
    seen = {x.artifact.idea_id for x in archive}
    proposed = {x.idea_id for x in evolved}
    if len(proposed) != len(evolved) or seen & proposed:
        raise ValueError("evolved proposals must have unique previously unevaluated identities")
    remaining = sorted((x for x in seeds if x.idea_id not in seen | proposed),
                       key=lambda x: (-x.novelty, x.idea_id))
    return tuple(evolved) + tuple(remaining[:exploration_count])


def search_decision(history: Sequence[Assessment], *, rounds_completed: int,
                    maximum_rounds: int = 4, success_target: int = 4) -> str:
    """Selection requires full-set Good, not intermediate subset success."""
    archive = _history(history)
    _budget(rounds_completed, "completed rounds")
    _budget(maximum_rounds, "maximum rounds")
    if type(success_target) is not int or success_target < 1:
        raise ValueError("positive success target required")
    successes = sum(x.decision == "Good" for x in archive)
    if successes >= success_target or (rounds_completed >= maximum_rounds and successes):
        return "select_best_externally"
    return "terminate_without_success" if rounds_completed >= maximum_rounds else "continue"


def strict_refinement(best: Artifact, proposed: Artifact,
                      compare: Callable[[Artifact, Artifact], bool]) -> tuple[Artifact, bool]:
    """Sections3.4/3.6: compare(proposed,best) must certify STRICT superiority.

    True requests new ablations/drafting outside this kernel. False (including
    ties, regression, or no established superiority) retains the original object.
    """
    if not isinstance(best, Artifact) or not isinstance(proposed, Artifact) or not callable(compare):
        raise ValueError("artifacts and external strict-comparison callback required")
    better = compare(proposed, best)
    if type(better) is not bool:
        raise ValueError("strict superiority must be an explicit external boolean")
    return (proposed, True) if better else (best, False)


@dataclass(frozen=True)
class Review:
    score: float
    feedback: str

    def __post_init__(self):
        if (isinstance(self.score, bool) or not isinstance(self.score, Real)
                or not math.isfinite(self.score) or not 1 <= self.score <= 10):
            raise ValueError("external finite ICLR-style score in [1,10] required")
        _text(self.feedback, "review feedback", nonempty=False)


@dataclass(frozen=True)
class ReviewResult:
    artifact: Artifact
    accepted: bool
    reviews: tuple[Review, ...]
    rebuttal_calls: int


def review_rebuttal(draft: Artifact, review: Callable[[Artifact], Review],
                    rebuttal: Callable[[Artifact, Review], Artifact], *,
                    maximum_reviews: int = 2, threshold: float = 8) -> ReviewResult:
    """Bound review calls; an unreviewed last revision cannot be called accepted.

    Refine only if a follow-up review slot remains. This explicit accounting
    convention bounds review calls; it is not the complete paper/meta-review loop.
    """
    _budget(maximum_reviews, "review budget")
    Review(threshold, "threshold")
    if not isinstance(draft, Artifact) or not callable(review) or not callable(rebuttal):
        raise ValueError("draft and external review/rebuttal callbacks required")
    reviews, rebuttals = [], 0
    for index in range(maximum_reviews):
        result = review(draft)
        if not isinstance(result, Review):
            raise ValueError("review callback must return a typed external review")
        reviews.append(result)
        if result.score >= threshold:
            return ReviewResult(draft, True, tuple(reviews), rebuttals)
        if index + 1 < maximum_reviews:
            updated = rebuttal(draft, result)
            if not isinstance(updated, Artifact) or updated.idea_id != draft.idea_id:
                raise ValueError("rebuttal must retain the idea identity")
            draft, rebuttals = updated, rebuttals + 1
    return ReviewResult(draft, False, tuple(reviews), rebuttals)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Fixed callback truth tables only, never model critics or research outcomes."""
    if device != "cpu":
        raise ValueError("CPU control contract only; no CUDA scientist model")
    if type(seed) is not int:
        raise ValueError("integer diagnostic seed required")
    initial = Artifact("idea", "v0", "fixture://not-real-experiment")
    critique_calls = []

    def critic(artifact):
        critique_calls.append(artifact.artifact_id)
        return Critique("refine" if len(critique_calls) == 1 else "accept", "fixture feedback")

    def refine(artifact, feedback):
        return Artifact(artifact.idea_id, "v1", artifact.evidence_ref)

    stage = run_stage(initial, critic, refine, max_rounds=2)
    history = (Assessment(Artifact("failed", "f", "fixture://failure"), "subset", "Bad"),
               Assessment(Artifact("succeeded", "s", "fixture://success"), "full", "Good"))
    delivered_history = []

    def evolve(archive, count):
        delivered_history.extend(archive)
        return [Idea("evolved", "external fixture proposal", 0)]

    seeds = [Idea("seed-low", "fixture seed", 1), Idea("seed-high", "fixture seed", 2)]
    random.Random(seed).shuffle(seeds)
    pool = build_round(seeds, history, evolve)
    full_calls = []

    def full(artifact):
        full_calls.append(artifact.idea_id)
        return Assessment(artifact, "full", "Bad")

    blocked = promote_subset(Assessment(initial, "subset", "Engineer"), full)
    full_result = promote_subset(Assessment(initial, "subset", "Good"), full)
    retained, changed = strict_refinement(initial, refine(initial, ""), lambda proposed, best: False)
    scores = iter([7, 8])
    reviewed = review_rebuttal(initial, lambda draft: Review(next(scores), "fixture only"),
                               lambda draft, review: refine(draft, review.feedback))
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"critic_calls": len(stage.observations), "stage_refinements": stage.refinement_calls,
                        "history_records_forwarded": len(delivered_history), "round_candidates": len(pool),
                        "full_callback_calls": len(full_calls), "review_calls": len(reviewed.reviews),
                        "rebuttal_calls": reviewed.rebuttal_calls},
            "checks": {"bounded_stage_accepts_reviewed_revision": stage.accepted is not None
                       and stage.accepted.artifact_id == "v1",
                       "history_keeps_success_and_failure": delivered_history == list(history),
                       "evolved_plus_untried_novel_seed": [x.idea_id for x in pool] == ["evolved", "seed-high"],
                       "engineer_does_not_unlock_full": blocked is None and len(full_calls) == 1,
                       "full_failure_not_promoted": full_result is not None and full_result.decision == "Bad",
                       "non_improvement_retains_original": retained is initial and not changed,
                       "review_threshold_and_budget": reviewed.accepted and len(reviewed.reviews) == 2
                       and reviewed.rebuttal_calls == 1,
                       "budget_with_some_success_selects": search_decision(history, rounds_completed=4)
                       == "select_best_externally"}}
