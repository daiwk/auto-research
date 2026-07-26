def render(result: dict) -> str:
    lines = [
        "# AdaDSF", "",
        "公开数据：WikiText-2；Uniform MoD 与 AdaDSF 共享同一 dense teacher、"
        "80% 全局 token budget 和 alignment steps。", "",
        "| Variant | Test loss | Perplexity | Active token fraction |",
        "|---|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(
            f"| {name} | {row['loss']:.4f} | {row['perplexity']:.3f} | "
            f"{row.get('active_token_fraction', 1.0):.3f} |"
        )
    lines += [
        "",
        "AdaDSF 相对 Uniform MoD 的 PPL 降幅："
        f"{result['relative']['adaptive_vs_uniform_ppl_reduction_percent']:+.2f}%；"
        "相对 dense teacher 的 PPL 变化："
        f"{result['relative']['adaptive_vs_dense_ppl_change_percent']:+.2f}%。",
        "",
        "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
