"""CPU-only, public WikiText-2 mechanism run for the small KITE/SST model.

Usage: PYTHONPATH=src python scripts/run_kite_sst.py --data-root data
The fixed split/budget is diagnostic, not the paper's 67B scaling result.
"""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import statistics
import time

import torch
from torch.nn import functional as F

from auto_research.datasets import wikitext_2
from auto_research.foundation_models.kite_sst import SmallSST, train_two_stages


def _batch(text: str, *, seed: int, batch_size: int, sequence: int) -> torch.Tensor:
    values = torch.tensor(list(text.encode("utf-8")), dtype=torch.long)
    generator = torch.Generator().manual_seed(seed)
    starts = torch.randint(0, len(values) - sequence - 1, (batch_size,), generator=generator)
    return torch.stack([values[index:index + sequence + 1] for index in starts])


def _nll(model: SmallSST, batch: torch.Tensor) -> float:
    model.eval()
    with torch.no_grad():
        logits, _ = model(batch[:, :-1])
        return float(F.cross_entropy(logits.reshape(-1, 256), batch[:, 1:].reshape(-1)))


def _source_control(model: SmallSST, batch: torch.Tensor, budgets: tuple[int, int]) -> None:
    """Same examples, number of updates, and optimizer restart as the two-stage SST."""
    inputs, labels = batch[:, :-1], batch[:, 1:]
    for steps in budgets:
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
        for _ in range(steps):
            logits, _ = model(inputs)
            loss = F.cross_entropy(logits.reshape(-1, 256), labels.reshape(-1))
            optimizer.zero_grad(set_to_none=True)
            loss.backward()
            optimizer.step()


def run(*, data_root: Path, seeds: tuple[int, ...], source_steps: int,
        continuation_steps: int) -> dict:
    if not seeds or source_steps < 1 or continuation_steps < 1:
        raise ValueError("nonempty seeds and positive budgets required")
    torch.set_num_threads(min(torch.get_num_threads(), 2))
    corpus = wikitext_2(data_root, allow_network=False)
    revisions = {name: hashlib.sha256(value.encode()).hexdigest()
                 for name, value in corpus.items()}
    runs = []
    for seed in seeds:
        torch.manual_seed(seed)
        model = SmallSST(256, width=32, layers=2, max_positions=64).cpu()
        control = deepcopy(model)
        train = _batch(corpus["train"], seed=seed, batch_size=8, sequence=32)
        validation = _batch(corpus["validation"], seed=seed + 1000, batch_size=64, sequence=32)
        test = _batch(corpus["test"], seed=seed + 2000, batch_size=64, sequence=32)
        source_validation = _nll(model, validation)
        started = time.perf_counter()
        losses = train_two_stages(model, train, source_steps=source_steps,
                                  continuation_steps=continuation_steps)
        train_seconds = time.perf_counter() - started
        _source_control(control, train, (source_steps, continuation_steps))
        validation_nll = _nll(model, validation)
        control_validation_nll = _nll(control, validation)
        test_nll = _nll(model, test)  # never used for selection
        control_test_nll = _nll(control, test)
        prompt = validation[:1, :32]
        model.eval()
        with torch.no_grad():
            dense, _ = model(prompt)
            last, _ = model(prompt, last_only=True)
        runs.append({
            "seed": seed,
            "source_validation_nll_untrained": source_validation,
            "expanded_validation_nll": validation_nll,
            "expanded_test_nll": test_nll,
            "source_control_validation_nll": control_validation_nll,
            "source_control_test_nll": control_test_nll,
            "expanded_parameters": sum(p.numel() for p in model.parameters()),
            "source_control_parameters": sum(p.numel() for p in control.parameters()),
            "last_only_max_logit_error": float((dense[:, -1:] - last).abs().max()),
            "train_seconds_cpu": train_seconds,
            **losses,
        })
    return {
        "paper": "KITE arXiv:2609.27294",
        "status": "diagnostic_only",
        "device": "cpu",
        "dataset": "WikiText-2 raw; fixed 32-byte contexts",
        "dataset_sha256": revisions,
        "source_steps": source_steps,
        "continuation_steps": continuation_steps,
        "model": "2+2 layer dense SST; width=32; byte vocabulary=256",
        "runs": runs,
        "validation_nll_mean": statistics.mean(item["expanded_validation_nll"] for item in runs),
        "test_nll_mean": statistics.mean(item["expanded_test_nll"] for item in runs),
        "source_control_validation_nll_mean": statistics.mean(
            item["source_control_validation_nll"] for item in runs),
        "source_control_test_nll_mean": statistics.mean(
            item["source_control_test_nll"] for item in runs),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, default=Path("data"))
    parser.add_argument("--seeds", default="42,43,44")
    parser.add_argument("--source-steps", type=int, default=30)
    parser.add_argument("--continuation-steps", type=int, default=30)
    args = parser.parse_args()
    print(json.dumps(run(data_root=args.data_root,
                         seeds=tuple(int(value) for value in args.seeds.split(",")),
                         source_steps=args.source_steps,
                         continuation_steps=args.continuation_steps), indent=2))
