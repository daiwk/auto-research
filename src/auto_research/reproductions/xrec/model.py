"""Anchor-conditioned Riemannian flow matching on item embeddings.

The interpolation, target velocity, tangent projection and integration follow
X-Rec equations (20), (21), (31) and (24), respectively.
"""

from __future__ import annotations

import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def sphere_normalize(x: Tensor) -> Tensor:
    return F.normalize(x, p=2, dim=-1, eps=1e-8)


def geodesic_interpolate(noise: Tensor, target: Tensor, time: Tensor) -> tuple[Tensor, Tensor]:
    """Return the great-circle point and its exact time derivative."""
    noise, target = sphere_normalize(noise), sphere_normalize(target)
    dot = (noise * target).sum(dim=-1, keepdim=True).clamp(-1 + 1e-6, 1 - 1e-6)
    omega = torch.acos(dot)
    sine = torch.sin(omega).clamp_min(1e-6)
    time = time.reshape(-1, 1)
    point = (torch.sin((1 - time) * omega) * noise + torch.sin(time * omega) * target) / sine
    velocity = omega * (torch.cos(time * omega) * target - torch.cos((1 - time) * omega) * noise) / sine
    return sphere_normalize(point), velocity


def tangent_projection(point: Tensor, velocity: Tensor) -> Tensor:
    return velocity - (velocity * point).sum(dim=-1, keepdim=True) * point


def riemannian_euler(point: Tensor, velocity: Tensor, step: float) -> Tensor:
    """Exponential-map Euler update, stable also for a zero velocity."""
    norm = velocity.norm(dim=-1, keepdim=True)
    angle = norm * step
    scale = torch.where(norm > 1e-8, torch.sin(angle) / norm.clamp_min(1e-8), torch.full_like(norm, step))
    return sphere_normalize(torch.cos(angle) * point + scale * velocity)


