#!/usr/bin/env python3
"""Build source-backed learning cards without model calls or runtime imports."""

from __future__ import annotations

import argparse
import hashlib
import html
from importlib.util import module_from_spec, spec_from_file_location
import json
import posixpath
import re
import sys
from datetime import date
from pathlib import Path, PurePosixPath
from urllib.parse import quote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = Path("docs/learning/all.md")
DOMAINS = {
    "recommendation": "搜广推与 LLM 应用",
    "foundation-models": "基础模型",
    "multimodal-models": "多模态大模型",
    "post-training": "LLM 后训练",
    "agent-research": "Agent",
}
HEADING = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
TERMINAL_STATUS = re.compile(
    r"成本过高|不复现|未复现|不执行复现|不提供(?:可执行)?复现|没有本地模型实现"
)
DIAGNOSTIC_STATUS = re.compile(
    r"诊断|概念演示|concept_demo|未运行|未训练|未验证|未执行|复现级别|保真度"
)


def _topic_module():
    # MkDocs loads this script by file path, including from other working directories.
    name = "_auto_research_learning_topics"
    if name not in sys.modules:
        spec = spec_from_file_location(name, Path(__file__).with_name("learning_topics.py"))
        if spec is None or spec.loader is None:
            raise RuntimeError("Cannot load learning topic generator")
        module = module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
    return sys.modules[name]


def _prose_lines(text: str, *, keep_tables: bool = False) -> list[str]:
    """Discard non-prose blocks before finding headings or paragraphs."""
    result = []
    fence = ""
    fence_length = 0
    equation = ""
    comment = False
    for line in text.splitlines():
        stripped = line.strip()
        if comment:
            comment = "-->" not in stripped
            result.append("")
            continue
        if "<!--" in stripped:
            comment = "-->" not in stripped.split("<!--", 1)[1]
            result.append("")
            continue
        marker = re.match(r"^(`{3,}|~{3,})", stripped)
        if marker:
            run = marker.group(1)
            if not fence:
                fence, fence_length = run[0], len(run)
            elif run[0] == fence and len(run) >= fence_length:
                fence = ""
            result.append("")
            continue
        if fence:
            result.append("")
            continue
        if equation:
            if equation in stripped:
                equation = ""
            result.append("")
            continue
        if stripped.startswith(("$$", r"\[", r"\begin{")):
            end = "$$" if stripped.startswith("$$") else (
                r"\]" if stripped.startswith(r"\[") else r"\end{"
            )
            if end not in stripped[len("$$") if end == "$$" else 2:]:
                equation = end
            result.append("")
            continue
        if stripped.startswith("|"):
            result.append(line if keep_tables else "")
            continue
        if stripped.startswith(("![", "<img", "<table", "</table")):
            result.append("")
            continue
        result.append(line)
    return result


def _plain(text: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^\n]*?\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^\n]*?\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)
    text = re.sub(r"(?<!\\)\$[^$\n]+(?<!\\)\$", "", text)
    text = re.sub(r"\\\(.*?\\\)", "", text)
    text = re.sub(r"<[^>]*>", "", text)
    text = re.sub(r"[*`~]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(?<=[\u3400-\u9fff]) (?=[\u3400-\u9fff])", "", text)
    text = re.sub(r"(?<=[，。；：、！？]) +", "", text)
    return re.sub(r" +(?=[，。；：、！？])", "", text)


def _section(lines: list[str], pattern: str) -> list[str]:
    start = None
    depth = 0
    for index, line in enumerate(lines):
        match = HEADING.match(line)
        if not match:
            continue
        if start is None and re.search(pattern, match.group(2)):
            start, depth = index + 1, len(match.group(1))
        elif start is not None and len(match.group(1)) <= depth:
            return lines[start:index]
    return [] if start is None else lines[start:]


def _paragraphs(lines: list[str]) -> list[str]:
    paragraphs = []
    current = []

    def flush() -> None:
        if current:
            value = _plain(" ".join(current))
            if value:
                paragraphs.append(value)
            current.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped or HEADING.match(line):
            flush()
            continue
        stripped = re.sub(r"^>\s?", "", stripped)
        bullet = re.match(r"^(?:[-+*]|\d+[.)])\s+", stripped)
        if bullet:
            flush()
            stripped = stripped[bullet.end():]
        if stripped and not re.fullmatch(r"[-:= ]+", stripped):
            current.append(stripped)
    flush()
    return paragraphs


