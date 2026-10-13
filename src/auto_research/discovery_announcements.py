"""Independent arXiv bulletin recall, including older-month replacements.

The bulletin date is not the original publication date. If the API is down we
retain unresolved bulletin entries instead of fabricating a publication date or
throwing away the only successful recall channel.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
import datetime as dt
import hashlib
from html.parser import HTMLParser
import re
from typing import Callable
import xml.etree.ElementTree as ET

from .discovery_sources import fetch_text
from .models import Paper
from .papers import canonical_arxiv_id, paper_revision


BULLETIN_CATEGORIES = {
    "recommendation": ("cs.IR", "cs.LG"),
    "foundation-model": ("cs.CL", "cs.LG", "cs.CV", "cs.RO"),
    "post-training": ("cs.CL", "cs.LG"),
    "agent": ("cs.AI", "cs.CL", "cs.RO"),
}
_IDENTIFIER = re.compile(r"arxiv\.org/(?:abs|html|pdf)/(\d{4}\.\d{4,5}(?:v\d+)?)")


@dataclass
class Announcement:
    arxiv_id: str = ""
    title: str = ""
    abstract: str = ""
    authors: list[str] = field(default_factory=list)
    entry_kind: str = "unknown"


class _BulletinParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack: list[str] = []
        self.entries: list[Announcement] = []
        self.entry: Announcement | None = None
        self.fields: dict[str, tuple[int, list[str]]] = {}
        self.heading: list[str] | None = None
        self.kind = "unknown"
        self.announced_on: dt.date | None = None
        self.total_expected = 0
        self.sections: list[dict] = []
        self.author: list[str] | None = None

    def handle_starttag(self, tag, attrs):
        if tag in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                   "link", "meta", "param", "source", "track", "wbr"}:
            return
        attrs = dict(attrs)
        self.stack.append(tag)
        if tag == "h3":
            self.heading = []
        if tag == "dt":
            self.entry = Announcement(entry_kind=self.kind)
        if tag == "a" and self.entry is not None:
            href = attrs.get("href") or ""
            if href.startswith("/"):
                href = "https://arxiv.org" + href
            match = _IDENTIFIER.search(href)
            if match and (not self.entry.arxiv_id or "v" in match.group(1)):
                self.entry.arxiv_id = match.group(1)
            if "authors" in self.fields:
                self.author = []
        classes = (attrs.get("class") or "").split()
        for css, field_name in (("list-title", "title"), ("list-authors", "authors")):
            if css in classes and self.entry is not None:
                self.fields[field_name] = (len(self.stack), [])
        if tag == "p" and "mathjax" in classes and self.entry is not None:
            self.fields["abstract"] = (len(self.stack), [])

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.heading is not None:
            self.heading.append(data)
        for _, value in self.fields.values():
            value.append(data)
        if self.author is not None:
            self.author.append(data)

    def handle_endtag(self, tag):
        if tag == "h3" and self.heading is not None:
            heading = " ".join("".join(self.heading).split())
            self.heading = None
            date = re.search(r"new listings for \w+, (\d+ \w+ \d{4})", heading)
            if date:
                self.announced_on = dt.datetime.strptime(date.group(1), "%d %B %Y").date()
            for marker, kind in (("New submissions", "new"),
                                 ("Cross submissions", "cross-list"),
                                 ("Replacement submissions", "replacement")):
                if heading.startswith(marker):
                    self.kind = kind
                    count = re.search(r"showing (\d+) of (\d+) entries", heading)
                    if count:
                        shown, total = map(int, count.groups())
                        self.total_expected += total
                        self.sections.append({"kind": kind, "shown": shown, "expected": total})
        if tag == "a" and self.author is not None:
            if self.entry is not None:
                self.entry.authors.append(" ".join("".join(self.author).split()))
            self.author = None
        depth = len(self.stack)
        for name, (start, value) in list(self.fields.items()):
            if start == depth and self.entry is not None:
                if name != "authors":
                    text = " ".join("".join(value).split())
                    setattr(self.entry, name, text.removeprefix("Title:").strip())
                del self.fields[name]
        if tag == "dd" and self.entry is not None:
            if self.entry.arxiv_id:
                self.entries.append(self.entry)
            self.entry = None
            self.fields.clear()
        # HTML has void tags; keep depth correct without depending on a browser.
        if tag in self.stack:
            index = len(self.stack) - 1 - self.stack[::-1].index(tag)
            del self.stack[index:]


def parse_bulletin(content: str) -> tuple[list[Announcement], dict]:
    parser = _BulletinParser()
    parser.feed(content)
    return parser.entries, {
        "announced_on": str(parser.announced_on) if parser.announced_on else None,
        "expected_entries": parser.total_expected,
        "parsed_entries": len(parser.entries),
        "sections": parser.sections,
        "sha256": hashlib.sha256(content.encode()).hexdigest(),
        "parse_complete": bool(parser.sections) and len(parser.entries) == parser.total_expected,
    }


def discover_announcements(*, track: str, start_date: dt.date, end_date: dt.date,
                           client, fetch: Callable[[str], str] = fetch_text):
    if track not in BULLETIN_CATEGORIES:
        raise ValueError(f"unsupported announcement track: {track}")
    found: dict[str, Paper] = {}
    provenance: dict[str, list[dict]] = {}
    reports = []
    for category in BULLETIN_CATEGORIES[track]:
        url = f"https://arxiv.org/list/{category}/new?show=2000"
        try:
            entries, report = parse_bulletin(fetch(url))
        except (OSError, ValueError, ET.ParseError) as exc:
            reports.append({"source_url": url, "category": category,
                            "status": "failed", "error": f"{type(exc).__name__}: {exc}",
                            "coverage_complete": False})
            continue
        date = report["announced_on"]
        in_window = bool(date and str(start_date) <= date <= str(end_date))
        report.update(source_url=url, category=category,
                      status="retrieved" if in_window else "outside-window",
                      coverage_complete=report["parse_complete"] and in_window,
                      publication_dates_resolved=False)
        reports.append(report)
        if not in_window:
            continue
        for entry in entries:
            identity = canonical_arxiv_id(entry.arxiv_id)
            # Prefer an explicit revision from HTML over a canonical cross-list.
            previous = found.get(identity)
            if previous is None or "v" in entry.arxiv_id:
                found[identity] = Paper(entry.title, entry.abstract, entry.authors, "",
                                        f"https://arxiv.org/abs/{entry.arxiv_id}", entry.arxiv_id)
            provenance.setdefault(identity, []).append({
                "source": f"arxiv-announcement-{category}", "source_kind": "arxiv-announcement",
                "source_url": url, "source_published": date,
                "announced_on": date, "entry_kind": entry.entry_kind,
                "listed_arxiv_id": entry.arxiv_id, "listing_sha256": report["sha256"],
                "publication_date_unresolved": True,
            })
    resolved = {}
    failures = []
    identifiers = list(found)
    for offset in range(0, len(identifiers), 100):
        try:
            rows = client.lookup(identifiers[offset:offset + 100])
        except (OSError, ValueError, ET.ParseError) as exc:
            failures.append({"ids": identifiers[offset:offset + 100],
                             "error": f"{type(exc).__name__}: {exc}"})
            continue
        for row in rows:
            resolved[canonical_arxiv_id(row.arxiv_id)] = row
    for identity, row in resolved.items():
        if identity in found:
            listed_revision = paper_revision(found[identity])
            api_revision = paper_revision(row)
            stale = listed_revision is not None and (api_revision is None or api_revision < listed_revision)
            found[identity] = replace(found[identity], published=row.published) if stale else row
            for source in provenance[identity]:
                source["publication_date_unresolved"] = False
                source["revision_metadata_unresolved"] = stale
            if stale:
                failures.append({"ids": [identity], "error": "API metadata older than explicit bulletin revision"})
    for report in reports:
        report["metadata_resolution_failures"] = failures
        report["publication_dates_resolved"] = bool(found) and not failures and all(
            paper.published for paper in found.values()
        )
        report["review_complete"] = False
        report["watermark_eligible"] = False
    return list(found.values()), provenance, reports
