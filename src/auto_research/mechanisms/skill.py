"""Extracted unchanged from auto_research.recommendation_latest_20260930_closure; stable mechanism boundary."""
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
