def render(result: dict) -> str:
    validation, test = result["validation"], result["test"]
    lines = [
        "# X-Rec 公开数据核心机制复现", "",
        "论文线上 A/B 与以下 MovieLens 结果互不等价。", "",
        "| Split | Model | Hit@10 | NDCG@10 | Head share@10 |",
        "| --- | --- | ---: | ---: | ---: |",
    ]
    for name, split in (("validation", validation), ("test", test)):
        for model in ("u2i", "xrec"):
            metrics = split[model]
            lines.append(
                f"| {name} | {model} | {metrics['hit_at_10']:.5f} | "
                f"{metrics['ndcg_at_10']:.5f} | {metrics['head_share_at_10']:.5f} |"
            )
    return "\n".join(lines + ["", "## 边界", "", result["scope"], ""])
