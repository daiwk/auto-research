#!/usr/bin/env python3
"""Build the readable and machine-readable 2026 historical scan backlog.

The input files are the classified high-recall artifacts produced by
``classify_discovery_artifact.py``.  The committed output keeps every unique
new candidate visible while the Markdown page focuses on the papers that still
require full-text review and the fixed implementation batches.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "paper-audits"
JSON_PATH = OUT_DIR / "2026-historical-candidates.json"
MARKDOWN_PATH = OUT_DIR / "2026-historical-scan-plan.md"
TRACK_LABELS = {
    "recommendation": "搜广推与 LLM 应用",
    "foundation-model": "基础模型",
    "post-training": "LLM 后训练",
    "agent": "Agent",
}


COMPLETED = {
    "2607.26369": "PR #120 / ClockRoPE",
    "2607.27475": "PR #120 / OneShot",
    "2607.24789": "PR #120 / NEXT",
    "2606.26859": "PR #120 / AgentX",
}

# These fixed batches were completed after the initial scan PR.  Keeping the
# batch identity (instead of moving papers into B00) makes the historical plan
# auditable while removing them from the pending queue.
COMPLETED_BATCHES = {"B01", "B02", "B03"}


BATCHES: dict[str, dict] = {
    "B01": {
        "name": "8 月工业生成推荐与多模态",
        "ids": ["2608.21012", "2608.18322", "2608.17613", "2608.09634", "2608.07989"],
    },
    "B02": {
        "name": "7 月工业生成推荐、Agent harness 与搜索",
        "ids": ["2607.29241", "2607.29213", "2607.27789", "2607.14835", "2607.14418", "2607.26073", "2606.31031"],
    },
    "B03": {
        "name": "6–5 月序列建模、生成搜索与多场景排序",
        "ids": ["2606.19108", "2605.26717", "2605.25514", "2605.23702", "2605.21752", "2605.17863"],
    },
    "B04": {
        "name": "推荐 RL、知识迁移与 Semantic ID",
        "ids": ["2605.16344", "2605.05730", "2604.23522", "2604.12234", "2603.24226", "2603.22916"],
    },
    "B05": {
        "name": "电商生成、搜索融合与工业排序",
        "ids": ["2603.19710", "2603.19585", "2603.03988", "2603.00632", "2602.20995", "2602.17058"],
    },
    "B06": {
        "name": "2 月召回、广告、长序列与 LLM 排序",
        "ids": ["2602.12968", "2602.12354", "2602.11410", "2602.09744", "2602.09401", "2602.09194", "2602.01023"],
    },
    "B07": {
        "name": "LLM 架构、长上下文、KV cache 与评测基础设施",
        "ids": ["2608.12831", "2608.10296", "2608.08878", "2608.06849", "2608.05000", "2608.01672", "2608.02032", "2607.29032", "2607.17715"],
    },
    "B08": {
        "name": "OPD 与多教师/过程蒸馏",
        "ids": ["2608.19408", "2608.09745", "2608.05802", "2608.03673", "2608.03092", "2608.00782"],
    },
    "B09": {
        "name": "Rubric、外部 rollout 与多奖励 RL",
        "ids": ["2608.16072", "2608.11669", "2608.01717", "2607.28026", "2607.26873", "2607.19331"],
    },
    "B10": {
        "name": "Agentic RL 与长时序 credit assignment",
        "ids": ["2608.19842", "2608.19197", "2608.18682", "2608.17289", "2608.16156", "2608.11967"],
    },
    "B11": {
        "name": "Agent 记忆、工具规划与自进化系统",
        "ids": ["2608.15703", "2608.09380", "2608.06811", "2608.03468", "2608.02650", "2607.28527"],
    },
}


def _parse_artifact(value: str) -> tuple[str, Path]:
    track, separator, path = value.partition("=")
    if not separator or track not in TRACK_LABELS:
        raise argparse.ArgumentTypeError("artifact must be TRACK=PATH")
    return track, Path(path)


def _load(artifacts: list[tuple[str, Path]]) -> list[dict]:
    merged: dict[str, dict] = {}
    for expected_track, path in artifacts:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("track") != expected_track:
            raise ValueError(f"{path}: expected track {expected_track!r}")
        for source in payload.get("candidates", []):
            if source.get("repository_status") != "new":
                continue
            paper_id = source["arxiv_id"]
            row = merged.setdefault(paper_id, {
                "arxiv_id": paper_id,
                "title": source["title"],
                "published": source.get("published", ""),
                "tracks": [],
                "review_buckets": [],
                "matched_queries": [],
                "full_text_review_required": False,
            })
            row["tracks"].append(expected_track)
            row["review_buckets"].append(source["review_bucket"])
            row["matched_queries"].extend(source.get("matched_queries", []))
            row["full_text_review_required"] |= bool(source.get("full_text_review_required"))
    batch_for = {
        paper_id: batch
        for batch, spec in BATCHES.items()
        for paper_id in spec["ids"]
    }
    if len(batch_for) != sum(len(spec["ids"]) for spec in BATCHES.values()):
        raise ValueError("a paper is assigned to more than one implementation batch")
    missing = (set(batch_for) | set(COMPLETED)) - set(merged)
    if missing:
        raise ValueError(f"planned papers missing from classified artifacts: {sorted(missing)}")
    for paper_id, row in merged.items():
        row["tracks"] = sorted(set(row["tracks"]))
        row["review_buckets"] = sorted(set(row["review_buckets"]))
        row["matched_queries"] = sorted(set(row["matched_queries"]))
        if paper_id in COMPLETED:
            row["plan_status"] = "implemented-in-current-pr"
            row["implementation_batch"] = "B00"
            row["plan_reason"] = COMPLETED[paper_id]
        elif paper_id in batch_for and batch_for[paper_id] in COMPLETED_BATCHES:
            row["plan_status"] = "implemented-in-current-pr"
            row["implementation_batch"] = batch_for[paper_id]
            row["plan_reason"] = f"{BATCHES[batch_for[paper_id]]['name']} — completed"
        elif paper_id in batch_for:
            row["plan_status"] = "planned-implementation"
            row["implementation_batch"] = batch_for[paper_id]
            row["plan_reason"] = BATCHES[batch_for[paper_id]]["name"]
        elif row["full_text_review_required"]:
            row["plan_status"] = "fulltext-review-backlog"
            row["implementation_batch"] = None
            row["plan_reason"] = "not in fixed P0/P1 batches; retain until full-text rejection or promotion"
        else:
            row["plan_status"] = "p2-or-query-collision"
            row["implementation_batch"] = None
            row["plan_reason"] = "below current P0/P1 threshold; retained for audit, not silently discarded"
    return sorted(merged.values(), key=lambda row: (row["published"], row["arxiv_id"]), reverse=True)


def _render(rows: list[dict]) -> str:
    by_id = {row["arxiv_id"]: row for row in rows}
    review = [row for row in rows if row["full_text_review_required"]]
    counts = Counter(row["plan_status"] for row in rows)
    lines = [
        "# 2026-01-01 至 2026-08-24 历史扫描清单与实现批次",
        "",
        "> 本页不是把原始关键词命中冒充入选论文。机器可读全集见",
        "> [`2026-historical-candidates.json`](2026-historical-candidates.json)：每个去重后的新候选都保留检索来源、初筛桶和计划状态。",
        "",
        "## 漏斗与状态",
        "",
        "| 项目 | 数量 |",
        "|---|---:|",
        f"| 去重后的新候选 | {len(rows)} |",
        f"| 需要全文审查 | {len(review)} |",
        f"| 当前 PR 已实现 | {counts['implemented-in-current-pr']} |",
        f"| 固定后续实现队列 | {counts['planned-implementation']} |",
        f"| 仍待全文决定、未承诺实现 | {counts['fulltext-review-backlog']} |",
        f"| P2 或查询碰撞（保留审计记录） | {counts['p2-or-query-collision']} |",
        "",
        "`fulltext-review-backlog` 不是拒绝。只有核验机构、正文实验、代码状态和与现有实现的增量后，才能晋级后续批次或写入带原因的终态。工业搜广推继续执行量化线上 A/B/明确全流量硬门槛。",
        "",
        "## 固定实现批次",
        "",
        "### B00：当前 PR 已完成",
        "",
    ]
    for paper_id, reason in COMPLETED.items():
        row = by_id[paper_id]
        lines.append(f"- [{paper_id}](https://arxiv.org/abs/{paper_id}) {row['title']} — {reason}")
    for batch, spec in BATCHES.items():
        status = "（已完成）" if batch in COMPLETED_BATCHES else ""
        lines.extend(["", f"### {batch}：{spec['name']}{status}", ""])
        for paper_id in spec["ids"]:
            row = by_id[paper_id]
            labels = "、".join(TRACK_LABELS[track] for track in row["tracks"])
            lines.append(f"- [{paper_id}](https://arxiv.org/abs/{paper_id}) {row['title']} — {labels}")
    lines.extend([
        "",
        "## 全部 404 个全文审查候选",
        "",
        "状态含义：`Bxx` 为固定实现批次；`B00` 已完成；`待全文` 表示尚未承诺实现，但不会从账本消失。",
        "",
        "| 日期 | 领域 | 论文 | 初筛 | 计划 |",
        "|---|---|---|---|---|",
    ])
    for row in review:
        date = row["published"][:10]
        tracks = " / ".join(TRACK_LABELS[track] for track in row["tracks"])
        title = row["title"].replace("|", "\\|")
        bucket = ", ".join(row["review_buckets"])
        plan = row["implementation_batch"] or "待全文"
        lines.append(
            f"| {date} | {tracks} | [{row['arxiv_id']}](https://arxiv.org/abs/{row['arxiv_id']}) {title} | {bucket} | {plan} |"
        )
    lines.extend([
        "",
        "## 执行约束",
        "",
        "1. 每批开始前重新读论文正文，若不存在声称的证据则从批次移出，并在机器账本写明理由。",
        "2. 每篇必须有独立机制代码、公开数据/mini-suite 指标、完整论文信息、原文关键图和复现边界。",
        "3. 可接入 evolve 的机制必须同时注册 mutation；负结果照常保存。",
        "4. B01–B11 全部关闭前，后续扫描仍以本历史账本为基线；关闭后才恢复近期增量扫描。",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", action="append", type=_parse_artifact, required=True)
    args = parser.parse_args()
    rows = _load(args.artifact)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps({
        "schema_version": 1,
        "date_from": "2026-01-01",
        "date_to": "2026-08-24",
        "unique_new_candidates": len(rows),
        "papers": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MARKDOWN_PATH.write_text(_render(rows), encoding="utf-8")
    print(f"wrote {JSON_PATH} and {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
