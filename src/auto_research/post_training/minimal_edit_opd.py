"""ME-OPD Appendix A routing and selected-token corrective objective.

Independent numerical component, not a VLM, verifier or teacher-prompt system.
Only incorrect TRAINING rollouts use privileged teacher scores. The complete
rollout is scored, not decoded, by an external teacher. No gold/reference input
is accepted by an evaluated student here; there is no capability evaluation.
"""
from __future__ import annotations

from dataclasses import dataclass
import math

import torch
from torch import Tensor


@dataclass(frozen=True)
class FrozenRollouts:
    """Snapshot created once before policy updates; do not mutate its tensors."""

    old_log_prob: Tensor
    teacher_log_prob: Tensor
    actor_mask: Tensor
    correct: Tensor
    corrective_mask: Tensor
    advantages: Tensor


def full_group_advantages(rewards: Tensor, group_ids: Tensor, *,
                          std_correction: int, epsilon: float) -> Tensor:
    """Group statistics use ALL K binary rewards before correct-only routing.

    The paper leaves TaskAdvantages abstract. The caller must therefore choose
    std correction and epsilon explicitly; neither is claimed to be an author
    implementation default. Both population and sample std are supported.
    """
    if rewards.ndim != 1 or rewards.numel() == 0 or not rewards.is_floating_point():
        raise ValueError("a nonempty floating binary reward vector required")
    if group_ids.shape != rewards.shape or group_ids.dtype != torch.long or group_ids.device != rewards.device:
        raise ValueError("aligned int64 prompt groups on the reward device required")
    if not bool(torch.isfinite(rewards).all()) or not bool(((rewards == 0) | (rewards == 1)).all()):
        raise ValueError("finite binary verifier rewards required")
    if type(std_correction) is not int or std_correction not in (0, 1):
        raise ValueError("explicit std_correction 0 or 1 required")
    if not math.isfinite(epsilon) or epsilon <= 0:
        raise ValueError("positive finite advantage epsilon required")
    dtype = torch.float32 if rewards.dtype in (torch.float16, torch.bfloat16) else rewards.dtype
    frozen = rewards.detach().to(dtype)
    advantages = torch.empty_like(frozen)
    sizes = []
    for group in torch.unique(group_ids):
        members = group_ids == group
        count = int(members.sum())
        if count < 2:
            raise ValueError("each full rollout group must contain K >= 2 rewards")
        sizes.append(count)
        values = frozen[members]
        advantages[members] = (values - values.mean()) / (values.std(correction=std_correction) + epsilon)
    if len(set(sizes)) != 1:
        raise ValueError("all complete prompt groups must have the same K")
    if not bool(torch.isfinite(advantages).all()):
        raise ValueError("advantages must be representable")
    return advantages.detach()


