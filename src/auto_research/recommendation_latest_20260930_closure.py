"""Executable recommendation mechanisms reviewed in the Sep-30 closure."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable


@dataclass(frozen=True)
class Skill:
    """Typed executable skill stored by the EvoSkillRec controller."""

    name: str
    input_type: str
    output_type: str
    operator: Callable


@dataclass(frozen=True)
class SkillGenome:
    names: tuple[str, ...]
    input_type: str
    output_type: str


class SkillGenomeController:
    """Minimal promotion-and-reuse loop; evaluator owns the validation split."""

    def __init__(self, evaluator: Callable[[object], float]) -> None:
        self.evaluator = evaluator
        self.skills: dict[str, Skill] = {}
        self.promoted: dict[tuple[str, ...], float] = {}

    def register(self, skill: Skill) -> None:
        if skill.name in self.skills:
            raise ValueError(f"duplicate skill: {skill.name}")
        self.skills[skill.name] = skill

    def validate(self, genome: SkillGenome) -> None:
        current = genome.input_type
        for name in genome.names:
            skill = self.skills[name]
            if skill.input_type != current:
                raise TypeError(f"{name} expects {skill.input_type}, received {current}")
            current = skill.output_type
        if current != genome.output_type:
            raise TypeError(f"genome returns {current}, expected {genome.output_type}")

    def execute(self, genome: SkillGenome, value):
        self.validate(genome)
        for name in genome.names:
            value = self.skills[name].operator(value)
        return value

    def evaluate_and_promote(
        self, genome: SkillGenome, value, *, baseline: float, minimum_gain: float = 0.0,
    ) -> dict:
        """Execute before evaluation; only validation gains enter the reusable library."""
        output = self.execute(genome, value)
        score = float(self.evaluator(output))
        promoted = score > baseline + minimum_gain
        if promoted:
            self.promoted[genome.names] = score
        return {"score": score, "promoted": promoted, "output": output}

    def reuse(self) -> tuple[SkillGenome, ...]:
        return tuple(
            SkillGenome(names, self.skills[names[0]].input_type,
                        self.skills[names[-1]].output_type)
            for names, _ in sorted(self.promoted.items(), key=lambda item: -item[1])
        )


def promptshift_metrics(reference, cued, slice_popularity, relevant: Iterable[int], *, k=20):
    """PromptShift Drift, SliceShift and difficulty-weighted hit diagnostics."""
    import numpy as np

    reference = list(reference)[:k]
    cued = list(cued)[:k]
    if len(reference) != len(cued) or len(set(reference)) != len(reference) or len(set(cued)) != len(cued):
        raise ValueError("rankings must be equally sized and contain unique items")
    popularity = np.asarray(slice_popularity, dtype=np.float64)
    overlap = len(set(reference) & set(cued)) / max(1, len(reference))
    common = set(reference) & set(cued)
    rank_shift = sum(abs(reference.index(item) - cued.index(item)) for item in common)
    rank_shift /= max(1, len(common) * max(1, len(reference) - 1))
    drift = 0.5 * (1 - overlap) + 0.5 * rank_shift
    slice_shift = float(np.mean([popularity[item] for item in cued]) - np.mean([
        popularity[item] for item in reference
    ]))
    relevant = set(relevant)
    difficulty = sum(
        (1.0 / (rank + 1)) * (1.0 - popularity[item])
        for rank, item in enumerate(cued) if item in relevant
    )
    return {"drift": float(drift), "slice_shift": slice_shift,
            "difficulty_at_k": float(difficulty)}


def promptshift_rerank(items, scores, slice_popularity, mainstreamness):
    """Adaptive interpolation with inverse slice popularity."""
    import numpy as np

    items = np.asarray(items, dtype=np.int64)
    scores = np.asarray(scores, dtype=np.float64)
    popularity = np.asarray(slice_popularity, dtype=np.float64)[items]
    if scores.shape != items.shape or not 0 <= mainstreamness <= 1:
        raise ValueError("scores must align with items and mainstreamness must be in [0,1]")
    score_norm = (scores - scores.min()) / max(float(scores.max() - scores.min()), 1e-12)
    combined = (1 - mainstreamness) * score_norm + mainstreamness * (1 - popularity)
    order = np.argsort(-combined, kind="stable")
    return items[order], combined[order]
