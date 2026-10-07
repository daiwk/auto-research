"""Extracted unchanged from auto_research.agent_research.latest_20261001; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass, field

from dataclasses import dataclass, field

@dataclass
class MetaSkillBank:
    """Development-only meta-skill refinement; test tasks can only read the bank."""

    skills: dict[str, dict] = field(default_factory=dict)

    def revise(self, outcomes):
        for item in outcomes:
            name = item["skill"]
            current = self.skills.setdefault(name, {"when": set(), "provide": set(), "use": set(), "score": 0.0})
            weight = float(item["reward"])
            current["score"] += weight
            if weight > 0:
                for field_name in ("when", "provide", "use"):
                    current[field_name].update(item.get(field_name, ()))

    def select(self, task_tags, *, limit: int):
        tags = set(task_tags)
        ranked = []
        for name, skill in self.skills.items():
            overlap = len(tags & set(skill["when"]))
            ranked.append((overlap, skill["score"], name))
        return tuple(name for overlap, _, name in sorted(ranked, reverse=True)[:limit] if overlap)
