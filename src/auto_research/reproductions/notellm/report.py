def render(result):
    base = result["results"]["frozen_compression_embedding"]
    method = result["results"]["notellm_gcl_csft"]
    return f'''# NoteLLM reproduction

- Frozen compression embedding NDCG@10: {base["ndcg_at_10"]:.5f}
- GCL + CSFT NoteLLM NDCG@10: {method["ndcg_at_10"]:.5f}
- Paper online A/B: I2I CTR +16.20%; comments +1.10%
'''
