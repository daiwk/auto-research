"""Executable, model-agnostic mechanisms from recent foundation-model papers."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CritiqueExample:
    question: str
    incorrect_response: str
    failure_mode: str
    critique: str


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def select_criticl_examples(
    query: str,
    bank: tuple[CritiqueExample, ...],
    *,
    mode: str = "dynamic",
    maximum_examples: int = 3,
) -> tuple[CritiqueExample, ...]:
    """Select CritBank entries using the paper's static or dynamic policy."""
    if mode not in {"static", "dynamic"}:
        raise ValueError("mode must be static or dynamic")
    if maximum_examples < 1:
        raise ValueError("maximum_examples must be positive")
    frequencies = Counter(item.failure_mode for item in bank)
    query_tokens = _tokens(query)

    def score(item: CritiqueExample):
        overlap = len(query_tokens & _tokens(item.question)) / max(
            1, len(query_tokens | _tokens(item.question))
        )
        if mode == "static":
            return frequencies[item.failure_mode], overlap
        mode_overlap = len(query_tokens & _tokens(item.failure_mode.replace("_", " ")))
        return mode_overlap + overlap, frequencies[item.failure_mode]

    return tuple(sorted(bank, key=score, reverse=True)[:maximum_examples])


def build_criticl_prompt(
    query: str,
    bank: tuple[CritiqueExample, ...],
    *,
    mode: str = "dynamic",
    maximum_examples: int = 3,
) -> tuple[str, dict[str, float]]:
    selected = select_criticl_examples(
        query, bank, mode=mode, maximum_examples=maximum_examples
    )
    blocks = [
        (
            f"Failure mode: {item.failure_mode}\n"
            f"Past question: {item.question}\n"
            f"Incorrect reasoning: {item.incorrect_response}\n"
            f"Critique: {item.critique}"
        )
        for item in selected
    ]
    prompt = "\n\n".join([
        "Use the recurring failure critiques below as warnings; solve the new problem yourself.",
        *blocks,
        f"New problem: {query}",
    ])
    return prompt, {
        "critbank_size": float(len(bank)),
        "retrieved_critiques": float(len(selected)),
        "unique_failure_modes": float(len({item.failure_mode for item in selected})),
        "online_weak_model_calls": 0.0,
    }
