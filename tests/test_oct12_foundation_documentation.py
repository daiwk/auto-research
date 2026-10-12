"""Five-paper metadata and honest-evidence contracts (no GPU receipt fixture)."""
import json
import re
import struct
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPERS = {
    "msar": ("2610.13630", "2026-10-09", "foundation-models"),
    "orthros": ("2610.13735", "2026-10-09", "foundation-models"),
    "dualquant": ("2610.13767", "2026-10-09", "foundation-models"),
    "woven": ("2610.12417", "2026-10-08", "multimodal-models"),
    "umrm": ("2610.12707", "2026-10-08", "multimodal-models"),
}
FIRST_AUTHOR_INSTITUTION = {
    "msar": "Shanghai Jiao Tong University",
    "orthros": "The Hong Kong Polytechnic University",
    "dualquant": "d-Matrix",
    "woven": "Northwestern University",
    "umrm": "Massachusetts Institute of Technology",
}


@pytest.mark.parametrize("key", PAPERS)
def test_oct12_five_paper_metadata_figures_and_diagnostic_contract(key):
    identifier, date, domain = PAPERS[key]
    package = ROOT / "src/auto_research/reproductions" / key
    spec = json.loads((package / "paper.yaml").read_text())
    catalog = json.loads((ROOT / "src/auto_research/paper_specs/catalog" / domain / f"{key}.json").read_text())
    directory = ROOT / "docs/reproductions" / f"{identifier}-{key}"
    text = (directory / "README.md").read_text()
    assert spec["arxiv_id"] == identifier and spec["published"] == date
    assert spec["fidelity"] == "core_mechanism" and spec["evaluation_tier"] == "l1_mechanism"
    assert spec["execution"]["requires_gpu_validation"] is True
    assert catalog["gpu_validation_artifact"] == spec["execution"]["gpu_validation_artifact"]
    assert catalog["first_author_affiliation"] == FIRST_AUTHOR_INSTITUTION[key]
    assert spec["evolve_operators"] == []
    for required in ("## 论文信息", f"[arXiv {identifier}](https://arxiv.org/abs/{identifier})",
                     "| 公司/机构 |", f"| 首次公开日期 | {date}（arXiv v1） |",
                     "| 原文开源代码 |", f"| Adapter | `{key}` |",
                     f"src/auto_research/reproductions/{key}/", "## 原始论文总结",
                     "### 核心公式", "### 论文离线与线上效果", "## 本地复现",
                     "```mermaid", "版权归原作者所有"):
        assert required in text
    assert re.search(r"^\| 原文开源代码 \| (?:是：\[[^]]+\]\(https?://[^)]+\)|否：[^|]+) \|$", text, re.M)
    image = (directory / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n") and len(image) > 5000
    width, height = struct.unpack(">II", image[16:24])
    assert width >= 400 and height >= 140
    protocol = json.loads((directory / "assets/runtime-protocol.json").read_text())
    assert protocol["diagnostic_only"] is True
    assert "paper_results" not in protocol and "paper_reported" not in protocol
    assert not (directory / "metrics/protocol.json").exists()
    metrics = list((directory / "metrics").glob("*.json"))
    assert metrics, "completed public CUDA run must have a measured artifact, not only a protocol"
    for path in metrics:
        payload = json.loads(path.read_text())
        assert payload["schema_version"] == 2 and payload["diagnostic_only"] is True
        assert payload["measured_locally"] is True and payload["metrics"]
        assert f"metrics/{path.name}" in text
    from auto_research.gpu_validation import load_gpu_receipt
    receipt = load_gpu_receipt(ROOT / spec["execution"]["gpu_validation_artifact"])
    assert receipt["adapter_key"] == key and receipt["executed_source_sha256"]
    assert "线上 A/B：未报告" in text


def test_oct12_sources_are_hash_verified_and_test_selection_is_separate():
    reward = (ROOT / "src/auto_research/multimodal/oct12_reward_transition.py").read_text()
    assert 'for name in ("train", "validation"):' in reward
    assert reward.index('selected = select_probe_layer(validation)') < reward.index(
        'features["test"] = extract_split("test", [selected])')
    for key in ("msar", "orthros", "dualquant", "woven", "umrm"):
        assert (ROOT / f"src/auto_research/reproductions/{key}/adapter.py").is_file()


def test_oct12_foundation_owned_review_range_is_closed_with_bounded_read_scope():
    audit = json.loads((ROOT / "docs/research-audits/oct12-review-closure/foundation-model-reviews.json").read_text())
    reviews = audit["reviews"]
    assert len(reviews) == len({review["arxiv_id"] for review in reviews}) == 143
    owned = {review["assignment_index"] for review in reviews if review["assignment_index"] <= 138}
    assert owned == set(range(139))
    assert audit["counts"]["reviewed_in_owned_range"] == 139
    assert audit["counts"]["owned_not_reviewed"] == 0
    assert {review["assignment_index"] for review in reviews if review["assignment_index"] > 138} == {139, 157, 234, 246}
    assert re.fullmatch(r"[a-f0-9]{64}", audit["assignment_sha256"])
    for review in reviews:
        assert review["full_paper_read"] is False
        assert review["read_scope"] and review["defining_method"] and review["evaluation_evidence"]
        assert re.fullmatch(r"[a-f0-9]{64}", review["source_sha256"])
        assert review["source_url"].startswith("https://arxiv.org/")
        assert review["source_bytes"] > 0
        if not review["in_frozen_16_paper_batch"]:
            assert review["implementation_status"] == "not_implemented"
        if review["status"] == "reviewed_deferred":
            assert review["next_batch"] is True


def test_oct12_frozen_supplement_v1_proof_and_single_first_institution():
    audit = json.loads((ROOT / "docs/research-audits/oct12-review-closure/frozen-foundation-reviews.json").read_text())
    assert audit["counts"]["manual_supplement_not_recalled"] == 1
    assert {review["key"] for review in audit["reviews"]} == set(PAPERS)
    for review in audit["reviews"]:
        identifier, date, _ = PAPERS[review["key"]]
        assert review["arxiv_id"] == identifier
        assert review["status"] == "accepted" and review["in_frozen_16_paper_batch"] is True
        assert review["fidelity"] == "L1_core_mechanism" and review["next_batch"] is False
        assert review["first_author_affiliation"] == FIRST_AUTHOR_INSTITUTION[review["key"]]
        assert review["published"].startswith(date) and review["published"].endswith("Z")
        proof = review["publication_date_evidence"]
        assert "[v1]" in proof["text"] and "UTC" in proof["text"]
        assert proof["source_url"] == f"https://arxiv.org/abs/{identifier}v1"
        for source in (review["source_pdf"], proof):
            assert re.fullmatch(r"[a-f0-9]{64}", source["sha256"])
            assert source["bytes"] > 0
        assert review["full_paper_read"] is False and review["actual_boundary"]
        assert review["evidence_sections"] and review["evidence_pdf_pages"]["method"]
