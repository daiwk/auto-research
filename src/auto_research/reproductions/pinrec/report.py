def render(result):
    base = result["results"]["unconditioned_next_token"]
    method = result["results"]["outcome_conditioned_multi_token"]
    return f'''# PinRec reproduction

- Unconditioned next-token unordered Recall@10: {base["unordered_recall_at_10"]:.5f}
- Outcome-conditioned multi-token unordered Recall@10: {method["unordered_recall_at_10"]:.5f}
- Paper online A/B: Homefeed grid clicks up to +4.01%; multi-token+OC +3.33%
'''
