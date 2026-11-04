"""SpecOPD's proposal-tree contract and E2E-TV objective (arXiv:2611.02846).

Numerical L1 components only: no drafter, target checkpoint, production kernel,
rollout service or inference speed benchmark is implemented by this module.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor


@dataclass(frozen=True)
class ProposalTree:
    """Zero-based packed trunk then private branches; True means visible."""

    parent: Tensor
    positions: Tensor
    attention_mask: Tensor
    branch_rows: Tensor
    prediction_rows: Tensor


def proposal_tree(trunk_length: int, anchors: Tensor, width: int) -> ProposalTree:
    """Equations 1--4 / Appendix C.1, without sampling or a backbone.

    Each first sample is predicted by its anchor, and later samples by their
    predecessor. A sample must NOT be scored from its own hidden-state row.
    """
    if type(trunk_length) is not int or trunk_length < 1 or type(width) is not int or width < 1:
        raise ValueError("positive integer trunk_length and width required")
    if anchors.ndim != 1 or anchors.numel() < 1 or anchors.dtype != torch.long:
        raise ValueError("nonempty int64 anchor vector required")
    if bool(((anchors < 0) | (anchors >= trunk_length)).any()):
        raise ValueError("anchors must index the reference trunk")
    device = anchors.device
    branches = anchors.numel()
    total = trunk_length + branches * width
    parent = torch.arange(total, device=device) - 1
    positions = torch.arange(total, device=device)
    mask = torch.zeros((total, total), dtype=torch.bool, device=device)
    mask[:trunk_length, :trunk_length] = torch.ones(
        (trunk_length, trunk_length), dtype=torch.bool, device=device).tril()
    rows = torch.arange(trunk_length, total, device=device).reshape(branches, width)
    prediction_rows = torch.empty_like(rows)
    for branch, anchor in enumerate(anchors.tolist()):
        branch_rows = rows[branch]
        parent[branch_rows[0]] = anchor
        prediction_rows[branch, 0] = anchor
        if width > 1:
            parent[branch_rows[1:]] = branch_rows[:-1]
            prediction_rows[branch, 1:] = branch_rows[:-1]
        positions[branch_rows] = anchor + 1 + torch.arange(width, device=device)
        mask[branch_rows, :anchor + 1] = True
        mask[branch_rows[:, None], branch_rows[None, :]] = torch.ones(
            (width, width), dtype=torch.bool, device=device).tril()
    return ProposalTree(parent, positions, mask, rows, prediction_rows)


def prediction_logits(hidden: Tensor, head: Tensor, tree: ProposalTree) -> Tensor:
    """Read predecessor states, then use the supplied frozen target LM head.

    This function does not freeze the backbone itself. Callers must use a
    frozen teacher/no_grad when collecting actual teacher distributions.
    """
    if hidden.ndim != 2 or head.ndim != 2 or hidden.shape[1] != head.shape[1]:
        raise ValueError("hidden [packed,dim] and head [vocab,dim] required")
    if hidden.shape[0] != tree.parent.numel() or hidden.device != head.device or hidden.device != tree.parent.device:
        raise ValueError("aligned packed rows and devices required")
    if not hidden.is_floating_point() or not head.is_floating_point() or not bool(torch.isfinite(hidden).all()) or not bool(torch.isfinite(head).all()):
        raise ValueError("finite floating states and head required")
    return hidden[tree.prediction_rows] @ head.T


def e2e_tv_loss(student_logits: Tensor, teacher_logits: Tensor, *, support: Tensor | None = None) -> Tensor:
    """Equations 8--9: 1 - mean of prefix products of distribution overlap.

    The teacher remains normalized on its FULL vocabulary (Appendix C.2).
    Masking the draft support must not renormalize the teacher onto that support.
    Samples are externally supplied histories, not differentiated actions.
    """
    if student_logits.ndim != 3 or min(student_logits.shape) < 1 or teacher_logits.shape != student_logits.shape:
        raise ValueError("aligned nonempty [branch,width,vocab] logits required")
    if student_logits.device != teacher_logits.device or not student_logits.is_floating_point() or not teacher_logits.is_floating_point():
        raise ValueError("floating logits on the same device required")
    if support is None:
        support = torch.ones_like(student_logits, dtype=torch.bool)
    if support.dtype != torch.bool or support.shape != student_logits.shape or support.device != student_logits.device or not bool(support.any(-1).all()):
        raise ValueError("nonempty Boolean draft support per position required")
    if not bool(torch.isfinite(student_logits[support]).all()) or not bool(torch.isfinite(teacher_logits).all()):
        raise ValueError("finite active draft and full-vocabulary teacher logits required")
    dtype = torch.promote_types(student_logits.dtype, teacher_logits.dtype)
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    q = torch.where(support, student_logits.to(dtype), -torch.inf).softmax(-1)
    p = teacher_logits.detach().to(dtype).softmax(-1)
    overlap = torch.minimum(q, p).sum(-1)
    return 1 - overlap.cumprod(-1).mean()


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Seeded tensor/gradient checks, not acceptance or generation capability."""
    generator = torch.Generator(device="cpu").manual_seed(seed)
    anchors = torch.tensor([1, 3], dtype=torch.long, device=device)
    tree = proposal_tree(5, anchors, 3)
    embeddings = torch.randn(11, 7, generator=generator, dtype=torch.float64).to(device)
    scores = embeddings @ embeddings.T / math.sqrt(7)
    hidden = scores.masked_fill(~tree.attention_mask, -torch.inf).softmax(-1) @ embeddings
    head = torch.randn(6, 7, generator=generator, dtype=torch.float64).to(device)
    packed = prediction_logits(hidden, head, tree)
    separate = []
    for branch, anchor in enumerate(anchors.tolist()):
        indices = torch.cat((torch.arange(anchor + 1, device=device), tree.branch_rows[branch]))
        values = embeddings[indices]
        local_scores = values @ values.T / math.sqrt(7)
        causal = torch.ones(local_scores.shape, dtype=torch.bool, device=device).tril()
        states = local_scores.masked_fill(~causal, -torch.inf).softmax(-1) @ values
        separate.append(states[anchor:anchor + 3] @ head.T)
    separate_logits = torch.stack(separate)
    student = torch.randn(2, 3, 6, generator=generator, dtype=torch.float64).to(device).requires_grad_()
    teacher = packed.detach().requires_grad_()
    support = torch.ones_like(student, dtype=torch.bool)
    support[..., -1] = False
    loss = e2e_tv_loss(student, teacher, support=support)
    q = student.detach().masked_fill(~support, -torch.inf).softmax(-1)
    p = teacher.detach().softmax(-1)
    reference_terms = []
    for branch in range(2):
        product = 1.
        for position in range(3):
            product *= sum(min(float(q[branch, position, token]), float(p[branch, position, token])) for token in range(6))
            reference_terms.append(product)
    reference = 1 - sum(reference_terms) / 6
    loss.backward()
    gradient = student.grad.detach().clone()
    updated = student.detach() - .01 * gradient
    after = e2e_tv_loss(updated, teacher, support=support)
    # A one-step support mismatch is not a perfect match after teacher renorm.
    q_example = torch.tensor([[[0., 0., 0.]]], dtype=torch.float64, device=device)
    p_example = torch.tensor([[[.4, .4, .2]]], dtype=torch.float64, device=device).log()
    support_example = torch.tensor([[[True, True, False]]], device=device)
    missing_mass = e2e_tv_loss(q_example, p_example, support=support_example)
    error = float((packed - separate_logits).abs().max())
    checks = {
        "packed_matches_independent_causal_scoring": error < 1e-10,
        "predecessor_readout_not_own_token": bool(torch.equal(tree.prediction_rows[:, 0], anchors)) and bool(torch.equal(tree.prediction_rows[:, 1:], tree.branch_rows[:, :-1])),
        "no_future_or_sibling_visibility": not bool(tree.attention_mask[5:8, 2:5].any()) and not bool(tree.attention_mask[5:8, 8:].any()),
        "reference_loss_matches": abs(float(loss.detach()) - reference) < 1e-10,
        "teacher_frozen": teacher.grad is None,
        "draft_gradient_finite_nonzero": bool(torch.isfinite(gradient).all()) and float(gradient.norm()) > 0,
        "excluded_support_zero_gradient": bool((gradient[~support] == 0).all()),
        "teacher_outside_support_mass_retained": abs(float(missing_mass) - .2) < 1e-10,
        "small_update_decreases_component_loss": float(after.detach()) < float(loss.detach()),
    }
    return {"seed": seed, "device": device, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"loss": float(loss.detach()), "loss_after": float(after.detach()), "gradient_norm": float(gradient.norm()), "causal_scoring_max_error": error, "outside_support_loss": float(missing_mass), "model_calls": 0}, "checks": checks}
