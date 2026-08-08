from pathlib import Path

from auto_research.reproductions.registry import get_adapter


def test_industrial_p0_has_quantified_online_evidence_and_exact_dates():
    for key in ("dme", "steps", "spear"):
        paper = get_adapter(key).paper
        assert paper.published == "2026-08-03"
        assert paper.has_online_ab
        assert paper.organization
    assert get_adapter("spear").paper.code_url == "https://github.com/mallocagi1-cell/spear"


def test_industrial_p0_executes_distinct_mechanisms():
    for key, diagnostic in (
        ("dme", "cross_conditional_reconstruction_training_only"),
        ("steps", "planning_agent_gated_ordinal_regression"),
        ("spear", "multiplicative_rewrite_gate"),
    ):
        result = get_adapter(key).run(Path("data"), 42)
        assert result["stages"][diagnostic]
        assert result["setup"]["same_split_and_candidates"]


def test_open_language_model_is_a_composable_evolve_architecture():
    paper = get_adapter("open-language-model").paper
    assert paper.published == "2026-07-18"
    assert paper.track == "llm"
    assert paper.code_url == "https://github.com/openlanguagemodel/openlanguagemodel"
    metrics = Path(
        "docs/reproductions/2607.16669-open-language-model/metrics/public-seed42.json"
    ).read_text(encoding="utf-8")
    assert '"ordinary_pytorch_modules": 1.0' in metrics
    assert '"olm_composable"' in metrics
