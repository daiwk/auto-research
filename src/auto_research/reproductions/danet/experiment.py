from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, load_industrial_data, summary_result, tune_blend
from .model import score_danet, train_danet


def reproduce_danet(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    series, low, high, sensitivity, stages = train_danet(data)
    baseline = evaluate(data, lambda h: base_scores(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: base_scores(data, h), lambda h: score_danet(data, series, low, high, sensitivity, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="danet", paper={"arxiv_id": "2607.12578", "title": "Cheaper is Better: A Discount-Aware Network for Conversion Rate Prediction in E-commerce Recommendation System", "url": "https://arxiv.org/abs/2607.12578", "organization": "Alibaba Group / Tmall"}, data=data, baseline_name="IPN-interest", method_name="DANet", baseline=baseline, proposed=method, stages=stages, paper_results={"pCVR": 3.63, "GMV": 2.23, "discount-item PVR": 47.32}, scope="参照作者开源 TensorFlow 实现，实际执行 IPN score、FFT/IFFT 低高频分解、user attribute correction、promotion context gate 与 discount regression auxiliary。MovieLens 没有价格，周期性 popularity/rating 强度仅作为 DR time-series 代理，因此本地指标不解释为 CVR。")
