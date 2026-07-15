from __future__ import annotations


def render(result: dict) -> str:
    test = result["test"]
    downstream = result["downstream"]
    return "\n".join(
        [
            "# Pinterest complementary LLM advertiser predictor",
            "",
            "| Variant | Recall@1 | Recall@5 | Recall@20 |",
            "|---|---:|---:|---:|",
            *[
                f"| {name} | {values['recall_at_1']:.4f} | {values['recall_at_5']:.4f} | {values['recall_at_20']:.4f} |"
                for name, values in test.items()
            ],
            "",
            f"Validation selected `{result['setup']['selected_variant']}`.",
            f"Two-tower Recall@50: {downstream['retrieval_recall_at_50_baseline']:.4f} → {downstream['retrieval_recall_at_50_complementary']:.4f}.",
            f"Sampled ranking AUC: {downstream['ranking_auc_baseline']:.4f} → {downstream['ranking_auc_with_llm_feature']:.4f}.",
            "",
            "## Reproduction boundary",
            "",
            result["scope"],
        ]
    )
