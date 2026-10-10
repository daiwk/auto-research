"""Delivery contracts for the accepted twelve-paper October batch."""

import json
from pathlib import Path

from auto_research.gpu_validation import STANDALONE_GPU_RECEIPTS, validate_gpu_receipt


ROOT = Path(__file__).resolve().parents[1]
KEYS = {
    "dial-opd", "meta-opd", "mass", "race", "grpo-dropout",
    "residual-advantage", "semi-opd", "elastic-expert-routing", "vimod",
    "hippocam", "evoalloc", "jev-capability",
}


def test_oct10_batch_has_documents_and_real_gpu_evidence():
    specs = {}
    for path in (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json"):
        spec = json.loads(path.read_text())
        if spec["key"] in KEYS:
            specs[spec["key"]] = spec
    assert set(specs) == KEYS
    for key, spec in specs.items():
        assert spec["published"] == "2026-10-08"
        assert spec["requires_gpu_validation"] is True
        artifact = spec["gpu_validation_artifact"]
        assert STANDALONE_GPU_RECEIPTS[key] == artifact
        receipt = json.loads((ROOT / artifact).read_text())
        assert receipt["adapter_key"] == key
        assert not validate_gpu_receipt(receipt)
        text = (ROOT / "docs" / spec["detail_path"]).read_text()
        for field in ("论文信息", "论文链接", "原作者", "Adapter", "代码"):
            assert field in text, (key, field)
        assert "2026-10-08" in text
        assert spec["paper_url"] in text


def test_oct10_papers_are_visible_in_all_domain_browse_dimensions():
    specs = [json.loads(path.read_text()) for path in
             (ROOT / "src/auto_research/paper_specs/catalog").glob("*/*.json")]
    for spec in specs:
        if spec["key"] not in KEYS:
            continue
        domain = ROOT / "docs" / spec["domain"]
        for dimension in ("organization", "topic", "year"):
            text = (domain / "catalog" / f"by-{dimension}.md").read_text()
            assert f"`{spec['key']}`" in text, (spec["key"], dimension)
