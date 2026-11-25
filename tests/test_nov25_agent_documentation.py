"""Source-bound metadata, bilingual questions and same-topic review contracts."""

from hashlib import sha256
import json
from pathlib import Path
import re

import pytest


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov25-latest"


def load(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("key", ["agent-kernel", "cape", "recurscibench"])
def test_nov25_agent_metadata_english_and_original_figure(key):
    spec = load(AUDIT / "paper-proposals-agent.json")["papers"]["agent-research:" + key]
    path = ROOT / "docs" / spec["detail_path"]
    cn, en = path.read_text(), path.with_name("README-en.md").read_text()
    for label in ("论文链接", "公司/机构/学校", "首次公开日期", "原作者开源代码",
                  "本地 Adapter / 方法", "本地复现代码目录"):
        assert label in cn
    assert spec["published_at"].replace("T", " ").replace("Z", " UTC") in cn
    assert spec["discovered_on"] == "2026-11-25"
    assert spec["published"] == "2026-11-24"
    assert spec["code"] is None and "未找到" in spec["code_status"]
    assert "<!-- source-sha256: " + sha256(path.read_bytes()).hexdigest() + " -->" in en
    assert "[简体中文](README.md)" in en
    for content in (cn, en):
        assert "图片来自[原论文]" in content and "版权归原作者所有" in content
    provenance = load(path.parent / "assets/provenance.json")
    assert provenance["visually_reviewed"] and provenance["caption_preserved"]
    assert provenance["source_sha256"] == spec["method_source_sha256"]
    assert provenance["asset_sha256"] == sha256(
        (path.parent / "assets/paper-figure-01.png").read_bytes()).hexdigest()
    assert "成本过高，不复现（审查 DONE）" in spec["deferral_reason"]
    assert not spec["automatic_retry"] and not spec["evolve_integrated"]
    if key == "recurscibench":
        assert not spec["component_implemented"] and spec["local_operator"] is None
    else:
        assert spec["implementation_status"] == "component_only"
        assert spec["diagnostic_only"] and not spec["requires_gpu_validation"]


def test_nov25_agent_questions_are_authored_four_level_and_source_bound():
    bundle = load(AUDIT / "agent-authored-bundle.json")
    specs = load(AUDIT / "paper-proposals-agent.json")["papers"]
    count = 0
    for identity, row in bundle["papers"].items():
        cn = (ROOT / "docs" / specs[identity]["detail_path"]).read_text()
        headings = set(re.findall(r"^#{2,6}\s+(.+)$", cn, re.M))
        assert {q["level"] for q in row["questions"]} == {
            "basics", "mechanism", "comparison", "implementation"}
        for q in row["questions"]:
            assert q["added"] == "2026-11-25"
            assert set(q["source_sections"]) <= headings
            assert all(q[field].strip() for field in ("question", "answer", "example"))
            english = bundle["english_question_units"][f"qa/{identity}/{q['id']}"]
            expected = sha256(json.dumps(q, ensure_ascii=False, sort_keys=True,
                                        separators=(",", ":")).encode()).hexdigest()
            assert english["reviewed"] and english["source_sha256"] == expected
            assert set(english["fields"]) == {"question", "answer", "example"}
            assert not re.search(r"[\u3400-\u9fff]", "".join(english["fields"].values()))
            count += 1
    assert count == 12


def test_nov25_agent_deep_reviews_match_topic_and_readme_revisions():
    topics = load(ROOT / "docs/learning/topics/agent-research.json")["topics"]
    specs = load(AUDIT / "paper-proposals-agent.json")["papers"]
    paths = {"agent-research:runtime-tickets": "agent-research/2611.03772-runtime-tickets/README.md",
             "agent-research:caplite": "agent-research/2611.17115-caplite/README.md",
             "agent-research:coevobench": "agent-research/2611.27116-coevobench/README.md"}
    paths.update({key: row["detail_path"] for key, row in specs.items()})
    proposals = load(AUDIT / "deep-dive-proposals-agent.json")["proposals"]
    assert len(proposals) == 3
    for row in proposals:
        topic = next(t for t in topics if t["id"] == row["target_card"].split("/")[1])
        peers = set(row["source_revisions"]) - {row["paper"]}
        assert peers and peers <= set(topic["papers"])
        assert row["update"]["date"] == "2026-11-25"
        for identity, digest in row["source_revisions"].items():
            assert sha256((ROOT / "docs" / paths[identity]).read_bytes()).hexdigest() == digest
