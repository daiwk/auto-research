from __future__ import annotations

import copy
import math


def forward_with_trace(model, tokens):
    """Run the local decoder while exposing the layer trajectory for alignment."""
    import torch

    values = model.token(tokens)
    if model.position is not None:
        positions = torch.arange(tokens.shape[1], device=tokens.device)
        values = values + model.position(positions)[None]
    hidden = []
    for block in model.blocks:
        values = block(values)
        hidden.append(values)
    values = model.final_norm(values)
    return model.output(values), hidden


class SparseBlockFactory:
    """Late factory keeps torch an optional dependency at package-import time."""

    @staticmethod
    def build(block, dimensions: int, retention: float):
        import torch
        from torch import nn

        class SparseBlock(nn.Module):
            def __init__(self):
                super().__init__()
                self.block = block
                self.retention = float(retention)
                hidden = max(8, dimensions // 4)
                self.router = nn.Sequential(
                    nn.Linear(dimensions, hidden),
                    nn.SiLU(),
                    nn.Linear(hidden, 1),
                )
                self.last_active_fraction = 1.0

            def forward(self, values):
                batch, length, width = values.shape
                keep = max(1, min(length, int(math.floor(self.retention * length))))
                scores = self.router(values).squeeze(-1)
                indices = scores.topk(keep, dim=1).indices.sort(dim=1).values
                gather = indices.unsqueeze(-1).expand(batch, keep, width)
                selected = values.gather(1, gather)
                transformed = self.block(selected)
                # The score gate gives the lightweight router an end-to-end
                # alignment gradient while the expensive block really runs on K tokens.
                selected_scores = scores.gather(1, indices)
                gate = torch.sigmoid(selected_scores).unsqueeze(-1)
                transformed = selected + gate * (transformed - selected)
                output = values.clone()
                output.scatter_(1, gather, transformed)
                self.last_active_fraction = keep / length
                return output

        return SparseBlock()


def calibration_similarities(dense, tokens) -> list[float]:
    import torch

    dense.eval()
    values = dense.token(tokens)
    if dense.position is not None:
        positions = torch.arange(tokens.shape[1], device=tokens.device)
        values = values + dense.position(positions)[None]
    similarities = []
    with torch.inference_mode():
        for block in dense.blocks:
            output = block(values)
            cosine = torch.nn.functional.cosine_similarity(
                values.float(), output.float(), dim=-1
            )
            similarities.append(float(cosine.mean().cpu()))
            values = output
    return similarities


def allocate_retentions(
    similarities: list[float],
    *,
    target: float = 0.8,
    temperature: float = 0.05,
    beta: float = 10.0,
) -> list[float]:
    """Equations 5–8: similarity weighting, deviation, sigmoid and budget correction."""
    import numpy as np

    scores = np.asarray(similarities, dtype=np.float64)
    weights = np.exp((scores - scores.max()) / temperature)
    weights /= weights.sum()
    deviation = beta * (weights.mean() - weights)
    raw = 0.05 + 0.9 / (1.0 + np.exp(-deviation))
    corrected = raw * (target * len(raw) / raw.sum())
    # Eq. 8 fixes the global budget; enforce the physical [0.05, 1] bounds
    # with a small bounded-simplex projection so clipping cannot change it.
    values = corrected.copy()
    fixed = np.zeros(len(values), dtype=bool)
    for _ in range(len(values) + 1):
        high, low = values > 1.0, values < 0.05
        newly_fixed = (high | low) & ~fixed
        values[high], values[low] = 1.0, 0.05
        fixed |= high | low
        free = ~fixed
        if not free.any():
            break
        remaining = target * len(values) - values[fixed].sum()
        values[free] *= remaining / values[free].sum()
        if not newly_fixed.any() and np.all(
            (values[free] >= 0.05) & (values[free] <= 1.0)
        ):
            break
    return values.tolist()


def sparsify(dense, retentions: list[float]):
    sparse = copy.deepcopy(dense)
    dimensions = sparse.token.embedding_dim
    sparse.blocks = type(sparse.blocks)([
        SparseBlockFactory.build(block, dimensions, ratio)
        for block, ratio in zip(sparse.blocks, retentions)
    ])
    return sparse


def train_alignment(
    student,
    teacher,
    tokens,
    *,
    steps: int,
    batch_size: int,
    length: int,
    learning_rate: float,
    seed: int,
    torch,
) -> dict:
    import numpy as np

    device = next(teacher.parameters()).device
    teacher.eval()
    student.to(device).train()
    optimizer = torch.optim.AdamW(student.parameters(), lr=learning_rate)
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        starts = rng.integers(0, len(tokens) - length - 1, size=batch_size)
        rows = np.stack([tokens[start : start + length] for start in starts])
        batch = torch.tensor(rows, dtype=torch.long, device=device)
        with torch.no_grad():
            teacher_logits, teacher_hidden = forward_with_trace(teacher, batch)
        student_logits, student_hidden = forward_with_trace(student, batch)
        teacher_distribution = torch.softmax(teacher_logits.float(), dim=-1)
        output_kl = torch.nn.functional.kl_div(
            torch.log_softmax(student_logits.float(), dim=-1),
            teacher_distribution,
            reduction="batchmean",
        ) / (batch_size * length)
        hidden_loss = torch.stack([
            (
                torch.softmax(student_value.float(), dim=-1)
                - torch.softmax(teacher_value.float(), dim=-1)
            ).pow(2).mean().sqrt()
            for student_value, teacher_value in zip(student_hidden, teacher_hidden)
        ]).mean()
        loss = output_kl + hidden_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(student.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_alignment_loss": float(np.mean(losses[:5])),
        "final_alignment_loss": float(np.mean(losses[-5:])),
    }


def routing_statistics(model) -> dict:
    fractions = [block.last_active_fraction for block in model.blocks]
    return {
        "retentions": [float(block.retention) for block in model.blocks],
        "active_token_fraction": float(sum(fractions) / len(fractions)),
    }
