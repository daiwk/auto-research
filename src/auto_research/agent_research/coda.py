"""Content-only skill drift and paired CODA audit metrics; no agent training."""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Skill:
    skill_id: str
    retrieval_fields: Mapping[str, object]
    content_fields: Mapping[str, str]


def rewrite_selected(bank, selected_ids, rewrites: Mapping[str, Mapping[str, str]]):
    """Freeze one retrieval decision before substituting declared content fields.

No similarity threshold claims to certify semantic equivalence. The caller must
pin and disclose the actual rewriting suite and its banks.
"""
    skills = tuple(bank)
    ids = {s.skill_id for s in skills}
    selected = tuple(selected_ids)
    if len(ids) != len(skills) or len(set(selected)) != len(selected) or not set(selected) <= ids:
        raise ValueError("unique known skill and selected IDs required")
    if not set(rewrites) <= set(selected):
        raise ValueError("only originally retrieved skills can be rewritten")
    result = []
    for skill in skills:
        update = rewrites.get(skill.skill_id, {})
        if not set(update) <= set(skill.content_fields) or any(not isinstance(v, str) for v in update.values()):
            raise ValueError("only declared content fields may change")
        result.append(Skill(skill.skill_id, deepcopy(dict(skill.retrieval_fields)),
                            {**deepcopy(dict(skill.content_fields)), **dict(update)}))
    return tuple(result)


def audit(outcomes: Mapping[str, Mapping[str, bool]]) -> dict[str, float]:
    """Require paired complete outcomes, including explicit failed episodes.

RR is a fraction of the entire task set, not success conditional on the no-skill
baseline. CR compares outcome flips, not just aggregate success rates.
"""
    required = {"delivered", "repeat", "reword", "incomplete", "misleading", "no_skill"}
    if set(outcomes) != required:
        raise ValueError("all six audit conditions required")
    ids = set(outcomes["delivered"])
    if not ids or any(set(values) != ids for values in outcomes.values()):
        raise ValueError("all conditions must retain the exact same task IDs")
    if any(type(v) is not bool for values in outcomes.values() for v in values.values()):
        raise ValueError("explicit binary per-task outcomes required")
    n = len(ids)
    rates = {key: sum(values.values()) / n for key, values in outcomes.items()}
    return {"tasks": n, "delivered_success_rate": rates["delivered"],
            "worst_case_success_rate": min(rates[x] for x in ("delivered", "reword", "incomplete", "misleading")),
            "peak_to_worst_drop": rates["delivered"] - min(rates[x] for x in (
                "delivered", "reword", "incomplete", "misleading")),
            "consistency_rate": sum(outcomes["delivered"][i] == outcomes["reword"][i] for i in ids) / n,
            "noise_floor_consistency": sum(outcomes["delivered"][i] == outcomes["repeat"][i] for i in ids) / n,
            "resistance_incomplete": sum(outcomes["no_skill"][i] and outcomes["incomplete"][i] for i in ids) / n,
            "resistance_misleading": sum(outcomes["no_skill"][i] and outcomes["misleading"][i] for i in ids) / n}
