from __future__ import annotations

import json
import re
from html.parser import HTMLParser
from pathlib import Path

import pytest

from scripts.generate_learning_cards import generate, render


SOURCE = """# 测试方法

> **核心机制诊断。** 本地执行状态更新；没有运行完整模型。

## 论文信息

| 字段 | 内容 |
|---|---|
| 公司/机构 | 来源机构 |
| 首次公开日期 | 2025-04-03（arXiv v1） |

## 原始论文总结

### 背景与主要改动

为避免历史信息被过早压缩，
方法用少量查询重复读取历史，保留候选相关信号。

```python
SHOULD_NOT_APPEAR_FROM_FENCE
### 背景与主要改动
```

![SHOULD_NOT_APPEAR_FROM_IMAGE](image.png)

$$
SHOULD_NOT_APPEAR_FROM_EQUATION
$$

| SHOULD_NOT_APPEAR_FROM_TABLE | value |
|---|---|

### 核心公式

SHOULD_NOT_APPEAR_FROM_NEXT_SECTION

## 本地复现

本地仅在小数据上检查机制；未验证工业吞吐。

### 复现边界

只验证状态转换，不把诊断当作模型能力。
"""


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _paper(key="example", domain="recommendation", **values):
    return {
        "domain": domain,
        "key": key,
        "title": f"测试方法 {key}",
        "paper_url": "https://arxiv.org/abs/2504.00001",
        "detail_path": f"reproductions/{domain}-{key}/README.md",
        "topic": ["历史压缩"],
        "first_author_affiliation": None,
        "published": None,
        "adapter": {"organization": None},
        **values,
    }


def _manifest(root, papers):
    _write(root, "docs/research-manifest.json", json.dumps({"papers": papers}))
    for paper in papers:
        _write(root, f"docs/{paper['detail_path']}", SOURCE)


@pytest.fixture
def repository(tmp_path):
    _manifest(tmp_path, [_paper()])
    return tmp_path


