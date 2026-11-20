"""HiSA equation-3 reference, not Flash-HiSA or a trained language model.

Q/K are pre-RoPE tensors [batch, heads, tokens, even head_dim]. This small
fp32/fp64 reference materializes pair scores. It demonstrates the exact static
partial dot product, not the paper's sparse-kernel speed or compact KV storage.
"""

import math
import torch

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/hisa-a100-20261120-latest.json"


def _parameters(head_dim, rope_base, angle_budget):
    if type(head_dim) is not int or head_dim <= 0 or head_dim % 2:
        raise ValueError("positive even head dimension required")
    if (
        type(rope_base) not in (int, float)
        or not math.isfinite(rope_base)
        or rope_base <= 0
        or type(angle_budget) not in (int, float)
        or math.isnan(angle_budget)
        or angle_budget <= 0
    ):
        raise ValueError("positive finite RoPE base and positive angle budget required")


def _positions(positions, length, device):
    if positions is None:
        return torch.arange(length, device=device)
    positions = torch.as_tensor(positions, device=device)
    if (
        positions.ndim != 1
        or not positions.numel()
        or positions.numel() != length
        or positions.dtype == torch.bool
        or positions.is_floating_point()
        or positions.is_complex()
    ):
        raise ValueError("strictly increasing nonnegative integer positions required")
    # uint64 comparisons are not implemented on every PyTorch backend. Inspect
    # unsigned values before casting, rather than accepting int64 wraparound.
    if positions.dtype == torch.uint64 and any(
        value > torch.iinfo(torch.int64).max for value in positions.detach().cpu().tolist()
    ):
        raise ValueError("positions exceed the supported signed int64 range")
    # uint8 subtraction would wrap a future key's negative distance around.
    positions = positions.to(torch.int64)
    if (positions < 0).any() or (positions[1:] <= positions[:-1]).any():
        raise ValueError("strictly increasing nonnegative int64-range positions required")
    # Both operands are now in [0, INT64_MAX], so every difference is in
    # [-INT64_MAX, INT64_MAX]; subtraction cannot overflow signed int64.
    return positions


def pair_mask(query_positions, key_positions, head_dim, rope_base=10000.0,
              angle_budget=math.pi / 2):
    """Keep a frequency pair iff 0 <= (i-j)*theta_l < Phi; no angle wrapping."""
    _parameters(head_dim, rope_base, angle_budget)
    q = torch.as_tensor(query_positions)
    k = torch.as_tensor(key_positions, device=q.device)
    q = _positions(q, q.numel(), q.device)
    k = _positions(k, k.numel(), q.device)
    frequencies = rope_base ** (-2 * torch.arange(head_dim // 2, device=q.device,
                                                  dtype=torch.float64) / head_dim)
    distance = q[:, None] - k[None, :]
    return (distance[..., None] >= 0) & (
        distance[..., None].to(torch.float64) * frequencies < angle_budget
    )


def _validate(q, k, v=None):
    tensors = (q, k) if v is None else (q, k, v)
    if any(
        not isinstance(t, torch.Tensor)
        or t.ndim != 4
        or not t.numel()
        or t.dtype not in (torch.float32, torch.float64)
        or t.dtype != q.dtype
        or t.device != q.device
        or not torch.isfinite(t).all()
        for t in tensors
    ):
        raise ValueError("finite compatible nonempty rank-4 fp32/fp64 tensors required")
    if q.shape[:2] != k.shape[:2] or q.shape[-1] != k.shape[-1]:
        raise ValueError("query/key batch, head count and head dimension must match")
    if v is not None and v.shape[:3] != k.shape[:3]:
        raise ValueError("values must match the key batch, heads and token axis")


