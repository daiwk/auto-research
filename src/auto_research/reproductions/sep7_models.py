"""Trainable category-conditioned retrieval and an offline evidence controller."""
from copy import deepcopy
import json
import math
from pathlib import Path

import numpy as np
import torch
from torch import nn
from torch.nn import functional as F


class CategoryTwoTower(nn.Module):
    """Shared content encoder, category adapter and category reconstruction."""
    def __init__(self, feature_dim, categories, dim=32, adapter=True):
        super().__init__()
        self.category = nn.Embedding(categories, dim)
        self.encoder = nn.Sequential(nn.Linear(feature_dim + dim, dim), nn.ReLU(), nn.Linear(dim, dim))
        self.adapter = nn.Linear(2 * dim, dim) if adapter else None
        self.reconstruction = nn.Linear(dim, dim)

    def encode(self, features, categories):
        return F.normalize(self.encoder(torch.cat((features, self.category(categories)), -1)), dim=-1)

    def query(self, features, categories, requested):
        base = self.encode(features, categories)
        return base if self.adapter is None else F.normalize(
            self.adapter(torch.cat((base, self.category(requested)), -1)), dim=-1)

    def objective(self, features, categories, source, target, negatives, temperature=0.1):
        query = self.query(features[source], categories[source], categories[target])
        # All in-batch positives plus uniform catalog negatives: mixed sampling.
        candidates = torch.cat((target, negatives))
        scores = query @ self.encode(features[candidates], categories[candidates]).T / temperature
        # Repeated positives must not be false negatives.
        positives = target[:, None] == candidates[None, :]
        retrieval = (torch.logsumexp(scores, -1)
                     - torch.logsumexp(scores.masked_fill(~positives, -torch.inf), -1)).mean()
        auxiliary = F.cross_entropy(self.reconstruction(query) @ self.category.weight.T,
                                    categories[target]) if self.adapter is not None else retrieval * 0
        return retrieval + auxiliary


def train_two_tower(data, seed, adapter=True, steps=80):
    """Train solely on train adjacency; public genres stand in for categories."""
    with torch.random.fork_rng():
        torch.manual_seed(seed)
        model = CategoryTwoTower(data.sequences.features.shape[1], int(data.domains.max()) + 1,
                                 adapter=adapter)
        features = torch.tensor(data.sequences.features, dtype=torch.float32)
        categories = torch.tensor(data.domains, dtype=torch.long)
        pairs = torch.tensor([(a, b) for history in data.sequences.train
                              for a, b in zip(history, history[1:])], dtype=torch.long)
        if not len(pairs):
            raise ValueError("training pairs required")
        generator = torch.Generator().manual_seed(seed)
        optimizer = torch.optim.Adam(model.parameters(), lr=0.003)
        losses = []
        for _ in range(steps):
            batch = pairs[torch.randint(len(pairs), (64,), generator=generator)]
            negatives = torch.randint(data.item_count, (64,), generator=generator)
            optimizer.zero_grad()
            loss = model.objective(features, categories, batch[:, 0], batch[:, 1], negatives)
            loss.backward()
            optimizer.step()
            losses.append(float(loss.detach()))
        model.eval()
        with torch.no_grad():
            targets = model.encode(features, categories)
            table = torch.empty(data.item_count, data.item_count)
            # Score requested categories independently; no held-out target
            # category is supplied to the query at inference.
            for category in categories.unique():
                selected = categories == category
                queries = model.query(features, categories, category.expand(len(features)))
                table[:, selected] = queries @ targets[selected].T
        return table.numpy(), {"steps": steps, "first_loss": losses[0], "last_loss": losses[-1],
                               "train_pairs": len(pairs), "seed": seed}


class EvidenceController:
    """AutoLR offline state/guardrail core; online authority is never granted.

    Candidates and independent council reviews are supplied artifacts, not
    fabricated LLM research. A fixed reference prevents an implicit KEEP ratchet.
    """
    def __init__(self, reference, ledger_path=None):
        self.reference = deepcopy(reference)
        self.ledger_path = Path(ledger_path) if ledger_path else None
        self.records = []
        self.incumbent = "baseline"
        if self.ledger_path and self.ledger_path.exists():
            payload = json.loads(self.ledger_path.read_text())
            if payload["reference"] != self.reference:
                raise ValueError("reference contract changed")
            self.records, self.incumbent = payload["records"], payload["incumbent"]

    def select(self, candidates):
        seen = {row["candidate"] for row in self.records}
        legal = [c for c in candidates if c["key"] not in seen and c.get("evidence")
                 and len(c.get("reviews", [])) >= 2 and all(r["feasible"] for r in c["reviews"])]
        if not legal:
            return None
        def score(candidate):
            values = [float(r["score"]) for r in candidate["reviews"]]
            if not all(math.isfinite(v) for v in values):
                raise ValueError("nonfinite council score")
            return (float(np.mean(values)) + 0.1 * float(np.std(values)), candidate["key"])
        return max(legal, key=score)

    def evaluate(self, candidate, execute, guardrails):
        events = ["selected", "verified"]
        try:
            metrics = execute(candidate)
            events.append("offline-evaluated")
            if not all(math.isfinite(float(v)) for v in metrics.values()):
                raise ValueError("nonfinite metrics")
            protected = all(metrics[k] >= lower for k, lower in guardrails.items())
            improved = metrics["ndcg_at_10"] > self.reference["ndcg_at_10"]
            verdict = "packaged-for-human-review" if protected and improved else "rejected"
            if verdict == "packaged-for-human-review":
                prior = [r["metrics"]["ndcg_at_10"] for r in self.records
                         if r["verdict"] == verdict]
                if metrics["ndcg_at_10"] > max(prior, default=self.reference["ndcg_at_10"]):
                    self.incumbent = candidate["key"]
        except (ValueError, KeyError, RuntimeError) as error:
            metrics, verdict = {}, "failed"
            events.append(type(error).__name__)
        row = {"candidate": candidate["key"], "events": [*events, verdict],
               "metrics": metrics, "verdict": verdict, "evidence": candidate["evidence"],
               "reviews": deepcopy(candidate["reviews"]), "online_authorized": False}
        self.records.append(row)
        if self.ledger_path:
            self.ledger_path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.ledger_path.with_suffix(".tmp")
            temporary.write_text(json.dumps({"reference": self.reference, "records": self.records,
                                             "incumbent": self.incumbent}, indent=2) + "\n")
            temporary.replace(self.ledger_path)
        return row