def _excerpt(paragraphs: list[str], limit: int = 260) -> str:
    distinct = list(dict.fromkeys(value for value in paragraphs if value))
    selected = []
    for paragraph in distinct:
        sentences = re.split(r"(?<=[。！？；])\s*", paragraph)
        for sentence in sentences:
            if not sentence:
                continue
            if selected and len(" ".join(selected + [sentence])) > limit:
                return " ".join(selected)
            selected.append(sentence)
    return " ".join(selected)


def _metadata(text: str, field: str) -> str:
    match = re.search(
        rf"^\|\s*{re.escape(field)}\s*\|\s*([^|]+?)\s*\|\s*$",
        text,
        re.MULTILINE,
    )
    return _plain(match.group(1)) if match else ""


def _declared_status(lines: list[str], text: str) -> list[str]:
    """Keep explicit local evidence limits even outside the opening paragraph.

    Source placement varies: a status may follow the metadata table, live in a
    table cell, or conclude a cost discussion. Never infer it from adapter type.
    """
    quotes = _paragraphs([
        line if line.strip().startswith(">") else "" for line in lines
    ])
    candidates = [
        value for value in quotes
        if TERMINAL_STATUS.search(value)
        or re.match(r"^(?:本地|本页|本轮|复现|保真度|成本|完整实验|核心机制|机制|L[0-3])", value)
    ]
    for index, line in enumerate(lines):
        heading = HEADING.match(line)
        if not heading or not re.search(r"本地|成本|复现边界|验证", heading.group(2)):
            continue
        end = len(lines)
        for following in range(index + 1, len(lines)):
            next_heading = HEADING.match(lines[following])
            if next_heading and len(next_heading.group(1)) <= len(heading.group(1)):
                end = following
                break
        candidates.extend(_paragraphs(lines[index + 1:end]))
        # A heading can itself carry the terminal decision.
        if TERMINAL_STATUS.search(heading.group(2)):
            candidates.append(_plain(heading.group(2)))
    metadata_text = "\n".join(_prose_lines(text, keep_tables=True))
    for match in re.finditer(r"^\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*$", metadata_text, re.MULTILINE):
        if re.search(r"本地|成本|复现|实验", match.group(1)):
            candidates.append(_plain(match.group(2)))
    statements = [
        sentence.strip()
        for paragraph in candidates
        for sentence in re.split(r"(?<=[。！？；])\s*", paragraph)
        if sentence.strip()
    ]
    terminal = next((value for value in statements if "成本过高" in value and "不复现" in value), "")
    terminal = terminal or next((value for value in statements if "成本过高" in value), "")
    terminal = terminal or next((value for value in statements if TERMINAL_STATUS.search(value)), "")
    diagnostic = next((value for value in statements if DIAGNOSTIC_STATUS.search(value)), "")
    return list(dict.fromkeys(value for value in (terminal, diagnostic) if value))


def _source_link(text: str) -> str:
    match = re.search(
        r"^\|\s*(?:论文|资料)链接\s*\|\s*\[[^\]]+\]\((https?://[^\s)]+)\)",
        text, re.MULTILINE,
    )
    return match.group(1) if match else ""


def _doc_path(root: Path, value: str) -> Path:
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "\\" in value:
        raise ValueError(f"unsafe documentation path: {value}")
    docs = (root / "docs").resolve()
    target = docs.joinpath(*path.parts).resolve()
    if not target.is_relative_to(docs) or not target.is_file():
        raise ValueError(f"missing documentation source: {value}")
    return target


def _publication_date(*values: object) -> str:
    for value in values:
        match = re.search(r"\b\d{4}-\d{2}-\d{2}\b", str(value or ""))
        if match:
            try:
                return date.fromisoformat(match.group()).isoformat()
            except ValueError:
                continue
    return "未标注"


