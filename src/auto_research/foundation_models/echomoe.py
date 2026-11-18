"""EchoMoE v1 Eqs2–7: folded compressed experts; no distributed speed claim."""

from __future__ import annotations

import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/echomoe-a100-20261118-latest.json"


def expert_combine(
    x: Tensor,
    reference: Tensor,
    routing: Tensor,
    *,
    gain: Tensor,
    dispatch_encoder: Tensor,
    dispatch_decoder: Tensor,
    reference_map: Tensor,
    gate: Tensor,
    up: Tensor,
    down: Tensor,
    combine_encoder: Tensor,
    combine_decoder: Tensor,
    folded: bool = True,
) -> Tensor:
    """routing must be produced from full x, not compressed reconstruction.

    D_d/G may be expert-specific after folding; C_d/a and D_c remain shared.
    Reference layers bypass dispatch compression and are outside this nonreference operator.
    """
    if x.ndim != 2 or reference.shape != x.shape or routing.shape != (x.shape[0], gate.shape[0]):
        raise ValueError("[tokens,width] states and [tokens,experts] routing required")
    tensors = (
        x,
        reference,
        routing,
        gain,
        dispatch_encoder,
        dispatch_decoder,
        reference_map,
        gate,
        up,
        down,
        combine_encoder,
        combine_decoder,
    )
    if any(t.device != x.device or not bool(torch.isfinite(t).all()) for t in tensors):
        raise ValueError("finite colocated tensors required")
    code = F.linear(x - gain * reference, dispatch_encoder)
    codes = []
    for expert in range(gate.shape[0]):
        if folded:
            inputs = torch.cat([reference, code], -1)
            reconstruction = torch.cat([reference_map[expert], dispatch_decoder[expert]], -1)
            gate_up = torch.cat([gate[expert], up[expert]], 0) @ reconstruction
            g, u = F.linear(inputs, gate_up).chunk(2, -1)
            output = F.linear(F.silu(g) * u, combine_encoder @ down[expert])
        else:
            reconstructed = F.linear(reference, reference_map[expert]) + F.linear(
                code, dispatch_decoder[expert]
            )
            hidden = F.silu(F.linear(reconstructed, gate[expert])) * F.linear(
                reconstructed, up[expert]
            )
            output = F.linear(F.linear(hidden, down[expert]), combine_encoder)
        codes.append(routing[:, expert, None] * output)
    return F.linear(torch.stack(codes).sum(0), combine_decoder)


def traffic_bytes(
    tokens: int,
    layers: int,
    stride: int,
    width: int,
    dispatch_rank: int,
    combine_rank: int,
    remote_nodes: int,
    selected_nodes: float,
    bytes_per_scalar: int = 2,
) -> float:
    if (
        min(tokens, layers, stride, width, dispatch_rank, combine_rank, bytes_per_scalar) < 1
        or not 0 <= selected_nodes <= remote_nodes
    ):
        raise ValueError("positive dimensions and valid remote-node count required")
    if layers % stride:
        raise ValueError("paper Eq8 assumes complete reference groups")
    return (
        bytes_per_scalar
        * tokens
        * layers
        * (
            width * remote_nodes / stride
            + dispatch_rank * (stride - 1) * selected_nodes / stride
            + combine_rank * selected_nodes
        )
    )


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)

    def random(*shape):
        return torch.randn(*shape, dtype=torch.float64, device=device) * 0.2

    x = random(5, 8).requires_grad_()
    z = random(5, 8)
    kw = {
        "gain": random(8),
        "dispatch_encoder": random(3, 8),
        "dispatch_decoder": random(2, 8, 3),
        "reference_map": random(2, 8, 8),
        "gate": random(2, 6, 8),
        "up": random(2, 6, 8),
        "down": random(2, 8, 6),
        "combine_encoder": random(4, 8),
        "combine_decoder": random(8, 4),
    }
    routing = random(5, 2).softmax(-1)
    folded = expert_combine(x, z, routing, **kw)
    literal = expert_combine(x, z, routing, **kw, folded=False)
    grad1 = torch.autograd.grad(folded.sum(), x, retain_graph=True)[0]
    grad2 = torch.autograd.grad(literal.sum(), x)[0]
    error = float((folded - literal).abs().max().detach())
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {
            "folded_max_error": error,
            "analytic_traffic_bytes": traffic_bytes(5, 12, 4, 8, 3, 4, 3, 2),
        },
        "checks": {
            "folded_output_parity": error < 1e-12,
            "folded_gradient_parity": bool(torch.allclose(grad1, grad2, atol=1e-12)),
            "reference_matters": bool(
                not torch.allclose(folded, expert_combine(x, torch.zeros_like(z), routing, **kw))
            ),
        },
    }
