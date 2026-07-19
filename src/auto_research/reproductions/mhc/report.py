def render(result: dict) -> str:
    lines = [
        "# mHC: Manifold-Constrained Hyper-Connections", "",
        f"WikiText-2 · seed {result['setup']['seed']} · {result['setup']['steps']} steps", "",
        "| Variant | Validation loss | PPL | Trainable params | row error | column error | spectral norm |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        stats = row["stability"]
        lines.append(
            f"| {name} | {row['loss']:.4f} | {row['perplexity']:.3f} | {row['parameters']} | "
            f"{stats.get('row_sum_error', 0):.2e} | {stats.get('column_sum_error', 0):.2e} | {stats.get('spectral_norm_max', 0):.4f} |"
        )
    lines += ["", f"mHC PPL change vs Transformer: **{result['relative']['perplexity_reduction_percent']:+.2f}%**.", "", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
