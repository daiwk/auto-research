from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np

from ..industrial_ranking import NeuralRankingConfig, require_backend, summarize_training


@dataclass(frozen=True)
class RecDistillConfig(NeuralRankingConfig):
    teacher_dimensions: int = 96
    teacher_layers: int = 3
    student_dimensions: int = 48
    student_layers: int = 1
    negatives: int = 15
    examples: int = 12000
    teacher_steps: int = 240
    student_batch_steps: int = 160
    student_stream_steps: int = 80
    distillation_weight: float = 1.0


def build_teacher(data, config: RecDistillConfig):
    torch, nn = require_backend()
    features = torch.tensor(data.item_features, dtype=torch.float32)
    feature_count = features.shape[1]

    class Teacher(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.teacher_dimensions)
            layer = nn.TransformerEncoderLayer(
                config.teacher_dimensions, config.heads,
                4 * config.teacher_dimensions, batch_first=True,
                norm_first=True, dropout=0.0,
            )
            self.sequence = nn.TransformerEncoder(layer, config.teacher_layers)
            self.score = nn.Sequential(
                nn.Linear(2 * config.teacher_dimensions + 2 * feature_count, config.teacher_dimensions),
                nn.GELU(), nn.Linear(config.teacher_dimensions, 1),
            )
            self.register_buffer("features", features)

        def pair_scores(self, history, candidates):
            user = self.sequence(self.item(history))[:, -1]
            profile = self.features[history].mean(dim=1)
            count = candidates.shape[1]
            values = torch.cat((
                user[:, None].expand(-1, count, -1), self.item(candidates),
                profile[:, None].expand(-1, count, -1), self.features[candidates],
            ), dim=-1)
            return self.score(values).squeeze(-1)

        def forward(self, history):
            candidates = torch.arange(data.item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates)

    return Teacher()


def build_student(data, config: RecDistillConfig):
    torch, nn = require_backend()
    features = torch.tensor(data.item_features, dtype=torch.float32)
    feature_count = features.shape[1]

    class Student(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.student_dimensions)
            layer = nn.TransformerEncoderLayer(
                config.student_dimensions, config.heads,
                4 * config.student_dimensions, batch_first=True,
                norm_first=True, dropout=0.0,
            )
            self.backbone = nn.TransformerEncoder(layer, config.student_layers)
            width = 2 * config.student_dimensions + 2 * feature_count
            self.main = nn.Sequential(
                nn.Linear(width, config.student_dimensions), nn.GELU(),
                nn.Linear(config.student_dimensions, 1),
            )
            self.auxiliary = nn.Sequential(
                nn.Linear(width, config.student_dimensions), nn.GELU(),
                nn.Linear(config.student_dimensions, 1),
            )
            self.register_buffer("features", features)

        def pair_scores(self, history, candidates):
            user = self.backbone(self.item(history))[:, -1]
            profile = self.features[history].mean(dim=1)
            count = candidates.shape[1]
            shared = torch.cat((
                user[:, None].expand(-1, count, -1), self.item(candidates),
                profile[:, None].expand(-1, count, -1), self.features[candidates],
            ), dim=-1)
            return self.main(shared).squeeze(-1), self.auxiliary(shared).squeeze(-1)

        def forward(self, history):
            candidates = torch.arange(data.item_count, device=history.device)[None].expand(len(history), -1)
            return self.pair_scores(history, candidates)

    return Student()


def materialize_examples(data, config: RecDistillConfig, seed: int):
    from ..industrial_ranking import training_examples

    rows = list(training_examples(data.train, config.sequence_length))
    rng = np.random.default_rng(seed)
    rng.shuffle(rows)
    rows = rows[: min(config.examples, len(rows))]
    candidates = []
    for _, positive in rows:
        negatives = rng.integers(0, data.item_count, config.negatives).tolist()
        candidates.append((positive, *negatives))
    return tuple(rows), np.asarray(candidates, dtype=np.int64)


def train_teacher(model, rows, candidates, config: RecDistillConfig, seed: int):
    return _train_binary(model, rows, candidates, config.teacher_steps, config, seed)


