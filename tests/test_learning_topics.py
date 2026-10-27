from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.generate_learning_cards import ROOT, _collection, _page_href, generate
from scripts.learning_topics import load_topics, navigation


def _write(root: Path, path: str, value: str) -> Path:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")
    return target


@pytest.fixture
def topic_repo(tmp_path):
    paper = {
        "domain": "recommendation", "key": "first", "title": "First paper",
        "detail_path": "reproductions/first/README.md",
        "paper_url": "https://example.org/first", "topic": ["序列"],
    }
    _write(tmp_path, "docs/research-manifest.json", json.dumps({"papers": [paper]}))
    _write(tmp_path, "docs/reproductions/first/README.md", """# First

> 成本过高，不复现（审查 DONE）。

## 原始论文总结

### 背景与主要改动

用短查询读取长历史。

## 本地复现

未执行原始规模训练。
""")
    _write(tmp_path, "docs/learning/index.md", """# 学习卡片

保留人工精选和说明。

<!-- learning-topics:start -->
<!-- learning-topics:end -->

保留结尾。
""")
    theme = {
        "id": "recommendation", "title": "搜广推", "intro": "学习用户与物品的交互。",
        "topics": [{
            "id": "sequence", "title": "长序列", "question": "如何保留历史？",
            "takeaway": "先判断哪些状态必须更新。", "example": "用短查询读取三条历史。",
            "pitfall": "不能直接外推生产成本。", "reading_order": "先读基础机制再看缓存。",
            "self_test": {"question": "历史何时能共享？", "answer": "用户路径与候选无关时。"},
            "start_here": ["recommendation:first"], "papers": ["recommendation:first"],
        }],
    }
    _write(tmp_path, "docs/learning/topics/recommendation.json", json.dumps(theme))
    _write(tmp_path, "docs/learning/questions/recommendation.json", json.dumps({
        "schema_version": 1, "papers": {"recommendation:first": {"questions": [{
            "id": "mechanism", "level": "mechanism", "question": "短查询为何仍需保留长历史？",
            "answer": "查询是读取入口，历史保存可寻址证据，二者不能混为同一状态。",
            "example": "教学例子：少量查询可按需读取多条旧记录。",
            "source_sections": ["背景与主要改动"], "added": "2026-10-27",
        }]}}
    }))
    return tmp_path, theme


def test_topic_pages_have_guides_sources_and_correct_routes(topic_repo):
    root, _ = topic_repo
    generate(root)
    page = (root / "docs/learning/paths/recommendation/sequence.md").read_text()
    for value in ["## 记住这一点", "## 一个例子", "## 什么时候要小心", "## 自测一下",
                  '??? note "展开参考答案"', "https://example.org/first",
                  "../../../reproductions/first/README.md"]:
        # Markdown source links must keep .md; raw HTML links target deployed routes.
        assert value in page
    assert '[跨主题搜索全部问答](../../all.md)' in page
    assert 'href="../../../../reproductions/first/"' in page
    assert '短查询为何仍需保留长历史' in page
    assert 'ar-learning-boundary' not in page
    assert 'data-learning-page-size="12"' in page
    hub = (root / "docs/learning/index.md").read_text()
    assert "保留人工精选和说明" in hub and "保留结尾" in hub
    assert "1 个主题 · 1 个子主题 · 1 个问题 / 1 篇论文" in hub
    assert '<details><summary>展开子主题问题库' in hub
    assert 'href="paths/recommendation/sequence/"' in hub


def test_unassigned_new_paper_is_visible_in_inbox_and_all_search(topic_repo):
    root, _ = topic_repo
    manifest = json.loads((root / "docs/research-manifest.json").read_text())
    added = dict(manifest["papers"][0], key="new", title="Unassigned new paper")
    manifest["papers"].append(added)
    _write(root, "docs/research-manifest.json", json.dumps(manifest))
    generate(root)
    inbox = (root / "docs/learning/inbox.md").read_text()
    assert "Unassigned new paper" in inbox and "First paper" not in inbox
    all_cards = (root / "docs/learning/all.md").read_text()
    assert "Unassigned new paper" in all_cards and 'data-theme="inbox"' in all_cards
    assert 'data-topic="recommendation/sequence"' in all_cards
    assert 'data-theme="recommendation">长序列</option>' in all_cards


def test_representative_metadata_cannot_inject_html_or_break_markdown(topic_repo):
    root, _ = topic_repo
    manifest = json.loads((root / "docs/research-manifest.json").read_text())
    manifest["papers"][0]["title"] = '<img src=x onerror="bad"> [title]'
    manifest["papers"][0]["paper_url"] = "https://example.org/paper?q=[x])"
    _write(root, "docs/research-manifest.json", json.dumps(manifest))
    generate(root)
    page = (root / "docs/learning/paths/recommendation/sequence.md").read_text()
    assert '<img src=x' not in page
    assert r'\[title\]' in page
    assert "https://example.org/paper?q=%5Bx%5D%29" in page


