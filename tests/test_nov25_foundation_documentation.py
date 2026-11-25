from hashlib import sha256
import json
from pathlib import Path

import pytest

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov25-latest"
KEYS = ["udvr", "thresholded-longce", "criticjepa"]


@pytest.mark.parametrize("key", KEYS)
def test_new_paper_metadata_reviewed_english_and_original_figure_contract(key):
    spec = next(x for x in json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"] if x["key"] == key)
    path = ROOT / "docs" / spec["detail_path"]
    cn, en = path.read_bytes(), path.with_name("README-en.md").read_text()
    assert f"<!-- source-sha256: {sha256(cn).hexdigest()} -->" in en
    for page in (cn.decode(), en):
        for token in (spec["paper_url"], spec["published_at"], spec["first_author_affiliation"],
                      "`adapter: null`", f"`{key}`", "paper-figure:start", "paper-figure:end",
                      "图片来自[原论文]", "版权归原作者所有", "```mermaid", "assets/provenance.json"):
            assert token in page
    assert "首次公开日期" in cn.decode() and "原作者开源代码" in cn.decode()
    assert "简体中文" in en
    provenance = json.loads((path.parent / "assets/provenance.json").read_text())
    image = (path.parent / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n")
    assert provenance["asset_sha256"] == sha256(image).hexdigest()
    assert provenance["source_sha256"] == spec["method_source_sha256"]
    assert provenance["reviewed_version"] == "v1"
    assert provenance["visually_reviewed"] and not provenance["scientific_content_modified"]
    assert "complete caption" in provenance["extraction"]
    assert spec["requires_gpu_validation"] is False
    assert not spec["automatic_retry"] and not spec["automatic_implementation_queue"]
    assert not spec["evolve_integrated"] and not spec["promotion_eligible"]
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    if key == "criticjepa":
        assert spec["local_operator"] is None and spec["implementation_status"] == "deferred_high_cost"
        assert "成本过高，不复现（审查 DONE）" in spec["deferral_reason"]
        assert not (path.parent / "metrics").exists()
        metrics = json.loads((path.parent / "review/cost-assessment.json").read_text())
        assert metrics["local_metrics"] == {} and metrics["upstream_revision"] is None
    else:
        assert "CPU-only" in cn.decode() and "CPU-only" in en
        assert spec["code"] is None and spec["upstream_revision"] is None
        assert not (path.parent / "metrics/component-cpu.json").exists()
        assert (AUDIT / f"preflight-{key}.json").exists()
        assert "metrics/component-cpu-seeds42-44.json" in cn.decode()


@pytest.mark.parametrize("key", KEYS)
def test_authored_four_level_bilingual_questions_and_real_peer_readme_hashes(key):
    identity = "foundation-models:" + key
    bundle = json.loads((AUDIT / "foundation-authored-bundle.json").read_text())
    questions = bundle["papers"][identity]["questions"]
    assert len(questions) == 4
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    units = question_units({identity: questions})
    spec = next(x for x in json.loads((AUDIT / "paper-proposals-foundation.json").read_text())["papers"] if x["key"] == key)
    cn = (ROOT / "docs" / spec["detail_path"]).read_text()
    for q in questions:
        assert q["added"] == "2026-11-25" and q["answer"] and q["example"]
        assert all("### " + section in cn for section in q["source_sections"])
        uid = f"qa/{identity}/{q['id']}"
        translation = bundle["english_question_units"][uid]
        assert translation["reviewed"] and set(translation["fields"]) == {"question", "answer", "example"}
        assert translation["source_sha256"] == units[uid].source_sha256
    proposal = next(x for x in json.loads((AUDIT / "deep-dive-proposals-foundation.json").read_text())["proposals"] if x["paper"] == identity)
    assert len(proposal["source_revisions"]) == 2 and proposal["update"]["date"] == "2026-11-25"
    assert proposal["source_revisions"][identity] == sha256((ROOT / "docs" / spec["detail_path"]).read_bytes()).hexdigest()
    peers = {
        "udvr": "foundation-models/2611.00236-proland/README.md",
        "thresholded-longce": "foundation-models/2610.37645-merlin/README.md",
        "criticjepa": "foundation-models/2610.19375-jepa-prediction-planning/README.md",
    }
    peer = next(x for x in proposal["source_revisions"] if x != identity)
    assert proposal["source_revisions"][peer] == sha256((ROOT / "docs" / peers[key]).read_bytes()).hexdigest()
