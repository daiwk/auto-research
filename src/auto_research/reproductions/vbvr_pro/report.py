def render(result: dict) -> str:
    lines = ["# VBVR-Pro", "", "| Variant | Reward | Std |", "|---|---:|---:|"]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['reward_mean']:.4f} | {row['reward_std']:.4f} |")
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
