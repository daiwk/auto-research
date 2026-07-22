def render(result: dict) -> str:
    base, method = result["variants"]["Transformer"], result["variants"]["QKV-Conv"]
    return "\n".join([
        "# Convolution for Large Language Models", "",
        f"公开数据：WikiText-2；同预算训练 {result['setup']['steps']} steps。", "",
        "| Variant | Parameters | Test loss | Perplexity |",
        "|---|---:|---:|---:|",
        f"| Transformer | {base['parameters']} | {base['loss']:.4f} | {base['perplexity']:.3f} |",
        f"| QKV-Conv | {method['parameters']} | {method['loss']:.4f} | {method['perplexity']:.3f} |", "",
        f"Perplexity 相对变化：{result['relative']['perplexity_reduction_percent']:+.2f}%（正数表示降低）。", "",
        "## 复现边界", "", result["scope"], "",
    ])
