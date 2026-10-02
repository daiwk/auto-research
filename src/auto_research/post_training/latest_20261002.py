"""Faithful mechanism kernels for the 2026-10-02 post-training intake."""

from __future__ import annotations


def dependency_shaped_rewards(events, prerequisites, *, discount: float = 0.5):
    """DARS potential differences over verified, broken and repaired predicates.

    ``events`` is a sequence of mappings with optional ``verify``, ``invalidate``
    and ``repair`` predicate lists.  A broken prerequisite attenuates dependent
    predicates while independent verified work retains credit.
    """
    if not 0 <= discount <= 1:
        raise ValueError("discount must be in [0, 1]")
    verified: set[str] = set()
    broken: set[str] = set()

    def potential() -> float:
        score = 0.0
        for predicate in verified:
            frontier = [predicate]
            seen: set[str] = set()
            distance = 0
            weight = 1.0
            while frontier:
                if any(node in broken for node in frontier):
                    weight = discount ** max(distance, 1)
                    break
                seen.update(frontier)
                frontier = [
                    parent
                    for node in frontier
                    for parent in prerequisites.get(node, ())
                    if parent not in seen
                ]
                distance += 1
            score += weight
        return score

    rewards = []
    previous = potential()
    for event in events:
        for predicate in event.get("invalidate", ()):
            broken.add(predicate)
            verified.discard(predicate)
        for predicate in event.get("repair", ()):
            broken.discard(predicate)
        for predicate in event.get("verify", ()):
            verified.add(predicate)
            broken.discard(predicate)
        current = potential()
        rewards.append(current - previous)
        previous = current
    return rewards, {"verified": tuple(sorted(verified)), "broken": tuple(sorted(broken))}


def range_grpo_advantages(lower, upper):
    """Range-GRPO pairwise interval advantages.

    Non-overlapping intervals receive signed confidence proportional to their
    separation. Overlap produces no unjustified ordering. Point intervals
    reduce to the usual pairwise relative-score signal.
    """
    import torch

    lower = torch.as_tensor(lower)
    upper = torch.as_tensor(upper, device=lower.device, dtype=lower.dtype)
    if lower.ndim != 1 or lower.shape != upper.shape or torch.any(lower > upper):
        raise ValueError("reward intervals must be aligned one-dimensional bounds")
    left = lower[:, None]
    right = upper[:, None]
    separation = torch.where(
        left > upper[None, :],
        left - upper[None, :],
        torch.where(right < lower[None, :], right - lower[None, :], 0.0),
    )
    scale = (upper - lower)[:, None] + (upper - lower)[None, :] + 1.0
    return (separation / scale).mean(-1)


def fault_terminal_redistribution(
    terminal_rewards,
    diagnoses,
    error_costs,
    *,
    maximum_penalty: float = 0.8,
):
    """FAULT terminal-anchored, conserved credit redistribution.

    Diagnosed error claims are used only when ``verified``.  Their learned
    costs form localization weights; total redistributed credit is conserved
    for each trajectory and the terminal ordering is retained.
    """
    import torch

    rewards = torch.as_tensor(terminal_rewards, dtype=torch.float32)
    if not 0 <= maximum_penalty < 1:
        raise ValueError("maximum_penalty must be in [0, 1)")
    rows = []
    coverage = []
    for terminal, claims in zip(rewards, diagnoses):
        length = max((int(item["step"]) for item in claims), default=0) + 1
        weights = torch.zeros(length, dtype=rewards.dtype)
        for claim in claims:
            if claim.get("verified", False):
                weights[int(claim["step"])] += float(error_costs[claim["category"]])
        if float(weights.sum()) > 0:
            normalized = weights / weights.sum()
            penalty = maximum_penalty * normalized
            redistributed = terminal * (1.0 / length + penalty.mean() - penalty)
            coverage.append(True)
        else:
            redistributed = terminal.expand(length) / length
            coverage.append(False)
        # Numerical guard: preserve the terminal total exactly.
        redistributed[-1] += terminal - redistributed.sum()
        rows.append(redistributed)
    return rows, {"signal_coverage": sum(coverage) / max(len(coverage), 1)}


def where_opd_loss(student_logits, privileged_teacher_logits, spatial_mask):
    """Where-OPD privileged-spatial teacher KL on student on-policy tokens."""
    import torch
    import torch.nn.functional as F

    if student_logits.shape != privileged_teacher_logits.shape:
        raise ValueError("student and teacher logits must align")
    if spatial_mask.shape != student_logits.shape[:-1]:
        raise ValueError("spatial mask must align with token positions")
    student_logp = F.log_softmax(student_logits, dim=-1)
    with torch.no_grad():
        teacher = F.softmax(privileged_teacher_logits, dim=-1)
    token_kl = F.kl_div(student_logp, teacher, reduction="none").sum(-1)
    weights = spatial_mask.to(token_kl.dtype)
    return (token_kl * weights).sum() / weights.sum().clamp_min(1.0)
