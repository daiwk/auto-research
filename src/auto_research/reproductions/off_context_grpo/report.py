def render(result):
    baseline, method = result["baseline"], result["method"]
    return "\n".join([
        "# Off-Context GRPO", "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['test_examples']} test examples）", "",
        "| Variant | Pass@1 | Pass@8 | Gold margin |",
        "|---|---:|---:|---:|",
        f"| {baseline['name']} | {baseline['pass_at_1']:.4f} | {baseline['pass_at_8']:.4f} | {baseline['gold_margin']:.4f} |",
        f"| {method['name']} | {method['pass_at_1']:.4f} | {method['pass_at_8']:.4f} | {method['gold_margin']:.4f} |", "",
        f"相对 vanilla GRPO：Pass@1 {result['relative']['pass_at_1_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])
