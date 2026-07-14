def render(result):
    baseline = result["results"]["full_text_upper_tuning"]
    method = result["results"]["bahe_atomic_hierarchical"]
    return f'''# BAHE reproduction

- Full-text AUC: {baseline["auc"]:.4f}; latency: {baseline["milliseconds_per_example"]:.3f} ms/example
- BAHE AUC: {method["auc"]:.4f}; latency: {method["milliseconds_per_example"]:.3f} ms/example
- Paper online A/B: CTR +9.65%, advertising CPM +2.41% over two weeks
'''