def _card(root: Path, paper: dict, overrides: dict) -> dict[str, str]:
    identity = f"{paper['domain']}:{paper['key']}"
    path = _doc_path(root, paper["detail_path"])
    text = path.read_text(encoding="utf-8")
    lines = _prose_lines(text)
    override = overrides.get(identity, {})
    if not isinstance(override, dict):
        raise ValueError(f"invalid learning-card override: {identity}")
    for field, value in override.items():
        if field not in {"summary", "local_scope", "question", "curated_path"}:
            raise ValueError(f"unknown learning-card override field: {field}")
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"empty learning-card override {identity}: {field}")

    summary = override.get("summary") or _excerpt(
        _paragraphs(_section(lines, r"^背景与主要改动$"))[:2], 260
    )
    intro = []
    for line in lines:
        heading = HEADING.match(line)
        if heading and len(heading.group(1)) >= 2:
            break
        if line.strip().startswith(">"):
            intro.append(line)
    boundary = _paragraphs(_section(lines, r"^(?:复现边界|.*本地.*边界)$"))
    local = _paragraphs(_section(lines, r"^(?:本地|成本)"))
    scope_prose = (
        [override["local_scope"]] if override.get("local_scope")
        else _paragraphs(intro) + boundary[:1] + local[:1]
    )
    local_scope = _excerpt(_declared_status(lines, text) + scope_prose, 320)
    if not summary or not local_scope:
        raise ValueError(f"{identity} needs mechanism and local-scope prose: {path}")
    adapter = paper.get("adapter")
    adapter = adapter if isinstance(adapter, dict) else {}
    organization = (
        paper.get("first_author_affiliation") or adapter.get("organization")
        or _metadata(text, "公司/机构") or _metadata(text, "公司 / 机构") or "未标注机构"
    )
    published = _publication_date(
        paper.get("published"), adapter.get("published"), _metadata(text, "首次公开日期")
    )
    paper_url = paper["paper_url"]
    url = urlsplit(paper_url)
    # A few canonical records refer to a local page for a non-paper source.
    # Use its explicitly documented source link instead of inventing an arXiv URL.
    if not url.scheme and not url.netloc:
        paper_url = _source_link(text)
        url = urlsplit(paper_url)
    if url.scheme not in {"http", "https"} or not url.netloc:
        raise ValueError(f"unsafe paper URL for {identity}: {paper_url}")
    curated = override.get("curated_path", "")
    if curated:
        _doc_path(root, curated)
    slug = re.sub(r"[^a-zA-Z0-9-]+", "-", identity).strip("-").lower()
    anchor = f"paper-{slug}-{hashlib.sha256(identity.encode()).hexdigest()[:8]}"
    return {
        "identity": identity, "domain": paper["domain"], "key": paper["key"],
        "title": str(paper["title"]), "organization": _plain(str(organization)),
        "published": published, "summary": _plain(summary),
        "local_scope": _plain(local_scope), "question": _plain(override.get("question", "")),
        "curated_path": curated, "paper_url": paper_url,
        "source_label": "原始资料" if "## 资料信息" in text else "原论文",
        "detail_path": paper["detail_path"], "anchor": anchor,
        "topics": " ".join(str(item) for item in paper.get("topic", [])),
    }


def _page_href(path: str, from_path: str = "learning/all.md") -> str:
    """Raw HTML links target deployed directory URLs, not Markdown sources."""
    source = PurePosixPath(path)
    route = source.parent if source.name.lower() in {"readme.md", "index.md"} else source.with_suffix("")
    origin = PurePosixPath(from_path)
    origin = origin.parent if origin.name in {"index.md", "README.md"} else origin.with_suffix("")
    relative = posixpath.relpath(str(route), str(origin))
    return quote(relative, safe="/.-") + "/"


def _collection(root: Path) -> tuple[list[dict], list[dict]]:
    root = Path(root)
    payload = json.loads((root / "docs/research-manifest.json").read_text(encoding="utf-8"))
    override_path = root / "docs/learning/card-overrides.json"
    overrides = json.loads(override_path.read_text(encoding="utf-8")) if override_path.exists() else {}
    if not isinstance(overrides, dict):
        raise ValueError("learning-card overrides must be a dictionary")
    cards = [_card(root, paper, overrides) for paper in payload["papers"]]
    identities = [card["identity"] for card in cards]
    if len(set(identities)) != len(identities):
        raise ValueError("duplicate learning-card identity in research manifest")
    cards.sort(key=lambda card: (
        -date.fromisoformat(card["published"]).toordinal() if card["published"] != "未标注" else 0,
        card["domain"], card["key"],
    ))
    topics = _topic_module()
    themes = topics.load_topics(root, set(identities))
    topics.assign_topics(cards, themes)
    return cards, themes


