"""TaskPress Eqs.1--3: task-to-context attention x per-token value scale.

External task-guide attention and real K/V tensors; no LLM/guide generation,
quantized kernel, evolutionary search or end-to-end speed claim.
"""
import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/taskpress-a100-20261025.json"


def taskpress_scores(task_attention: Tensor, value_scale: Tensor, *, kernel_size: int) -> Tensor:
    """[B,KV-head,guide,context] sum-guide, zero-padded odd-width mean, multiply.

    GQA query-head -> KV-head aggregation is the caller's declared model policy;
    no silent head averaging. Scale is the existing per-token quantization scale,
    not an L2 norm or additive heuristic. No downstream query is an input here.
    """
    if (task_attention.ndim != 4 or min(task_attention.shape) < 1
            or not task_attention.is_floating_point() or task_attention.numel() > 1_048_576
            or not bool(torch.isfinite(task_attention).all()) or bool((task_attention < 0).any())):
        raise ValueError("bounded finite nonnegative [B,head,guide,context] attention required")
    if (value_scale.shape != task_attention.shape[:2] + task_attention.shape[-1:]
            or value_scale.device != task_attention.device or value_scale.dtype != task_attention.dtype
            or not bool(torch.isfinite(value_scale).all()) or bool((value_scale < 0).any())):
        raise ValueError("matching nonnegative per-context-token scales required")
    if isinstance(kernel_size, bool) or not isinstance(kernel_size, int) or kernel_size < 1 or kernel_size % 2 != 1:
        raise ValueError("explicit positive odd pooling kernel required")
    if kernel_size > 129:
        raise ValueError("cost gate: kernel<=129")
    work = task_attention.float() if task_attention.dtype in (torch.float16, torch.bfloat16) else task_attention
    pooled = F.avg_pool1d(work.sum(-2).flatten(0, 1)[:, None], kernel_size,
                          stride=1, padding=kernel_size // 2, count_include_pad=True).squeeze(1)
    result = pooled.reshape(value_scale.shape) * value_scale.to(work.dtype)
    if not bool(torch.isfinite(result).all()):
        raise ValueError("nonfinite TaskPress score; no silent clamp")
    return result


def symmetric_value_scale(values: Tensor, *, bits: int = 4) -> Tensor:
    """Eq.2 FP reference, max(abs(v))/(2**(b-1)-1); not a quantized runtime."""
    if (values.ndim != 4 or min(values.shape) < 1 or not values.is_floating_point()
            or not bool(torch.isfinite(values).all()) or not isinstance(bits, int) or not 2 <= bits <= 16):
        raise ValueError("finite [B,head,context,dimension] values and bits2..16 required")
    return values.abs().amax(-1) / (2 ** (bits - 1) - 1)


def prune_taskpress(keys: Tensor, values: Tensor, task_attention: Tensor, *, context_length: int,
                   keep: int, kernel_size: int, value_scale: Tensor | None = None, bits: int = 4) -> dict:
    """Uniform per-KV-head top-k, chronological gather, discarding guide K/V.

    K/V may include the appended guide; only the first context_length entries are
    scored and retained. Tie-break: stable lower context index (local convention,
    paper unspecified). Return original position IDs; never renumber RoPE slots.
    """
    if (keys.shape != values.shape or keys.ndim != 4 or keys.device != values.device
            or keys.dtype != values.dtype or not keys.is_floating_point()
            or keys.numel() > 1_048_576 or not bool(torch.isfinite(keys).all())
            or not bool(torch.isfinite(values).all())):
        raise ValueError("bounded matching finite K/V [B,head,prefill,dim] required")
    if (not isinstance(context_length, int) or not isinstance(keep, int)
            or not 1 <= keep <= context_length <= keys.shape[-2]
            or task_attention.shape[:2] != keys.shape[:2] or task_attention.shape[-1] != context_length):
        raise ValueError("valid context length/keep and aligned task attention required")
    scale = symmetric_value_scale(values[:, :, :context_length], bits=bits) if value_scale is None else value_scale
    scores = taskpress_scores(task_attention, scale, kernel_size=kernel_size)
    indices = scores.argsort(dim=-1, descending=True, stable=True)[..., :keep].sort(-1).values
    gather = indices[..., None].expand(-1, -1, -1, keys.shape[-1])
    return {"keys": keys.gather(-2, gather), "values": values.gather(-2, gather),
            "positions": indices, "scores": scores}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    keys = torch.randn(2, 2, 11, 4, generator=gen, device=device, dtype=torch.float64)
    values = torch.randn(keys.shape, generator=gen, device=device, dtype=torch.float64)
    attention = torch.rand(2, 2, 3, 8, generator=gen, device=device, dtype=torch.float64)
    scale = symmetric_value_scale(values[:, :, :8])
    result = prune_taskpress(keys, values, attention, context_length=8, keep=4, kernel_size=3)
    reference = torch.zeros_like(scale)
    for b in range(2):
        for h in range(2):
            for i in range(8):
                reference[b, h, i] = sum(attention[b, h, :, j].sum() for j in range(max(0, i - 1), min(8, i + 2))) / 3 * scale[b, h, i]
    error = (result["scores"] - reference).abs().max().item()
    expected = reference.argsort(dim=-1, descending=True, stable=True)[..., :4].sort(-1).values
    shifted_guide = values.clone()
    shifted_guide[:, :, 8:] = 1e5
    control = prune_taskpress(keys, shifted_guide, attention, context_length=8, keep=4, kernel_size=3)
    additive_gap = (result["scores"] - (reference / scale + scale)).abs().max().item()
    checks = {"eq1_3_independent_reference": error < 1e-12,
              "per_head_topk_and_original_positions": torch.equal(result["positions"], expected),
              "guide_tokens_discarded": torch.equal(control["positions"], expected) and int(expected.max()) < 8,
              "actual_kv_gather": torch.equal(result["values"], values.gather(-2, expected[..., None].expand(-1, -1, -1, 4))),
              "multiplicative_not_additive": additive_gap > 0}
    if not all(checks.values()):
        raise RuntimeError(f"TaskPress contract failed: {checks}")
    return {"seed": seed, "metrics": {"score_reference_error": error, "additive_negative_control_gap": additive_gap,
        "original_tokens": 11, "context_tokens": 8, "guide_tokens": 3, "retained_tokens_per_head": 4,
        "kv_heads": 2, "value_scale_reference_error": (scale - values[:, :, :8].abs().amax(-1) / 7).abs().max().item(),
        "pretrained_model_calls": 0}, "checks": checks}
