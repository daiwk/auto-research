"""MS-GLA multi-scale decomposition, causal hold and learned fusion."""

from __future__ import annotations

import math


def _symmetric_quantize(tensor, bits: int, scale=None):
    """Symmetric fake quantization used by the two recurrent-state papers."""
    import torch

    if bits < 2 or bits > 16:
        raise ValueError("bits must be in [2, 16]")
    limit = 2 ** (bits - 1) - 1
    if scale is None:
        scale = tensor.abs().amax().clamp_min(torch.finfo(tensor.dtype).eps) / limit
    quantized = torch.round(tensor / scale).clamp(-limit, limit)
    return quantized * scale, scale


def lifetime_weight(log_retention, horizon: int):
    """STEPQuant Eq. (7), including the stable unit-retention limit."""
    import torch

    if horizon < 1:
        raise ValueError("horizon must be positive")
    ratio = torch.exp(2 * log_retention)
    denominator = 1 - ratio
    geometric = (1 - ratio.pow(horizon)) / denominator.clamp_min(1e-12)
    return torch.where(denominator.abs() < 1e-8, torch.full_like(ratio, float(horizon)), geometric)


def stepquant_bit_allocation(distortions, log_retention, bit_options, average_bits: float, sizes=None):
    """Solve STEPQuant Eq. (8) by exact multiple-choice dynamic programming.

    ``distortions[u, j]`` is the calibrated distortion for unit ``u`` at
    ``bit_options[j]``.  The returned map is fixed across requests, matching
    the paper's post-training calibration contract.
    """
    import numpy as np

    distortions = np.asarray(distortions, dtype=np.float64)
    retention = np.asarray(log_retention, dtype=np.float64)
    bits = tuple(int(value) for value in bit_options)
    if distortions.ndim != 2 or distortions.shape[1] != len(bits):
        raise ValueError("distortions must be [units, bit options]")
    if retention.shape != (distortions.shape[0],):
        raise ValueError("one log-retention value is required per unit")
    sizes = np.ones(distortions.shape[0], dtype=np.int64) if sizes is None else np.asarray(sizes, dtype=np.int64)
    if sizes.shape != retention.shape or np.any(sizes <= 0):
        raise ValueError("sizes must be positive and match units")
    budget = int(math.floor(float(average_bits) * int(sizes.sum())))
    weights = np.asarray([
        sum(math.exp(2 * step * value) for step in range(128)) for value in retention
    ])
    states = {0: (0.0, ())}
    for unit in range(distortions.shape[0]):
        next_states = {}
        for used, (cost, choices) in states.items():
            for option, bit in enumerate(bits):
                total = used + bit * int(sizes[unit])
                if total > budget:
                    continue
                candidate = (cost + weights[unit] * distortions[unit, option], choices + (bit,))
                if total not in next_states or candidate[0] < next_states[total][0]:
                    next_states[total] = candidate
        states = next_states
    if not states:
        raise ValueError("bit budget cannot accommodate the minimum precision")
    used = min(states, key=lambda value: (states[value][0], -value))
    return {"bits": np.asarray(states[used][1], dtype=np.int64), "weighted_distortion": states[used][0], "used_bits": used, "budget_bits": budget}


def stepquant_dual_axis(state, row_impact, bits: int = 6, iterations: int = 4):
    """STEPQuant Eqs. (11)-(14): impact-aware row and column fitting."""
    import torch

    if state.ndim != 2 or row_impact.shape != state.shape[:1]:
        raise ValueError("state must be [key rows, value columns] with one row impact per row")
    eps = torch.finfo(state.dtype).eps
    magnitude = state.abs().mean(dim=1).clamp_min(eps)
    impact = row_impact.to(state).clamp_min(eps)
    row_scale = magnitude.sqrt() / impact.sqrt()
    column_scale = torch.ones(state.shape[1], device=state.device, dtype=state.dtype)
    limit = 2 ** (bits - 1) - 1
    for _ in range(iterations):
        normalized = state / (row_scale[:, None] * column_scale[None, :]).clamp_min(eps)
        codes = normalized.round().clamp(-limit, limit)
        numerator = ((impact[:, None] * row_scale[:, None] * codes) * (impact[:, None] * state)).sum(dim=0)
        denominator = (impact[:, None] * row_scale[:, None] * codes).square().sum(dim=0).clamp_min(eps)
        column_scale = (numerator / denominator).abs().clamp_min(eps)
    restored = row_scale[:, None] * column_scale[None, :] * codes
    return restored, {"row_scale": row_scale, "column_scale": column_scale, "codes": codes}


