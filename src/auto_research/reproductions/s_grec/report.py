from __future__ import annotations


def render(result: dict) -> str:
    test = result["test"]
    baseline = test["business"]
    method = test["a2po"]
    hr_lift = _lift(method["hr_at_10"], baseline["hr_at_10"])
    ndcg_lift = _lift(method["ndcg_at_10"], baseline["ndcg_at_10"])
    selected = result["setup"]["selected_variant"]
    psj = result["training"]["psj"]
    a2po = result["training"]["policy"]["a2po"]
    return f"""# S-GRec reproduction

## Outcome

- Dataset: `{result['dataset']['name']}` ({result['dataset']['test_users']} test users)
- Validation-selected production candidate: `{selected}`
- Business-only HR@10: `{baseline['hr_at_10']:.6f}`
- A2PO HR@10: `{method['hr_at_10']:.6f}` ({hr_lift:+.2f}%)
- Business-only NDCG@10: `{baseline['ndcg_at_10']:.6f}`
- A2PO NDCG@10: `{method['ndcg_at_10']:.6f}` ({ndcg_lift:+.2f}%)
- PSJ point accuracy SFT → aligned: `{psj['sft_point_accuracy']:.4f}` → `{psj['aligned_point_accuracy']:.4f}`
- PSJ pairwise accuracy: `{psj['pairwise_accuracy']:.4f}`
- A2PO semantic queries: `{a2po['semantic_queries']}`; directional consistency: `{a2po['directional_consistency']:.4f}`
- A2PO semantic-bound violations: `{a2po['semantic_bound_violations']}`

The local result is a public-data reproduction and is not the paper's online A/B result.
"""


def _lift(value, baseline):
    return 100.0 * (value - baseline) / baseline if baseline else 0.0
