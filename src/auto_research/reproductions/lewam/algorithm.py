"""LeWAM mathematical contracts, not a substitute for its visual backbone."""
from __future__ import annotations


def mot_visibility(history: int = 2, clean: int = 5, noisy: int = 10, goal: bool = True):
    import torch
    # [history | state query | optional goal | clean actions | noisy actions]
    clean_start = history + 1 + int(goal)
    noisy_start = clean_start + clean
    allowed = torch.zeros(noisy_start + noisy, noisy_start + noisy, dtype=torch.bool)
    allowed[:history, :history] = True
    allowed[history, :history + 1] = True
    allowed[history, clean_start:noisy_start] = True
    if goal:
        allowed[history + 1, history + 1] = True
    for i in range(clean):
        allowed[clean_start + i, :history] = True
        allowed[clean_start + i, clean_start:clean_start + i + 1] = True
    for i in range(noisy):
        allowed[noisy_start + i, :history] = True
        allowed[noisy_start + i, noisy_start:noisy_start + i + 1] = True
        if goal:
            allowed[noisy_start + i, history + 1] = True
    return allowed


def action_flow_targets(action, noise, time):
    """s=0 noise, s=1 data; target velocity is action-noise (Eq. 2)."""
    return (1 - time) * noise + time * action, action - noise


def sigreg(latents, directions, knots: int = 17):
    """Epps–Pulley characteristic-function distance on random unit projections."""
    import torch
    directions = directions / directions.norm(dim=0, keepdim=True).clamp_min(1e-12)
    values = latents @ directions
    t = torch.linspace(0, 3, knots, device=latents.device, dtype=latents.dtype)
    phase = values.unsqueeze(-1) * t
    target = torch.exp(-0.5 * t.square())
    error = (phase.cos().mean(0) - target).square() + phase.sin().mean(0).square()
    return 2 * len(latents) * torch.trapezoid(error * target, t, dim=-1).mean()


def joint_loss(predicted_state, target_state, predicted_velocity, velocity, regularizer,
               weight: float = 0.04):
    return ((predicted_state - target_state).square().mean()
            + (predicted_velocity - velocity).square().mean() + weight * regularizer)


def refine_plans(plans, goal_cost, steps: int = 5, lr: float = 0.05,
                 proximity: float = 0.01, action_bound: float = 3):
    """Appendix A.1: retain best unpenalized iterate, optimize actions only."""
    import torch
    original = plans.detach().clone()
    current = original.clone().requires_grad_(True)
    optimizer = torch.optim.Adam([current], lr=lr)
    with torch.no_grad():
        best, best_cost = original.clone(), goal_cost(original).clone()
    for _ in range(steps):
        optimizer.zero_grad()
        objective = goal_cost(current).sum() + proximity * (current - original).square().sum()
        objective.backward()
        torch.nn.utils.clip_grad_norm_([current], 10)
        optimizer.step()
        with torch.no_grad():
            current.clamp_(-action_bound, action_bound)
            costs = goal_cost(current)
            improved = costs < best_cost
            best[improved], best_cost[improved] = current[improved], costs[improved]
    chosen = int(best_cost.argmin())
    return best[chosen], best_cost[chosen]
