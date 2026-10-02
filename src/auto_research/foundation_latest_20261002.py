"""Foundation-model mechanisms from the 2026-10-02 intake."""

from __future__ import annotations


def taco_direction(gradient):
    """Exact column-wise one-sparse steepest direction used by TACO."""
    import torch

    if gradient.ndim != 2:
        raise ValueError("TACO applies its one-sparse rule to matrices")
    rows = gradient.abs().argmax(dim=0, keepdim=True)
    signs = gradient.gather(0, rows).sign()
    return torch.zeros_like(gradient).scatter_(0, rows, signs)


class TACO:
    """Minimal first-order TACO optimizer with low-precision column momentum."""

    def __init__(self, parameters, *, lr: float = 1e-3, beta: float = 0.9):
        import torch

        if lr <= 0 or not 0 <= beta < 1:
            raise ValueError("invalid TACO hyperparameters")
        self.parameters = list(parameters)
        self.lr = lr
        self.beta = beta
        self.state: dict[int, torch.Tensor] = {}

    def step(self):
        import torch

        with torch.no_grad():
            for parameter in self.parameters:
                if parameter.grad is None:
                    continue
                if parameter.ndim != 2:
                    parameter.add_(parameter.grad, alpha=-self.lr)
                    continue
                direction = taco_direction(parameter.grad)
                rows = parameter.grad.abs().argmax(dim=0)
                components = parameter.grad.gather(0, rows[None]).squeeze(0)
                momentum = self.state.get(id(parameter), torch.zeros_like(components, dtype=torch.float16))
                momentum.mul_(self.beta).add_(components.to(momentum.dtype), alpha=1 - self.beta)
                self.state[id(parameter)] = momentum
                update = direction * momentum.to(parameter.dtype).abs()[None]
                parameter.add_(update, alpha=-self.lr)

    @property
    def state_elements(self):
        return sum(value.numel() for value in self.state.values())


def veto_compress(video_tokens, *, spatial_keep: int, temporal_keep: int):
    """VETO spatial-first token merging followed by frame-level merging."""
    import torch
    import torch.nn.functional as F

    if video_tokens.ndim != 3:
        raise ValueError("video tokens must have [frames, spatial_tokens, dim]")
    frames, tokens, _ = video_tokens.shape
    if not 0 < spatial_keep <= tokens or not 0 < temporal_keep <= frames:
        raise ValueError("invalid VETO budgets")
    # Deterministic farthest-point representatives approximate OT matching.
    representatives = [0]
    normalized = F.normalize(video_tokens, dim=-1)
    while len(representatives) < spatial_keep:
        similarity = normalized @ normalized[:, representatives].transpose(1, 2)
        distance = 1 - similarity.max(-1).values.mean(0)
        representatives.append(int(distance.argmax()))
    spatial = video_tokens[:, representatives]
    frame_repr = F.normalize(spatial.mean(1), dim=-1)
    selected = [0]
    while len(selected) < temporal_keep:
        distance = 1 - (frame_repr @ frame_repr[selected].T).max(-1).values
        distance[selected] = -1
        selected.append(int(distance.argmax()))
    return spatial[selected], {
        "spatial_indices": tuple(representatives),
        "frame_indices": tuple(selected),
        "compression_ratio": spatial_keep * temporal_keep / (tokens * frames),
    }


def gfg_mixed_objective(current_loss, replay_loss, *, replay_fraction: float):
    """GfG mid-training blend that exposes the anti-forgetting trade-off."""
    if not 0 <= replay_fraction <= 1:
        raise ValueError("replay_fraction must be in [0, 1]")
    return (1 - replay_fraction) * current_loss + replay_fraction * replay_loss
