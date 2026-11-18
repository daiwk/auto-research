"""LEAF-OPD v1 teacher assessment and separated distillation operators."""

import torch
from ._nov18_contracts import mask, receipt, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def supervision_signals(context_logp, bare_logp, token_mask):
    tensor(context_logp, "context", ndim=2)
    tensor(bare_logp, "bare", shape=context_logp.shape, device=context_logp.device)
    mask(token_mask, context_logp)
    if not bool(token_mask.any(-1).all()):
        raise ValueError("every trajectory requires a supervised token")
    full, tail = [], []
    for c, b, m in zip(context_logp, bare_logp, token_mask):
        delta = (c - b)[m]
        full.append(-delta.mean())
        tail.append(-delta[len(delta) // 2 :].mean())
    return torch.stack(full), torch.stack(tail)


def teacher_is_good(ss1, ss_half):
    tensor(ss1, "ss1", ndim=1)
    tensor(ss_half, "ss_half", shape=ss1.shape, device=ss1.device)
    return bool(ss1.mean() > 1 and ss_half.mean() > 1)


def contexts(prompt, privileged_context, *, forget):
    """No target answer is accepted; privileged instruction is teacher-only."""
    if type(forget) is not bool or not isinstance(prompt, str) or not prompt:
        raise ValueError("prompt and Boolean forget flag required")
    if not isinstance(privileged_context, str) or (forget and not privileged_context):
        raise ValueError("forget teacher requires an explicit privileged instruction")
    return {
        "student": prompt,
        "teacher": (privileged_context + "\n" + prompt) if forget else prompt,
    }


def distillation_loss(student_logits, teacher_logits, token_mask):
    tensor(student_logits, "student", ndim=3)
    tensor(teacher_logits, "teacher", shape=student_logits.shape, device=student_logits.device)
    mask(token_mask, student_logits[..., 0])
    if not bool(token_mask.any(-1).all()):
        raise ValueError("empty per-trajectory supervision")
    logq = teacher_logits.detach().log_softmax(-1)
    per_token = (logq.exp() * (logq - student_logits.log_softmax(-1))).sum(-1)
    return ((per_token * token_mask).sum(-1) / token_mask.sum(-1)).mean()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    c = torch.tensor([[-3.0, -3.0, -3.0, -3.0], [-5.0, -1.0, -1.0, -1.0]], device=device)
    b = torch.full_like(c, -1.0)
    m = torch.ones_like(c, dtype=torch.bool)
    full, half = supervision_signals(c, b, m)
    s = torch.randn(2, 4, 3, generator=g, dtype=torch.float64).to(device).requires_grad_()
    t = torch.randn(2, 4, 3, generator=g, dtype=torch.float64).to(device).requires_grad_()
    out = distillation_loss(s, t, m)
    out.backward()
    ctx = contexts("question", "do not disclose", forget=True)
    return receipt(
        seed,
        "l1_mechanism",
        {
            "persistent_teacher_passes": teacher_is_good(full[:1], half[:1]),
            "front_loaded_teacher_rejected": not teacher_is_good(full[1:], half[1:]),
            "student_never_gets_privileged_context": ctx["student"] == "question"
            and "do not disclose" not in ctx["student"],
            "retain_teacher_is_bare": contexts("question", "unused", forget=False)["teacher"]
            == "question",
            "teacher_frozen_and_student_updates": t.grad is None and bool(s.grad.abs().sum() > 0),
        },
        {"loss": out.item(), "persistent_ss_half": half[0].item(), "weak_ss_half": half[1].item()},
    )
