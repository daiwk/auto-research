"""Actual continuous diffusion LM: DoubleCat/SemiCat Eqs. 3.2/3.6/3.7.

The denoiser uses bidirectional attention and has no autoregressive token path.
One-hot signals, Gaussian noise and a simplex prior remain explicit. Sampling
uses the paper's recommended usual one-hot flow (discard Y_t at inference),
plus the exact conditional reveal hazard for SemiCat Algorithm 1.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


@dataclass(frozen=True)
class Corruption:
    state: Tensor
    revealed: Tensor
    time: Tensor
    noise: Tensor
    simplex_prior: Tensor


def corrupt(tokens: Tensor, vocabulary: int, time: Tensor, *, method: str,
            generator: torch.Generator | None = None) -> Corruption:
    if method not in ("onehot", "doublecat", "semicat") or tokens.ndim != 2:
        raise ValueError("B-by-L tokens and a supported diffusion method required")
    if time.shape != (len(tokens),) or (time < 0).any() or (time > 1).any():
        raise ValueError("one time in [0,1] per example required")
    clean = F.one_hot(tokens, vocabulary).float()
    noise = torch.randn(clean.shape, device=tokens.device, generator=generator)
    exponential = -torch.rand(clean.shape, device=tokens.device, generator=generator).clamp_min(1e-8).log()
    prior = exponential / exponential.sum(-1, keepdim=True)  # Dirichlet(1): uniform ON simplex
    gamma = time[:, None, None]
    kappa = torch.ones_like(gamma) if method == "onehot" else gamma.sqrt()
    state = (1 - gamma) * noise + gamma * ((1 - kappa) * prior + kappa * clean)
    tau = torch.rand(tokens.shape, device=tokens.device, generator=generator)
    revealed = time[:, None] >= tau if method == "semicat" else torch.zeros_like(tokens, dtype=torch.bool)
    state = torch.where(revealed[..., None], clean, state)
    return Corruption(state, revealed, time, noise, prior)


class DiTBlock(nn.Module):
    def __init__(self, width: int, heads: int):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(width, elementwise_affine=False), nn.LayerNorm(width, elementwise_affine=False)
        self.attention = nn.MultiheadAttention(width, heads, dropout=0., batch_first=True)
        self.mlp = nn.Sequential(nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width))
        self.modulation = nn.Linear(width, 6 * width)

    def forward(self, state: Tensor, conditioning: Tensor) -> Tensor:
        shift1, scale1, gate1, shift2, scale2, gate2 = self.modulation(conditioning)[:, None].chunk(6, -1)
        normalized = self.norm1(state) * (1 + scale1) + shift1
        # Bidirectional joint denoising, never an AR causal attention mask.
        update, _ = self.attention(normalized, normalized, normalized, need_weights=False)
        state = state + gate1.tanh() * update
        return state + gate2.tanh() * self.mlp(self.norm2(state) * (1 + scale2) + shift2)


class DiffusionLM(nn.Module):
    def __init__(self, vocabulary: int = 256, width: int = 64, layers: int = 2,
                 heads: int = 4, length: int = 64, *, self_conditioning: bool = True):
        super().__init__()
        if width % heads or width % 2 or length < 1:
            raise ValueError("even width divisible by heads and positive length required")
        self.vocabulary, self.self_conditioning = vocabulary, self_conditioning
        self.input = nn.Linear(vocabulary, width)
        self.self_condition = nn.Linear(vocabulary, width, bias=False) if self_conditioning else None
        self.positions = nn.Parameter(torch.randn(length, width) * .01)
        self.time = nn.Sequential(nn.Linear(width, width), nn.SiLU(), nn.Linear(width, width))
        self.blocks = nn.ModuleList(DiTBlock(width, heads) for _ in range(layers))
        self.norm, self.output = nn.LayerNorm(width), nn.Linear(width, vocabulary)

    def forward(self, state: Tensor, time: Tensor, self_condition: Tensor | None = None) -> Tensor:
        width = self.positions.shape[-1]
        frequency = torch.exp(-math.log(10000) * torch.arange(width // 2, device=state.device) / (width // 2))
        argument = time[:, None] * frequency[None] * 1000
        conditioning = self.time(torch.cat((argument.sin(), argument.cos()), -1))
        hidden = self.input(state) + self.positions[:state.shape[1]][None]
        if self.self_condition is not None:
            if self_condition is None:
                self_condition = torch.zeros_like(state)
            hidden = hidden + self.self_condition(self_condition.detach())
        elif self_condition is not None:
            raise ValueError("self-conditioning input supplied to a disabled model")
        for block in self.blocks:
            hidden = block(hidden, conditioning)
        return self.output(self.norm(hidden))


def denoising_loss(model: DiffusionLM, tokens: Tensor, corruption: Corruption,
                   *, use_self_condition: bool = False) -> Tensor:
    condition = None
    if use_self_condition:
        if not model.self_conditioning:
            raise ValueError("self-conditioning must be enabled in the denoiser")
        with torch.no_grad():
            condition = model(corruption.state, corruption.time).softmax(-1)
            condition = torch.where(corruption.revealed[..., None], corruption.state, condition)
    logits = model(corruption.state, corruption.time, condition)
    per_token = F.cross_entropy(logits.flatten(0, 1), tokens.flatten(), reduction="none").reshape_as(tokens)
    valid = ~corruption.revealed
    # Eq. 3.7: loss only on unrevealed tokens, preserving a differentiable zero
    # if a complete example has already been revealed.
    return (per_token * valid).sum() / valid.sum().clamp_min(1)


@torch.no_grad()
def sample(model: DiffusionLM, batch: int, length: int, *, method: str,
           steps: int = 32, temperature: float = 1.,
           generator: torch.Generator | None = None) -> tuple[Tensor, dict]:
    if method not in ("onehot", "doublecat", "semicat") or min(batch, length, steps) < 1 or temperature <= 0:
        raise ValueError("valid diffusion sampler settings required")
    device = next(model.parameters()).device
    state = torch.randn(batch, length, model.vocabulary, device=device, generator=generator)
    revealed = torch.zeros(batch, length, device=device, dtype=torch.bool)
    condition = None
    counts, changed_revealed = [], 0
    model.eval()
    for index in range(steps):
        t, next_t = index / steps, (index + 1) / steps
        logits = model(state, torch.full((batch,), t, device=device), condition)
        probability = logits.softmax(-1)
        probability = torch.where(revealed[..., None], state, probability)
        old = state.clone()
        # Algorithm 1 uses raw denoiser probability for Euler; temperature is
        # applied only to the categorical commit, not to the continuous step.
        updated = state + ((next_t - t) / (1 - t)) * (probability - state)
        state = torch.where(revealed[..., None], state, updated)
        if method == "semicat":
            hazard = (next_t - t) / (1 - t)
            commit = (~revealed) & (torch.rand(revealed.shape, device=device, generator=generator) < hazard)
            ids = torch.multinomial((logits / temperature).softmax(-1).flatten(0, 1), 1,
                                    generator=generator).reshape(batch, length)
            state = torch.where(commit[..., None], F.one_hot(ids, model.vocabulary).float(), state)
            changed_revealed += int((old[revealed] != state[revealed]).any())
            revealed |= commit
        if model.self_conditioning:
            condition = torch.where(revealed[..., None], state, probability)
        counts.append(int(revealed.sum()))
    if method == "semicat" and not revealed.all():
        raise RuntimeError("final reveal hazard must commit all positions")
    return state.argmax(-1), {"nfe": steps, "revealed_counts": counts,
                              "previously_revealed_changes": changed_revealed,
                              "sampler": "paper Algorithm 1" if method == "semicat" else "paper recommended one-hot sampler"}
