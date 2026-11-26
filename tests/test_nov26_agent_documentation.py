"""Source-bound Nov26 metadata, original figures, bilingual QA and peer reviews."""

from hashlib import sha256
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs/research-audits/nov26-latest"


def load(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize("identity", ["agent-research:home", "agent-research:dualpm", "multimodal-models:agentic-longlive"])
def test_nov26_agent_metadata_bilingual_original_figure(identity):
    spec = load(AUDIT / "paper-proposals-agent.json")["papers"][identity]
    source = ROOT / "docs" / spec["detail_path"]
    cn, en = source.read_text(), source.with_name("README-en.md").read_text()
    for label in ("论文链接", "公司/机构/学校", "首次公开日期", "原作者开源代码",
                  "本地 Adapter / 方法", "本地复现代码目录"):
        assert label in cn
    assert spec["published_at"].replace("T", " ").replace("Z", " UTC") in cn
    assert spec["published"] == "2026-11-25" and spec["discovered_on"] == "2026-11-26"
    assert spec["announced_on"] == "2026-11-26"
    assert "<!-- source-sha256: " + sha256(source.read_bytes()).hexdigest() + " -->" in en
    assert "[简体中文](README.md)" in en
    for text in (cn, en):
        assert "图片来自[原论文]" in text and "版权归原作者所有" in text
    provenance = load(source.parent / "assets/provenance.json")
    assert provenance["visually_reviewed"] and provenance["caption_preserved"]
    assert provenance["source_sha256"] == spec["method_source_sha256"]
    assert provenance["asset_sha256"] == sha256((source.parent / "assets/paper-figure-01.png").read_bytes()).hexdigest()
    assert "成本过高，不复现（审查 DONE）" in spec["deferral_reason"]
    assert spec["full_experiment_status"] == "not_reproduced_high_cost"
    assert not spec["automatic_retry"] and not spec["automatic_implementation_queue"]
    assert not spec["promotion_eligible"] and not spec["evolve_integrated"]
    assert spec["adapter"] is None and spec["gpu_validation_artifact"] is None
    if spec["key"] == "agentic-longlive":
        assert spec["code"] == "https://github.com/NVlabs/LongLive/tree/main/Agentic-LongLive"
        assert spec["local_operator"] is None and spec["local_command"] is None
        assert not spec["component_implemented"] and spec["implementation_status"] == "deferred_high_cost"
        assert not (source.parent / "metrics").exists()
    else:
        assert spec["component_implemented"] and spec["implementation_status"] == "component_only"
        assert spec["evaluation_tier"] == ("l0_interface" if spec["key"] == "dualpm" else "l1_mechanism")
        assert not spec["requires_gpu_validation"] and spec["diagnostic_only"]


def test_nov26_agent_four_level_authored_questions_and_english():
    specs = load(AUDIT / "paper-proposals-agent.json")["papers"]
    bundle = load(AUDIT / "agent-authored-bundle.json")
    assert set(bundle["papers"]) == set(specs)
    for identity, row in bundle["papers"].items():
        cn = (ROOT / "docs" / specs[identity]["detail_path"]).read_text()
        headings = set(re.findall(r"^#{2,6}\s+(.+)$", cn, re.M))
        assert {q["level"] for q in row["questions"]} == {"basics", "mechanism", "comparison", "implementation"}
        for q in row["questions"]:
            assert q["added"] == "2026-11-26" and set(q["source_sections"]) <= headings
            assert all(q[field].strip() for field in ("question", "answer", "example"))
            english = bundle["english_question_units"][f"qa/{identity}/{q['id']}"]
            fingerprint = sha256(json.dumps(q, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
            assert english["reviewed"] and english["source_sha256"] == fingerprint
            assert set(english["fields"]) == {"question", "answer", "example"}
            assert not re.search(r"[\u3400-\u9fff]", "".join(english["fields"].values()))
    assert len(bundle["english_question_units"]) == 12


def test_nov26_agent_same_topic_reviews_bind_final_readmes():
    specs = load(AUDIT / "paper-proposals-agent.json")["papers"]
    paths = {"agent-research:morse": "agent-research/2611.30011-morse/README.md",
             "agent-research:grepmem": "agent-research/2611.25123-grepmem/README.md",
             "multimodal-models:pixvid": "multimodal-models/2611.17336-pixvid/README.md"}
    paths.update({key: spec["detail_path"] for key, spec in specs.items()})
    proposals = load(AUDIT / "deep-dive-proposals-agent.json")["proposals"]
    assert {row["paper"] for row in proposals} == set(specs)
    for row in proposals:
        theme, topic_id = row["target_card"].split("/")
        topics = load(ROOT / "docs/learning/topics" / (theme + ".json"))["topics"]
        topic = next(t for t in topics if t["id"] == topic_id)
        assert set(row["source_revisions"]) - {row["paper"]} <= set(topic["papers"])
        assert row["update"]["date"] == "2026-11-26"
        assert row["update"]["source_revisions"] == row["source_revisions"]
        for identity, digest in row["source_revisions"].items():
            assert sha256((ROOT / "docs" / paths[identity]).read_bytes()).hexdigest() == digest
        assert not re.search(r"[\u3400-\u9fff]", json.dumps(row["english"], ensure_ascii=False))


def test_nov26_agent_preflight_is_cpu_and_keeps_dualpm_l0():
    preflight = load(AUDIT / "preflight-agent.json")
    assert preflight["api_calls"] == preflight["model_and_dataset_downloads"] == 0
    assert set(preflight["components"]) == {"home", "dualpm"}
    assert preflight["components"]["dualpm"]["evaluation_tier"] == "l0_interface"
    assert not any(row["cuda"] for row in preflight["components"].values())
