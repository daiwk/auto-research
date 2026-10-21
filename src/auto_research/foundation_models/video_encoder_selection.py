"""Training-free source selection from arXiv:2610.06616v1, Appendix I.

This module implements the conditional selector, not the unpublished SITE
allocator, a learned temporal refiner, or a video QA benchmark. The caller must
provide frozen visual/text features, frame quotas and a scene statistic.
"""
from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Mapping

import torch
from torch.nn import functional as F


@dataclass(frozen=True)
class CorrespondenceEdge:
    first: int
    second: int
    weight: float


@dataclass(frozen=True)
class SelectionResult:
    indices: torch.Tensor
    embeddings: torch.Tensor
    positions: torch.Tensor
    streams: dict[str, torch.Tensor]
    relevance: torch.Tensor
    quotas: torch.Tensor
    edges: tuple[CorrespondenceEdge, ...]
    trace: tuple[dict, ...]
    objective: float


def quotas_from_representatives(
    representatives: torch.Tensor, *, frames: int, tokens_per_frame: int, budget: int,
) -> torch.Tensor:
    """Inherit SITE's representative frame counts, Eq.45–48 (not SITE itself).

    Compressed slots may share representatives. Clipped overflow is assigned
    one slot at a time to the largest residual capacity; ties use earlier frames.
    """
    if frames < 1 or tokens_per_frame < 1 or not 0 <= budget <= frames * tokens_per_frame:
        raise ValueError("invalid frame capacities or budget")
    if representatives.ndim != 1 or len(representatives) != budget:
        raise ValueError("one representative source index per compressed slot required")
    if representatives.dtype not in (torch.int32, torch.int64):
        raise ValueError("representatives must be integer source indices")
    if representatives.numel() and (
        int(representatives.min()) < 0 or int(representatives.max()) >= frames * tokens_per_frame
    ):
        raise ValueError("representative source index outside candidate pool")
    quotas = torch.bincount(representatives.long() // tokens_per_frame, minlength=frames)
    quotas = quotas.clamp_max(tokens_per_frame)
    while int(quotas.sum()) < budget:
        frame = int((tokens_per_frame - quotas).argmax())
        quotas[frame] += 1
    return quotas


def question_relevance(features: torch.Tensor, question_vectors: torch.Tensor) -> torch.Tensor:
    """Maximum normalized fragment cosine, Eq.39–40; no answer is an input."""
    if features.ndim != 3 or question_vectors.ndim != 2:
        raise ValueError("features [T,N,D] and question_vectors [R,D] required")
    if features.shape[-1] != question_vectors.shape[-1] or not 1 <= len(question_vectors) <= 9:
        raise ValueError("one complete question and at most eight same-space fragments required")
    if not torch.isfinite(features).all() or not torch.isfinite(question_vectors).all():
        raise ValueError("features must be finite")
    if torch.any(question_vectors.norm(dim=-1) == 0):
        raise ValueError("question vectors must be nonzero")
    z = F.normalize(features.double(), dim=-1)
    q = F.normalize(question_vectors.to(device=features.device, dtype=torch.float64), dim=-1)
    # In particular, retain negative relevance: Eq.40 applies no ReLU or
    # additional clipping before the quality factor 1 + .8*m.
    return (z @ q.T).amax(dim=-1)


def dpp_kernels(features: torch.Tensor, relevance: torch.Tensor) -> torch.Tensor:
    """Feature-norm/question quality and frame-normalized kernels, Eq.41–44."""
    if features.ndim != 3 or relevance.shape != features.shape[:2]:
        raise ValueError("relevance must align with visual candidates")
    z = features.double()
    quality = (z.norm(dim=-1) * (1 + .8 * relevance)).clamp_min(1e-6)
    quality = quality / quality.mean(dim=-1, keepdim=True)
    unit = F.normalize(z, dim=-1)
    kernel = quality[:, :, None] * quality[:, None, :] * (unit @ unit.transpose(-1, -2))
    jitter = 1e-3 * quality.square().mean(dim=-1)
    identity = torch.eye(z.shape[1], device=z.device, dtype=z.dtype)
    return kernel + jitter[:, None, None] * identity


def dpp_residual(kernel: torch.Tensor, selected: list[int]) -> torch.Tensor:
    """All Schur-complement residuals, Eq.58; no explicit matrix inverse."""
    if not selected:
        return kernel.diagonal().clone()
    indices = torch.tensor(selected, device=kernel.device, dtype=torch.long)
    block = kernel[indices[:, None], indices[None, :]]
    cholesky = torch.linalg.cholesky(block)
    projected = torch.linalg.solve_triangular(cholesky, kernel[indices], upper=False)
    return kernel.diagonal() - projected.square().sum(dim=0)


def _validate_positions(positions: torch.Tensor, frames: int, tokens: int) -> None:
    if positions.shape != (frames, tokens, 3) or not torch.isfinite(positions).all():
        raise ValueError("finite source positions [T,N,(time,u,v)] required")
    if torch.any(positions[..., 1:] < 0) or torch.any(positions[..., 1:] > 1):
        raise ValueError("patch coordinates must be normalized to [0,1]")
    if not torch.all(positions[..., 0] == positions[:, :1, 0]):
        raise ValueError("source time must be identical for all tokens in a frame")
    if frames > 1 and not torch.all(positions[1:, 0, 0] > positions[:-1, 0, 0]):
        raise ValueError("frames must be in strictly increasing source time")
    if any(len(torch.unique(frame, dim=0)) != tokens for frame in positions):
        raise ValueError("source positions must be unique within a frame")


def correspondence_graph(
    features: torch.Tensor, positions: torch.Tensor, scene_similarities: torch.Tensor,
) -> tuple[CorrespondenceEdge, ...]:
    """Mutual adjacent-frame matches, confidence and state change, Eq.49–55.

    The paper does not define its scene statistic. It is deliberately supplied
    by the caller, rather than silently substituting a statistic in this core.
    For a one-candidate frame, the missing second cosine is the lower bound -1.
    """
    frames, tokens, _ = features.shape
    _validate_positions(positions, frames, tokens)
    if scene_similarities.shape != (max(0, frames - 1),):
        raise ValueError("one scene-similarity statistic per adjacent frame pair required")
    if not torch.isfinite(scene_similarities).all() or torch.any(scene_similarities.abs() > 1):
        raise ValueError("scene similarity must be finite and within [-1,1]")
    unit = F.normalize(features.double(), dim=-1)
    spatial = positions[..., 1:].to(device=features.device, dtype=torch.float64)
    edges = []
    for frame in range(frames - 1):
        if float(scene_similarities[frame]) < .65:
            continue
        similarity = (unit[frame] @ unit[frame + 1].T).clamp(-1, 1)
        forward = similarity.argmax(dim=1)
        reverse = similarity.argmax(dim=0)
        if tokens > 1:
            forward_values = similarity.topk(2, dim=1).values
            reverse_values = similarity.topk(2, dim=0).values
            forward_margin = forward_values[:, 0] - forward_values[:, 1]
            reverse_margin = reverse_values[0] - reverse_values[1]
        else:
            forward_margin = similarity[:, 0] + 1
            reverse_margin = similarity[0] + 1
        for first in range(tokens):
            second = int(forward[first])
            if int(reverse[second]) != first:
                continue
            cosine = float(similarity[first, second])
            margin = min(float(forward_margin[first]), float(reverse_margin[second]))
            distance = float((spatial[frame, first] - spatial[frame + 1, second]).norm()) / math.sqrt(2)
            if cosine < .65 or margin < .005 or distance > .5:
                continue
            confidence = min(1., max(0., (cosine - .65) / .35)) * min(1., max(0., margin / .05))
            change = max(min(1., distance / .25), min(1., max(0., 2 * (1 - cosine))))
            edges.append(CorrespondenceEdge(frame * tokens + first, (frame + 1) * tokens + second,
                                            confidence * change))
    return tuple(edges)


def greedy_source_indices(
    kernels: torch.Tensor, quotas: torch.Tensor, edges: tuple[CorrespondenceEdge, ...],
) -> tuple[list[int], tuple[dict, ...]]:
    """Eq.59–60: compare best singleton with per-token adjacent pair gain."""
    frames, tokens, _ = kernels.shape
    quotas = torch.as_tensor(quotas, device=kernels.device)
    if quotas.shape != (frames,) or quotas.dtype not in (torch.int32, torch.int64):
        raise ValueError("one integer quota per frame required")
    if torch.any(quotas < 0) or torch.any(quotas > tokens):
        raise ValueError("quota exceeds frame capacity")
    if not torch.isfinite(kernels).all() or kernels.shape[-1] != tokens:
        raise ValueError("finite square frame kernels required")
    for edge in edges:
        if not (0 <= edge.first < edge.second < frames * tokens):
            raise ValueError("invalid correspondence source indices")
        if edge.second // tokens != edge.first // tokens + 1 or not math.isfinite(edge.weight) or edge.weight < 0:
            raise ValueError("correspondence must be a nonnegative adjacent-frame edge")
    if len({(edge.first, edge.second) for edge in edges}) != len(edges):
        raise ValueError("duplicate correspondence edges")
    selected: list[int] = []
    per_frame: list[list[int]] = [[] for _ in range(frames)]
    remaining = quotas.tolist()
    trace = []
    while len(selected) < int(quotas.sum()):
        scores = {}
        for frame in range(frames):
            if not remaining[frame]:
                continue
            residuals = dpp_residual(kernels[frame], per_frame[frame])
            for token in range(tokens):
                index = frame * tokens + token
                if token not in per_frame[frame]:
                    scores[index] = float(residuals[token].clamp_min(1e-14).log())
        retained = set(selected)
        for edge in edges:
            if edge.first in scores and edge.second in retained:
                scores[edge.first] += 2 * edge.weight
            if edge.second in scores and edge.first in retained:
                scores[edge.second] += 2 * edge.weight
        best = min(scores, key=lambda index: (-scores[index], index))
        move = [best]
        score = scores[best]
        for edge in edges:
            if edge.first in scores and edge.second in scores:
                pair_score = (scores[edge.first] + scores[edge.second] + 2 * edge.weight) / 2
                if pair_score > score:
                    score = pair_score
                    move = [edge.first, edge.second]
        # A cross-frame pair consumes one slot in each frame and cannot exceed
        # B when both quotas remain positive; singletons complete odd budgets.
        trace.append({"indices": move.copy(), "score_per_token": score,
                      "best_singleton_score": scores[best]})
        for index in move:
            frame, token = divmod(index, tokens)
            selected.append(index)
            per_frame[frame].append(token)
            remaining[frame] -= 1
    return selected, tuple(trace)


@torch.no_grad()
def select_source_tokens(
    features: torch.Tensor, question_vectors: torch.Tensor, positions: torch.Tensor,
    quotas: torch.Tensor, scene_similarities: torch.Tensor,
    *, streams: Mapping[str, torch.Tensor] | None = None,
) -> SelectionResult:
    """Return unchanged source rows in time/spatial order; never pool/refine."""
    if features.ndim != 3 or min(features.shape) < 1:
        raise ValueError("nonempty visual features [T,N,D] required")
    frames, tokens, dimensions = features.shape
    _validate_positions(positions, frames, tokens)
    streams = dict(streams or {})
    if any(value.shape[:2] != (frames, tokens) for value in streams.values()):
        raise ValueError("every intermediate stream must share the visual source rows")
    relevance = question_relevance(features, question_vectors)
    kernels = dpp_kernels(features, relevance)
    edges = correspondence_graph(features, positions, scene_similarities)
    selected, trace = greedy_source_indices(kernels, quotas, edges)
    source = positions.reshape(frames * tokens, 3)
    selected.sort(key=lambda index: tuple(source[index].tolist()))
    indices = torch.tensor(selected, device=features.device, dtype=torch.long)
    objective = 0.
    retained = set(selected)
    for frame in range(frames):
        local = [index % tokens for index in selected if index // tokens == frame]
        if local:
            sign, logdet = torch.linalg.slogdet(kernels[frame][local][:, local])
            if float(sign) <= 0:
                raise RuntimeError("regularized DPP principal block is not positive definite")
            objective += float(logdet)
    objective += 2 * sum(edge.weight for edge in edges if edge.first in retained and edge.second in retained)
    return SelectionResult(
        indices=indices, embeddings=features.reshape(-1, dimensions)[indices],
        positions=source[indices.to(source.device)],
        streams={name: value.flatten(0, 1)[indices.to(value.device)] for name, value in streams.items()},
        relevance=relevance, quotas=quotas.clone(), edges=edges, trace=trace, objective=objective,
    )
