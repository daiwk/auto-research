"""NarrowSpec linear boundary folds, not a trained narrow speculative decoder.

Weights use PyTorch Linear convention [out,in]. No nonlinearity, normalization
or pre-quantized weight may be moved across these folds.
"""

import torch

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/narrow-spec-a100-20261119-latest.json"


def _pair(left, right):
    if (
        not isinstance(left, torch.Tensor)
        or not isinstance(right, torch.Tensor)
        or left.ndim != 2
        or right.ndim != 2
        or not left.is_floating_point()
        or not right.is_floating_point()
        or left.dtype != right.dtype
        or left.device != right.device
        or not left.numel()
        or not right.numel()
        or not torch.isfinite(left).all()
        or not torch.isfinite(right).all()
    ):
        raise ValueError("finite compatible 2D floating weights required")


def fold_output_head(target_head, output_adapter):
    """[V,d_target] @ [d_target,d_draft] -> [V,d_draft]."""
    _pair(target_head, output_adapter)
    if target_head.shape[1] != output_adapter.shape[0]:
        raise ValueError("output adapter must map draft width to target width")
    return target_head @ output_adapter


def fold_input_embedding(target_embedding, input_adapter):
    """[V,d_target] @ [d_draft,d_target].T -> [V,d_draft]."""
    _pair(target_embedding, input_adapter)
    if target_embedding.shape[1] != input_adapter.shape[1]:
        raise ValueError("input adapter must map target width to draft width")
    return target_embedding @ input_adapter.T


def diagnostic(seed, device="cpu"):
    if type(seed) is not int or seed < 0:
        raise ValueError("nonnegative integer seed required")
    g = torch.Generator(device=device).manual_seed(seed)
    options = {"generator": g, "device": device, "dtype": torch.float64}
    head, up, x = (
        torch.randn(17, 8, **options),
        torch.randn(8, 3, **options),
        torch.randn(6, 3, **options),
    )
    x.requires_grad_()
    unfolded = (x @ up.T) @ head.T
    folded = x @ fold_output_head(head, up).T
    expected_grad = torch.autograd.grad(unfolded.square().sum(), x, retain_graph=True)[0]
    actual_grad = torch.autograd.grad(folded.square().sum(), x)[0]
    embedding, down = torch.randn(17, 8, **options), torch.randn(3, 8, **options)
    ids = torch.tensor([1, 4, 4, 16], device=device)
    in_error = (
        (embedding[ids] @ down.T - fold_input_embedding(embedding, down)[ids]).abs().max().item()
    )
    # Deliberately quantized negative control: folding and quantization do not commute.
    quantize = lambda w: torch.round(w * 4) / 4
    quantization_difference = (quantize(head @ up) - quantize(head) @ up).abs().max().item()
    error = (folded - unfolded).abs().max().item()
    return {
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": {
            "output_fold_parity": error < 1e-10,
            "input_fold_parity": in_error < 1e-12,
            "hidden_gradient_parity": bool(torch.allclose(expected_grad, actual_grad, atol=1e-10)),
            "quantization_does_not_commute": quantization_difference > 1e-3,
            "narrow_head_shape": tuple(fold_output_head(head, up).shape) == (17, 3),
        },
        "metrics": {
            "output_fold_max_abs_error": error,
            "input_fold_max_abs_error": in_error,
            "quantized_order_max_difference": quantization_difference,
        },
    }
