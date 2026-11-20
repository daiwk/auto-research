"""VisAlloc v1 weighting and positive-teacher JSD, on explicit tensor inputs.

No VLM, crop pipeline, teacher generator, dataset or trainer is substituted.
"""

from collections import Counter

import torch

from ._nov18_contracts import receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def _working(value):
    """Upstream computes gating/JSD statistics in fp32, retaining fp64 inputs.

    Promote BEFORE log_softmax or subtraction: finite fp16 logits can have an
    unrepresentable half-precision log-probability gap (e.g. +60000/-60000).
    The cast remains differentiable back to the original student tensor.
    """
    return value.float() if value.dtype in {torch.float16, torch.bfloat16} else value


def _mask(value, shape, device):
    if (not isinstance(value, torch.Tensor) or value.dtype != torch.bool
            or value.shape != shape or value.device != device):
        raise ValueError("same-shape/device Boolean mask required")


def _ids(value, shape, vocab, device):
    if (not isinstance(value, torch.Tensor) or value.dtype != torch.long
            or value.shape != shape or value.device != device
            or not bool(((value >= 0) & (value < vocab)).all())):
        raise ValueError("valid same-device token IDs required")


def sample_filter(annotation_ok, positive_correct, negative_correct):
    if not isinstance(annotation_ok, torch.Tensor) or annotation_ok.ndim != 1:
        raise ValueError("training-only sample verdict vectors required")
    for x in (annotation_ok, positive_correct, negative_correct):
        _mask(x, annotation_ok.shape, annotation_ok.device)
    return annotation_ok & positive_correct & ~negative_correct


def _jsd(logp, logq):
    mix = torch.logaddexp(logp, logq)-torch.log(logp.new_tensor(2.))
    return .5*((logp.exp()*(logp-mix)).sum(-1)+(logq.exp()*(logq-mix)).sum(-1))


def _tail(log_probs):
    # Matches fixed upstream _add_tail_bucket: stable residual, no top-k renormalization.
    mass = torch.logsumexp(log_probs, -1, keepdim=True).clamp(max=-1e-7)
    return torch.cat([log_probs, torch.log(-torch.expm1(mass))], -1)


def coarsened_jsd(student_logits, positive_logits, negative_logits, *, k=100):
    tensor(student_logits, "student", ndim=3)
    for name, x in [("positive", positive_logits), ("negative", negative_logits)]:
        tensor(x, name, shape=student_logits.shape, device=student_logits.device)
    if type(k) is not int or not 1 <= k < student_logits.shape[-1]:
        raise ValueError("integer 1 <= k < vocabulary required for top-k plus tail")
    p = _working(student_logits).log_softmax(-1)
    q = _working(positive_logits.detach()).log_softmax(-1)
    n = _working(negative_logits.detach()).log_softmax(-1)
    support = p.detach().topk(k, dim=-1).indices
    pc, qc, nc = [_tail(x.gather(-1, support)) for x in [p, q, n]]
    return _jsd(pc, qc), _jsd(qc, nc), p, q, n


def frozen_priors(token_ids, student_logp, positive_logp, negative_logp, valid_mask,
                  *, vocab_size, group_size=16):
    """Training-side dual-signal prior and once-per-response template frequency."""
    tensor(student_logp, "student_logp", ndim=2)
    shape, device = student_logp.shape, student_logp.device
    for name, x in [("positive_logp", positive_logp), ("negative_logp", negative_logp)]:
        tensor(x, name, shape=shape, device=device)
    if type(vocab_size) is not int or vocab_size < 1 or type(group_size) is not int or group_size < 1:
        raise ValueError("positive integer vocabulary and prior response-group size required")
    _ids(token_ids, shape, vocab_size, device)
    _mask(valid_mask, shape, device)
    student_logp, positive_logp, negative_logp = [
        _working(x) for x in [student_logp, positive_logp, negative_logp]
    ]
    selected = torch.zeros_like(valid_mask)
    with torch.no_grad():
        d, err = (positive_logp-negative_logp).abs(), (student_logp-positive_logp).abs()
        for first in range(0, shape[0], group_size):
            sl = slice(first, first+group_size)
            m = valid_mask[sl]
            if not bool(m.any()):
                continue
            td, te = [x[sl][m].quantile(.9).clamp(min=.25) for x in [d, err]]
            dual = d[sl]/(d[sl]+td)*err[sl]/(err[sl]+te)
            selected[sl] = m & (dual > dual[m].quantile(.9))
        counts = torch.bincount(token_ids[valid_mask], minlength=vocab_size).to(student_logp.dtype)
        chosen = torch.bincount(token_ids[selected], minlength=vocab_size).to(student_logp.dtype)
        rates = ((chosen+5)/(counts+50)*10000).round()/10000
        pair_counts = Counter()
        for ids, m in zip(token_ids.tolist(), valid_mask.tolist(), strict=True):
            pairs = {(ids[t-1], ids[t]) for t in range(1, len(ids)) if m[t-1] and m[t]}
            pair_counts.update(pairs)
        templates = frozenset(pair for pair, count in pair_counts.items() if count >= .25*shape[0])
    return rates, counts, templates


