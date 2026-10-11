"""OPD residual/gradient/parameter/representation diagnostics (2610.11247).

Finite-minibatch proxies are not causal explanations or predicted AdamW gains.
Negative truncated residuals and nonpositive cross-fit norms stay undefined.
"""
from __future__ import annotations

import math

import torch


def topk_residual(student_logits, teacher_logits, response_mask, *, topk=16):
    if student_logits.shape != teacher_logits.shape or response_mask.shape != student_logits.shape[:-1]:
        raise ValueError("aligned vocabulary and response positions required")
    if not 0 < topk <= student_logits.shape[-1] or not bool(response_mask.any()):
        raise ValueError("valid support and nonempty response required")
    s = student_logits.float().log_softmax(-1)
    t = teacher_logits.detach().float().log_softmax(-1)
    selected, indices = s.topk(topk, -1)
    residual = (selected.softmax(-1) * (selected - t.gather(-1, indices))).sum(-1)
    return residual.masked_select(response_mask.bool()).mean()


def learning_signal_proxy(loss, pre_clip_gradient_norm):
    loss = float(loss.detach()) if isinstance(loss, torch.Tensor) else float(loss)
    norm = float(pre_clip_gradient_norm.detach()) if isinstance(pre_clip_gradient_norm, torch.Tensor) else float(pre_clip_gradient_norm)
    if not math.isfinite(loss) or not math.isfinite(norm) or norm < 0:
        raise ValueError("finite loss and nonnegative pre-clipping gradient required")
    return norm**2 / (2 * loss) if loss > 0 else None


def _dot(a, b):
    if len(a) != len(b) or any(x.shape != y.shape for x, y in zip(a, b)):
        raise ValueError("aligned parameter-gradient tensors required")
    return sum(float((x.detach().double() * y.detach().double()).sum()) for x, y in zip(a, b))


def cross_fitted_occupancy(g0, g1, h0, h1):
    norm = _dot(g0, g1)
    cross = .5 * (_dot(h0, g1) + _dot(h1, g0))
    if not math.isfinite(norm) or not math.isfinite(cross):
        raise ValueError("finite cross-fitted gradients required")
    return {"cross_gradient_squared": norm, "occupancy_cross_product": cross,
            "alpha": cross / norm if norm > 0 else None,
            "occupancy_factor": 1 + cross / norm if norm > 0 else None,
            "valid_positive_denominator": norm > 0}


def occupancy_surrogate(response_losses, response_log_likelihoods):
    """Opposite-fold per-prompt baseline; 8 rollouts = even 2x4 folds.

    Loss values are detached. Score log-likelihoods sum response tokens, not
    token means. Returned terms must differentiate on the matching fold only.
    """
    if response_losses.shape != response_log_likelihoods.shape or response_losses.ndim != 2:
        raise ValueError("aligned prompt-by-rollout losses and sequence log likelihoods required")
    rolls = response_losses.shape[1]
    if rolls < 2 or rolls % 2:
        raise ValueError("two equal independent rollout folds required")
    losses = response_losses.detach()
    split = rolls // 2
    first, second = losses[:, :split], losses[:, split:]
    h0 = ((first - second.mean(-1, keepdim=True)) * response_log_likelihoods[:, :split]).mean()
    h1 = ((second - first.mean(-1, keepdim=True)) * response_log_likelihoods[:, split:]).mean()
    return h0, h1


def parameter_displacement(before, after):
    if set(before) != set(after):
        raise ValueError("same named parameter space required, not different architectures")
    norm2, delta2, total, changed = 0., 0., 0, 0
    seen = set()
    for name, a in before.items():
        b = after[name]
        if a.shape != b.shape:
            raise ValueError("matching parameter shapes required")
        identity = (a.data_ptr(), b.data_ptr(), tuple(a.shape), a.stride(), b.stride())
        if identity in seen:
            continue
        seen.add(identity)
        x, y = a.detach().float(), b.detach().float()
        norm2 += float(x.double().square().sum())
        delta2 += float((y - x).double().square().sum())
        changed += int((x != y).sum())
        total += x.numel()
    return {"delta_l2": delta2**.5, "relative_displacement": (delta2 / norm2)**.5 if norm2 else None,
            "changed_fraction": changed / total if total else None,
            "unique_parameter_entries": total}


def mean_pool_prompt(hidden, mask):
    if hidden.shape[:-1] != mask.shape or not bool(mask.bool().any(-1).all()):
        raise ValueError(f"nonempty aligned prompt token masks required: hidden={tuple(hidden.shape)}, mask={tuple(mask.shape)}")
    return hidden.float().masked_fill(~mask.bool()[..., None], 0).sum(-2) / mask.sum(-1, keepdim=True)


def prompt_layer_features(model, inputs):
    """Embedding, intermediate decoder states, and final normalized state.

    Collect explicitly rather than trusting version-dependent hidden_states
    recorders. This follows the usual N+1 causal-LM hidden-state convention:
    the final raw decoder output is replaced by the final normalized output.
    Only the standard embed_tokens/layers/norm decoder interface is supported.
    """
    decoder = getattr(model, "model", None)
    if decoder is None or any(not hasattr(decoder, name) for name in ("embed_tokens", "layers", "norm")):
        raise ValueError("standard embedding/decoder layers/final norm required")
    if not inputs or not len(decoder.layers):
        raise ValueError("nonempty prompt bank and decoder layers required")
    modules = [decoder.embed_tokens, *decoder.layers[:-1], decoder.norm]
    captured, handles, rows = {}, [], []
    current_shape = None

    def capture(index, output):
        hidden = output[0] if isinstance(output, (tuple, list)) else output
        if not isinstance(hidden, torch.Tensor) or hidden.ndim != 3 or hidden.shape[:2] != current_shape:
            raise ValueError("every layer must expose aligned batch/token/hidden states")
        if index in captured:
            raise ValueError("each hidden-state position must execute exactly once")
        mask = torch.ones(current_shape, dtype=torch.bool, device=hidden.device)
        captured[index] = mean_pool_prompt(hidden.detach(), mask).cpu()

    try:
        for index, module in enumerate(modules):
            def hook(_, args, output, index=index):
                capture(index, output)
            handles.append(module.register_forward_hook(hook))
        for ids in inputs:
            if ids.ndim != 2 or ids.shape[0] != 1 or ids.shape[1] < 1:
                raise ValueError("one nonempty unpadded prompt per feature-bank entry required")
            current_shape = ids.shape
            captured.clear()
            with torch.no_grad():
                model(ids, use_cache=False, output_hidden_states=False)
            if set(captured) != set(range(len(modules))):
                raise ValueError("missing decoder hidden-state positions")
            rows.append(torch.stack([captured[i][0] for i in range(len(modules))]))
    finally:
        for handle in handles:
            handle.remove()
    return torch.stack(rows).transpose(0, 1)


def linear_cka(first, second):
    if first.ndim != 2 or second.ndim != 2 or first.shape[0] != second.shape[0] or len(first) < 2:
        raise ValueError("same bank of at least two mean-pooled prompts required")
    if not torch.isfinite(first).all() or not torch.isfinite(second).all():
        raise ValueError("finite representations required")
    x, y = first.double(), second.double()
    x, y = x - x.mean(0, keepdim=True), y - y.mean(0, keepdim=True)
    # Equivalent centered linear CKA using prompt Gram matrices: no dim^2 storage.
    gx, gy = x @ x.T, y @ y.T
    denominator = torch.linalg.vector_norm(gx) * torch.linalg.vector_norm(gy)
    return float((gx * gy).sum() / denominator) if float(denominator) > 0 else None
