#!/usr/bin/env python3
"""Read-only reconciliation of review acceptance, delivery, and source leads.

This report never edits the ledger, the review watermark, or runtime classifiers.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.discovery import repository_paper_statuses
from auto_research.discovery_review import TERMINAL_EXCEPTION_RESOLUTIONS
from auto_research.papers import canonical_arxiv_id

REGISTER_PATHS = [
    "docs/research-audits/oct07-review-closure/paper-register.json",
    "docs/research-audits/oct12-review-closure/paper-register.json",
    "docs/research-audits/oct15-review-closure/paper-register.json",
]


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_title(title):
    return re.sub(r"[^\w]+", "", unicodedata.normalize("NFKC", title).casefold())


def build():
    ledger_path = ROOT / "docs/paper-discovery-ledger.json"
    manifest_path = ROOT / "docs/research-manifest.json"
    inventory_path = ROOT / "docs/research-audits/harness2-priority-repair/backfill-inventory.json"
    ledger, manifest = load(ledger_path), load(manifest_path)
    statuses = repository_paper_statuses(manifest_path, ledger_path)
    observations = defaultdict(list)
    for bi, batch in enumerate(ledger["batches"]):
        for ri, row in enumerate(batch.get("candidates", [])):
            identity = canonical_arxiv_id(str(row.get("id", "")))
            if identity:
                observations[identity].append({
                    "batch": batch.get("batch"), "row": row,
                    "pointer": f"docs/paper-discovery-ledger.json#/batches/{bi}/candidates/{ri}",
                })
    catalog = defaultdict(list)
    for row in manifest["papers"]:
        match = re.search(r"(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", row.get("paper_url", ""))
        if match:
            catalog[match[1]].append(row)
    accepted = defaultdict(list)
    registers = []
    for name in REGISTER_PATHS:
        register = load(ROOT / name)
        registers.append(register)
        for index, row in enumerate(register["papers"]):
            if row.get("status") == "accepted":
                accepted[canonical_arxiv_id(row["id"])].append({
                    "source": f"{name}#/papers/{index}", "row": row,
                })
    old_pending = {key for key, value in statuses.items() if value == "implementation-pending"}
    unclosed, catalogued, closed = [], [], []
    for identity, reviews in sorted(accepted.items()):
        terminal = [obs for obs in observations[identity]
                    if obs["row"].get("resolution") in TERMINAL_EXCEPTION_RESOLUTIONS]
        base = {"id": identity, "title": reviews[-1]["row"]["title"],
                "accepted_evidence": [item["source"] for item in reviews]}
        if catalog.get(identity):
            catalogued.append({**base, "entries": [{
                "key": entry["key"], "domain": entry["domain"],
                "detail_path": entry["detail_path"],
                "document_exists": (ROOT / "docs" / entry["detail_path"]).is_file(),
                "capability_complete_inferred": False,
            } for entry in catalog[identity]]})
        elif terminal:
            closed.append({**base, "terminal_evidence": [obs["pointer"] for obs in terminal]})
        else:
            source = observations[identity][0] if observations[identity] else None
            track = (source["row"].get("track") if source else None) or "unassigned"
            unclosed.append({**base, "track": track, "old_computed_status": statuses.get(identity),
                "ledger_evidence": [obs["pointer"] for obs in observations[identity]],
                "reason": source["row"].get("reason", "") if source else "",
                "catalog_match": False, "source_ledger_cost_gate_closed": False,
                "user_implementation_authorization_inferred": False,
                "automatic_implementation_queue": False})
    unclosed_ids = {row["id"] for row in unclosed}
    deferred = []
    for identity in sorted(old_pending - set(accepted)):
        row = observations[identity][0]
        deferred.append({"id": identity, "title": row["row"]["title"],
            "reason": row["row"]["reason"], "evidence": row["pointer"],
            "structured_acceptance_found": False, "automatic_implementation_queue": False})
    google = load(HERE / "data/google-review.json")
    google_new = [row for row in load(inventory_path)["papers"]
                  if row["current_repository_status"] == "new"]
    google_ids = {row["id"] for row in google_new}
    earlier = {identity for identity in google_ids if identity[:2] < "26"}
    divided = {row["id"] for row in google["papers"]
               if row["audit_disposition"] != "genuine_substantive_review_gap_not_accepted_implementation"}
    current_unreviewed = google_ids - earlier - divided
    audit_decisions = {row["id"]: row for row in load(HERE / "data/this-audit-dispositions.json")["decisions"]}
    for row in unclosed:
        decision = audit_decisions.get(row["id"])
        row["this_audit_full_experiment_resolution"] = decision["resolution"] if decision else None
        row["this_audit_full_experiment_review_done"] = bool(decision)
        row["component_implementation_authorized_by_this_report"] = False
    for row in deferred:
        decision = audit_decisions.get(row["id"])
        row["this_audit_full_experiment_resolution"] = decision["resolution"] if decision else None
    title_groups = defaultdict(set)
    for row in unclosed:
        title_groups[normalized_title(row["title"])].add(row["id"])
    source_names = [*REGISTER_PATHS, "docs/paper-discovery-ledger.json",
                    "docs/research-manifest.json", str(inventory_path.relative_to(ROOT))]
    source_names.extend(str(path.relative_to(ROOT)) for path in sorted((HERE / "data").glob("*.json")))
    result = {
        "schema_version": 1, "as_of": "2026-10-21",
        "snapshot_commit": "d1b4851b0cfc5b2bfa0624e5ef4f987a511e1995",
        "scope": "Three frozen review registers plus the previously reported 54-source-lead cohort",
        "read_only_reconciliation": True, "ledger_modified": False,
        "review_watermark_modified": False, "all_history_implementation_complete": False,
        "sources": [{"path": name, "sha256": hashlib.sha256((ROOT / name).read_bytes()).hexdigest()}
                    for name in source_names],
        "counts": {
            "ledger_candidate_rows": sum(len(b.get("candidates", [])) for b in ledger["batches"]),
            "ledger_unique_identities": len(observations),
            "ledger_repeated_identities": sum(len(rows) > 1 for rows in observations.values()),
            "old_pending": len(old_pending), "accepted_union": len(accepted),
            "accepted_catalogued": len(catalogued), "accepted_cost_or_source_terminal": len(closed),
            "accepted_not_catalogued_no_terminal": len(unclosed),
            "accepted_omitted_from_old_pending": len(unclosed_ids - old_pending),
            "deferred_misrepresented_as_accepted_delivery": len(deferred),
            "duplicates_within_old_pending": sum(len(observations[i]) > 1 for i in old_pending),
            "catalog_matches_within_old_pending": sum(bool(catalog.get(i)) for i in old_pending),
            "duplicate_normalized_titles_among_unclosed": sum(len(ids) > 1 for ids in title_groups.values()),
            "previous_google_new": len(google_new), "pre_2026_source_leads": len(earlier),
            "scope_or_document_type_diversions": len(divided),
            "current_2026_substantive_review_leads": len(current_unreviewed),
            "source_lead_overlap_with_accepted_or_deferred": len(google_ids & (set(accepted) | old_pending)),
            "this_audit_full_experiment_terminals": len(audit_decisions),
            "this_audit_terminal_from_accepted": len(unclosed_ids & set(audit_decisions)),
            "accepted_without_full_experiment_terminal_after_this_audit": len(unclosed_ids - set(audit_decisions)),
            "this_audit_terminal_from_deferred": len({row["id"] for row in deferred} & set(audit_decisions)),
            "deferred_not_accepted_still_unclosed": len({row["id"] for row in deferred} - set(audit_decisions)),
        },
        "source_unclosed_observations_by_track": dict(sorted(Counter(row["track"] for row in unclosed).items())),
        "accepted_not_delivered": unclosed, "accepted_catalogued": catalogued,
        "accepted_terminal": closed, "deferred_not_accepted": deferred,
        "current_2026_google_review_leads": sorted(current_unreviewed),
        "pre_2026_google_reference_leads": sorted(earlier),
        "non_implementation_google_source_leads": sorted(divided),
        "this_audit_full_experiment_decisions": list(audit_decisions.values()),
        "limits": [
            "Accepted is a paper-review decision, not a human request to implement every candidate.",
            "No catalog match is an unfulfilled component/delivery observation, not proof of affordable faithful reproduction.",
            "Catalog membership and a diagnostic do not prove full capability reproduction.",
            "Priority-institution author blocks were not independently available for every old accepted candidate.",
            "New primary-source cost recommendations are separate from already committed ledger terminal decisions.",
            "Source unclosed observations by track refer to 504 catalog/delivery observations; full-experiment closure does not deliver the corresponding affordable component.",
        ],
    }
    assert len(accepted) == len(catalogued) + len(closed) + len(unclosed)
    assert old_pending - unclosed_ids == {row["id"] for row in deferred}
    assert not (earlier & divided)
    assert len(google_ids) == len(earlier) + len(divided) + len(current_unreviewed)
    return result


def cell(value):
    return re.sub(r"\$(?=\d)", "USD ", str(value)).replace("|", " / ").replace("\n", " ")


def render_lists(result):
    global_review = load(HERE / "data/global-review.json")
    google = load(HERE / "data/google-review.json")
    meta = load(HERE / "data/meta-review.json")
    dates = {row["id"]: row for row in load(HERE / "data/date-checks.json")["papers"]}
    pri = {row["id"] for row in google["priority_pending_shortlist"]}
    pri.update(row["id"] for row in meta["pending_rows"])
    labels = {"agent": "Agent", "foundation-model": "基础模型",
              "post-training": "后训练", "recommendation": "搜广推"}
    for track, label in labels.items():
        rows = [row for row in result["accepted_not_delivered"] if row["track"] == track]
        lines = [f"# {label}：审查接受但尚未交付（{len(rows)}）", "",
                 "只表示既有审查接受、没有当前目录或明确成本终态。不是全部获用户实施授权，",
                 "也未逐篇完成现行成本门禁；不能直接当成自动实施队列。按论文 ID 倒排。", "",
                 "本轮已确认的完整实验不复现项单独标注；其他项必须先完成成本/范围裁剪，不是直接接单。", "",
                 "| ID / 论文 | 本轮处置 | 优先机构核验 | 既有审查理由 |", "| --- | --- | --- | --- |"]
        for row in sorted(rows, key=lambda x: x["id"], reverse=True):
            priority = "Google/Meta 已确认，见优先清单" if row["id"] in pri else "未在本轮独立确认；不是已排除"
            disposition = "完整实验不复现，审查DONE；低成本组件另议" if row["this_audit_full_experiment_review_done"] else "尚需成本/范围裁剪或交付；未排自动队列"
            lines.append(f"| [{row['id']}](https://arxiv.org/abs/{row['id']}) {cell(row['title'])} | {disposition} | {priority} | {cell(row['reason'])} |")
        lines.extend(["", "逐项登记指针、标题和当前状态见 [reconciliation.json](reconciliation.json)。", ""])
        (HERE / f"accepted-{track}.md").write_text("\n".join(lines), encoding="utf-8")
    categories = {row["id"]: row["reason_category"] for row in global_review["legacy_deferred_not_structured_accepted"]}
    lines = ["# 31 条审后延期线索：不等于已接受实施", "",
             "原脚本仅凭‘待实现/下一批须/保留下一批’等自由文本，将这些 `reviewed_deferred` 项升为待交付。",
             "这里保留全部线索和理由；不将它们假装已完成，也不混进结构化接受的 504 项。", "",
             "| 论文 | 理由类型 | 原始理由 |", "| --- | --- | --- |"]
    for row in reversed(result["deferred_not_accepted"]):
        category = "完整实验不复现，审查DONE；原理由类型=" if row["this_audit_full_experiment_resolution"] else ""
        lines.append(f"| [{row['id']}](https://arxiv.org/abs/{row['id']}) {cell(row['title'])} | {category}{categories[row['id']]} | {cell(row['reason'])} |")
    (HERE / "deferred-candidates.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    lines = ["# 原 54 个官方源线索的重新分组", "",
             "这些不是 54 个已接受实现任务。9 项为 2024/2025 年首发历史参考，",
             "6 项已有 P2 初筛或无直接实现对象，剩下 39 项为 2026 年待实质审查线索。",
             "历史参考不等于无价值，也不以旧日期作为方法拒绝理由；是否另立复现任务需要独立判断。", ""]
    groups = [("2026 年待实质审查（39）", set(result["current_2026_google_review_leads"])),
              ("2024/2025 历史参考（9）", set(result["pre_2026_google_reference_leads"])),
              ("非实施分流（6）", set(result["non_implementation_google_source_leads"]))]
    for heading, identities in groups:
        lines.extend([f"## {heading}", "", "| 论文 | 本轮判定 |", "| --- | --- |"])
        for row in sorted(google["papers"], key=lambda x: x["id"], reverse=True):
            if row["id"] not in identities:
                continue
            judgment = row["judgement_zh"]
            if row["id"] in dates:
                judgment = "历史参考；官方 v1=" + dates[row["id"]]["original_arxiv_publication_date"]
            lines.append(f"| [{row['id']}](https://arxiv.org/abs/{row['id']}) {cell(row['title'])} | {cell(judgment)} |")
        lines.append("")
    lines.extend(["`2511.02767` 的旧审计日期 2026-04-23 不能作首发日，官方 v1 是 2025-11-04。",
                  "原快照不改写，本轮校正见 [日期证据](data/date-checks.json)。", ""])
    (HERE / "google-source-leads.md").write_text("\n".join(lines), encoding="utf-8")
    lines = ["# 已确认的 Google/Meta 优先短名单（9）", "",
             "这 9 项是有原文作者/机构或参与角色证据的优先项，不是全部候选的机构穷尽结论。",
             "没有现有可运行实现/指标匹配；完整实验成本建议与低成本组件机会分别列出。",
             "本轮只核查，不实施、不训练、不改原账本；9项完整实验的成本/来源终态已写在本轮报告，",
             "后续同步原账本与新分类器属于数据修复，而不是重新启动这些完整实验。",
             "成本终态只关闭完整实验，不把尚未实现的低成本组件变成已实现。", ""]
    for row in google["priority_pending_shortlist"]:
        lines.extend([f"## {row['id']} · {row['title']}", "",
            f"- 机构/角色：{row['affiliation']}", f"- 作者代码：{row['upstream_code']}",
            f"- 可负担对象：{row['low_cost_object']}",
            "- 完整实验：" + re.sub(r"\$(?=\d)", "USD ", row["full_experiment_cost"]),
            f"- 本轮完整实验终态：{next(d['full_experiment'] for d in result['this_audit_full_experiment_decisions'] if d['id'] == row['id'])}",
            f"- 低成本范围建议：{row['recommended_disposition']}",
            f"- 证据：[原文](https://arxiv.org/html/{row['id']}v1)；逐段定位见 [Google 对账](data/google-review.json)。", ""])
    for row in meta["pending_rows"]:
        lines.extend([f"## {row['id']} · {row['title']}", "",
            "- 机构：Meta 作者/合作机构已由原文核实。", f"- 原文资源：{row['primary_resource_evidence']}",
            f"- 当前缺项：{row['implementation_search_result']}",
            "- 本轮完整实验终态：成本过高，不复现（审查 DONE）。若拆廉价保真组件，应先另立明确范围；不以固定模拟器/图答案冒充核心算法。",
            f"- 证据：[原文]({row['official_source']})；{row['primary_locations']}；仓库定位见 [Meta 对账](data/meta-review.json)。", ""])
    lines.extend(["## 覆盖边界", "", "大部分旧候选未保留可独立验证的完整作者机构块。",
        "本轮对现有 45 份作者字段缓存做保险检查，另定向读取优先项官方作者块；部分缓存字段本身不完整。",
        "因此不能断言其余候选没有 Google/Meta 合作者，更不能把使用 Gemini/Llama 当成机构证据。", ""])
    (HERE / "priority-google-meta.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--import-reviews", type=Path)
    args = parser.parse_args()
    if args.import_reviews:
        sources = {"global-pending-review.json": "global-review.json",
                   "google-backlog-dedup.json": "google-review.json",
                   "meta-backlog-dedup.json": "meta-review.json",
                   "backlog-date-checks.json": "date-checks.json"}
        (HERE / "data").mkdir(exist_ok=True)
        prefix = str(ROOT.parents[1])
        for origin, destination in sources.items():
            data = json.dumps(load(args.import_reviews / origin), ensure_ascii=False, indent=2)
            data = data.replace(str(ROOT), ".").replace(prefix, "<repository>")
            (HERE / "data" / destination).write_text(data + "\n", encoding="utf-8")
    result = build()
    path = HERE / "reconciliation.json"
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if path.read_text(encoding="utf-8") != rendered:
            raise SystemExit("reconciliation changed; inspect the underlying evidence")
    else:
        path.write_text(rendered, encoding="utf-8")
        render_lists(result)
    print(json.dumps(result["counts"], ensure_ascii=False))


if __name__ == "__main__":
    main()
