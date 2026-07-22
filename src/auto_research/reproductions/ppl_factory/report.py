def render(result: dict) -> str:
    rows = result["variants"]
    lines = ["# PPL-Factory", "", "公开数据：WikiText-2；20% 数据预算、同微调 step。", "", "| Selection | Blocks | Mean scorer NLL | Test loss | Perplexity |", "|---|---:|---:|---:|---:|"]
    for name, row in rows.items():
        lines.append(f"| {name} | {row['selected_blocks']} | {row['mean_selection_nll']:.4f} | {row['loss']:.4f} | {row['perplexity']:.3f} |")
    lines += ["", f"PPL-Factory 相对随机选择 perplexity 变化：{result['relative']['perplexity_reduction_vs_random_percent']:+.2f}%（正数表示降低）。", "", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
