"""Extracted unchanged from auto_research.reproductions.latest_20260809_common; stable mechanism boundary."""
from __future__ import annotations



def render_latest(result: dict) -> str:
    paper = result["paper"]
    rows = []
    source = result.get("variants", result.get("metrics", {}))
    if isinstance(source, dict):
        for key, value in source.items():
            if isinstance(value, dict):
                rows.extend((f"| {key} / {metric} | {number:.6f} |" for metric, number in value.items() if isinstance(number, (int, float))))
            elif isinstance(value, (int, float)):
                rows.append(f"| {key} | {value:.6f} |")
    return f"""# {paper['title']} 本地实验

> 本报告严格区分论文结果与本地缩小实验；具体复现边界见详情文档。

- 论文：[{paper['arxiv_id']}]({paper['url']})
- 数据：`{result['dataset']['name']}`
- seed：{result['setup']['seed']}

| 本地指标 | 值 |
| --- | ---: |
{chr(10).join(rows)}

## 复现边界

{result['scope']}
"""
