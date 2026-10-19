"""FPoT weight grids and integer PE simulation (arXiv:2610.21257).

This is an operator implementation, not OSTQuant/GPTQ or a fast GPU kernel.
The approximate-grid calibration searches the grid actually used at inference.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence

import torch


@dataclass(frozen=True)
class FPoTCodes:
    signs: torch.Tensor
    magnitudes: torch.Tensor
    scales: torch.Tensor
    bits: int
    resolution: int
    approximate: bool


def _configuration(bits: int, resolution: int, approximate: bool) -> int:
    if isinstance(bits, bool) or not isinstance(bits, int) or not 2 <= bits <= 8:
        raise ValueError("bits must be an integer in [2,8]")
    if isinstance(resolution, bool) or not isinstance(resolution, int) or resolution < 1:
        raise ValueError("positive integer exponent resolution required")
    if approximate and resolution != 2:
        raise ValueError("the one-adder approximation is defined only for resolution=2")
    return 2 ** (bits - 1) - 2


def _levels(exponents: torch.Tensor, resolution: int, approximate: bool) -> torch.Tensor:
    if approximate:
        return torch.exp2(exponents.div(2, rounding_mode="floor")) * torch.where(
            exponents.remainder(2) == 0, 1., 1.5)
    return torch.exp2(exponents / resolution)


def _encode(weight: torch.Tensor, scales: torch.Tensor, bits: int, resolution: int,
            approximate: bool) -> FPoTCodes:
    emax = _configuration(bits, resolution, approximate)
    normalized = weight.abs() / scales[:, None]
    if approximate:
        # Sec.3 ApproxGrid: nearest level in the actual 1.5 odd-exponent grid,
        # NOT exact-log-grid quantization followed by coefficient replacement.
        exponents = torch.arange(emax + 1, device=weight.device, dtype=weight.dtype)
        levels = _levels(exponents, resolution, True)
        exponent = (normalized[..., None] - levels).abs().argmin(-1)
    else:
        exponent = (resolution * normalized.clamp_min(torch.finfo(weight.dtype).tiny).log2()).round().clamp(0, emax).long()
    zero = normalized < 2 ** (-1 / (2 * resolution))
    magnitude = torch.where(zero, 0, exponent + 1)
    signs = torch.where(zero, 0, weight.sign()).to(torch.int64)
    return FPoTCodes(signs, magnitude, scales, bits, resolution, approximate)


def quantize_weights(weight: torch.Tensor, *, bits: int = 4, resolution: int = 2,
                     approximate: bool = True, clip_ratios: Sequence[float] = (.7, .8, .9, 1.),
                     phase_steps: int = 16) -> FPoTCodes:
    """Per-channel MSE clip/phase search; the returned static codes are detached.

    Eq.4 searches s_base * 2**(g/G), after the Appendix-F clip search.
    Ties retain the first candidate deterministically. All-zero rows use scale=1.
    FP16/BF16 calibration is promoted to FP32 before scale arithmetic; codes keep
    FP32 scales and dequantization. The STE explicitly casts back to weight dtype.
    """
    emax = _configuration(bits, resolution, approximate)
    if weight.ndim != 2 or min(weight.shape) < 1 or not weight.is_floating_point():
        raise ValueError("nonempty floating [output,input] weights required")
    if not bool(torch.isfinite(weight).all()):
        raise ValueError("finite weights required")
    if isinstance(phase_steps, bool) or not isinstance(phase_steps, int) or not 1 <= phase_steps <= 128:
        raise ValueError("phase_steps must be in [1,128]")
    ratios = tuple(clip_ratios)
    if not ratios or any(not math.isfinite(r) or not 0 < r <= 1 for r in ratios):
        raise ValueError("clip ratios must be finite and in (0,1]")
    with torch.no_grad():
        raw = weight.detach()
        if raw.dtype in (torch.float16, torch.bfloat16):
            raw = raw.float()
        maximum = raw.abs().amax(1)
        best_error = torch.full_like(maximum, float("inf"))
        best_scale = torch.ones_like(maximum)
        for ratio in ratios:
            base = ratio * maximum / 2 ** (emax / resolution)
            base = torch.where(maximum == 0, torch.ones_like(base), base)
            for phase in range(phase_steps):
                scales = base * 2 ** (phase / phase_steps)
                candidate = _encode(raw, scales, bits, resolution, approximate)
                error = (dequantize(candidate) - raw).square().mean(1)
                better = error < best_error
                best_error = torch.where(better, error, best_error)
                best_scale = torch.where(better, scales, best_scale)
        return _encode(raw, best_scale, bits, resolution, approximate)


def validate_codes(codes: FPoTCodes) -> None:
    emax = _configuration(codes.bits, codes.resolution, codes.approximate)
    if codes.signs.ndim != 2 or codes.signs.shape != codes.magnitudes.shape or min(codes.signs.shape) < 1:
        raise ValueError("matching nonempty code matrices required")
    if codes.signs.dtype != torch.int64 or codes.magnitudes.dtype != torch.int64:
        raise ValueError("integer signs and magnitude codes required")
    if codes.scales.shape != (codes.signs.shape[0],) or not codes.scales.is_floating_point():
        raise ValueError("one floating scale per output channel required")
    if len({codes.signs.device, codes.magnitudes.device, codes.scales.device}) != 1:
        raise ValueError("codes and scales must share a device")
    if not bool(torch.isfinite(codes.scales).all()) or not bool((codes.scales > 0).all()):
        raise ValueError("finite positive scales required")
    if not bool(((codes.magnitudes >= 0) & (codes.magnitudes <= emax + 1)).all()):
        raise ValueError("magnitude code outside bit budget")
    if not bool(((codes.signs >= -1) & (codes.signs <= 1)).all()):
        raise ValueError("invalid sign")
    if not torch.equal(codes.signs == 0, codes.magnitudes == 0):
        raise ValueError("zero-gating sign/magnitude mismatch")


def dequantize(codes: FPoTCodes) -> torch.Tensor:
    validate_codes(codes)
    exponent = (codes.magnitudes - 1).clamp_min(0).to(codes.scales.dtype)
    return codes.signs * codes.scales[:, None] * _levels(exponent, codes.resolution, codes.approximate)


def straight_through_weights(weight: torch.Tensor, codes: FPoTCodes) -> torch.Tensor:
    """Forward uses fixed calibrated weights; backward is the identity STE."""
    reconstruction = dequantize(codes).detach()
    if not weight.is_floating_point() or weight.shape != reconstruction.shape or weight.device != reconstruction.device:
        raise ValueError("floating STE weights must match calibrated code shape/device")
    reconstruction = reconstruction.to(dtype=weight.dtype)
    return weight + (reconstruction - weight).detach()


def integer_accumulate(activations: torch.Tensor, codes: FPoTCodes) -> torch.Tensor:
    """Int64 reference PE, with signed arithmetic right shift and zero gating.

    Output is an unscaled integer accumulator. The caller applies activation and
    per-channel weight scales. Integer rounding is retained, not called 1.5*x
    exactly for odd signed integers. This simulation makes no speed/energy claim.
    """
    validate_codes(codes)
    if codes.resolution != 2 or not codes.approximate:
        raise ValueError("integer PE requires the half-octave approximate grid")
    if activations.ndim != 2 or activations.shape[1] != codes.signs.shape[1] or activations.shape[0] < 1:
        raise ValueError("[batch,input] activations required")
    if activations.dtype != torch.int64 or activations.device != codes.signs.device:
        raise ValueError("same-device int64 uniform activation codes required")
    # Subtract m's reserved zero code BEFORE extracting shift/parity bits.
    exponent = (codes.magnitudes - 1).clamp_min(0)
    max_shift = int(exponent.max()) // 2
    safe_bound = (2 ** 61 - 1) // max(1, 3 * codes.signs.shape[1] * 2 ** max_shift)
    if bool((activations > safe_bound).any()) or bool((activations < -safe_bound).any()):
        raise ValueError("activation magnitude risks int64 accumulator overflow")
    shifted = torch.bitwise_left_shift(activations[:, None, :], exponent[None] // 2)
    term = torch.where(exponent[None] % 2 == 0, shifted, shifted + torch.bitwise_right_shift(shifted, 1))
    return (term * codes.signs[None]).sum(-1)
