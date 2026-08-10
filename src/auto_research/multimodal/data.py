from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class VisualShapesSplit:
    images: np.ndarray
    questions: np.ndarray
    answers: np.ndarray


@dataclass(frozen=True)
class VisualShapesData:
    train: VisualShapesSplit
    validation: VisualShapesSplit
    test: VisualShapesSplit
    answer_names: tuple[str, ...]


def load_visual_shapes(seed: int = 2026) -> VisualShapesData:
    """Build a deterministic, fully local image-question benchmark.

    Every answer depends on pixels: colour, shape or quadrant.  Splits use
    independently rendered examples, so the benchmark also works offline in CI.
    """

    rng = np.random.default_rng(seed)
    splits = [_render_split(rng, size) for size in (480, 120, 120)]
    return VisualShapesData(
        *splits,
        answer_names=(
            "red", "green", "blue", "square", "cross",
            "top-left", "top-right", "bottom-left", "bottom-right",
        ),
    )


def _render_split(rng: np.random.Generator, size: int) -> VisualShapesSplit:
    images = np.zeros((size, 3, 32, 32), dtype=np.float32)
    questions = np.arange(size, dtype=np.int64) % 3
    answers = np.empty(size, dtype=np.int64)
    colors = np.eye(3, dtype=np.float32)
    centers = ((8, 8), (8, 24), (24, 8), (24, 24))
    for index in range(size):
        # Attributes are sampled independently of question order.  Coupling an
        # attribute to ``index % 3`` would let the model answer from the question
        # token alone and turn a multimodal benchmark into a text shortcut.
        color = int(rng.integers(3))
        shape = int(rng.integers(2))
        position = int(rng.integers(4))
        row, column = centers[position]
        image = images[index]
        if shape == 0:
            image[:, row - 4:row + 4, column - 4:column + 4] = colors[color, :, None, None]
        else:
            image[:, row - 2:row + 2, column - 6:column + 6] = colors[color, :, None, None]
            image[:, row - 6:row + 6, column - 2:column + 2] = colors[color, :, None, None]
        image += rng.normal(0.0, 0.015, image.shape).astype(np.float32)
        np.clip(image, 0.0, 1.0, out=image)
        question = int(questions[index])
        answers[index] = (color, 3 + shape, 5 + position)[question]
    order = rng.permutation(size)
    return VisualShapesSplit(images[order], questions[order], answers[order])