def render_browser(cards: list[dict], themes: list[dict], *,
                   path: str = "learning/all.md", filters: bool = True) -> str:
    esc = html.escape
    lines = [
        '<div class="ar-learning-browser" data-learning-browser data-learning-page-size="12">',
        '<div class="ar-learning-controls">',
        '<label for="learning-search">搜索卡片',
        '<input id="learning-search" type="search" data-learning-search '
        'placeholder="搜索论文、机制、机构或本地边界"></label>',
    ]
    if filters and themes:
        lines += [
            '<label for="learning-theme">主题',
            '<select id="learning-theme" data-learning-theme>',
            '<option value="">全部主题</option>',
            *[f'<option value="{theme["id"]}">{esc(theme["title"])}</option>' for theme in themes],
            '<option value="inbox">待归类</option>',
            '</select></label>',
            '<label for="learning-topic">子主题',
            '<select id="learning-topic" data-learning-topic>',
            '<option value="">全部子主题</option>',
        ]
        for theme in themes:
            lines.extend(
                f'<option value="{theme["id"]}/{topic["id"]}" data-theme="{theme["id"]}">'
                f'{esc(topic["title"])}</option>' for topic in theme["topics"]
            )
        lines += ['</select></label>']
    elif filters:
        domains = sorted({card["domain"] for card in cards})
        lines += [
            '<label for="learning-domain">研究领域',
            '<select id="learning-domain" data-learning-domain><option value="">全部领域</option>',
            *[f'<option value="{esc(value)}">{esc(DOMAINS.get(value, value))}</option>' for value in domains],
            '</select></label>',
        ]
    lines += [
        "</div>",
        f'<p class="ar-learning-status" data-learning-status role="status">共 {len(cards)} 张卡片</p>',
        "<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>",
        '<div class="ar-learning-grid">',
    ]
    for card in cards:
        domain_label = DOMAINS.get(card["domain"], card["domain"])
        search = " ".join([card["title"], domain_label, card["organization"], card["published"],
                           card["summary"], card["local_scope"], card["question"], card["topics"],
                           card["theme_title"], card["subtopic_title"]])
        label = " / ".join(filter(None, (card["theme_title"], card["subtopic_title"])))
        scope_label = "本地范围与边界"
        if "成本过高" in card["local_scope"] and "不复现" in card["local_scope"]:
            scope_label += " · 成本过高，未复现"
        elif re.search(r"核心机制诊断|概念演示|concept_demo|仅为\s?L1", card["local_scope"]):
            scope_label += " · 机制诊断"
        lines += [
            f'<article class="ar-learning-card" data-learning-card data-domain="{esc(card["domain"])}" '
            f'data-theme="{card["theme"]}" data-topic="{card["theme"]}/{card["subtopic"]}" '
            f'data-search="{esc(search)}">',
            f'<p class="ar-learning-card__domain"><a href="{_page_href(card["topic_path"], path)}">{esc(label)}</a></p>',
            f'<h2 id="{card["anchor"]}">{esc(card["title"])}</h2>',
            f'<p class="ar-learning-card__meta">{esc(card["organization"])} · 论文公开：{esc(card["published"])}</p>',
            f'<p><strong>方法要点：</strong>{esc(card["summary"])}</p>',
            f'<details class="ar-learning-boundary"><summary>{scope_label}</summary>',
            f'<p>{esc(card["local_scope"])}</p></details>',
        ]
        if card["question"]:
            lines.append(f'<p class="ar-learning-question"><strong>想一想：</strong>{esc(card["question"])}</p>')
        links = [
            f'<a href="{esc(card["paper_url"])}">{card["source_label"]}</a>',
            f'<a href="{_page_href(card["detail_path"], path)}">实现解读</a>',
        ]
        if card["curated_path"]:
            links.append(f'<a href="{_page_href(card["curated_path"], path)}">阅读精选对比</a>')
        lines += [f'<p class="ar-learning-card__links">{" · ".join(links)}</p>', "</article>"]
    lines += [
        "</div>",
        '<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>',
        "</div>", "",
    ]
    return "\n".join(lines)


