"""MICE paper-v1 instance-aware joint-attention operator (arXiv:2606.31278).

This is an independent, checkpoint-free implementation of Sec. 3.2. It follows
the paper's block rules, NOT every default of the authors' later FLUX processor
at 43b289de84dfd184c0ee1b551b0e1bea02f6e92d. Torch is imported only on execution.
No image generator, pretrained feature, editing benchmark or Evolve promotion
is supplied. Inputs are already on a common latent raster with disjoint masks;
overlapping-instance token ownership is outside this bounded operator contract.
"""
from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from torch import Tensor


PAPER_ID = "2606.31278v1"
UPSTREAM_REVISION = "43b289de84dfd184c0ee1b551b0e1bea02f6e92d"


def _masks(value: Tensor) -> Tensor:
    import torch

    if value.ndim != 3 or min(value.shape) < 1:
        raise ValueError("masks must be nonempty (instances, height, width)")
    if not bool(torch.isfinite(value).all()) or not bool(((value == 0) | (value == 1)).all()):
        raise ValueError("instance masks must be finite and binary")
    masks = value.detach().bool()
    if bool((masks.sum(dim=0) > 1).any()):
        raise ValueError("overlapping instance ownership is outside this operator contract")
    if not bool(masks.flatten(1).any(dim=1).all()):
        raise ValueError("each instance must have at least one raster token")
    return masks


