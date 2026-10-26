from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from scripts.generate_learning_cards import ROOT, _collection, generate, render
from scripts.learning_questions import question_anchor, require_complete, source_headings


def _write(root, relative, value):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False) if isinstance(value, dict) else value)
    return path


def _question(key="mechanism", added="2026-10-27"):
    return {"id": key, "question": f"{key}为什么要保留连续gate？",
            "answer": "索引选择离散，但选中gate仍把任务梯度传给选择器。",
            "example": "教学例子：相同两个索引，0.8/0.2与0.5/0.5产生不同输出。",
            "source_sections": ["背景与主要改动", "核心公式"], "added": added}


@pytest.fixture
def question_repo(tmp_path):
    papers = [{"domain": "recommendation", "key": key, "title": f"Paper {key}",
               "detail_path": f"reproductions/{key}/README.md",
               "paper_url": f"https://example.org/{key}", "published": "2020-01-01"}
              for key in ("first", "second")]
    _write(tmp_path, "docs/research-manifest.json", {"papers": papers})
    for paper in papers:
        _write(tmp_path, "docs/" + paper["detail_path"], """# Example

> 本地仅为机制诊断，未验证完整模型能力。

## 原始论文总结

### 背景与主要改动

选择器需要通过连续gate获得反馈。

### 核心公式

将log gate加入attention分数。

## 复现边界

没有完整模型实验。
""")
    bank = {"schema_version": 1, "papers": {
        "recommendation:first": {"questions": [_question(), _question("cost", "2026-10-28")]},
        "recommendation:second": {"questions": [_question("selection")]},
    }}
    _write(tmp_path, "docs/learning/questions/recommendation.json", bank)
    return tmp_path, bank


def test_every_authored_question_is_rendered_with_answer_example_and_sources(question_repo):
    root, _ = question_repo
    text = render(root)
    assert text.count('data-learning-card data-identity=') == 3
    assert text.count('<details class="ar-learning-answer">') == 3
    assert "3 个问题 · 2 篇论文" in text
    assert "索引选择离散，但选中gate仍把任务梯度传给选择器" in text
    assert "教学例子：相同两个索引" in text
    assert "依据：背景与主要改动、核心公式" in text
    assert 'ar-learning-boundary' not in text
    assert "展开答案与例子" in text
    assert 'href="../../reproductions/first/">实现解读' in text
    assert '?paper=recommendation%3Afirst' in text


def test_append_question_keeps_existing_bookmarks_and_updates_recent(question_repo):
    root, bank = question_repo
    original = question_anchor("recommendation:first", "mechanism")
    generate(root, require_questions=True)
    bank["papers"]["recommendation:first"]["questions"].append(_question("later", "2026-10-29"))
    _write(root, "docs/learning/questions/recommendation.json", bank)
    generate(root, require_questions=True)
    all_text = (root / "docs/learning/all.md").read_text()
    assert f'id="{original}"' in all_text
    assert all_text.count('id="paper-recommendation-first-') == 1
    recent = (root / "docs/learning/recent.md").read_text()
    assert recent.index("later为什么") < recent.index("cost为什么") < recent.index("mechanism为什么")
    assert "4 个问题 · 2 篇论文" in recent


def test_recent_home_links_and_subtopic_bank_share_questions(question_repo):
    root, _ = question_repo
    theme = {"id": "recommendation", "title": "搜广推", "intro": "按机制学习。", "topics": [{
        "id": "selectors", "title": "选择器", "question": "为什么保留gate？",
        "takeaway": "选择和梯度通路不同。", "example": "相同索引不同权重。",
        "pitfall": "不能把索引当连续值。", "reading_order": "先看机制。",
        "self_test": {"question": "离散索引可导吗？", "answer": "不能直接沿索引求导。"},
        "start_here": ["recommendation:first"], "papers": ["recommendation:first"],
    }]}
    _write(root, "docs/learning/topics/recommendation.json", theme)
    _write(root, "docs/learning/index.md", """# Home
<!-- learning-topics:start -->
<!-- learning-topics:end -->
<!-- learning-recent:start -->
<!-- learning-recent:end -->
""")
    generate(root, require_questions=True)
    hub = (root / "docs/learning/index.md").read_text()
    topic = (root / "docs/learning/paths/recommendation/selectors.md").read_text()
    anchor = question_anchor("recommendation:first", "cost")
    assert f'href="all/#{anchor}"' in hub
    assert 'cost为什么要保留连续gate' in hub and 'cost为什么要保留连续gate' in topic
    assert '2 个问题 · 1 篇论文' in topic
    assert 'ar-learning-guide' in topic


