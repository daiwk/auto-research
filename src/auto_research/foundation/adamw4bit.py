"""Packed-state AdamW reference for arXiv:2610.12444, not a fused kernel.

ZIP-SR rounds v in bias-corrected preconditioner coordinates. ZE-EDEN
uses the zero-excluding Dyn4 grid with guarded block-scale calibration.
Parameters/gradients and temporary moments remain floating point; only the
persistent eligible moments use packed uint8 codes plus FP32 block scales.
"""

from __future__ import annotations

import math
import torch


NF4 = (-1., -.6961928, -.5250731, -.3949175, -.2844414, -.1847734,
       -.0910500, 0., .0795803, .1609302, .2461123, .3379152,
       .4407098, .5626170, .7229568, 1.)


def dynamic4(device):
    levels = [0., 1.]
    for exponent in range(3):
        edges = torch.linspace(.1, 1., 2 ** (exponent + 1) + 1)
        levels.extend(((edges[:-1] + edges[1:]) * .5 * 10 ** (exponent - 2)).tolist())
    return torch.tensor(sorted(levels), device=device, dtype=torch.float32)


def pack4(codes):
    if codes.numel() % 2 or bool((codes > 15).any()):
        raise ValueError("packing requires even length and four-bit codes")
    flat = codes.flatten().to(torch.uint8)
    return flat[0::2] | (flat[1::2] << 4)


def unpack4(packed):
    return torch.stack((packed & 15, packed >> 4), -1).flatten().long()


def rounding_probabilities(values, left, right, *, bias_correction, eps):
    """Probability of lower v level, Eq.1; compute tiny zero-cell p directly."""
    if not 0 < bias_correction <= 1 or eps <= 0:
        raise ValueError("positive epsilon and valid bias correction required")
    h = lambda x: (x.clamp_min(0).div(bias_correction).sqrt() + eps).reciprocal()
    denominator = h(left) - h(right)
    return torch.where(right > left,
                       (h(values) - h(right)) / denominator.clamp_min(1e-30),
                       torch.ones_like(values)).clamp(0, 1)


def quantize_blockwise(values, *, block_size, scheme, bias_correction=1., eps=1e-8):
    if values.numel() % block_size:
        raise ValueError("eligible tensors must contain complete blocks")
    blocks = values.float().reshape(-1, block_size)
    scale = blocks.abs().amax(-1).clamp_min(1e-30)
    normalized = (blocks / scale[:, None]).contiguous()
    signed = scheme in {"nf4", "nf4-sr"}
    book = torch.tensor(NF4, device=values.device) if signed else dynamic4(values.device)
    right = torch.searchsorted(book, normalized).clamp(max=15)
    left = (right - 1).clamp_min(0)
    a, b = book[left], book[right]
    if scheme == "zip-sr":
        probability = rounding_probabilities(blocks, a * scale[:, None], b * scale[:, None],
                                               bias_correction=bias_correction, eps=eps)
        codes = torch.where(torch.rand_like(probability) < probability, left, right)
    elif scheme == "nf4-sr":
        probability = ((b - normalized) / (b - a).clamp_min(1e-30)).clamp(0, 1)
        codes = torch.where(torch.rand_like(probability) < probability, left, right)
    elif scheme in {"nf4", "ze-eden"}:
        codes = torch.where(normalized - a <= b - normalized, left, right)
        if scheme == "ze-eden":
            codes = codes.clamp_min(1)
            decoded = book[codes]
            calibration = normalized.square().sum(-1) / (
                normalized * decoded).sum(-1).clamp_min(1e-12)
            scale = scale * calibration
    else:
        raise ValueError(f"unknown quantization recipe {scheme}")
    return pack4(codes), scale


def decode_blockwise(packed, scale, *, block_size, signed, shape):
    book = torch.tensor(NF4, device=packed.device) if signed else dynamic4(packed.device)
    return (book[unpack4(packed)].reshape(-1, block_size) * scale[:, None]).reshape(shape)


