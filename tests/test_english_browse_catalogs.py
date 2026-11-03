"""Coverage and integrity checks for bilingual research browse catalogs."""

from hashlib import sha256
from pathlib import Path

import pytest

from scripts.english_browse_catalogs import CATALOG_PAIRS, catalog_pages


ZH_OLD = "docs/agent-research/old/README.md"
ZH_NEW = "docs/agent-research/new/README.md"
TOPIC = "docs/agent-research/catalog/by-topic.md"
ORG = "docs/agent-research/catalog/by-organization.md"
INDEX = "docs/agent-research/catalog.md"


def put(root, name, text):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def english_paper(root, chinese, summary, code="No author code found."):
    source = "# 论文\n"
    put(root, chinese, source)
    target = str(Path(chinese).with_name("README-en.md"))
    digest = sha256(source.encode()).hexdigest()
    put(
        root, target,
        f"<!-- source-sha256: {digest} -->\n\n[简体中文](README.md)\n\n"
        f"# Paper\n\n## Paper information\n\n| Authors' open-source code | {code} |\n\n"
        f"## What the paper changes\n\n{summary}\n",
    )
    return target


@pytest.fixture
def research(tmp_path):
    english_paper(tmp_path, ZH_OLD, "Old method applies its frozen retriever to new tasks.")
    english_paper(
        tmp_path, ZH_NEW,
        "Earlier methods can overfit to held-out labels.\n\n"
        "New method scores evidence. It does not access held-out labels. "
        "This third sentence is not part of the browse synopsis.",
        "See the [authors' release](https://github.com/example/paper); only evaluation code.",
    )
    rows = [
        {"key": "old", "title": "Old method", "detail_path": ZH_OLD.removeprefix("docs/")},
        {"key": "new", "title": "New method", "detail_path": ZH_NEW.removeprefix("docs/"),
         "code": "https://github.com/example/paper", "implementation_status": "deferred_high_cost",
         "review_done": True},
    ]
    return tmp_path, rows


def render(root, rows, *sources):
    pairs = {source: CATALOG_PAIRS[source] for source in sources}
    return catalog_pages(root, rows, pairs=pairs)


def test_all_twenty_four_supported_sources_are_paired():
    assert len(CATALOG_PAIRS) == 24
    assert "docs/reproductions/catalog/README.md" in CATALOG_PAIRS
    assert all(target == source.replace("docs/", "docs/en/", 1)
               for source, target in CATALOG_PAIRS.items())


def test_browse_preserves_taxonomy_memberships_order_references_and_scope(research):
    root, rows = research
    put(
        root, TOPIC,
        "# Agent 研究：按主题\n\n## 规划、搜索与反思\n\n### 树搜索与自我改进\n\n"
        "- [新方法](../new/README.md)（`new`）：中文介绍。 [原文](https://example.org/paper#method)\n"
        "- [Old method](../old/README.md)（`old`）：中文介绍。\n\n"
        "### Harness 与自我改进\n\n- [New method](../new/README.md)：另一中文介绍。\n",
    )
    result = render(root, rows, TOPIC)[CATALOG_PAIRS[TOPIC]]
    assert "## Planning, search, and reflection" in result
    assert "### Tree search and self-improvement" in result
    assert "### Harnesses and self-improvement" in result
    assert result.count("../../../agent-research/new/README-en.md") == 2
    assert result.index("New method") < result.index("Old method")
    assert "New method scores evidence. It does not access held-out labels." in result
    assert "third sentence" not in result
    assert "research material only, no executable entry" in result
    assert "https://example.org/paper#method" in result
    assert "[简体中文](../../../agent-research/catalog/by-topic.md)" in result
    digest = sha256((root / TOPIC).read_bytes()).hexdigest()
    assert f"<!-- source-sha256: {digest} -->" in result
    assert not (root / CATALOG_PAIRS[TOPIC]).exists()


def test_organization_prefix_preserves_date_and_co_first_author(research):
    root, rows = research
    put(
        root, ORG,
        "# Agent 研究：按机构/公司/学校\n\n## Google / Emory University（共同署名）\n"
        "- 2026-10-19 · 一作：A / B（共同一作，随机排序） · [New method](../new/README.md)"
        "（`new`）：中文介绍。\n",
    )
    result = render(root, rows, ORG)[CATALOG_PAIRS[ORG]]
    assert "## Google / Emory University (joint affiliation)" in result
    assert "2026-10-19 · First author: A / B (co-first authors, randomized order) · " in result


def test_index_preserves_local_evidence_distinctions_and_crosslinks(research):
    root, rows = research
    put(
        root, INDEX,
        "# Agent 研究论文与资料索引\n\n## 论文实现与研究资料\n\n"
        "| 方向 | 方法 | 一作机构与日期 | 原作者代码 | 本地入口 |\n"
        "|---|---|---|---|---|\n"
        "| 自进化与工作流 | [New method](new/README.md) | Example Institute，2026-10-19 | "
        "[原作者入口](https://github.com/example/paper)；另有公开数据 https://example.org/dataset | "
        "计划键 `new`：成本过高，不复现（审查 DONE）；仅研究资料，无可执行入口。 |\n\n"
        "- [按机构/公司/学校](catalog/by-organization.md)\n",
    )
    result = render(root, rows, INDEX)[CATALOG_PAIRS[INDEX]]
    assert "First author's institution and first publication" in result
    assert "Self-improvement and workflows" in result
    assert "Example Institute, 2026-10-19" in result
    assert "only evaluation code" in result
    assert "https://example.org/dataset" in result
    assert "Planned key `new`" in result and "no executable entry" in result
    assert "[Browse by institution, company, or university](catalog/by-organization.md)" in result


def test_system_one_product_links_are_not_treated_as_papers(tmp_path):
    source = "docs/system-one/catalog/by-topic.md"
    put(
        tmp_path, source,
        "# 结构化决策：按主题\n\n## 类型化决策协议\n\n"
        "- [TypeSafe Jev](../implementations.md#official-jev)："
        "Choice、Score、Noul 三类问题共享状态输入，返回机器可直接消费的概率化结果。\n",
    )
    result = render(tmp_path, [], source)[CATALOG_PAIRS[source]]
    assert "## Typed decision protocols" in result
    assert "[TypeSafe Jev](../implementations.md#official-jev)" in result
    assert "machine-readable probabilities" in result


@pytest.mark.parametrize(
    ("case", "error"),
    [("missing", "reviewed English write-up required"),
     ("stale", "stale or unpaired English write-up"),
     ("unreviewed-summary", "needs a method paragraph"),
     ("unknown-label", "add a reviewed English label")],
)
def test_render_fails_closed_and_does_not_write_any_page(research, case, error):
    root, rows = research
    put(root, TOPIC, "# 按主题\n\n- [Old method](../old/README.md)：中文介绍。\n")
    put(root, ORG, "# 按公司\n\n- [New method](../new/README.md)：中文介绍。\n")
    target = (root / ZH_NEW).with_name("README-en.md")
    if case == "missing":
        target.unlink()
    elif case == "stale":
        put(root, ZH_NEW, "# Changed Chinese source\n")
    elif case == "unreviewed-summary":
        target.write_text(target.read_text().replace("What the paper changes", "Metadata only"))
    else:
        put(root, ORG, "# 未翻译的新目录\n")
    with pytest.raises(ValueError, match=error):
        render(root, rows, TOPIC, ORG)
    assert not (root / CATALOG_PAIRS[TOPIC]).exists()
    assert not (root / CATALOG_PAIRS[ORG]).exists()
