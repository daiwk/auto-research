from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.generate_learning_cards import ROOT, _collection, _page_href, generate
from scripts.learning_deep_dives import load_deep_dives, navigation, render_pages, source_revisions
from scripts.learning_questions import source_headings


def _write(root, name, value):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value)
    return path


@pytest.fixture
def deep_repo(tmp_path):
    identities = [f"recommendation:{key}" for key in ("first", "second", "third")]
    cards = [{"identity": identity, "key": identity.split(":")[1], "theme": "recommendation",
              "title": f"Paper {index}", "detail_path": f"papers/{index}/README.md",
              "paper_url": f"https://example.org/{index}"} for index, identity in enumerate(identities)]
    for card in cards:
        _write(tmp_path, "docs/" + card["detail_path"], "# Paper\n\n## 核心机制\n\n机制描述。\n")
    themes = [{"id": "recommendation", "title": "搜广推", "topics": [
        {"id": "sequence", "title": "长序列", "papers": identities},
    ]}]
    record = {
        "title": "用户历史应当在哪里压缩？", "thesis": "压缩查询与固定池读取保留不同信息。",
        "updated": "2026-10-27", "reviewed_papers": identities.copy(),
        "axes": ["状态是否更新", "候选相关性"],
        "comparisons": [{"paper": identity, "position": "本篇的机制。", "tradeoff": "本篇的取舍。",
                         "sections": ["核心机制"]} for identity in identities],
        "analysis": [{"title": f"取舍 {i}", "body": "具体分析。", "papers": identities[:2]} for i in range(2)],
        "questions": [{"id": f"question-{i}", "question": f"对照问题{i}？", "answer": "直接答案。",
                       "example": "具体教学例子。", "papers": identities[:2]} for i in range(3)],
        "updates": [{"date": "2026-10-27", "summary": "首版比较。", "papers": identities.copy(),
                     "source_revisions": source_revisions(tmp_path, cards, identities)}],
    }
    payload = {"schema_version": 1, "theme": "recommendation", "topics": {"sequence": record}}
    _write(tmp_path, "docs/learning/deep-dives/recommendation.json", payload)
    return tmp_path, themes, cards, payload


def _load(fixture):
    root, themes, cards, _ = fixture
    return load_deep_dives(root, themes, cards, source_headings, required=True)


def test_card_has_comparison_analysis_multiple_qa_and_folded_catalog(deep_repo):
    root, themes, cards, _ = deep_repo
    bank = _load(deep_repo)
    pages = render_pages(themes, cards, bank, _page_href)
    text = pages[Path("docs/learning/deep-dives/recommendation/sequence.md")]
    for section in ("机制对照", "取舍分析", "跨论文问答", "更新记录"):
        assert "## " + section in text
    assert text.count('??? note "展开答案与例子"') == 3
    assert "#cross-question-0" in text
    assert "[Paper 0](../../../papers/0/README.md)" in text
    assert "[原始来源](https://example.org/0)" in text
    assert "章节：核心机制" in text
    assert '本主题全部 3 篇资料</summary>' in text
    assert "[进入本主题逐篇四层问答](../../paths/recommendation/sequence.md)" in text
    index = pages[Path("docs/learning/deep-dives/index.md")]
    assert '<details class="ar-deep-shelf"><summary>搜广推 · 1 张</summary>' in index
    assert 'href="recommendation/sequence/"' in index
    assert '<details open' not in index
    assert navigation(themes)[1]["搜广推"][0] == {
        "长序列": "learning/deep-dives/recommendation/sequence.md",
    }


def test_new_paper_needs_membership_review_and_dated_update(deep_repo):
    root, themes, cards, payload = deep_repo
    identity = "recommendation:fourth"
    themes[0]["topics"][0]["papers"].append(identity)
    cards.append(dict(cards[0], identity=identity, key="fourth"))
    with pytest.raises(ValueError, match="needs an update for new papers"):
        _load(deep_repo)
    record = payload["topics"]["sequence"]
    record["reviewed_papers"].append(identity)
    _write(root, "docs/learning/deep-dives/recommendation.json", payload)
    with pytest.raises(ValueError, match="update log must cover"):
        _load(deep_repo)
    record["updated"] = "2026-10-28"
    record["updates"].append({"date": "2026-10-28", "summary": "新论文增加固定池读取路线，更新取舍。",
                              "papers": [identity], "source_revisions": source_revisions(root, cards, [identity])})
    _write(root, "docs/learning/deep-dives/recommendation.json", payload)
    assert _load(deep_repo)["recommendation/sequence"]["updated"] == "2026-10-28"


