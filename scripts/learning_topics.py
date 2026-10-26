"""Validated, human-authored learning paths over the canonical paper collection.

Membership is explicit so a new paper cannot silently acquire a misleading topic.
Unassigned additions remain discoverable in the inbox until their author places them.
"""

from __future__ import annotations

import html
import json
import posixpath
import re
from pathlib import Path, PurePosixPath
from urllib.parse import quote


THEME_ORDER = (
    "recommendation", "foundation-models", "system-one", "multimodal-models",
    "post-training", "agent-research",
)
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
GENERATED = "<!-- Generated learning path; edit docs/learning/topics/*.json. -->"


def load_topics(root: Path, identities: set[str]) -> list[dict]:
    themes = []
    assigned: set[str] = set()
    for path in sorted((root / "docs/learning/topics").glob("*.json")):
        theme = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(theme, dict) or not isinstance(theme.get("id"), str) or not SLUG.fullmatch(
            theme["id"]
        ) or path.stem != theme["id"]:
            raise ValueError(f"invalid learning theme ID: {path}")
        _require_text(theme, ("title", "intro"), str(path))
        if not isinstance(theme.get("topics"), list) or not theme["topics"]:
            raise ValueError(f"empty learning theme: {path}")
        topic_ids = set()
        for topic in theme["topics"]:
            if not isinstance(topic, dict):
                raise ValueError(f"invalid learning subtopic: {path}")
            slug = topic.get("id", "")
            if not isinstance(slug, str) or not SLUG.fullmatch(slug) or slug in topic_ids:
                raise ValueError(f"invalid or duplicate learning subtopic: {path}: {slug}")
            topic_ids.add(slug)
            label = f"{theme['id']}/{slug}"
            _require_text(topic, (
                "title", "question", "takeaway", "example", "pitfall", "reading_order",
            ), label)
            _require_text(topic.get("self_test", {}), ("question", "answer"), label)
            members = topic.get("papers")
            if not isinstance(members, list) or not members or any(
                not isinstance(value, str) for value in members
            ):
                raise ValueError(f"empty or invalid learning topic membership: {label}")
            for identity in members:
                if identity not in identities:
                    raise ValueError(f"unknown learning paper: {identity} in {label}")
                if identity in assigned:
                    raise ValueError(f"duplicate learning topic assignment: {identity}")
                assigned.add(identity)
            starters = topic.get("start_here")
            if not isinstance(starters, list) or not starters or any(
                identity not in members for identity in starters
            ) or len(set(starters)) != len(starters):
                raise ValueError(f"reading path must use distinct topic members: {label}")
        themes.append(theme)
    rank = {key: index for index, key in enumerate(THEME_ORDER)}
    return sorted(themes, key=lambda theme: (rank.get(theme["id"], 99), theme["id"]))


def _require_text(record: dict, fields: tuple[str, ...], label: str) -> None:
    for field in fields:
        if not isinstance(record, dict) or not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"learning guide needs {field}: {label}")


def assign_topics(cards: list[dict], themes: list[dict]) -> None:
    index = {
        identity: (theme, topic)
        for theme in themes for topic in theme["topics"] for identity in topic["papers"]
    }
    for card in cards:
        pair = index.get(card["identity"])
        theme, topic = pair if pair else ({"id": "inbox", "title": "待归类"}, {})
        card.update({
            "theme": theme["id"], "theme_title": theme["title"],
            "subtopic": topic.get("id", ""), "subtopic_title": topic.get("title", ""),
            "topic_path": (
                f"learning/paths/{theme['id']}/{topic['id']}.md" if topic else "learning/inbox.md"
            ),
        })


def navigation(themes: list[dict]) -> list[dict]:
    return [{theme["title"]: [
        {"主题概览": f"learning/paths/{theme['id']}/index.md"},
        *[{topic["title"]: f"learning/paths/{theme['id']}/{topic['id']}.md"}
          for topic in theme["topics"]],
    ]} for theme in themes]


