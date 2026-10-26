#!/usr/bin/env python3
"""Build source-backed learning cards without model calls or runtime imports."""

from __future__ import annotations

import argparse
import hashlib
import html
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


def _prose_lines(text: str) -> list[str]:
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
        if stripped.startswith(("|", "![", "<img", "<table", "</table")):
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
    local_scope = override.get("local_scope") or _excerpt(
        _paragraphs(intro) + boundary[:1] + local[:1], 320
    )
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


def _page_href(path: str) -> str:
    """Raw HTML links target deployed directory URLs, not Markdown sources."""
    source = PurePosixPath(path)
    route = source.parent if source.name.lower() in {"readme.md", "index.md"} else source.with_suffix("")
    relative = posixpath.relpath(str(route), "learning/all")
    return quote(relative, safe="/.-") + "/"


def render(root: Path) -> str:
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
    domains = sorted({card["domain"] for card in cards}, key=lambda value: DOMAINS.get(value, value))
    esc = html.escape
    lines = [
        "---", "hide:", "  - toc", "---", "",
        "<!-- Generated by scripts/generate_learning_cards.py; edit source pages or overrides. -->",
        "# 全部论文学习卡片", "",
        "每张卡片按已有论文解读摘录，帮助快速了解方法与本地验证边界；精选对比另行标注。",
        "日期为论文公开日期。原论文结论、本地实验与未复现的部分请分别理解。", "",
        '<div class="ar-learning-browser" data-learning-browser>',
        '<div class="ar-learning-controls">',
        '<label for="learning-search">搜索卡片',
        '<input id="learning-search" type="search" data-learning-search '
        'placeholder="搜索论文、机制、机构或本地边界"></label>',
        '<label for="learning-domain">研究领域',
        '<select id="learning-domain" data-learning-domain>',
        '<option value="">全部领域</option>',
    ]
    lines.extend(f'<option value="{esc(value)}">{esc(DOMAINS.get(value, value))}</option>' for value in domains)
    lines += [
        "</select></label>", "</div>",
        f'<p class="ar-learning-status" data-learning-status role="status">共 {len(cards)} 张卡片</p>',
        "<noscript>已显示全部卡片；启用 JavaScript 后可搜索和筛选。</noscript>",
        '<div class="ar-learning-grid">',
    ]
    for card in cards:
        domain_label = DOMAINS.get(card["domain"], card["domain"])
        search = " ".join([card["title"], domain_label, card["organization"], card["published"],
                           card["summary"], card["local_scope"], card["question"], card["topics"]])
        lines += [
            f'<article class="ar-learning-card" data-learning-card data-domain="{esc(card["domain"])}" '
            f'data-search="{esc(search)}">',
            f'<p class="ar-learning-card__domain">{esc(domain_label)}</p>',
            f'<h2 id="{card["anchor"]}">{esc(card["title"])}</h2>',
            f'<p class="ar-learning-card__meta">{esc(card["organization"])} · 论文公开：{esc(card["published"])}</p>',
            f'<p><strong>方法要点：</strong>{esc(card["summary"])}</p>',
            f'<p><strong>本地范围与边界：</strong>{esc(card["local_scope"])}</p>',
        ]
        if card["question"]:
            lines.append(f'<p class="ar-learning-question"><strong>想一想：</strong>{esc(card["question"])}</p>')
        links = [
            f'<a href="{esc(card["paper_url"])}">{card["source_label"]}</a>',
            f'<a href="{_page_href(card["detail_path"])}">实现解读</a>',
        ]
        if card["curated_path"]:
            links.append(f'<a href="{_page_href(card["curated_path"])}">阅读精选对比</a>')
        lines += [f'<p class="ar-learning-card__links">{" · ".join(links)}</p>', "</article>"]
    lines += [
        "</div>",
        '<button type="button" class="ar-learning-more" data-learning-more hidden>显示更多</button>',
        "</div>", "",
    ]
    return "\n".join(lines)


def generate(root: Path = ROOT, check: bool = False) -> Path:
    root = Path(root)
    target = root / OUTPUT
    expected = render(root)
    actual = target.read_text(encoding="utf-8") if target.exists() else None
    if expected != actual:
        if check:
            raise ValueError(f"learning cards are stale; run scripts/generate_learning_cards.py: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(expected, encoding="utf-8")
    return target


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