@pytest.mark.parametrize("fault,match", [
    ("source", "missing source section"), ("same-paper", "distinct topic papers"),
    ("duplicate-id", "duplicate deep-dive question"), ("date", "invalid deep-dive date"),
    ("new-topic", "topics differ from taxonomy"), ("three-questions", "needs 3 questions"),
    ("comparison", "at least three comparison papers"), ("latest", "update log must cover"),
])
def test_invalid_authored_readings_are_rejected(deep_repo, fault, match):
    root, _, _, payload = deep_repo
    record = payload["topics"]["sequence"]
    if fault == "source":
        record["comparisons"][0]["sections"] = ["编造标题"]
    elif fault == "same-paper":
        record["questions"][0]["papers"] = ["recommendation:first"]
    elif fault == "duplicate-id":
        record["questions"][1]["id"] = record["questions"][0]["id"]
    elif fault == "date":
        record["updated"] = "2026-02-30"
    elif fault == "new-topic":
        payload["topics"]["extra"] = record
    elif fault == "three-questions":
        record["questions"].pop()
    elif fault == "comparison":
        record["comparisons"].pop()
    elif fault == "latest":
        record["updated"] = "2026-10-28"
    _write(root, "docs/learning/deep-dives/recommendation.json", payload)
    with pytest.raises(ValueError, match=match):
        _load(deep_repo)


def test_missing_cards_and_unassigned_papers_block_publication(deep_repo):
    root, themes, cards, _ = deep_repo
    cards.append(dict(cards[0], identity="recommendation:unassigned", theme="inbox"))
    with pytest.raises(ValueError, match="topic assignment"):
        _load(deep_repo)
    (root / "docs/learning/deep-dives/recommendation.json").unlink()
    with pytest.raises(ValueError, match="topics need authored deep dives"):
        load_deep_dives(root, themes, cards, source_headings, required=True)


def test_cannot_hide_later_addition_inside_an_older_update(deep_repo):
    root, _, cards, payload = deep_repo
    cards[0]["questions"] = [{"added": "2026-10-28"}]
    with pytest.raises(ValueError, match="predates paper's first authored questions"):
        _load(deep_repo)
    record = payload["topics"]["sequence"]
    record["updated"] = "2026-10-28"
    record["updates"].append({"date": "2026-10-28", "summary": "增加该论文与现有路线的对照。",
                              "papers": [cards[0]["identity"]],
                              "source_revisions": source_revisions(root, cards, [cards[0]["identity"]])})
    _write(root, "docs/learning/deep-dives/recommendation.json", payload)
    assert _load(deep_repo)


def test_existing_paper_source_upgrade_requires_new_review(deep_repo):
    root, _, cards, payload = deep_repo
    source = root / "docs" / cards[0]["detail_path"]
    source.write_text(source.read_text() + "\n新机制与实测边界。\n")
    with pytest.raises(ValueError, match="source changed; review and append an update"):
        _load(deep_repo)
    record = payload["topics"]["sequence"]
    record["updates"].append({"date": "2026-10-27", "summary": "补充新实现边界，并修订本卡取舍。",
                              "papers": [cards[0]["identity"]],
                              "source_revisions": source_revisions(root, cards, [cards[0]["identity"]])})
    _write(root, "docs/learning/deep-dives/recommendation.json", payload)
    assert _load(deep_repo)


def test_failed_gate_does_not_write_generated_files(deep_repo):
    root, _, _, _ = deep_repo
    _write(root, "docs/research-manifest.json", {"papers": []})
    target = _write(root, "docs/learning/all.md", "保留原有文件。")
    with pytest.raises(ValueError, match="invalid deep-dive schema"):
        generate(root, require_deep_dives=True)
    assert target.read_text() == "保留原有文件。"


def test_real_collection_has_one_reading_per_topic_and_preserves_paper_bank():
    cards, themes = _collection(ROOT)
    bank = load_deep_dives(ROOT, themes, cards, source_headings, required=True)
    assert len(bank) == sum(len(theme["topics"]) for theme in themes)
    assert len(bank) >= 31
    assert sum(len(card["questions"]) for card in cards) >= 4143
    assert sum(len(record["reviewed_papers"]) for record in bank.values()) == len(cards)
    for name in ("001-hstu-longer-slimper.md", "002-rankmixer-tokenmix.md"):
        assert not (ROOT / "docs/learning" / name).exists()
    source = (ROOT / "mkdocs.yml").read_text()
    assert "001-hstu-longer-slimper" not in source and "002-rankmixer-tokenmix" not in source
