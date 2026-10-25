"""POLARIS Eq.5 human-reference injection and its clipped GRPO surrogate.

Rewards come from the SAME external rubric for policy/reference. No LLM judge,
copyrighted human stories, generation or 9B training is supplied. References are
teacher-forced TRAINING trajectories, not hidden evaluation answers.
"""
import math

import torch
from torch import Tensor

REQUIRES_GPU_VALIDATION = True
GPU_VALIDATION_ARTIFACT = "docs/gpu-validations/polaris-hri-a100-20261025.json"


@torch.no_grad()
def hri_advantages(policy_rewards: Tensor, reference_reward: Tensor, *, step: int,
                   warmup_steps: int = 15, peak_weight: float = .4, epsilon: float = 1e-6) -> Tensor:
    """Policy-only mean/sample-std; reference does NOT alter policy advantages.

    Sample std (correction1) matches the fixed official verl core_algos.py.
    At zero-indexed step0 the teacher-forced reference has zero advantage.
    """
    if (policy_rewards.ndim != 2 or policy_rewards.shape[0] < 1 or policy_rewards.shape[1] < 2
            or policy_rewards.numel() > 65536 or not policy_rewards.is_floating_point()
            or reference_reward.shape != policy_rewards.shape[:1]
            or reference_reward.device != policy_rewards.device or reference_reward.dtype != policy_rewards.dtype
            or not bool(torch.isfinite(policy_rewards).all()) or not bool(torch.isfinite(reference_reward).all())):
        raise ValueError("finite [groups,K>=2] policy rewards and matching [groups] reference rewards required")
    if (isinstance(step, bool) or not isinstance(step, int) or step < 0 or not isinstance(warmup_steps, int)
            or warmup_steps < 1 or not math.isfinite(peak_weight) or peak_weight < 0
            or not math.isfinite(epsilon) or epsilon <= 0):
        raise ValueError("nonnegative step/peak, positive warmup and epsilon required")
    work = policy_rewards.float() if policy_rewards.dtype in (torch.float16, torch.bfloat16) else policy_rewards
    mean, std = work.mean(-1, keepdim=True), work.std(-1, correction=1, keepdim=True)
    policy = (work - mean) / (std + epsilon)
    alpha = peak_weight * min(1., step / warmup_steps)
    reference = alpha * (reference_reward.to(work.dtype)[:, None] - mean) / (std + epsilon)
    result = torch.cat((policy, reference), -1)
    if not bool(torch.isfinite(result).all()):
        raise ValueError("nonfinite HRI advantages; no silent clamp")
    return result.detach()


