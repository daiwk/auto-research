import json

from auto_research.reproductions.registry import get_adapter, list_adapters
from auto_research.reproductions.base import ReproductionFidelity
from auto_research.reproductions.reporting import write_reproduction_result


def test_builtin_adapters_are_discoverable():
    assert {adapter.key for adapter in list_adapters()} == {
        "cluster-goobs",
        "cmsl",
        "g2rec",
        "llatte",
        "longer",
        "mdcns",
        "memento",
        "mixformer",
        "onerec",
        "plum",
        "self-evolving-rec",
        "sis",
    }
    assert get_adapter("sis").paper.arxiv_id == "2607.04728"
    assert get_adapter("plum").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("onerec").fidelity is ReproductionFidelity.CONCEPT_DEMO
    assert "iterative DPO" in get_adapter("onerec").omitted_core_components


def test_each_result_gets_an_isolated_artifact_directory(tmp_path):
    adapter = get_adapter("sis")
    result = {
        "paper": adapter.paper.to_dict(),
        "dataset": "fixture",
        "baseline": {
            "method": "is",
            "weight_variance": 1.0,
            "mean_abs_log_ratio": 1.0,
            "effective_sample_size": 1.0,
            "acceptance_rate": 0.0,
        },
        "method": {
            "method": "sis",
            "weight_variance": 0.5,
            "mean_abs_log_ratio": 0.5,
            "effective_sample_size": 2.0,
            "acceptance_rate": 0.5,
        },
        "variance_reduction_percent": 50.0,
    }
    report = write_reproduction_result(adapter, result, tmp_path, "fixed-run")
    assert report == tmp_path / "2607.04728-sis" / "fixed-run" / "report.md"
    assert json.loads((report.parent / "result.json").read_text())["dataset"] == "fixture"
    payload = json.loads((report.parent / "result.json").read_text())
    assert payload["reproduction_fidelity"]["level"] == "core_mechanism"
    assert "核心机制复现" in report.read_text()
