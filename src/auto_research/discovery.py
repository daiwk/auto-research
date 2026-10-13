"""High-recall, auditable paper candidate discovery.

This module deliberately separates *candidate recall* from the downstream
evidence gate.  Abstract keywords may retrieve a paper, but industrial online
evidence is still accepted only after a full-text review.
"""

from __future__ import annotations

from dataclasses import dataclass
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Iterable

from .models import Paper
from .papers import ArxivClient, canonical_arxiv_id, paper_recency, paper_revision


@dataclass(frozen=True)
class DiscoveryQuery:
    name: str
    text: str
    categories: tuple[str, ...]
    match: str = "all"


@dataclass(frozen=True)
class DiscoveredPaper:
    paper: Paper
    query_names: tuple[str, ...]
    source_provenance: tuple[dict, ...] = ()

    def to_dict(self) -> dict:
        return {
            "arxiv_id": canonical_arxiv_id(self.paper.arxiv_id),
            "title": self.paper.title,
            "abstract": self.paper.abstract,
            "published": self.paper.published,
            "updated": self.paper.updated,
            "revision": paper_revision(self.paper),
            "metadata_sha256": paper_metadata_sha256(self.paper),
            "url": self.paper.url,
            "authors": self.paper.authors,
            "matched_queries": list(self.query_names),
            "source_provenance": list(self.source_provenance),
            "evidence_status": "full-text-review-required",
        }


# Use multiple narrow queries instead of one long AND expression.  The matrix
# includes architectural synonyms and production language; company names are
# intentionally not required, so an unfamiliar industrial team remains visible.
RECOMMENDATION_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("recsys-general", "recommender system", ("cs.IR", "cs.LG")),
    DiscoveryQuery("recommendation-ranking", "recommendation ranker", ("cs.IR", "cs.LG")),
    DiscoveryQuery("generative-recommendation", "generative recommendation", ("cs.IR", "cs.LG")),
    DiscoveryQuery("llm-recommendation", "LLM recommendation", ("cs.IR", "cs.CL")),
    DiscoveryQuery("industrial-ranking", "industrial ranking recommendation", ("cs.IR", "cs.LG")),
    DiscoveryQuery("production-evidence", "recommendation online A/B", ("cs.IR", "cs.LG")),
    DiscoveryQuery("deployment-evidence", "recommendation deployed production", ("cs.IR", "cs.LG")),
    DiscoveryQuery("search-ranking", "search ranking online A/B", ("cs.IR", "cs.LG")),
    DiscoveryQuery("advertising-ranking", "advertising ranking online A/B", ("cs.IR", "cs.LG")),
    DiscoveryQuery("user-interest-modeling", "user interests", ("cs.IR", "cs.LG")),
    DiscoveryQuery("semantic-id-modeling", "SID recommendation", ("cs.IR", "cs.LG")),
)

FOUNDATION_MODEL_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("llm-architecture", "language model architecture", ("cs.CL", "cs.LG")),
    DiscoveryQuery("transformer-architecture", "transformer architecture", ("cs.CL", "cs.LG")),
    DiscoveryQuery("efficient-inference", "efficient LLM inference", ("cs.CL", "cs.LG")),
    DiscoveryQuery("long-context", "language model long context", ("cs.CL", "cs.LG")),
    DiscoveryQuery("pretraining-data", "language model pretraining data", ("cs.CL", "cs.LG")),
    DiscoveryQuery("multimodal-llm", "multimodal language model", ("cs.CV", "cs.CL")),
    DiscoveryQuery("vision-language", "vision language model", ("cs.CV", "cs.CL")),
    DiscoveryQuery("model-compression", "language model compression", ("cs.CL", "cs.LG")),
    DiscoveryQuery("llm-abbreviation", "LLM", ("cs.CL", "cs.LG")),
    DiscoveryQuery("ssm-inference", "SSM speculative", ("cs.CL", "cs.LG")),
    DiscoveryQuery("jepa-world-action", "JEPA world-action WAM", ("cs.CV", "cs.RO", "cs.LG"), "any"),
    DiscoveryQuery("diffusion-language", "diffusion language", ("cs.CL", "cs.LG")),
)

