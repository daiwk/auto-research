"""GroupDPO's first-order-exact response-wise surrogate (2604.15602v2).

The no-grad coefficients use the WHOLE optimizer batch. Backward microbatches
only release activations; they do not redefine groups or normalization. This is
an L1 mechanism component, not an LLM training/benchmark implementation.
"""
from __future__ import annotations

from collections.abc import Callable, Sequence
from copy import deepcopy
from dataclasses import dataclass
import math

import torch
from torch import Tensor
from torch.nn import functional as F

OBJECTIVES = ("margin", "mpo", "softmax", "all_pairs")


@dataclass(frozen=True)
class PreferenceGroup:
    positive: tuple[int, ...]
    negative: tuple[int, ...]


def _validate(scores: Tensor, groups: Sequence[PreferenceGroup], objective: str) -> None:
    if (scores.ndim != 1 or not len(scores) or not scores.is_floating_point()
            or not bool(torch.isfinite(scores).all())):
        raise ValueError("finite floating response-score vector required")
    if objective not in OBJECTIVES or not groups:
        raise ValueError("nonempty groups and a supported objective required")
    covered = set()
    for group in groups:
        if not isinstance(group, PreferenceGroup) or not group.positive or not group.negative:
            raise ValueError("every group needs nonempty positive and negative sets")
        indices = (*group.positive, *group.negative)
        if (any(isinstance(i, bool) or not isinstance(i, int) or not 0 <= i < len(scores) for i in indices)
                or len(set(indices)) != len(indices)):
            raise ValueError("group indices must be in range, unique and disjoint")
        covered.update(indices)
    if covered != set(range(len(scores))):
        raise ValueError("response set must be exactly the union of the groups")


def group_objective(scores: Tensor, groups: Sequence[PreferenceGroup],
                    objective: str = "all_pairs") -> Tensor:
    """Table 1 group loss, normalized by total groups, NOT response count."""
    _validate(scores, groups, objective)
    work = scores.float() if scores.dtype in (torch.float16, torch.bfloat16) else scores
    losses = []
    for group in groups:
        positive, negative = work[list(group.positive)], work[list(group.negative)]
        if objective == "margin":
            loss = F.softplus(negative.mean() - positive.mean())
        elif objective == "mpo":
            loss = torch.logsumexp(torch.cat((positive, negative)), 0) - torch.logsumexp(positive, 0)
        elif objective == "softmax":
            loss = F.softplus(torch.logsumexp(negative, 0) - positive).mean()
        else:
            loss = F.softplus(negative[None, :] - positive[:, None]).mean()
        losses.append(loss)
    return torch.stack(losses).mean()


@torch.no_grad()
def precompute_coefficients(scores: Tensor, groups: Sequence[PreferenceGroup],
                            objective: str = "all_pairs") -> Tensor:
    """Algorithm 1: detached analytic dL_group/du; overlap adds contributions.

    Recompute at the CURRENT parameter point before EVERY optimizer update.
    Stable MPO uses softmax(P), not a tiny positive mass divided by itself.
    """
    _validate(scores, groups, objective)
    work = scores.float() if scores.dtype in (torch.float16, torch.bfloat16) else scores.detach()
    coefficients = torch.zeros_like(work)
    for group in groups:
        pi = torch.tensor(group.positive, device=work.device)
        ni = torch.tensor(group.negative, device=work.device)
        positive, negative = work[pi], work[ni]
        if objective == "margin":
            q = -torch.sigmoid(negative.mean() - positive.mean())
            cp, cn = q.expand_as(positive) / len(pi), -q.expand_as(negative) / len(ni)
        elif objective == "mpo":
            probabilities = torch.cat((positive, negative)).softmax(0)
            cp = probabilities[:len(pi)] - positive.softmax(0)
            cn = probabilities[len(pi):]
        elif objective == "softmax":
            q = -torch.sigmoid(torch.logsumexp(negative, 0) - positive)
            cp, cn = q / len(pi), -q.mean() * negative.softmax(0)
        else:
            q = -torch.sigmoid(negative[None, :] - positive[:, None])
            cp, cn = q.mean(1) / len(pi), -q.mean(0) / len(ni)
        coefficients.index_add_(0, pi, cp / len(groups))
        coefficients.index_add_(0, ni, cn / len(groups))
    return coefficients.detach()


@torch.no_grad()
def positive_nll_weights(scores: Tensor, groups: Sequence[PreferenceGroup]) -> Tensor:
    """Mean positive NLL within each group, then mean over the full batch."""
    _validate(scores, groups, "all_pairs")
    weights = torch.zeros_like(scores)
    for group in groups:
        indices = torch.tensor(group.positive, device=scores.device)
        weights.index_add_(0, indices, scores.new_full((len(indices),), 1 / (len(groups) * len(indices))))
    return weights.detach()


