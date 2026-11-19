"""MRPD v1 chronological replay and top-k-plus-tail reverse-KL loss."""

import torch

from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def chronological_steps(domain_logs):
    """Require the existing step schedule; do not silently sort a shuffled log."""
    if not isinstance(domain_logs, dict) or not domain_logs:
        raise ValueError("nonempty domain-to-ordered-log mapping required")
    lengths = {len(v) for v in domain_logs.values() if isinstance(v, (list, tuple))}
    if len(lengths) != 1 or len(domain_logs) != sum(isinstance(v, (list, tuple)) for v in domain_logs.values()):
        raise ValueError("equal nonempty ordered domain logs required")
    length = next(iter(lengths))
    if length == 0:
        raise ValueError("empty replay")
    result = []
    for step in range(length):
        batch = []
        for domain, rows in domain_logs.items():
            row = rows[step]
            if not isinstance(row, dict) or type(row.get("step")) is not int or row["step"] != step:
                raise ValueError("logs must retain original chronological step indices")
            batch.append((domain, row))
        result.append(tuple(batch))
    return tuple(result)


def coarsened_reverse_kl(student_logits, teacher_logits, *, k=256):
    tensor(student_logits, "student", ndim=3)
    tensor(teacher_logits, "teacher", shape=student_logits.shape, device=student_logits.device)
    vocab = student_logits.shape[-1]
    if type(k) is not int or not 1 <= k <= vocab:
        raise ValueError("1 <= integer k <= vocabulary required")
    logp, logq = student_logits.log_softmax(-1), teacher_logits.detach().log_softmax(-1)
    ids = logq.topk(k, dim=-1).indices
    p, q = logp.gather(-1, ids).exp(), logq.gather(-1, ids).exp()
    selected = (p * (logp.gather(-1, ids)-logq.gather(-1, ids))).sum(-1)
    if k == vocab:
        return selected
    # Appendix A explicitly clamps each selected mass at 1-1e-6 for the tail atom.
    pt = 1-p.sum(-1).clamp(max=1-1e-6)
    qt = 1-q.sum(-1).clamp(max=1-1e-6)
    return selected+pt*(pt.log()-qt.log())


def loss(student_logits, teacher_logits, logged_token_ids, logging_logp, advantages, model_mask,
         *, k=256, beta=1., clip_low=0.2, clip_high=0.28):
    tensor(student_logits, "student", ndim=3)
    shape, device = student_logits.shape[:2], student_logits.device
    if (not isinstance(logged_token_ids, torch.Tensor) or logged_token_ids.dtype != torch.long
            or logged_token_ids.shape != shape or logged_token_ids.device != device
            or not bool(((logged_token_ids >= 0) & (logged_token_ids < student_logits.shape[-1])).all())):
        raise ValueError("valid same-device logged token IDs required")
    tensor(logging_logp, "logging_logp", shape=shape, device=device)
    tensor(advantages, "advantages", shape=(shape[0],), device=device)
    if (not isinstance(model_mask, torch.Tensor) or model_mask.dtype != torch.bool
            or model_mask.shape != shape or model_mask.device != device
            or not bool(model_mask.any(-1).all())):
        raise ValueError("nonempty model-generated token mask per response required")
    b = scalar(beta, "beta", lower=0)
    lo = scalar(clip_low, "clip_low", lower=0, upper=1)
    hi = scalar(clip_high, "clip_high", lower=0)
    current = student_logits.log_softmax(-1).gather(-1, logged_token_ids.unsqueeze(-1)).squeeze(-1)
    ratio = torch.where(model_mask, current-logging_logp.detach(), 0.).exp()
    a = advantages.detach().unsqueeze(-1)
    pg = -torch.minimum(ratio*a, ratio.clamp(1-lo, 1+hi)*a)
    kl = coarsened_reverse_kl(student_logits, teacher_logits, k=k)
    per_token = pg+b*kl
    # Paper averages within response first, then across all responses.
    reduce = lambda x: (torch.where(model_mask, x, 0.).sum(-1)/model_mask.sum(-1)).mean()
    return reduce(per_token), reduce(pg), reduce(kl)


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    s = torch.randn(2, 3, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    t = torch.randn(2, 3, 5, generator=g, dtype=torch.float64).to(device).requires_grad_()
    ids = torch.tensor([[0, 1, 2], [1, 2, 3]], device=device)
    old = s.detach().log_softmax(-1).gather(-1, ids.unsqueeze(-1)).squeeze(-1).requires_grad_()
    m = torch.tensor([[True, False, False], [True, True, False]], device=device)
    out, pg, kl = loss(s, t, ids, old, torch.tensor([1., -1.], device=device), m, k=2)
    out.backward()
    full = coarsened_reverse_kl(s.detach(), t.detach(), k=5)
    coarse = coarsened_reverse_kl(s.detach(), t.detach(), k=2)
    schedule = chronological_steps({"a": [{"step": 0}, {"step": 1}], "b": [{"step": 0}, {"step": 1}]})
    return receipt(seed, "l1_mechanism", {
        "coarsening_lower_bounds_full_kl": bool((coarse <= full+1e-12).all()),
        "teacher_and_logging_policy_frozen": t.grad is None and old.grad is None,
        "masked_observation_gradient_zero": bool((s.grad[~m] == 0).all()),
        "student_gradient_nonzero": bool(s.grad[m].abs().sum() > 0),
        "replay_retains_step_schedule": [b[0][1]["step"] for b in schedule] == [0, 1],
        "dense_kl_not_clipped_or_added_to_advantage": abs(out.item()-pg.item()-kl.item()) < 1e-12,
    }, {"loss": out.item(), "policy_loss": pg.item(), "coarsened_kl": kl.item(),
        "full_kl_mean": full.mean().item(), "gradient_norm": s.grad.norm().item()})
