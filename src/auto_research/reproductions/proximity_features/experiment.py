from pathlib import Path

from ..industrial_2026 import load_industrial_data, summary_result
from ..rec_utils import load_movielens_sequences
from .model import evaluate_proximity, train_proximity


def reproduce_proximity_features(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir, maximum_users=700, maximum_items=1500)
    full_catalog = load_movielens_sequences(dataset_dir)
    rows, keys, aggregates, global_feature, stages = train_proximity(dataset_dir, full_catalog.item_features)
    baseline, method, alpha = evaluate_proximity(rows, keys, aggregates, global_feature, full_catalog.item_features)
    stages["selected_blend"] = alpha
    result = summary_result(key="proximity-features", paper={"arxiv_id": "2607.12246", "title": "Proximity Features: Privacy-Compliant Cold-Start Personalization at Airbnb", "url": "https://arxiv.org/abs/2607.12246", "organization": "Airbnb"}, data=data, baseline_name="global-cold-start", method_name="adaptive-proximity", baseline=baseline, proposed=method, stages=stages, paper_results={"marketing bookings": 0.011, "first-time bookers": 2.0, "autosuggest bookings": 0.16}, scope="实际执行 dense ZIP hash refinement、sparse ZIP-prefix fine-to-coarse 聚合、稳定 proximity key 与 bucket aggregate cold-start scoring。公开 ZIP 只代理 geo-IP population-center 坐标；阈值按 943 用户缩为 12，不能解释为论文约 1000 用户的隐私保证。")
    result["dataset"].update({"zip_users": len(rows), "public_geo_proxy": "MovieLens ZIP"})
    return result
