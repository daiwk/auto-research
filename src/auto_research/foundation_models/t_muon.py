"""Exact low-dimensional t-Muon (arXiv:2610.24938), not a fast polar kernel.

The transform acts on grouped matrix slices, not a tensor unfolding.  Original
matrix fan-out/fan-in scaling is applied *after* unpacking the tensor update.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor, nn


def transform_matrix(size: int, kind: str, *, device=None, dtype=torch.float64) -> Tensor:
    """Orthonormal identity/DCT-II/DST-II, or unitary complex DFT."""
    if size < 1 or dtype not in (torch.float32, torch.float64):
        raise ValueError("positive transform size and float32/float64 required")
    row = torch.arange(size, device=device, dtype=dtype)[:, None]
    col = torch.arange(size, device=device, dtype=dtype)[None, :]
    if kind == "identity":
        return torch.eye(size, device=device, dtype=dtype)
    if kind == "dct":
        result = math.sqrt(2 / size) * torch.cos(math.pi * row * (col + .5) / size)
        result[0] /= math.sqrt(2)
        return result
    if kind == "dst":
        result = math.sqrt(2 / size) * torch.sin(math.pi * (row + 1) * (col + .5) / size)
        result[-1] /= math.sqrt(2)
        return result
    if kind == "dft":
        return torch.exp(-2j * math.pi * row * col / size) / math.sqrt(size)
    raise ValueError("unknown M-transform")


def rank_polar(matrix: Tensor) -> Tensor:
    """Rank-reduced partial isometry; in particular polar(0) is zero."""
    if matrix.ndim < 2 or not torch.isfinite(matrix).all():
        raise ValueError("finite matrices required")
    u, singular, vh = torch.linalg.svd(matrix, full_matrices=False)
    tolerance = torch.finfo(singular.dtype).eps * max(matrix.shape[-2:]) * singular.amax(-1, keepdim=True)
    return (u * (singular > tolerance).to(u.dtype).unsqueeze(-2)) @ vh


def tensor_polar(tensor: Tensor, transform: Tensor) -> Tensor:
    """X[m,n,K] -> inverse-M(slice polar(M X)); Eq.2--6 and Algorithm 1."""
    if tensor.ndim != 3 or transform.shape != (tensor.shape[-1], tensor.shape[-1]):
        raise ValueError("third-order tensor and matching square transform required")
    if not tensor.is_floating_point() or not torch.isfinite(tensor).all():
        raise ValueError("finite real floating tensor required")
    if tensor.dtype not in (torch.float32, torch.float64) or transform.device != tensor.device:
        raise ValueError("float32/float64 and same-device transform required")
    identity = torch.eye(transform.shape[0], device=transform.device, dtype=transform.dtype)
    if not torch.allclose(transform @ transform.mH, identity, atol=1e-5, rtol=1e-5):
        raise ValueError("M must be orthogonal/unitary")
    mixed = torch.einsum("kl,mnl->kmn", transform, tensor.to(transform.dtype))
    polarized = rank_polar(mixed)
    restored = torch.einsum("lk,kmn->mnl", transform.mH, polarized)
    if restored.is_complex():
        limit = 100 * torch.finfo(tensor.dtype).eps * max(1., float(restored.abs().max()))
        if float(restored.imag.abs().max()) > limit:
            raise ValueError("transform does not preserve a real update")
        restored = restored.real
    return restored.to(tensor.dtype)


def pack_matrices(matrices: list[Tensor], mode: str, heads: int) -> Tensor:
    if not matrices or any(m.ndim != 2 or m.shape != matrices[0].shape for m in matrices):
        raise ValueError("nonempty equal-shaped matrices required")
    if mode == "stack":  # layer or QKV grouping; caller supplies the actual related matrices
        return torch.stack(matrices, -1)
    if mode not in ("head", "head-stack") or heads < 1 or matrices[0].shape[0] % heads:
        raise ValueError("valid head grouping and divisible row dimension required")
    if mode == "head" and len(matrices) != 1:
        raise ValueError("head mode groups one original matrix")
    return torch.stack([block for matrix in matrices for block in matrix.chunk(heads, 0)], -1)


def unpack_matrices(tensor: Tensor, count: int, mode: str, heads: int) -> list[Tensor]:
    if mode == "stack":
        return list(tensor.unbind(-1))
    return [torch.cat(list(tensor[..., index * heads:(index + 1) * heads].unbind(-1)), 0)
            for index in range(count)]


class TensorMuon(torch.optim.Optimizer):
    """One structurally related parameter group; exact SVD, Algorithm 1 momentum.

    Unrelated biases/embeddings must use a separate optimizer. No silent
    fallback for missing gradients or unequal shapes is performed.
    """
    def __init__(self, parameters: list[nn.Parameter], *, lr: float = .01, momentum: float = .95,
                 weight_decay: float = .01, mode: str = "stack", heads: int = 1,
                 transform: str = "identity"):
        if not parameters or lr <= 0 or not 0 <= momentum < 1 or weight_decay < 0 or lr * weight_decay >= 1:
            raise ValueError("invalid optimizer configuration")
        if any(p.dtype not in (torch.float32, torch.float64) or p.device != parameters[0].device
               or p.dtype != parameters[0].dtype for p in parameters):
            raise ValueError("homogeneous float32/float64 parameters required")
        example = pack_matrices(parameters, mode, heads)
        transform_matrix(example.shape[-1], transform, device=example.device, dtype=example.dtype)
        super().__init__(parameters, dict(lr=lr, momentum=momentum, weight_decay=weight_decay,
                                         mode=mode, heads=heads, transform=transform))

    @torch.no_grad()
    def step(self, closure=None):
        loss = None
        if closure is not None:
            with torch.enable_grad():
                loss = closure()
        for group in self.param_groups:
            parameters = group["params"]
            if any(p.grad is None or p.grad.is_sparse or not torch.isfinite(p.grad).all() for p in parameters):
                raise ValueError("all grouped parameters need finite dense gradients")
            directions = []
            for parameter in parameters:
                gradient = parameter.grad
                buffer = self.state[parameter].setdefault("momentum_buffer", torch.zeros_like(parameter))
                buffer.mul_(group["momentum"]).add_(gradient)
                directions.append(gradient + group["momentum"] * buffer)
            tensor = pack_matrices(directions, group["mode"], group["heads"])
            transform = transform_matrix(tensor.shape[-1], group["transform"], device=tensor.device, dtype=tensor.dtype)
            updates = unpack_matrices(tensor_polar(tensor, transform), len(parameters), group["mode"], group["heads"])
            for parameter, update in zip(parameters, updates, strict=True):
                scale = math.sqrt(parameter.shape[0] / parameter.shape[1])
                parameter.mul_(1 - group["lr"] * group["weight_decay"]).add_(update, alpha=-group["lr"] * scale)
        return loss
