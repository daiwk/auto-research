"""VFold: full-rank CCA/head assignment and function-preserving GQA folding.

Maps use the uncentered second moments in paper Appendix B. There is no
low-rank truncation, affine intercept, key averaging, or learned predictor.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch


def _root(matrix, exponent):
    values, vectors = torch.linalg.eigh(matrix)
    if not bool((values > 0).all()):
        raise ValueError("positive definite regularized second moment required")
    return (vectors * values.pow(exponent)[None]) @ vectors.T


def cca_map(reference, source, ridge=1e-4):
    """Return T such that source @ T aligns with reference, preserving rank."""
    if reference.shape != source.shape or reference.ndim != 2 or reference.shape[0] < 2:
        raise ValueError("matched token-by-channel calibration matrices required")
    if ridge <= 0 or not torch.isfinite(reference).all() or not torch.isfinite(source).all():
        raise ValueError("finite samples and positive regularization required")
    x, y = reference.double(), source.double()
    identity = torch.eye(x.shape[1], device=x.device, dtype=x.dtype)
    xx, yy = x.T @ x / len(x) + ridge * identity, y.T @ y / len(y) + ridge * identity
    xy = x.T @ y / len(x)
    u, _, vh = torch.linalg.svd(_root(xx, -.5) @ xy @ _root(yy, -.5))
    result = _root(yy, -.5) @ vh.T @ u.T @ _root(xx, .5)
    if not bool(torch.isfinite(result).all()):
        raise ValueError("nonfinite CCA map")
    return result


def minimum_assignment(cost):
    """Square Hungarian shortest-augmenting-path algorithm, no scipy dependency."""
    if cost.ndim != 2 or cost.shape[0] != cost.shape[1] or not torch.isfinite(cost).all():
        raise ValueError("finite square head-cost matrix required")
    c = cost.detach().double().cpu().tolist()
    n = len(c)
    if not n:
        raise ValueError("nonempty head assignment required")
    u, v, p, way = [0.] * (n + 1), [0.] * (n + 1), [0] * (n + 1), [0] * (n + 1)
    for i in range(1, n + 1):
        p[0], j0 = i, 0
        best, used = [math.inf] * (n + 1), [False] * (n + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = p[j0], math.inf, 0
            for j in range(1, n + 1):
                if not used[j]:
                    value = c[i0 - 1][j - 1] - u[i0] - v[j]
                    if value < best[j]:
                        best[j], way[j] = value, j0
                    if best[j] < delta:
                        delta, j1 = best[j], j
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    best[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [0] * n
    for j in range(1, n + 1):
        assignment[p[j] - 1] = j - 1
    return tuple(assignment)


@dataclass(frozen=True)
class Alignment:
    permutation: tuple[int, ...]
    maps: torch.Tensor  # new KV head, old channel, aligned channel
    cost: float


def fit_alignment(reference, source, ridge=1e-4):
    """Inputs are matched calibration [tokens, KV heads, head dim]."""
    if reference.ndim != 3 or reference.shape != source.shape:
        raise ValueError("same token/head/channel calibration shape required")
    heads = reference.shape[1]
    maps, cost = [], torch.empty(heads, heads, dtype=torch.float64)
    for i in range(heads):
        row = []
        for j in range(heads):
            transform = cca_map(reference[:, i], source[:, j], ridge)
            row.append(transform)
            # Equation 3 evaluates the inverse reconstruction, not raw cosine.
            error = reference[:, i].double() @ torch.linalg.inv(transform) - source[:, j].double()
            cost[i, j] = torch.linalg.vector_norm(error).cpu()
        maps.append(row)
    permutation = minimum_assignment(cost)
    chosen = torch.stack([maps[i][j] for i, j in enumerate(permutation)])
    return Alignment(permutation, chosen, sum(float(cost[i, j]) for i, j in enumerate(permutation)))


@torch.no_grad()
def fold_attention(attention, alignment, *, head_dim, query_heads, kv_heads):
    """Absorb Appendix A maps into ordinary PyTorch q/k/v/o Linear weights."""
    if query_heads % kv_heads or tuple(sorted(alignment.permutation)) != tuple(range(kv_heads)):
        raise ValueError("valid GQA head grouping and bijective permutation required")
    modules = [getattr(attention, name) for name in ("q_proj", "k_proj", "v_proj", "o_proj")]
    if not all(isinstance(m, torch.nn.Linear) for m in modules):
        raise ValueError("unwrapped Linear projections required; fold before installing adapters")
    if alignment.maps.shape != (kv_heads, head_dim, head_dim):
        raise ValueError("full-rank per-head maps required")
    for name in ("q_norm", "k_norm"):
        norm = getattr(attention, name, None)
        if norm is not None and norm.weight.numel() != head_dim:
            raise ValueError("only shared within-head QK normalization supported")
    q, k, value, out = modules
    group = query_heads // kv_heads
    permutation = torch.tensor(alignment.permutation, device=value.weight.device)
    t = alignment.maps.to(value.weight.device).float()
    inverse = torch.linalg.inv(t)
    for projection, repeats in ((q, group), (k, 1), (value, 1)):
        weights = projection.weight.reshape(kv_heads, repeats, head_dim, -1)[permutation].float()
        if projection is value:
            weights = torch.einsum("hcd,hrci->hrdi", t, weights)
        projection.weight.copy_(weights.reshape_as(projection.weight))
        if projection.bias is not None:
            bias = projection.bias.reshape(kv_heads, repeats, head_dim)[permutation].float()
            if projection is value:
                bias = torch.einsum("hcd,hrc->hrd", t, bias)
            projection.bias.copy_(bias.reshape_as(projection.bias))
    weights = out.weight.reshape(out.out_features, kv_heads, group, head_dim)[:, permutation].float()
    weights = torch.einsum("ohrc,hdc->ohrd", weights, inverse)
    out.weight.copy_(weights.reshape_as(out.weight))


def attach_finish_hooks(model):
    """Finish merging only AFTER attention consumed the current full values."""
    handles = []
    for layer in model.model.layers:
        def finished(module, args, kwargs, output):
            cache = kwargs.get("past_key_values")
            if cache is not None and hasattr(cache, "finish_layer"):
                cache.finish_layer(module.layer_idx)
        handles.append(layer.self_attn.register_forward_hook(finished, with_kwargs=True))
    return handles


class ValueBanks:
    """Paired shared middle + per-layer protected sinks/recent values.

    Materialized attention values are temporary. Middle cache storage exists
    once per pair. This eager backend saves persistent bytes, not CUDA latency.
    """

    def __init__(self, layers, sink=4, recent=128):
        if layers < 2 or layers % 2 or sink < 0 or recent < 0:
            raise ValueError("positive even layer count and nonnegative protection required")
        self.layers, self.sink, self.recent = layers, sink, recent
        self.keys, self.prefix, self.tail, self.shared, self.pending = {}, {}, {}, {}, {}
        self.consumed = set()

    def update(self, layer, keys, values):
        if not 0 <= layer < self.layers or layer in self.pending:
            raise ValueError("valid layer and completed prior attention required")
        if keys.shape != values.shape or keys.ndim != 4 or keys.shape[0] != 1:
            raise ValueError("matching batch-one B/H/T/D keys and values required")
        if keys.requires_grad or values.requires_grad:
            raise ValueError("inference-only detached cache required")
        if layer in self.keys:
            old = torch.cat((self.prefix[layer], self.shared[layer // 2], self.tail[layer]), -2)
            values = torch.cat((old, values), -2)
            keys = torch.cat((self.keys[layer], keys), -2)
        else:
            keys = keys.clone()
        self.keys[layer] = keys
        self.pending[layer] = values
        return keys, values

    def finish_layer(self, layer):
        if layer not in self.pending:
            raise ValueError("cannot merge before cache update")
        self.consumed.add(layer)
        if layer % 2 == 0:
            return
        first = layer - 1
        if first not in self.consumed:
            raise ValueError("pair attention must consume both current values before merge")
        a, b = self.pending[first], self.pending[layer]
        if a.shape != b.shape:
            raise ValueError("paired cache lengths/shapes differ")
        length = a.shape[-2]
        left = min(self.sink, length)
        right = max(left, length - self.recent)
        # Protected slices must own compact storage: a view would retain the
        # entire uncompressed cache allocation and invalidate memory savings.
        for index, tensor in ((first, a), (layer, b)):
            self.prefix[index] = tensor[..., :left, :].clone()
            self.tail[index] = tensor[..., right:, :].clone()
            del self.pending[index]
            self.consumed.remove(index)
        self.shared[layer // 2] = (a[..., left:right, :] + b[..., left:right, :]) * .5

    def materialize(self, layer):
        if layer in self.pending:
            return self.pending[layer]
        return torch.cat((self.prefix[layer], self.shared[layer // 2], self.tail[layer]), -2)

    def persistent_bytes(self):
        tensors = [t for bank in (self.keys, self.prefix, self.tail, self.shared, self.pending)
                   for t in bank.values()]
        storage = {t.untyped_storage().data_ptr(): t.untyped_storage().nbytes() for t in tensors}
        return sum(storage.values())