POST_TRAINING_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("post-training", "language model post training", ("cs.CL", "cs.LG")),
    DiscoveryQuery("preference-optimization", "language model preference optimization", ("cs.CL", "cs.LG")),
    DiscoveryQuery("llm-rl", "reinforcement learning language model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("on-policy-distillation", "on policy distillation language model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("reward-model", "language model reward model", ("cs.CL", "cs.LG")),
    DiscoveryQuery("process-reward", "language model process reward", ("cs.CL", "cs.LG")),
    DiscoveryQuery("test-time-rl", "test time reinforcement learning", ("cs.CL", "cs.LG")),
    DiscoveryQuery("opd", "online policy distillation", ("cs.CL", "cs.LG")),
    DiscoveryQuery("opd-abbreviation", "OPD", ("cs.CL", "cs.LG", "cs.CV")),
    DiscoveryQuery("rlvr-abbreviation", "RLVR GRPO PPO", ("cs.CL", "cs.LG"), "any"),
    DiscoveryQuery("policy-llm-abbreviation", "LLM policy", ("cs.CL", "cs.LG")),
)

AGENT_QUERIES: tuple[DiscoveryQuery, ...] = (
    DiscoveryQuery("llm-agent", "LLM agent", ("cs.AI", "cs.CL")),
    DiscoveryQuery("agentic-rl", "agentic reinforcement learning", ("cs.AI", "cs.LG")),
    DiscoveryQuery("tool-agent", "language model tool use agent", ("cs.AI", "cs.CL")),
    DiscoveryQuery("web-agent", "web agent language model", ("cs.AI", "cs.CL")),
    DiscoveryQuery("software-agent", "software engineering agent", ("cs.SE", "cs.AI")),
    DiscoveryQuery("agent-memory", "language model agent memory", ("cs.AI", "cs.CL")),
    DiscoveryQuery("agent-planning", "language model agent planning", ("cs.AI", "cs.CL")),
    DiscoveryQuery("multi-agent", "large language model multi agent", ("cs.AI", "cs.CL")),
    DiscoveryQuery("memory-retrieval", "memory retrieval", ("cs.AI", "cs.CL", "cs.IR")),
    DiscoveryQuery("skill-retrieval", "skill retrieval", ("cs.AI", "cs.CL")),
    DiscoveryQuery("agentic-opd", "agentic OPD", ("cs.AI", "cs.CL", "cs.LG")),
)

PRIORITY_ORGANIZATION_TERMS: tuple[str, ...] = (
    "Google",
    "Google DeepMind",
    "Meta",
    "Netflix",
    "ByteDance",
    "TikTok",
    "Alibaba",
    "Taobao",
    "Kuaishou",
    "Pinterest",
    "Amazon",
    "Microsoft",
    "Tencent",
)

# These are the only organizations that receive an automatic high-priority
# review warning. Other organization queries improve recall but remain in the
# normal queue; in particular, Netflix is deliberately not promoted.
PRIORITY_REVIEW_QUERY_NAMES: frozenset[str] = frozenset(
    {"priority-org-google", "priority-org-google-deepmind", "priority-org-meta"}
)


def repository_paper_statuses(
    manifest_path: Path,
    ledger_path: Path,
) -> dict[str, str]:
    """Load canonical arXiv IDs already implemented or explicitly reviewed."""
    statuses: dict[str, str] = {}
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for paper in manifest.get("papers", []):
        paper_url = str(paper.get("paper_url", ""))
        arxiv_id = paper_url.rstrip("/").split("/")[-1]
        if arxiv_id:
            statuses[canonical_arxiv_id(arxiv_id)] = "implemented"

    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    for batch in ledger.get("batches", []):
        for candidate in batch.get("candidates", []):
            arxiv_id = candidate.get("id")
            if not arxiv_id:
                continue
            identity = canonical_arxiv_id(str(arxiv_id))
            statuses.setdefault(identity, "reviewed")
    return statuses


