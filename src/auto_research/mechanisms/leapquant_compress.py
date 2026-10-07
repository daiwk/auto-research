"""Extracted unchanged from auto_research.foundation_latest_20260930; stable mechanism boundary."""
from __future__ import annotations



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
