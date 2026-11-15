"""LGPO fixed-v1 sequence-likelihood gate and policy-gradient objective.

No rollout engine, reward function, advantage estimator or LLM is supplied.
The gate uses current-policy mean token log-probability, not a sequence sum,
importance ratio or a sign-dependent gate. It is detached from differentiation.
"""

from __future__ import annotations

import math

import torch

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/lgpo-a100-20261115.json"


def loss(
    log_probs: torch.Tensor,
    advantages: torch.Tensor,
    token_mask: torch.Tensor,
    *,
    threshold: float = -0.15,
) -> tuple[torch.Tensor, torch.Tensor]:
    """Negative Section 4 objective: sum tokens, then mean over all sequences.

    The all-sequence denominator includes gated sequences, rather than silently
    changing the update scale by renormalizing the survivors. Advantages are
    external, detached per-token inputs; no old-policy probabilities are needed.
    """
    if (
        not isinstance(log_probs, torch.Tensor)
        or log_probs.ndim != 2
        or not log_probs.is_floating_point()
        or min(log_probs.shape) < 1
        or not bool(torch.isfinite(log_probs).all())
        or bool((log_probs > 0).any())
    ):
        raise ValueError("finite nonpositive [sequence,token] log-probabilities required")
    if (
        not isinstance(advantages, torch.Tensor)
        or advantages.shape != log_probs.shape
        or advantages.device != log_probs.device
        or advantages.dtype != log_probs.dtype
        or not bool(torch.isfinite(advantages).all())
    ):
        raise ValueError("same-shape/device/dtype finite token advantages required")
    if (
        not isinstance(token_mask, torch.Tensor)
        or token_mask.shape != log_probs.shape
        or token_mask.dtype != torch.bool
        or token_mask.device != log_probs.device
        or not bool(token_mask.any(-1).all())
    ):
        raise ValueError("same-device Boolean mask with a valid token in every sequence required")
    if (
        isinstance(threshold, bool)
        or not isinstance(threshold, (float, int))
        or not math.isfinite(threshold)
        or threshold > 0
    ):
        raise ValueError("finite nonpositive log-likelihood threshold required")
    mean_logp = log_probs.detach().masked_fill(~token_mask, 0.0).sum(-1) / token_mask.sum(-1)
    retained = mean_logp <= threshold
    per_sequence = (log_probs * advantages.detach()).masked_fill(~token_mask, 0.0).sum(-1)
    return -(retained.to(log_probs.dtype) * per_sequence).mean(), retained


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if type(seed) is not int or device not in {"cpu", "cuda"}:
        raise ValueError("integer seed and explicit CPU/CUDA required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    logits = torch.tensor(
        [
            [[6.0, 0.0], [6.0, 0.0]],
            [[6.0, 0.0], [6.0, 0.0]],
            [[0.0, 1.0], [0.0, 1.0]],
            [[0.0, 1.0], [0.0, 1.0]],
        ],
        dtype=torch.float64,
        device=device,
    ).requires_grad_()
    mask = torch.ones((4, 2), dtype=torch.bool, device=device)
    advantage = torch.tensor(
        [[1.0, 1.0], [-1.0, -1.0], [2.0, 2.0], [-2.0, -2.0]], dtype=logits.dtype, device=device
    )
    advantage = advantage * float(1 + torch.rand((), generator=generator))
    logp = logits.log_softmax(-1)[..., 0]
    objective, retained = loss(logp, advantage, mask)
    objective.backward()
    expected = -(advantage[2:] * logp.detach()[2:]).sum() / 4
    before = logp.detach().clone()
    with torch.no_grad():
        logits -= 0.1 * logits.grad
    after = logits.log_softmax(-1)[..., 0].detach()
    checks = {
        "sequence_gate_both_advantage_signs": retained.tolist() == [False, False, True, True],
        "gated_sequences_have_zero_gradient": bool((logits.grad[:2] == 0).all()),
        "exact_all_sequence_reduction": bool(torch.allclose(objective.detach(), expected)),
        "positive_advantage_increases_selected_logp": bool((after[2] > before[2]).all()),
        "negative_advantage_decreases_selected_logp": bool((after[3] < before[3]).all()),
        "requested_device": logits.device.type == device,
    }
    return {
        "seed": seed,
        "device": device,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "checks": checks,
        "metrics": {
            "retained_sequences": int(retained.sum()),
            "gradient_norm": float(logits.grad.norm()),
            "gated_gradient_max": float(logits.grad[:2].abs().max()),
            "objective_formula_error": float((objective.detach() - expected).abs()),
            "old_policy_calls": 0,
        },
    }
