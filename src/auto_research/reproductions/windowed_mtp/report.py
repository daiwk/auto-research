def render(result: dict) -> str:
    generation = result["generation"]
    lines = [
        "# Windowed-MTP", "",
        "公开数据：WikiText-2；同一 MTP draft 权重，仅改变 draft 可见的 KV key 集。", "",
        "| 路径 | Acceptance rate | Mean accepted / round | 与 dense greedy 完全一致 |",
        "|---|---:|---:|---:|",
        f"| Native full-context draft | {generation['native']['acceptance_rate']:.3f} | "
        f"{generation['native']['mean_accepted_per_round']:.3f} | "
        f"{generation['native_exact_match']} |",
        f"| Window + sink draft | {generation['windowed']['acceptance_rate']:.3f} | "
        f"{generation['windowed']['mean_accepted_per_round']:.3f} | "
        f"{generation['windowed_exact_match']} |",
        "",
        "| Context | Mode | Draft keys | ms / draft call | KV read reduction |",
        "|---:|---|---:|---:|---:|",
    ]
    for row in result["latency"]:
        lines.append(
            f"| {row['context']} | {row['mode']} | {row['key_count']} | "
            f"{row['milliseconds']:.4f} | {row['kv_read_reduction_percent']:.2f}% |"
        )
    lines += [
        "",
        "16384-token 本地 draft KV read 降幅："
        f"{result['relative']['context_16384_kv_read_reduction_percent']:.2f}%；"
        "实测 draft-call latency 变化："
        f"{result['relative']['context_16384_latency_reduction_percent']:+.2f}%。",
        "",
        "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
