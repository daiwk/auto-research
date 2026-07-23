#!/usr/bin/env python3
"""Synchronize the standard paper-information block in reproduction READMEs."""

from __future__ import annotations

from pathlib import Path

from auto_research.reproductions.registry import list_adapters


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "reproductions"
CHECKED_ON = "2026-07-23"
GITHUB_TREE = "https://github.com/daiwk/auto-research/tree/main"

# arXiv v1 publication dates, retrieved from the official arXiv API.
PUBLISHED_DATES = {
    "1706.06978": "2017-06-21",
    "1808.09781": "2018-08-20",
    "2205.08084": "2022-05-17",
    "2305.05065": "2023-05-08",
    "2306.10933": "2023-06-19",
    "2311.03758": "2023-11-07",
    "2402.17152": "2024-02-27",
    "2403.01744": "2024-03-04",
    "2403.13574": "2024-03-20",
    "2403.19347": "2024-03-28",
    "2405.03988": "2024-05-07",
    "2411.13789": "2024-11-21",
    "2412.06308": "2024-12-09",
    "2412.06860": "2024-12-09",
    "2502.08309": "2025-02-12",
    "2502.10157": "2025-02-14",
    "2502.13539": "2025-02-19",
    "2502.18965": "2025-02-26",
    "2503.02453": "2025-03-04",
    "2504.10507": "2025-04-09",
    "2505.04180": "2025-05-07",
    "2505.04421": "2025-05-07",
    "2505.07197": "2025-05-12",
    "2506.02267": "2025-06-02",
    "2507.12704": "2025-07-17",
    "2507.15551": "2025-07-21",
    "2507.15994": "2025-07-21",
    "2508.01375": "2025-08-02",
    "2508.20900": "2025-08-28",
    "2510.07784": "2025-10-09",
    "2510.26104": "2025-10-30",
    "2512.24880": "2025-12-31",
    "2601.12681": "2026-01-19",
    "2601.20083": "2026-01-27",
    "2602.10226": "2026-02-10",
    "2602.10606": "2026-02-11",
    "2602.14110": "2026-02-15",
    "2602.22732": "2026-02-26",
    "2602.22913": "2026-02-26",
    "2602.23639": "2026-02-27",
    "2603.28994": "2026-03-30",
    "2604.02684": "2026-04-03",
    "2605.05803": "2026-05-07",
    "2605.04726": "2026-05-06",
    "2605.09338": "2026-05-10",
    "2605.18771": "2026-04-16",
    "2605.19651": "2026-05-19",
    "2605.20948": "2026-05-20",
    "2605.21832": "2026-05-20",
    "2605.21969": "2026-05-21",
    "2605.23310": "2026-05-22",
    "2605.23572": "2026-05-22",
    "2605.24051": "2026-05-22",
    "2605.25749": "2026-05-25",
    "2605.27856": "2026-05-27",
    "2605.29755": "2026-05-28",
    "2606.20554": "2026-06-18",
    "2606.28533": "2026-06-26",
    "2607.00448": "2026-07-01",
    "2607.04728": "2026-07-06",
    "2607.11326": "2026-07-13",
    "2607.12246": "2026-07-14",
    "2607.12277": "2026-07-14",
    "2607.12392": "2026-07-14",
    "2607.12578": "2026-07-14",
    "2607.12714": "2026-07-14",
    "2607.12281": "2026-07-14",
    "2607.15730": "2026-07-17",
    "2607.15591": "2026-07-17",
    "2607.17092": "2026-07-19",
    "2607.18199": "2026-07-20",
    "2607.18413": "2026-07-20",
    "2607.13398": "2026-07-15",
    "2607.14192": "2026-07-15",
    "2607.14331": "2026-07-15",
    "2607.17017": "2026-07-19",
    "2607.17473": "2026-07-20",
    "2607.18796": "2026-07-21",
    "2607.19313": "2026-07-21",
    "2607.20083": "2026-07-22",
    "2605.17994": "2026-05-18",
}

# Older adapters predate the catalog metadata contract. Keep verified affiliations here
# until their PaperMetadata entries are migrated.
ORGANIZATION_OVERRIDES = {
    "cluster-goobs": "Meta",
    "cmsl": "Meta",
    "din": "Alibaba",
    "g2rec": "Meta",
    "hstu": "Meta",
    "hyformer": "ByteDance / Douyin Search",
    "llatte": "Meta",
    "longer": "ByteDance / Douyin",
    "memento": "Meta",
    "mixformer": "ByteDance / Douyin",
    "onerec": "Kuaishou",
    "onetrans": "ByteDance",
    "pinfm": "Pinterest",
    "plum": "Google DeepMind / YouTube",
    "rankmixer": "ByteDance / Douyin",
    "rec-distill": "ByteDance / Douyin / TikTok",
    "sasrec": "UC San Diego",
    "self-evolving-rec": "Google / YouTube",
    "tiger": "Google / Google DeepMind",
    "transact-v2": "Pinterest",
}


def _information_block(adapter) -> str:
    paper = adapter.paper
    try:
        published = PUBLISHED_DATES[paper.arxiv_id]
    except KeyError as exc:
        raise ValueError(
            f"Add the arXiv v1 date for {paper.arxiv_id} before publishing its docs"
        ) from exc

    organization = paper.organization or ORGANIZATION_OVERRIDES.get(adapter.key)
    if not organization:
        organization = "论文作者团队（原文未标注公司）"

    source_directory = f"src/auto_research/reproductions/{adapter.key.replace('-', '_')}/"
    if not (ROOT / source_directory).is_dir():
        raise ValueError(f"Missing reproduction source directory: {source_directory}")

    if paper.code_url:
        upstream_code = f"是：[官方/作者代码]({paper.code_url})"
    else:
        upstream_code = f"否：论文未提供官方/作者代码（核查日期：{CHECKED_ON}）"

    return "\n".join(
        (
            "## 论文信息",
            "",
            "| 项目 | 内容 |",
            "| --- | --- |",
            f"| 论文链接 | [arXiv {paper.arxiv_id}]({paper.url}) |",
            f"| 公司/机构 | {organization} |",
            f"| 首次公开日期 | {published}（arXiv v1） |",
            f"| 原文开源代码 | {upstream_code} |",
            f"| Adapter | `{adapter.key}` |",
            f"| 本地复现代码 | [`{source_directory}`]({GITHUB_TREE}/{source_directory}) |",
        )
    )


def main() -> None:
    marker = "## 原始论文总结"
    for adapter in list_adapters():
        path = DOCS / f"{adapter.paper.arxiv_id}-{adapter.key}" / "README.md"
        text = path.read_text(encoding="utf-8")
        if marker not in text:
            raise ValueError(f"Missing {marker!r} in {path}")

        prefix, body = text.split(marker, maxsplit=1)
        prefix_lines = prefix.rstrip().splitlines()
        title = prefix_lines[0]
        fidelity = [line for line in prefix_lines[1:] if line.startswith(">")]
        if not fidelity:
            raise ValueError(f"Missing fidelity statement in {path}")

        new_text = "\n\n".join(
            (
                title,
                "\n".join(fidelity),
                _information_block(adapter),
                marker + body,
            )
        )
        path.write_text(new_text.rstrip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
