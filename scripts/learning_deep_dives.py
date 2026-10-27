"""Authored cross-paper readings, with an explicit topic membership update gate."""

from __future__ import annotations

import html
import hashlib
import json
import posixpath
import re
from datetime import date
from pathlib import Path, PurePosixPath


GENERATED = "<!-- Generated topic deep dive; edit docs/learning/deep-dives/*.json. -->"
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")


def source_revisions(root, cards, identities):
    """Read-only fingerprints for the sources reviewed in an authored update."""
    index = {card["identity"]: card for card in cards}
    return {identity: hashlib.sha256(
        (root / "docs" / index[identity]["detail_path"]).read_bytes()
    ).hexdigest() for identity in identities}


def page_path(theme: str, topic: str) -> str:
    return f"learning/deep-dives/{theme}/{topic}.md"


def _text(record, fields, label):
    if not isinstance(record, dict) or any(
        not isinstance(record.get(field), str) or not record[field].strip() for field in fields
    ):
        raise ValueError(f"deep dive needs {', '.join(fields)}: {label}")


def _date(value, label):
    try:
        if not isinstance(value, str) or date.fromisoformat(value).isoformat() != value:
            raise ValueError()
    except ValueError as error:
        raise ValueError(f"invalid deep-dive date: {label}") from error


def _papers(values, members, label, minimum=1):
    if not isinstance(values, list) or len(values) < minimum or any(
        not isinstance(value, str) or value not in members for value in values
    ) or len(set(values)) != len(values):
        raise ValueError(f"deep dive needs {minimum} distinct topic papers: {label}")
    return set(values)


def load_deep_dives(root, themes, cards, source_headings, *, required=False):
    """Fail before writing if a new topic member has no authored card update."""
    directory = root / "docs/learning/deep-dives"
    files = sorted(directory.glob("*.json"))
    if not files and not required:
        return {}
    by_identity = {card["identity"]: card for card in cards}
    expected = {theme["id"]: theme for theme in themes}
    bank = {}
    for path in files:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("schema_version") != 1 or (
            payload.get("theme") != path.stem or path.stem not in expected
            or not isinstance(payload.get("topics"), dict)
        ):
            raise ValueError(f"invalid deep-dive schema: {path}")
        topics = {topic["id"]: topic for topic in expected[path.stem]["topics"]}
        if set(payload["topics"]) != set(topics):
            raise ValueError(f"deep-dive topics differ from taxonomy: {path}")
        for topic_id, record in payload["topics"].items():
            label = f"{path.stem}/{topic_id}"
            _text(record, ("title", "thesis", "updated"), label)
            _date(record["updated"], label)
            members = set(topics[topic_id]["papers"])
            reviewed = _papers(record.get("reviewed_papers"), members, label)
            if reviewed != members:
                raise ValueError(f"topic deep dive needs an update for new papers: {label}: "
                                 + ", ".join(sorted(members - reviewed)))
            axes = record.get("axes")
            if not isinstance(axes, list) or not 2 <= len(axes) <= 4 or any(
                not isinstance(axis, str) or not axis.strip() for axis in axes
            ) or len(set(axes)) != len(axes):
                raise ValueError(f"deep dive needs 2–4 comparison axes: {label}")
            rows = record.get("comparisons")
            if not isinstance(rows, list) or len(rows) < 3:
                raise ValueError(f"deep dive needs at least three comparison papers: {label}")
            representatives = []
            for row in rows:
                _text(row, ("paper", "position", "tradeoff"), label)
                identity = row["paper"]
                _papers([identity], members, label)
                source = (root / "docs" / by_identity[identity]["detail_path"]).read_text(encoding="utf-8")
                headings = source_headings(source)
                sections = row.get("sections")
                if not isinstance(sections, list) or not sections or any(
                    not isinstance(section, str) or section not in headings for section in sections
                ):
                    raise ValueError(f"deep dive references missing source section: {label}/{identity}")
                representatives.append(identity)
            if len(set(representatives)) != len(representatives):
                raise ValueError(f"duplicate deep-dive comparison paper: {label}")
            for field, minimum, text_fields in (
                ("analysis", 2, ("title", "body")),
                ("questions", 3, ("id", "question", "answer", "example")),
                ("updates", 1, ("date", "summary")),
            ):
                items = record.get(field)
                if not isinstance(items, list) or len(items) < minimum:
                    raise ValueError(f"deep dive needs {minimum} {field}: {label}")
                ids, prompts, covered, dates = set(), set(), set(), []
                for item in items:
                    _text(item, text_fields, label)
                    covered |= _papers(item.get("papers"), members, label, 1 if field == "updates" else 2)
                    if field == "questions":
                        key = item["id"]
                        if not SLUG.fullmatch(key) or key in ids or item["question"] in prompts:
                            raise ValueError(f"invalid or duplicate deep-dive question: {label}/{key}")
                        ids.add(key)
                        prompts.add(item["question"])
                    if field == "updates":
                        _date(item["date"], label)
                        dates.append(item["date"])
                        revisions = item.get("source_revisions")
                        if not isinstance(revisions, dict) or set(revisions) != set(item["papers"]) or any(
                            not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value)
                            for value in revisions.values()
                        ):
                            raise ValueError(f"deep-dive update needs source revisions for its papers: {label}")
                if field == "updates" and (covered != members or record["updated"] != max(dates)
                                           or dates != sorted(dates)):
                    raise ValueError(f"deep-dive update log must cover every topic paper and latest date: {label}")
            current_revisions = source_revisions(root, cards, sorted(members))
            for identity in members:
                latest = [update for update in record["updates"] if identity in update["papers"]][-1]
                if latest["source_revisions"][identity] != current_revisions[identity]:
                    raise ValueError(f"topic deep-dive source changed; review and append an update: {label}/{identity}")
                questions = by_identity[identity].get("questions", [])
                if questions:
                    first_added = min(question["added"] for question in questions)
                    last_reviewed = max(update["date"] for update in record["updates"]
                                        if identity in update["papers"])
                    if last_reviewed < first_added:
                        raise ValueError(f"deep-dive update predates paper's first authored questions: {label}/{identity}")
            bank[label] = record
    missing = [f"{theme['id']}/{topic['id']}" for theme in themes for topic in theme["topics"]
               if f"{theme['id']}/{topic['id']}" not in bank]
    if missing:
        raise ValueError("topics need authored deep dives: " + ", ".join(missing))
    if required and any(card["theme"] == "inbox" for card in cards):
        raise ValueError("new papers need a topic assignment and an authored topic deep-dive update")
    return bank


