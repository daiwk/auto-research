def render(result):
    base = result["results"]["frozen_llm_semantic_mean"]
    method = result["results"]["learn_ceg_pch"]
    return f'''# LEARN reproduction

- Frozen LLM semantic mean NDCG@10: {base["ndcg_at_10"]:.5f}
- CEG + PCH + dense all-action NDCG@10: {method["ndcg_at_10"]:.5f}
- Paper online A/B: cold-start item revenue +8.77%; long-tail item revenue +4.63%
'''