def freeze_rollouts(old_log_prob: Tensor, teacher_log_prob: Tensor, rewards: Tensor,
                    actor_mask: Tensor, *, task_advantages: Tensor) -> FrozenRollouts:
    """Algorithm 1 lines 9--18: freeze OLD-policy k>0 mask, not current k.

    Teacher scores are required only on active tokens of incorrect rollouts;
    NaNs on correct rows or padding are ignored. A student/teacher tokenizer
    alignment and a real verifier are caller preconditions, not checked by this
    numerical component. Every row must contain its full response-token mask.
    ``task_advantages`` must be computed over ALL K rewards before routing; the
    formula itself is an external training configuration. See the explicitly
    configurable ``full_group_advantages`` helper for a local implementation.
    """
    if old_log_prob.ndim != 2 or min(old_log_prob.shape) < 1 or not old_log_prob.is_floating_point():
        raise ValueError("nonempty floating [rollout,token] old log probabilities required")
    if teacher_log_prob.shape != old_log_prob.shape or not teacher_log_prob.is_floating_point():
        raise ValueError("aligned floating teacher log probabilities required")
    if actor_mask.shape != old_log_prob.shape or actor_mask.dtype != torch.bool or not bool(actor_mask.any(1).all()):
        raise ValueError("a nonempty Boolean response mask per rollout required")
    if rewards.shape != (old_log_prob.shape[0],):
        raise ValueError("one verifier reward per rollout required")
    if any(t.device != old_log_prob.device for t in (teacher_log_prob, rewards, actor_mask, task_advantages)):
        raise ValueError("all snapshot inputs must share a device")
    if not rewards.is_floating_point() or not bool(torch.isfinite(rewards).all()) or not bool(((rewards == 0) | (rewards == 1)).all()):
        raise ValueError("finite binary verifier rewards required")
    if task_advantages.shape != rewards.shape or not task_advantages.is_floating_point() or not bool(torch.isfinite(task_advantages).all()):
        raise ValueError("one finite externally computed full-group advantage per rollout required")
    correct = rewards.detach() == 1
    failed_mask = actor_mask & ~correct[:, None]
    for values, mask in ((old_log_prob, actor_mask), (teacher_log_prob, failed_mask)):
        if not bool(torch.isfinite(values[mask]).all()) or bool((values[mask] > 0).any()):
            raise ValueError("finite nonpositive active log probabilities required")
    dtype = torch.promote_types(old_log_prob.dtype, teacher_log_prob.dtype)
    if dtype in (torch.float16, torch.bfloat16):
        dtype = torch.float32
    old = torch.where(actor_mask, old_log_prob.detach().to(dtype), 0.)
    teacher = torch.where(failed_mask, teacher_log_prob.detach().to(dtype), 0.)
    # Comparing log probabilities avoids overflow of their difference. Equality
    # is excluded. This frozen mask stays unchanged during all policy updates.
    corrective = (failed_mask & (old > teacher)).detach()
    return FrozenRollouts(old.clone(), teacher.clone(), actor_mask.detach().clone(),
        correct.clone(), corrective.clone(), task_advantages.detach().clone())


def correct_rollout_grpo(current_log_prob: Tensor, batch: FrozenRollouts, *,
                         clip_epsilon: float = .2) -> Tensor:
    """Correct-only clipped PG with a documented LOCAL sequence-mean reduction.

    Appendix A does not specify PG reduction. This helper uses mean tokens in
    each correct response, then mean correct responses, with no KL/entropy term.
    It is not claimed to resolve the paper's unspecified verl configuration.
    """
    if not math.isfinite(clip_epsilon) or not 0 < clip_epsilon < 1:
        raise ValueError("finite clipping epsilon in (0,1) required")
    selected = batch.actor_mask & batch.correct[:, None]
    if not bool(batch.correct.any()):
        return current_log_prob.sum() * 0.
    difference = torch.where(selected, current_log_prob - batch.old_log_prob, 0.)
    advantage = batch.advantages.to(current_log_prob.dtype)[:, None]
    # Exactly the PPO minimum without overflowing an unselected exp branch.
    clipped_log = torch.where(advantage >= 0,
        difference.clamp_max(math.log1p(clip_epsilon)),
        difference.clamp_min(math.log1p(-clip_epsilon)))
    objective = clipped_log.exp() * advantage
    if not bool(torch.isfinite(objective[selected]).all()):
        raise ValueError("correct-rollout importance objective is not representable")
    per_response = torch.where(selected, objective, 0.).sum(1) / batch.actor_mask.sum(1)
    return -per_response[batch.correct].mean()