def leapquant_compress(state, *, bits: int = 8, rank: int = 1):
    """LeapQuant Eqs. (5)-(6): low-bit residual plus compensator tokens."""
    import torch

    if state.ndim != 2 or rank < 0 or rank > min(state.shape):
        raise ValueError("invalid state or compensator rank")
    if rank:
        left, singular, right = torch.linalg.svd(state.float(), full_matrices=False)
        compensator = (left[:, :rank] * singular[:rank]) @ right[:rank]
        compensator = compensator.to(state.dtype)
    else:
        compensator = torch.zeros_like(state)
    residual = state - compensator
    quantized, scale = _symmetric_quantize(residual, bits)
    return quantized + compensator, {"quantized_residual": quantized, "compensator": compensator, "scale": scale}


def leapquant_window(boundary_state, decays, keys, corrections, *, bits: int = 8, rank: int = 1):
    """LeapQuant Eq. (4): buffer updates and quantize only at a window boundary."""
    if decays.ndim != 2 or keys.shape != corrections.shape or keys.ndim != 2:
        raise ValueError("decays, keys and corrections must be [time, dimension]")
    if boundary_state.shape != (keys.shape[1], corrections.shape[1]):
        raise ValueError("boundary state shape must match update dimensions")
    state = boundary_state
    outputs = []
    for decay, key, correction in zip(decays, keys, corrections):
        state = decay[:, None] * state + key[:, None] * correction[None, :]
        outputs.append(state)
    compressed, audit = leapquant_compress(state, bits=bits, rank=rank)
    audit["intermediate_states"] = outputs
    return compressed, audit


def chinese_jev_objective(logits, targets, decision_types, *, perturbations: int = 4, sigma: float = 0.3, generator=None):
    """Chinese-Jev CE plus RLCD objective from Eqs. (6)-(13)."""
    import torch
    import torch.nn.functional as F

    if logits.shape != targets.shape or logits.ndim != 2:
        raise ValueError("logits and target distributions must be [batch, candidates]")
    if decision_types.shape != logits.shape[:1]:
        raise ValueError("one decision type per batch row is required")
    targets = targets / targets.sum(-1, keepdim=True).clamp_min(1e-12)
    ce = -(targets * torch.log_softmax(logits, -1)).sum(-1).mean()
    noise = torch.randn((*logits.shape[:1], perturbations, logits.shape[-1]), device=logits.device, dtype=logits.dtype, generator=generator) * sigma
    noise = noise - noise.mean(-1, keepdim=True)
    sampled_logits = logits.detach()[:, None, :] + noise
    probabilities = torch.softmax(sampled_logits, -1)
    target = targets[:, None, :]
    log_score = (target * probabilities.clamp_min(math.exp(-9.21)).log()).sum(-1)
    spherical = 0.75 * (target * probabilities).sum(-1) / probabilities.square().sum(-1).sqrt().clamp_min(1e-12)
    cumulative = (probabilities - target).cumsum(-1)[..., :-1]
    rps = cumulative.square().mean(-1)
    ordered = (decision_types == 2).to(logits.dtype)[:, None]
    rewards = log_score + spherical - ordered * rps
    advantages = rewards - rewards.mean(-1, keepdim=True)
    advantages = advantages / advantages.std().clamp_min(1e-6)
    gaussian_log_prob = -noise.square().sum(-1) / (2 * sigma**2)
    rlcd = -(advantages.detach() * gaussian_log_prob).mean()
    return ce + rlcd, {"cross_entropy": float(ce.detach()), "rlcd": float(rlcd.detach()), "reward_std": float(rewards.std().detach())}


class ChineseJevHead:
    """Compact executable candidate-marker head preserving Chinese-Jev Eq. (5)."""

    def __new__(cls, hidden_size: int, decision_types: int = 3):
        import torch.nn as nn

        class _Head(nn.Module):
            def __init__(self):
                super().__init__()
                self.type_embedding = nn.Embedding(decision_types, hidden_size)
                self.decision = nn.TransformerEncoderLayer(hidden_size, 4, 2 * hidden_size, batch_first=True)
                self.scorer = nn.Sequential(nn.Linear(hidden_size, hidden_size), nn.GELU(), nn.Linear(hidden_size, 1))

            def forward(self, candidate_hidden, decision_type):
                hidden = candidate_hidden + self.type_embedding(decision_type)[:, None, :]
                return self.scorer(self.decision(hidden)).squeeze(-1)

        return _Head()


