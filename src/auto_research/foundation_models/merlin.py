"""MERLIN (2610.37645v1) Eqs.7--9: bounded moment-routing subkernel.

No Gated DeltaNet/Mamba state transition, learned backbone, local/current
segment, or language task is implemented. Projected routing keys/queries and
segment readouts are external. This is NOT full multi-state linear attention.
"""
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/merlin-a100-20261030.json"


def _finite(x: Tensor, ndim: int) -> None:
    if (x.ndim != ndim or not 0 < x.numel() <= 1_048_576
            or x.dtype not in (torch.float32, torch.float64)
            or not bool(torch.isfinite(x).all())):
        raise ValueError("bounded finite float32/float64 tensor required")


def segment_moments(keys: Tensor) -> tuple[Tensor, Tensor]:
    """Eq.7 for [segments, uniform_segment_length, routing_width].

    The second tensor is E[kk^T], NOT a centered covariance. Padding is not
    admitted: supply equal-length segments of actual projected keys.
    """
    _finite(keys, 3)
    if keys.shape[0] * keys.shape[2] ** 2 > 1_048_576:
        raise ValueError("bounded derived second-moment matrix required")
    means = keys.mean(1)
    seconds = torch.einsum("smr,smd->srd", keys, keys) / keys.shape[1]
    _finite(means, 2)
    _finite(seconds, 3)
    return means, seconds


def completed_segment_visibility(starts: Tensor, segment_length: int,
                                 query_positions: Tensor) -> Tensor:
    """Past/completed segments only; end <= query_position+1 is causal.

    Starts are zero-based absolute token positions, intervals are disjoint and
    half-open. The current incomplete segment must be handled by the caller's
    actual recurrent model; this helper never reads its future final state.
    """
    if (starts.ndim != 1 or starts.numel() < 1 or starts.dtype != torch.long
            or query_positions.ndim != 1 or query_positions.numel() < 1
            or query_positions.dtype != torch.long or starts.device != query_positions.device
            or isinstance(segment_length, bool) or not isinstance(segment_length, int) or not 1 <= segment_length <= 100_000_000
            or starts.numel() * query_positions.numel() > 1_048_576
            or bool(((starts < 0) | (starts > 100_000_000)).any())
            or bool(((query_positions < 0) | (query_positions > 100_000_000)).any())
            or bool((starts[1:] < starts[:-1] + segment_length).any())):
        raise ValueError("ordered disjoint uniform segments and nonnegative absolute positions required")
    return starts[None] + segment_length <= query_positions[:, None] + 1


def routing_weights(queries: Tensor, means: Tensor, raw_seconds: Tensor,
                    visible: Tensor, gate: Tensor, mean_scale: Tensor,
                    variance_scale: Tensor) -> dict:
    """Eqs.8--9; scales MULTIPLY logits, two softmaxes mix AFTER normalization.

    Gate is the caller's learned sigmoid projection, one scalar per query.
    Temperatures are unconstrained finite scalar tensors as in the stated
    equation; this subkernel invents no softplus/initialization convention.
    """
    for x, n in ((queries, 2), (means, 2), (raw_seconds, 3), (gate, 1),
                 (mean_scale, 0), (variance_scale, 0)):
        _finite(x, n)
    t, width = queries.shape
    segments = len(means)
    if (t * segments > 1_048_576 or means.shape[1] != width or raw_seconds.shape != (segments, width, width)
            or visible.shape != (t, segments) or visible.dtype != torch.bool
            or gate.shape != (t,) or bool(((gate < 0) | (gate > 1)).any())
            or not bool(visible.any(-1).all()) or visible.device != queries.device
            or any(x.dtype != queries.dtype or x.device != queries.device
                   for x in (means, raw_seconds, gate, mean_scale, variance_scale))):
        raise ValueError("aligned routing tensors and at least one visible segment per query required")
    tolerance = 64 * torch.finfo(queries.dtype).eps
    if not torch.allclose(raw_seconds, raw_seconds.transpose(-1, -2), rtol=tolerance, atol=tolerance):
        raise ValueError("raw second moments must be symmetric")
    mean = queries @ means.T
    raw = torch.einsum("tr,srd,td->ts", queries, raw_seconds, queries)
    _finite(mean, 2)
    _finite(raw, 2)
    variance = raw - mean.square()
    _finite(variance, 2)
    bound = tolerance * torch.maximum(torch.ones_like(raw), raw.abs() + mean.square())
    _finite(bound, 2)
    if bool((variance < -bound).any()):
        raise ValueError("raw moments imply a negative query-alignment variance")
    # Only a round-off-sized negative is removed, not arbitrary bad moments.
    variance = variance.clamp_min(0)
    mean_logits, variance_logits = mean_scale * mean, variance_scale * variance
    _finite(mean_logits, 2)
    _finite(variance_logits, 2)
    mean_weights = mean_logits.masked_fill(~visible, -torch.inf).softmax(-1)
    variance_weights = variance_logits.masked_fill(~visible, -torch.inf).softmax(-1)
    weights = gate[:, None] * mean_weights + (1 - gate[:, None]) * variance_weights
    _finite(weights, 2)
    return {"weights": weights, "mean_scores": mean, "variance_scores": variance,
            "mean_weights": mean_weights, "variance_weights": variance_weights}


