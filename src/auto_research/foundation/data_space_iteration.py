"""Data-space self-rollout and alternating distribution matching (2610.12102).

The frozen teacher is a *trained* linear-path velocity model.  The fake model
tracks each generator prefix.  Refinement index is not a flow-time schedule;
every generator invocation uses the same source noise and fixed flow time one.
"""
from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass

import torch
from torch import nn
from torch.nn import functional as F


class ResidualBlock(nn.Module):
    def __init__(self, width):
        super().__init__()
        self.norm1 = nn.GroupNorm(4, width)
        self.conv1 = nn.Conv2d(width, width, 3, padding=1)
        self.norm2 = nn.GroupNorm(4, width)
        self.conv2 = nn.Conv2d(width, width, 3, padding=1)

    def forward(self, x, condition):
        y = self.conv1(F.silu(self.norm1(x)))
        y = y + condition[:, :, None, None]
        return x + self.conv2(F.silu(self.norm2(y)))


class SmallFlowNetwork(nn.Module):
    """Bounded two-scale residual U-Net, not the author's 55M SongUNet.

    The input/time/step pathways are explicit so a trained teacher's parameters
    transfer exactly into generator and fake networks before distillation.
    """
    def __init__(self, width=32, depth=3, refinements=4):
        super().__init__()
        if width < 4 or width % 4 or depth < 1 or refinements < 1:
            raise ValueError("width divisible by four and positive depth/refinements required")
        self.input = nn.Conv2d(3, width, 3, padding=1)
        self.time = nn.Sequential(nn.Linear(1, width), nn.SiLU(), nn.Linear(width, width))
        self.blocks = nn.ModuleList(ResidualBlock(width) for _ in range(depth))
        self.down = nn.Conv2d(width, width, 3, stride=2, padding=1)
        self.middle = ResidualBlock(width)
        self.up = nn.Conv2d(width, width, 3, padding=1)
        self.output = nn.Conv2d(width, 3, 3, padding=1)
        self.refinements, self.width = refinements, width

    def features(self, x, time, extra=None):
        h = self.input(x) if extra is None else self.input(x) + extra
        condition = self.time(time.reshape(-1, 1).to(x.dtype))
        for block in self.blocks:
            h = block(h, condition)
        skip = h
        h = self.middle(self.down(h), condition)
        h = self.up(F.interpolate(h, size=skip.shape[-2:], mode="nearest")) + skip
        return self.output(F.silu(h))

    def forward(self, x, time):
        return self.features(x, time)


class DataSpaceGenerator(nn.Module):
    def __init__(self, teacher: SmallFlowNetwork):
        super().__init__()
        # A real pretrained teacher is frozen before distillation. Deepcopy
        # preserves requires_grad flags, so explicitly unfreeze the student.
        self.backbone = deepcopy(teacher).requires_grad_(True)
        self.estimate = nn.Conv2d(3, teacher.width, 3, padding=1, bias=False)
        self.step = nn.Embedding(teacher.refinements, teacher.width)
        nn.init.xavier_uniform_(self.estimate.weight)
        nn.init.normal_(self.step.weight, std=.02)

    def forward(self, estimate, noise, refinement):
        if estimate.shape != noise.shape:
            raise ValueError("estimate/source-noise shapes must agree")
        index = torch.full((len(noise),), refinement, device=noise.device, dtype=torch.long)
        extra = self.estimate(estimate) + self.step(index)[:, :, None, None]
        # Eq.12: G = z - g(current estimate, z, r, t=1).
        return noise - self.backbone.features(noise, torch.ones(len(noise), device=noise.device), extra)


class FakeFlowNetwork(nn.Module):
    def __init__(self, teacher: SmallFlowNetwork):
        super().__init__()
        self.backbone = deepcopy(teacher).requires_grad_(True)
        self.step = nn.Embedding(teacher.refinements, teacher.width)
        nn.init.normal_(self.step.weight, std=.02)

    def forward(self, noisy, time, refinement):
        index = torch.full((len(noisy),), refinement, device=noisy.device, dtype=torch.long)
        extra = self.step(index)[:, :, None, None]
        return self.backbone.features(noisy, time, extra)


class FlowRenoiseGenerator(nn.Module):
    """Matched baseline: same teacher backbone, uniform trailing schedule."""
    def __init__(self, teacher: SmallFlowNetwork):
        super().__init__()
        self.backbone = deepcopy(teacher).requires_grad_(True)

    def forward(self, noisy, time):
        t = time[:, None, None, None]
        return noisy - t * self.backbone(noisy, time)


def rollout_data_space(generator, noise, refinement, *, track_grad=False):
    if refinement < 0:
        raise ValueError("refinement index must be nonnegative")
    estimate = torch.zeros_like(noise)
    for step in range(refinement + 1):
        with torch.set_grad_enabled(track_grad and step == refinement):
            estimate = generator(estimate, noise, step)
    return estimate


