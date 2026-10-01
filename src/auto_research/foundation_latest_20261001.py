"""Foundation-model and serving kernels from the Oct-1 intake batch."""

from __future__ import annotations


def vjepa_policy_losses(predicted_latents, target_latents, predicted_velocity, target_actions, noise, time):
    """Future-latent L1 plus conditional flow-matching action objective."""
    import torch
    import torch.nn.functional as F

    if predicted_latents.shape != target_latents.shape:
        raise ValueError("future latent tensors must align")
    latent_loss = F.l1_loss(predicted_latents, target_latents.detach())
    while time.ndim < target_actions.ndim:
        time = time.unsqueeze(-1)
    interpolated = (1 - time) * noise + time * target_actions
    target_velocity = target_actions - noise
    if predicted_velocity(interpolated, predicted_latents).shape != target_velocity.shape:
        raise ValueError("action velocity tensors must align")
    action_loss = F.mse_loss(predicted_velocity(interpolated, predicted_latents), target_velocity)
    return latent_loss + action_loss, {"latent_loss": float(latent_loss.detach()), "action_loss": float(action_loss.detach())}


def ce_guided_router(native_logits, predicted_error, *, gamma: float = 1.0, tau: float = 1.0):
    """Error-aware MoE affinity attenuation from Eq. 5--7."""
    import torch

    if native_logits.shape != predicted_error.shape or tau <= 0 or gamma < 0:
        raise ValueError("invalid CE-guided router inputs")
    adjusted = native_logits - gamma * torch.log1p(predicted_error.clamp_min(0) / tau)
    return torch.softmax(adjusted, dim=-1), adjusted


def tadm_fusion(stale_anchor, current_state, gate, correction):
    """Time-anchored latent cache correction h'=h+g(c,h)*Delta(c,h)."""
    if stale_anchor.shape != current_state.shape:
        raise ValueError("anchor and current state must align")
    update = correction(current_state, stale_anchor)
    weight = gate(current_state, stale_anchor).sigmoid()
    if update.shape != stale_anchor.shape or weight.shape != stale_anchor.shape:
        raise ValueError("fusion outputs must align with anchor")
    return stale_anchor + weight * update, weight


def pumba_window(step_fn, initial_logits, targets, *, window: int, detach_between_windows: bool = True):
    """Unroll consecutive denoising steps and backpropagate through the carry."""
    import torch.nn.functional as F

    if window < 1:
        raise ValueError("window must be positive")
    logits = initial_logits
    carry = None
    losses = []
    for step in range(window):
        logits, carry = step_fn(logits, carry, step)
        losses.append(F.cross_entropy(logits.reshape(-1, logits.shape[-1]), targets.reshape(-1)))
    if detach_between_windows and carry is not None:
        carry = carry.detach()
    return sum(losses) / len(losses), carry, tuple(losses)


def splash_memory(layout: str, *, attention_weights: float, batch: int, kv_heads: int, sequence: int, tensor_parallel: int):
    """Per-device attention memory model from SPLASH Section 2."""
    if tensor_parallel < 1 or min(attention_weights, batch, kv_heads, sequence) < 0:
        raise ValueError("invalid SPLASH memory inputs")
    kv = batch * kv_heads * sequence
    if layout == "tp":
        return attention_weights / tensor_parallel + kv
    if layout == "dop":
        return attention_weights / tensor_parallel + kv / tensor_parallel
    if layout in {"dp", "cp"}:
        return attention_weights + kv / tensor_parallel
    raise ValueError(f"unknown layout {layout}")


def splash_select_layout(costs, previous: str | None, transition_costs, *, remaining_steps: int):
    """Choose the layout with transition cost amortized over remaining steps."""
    if remaining_steps < 1 or not costs:
        raise ValueError("invalid scheduling inputs")
    effective = {}
    for layout, step_cost in costs.items():
        switch = 0.0 if previous in (None, layout) else float(transition_costs.get((previous, layout), 0.0))
        effective[layout] = float(step_cost) + switch / remaining_steps
    return min(effective, key=lambda key: (effective[key], key)), effective
