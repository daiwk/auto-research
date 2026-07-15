from __future__ import annotations

import copy
import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import initialize, require_backend, summarize_training


@dataclass(frozen=True)
class NONTPConfig:
    dimensions: int = 48
    heads: int = 4
    layers: int = 2
    sequence_length: int = 16
    batch_size: int = 32
    steps: int = 180
    learning_rate: float = 3e-4
    future_steps: int = 3
    temperature: float = 0.07
    ema_momentum: float = 0.999
    auxiliary_weight: float = 0.1


def build_model(item_count: int, config: NONTPConfig):
    torch, nn = require_backend()

    class SequenceBackbone(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            layer = nn.TransformerEncoderLayer(
                config.dimensions,
                config.heads,
                4 * config.dimensions,
                batch_first=True,
                norm_first=True,
                dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.normalization = nn.LayerNorm(config.dimensions)
            nn.init.normal_(self.item.weight, std=0.02)

        def hidden(self, items):
            positions = torch.arange(items.shape[1], device=items.device)
            values = self.item(items) + self.position(positions)
            causal = torch.triu(
                torch.ones(items.shape[1], items.shape[1], device=items.device),
                diagonal=1,
            ).bool()
            return self.normalization(self.encoder(values, mask=causal))

        def logits(self, hidden):
            return hidden @ self.item.weight.T

        def forward(self, items):
            return self.logits(self.hidden(items))

    return SequenceBackbone()


def sequence_windows(sequences, length: int):
    rows = []
    for sequence in sequences:
        for end in range(3, len(sequence) + 1):
            window = tuple(sequence[max(0, end - length - 1) : end])
            padded = (window[0],) * (length + 1 - len(window)) + window
            rows.append(padded)
    return tuple(rows)


def train_model(kind: str, data, domains: np.ndarray, config: NONTPConfig, seed: int):
    torch, nn = require_backend()
    if kind not in {"ntp", "tcl", "tdl", "nontp"}:
        raise ValueError(f"unknown NONTP variant: {kind}")
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    model, device, torch = initialize(build_model(data.item_count, config), seed)
    uses_tcl = kind in {"tcl", "nontp"}
    teacher = copy.deepcopy(model).to(device).eval() if uses_tcl else None
    if teacher is not None:
        for parameter in teacher.parameters():
            parameter.requires_grad_(False)
    predictors = nn.ModuleList(
        [nn.Linear(config.dimensions, config.dimensions) for _ in range(config.future_steps)]
        if uses_tcl else []
    ).to(device)
    parameters = list(model.parameters()) + list(predictors.parameters())
    optimizer = torch.optim.AdamW(parameters, lr=config.learning_rate)
    domain_tensor = torch.tensor(domains, dtype=torch.long, device=device)
    rows = sequence_windows(data.train, config.sequence_length)
    rng = random.Random(seed)
    losses = []
    components = {"ntp": [], "tcl": [], "tdl": []}
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        values = torch.tensor(batch, dtype=torch.long, device=device)
        source, targets = values[:, :-1], values[:, 1:]
        hidden = model.hidden(source)
        ntp = torch.nn.functional.cross_entropy(
            model.logits(hidden).reshape(-1, data.item_count), targets.reshape(-1)
        )
        zero = ntp.new_zeros(())
        tcl = _temporal_loss(model, teacher, predictors, source, hidden, config, torch) \
            if uses_tcl else zero
        tdl = _trans_domain_loss(model, hidden, source, targets, domain_tensor, torch) \
            if kind in {"tdl", "nontp"} else zero
        loss = ntp + config.auxiliary_weight * (tcl + tdl)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.0)
        optimizer.step()
        if uses_tcl:
            _ema_update(teacher, model, config.ema_momentum)
        losses.append(float(loss.detach().cpu()))
        components["ntp"].append(float(ntp.detach().cpu()))
        components["tcl"].append(float(tcl.detach().cpu()))
        components["tdl"].append(float(tdl.detach().cpu()))
    metrics = summarize_training(model, losses, device.type)
    metrics["loss_components"] = {
        name: float(np.mean(values[-min(20, len(values)) :]))
        for name, values in components.items()
    }
    metrics["training_parameters"] = sum(p.numel() for p in parameters if p.requires_grad)
    return model, metrics


def _temporal_loss(model, teacher, predictors, source, hidden, config, torch):
    with torch.no_grad():
        targets = teacher.hidden(source)
    losses = []
    batch, length, _ = hidden.shape
    sequence_ids = torch.arange(batch, device=hidden.device).repeat_interleave(length)
    for offset, predictor in enumerate(predictors, start=1):
        if offset >= length:
            continue
        queries = torch.nn.functional.normalize(predictor(hidden[:, :-offset]), dim=-1)
        positives = torch.nn.functional.normalize(targets[:, offset:], dim=-1)
        queries = queries.reshape(-1, queries.shape[-1])
        positives = positives.reshape(-1, positives.shape[-1])
        local_ids = sequence_ids.reshape(batch, length)[:, :-offset].reshape(-1)
        logits = queries @ positives.T / config.temperature
        same_sequence = local_ids[:, None] == local_ids[None, :]
        diagonal = torch.eye(len(logits), dtype=torch.bool, device=logits.device)
        logits = logits.masked_fill(same_sequence & ~diagonal, -torch.inf)
        labels = torch.arange(len(logits), device=logits.device)
        losses.append(torch.nn.functional.cross_entropy(logits, labels))
    return torch.stack(losses).mean()


def _trans_domain_loss(model, hidden, source, targets, domains, torch):
    pooled, expected = [], []
    source_domains = domains[source]
    target_domains = domains[targets]
    for row in range(source.shape[0]):
        for position in range(1, source.shape[1]):
            mask = source_domains[row, :position] != target_domains[row, position]
            if mask.any():
                pooled.append(hidden[row, :position][mask].mean(dim=0))
                expected.append(targets[row, position])
    if not pooled:
        return hidden.new_zeros(())
    logits = model.logits(torch.stack(pooled))
    return torch.nn.functional.cross_entropy(logits, torch.stack(expected))


def _ema_update(teacher, model, momentum: float):
    with require_backend()[0].no_grad():
        for target, online in zip(teacher.parameters(), model.parameters()):
            target.mul_(momentum).add_(online, alpha=1.0 - momentum)


def score_all(model, history, config: NONTPConfig):
    return score_batch(model, [history], config)[0]


def score_batch(model, histories, config: NONTPConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    rows = []
    for history in histories:
        recent = tuple(history[-config.sequence_length :])
        rows.append((recent[0],) * (config.sequence_length - len(recent)) + recent)
    model.eval()
    with torch.inference_mode():
        values = torch.tensor(rows, dtype=torch.long, device=device)
        return model(values)[:, -1].cpu().numpy()
