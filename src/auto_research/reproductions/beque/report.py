def render(result):
    sft = result["results"]["sft"]
    pro = result["results"]["sft_plus_pro"]
    return f'''# BEQUE reproduction

- SFT retrieval Hit@1: {sft["hit_at_1"]:.4f}; feedback: {sft["feedback"]:.4f}
- SFT + PRO Hit@1: {pro["hit_at_1"]:.4f}; feedback: {pro["feedback"]:.4f}
- Paper online A/B (14 days): GMV +0.40%, transactions +0.34%, UV +0.33%
'''
