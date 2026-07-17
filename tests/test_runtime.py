from __future__ import annotations

from types import SimpleNamespace

import pytest

from auto_research.cli import build_parser
from auto_research.runtime import configure_runtime, device_for


class _FakeCuda:
    def __init__(self, available=False, count=0):
        self._available = available
        self._count = count

    def is_available(self):
        return self._available

    def device_count(self):
        return self._count


class _FakeMPS:
    def __init__(self, available=False):
        self._available = available

    def is_available(self):
        return self._available


class _FakeTorch:
    def __init__(self, cuda=False, cuda_count=0, mps=False):
        self.cuda = _FakeCuda(cuda, cuda_count)
        self.backends = SimpleNamespace(mps=_FakeMPS(mps))
        self.threads = None

    def device(self, value):
        return value

    def set_num_threads(self, value):
        self.threads = value


def test_auto_device_priority_is_cuda_then_mps_then_cpu(monkeypatch):
    monkeypatch.delenv("AUTO_RESEARCH_DEVICE", raising=False)
    assert device_for(_FakeTorch(cuda=True, cuda_count=1, mps=True)) == "cuda"
    assert device_for(_FakeTorch(mps=True)) == "mps"
    assert device_for(_FakeTorch()) == "cpu"


def test_explicit_device_fails_instead_of_silently_falling_back(monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cuda:1")
    with pytest.raises(RuntimeError, match="only 1 CUDA device"):
        device_for(_FakeTorch(cuda=True, cuda_count=1))
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "mps")
    with pytest.raises(RuntimeError, match="MPS is unavailable"):
        device_for(_FakeTorch())


def test_linux_cpu_thread_setting_is_applied(monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    monkeypatch.setenv("AUTO_RESEARCH_CPU_THREADS", "6")
    torch = _FakeTorch()
    assert device_for(torch) == "cpu"
    assert torch.threads == 6


def test_all_training_commands_expose_the_same_runtime_flags():
    parser = build_parser()
    reproduce = parser.parse_args(["reproduce", "--paper", "din", "--device", "cuda:0"])
    evolve = parser.parse_args([
        "evolve", "--model", "rankmixer", "--dataset", "movielens-100k",
        "--direction", "test", "--device", "cpu", "--cpu-threads", "8",
    ])
    run = parser.parse_args(["run", "--topic", "test", "--track", "llm", "--device", "mps"])
    assert reproduce.device == "cuda:0"
    assert evolve.device == "cpu" and evolve.cpu_threads == 8
    assert run.device == "mps"


def test_configure_runtime_rejects_invalid_values(monkeypatch):
    monkeypatch.delenv("AUTO_RESEARCH_DEVICE", raising=False)
    with pytest.raises(ValueError, match="device must be"):
        configure_runtime("tpu")


def test_cli_default_preserves_an_explicit_environment_device(monkeypatch):
    monkeypatch.setenv("AUTO_RESEARCH_DEVICE", "cpu")
    configure_runtime(None, 3)
    assert device_for(_FakeTorch()) == "cpu"
