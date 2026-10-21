"""SSA Algorithm 1 and RACE native projection operators, arXiv v1 formula scope.

These are single-head reference operators, not paged-cache kernels or pretrained
model adapters. Calibration and discrete selection are outside the gradient path.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch


def _matrix(value: torch.Tensor, name: str) -> None:
    if value.ndim != 2 or not value.is_floating_point() or not bool(torch.isfinite(value).all()):
        raise ValueError(f"{name} must be a finite floating matrix")


@dataclass(frozen=True)
class SSAResult:
    output: torch.Tensor
    selected_indices: torch.Tensor
    heavy_indices: torch.Tensor
    inclusion_probabilities: torch.Tensor
    residual_draws: torch.Tensor


def stratified_sparse_attention(
    query: torch.Tensor,
    keys: torch.Tensor,
    values: torch.Tensor,
    proxy_scores: torch.Tensor,
    budget: int,
    *,
    generator: torch.Generator | None = None,
) -> SSAResult:
    """Exact SSA adaptive-budget Algorithm 1 (not its fixed-heavy GPU variant).

    Residual draws are WITH replacement, then deduplicated. Their correction is
    1 / (1 - (1 - p)**m), not 1/p or a draw-count correction. The returned
    self-normalized ratio is not an unbiased attention estimator. Gradients flow
    through exact selected Q/K/V, not the sampled allocation/proxy scores.
    """
    _matrix(keys, "keys")
    _matrix(values, "values")
    count, dimension = keys.shape
    if count == 0 or dimension == 0 or values.shape[0] != count or values.shape[1] == 0:
        raise ValueError("nonempty aligned keys and values required")
    if (query.shape != (dimension,) or proxy_scores.shape != (count,)
            or not query.is_floating_point() or not proxy_scores.is_floating_point()
            or not bool(torch.isfinite(query).all()) or not bool(torch.isfinite(proxy_scores).all())):
        raise ValueError("query/proxy shape and finite floating values required")
    if any(item.device != keys.device for item in (query, values, proxy_scores)):
        raise ValueError("all tensors must share a device")
    if isinstance(budget, bool) or not isinstance(budget, int) or not 1 <= budget <= count:
        raise ValueError("budget must be an integer in [1, number of keys]")
    dtype = torch.float64 if query.dtype == torch.float64 or keys.dtype == torch.float64 else torch.float32
    with torch.no_grad():
        if budget == count:
            selected = torch.arange(count, device=keys.device)
            heavy = selected
            inclusion = torch.ones(count, device=keys.device, dtype=torch.float64)
            draws = selected[:0]
        else:
            probabilities = torch.softmax(proxy_scores.detach().double(), dim=0)
            if not bool((probabilities > 0).all()):
                raise ValueError("proxy softmax underflow: unsupported score dynamic range")
            heavy_mask = torch.zeros(count, dtype=torch.bool, device=keys.device)
            # Water filling solves sum min(1, lambda*q_i) = budget. Each pass
            # permanently saturates >=1 coordinates; at least one residual remains.
            for _ in range(count):
                residual_mask = ~heavy_mask
                remaining = budget - int(heavy_mask.sum())
                scale = remaining / probabilities[residual_mask].sum()
                updated = heavy_mask | (probabilities * scale >= 1)
                if torch.equal(updated, heavy_mask):
                    break
                heavy_mask = updated
            heavy = torch.where(heavy_mask)[0]
            residual = torch.where(~heavy_mask)[0]
            draw_count = budget - heavy.numel()
            if draw_count < 1 or residual.numel() == 0:
                raise RuntimeError("invalid SSA water-filling allocation")
            proposal = probabilities[residual]
            proposal = proposal / proposal.sum()
            draws = residual[torch.multinomial(proposal, draw_count, replacement=True, generator=generator)]
            sampled = torch.unique(draws, sorted=True)
            selected = torch.sort(torch.cat((heavy, sampled)))[0]
            all_inclusion = torch.ones(count, device=keys.device, dtype=torch.float64)
            all_inclusion[residual] = -torch.expm1(draw_count * torch.log1p(-proposal))
            inclusion = all_inclusion[selected]
    logits = (keys[selected].to(dtype) @ query.to(dtype)) / math.sqrt(dimension)
    corrected = torch.softmax(logits.double() - torch.log(inclusion), dim=0).to(dtype)
    output = corrected @ values[selected].to(dtype)
    return SSAResult(output, selected, heavy, inclusion, draws)


def rotary_pair_indices(dimension: int, layout: str, *, device=None) -> torch.Tensor:
    if dimension < 2 or dimension % 2 or layout not in {"split_half", "interleaved"}:
        raise ValueError("even dimension and supported rotary layout required")
    ids = torch.arange(dimension // 2, device=device)
    return torch.stack((ids, ids + dimension // 2), 1) if layout == "split_half" else torch.stack((2 * ids, 2 * ids + 1), 1)


def apply_rope(
    inputs: torch.Tensor, positions: torch.Tensor, inverse_frequencies: torch.Tensor, *, layout: str,
) -> torch.Tensor:
    """Apply supplied ORIGINAL frequencies; never regenerate from reduced width."""
    _matrix(inputs, "inputs")
    pairs = rotary_pair_indices(inputs.shape[1], layout, device=inputs.device)
    if (positions.shape != (inputs.shape[0],) or inverse_frequencies.shape != (pairs.shape[0],)
            or positions.device != inputs.device or inverse_frequencies.device != inputs.device
            or not bool(torch.isfinite(positions).all()) or not bool(torch.isfinite(inverse_frequencies).all())):
        raise ValueError("positions/frequencies must be finite, aligned and on the input device")
    angles = positions.to(inputs.dtype)[:, None] * inverse_frequencies.to(inputs.dtype)[None, :]
    first, second = inputs[:, pairs[:, 0]], inputs[:, pairs[:, 1]]
    output = torch.empty_like(inputs)
    output[:, pairs[:, 0]] = first * angles.cos() - second * angles.sin()
    output[:, pairs[:, 1]] = first * angles.sin() + second * angles.cos()
    return output


def race_pair_selection(
    queries: torch.Tensor, keys: torch.Tensor, retained_dimension: int, *, layout: str,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """RACE Eq. 4: joint energy top-pairs, retaining original pair ordering."""
    _matrix(queries, "queries")
    _matrix(keys, "keys")
    if queries.shape != keys.shape or queries.device != keys.device or queries.shape[0] == 0:
        raise ValueError("nonempty matching Q/K calibration matrices required")
    pairs = rotary_pair_indices(queries.shape[1], layout, device=queries.device)
    if retained_dimension < 2 or retained_dimension % 2 or retained_dimension > queries.shape[1]:
        raise ValueError("retained dimension must be even and within head width")
    with torch.no_grad():
        energies = (queries.detach().double().square() + keys.detach().double().square()).sum(0)[pairs].sum(1)
        selected_pairs = torch.argsort(energies, descending=True, stable=True)[:retained_dimension // 2].sort()[0]
        if layout == "split_half":
            coordinates = torch.cat((pairs[selected_pairs, 0], pairs[selected_pairs, 1]))
        else:
            coordinates = pairs[selected_pairs].reshape(-1)
    return selected_pairs, coordinates, energies


@dataclass(frozen=True)
class RaceProjection:
    pair_ids: torch.Tensor
    coordinate_ids: torch.Tensor
    value_basis: torch.Tensor
    energies: torch.Tensor
    original_head_dimension: int
    layout: str


def calibrate_race(
    queries: torch.Tensor, keys: torch.Tensor, values: torch.Tensor,
    retained_qk_dimension: int, retained_value_dimension: int, *, layout: str,
) -> RaceProjection:
    pair_ids, coordinates, energies = race_pair_selection(queries, keys, retained_qk_dimension, layout=layout)
    _matrix(values, "values")
    if values.device != queries.device or values.shape[0] != queries.shape[0]:
        raise ValueError("V calibration must align with Q/K")
    if not 1 <= retained_value_dimension <= min(values.shape):
        raise ValueError("value rank must fit calibration matrix")
    with torch.no_grad():
        _, _, vh = torch.linalg.svd(values.detach().double(), full_matrices=False)
        basis = vh[:retained_value_dimension].T.to(values.dtype).contiguous()
    return RaceProjection(pair_ids, coordinates, basis, energies, queries.shape[1], layout)


def fold_race_weights(
    query_weight: torch.Tensor, key_weight: torch.Tensor, value_weight: torch.Tensor,
    output_weight: torch.Tensor, projection: RaceProjection,
) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Fold row-vector weights [input, output], exactly RACE Algorithm 1."""
    for name, value in (("Wq", query_weight), ("Wk", key_weight), ("Wv", value_weight), ("Wo", output_weight)):
        _matrix(value, name)
    if (query_weight.shape != key_weight.shape
            or query_weight.shape[1] != projection.original_head_dimension
            or query_weight.shape[0] != value_weight.shape[0]
            or value_weight.shape[1] != projection.value_basis.shape[0]
            or output_weight.shape[0] != value_weight.shape[1]):
        raise ValueError("projection/weight shapes do not align")
    if any(value.device != query_weight.device for value in (key_weight, value_weight, output_weight, projection.value_basis)):
        raise ValueError("weights and calibration basis must share a device")
    basis = projection.value_basis.to(value_weight.dtype)
    return (query_weight[:, projection.coordinate_ids], key_weight[:, projection.coordinate_ids],
            value_weight @ basis, basis.T.to(output_weight.dtype) @ output_weight)


def native_race_attention(
    inputs: torch.Tensor, positions: torch.Tensor, inverse_frequencies: torch.Tensor,
    folded_weights: tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor],
    projection: RaceProjection, *, causal: bool = True,
) -> torch.Tensor:
    """Native reduced Q/K/V path, preserving 1/sqrt(ORIGINAL d_k) scale."""
    _matrix(inputs, "inputs")
    wq, wk, wv, wo = folded_weights
    frequencies = inverse_frequencies[projection.pair_ids]
    queries = apply_rope(inputs @ wq, positions, frequencies, layout=projection.layout)
    keys = apply_rope(inputs @ wk, positions, frequencies, layout=projection.layout)
    scores = queries @ keys.T / math.sqrt(projection.original_head_dimension)
    if causal:
        scores = scores.masked_fill(torch.ones_like(scores, dtype=torch.bool).triu(1), -torch.inf)
    return (scores.softmax(-1) @ (inputs @ wv)) @ wo
