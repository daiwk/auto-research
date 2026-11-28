"""Authored Habitats metadata, provenance and bilingual learning contracts."""
from hashlib import sha256
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov28-latest"
FOLDER = ROOT / "docs/agent-research/2611.31160-habitats"
IDENTITY = "agent-research:habitats"


def read(path):
    return json.loads(path.read_text())


def test_habitats_paper_information_bilingual_and_original_date():
    chinese = (FOLDER / "README.md").read_text()
    english = (FOLDER / "README-en.md").read_text()
    assert "## 论文信息" in chinese and "## Paper information" in english
    assert sha256(chinese.encode()).hexdigest() in english
    for text in (chinese, english):
        assert "2026-11-23 18:23:16 UTC" in text
        assert "Google DeepMind" in text and "Nicolas Bolouri" in text
        assert "https://github.com/google-deepmind/habitats" in text
        assert "src/auto_research/agent_research/habitats.py" in text
        assert "adapter: null" in text and "not_reproduced_high_cost" in text
        assert "full_experiment_review_done=true" in text
        assert "2026-11-24" in text and "2026-11-28" in text
        assert "```mermaid" in text and "\\widetilde F[i,j]" in text
        assert "403" in text and "PENDING" not in text
    assert "原作者开源代码" in chinese and "| Author code |" in english


def test_habitats_original_figure_provenance_and_paper_scope():
    p = read(FOLDER / "assets/provenance.json")
    assert p["source_url"] == "https://arxiv.org/pdf/2611.31160v1"
    assert p["source_sha256"] == "d508f7db9dbdf8dfeb4e159826419f56bef345bb100e124f85e9648c84d94a59"
    assert p["asset_sha256"] == sha256((FOLDER / "assets/paper-figure-01.png").read_bytes()).hexdigest()
    assert p["page"] == 4 and p["figure"] == "Figure 1"
    assert p["visually_reviewed"] is True and p["caption_preserved"] is True
    spec = read(AUDIT / "paper-proposals-agent.json")["papers"][IDENTITY]
    assert spec["component_implemented"] and spec["diagnostic_only"]
    assert not spec["evolve_integrated"] and not spec["promotion_eligible"]
    assert not spec["requires_gpu_validation"] and not spec["automatic_retry"]
    assert spec["full_experiment_review_done"]
    assert spec["identity_note"]["openreview_public_date"] is None


def test_habitats_four_authored_levels_english_hashes_and_deep_peer_revisions():
    bundle = read(AUDIT / "agent-authored-bundle.json")
    questions = bundle["papers"][IDENTITY]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    source = (FOLDER / "README.md").read_text()
    for q in questions:
        assert q["added"] == "2026-11-28" and q["example"].startswith("教学例")
        assert all("### " + s in source for s in q["source_sections"])
        unit = bundle["english_question_units"][f"qa/{IDENTITY}/{q['id']}"]
        expected = sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        assert unit["reviewed"] and unit["source_sha256"] == expected
        assert all(unit["fields"][k] for k in ("question", "answer", "example"))
    deep = read(AUDIT / "deep-dive-proposals-agent.json")["proposals"][0]
    assert deep["target_card"] == "agent-research/harness-and-self-improvement"
    peer = "agent-research:alphaevolve"
    assert peer in deep["analysis"]["papers"]
    for identity, path in [(IDENTITY, FOLDER / "README.md"),
                           (peer, ROOT / "docs/agent-research/2506.13131-alphaevolve/README.md")]:
        assert deep["source_revisions"][identity] == sha256(path.read_bytes()).hexdigest()
        assert deep["update"]["source_revisions"][identity] == sha256(path.read_bytes()).hexdigest()
