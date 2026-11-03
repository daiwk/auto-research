import json

import pytest

from scripts.english_learning_sources import deep_dive_units, load_reviewed, question_units, topic_units


def test_questions_have_stable_ids_and_preserve_provenance(tmp_path):
    identity = "agents:example"
    row = {
        "id": "mechanism", "question": "为何？", "answer": "减少重试。", "example": "失败后重新执行。",
        "source_sections": ["核心公式"], "level": "mechanism", "added": "2026-11-01",
    }
    units = question_units({identity: [row]})
    key = f"qa/{identity}/mechanism"
    assert set(units) == {key}
    assert set(units[key].fields) == {"question", "answer", "example"}
    english = {"question": "Why?", "answer": "To limit retries.", "example": "Retry after failure."}
    entry = {"source_sha256": units[key].source_sha256, "reviewed": True, "fields": english}
    path = tmp_path / "agent.json"

    def write(data):
        path.write_text(json.dumps({"schema_version": 1, "units": {key: data}}), encoding="utf-8")

    write(entry)
    assert load_reviewed(tmp_path, units) == {key: english}
    changed = question_units({identity: [row | {"source_sections": ["本地复现"]}]})
    with pytest.raises(ValueError, match="source changed"):
        load_reviewed(tmp_path, changed)
    write(entry | {"reviewed": False})
    with pytest.raises(ValueError, match="not reviewed"):
        load_reviewed(tmp_path, units)
    write(entry | {"fields": english | {"answer": "没有翻译"}})
    with pytest.raises(ValueError, match="incomplete"):
        load_reviewed(tmp_path, units)


def test_missing_units_fail_closed(tmp_path):
    units = question_units({"agents:x": [{"id": "one", "question": "问", "answer": "答", "example": "例"}]})
    with pytest.raises(ValueError, match="1 English learning units missing"):
        load_reviewed(tmp_path, units)
    assert load_reviewed(tmp_path, units, require_complete=False) == {}


def test_topic_membership_is_not_translatable_prose():
    topic = {
        "id": "demo", "title": "标题", "question": "问题", "takeaway": "结论", "example": "示例",
        "pitfall": "风险", "reading_order": "顺序", "self_test": {"question": "问", "answer": "答"},
        "papers": ["domain:one"],
    }
    theme = {"id": "example", "title": "主题", "intro": "介绍", "topics": [topic]}
    original = topic_units([theme])
    revised = topic_units([theme | {"topics": [topic | {"papers": ["domain:one", "domain:two"]}]}])
    assert original == revised
    assert set(original) == {"theme/example", "theme/example/demo", "theme/example/demo/self-test"}


def test_deep_dive_source_references_are_fingerprinted():
    record = {
        "title": "标题", "thesis": "命题", "axes": ["对照", "成本"],
        "comparisons": [{"paper": "domain:p", "position": "机制", "tradeoff": "取舍", "sections": ["边界"]}],
        "analysis": [{"title": "分析", "body": "正文", "papers": ["domain:p", "domain:q"]}],
        "questions": [{"id": "q", "question": "问", "answer": "答", "example": "例", "papers": ["domain:p", "domain:q"]}],
        "updates": [{"date": "2026-11-01", "summary": "更新", "papers": ["domain:p"], "source_revisions": {"domain:p": "a" * 64}}],
    }
    path = "theme/topic"
    unit = deep_dive_units({path: record})["dive/theme/topic/comparison/domain:p"]
    changed = record | {"comparisons": [record["comparisons"][0] | {"sections": ["方法"]}]}
    new_unit = deep_dive_units({path: changed})["dive/theme/topic/comparison/domain:p"]
    assert unit.fields == new_unit.fields
    assert unit.source_sha256 != new_unit.source_sha256