def masked_block_average(hidden, scale: int, attention_mask=None):
    """Equation (8): right-padded, non-overlapping masked average pooling."""
    import torch
    import torch.nn.functional as F

    if hidden.ndim != 3 or scale < 1:
        raise ValueError("hidden must be [batch, time, dim] and scale positive")
    batch, length, dim = hidden.shape
    if attention_mask is None:
        attention_mask = torch.ones(batch, length, device=hidden.device, dtype=hidden.dtype)
    if attention_mask.shape != (batch, length):
        raise ValueError("attention_mask must be [batch, time]")
    padded_length = math.ceil(length / scale) * scale
    pad = padded_length - length
    padded_hidden = F.pad(hidden, (0, 0, 0, pad))
    padded_mask = F.pad(attention_mask.to(hidden.dtype), (0, pad))
    blocks = padded_hidden.reshape(batch, -1, scale, dim)
    mask_blocks = padded_mask.reshape(batch, -1, scale, 1)
    pooled = (blocks * mask_blocks).sum(dim=2) / mask_blocks.sum(dim=2).clamp_min(1)
    pooled_mask = (mask_blocks.sum(dim=2).squeeze(-1) > 0).to(attention_mask.dtype)
    return pooled, pooled_mask


def causal_hold_upsample(branch_output, scale: int, target_length: int):
    """Equation (10) alignment: reveal a block only after its last token."""
    import torch.nn.functional as F

    if scale < 1:
        raise ValueError("scale must be positive")
    repeated = branch_output.repeat_interleave(scale, dim=1)
    if scale > 1:
        repeated = F.pad(repeated, (0, 0, scale - 1, 0))
    return repeated[:, :target_length]


def fuse_scales(hidden, aligned_outputs, fusion_projection):
    """Equations (10)-(11): input-dependent softmax routing across scales."""
    import torch

    if not aligned_outputs:
        raise ValueError("at least one scale output is required")
    stacked = torch.stack(aligned_outputs, dim=2)
    weights = torch.softmax(fusion_projection(hidden), dim=-1)
    if weights.shape != stacked.shape[:3]:
        raise ValueError("fusion projection scale count differs from outputs")
    return (stacked * weights.unsqueeze(-1)).sum(dim=2), weights


def gated_linear_recurrence(hidden, in_projection, out_projection):
    """Small recurrent GLA branch used for executable mechanism validation."""
    import torch

    q, k, value, gate = in_projection(hidden).chunk(4, dim=-1)
    gate = torch.sigmoid(gate)
    state = torch.zeros(
        hidden.shape[0], hidden.shape[-1], hidden.shape[-1],
        device=hidden.device, dtype=hidden.dtype,
    )
    outputs = []
    for index in range(hidden.shape[1]):
        decay = gate[:, index].unsqueeze(-1)
        state = decay * state + torch.einsum("bi,bj->bij", k[:, index], value[:, index])
        outputs.append(torch.einsum("bi,bij->bj", q[:, index], state))
    return out_projection(torch.stack(outputs, dim=1))


class MultiScaleGLA:
    """A compact executable MS-GLA layer preserving the paper's three stages.

    This implementation validates the architecture rather than the paper's
    flash-linear-attention kernel or matched 340M parameter training recipe.
    """

    def __new__(cls, hidden_size: int, scales=(1, 2, 4)):
        import torch.nn as nn

        if not scales or any(scale < 1 for scale in scales) or len(set(scales)) != len(scales):
            raise ValueError("scales must be unique positive integers")

        class _Layer(nn.Module):
            def __init__(self):
                super().__init__()
                self.scales = tuple(scales)
                self.in_projections = nn.ModuleList(
                    nn.Linear(hidden_size, 4 * hidden_size) for _ in self.scales
                )
                self.out_projections = nn.ModuleList(
                    nn.Linear(hidden_size, hidden_size) for _ in self.scales
                )
                self.fusion = nn.Linear(hidden_size, len(self.scales))

            def forward(self, hidden, attention_mask=None):
                aligned = []
                for scale, in_projection, out_projection in zip(
                    self.scales, self.in_projections, self.out_projections
                ):
                    pooled, _ = masked_block_average(hidden, scale, attention_mask)
                    branch = gated_linear_recurrence(pooled, in_projection, out_projection)
                    aligned.append(causal_hold_upsample(branch, scale, hidden.shape[1]))
                output, weights = fuse_scales(hidden, aligned, self.fusion)
                return output, {"routing_weights": weights, "scales": self.scales}

        return _Layer()