def _rotate(tensor, positions, base):
    d = tensor.shape[-1]
    frequencies = base ** (-2 * torch.arange(d // 2, device=tensor.device,
                                            dtype=tensor.dtype) / d)
    angles = positions.to(tensor.dtype)[:, None] * frequencies
    pairs = tensor.reshape(*tensor.shape[:-1], d // 2, 2)
    first, second = pairs.unbind(-1)
    return torch.stack((first * angles.cos() - second * angles.sin(),
                        first * angles.sin() + second * angles.cos()), -1)


def scores(q, k, *, query_positions=None, key_positions=None, rope_base=10000.0,
           angle_budget=math.pi / 2):
    """Exact HiSA logits; causal/out-of-reach keys are -inf, not zero logits."""
    _validate(q, k)
    _parameters(q.shape[-1], rope_base, angle_budget)
    qp = _positions(query_positions, q.shape[2], q.device)
    kp = _positions(key_positions, k.shape[2], q.device)
    mask = pair_mask(qp, kp, q.shape[-1], rope_base, angle_budget)
    valid = mask.any(-1)
    if not valid.any(-1).all():
        raise ValueError("every query needs at least one causal key within reach")
    rq, rk = _rotate(q, qp, rope_base), _rotate(k, kp, rope_base)
    parts = torch.einsum("bhqpc,bhkpc->bhqkp", rq, rk)
    # Fixed 1/sqrt(d), not a normalization by the number of surviving pairs.
    logits = torch.where(mask, parts, 0).sum(-1) / math.sqrt(q.shape[-1])
    if not torch.isfinite(logits.masked_select(valid)).all():
        raise ValueError("valid attention scores overflowed the reference precision")
    return logits.masked_fill(~valid, -torch.inf)


def attention(q, k, v, **kwargs):
    """Reference softmax/value product; caller explicitly supplies GQA expansion."""
    _validate(q, k, v)
    return scores(q, k, **kwargs).softmax(-1) @ v


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative integer seed required")
    generator = torch.Generator(device=device).manual_seed(seed)
    options = {"generator": generator, "device": device, "dtype": torch.float64}
    q, k, v = (torch.randn(1, 2, 9, 8, **options) for _ in range(3))
    q.requires_grad_()
    positions = torch.arange(9, device=device)
    rq, rk = _rotate(q, positions, 10000), _rotate(k, positions, 10000)
    dense_scores = torch.einsum("bhqpc,bhkpc->bhqk", rq, rk) / math.sqrt(8)
    dense_scores = dense_scores.masked_fill(
        positions[:, None] < positions[None, :], -torch.inf
    )
    dense = dense_scores.softmax(-1) @ v
    infinite = attention(q, k, v, angle_budget=math.inf)
    sparse = attention(q, k, v)
    decoded = attention(q[:, :, -1:], k, v, query_positions=[8])
    future_k, future_v = k.clone(), v.clone()
    future_k[:, :, 5:] *= 17
    future_v[:, :, 5:] += 100
    perturbed = attention(q, future_k, future_v)
    gradient = torch.autograd.grad(sparse.square().sum(), q)[0]
    boundary = pair_mask(torch.tensor([1], device=device),
                         torch.tensor([0, 1], device=device), 2, angle_budget=1.0)
    # With d=2 and Phi=1 only distance zero is in reach. A zero logit for an
    # expired key would still admit it to softmax and corrupt the value read.
    probe_q = torch.ones(1, 1, 1, 2, device=device, dtype=torch.float64)
    probe_k = torch.ones(1, 1, 2, 2, device=device, dtype=torch.float64)
    probe_v = torch.tensor([100.0, 3.0], device=device, dtype=torch.float64).view(1, 1, 2, 1)
    expired = attention(probe_q, probe_k, probe_v, query_positions=[1],
                        angle_budget=1.0)
    active = pair_mask(positions, positions, 8)
    keep_fraction = active.sum().item() / (9 * 10 / 2 * 4)
    unsigned_mask = pair_mask(torch.tensor([0], device=device, dtype=torch.uint8),
                              torch.tensor([0, 1], device=device, dtype=torch.uint8), 8)
    largest = torch.iinfo(torch.int64).max
    signed_mask = pair_mask(torch.tensor([0, largest], device=device),
                            torch.tensor([0, largest], device=device), 8)
    unsigned_overflow_rejected = False
    try:
        pair_mask(torch.tensor([2**63], device=device, dtype=torch.uint64), [0], 8)
    except ValueError:
        unsigned_overflow_rejected = True
    dense_error = (infinite - dense).abs().max().item()
    continuation_error = (decoded - sparse[:, :, -1:]).abs().max().item()
    future_error = (perturbed[:, :, :5] - sparse[:, :, :5]).abs().max().item()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "infinite_budget_is_dense_rope": dense_error < 1e-11,
            "positioned_decode_equals_prefill_row": continuation_error < 1e-11,
            "future_values_and_keys_cannot_leak": future_error < 1e-11,
            "strict_angle_boundary": not boundary[0, 0, 0].item(),
            "self_pair_retained": boundary[0, 1, 0].item(),
            "expired_key_has_no_softmax_mass": abs(expired.item() - 3) < 1e-12,
            "partial_score_changes_output": (sparse - dense).abs().max().item() > 1e-4,
            "finite_nonzero_query_gradient": bool(torch.isfinite(gradient).all())
            and gradient.abs().sum().item() > 0,
            "nontrivial_static_pair_sparsity": 0 < keep_fraction < 1,
            "unsigned_future_distance_does_not_wrap": not unsigned_mask[0, 1].any().item(),
            "signed_distance_extremes_stay_causal": not signed_mask[0, 1].any().item()
            and not signed_mask[1, 0].any().item() and signed_mask[1, 1].all().item(),
            "uint64_out_of_range_rejected_before_cast": unsigned_overflow_rejected,
        },
        "metrics": {
            "dense_limit_max_abs_error": dense_error,
            "decode_continuation_max_abs_error": continuation_error,
            "future_perturbation_max_abs_error": future_error,
            "retained_pair_fraction": keep_fraction,
            "partial_vs_dense_max_abs_difference": (sparse - dense).abs().max().item(),
        },
    }
