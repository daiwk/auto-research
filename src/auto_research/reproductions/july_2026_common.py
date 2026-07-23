from __future__ import annotations

import math
import os
import random
from dataclasses import dataclass

import numpy as np

from .industrial_ranking import initialize, require_backend, summarize_training
from .rec_utils import batched_ranking_metrics, load_movielens_sequences


PAPER_IDS = {
    "tsgr": "2607.18796",
    "whale": "2607.17017",
    "ramp": "2607.17473",
    "tmallgs": "2607.13398",
    "long-history-transformer": "2607.14331",
    "downstream-rewards": "2607.14192",
}


@dataclass(frozen=True)
class JulyRankingConfig:
    dimensions: int = 32
    heads: int = 4
    layers: int = 2
    sequence_length: int = 16
    batch_size: int = 32
    steps: int = 60
    learning_rate: float = 6e-4

    @classmethod
    def from_env(cls, prefix: str, **overrides):
        values = {
            "steps": int(os.environ.get(f"AUTO_RESEARCH_{prefix}_STEPS", overrides.pop("steps", 60))),
            "batch_size": int(
                os.environ.get(f"AUTO_RESEARCH_{prefix}_BATCH_SIZE", overrides.pop("batch_size", 32))
            ),
        }
        values.update(overrides)
        return cls(**values)


def ranking_data(dataset_dir):
    return load_movielens_sequences(dataset_dir)


def point_examples(data, length: int):
    rows = []
    for user, sequence in enumerate(data.train):
        for end in range(2, len(sequence) + 1):
            history = tuple(sequence[max(0, end - length) : end])
            rows.append((user, _left_pad(history, length), sequence[end - 1]))
    return tuple(rows)


def _left_pad(history, length: int):
    history = tuple(history[-length:])
    return (history[0],) * (length - len(history)) + history


def train_catalog_model(model, data, config: JulyRankingConfig, seed: int, loss_builder=None):
    model, device, torch = initialize(model, seed)
    rows = point_examples(data, config.sequence_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses, components = [], {}
    model.train()
    for step in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        users = torch.tensor([row[0] for row in batch], dtype=torch.long, device=device)
        histories = torch.tensor([row[1] for row in batch], dtype=torch.long, device=device)
        targets = torch.tensor([row[2] for row in batch], dtype=torch.long, device=device)
        output = model(histories, users=users, training_step=step)
        if isinstance(output, dict):
            logits = output["logits"]
            extras = output
        else:
            logits, extras = output, {}
        if loss_builder is None:
            loss = torch.nn.functional.cross_entropy(logits, targets)
            values = {"ranking": loss}
        else:
            loss, values = loss_builder(model, extras, logits, targets, histories, users, step, torch)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        for name, value in values.items():
            components.setdefault(name, []).append(float(value.detach().cpu()))
    metrics = summarize_training(model, losses, device.type)
    metrics["loss_components"] = {
        key: float(np.mean(values[-min(10, len(values)) :]))
        for key, values in components.items()
    }
    return model, metrics


def score_batch(model, histories, config: JulyRankingConfig, *, mode=None):
    torch, _ = require_backend()
    device = next(model.parameters()).device
    rows = [_left_pad(history, config.sequence_length) for history in histories]
    model.eval()
    with torch.inference_mode():
        output = model(torch.tensor(rows, dtype=torch.long, device=device), mode=mode)
        logits = output["logits"] if isinstance(output, dict) else output
    return logits.detach().cpu().numpy()


def evaluate_catalog(model, data, config: JulyRankingConfig, *, mode=None, target="test"):
    return batched_ranking_metrics(
        data,
        lambda histories: score_batch(model, histories, config, mode=mode),
        batch_size=128,
        target=target,
    )


def relative(method, baseline):
    return {
        f"{key}_percent": 100.0 * (method[key] - baseline[key]) / max(abs(baseline[key]), 1e-12)
        for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10", "mean_popularity_at_10")
    }


def item_feature_tensor(data, dimensions: int, torch):
    features = np.asarray(data.item_features, dtype=np.float32)
    rng = np.random.default_rng(202607)
    projection = rng.normal(0.0, 1.0 / math.sqrt(max(features.shape[1], 1)),
                            size=(features.shape[1], dimensions)).astype(np.float32)
    return torch.tensor(features @ projection, dtype=torch.float32)


def build_late_fusion_baseline(data, config: JulyRankingConfig, history_limit: int | None = None):
    torch, nn = require_backend()

    class LateFusionRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(data.item_count, config.dimensions)
            self.position = nn.Embedding(config.sequence_length, config.dimensions)
            self.content = nn.Parameter(
                item_feature_tensor(data, config.dimensions, torch), requires_grad=False
            )
            layer = nn.TransformerEncoderLayer(
                config.dimensions,
                config.heads,
                3 * config.dimensions,
                batch_first=True,
                norm_first=True,
                dropout=0.0,
            )
            self.encoder = nn.TransformerEncoder(layer, config.layers)
            self.fusion = nn.Sequential(
                nn.Linear(2 * config.dimensions, config.dimensions),
                nn.SiLU(),
                nn.LayerNorm(config.dimensions),
            )

        def forward(self, histories, **_):
            if history_limit is not None:
                histories = histories[:, -history_limit:]
            positions = torch.arange(histories.shape[1], device=histories.device)
            tokens = self.item(histories) + self.position(positions)
            encoded = self.encoder(tokens)
            context = self.fusion(torch.cat([encoded[:, -1], tokens.mean(1)], dim=-1))
            catalog = self.item.weight + self.content
            return context @ catalog.T

    return LateFusionRanker()


def standard_result(*, key, title, organization, data, config, baseline_name, method_name,
                    baseline, method, training, stages, paper_results, scope, seed=42):
    return {
        "paper": {
            "arxiv_id": PAPER_IDS[key],
            "title": title,
            "url": f"https://arxiv.org/abs/{PAPER_IDS[key]}",
            "organization": organization,
        },
        "dataset": {"name": "MovieLens 100K", "users": len(data.train), "items": data.item_count},
        "setup": {
            "seed": seed,
            "steps_per_model": config.steps,
            "sequence_length": config.sequence_length,
            "same_split_candidates_and_item_features": True,
        },
        "baseline": {"name": baseline_name, **baseline},
        "method": {"name": method_name, **method},
        "relative": relative(method, baseline),
        "training": training,
        "stages": stages,
        "paper_results": paper_results,
        "scope": scope,
    }


def render_standard(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join([
        f"# {result['paper']['title']}",
        "",
        (
            f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / "
            f"{result['dataset']['items']} items）"
        ),
        "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 | Mean popularity@10 |",
        "|---|---:|---:|---:|---:|",
        (
            f"| {baseline['name']} | {baseline['hit_at_10']:.4f} | "
            f"{baseline['ndcg_at_10']:.4f} | {baseline['head_share_at_10']:.4f} | "
            f"{baseline['mean_popularity_at_10']:.6f} |"
        ),
        (
            f"| {method['name']} | {method['hit_at_10']:.4f} | "
            f"{method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} | "
            f"{method['mean_popularity_at_10']:.6f} |"
        ),
        "",
        (
            "相对同协议基线："
            f"Hit@10 {result['relative']['hit_at_10_percent']:+.2f}%，"
            f"NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。"
        ),
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ])
