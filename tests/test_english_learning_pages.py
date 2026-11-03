from hashlib import sha256
import json

import pytest

from scripts import english_learning_pages as pages
from scripts import english_learning_sources as source


def test_english_views_reuse_reviewed_questions_and_preserve_routes(tmp_path, monkeypatch):
    identity = "foundation-models:sample"
    question = {
        "id": "what", "question": "问", "answer": "答", "example": "例",
        "added": "2026-11-01", "level": "basics", "source_sections": ["核心公式"],
    }
    topic = {
        "id": "one", "title": "子主题", "question": "问", "takeaway": "结论", "example": "示例",
        "pitfall": "风险", "reading_order": "顺序", "self_test": {"question": "问", "answer": "答"},
        "papers": [identity], "start_here": [identity], "question_count": 1,
    }
    themes = [{"id": "foundation-models", "title": "主题", "intro": "介绍",
               "topics": [topic], "question_count": 1}]
    card = {
        "identity": identity, "domain": "foundation-models", "key": "sample", "title": "Sample",
        "organization": "Example University", "published": "2026-10-31", "summary": "", "local_scope": "",
        "question": "", "topics": "", "paper_url": "https://example.test/paper", "source_label": "原论文",
        "anchor": "paper-sample", "detail_path": "foundation-models/sample/README.md",
        "curated_path": "", "questions": [question],
    }
    dives = {"foundation-models/one": {
        "title": "精读", "thesis": "比较", "updated": "2026-11-01", "axes": ["取舍"],
        "comparisons": [{"paper": identity, "position": "方法", "tradeoff": "取舍", "sections": ["核心公式"]}],
        "analysis": [], "questions": [], "updates": [],
    }}
    monkeypatch.setattr(pages.zh, "_collection", lambda _: ([dict(card)], themes))
    monkeypatch.setattr(pages.zh._deep_dive_module(), "load_deep_dives", lambda *_, **__: dives)
    src_paths = (
        "all.md", "recent.md", "inbox.md", "index.md", "deep-dives/index.md",
        "paths/foundation-models/index.md", "paths/foundation-models/one.md",
        "deep-dives/foundation-models/one.md",
    )
    for path in src_paths:
        file = tmp_path / "docs/learning" / path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text("# 中文\n", encoding="utf-8")
    paper = tmp_path / "docs/foundation-models/sample/README-en.md"
    paper.parent.mkdir(parents=True)
    paper.write_text("# Sample\n", encoding="utf-8")
    directory = tmp_path / "docs/en/learning/translations"
    directory.mkdir(parents=True)
    with pytest.raises(ValueError, match="English learning units missing"):
        pages.render_pages(tmp_path)
    units = (
        source.question_units({identity: [question]}) | source.topic_units(themes) | source.deep_dive_units(dives)
    )
    english = {
        name: {"source_sha256": unit.source_sha256, "reviewed": True,
               "fields": {field: f"Localized {field}" for field in unit.fields}}
        for name, unit in units.items()
    }
    english[f"qa/{identity}/what"]["fields"]["question"] = "What changes in the attention path?"
    (directory / "reviewed.json").write_text(json.dumps({"schema_version": 1, "units": english}))
    rendered = pages.render_pages(tmp_path)
    assert set(rendered) == {f"docs/en/learning/{path}" for path in src_paths}
    for path in ("all.md", "recent.md", "paths/foundation-models/one.md"):
        content = rendered[f"docs/en/learning/{path}"]
        anchor = pages.zh._question_module().question_anchor(identity, "what")
        assert f'id="{anchor}"' in content
        assert "What changes in the attention path?" in content
        assert 'data-learning-lang="en"' in content
        assert 'data-search=' not in content
        assert "Show answer and example" in content
        assert "README-en/" in content
        assert "2026-11-01" in content
        digest = sha256((tmp_path / "docs/learning" / path).read_bytes()).hexdigest()
        assert f"<!-- source-sha256: {digest} -->" in content