def navigation(themes):
    return [{"精读卡片汇总": "learning/deep-dives/index.md"}, *[
        {theme["title"]: [{topic["title"]: page_path(theme["id"], topic["id"])}
                           for topic in theme["topics"]]} for theme in themes
    ]]


def _relative(target, origin):
    return posixpath.relpath(target, str(PurePosixPath(origin).parent))


def _md(value):
    return html.escape(" ".join(value.split())).replace("[", r"\[").replace("]", r"\]").replace("|", r"\|")


def render_pages(themes, cards, bank, href):
    if not bank:
        return {}
    by_identity = {card["identity"]: card for card in cards}
    output = {}
    index_path = "learning/deep-dives/index.md"
    index = ["---", "hide:", "  - toc", "---", "", GENERATED, "", "# 专题精读", "",
             "围绕一个问题，把多篇论文放在一起比较：先读机制对照，再看取舍分析，最后用跨论文问答自测。", "",
             "每个子主题维护一张卡片。新论文进入后，更新对应卡片的比较或结论，并记录这次变化；不必再从头读整批论文。", "",
             f"{len(bank)} 张精读卡片 · {len(cards)} 篇主题资料 · 按主题折叠", ""]
    for theme in themes:
        index += [f'<details class="ar-deep-shelf"><summary>{html.escape(theme["title"])} · {len(theme["topics"])} 张</summary>',
                  '<div class="ar-deep-grid">']
        for topic in theme["topics"]:
            record = bank[f"{theme['id']}/{topic['id']}"]
            path = page_path(theme["id"], topic["id"])
            index += ['<article class="ar-deep-tile">',
                      f'<h2><a href="{href(path, index_path)}">{html.escape(record["title"])}</a></h2>',
                      f'<p>{html.escape(record["thesis"])}</p>',
                      f'<p class="ar-learning-topic-meta">{len(record["comparisons"])} 篇重点对照 · '
                      f'{len(record["questions"])} 个跨论文问答 · {record["updated"]}</p>', '</article>']
            output[Path("docs") / path] = _render_card(theme, topic, record, by_identity, href, path)
        index += ['</div></details>', '']
    index += ['[逐篇四层问答](../all.md) · [学习入口](../index.md)', '']
    output[Path("docs") / index_path] = "\n".join(index)
    return output