class _Cards(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.cards = []
        self.headings = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "data-learning-card" in attrs:
            self.cards.append(attrs)
        if tag == "h2":
            self.headings.append(attrs["id"])


def test_new_paper_appears_and_removed_paper_disappears(repository):
    target = generate(repository)
    initial = _Cards(target.read_text())
    assert len(initial.cards) == 1
    added = _paper("new", "agent-research", adapter="new")
    _manifest(repository, [_paper(), added])
    generate(repository)
    content = target.read_text()
    assert len(_Cards(content).cards) == 2
    assert "测试方法 new" in content
    _manifest(repository, [added])
    generate(repository)
    content = target.read_text()
    assert len(_Cards(content).cards) == 1
    assert "测试方法 example" not in content


def test_same_key_in_different_domains_has_unique_stable_identity(repository):
    _manifest(repository, [_paper("same"), _paper("same", "agent-research", adapter="same")])
    first = _Cards(render(repository)).headings
    assert len(set(first)) == 2
    _manifest(repository, [_paper("same", "agent-research", adapter="same"), _paper("same")])
    assert _Cards(render(repository)).headings == first


def test_metadata_fallback_from_source_and_dictionary_adapter(repository):
    content = render(repository)
    assert "来源机构 · 论文公开：2025-04-03" in content
    _manifest(repository, [_paper(adapter={"organization": "注册机构", "published": "2026-01-02"})])
    content = render(repository)
    assert "注册机构 · 论文公开：2026-01-02" in content
    assert "实现日期" not in content


def test_invalid_date_falls_back_and_unknown_domain_remains_visible(repository):
    _manifest(repository, [_paper(domain="future-domain", adapter="example", published="2026-02-30")])
    content = render(repository)
    assert "future-domain" in content
    assert "论文公开：2025-04-03" in content


def test_excerpts_skip_non_prose_and_stop_at_next_heading(repository):
    content = render(repository)
    assert "为避免历史信息被过早压缩，方法用少量查询重复读取历史" in content
    assert "本地执行状态更新；没有运行完整模型" in content
    assert "只验证状态转换，不把诊断当作模型能力" in content
    assert "SHOULD_NOT_APPEAR" not in content
    assert "<article" in content
    assert not any("hidden" in card for card in _Cards(content).cards)
    assert 'data-learning-status role="status"' in content
    assert '<noscript>' in content


def test_html_escaped_and_non_http_paper_url_rejected(repository):
    _manifest(repository, [_paper(title='<img src=x onerror="alert(1)">',
                                  first_author_affiliation='A " onmouseover="bad')])
    content = render(repository)
    assert '&lt;img src=x onerror=&quot;alert(1)&quot;&gt;' in content
    assert '<img src=x' not in content
    assert 'onmouseover=&quot;bad' in content
    assert all('onmouseover' not in attrs for attrs in _Cards(content).cards)
    _manifest(repository, [_paper(paper_url="javascript:alert(1)")])
    with pytest.raises(ValueError, match="unsafe paper URL"):
        render(repository)


def test_missing_detail_file_fails_without_partial_output(repository):
    (repository / "docs/reproductions/recommendation-example/README.md").unlink()
    with pytest.raises(ValueError, match="missing documentation source"):
        generate(repository)
    assert not (repository / "docs/learning/all.md").exists()


def test_missing_manifest_or_mechanism_source_fails(repository):
    source = repository / "docs/reproductions/recommendation-example/README.md"
    source.write_text(SOURCE.replace("### 背景与主要改动", "### 不相关段落"))
    with pytest.raises(ValueError, match="needs mechanism and local-scope prose"):
        generate(repository)
    (repository / "docs/research-manifest.json").unlink()
    with pytest.raises(FileNotFoundError):
        generate(repository)


def test_paths_cannot_escape_documentation_root(repository):
    payload = {"papers": [_paper(detail_path="../private.md")]}
    _write(repository, "docs/research-manifest.json", json.dumps(payload))
    with pytest.raises(ValueError, match="unsafe documentation path"):
        render(repository)


def test_repeat_generation_is_idempotent_and_check_never_writes(repository):
    target = generate(repository)
    original = target.read_bytes()
    modified = target.stat().st_mtime_ns
    generate(repository)
    generate(repository, check=True)
    assert target.read_bytes() == original
    assert target.stat().st_mtime_ns == modified
    target.write_text("stale")
    with pytest.raises(ValueError, match="learning cards are stale"):
        generate(repository, check=True)
    assert target.read_text() == "stale"


def test_overrides_and_curated_source_are_preserved(repository):
    curated = _write(repository, "docs/learning/001-example.md", "# 人工精选\n保留原文。\n")
    index = _write(repository, "docs/learning/index.md", "# 学习入口\n")
    overrides = {
        "recommendation:example": {
            "summary": "核验过的机制说明。",
            "local_scope": "核验过的实现边界。",
            "question": "什么时候值得支付更高的历史交互成本？",
            "curated_path": "learning/001-example.md",
        }
    }
    _write(repository, "docs/learning/card-overrides.json", json.dumps(overrides))
    generate(repository)
    content = (repository / "docs/learning/all.md").read_text()
    assert "核验过的机制说明" in content
    assert "核验过的实现边界" in content
    assert "什么时候值得支付" in content
    assert 'href="../001-example/"' in content
    assert curated.read_text() == "# 人工精选\n保留原文。\n"
    assert index.read_text() == "# 学习入口\n"


def test_override_curated_link_must_exist(repository):
    _write(repository, "docs/learning/card-overrides.json", json.dumps({
        "recommendation:example": {"curated_path": "learning/missing.md"}
    }))
    with pytest.raises(ValueError, match="missing documentation source"):
        generate(repository)


def test_review_only_source_keeps_not_reproduced_status(repository):
    source = SOURCE.replace(
        "**核心机制诊断。** 本地执行状态更新；没有运行完整模型。",
        "完整实验成本过高，不复现（审查 DONE）；没有本地模型实现。",
    ).replace("## 本地复现", "## 成本决策与本地状态")
    _write(repository, "docs/reproductions/recommendation-example/README.md", source)
    content = render(repository)
    assert "成本过高，不复现（审查 DONE）；没有本地模型实现" in content


def test_summary_does_not_read_omitted_mechanisms_from_paper_specs(repository):
    _write(repository, "src/auto_research/reproductions/example/paper.yaml",
           '{"mechanisms": ["OMITTED_COMPONENT_NOT_IMPLEMENTED"]}')
    assert "OMITTED_COMPONENT_NOT_IMPLEMENTED" not in render(repository)


def test_duplicate_identity_fails_instead_of_creating_duplicate_cards(repository):
    _manifest(repository, [_paper(), _paper()])
    with pytest.raises(ValueError, match="duplicate learning-card identity"):
        render(repository)


def test_web_source_uses_documented_url_instead_of_local_manifest_placeholder(repository):
    _manifest(repository, [_paper(paper_url="web-source/README.md")])
    source = SOURCE.replace("## 论文信息", "## 资料信息").replace(
        "| 字段 | 内容 |", "| 字段 | 内容 |\n| 资料链接 | [作者说明](https://example.org/source) |"
    )
    _write(repository, "docs/reproductions/recommendation-example/README.md", source)
    content = render(repository)
    assert 'href="https://example.org/source">原始资料</a>' in content
    assert 'href="web-source/README.md"' not in content


def test_all_paper_links_are_individually_present(repository):
    _manifest(repository, [_paper(), _paper("other", paper_url="https://example.org/other")])
    content = render(repository)
    assert len(re.findall(r'>原论文</a>', content)) == 2
    assert len(re.findall(r'>实现解读</a>', content)) == 2
    assert 'href="../../reproductions/recommendation-other/"' in content
