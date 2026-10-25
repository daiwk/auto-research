"""Judging with Confidence Eq.1--2 proper rewards; no autorater/GRPO claim."""
from __future__ import annotations
import math
import re
import torch
from torch import Tensor


def parse_probability(response: str) -> float | None:
    """Strict LOCAL parser for the paper's tag; author's parser is unpublished."""
    matches = re.findall(r"<prob_rb_better>\s*([^<>]+?)\s*</prob_rb_better>", response)
    if len(matches) != 1 or response.count("<prob_rb_better>") != 1:
        return None
    try:
        value = float(matches[0])
    except ValueError:
        return None
    return value if math.isfinite(value) and 0 <= value <= 1 else None


def proper_rewards(probabilities: Tensor, labels: Tensor, valid: Tensor, *,
                    epsilon: float = 1e-3) -> tuple[Tensor, Tensor]:
    """Piecewise Brier / clipped-log rewards, including unparseable penalties.

    Numeric gradients are mathematical diagnostics only: a real textual-policy
    RL trainer detaches these rewards, it cannot backprop through float parsing.
    """
    if probabilities.ndim != 1 or not probabilities.numel() or not probabilities.is_floating_point():
        raise ValueError("nonempty floating reported-probability vector required")
    if labels.shape != probabilities.shape or not labels.is_floating_point() or valid.shape != probabilities.shape or valid.dtype != torch.bool:
        raise ValueError("aligned binary labels and Boolean parser-valid mask required")
    if labels.device != probabilities.device or valid.device != probabilities.device:
        raise ValueError("reward inputs must share a device")
    if not bool(torch.isfinite(labels).all()) or not bool(((labels == 0) | (labels == 1)).all()):
        raise ValueError("finite binary preference labels required")
    if not bool(torch.isfinite(probabilities[valid]).all()) or bool(((probabilities[valid] < 0) | (probabilities[valid] > 1)).any()):
        raise ValueError("valid reported probabilities must lie in [0,1]")
    if not math.isfinite(epsilon) or not 0 < epsilon < .5:
        raise ValueError("epsilon must lie in (0,.5)")
    dtype = torch.float32 if probabilities.dtype in (torch.float16, torch.bfloat16) else probabilities.dtype
    p = torch.where(valid, probabilities.to(dtype), .5)
    y = labels.detach().to(dtype)
    brier = torch.where(valid, 1 - (p - y).square(), 0.)
    p_clip = p.clamp(epsilon, 1 - epsilon)
    log = torch.where(valid, y * p_clip.log() + (1-y) * torch.log1p(-p_clip), math.log(epsilon))
    return brier, log


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(5, device=device, dtype=torch.float64, generator=generator).requires_grad_()
    q = torch.tensor([.1,.3,.5,.7,.9], device=device, dtype=torch.float64)
    valid = torch.ones(5, device=device, dtype=torch.bool)
    ones, zeros = torch.ones_like(q), torch.zeros_like(q)
    p = logits.sigmoid()
    r1, _ = proper_rewards(p, ones, valid)
    r0, _ = proper_rewards(p, zeros, valid)
    loss = -(q * r1 + (1-q) * r0).mean()
    expected = ((p-q).square() + q*(1-q) - 1).mean()
    reference_gradient = torch.autograd.grad(expected, logits, retain_graph=True)[0]
    loss.backward()
    gradient_error = float((logits.grad - reference_gradient).abs().max())
    with torch.no_grad():
        logits -= .1 * logits.grad
    after = ((logits.sigmoid()-q).square() + q*(1-q)-1).mean()
    invalid = torch.tensor([float("nan"),0.,1.], device=device, dtype=torch.float64, requires_grad=True)
    b,l = proper_rewards(invalid, torch.tensor([1.,0.,1.],device=device), torch.tensor([False,True,True],device=device))
    (b.sum()+l.sum()).backward()
    return {"seed": seed,"diagnostic_only": True,"metrics": {
        "analytic_loss_before":float(loss.detach()),"analytic_loss_after":float(after.detach()),
        "formula_abs_error":float((loss.detach()-expected.detach()).abs()),
        "gradient_max_abs_error":gradient_error,"model_calls":0},"checks": {
        "proper_reward_matches_expected_brier":float((loss.detach()-expected.detach()).abs()) < 1e-12,
        "analytic_gradient_matches":gradient_error < 1e-12,
        "analytic_optimizer_update_decreases_loss":float(after.detach()) < float(loss.detach()),
        "unparseable_penalties_exact":float(b[0].detach()) == 0 and abs(float(l[0].detach())-math.log(.001)) < 1e-12,
        "invalid_probability_zero_gradient":float(invalid.grad[0]) == 0 and bool(invalid.grad.isfinite().all()),
        "strict_tag_parser_rejects_duplicates":parse_probability('<prob_rb_better>.4</prob_rb_better>') == .4 and parse_probability('<prob_rb_better>.4</prob_rb_better><prob_rb_better>.6</prob_rb_better>') is None,
        "overconfident_wrong_log_penalty":float(proper_rewards(torch.tensor([1.],device=device),torch.tensor([0.],device=device),torch.tensor([True],device=device))[1][0]) < -6.}}
