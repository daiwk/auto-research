from hashlib import sha256
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov24-latest"


@pytest.mark.parametrize("key,published,affiliation,module", [
    ("deep-cross-attention", "2025-02-10T18:58:52Z", "University of California, Irvine", "deep_cross_attention"),
    ("stablekl", "2026-11-23T15:18:30Z", "Yale University", "stablekl"),
])
def test_complete_paper_metadata_bilingual_review_and_source_figure(key, published, affiliation, module):
    spec = next(x for x in json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"] if x["key"] == key)
    cn_path = ROOT / "docs" / spec["detail_path"]
    cn, en = cn_path.read_bytes(), cn_path.with_name("README-en.md").read_text()
    assert f"<!-- source-sha256: {sha256(cn).hexdigest()} -->" in en
    for page in (cn.decode(), en):
        for fact in (published, affiliation, spec["paper_url"], "`adapter: null`", f"`{key}`",
                     f"src/auto_research/foundation_models/{module}.py", "paper-figure:start", "```mermaid"):
            assert fact in page
    assert "首次公开日期" in cn.decode() and "原作者开源代码" in cn.decode()
    if key == "deep-cross-attention":
        assert "2025-07-23T19:32:20Z" in cn.decode()
        assert spec["intake_class"] == "historical_priority_backfill"
        assert spec["first_author_affiliation"] != "Google Research"
    else:
        assert spec["code"] in cn.decode() and spec["upstream_revision"] in en
        assert spec["requires_gpu_validation"] is False
    provenance = json.loads((cn_path.parent / "assets/provenance.json").read_text())
    image = (cn_path.parent / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n")
    assert provenance["asset_sha256"] == sha256(image).hexdigest()
    assert provenance["source_sha256"] == spec["method_source_sha256"]
    assert provenance["visually_reviewed"] and not provenance["scientific_content_modified"]


@pytest.mark.parametrize("key", ["deep-cross-attention", "stablekl"])
def test_authored_four_level_questions_and_fingerprinted_peer_review(key):
    identity = "foundation-models:" + key
    bundle = json.loads((AUDIT / "foundation-authored-bundle.json").read_text())
    questions = bundle["papers"][identity]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    spec = next(x for x in json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"] if x["key"] == key)
    source = ROOT / "docs" / spec["detail_path"]
    cn = source.read_text()
    for question in questions:
        assert question["added"] == "2026-11-24" and question["answer"] and question["example"]
        assert all("### " + heading in cn for heading in question["source_sections"])
        unit = bundle["english_question_units"][f"qa/{identity}/{question['id']}"]
        assert unit["reviewed"] and set(unit["fields"]) == {"question", "answer", "example"}
    proposal = next(x for x in json.loads((AUDIT / "deep-dive-proposals-foundation.json").read_text())["proposals"] if x["paper"] == identity)
    assert proposal["source_revisions"][identity] == sha256(source.read_bytes()).hexdigest()
    assert len(proposal["source_revisions"]) == 2
    assert proposal["update"]["date"] == "2026-11-24"
