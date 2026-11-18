"""Ambient SFT fixed-v1 Eq.4: CE + unscaled tempered forward KL.

No generation/training campaign. Frozen teacher logits share the observed prefix.
"""

import torch
from ._nov18_contracts import mask, receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def loss(student_logits, teacher_logits, labels, token_mask, *, temperature, weight):
    tensor(student_logits, "student", ndim=3)
    tensor(teacher_logits, "teacher", shape=student_logits.shape, device=student_logits.device)
    if (
        not isinstance(labels, torch.Tensor)
        or labels.dtype != torch.long
        or labels.shape != student_logits.shape[:-1]
        or labels.device != student_logits.device
    ):
        raise ValueError("same-device integer next-token labels required")
    if bool(((labels < 0) | (labels >= student_logits.shape[-1])).any()):
        raise ValueError("labels out of vocabulary")
    mask(token_mask, labels)
    t = scalar(temperature, "temperature", lower=0, strict_lower=True)
    w = scalar(weight, "weight", lower=0)
    logp = student_logits.log_softmax(-1)
    clean = -logp.gather(-1, labels.unsqueeze(-1)).squeeze(-1)
    logq = (teacher_logits.detach() / t).log_softmax(-1)
    logpt = (student_logits / t).log_softmax(-1)
    matching = (logq.exp() * (logq - logpt)).sum(-1)
    return (
        (clean + w * matching)[token_mask].mean(),
        clean[token_mask].mean(),
        matching[token_mask].mean(),
    )


def branch(clean_probability, draw):
    """The practical stochastic branch; E[L]=p_c*(CE+lambda*KL)."""
    p = scalar(clean_probability, "clean_probability", lower=0, upper=1, strict_lower=True)
    u = scalar(draw, "draw", lower=0, upper=1)
    return "clean" if u < p else "matching"


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    s = torch.randn(2, 3, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    q = torch.randn(2, 3, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    labels = torch.zeros((2, 3), dtype=torch.long, device=device)
    m = torch.tensor([[True, True, False], [True, False, False]], device=device)
    out, ce, kl = loss(s, q, labels, m, temperature=2, weight=0.4)
    out.backward()
    high, high_ce, high_kl = loss(s.detach(), q, labels, m, temperature=1e6, weight=0.4)
    return receipt(
        seed,
        "l1_mechanism",
        {
            "teacher_frozen": q.grad is None,
            "exact_unscaled_combination": bool(
                torch.allclose(out.detach(), ce.detach() + 0.4 * kl.detach())
            ),
            "masked_tokens_have_zero_gradient": bool((s.grad[~m] == 0).all()),
            "high_temperature_recovers_sft": bool(torch.allclose(high, high_ce, atol=1e-10)),
            "stochastic_branch_boundary": branch(0.75, 0.75) == "matching",
        },
        {
            "loss": out.item(),
            "temperature_matching": kl.item(),
            "high_temperature_kl": high_kl.item(),
        },
    )
