from __future__ import annotations

import os
import platform
from typing import Any


DEVICE_ENV = "AUTO_RESEARCH_DEVICE"
CPU_THREADS_ENV = "AUTO_RESEARCH_CPU_THREADS"


def configure_runtime(device: str | None = None, cpu_threads: int | None = None) -> None:
    """Configure the process and all child experiment processes."""
    normalized = (device or os.environ.get(DEVICE_ENV, "auto")).strip().lower()
    if normalized != "auto" and not (
        normalized == "cpu" or normalized == "mps" or normalized == "cuda"
        or normalized.startswith("cuda:")
    ):
        raise ValueError("device must be auto, cpu, mps, cuda or cuda:<index>")
    if device is None:
        os.environ.setdefault(DEVICE_ENV, normalized)
    else:
        os.environ[DEVICE_ENV] = normalized
    if cpu_threads is not None:
        if cpu_threads < 1:
            raise ValueError("cpu threads must be positive")
        os.environ[CPU_THREADS_ENV] = str(cpu_threads)


def device_for(torch: Any, requested: str | None = None):
    """Resolve one explicit or automatically detected PyTorch device.

    Automatic priority is CUDA, Apple MPS, then CPU. An explicitly requested
    unavailable accelerator fails early instead of silently running on CPU.
    """
    choice = (requested or os.environ.get(DEVICE_ENV, "auto")).strip().lower()
    if choice == "auto":
        if torch.cuda.is_available():
            choice = "cuda"
        elif getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            choice = "mps"
        else:
            choice = "cpu"
    if choice.startswith("cuda"):
        if not torch.cuda.is_available():
            raise RuntimeError(f"requested {choice}, but CUDA is unavailable in this PyTorch build")
        if ":" in choice:
            index = int(choice.split(":", 1)[1])
            if index < 0 or index >= torch.cuda.device_count():
                raise RuntimeError(f"requested {choice}, but only {torch.cuda.device_count()} CUDA device(s) are visible")
    elif choice == "mps":
        if not (getattr(torch.backends, "mps", None) and torch.backends.mps.is_available()):
            raise RuntimeError("requested mps, but Apple MPS is unavailable")
    elif choice != "cpu":
        raise ValueError("device must be auto, cpu, mps, cuda or cuda:<index>")
    if choice == "cpu":
        threads = os.environ.get(CPU_THREADS_ENV)
        if threads:
            torch.set_num_threads(int(threads))
    return torch.device(choice)


def runtime_summary(torch: Any | None = None) -> dict[str, Any]:
    result: dict[str, Any] = {
        "requested_device": os.environ.get(DEVICE_ENV, "auto"),
        "cpu_threads": int(os.environ[CPU_THREADS_ENV]) if os.environ.get(CPU_THREADS_ENV) else None,
        "platform": platform.platform(),
    }
    if torch is not None:
        device = device_for(torch)
        result.update({"resolved_device": str(device), "torch_version": torch.__version__})
        if device.type == "cuda":
            result["accelerator"] = torch.cuda.get_device_name(device)
            result["cuda_version"] = torch.version.cuda
        elif device.type == "mps":
            result["accelerator"] = "Apple Metal Performance Shaders"
        else:
            result["accelerator"] = platform.processor() or platform.machine()
    return result
