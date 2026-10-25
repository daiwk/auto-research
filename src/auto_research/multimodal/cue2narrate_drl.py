"""Cue2Narrate Eqs.5--8: current-policy caption/AD likelihood ranking.

Only the masked Stage-2 loss, not the dual-head localizer, negative-caption
generation, VLM, LongLSMDC data or video benchmark. Independent paper rewrite.
"""
import math

import torch
from torch import Tensor
from torch.nn import functional as F

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/cue2narrate-drl-a100-20261025.json"


def _logps(logits: Tensor, labels: Tensor) -> tuple[Tensor, Tensor]:
    if (logits.ndim != 3 or min(logits.shape) < 1 or not logits.is_floating_point()
            or logits.numel() > 1_048_576 or not bool(torch.isfinite(logits).all())):
        raise ValueError("bounded finite floating [batch,tokens,vocab] logits required")
    if labels.shape != logits.shape[:2] or labels.device != logits.device or labels.dtype != torch.long:
        raise ValueError("aligned int64 labels on logits device required; -100 excludes prompt/padding")
    valid = labels != -100
    if bool((valid.sum(-1) == 0).any()) or bool(((labels[valid] < 0) | (labels[valid] >= logits.shape[-1])).any()):
        raise ValueError("each sequence must have a nonempty valid AD/caption target")
    work = logits.float() if logits.dtype in (torch.float16, torch.bfloat16) else logits
    return work.log_softmax(-1).gather(-1, labels.masked_fill(~valid, 0)[..., None]).squeeze(-1) * valid, valid


def description_ranking_loss(positive_logits: Tensor, positive_labels: Tensor,
                             negative_logits: Tensor, negative_labels: Tensor, *,
                             temperature: float = .5, ranking_weight: float = .2) -> dict[str, Tensor]:
    """SFT sums target tokens per sample; DRL uses LENGTH-MEAN log probabilities.

    Both positive/negative logits belong to the CURRENT trained model, under the
    same prompt and visual cue. Only negative text generation is frozen/offline;
    detaching its current-policy likelihood would change Eq.7's gradient.
    Caller aligns teacher-forced logits/labels and masks prompt tokens with -100.
    """
    if (not math.isfinite(temperature) or temperature <= 0
            or not math.isfinite(ranking_weight) or ranking_weight < 0):
        raise ValueError("positive finite temperature/nonnegative finite weight required")
    if (positive_logits.shape[0] != negative_logits.shape[0]
            or positive_logits.shape[-1] != negative_logits.shape[-1]
            or positive_logits.device != negative_logits.device or positive_logits.dtype != negative_logits.dtype):
        raise ValueError("positive and negative require shared batch/vocabulary/dtype/device")
    lp, mp = _logps(positive_logits, positive_labels)
    ln, mn = _logps(negative_logits, negative_labels)
    positive = lp.sum(-1) / mp.sum(-1)
    negative = ln.sum(-1) / mn.sum(-1)
    sft = -lp.sum(-1).mean()
    ranking = F.softplus(-(positive - negative) / temperature).mean()
    loss = sft + ranking_weight * ranking
    if not all(bool(torch.isfinite(value)) for value in (sft, ranking, loss)):
        raise ValueError("nonfinite Stage-2 loss; no silent clipping")
    return {"loss": loss, "sft": sft, "ranking": ranking,
            "positive_score": positive, "negative_score": negative}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    generator = torch.Generator(device=device).manual_seed(seed)
    positive = torch.randn(3, 5, 7, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    negative = torch.randn(3, 8, 7, generator=generator, device=device, dtype=torch.float64).requires_grad_()
    yp = torch.tensor([[1, 2, 3, -100, -100]] * 3, device=device)
    yn = torch.tensor([[1, 2, 3, 4, 5, 6, -100, -100]] * 3, device=device)
    before = description_ranking_loss(positive, yp, negative, yn)
    plp, nlp = positive.log_softmax(-1), negative.log_softmax(-1)
    p = torch.stack([plp[i, torch.arange(3, device=device), yp[i, :3]].mean() for i in range(3)])
    n = torch.stack([nlp[i, torch.arange(6, device=device), yn[i, :6]].mean() for i in range(3)])
    oracle = -3 * p.mean() - .2 * F.logsigmoid((p - n) / .5).mean()
    reference_error = float((before["loss"] - oracle).detach().abs())
    expected = torch.autograd.grad(oracle, (positive, negative), retain_graph=True)
    actual = torch.autograd.grad(before["loss"], (positive, negative), retain_graph=True)
    gradient_error = max(float((a - b).abs().max()) for a, b in zip(actual, expected))
    optimizer = torch.optim.SGD((positive, negative), lr=.05)
    optimizer.zero_grad()
    before["loss"].backward()
    optimizer.step()
    after = description_ranking_loss(positive, yp, negative, yn)
    checks = {"equations5_8_reference": reference_error < 1e-12,
              "both_current_policy_gradients_match": gradient_error < 1e-12 and actual[1].norm().item() > 0,
              "prompt_padding_zero_gradient": bool((actual[0][yp == -100] == 0).all()) and bool((actual[1][yn == -100] == 0).all()),
              "real_optimizer_step_decreases_fixture": after["loss"].item() < before["loss"].item()}
    if not all(checks.values()):
        raise RuntimeError(f"Cue2Narrate DRL contract failed: {checks}")
    return {"seed": seed, "metrics": {"formula_error": reference_error, "gradient_error": gradient_error,
        "negative_gradient_norm": actual[1].norm().item(), "fixture_loss_before": before["loss"].item(),
        "fixture_loss_after": after["loss"].item(), "positive_tokens": 9, "negative_tokens": 18,
        "optimizer_steps": 1, "pretrained_model_calls": 0}, "checks": checks}
