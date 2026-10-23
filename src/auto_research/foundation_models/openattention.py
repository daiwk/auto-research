"""OpenAttention's single-head tensor reference (arXiv:2610.30951v1).

QGC/QGS, ErrorGate water filling and residual count-aware proxies are executed.
No Triton kernel, pretrained model, incremental KV update or latency claim.
Upstream reference: 6e43d4fc8c0e95b26d17d198a4545c627b2d6931 (Apache-2.0).
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/openattention-a100-20261023.json"


def _matrix(value: Tensor, name: str) -> None:
    if value.ndim != 2 or min(value.shape) < 1 or value.dtype not in (torch.float32, torch.float64) or not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be a finite nonempty floating matrix")


def query_geometry(static_queries: Tensor, conditioning_queries: Tensor) -> tuple[Tensor, Tensor]:
    """Equal-weight query second moments; never use future/answer queries to fit."""
    _matrix(static_queries, "static queries")
    _matrix(conditioning_queries, "conditioning queries")
    if static_queries.shape[1] != conditioning_queries.shape[1] or static_queries.device != conditioning_queries.device:
        raise ValueError("query dimensions/device must match")
    moment = .5 * (static_queries.T @ static_queries / len(static_queries)
                   + conditioning_queries.T @ conditioning_queries / len(conditioning_queries))
    eigenvalues, eigenvectors = torch.linalg.eigh(moment)
    return eigenvalues.flip(0).clamp_min(0), eigenvectors.flip(1)


def waterfill(scores: Tensor, capacities: Tensor, budget: int) -> Tensor:
    """Eq. 7 with flooring; residual budget goes to highest-score free clusters.

    All-zero scores have no discrepancy preference: use equal weights as an
    explicit degeneracy policy. The allocation is heuristic, not an optimum.
    """
    if scores.ndim != 1 or capacities.shape != scores.shape or not scores.numel():
        raise ValueError("matching nonempty score/capacity vectors required")
    if not scores.is_floating_point() or capacities.dtype != torch.long or scores.device != capacities.device:
        raise ValueError("floating scores and same-device int64 capacities required")
    if not bool(torch.isfinite(scores).all()) or bool((scores < 0).any()) or bool((capacities < 0).any()):
        raise ValueError("nonnegative finite scores/capacities required")
    if not isinstance(budget, int) or not 0 <= budget <= int(capacities.sum()):
        raise ValueError("budget outside total capacity")
    if budget == int(capacities.sum()):
        return capacities.clone()
    if budget == 0:
        return torch.zeros_like(capacities)
    weights = scores.to(torch.float64)
    capacity = capacities.to(torch.float64)
    continuous = torch.zeros_like(weights)
    remaining = float(budget)
    # Solve the capped proportional allocation by active sets. A global bracket
    # max(capacity)/min(weight) can span 1e300; any fixed bisection count then
    # saturates unrelated clusters and destroys their relative quotas. Normalize
    # AGAIN on each active set, so filling a large-weight cluster exposes even
    # subnormal positive weights without constructing an enormous water level.
    active = (capacities > 0) & (weights > 0)
    while bool(active.any()) and remaining > 0:
        relative = weights[active] / weights[active].max()
        proposed = remaining * relative / relative.sum()
        positions = torch.nonzero(active, as_tuple=False).flatten()
        saturated = proposed >= capacity[active]
        if not bool(saturated.any()):
            continuous[positions] = proposed
            remaining = 0.
            break
        filled = positions[saturated]
        continuous[filled] = capacity[filled]
        remaining -= float(capacity[filled].sum())
        active[filled] = False
    # Positive discrepancy has priority. If its total capacity is exhausted,
    # zero-score clusters are exactly tied and use the documented equal-weight
    # degeneracy policy, rather than injecting epsilon into positive ratios.
    active = (capacities > 0) & (weights == 0)
    while bool(active.any()) and remaining > 0:
        positions = torch.nonzero(active, as_tuple=False).flatten()
        proposed = remaining / len(positions)
        saturated = capacity[positions] <= proposed
        if not bool(saturated.any()):
            continuous[positions] = proposed
            remaining = 0.
            break
        filled = positions[saturated]
        continuous[filled] = capacity[filled]
        remaining -= float(capacity[filled].sum())
        active[filled] = False
    quotas = continuous.floor().to(torch.long)
    # Floating boundary rounding can be one token above the target.
    while int(quotas.sum()) > budget:
        for cluster in scores.argsort(stable=True).tolist():
            if quotas[cluster] > 0:
                quotas[cluster] -= 1
                break
    while int(quotas.sum()) < budget:
        for cluster in scores.argsort(descending=True, stable=True).tolist():
            if quotas[cluster] < capacities[cluster]:
                quotas[cluster] += 1
                if int(quotas.sum()) == budget:
                    break
    return quotas


def errorgate(query: Tensor, mean_keys: Tensor, key_variances: Tensor, counts: Tensor) -> Tensor:
    """Eq. 6 in a common log scale; NOT a certified attention-output error bound."""
    if query.ndim != 1 or mean_keys.ndim != 2 or key_variances.shape != mean_keys.shape or counts.shape != mean_keys.shape[:1]:
        raise ValueError("incompatible query/cluster statistics")
    if query.shape[0] != mean_keys.shape[1] or any(x.device != query.device for x in (mean_keys, key_variances, counts)):
        raise ValueError("dimension/device mismatch")
    if any(not bool(torch.isfinite(x).all()) for x in (query, mean_keys, key_variances)) or bool((key_variances < 0).any()) or bool((counts < 0).any()):
        raise ValueError("invalid cluster statistics")
    mean_logit = mean_keys @ query / math.sqrt(query.numel())
    variance = key_variances @ query.square() / query.numel()
    spread = torch.erf(variance.sqrt() / math.sqrt(2))
    log_score = (counts.to(mean_keys.dtype).clamp_min(1).log() + mean_logit
                 + variance / 2 + spread.clamp_min(torch.finfo(mean_keys.dtype).tiny).log())
    valid = (counts > 0) & (spread > 0)
    if not bool(valid.any()):
        return torch.zeros_like(mean_logit)
    # Common rescaling preserves Eq. 7 ratios and avoids exp overflow.
    return torch.where(valid, (log_score - log_score[valid].max()).exp(), 0)


@dataclass(frozen=True)
class CacheIndex:
    keys: Tensor
    values: Tensor
    labels: Tensor
    basis: Tensor
    key_codes: Tensor
    key_scales: Tensor
    clusters: int


@torch.no_grad()
def fit_cache(keys: Tensor, values: Tensor, static_queries: Tensor, conditioning_queries: Tensor,
              *, clusters: int = 64, cluster_rank: int = 16, selector_rank: int = 32,
              iterations: int = 10, generator: torch.Generator | None = None) -> CacheIndex:
    """Prefill-only QGC and int8 QGS indexing for one head, no future queries."""
    for value, name in ((keys, "keys"), (values, "values"), (static_queries, "static queries"), (conditioning_queries, "conditioning queries")):
        _matrix(value, name)
        if value.device != keys.device or value.dtype != keys.dtype:
            raise ValueError("all matrices must share dtype and device")
    if keys.shape[0] != values.shape[0] or keys.shape[1] != static_queries.shape[1]:
        raise ValueError("cache/query dimensions mismatch")
    if not (1 <= clusters <= len(keys) and 1 <= cluster_rank and 1 <= selector_rank and iterations >= 1):
        raise ValueError("invalid cluster/rank/iteration count")
    eigenvalues, basis = query_geometry(static_queries, conditioning_queries)
    rank = min(cluster_rank, keys.shape[1])
    projected = (keys @ basis[:, :rank]) * eigenvalues[:rank].sqrt()
    centers = projected[torch.randperm(len(keys), device=keys.device, generator=generator)[:clusters]].clone()
    for _ in range(iterations):
        labels = torch.cdist(projected, centers).argmin(-1)
        for cluster in range(clusters):
            members = projected[labels == cluster]
            if len(members):
                centers[cluster] = members.mean(0)
    labels = torch.cdist(projected, centers).argmin(-1)
    selector_basis = basis[:, :min(selector_rank, keys.shape[1])]
    compressed_keys = keys @ selector_basis
    scales = compressed_keys.abs().amax(0) / 127
    scales = torch.where(scales > 0, scales, torch.ones_like(scales))
    codes = (compressed_keys / scales).round().clamp(-127, 127).to(torch.int8)
    return CacheIndex(keys, values, labels, selector_basis, codes, scales, clusters)


def qgs_scores(index: CacheIndex, query: Tensor) -> Tensor:
    if query.shape != index.keys.shape[1:] or query.device != index.keys.device or query.dtype != index.keys.dtype or not bool(torch.isfinite(query).all()):
        raise ValueError("query must match indexed key dimension/device/dtype")
    return (index.key_codes.to(index.keys.dtype) * index.key_scales) @ (query @ index.basis)


def residual_proxy_attention(query: Tensor, keys: Tensor, values: Tensor, labels: Tensor,
                             exact_indices: Tensor) -> Tensor:
    """Exact tokens plus count-aware means of *remaining* cluster members.

    This deliberately recomputes residual statistics as a transparent reference.
    The production kernel subtracts exact rows from cached sums instead.
    """
    _matrix(keys, "keys")
    _matrix(values, "values")
    if query.shape != keys.shape[1:] or values.shape[0] != len(keys) or labels.shape != keys.shape[:1]:
        raise ValueError("query/cache/labels mismatch")
    if labels.dtype != torch.long or exact_indices.ndim != 1 or exact_indices.dtype != torch.long:
        raise ValueError("integer labels and exact-index vector required")
    if any(x.device != keys.device for x in (query, values, labels, exact_indices)) or query.dtype != keys.dtype or values.dtype != keys.dtype:
        raise ValueError("cache/query dtype/device mismatch")
    if not bool(torch.isfinite(query).all()) or bool((labels < 0).any()):
        raise ValueError("finite query and nonnegative labels required")
    if exact_indices.numel() and (int(exact_indices.min()) < 0 or int(exact_indices.max()) >= len(keys)):
        raise ValueError("exact index outside cache")
    if exact_indices.unique().numel() != exact_indices.numel():
        raise ValueError("exact rows must not be duplicated")
    unread = torch.ones(len(keys), device=keys.device, dtype=torch.bool)
    unread[exact_indices] = False
    logits = [keys[exact_indices] @ query / math.sqrt(keys.shape[1])]
    payloads = [values[exact_indices]]
    for cluster in labels.unique(sorted=True):
        mask = unread & (labels == cluster)
        count = int(mask.sum())
        if count:
            logits.append((keys[mask].mean(0) @ query / math.sqrt(keys.shape[1]) + math.log(count)).reshape(1))
            payloads.append(values[mask].mean(0, keepdim=True))
    return torch.cat(logits).softmax(0) @ torch.cat(payloads)


@dataclass(frozen=True)
class AttentionResult:
    output: Tensor
    exact_indices: Tensor
    expansion_quotas: Tensor
    error_scores: Tensor
    charged_kv_rows: float


@torch.no_grad()
def attend(index: CacheIndex, query: Tensor, exact_budget: int, *,
           initial_indices: Tensor | None = None) -> AttentionResult:
    """QGS initial selection (or caller sink/window set), ErrorGate, residual merge.

    exact_budget counts all exact rows; 1.5*C detector rows are charged separately,
    as in the paper. The int8 index scan/preparation is NOT a free end-to-end cost.
    """
    scores = qgs_scores(index, query)
    if not isinstance(exact_budget, int) or not 0 <= exact_budget <= len(index.keys):
        raise ValueError("invalid exact token budget")
    if initial_indices is None:
        initial_indices = scores.argsort(descending=True, stable=True)[:min(2, exact_budget)]
    if initial_indices.ndim != 1 or initial_indices.dtype != torch.long or initial_indices.device != index.keys.device:
        raise ValueError("same-device integer initial indices required")
    if initial_indices.unique().numel() != initial_indices.numel() or initial_indices.numel() > exact_budget:
        raise ValueError("initial rows duplicated or over budget")
    if initial_indices.numel() and (int(initial_indices.min()) < 0 or int(initial_indices.max()) >= len(index.keys)):
        raise ValueError("initial index outside cache")
    available = torch.ones(len(index.keys), device=query.device, dtype=torch.bool)
    available[initial_indices] = False
    means, variances, counts = [], [], []
    for cluster in range(index.clusters):
        members = index.keys[available & (index.labels == cluster)]
        counts.append(len(members))
        means.append(members.mean(0) if len(members) else torch.zeros_like(query))
        variances.append(members.var(0, unbiased=False) if len(members) else torch.zeros_like(query))
    capacities = torch.tensor(counts, device=query.device, dtype=torch.long)
    errors = errorgate(query, torch.stack(means), torch.stack(variances), capacities)
    quotas = waterfill(errors, capacities, exact_budget - len(initial_indices))
    exact = [initial_indices]
    for cluster in range(index.clusters):
        positions = torch.arange(len(index.keys), device=query.device)[available & (index.labels == cluster)]
        order = scores[positions].argsort(descending=True, stable=True)
        exact.append(positions[order[:int(quotas[cluster])]])
    selected = torch.cat(exact).sort().values
    output = residual_proxy_attention(query, index.keys, index.values, index.labels, selected)
    return AttentionResult(output, selected, quotas, errors, len(selected) + 1.5 * index.clusters)


def diagnostic(seed: int, device: str = "cpu") -> dict:
    """Generated-tensor L1 check; no pretrained model or capability evaluation."""
    import hashlib
    generator = torch.Generator(device=device).manual_seed(seed)
    k = torch.randn(128, 16, generator=generator, device=device)
    v = torch.randn(128, 8, generator=generator, device=device)
    static = torch.randn(24, 16, generator=generator, device=device)
    conditioning = torch.randn(8, 16, generator=generator, device=device)
    # Decode query is sampled AFTER the prefill index inputs; never fits geometry.
    index = fit_cache(k, v, static, conditioning, clusters=8, cluster_rank=8,
                      selector_rank=12, generator=generator)
    q = torch.randn(16, generator=generator, device=device)
    result = attend(index, q, 16)
    dense = (k @ q / 4).softmax(0) @ v
    all_read = attend(index, q, 128).output
    expanded_k, expanded_v = k.clone(), v.clone()
    unread = torch.ones(128, device=device, dtype=torch.bool)
    unread[result.exact_indices] = False
    for cluster in range(index.clusters):
        mask = unread & (index.labels == cluster)
        if bool(mask.any()):
            expanded_k[mask] = k[mask].mean(0)
            expanded_v[mask] = v[mask].mean(0)
    expanded_output = (expanded_k @ q / 4).softmax(0) @ expanded_v
    # Equal-key clusters must be exactly reducible even with unequal counts.
    simple_k = torch.tensor([[0.], [0.], [0.], [2.]], device=device)
    simple_v = torch.tensor([[1.], [1.], [1.], [4.]], device=device)
    simple_q = torch.ones(1, device=device)
    simple = residual_proxy_attention(simple_q, simple_k, simple_v,
                                      torch.tensor([0, 0, 0, 1], device=device),
                                      torch.empty(0, dtype=torch.long, device=device))
    expected = (simple_k[:, 0]).softmax(0) @ simple_v
    errors = {"full_read_max_abs_error": float((all_read - dense).abs().max()),
              "expanded_proxy_max_abs_error": float((result.output - expanded_output).abs().max()),
              "equal_key_proxy_max_abs_error": float((simple - expected).abs().max())}
    checks = {name: error <= 2e-5 for name, error in errors.items()}
    checks["exact_budget_and_uniqueness"] = len(result.exact_indices) == 16 and len(result.exact_indices.unique()) == 16
    checks["detector_rows_charged"] = result.charged_kv_rows == 16 + 1.5 * 8
    checks["int8_selector_index"] = index.key_codes.dtype == torch.int8
    dynamic_allocation = waterfill(torch.tensor([1., .5, 1e-30], device=device, dtype=torch.float64),
                                   torch.tensor([100, 100, 100], device=device), 20)
    checks["dynamic_range_waterfill_exact"] = dynamic_allocation.tolist() == [14, 6, 0]
    if not all(checks.values()):
        raise RuntimeError(f"OpenAttention reference mismatch: {errors}")
    return {"seed": seed, "checks": checks, "metrics": {**errors,
            "dense_relative_output_error": float((result.output - dense).norm() / dense.norm().clamp_min(1e-12)),
            "exact_rows": len(result.exact_indices), "charged_kv_rows": result.charged_kv_rows},
            "data_sha256": hashlib.sha256(k.cpu().numpy().tobytes() + static.cpu().numpy().tobytes()
                                          + conditioning.cpu().numpy().tobytes()).hexdigest()}
