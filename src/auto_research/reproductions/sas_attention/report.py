def render(result: dict) -> str:
    dense = result["test"]["dense"]
    sparse = result["test"]["sas"]
    return "\n".join([
        "# SAS: Simple Attention Sparsification", "",
        f"WikiText-2 · seed {result['setup']['seed']} · frozen backbone selector training", "",
        "| Variant | Test loss | Test PPL | Retained positions |",
        "|---|---:|---:|---:|",
        f"| Dense causal attention | {dense['loss']:.4f} | {dense['perplexity']:.3f} | 100% |",
        f"| SAS | {sparse['loss']:.4f} | {sparse['perplexity']:.3f} | {100 * result['routing']['retained_attention_fraction']:.1f}% |",
        "",
        f"Selector mean gradient norm: **{result['selector_training']['selector_gradient_norm_mean']:.4g}**.",
        "", "## 复现边界", "", result["scope"], "",
    ])
