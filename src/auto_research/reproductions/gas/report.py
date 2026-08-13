import json


def render(result: dict) -> str:
    baseline = result["baseline"]
    method = result["method"]
    relative = result["relative"]
    return "\n".join((
        "# GAS 本地复现",
        "",
        f"- 数据集：{result['dataset']['name']}",
        f"- baseline test accuracy：{baseline['test_accuracy']:.4f}",
        f"- GAS test accuracy：{method['test_accuracy']:.4f}",
        f"- 变化：{relative['test_accuracy_points']:+.2f} pp",
        f"- 部署参数开销：{relative['deployed_parameter_overhead_percent']:.2f}%",
        f"- 生成分支最终 cosine loss：{method['final_generation_loss']:.4f}",
        "",
        "```json",
        json.dumps(result, ensure_ascii=False, indent=2),
        "```",
    ))
