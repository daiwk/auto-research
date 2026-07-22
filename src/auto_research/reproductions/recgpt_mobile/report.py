def render(result: dict) -> str:
    base, lora, quant = result["baseline"], result["method"], result["quantized_method"]
    return "\n".join([
        "# RecGPT-Mobile", "", f"公开数据：{result['dataset']['name']}（{result['dataset']['test_users']} test users）。", "",
        "| Variant | Primary intent acc. | Semantic intent acc. | Latency ms |", "|---|---:|---:|---:|",
        f"| {base['name']} | {base['primary_intent_accuracy']:.4f} | {base['semantic_intent_accuracy']:.4f} | {base['mean_latency_ms']:.2f} |",
        f"| {lora['name']} | {lora['primary_intent_accuracy']:.4f} | {lora['semantic_intent_accuracy']:.4f} | {lora['mean_latency_ms']:.2f} |",
        f"| {quant['name']} | {quant['primary_intent_accuracy']:.4f} | {quant['semantic_intent_accuracy']:.4f} | {quant['mean_latency_ms']:.2f} |", "",
        f"LoRA semantic accuracy {result['relative']['lora_semantic_accuracy_percent']:+.2f}%；INT8 serialized size 减少 {result['relative']['serialized_size_reduction_percent']:.2f}%；trigger 避免推理 {result['trigger']['inference_saved_percent']:.2f}%。", "", "## 复现边界", "", result["scope"], "",
    ])