def rollout_flow_renoise(generator, noise, refinement, *, track_grad=False, refinements=4):
    if not 0 <= refinement < refinements:
        raise ValueError("refinement outside the trained schedule")
    estimate = torch.zeros_like(noise)
    for step in range(refinement + 1):
        time = torch.full((len(noise),), 1 - step / refinements, device=noise.device)
        t = time[:, None, None, None]
        epsilon = noise if step == 0 else torch.randn_like(noise)
        noisy = (1 - t) * estimate + t * epsilon
        with torch.set_grad_enabled(track_grad and step == refinement):
            estimate = generator(noisy, time)
    return estimate


def flow_matching_loss(teacher, images, *, noise=None, time=None):
    noise = torch.randn_like(images) if noise is None else noise
    time = torch.rand(len(images), device=images.device) if time is None else time
    t = time[:, None, None, None]
    return F.mse_loss(teacher((1 - t) * images + t * noise, time), noise - images)


def distribution_matching_loss(generator, teacher, fake, shape_source, refinement,
                               *, generator_update, rollout=rollout_data_space,
                               noise=None, epsilon=None, time=None):
    """Eq.10/11; teacher/fake gradients must never reach generator updates."""
    noise = torch.randn_like(shape_source) if noise is None else noise
    epsilon = torch.randn_like(shape_source) if epsilon is None else epsilon
    if time is None:
        time = torch.distributions.Beta(2.5, 1.).sample((len(noise),)).to(noise.device)
    if time.shape != (len(noise),) or not bool(((time > 0) & (time < 1)).all()):
        raise ValueError("DMD times must lie strictly inside (0,1)")
    generated = rollout(generator, noise, refinement, track_grad=generator_update)
    t = time[:, None, None, None]
    noisy = (1 - t) * generated + t * epsilon
    if not generator_update:
        # generated is detached by the no-grad rollout, not only the target.
        return F.mse_loss(fake(noisy, time, refinement), epsilon - generated)
    with torch.no_grad():
        direction = teacher(noisy, time) - fake(noisy, time, refinement)
    return (generated * direction).mean()


@dataclass
class DMDTrainer:
    generator: nn.Module
    teacher: nn.Module
    fake: nn.Module
    generator_optimizer: object
    fake_optimizer: object
    refinements: int = 4
    fake_updates: int = 4
    ema_decay: float = .9999
    rollout: object = rollout_data_space

    def __post_init__(self):
        if self.refinements < 1 or self.fake_updates < 1 or not 0 <= self.ema_decay < 1:
            raise ValueError("invalid alternating update/EMA budget")
        self.teacher.eval().requires_grad_(False)
        self.ema = deepcopy(self.generator).eval().requires_grad_(False)
        self.iteration = 0

    def step(self, shape_source):
        # Appendix A cycles r=i mod R; no fixed flow times in data-space rollout.
        refinement = self.iteration % self.refinements
        fake_losses, fake_gradient_norms = [], []
        for _ in range(self.fake_updates):
            self.fake_optimizer.zero_grad(set_to_none=True)
            loss = distribution_matching_loss(self.generator, self.teacher, self.fake,
                shape_source, refinement, generator_update=False, rollout=self.rollout)
            if not torch.isfinite(loss):
                raise FloatingPointError("nonfinite fake velocity loss; do not mask divergence")
            loss.backward()
            norm = sum(float(p.grad.detach().double().square().sum())
                       for p in self.fake.parameters() if p.grad is not None) ** .5
            if not torch.isfinite(torch.tensor(norm)):
                raise FloatingPointError("nonfinite fake velocity gradient; update refused")
            self.fake_optimizer.step()
            fake_losses.append(float(loss.detach()))
            fake_gradient_norms.append(norm)
        self.fake_optimizer.zero_grad(set_to_none=True)
        self.generator_optimizer.zero_grad(set_to_none=True)
        loss = distribution_matching_loss(self.generator, self.teacher, self.fake,
            shape_source, refinement, generator_update=True, rollout=self.rollout)
        if not torch.isfinite(loss):
            raise FloatingPointError("nonfinite DMD generator loss; do not mask divergence")
        loss.backward()
        norm = sum(float(p.grad.detach().double().square().sum())
                   for p in self.generator.parameters() if p.grad is not None) ** .5
        if not torch.isfinite(torch.tensor(norm)):
            raise FloatingPointError("nonfinite DMD generator gradient; update refused")
        self.generator_optimizer.step()
        with torch.no_grad():
            for target, source in zip(self.ema.parameters(), self.generator.parameters(), strict=True):
                target.lerp_(source, 1 - self.ema_decay)
        self.iteration += 1
        return {"refinement": refinement, "fake_losses": fake_losses,
                "fake_gradient_norms": fake_gradient_norms,
                "generator_loss": float(loss.detach()), "generator_gradient_norm": norm}


@torch.no_grad()
def teacher_sample(teacher, noise, evaluations=32):
    if evaluations < 1:
        raise ValueError("positive ODE evaluation count required")
    sample = noise.clone()
    for step in range(evaluations):
        time = torch.full((len(noise),), 1 - step / evaluations, device=noise.device)
        sample = sample - teacher(sample, time) / evaluations
    return sample
