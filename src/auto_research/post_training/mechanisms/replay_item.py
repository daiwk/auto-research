"""Extracted unchanged from auto_research.post_training.latest_20260930; stable mechanism boundary."""
from __future__ import annotations

from dataclasses import dataclass

from collections import deque
import numpy as np

@dataclass(frozen=True)
class ReplayItem:
    student_log_prob: np.ndarray
    teacher_log_prob: np.ndarray

class LSPDReplayBuffer:
    """Bounded FIFO replay of off-policy query-response token statistics."""

    def __init__(self, capacity: int = 256):
        if capacity < 1:
            raise ValueError("capacity must be positive")
        self._items: deque[ReplayItem] = deque(maxlen=capacity)

    def append(self, student_log_prob, teacher_log_prob) -> None:
        student = np.asarray(student_log_prob, dtype=np.float64).copy()
        teacher = np.asarray(teacher_log_prob, dtype=np.float64).copy()
        if student.shape != teacher.shape:
            raise ValueError("student and teacher log probabilities must match")
        self._items.append(ReplayItem(student, teacher))

    def sample(self, size: int, rng: np.random.Generator) -> list[ReplayItem]:
        if not self._items:
            raise ValueError("cannot sample an empty replay buffer")
        indices = rng.choice(len(self._items), size=min(size, len(self._items)), replace=False)
        return [self._items[int(index)] for index in indices]

    def __len__(self) -> int:
        return len(self._items)
