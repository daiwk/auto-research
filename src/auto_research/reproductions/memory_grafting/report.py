def render(result: dict) -> str:
    lines = [
        "# Memory Grafting", "",
        f"WikiText-2 · seed {result['setup']['seed']} · {result['setup']['memory_capacity']} frozen n-grams", "",
        "| Variant | Validation loss | PPL | Trainable params | Exact hit rate |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['loss']:.4f} | {row['perplexity']:.3f} | {row['parameters']} | {row['memory_hit_rate']:.2%} |")
    lines += [
        "",
        f"PPL change vs Transformer: **{result['relative']['ppl_vs_transformer_percent']:+.2f}%**; vs Engram: **{result['relative']['ppl_vs_engram_percent']:+.2f}%**.",
        "", "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
