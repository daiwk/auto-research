"""Source, metadata, bilingual/learning and status contracts for this batch."""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from english_learning_sources import question_units

AUDIT = ROOT / "docs/research-audits/nov18-latest"
ROWS = json.loads((AUDIT / "post-review.json").read_text())["accepted"]


def test_exact_fixed_scope_and_cost_preflight():
    assert len(ROWS) == 16
    assert sum(r["implementation_status"] == "component_only" for r in ROWS) == 12
    assert sum(r["implementation_status"] == "deferred_high_cost" for r in ROWS) == 4
    assert sum(r["gpu"] for r in ROWS) == 8
    assert len({r["id"] for r in ROWS}) == 16
    for r in ROWS:
        assert r["review_done"] is True
        assert r["automatic_retry"] is r["automatic_implementation_queue"] is False
        assert r["full_experiment_status"] == "not_reproduced_high_cost"
        assert len(r["source_sha256"]) == 64 and r["sections"]
        assert r["preimplementation_budget"]["checkpoint_download_bytes"] == 0
        assert r["preimplementation_budget"]["dataset_download_bytes"] == 0
        assert r["preimplementation_budget"]["paid_api_calls"] == 0


@pytest.mark.parametrize("row", ROWS, ids=lambda r: r["key"])
def test_paper_information_bilingual_hash_and_original_figure(row):
    directory = ROOT / f"docs/post-training/{row['id']}-{row['key']}"
    cn = (directory / "README.md").read_text()
    en = (directory / "README-en.md").read_text()
    assert f"<!-- source-sha256: {sha256(cn.encode()).hexdigest()} -->" in en
    assert "[简体中文](README.md)" in en
    assert row["author"] in cn and row["id"] + "v1" in cn
    assert row["published_at"].replace("T", " ").replace("Z", " UTC") in cn
    assert "原作者开源代码" in cn and "本地复现代码" in cn and "本地 adapter / key" in cn
    assert "完整实验成本过高，不复现（审查 DONE）" in cn
    assert "Copyright belongs to the original authors" in en
    assert "版权归原作者所有" in cn
    assert all(line == "$$" for line in cn.splitlines() if "$$" in line)
    fig = json.loads((directory / "assets/provenance.json").read_text())["figures"][0]
    assert fig["caption_included"] is fig["visual_review_done"] is True
    assert fig["scientific_content_modified"] is False
    assert fig["version"] == "v1" and fig["page_number"] >= 1
    assert (
        sha256((directory / "assets" / fig["file"]).read_bytes()).hexdigest() == fig["image_sha256"]
    )
    spec = json.loads(
        (
            ROOT / f"src/auto_research/paper_specs/catalog/post-training/{row['key']}.json"
        ).read_text()
    )
    assert spec["adapter"] is None
    assert spec["evolve_integrated"] is spec["promotion_eligible"] is False
    assert spec["requires_gpu_validation"] is row["gpu"]
    assert spec["implementation_status"] == row["implementation_status"]
    if row["implementation_status"] == "deferred_high_cost":
        assert "local_operator" not in spec and not (directory / "metrics").exists()
    else:
        result = json.loads((directory / "metrics/component-cpu-seeds42-44.json").read_text())
        assert [r["seed"] for r in result["per_seed"]] == [42, 43, 44]
        assert all(all(x["checks"].values()) for x in result["per_seed"])


def test_each_paper_has_four_reviewed_bilingual_layers_and_exact_source_units():
    bank = json.loads((ROOT / "docs/learning/questions/nov18-latest-post.json").read_text())[
        "papers"
    ]
    translations = json.loads(
        (ROOT / "docs/en/learning/translations/qa-nov18-latest-post.json").read_text()
    )["units"]
    expected = {"post-training:" + r["key"] for r in ROWS}
    assert set(bank) == expected
    units = question_units({k: v["questions"] for k, v in bank.items()})
    assert len(units) == 64 and set(units) == set(translations)
    for identity, record in bank.items():
        assert [q["level"] for q in record["questions"]] == [
            "basics",
            "mechanism",
            "comparison",
            "implementation",
        ]
        assert all(
            len(q["answer"]) > 30 and q["example"].startswith("教学例：")
            for q in record["questions"]
        )
    for key, unit in units.items():
        english = translations[key]
        assert english["source_sha256"] == unit.source_sha256 and english["reviewed"] is True
        assert set(english["fields"]) == {"question", "answer", "example"}
        assert not re.search(r"[\u3400-\u9fff]", " ".join(english["fields"].values()))


def test_deep_dive_proposals_read_same_topic_representatives_and_fingerprint_both():
    proposals = json.loads((AUDIT / "deep-dive-proposals-post.json").read_text())["proposals"]
    topics = json.loads((ROOT / "docs/learning/topics/post-training.json").read_text())["topics"]
    membership = {"post-training/" + t["id"]: set(t["papers"]) for t in topics}
    specs = {r["key"]: r for r in ROWS}
    assert len(proposals) == 16
    for p in proposals:
        own = p["paper"]
        assert len(p["source_revisions"]) == 2
        peer = next(identity for identity in p["source_revisions"] if identity != own)
        assert peer in membership[p["target_card"]]
        own_key = own.split(":")[1]
        row = specs[own_key]
        own_path = ROOT / f"docs/post-training/{row['id']}-{own_key}/README.md"
        peer_spec = json.loads(
            (
                ROOT
                / f"src/auto_research/paper_specs/catalog/post-training/{peer.split(':')[1]}.json"
            ).read_text()
        )
        peer_path = ROOT / "docs" / peer_spec["detail_path"]
        assert sha256(own_path.read_bytes()).hexdigest() == p["source_revisions"][own]
        assert sha256(peer_path.read_bytes()).hexdigest() == p["source_revisions"][peer]
        assert set(p["analysis"]["papers"]) == set(p["source_revisions"])
        assert set(p["question"]["papers"]) == set(p["source_revisions"])
        assert set(p["update"]["papers"]) == set(p["source_revisions"])
        assert p["question"]["question"] != p["english"]["question"]["question"]
