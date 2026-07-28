from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import random

import numpy as np

from .industrial_batch import (
    compact_movielens,
    evaluate_scores,
    padded_histories,
    require_torch,
    training_pairs,
)


@dataclass(frozen=True)
class FoundationalConfig:
    dimensions: int = 32
    history_length: int = 20
    batch_size: int = 48
    steps: int = 80
    learning_rate: float = 8e-4


def build_foundational_model(kind: str, item_count: int, item_features, config):
    torch, nn = require_torch()
    features = torch.tensor(item_features, dtype=torch.float32)

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            d = config.dimensions
            self.kind = kind
            self.item = nn.Embedding(item_count, d)
            self.feature = nn.Linear(features.shape[1], d, bias=False)
            self.register_buffer("features", features)
            self.deep = nn.Sequential(
                nn.Linear(4 * d, 2 * d), nn.ReLU(), nn.Linear(2 * d, 1)
            )
            self.youtube_user = nn.Sequential(
                nn.Linear(d, 2 * d), nn.ReLU(), nn.Linear(2 * d, d)
            )
            self.wide_bias = nn.Embedding(item_count, 1)
            self.wide_genre = nn.Parameter(torch.zeros(features.shape[1]))
            self.din_attention = nn.Sequential(
                nn.Linear(4 * d, d), nn.Sigmoid(), nn.Linear(d, 1)
            )
            self.gru = nn.GRU(d, d, batch_first=True)
            self.auxiliary = nn.Linear(d, item_count)
            self.position = nn.Embedding(config.history_length + 1, d)
            layer = nn.TransformerEncoderLayer(
                d, 4, 2 * d, batch_first=True, norm_first=True
            )
            self.transformer = nn.TransformerEncoder(layer, 1)
            cross_width = 4 * d
            rank = max(4, d // 2)
            self.cross_u = nn.ModuleList(
                [nn.Linear(cross_width, rank, bias=False) for _ in range(2)]
            )
            self.cross_v = nn.ModuleList(
                [nn.Linear(rank, cross_width, bias=False) for _ in range(2)]
            )
            self.cross_gate = nn.Linear(cross_width, 2)
            self.cross_out = nn.Linear(cross_width, 1)
            self.cycle_gate = nn.Linear(2 * d, d)
            self.sync = nn.Linear(4 * d, 1)
            nn.init.normal_(self.item.weight, std=0.02)
            nn.init.zeros_(self.wide_bias.weight)

        def embed(self, ids):
            return self.item(ids) + self.feature(self.features[ids])

        def _din(self, history, candidate):
            query = candidate[:, None, :]
            attention_input = torch.cat(
                (
                    history,
                    query.expand_as(history),
                    history - query,
                    history * query,
                ),
                dim=-1,
            )
            weight = torch.softmax(
                self.din_attention(attention_input).squeeze(-1), dim=-1
            )
            return (weight[..., None] * history).sum(1)

        def forward(self, histories, candidates):
            history = self.embed(histories)
            candidate = self.embed(candidates)
            pooled = history.mean(1)
            if kind in {
                "deep", "wide-deep", "deepfm", "dcn-v2",
                "two-tower", "youtube-dnn", "cs3",
            }:
                interest = pooled
            elif kind == "din":
                interest = self._din(history, candidate)
            elif kind == "dien":
                states, _ = self.gru(history)
                relevance = torch.softmax(
                    (states * candidate[:, None]).sum(-1)
                    / config.dimensions**0.5,
                    dim=-1,
                )
                # AUGRU's target-aware update gate is represented explicitly:
                # high-relevance states receive a larger recurrent update.
                evolved = torch.zeros_like(states[:, 0])
                for index in range(states.shape[1]):
                    gate = relevance[:, index, None]
                    evolved = (1.0 - gate) * evolved + gate * states[:, index]
                interest = evolved
            elif kind == "bst":
                sequence = torch.cat((history, candidate[:, None]), dim=1)
                positions = torch.arange(sequence.shape[1], device=sequence.device)
                encoded = self.transformer(sequence + self.position(positions)[None])
                interest = encoded[:, -1]
            else:
                raise ValueError(f"unknown foundational ranking kind: {kind}")
            joined = torch.cat(
                (interest, candidate, interest - candidate, interest * candidate),
                dim=-1,
            )
            if kind == "dcn-v2":
                gate = torch.softmax(self.cross_gate(joined), dim=-1)
                crossed = sum(
                    gate[:, index : index + 1]
                    * self.cross_v[index](torch.relu(self.cross_u[index](joined)))
                    for index in range(2)
                )
                logits = self.cross_out(joined + joined * crossed).squeeze(-1)
            elif kind == "two-tower":
                logits = (interest * candidate).sum(-1) / config.dimensions**0.5
            elif kind == "youtube-dnn":
                user = self.youtube_user(interest)
                logits = (user * candidate).sum(-1) / config.dimensions**0.5
            elif kind == "cs3":
                cycle = torch.sigmoid(
                    self.cycle_gate(torch.cat((interest, candidate), dim=-1))
                )
                revised_user = cycle * interest + (1.0 - cycle) * pooled
                synced = torch.cat(
                    (
                        revised_user,
                        candidate,
                        revised_user * candidate,
                        (revised_user - candidate).abs(),
                    ),
                    dim=-1,
                )
                logits = self.sync(synced).squeeze(-1)
            else:
                logits = self.deep(joined).squeeze(-1)
            if kind == "deepfm":
                # Four genuine fields share the same latent width between the
                # FM and deep paths: historical ID interest, candidate ID,
                # historical content and candidate content.
                history_content = self.feature(self.features[histories]).mean(1)
                candidate_content = self.feature(self.features[candidates])
                fields = torch.stack(
                    (interest, self.item(candidates), history_content, candidate_content),
                    dim=1,
                )
                fm = 0.5 * (
                    fields.sum(1).square() - fields.square().sum(1)
                ).sum(-1)
                logits = logits + fm / config.dimensions**0.5
            if kind == "wide-deep":
                genre_cross = (
                    self.features[histories].mean(1)
                    * self.features[candidates]
                    * self.wide_genre
                ).sum(-1)
                logits = logits + self.wide_bias(candidates).squeeze(-1) + genre_cross
            return logits

        def auxiliary_loss(self, histories, positives):
            if kind == "dien":
                states, _ = self.gru(self.embed(histories))
                prediction = self.auxiliary(states[:, -2])
                return torch.nn.functional.cross_entropy(prediction, positives)
            if kind == "cs3":
                # Cascade sharing: the downstream popularity/content teacher
                # supplies a soft target without entering serving.
                teacher = (
                    self.features[positives]
                    * self.features[histories].mean(1)
                ).sum(-1)
                student = self(histories, positives)
                return torch.nn.functional.mse_loss(
                    torch.sigmoid(student), torch.sigmoid(teacher)
                )
            return self.item.weight.sum() * 0.0

    return Model()


def _train(kind, data, config, seed):
    torch, _ = require_torch()
    from auto_research.runtime import device_for

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_foundational_model(
        kind, data.item_count, data.features, config
    ).to(device)
    rows = training_pairs(data, config.history_length)
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    losses = []
    auxiliary = []
    model.train()
    for _ in range(config.steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
        histories = padded_histories(
            [row[0] for row in batch], config.history_length, device, torch
        )
        positive = torch.tensor([row[1] for row in batch], device=device)
        negative = torch.randint(0, data.item_count, positive.shape, device=device)
        candidates = torch.cat((positive, negative))
        repeated = torch.cat((histories, histories))
        labels = torch.cat(
            (torch.ones_like(positive, dtype=torch.float32),
             torch.zeros_like(negative, dtype=torch.float32))
        )
        logits = model(repeated, candidates)
        aux = model.auxiliary_loss(histories, positive)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            logits, labels
        ) + 0.1 * aux
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
        auxiliary.append(float(aux.detach().cpu()))
    return model, {
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "auxiliary_loss": auxiliary[-1],
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def _score(model, history, data, config):
    torch, _ = require_torch()
    device = next(model.parameters()).device
    histories = padded_histories(
        [history], config.history_length, device, torch
    ).expand(data.item_count, -1)
    candidates = torch.arange(data.item_count, device=device)
    model.eval()
    with torch.inference_mode():
        return model(histories, candidates).cpu().numpy()


def run_foundational_reproduction(
    dataset_dir: Path,
    seed: int,
    *,
    paper: dict,
    baseline_kind: str,
    method_kind: str,
    baseline_name: str,
    method_name: str,
    paper_results: dict,
    scope: str,
):
    data = compact_movielens(dataset_dir, maximum_users=180, maximum_items=320)
    config = FoundationalConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_FOUNDATIONAL_STEPS", "80"))
    )
    seeds = (seed, seed + 1, seed + 2)
    from .rec_utils import summarize_runs

    runs = {baseline_kind: [], method_kind: []}
    training = {baseline_kind: [], method_kind: []}
    for run_seed in seeds:
        for kind in runs:
            model, diagnostics = _train(kind, data, config, run_seed)
            training[kind].append(diagnostics)
            runs[kind].append(
                evaluate_scores(
                    data,
                    lambda history, model=model: _score(
                        model, history, data, config
                    ),
                )
            )
    aggregate = {kind: summarize_runs(rows) for kind, rows in runs.items()}
    baseline, method = aggregate[baseline_kind], aggregate[method_kind]
    return {
        "paper": paper,
        "dataset": {
            "name": "MovieLens-100K compact",
            "users": len(data.train),
            "items": data.item_count,
        },
        "setup": {
            "seeds": list(seeds),
            "steps_per_variant": config.steps,
            "same_split_optimizer_budget": True,
        },
        "baseline": {"name": baseline_name, **baseline},
        "method": {"name": method_name, **method},
        "relative": {
            key + "_percent": 100.0 * (method[key] - baseline[key])
            / max(abs(baseline[key]), 1e-12)
            for key in ("hit_at_10", "ndcg_at_10", "head_share_at_10")
        },
        "training": training,
        "paper_results": paper_results,
        "scope": scope,
    }


def render_foundational(result):
    base, method = result["baseline"], result["method"]
    return "\n".join(
        [
            f"# {result['paper']['title']}",
            "",
            f"{result['dataset']['name']} · seeds {result['setup']['seeds']}",
            "",
            "| Variant | Hit@10 | NDCG@10 | Head share@10 |",
            "|---|---:|---:|---:|",
            f"| {base['name']} | {base['hit_at_10']:.4f} | {base['ndcg_at_10']:.4f} | {base['head_share_at_10']:.4f} |",
            f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} |",
            "",
            f"NDCG@10 relative change: **{result['relative']['ndcg_at_10_percent']:+.2f}%**.",
            "",
            "## Reproduction boundary",
            "",
            result["scope"],
            "",
        ]
    )
