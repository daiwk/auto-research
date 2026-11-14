"""2606.32032 Eqs.2--4: metacognitive feedback and selective advantage boost.

Intrinsic-confidence estimates and completion self-judgments remain external.
This is not an uncertainty estimator, answer verifier, GRPO trainer or rewriter.
"""
from __future__ import annotations

import math
import torch

REQUIRES_GPU_VALIDATION = True


def _unit_interval(x, *, name):
    if not isinstance(x, torch.Tensor) or not x.is_floating_point() or not torch.isfinite(x).all() or ((x < 0) | (x > 1)).any():
        raise ValueError(f"{name} must be a finite floating tensor in [0,1]")


def faithful_calibration(expressed, intrinsic, sentence_mask, *, tau: float = .1):
    _unit_interval(expressed, name="expressed confidence")
    _unit_interval(intrinsic, name="external intrinsic confidence")
    if expressed.shape != intrinsic.shape or expressed.ndim < 2 or sentence_mask.shape != expressed.shape or sentence_mask.dtype != torch.bool:
        raise ValueError("aligned completion/sentence confidence and Boolean masks required")
    if not (expressed.device == intrinsic.device == sentence_mask.device) or expressed.dtype != intrinsic.dtype or not sentence_mask.any(-1).all():
        raise ValueError("same device/dtype and nonempty sentence groups required")
    if not math.isfinite(tau) or not 0 < tau <= 1:
        raise ValueError("0 < tau <= 1 required")
    calibrated = ((expressed-intrinsic).abs() < tau) & sentence_mask
    return calibrated.sum(-1).to(expressed.dtype) / sentence_mask.sum(-1)


def metacognitive_feedback(predicted_fc, gold_fc):
    _unit_interval(predicted_fc, name="self-predicted FC")
    _unit_interval(gold_fc, name="evaluated FC")
    if predicted_fc.shape != gold_fc.shape or predicted_fc.device != gold_fc.device or predicted_fc.dtype != gold_fc.dtype:
        raise ValueError("aligned self-predicted and evaluated completion FC required")
    return 1 - (predicted_fc-gold_fc).square()


def advantages(faithfulness, other_rewards, feedback, *, k: float = 1.):
    """Last axis is one same-prompt completion group; do NOT std-normalize.

    Boost only the above-mean faithfulness component. Other rewards and
    below/equal-mean faithfulness stay unchanged, including their signs.
    """
    if not all(isinstance(x, torch.Tensor) and x.is_floating_point() and torch.isfinite(x).all() for x in (faithfulness, other_rewards, feedback)):
        raise ValueError("finite floating reward and feedback tensors required")
    if faithfulness.ndim < 1 or faithfulness.shape[-1] < 2 or any(x.shape != faithfulness.shape or x.device != faithfulness.device or x.dtype != faithfulness.dtype for x in (other_rewards, feedback)):
        raise ValueError("aligned groups of at least two completions required")
    _unit_interval(feedback, name="metacognitive feedback")
    if not math.isfinite(k) or k < 0:
        raise ValueError("finite nonnegative boost k required")
    faith_centered = faithfulness-faithfulness.mean(-1, keepdim=True)
    other_centered = other_rewards-other_rewards.mean(-1, keepdim=True)
    return other_centered + torch.where(faith_centered > 0, faith_centered*(k+feedback), faith_centered)


def select_training_tails(example_ids, self_fc_percent, count: int, *, split: str):
    """Section3.3: balanced highest/lowest self-judged training examples.

    Ties use stable ID order. The source does not define odd counts, so this
    local interface rejects them instead of silently changing the half/half rule.
    """
    ids, scores = tuple(example_ids), tuple(float(x) for x in self_fc_percent)
    if split != "train" or type(count) is not int or count <= 0 or count % 2 or count > len(ids):
        raise ValueError("training-only, positive even count within available examples required")
    if len(ids) != len(scores) or len(set(ids)) != len(ids) or any(not isinstance(i, str) or not i for i in ids) or any(not math.isfinite(x) or not 0 <= x <= 100 for x in scores):
        raise ValueError("unique example IDs and finite self-judgments on [0,100] required")
    order = sorted(range(len(ids)), key=lambda i: (scores[i], ids[i]))
    half = count//2
    return tuple(ids[i] for i in order[:half] + order[-half:])


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    f = torch.tensor([[.1, .4, .7]], dtype=torch.float64, device=device)
    o = torch.rand(1, 3, generator=generator, dtype=torch.float64).to(device)
    z = torch.tensor([[.2, .5, 1.]], dtype=torch.float64, device=device)
    actual = advantages(f, o, z)
    centered_f, centered_o = f-f.mean(-1, keepdim=True), o-o.mean(-1, keepdim=True)
    expected = centered_o + centered_f*torch.where(centered_f > 0, 1+z, torch.ones_like(z))
    c = torch.tensor([[[0., .2, .4]]], dtype=torch.float64, device=device)
    g = torch.tensor([[[.125, .2, .5]]], dtype=torch.float64, device=device)
    fc = faithful_calibration(c, g, torch.ones_like(c, dtype=torch.bool), tau=.125)
    selected = select_training_tails(["a", "b", "c", "d"], [10, 40, 70, 90], 2, split="train")
    checks = {"eq4_selective_faithfulness_boost": bool(torch.allclose(actual, expected)),
              "negative_faithfulness_not_boosted": bool(torch.allclose(actual[0, 0], (centered_o+centered_f)[0, 0])),
              "strict_tau_boundary": math.isclose(fc.item(), 2/3),
              "perfect_self_judgment_feedback_one": metacognitive_feedback(fc, fc).item() == 1.,
              "balanced_training_tail_selection": selected == ("a", "d")}
    return {"seed": seed, "device": str(device), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"advantage_formula_error": float((actual-expected).abs().max().item()),
                        "synthetic_fc": float(fc.item()), "pretrained_model_calls": 0, "training_steps": 0}, "checks": checks}