def triage_candidates(
    papers: Iterable[DiscoveredPaper],
    repository_statuses: dict[str, str],
    *,
    repository_versions: dict[str, dict] | None = None,
) -> list[dict]:
    """Diff recalled papers against the repository and add review signals."""
    candidates: list[dict] = []
    for discovered in papers:
        item = discovered.to_dict()
        identity = item["arxiv_id"]
        status = repository_statuses.get(identity, "new")
        baseline = (repository_versions or {}).get(identity, {})
        revision = item["revision"]
        baseline_revision = baseline.get("revision")
        newer = (revision is not None and baseline_revision is not None
                 and revision > baseline_revision)
        changed_metadata = bool(
            baseline.get("metadata_sha256")
            and item["metadata_sha256"] != baseline["metadata_sha256"]
            and (baseline_revision is None or revision is None or revision >= baseline_revision)
        )
        replacement = any(source.get("entry_kind") == "replacement"
                          for source in discovered.source_provenance)
        baseline_missing = status != "new" and not baseline and replacement
        revision_review = status != "new" and (newer or changed_metadata or baseline_missing)
        priority_matches = sorted(PRIORITY_REVIEW_QUERY_NAMES.intersection(discovered.query_names))
        priority_sources = sorted({
            source["organization"] for source in discovered.source_provenance
            if source.get("organization") in {"Google", "Google DeepMind", "Meta"}
        })
        item.update(
            {
                "repository_status": status,
                "priority_review_required": (status == "new" or revision_review) and bool(priority_matches or priority_sources),
                "priority_query_matches": priority_matches,
                "priority_source_matches": priority_sources,
                "revision_review_required": revision_review,
                "review_required": status == "new" or revision_review,
                "revision_review_reason": (
                    "newer-version" if newer else "metadata-changed" if changed_metadata
                    else "replacement-without-reviewed-baseline" if baseline_missing else None
                ),
                "reviewed_revision": baseline_revision,
            }
        )
        candidates.append(item)
    return candidates


def build_discovery_payload(
    *,
    track: str,
    start_date: dt.date,
    end_date: dt.date,
    query_names: Iterable[str],
    candidates: list[dict],
) -> dict:
    counts = {
        status: sum(candidate["repository_status"] == status for candidate in candidates)
        for status in ("new", "implemented", "reviewed")
    }
    counts["google_meta_priority_review"] = sum(
        bool(candidate["priority_review_required"]) for candidate in candidates
    )
    counts["revision_review"] = sum(bool(candidate.get("revision_review_required"))
                                    for candidate in candidates)
    return {
        "schema_version": 3,
        "track": track,
        "window": {"start": str(start_date), "end": str(end_date)},
        "query_matrix": list(query_names),
        "candidate_count": len(candidates),
        "triage_counts": counts,
        "candidates": candidates,
    }