def _render_all(cards: list[dict], themes: list[dict]) -> str:
    lines = [
        "---", "hide:", "  - toc", "---", "",
        "<!-- Generated by scripts/generate_learning_cards.py; edit source pages or overrides. -->",
        "# 全部论文学习卡片", "",
        "每张卡片按已有论文解读摘录，帮助快速了解方法与本地验证边界；精选对比另行标注。",
        "日期为论文公开日期。原论文结论、本地实验与未复现的部分请分别理解。", "",
        "[按主题开始学习](index.md) · [查看待归类的新论文](inbox.md)", "",
        render_browser(cards, themes),
    ]
    return "\n".join(lines)


def render(root: Path) -> str:
    return _render_all(*_collection(root))


def _outputs(root: Path) -> dict[Path, str]:
    cards, themes = _collection(root)
    outputs = {OUTPUT: _render_all(cards, themes)}
    topic_module = _topic_module()
    outputs.update(topic_module.guide_pages(themes, cards, render_browser, _page_href))
    inbox = [card for card in cards if card["theme"] == "inbox"]
    outputs[Path("docs/learning/inbox.md")] = "\n".join([
        "---", "hide:", "  - toc", "---", "", topic_module.GENERATED, "",
        "# 待归类的新论文", "",
        "新收录论文先自动出现在这里。完成主题判断后，纳入相应子主题和阅读路线。", "",
        f"当前 {len(inbox)} 张。" if inbox else "当前全部论文均已归类。", "",
        render_browser(inbox, themes, path="learning/inbox.md", filters=False) if inbox else "",
        "[返回学习主题](index.md) · [搜索全部卡片](all.md)", "",
    ])
    # Only the marked region is generated; the current featured card stays editorial.
    index = root / "docs/learning/index.md"
    text = index.read_text(encoding="utf-8") if index.exists() else ""
    if "<!-- learning-topics:" in text:
        if text.count("<!-- learning-topics:start -->") != 1 or text.count(
            "<!-- learning-topics:end -->"
        ) != 1 or text.index("<!-- learning-topics:start -->") > text.index("<!-- learning-topics:end -->"):
            raise ValueError("learning index needs one ordered pair of topic markers")
        tiles = topic_module.topic_tiles(themes, lambda path: _page_href(path, "learning/index.md"))
        block = (f"<!-- learning-topics:start -->\n\n{len(themes)} 个主题 · "
                 f"{sum(len(theme['topics']) for theme in themes)} 张导学卡 · {len(cards)} 张论文卡\n\n"
                 f"{tiles}\n\n<!-- learning-topics:end -->")
        outputs[Path("docs/learning/index.md")] = re.sub(
            r"<!-- learning-topics:start -->.*?<!-- learning-topics:end -->", lambda _: block,
            text, flags=re.S,
        )
    return outputs


def generate(root: Path = ROOT, check: bool = False) -> Path:
    root = Path(root)
    outputs = _outputs(root)
    stale = []
    for relative, expected in outputs.items():
        target = root / relative
        actual = target.read_text(encoding="utf-8") if target.exists() else None
        if expected != actual:
            stale.append((target, expected))
    # Remove only obsolete generated topic pages, never authored cards or unknown files.
    obsolete = [path for path in (root / "docs/learning/paths").rglob("*.md")
                if path.relative_to(root) not in outputs
                and _topic_module().GENERATED in path.read_text(encoding="utf-8")[:180]]
    if check and (stale or obsolete):
        raise ValueError("learning cards are stale; run scripts/generate_learning_cards.py: "
                         + ", ".join(str(path) for path, _ in stale) + str(obsolete or ""))
    for target, expected in stale:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(expected, encoding="utf-8")
    for path in obsolete:
        path.unlink()
    return root / OUTPUT


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if generated cards are stale.")
    args = parser.parse_args()
    try:
        target = generate(ROOT, check=args.check)
    except (OSError, ValueError, KeyError) as error:
        print(error, file=sys.stderr)
        raise SystemExit(1) from error
    print(f"Learning cards {'checked' if args.check else 'generated'}: {target}")


if __name__ == "__main__":
    main()
