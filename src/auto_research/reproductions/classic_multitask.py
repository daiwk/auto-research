from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import random

import numpy as np

from ..datasets import movielens_100k
from .industrial_batch import require_torch


@dataclass(frozen=True)
class MultiTaskConfig:
    dimensions: int = 24
    experts: int = 4
    batch_size: int = 128
    steps: int = 200
    learning_rate: float = 1e-3
    maximum_users: int = 420
    maximum_items: int = 900


def _examples(root: Path, config: MultiTaskConfig, seed: int):
    ratings = movielens_100k(root)
    users = sorted({row[0] for row in ratings})[: config.maximum_users]
    items = sorted({row[1] for row in ratings})[: config.maximum_items]
    user_ids = {value: index for index, value in enumerate(users)}
    item_ids = {value: index for index, value in enumerate(items)}
    observed: dict[int, set[int]] = {user_ids[user]: set() for user in users}
    rows = []
    for user, item, rating, timestamp in ratings:
        if user in user_ids and item in item_ids:
            u, i = user_ids[user], item_ids[item]
            observed[u].add(i)
            rows.append((u, i, float(rating >= 3), float(rating >= 4), timestamp))
    rng = random.Random(seed)
    negative_rows = []
    for u, _, _, _, timestamp in rows:
        item = rng.randrange(len(items))
        while item in observed[u]:
            item = rng.randrange(len(items))
        negative_rows.append((u, item, 0.0, 0.0, timestamp))
    rows += negative_rows
    rows.sort(key=lambda row: row[-1])
    cutoff = int(len(rows) * 0.8)
    return rows[:cutoff], rows[cutoff:], len(users), len(items)


def build_multitask_model(kind: str, users: int, items: int, config: MultiTaskConfig):
    torch, nn = require_torch()

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            d = config.dimensions
            self.user = nn.Embedding(users, d)
            self.item = nn.Embedding(items, d)
            width = 2 * d
            if kind == "shared-bottom":
                self.shared = nn.Sequential(nn.Linear(width, d), nn.ReLU())
                self.shared_heads = nn.ModuleList(
                    [nn.Linear(d, 1), nn.Linear(d, 1)]
                )
            if kind in {"clicked-cvr", "esmm"}:
                self.towers = nn.ModuleList(
                    [
                        nn.Sequential(
                            nn.Linear(width, d), nn.ReLU(), nn.Linear(d, 1)
                        )
                        for _ in range(2)
                    ]
                )
            if kind == "mmoe":
                self.experts = nn.ModuleList(
                    [
                        nn.Sequential(nn.Linear(width, d), nn.ReLU())
                        for _ in range(config.experts)
                    ]
                )
                self.gates = nn.ModuleList(
                    [nn.Linear(width, config.experts) for _ in range(2)]
                )
                self.mmoe_heads = nn.ModuleList(
                    [nn.Linear(d, 1), nn.Linear(d, 1)]
                )
            # PLE layer: shared experts plus task-specific experts; each task
            # selects from its own and the shared pool.
            if kind == "ple":
                self.ple_shared = nn.ModuleList(
                    [
                        nn.Sequential(nn.Linear(width, d), nn.ReLU())
                        for _ in range(2)
                    ]
                )
                self.ple_task = nn.ModuleList(
                    [
                        nn.Sequential(nn.Linear(width, d), nn.ReLU())
                        for _ in range(4)
                    ]
                )
                self.ple_gates = nn.ModuleList(
                    [nn.Linear(width, 4) for _ in range(2)]
                )
                self.ple_heads = nn.ModuleList(
                    [nn.Linear(d, 1), nn.Linear(d, 1)]
                )

        def forward(self, user, item):
            x = torch.cat((self.user(user), self.item(item)), dim=-1)
            if kind in {"clicked-cvr", "esmm"}:
                return tuple(tower(x).squeeze(-1) for tower in self.towers)
            if kind == "shared-bottom":
                hidden = self.shared(x)
                return tuple(head(hidden).squeeze(-1) for head in self.shared_heads)
            if kind == "mmoe":
                experts = torch.stack([expert(x) for expert in self.experts], dim=1)
                return tuple(
                    self.mmoe_heads[task](
                        (torch.softmax(self.gates[task](x), -1)[..., None] * experts).sum(1)
                    ).squeeze(-1)
                    for task in range(2)
                )
            if kind == "ple":
                shared = [expert(x) for expert in self.ple_shared]
                outputs = []
                for task in range(2):
                    candidates = torch.stack(
                        [self.ple_task[2 * task](x), self.ple_task[2 * task + 1](x), *shared],
                        dim=1,
                    )
                    mixed = (
                        torch.softmax(self.ple_gates[task](x), -1)[..., None] * candidates
                    ).sum(1)
                    outputs.append(self.ple_heads[task](mixed).squeeze(-1))
                return tuple(outputs)
            raise ValueError(f"unknown multitask model: {kind}")

    return Model()


def _loss(kind, click_logit, conversion_logit, click, conversion):
    torch, _ = require_torch()
    bce = torch.nn.functional.binary_cross_entropy_with_logits
    if kind == "esmm":
        joint = torch.sigmoid(click_logit) * torch.sigmoid(conversion_logit)
        return bce(click_logit, click) + torch.nn.functional.binary_cross_entropy(
            joint.clamp(1e-6, 1 - 1e-6), conversion
        )
    if kind == "clicked-cvr":
        selected = click > 0
        cvr = bce(conversion_logit[selected], conversion[selected]) if selected.any() else 0
        return bce(click_logit, click) + cvr
    return bce(click_logit, click) + bce(conversion_logit, conversion)


