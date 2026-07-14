import json

from auto_research.reproductions.registry import get_adapter, list_adapters
from auto_research.reproductions.base import ReproductionFidelity
from auto_research.reproductions.reporting import write_reproduction_result


def test_builtin_adapters_are_discoverable():
    assert {adapter.key for adapter in list_adapters()} == {
        "bahe",
        "beque",
        "cluster-goobs",
        "cmsl",
        "din",
        "g2rec",
        "genrank",
        "hstu",
        "hyformer",
        "kar",
        "learn",
        "llatte",
        "longer",
        "lsvcr",
        "lum",
        "m6rec",
        "mdcns",
        "memento",
        "mixformer",
        "msd",
        "notellm",
        "onerec",
        "onerec-v2",
        "onetrans",
        "pinfm",
        "pinrec",
        "plum",
        "precise",
        "rankmixer",
        "rec-distill",
        "self-evolving-rec",
        "sessionrec",
        "sasrec",
        "saviorrec",
        "sis",
        "tiger",
        "transact-v2",
    }
    assert get_adapter("sis").paper.arxiv_id == "2607.04728"
    assert get_adapter("plum").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("onerec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("g2rec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("mixformer").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("rankmixer").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("hyformer").paper.arxiv_id == "2601.12681"
    assert get_adapter("onetrans").paper.arxiv_id == "2510.26104"
    assert get_adapter("rec-distill").paper.arxiv_id == "2605.29755"
    assert get_adapter("din").paper.arxiv_id == "1706.06978"
    assert get_adapter("sasrec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("hstu").paper.arxiv_id == "2402.17152"
    assert get_adapter("tiger").paper.arxiv_id == "2305.05065"
    assert get_adapter("pinfm").paper.arxiv_id == "2507.12704"
    assert get_adapter("transact-v2").paper.arxiv_id == "2506.02267"
    assert get_adapter("m6rec").paper.has_online_ab
    assert get_adapter("onerec-v2").paper.has_online_ab
    assert get_adapter("kar").paper.has_online_ab
    assert get_adapter("bahe").paper.has_online_ab
    assert get_adapter("beque").paper.has_online_ab
    assert get_adapter("genrank").paper.has_online_ab
    assert get_adapter("pinrec").paper.has_online_ab
    assert get_adapter("learn").paper.has_online_ab
    assert get_adapter("notellm").paper.has_online_ab


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
