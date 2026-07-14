def render(result):
    option = result["results"]["option_tuning"]
    adapter = result["results"]["option_adapter_tuning"]
    return f'''# M6-Rec reproduction

- Dataset: {result["dataset"]}
- Option tuning AUC: {option["auc"]:.4f}
- Option-adapter tuning AUC: {adapter["auc"]:.4f}
- Relative local AUC gain: {result["auc_gain_percent"]:+.2f}%
- Paper online A/B: Alipay mini-app retrieval relative CTR > +1.0%
'''
