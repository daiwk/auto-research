"""Extracted unchanged from auto_research.reproductions.latest_20260801_common; stable mechanism boundary."""
from __future__ import annotations



def render_latest(result: dict) -> str:
    lines = [
        f"# {result['paper']['title']}", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['users']} users / {result['dataset']['items']} items）。", "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 | Params |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['hit_at_10']:.4f} | {row['ndcg_at_10']:.4f} | {row['head_share_at_10']:.4f} | {row['parameters']} |")
    lines += ["", f"相对同预算基线：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。"]
    if "request_sharing" in result:
        lines += ["", f"本地 request-sharing 微基准：{result['request_sharing']['measured_speedup_x']:.2f}x（仅解释执行路径，不代表生产 QPS）。"]
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
