def render(result: dict) -> str:
    lines = ["# OneTrans-V2 公开代理任务", "", "MovieLens 没有购买、金额、广告或真实漏斗；下列指标不能与原论文线上 A/B 比较。", "", "| 指标 | Validation | Test |", "| --- | ---: | ---: |"]
    for key in ("decision_exact_accuracy", "sid_exact_accuracy", "pre_rating_ge_3_auc", "fine_rating_ge_3_auc", "pre_rating_ge_4_auc", "fine_rating_ge_4_auc"):
        lines.append(f"| {key} | {result['validation'][key]:.5f} | {result['test'][key]:.5f} |")
    return "\n".join(lines + ["", result["scope"], ""])