def aggregate_readouts(readouts: Tensor, weights: Tensor) -> Tensor:
    """Eq.4 on caller-computed state readouts; no recurrent model substitute."""
    _finite(readouts, 3)
    _finite(weights, 2)
    if (weights.shape != readouts.shape[:2] or weights.dtype != readouts.dtype
            or weights.device != readouts.device or bool((weights < 0).any())
            or not torch.allclose(weights.sum(-1), torch.ones_like(weights.sum(-1)), atol=1e-6, rtol=0)):
        raise ValueError("aligned normalized routing weights required")
    result = torch.einsum("ts,tsv->tv", weights, readouts)
    _finite(result, 2)
    return result


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or actual available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    args = {"device": device, "dtype": torch.float64, "generator": gen}
    keys = torch.randn(3, 4, 5, **args).requires_grad_()
    query = torch.randn(2, 5, **args).requires_grad_()
    means, seconds = segment_moments(keys)
    starts = torch.tensor([0, 4, 8], device=device)
    positions = torch.tensor([7, 11], device=device)
    visible = completed_segment_visibility(starts, 4, positions)
    logits = torch.randn(2, **args).requires_grad_()
    tau_mean = torch.tensor(1.3, device=device, dtype=torch.float64, requires_grad=True)
    tau_var = torch.tensor(.7, device=device, dtype=torch.float64, requires_grad=True)
    result = routing_weights(query, means, seconds, visible, logits.sigmoid(), tau_mean, tau_var)
    alignments = torch.einsum("tr,smr->tsm", query, keys)
    mean_error = (result["mean_scores"] - alignments.mean(-1)).abs().max().item()
    variance_error = (result["variance_scores"] - alignments.var(-1, unbiased=False)).abs().max().item()
    wrong_raw = tau_var * torch.einsum("tr,srd,td->ts", query, seconds, query)
    raw_gap = (wrong_raw.masked_fill(~visible, -torch.inf).softmax(-1)
               - result["variance_weights"]).abs().max().item()
    wrong_combined = (logits.sigmoid()[:, None] * tau_mean * result["mean_scores"]
        + (1 - logits.sigmoid()[:, None]) * tau_var * result["variance_scores"])
    combined_gap = (wrong_combined.masked_fill(~visible, -torch.inf).softmax(-1)
                    - result["weights"]).abs().max().item()
    readouts = torch.randn(2, 3, 4, **args)
    output = aggregate_readouts(readouts, result["weights"])
    reference = torch.stack([sum(result["weights"][t, s] * readouts[t, s] for s in range(3)) for t in range(2)])
    future_changed = readouts.clone()
    future_changed[~visible] += 1e3
    leak_error = (aggregate_readouts(future_changed, result["weights"]) - output).abs().max().item()
    output.square().sum().backward()
    gradient_norms = [x.grad.norm().item() for x in (keys, query, logits, tau_mean, tau_var)]
    gradient_norm = sum(gradient_norms)
    checks = {"alignment_mean_independent_reference": mean_error < 1e-12,
        "alignment_variance_independent_reference": variance_error < 1e-12,
        "raw_second_is_not_variance": raw_gap > 1e-8,
        "two_softmax_mixture_not_logit_mixture": combined_gap > 1e-8,
        "segment_future_mask_blocks_readout_changes": leak_error == 0 and bool((result["weights"][~visible] == 0).all()),
        "completed_segments_have_exact_boundary": torch.equal(visible, torch.tensor([[1, 1, 0], [1, 1, 1]], device=device, dtype=torch.bool)),
        "readout_aggregation_reference": torch.allclose(output, reference, atol=1e-12, rtol=0),
        "moments_gate_queries_receive_real_gradient": all(v > 0 and math.isfinite(v) for v in gradient_norms)}
    if not all(checks.values()):
        raise RuntimeError(f"MERLIN checks failed: {checks}")
    return {"seed": seed, "metrics": {"mean_reference_error": mean_error,
        "variance_reference_error": variance_error, "raw_moment_negative_control_gap": raw_gap,
        "single_softmax_negative_control_gap": combined_gap, "future_readout_leak_error": leak_error,
        "gradient_norm": gradient_norm, "minimum_gradient_group_norm": min(gradient_norms),
        "model_calls": 0}, "checks": checks}
