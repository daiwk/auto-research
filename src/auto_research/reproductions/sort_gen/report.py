def render(result: dict) -> str:
    base, method = result["baseline"], result["method"]
    return "\n".join([
        "# SORT-Gen", "", f"公开数据：{result['dataset']['name']}（{result['dataset']['test_slates']} test slates）。", "",
        "| Variant | Click/slate | Pay/slate | GMV proxy | ILAD | Model calls |", "|---|---:|---:|---:|---:|---:|",
        f"| {base['name']} | {base['click_per_slate']:.4f} | {base['pay_per_slate']:.4f} | {base['gmv_proxy_per_slate']:.4f} | {base['ilad']:.4f} | {base['model_calls_per_slate']:.1f} |",
        f"| {method['name']} | {method['click_per_slate']:.4f} | {method['pay_per_slate']:.4f} | {method['gmv_proxy_per_slate']:.4f} | {method['ilad']:.4f} | {method['model_calls_per_slate']:.1f} |", "",
        f"Click {result['relative']['click_per_slate_percent']:+.2f}%；Pay {result['relative']['pay_per_slate_percent']:+.2f}%；GMV proxy {result['relative']['gmv_proxy_per_slate_percent']:+.2f}%；ILAD {result['relative']['ilad_percent']:+.2f}%。", "", "## 复现边界", "", result["scope"], "",
    ])