def instance_aware_masks(masks: Tensor, *, kernel_size: int = 3) -> Tensor:
    """Gaussian smoothing followed by zeroing pixels owned by other instances.

    Masks are already downsampled binary latent-raster masks. Kernel sigma uses
    the fixed author's code rule; sum-normalized convolution uses zero padding.
    The original mask values are not replaced by one here: strict intra-instance
    zero bias is applied separately by :func:`instance_log_bias`.
    """
    import torch
    from torch.nn import functional as F

    hard = _masks(masks)
    if isinstance(kernel_size, bool) or not isinstance(kernel_size, int) or kernel_size < 1 or kernel_size % 2 != 1:
        raise ValueError("kernel_size must be a positive odd integer")
    dtype = torch.float64 if masks.dtype == torch.float64 else torch.float32
    sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8
    axis = torch.arange(kernel_size, dtype=dtype, device=masks.device) - (kernel_size - 1) / 2
    kernel = torch.exp(-(axis[:, None].square() + axis[None, :].square()) / (2 * sigma**2))
    kernel = (kernel / kernel.sum())[None, None]
    smoothed = F.conv2d(hard.to(dtype)[:, None], kernel, padding=kernel_size // 2)[:, 0]
    occupied_elsewhere = hard.any(dim=0)[None] & ~hard
    return smoothed.clamp(0, 1).masked_fill(occupied_elsewhere, 0)


def instance_log_bias(masks: Tensor, *, kernel_size: int = 3,
                      temperature: float = 8.0, epsilon: float = 1e-30) -> Tensor:
    """Sec. 3.2: log(s_n + epsilon)/tau outside n, exactly zero inside n.

    The paper epsilon is kept representable by doing this operation in at least
    float32. Zeroed other-instance pixels therefore receive a finite log(eps)
    penalty, as in the paper equation; unrelated *text* groups are hard-blocked
    separately. It is not silently replaced by the upstream code's -inf rule.
    """
    import torch

    if not math.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be finite and positive")
    if not math.isfinite(epsilon) or not 0 < epsilon < 1:
        raise ValueError("epsilon must be finite and in (0, 1)")
    hard = _masks(masks)
    smoothed = instance_aware_masks(masks, kernel_size=kernel_size)
    # Reject epsilons that would underflow in the chosen statistics precision.
    if epsilon < torch.finfo(smoothed.dtype).tiny:
        raise ValueError("epsilon is not representable in the statistics dtype")
    bias = (smoothed + epsilon).log().div(temperature).clamp_max(0)
    return bias.masked_fill(hard, 0)


def mice_joint_bias(masks: Tensor, prompt_groups: Tensor, *, kernel_size: int = 3,
                    temperature: float = 8.0, epsilon: float = 1e-30) -> Tensor:
    """Construct paper-v1 B for [prompt, latent raster, context raster].

    ``prompt_groups`` contains 0 for global text and 1..N for each local text
    group. Every local group must occur; a global prompt is optional. Latent and
    context rasters have identical H*W positions. Context-to-visual rows remain
    unbiased (paper Case 5), so this matrix is deliberately not symmetric.
    """
    import torch

    hard = _masks(masks)
    n, height, width = hard.shape
    if (prompt_groups.ndim != 1 or prompt_groups.numel() < 1
            or prompt_groups.dtype not in (torch.int8, torch.int16, torch.int32, torch.int64, torch.uint8)
            or prompt_groups.device != masks.device):
        raise ValueError("prompt_groups must be nonempty integer vector on the masks device")
    if bool(((prompt_groups < 0) | (prompt_groups > n)).any()):
        raise ValueError("prompt groups must be 0 (global) or 1..number of instances")
    if any(not bool((prompt_groups == index).any()) for index in range(1, n + 1)):
        raise ValueError("each instance must have a corresponding local text group")
    spatial = instance_log_bias(masks, kernel_size=kernel_size,
                                temperature=temperature, epsilon=epsilon).flatten(1)
    prompt_count, area = prompt_groups.numel(), height * width
    length = prompt_count + 2 * area
    bias = torch.full((length, length), -torch.inf, dtype=spatial.dtype, device=masks.device)
    latent = torch.arange(prompt_count, prompt_count + area, device=masks.device)
    context = latent + area
    visual = torch.cat((latent, context))
    global_text = torch.where(prompt_groups == 0)[0]
    background = ~hard.flatten(1).any(dim=0)

    # Case 1: text self-attention is confined to the identical prompt group.
    bias[:prompt_count, :prompt_count] = torch.where(
        prompt_groups[:, None] == prompt_groups[None, :], 0.0, -torch.inf)
    # Cases 2/3: global text and unedited latent background preserve coherence.
    bias[global_text[:, None], visual] = 0
    bias[latent[background, None], visual] = 0
    bias[latent[background, None], global_text] = 0
    bias[context[:, None], global_text] = 0
    # Case 5: ALL context queries see the whole visual domain without bias.
    bias[context[:, None], visual] = 0

    for index in range(n):
        local_text = torch.where(prompt_groups == index + 1)[0]
        owned = hard[index].flatten()
        # Case 4: reference context sees only its matching local instruction.
        bias[context[owned, None], local_text] = 0
        # Case 6: local prompt / edited latent -> noisy and context image.
        rows = torch.cat((local_text, latent[owned]))
        visual_penalty = spatial[index].repeat(2)
        bias[rows[:, None], visual] = visual_penalty[None]
        # Case 7: each latent query -> local prompt uses its own raster bias.
        bias[latent[:, None], local_text] = spatial[index, :, None]
    return bias


def mice_joint_attention(query: Tensor, key: Tensor, value: Tensor, bias: Tensor,
                         *, return_weights: bool = False):
    """Actual joint softmax attention with differentiable Q/K/V, no dropout.

    Q/K/V use (..., tokens, head_dim), and B is the shared (tokens, tokens)
    matrix. This is a mathematical attention operator, not a FLUX adapter.
    """
    import torch

    if (query.ndim < 2 or query.shape != key.shape or query.shape != value.shape
            or min(query.shape) < 1):
        raise ValueError("Q/K/V must have equal nonempty (..., tokens, head_dim) shapes")
    if not all(x.is_floating_point() and bool(torch.isfinite(x).all()) for x in (query, key, value)):
        raise ValueError("Q/K/V must be finite floating tensors")
    if query.device != key.device or query.device != value.device or query.device != bias.device:
        raise ValueError("Q/K/V and bias must share one device")
    tokens = query.shape[-2]
    if bias.shape != (tokens, tokens) or not bias.is_floating_point():
        raise ValueError("bias must be a floating square matrix matching the token count")
    if bool((torch.isnan(bias) | torch.isposinf(bias) | (bias > 0)).any()):
        raise ValueError("bias may contain nonpositive values or -inf, not NaN or +inf")
    if not bool(torch.isfinite(bias).any(dim=-1).all()):
        raise ValueError("every attention row must contain at least one legal key")
    dtype = torch.float64 if any(x.dtype == torch.float64 for x in (query, key, value, bias)) else torch.float32
    logits = query.to(dtype) @ key.to(dtype).transpose(-2, -1) / math.sqrt(query.shape[-1])
    weights = torch.softmax(logits + bias.to(dtype), dim=-1)
    output = (weights @ value.to(dtype)).to(query.dtype)
    return (output, weights) if return_weights else output


def run_mice_diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Small deterministic mechanism run, usable unchanged on CPU or A100/A30.

    No dataset/model download or pretrained call. Returned scores describe only
    the generated Q/K/V operator, never image quality or paper benchmark gains.
    The root runner records command/source/commit and curates device evidence.
    """
    import torch

    selected = torch.device(device)
    if selected.type == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable; no CPU fallback")
    generator = torch.Generator(device=selected).manual_seed(seed)
    masks = torch.zeros(2, 6, 8, dtype=torch.bool, device=selected)
    masks[0, 1:3, 1:3] = True
    masks[1, 2:5, 3:5] = True
    groups = torch.tensor([0, 1, 1, 2, 2], device=selected)
    bias = mice_joint_bias(masks, groups)
    q, k, v = [torch.randn(2, bias.shape[0], 8, generator=generator, device=selected,
                          requires_grad=True) for _ in range(3)]
    output, weights = mice_joint_attention(q, k, v, bias, return_weights=True)
    formula = (torch.softmax(q.float() @ k.float().transpose(-1, -2) / math.sqrt(8)
                             + bias, dim=-1) @ v.float())
    no_mask = mice_joint_attention(q, k, v, torch.zeros_like(bias))
    no_log_bias = mice_joint_attention(q, k, v, bias.masked_fill(torch.isfinite(bias), 0))
    no_mask_delta = float((no_mask-output).square().mean().detach())
    no_log_delta = float((no_log_bias-output).square().mean().detach())
    loss = output.square().mean()
    loss.backward()
    gradients_finite = all(bool(torch.isfinite(x.grad).all()) for x in (q, k, v))
    if not gradients_finite or not bool(torch.isfinite(output).all()):
        raise RuntimeError("MICE diagnostic produced nonfinite output or gradients")
    text_cross = groups[:, None] != groups[None, :]
    cross_max = weights[:, :groups.numel(), :groups.numel()][:, text_cross].max()
    return {
        "paper": PAPER_ID, "seed": seed, "device": selected.type,
        "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
        "promotion_eligible": False, "evolve_integrated": False,
        "full_experiment_status": "not_reproduced_high_cost",
        "pretrained_model_calls": 0, "dataset": "generated-disjoint-mask-qkv-mini-suite",
        "recipe": {"instances": 2, "raster": [6, 8], "heads": 2, "head_dim": 8,
                   "kernel_size": 3, "temperature": 8.0, "epsilon": 1e-30,
                   "implementation_policy": "paper_v1", "upstream_revision": UPSTREAM_REVISION},
        "checks": {"independent_formula_match": bool(torch.allclose(output.float(), formula)),
                   "finite_output_and_gradients": gradients_finite,
                   "cross_prompt_hard_binding": float(cross_max.detach()) == 0,
                   "remove_mask_changes_output": no_mask_delta > 0,
                   "remove_log_bias_changes_output": no_log_delta > 0},
        "metrics": {"output_mean_square": float(loss.detach()),
                    "cross_prompt_probability_max": float(cross_max.detach()),
                    "removed_mask_mean_square_delta": no_mask_delta,
                    "removed_log_bias_mean_square_delta": no_log_delta,
                    "q_gradient_norm": float(q.grad.norm()),
                    "k_gradient_norm": float(k.grad.norm()),
                    "v_gradient_norm": float(v.grad.norm()),
                    "finite_output_and_gradients": float(gradients_finite),
                    "tokens": float(bias.shape[0])},
    }


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Unified bounded runner API; see :func:`run_mice_diagnostic`."""
    return run_mice_diagnostic(seed, device)
