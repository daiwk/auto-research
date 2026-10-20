"""Historical priority papers stay references, not invented executable adapters."""

from __future__ import annotations

import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "src/auto_research/paper_specs/catalog"
EXPECTED = {
    "code-optimization-rl": ("post-training", "2607.25970", "2026-07-28"),
    "autoformbot": ("agent-research", "2605.29955", "2026-05-28"),
    "airs-bench": ("agent-research", "2602.06855", "2026-02-06"),
    "metaencoder": ("foundation-models", "2610.11316", "2026-10-08"),
    "raw-video-midtraining": ("multimodal-models", "2610.11019", "2026-10-08"),
    "mad-rl": ("post-training", "2609.31644", "2026-09-12"),
}


@pytest.mark.parametrize("key", EXPECTED)
def test_meta_backfill_has_honest_non_executable_cost_terminal(key):
    domain, arxiv_id, published = EXPECTED[key]
    row = json.loads((CATALOG / domain / f"{key}.json").read_text())
    assert row["key"] == key and row["domain"] == domain
    assert arxiv_id in row["paper_url"]
    assert row["published"] == published
    assert row["published_at"].startswith(published)
    assert row["first_author"] and "Meta" in row["first_author_affiliation"]
    assert row["adapter"] is None
    assert row["implementation_status"] == "deferred_high_cost"
    assert row["review_done"] is True
    assert row["review_resolution"] == "not_reproduced_high_cost"
    assert row["full_experiment_status"] == "not_reproduced_high_cost"
    assert "不复现（审查 DONE）" in row["deferral_reason"]
    assert row["requires_gpu_validation"] is False
    assert row["gpu_validation_passed"] is False
    assert row["evolve_integrated"] is False
    assert row["promotion_eligible"] is False
    assert not row.get("gpu_validation_artifact")
    assert not row.get("local_command") and not row.get("local_operator")
    document = (ROOT / "docs" / row["detail_path"]).read_text()
    for label in ("论文信息", "论文链接", "公司 / 机构", "首次公开日期", "本地复现代码"):
        assert label in document
    assert "不复现（审查 DONE）" in document


def test_mad_rl_linkage_does_not_rebind_existing_cuda_receipt():
    receipt = json.loads(
        (ROOT / "docs/gpu-validations/mad-rl-qwen-choice-a100-20260929.json").read_text()
    )
    assert receipt["adapter_key"] == "mad-rl-qwen-choice"
    document = (ROOT / "docs/experiments/mad-rl-mechanism.md").read_text()
    assert "2026-09-12 11:12:59 UTC" in document
    assert "mad-rl-qwen-choice" in document
    assert "不重新绑定" in document
    assert "三臂验证完全打平" in document


@pytest.mark.parametrize(
    "relative",
    [
        "agent-research/2605.29955-autoformbot",
        "foundation-models/2610.11316-metaencoder",
        "multimodal-models/2610.11019-raw-video-midtraining",
    ],
)
def test_captured_primary_figures_are_local_pngs(relative):
    path = ROOT / "docs" / relative / "assets/paper-figure-01.png"
    assert path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    assert path.stat().st_size > 10_000
