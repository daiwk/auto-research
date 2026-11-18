"""GaugeRoPE v1 §4: compatible carriers plus explicitly approximate RKV correction."""

from __future__ import annotations

from dataclasses import dataclass
import math
import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/gaugerope-a100-20261118-latest.json"


def complex_pairs(x: Tensor) -> Tensor:
    if x.shape[-1] % 2:
        raise ValueError("even rotary width required")
    return torch.view_as_complex(x.reshape(*x.shape[:-1], -1, 2).contiguous())


def real_pairs(x: Tensor) -> Tensor:
    return torch.view_as_real(x).flatten(-2)


@dataclass
class LatentCache:
    basis: Tensor
    rkv_encoder: Tensor
    key_decoder: Tensor
    value_decoder: Tensor
    balance: Tensor

    @classmethod
    def calibrate(
        cls, keys: Tensor, values: Tensor, carrier_rank: int, code_rank: int
    ) -> "LatentCache":
        if keys.ndim != 3 or values.shape != keys.shape or min(keys.shape) < 1:
            raise ValueError("[calibration tokens,KV heads,even width] tensors required")
        n, heads, width = keys.shape
        if not 1 <= carrier_rank <= heads or not 1 <= code_rank <= min(n, 2 * heads * width):
            raise ValueError("carrier/code ranks outside calibration support")
        k = complex_pairs(keys)
        gram = torch.einsum("nhf,njf->fhj", k, k.conj())
        _, eigenvectors = torch.linalg.eigh(gram)
        basis = eigenvectors[..., -carrier_rank:]
        z = torch.einsum("nhf,fhr->nfr", k, basis.conj())
        reconstructed = torch.einsum("nfr,fhr->nhf", z, basis)
        residual = real_pairs(k - reconstructed).flatten(1)
        native_values = values.flatten(1)
        balance = (native_values.square().mean() / residual.square().mean().clamp_min(1e-20)).sqrt()
        joint = torch.cat([residual * balance, native_values], -1)
        # Uncentered PCA stores no per-token intercept, matching a linear RKV map.
        _, _, vh = torch.linalg.svd(joint, full_matrices=False)
        encoder = vh[:code_rank].T
        key_decoder = encoder[: heads * width] / balance
        value_decoder = encoder[heads * width :]
        return cls(basis, encoder, key_decoder, value_decoder, balance)

    def encode(self, keys: Tensor, values: Tensor) -> tuple[Tensor, Tensor]:
        k = complex_pairs(keys)
        z = torch.einsum("nhf,fhr->nfr", k, self.basis.conj())
        reconstructed = torch.einsum("nfr,fhr->nhf", z, self.basis)
        residual = real_pairs(k - reconstructed).flatten(1)
        code = torch.cat([residual * self.balance, values.flatten(1)], -1) @ self.rkv_encoder
        return z, code

    def attention(
        self,
        query: Tensor,
        z: Tensor,
        code: Tensor,
        frequencies: Tensor,
        positions: Tensor,
        query_position: int,
    ) -> Tensor:
        """One GQA decoding position. History is scored without reconstructing each K/V."""
        heads, width = query.shape
        kv_heads = self.basis.shape[1]
        if heads % kv_heads or z.shape[0] != code.shape[0] or positions.shape != z.shape[:1]:
            raise ValueError("valid GQA groups and cache positions required")
        if bool((positions > query_position).any()):
            raise ValueError("cache may contain only causally available positions")
        group = torch.arange(heads, device=query.device) // (heads // kv_heads)
        q = complex_pairs(query)
        absorbed = self.basis[:, group].permute(1, 0, 2).conj() * q[..., None]
        rotation = torch.exp(1j * (positions - query_position)[:, None] * frequencies)
        carrier = torch.einsum("gfr,nf,nfr->gn", absorbed.conj(), rotation, z).real
        kd = self.key_decoder.reshape(kv_heads, width, -1)[group]
        residual_query = torch.einsum("gd,gdr->gr", query, kd)
        scores = (carrier + residual_query @ code.T) / math.sqrt(width)
        weights = scores.softmax(-1)
        latent_output = weights @ code
        vd = self.value_decoder.reshape(kv_heads, width, -1)[group]
        return torch.einsum("gr,gdr->gd", latent_output, vd)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    keys = torch.randn(32, 2, 4, device=device, dtype=torch.float64)
    values = torch.randn_like(keys)
    cache = LatentCache.calibrate(keys, values, 2, 16)
    z, code = cache.encode(keys, values)
    query = torch.randn(4, 4, device=device, dtype=keys.dtype, requires_grad=True)
    positions = torch.arange(32, device=device)
    frequencies = torch.tensor([0.5, 0.1], device=device, dtype=keys.dtype)
    result = cache.attention(query, z, code, frequencies, positions, 32)
    rotated = complex_pairs(keys) * torch.exp(1j * (positions - 32)[:, None, None] * frequencies)
    native = real_pairs(rotated).repeat_interleave(2, 1)
    score = torch.einsum("gd,ngd->gn", query, native) / 2
    expected = torch.einsum("gn,ngd->gd", score.softmax(-1), values.repeat_interleave(2, 1))
    error = float((result - expected).abs().max().detach())
    result.sum().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"full_rank_native_attention_error": error},
        "checks": {
            "full_rank_carrier_exact": error < 1e-9,
            "latent_query_gradient": bool(
                query.grad is not None and torch.isfinite(query.grad).all()
            ),
            "frequency_basis_shape_preserved": cache.basis.shape == (2, 2, 2),
        },
    }
