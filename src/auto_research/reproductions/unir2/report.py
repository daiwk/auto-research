def render(result: dict) -> str:
    rows = result["variants"]
    lines = [
        "# UniR²",
        "",
        f"公开数据：MovieLens-1M（{result['dataset']['users']} users / {result['dataset']['items']} items）。",
        "",
        "| Variant | SID code acc. | Hit@10 | NDCG@10 | Params |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in rows.items():
        lines.append(
            f"| {name} | {row['sid_code_accuracy']:.4f} | {row['hit_at_10']:.4f} | "
            f"{row['ndcg_at_10']:.4f} | {row['parameters']} |"
        )
    lines += [
        "",
        f"统一模型相对独立 cascade：NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%。",
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
