"""Exact small-tensor semantic-block selection/attention, arXiv:2611.04313.

This reference implements equations 1--4, not the FlashAttention/vLLM kernels
or a long-context model benchmark. Routing and attention representations are
separate; fitting an index over a whole prompt is not a streaming-causality proof.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True


def _finite(value, name, ndim):
    if (value.ndim != ndim or min(value.shape) < 1 or not value.is_floating_point()
            or not bool(torch.isfinite(value).all())):
        raise ValueError(f'{name} must be a nonempty finite floating tensor of rank {ndim}')


def _unit(value):
    norms = torch.linalg.vector_norm(value, dim=-1, keepdim=True)
    if bool((norms == 0).any()):
        raise ValueError('routing vectors must have nonzero norm')
    return value / norms


@dataclass(frozen=True)
class SemanticIndex:
    centroids: torch.Tensor  # [KV heads, clusters, routing dimension]
    assignments: torch.Tensor  # [KV heads, indexed prompt positions]


@torch.no_grad()
def build_index(keys, *, seed=42, target_block_size=2048, clusters=None,
                iterations=8, fit_samples=None):
    """Spherical k-means per KV head; Appendix B defaults, optional scaled C.

    keys are pre-RoPE ROUTING keys [prompt, KV heads, dimension]. Empty clusters
    are reseeded from the sampled keys. No contiguous-position clustering is used.
    """
    _finite(keys, 'routing keys', 3)
    length, heads, _ = keys.shape
    if type(target_block_size) is not int or target_block_size < 1 or type(iterations) is not int or iterations < 1:
        raise ValueError('positive integer block size and iterations required')
    if clusters is None:
        clusters = min(length, max(128, 2 ** math.ceil(math.log2(length / target_block_size))))
    if type(clusters) is not int or not 1 <= clusters <= length:
        raise ValueError('cluster count must lie in [1, prompt length]')
    count = min(length, max(8192, 32 * clusters)) if fit_samples is None else fit_samples
    if type(count) is not int or not clusters <= count <= length:
        raise ValueError('fit sample count must cover every centroid and not exceed prompt length')
    generator = torch.Generator(device=keys.device).manual_seed(seed)
    normalized = _unit(keys)
    centers, assignments = [], []
    for head in range(heads):
        sample = normalized[torch.randperm(length, generator=generator, device=keys.device)[:count], head]
        center = sample[torch.randperm(count, generator=generator, device=keys.device)[:clusters]].clone()
        for _ in range(iterations):
            labels = (sample @ center.T).argmax(-1)
            updated = []
            for cluster in range(clusters):
                members = sample[labels == cluster]
                mean = members.sum(0) if len(members) else torch.zeros_like(center[cluster])
                if not bool(torch.linalg.vector_norm(mean) > 0):
                    mean = sample[torch.randint(count, (), generator=generator, device=keys.device)]
                updated.append(F.normalize(mean, dim=0))
            center = torch.stack(updated)
        centers.append(center)
        assignments.append((normalized[:, head] @ center.T).argmax(-1))
    return SemanticIndex(torch.stack(centers), torch.stack(assignments))


@torch.no_grad()
def select_positions(queries, index, positions, dense_starts, *, history_budget,
                     total_length=None, temperature=.1, size_exponent=.25):
    """Return [queries, KV heads, KV positions] exact score-ordered support.

    dense_starts defines D_t=[dense_start,t]. Unindexed generated tokens must
    lie in D_t. Whole selected blocks may overshoot the history budget.
    """
    _finite(queries, 'routing queries', 3)
    _finite(index.centroids, 'centroids', 3)
    qcount, qheads, dim = queries.shape
    heads, clusters, cdim = index.centroids.shape
    labels = index.assignments
    if (dim != cdim or qheads % heads or labels.ndim != 2 or labels.shape[0] != heads
            or labels.dtype != torch.long or labels.device != queries.device
            or index.centroids.device != queries.device or index.centroids.dtype != queries.dtype
            or labels.numel() == 0 or bool(((labels < 0) | (labels >= clusters)).any())):
        raise ValueError('compatible GQA routing queries and index required')
    indexed = labels.shape[1]
    length = indexed if total_length is None else total_length
    if type(length) is not int or length < indexed:
        raise ValueError('total KV length must include indexed prompt')
    for tensor in (positions, dense_starts):
        if tensor.shape != (qcount,) or tensor.dtype != torch.long or tensor.device != queries.device:
            raise ValueError('positions and dense starts must be same-device long query vectors')
    if (bool(((positions < 0) | (positions >= length)).any())
            or bool(((dense_starts < 0) | (dense_starts > indexed) | (dense_starts > positions + 1)).any())):
        raise ValueError('invalid causal positions or unindexed history outside dense region')
    if (type(history_budget) is not int or history_budget < 0 or not math.isfinite(temperature)
            or temperature <= 0 or not math.isfinite(size_exponent) or size_exponent < 0):
        raise ValueError('nonnegative integer budget, positive temperature and nonnegative size penalty required')
    normalized = _unit(queries)
    centers = _unit(index.centroids)
    support = torch.zeros(qcount, heads, length, dtype=torch.bool, device=queries.device)
    slots = torch.arange(length, device=queries.device)
    group = qheads // heads
    for row in range(qcount):
        dense = (slots >= dense_starts[row]) & (slots <= positions[row])
        history = (slots[:indexed] < dense_starts[row]) & (slots[:indexed] <= positions[row])
        support[row] = dense
        for head in range(heads):
            sizes = torch.bincount(labels[head, history], minlength=clusters)
            logits = normalized[row, head * group:(head + 1) * group] @ centers[head].T / temperature
            scores = logits.softmax(-1).sum(0) / (1 + sizes).to(queries.dtype).pow(size_exponent)
            selected = 0
            for cluster in torch.argsort(scores, descending=True, stable=True):
                if selected >= history_budget:
                    break
                members = history & (labels[head] == cluster)
                if bool(members.any()):
                    support[row, head, :indexed] |= members
                    selected += int(sizes[cluster])
    return support


def sparse_attention(queries, keys, values, index, positions, dense_starts, *,
                     history_budget, routing_queries=None):
    """Equation 4 over original QKV, with exact selected support and GQA."""
    for tensor, name in ((queries, 'queries'), (keys, 'keys'), (values, 'values')):
        _finite(tensor, name, 3)
    if (keys.shape[:2] != values.shape[:2] or queries.shape[-1] != keys.shape[-1]
            or queries.shape[1] % keys.shape[1] or keys.shape[1] != index.centroids.shape[0]
            or any(t.device != queries.device or t.dtype != queries.dtype for t in (keys, values))):
        raise ValueError('compatible original QKV shapes, devices and dtypes required')
    route = queries if routing_queries is None else routing_queries
    if route.shape != queries.shape or route.dtype != queries.dtype or route.device != queries.device:
        raise ValueError('routing queries must match original query shape, dtype and device')
    support = select_positions(route, index, positions, dense_starts, history_budget=history_budget,
                               total_length=len(keys))
    if not bool(support.any(-1).all()):
        raise ValueError('every query must have at least one visible selected position')
    group = queries.shape[1] // keys.shape[1]
    expanded_keys = keys.repeat_interleave(group, dim=1)
    expanded_values = values.repeat_interleave(group, dim=1)
    mask = support.repeat_interleave(group, dim=1)
    logits = torch.einsum('qhd,lhd->qhl', queries, expanded_keys) / math.sqrt(keys.shape[-1])
    weights = logits.masked_fill(~mask, -torch.inf).softmax(-1)
    return torch.einsum('qhl,lhv->qhv', weights, expanded_values), support


def diagnostic(seed=42, device='cpu'):
    generator = torch.Generator(device=device).manual_seed(seed)
    def rand(*shape):
        return torch.randn(shape, dtype=torch.float64, device=device, generator=generator)
    keys, values = rand(24, 2, 5), rand(24, 2, 4)
    queries = rand(3, 4, 5).requires_grad_()
    index = build_index(keys, seed=seed, clusters=4)
    positions = torch.tensor([7, 15, 23], device=device)
    starts = torch.tensor([4, 12, 20], device=device)
    dense, _ = sparse_attention(queries, keys, values, index, positions, starts, history_budget=24)
    full_mask = torch.arange(24, device=device)[None, None] <= positions[:, None, None]
    k, v = keys.repeat_interleave(2, 1), values.repeat_interleave(2, 1)
    reference = torch.einsum('qhl,lhv->qhv',
        (torch.einsum('qhd,lhd->qhl', queries, k) / math.sqrt(5)).masked_fill(~full_mask, -torch.inf).softmax(-1), v)
    output, support = sparse_attention(queries, keys, values, index, positions, starts, history_budget=3)
    output.square().sum().backward()
    error = float((dense - reference).detach().abs().max())
    gradient = float(queries.grad.abs().sum())
    future = int((support & ~full_mask).sum())
    return {'seed': seed, 'diagnostic_only': True, 'evaluation_tier': 'l1_mechanism',
            'metrics': {'dense_reference_max_error': error, 'query_gradient_l1': gradient,
                        'future_positions_selected': future, 'mean_selected_positions': float(support.sum(-1).double().mean())},
            'checks': {'dense_limit_agrees': error < 1e-10, 'causal_support': future == 0,
                       'actual_attention_gradient': gradient > 0, 'no_empty_support': bool(support.any(-1).all())}}
