"""WM-Quant v1 §3.4: rollout-range calibration with a floating control path."""

from __future__ import annotations

import torch
from torch import Tensor, nn
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/wm-quant-a100-20261118-latest.json"


def fake_quantize(x: Tensor, low: Tensor, log_width: Tensor, bits: int) -> Tensor:
    if not 2 <= bits <= 16:
        raise ValueError("bit width must be 2–16")
    width = F.softplus(log_width) + 1e-6
    scale = width / (2**bits - 1)
    coordinate = ((x - low) / scale).clamp(0, 2**bits - 1)
    rounded = coordinate + (coordinate.round() - coordinate).detach()
    return low + rounded * scale


class RolloutCalibrator(nn.Module):
    """Four tiny encoder blocks + shared predictor; no LeWM/DINO-WM replacement.

    Real implementations can reuse the range bank/objective; this reference
    retains action contributions outside state fake quantization.
    """

    def __init__(self, width: int, horizon: int, bits: int = 3):
        super().__init__()
        if width < 1 or horizon < 1 or not 2 <= bits <= 8:
            raise ValueError("positive dimensions and 2–8 target bits required")
        self.bits, self.horizon = bits, horizon
        self.encoder = nn.ModuleList([nn.Linear(width, width, bias=False) for _ in range(4)])
        self.predictor = nn.Linear(width, width, bias=False)
        self.control = nn.Linear(1, width, bias=False)
        for block in self.encoder:
            nn.init.eye_(block.weight)
        with torch.no_grad():
            self.predictor.weight.copy_(1.05 * torch.eye(width))
        for parameter in self.parameters():
            parameter.requires_grad_(False)
        self.low = nn.Parameter(torch.full((4 + horizon,), -0.3))
        self.log_width = nn.Parameter(torch.full((4 + horizon,), 0.0))

    def forward(self, observations: Tensor, actions: Tensor, *, quantized: bool = True) -> Tensor:
        if (
            observations.ndim != 2
            or actions.shape != (observations.shape[0], self.horizon, 1)
            or not bool(torch.isfinite(observations).all() and torch.isfinite(actions).all())
        ):
            raise ValueError("finite [B,D] observations and [B,horizon,1] actions required")
        z = observations
        for index, block in enumerate(self.encoder):
            z = block(z)
            if quantized:
                z = fake_quantize(
                    z, self.low[index], self.log_width[index], 8 if index < 3 else self.bits
                )
        outputs = []
        for step in range(self.horizon):
            source = (
                fake_quantize(z, self.low[4 + step], self.log_width[4 + step], self.bits)
                if quantized
                else z
            )
            z = self.predictor(source) + self.control(actions[:, step])
            outputs.append(z)
        return torch.stack(outputs, 1)

    def objective(self, observations: Tensor, actions: Tensor) -> Tensor:
        full = self(observations, actions, quantized=False).detach()
        delta = self(observations, actions) - full
        weights = torch.arange(1, self.horizon + 1, device=delta.device, dtype=delta.dtype)
        weights = weights / weights.sum()
        return (delta.square().sum(-1) * weights).sum(-1).mean()


def diagnostic(seed: int, device: str = "cpu") -> dict:
    torch.manual_seed(seed)
    model = RolloutCalibrator(6, 4).to(device)
    observations = torch.randn(8, 6, device=device)
    actions = torch.randn(8, 4, 1, device=device) * 0.01
    before = float(model.objective(observations, actions).detach())
    optimizer = torch.optim.Adam([model.low, model.log_width], lr=0.06)
    for _ in range(30):
        optimizer.zero_grad()
        loss = model.objective(observations, actions)
        loss.backward()
        optimizer.step()
    after = float(model.objective(observations, actions).detach())
    base = model(observations, torch.zeros_like(actions))[:, 0]
    changed = actions * 0
    changed[:, 0] = 1e-4
    control_effect = model(observations, changed)[:, 0] - base
    expected = model.control(changed[:, 0])
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "metrics": {"rollout_calibration_before": before, "rollout_calibration_after": after},
        "checks": {
            "joint_ranges_optimized": after < before,
            "control_path_preserved": bool(torch.allclose(control_effect, expected, atol=1e-6)),
            "step_ranges_not_shared": bool(model.low[4:].std() > 0),
            "model_weights_frozen": all(not p.requires_grad for p in model.encoder.parameters()),
        },
    }
