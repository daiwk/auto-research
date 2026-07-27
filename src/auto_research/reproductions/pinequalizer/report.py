def render(result: dict) -> str:
    baseline = result["results"]["baseline"]
    proposed = result["results"]["pinequalizer"]
    lines = [
        "# PinEqualizer", "",
        "公开数据：MovieLens-1M；以物品首见时间构造 fresh/underexplored cohort。", "",
        "| 指标 | Baseline | PinEqualizer | 相对变化 |",
        "|---|---:|---:|---:|",
    ]
    for metric, relative in (
        ("ndcg_at_10", "ndcg_at_10_percent"),
        ("fresh_ndcg_at_10", "fresh_ndcg_at_10_percent"),
        ("underexplored_exposure_at_10", "underexplored_exposure_percent"),
    ):
        lines.append(
            f"| {metric} | {baseline[metric]:.5f} | {proposed[metric]:.5f} | "
            f"{result['relative'][relative]:+.2f}% |"
        )
    lines += [
        "",
        "各 seed 的 UCB 系数只由 validation 选择，test 不参与调参。",
        "",
        "## 复现边界", "", result["scope"], "",
    ]
    return "\n".join(lines)