def _auc(labels, scores):
    positive = scores[labels == 1]
    negative = scores[labels == 0]
    if not len(positive) or not len(negative):
        return 0.5
    return float(
        ((positive[:, None] > negative[None]).mean()
         + 0.5 * (positive[:, None] == negative[None]).mean())
    )


def _train_and_evaluate(kind, train, validation, users, items, config, seed):
    torch, _ = require_torch()
    from auto_research.runtime import device_for

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    device = device_for(torch)
    model = build_multitask_model(kind, users, items, config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    model.train()
    for _ in range(config.steps):
        batch = [train[rng.randrange(len(train))] for _ in range(config.batch_size)]
        user = torch.tensor([row[0] for row in batch], device=device)
        item = torch.tensor([row[1] for row in batch], device=device)
        click = torch.tensor([row[2] for row in batch], device=device)
        conversion = torch.tensor([row[3] for row in batch], device=device)
        click_logit, conversion_logit = model(user, item)
        loss = _loss(kind, click_logit, conversion_logit, click, conversion)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    model.eval()
    labels = np.asarray([[row[2], row[3]] for row in validation])
    probabilities = []
    with torch.inference_mode():
        for start in range(0, len(validation), 512):
            batch = validation[start : start + 512]
            user = torch.tensor([row[0] for row in batch], device=device)
            item = torch.tensor([row[1] for row in batch], device=device)
            click_logit, conversion_logit = model(user, item)
            click = torch.sigmoid(click_logit)
            conversion = (
                click * torch.sigmoid(conversion_logit)
                if kind in {"esmm", "clicked-cvr"}
                else torch.sigmoid(conversion_logit)
            )
            probabilities.append(torch.stack((click, conversion), -1).cpu().numpy())
    scores = np.concatenate(probabilities)
    eps = 1e-7
    metrics = {
        "click_auc": _auc(labels[:, 0], scores[:, 0]),
        "conversion_auc": _auc(labels[:, 1], scores[:, 1]),
        "click_logloss": float(
            -(labels[:, 0] * np.log(scores[:, 0] + eps)
              + (1 - labels[:, 0]) * np.log(1 - scores[:, 0] + eps)).mean()
        ),
        "conversion_logloss": float(
            -(labels[:, 1] * np.log(scores[:, 1] + eps)
              + (1 - labels[:, 1]) * np.log(1 - scores[:, 1] + eps)).mean()
        ),
    }
    metrics["mean_auc"] = (metrics["click_auc"] + metrics["conversion_auc"]) / 2
    return metrics, {
        "initial_loss": losses[0],
        "final_loss": losses[-1],
        "parameters": sum(parameter.numel() for parameter in model.parameters()),
        "device": device.type,
    }


def run_multitask_reproduction(
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
    config = MultiTaskConfig(
        steps=int(os.environ.get("AUTO_RESEARCH_MULTITASK_STEPS", "200"))
    )
    train, validation, users, items = _examples(dataset_dir, config, seed)
    seeds = (seed, seed + 1, seed + 2)
    metrics, diagnostics = {}, {}
    for kind in (baseline_kind, method_kind):
        runs, traces = [], []
        for run_seed in seeds:
            result, trace = _train_and_evaluate(
                kind, train, validation, users, items, config, run_seed
            )
            runs.append(result)
            traces.append(trace)
        metrics[kind] = {
            key: float(np.mean([run[key] for run in runs])) for key in runs[0]
        } | {
            f"{key}_std": float(np.std([run[key] for run in runs]))
            for key in runs[0]
        }
        diagnostics[kind] = traces
    baseline, method = metrics[baseline_kind], metrics[method_kind]
    return {
        "paper": paper,
        "dataset": {
            "name": "MovieLens-100K entire-space multitask construction",
            "users": users,
            "items": items,
            "train_examples": len(train),
            "validation_examples": len(validation),
        },
        "setup": {"seeds": list(seeds), "steps_per_variant": config.steps},
        "baseline": {"name": baseline_name, **baseline},
        "method": {"name": method_name, **method},
        "relative": {
            "conversion_auc_percent": 100
            * (method["conversion_auc"] - baseline["conversion_auc"])
            / max(abs(baseline["conversion_auc"]), 1e-12),
            "mean_auc_percent": 100
            * (method["mean_auc"] - baseline["mean_auc"])
            / max(abs(baseline["mean_auc"]), 1e-12),
        },
        "training": diagnostics,
        "paper_results": paper_results,
        "scope": scope,
    }


def render_multitask(result):
    baseline, method = result["baseline"], result["method"]
    return "\n".join(
        [
            f"# {result['paper']['title']}",
            "",
            f"{result['dataset']['name']} · seeds {result['setup']['seeds']}",
            "",
            "| Variant | CTR AUC | CTCVR/CVR AUC | Mean AUC | CTR logloss | Conversion logloss |",
            "|---|---:|---:|---:|---:|---:|",
            f"| {baseline['name']} | {baseline['click_auc']:.4f} | {baseline['conversion_auc']:.4f} | {baseline['mean_auc']:.4f} | {baseline['click_logloss']:.4f} | {baseline['conversion_logloss']:.4f} |",
            f"| {method['name']} | {method['click_auc']:.4f} | {method['conversion_auc']:.4f} | {method['mean_auc']:.4f} | {method['click_logloss']:.4f} | {method['conversion_logloss']:.4f} |",
            "",
            f"Conversion AUC relative change: **{result['relative']['conversion_auc_percent']:+.2f}%**.",
            f"Mean task AUC relative change: **{result['relative']['mean_auc_percent']:+.2f}%**.",
            "",
            "## Reproduction boundary",
            "",
            result["scope"],
            "",
        ]
    )
