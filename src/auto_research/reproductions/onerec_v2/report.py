def render(result):
    rows = result["results"]
    return f'''# OneRec-V2 reproduction

- Dataset: {result["dataset"]}
- Encoder-decoder loss: {rows["encoder_decoder"]["loss"]:.4f}
- Lazy decoder SFT loss: {rows["lazy_decoder_sft"]["loss"]:.4f}
- Lazy decoder + GBPO feedback-weighted probability: {rows["lazy_decoder_gbpo"]["feedback_weighted_probability"]:.6f}
- Paper online A/B: Kuaishou stay time +0.467%, Kuaishou Lite +0.741% (5% traffic, one week)
'''