def _render_card(theme, topic, record, cards, href, path):
    def sources(identities):
        return " · ".join(f'[{_md(cards[identity]["key"])}]('
                          f'{_relative(cards[identity]["detail_path"], path)})' for identity in identities)

    bank_path = f"learning/paths/{theme['id']}/{topic['id']}.md"
    lines = ["---", "hide:", "  - toc", "---", "", GENERATED, "", f'# {record["title"]}', "",
             f'[{theme["title"]}]({_relative("learning/deep-dives/index.md", path)}) · '
             f'更新 {record["updated"]} · {len(topic["papers"])} 篇主题资料 / '
             f'{len(record["comparisons"])} 篇重点对照', "", record["thesis"], "",
             f'[机制对照](#comparison) · [取舍分析](#analysis) · [跨论文问答](#questions) · '
             f'[更新记录](#updates) · [本主题逐篇问答]({_relative(bank_path, path)})', "",
             '!!! note "怎么读这张卡片"', "",
             '    重点比较下表代表论文；完整主题目录保留在文末。机制与假设的对照不等于统一 benchmark 的性能排名；教学例子不是论文实测。', "",
             '## 机制对照 {#comparison}', "", '比较维度：' + ' · '.join(record["axes"]), "",
             '<div class="ar-deep-comparison" markdown="1">', "",
             '| 论文与来源 | 机制定位 | 得到了什么，付出什么 |', '| --- | --- | --- |']
    for row in record["comparisons"]:
        paper = cards[row["paper"]]
        url = _relative(paper["detail_path"], path)
        sections = '、'.join(_md(section) for section in row["sections"])
        source_url = paper['paper_url']
        # Manifest paper URLs have already passed the collection URL validator.
        source_url = source_url.replace('(', '%28').replace(')', '%29').replace(' ', '%20')
        lines.append(f'| [{_md(paper["title"])}]({url}) · [原始来源]({source_url})<br>章节：{sections} '
                     f'| {_md(row["position"])} | {_md(row["tradeoff"])} |')
    lines += ["", '</div>', "", '## 取舍分析 {#analysis}', ""]
    for section in record["analysis"]:
        lines += [f'### {section["title"]}', "", section["body"], "", f'对照来源：{sources(section["papers"])}', ""]
    lines += ['## 跨论文问答 {#questions}', "", '先想自己的答案，再展开；每个问题至少联系两篇论文。', ""]
    for question in record["questions"]:
        lines += [f'### {question["question"]} {{#cross-{question["id"]}}}', "",
                  '??? note "展开答案与例子"', ""]
        body = f'**答案：** {question["answer"]}\n\n**教学例子：** {question["example"]}\n\n对照来源：{sources(question["papers"])}'
        lines += ['    ' + line if line else '' for line in body.splitlines()]
        lines.append('')
    lines += ['## 更新记录 {#updates}', "", '新论文带来新路线、改变取舍，或补充现有路线时，都在这里说明。', ""]
    for update in reversed(record["updates"]):
        lines += [f'**{update["date"]}** · {update["summary"]}', ""]
        # Initial membership can be large; the full list is shown once below.
        if len(update["papers"]) <= 8:
            lines += [f'涉及：{sources(update["papers"])}', ""]
        else:
            lines += [f'覆盖 {len(update["papers"])} 篇主题资料；目录见下。', ""]
    lines += [f'<details class="ar-deep-catalog" markdown="1"><summary>本主题全部 {len(topic["papers"])} 篇资料</summary>', "",
              '目录归类覆盖本主题全部资料；重点对照范围以上表为准。', ""]
    for identity in topic["papers"]:
        paper = cards[identity]
        lines += [f'- [{_md(paper["title"])}]({_relative(paper["detail_path"], path)})']
    lines += ["", '</details>', "", f'[进入本主题逐篇四层问答]({_relative(bank_path, path)}) · '
              f'[返回全部精读卡片]({_relative("learning/deep-dives/index.md", path)})', ""]
    return "\n".join(lines)