def test_recent_region_is_independent_and_malformed_markers_fail(question_repo):
    root, _ = question_repo
    _write(root, "docs/learning/index.md", "# Editorial\n<!-- learning-recent:start -->\n<!-- learning-recent:end -->\n")
    generate(root)
    hub = root / "docs/learning/index.md"
    assert "cost为什么要保留连续gate" in hub.read_text()
    text = hub.read_text()
    hub.write_text(text.replace("<!-- learning-recent:end -->", ""))
    with pytest.raises(ValueError, match="one ordered pair of recent markers"):
        generate(root)


def test_no_automatic_template_can_satisfy_question_coverage(question_repo):
    root, bank = question_repo
    del bank["papers"]["recommendation:second"]
    _write(root, "docs/learning/questions/recommendation.json", bank)
    text = render(root)
    assert "待补逐篇问答" in text
    assert "这篇论文解决了什么问题" not in text
    with pytest.raises(ValueError, match="1 papers need authored Q&A"):
        generate(root, require_questions=True)
    assert not (root / "docs/learning/all.md").exists()


@pytest.mark.parametrize("fault, message", [
    ("empty", "needs answer"), ("example", "needs example"),
    ("date", "invalid question date"), ("id", "duplicate question ID"),
    ("section", "missing source section"), ("unknown", "unknown question-bank paper"),
])
def test_editorial_contract_rejects_invalid_content_before_generation(question_repo, fault, message):
    root, bank = question_repo
    question = bank["papers"]["recommendation:first"]["questions"][0]
    if fault == "empty":
        question["answer"] = ""
    elif fault == "example":
        question.pop("example")
    elif fault == "date":
        question["added"] = "2026-02-30"
    elif fault == "id":
        bank["papers"]["recommendation:first"]["questions"].append(copy.deepcopy(question))
    elif fault == "section":
        question["source_sections"] = ["不存在的段落"]
    elif fault == "unknown":
        bank["papers"]["recommendation:unknown"] = {"questions": [_question()]}
    _write(root, "docs/learning/questions/recommendation.json", bank)
    with pytest.raises(ValueError, match=message):
        generate(root)
    assert not (root / "docs/learning/all.md").exists()


def test_bank_shards_cannot_duplicate_a_paper(question_repo):
    root, bank = question_repo
    _write(root, "docs/learning/questions/duplicate.json", bank)
    with pytest.raises(ValueError, match="duplicate question-bank paper"):
        generate(root)


def test_content_is_html_escaped_and_examples_do_not_create_source_headings(question_repo):
    root, bank = question_repo
    question = bank["papers"]["recommendation:first"]["questions"][0]
    question["question"] = '<img src=x onerror="bad">?'
    question["answer"] = "<script>bad</script>"
    _write(root, "docs/learning/questions/recommendation.json", bank)
    text = render(root)
    assert '<img src=x' not in text and '<script>bad' not in text
    assert '&lt;script&gt;bad&lt;/script&gt;' in text
    assert source_headings("# Real\n```text\n## Fake\n```\n## Source") == {"Real", "Source"}
    assert source_headings("# Real\n````text\n```\n## Fake\n```\n````\n## Source") == {"Real", "Source"}
    assert source_headings("# Real\n~~~text\n~~~not-a-close\n## Fake\n~~~~\n## Source") == {"Real", "Source"}


def test_current_repository_has_authored_qa_for_every_manifest_record():
    cards, _ = _collection(ROOT)
    require_complete(cards)
    assert all(card["questions"] for card in cards)
