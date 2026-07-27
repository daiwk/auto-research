def render(result: dict) -> str:
    rows = result["results"]
    lines = [
        "# Gzip-guided Sparse Attention",
        "",
        "公开数据：WikiText-2 原始 UTF-8 bytes；三个模型共享参数量、初始化和训练预算。",
        "",
        "| Mask | Validation BPB | Final train loss | Parameters |",
        "|---|---:|---:|---:|",
    ]
    for mode in ("dense", "bigbird", "gzip"):
        row = rows[mode]
        lines.append(
            f"| {mode} | {row['bits_per_byte']:.4f} | "
            f"{row['final_loss']:.4f} | {row['parameters']} |"
        )
    lines += [
        "",
        f"Gzip 相对 BigBird BPB 变化："
        f"{result['relative']['gzip_vs_bigbird_bpb_reduction_percent']:+.2f}%；"
        f"样例 attention edge 减少 "
        f"{result['mask']['sample_edge_reduction_percent']:.2f}%。",
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
