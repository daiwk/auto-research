"""TAR: correctness-filtered FPS and detached trajectory/token replay gates.

Embeddings and verifier observations are explicit caller inputs. This component
does not provide a semantic encoder or infer mathematical correctness.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor


def farthest_point_prototypes(embeddings: Tensor, correct: Tensor, *, limit: int = 3,
                              initial_index: int | None = None) -> list[int]:
    """FPS by cosine distance among verifier-approved candidates only.

    The seed prototype is uniformly random among correct responses unless an
    explicit original row index is given. Returned IDs refer to original rows.
    Embedding validity does not certify semantic diversity; callers must label
    the representation source rather than passing random vectors as an encoder.
    """
    if embeddings.ndim != 2 or not embeddings.is_floating_point() or embeddings.shape[1] < 1:
        raise ValueError("floating [candidate,nonempty hidden] embeddings required")
    if correct.shape != (embeddings.shape[0],) or correct.dtype != torch.bool or correct.device != embeddings.device:
        raise ValueError("aligned Boolean verifier observations on one device required")
    if type(limit) is not int or limit < 1:
        raise ValueError("positive prototype limit required")
    eligible = correct.nonzero().flatten()
    if len(eligible) == 0:
        if initial_index is not None:
            raise ValueError("seed prototype must be a correct response")
        return []
    rows = embeddings.detach()[eligible]
    norms = rows.norm(dim=1)
    if not torch.isfinite(rows).all() or not torch.isfinite(norms).all() or bool((norms == 0).any()):
        raise ValueError("finite nonzero correct-response embeddings with representable norms required")
    if initial_index is None:
        first = int(torch.randint(len(eligible), (1,), device=eligible.device))
    else:
        if type(initial_index) is not int:
            raise ValueError("seed prototype must be a correct response")
        matches = (eligible == initial_index).nonzero().flatten()
        if len(matches) != 1:
            raise ValueError("seed prototype must be a correct response")
        first = int(matches[0])
    normalized = rows / norms[:, None]
    distance = (1 - normalized @ normalized.T).clamp(0, 2)
    selected = [first]
    while len(selected) < min(limit, len(eligible)):
        nearest = distance[:, selected].min(1).values
        nearest[selected] = -1.
        selected.append(int(nearest.argmax()))
    return [int(eligible[i]) for i in selected]


def adaptive_replay_loss(current_logp: Tensor, base_logp: Tensor, actor_mask: Tensor,
                         *, epsilon: float = 1e-8) -> tuple[Tensor, dict]:
    """Equation 8: mean across ALL replay trajectories, including zero gates."""
    if current_logp.ndim != 2 or current_logp.shape != base_logp.shape or min(current_logp.shape) < 1:
        raise ValueError("aligned nonempty [stored trajectory,token] log probabilities required")
    if not current_logp.is_floating_point() or current_logp.dtype != base_logp.dtype or current_logp.device != base_logp.device:
        raise ValueError("floating replay scores need matching dtype/device")
    if actor_mask.shape != current_logp.shape or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()) or actor_mask.device != current_logp.device:
        raise ValueError("each replay trajectory needs a Boolean actor mask on one device")
    if not torch.isfinite(current_logp[actor_mask]).all() or not torch.isfinite(base_logp[actor_mask]).all():
        raise ValueError("finite active replay log probabilities required")
    if bool((current_logp[actor_mask] > 0).any()) or bool((base_logp[actor_mask] > 0).any()):
        raise ValueError("active replay log probabilities must be nonpositive")
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("positive finite denominator safeguard required")
    if current_logp.dtype in (torch.float16, torch.bfloat16):
        current_logp, base_logp = current_logp.float(), base_logp.float()
    current = torch.where(actor_mask, current_logp, 0.)
    discrepancy = torch.where(actor_mask, base_logp.detach(), 0.) - current.detach()
    # Algebraically phi(x)=max(1-exp(-x),0), without overflow for x<<0.
    phi = lambda x: -torch.expm1(-x.clamp_min(0))
    trajectory_gap = discrepancy.sum(1) / actor_mask.sum(1)
    gate = phi(trajectory_gap).detach()
    weights = torch.where(actor_mask, phi(discrepancy), 0.).detach()
    weighted_nll = (weights * -current).sum(1) / (epsilon + weights.sum(1))
    return (gate * weighted_nll).mean(), {"trajectory_gap": trajectory_gap.detach(),
        "trajectory_gate": gate, "token_weights": weights,
        "per_trajectory_replay": (gate * weighted_nll).detach()}
