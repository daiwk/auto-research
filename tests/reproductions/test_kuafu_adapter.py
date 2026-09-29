"""KuaFu is registered as a bounded CUDA diagnostic, not a claimed A/B replay."""

from pathlib import Path

import pytest

from auto_research.reproductions.base import ReproductionFidelity
from auto_research.reproductions.registry import get_adapter


def test_kuafu_registration_and_private_data_boundary(monkeypatch) -> None:
    adapter = get_adapter("kuafu")
    assert adapter.paper.arxiv_id == "2609.31045"
    assert adapter.paper.has_online_ab
    assert adapter.fidelity is ReproductionFidelity.CONCEPT_DEMO
    assert adapter.requires_gpu_validation
    assert adapter.device_capabilities == ("cuda",)
    monkeypatch.delenv("AUTO_RESEARCH_KUAFU_CHECKPOINT", raising=False)
    with pytest.raises(RuntimeError, match="AUTO_RESEARCH_KUAFU_CHECKPOINT"):
        adapter.run(Path("data"), 42)
