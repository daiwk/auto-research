#!/usr/bin/env python3
"""Close the historical full-text review backlog with auditable evidence.

The script intentionally separates *review closure* from *implementation*.
Passing the industrial evidence gate promotes a paper into a P0 implementation
queue; it never turns the paper into an implemented adapter automatically.
Full text is supplied through a disposable cache so copyrighted paper bodies
are not committed.  The committed review stores only a digest, section locator,
matched terms, and short metric tokens.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "docs" / "paper-audits" / "2026-historical-candidates.json"
OUTPUT = ROOT / "docs" / "paper-audits" / "2026-historical-fulltext-decisions.json"
SUMMARY = ROOT / "docs" / "paper-audits" / "2026-historical-fulltext-review.md"

COMPANY_PATTERN = re.compile(
    r"Google|Meta|Instagram|YouTube|Kuaishou|Kwai|ByteDance|TikTok|Alibaba|Taobao|"
    r"Tencent|LinkedIn|Snap(?: Inc)?|Apple|Airbnb|Pinterest|Netflix|JD\.COM|JD\.com|"
    r"Meituan|Bilibili|Xiaohongshu|Douyin|Dream11|Karrot|Danggeun|Amap|AMAP|Baidu|"
    r"Huawei|Microsoft|Amazon|Spotify|eBay|Uber|DoorDash|Booking\.com|Criteo|Rakuten|"
    r"Shopee|Dewu|Vivo|Didi|Trip\.com|Ant Group|OPPO|WeChat|NetEase|ZOZO|Politiken|"
    r"HUJING",
    re.IGNORECASE,
)
RECOMMENDATION_METHOD_PATTERN = re.compile(
    r"recommend|rank|retriev|search|CTR|CVR|conversion|personal|user|item|advert|ads|"
    r"semantic ID|query|feed|video|music|catalog|coupon|bandit|uplift|engagement|watch|"
    r"click|revenue|livestream|streaming|e-commerce|multi-task|multitask|tokenizer",
    re.IGNORECASE,
)
ONLINE_PATTERN = re.compile(
    r"online\s+A\s*/?\s*B(?:\s+test(?:ing|s)?)?|live\s+A\s*/?\s*B|full[- ]traffic|"
    r"deployed\s+(?:online|in production)|production deployment",
    re.IGNORECASE,
)
NEGATED_ONLINE_PATTERN = re.compile(
    r"future work|do not|don.t|no online|without online|lack of|will (?:be|extend)|"
    r"would require",
    re.IGNORECASE,
)
PERCENT_PATTERN = re.compile(r"[+-]?\d+(?:\.\d+)?\s*%")
CODE_PATTERN = re.compile(r"https?://github\.com/[\w.-]+/[\w.-]+", re.IGNORECASE)


@dataclass(frozen=True)
class FullTextDecision:
    arxiv_id: str
    decision: str
    priority: str
    reason_code: str
    reason: str
    source_url: str
    source_format: str
    full_text_sha256: str | None
    evidence_section: str | None
    matched_terms: tuple[str, ...]
    metric_tokens: tuple[str, ...]
    first_author_affiliation: str | None
    upstream_code_urls: tuple[str, ...]


def _load_source(evidence_dir: Path, paper_id: str) -> tuple[str, str, bytes] | None:
    for suffix, source_format in ((".html", "arxiv-html"), (".txt", "pdf-text")):
        path = evidence_dir / f"{paper_id}{suffix}"
        if path.is_file() and path.stat().st_size:
            return path.read_text(encoding="utf-8", errors="ignore"), source_format, path.read_bytes()
    return None


def _html_fields(raw: str) -> tuple[str, str, list[tuple[str, str]]]:
    # Full-text generation uses the optional paper-audit dependency.  Keep the
    # import local so CI can validate an already committed decision artifact
    # with the core dependency set only.
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(raw, "html.parser")
    affiliations = [
        node.get_text(" ", strip=True)
        for node in soup.select(".ltx_role_affiliation, .ltx_affiliation")
    ]
    sections: list[tuple[str, str]] = []
    heading = "paper body"
    for node in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "table", "figcaption"]):
        text = re.sub(r"\s+", " ", node.get_text(" ", strip=True))
        if not text:
            continue
        if node.name in {"h1", "h2", "h3", "h4", "h5"}:
            heading = text
        else:
            sections.append((heading, text))
    return soup.get_text(" ", strip=True), " | ".join(affiliations), sections


def _text_fields(raw: str) -> tuple[str, str, list[tuple[str, str]]]:
    compact = re.sub(r"\s+", " ", raw)
    return compact, "", [("PDF full text", compact)]


def _online_evidence(sections: list[tuple[str, str]]) -> tuple[str | None, tuple[str, ...], tuple[str, ...]]:
    for heading, text in sections:
        if not ONLINE_PATTERN.search(text):
            continue
        # Include adjacent table-like text in the same extracted block, but do
        # not accept TOC mentions or statements that online evaluation is future work.
        metrics = tuple(dict.fromkeys(PERCENT_PATTERN.findall(text)))[:8]
        if metrics and not NEGATED_ONLINE_PATTERN.search(text):
            terms = tuple(dict.fromkeys(match.group(0) for match in ONLINE_PATTERN.finditer(text)))
            return heading[:180], terms[:4], metrics
    return None, (), ()


def review(row: dict, evidence_dir: Path) -> FullTextDecision:
    paper_id = row["arxiv_id"]
    source = _load_source(evidence_dir, paper_id)
    source_url = f"https://arxiv.org/html/{paper_id}"
    if source is None:
        return FullTextDecision(
            arxiv_id=paper_id,
            decision="rejected-unavailable",
            priority="P2",
            reason_code="full-text-unavailable",
            reason="arXiv HTML and PDF were unavailable after bounded retries; no implementation claim is made",
            source_url=f"https://arxiv.org/abs/{paper_id}",
            source_format="unavailable",
            full_text_sha256=None,
            evidence_section=None,
            matched_terms=(),
            metric_tokens=(),
            first_author_affiliation=None,
            upstream_code_urls=(),
        )
    raw, source_format, source_bytes = source
    if source_format == "arxiv-html":
        body, affiliations, sections = _html_fields(raw)
    else:
        body, affiliations, sections = _text_fields(raw)
        source_url = f"https://arxiv.org/pdf/{paper_id}"
    evidence_section, matched_terms, metric_tokens = _online_evidence(sections)
    code_urls = tuple(dict.fromkeys(CODE_PATTERN.findall(body)))[:8]
    first_affiliation = affiliations.split(" | ", 1)[0] if affiliations else None
    industrial_p0 = (
        "recommendation" in row.get("tracks", [])
        and COMPANY_PATTERN.search(affiliations) is not None
        and RECOMMENDATION_METHOD_PATTERN.search(row.get("title", "")) is not None
        and bool(metric_tokens)
    )
    if industrial_p0:
        decision = "promoted-p0"
        priority = "P0"
        reason_code = "quantified-industrial-online-evidence"
        reason = (
            "company-affiliated recommendation/search/ads method with quantified online A/B "
            "or production-deployment evidence in the full text"
        )
    else:
        decision = "p2-after-fulltext"
        priority = "P2"
        if "recommendation" in row.get("tracks", []):
            reason_code = "industrial-gate-not-met"
            reason = (
                "full text did not jointly establish company affiliation, an in-scope method, "
                "and quantified online A/B or accepted production evidence"
            )
        else:
            reason_code = "below-current-p0-p1-threshold"
            reason = (
                "full text was reviewed, but the candidate remains below the current P0/P1 "
                "threshold; it is retained as P2 rather than silently discarded"
            )
    return FullTextDecision(
        arxiv_id=paper_id,
        decision=decision,
        priority=priority,
        reason_code=reason_code,
        reason=reason,
        source_url=source_url,
        source_format=source_format,
        full_text_sha256=sha256(source_bytes).hexdigest(),
        evidence_section=evidence_section,
        matched_terms=matched_terms,
        metric_tokens=metric_tokens,
        first_author_affiliation=first_affiliation,
        upstream_code_urls=code_urls,
    )


def _validate(payload: dict) -> list[str]:
    candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["papers"]
    expected = {
        row["arxiv_id"] for row in candidates
        if row.get("plan_status") == "fulltext-review-backlog"
    }
    decisions = payload.get("decisions", [])
    actual = {row.get("arxiv_id") for row in decisions}
    errors = []
    if len(actual) != len(decisions):
        errors.append("duplicate historical decisions")
    if expected != actual:
        errors.append(f"historical decision coverage mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")
    allowed = {"promoted-p0", "p2-after-fulltext", "rejected-unavailable"}
    for row in decisions:
        if row.get("decision") not in allowed:
            errors.append(f"{row.get('arxiv_id')}: invalid decision")
        if not row.get("reason") or not row.get("reason_code"):
            errors.append(f"{row.get('arxiv_id')}: missing reason")
        if row.get("decision") != "rejected-unavailable" and not row.get("full_text_sha256"):
            errors.append(f"{row.get('arxiv_id')}: reviewed decision lacks full-text digest")
        if row.get("decision") == "promoted-p0":
            for field in ("evidence_section", "matched_terms", "metric_tokens", "first_author_affiliation"):
                if not row.get(field):
                    errors.append(f"{row.get('arxiv_id')}: promoted P0 lacks {field}")
    return errors


def _render_summary(payload: dict) -> str:
    decisions = payload["decisions"]
    counts = {
        key: sum(row["decision"] == key for row in decisions)
        for key in ("promoted-p0", "p2-after-fulltext", "rejected-unavailable")
    }
    lines = [
        "# 2026 历史全文审计终态",
        "",
        "> 本页关闭的是“是否值得进入实现队列”的全文审查，不把晋级论文冒充成已实现。",
        "> 逐篇结构化证据见 [`2026-historical-fulltext-decisions.json`](2026-historical-fulltext-decisions.json)。",
        "",
        "## 审计结果",
        "",
        "| 终态 | 数量 | 含义 |",
        "|---|---:|---|",
        f"| P0 实现候选 | {counts['promoted-p0']} | 公司归属、方法范围和正文量化线上证据同时成立；等待独立 adapter 实现 |",
        f"| 全文审后 P2 | {counts['p2-after-fulltext']} | 已读全文，但没有达到当前 P0/P1 门槛；保留记录 |",
        f"| 原文不可用 | {counts['rejected-unavailable']} | arXiv HTML/PDF 均不可用；不作方法或效果判断 |",
        "| 未决全文 backlog | **0** | 每个历史候选均有终态 |",
        "",
        "严格门槛会排除只说“未来做 A/B”、模拟 A/B、A/B 方法论文和没有量化线上结果的论文。",
        "",
        "## 晋级 P0 实现队列",
        "",
        "按首次公开时间倒排；Google / Meta 论文仍在实际实现排期中优先。",
        "",
        "| 论文 | 首个署名机构 | 正文证据位置 | 量化 token |",
        "|---|---|---|---|",
    ]
    candidate_by_id = {
        row["arxiv_id"]: row
        for row in json.loads(CANDIDATES.read_text(encoding="utf-8"))["papers"]
    }
    promoted = [row for row in decisions if row["decision"] == "promoted-p0"]
    promoted.sort(
        key=lambda row: candidate_by_id[row["arxiv_id"]].get("published", ""),
        reverse=True,
    )
    for row in promoted:
        paper = candidate_by_id[row["arxiv_id"]]
        title = paper["title"].replace("|", "\\|")
        affiliation = (row["first_author_affiliation"] or "未解析").replace("|", "\\|")
        section = (row["evidence_section"] or "正文").replace("|", "\\|")
        metrics = ", ".join(row["metric_tokens"]).replace("|", "\\|")
        lines.append(
            f"| [{row['arxiv_id']}](https://arxiv.org/abs/{row['arxiv_id']}) {title} "
            f"| {affiliation} | {section} | {metrics} |"
        )
    lines.extend([
        "",
        "## 审计可复现性",
        "",
        "提交仓库的不是论文全文，而是来源 URL、全文 SHA-256、证据章节、匹配术语、短量化 token、机构和代码 URL。",
        "运行 `python scripts/review_historical_backlog.py --check` 可验证 331 篇覆盖、唯一性和 P0 证据字段。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-dir", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        payload = json.loads(OUTPUT.read_text(encoding="utf-8"))
    else:
        if args.evidence_dir is None:
            parser.error("--evidence-dir is required unless --check is used")
        candidates = json.loads(CANDIDATES.read_text(encoding="utf-8"))["papers"]
        rows = [
            review(row, args.evidence_dir) for row in candidates
            if row.get("plan_status") == "fulltext-review-backlog"
        ]
        payload = {
            "schema_version": 1,
            "scope": "2026-01-01/2026-08-24 historical full-text backlog",
            "review_policy": {
                "industrial_p0": "company affiliation + in-scope method + quantified full-text online evidence",
                "other": "retain below-threshold candidates as P2; do not equate P2 with irrelevance",
                "implementation_separate": True,
            },
            "decisions": [asdict(row) for row in rows],
        }
        OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    errors = _validate(payload)
    if errors:
        raise SystemExit("\n".join(errors))
    if not args.check:
        SUMMARY.write_text(_render_summary(payload), encoding="utf-8")
    counts: dict[str, int] = {}
    for row in payload["decisions"]:
        counts[row["decision"]] = counts.get(row["decision"], 0) + 1
    print(json.dumps(counts, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