def redistribute_bonus(bonus, counts, token_ids, valid_mask):
    """Eq.13 preserves even tiny positive budgets; only the bonus is moved."""
    tensor(bonus, "bonus", ndim=2)
    tensor(counts, "counts", ndim=1, device=bonus.device)
    _ids(token_ids, bonus.shape, len(counts), bonus.device)
    _mask(valid_mask, bonus.shape, bonus.device)
    if bool((bonus < 0).any()) or bool((counts < 0).any()):
        raise ValueError("nonnegative bonus and frozen counts required")
    bonus, counts = _working(bonus), _working(counts)
    b = torch.where(valid_mask, bonus, 0.)
    total = b.sum()
    if total.item() == 0:
        return torch.zeros_like(b)
    weighted = b*torch.rsqrt(counts.detach()[token_ids]+50)
    return weighted*(total/weighted.sum())


def allocation(token_ids, student_logp, positive_logp, negative_logp,
               student_positive_jsd, teacher_jsd, valid_mask, rates, counts,
               template_pairs=frozenset(), *, strength=4.):
    """Default paper coefficients: dd-only base, OR bonus and frozen gates."""
    tensor(student_logp, "student_logp", ndim=2)
    shape, device = student_logp.shape, student_logp.device
    for name, x in [("positive_logp", positive_logp), ("negative_logp", negative_logp),
                    ("student_positive_jsd", student_positive_jsd), ("teacher_jsd", teacher_jsd)]:
        tensor(x, name, shape=shape, device=device)
    for name, x in [("rates", rates), ("counts", counts)]:
        tensor(x, name, ndim=1, device=device)
    if rates.shape != counts.shape or bool(((rates < 0) | (rates > 1)).any()) or bool((counts < 0).any()):
        raise ValueError("aligned probability rates and nonnegative frozen counts required")
    _ids(token_ids, shape, len(rates), device)
    _mask(valid_mask, shape, device)
    lam = scalar(strength, "strength", lower=0)
    if any(not isinstance(pair, tuple) or len(pair) != 2
           or any(type(x) is not int or not 0 <= x < len(rates) for x in pair) for pair in template_pairs):
        raise ValueError("valid frozen template bigrams required")
    student_logp, positive_logp, negative_logp, student_positive_jsd, teacher_jsd = [
        _working(x) for x in [student_logp, positive_logp, negative_logp,
                             student_positive_jsd, teacher_jsd]
    ]
    rates, counts = _working(rates), _working(counts)
    with torch.no_grad():
        if not bool(valid_mask.any()):
            zero = torch.zeros_like(student_logp)
            return torch.ones_like(zero), {"base": torch.ones_like(zero), "bonus": zero,
                                           "redistributed_bonus": zero, "eligible": valid_mask}
        d = (positive_logp-negative_logp).abs()
        tau = d[valid_mask].quantile(.9).clamp(min=.25)
        s = d/(d+tau)
        theta_d = s[valid_mask].quantile(.8)
        theta_j = student_positive_jsd[valid_mask].quantile(.5)
        theta_h = teacher_jsd[valid_mask].quantile(.9).clamp(min=1e-6)
        u = teacher_jsd/(teacher_jsd+theta_h)
        context_ok = torch.ones_like(valid_mask)
        for row, (ids, m) in enumerate(zip(token_ids.tolist(), valid_mask.tolist(), strict=True)):
            for t in range(1, shape[1]):
                if m[t-1] and m[t] and (ids[t-1], ids[t]) in template_pairs:
                    context_ok[row, t] = False
        shared = valid_mask & (rates.detach()[token_ids] >= .12) & context_ok & (student_positive_jsd > theta_j)
        a, b = shared & (s > theta_d), shared & (teacher_jsd > theta_h)
        bonus = lam*torch.maximum((s-theta_d).clamp(min=0), (u-.5).clamp(min=0)*b)*(a | b)
        ext = redistribute_bonus(bonus, counts, token_ids, valid_mask)
        base = 1+s
        raw = base+ext
        weights = torch.where(valid_mask, raw*(valid_mask.sum()/raw[valid_mask].sum()), 1.)
        return weights, {"base": base, "bonus": bonus, "redistributed_bonus": ext,
                         "eligible": a | b, "tau": tau, "theta_s": theta_d,
                         "theta_j": theta_j, "theta_h": theta_h}


def loss(student_logits, positive_logits, negative_logits, token_ids, old_logp,
         response_mask, negative_available, rates, counts, template_pairs=frozenset(),
         *, k=100, strength=4., rollout_correction=None):
    j, h, p, q, n = coarsened_jsd(student_logits, positive_logits, negative_logits, k=k)
    shape, device = p.shape[:2], p.device
    _ids(token_ids, shape, p.shape[-1], device)
    _mask(response_mask, shape, device)
    _mask(negative_available, (shape[0],), device)
    if not bool(response_mask.any()):
        raise ValueError("nonempty response supervision required")
    tensor(old_logp, "old_logp", shape=shape, device=device)
    realized = [x.gather(-1, token_ids[..., None]).squeeze(-1) for x in [p, q, n]]
    valid = response_mask & negative_available[:, None]
    weights, info = allocation(token_ids, *realized, j.detach(), h.detach(), valid,
                               rates, counts, template_pairs, strength=strength)
    correction = torch.ones_like(j) if rollout_correction is None else rollout_correction
    tensor(correction, "rollout_correction", shape=shape, device=device)
    if bool((correction < 0).any()):
        raise ValueError("nonnegative rollout correction required")
    ratio = torch.where(response_mask, realized[0]-_working(old_logp.detach()), 0.).exp().clamp(max=2)
    coefficient = (weights*ratio*_working(correction)).detach()
    result = torch.where(response_mask, coefficient*j, 0.).sum()/response_mask.sum()
    return result, weights, info


