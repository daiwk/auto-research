def render(result):
    baseline = result["results"]["id_ranker"]
    method = result["results"]["kar_hybrid_expert"]
    return f'''# KAR reproduction

- ID ranker AUC: {baseline["auc"]:.4f}
- KAR hybrid-expert AUC: {method["auc"]:.4f}
- Generated knowledge prompts: {result["setup"]["generated_prompts"]}
- Paper online A/B: news recall +7%; music song plays +1.7% over seven days
'''
