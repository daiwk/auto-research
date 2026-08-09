"""Isolated reproduction execution with enforceable wall-clock budgets."""

from __future__ import annotations

import multiprocessing as mp
import os
import queue
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .base import ReproductionAdapter


@dataclass(frozen=True)
class ExecutionBudget:
    name: str
    timeout_seconds: int | None


BUDGETS = {
    "smoke": ExecutionBudget("smoke", 300),
    "standard": ExecutionBudget("standard", 3600),
    "paper-specific": ExecutionBudget("paper-specific", None),
}


def run_with_budget(
    adapter: ReproductionAdapter,
    dataset_dir: Path,
    seed: int,
    budget: str,
    timeout_override: int | None = None,
) -> dict[str, Any]:
    """Run an adapter and terminate its process if its declared budget expires.

    ``paper-specific`` preserves the adapter's own training schedule. ``smoke`` and
    ``standard`` add hard wall-clock ceilings. The selected profile is also exposed
    to adapter code through environment variables so adapters can optionally reduce
    their step/data budgets without coupling their public ``run`` signature to CLI.
    """

    if budget not in BUDGETS:
        raise ValueError(f"unknown reproduction budget: {budget}")
    profile = BUDGETS[budget]
    timeout = timeout_override if timeout_override is not None else profile.timeout_seconds
    if timeout is None:
        return adapter.run(dataset_dir, seed)
    if timeout < 1:
        raise ValueError("reproduction timeout must be positive")

    context = mp.get_context("spawn")
    output = context.Queue(maxsize=1)
    process = context.Process(
        target=_adapter_worker,
        args=(adapter, dataset_dir, seed, budget, timeout, output),
        name=f"reproduce-{adapter.key}-seed{seed}",
    )
    process.start()
    process.join(timeout)
    if process.is_alive():
        process.terminate()
        process.join(5)
        if process.is_alive():
            process.kill()
            process.join()
        output.close()
        raise TimeoutError(
            f"{adapter.key} seed {seed} exceeded the {budget} budget ({timeout}s)"
        )
    try:
        kind, payload = output.get(timeout=1)
    except queue.Empty as exc:
        output.close()
        raise RuntimeError(
            f"{adapter.key} seed {seed} worker exited with code {process.exitcode}"
        ) from exc
    if kind == "error":
        output.close()
        raise RuntimeError(payload)
    result = payload
    output.close()
    result.setdefault("execution_budget", {})
    result["execution_budget"].update({
        "profile": budget,
        "hard_timeout_seconds": timeout,
        "isolated_process": True,
    })
    return result


def _adapter_worker(adapter, dataset_dir, seed, budget, timeout, output) -> None:
    os.environ["AUTO_RESEARCH_BUDGET"] = budget
    os.environ["AUTO_RESEARCH_TIMEOUT_SECONDS"] = str(timeout)
    try:
        output.put(("ok", adapter.run(dataset_dir, seed)))
    except BaseException as exc:  # process boundary must serialize every failure
        output.put(("error", f"{type(exc).__name__}: {exc}"))
