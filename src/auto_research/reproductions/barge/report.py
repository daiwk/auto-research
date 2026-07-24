def render(result: dict) -> str:
    base, method = result["baseline"], result["method"]
    osq = result["tokenizers"]["osqvae"]
    return "\n".join([
        "# BARGE", "",
        f"公开数据：MovieLens 100K（{result['dataset']['users']} users / {result['dataset']['items']} items）。", "",
        "| Variant | Hit@10 | NDCG@10 | Head share@10 |",
        "|---|---:|---:|---:|",
        f"| {base['name']} | {base['hit_at_10']:.4f} | {base['ndcg_at_10']:.4f} | {base['head_share_at_10']:.4f} |",
        f"| {method['name']} | {method['hit_at_10']:.4f} | {method['ndcg_at_10']:.4f} | {method['head_share_at_10']:.4f} |", "",
        f"NDCG@10 {result['relative']['ndcg_at_10_percent']:+.2f}%；"
        f"ICA gate mean={result['training']['barge']['ica_gate_mean']:.3f}；"
        f"OSQ orthogonality max error={osq['orthogonality_error']:.2e}。", "",
        "## 复现边界", "", result["scope"], "",
    ])
