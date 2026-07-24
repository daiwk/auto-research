def render(result: dict) -> str:
    rows = result["variants"]
    lines = [
        "# Möbius RoPE", "",
        "公开数据：WikiText-2 + 合成单针检索；两组同初始化、同数据和同训练步数。", "",
        "| Variant | Parameters | Test PPL | Needle accuracy | Far-needle accuracy |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in rows.items():
        lines.append(
            f"| {name} | {row['parameters']} | {row['perplexity']:.3f} | "
            f"{row['needle_accuracy']:.3f} | {row['far_needle_accuracy']:.3f} |"
        )
    lines += [
        "",
        f"PPL 相对变化 {result['relative']['perplexity_reduction_percent']:+.2f}%；"
        f"needle accuracy {result['relative']['needle_accuracy_points']:+.2f} points。",
        "",
        "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
