from pathlib import Path

from ..foundational_ranking import run_foundational_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir,
        seed,
        paper={
            "arxiv_id": "1703.04247",
            "title": "DeepFM",
            "url": "https://arxiv.org/abs/1703.04247",
            "organization": "Huawei Noah's Ark Lab",
        },
        baseline_kind="deep",
        method_kind="deepfm",
        baseline_name="embedding MLP",
        method_name="DeepFM shared-embedding FM + deep network",
        paper_results={"offline": "DeepFM improves AUC/logloss over FM and deep baselines on Criteo and Company datasets."},
        scope="实际联合训练二阶 FM 交互项与深层网络，并共享同一组 item/content embedding；MovieLens 隐式反馈替代华为私有 CTR 特征。",
    )