@pytest.mark.parametrize("fault, message", [
    ("duplicate", "duplicate learning topic assignment"),
    ("unknown", "unknown learning paper"),
    ("starter", "reading path must use distinct topic members"),
    ("answer", "learning guide needs answer"),
    ("path", "invalid or duplicate learning subtopic"),
])
def test_invalid_taxonomy_fails_before_writing_outputs(topic_repo, fault, message):
    root, theme = topic_repo
    topic = theme["topics"][0]
    if fault == "duplicate":
        duplicate = copy.deepcopy(topic)
        duplicate["id"] = "other"
        theme["topics"].append(duplicate)
    elif fault == "unknown":
        topic["papers"].append("recommendation:missing")
    elif fault == "starter":
        topic["start_here"] = ["recommendation:missing"]
    elif fault == "answer":
        topic["self_test"]["answer"] = ""
    elif fault == "path":
        topic["id"] = "../escape"
    _write(root, "docs/learning/topics/recommendation.json", json.dumps(theme))
    with pytest.raises(ValueError, match=message):
        generate(root)
    assert not (root / "docs/learning/all.md").exists()


def test_check_covers_guides_hub_and_inbox_without_writing(topic_repo):
    root, _ = topic_repo
    generate(root)
    paths = ["docs/learning/paths/recommendation/sequence.md", "docs/learning/index.md",
             "docs/learning/inbox.md"]
    for path in paths:
        target = root / path
        original = target.read_text()
        if path.endswith("index.md"):
            target.write_text(original.replace("1 个主题", "99 个主题"))
        else:
            target.write_text(original + "stale")
        with pytest.raises(ValueError, match="learning cards are stale"):
            generate(root, check=True)
        assert target.read_text() != original
        target.write_text(original)
    generate(root, check=True)


def test_removed_topic_only_removes_owned_generated_pages(topic_repo):
    root, theme = topic_repo
    generate(root)
    old = root / "docs/learning/paths/recommendation/sequence.md"
    authored = _write(root, "docs/learning/paths/recommendation/notes.md", "# User notes\n")
    theme["topics"][0]["id"] = "renamed"
    _write(root, "docs/learning/topics/recommendation.json", json.dumps(theme))
    with pytest.raises(ValueError, match="learning cards are stale"):
        generate(root, check=True)
    assert old.exists()
    generate(root)
    assert not old.exists()
    assert authored.read_text() == "# User notes\n"
    assert (root / "docs/learning/paths/recommendation/renamed.md").exists()


def test_editorial_changes_are_preserved_but_broken_markers_fail(topic_repo):
    root, _ = topic_repo
    generate(root)
    hub = root / "docs/learning/index.md"
    text = hub.read_text().replace("保留结尾。", "新一期人工内容。")
    hub.write_text(text)
    generate(root, check=True)
    assert "新一期人工内容。" in hub.read_text()
    hub.write_text(text.replace("<!-- learning-topics:end -->", ""))
    with pytest.raises(ValueError, match="one ordered pair of topic markers"):
        generate(root)


def test_navigation_is_topic_tree_and_never_enumerates_papers(topic_repo):
    root, _ = topic_repo
    themes = load_topics(root, {"recommendation:first"})
    tree = navigation(themes)
    assert tree == [{"搜广推": [
        {"主题概览": "learning/paths/recommendation/index.md"},
        {"长序列": "learning/paths/recommendation/sequence.md"},
    ]}]
    assert "first" not in json.dumps(tree)
    assert _page_href("learning/paths/recommendation/sequence.md", "learning/index.md") == "paths/recommendation/sequence/"


def test_real_curated_topics_are_consistent_and_have_guides():
    cards, themes = _collection(ROOT)
    assert {"recommendation", "foundation-models", "system-one", "multimodal-models",
            "post-training", "agent-research"} <= {theme["id"] for theme in themes}
    assigned = [card for card in cards if card["theme"] != "inbox"]
    assert len(assigned) == sum(len(topic["papers"]) for theme in themes for topic in theme["topics"])
    # Future research additions may intentionally wait in the inbox. Existing
    # editorial cards must retain a real learning path.
    featured = json.loads((ROOT / "docs/learning/card-overrides.json").read_text())
    assert set(featured) <= {card["identity"] for card in assigned}
    for theme in themes:
        for topic in theme["topics"]:
            assert len(topic["start_here"]) >= 2
