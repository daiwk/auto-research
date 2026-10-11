"""ReCal damage-weighted calibration and genuine gated-FFN channel deletion."""
from __future__ import annotations

import torch
from torch import nn


def coarsened_forward_kl(teacher_logits, probe_logits, topk=16):
    """Teacher Top-k original masses plus residual bucket, appendix Eq.12."""
    if teacher_logits.shape != probe_logits.shape or not 1 <= topk < teacher_logits.shape[-1]:
        raise ValueError("aligned vocabulary and a proper Top-k subset required")
    t, p = teacher_logits.detach().float().log_softmax(-1), probe_logits.detach().float().log_softmax(-1)
    values, indices = t.topk(topk, dim=-1)
    selected_p = p.gather(-1, indices)
    mass_t, mass_p = values.exp(), selected_p.exp()
    other_t = (1 - mass_t.sum(-1)).clamp_min(1e-12)
    other_p = (1 - mass_p.sum(-1)).clamp_min(1e-12)
    return ((mass_t * (values - selected_p)).sum(-1)
            + other_t * (other_t.log() - other_p.log())).clamp_min(0)


def damage_weights(damage, response_mask):
    """Per-response unit mass, negligible-damage fallback is response-uniform."""
    if damage.shape != response_mask.shape or not bool(response_mask.bool().any(-1).all()):
        raise ValueError("nonempty aligned response masks required")
    d = damage.detach().masked_fill(~response_mask.bool(), 0)
    if not bool(torch.isfinite(d).all()) or bool((d < 0).any()):
        raise ValueError("finite nonnegative damage required")
    total = d.sum(-1, keepdim=True)
    uniform = response_mask.float() / response_mask.sum(-1, keepdim=True)
    return torch.where(total > 1e-9, d / total.clamp_min(1e-9), uniform)


def wanda_channel_score(activations, token_weights, down_weight):
    """Wanda-SP Eq.9: column L2 norm times weighted activation RMS."""
    if activations.shape[:-1] != token_weights.shape or activations.shape[-1] != down_weight.shape[1]:
        raise ValueError("unaligned gated activations, response weights or down projection")
    if not torch.allclose(token_weights.sum(-1), torch.ones_like(token_weights.sum(-1)), atol=1e-5):
        raise ValueError("each response must carry unit calibration mass")
    second = (activations.detach().float().square() * token_weights[..., None]).sum(-2).mean(0)
    return down_weight.detach().float().norm(dim=0) * second.sqrt()


def _slice_linear(layer, indices, dimension):
    if not isinstance(layer, nn.Linear):
        raise ValueError("prune base Linear weights before installing any adapters")
    shape = list(layer.weight.shape)
    shape[dimension] = len(indices)
    result = nn.Linear(shape[1], shape[0], bias=layer.bias is not None,
                       device=layer.weight.device, dtype=layer.weight.dtype)
    with torch.no_grad():
        result.weight.copy_(layer.weight.index_select(dimension, indices))
        if layer.bias is not None:
            result.bias.copy_(layer.bias.index_select(0, indices) if dimension == 0 else layer.bias)
    result.requires_grad_(layer.weight.requires_grad)
    return result


def prune_gated_ffn(mlp, retained_indices):
    """Physically delete gate/up rows and down columns; no zero-mask proxy."""
    indices = torch.as_tensor(retained_indices, dtype=torch.long, device=mlp.gate_proj.weight.device)
    width = mlp.gate_proj.out_features
    if indices.ndim != 1 or not 0 < indices.numel() < width or indices.unique().numel() != indices.numel():
        raise ValueError("a nonempty unique proper channel subset is required")
    if int(indices.min()) < 0 or int(indices.max()) >= width:
        raise ValueError("invalid retained channel index")
    if mlp.up_proj.out_features != width or mlp.down_proj.in_features != width:
        raise ValueError("incompatible gated FFN projections")
    mlp.gate_proj = _slice_linear(mlp.gate_proj, indices, 0)
    mlp.up_proj = _slice_linear(mlp.up_proj, indices, 0)
    mlp.down_proj = _slice_linear(mlp.down_proj, indices, 1)
    if hasattr(mlp, "intermediate_size"):
        mlp.intermediate_size = len(indices)


def restricted_opd_loss(student_logits, teacher_logits, rollout_logits, mask, *, topk=16, clip=.2):
    """Appendix Eqs.13-14: student support, original log-prob normalization."""
    if student_logits.shape != teacher_logits.shape or student_logits.shape != rollout_logits.shape:
        raise ValueError("aligned current/teacher/rollout distributions required")
    if mask.shape != student_logits.shape[:-1] or not bool(mask.any()):
        raise ValueError("nonempty response mask required")
    old = rollout_logits.detach().float().log_softmax(-1)
    s, t = student_logits.float().log_softmax(-1), teacher_logits.detach().float().log_softmax(-1)
    old_top, ids = old.topk(min(topk, old.shape[-1]), dim=-1)
    teacher_top = t.gather(-1, ids)
    # Weights normalize only on rollout-student support; log gaps do not.
    advantage = -(old_top.softmax(-1) * (old_top - teacher_top)).detach()
    ratio = (s.gather(-1, ids) - old_top).exp()
    loss = torch.maximum(-advantage * ratio, -advantage * ratio.clamp(1 - clip, 1 + clip)).sum(-1)
    return (loss.masked_fill(~mask.bool(), 0).sum(-1) / mask.sum(-1)).mean()
