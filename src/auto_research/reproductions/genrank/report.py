def render(result):
    base = result["results"]["interleaved_item_action"]
    method = result["results"]["genrank_action_oriented"]
    return f'''# GenRank reproduction

- Interleaved item/action AUC: {base["auc"]:.4f}; latency: {base["milliseconds_per_example"]:.4f} ms/example
- Action-oriented GenRank AUC: {method["auc"]:.4f}; latency: {method["milliseconds_per_example"]:.4f} ms/example
- Paper online A/B: engagements +1.2474%, time spent +0.3345%
'''
