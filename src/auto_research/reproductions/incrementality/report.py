def render(result: dict) -> str:
    baseline, method = result["baseline"], result["method"]
    return "\n".join(
        [
            f"# {result['paper']['title']}",
            "",
            "| Policy | Value | Total incremental value | Budget | Uplift correlation |",
            "|---|---:|---:|---:|---:|",
            f"| {baseline['name']} | {baseline['policy_value']:.4f} | {baseline['total_incremental_value']:.4f} | {baseline['budget_fraction']:.2f} | {baseline['uplift_rank_correlation']:.4f} |",
            f"| {method['name']} | {method['policy_value']:.4f} | {method['total_incremental_value']:.4f} | {method['budget_fraction']:.2f} | {method['uplift_rank_correlation']:.4f} |",
            "",
            f"相对预测式分配：policy value {result['relative']['policy_value_percent']:+.2f}% 。",
            "",
            "## 复现边界",
            "",
            result["scope"],
            "",
        ]
    )