def backward_microbatched(score_fn: Callable[[Tensor], Tensor], reference_logps: Tensor,
                         groups: Sequence[PreferenceGroup], *, objective: str = "all_pairs",
                         beta: float = 2., nll_coef: float = 1., microbatch_size: int = 1) -> dict:
    """Accumulate one exact optimizer-batch gradient without a joint graph.

    score_fn receives global response indices and returns response-length-MEAN
    policy log probabilities. It must be deterministic and response-independent
    across batch partitions (disable dropout/batch-stat updates). Reference is
    frozen; caller zeroes grads before this call and steps ONCE after it. Replay
    is checked before each backward; on a mismatch caller must discard/zero any
    already accumulated gradients. This function never steps an optimizer.

    Returns the actual original objective and separately the surrogate VALUE;
    only gradients, not values or higher derivatives, are guaranteed equal.
    """
    if (not math.isfinite(beta) or beta <= 0 or not math.isfinite(nll_coef) or nll_coef < 0
            or isinstance(microbatch_size, bool) or not isinstance(microbatch_size, int)
            or microbatch_size < 1):
        raise ValueError("positive beta/microbatch and nonnegative finite NLL coefficient required")
    _validate(reference_logps, groups, objective)
    reference = reference_logps.detach()
    slices = [torch.arange(i, min(i + microbatch_size, len(reference)), device=reference.device)
              for i in range(0, len(reference), microbatch_size)]
    with torch.no_grad():
        values = [score_fn(indices) for indices in slices]
        if any(v.shape != indices.shape or v.device != reference.device for v, indices in zip(values, slices)):
            raise ValueError("score callback must return one same-device value per index")
        policy = torch.cat(values)
        scores = beta * (policy - reference)
        _validate(scores, groups, objective)
        coefficients = precompute_coefficients(scores, groups, objective)
        nll_weights = positive_nll_weights(scores, groups)
        original = group_objective(scores, groups, objective) - nll_coef * (nll_weights * policy).sum()
    surrogate_value = 0.
    replay_error = 0.
    for indices in slices:
        current = score_fn(indices)
        if (current.shape != indices.shape or current.device != reference.device
                or not current.requires_grad or not bool(torch.isfinite(current).all())):
            raise ValueError("backward callback must return finite differentiable response scores")
        error = float((current.detach() - policy[indices]).abs().max())
        replay_error = max(replay_error, error)
        if not torch.allclose(current.detach(), policy[indices], rtol=1e-6, atol=1e-8):
            raise ValueError("score replay changed: disable stochastic/stateful/batch-dependent forward; discard gradients")
        term = (coefficients[indices] * beta * (current - reference[indices])
                - nll_coef * nll_weights[indices] * current).sum()
        surrogate_value += float(term.detach())
        term.backward()  # No retain_graph and no graph kept across microbatches.
    return {"objective_value": float(original), "surrogate_value": surrogate_value,
            "response_count": len(reference), "group_count": len(groups),
            "backward_microbatches": len(slices), "max_forward_microbatch": max(len(s) for s in slices),
            "replay_error": replay_error, "coefficients_detached": not coefficients.requires_grad,
            "reference_detached": not reference.requires_grad}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Four objectives x SGD/AdamW x three tiny genuine parameter updates."""
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("integer seed required")
    dev = torch.device(device)
    if dev.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    groups = (PreferenceGroup((0, 1), (2,)), PreferenceGroup((3,), (4, 5, 6)), PreferenceGroup((7,), (8,)))
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        features = torch.randn(9, 5, dtype=torch.float64).to(dev)
        labels = torch.randint(0, 7, (9,)).to(dev)
        base = torch.nn.Linear(5, 7).to(device=dev, dtype=torch.float64)
        reference_model = torch.nn.Linear(5, 7).to(device=dev, dtype=torch.float64)
    reference_model.requires_grad_(False)
    reference = reference_model(features).log_softmax(-1).gather(1, labels[:, None]).squeeze(1).detach()
    grad_error = parameter_error = loss_error = 0.
    parameter_delta = 0.
    max_microbatch = 0
    for objective in OBJECTIVES:
        for optimizer_type in (torch.optim.SGD, torch.optim.AdamW):
            naive, streamed = deepcopy(base), deepcopy(base)
            optimizers = [optimizer_type(model.parameters(), lr=.02) for model in (naive, streamed)]
            initial = torch.cat([p.detach().flatten().clone() for p in streamed.parameters()])
            for _ in range(3):
                for optimizer in optimizers:
                    optimizer.zero_grad(set_to_none=True)
                policy = naive(features).log_softmax(-1).gather(1, labels[:, None]).squeeze(1)
                scores = 2 * (policy - reference)
                nll_weights = positive_nll_weights(scores, groups)
                loss = group_objective(scores, groups, objective) - (nll_weights * policy).sum()
                loss.backward()

                def score(indices):
                    return streamed(features[indices]).log_softmax(-1).gather(1, labels[indices, None]).squeeze(1)

                audit = backward_microbatched(score, reference, groups, objective=objective, microbatch_size=2)
                max_microbatch = max(max_microbatch, audit["max_forward_microbatch"])
                loss_error = max(loss_error, abs(audit["objective_value"] - float(loss.detach())))
                for left, right in zip(naive.parameters(), streamed.parameters()):
                    grad_error = max(grad_error, float((left.grad - right.grad).abs().max()))
                for optimizer in optimizers:
                    optimizer.step()
                for left, right in zip(naive.parameters(), streamed.parameters()):
                    parameter_error = max(parameter_error, float((left.detach() - right.detach()).abs().max()))
            final = torch.cat([p.detach().flatten() for p in streamed.parameters()])
            parameter_delta = max(parameter_delta, float((final - initial).norm()))
    return {"seed": seed, "metrics": {
        "gradient_reference_error": grad_error, "parameter_reference_error": parameter_error,
        "objective_reference_error": loss_error, "student_parameter_delta": parameter_delta,
        "surrogate_optimizer_updates": 24, "objectives": len(OBJECTIVES),
        "response_count": len(reference), "max_forward_microbatch": max_microbatch},
        "checks": {"gradient_matches_joint": grad_error < 1e-10,
                   "multistep_sgd_adamw_match": parameter_error < 1e-10,
                   "original_objective_matches": loss_error < 1e-10,
                   "real_parameter_updates": parameter_delta > 0,
                   "whole_group_coefficients_microbatch_backward": max_microbatch == 2 < len(reference),
                   "frozen_reference": all(p.grad is None for p in reference_model.parameters())}}