def hri_grpo_loss(current_logps: Tensor, old_logps: Tensor, mask: Tensor,
                  advantages: Tensor, *, clip_ratio: float = .2,
                  reduction: str = "token_mean") -> Tensor:
    """Same clipped surrogate for policy and teacher-forced reference trajectories.

    [groups,K+1,tokens]. old policy and advantages are frozen. Explicit reduction
    permits token_mean or sequence_mean; no hidden reference-specific loss weight
    is applied again after Eq.5's warmup. KL is absent in the paper configuration.
    """
    if (current_logps.ndim != 3 or min(current_logps.shape) < 1 or current_logps.shape[1] < 3
            or current_logps.numel() > 1_048_576 or not current_logps.is_floating_point()
            or old_logps.shape != current_logps.shape or old_logps.dtype != current_logps.dtype
            or old_logps.device != current_logps.device or not bool(torch.isfinite(current_logps).all())
            or not bool(torch.isfinite(old_logps).all())):
        raise ValueError("bounded matching finite [groups,K+1,tokens] policy log probabilities required")
    if (mask.shape != current_logps.shape or mask.dtype != torch.bool or mask.device != current_logps.device
            or bool((mask.sum(-1) == 0).any()) or advantages.shape != current_logps.shape[:2]
            or advantages.device != current_logps.device or not bool(torch.isfinite(advantages).all())):
        raise ValueError("nonempty target masks and matching finite group advantages required")
    if not math.isfinite(clip_ratio) or not 0 < clip_ratio < 1 or reduction not in ("token_mean", "sequence_mean"):
        raise ValueError("clip in(0,1) and explicit token_mean/sequence_mean required")
    work = current_logps.float() if current_logps.dtype in (torch.float16, torch.bfloat16) else current_logps
    old = old_logps.detach().to(work.dtype)
    # Select the exact clipped branch in LOG space before exp. Computing exp(1000)
    # then minimum can have a finite forward but inf*0 -> NaN backward. Padding
    # and zero advantages must never evaluate an irrelevant exponential either.
    log_ratio = work.masked_fill(~mask, 0) - old.masked_fill(~mask, 0)
    advantage = advantages.detach().to(work.dtype)[..., None].expand_as(work).masked_fill(~mask, 0)
    positive_log = torch.minimum(log_ratio, work.new_tensor(math.log1p(clip_ratio)))
    negative_log = torch.maximum(log_ratio, work.new_tensor(math.log1p(-clip_ratio)))
    selected_log = torch.where(advantage >= 0, positive_log, negative_log)
    selected_log = torch.where(advantage == 0, torch.zeros_like(selected_log), selected_log)
    objective = selected_log.exp() * advantage
    if not bool(torch.isfinite(objective).all()):
        raise ValueError("nonfinite HRI surrogate; no silent ratio clamp")
    loss = (-(objective * mask).sum() / mask.sum() if reduction == "token_mean"
            else -((objective * mask).sum(-1) / mask.sum(-1)).mean())
    if not bool(torch.isfinite(loss)):
        raise ValueError("nonfinite HRI loss")
    return loss


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if device not in ("cpu", "cuda") or device == "cuda" and not torch.cuda.is_available():
        raise ValueError("cpu or real available cuda required; no fallback")
    gen = torch.Generator(device=device).manual_seed(seed)
    rewards = torch.tensor([[.1, .5, .9, .2, .4], [.3, .6, .4, .1, .8]], device=device, dtype=torch.float64)
    reference = torch.tensor([1.1, 1.2], device=device, dtype=torch.float64)
    advantages = hri_advantages(rewards, reference, step=15)
    expected = torch.empty_like(advantages)
    for i in range(2):
        mean = sum(float(x) for x in rewards[i]) / 5
        std = math.sqrt(sum((float(x) - mean) ** 2 for x in rewards[i]) / 4)
        expected[i, :5] = (rewards[i] - mean) / (std + 1e-6)
        expected[i, 5] = .4 * (reference[i] - mean) / (std + 1e-6)
    advantage_error = (advantages - expected).abs().max().item()
    old = torch.randn(2, 6, 4, generator=gen, device=device, dtype=torch.float64).requires_grad_()
    current = (old.detach() + .03 * torch.randn(old.shape, generator=gen, device=device, dtype=torch.float64)).requires_grad_()
    mask = torch.ones_like(current, dtype=torch.bool)
    mask[..., -1] = False
    before = hri_grpo_loss(current, old, mask, advantages)
    ratio = (current - old.detach()).exp()
    oracle = -(torch.minimum(ratio * expected[..., None], ratio.clamp(.8, 1.2) * expected[..., None]) * mask).sum() / mask.sum()
    loss_error = (before - oracle).detach().abs().item()
    optimizer = torch.optim.SGD((current,), lr=.02)
    optimizer.zero_grad()
    before.backward()
    gradient = current.grad.detach().clone()
    optimizer.step()
    after = hri_grpo_loss(current, old, mask, advantages)
    changed = hri_advantages(rewards, reference + 100, step=15)
    checks = {"eq5_policy_only_sample_statistics": advantage_error < 1e-12 and torch.equal(advantages[:, :5], changed[:, :5]),
              "zero_step_reference_warmup": bool((hri_advantages(rewards, reference, step=0)[:, -1] == 0).all()),
              "reference_uses_same_clipped_surrogate": loss_error < 1e-12 and gradient[:, -1].norm().item() > 0,
              "old_and_advantages_frozen": old.grad is None and not advantages.requires_grad,
              "padding_zero_gradient": bool((gradient[~mask] == 0).all()),
              "real_optimizer_step_decreases_fixture": after.item() < before.item()}
    if not all(checks.values()):
        raise RuntimeError(f"POLARIS HRI contract failed: {checks}")
    return {"seed": seed, "metrics": {"advantage_reference_error": advantage_error, "loss_reference_error": loss_error,
        "reference_gradient_norm": gradient[:, -1].norm().item(), "fixture_loss_before": before.item(),
        "fixture_loss_after": after.item(), "policy_rollouts_per_group": 5, "references_per_group": 1,
        "optimizer_steps": 1, "pretrained_model_calls": 0}, "checks": checks}
