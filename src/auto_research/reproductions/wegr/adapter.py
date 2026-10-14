"""WeGR public-data binding; no substitution of paper metrics."""
from pathlib import Path

from auto_research.paper_specs.runtime import adapter_from_spec


def reproduce(dataset_dir: Path, seed: int):
    import os
    import torch
    from auto_research.runtime import DEVICE_ENV, device_for
    from .experiment import run
    requested = os.environ.get(DEVICE_ENV, "auto")
    if requested == "auto":
        requested = "cuda" if torch.cuda.is_available() else "cpu"
    device = device_for(torch, requested)
    if device.type not in {"cpu", "cuda"}:
        raise ValueError("WeGR diagnostic supports CPU/CUDA; request --device cpu on Mac")
    return run(dataset_dir, seed, device=str(device))


def render(result):
    from .experiment import render as render_result
    return render_result(result)


ADAPTER = adapter_from_spec("wegr", run=reproduce, render=render)
