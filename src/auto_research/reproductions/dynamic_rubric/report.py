def render(result):
    baseline, method = result["baseline"], result["method"]
    return "\n".join([
        "# DynamicRubric", "",
        f"公开数据：{result['dataset']['name']}，{result['dataset']['test_preferences']} 条测试偏好。", "",
        "| Variant | Preference accuracy | Mean margin |",
        "|---|---:|---:|",
        f"| {baseline['name']} | {baseline['alpaca_preference_accuracy']:.4f} | {baseline['mean_good_vs_hard_negative_margin']:.4f} |",
        f"| {method['name']} | {method['alpaca_preference_accuracy']:.4f} | {method['mean_good_vs_hard_negative_margin']:.4f} |", "",
        f"相对静态 rubric：accuracy {result['relative']['preference_accuracy_percent']:+.2f}%。", "",
        "## 复现边界", "", result["scope"], "",
    ])
