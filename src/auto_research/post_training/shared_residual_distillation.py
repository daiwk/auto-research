"""SRD (2610.22080), Eqs. 6--10 and the disjoint peer/control protocol.

This is a distributional operator, not a pretrained reasoning model. Teacher
views must score the *same target prefix*; no gold answer is an input here.
"""
from __future__ import annotations

from dataclasses import dataclass
import random

import torch
from torch import Tensor


@dataclass(frozen=True)
class PeerAssignment:
    target: int
    peers: tuple[int, ...]
    control: int


def split_peers(problem_ids: list[str], *, peers: int = 2, seed: int = 42) -> list[PeerAssignment]:
    """Uniform M-peer split per problem; controls come from a different problem.

    Indices identify already sampled on-policy trajectories, not labels. All
    non-peer trajectories become targets; a target is never its own context.
    """
    if peers < 2 or len(set(problem_ids)) < 2 or any(not p for p in problem_ids):
        raise ValueError("at least two problems and M >= 2 peers are required")
    groups: dict[str, list[int]] = {}
    for index, problem in enumerate(problem_ids):
        groups.setdefault(problem, []).append(index)
    if any(len(indices) <= peers for indices in groups.values()):
        raise ValueError("every problem needs K > M trajectories")
    rng, assignments = random.Random(seed), []
    for problem, indices in groups.items():
        selected = tuple(sorted(rng.sample(indices, peers)))
        controls = [i for i, p in enumerate(problem_ids) if p != problem]
        for target in indices:
            if target not in selected:
                assignments.append(PeerAssignment(target, selected, rng.choice(controls)))
    return assignments


def _valid_logits(logits: Tensor, mask: Tensor) -> Tensor:
    expanded = mask.unsqueeze(-1).expand_as(logits)
    if not torch.isfinite(logits[expanded]).all():
        raise ValueError("teacher/student logits must be finite at valid positions")
    # Invalid padding is replaced *before* log_softmax/exp, avoiding NaN grads.
    return logits.masked_fill(~expanded, 0)


@torch.no_grad()
def shared_residual_target(base_logits: Tensor, control_logits: Tensor,
                           peer_logits: Tensor, mask: Tensor | None = None,
                           *, temperature: float = 1.) -> tuple[Tensor, dict[str, Tensor]]:
    """Centered log residual -> conservative minmod -> normalized q_cap.

    Shapes: base/control (..., V), peers (M, ..., V). Returns detached targets;
    q0 and qc have different roles and may not be substituted for each other.
    """
    if base_logits.shape != control_logits.shape or peer_logits.shape[1:] != base_logits.shape:
        raise ValueError("base/control and every peer must score identical prefix/vocabulary shapes")
    if base_logits.ndim < 2 or peer_logits.shape[0] < 2 or temperature <= 0:
        raise ValueError("need M >= 2, vocabulary and a positive temperature")
    mask = torch.ones(base_logits.shape[:-1], dtype=torch.bool, device=base_logits.device) if mask is None else mask
    if mask.shape != base_logits.shape[:-1] or mask.dtype != torch.bool or not mask.any():
        raise ValueError("nonempty boolean valid-token mask required")
    base = _valid_logits(base_logits.detach(), mask) / temperature
    control = _valid_logits(control_logits.detach(), mask) / temperature
    peer = torch.stack([_valid_logits(view.detach(), mask) for view in peer_logits]) / temperature
    log_q0, log_qc = base.log_softmax(-1), control.log_softmax(-1)
    difference = peer.log_softmax(-1) - log_qc.unsqueeze(0)
    centered = difference - (log_q0.exp().unsqueeze(0) * difference).sum(-1, keepdim=True)
    low, high = centered.min(0).values, centered.max(0).values
    residual = torch.where(low > 0, low, torch.where(high < 0, high, torch.zeros_like(low)))
    target = (log_q0 + residual).softmax(-1)
    target = target.masked_fill(~mask.unsqueeze(-1), 0)
    return target.detach(), {"centered_residuals": centered.detach(),
        "shared_residual": residual.masked_fill(~mask.unsqueeze(-1), 0).detach(),
        "base_probabilities": log_q0.exp().detach()}


def clipped_distillation_loss(student_logits: Tensor, teacher_target: Tensor,
                              mask: Tensor, *, coordinate_cap: float = 1e-6) -> Tensor:
    """Eq. 9: cap each signed q*log(q/p) term, *then* sum and token-mean.

    This surrogate can be negative. Do not clamp the total KL or discard signed
    summands. A large cap recovers forward KL; targets always stop gradient.
    """
    if student_logits.shape != teacher_target.shape or mask.shape != student_logits.shape[:-1]:
        raise ValueError("incompatible logits/target/mask shapes")
    if mask.dtype != torch.bool or not mask.any() or coordinate_cap <= 0:
        raise ValueError("positive cap and nonempty boolean mask required")
    q = teacher_target.detach().masked_fill(~mask.unsqueeze(-1), 0)
    if not torch.isfinite(q).all() or (q < 0).any():
        raise ValueError("teacher target must be finite and nonnegative")
    if not torch.allclose(q.sum(-1)[mask], torch.ones_like(q.sum(-1)[mask]), atol=1e-5):
        raise ValueError("valid teacher targets must sum to one")
    log_p = _valid_logits(student_logits, mask).log_softmax(-1)
    terms = torch.xlogy(q, q) - q * log_p
    return terms.clamp_max(coordinate_cap).sum(-1).masked_fill(~mask, 0).sum() / mask.sum()
