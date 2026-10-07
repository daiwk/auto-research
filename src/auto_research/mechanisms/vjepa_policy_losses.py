"""Extracted unchanged from auto_research.foundation_latest_20261001; stable mechanism boundary."""
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
