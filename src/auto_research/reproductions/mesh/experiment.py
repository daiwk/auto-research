from pathlib import Path

from ..industrial_2026 import evaluate, load_industrial_data, summary_result, tune_blend
from .model import benchmark, score_flat, score_mesh, train_mesh


def reproduce_mesh(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    amplified, stages = train_mesh(data)
    stages["serving_benchmark"] = benchmark(data, amplified)
    baseline = evaluate(data, lambda h: score_flat(data, h))
    alpha, scorer, validation = tune_blend(data, lambda h: score_flat(data, h), lambda h: score_mesh(data, amplified, h))
    stages.update({"selected_blend": alpha, "validation": validation})
    method = evaluate(data, scorer)
    return summary_result(key="mesh", paper={"arxiv_id": "2607.12392", "title": "MESH: Scaling Up Retrieval with Heterogeneous Content Unification", "url": "https://arxiv.org/abs/2607.12392", "organization": "Pinterest"}, data=data, baseline_name="flat-retrieval", method_name="MESH", baseline=baseline, proposed=method, stages=stages, paper_results={"fresh-item repins": 5.5, "funnel efficiency": 55.0, "retention": 0.46, "throughput multiplier": 2.87}, scope="实际执行 user/item/context 分塔归一化、三层 residual signal amplification、intrinsic user-item Hadamard affinity 与 context 驱动 RGBC；本地缓存 item tower 测试 serving 路径，但不声称复现 Pinterest GPU inter-op 数值。")
