"""2604.22191 Eq.1/C.3: held-out paired sequence-logprob amplification.

No canary induction, reward model, PPO/GRPO training, semantic correctness judge
or individual-document misuse conclusion is supplied by this tensor audit.
"""
from __future__ import annotations

import torch

REQUIRES_GPU_VALIDATION = True


def assert_document_disjoint(rm_ids, rl_ids, eval_ids):
    groups = []
    for values in (rm_ids, rl_ids, eval_ids):
        values = tuple(values)
        if not values or any(not isinstance(v, str) or not v for v in values):
            raise ValueError("explicit nonempty document identities required in every partition")
        groups.append(set(values))
    if any(groups[i] & groups[j] for i, j in ((0, 1), (0, 2), (1, 2))):
        raise ValueError("RM/RL/evaluation documents must be disjoint, not merely rows")


def sequence_log_probability(logits: torch.Tensor, token_ids: torch.Tensor, mask: torch.Tensor):
    if not isinstance(logits, torch.Tensor) or logits.ndim != 3 or not logits.is_floating_point() or not torch.isfinite(logits).all():
        raise ValueError("finite [pair,canary_token,vocabulary] autoregressive logits required")
    if token_ids.shape != logits.shape[:2] or mask.shape != token_ids.shape or token_ids.dtype != torch.long or mask.dtype != torch.bool:
        raise ValueError("aligned Long token IDs and Boolean token mask required")
    if not (logits.device == token_ids.device == mask.device) or not mask.any(-1).all():
        raise ValueError("same device and nonempty target sequence per pair required")
    if (token_ids[mask] < 0).any() or (token_ids[mask] >= logits.shape[-1]).any():
        raise ValueError("active target IDs must be inside the vocabulary")
    safe_ids = token_ids.masked_fill(~mask, 0)
    token_lp = logits.log_softmax(-1).gather(-1, safe_ids[..., None]).squeeze(-1)
    return token_lp.masked_fill(~mask, 0.).sum(-1)


def amplification_score(triggered_logits, clean_logits, canary_ids, mask, *, rm_document_ids, rl_document_ids, eval_document_ids):
    assert_document_disjoint(rm_document_ids, rl_document_ids, eval_document_ids)
    if triggered_logits.shape != clean_logits.shape or triggered_logits.device != clean_logits.device or triggered_logits.dtype != clean_logits.dtype:
        raise ValueError("paired clean/triggered logits must have identical shape/device/dtype")
    if len(eval_document_ids) != triggered_logits.shape[0]:
        raise ValueError("one held-out document identity per paired example required")
    triggered = sequence_log_probability(triggered_logits, canary_ids, mask)
    clean = sequence_log_probability(clean_logits, canary_ids, mask)
    differences = triggered - clean
    return differences.mean(), differences


def policy_auroc(compliant_scores, violating_scores) -> float:
    clean = torch.as_tensor(compliant_scores, dtype=torch.float64, device="cpu")
    violation = torch.as_tensor(violating_scores, dtype=torch.float64, device="cpu")
    if clean.ndim != 1 or violation.ndim != 1 or not clean.numel() or not violation.numel() or not torch.isfinite(clean).all() or not torch.isfinite(violation).all():
        raise ValueError("finite scores from independent trained policies in both regimes required")
    return float(((violation[:, None] > clean[None, :]).double() + .5*(violation[:, None] == clean[None, :])).mean().item())


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int:
        raise ValueError("integer seed required")
    generator = torch.Generator(device="cpu").manual_seed(seed)
    clean = torch.randn(3, 4, 5, generator=generator, dtype=torch.float64).to(device)
    ids = torch.tensor([[0, 1, 2, 3]]*3, dtype=torch.long, device=device)
    mask = torch.ones(3, 4, dtype=torch.bool, device=device); mask[0, -1] = False
    triggered = clean.clone().scatter_add(-1, ids[..., None], torch.ones_like(ids[..., None], dtype=clean.dtype))
    score, differences = amplification_score(triggered, clean, ids, mask, rm_document_ids=["rm"], rl_document_ids=["rl"], eval_document_ids=["a", "b", "c"])
    reverse, _ = amplification_score(clean, triggered, ids, mask, rm_document_ids=["rm"], rl_document_ids=["rl"], eval_document_ids=["a", "b", "c"])
    zero, _ = amplification_score(clean, clean, ids, mask, rm_document_ids=["rm"], rl_document_ids=["rl"], eval_document_ids=["a", "b", "c"])
    overlap_rejected = False
    try:
        assert_document_disjoint(["a"], ["b"], ["a"])
    except ValueError:
        overlap_rejected = True
    checks = {"paired_direction_positive": bool((differences > 0).all()),
              "swap_reverses_statistic": bool(torch.allclose(score, -reverse)),
              "identical_context_is_zero": zero.item() == 0., "document_leakage_rejected": overlap_rejected,
              "tie_aware_policy_auroc": policy_auroc([0., 1.], [1., 2.]) == .875}
    return {"seed": seed, "device": str(device), "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"synthetic_amplification": float(score.item()), "zero_control_amplification": float(zero.item()),
                        "pretrained_model_calls": 0, "trained_policies": 0}, "checks": checks}