def _mixed_precision_control(generator, device, dtype, *, extreme):
    shape = (1, 4, 128)
    if extreme:
        source = torch.full(shape, -60000., dtype=torch.float32)
        source[..., :2] = 60000.
        positive = source.clone()
        negative = source.clone()
        positive[..., 1] = 58000.
        negative[..., 0] = 58000.
    else:
        source, positive, negative = [torch.randn(shape, generator=generator) for _ in range(3)]
    s, p, n = [x.to(device=device, dtype=dtype).requires_grad_()
               for x in [source, positive, negative]]
    ids = torch.tensor([[0, 1, 0, 1]], device=device)
    mask = torch.tensor([[True, True, True, False]], device=device)
    old = _working(s.detach()).log_softmax(-1).gather(-1, ids[..., None]).squeeze(-1).requires_grad_()
    rates = torch.full((128,), .3, dtype=dtype, device=device)
    counts = torch.ones(128, dtype=dtype, device=device)
    value, weights, info = loss(s, p, n, ids, old, mask,
                                torch.tensor([True], device=device), rates, counts)
    value.backward()
    finite = bool(torch.isfinite(value) and torch.isfinite(weights).all()
                  and torch.isfinite(s.grad).all()
                  and all(torch.isfinite(x).all() for x in info.values()
                          if isinstance(x, torch.Tensor)))
    check = finite and bool(s.grad[mask].abs().sum() > 0) and bool((s.grad[~mask] == 0).all())
    check = check and p.grad is None and n.grad is None and old.grad is None
    return check, value.item(), s.grad.float().abs().sum().item()


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    p, q, n = [torch.randn(2, 12, 128, generator=g, dtype=torch.float64).to(device).requires_grad_()
               for _ in range(3)]
    ids = torch.randint(0, 128, (2, 12), generator=g).to(device)
    mask = torch.ones(2, 12, dtype=torch.bool, device=device)
    mask[:, -2:] = False
    available = torch.tensor([True, False], device=device)
    old = p.detach().log_softmax(-1).gather(-1, ids[..., None]).squeeze(-1).requires_grad_()
    rates = torch.full((128,), .3, dtype=torch.float64, device=device)
    counts = torch.arange(128, dtype=torch.float64, device=device)
    value, weights, info = loss(p, q, n, ids, old, mask, available, rates, counts)
    value.backward()
    valid = mask & available[:, None]
    b = torch.tensor([[1e-30, 1e-30]], dtype=torch.float64, device=device)
    red = redistribute_bonus(b, torch.tensor([0., 1000.], dtype=b.dtype, device=device),
                             torch.tensor([[0, 1]], device=device), torch.ones_like(b, dtype=torch.bool))
    precision_checks, precision_metrics = {}, {}
    for name, dtype in [("fp16", torch.float16), ("bf16", torch.bfloat16)]:
        for mode in ["random", "extreme"]:
            checked, loss_value, grad_l1 = _mixed_precision_control(g, device, dtype, extreme=mode == "extreme")
            prefix = name+"_"+mode
            precision_checks[prefix+"_finite_frozen_teacher_masked_nonzero_gradient"] = checked
            precision_metrics[prefix+"_loss"] = loss_value
            precision_metrics[prefix+"_student_gradient_l1"] = grad_l1
    return receipt(seed, "l1_mechanism", {
        "teacher_states_and_old_policy_detached": q.grad is None and n.grad is None and old.grad is None,
        "padding_gradient_zero": bool((p.grad[~mask] == 0).all()),
        "student_gradient_present": bool(p.grad[mask].abs().sum() > 0),
        "missing_negative_view_keeps_neutral_weight": bool((weights[1] == 1).all()),
        "valid_mean_weight_one": abs(weights[valid].mean().item()-1) < 1e-12,
        "additional_budget_conserved": abs(info["bonus"].sum().item()-info["redistributed_bonus"].sum().item()) < 1e-12,
        "tiny_budget_is_not_dropped": abs(red.sum().item()/b.sum().item()-1) < 1e-12,
        "inverse_frequency_increases_rare_share": red[0, 0].item() > red[0, 1].item(),
        "weights_are_detached": not weights.requires_grad,
        **precision_checks,
    }, {"loss": value.item(), "gradient_norm": p.grad.norm().item(),
        "raw_bonus": info["bonus"].sum().item(), "eligible_tokens": info["eligible"].sum().item(),
        **precision_metrics})
