def render(result: dict) -> str:
    lines = [
        "# CORE",
        "",
        f"公开数据：{result['dataset']['name']}（{result['dataset']['train_pairs']} train / {result['dataset']['test_pairs']} test pairs）。",
        "",
        "| Variant | Accuracy | Macro-F1 | NDCG@5 | Badcase@5 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, row in result["variants"].items():
        lines.append(
            f"| {name} | {row['accuracy']:.4f} | {row['macro_f1']:.4f} | "
            f"{row['ndcg_at_5']:.4f} | {row['badcase_at_5']:.4f} |"
        )
    lines += [
        "",
        f"PostCoT distilled cascade 相对 flat 基线：Accuracy {result['relative']['accuracy_points']:+.2f} 个百分点，"
        f"NDCG@5 {result['relative']['ndcg_at_5_percent']:+.2f}%。",
        "",
        "## 复现边界",
        "",
        result["scope"],
        "",
    ]
    return "\n".join(lines)