def _train_binary(model, rows, candidates, steps, config, seed):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    for _ in range(steps):
        indices = [rng.randrange(len(rows)) for _ in range(config.batch_size)]
        history = torch.tensor([rows[index][0] for index in indices], dtype=torch.long, device=device)
        items = torch.tensor(candidates[indices], dtype=torch.long, device=device)
        logits = model.pair_scores(history, items)
        if isinstance(logits, tuple):
            logits = logits[0]
        labels = torch.zeros_like(logits)
        labels[:, 0] = 1.0
        loss = torch.nn.functional.binary_cross_entropy_with_logits(logits, labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, summarize_training(model, losses, device.type)


def cache_teacher_logits(model, rows, candidates, config: RecDistillConfig):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    values = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(rows), config.batch_size):
            subset = rows[start : start + config.batch_size]
            history = torch.tensor([row[0] for row in subset], dtype=torch.long, device=device)
            items = torch.tensor(candidates[start : start + len(subset)], dtype=torch.long, device=device)
            values.append(model.pair_scores(history, items).cpu().numpy().astype(np.float16))
    return np.concatenate(values)


def debias_probability(logits, negative_ratio: float):
    """Paper Eq. 12 with r+=pX=1 and bs=0 in the local sampler."""

    torch, _ = require_backend()
    return 1.0 / (1.0 + negative_ratio * torch.exp(-logits))


def train_distilled_student(model, rows, candidates, teacher_logits, config, seed):
    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    split = int(0.8 * len(rows))
    phases = ((range(split), config.student_batch_steps), (range(split, len(rows)), config.student_stream_steps))
    rng = random.Random(seed)
    losses, phase_losses = [], []
    for population, steps in phases:
        population = tuple(population)
        current = []
        for _ in range(steps):
            indices = [population[rng.randrange(len(population))] for _ in range(config.batch_size)]
            history = torch.tensor([rows[index][0] for index in indices], dtype=torch.long, device=device)
            items = torch.tensor(candidates[indices], dtype=torch.long, device=device)
            teacher = torch.tensor(teacher_logits[indices], dtype=torch.float32, device=device)
            main, auxiliary = model.pair_scores(history, items)
            labels = torch.zeros_like(main)
            labels[:, 0] = 1.0
            main_loss = torch.nn.functional.binary_cross_entropy_with_logits(main, labels)
            auxiliary_task = torch.nn.functional.binary_cross_entropy_with_logits(auxiliary, labels)
            teacher_probability = debias_probability(teacher, config.negatives)
            student_probability = debias_probability(auxiliary, config.negatives)
            distill = torch.nn.functional.binary_cross_entropy(
                student_probability.clamp(1e-6, 1 - 1e-6), teacher_probability
            )
            loss = main_loss + auxiliary_task + config.distillation_weight * distill
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            value = float(loss.detach().cpu())
            losses.append(value)
            current.append(value)
        phase_losses.append(float(np.mean(current[-20:])))
    metrics = summarize_training(model, losses, device.type)
    metrics.update({"batch_final_loss": phase_losses[0], "stream_final_loss": phase_losses[1]})
    return model, metrics


def train_raw_student_phased(model, rows, candidates, config, seed):
    """Matched batch/stream schedule without teacher supervision."""

    torch, _ = require_backend()
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    split = int(0.8 * len(rows))
    phases = (
        (range(split), config.student_batch_steps),
        (range(split, len(rows)), config.student_stream_steps),
    )
    rng = random.Random(seed)
    losses, phase_losses = [], []
    for population, steps in phases:
        population = tuple(population)
        current = []
        for _ in range(steps):
            indices = [
                population[rng.randrange(len(population))]
                for _ in range(config.batch_size)
            ]
            history = torch.tensor(
                [rows[index][0] for index in indices], dtype=torch.long, device=device
            )
            items = torch.tensor(
                candidates[indices], dtype=torch.long, device=device
            )
            main, auxiliary = model.pair_scores(history, items)
            labels = torch.zeros_like(main)
            labels[:, 0] = 1.0
            loss = (
                torch.nn.functional.binary_cross_entropy_with_logits(main, labels)
                + torch.nn.functional.binary_cross_entropy_with_logits(
                    auxiliary, labels
                )
            )
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            value = float(loss.detach().cpu())
            losses.append(value)
            current.append(value)
        phase_losses.append(float(np.mean(current[-20:])))
    metrics = summarize_training(model, losses, device.type)
    metrics.update(
        {"batch_final_loss": phase_losses[0], "stream_final_loss": phase_losses[1]}
    )
    return model, metrics
