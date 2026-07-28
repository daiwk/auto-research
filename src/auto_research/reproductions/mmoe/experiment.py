from pathlib import Path

from ..classic_multitask import run_multitask_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_multitask_reproduction(
        dataset_dir,
        seed,
        paper={
            "arxiv_id": "kdd2018-mmoe",
            "title": "Multi-gate Mixture-of-Experts",
            "url": "https://research.google/pubs/modeling-task-relationships-in-multi-task-learning-with-multi-gate-mixture-of-experts/",
            "organization": "Google",
        },
        baseline_kind="shared-bottom",
        method_kind="mmoe",
        baseline_name="shared-bottom multitask MLP",
        method_name="MMoE task-specific gates over shared experts",
        paper_results={"offline": "MMoE is more robust than shared-bottom models when task correlations vary."},
        scope="实际训练多个共享 expert、每个任务独立 softmax gate 与 CTR/conversion head；公开 MovieLens 构造两任务替代 Google 私有任务。",
    )
