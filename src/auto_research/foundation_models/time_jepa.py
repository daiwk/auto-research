"""Time-JEPA's train-only physical-state supervision and a tiny two-path JEPA.

This is a mechanism diagnostic, not V-JEPA weights, video benchmark capability,
or the original predictor architecture. Physical state never enters an encoder.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass

import torch
from torch import Tensor, nn
from torch.nn import functional as F


def align_nearest(sample_times: Tensor, measurement_times: Tensor, values: Tensor,
                  valid: Tensor, *, max_gap: float) -> tuple[Tensor, Tensor]:
    """Explicit local nearest-timestamp policy before the paper's tubelet pool.

    Ties choose the earlier measurement; distances above caller-supplied max_gap
    are invalid. This is not a claim of reproducing every dataset's decoder.
    """
    if sample_times.ndim != 1 or measurement_times.ndim != 1 or not measurement_times.numel():
        raise ValueError("one-dimensional nonempty measurement timestamps required")
    if not torch.isfinite(sample_times).all() or not torch.isfinite(measurement_times).all() or max_gap < 0:
        raise ValueError("finite timestamps and nonnegative gap required")
    if (measurement_times[1:] <= measurement_times[:-1]).any():
        raise ValueError("measurement timestamps must be strictly increasing")
    if values.ndim != 3 or values.shape != valid.shape or values.shape[1] != measurement_times.numel() or valid.dtype != torch.bool:
        raise ValueError("[batch,measurement,variable] values and bool validity required")
    right = torch.searchsorted(measurement_times, sample_times).clamp(max=measurement_times.numel() - 1)
    left = (right - 1).clamp(min=0)
    choose_left = (sample_times - measurement_times[left]).abs() <= (sample_times - measurement_times[right]).abs()
    index = torch.where(choose_left, left, right)
    accepted = (sample_times - measurement_times[index]).abs() <= max_gap
    mask = valid[:, index] & accepted[None, :, None]
    return torch.where(mask, values[:, index], 0), mask


def pool_tubelets(values: Tensor, valid: Tensor, tubelet_size: int = 2) -> tuple[Tensor, Tensor]:
    """Appendix C.1: mean only valid aligned frames, separately per variable."""
    if values.ndim != 3 or values.shape != valid.shape or valid.dtype != torch.bool or not values.is_floating_point():
        raise ValueError("[batch,frame,variable] values and bool validity required")
    if tubelet_size < 1 or values.shape[1] % tubelet_size or values.device != valid.device:
        raise ValueError("complete tubelets and same-device validity required")
    if not torch.isfinite(values[valid]).all():
        raise ValueError("valid state entries must be finite")
    shape = (values.shape[0], values.shape[1] // tubelet_size, tubelet_size, values.shape[2])
    mask = valid.reshape(shape)
    count = mask.sum(2)
    pooled = torch.where(valid, values, 0).reshape(shape).sum(2) / count.clamp_min(1)
    return pooled, count > 0


@dataclass(frozen=True)
class StateNormalizer:
    mean: Tensor
    std: Tensor
    observed: Tensor

    @classmethod
    def fit(cls, values: Tensor, valid: Tensor, *, split: str) -> StateNormalizer:
        if split != "train":
            raise ValueError("normalization fit is training-only")
        if values.ndim != 3 or valid.shape != values.shape or valid.dtype != torch.bool or not values.is_floating_point():
            raise ValueError("matching state tensor and boolean validity required")
        if not torch.isfinite(values[valid]).all():
            raise ValueError("nonfinite valid training states")
        # Calibration is detached and immutable; no learning through labels/statistics.
        values = values.detach()
        count = valid.sum((0, 1))
        mean = torch.where(valid, values, 0).sum((0, 1)) / count.clamp_min(1)
        variance = torch.where(valid, (values - mean).square(), 0).sum((0, 1)) / count.clamp_min(1)
        std = variance.sqrt().clamp_min(torch.finfo(values.dtype).eps)
        return cls(mean, torch.where(count > 0, std, torch.ones_like(std)), count > 0)

    def normalize(self, values: Tensor, valid: Tensor) -> tuple[Tensor, Tensor]:
        if values.shape != valid.shape or values.shape[-1] != self.mean.numel() or valid.dtype != torch.bool:
            raise ValueError("state/normalizer dimension mismatch")
        mask = valid & self.observed
        if not torch.isfinite(values[mask]).all():
            raise ValueError("nonfinite valid state")
        return torch.where(mask, (values - self.mean) / self.std, 0).detach(), mask


def physical_state_loss(prediction: Tensor, target: Tensor, valid: Tensor, beta: float = .5) -> Tensor:
    if prediction.shape != target.shape or valid.shape != prediction.shape or valid.dtype != torch.bool or beta <= 0:
        raise ValueError("matching tensors, bool mask and positive beta required")
    if not torch.isfinite(prediction).all() or not torch.isfinite(target[valid]).all():
        raise ValueError("finite predictions and valid targets required")
    difference = prediction - torch.where(valid, target.detach(), prediction.detach())
    absolute = difference.abs()
    element = torch.where(absolute < beta, difference.square() / (2 * beta), absolute - beta / 2)
    return torch.where(valid, element, 0).sum() / valid.sum().clamp_min(1)


class TokenVideoEncoder(nn.Module):
    """Small contextual token encoder used solely to exercise the shared paths."""
    def __init__(self, input_dim: int, width: int, tokens: int):
        super().__init__()
        self.project = nn.Linear(input_dim, width)
        self.position = nn.Parameter(torch.randn(tokens, width) * .02)
        self.norm = nn.LayerNorm(width)
        self.qkv = nn.Linear(width, width * 3)
        self.output = nn.Linear(width, width)
        self.ffn = nn.Sequential(nn.LayerNorm(width), nn.Linear(width, width * 2), nn.GELU(), nn.Linear(width * 2, width))

    def forward(self, video: Tensor, indices: Tensor | None = None) -> Tensor:
        flat = video.flatten(1, 2)
        if indices is None:
            indices = torch.arange(flat.shape[1], device=flat.device)
        x = self.project(flat[:, indices]) + self.position[indices]
        q, k, v = self.qkv(self.norm(x)).chunk(3, -1)
        x = x + self.output((q @ k.transpose(-1, -2) / q.shape[-1] ** .5).softmax(-1) @ v)
        return x + self.ffn(x)


class TinyTimeJEPA(nn.Module):
    def __init__(self, *, frames: int = 4, patches: int = 3, input_dim: int = 5,
                 width: int = 8, state_dim: int = 2):
        super().__init__()
        self.frames, self.patches = frames, patches
        self.online = TokenVideoEncoder(input_dim, width, frames * patches)
        self.target = copy.deepcopy(self.online).requires_grad_(False).eval()
        self.query = nn.Parameter(torch.randn(frames * patches, width) * .02)
        self.predictor = nn.Sequential(nn.Linear(width * 2, width), nn.GELU(), nn.Linear(width, width))
        self.physical_head = nn.Sequential(nn.Linear(width, width * 2), nn.GELU(), nn.Linear(width * 2, state_dim))

    def encode_video(self, video: Tensor) -> Tensor:
        return self.online(video)

    def forward(self, video: Tensor, *, context: Tensor, masked: Tensor,
                states: Tensor, valid: Tensor, time_weight: float = 1.) -> dict[str, Tensor]:
        if video.ndim != 4 or video.shape[1:3] != (self.frames, self.patches) or time_weight < 0:
            raise ValueError("video shape or time loss weight invalid")
        size = self.frames * self.patches
        for index in (context, masked):
            if index.ndim != 1 or index.dtype != torch.long or not index.numel() or index.unique().numel() != index.numel():
                raise ValueError("nonempty unique context/masked indices required")
            if int(index.min()) < 0 or int(index.max()) >= size:
                raise ValueError("index outside video tokens")
        if torch.isin(context, masked).any():
            raise ValueError("masked target tokens may not enter online context")
        encoded_context = self.online(video, context)
        query = self.query[masked].expand(video.shape[0], -1, -1)
        attention = (query @ encoded_context.transpose(-1, -2) / query.shape[-1] ** .5).softmax(-1)
        prediction = self.predictor(torch.cat((query, attention @ encoded_context), -1))
        with torch.no_grad():
            target = F.layer_norm(self.target(video)[:, masked], (query.shape[-1],))
        # Local JEPA skeleton uses L1; it is not the released V-JEPA predictor.
        latent_loss = (prediction - target).abs().mean()
        full = self.online(video).reshape(video.shape[0], self.frames, self.patches, -1).mean(2)
        state_prediction = self.physical_head(full)
        time_loss = physical_state_loss(state_prediction, states, valid)
        return {"loss": latent_loss + time_weight * time_loss, "latent_loss": latent_loss, "time_loss": time_loss,
                "latent_prediction": prediction, "latent_target": target, "state_prediction": state_prediction}

    @torch.no_grad()
    def update_target(self, decay: float = .99) -> None:
        if not 0 <= decay <= 1:
            raise ValueError("EMA decay outside [0,1]")
        for target, online in zip(self.target.parameters(), self.online.parameters(), strict=True):
            target.mul_(decay).add_(online, alpha=1 - decay)
