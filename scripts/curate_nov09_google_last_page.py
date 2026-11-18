"""Close nine Google page31 details by exact identity/date/scope, not directory year."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

from bs4 import BeautifulSoup
import fitz

from route_nov09_title_abstract import normalized


SPECS = (
    ("distributional-alignment-games-for-answer-level-fine-tuning-2", "2604.27166", "historical",
     "Google官方Download的NYU原稿题目/三作者与arXiv2604.27166一致，原稿第一页还明确Google Research/NYU/Microsoft机构。arXiv v1已于2026-04-29T20:15:37Z公开（上海4/30），早于本窗；不是用ICML2026目录年份推定首发。只做身份/日期核查，不声称方法或实现已完成。"),
    ("extending-the-uxr-point-of-view-playbook-triangulating-insights-in-complex-developer-domains", "2605.31104", "historical",
     "Google Download直接指向arXiv2605.31104，精确题目与Sarah Kianfar署名匹配；v1为2026-05-29T10:15:54Z，早于10/16。UXR playbook的2026目录新增不是本窗新论文，未作全文算法审查。"),
    ("csnake-detecting-self-sustaining-cascading-failure-via-causal-stitching-of-fault-propagations", "2509.26529", "historical",
     "官方Download直接给arXiv2509.26529；题目与三作者完全对应，v1于2025-09-30T17:04:31Z公开。EuroSys2026出版记录不是首次公开日期，本窗按已证实历史身份结案，而非把未读Google论文按目录年份排期。"),
    ("the-business-case-for-investing-in-employee-health-to-generate-organisational-success-2", None, "out_of_scope",
     "已读取官方详情完整摘要：IOMSC工作组的occupational/employee health商业价值position paper，论述慢病、缺勤、组织ROI及OEH协作，并非项目的搜广推、基础模型、后训练或Agent新算法/公共评测研究。无Download，精确首发日不在页面列出，但本项凭明确题外内容结案；不将页面2026或to-appear当首发证据，也不伪造访问故障。"),
    ("rational-transductors-2", "2602.07599", "historical",
     "Google Download NYU原稿的题目、Mehryar Mohri和GoogleResearch/NYU机构与arXiv2602.07599一致；已审Oct15账本同一canonical ID/题目有身份日期结案。新查arXiv历史进一步确认v1为2026-02-07T16:01:10Z，v2为10/14而非新首发。继承的是身份日期，不冒充本轮方法/实现复核。"),
    ("borrowed-identities-malleable-distillation-factories-and-a-unified-numerical-search", "2606.28518", "historical",
     "Google Download直接指向arXiv2606.28518且题目一致；arXiv完整署名为ShraddhaSingh/CraigGidney/CodyJones，Google目录只显示后两位Google作者，不能因此误判另一论文。v1为2026-06-26T18:14:09Z，早于窗口；量子magic-state distillation不是LLM蒸馏，保留真实研究主题，不用2026目录年份冒充新首发。"),
    ("agentic-knowledge-graphs-recursive-crawling-and-graph-construction-in-enterprise-documents", "2604.14220", "historical",
     "Google详情无Download，但精确检索定位arXiv2604.14220《Knowledge Graph RAG: Agentic Crawling and Graph Construction in Enterprise Documents》：两作者集合KoushikChakraborty/KoyelGuha相同，Google与arXiv完整摘要逐词归一后相同，故不是仅凭标题相似合并。v1为2026-04-14T05:26:50Z；这是已证实4月的同工作别名，未做新方法评测或声称已实现。"),
    ("2d-gum-net-unsupervised-dense-elastic-image-registration-via-symmetric-correlation-and-spectral-pooling", "2611.12805", "after_window",
     "Google Download直接对应arXiv2611.12805，题目匹配、作者名在Google使用缩写。v1为2026-11-09T18:11:45Z，换算Asia/Shanghai是11/10 02:11:45，严格晚于本次11/9本地日界线；不能按UTC日期11/9误算漏审。保留给后续窗口，不是题外拒绝或高成本结案。"),
    ("rsrcc-a-remote-sensing-regional-change-comprehension-benchmark-constructed-via-retrieval-augmented-best-of-n-ranking", "2604.20623", "historical",
     "Google Download直接给arXiv2604.20623，题目与五作者一致；v1为2026-04-22T14:38:41Z，v2为6/14。NeurIPS2026目录出现或出版年份不等于本窗新首发；只结案本窗口身份日期，不否定公共多模态基准的研究价值或声称其实现完成。"),
)
PDF_LINKS = {0: ("nyu-alft-http.pdf", "http://www.cs.nyu.edu/~mohri/pub/alft.pdf"),
             4: ("nyu-rbt.pdf", "https://cs.nyu.edu/~mohri/pub/rbt.pdf")}


def receipt(path: Path, url: str, source_dir: Path) -> dict:
    data = path.read_bytes()
    return {"url": url, "result": "retrieved", "source_capture": path.relative_to(source_dir).as_posix(),
            "body_sha256": sha256(data).hexdigest(), "bytes": len(data)}


def google_abstract(soup: BeautifulSoup) -> str:
    heading = next(h for h in soup.find_all(["h2", "h3"]) if h.get_text(" ", strip=True) == "Abstract")
    node = heading.parent.find_next_sibling("div")
    return node.get_text(" ", strip=True)


def build(source_dir: Path) -> dict:
    root = source_dir / "google-last-page"
    records = []
    for index, (slug, identity, status, reason) in enumerate(SPECS):
        url = f"https://research.google/pubs/{slug}/"
        detail = root / f"detail-{index + 1:02d}.html"
        soup = BeautifulSoup(detail.read_text(), "html.parser")
        title = soup.find("meta", attrs={"name": "citation_title"})["content"]
        authors = [n["content"] for n in soup.find_all("meta", attrs={"name": "citation_author"})]
        attempts = [receipt(detail, url, source_dir)]
        row = {"url": url, "title": title, "organization": "Google", "review_status": status,
               "status": status, "reason": reason,
               "scope_triage_completed": True, "counts_as_accepted": False,
               "fulltext_review_completed": False, "full_article_read": False,
               "method_review_completed": False, "implementation_status": "not_changed_by_review",
               "body_sha256": attempts[0]["body_sha256"], "authors_on_official_detail": authors,
               "arxiv_ids": [identity] if identity else [], "date_evidence": [],
               "reference_section": "new bounded Google page31 exact-detail/Download/identity check",
               "source_review_scope": "official detail, exact Download identity and first-submission metadata; PDF first page for two NYU downloads; not a whole-paper method review",
               "automatic_retry": False, "blocking": False,
               "reopen_when": "New contradictory canonical identity/date evidence, a materially changed manuscript, or explicit user-prioritized historical method review; no automatic retry."}
        if identity:
            abs_path = root / f"arxiv-{identity}.html"
            abs_url = f"https://arxiv.org/abs/{identity}"
            abstract_page = BeautifulSoup(abs_path.read_text(), "html.parser")
            arxiv_title = abstract_page.select_one(".title").get_text(" ", strip=True).removeprefix("Title:").strip()
            arxiv_authors = [a.get_text(" ", strip=True) for a in abstract_page.select(".authors a")]
            history = abstract_page.select_one(".submission-history").get_text(" ", strip=True)
            date_text = re.search(r"\[v1\]\s*(.+?UTC)", history)[1]
            first_utc = datetime.strptime(date_text, "%a, %d %b %Y %H:%M:%S %Z").replace(tzinfo=timezone.utc)
            local = first_utc.astimezone(ZoneInfo("Asia/Shanghai"))
            if status == "historical" and local.date().isoformat() >= "2026-10-16":
                raise ValueError("historical disposition lacks actual pre-window date")
            if status == "after_window" and local.date().isoformat() <= "2026-11-09":
                raise ValueError("after-window disposition has an in-window local date")
            if index == 6:
                abstract = abstract_page.select_one(".abstract").get_text(" ", strip=True).removeprefix("Abstract:").strip()
                if (normalized(google_abstract(soup)) != normalized(abstract)
                        or set(authors) != set(arxiv_authors)):
                    raise ValueError("Agentic KG alias lacks exact authors/full-abstract equivalence")
                row["identity_match"] = {"kind": "same_author_set_and_exact_normalized_full_abstract",
                                         "official_title": title, "arxiv_title": arxiv_title,
                                         "abstract_normalized_sha256": sha256(normalized(abstract).encode()).hexdigest()}
            else:
                if normalized(title) != normalized(arxiv_title):
                    raise ValueError(f"{identity}: exact title mismatch")
                row["identity_match"] = {"kind": "exact_official_download_or_pdf_title_and_author_identity", "arxiv_title": arxiv_title}
            attempts.append(receipt(abs_path, abs_url, source_dir))
            row.update(primary_source_url=abs_url, arxiv_authors=arxiv_authors,
                       first_submission_utc=first_utc.isoformat(), first_submission_shanghai=local.isoformat())
            row["date_evidence"] = [{"url": abs_url, "location": "Submission history [v1]",
                "date": local.date().isoformat(), "timezone": "Asia/Shanghai", "first_submission_utc": first_utc.isoformat(),
                "body_sha256": attempts[-1]["body_sha256"],
                "meaning": "Verified public arXiv v1 by this timestamp, not directory year, revision date or a claim of globally earliest publication."}]
        else:
            text = google_abstract(soup)
            if not all(word in text for word in ("position paper", "occupational and employee health", "OEH")):
                raise ValueError("health scope witness is missing")
            row.update(primary_source_url=url, first_publication_date="not established; not needed for explicit subject-scope exclusion",
                       scope_witness="IOMSC occupational/employee-health strategic position paper; not a research-track algorithm or benchmark")
        if index in PDF_LINKS:
            filename, download_url = PDF_LINKS[index]
            pdf = root / filename
            with fitz.open(pdf) as doc:
                text = doc[0].get_text()
                if title.casefold() not in " ".join(text.split()).casefold() or "Google Research" not in text:
                    raise ValueError("official NYU PDF first-page title/affiliation mismatch")
                row["pdf_identity_witness"] = {"page_one_based": 1,
                    "page_text_sha256": sha256(text.encode()).hexdigest(), "locations": "title, author names and Google Research / NYU affiliation block; visually inspected"}
            attempts.append(receipt(pdf, download_url, source_dir))
        if index == 4:
            prior = Path(__file__).resolve().parents[1] / "docs/research-audits/oct15-review-closure/foundation-model-reviews.json"
            old = json.loads(prior.read_bytes())
            previous = next(r for r in old["reviews"] if r["id"] == identity)
            if previous["title"] != title or previous["decision"] != "historical":
                raise ValueError("Rational Transductors inheritance lacks exact old identity")
            row["corroborating_evidence"] = [{"reference": prior.relative_to(Path(__file__).resolve().parents[1]).as_posix(),
                "reference_sha256": sha256(prior.read_bytes()).hexdigest(), "canonical_id": identity,
                "inherited_scope": "historical identity/date only, not method or implementation completion"}]
        row["attempts"] = attempts
        row["source_receipts"] = attempts
        records.append(row)
    return {"schema_version": 1, "checked_on": "2026-11-11",
            "window": {"start": "2026-10-16", "end": "2026-11-09", "timezone": "Asia/Shanghai"},
            "scope": "Only nine newly observed Google page31 details; no recrawl of previous30 pages",
            "all_sources_exhaustive": False, "counts": dict(Counter(r["review_status"] for r in records)),
            "source_exceptions": [], "records": records}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = build(args.source_dir)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["counts"]))


if __name__ == "__main__":
    main()
