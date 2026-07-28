from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class COREConfig:
    dimensions: int = 48
    sft_steps: int = 100
    grpo_steps: int = 35
    distill_steps: int = 80
    batch_size: int = 64
    group_size: int = 6
    learning_rate: float = 1e-3
    temperature: float = 2.0


def build_model(feature_width: int, config: COREConfig, *, cascaded: bool):
    import torch
    from torch import nn

    class RelevanceModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.cascaded = cascaded
            self.encoder = nn.Sequential(
                nn.Linear(4 * feature_width, 2 * config.dimensions),
                nn.GELU(),
                nn.Linear(2 * config.dimensions, config.dimensions),
                nn.LayerNorm(config.dimensions),
            )
            self.flat = nn.Linear(config.dimensions, 3)
            self.high = nn.Linear(config.dimensions, 1)
            self.mid = nn.Linear(config.dimensions, 1)

        def encode(self, query, item):
            return self.encoder(
                torch.cat((query, item, query * item, (query - item).abs()), -1)
            )

        def forward(self, query, item):
            hidden = self.encode(query, item)
            if not self.cascaded:
                return self.flat(hidden)
            return torch.cat((self.high(hidden), self.mid(hidden)), -1)

        def class_log_probs(self, query, item):
            if not self.cascaded:
                return torch.log_softmax(self(query, item), -1)
            binary = self(query, item)
            log_high = torch.nn.functional.logsigmoid(binary[:, 0])
            log_non_high = torch.nn.functional.logsigmoid(-binary[:, 0])
            log_mid = log_non_high + torch.nn.functional.logsigmoid(binary[:, 1])
            log_low = log_non_high + torch.nn.functional.logsigmoid(-binary[:, 1])
            return torch.stack((log_low, log_mid, log_high), -1)

    return RelevanceModel()


def cascaded_supervised_loss(logits, labels, torch):
    high = (labels == 2).float()
    first = torch.nn.functional.binary_cross_entropy_with_logits(logits[:, 0], high)
    active = labels != 2
    second = torch.nn.functional.binary_cross_entropy_with_logits(
        logits[active, 1], (labels[active] == 1).float()
    )
    return first + second


def teacher_binary_logits(class_logits, torch):
    """CORE Eq. 11-12: aggregate PostCoT 3-class logits for two BERT heads."""
    non_high = torch.logsumexp(class_logits[:, :2], -1)
    high = class_logits[:, 2]
    first = high - non_high
    second = class_logits[:, 1] - class_logits[:, 0]
    return torch.stack((first, second), -1)


def step_rewards(actions, labels, torch):
    """Verifiable +1/-1 rewards; inactive second decisions have zero credit."""
    gold_high = labels[:, None] == 2
    first = torch.where(actions[..., 0].bool() == gold_high, 1.0, -1.0)
    active = ~actions[..., 0].bool()
    gold_mid = labels[:, None] == 1
    second = torch.where(actions[..., 1].bool() == gold_mid, 1.0, -1.0)
    second = torch.where(active, second, 0.0)
    return torch.stack((first, second), -1), torch.stack(
        (torch.ones_like(active), active), -1
    )
