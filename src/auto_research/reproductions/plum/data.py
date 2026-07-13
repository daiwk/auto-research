from __future__ import annotations

import random
from dataclasses import dataclass

from .model import MovieMetadata, SemanticIDIndex


@dataclass(frozen=True)
class CompletionExample:
    prompt: str
    completion: str


def build_cpt_corpus(
    sequences,
    metadata: MovieMetadata,
    index: SemanticIDIndex,
    seed: int,
    examples_per_source: int = 6000,
) -> tuple[str, ...]:
    """Construct the paper's 50/50 behavior/metadata CPT mixture."""

    rng = random.Random(seed)
    behavior: list[str] = []
    histories = list(sequences.train)
    while len(behavior) < examples_per_source:
        history = rng.choice(histories)
        end = rng.randint(3, len(history))
        start = max(0, end - 20)
        sid_history = " ".join(index.text(item) for item in history[start:end])
        behavior.append(f"watch history = {sid_history}")

    metadata_rows = [
        (
            f"Video {index.text(item)} has title (en): {metadata.titles[item]}. "
            f"The topics in video {index.text(item)} are: "
            f"{', '.join(metadata.genres[item])}."
        )
        for item in range(len(metadata.titles))
    ]
    metadata_corpus = [
        metadata_rows[item % len(metadata_rows)]
        for item in range(examples_per_source)
    ]
    mixed = behavior + metadata_corpus
    rng.shuffle(mixed)
    return tuple(mixed)


def build_sft_examples(
    sequences,
    index: SemanticIDIndex,
    seed: int,
    maximum: int = 24000,
) -> tuple[CompletionExample, ...]:
    rows: list[CompletionExample] = []
    for sequence in sequences.train:
        for target_position in range(3, len(sequence)):
            history = sequence[max(0, target_position - 20) : target_position]
            rows.append(
                CompletionExample(
                    prompt=retrieval_prompt(history, index),
                    completion=index.text(sequence[target_position]),
                )
            )
    rng = random.Random(seed)
    rng.shuffle(rows)
    return tuple(rows[:maximum])


def retrieval_prompt(history: tuple[int, ...], index: SemanticIDIndex) -> str:
    watched = " ".join(index.text(item) for item in history[-20:])
    return (
        "Recommend the next movie from this watch history.\n"
        f"watch history = {watched}\nnext movie SID = "
    )