def sampled_log_probabilities(current_logits: Tensor, actions: Tensor,
                               batch: FrozenRollouts) -> Tensor:
    """Gather student probabilities; ignore padding before any nonlinear math."""
    if current_logits.ndim != 3 or min(current_logits.shape) < 1 or not current_logits.is_floating_point():
        raise ValueError("nonempty floating [rollout,token,vocabulary] logits required")
    shape = current_logits.shape[:2]
    if actions.shape != shape or actions.dtype != torch.long or batch.actor_mask.shape != shape:
        raise ValueError("aligned integer sampled actions and frozen batch required")
    tensors = (actions, batch.old_log_prob, batch.teacher_log_prob, batch.actor_mask,
               batch.correct, batch.corrective_mask, batch.advantages)
    if any(value.device != current_logits.device for value in tensors):
        raise ValueError("all loss inputs must share a device")
    mask = batch.actor_mask
    if not bool(torch.isfinite(current_logits[mask]).all()):
        raise ValueError("finite active logits required")
    if not bool(((actions[mask] >= 0) & (actions[mask] < current_logits.shape[-1])).all()):
        raise ValueError("active sampled actions must be within vocabulary")
    dtype = torch.float32 if current_logits.dtype in (torch.float16, torch.bfloat16) else current_logits.dtype
    clean_logits = torch.where(mask[..., None], current_logits.to(dtype), 0.)
    sampled = clean_logits.log_softmax(-1).gather(-1,
        torch.where(mask, actions, 0)[..., None]).squeeze(-1)
    if not bool(torch.isfinite(sampled[mask]).all()):
        raise ValueError("active current log probabilities must be representable")
    return sampled