def render_discovery_summary(payload: dict) -> str:
    """Render a compact GitHub Actions review queue."""
    counts = payload["triage_counts"]
    requested_start = payload.get("requested_window", payload["window"])["start"]
    end = payload["window"]["end"]
    new_candidates = [
        item for item in payload["candidates"] if item["repository_status"] == "new"
    ]
    current = [item for item in new_candidates if requested_start <= item["published"][:10] <= end]
    unresolved_dates = [item for item in new_candidates if not item["published"]]
    backlog = [item for item in new_candidates if item["published"] and not requested_start <= item["published"][:10] <= end]
    revisions = [item for item in payload["candidates"] if item.get("revision_review_required")]
    lines = [
        f"# {payload['track']} 论文候选差分",
        "",
        f"扫描窗口：{payload['window']['start']} 至 {payload['window']['end']}",
        "",
        "| 新候选 | 已实现 | 已审计 | Google / Meta 重点复核 |",
        "| ---: | ---: | ---: | ---: |",
        f"| {counts['new']} | {counts['implemented']} | {counts['reviewed']} | "
        f"{counts['google_meta_priority_review']} |",
        "",
        f"其中原始发布日期在本次请求窗口内的未审候选 {len(current)} 篇；"
        f"晚索引或历史未审候选 {len(backlog)} 篇。"
        "‘新候选’只表示仓库尚未审计，并不等于当天新发表；机构词命中也不等于作者单位。",
        f"已知论文待复核的版本更新 {len(revisions)} 篇，单独计数，不计入新 v1。",
        f"另有 {len(unresolved_dates)} 篇公告条目的原始日期待解析，不计为当天新发表或历史补漏。",
        "",
        "## Google / Meta 本窗口重点复核",
        "",
        "机构查询命中只是召回信号，必须打开 PDF 核对一作 affiliation 和正文线上证据。",
        "Netflix 及其他机构进入普通候选队列，不享受自动置顶。",
        "",
    ]
    transport = payload.get("arxiv_transport")
    if transport:
        lines.extend([
            "arXiv API：" + (
                "配置内查询已取尽（不等于全文审查完成）" if transport["coverage_complete"] else
                f"覆盖未完成：{transport.get('capped_queries', 0)} 个查询达到分页上限、"
                f"{transport.get('failed_queries', 0)} 个查询失败、"
                f"{transport['cache_fallback_pages']} 页使用缓存；不可据此推进扫描水位"
            ),
            "",
        ])
    announcements = payload.get("announcements")
    if announcements:
        lines.extend([
            "公告页独立召回：" + (
                "已显式禁用" if not announcements.get("enabled") else
                "请求窗口内页面已解析（不等于全文审查）" if announcements.get("coverage_complete")
                else "覆盖不完整；失败、过期公告与未解析日期见 JSON。保留已取到的条目。"
            ),
            "",
        ])
    cross_source = payload.get("cross_source")
    if cross_source and cross_source["source_failures"]:
        lines.extend([
            f"跨来源失败 {len(cross_source['source_failures'])} 项；本次不宣称全来源覆盖。",
            "",
        ])
    if cross_source:
        partial_sources = [
            source for source in cross_source.get("source_stats", [])
            if source.get("transport_status", source.get("status", "unknown")) != "ok"
            or source.get("unresolved_publications")
        ]
        if partial_sources:
            lines.extend([
                "官方列表仅部分对账：" + "、".join(
                    f"{source['source']}（精确匹配 {source.get('exact_title_matches', 0)}，"
                    f"未匹配 {len(source.get('unresolved_publications', ()))}）"
                    for source in partial_sources
                ) + "。未匹配标题与详情链接在 JSON artifact；不能推进全来源覆盖水位。",
                "",
            ])
        snapshot_sources = [
            source for source in cross_source.get("source_stats", [])
            if source.get("review_policy") == "snapshot"
        ]
        if snapshot_sources:
            lines.extend([
                "静态会议目录按已审快照做增量对账：" + "、".join(
                    f"{source['source']}（基线内 {source.get('snapshot_known_publications', 0)}，"
                    f"新增 {source.get('snapshot_new_publications', 0)}）"
                    for source in snapshot_sources
                ) + "。快照仅是目录库存，不代表论文已收录或已复现。",
                "",
            ])
        review_count = cross_source.get("official_review_queue_count", 0)
        if review_count:
            artifact = cross_source.get("official_review_output") or "JSON artifact"
            lines.extend([
                f"官方标题待核查 {review_count} 组：见 {artifact}。"
                "同名分组不是论文身份确认，也不是通过收录门槛。",
                "",
            ])
        elif cross_source.get("coverage_complete"):
            lines.extend([
                "本窗口官方来源传输正常，静态目录增量与动态研究页标题均已对账，"
                "没有遗留身份待核条目。",
                "",
            ])
        empty_sources = [
            source["source"] for source in cross_source.get("source_stats", [])
            if source["status"] == "no_arxiv_ids"
        ]
        if empty_sources:
            lines.extend([
                "跨来源页面可访问但未提取到 arXiv ID：" + "、".join(empty_sources)
                + "；不能据此宣称这些来源已覆盖。",
                "",
            ])
    lines.extend(_candidate_lines(
        [item for item in current if item["priority_review_required"]],
        empty="本窗口没有新的 Google / Meta 重点候选。",
    ))
    lines.extend(["", "## Google / Meta 晚索引重点复核", ""])
    lines.extend(_candidate_lines(
        [item for item in backlog if item["priority_review_required"]],
        empty="本次没有晚索引的 Google / Meta 重点候选。",
    ))
    lines.extend(["", "## 已知论文版本更新", ""])
    lines.extend(_candidate_lines(revisions, empty="未发现需复核的已知论文版本更新。"))
    lines.extend(["", "## 原始发布日期待解析", ""])
    lines.extend(_candidate_lines(unresolved_dates, empty="没有原始日期待解析的条目。"))
    lines.extend(["", "## 本窗口其他未审候选", ""])
    other_new = [
        item
        for item in current
        if not item["priority_review_required"]
    ]
    lines.extend(_candidate_lines(other_new, empty="本窗口没有其他未审候选。"))
    lines.extend(["", "## 晚索引或历史未审候选", ""])
    lines.extend(_candidate_lines(
        [item for item in backlog if not item["priority_review_required"]],
        empty="本次没有晚索引或历史未审候选。",
    ))
    lines.extend(
        [
            "",
            "## 已处理候选",
            "",
            f"已实现 {counts['implemented']} 篇，已审计但未实现 {counts['reviewed']} 篇；"
            "详情保留在 JSON artifact。",
            "",
        ]
    )
    return "\n".join(lines)


