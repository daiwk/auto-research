import pytest

from scripts.benchmark_kite_gpu_latency import run


def test_gpu_benchmark_rejects_cpu_host_without_claiming_result(monkeypatch):
    import torch

    monkeypatch.setattr(torch.cuda, "is_available", lambda: False)
    with pytest.raises(RuntimeError, match="real NVIDIA"):
        run()