def topic_tiles(themes: list[dict], href, *, expanded: bool = False) -> str:
    esc = html.escape
    lines = ['<div class="ar-learning-topics">']
    for theme in themes:
        count = sum(len(topic["papers"]) for topic in theme["topics"])
        url = href(f"learning/paths/{theme['id']}/index.md")
        lines += [
            '<article class="ar-learning-topic-tile">',
            f'<h2><a href="{url}">{esc(theme["title"])}</a></h2>',
            f'<p>{esc(theme["intro"])}</p>',
            f'<p class="ar-learning-topic-meta">{len(theme["topics"])} 个子主题 · {count} 张论文卡</p>',
            f'<details{" open" if expanded else ""}><summary>查看子主题与导学卡</summary><ul>',
        ]
        for topic in theme["topics"]:
            path = f"learning/paths/{theme['id']}/{topic['id']}.md"
            lines.append(
                f'<li><a href="{href(path)}">{esc(topic["title"])}</a>'
                f'<span>{len(topic["papers"])}</span></li>'
            )
        lines += ['</ul></details>', '</article>']
    return "\n".join(lines + ['</div>'])


def guide_pages(themes: list[dict], cards: list[dict], browser, page_href) -> dict[Path, str]:
    """Render static topic pages; all research claims remain linked to sources."""
    by_identity = {card["identity"]: card for card in cards}
    output = {}
    for theme in themes:
        parent = f"learning/paths/{theme['id']}/index.md"
        overview = [GENERATED, "", f"# {theme['title']}", "", theme["intro"], "",
                    "每次选一个问题，先读导学卡，再按阅读顺序看代表论文。", ""]
        overview.append('<div class="ar-learning-topics">')
        esc = html.escape
        for topic in theme["topics"]:
            url = page_href(f"learning/paths/{theme['id']}/{topic['id']}.md", parent)
            overview += [
                '<article class="ar-learning-topic-tile">',
                f'<h2><a href="{url}">{esc(topic["title"])}</a></h2>',
                f'<p>{esc(topic["question"])}</p>',
                f'<p class="ar-learning-topic-meta">导学约 3 分钟 · {len(topic["papers"])} 张论文卡</p>',
                '</article>',
            ]
        overview.append('</div>')
        overview += ["", "[返回全部主题](../../index.md)", ""]
        output[Path("docs") / parent] = "\n".join(overview)
        for topic in theme["topics"]:
            path = f"learning/paths/{theme['id']}/{topic['id']}.md"
            members = [card for card in cards if card["identity"] in topic["papers"]]
            lines = [
                "---", "hide:", "  - toc", "---", "", GENERATED, "",
                f"# {topic['title']}", "",
                f"[{theme['title']}](index.md) / 子主题导学 · 约 3 分钟 · {len(members)} 张论文卡", "",
                "## 先想一个问题", "", topic["question"], "",
                "## 记住这一点", "", topic["takeaway"], "",
                "## 一个例子", "", topic["example"], "",
                "## 什么时候要小心", "", topic["pitfall"], "",
                "## 先读这几篇", "", topic["reading_order"], "",
            ]
            for index, identity in enumerate(topic["start_here"], 1):
                card = by_identity[identity]
                title = html.escape(" ".join(card["title"].split())).replace("[", r"\[").replace("]", r"\]")
                source_url = quote(card["paper_url"], safe=":/?&=%#@+,;~.-_")
                lines.append(
                    f"{index}. [{title}]({doc_href(card['detail_path'], path)})"
                    f" · [{card['source_label']}]({source_url})"
                )
            lines += [
                "", "## 自测一下", "", topic["self_test"]["question"], "",
                "??? note \"展开参考答案\"", "",
                *[f"    {line}" if line else "" for line in topic["self_test"]["answer"].splitlines()],
                "", "## 这个子主题的论文卡片", "",
                "导学提炼自上述代表论文及仓库解读。以下卡片摘录各自来源；是否复现、验证到哪一步，以卡内说明为准。", "",
                browser(members, themes, path=path, filters=False), "",
                f"[跨主题搜索全部卡片]({doc_href('learning/all.md', path)})", "",
            ]
            output[Path("docs") / path] = "\n".join(lines)
    return output


def doc_href(path: str, origin: str) -> str:
    return posixpath.relpath(path, str(PurePosixPath(origin).parent))