def _candidate_lines(candidates: Iterable[dict], *, empty: str) -> list[str]:
    items = list(candidates)
    if not items:
        return [empty]
    lines = []
    for item in items:
        title = item['title'].replace('[', '\\[').replace(']', '\\]')
        date = item['published'][:10] or "原始日期待解析"
        version = f"，v{item['revision']}" if item.get('revision') is not None else ""
        lines.append(f"- [{item['arxiv_id']} · {title}]({item['url']})（{date}{version}）")
    return lines


def recommendation_queries() -> tuple[DiscoveryQuery, ...]:
    """Return topic queries plus a supplementary priority-organization sweep.

    arXiv does not expose structured affiliations, so these organization queries
    cannot replace PDF affiliation review. They catch company names present in
    titles/abstracts and make that extra sweep observable.
    """
    organization_queries = tuple(
        DiscoveryQuery(
            f"priority-org-{organization.lower().replace(' ', '-')}",
            f"{organization} recommendation",
            ("cs.IR", "cs.LG", "cs.CL"),
        )
        for organization in PRIORITY_ORGANIZATION_TERMS
    )
    return RECOMMENDATION_QUERIES + organization_queries


def queries_for_track(track: str) -> tuple[DiscoveryQuery, ...]:
    matrices = {
        "recommendation": recommendation_queries(),
        "foundation-model": FOUNDATION_MODEL_QUERIES,
        "post-training": POST_TRAINING_QUERIES,
        "agent": AGENT_QUERIES,
    }
    try:
        return matrices[track]
    except KeyError as exc:
        raise ValueError(f"unknown discovery track: {track}") from exc


def discover_candidates(
    client: ArxivClient,
    queries: Iterable[DiscoveryQuery],
    *,
    start_date: dt.date,
    end_date: dt.date,
    page_size: int = 50,
    maximum_results_per_query: int = 200,
    recall_mode: str = "submission-window",
) -> list[DiscoveredPaper]:
    """Run every query, retain provenance, date-filter and de-duplicate."""
    from contextlib import nullcontext
    from .discovery_checkpoint import prepare_scan
    from .runtime import exclusive_file_lock
    queries = tuple(queries)
    if recall_mode not in {"submission-window", "late-index"}:
        raise ValueError(f"unknown recall mode: {recall_mode}")
    if start_date > end_date:
        raise ValueError("discovery start must not exceed end")
    checkpoint_dir = getattr(client, "checkpoint_dir", None)
    with (exclusive_file_lock(checkpoint_dir / "scan.json") if checkpoint_dir else nullcontext()):
        prepare_scan(client, queries, start_date=start_date, end_date=end_date,
                     page_size=page_size, maximum_results=maximum_results_per_query,
                     recall_mode=recall_mode)
        return _discover_queries(client, queries, start_date=start_date, end_date=end_date,
                                 page_size=page_size, maximum_results_per_query=maximum_results_per_query,
                                 recall_mode=recall_mode)


