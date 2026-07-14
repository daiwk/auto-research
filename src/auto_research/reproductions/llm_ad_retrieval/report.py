from __future__ import annotations

from typing import Any


def render(result: dict[str, Any]) -> str:
    baseline = result["results"]["collaborative_graph"]
    method = result["results"]["collaborative_plus_llm_graph"]
    recall_gain = 100 * (method["recall_at_k"] / baseline["recall_at_k"] - 1) if baseline["recall_at_k"] else 0.0
    lexical = result["stability"]["lexical_graph"]
    semantic = result["stability"]["llm_semantic_graph"]
    ab = result["paper_online_ab"]
    return "\n".join([
        f"# {result['paper']['title']}", "",
        f"arXiv `{result['paper']['arxiv_id']}` · {result['dataset']}", "",
        "## Local public-data result", "",
        "| Route | Recall@K | NDCG@K |", "|---|---:|---:|",
        f"| Collaborative graph | {baseline['recall_at_k']:.4f} | {baseline['ndcg_at_k']:.4f} |",
        f"| + LLM semantic graph | {method['recall_at_k']:.4f} | {method['ndcg_at_k']:.4f} |",
        "", f"Matched-budget Recall@K change: **{recall_gain:+.2f}%**; validation selected semantic weight `{result['setup']['selected_alpha']}`.",
        "", "| Creative representation | Primary/shadow neighbor Jaccard@K | Mean score difference |", "|---|---:|---:|",
        f"| Lexical graph | {lexical['neighbor_jaccard_at_k']:.4f} | {lexical['mean_score_difference']:.4f} |",
        f"| LLM semantic graph | {semantic['neighbor_jaccard_at_k']:.4f} | {semantic['mean_score_difference']:.4f} |",
        "", "## Paper's production A/B evidence", "",
        f"The paper reports **+{ab['topline_lift_percent']:.2f}%** top-line performance, **+{ab['final_stage_recall_lift_percent']:.1f}%** final-stage recall, **-{ab['aa_difference_reduction_percent']:.2f}%** A/A' difference, and **+{ab['mad_improvement_percent']:.0f}%** MAD improvement.",
        "", "## Reproduction boundary", "", result["scope"], "",
    ])

