def render(result: dict) -> str:
    lines = [
        "# DataOrchestra",
        "",
        f"公开数据：WikiText-2；每组 {result['dataset']['train_tokens_per_variant']} 个训练 token、同模型同 step。",
        "",
        "| Variant | Final train loss | Test loss | Perplexity |",
        "|---|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(
            f"| {name} | {row['final_loss']:.4f} | {row['loss']:.4f} | {row['perplexity']:.3f} |"
        )
    lines += [
        "",
        f"DataOrchestra 相对 raw perplexity 变化：{result['relative']['perplexity_reduction_vs_raw_percent']:+.2f}%（正数表示降低）。",
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
