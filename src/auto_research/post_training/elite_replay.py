"""EliteReplay (2610.22290): directed MAP-Elites and GRPO/replay mixing.

The search API consumes caller-provided frozen-model generation, verification
and realized descriptors. It does not pretend that IID sampling is QD search.
"""
from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable, Hashable

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class Elite:
    question: str
    solution: str
    tokens: tuple[int, ...]
    approach: str
    structure: tuple[Hashable, ...]

    @property
    def cell(self) -> tuple:
        return (self.approach, *self.structure)


class EliteArchive:
    """One verified shortest elite per realized cell and per training question."""
    def __init__(self, applicable: dict[str, tuple[str, ...]]):
        if not applicable or any(not q or not a or len(set(a)) != len(a) for q, a in applicable.items()):
            raise ValueError("training questions need distinct nonempty applicable approaches")
        self.applicable = dict(applicable)
        self.cells: dict[str, dict[tuple, Elite]] = {q: {} for q in applicable}
        self.attempts = {q: dict.fromkeys(a, 0) for q, a in applicable.items()}
        self.frozen = False
        self._question_cursor = 0
        self._cell_cursors = dict.fromkeys(applicable, 0)

    def insert(self, candidate: Elite, verify: Callable[[str, str], bool]) -> bool:
        if self.frozen:
            raise RuntimeError("training archive is frozen")
        if candidate.question not in self.cells or candidate.approach not in self.applicable[candidate.question]:
            raise ValueError("unknown training question or realized approach")
        if not candidate.tokens or not candidate.solution:
            raise ValueError("nonempty solution/tokens required")
        # Verification happens here; a pre-marked 'correct' flag is not trusted.
        if not verify(candidate.question, candidate.solution):
            return False
        existing = self.cells[candidate.question].get(candidate.cell)
        if existing is None or len(candidate.tokens) < len(existing.tokens):
            self.cells[candidate.question][candidate.cell] = candidate
            return True
        return False

    def choose_target(self, question: str, rng: random.Random) -> tuple[str, Elite | None]:
        if self.frozen or question not in self.cells:
            raise ValueError("search requires an unfrozen known training question")
        represented = {elite.approach for elite in self.cells[question].values()}
        pool = [a for a in self.applicable[question] if a not in represented] or list(self.applicable[question])
        least_attempts = min(self.attempts[question][a] for a in pool)
        pool = [a for a in pool if self.attempts[question][a] == least_attempts]
        coverage = {a: sum(any(e.approach == a for e in cells.values()) for cells in self.cells.values()) for a in pool}
        least_coverage = min(coverage.values())
        target = rng.choice(sorted(a for a in pool if coverage[a] == least_coverage))
        self.attempts[question][target] += 1
        parents = list(self.cells[question].values())
        alternative = [e for e in parents if e.approach != target]
        return target, rng.choice(alternative or parents) if parents else None

    def freeze(self) -> None:
        if any(not cells for cells in self.cells.values()):
            raise ValueError("every training question needs a verified elite before replay")
        self.frozen = True

    def sample_balanced(self, count: int) -> list[Elite]:
        """Cyclic question/cell balance: large per-question archives cannot dominate."""
        if not self.frozen or count < 1:
            raise ValueError("positive sample count and frozen archive required")
        questions = sorted(self.cells)
        result = []
        for _ in range(count):
            question = questions[self._question_cursor % len(questions)]
            self._question_cursor += 1
            elites = sorted(self.cells[question].values(), key=lambda e: repr(e.cell))
            cursor = self._cell_cursors[question]
            result.append(elites[cursor % len(elites)])
            self._cell_cursors[question] = cursor + 1
        return result


@torch.no_grad()
def map_elites_search(base: nn.Module, archive: EliteArchive, *,
                      generate: Callable[[nn.Module, str, str, Elite | None], Elite],
                      verify: Callable[[str, str], bool], mutations_per_question: int,
                      seed: int = 42) -> dict[str, int]:
    """Appendix A.3 directed target -> frozen-base variation -> realized insertion.

    Applicable vocabulary and initial verified seeds are external interfaces.
    The local numerical demo supplies a reviewed arithmetic grammar, not an LLM
    labeler, and must retain that diagnostic boundary.
    """
    if archive.frozen or not 1 <= mutations_per_question <= 256:
        raise ValueError("unfrozen archive and bounded positive search budget required")
    rng, seen, verified, inserted = random.Random(seed), 0, 0, 0
    was_training = base.training
    base.eval()
    try:
        for question in sorted(archive.cells):
            for _ in range(mutations_per_question):
                target, parent = archive.choose_target(question, rng)
                candidate = generate(base, question, target, parent)
                if candidate.question != question:
                    raise ValueError("generator must preserve the training question")
                seen += 1
                accepted = bool(verify(question, candidate.solution))
                verified += accepted
                if accepted:
                    # insert verifies again, making the archive boundary safe on
                    # its own; verifiers must be pure/deterministic.
                    inserted += archive.insert(candidate, verify)
    finally:
        base.train(was_training)
    return {"mutation_attempts": seen, "verified_candidates": verified, "insertions_or_improvements": inserted,
        "occupied_cells": sum(len(c) for c in archive.cells.values())}


def grpo_replay_loss(current_logps: Tensor, old_logps: Tensor, rewards: Tensor,
                     mask: Tensor, replay_logps: Tensor, replay_mask: Tensor, *,
                     replay_weight: float = .05, clip_low: float = .2,
                     clip_high: float = .28, epsilon: float = 1e-6) -> tuple[Tensor, dict[str, Tensor]]:
    """Length-normalized GRPO plus length-normalized per-response elite NLL."""
    if current_logps.ndim != 3 or current_logps.shape != old_logps.shape or current_logps.shape != mask.shape:
        raise ValueError("on-policy tensors must have shape (questions, group, tokens)")
    if rewards.shape != current_logps.shape[:2] or replay_logps.ndim != 2 or replay_logps.shape != replay_mask.shape:
        raise ValueError("group rewards and replay response mask do not align")
    if mask.dtype != torch.bool or replay_mask.dtype != torch.bool or not mask.any(-1).all() or not replay_mask.any(-1).all():
        raise ValueError("each response must contain valid tokens")
    if not 0 <= replay_weight <= 1 or not 0 <= clip_low < 1 or clip_high < 0 or epsilon <= 0:
        raise ValueError("invalid mixture/clipping settings")
    if not all(torch.isfinite(t[m]).all() for t, m in ((current_logps, mask), (old_logps, mask), (replay_logps, replay_mask))):
        raise ValueError("valid log probabilities must be finite")
    if not torch.isfinite(rewards).all():
        raise ValueError("rewards must be finite")
    reward = rewards.detach()
    advantage = (reward - reward.mean(-1, keepdim=True)) / (reward.std(-1, keepdim=True, unbiased=False) + epsilon)
    log_ratio = (current_logps.masked_fill(~mask, 0) - old_logps.detach().masked_fill(~mask, 0))
    ratio = log_ratio.exp()
    raw = ratio * advantage.unsqueeze(-1)
    clipped = ratio.clamp(1 - clip_low, 1 + clip_high) * advantage.unsqueeze(-1)
    grpo = -(torch.minimum(raw, clipped).masked_fill(~mask, 0).sum(-1) / mask.sum(-1)).mean()
    replay = -(replay_logps.masked_fill(~replay_mask, 0).sum(-1) / replay_mask.sum(-1)).mean()
    return (1 - replay_weight) * grpo + replay_weight * replay, {
        "grpo_loss": grpo.detach(), "replay_loss": replay.detach(), "advantages": advantage.detach()}
