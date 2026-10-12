"""Scaled FORTE funnel; no synthetic online traffic or destructive deprecation."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any, Mapping

import numpy as np
import torch
from torch import nn

from auto_research.datasets import MOVIELENS_SHA256, MOVIELENS_URL, movielens_100k


@dataclass(frozen=True)
class Ragged:
    values: torch.Tensor
    offsets: torch.Tensor  # B+1, including the terminal offset


Feature = torch.Tensor | Ragged


def row_count(value: Feature) -> int:
    return len(value.offsets) - 1 if isinstance(value, Ragged) else value.shape[0]


def perturb(value: Feature, order: torch.Tensor | None) -> Feature:
    """Type-correct nulls or within-batch permutations; preserve sparse layout."""
    batch = row_count(value)
    if order is not None and (len(order) != batch or sorted(order.tolist()) != list(range(batch))):
        raise ValueError("order must be a permutation of the batch")
    if isinstance(value, Ragged):
        if order is None:
            return Ragged(value.values[:0], torch.zeros_like(value.offsets))
        chunks = [value.values[value.offsets[i] : value.offsets[i + 1]] for i in order.tolist()]
        sizes = torch.tensor([len(c) for c in chunks], device=value.offsets.device)
        return Ragged(torch.cat(chunks), torch.cat((sizes.new_zeros(1), sizes.cumsum(0))))
    if value.layout == torch.sparse_coo:
        value = value.coalesce()
        if order is None:
            return torch.sparse_coo_tensor(
                value.indices()[:, :0], value.values()[:0], value.shape, device=value.device
            ).coalesce()
        inverse = torch.empty_like(order)
        inverse[order] = torch.arange(batch, device=order.device)
        indices = value.indices().clone()
        indices[0] = inverse[indices[0]]
        return torch.sparse_coo_tensor(
            indices, value.values(), value.shape, device=value.device
        ).coalesce()
    return torch.zeros_like(value) if order is None else value[order]


class VirtualBatch:
    """One materialization and one perturbed dictionary for every experiment."""

    def __init__(self, original: Mapping[str, Feature], *, seed: int, ablate: bool = False):
        if not original:
            raise ValueError("empty feature dictionary")
        self.original = dict(original)
        sizes = {row_count(v) for v in original.values()}
        if len(sizes) != 1:
            raise ValueError("feature batch dimensions disagree")
        first = next(iter(original.values()))
        device = first.values.device if isinstance(first, Ragged) else first.device
        order = (
            None
            if ablate
            else torch.randperm(sizes.pop(), generator=torch.Generator().manual_seed(seed)).to(
                device
            )
        )
        self.perturbed = {k: perturb(v, order) for k, v in original.items()}

    def view(self, group: tuple[str, ...]) -> dict[str, Feature]:
        if not set(group).issubset(self.original):
            raise ValueError("unknown feature")
        return {k: self.perturbed[k] if k in group else v for k, v in self.original.items()}


def signed_change(baseline: float, treatment: float, *, higher_is_better: bool = True) -> float:
    if not np.isfinite([baseline, treatment]).all() or baseline <= 0:
        raise ValueError("normalized change requires finite metrics and a positive baseline")
    return 100 * (1 if higher_is_better else -1) * (treatment - baseline) / baseline


@dataclass(frozen=True)
class TemporalGate:
    max_mean_reliance: float = 1.0
    max_mean_rank: float = 0.5  # normalized rank, weakest=0
    max_rank_std: float = 0.25
    max_slope: float = 0.0
    windows: tuple[int, ...] = (2, 3)

    def select(self, scores: np.ndarray, names: tuple[str, ...]) -> dict[str, dict[str, Any]]:
        """scores[time, head/metric, feature]; all heads AND all lookbacks."""
        if scores.ndim != 3 or scores.shape[2] != len(names) or not np.isfinite(scores).all():
            raise ValueError("expected finite time/head/feature scores")
        if not self.windows or any(w < 2 or w > len(scores) for w in self.windows):
            raise ValueError("every lookback requires at least two actual observations")
        reliance = -scores
        ranks = np.argsort(
            np.argsort(reliance, axis=2, kind="stable"), axis=2, kind="stable"
        ) / max(1, len(names) - 1)
        result = {}
        for j, name in enumerate(names):
            checks = []
            for window in self.windows:
                x = np.arange(window, dtype=float)
                x -= x.mean()
                values = reliance[-window:, :, j]
                means = values.mean(0)
                slope = (values * x[:, None]).sum(0) / np.square(x).sum()
                rank_mean = ranks[-window:, :, j].mean(0)
                rank_std = ranks[-window:, :, j].std(0)
                passed = (
                    (means <= self.max_mean_reliance)
                    & (rank_mean <= self.max_mean_rank)
                    & (rank_std <= self.max_rank_std)
                    & (slope <= self.max_slope + 1e-12)
                )
                checks.append(
                    {
                        "window": window,
                        "mean_reliance": means.tolist(),
                        "slope": slope.tolist(),
                        "mean_rank": rank_mean.tolist(),
                        "rank_std": rank_std.tolist(),
                        "all_heads_pass": bool(passed.all()),
                    }
                )
            result[name] = {"passed": all(c["all_heads_pass"] for c in checks), "checks": checks}
        return result


STAGES = ("dataloader", "dataset", "ingestion", "logging")


class LineageAudit:
    """Audit ledger only: never deletes datasets or infrastructure."""

    def __init__(self, consumers: Mapping[str, set[str]]):
        self.consumers = {k: set(v) for k, v in consumers.items()}
        self.completed: dict[str, list[str]] = {k: [] for k in consumers}

    def retire_consumer(self, feature: str, model: str) -> None:
        self.consumers[feature].discard(model)

    def approve(self, feature: str, stage: str, *, owner_approved: bool) -> None:
        if stage not in STAGES or self.consumers[feature] or not owner_approved:
            raise ValueError("remaining consumers or missing owner approval prevents deprecation")
        if STAGES[len(self.completed[feature]) : len(self.completed[feature]) + 1] != (stage,):
            raise ValueError("deprecation stages must be audited in order")
        self.completed[feature].append(stage)


class FeatureRanker(nn.Module):
    def __init__(self, schema: Mapping[str, tuple[str, int]], *, dimension: int = 12):
        super().__init__()
        self.schema = dict(schema)
        self.blocks = nn.ModuleDict(
            {
                name: nn.EmbeddingBag(width, dimension, mode="mean", include_last_offset=True)
                if kind == "ragged"
                else nn.Linear(width, dimension, bias=False)
                for name, (kind, width) in schema.items()
            }
        )
        self.network = nn.Sequential(
            nn.Linear(dimension * len(schema), 48), nn.ReLU(), nn.Linear(48, 2)
        )

    def forward(self, features: Mapping[str, Feature]) -> torch.Tensor:
        blocks = []
        for name, (kind, _) in self.schema.items():
            value, layer = features[name], self.blocks[name]
            if kind == "ragged":
                blocks.append(layer(value.values, value.offsets))
            elif kind == "sparse":
                blocks.append(torch.sparse.mm(value, layer.weight.T))
            else:
                blocks.append(layer(value))
        return self.network(torch.cat(blocks, dim=1))


def parameter_digest(model: nn.Module) -> str:
    h = hashlib.sha256()
    for name, value in model.state_dict().items():
        h.update(name.encode())
        h.update(value.detach().cpu().contiguous().numpy().tobytes())
    return h.hexdigest()


def binary_metrics(labels: np.ndarray, probabilities: np.ndarray) -> dict[str, float]:
    """Tie-aware empirical ROC-AUC and average precision (step PR integral)."""
    y, p = np.asarray(labels, dtype=int), np.asarray(probabilities, dtype=float)
    positive, negative = int(y.sum()), int((1 - y).sum())
    if not positive or not negative:
        raise ValueError("both classes are required for a paired ROC/AP comparison")
    order = np.argsort(-p, kind="stable")
    y, p = y[order], p[order]
    ends = np.r_[np.flatnonzero(p[:-1] != p[1:]), len(p) - 1]
    tp, fp = np.r_[0, y.cumsum()[ends]], np.r_[0, (1 - y).cumsum()[ends]]
    auc = (
        np.trapezoid(tp / positive, fp / negative)
        if hasattr(np, "trapezoid")
        else np.trapz(tp / positive, fp / negative)
    )
    ap = (np.diff(tp / positive) * tp[1:] / (tp[1:] + fp[1:])).sum()
    return {"roc_auc": float(auc), "pr_auc": float(ap)}


def public_features(
    root: Path, *, limit: int | None = None
) -> tuple[dict[str, list[dict]], dict, dict]:
    rows = sorted(movielens_100k(root), key=lambda r: (r[3], r[0], r[1]))
    if limit:
        rows = rows[:limit]
    users = {
        int(r[0]): r
        for r in (line.split("|") for line in (root / "ml-100k/u.user").read_text().splitlines())
    }
    items = {
        int(r[0]): r
        for r in (
            line.split("|")
            for line in (root / "ml-100k/u.item").read_text(encoding="latin-1").splitlines()
        )
    }
    occupations = {k: i for i, k in enumerate(sorted({u[3] for u in users.values()}))}
    records = [
        {
            "user": user,
            "item": item,
            "age": int(users[user][1]) / 100,
            "occupation": occupations[users[user][3]],
            "genres": [i for i, g in enumerate(items[item][5:]) if g == "1"],
            "timestamp": stamp,
            "targets": [int(rating >= 4), int(rating >= 3)],
        }
        for user, item, rating, stamp in rows
    ]
    a, b = int(len(records) * 0.8), int(len(records) * 0.9)
    if a < 4 or b <= a or b == len(records):
        raise ValueError("dataset is too small")
    origin, span = (
        records[0]["timestamp"],
        max(1, records[a - 1]["timestamp"] - records[0]["timestamp"]),
    )
    for record in records:
        record["time"] = (record["timestamp"] - origin) / span
    schema = {
        "user": ("sparse", max(users) + 1),
        "item": ("sparse", max(items) + 1),
        "occupation": ("sparse", len(occupations)),
        "age": ("dense", 1),
        "time": ("dense", 1),
        "genres": ("ragged", 19),
    }
    digest = hashlib.sha256((root / "ml-100k/u.data").read_bytes()).hexdigest()
    splits = {"train": records[:a], "validation": records[a:b], "test": records[b:]}
    manifest = {
        "dataset": "MovieLens-100K",
        "revision": MOVIELENS_SHA256,
        "source": MOVIELENS_URL,
        "ratings_sha256": digest,
        "split": "chronological 80/10/10; normalization fitted on train timestamps only",
        "counts": {k: len(v) for k, v in splits.items()},
        "limit": limit,
    }
    return splits, schema, manifest


def collate(
    rows: list[dict], schema: Mapping[str, tuple[str, int]], device: str
) -> tuple[dict[str, Feature], torch.Tensor]:
    features = {}
    for name, (kind, width) in schema.items():
        if kind == "dense":
            features[name] = torch.tensor(
                [[r[name]] for r in rows], dtype=torch.float32, device=device
            )
        elif kind == "sparse":
            coordinates = torch.tensor(
                [list(range(len(rows))), [r[name] for r in rows]], device=device
            )
            features[name] = torch.sparse_coo_tensor(
                coordinates, torch.ones(len(rows), device=device), (len(rows), width), device=device
            ).coalesce()
        else:
            chunks = [r[name] for r in rows]
            offsets = np.r_[0, np.cumsum([len(c) for c in chunks])]
            features[name] = Ragged(
                torch.tensor([v for c in chunks for v in c], dtype=torch.long, device=device),
                torch.tensor(offsets, dtype=torch.long, device=device),
            )
    targets = torch.tensor([r["targets"] for r in rows], dtype=torch.float32, device=device)
    return features, targets


def fit(
    rows: list[dict], schema: dict, *, seed: int, device: str, epochs: int, batch_size: int
) -> tuple[FeatureRanker, list[float]]:
    torch.manual_seed(seed)
    model = FeatureRanker(schema).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003)
    rng, losses = np.random.default_rng(seed), []
    model.train()
    for _ in range(epochs):
        order = rng.permutation(len(rows))
        total = 0.0
        for start in range(0, len(rows), batch_size):
            batch = [rows[i] for i in order[start : start + batch_size]]
            features, targets = collate(batch, schema, device)
            loss = nn.functional.binary_cross_entropy_with_logits(model(features), targets)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total += loss.item() * len(batch)
        losses.append(total / len(rows))
    model.eval()
    return model, losses


@torch.no_grad()
def evaluate(
    model: FeatureRanker,
    rows: list[dict],
    *,
    device: str,
    batch_size: int,
    groups: tuple[tuple[str, ...], ...] = ((),),
    seed: int = 42,
    ablate: bool = False,
) -> list[dict[str, float]]:
    model.eval()
    predictions = [[] for _ in groups]
    targets = []
    before = parameter_digest(model)
    for start in range(0, len(rows), batch_size):
        original, labels = collate(rows[start : start + batch_size], model.schema, device)
        virtual = VirtualBatch(original, seed=seed + start, ablate=ablate)
        targets.append(labels.cpu().numpy())
        for i, group in enumerate(groups):
            predictions[i].append(model(virtual.view(group)).sigmoid().cpu().numpy())
    if parameter_digest(model) != before:
        raise RuntimeError("paired perturbation mutated the frozen checkpoint")
    labels = np.concatenate(targets)
    results = []
    for chunks in predictions:
        probabilities = np.concatenate(chunks)
        results.append(
            {
                f"head{h}.{metric}": value
                for h in range(2)
                for metric, value in binary_metrics(labels[:, h], probabilities[:, h]).items()
            }
        )
    return results


def run_forte(
    dataset_dir: Path,
    seed: int = 42,
    *,
    device: str = "cpu",
    epochs: int = 6,
    batch_size: int = 512,
    limit: int | None = None,
    guardrail_percent: float = 1.0,
) -> dict[str, Any]:
    if epochs < 1 or batch_size < 2 or guardrail_percent < 0:
        raise ValueError("invalid training/guardrail budget")
    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA requested but unavailable")
    splits, schema, manifest = public_features(Path(dataset_dir), limit=limit)
    model, losses = fit(
        splits["train"], schema, seed=seed, device=device, epochs=epochs, batch_size=batch_size
    )
    names = tuple(schema)
    temporal, metric_names = [], None
    for day, indices in enumerate(np.array_split(np.arange(len(splits["validation"])), 3)):
        records = [splits["validation"][i] for i in indices]
        result = evaluate(
            model,
            records,
            device=device,
            batch_size=batch_size,
            groups=((),) + tuple((n,) for n in names),
            seed=seed + day,
        )
        metric_names = tuple(result[0])
        temporal.append(
            [[signed_change(result[0][m], row[m]) for row in result[1:]] for m in metric_names]
        )
    temporal_scores = np.asarray(temporal)
    gate = TemporalGate().select(temporal_scores, names)
    ranked = sorted(names, key=lambda n: float(-temporal_scores[:, :, names.index(n)].mean()))
    # Failed gates remain failed. Experimental weakest-feature arms below also
    # run to expose interactions, but cannot be proposed as validated retirements.
    groups = tuple(tuple(ranked[:size]) for size in range(1, min(3, len(names) - 1) + 1))
    paired = evaluate(
        model,
        splits["validation"],
        device=device,
        batch_size=batch_size,
        groups=((),) + groups,
        seed=seed,
        ablate=True,
    )
    trials, candidates = [], {(): model}
    for group, perturbation_metrics in zip(groups, paired[1:]):
        reduced = {k: v for k, v in schema.items() if k not in group}
        candidate, trace = fit(
            splits["train"], reduced, seed=seed, device=device, epochs=epochs, batch_size=batch_size
        )
        validation = evaluate(
            candidate, splits["validation"], device=device, batch_size=batch_size
        )[0]
        deltas = {k: signed_change(paired[0][k], validation[k]) for k in validation}
        ablation_deltas = {
            k: signed_change(paired[0][k], perturbation_metrics[k]) for k in validation
        }
        passed = (
            all(gate[n]["passed"] for n in group)
            and min(ablation_deltas.values()) >= -guardrail_percent
            and min(deltas.values()) >= -guardrail_percent
        )
        trials.append(
            {
                "removed": list(group),
                "temporal_passed": all(gate[n]["passed"] for n in group),
                "ablation_change_percent": ablation_deltas,
                "validation": validation,
                "validation_change_percent": deltas,
                "eligible": passed,
                "train_loss": trace,
                "parameters": sum(p.numel() for p in candidate.parameters()),
            }
        )
        candidates[group] = candidate
    eligible = [t for t in trials if t["eligible"]]
    selected = tuple(max(eligible, key=lambda t: len(t["removed"]))["removed"]) if eligible else ()
    # Test is evaluated once only after validation has made the selection.
    test = evaluate(candidates[selected], splits["test"], device=device, batch_size=batch_size)[0]
    lineage = LineageAudit({n: {"local-incumbent"} for n in names})
    for name in selected:
        lineage.retire_consumer(name, "local-incumbent")
    return {
        "schema_version": 2,
        "adapter": "forte",
        "seed": seed,
        "dataset": manifest,
        "evaluation_tier": "l2_public_dataset",
        "diagnostic_only": True,
        "baseline": {
            "validation": paired[0],
            "train_loss": losses,
            "parameters": sum(p.numel() for p in model.parameters()),
            "checkpoint_sha256": parameter_digest(model),
        },
        "temporal": {
            "metric_names": metric_names,
            "scores": temporal_scores.tolist(),
            "gate": gate,
        },
        "trials": trials,
        "selected_removed": list(selected),
        "test": test,
        "lineage": {
            "remaining_consumers": {k: sorted(v) for k, v in lineage.consumers.items()},
            "completed_stages": lineage.completed,
            "owner_review_pending": list(selected),
            "online_ab": "not run; public offline data does not authorize production removal",
        },
        "hardware": {
            "device": device,
            "accelerator": torch.cuda.get_device_name(0) if device == "cuda" else device,
        },
        "omitted": [
            "Pinterest checkpoints/private multimodal features",
            "distributed fleet sensors",
            "real online A/B and manual infrastructure removal",
        ],
    }
