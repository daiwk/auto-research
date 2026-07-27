def render(result):
    base, method = result["baseline"], result["method"]
    return "\n".join([
        "# MiniMax Sparse Attention", "",
        f"公开数据：WikiText-2（{result['dataset']['train_tokens']} train bytes/tokens）", "",
        "| Variant | Validation loss | PPL | Attention pair ratio | Seconds |",
        "|---|---:|---:|---:|---:|",
        f"| {base['name']} | {base['validation_loss']:.4f} | {base['perplexity']:.2f} | {base['attention_pair_ratio']:.3f} | {base['seconds']:.2f} |",
        f"| {method['name']} | {method['validation_loss']:.4f} | {method['perplexity']:.2f} | {method['attention_pair_ratio']:.3f} | {method['seconds']:.2f} |", "",
        "## 复现边界", "", result["scope"], "",
    ])