class AdamW4Bit(torch.optim.Optimizer):
    """Portable eager reference. Uses global torch RNG; save RNG to resume SR.

    Eligible tensors: >=4096 elements, divisible by block_size (default 128).
    Noneligible tensors keep FP32 states as in the author's recipe. No latency
    improvement is promised: decode/update/encode uses floating-point workspace.
    """

    def __init__(self, params, *, recipe="zip-sr", lr=1e-3, betas=(.9, .95),
                 eps=1e-8, weight_decay=.1, block_size=128):
        if recipe not in {"zip-sr", "ze-eden"} or not isinstance(block_size, int) or block_size < 2 or block_size % 2:
            raise ValueError("invalid recipe or even block size")
        if not all(math.isfinite(x) for x in (lr, eps, weight_decay, *betas)):
            raise ValueError("optimizer settings must be finite")
        if lr <= 0 or eps <= 0 or weight_decay < 0 or not all(0 <= x < 1 for x in betas):
            raise ValueError("invalid AdamW settings")
        super().__init__(params, dict(lr=lr, betas=betas, eps=eps,
                                    weight_decay=weight_decay, block_size=block_size, recipe=recipe))
        self._head_ids = set()
        self._head_sr = False

    def schedule_lm_head(self, parameters, *, completed_steps, total_steps):
        if total_steps < 1 or not 0 <= completed_steps < total_steps:
            raise ValueError("invalid optimizer-step budget")
        self._head_ids = {id(parameter) for parameter in parameters}
        self._head_sr = completed_steps >= round(.9 * total_steps)

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            beta1, beta2 = group["betas"]
            block_size = group["block_size"]
            for parameter in group["params"]:
                if parameter.grad is None:
                    continue
                if parameter.grad.is_sparse or parameter.is_complex():
                    raise ValueError("sparse gradients and complex parameters are unsupported")
                state = self.state[parameter]
                packed = parameter.numel() >= 4096 and parameter.numel() % block_size == 0
                if not state:
                    state["step"] = 0
                    # Exactly-zero initial working moments, including ZE-EDEN.
                    m, v = torch.zeros_like(parameter, dtype=torch.float32), torch.zeros_like(parameter, dtype=torch.float32)
                elif packed:
                    m = decode_blockwise(state["m_codes"], state["m_scale"], block_size=block_size, signed=True, shape=parameter.shape)
                    v = decode_blockwise(state["v_codes"], state["v_scale"], block_size=block_size, signed=False, shape=parameter.shape)
                else:
                    m, v = state["m"], state["v"]
                state["step"] += 1
                step = state["step"]
                gradient = parameter.grad.float()
                m.mul_(beta1).add_(gradient, alpha=1 - beta1)
                v.mul_(beta2).addcmul_(gradient, gradient, value=1 - beta2)
                parameter.mul_(1 - group["lr"] * group["weight_decay"])
                update = m.div(1 - beta1**step) / (v.div(1 - beta2**step).sqrt() + group["eps"])
                parameter.add_(update.to(parameter.dtype), alpha=-group["lr"])
                # The current update always uses working FP32 moments; the
                # quantized moments affect only future recurrences.
                if packed:
                    scheme = "nf4-sr" if self._head_sr and id(parameter) in self._head_ids else "nf4"
                    state["m_codes"], state["m_scale"] = quantize_blockwise(m, block_size=block_size, scheme=scheme)
                    state["v_codes"], state["v_scale"] = quantize_blockwise(
                        v, block_size=block_size, scheme=group["recipe"],
                        bias_correction=1 - beta2**step, eps=group["eps"])
                else:
                    state["m"], state["v"] = m, v
        return loss

    def load_state_dict(self, state_dict):
        # torch Optimizer casts floating state to parameter dtype; packed bytes
        # and FP32 scales must retain their storage types after a BF16 resume.
        result = super().load_state_dict(state_dict)
        for group, original_group in zip(self.param_groups, state_dict["param_groups"]):
            for parameter, identifier in zip(group["params"], original_group["params"]):
                state = self.state.get(parameter, {})
                original = state_dict["state"].get(identifier, {})
                for key in ("m_codes", "v_codes"):
                    if key in state:
                        state[key] = original[key].to(device=parameter.device, dtype=torch.uint8)
                for key in ("m_scale", "v_scale", "m", "v"):
                    if key in state:
                        state[key] = original[key].to(device=parameter.device, dtype=torch.float32)
        return result
