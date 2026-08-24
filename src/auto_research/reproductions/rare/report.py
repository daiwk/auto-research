def render(result: dict) -> str:
    lines = ["# RARE", "", "| Variant | Route agreement | Flip rate | Steering gain |", "|---|---:|---:|---:|"]
    for name, row in result["variants"].items():
        lines.append(f"| {name} | {row['route_agreement']:.4f} | {row['route_flip_rate']:.4f} | {row['steering_gain']:.4f} |")
    lines += ["", "## 复现边界", "", result["scope"], ""]
    return "\n".join(lines)
