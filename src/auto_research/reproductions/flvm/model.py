"""Factorized latent value measurement and a separately trained multitask control."""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import functional as F


# Long view, click, like, hate. Each feedback head sees only its assigned axes.
ROUTES = torch.tensor(((1, 0, 0), (1, 1, 0), (0, 1, 1), (0, 1, 1)))


class ImpressionFeatures(nn.Module):
    def __init__(self, users: int, items: int, width: int = 16):
        super().__init__()
        self.user = nn.Embedding(users, width)
        self.item = nn.Embedding(items, width)

    def forward(self, users: torch.Tensor, items: torch.Tensor,
                confounders: torch.Tensor) -> torch.Tensor:
        return torch.cat((self.user(users), self.item(items), confounders), dim=-1)


class FLVM(nn.Module):
    """Restricted baseline + stopped logit + routed Gaussian advantage."""

    def __init__(self, users: int, items: int, width: int = 16):
        super().__init__()
        self.features = ImpressionFeatures(users, items, width)
        self.encoder = nn.Sequential(nn.Linear(2 * width + 3, 32), nn.ReLU(),
                                     nn.Linear(32, 6))
        self.baseline = nn.Sequential(nn.Linear(3, 16), nn.ReLU(), nn.Linear(16, 4))
        self.decoders = nn.ModuleList(
            nn.Sequential(nn.Linear(3, 12), nn.Tanh(), nn.Linear(12, 1))
            for _ in range(4)
        )
        self.gain_logit = nn.Parameter(torch.zeros(4))
        self.register_buffer("routes", ROUTES.float())

    def forward(self, users: torch.Tensor, items: torch.Tensor,
                confounders: torch.Tensor, *, sample: bool = True
                ) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
        stats = self.encoder(self.features(users, items, confounders))
        mean, log_variance = stats.chunk(2, dim=-1)
        log_variance = log_variance.clamp(-8, 4)
        latent = mean + torch.randn_like(mean) * torch.exp(0.5 * log_variance) \
            if sample else mean
        baseline = self.baseline(confounders)
        advantages = torch.cat([
            decoder(latent * self.routes[task]) * F.softplus(self.gain_logit[task])
            for task, decoder in enumerate(self.decoders)
        ], dim=-1)
        return baseline.detach() + advantages, baseline, mean, log_variance

    @staticmethod
    def loss(logits: torch.Tensor, baseline: torch.Tensor, labels: torch.Tensor,
             mask: torch.Tensor, mean: torch.Tensor, log_variance: torch.Tensor,
             *, kl_weight: float = 0.001) -> torch.Tensor:
        if logits.shape != labels.shape or mask.shape != labels.shape:
            raise ValueError("feedback labels and observation masks must match the logits")
        weights = labels.new_tensor((1.0, 1.0, 3.0, 5.0))
        normalizer = (mask * weights).sum().clamp_min(1)
        main = (F.binary_cross_entropy_with_logits(logits, labels, reduction="none")
                * mask * weights).sum() / normalizer
        auxiliary = (F.binary_cross_entropy_with_logits(baseline, labels, reduction="none")
                     * mask * weights).sum() / normalizer
        kl = -0.5 * (1 + log_variance - mean.square() - log_variance.exp()).sum(-1).mean()
        return main + auxiliary + kl_weight * kl

    @staticmethod
    def value_score(mean: torch.Tensor) -> torch.Tensor:
        return torch.sigmoid(mean[:, 2]) * F.softplus(mean[:, 0])


class MultitaskControl(nn.Module):
    """Same public serving features and feedback heads, without FLVM factorization."""

    def __init__(self, users: int, items: int, width: int = 16):
        super().__init__()
        self.features = ImpressionFeatures(users, items, width)
        self.head = nn.Sequential(nn.Linear(2 * width + 3, 32), nn.ReLU(),
                                  nn.Linear(32, 4))

    def forward(self, users: torch.Tensor, items: torch.Tensor,
                confounders: torch.Tensor) -> torch.Tensor:
        return self.head(self.features(users, items, confounders))
