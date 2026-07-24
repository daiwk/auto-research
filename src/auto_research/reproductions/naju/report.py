def render(result: dict) -> str:
    rows = result["variants"]
    lines = [
        "# Naju", "", "公开数据：WikiText-2；同 token、optimizer 和训练 step。", "",
        "| Variant | Parameters | Test loss | Perplexity |",
        "|---|---:|---:|---:|",
    ]
    for name, row in rows.items():
        lines.append(
            f"| {name} | {row['parameters']} | {row['loss']:.4f} | {row['perplexity']:.3f} |"
        )
    mixer = rows["Naju"]["mixer"]
    lines += [
        "",
        f"Naju PPL 相对变化：{result['relative']['perplexity_reduction_percent']:+.2f}%；"
        f"retain mean={mixer.get('forget_mean', 0):.3f}，"
        f"write mean={mixer.get('write_mean', 0):.3f}，"
        f"gate correlation={mixer.get('gate_correlation', 0):.3f}。",
        "",
        "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
