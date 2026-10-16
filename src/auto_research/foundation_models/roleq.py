"""RoleQ Eqs. 1-2 exact vector fit/role axis and actual ternary byte accounting.

No rotations, GPTQ sweep, scale-distillation, Fisher planes or LM conversion.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor


def exact_ternary_fit(vectors: Tensor) -> tuple[Tensor, Tensor]:
    """Globally optimal unweighted scale+ternary codes for each last-axis vector."""
    if vectors.ndim < 1 or not vectors.is_floating_point() or vectors.shape[-1] < 1 or not bool(torch.isfinite(vectors).all()):
        raise ValueError("finite nonempty floating vectors required")
    dtype = torch.float64 if vectors.dtype == torch.float64 else torch.float32
    w = vectors.to(dtype)
    magnitudes, permutation = w.abs().sort(dim=-1, descending=True, stable=True)
    counts = torch.arange(1, w.shape[-1] + 1, device=w.device, dtype=dtype)
    sums = magnitudes.cumsum(-1)
    objective_gain = sums.square() / counts
    best = objective_gain.argmax(-1, keepdim=True)
    k = best + 1
    scale = sums.gather(-1, best).squeeze(-1) / k.squeeze(-1)
    sorted_support = torch.arange(w.shape[-1], device=w.device) < k
    support = torch.zeros_like(sorted_support).scatter(-1, permutation, sorted_support)
    codes = (w.sign() * support).to(torch.int8)
    return codes, scale


def _pack_trits(codes: Tensor) -> Tensor:
    flat = codes.reshape(-1).to(torch.int64) + 1
    padding = (-flat.numel()) % 5
    if padding:
        flat = torch.cat((flat, torch.ones(padding, dtype=torch.int64, device=codes.device)))
    powers = torch.tensor([1, 3, 9, 27, 81], device=codes.device)
    return (flat.reshape(-1, 5) * powers).sum(-1).to(torch.uint8)


@dataclass(frozen=True)
class RoleQuantized:
    packed_trits: Tensor
    scales: Tensor
    shape: tuple[int, int]
    role: str

    def codes(self) -> Tensor:
        powers = torch.tensor([1, 3, 9, 27, 81], device=self.packed_trits.device)
        codes = (self.packed_trits.to(torch.int64).unsqueeze(-1) // powers) % 3 - 1
        return codes.reshape(-1)[:math.prod(self.shape)].reshape(self.shape).to(torch.int8)

    def reconstruct(self) -> Tensor:
        scale = self.scales[:, None] if self.role == "reader" else self.scales[None, :]
        return self.codes().to(self.scales.dtype) * scale

    def bit_accounting(self) -> dict[str, float | int]:
        count = math.prod(self.shape)
        scale_bits = self.scales.numel() * self.scales.element_size() * 8
        payload_bits = self.packed_trits.numel() * 8
        return {"weights": count, "packed_code_bits": payload_bits, "scale_bits": scale_bits,
                "payload_and_scale_storage_bits": payload_bits + scale_bits,
                "payload_and_scale_bpw": (payload_bits + scale_bits) / count,
                "information_lower_bound_bpw": math.log2(3) + scale_bits / count,
                "packing_padding_trits": self.packed_trits.numel() * 5 - count,
                "python_shape_role_header_bytes_excluded": True}


def quantize_by_role(weight: Tensor, role: str) -> RoleQuantized:
    if weight.ndim != 2 or role not in ("reader", "writer"):
        raise ValueError("[out,in] matrix and explicit reader/writer role required")
    vectors = weight if role == "reader" else weight.t()
    codes, scales = exact_ternary_fit(vectors)
    if role == "writer":
        codes = codes.t()
    return RoleQuantized(_pack_trits(codes), scales, tuple(weight.shape), role)
