"""ViMoD DART/TRACE operators (2610.12060), with actual recoverable KV banks.

Backbone adapters must supply causally observed hidden states and per-layer KV;
this module never obtains answers or future hidden states from an evaluator.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import nn
from torch.nn import functional as F


class _Capacity(torch.autograd.Function):
    @staticmethod
    def forward(ctx, score, prior, total, upper):
        groups = score.numel()
        if not groups <= total <= groups * upper or upper <= 1:
            raise ValueError("infeasible capacity bounds")
        if not torch.isfinite(score).all():
            raise ValueError("capacity scores must be finite")
        if total in (groups, groups * upper):
            out = torch.full_like(score, total / groups)
            derivative = torch.zeros_like(score)
        else:
            value = score + prior
            lo, hi = -value.max() - 60, -value.min() + 60
            for _ in range(80):
                mid = (lo + hi) / 2
                mass = (1 + (upper - 1) * torch.sigmoid(value + mid)).sum()
                lo, hi = (mid, hi) if mass < total else (lo, mid)
            p = torch.sigmoid(value + (lo + hi) / 2)
            out = 1 + (upper - 1) * p
            derivative = (upper - 1) * p * (1 - p)
        ctx.save_for_backward(derivative)
        return out

    @staticmethod
    def backward(ctx, grad):
        (d,) = ctx.saved_tensors
        result = d * (grad - (grad * d).sum() / d.sum().clamp_min(1e-20))
        return result, result, None, None


def capacities(score, initial_counts, upper):
    counts = initial_counts.to(score)
    eta = ((counts - 1) / (upper - 1)).clamp(1e-5, 1 - 1e-5)
    return _Capacity.apply(score, torch.logit(eta), int(counts.sum()), upper)


def integer_capacities(continuous, total):
    result = continuous.detach().floor().long()
    remaining = total - int(result.sum())
    if remaining < 0 or remaining > len(result):
        raise ValueError("capacity rounding failed")
    order = torch.argsort(continuous.detach() - result, descending=True, stable=True)
    result[order[:remaining]] += 1
    return result


@dataclass
class VisualMemory:
    coarse: torch.Tensor
    weights: torch.Tensor
    membership: torch.Tensor
    counts: torch.Tensor
    continuous_counts: torch.Tensor

    def fine_indices(self, active):
        if active.shape != self.counts.shape or active.dtype != torch.bool:
            raise ValueError("active groups must be a boolean group mask")
        return torch.where(active[self.membership])[0]


class DART(nn.Module):
    def __init__(self, dim, head_dim, affinity_dim=128, upper=18, epsilon=1.0):
        super().__init__()
        if epsilon <= 0:
            raise ValueError("positive Sinkhorn temperature required")
        self.upper, self.epsilon = upper, epsilon
        self.capacity = nn.Linear(dim, 1, bias=False)
        self.fine_projection = nn.Linear(dim, affinity_dim, bias=False)
        self.coarse_projection = nn.Linear(dim, affinity_dim, bias=False)
        self.grid_weight = nn.Parameter(torch.tensor(1.0))
        self.value_encoder = nn.Sequential(nn.LayerNorm(head_dim),
                                           nn.Linear(head_dim, head_dim * 2), nn.GELU(),
                                           nn.Linear(head_dim * 2, head_dim))
        nn.init.zeros_(self.capacity.weight)

    def forward(self, fine, grid):
        if fine.ndim != 2 or grid.shape != fine.shape[:1]:
            raise ValueError("one image fine bank and grid membership required")
        groups = int(grid.max()) + 1
        counts = torch.bincount(grid, minlength=groups)
        if (counts == 0).any() or (counts > self.upper).any():
            raise ValueError("initial grid must have nonempty bounded groups")
        initial = torch.stack([fine[grid == j].mean(0) for j in range(groups)])
        continuous = capacities(self.capacity(initial).squeeze(-1), counts, self.upper)
        integer = integer_capacities(continuous, len(fine))
        score = self.fine_projection(fine) @ self.coarse_projection(initial).T
        score = score / math.sqrt(self.fine_projection.out_features)
        score = score + self.grid_weight * F.one_hot(grid, groups).to(score)
        with torch.no_grad():
            ordered_scores = score.sort(-1, descending=True).values
            confidence = (ordered_scores[:, 0] - ordered_scores[:, 1]
                          if groups > 1 else torch.zeros(len(fine), device=fine.device))
            order = confidence.argsort(descending=True, stable=True)
            remaining = integer.clone()
            membership = torch.empty_like(grid)
            for i in order:
                j = score[i].masked_fill(remaining == 0, -torch.inf).argmax()
                membership[i] = j
                remaining[j] -= 1
        support = F.one_hot(membership, groups).bool()
        hard = score.masked_fill(~support, -torch.inf).softmax(0)
        # Log-domain balancing avoids overflow without detaching either score
        # or the differentiable, fixed-total column marginal.
        log_assignment = score / self.epsilon
        for _ in range(8):
            log_assignment = log_assignment - torch.logsumexp(log_assignment, 1, keepdim=True)
            log_assignment = (log_assignment - torch.logsumexp(log_assignment, 0, keepdim=True)
                              + continuous.log()[None])
        soft = log_assignment.softmax(0)
        weights = hard + soft - soft.detach() if self.training else hard
        return VisualMemory(weights.T @ fine, weights, membership, integer, continuous)

    def coarse_kv(self, memory, fine_key, fine_value):
        """Banks [heads, fine, head_dim]; encoder shared over heads and layers."""
        if fine_key.shape != fine_value.shape or fine_key.shape[-2] != len(memory.membership):
            raise ValueError("misaligned Fine KV bank")
        key = torch.einsum("nm,hnd->hmd", memory.weights, fine_key)
        value = fine_value + self.value_encoder(fine_value)
        value = torch.einsum("nm,hnd->hmd", memory.weights, value)
        return key, value


class TRACE(nn.Module):
    def __init__(self, hidden_dim, visual_dim, layers=3, state_dim=256, key_dim=128):
        super().__init__()
        self.fusion = nn.Parameter(torch.zeros(layers))
        self.adapter = nn.Linear(hidden_dim, state_dim)
        self.delta = nn.Linear(state_dim, state_dim)
        self.write = nn.Linear(state_dim, state_dim, bias=False)
        self.mixture = nn.Linear(state_dim, 4, bias=False)
        # softplus(theta)*softplus(delta(0)) ~= 1/timescale initially.
        scale = torch.tensor([1., 2., 4., 8.])
        theta = torch.log(torch.expm1(1 / scale / math.log(2)))
        self.theta = nn.Parameter(theta[:, None].expand(4, state_dim).clone())
        nn.init.zeros_(self.delta.weight)
        nn.init.zeros_(self.delta.bias)
        self.query = nn.Sequential(nn.RMSNorm(state_dim), nn.Linear(state_dim, key_dim, bias=False))
        self.key = nn.Sequential(nn.RMSNorm(visual_dim), nn.Linear(visual_dim, key_dim, bias=False))
        self.threshold = nn.Linear(state_dim, 1)
        self.gate = nn.Linear(state_dim + key_dim * 2, 2)

    def forward(self, hidden, coarse, previous, state=None, boundary_offset=0., gate_bias=0.):
        if hidden.ndim != 2 or hidden.shape[0] != len(self.fusion):
            raise ValueError("causal layer hidden states [layers, dim] required")
        u = self.adapter((hidden.detach() * self.fusion.softmax(0)[:, None]).sum(0))
        if state is None:
            state = torch.zeros_like(self.theta)
        rho = torch.exp(-F.softplus(self.theta) * F.softplus(self.delta(u))[None])
        state = rho * state + (1 - rho) * self.write(u)[None]
        z = (state * self.mixture(u).softmax(0)[:, None]).sum(0)
        keys = self.key(coarse.detach())
        logits = keys @ self.query(z) / math.sqrt(keys.shape[-1])
        logits = logits - self.threshold(z).squeeze() - boundary_offset
        probability = logits.sigmoid()
        retained = keys[previous].sum(0) / max(1, int(previous.sum()))
        proposed = (keys * probability[:, None]).sum(0) / (1e-8 + probability.sum())
        gate_logits = self.gate(torch.cat((z, retained, proposed)))
        gate_logits = gate_logits + torch.tensor([0., gate_bias], device=z.device)
        return {"region_logits": logits, "gate_logits": gate_logits, "state": state}

    @staticmethod
    def choose(output, previous, sample=False):
        gate_dist = torch.distributions.Categorical(logits=output["gate_logits"])
        gate = gate_dist.sample() if sample else output["gate_logits"].argmax()
        regions = torch.distributions.Bernoulli(logits=output["region_logits"])
        proposed = regions.sample().bool() if sample else output["region_logits"] > 0
        active = proposed if int(gate) == 1 else previous
        region_lp = (regions.log_prob(proposed.float()).sum() if int(gate) == 1
                     else output["region_logits"].sum() * 0)
        return active, gate_dist.log_prob(gate) + region_lp, region_lp, int(gate)


def joint_kv(memory, active, coarse_kv, fine_kv, text_kv):
    indices = memory.fine_indices(active)
    return tuple(torch.cat((coarse, fine[:, indices], text), dim=-2)
                 for coarse, fine, text in zip(coarse_kv, fine_kv, text_kv, strict=True))


def balanced_set_loss(logits, labels):
    labels = labels.bool()
    positive = -F.logsigmoid(logits[labels]).sum() / labels.sum().clamp_min(1)
    negative = -F.logsigmoid(-logits[~labels]).sum() / (~labels).sum().clamp_min(1)
    return positive + negative


def dart_distillation(student_logits, teacher_logits, targets, mask):
    if not mask.any():
        raise ValueError("nonempty verified response required")
    logp = student_logits.float().log_softmax(-1)
    q = teacher_logits.detach().float().softmax(-1)
    ce = -logp.gather(-1, targets[..., None]).squeeze(-1)[mask].mean()
    kl = (q * (q.clamp_min(1e-30).log() - logp)).sum(-1)[mask].mean()
    return ce + 2 * kl


def trace_policy_loss(all_logp, region_logp, correctness, occupancy):
    if len(correctness) < 2:
        raise ValueError("RLOO needs at least two independent rollouts")
    correctness, occupancy = correctness.detach(), occupancy.detach()
    accuracy_adv = 2 * correctness - 2 * (correctness.sum() - correctness) / (len(correctness) - 1)
    successes = correctness > 0
    cost_adv = torch.zeros_like(occupancy)
    if int(successes.sum()) >= 2:
        cost_adv[successes] = occupancy[successes].mean() - occupancy[successes]
    return -(accuracy_adv * all_logp + .5 * cost_adv * region_logp).mean()


def online_teacher_loss(logits, labels, valid):
    labels, valid = labels.bool(), valid.bool()
    chosen = labels[valid]
    if not len(chosen) or not chosen.any() or chosen.all():
        return logits.sum() * 0
    return F.binary_cross_entropy_with_logits(logits[valid], chosen.float())


def auxiliary_call_loss(update_logits, all_failed, any_autonomous_update):
    if not all_failed or any_autonomous_update:
        return update_logits.sum() * 0
    log_no_update = F.logsigmoid(-update_logits).sum()
    return -torch.log((-torch.expm1(log_no_update)).clamp_min(1e-12))