def minimal_edit_loss(current_logits: Tensor, actions: Tensor, batch: FrozenRollouts,
                       *, correct_task_loss: Tensor | None,
                       corrective_weight: float = .01) -> tuple[Tensor, dict]:
    """Exact Eq. 1 composition with an EXTERNAL correct-only task objective.

    The caller computes task loss from correct rows and ALL-K advantages; this
    interface does not silently select an unspecified GRPO reduction. When no
    correct rollout exists, pass None and receive a differentiable zero task
    term. A supplied task loss must not have a failed-rollout gradient.

    Corrective loss is the LINEAR selected sampled-token log ratio normalized
    by global selected-token count Z, not full-vocabulary KL, KL-weighted policy
    loss or generated teacher-target CE. A zero Z gives an autograd zero.
    """
    if not math.isfinite(corrective_weight) or corrective_weight < 0:
        raise ValueError("finite nonnegative corrective weight required")
    sampled = sampled_log_probabilities(current_logits, actions, batch)
    if bool(batch.correct.any()):
        if correct_task_loss is None or correct_task_loss.ndim != 0 or not correct_task_loss.is_floating_point() or correct_task_loss.device != sampled.device or not bool(torch.isfinite(correct_task_loss)):
            raise ValueError("a finite external scalar correct-only task loss required")
        task = correct_task_loss
    else:
        if correct_task_loss is not None:
            raise ValueError("no correct rollout: pass None for the task loss")
        task = sampled.sum() * 0.
    selected_count = int(batch.corrective_mask.sum())
    correction = torch.where(batch.corrective_mask,
        sampled - batch.teacher_log_prob, 0.).sum() / max(selected_count, 1)
    loss = task + corrective_weight * correction
    if not bool(torch.isfinite(loss)):
        raise ValueError("combined loss must be representable")
    return loss, {"task_loss": task.detach(), "corrective_loss": correction.detach(),
        "selected_tokens": selected_count, "correct_rollouts": int(batch.correct.sum()),
        "failed_rollouts": int((~batch.correct).sum())}


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Real autograd/SGD on synthetic logits, NOT VLM task evaluation."""
    generator = torch.Generator(device=device).manual_seed(seed)
    logits = torch.randn(6, 4, 5, device=device, dtype=torch.float64,
        generator=generator).requires_grad_()
    actions = torch.multinomial(logits.detach().softmax(-1).reshape(-1, 5), 1,
        generator=generator).reshape(6, 4)
    old = logits.detach().log_softmax(-1).gather(-1, actions[..., None]).squeeze(-1).clone().requires_grad_()
    teacher = (old.detach() + torch.tensor([[-.3, .2, 0., -.7]], device=device)).requires_grad_()
    # Teacher probabilities must remain valid; positive perturbations are capped.
    teacher = teacher.clamp_max(-1e-3).detach().requires_grad_()
    rewards = torch.tensor([1., 0., 0., 1., 1., 0.], device=device,
        dtype=torch.float64, requires_grad=True)
    groups = torch.tensor([0, 0, 0, 1, 1, 1], device=device)
    mask = torch.ones(6, 4, dtype=torch.bool, device=device)
    mask[1, 3] = False
    advantages = full_group_advantages(rewards, groups, std_correction=0, epsilon=1e-6)
    batch = freeze_rollouts(old, teacher, rewards, mask, task_advantages=advantages)
    before = logits.detach().clone()
    task = correct_rollout_grpo(sampled_log_probabilities(logits, actions, batch), batch)
    loss, audit = minimal_edit_loss(logits, actions, batch, correct_task_loss=task)
    probabilities = logits.softmax(-1).gather(-1, actions[..., None]).squeeze(-1)
    expected_adv = torch.tensor([2., -1., -1., 1., 1., -2.], device=device,
        dtype=torch.float64) / (math.sqrt(2.) + 3e-6)
    ratio = probabilities / old.detach().exp()
    terms = torch.minimum(ratio * expected_adv[:, None],
        ratio.clamp(.8, 1.2) * expected_adv[:, None])
    task_reference = -(terms.sum(1) / 4)[rewards.detach() == 1].mean()
    expected_mask = mask & (rewards.detach()[:, None] == 0) & (old.detach() > teacher.detach())
    correction_reference = (probabilities.log() - teacher.detach())[expected_mask].sum() / expected_mask.sum()
    reference = task_reference + .01 * correction_reference
    reference_gradient = torch.autograd.grad(reference, logits, retain_graph=True)[0]
    error = float((loss.detach() - reference.detach()).abs())
    loss.backward()
    gradient = logits.grad.detach().clone()
    gradient_error = float((gradient - reference_gradient).abs().max())
    with torch.no_grad():
        logits -= .01 * gradient
    task_after = correct_rollout_grpo(sampled_log_probabilities(logits, actions, batch), batch)
    after, _ = minimal_edit_loss(logits, actions, batch, correct_task_loss=task_after)
    delta = float((logits.detach() - before).norm())
    return {"seed": seed, "diagnostic_only": True, "component": "minimal_edit_frozen_routing_selected_token_loss",
        "metrics": {"loss_before": float(loss.detach()), "loss_after": float(after.detach()),
            "gradient_norm": float(gradient.norm()), "parameter_delta": delta,
            "formula_reference_error": error, "gradient_reference_error": gradient_error,
            "selected_tokens": audit["selected_tokens"], "correct_rollouts": audit["correct_rollouts"],
            "optimizer_updates": 1, "model_calls": 0},
        "checks": {"formula_reference_matches": error < 1e-12,
            "gradient_reference_matches": gradient_error < 1e-12,
            "old_policy_detached": old.grad is None, "teacher_detached": teacher.grad is None,
            "rewards_detached": rewards.grad is None,
            "full_group_advantages": bool(torch.allclose(batch.advantages, expected_adv)),
            "frozen_old_mask": bool(torch.equal(batch.corrective_mask, expected_mask)),
            "strict_sign_and_failed_only": not bool(batch.corrective_mask[batch.correct].any()),
            "padding_zero_gradient": bool((gradient[~mask] == 0).all()),
            "unselected_failed_zero_gradient": bool((gradient[mask & ~batch.correct[:, None] & ~batch.corrective_mask] == 0).all()),
            "finite_gradient": bool(gradient.isfinite().all()), "real_parameter_update": delta > 0,
            "fixed_objective_decreased": float(after.detach()) < float(loss.detach())}}