class LateInteractionLayer(nn.Module):
    """One final attention layer whose history K/V are computed once per request."""

    def __init__(self, width: int, heads: int) -> None:
        super().__init__()
        if width % heads:
            raise ValueError("width must be divisible by heads")
        self.width, self.heads = width, heads
        self.q = nn.Linear(width, width)
        self.k = nn.Linear(width, width)
        self.v = nn.Linear(width, width)
        self.out = nn.Linear(width, width)
        self.norm = nn.LayerNorm(width)
        self.ff = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, 4 * width), nn.GELU(), nn.Linear(4 * width, width))

    def cache(self, history: Tensor) -> tuple[Tensor, Tensor]:
        shape = (history.shape[0], history.shape[1], self.heads, self.width // self.heads)
        return self.k(history).reshape(shape).transpose(1, 2), self.v(history).reshape(shape).transpose(1, 2)

    def encode_history(self, history: Tensor, valid: Tensor) -> Tensor:
        """Causal last-layer history pass for the anchor classifier."""
        batch, length, _ = history.shape
        k, v = self.cache(history)
        q = self.q(history).reshape(batch, length, self.heads, self.width // self.heads).transpose(1, 2)
        scores = (q @ k.transpose(-1, -2)) / math.sqrt(self.width // self.heads)
        causal = torch.tril(torch.ones(length, length, dtype=torch.bool, device=history.device))
        mask = causal[None, None] & valid[:, None, None, :]
        scores = scores.masked_fill(~mask, torch.finfo(scores.dtype).min)
        mixed = (torch.softmax(scores, dim=-1) @ v).transpose(1, 2).reshape(batch, length, self.width)
        output = self.norm(history + self.out(mixed))
        return output + self.ff(output)

    def forward(self, token: Tensor, cached: tuple[Tensor, Tensor], valid: Tensor) -> Tensor:
        k_hist, v_hist = cached
        batch, _, heads, head_width = batch_shape = (token.shape[0], 1, self.heads, self.width // self.heads)
        q = self.q(token).reshape(batch_shape).transpose(1, 2)
        k = torch.cat((k_hist, self.k(token).reshape(batch_shape).transpose(1, 2)), dim=2)
        v = torch.cat((v_hist, self.v(token).reshape(batch_shape).transpose(1, 2)), dim=2)
        scores = (q @ k.transpose(-1, -2)) / math.sqrt(head_width)
        mask = torch.cat((valid, torch.ones(batch, 1, dtype=torch.bool, device=valid.device)), dim=1)
        scores = scores.masked_fill(~mask[:, None, None, :], torch.finfo(scores.dtype).min)
        attended = torch.softmax(scores, dim=-1) @ v
        mixed = attended.transpose(1, 2).reshape(batch, 1, heads * head_width)
        output = self.norm(token + self.out(mixed))
        return output + self.ff(output)


class XRec(nn.Module):
    """Reduced-width X-Rec with history prefill and a single denoising layer."""

    def __init__(self, item_vectors: Tensor, anchors: int, width: int = 48, heads: int = 4, max_history: int = 40) -> None:
        super().__init__()
        if item_vectors.ndim != 2 or item_vectors.shape[0] < anchors:
            raise ValueError("invalid item vectors or anchor count")
        self.register_buffer("items", sphere_normalize(item_vectors.float()))
        self.item_dim = item_vectors.shape[1]
        self.max_history = max_history
        self.item_project = nn.Linear(self.item_dim, width)
        self.positions = nn.Embedding(max_history, width)
        self.prefill = nn.TransformerEncoderLayer(width, heads, dim_feedforward=4 * width, dropout=0.0, batch_first=True, norm_first=True)
        self.last = LateInteractionLayer(width, heads)
        self.anchor_head = nn.Linear(width, anchors)
        self.anchor_embedding = nn.Embedding(anchors, width)
        self.time_embedding = nn.Sequential(nn.Linear(2, width), nn.SiLU(), nn.Linear(width, width))
        self.adaln = nn.Linear(width, 2 * width)
        self.velocity_head = nn.Linear(width, self.item_dim)

    def encode(self, history: Tensor, valid: Tensor) -> tuple[Tensor, tuple[Tensor, Tensor], Tensor]:
        batch, length = history.shape
        if length > self.max_history or not valid.any(dim=1).all():
            raise ValueError("history too long or contains an empty row")
        tokens = self.item_project(self.items[history])
        tokens = tokens + self.positions(torch.arange(length, device=history.device))[None]
        causal = torch.triu(torch.ones(length, length, device=history.device, dtype=torch.bool), diagonal=1)
        tokens = self.prefill(tokens, src_mask=causal, src_key_padding_mask=~valid)
        last_index = valid.long().sum(dim=1) - 1
        final_history = self.last.encode_history(tokens, valid)
        summary = final_history[torch.arange(batch, device=history.device), last_index]
        return self.anchor_head(summary), self.last.cache(tokens), valid

    def velocity(self, point: Tensor, time: Tensor, anchor: Tensor, cache: tuple[Tensor, Tensor], valid: Tensor) -> Tensor:
        point = sphere_normalize(point)
        token = self.item_project(point)[:, None, :]
        phase = torch.stack((torch.sin(time * math.pi), torch.cos(time * math.pi)), dim=-1)
        condition = self.anchor_embedding(anchor) + self.time_embedding(phase)
        scale, shift = self.adaln(condition).chunk(2, dim=-1)
        token = F.layer_norm(token, (token.shape[-1],)) * (1 + scale[:, None]) + shift[:, None]
        hidden = self.last(token, cache, valid)[:, 0]
        return tangent_projection(point, self.velocity_head(hidden))

    def loss(self, history: Tensor, valid: Tensor, target: Tensor, target_anchor: Tensor) -> tuple[Tensor, dict[str, Tensor]]:
        logits, cache, valid = self.encode(history, valid)
        # Multiple conditional flow samples per example approximate Eq. (22)
        # without rerunning the history transformer.
        draws = 4
        target_vector = self.items[target].repeat_interleave(draws, dim=0)
        expanded_anchor = target_anchor.repeat_interleave(draws)
        expanded_cache = tuple(t.repeat_interleave(draws, dim=0) for t in cache)
        expanded_valid = valid.repeat_interleave(draws, dim=0)
        noise = sphere_normalize(torch.randn_like(target_vector))
        time = torch.rand(len(target_vector), device=history.device)
        point, target_velocity = geodesic_interpolate(noise, target_vector, time)
        prediction = self.velocity(point, time, expanded_anchor, expanded_cache, expanded_valid)
        anchor_loss = F.cross_entropy(logits, target_anchor)
        # The paper minimizes a squared vector norm, not per-coordinate MSE.
        flow_loss = ((prediction - target_velocity) ** 2).sum(dim=-1).mean()
        return anchor_loss + flow_loss, {"anchor_ce": anchor_loss.detach(), "rfm_squared_norm": flow_loss.detach()}

    @torch.no_grad()
    def triggers(self, history: Tensor, valid: Tensor, *, samples: int = 8, steps: int = 3, seed: int = 42) -> Tensor:
        if samples < 1 or steps < 1:
            raise ValueError("samples and steps must be positive")
        generator = torch.Generator(device=history.device).manual_seed(seed)
        logits, cache, valid = self.encode(history, valid)
        anchors = torch.multinomial(torch.softmax(logits, dim=-1), samples, replacement=True, generator=generator)
        batch = history.shape[0]
        point = sphere_normalize(torch.randn(batch * samples, self.item_dim, device=history.device, generator=generator))
        expanded_cache = tuple(t.repeat_interleave(samples, dim=0) for t in cache)
        expanded_valid = valid.repeat_interleave(samples, dim=0)
        for iteration in range(steps):
            time = torch.full((batch * samples,), iteration / steps, device=history.device)
            velocity = self.velocity(point, time, anchors.reshape(-1), expanded_cache, expanded_valid)
            point = riemannian_euler(point, velocity, 1 / steps)
        return point.reshape(batch, samples, self.item_dim)