def _discover_queries(client, queries, *, start_date, end_date, page_size, maximum_results_per_query,
                      recall_mode):
    found: dict[str, Paper] = {}
    origins: dict[str, set[str]] = {}
    months = []
    month = start_date.replace(day=1)
    while month <= end_date:
        months.append(month.strftime("%y%m"))
        month = (month.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    for query in queries:
        date_bounds = (
            {"date_from": start_date, "date_to": end_date}
            if recall_mode == "submission-window" else {"identifier_months": tuple(months)}
        )
        papers = client.search_pages(
            query.text,
            categories=query.categories,
            page_size=page_size,
            maximum_results=maximum_results_per_query,
            match=query.match,
            tolerate_failures=True,
            **date_bounds,
        )
        for paper in papers:
            if not paper_is_in_window(paper, start_date=start_date, end_date=end_date):
                continue
            identity = canonical_arxiv_id(paper.arxiv_id)
            if identity not in found or paper_recency(paper) > paper_recency(found[identity]):
                found[identity] = paper
            origins.setdefault(identity, set()).add(query.name)
    return [
        DiscoveredPaper(found[identity], tuple(sorted(origins[identity])))
        for identity in sorted(found, key=lambda key: found[key].published, reverse=True)
    ]


def paper_is_in_window(paper: Paper, *, start_date: dt.date, end_date: dt.date) -> bool:
    """Keep normal submissions and late-indexed records whose arXiv ID month is current.

    The arXiv API ``published`` date can precede the identifier month for records that
    are indexed late (for example 2609.01622 reports a July publication date).  A
    date-only filter silently loses those papers, so the canonical ID month is an
    independent recall path; repository/ledger de-duplication handles overlap.
    """
    if paper.published:
        published = dt.date.fromisoformat(paper.published[:10])
        if start_date <= published <= end_date:
            return True
    identity = canonical_arxiv_id(paper.arxiv_id)
    match = __import__("re").match(r"^(\d{2})(\d{2})\.\d+$", identity)
    if not match:
        return False
    id_month = dt.date(2000 + int(match.group(1)), int(match.group(2)), 1)
    start_month = start_date.replace(day=1)
    end_month = end_date.replace(day=1)
    return start_month <= id_month <= end_month


def merge_external_candidates(
    arxiv_results: Iterable[DiscoveredPaper],
    external_papers: Iterable[Paper],
    provenance: dict[str, list[dict]],
) -> list[DiscoveredPaper]:
    """Merge external recall without erasing query or source provenance."""
    merged = {
        canonical_arxiv_id(item.paper.arxiv_id): DiscoveredPaper(
            item.paper, item.query_names,
            tuple((*item.source_provenance, *provenance.get(
                canonical_arxiv_id(item.paper.arxiv_id), (),
            ))),
        ) for item in arxiv_results
    }
    for paper in external_papers:
        identity = canonical_arxiv_id(paper.arxiv_id)
        sources = tuple(provenance.get(identity, ()))
        current = merged.get(identity)
        if current is None:
            merged[identity] = DiscoveredPaper(paper, (), sources)
        else:
            additional = tuple(
                source for source in sources if source not in current.source_provenance
            )
            merged[identity] = DiscoveredPaper(
                paper if paper_recency(paper) > paper_recency(current.paper) else current.paper,
                current.query_names,
                tuple((*current.source_provenance, *additional)),
            )
    return sorted(merged.values(), key=lambda item: item.paper.published, reverse=True)


def paper_metadata_sha256(paper: Paper) -> str:
    """Ignore formatting changes but keep actual title/abstract/author changes."""
    value = {"title": " ".join(paper.title.split()),
             "abstract": " ".join(paper.abstract.split()),
             "authors": [" ".join(author.split()) for author in paper.authors]}
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def repository_paper_versions(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {canonical_arxiv_id(row["arxiv_id"]): row for row in payload.get("papers", [])}
