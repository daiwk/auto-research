"""InfuseLoop v1 §3: causal cross-trajectory aggregation on old-cycle states."""

from __future__ import annotations

import math
import torch
from torch import Tensor, nn

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/infuseloop-a100-20261118-latest.json"


class CrossTrajectoryInjection(nn.Module):
    def __init__(self, loops: int, width: int):
        super().__init__()
        if loops < 2 or width < 1:
            raise ValueError("at least two loops and positive width required")
        self.loops, self.width = loops, width
        self.query = nn.Parameter(torch.randn(loops, width) / math.sqrt(width))
        self.bias = nn.Parameter(torch.zeros(loops, loops))
        self.scale = nn.Parameter(torch.ones(loops))

    def forward(self, states: Tensor, documents: Tensor) -> Tensor:
        """states[j-1,s] is h_s^j; every new loop reads the SAME immutable old bank."""
        if (
            states.ndim != 3
            or states.shape[0] != self.loops
            or states.shape[-1] != self.width
            or documents.shape != states.shape[1:2]
            or documents.device != states.device
            or not bool(torch.isfinite(states).all())
        ):
            raise ValueError("finite [loops,trajectory,width] and document ids required")
        outputs = [states[0]]
        n = states.shape[1]
        for r in range(2, self.loops + 1):
            source_rows, masks = [], []
            for j in range(1, r):
                # Previous execution cycle: s+j=t+r-1; no unpublished cycle state.
                index = torch.arange(n, device=states.device) + r - j - 1
                bounded = index.clamp(max=n - 1)
                source_rows.append(states[j - 1, bounded])
                masks.append((index < n) & (documents[bounded] == documents))
            sources = torch.stack(source_rows, 1)
            valid = torch.stack(masks, 1)
            normalized = sources * torch.rsqrt(sources.square().mean(-1, keepdim=True) + 1e-6)
            score = (normalized * self.query[r - 1]).sum(-1) / math.sqrt(self.width)
            score = score + self.bias[r - 1, : r - 1]
            # Empty rows must produce zero, not softmax(-inf,...,-inf)=NaN.
            score = score.masked_fill(~valid, -torch.inf)
            safe = torch.where(valid.any(-1, keepdim=True), score, torch.zeros_like(score))
            weights = safe.softmax(-1) * valid
            outputs.append(self.scale[r - 1] * (weights[..., None] * normalized).sum(1))
        return torch.stack(outputs)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    operator = CrossTrajectoryInjection(4, 8).to(device)
    states = torch.randn(4, 7, 8, device=device, requires_grad=True)
    docs = torch.tensor([0, 0, 0, 1, 1, 1, 1], device=device)
    output = operator(states, docs)
    altered = states.detach().clone()
    altered[:, 3:] += 50
    second = operator(altered, docs)
    output.square().sum().backward()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"output_norm": float(output.norm().detach())},
        "checks": {
            "first_loop_unchanged": bool(torch.equal(output[0], states[0])),
            "document_boundary_masked": bool(torch.allclose(output[1:, :3], second[1:, :3])),
            "last_trajectory_has_own_source": bool(torch.isfinite(output[:, -1]).all()),
            "learned_query_receives_gradient": bool(
                operator.query.grad is not None and operator.query.grad.abs().sum() > 0
            ),
        },
    }
