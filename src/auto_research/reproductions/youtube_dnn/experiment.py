from pathlib import Path

from ..foundational_ranking import run_foundational_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir,
        seed,
        paper={
            "arxiv_id": "recsys2016-youtube-dnn",
            "title": "Deep Neural Networks for YouTube Recommendations",
            "url": "https://research.google/pubs/deep-neural-networks-for-youtube-recommendations/",
            "organization": "Google / YouTube",
        },
        baseline_kind="two-tower",
        method_kind="youtube-dnn",
        baseline_name="mean-pooled two-tower",
        method_name="YouTube DNN nonlinear user tower",
        paper_results={"online": "Production serving architecture is described; the paper does not disclose a numeric online lift."},
        scope="实际训练历史平均池化、非线性 user tower 与全目录 item embedding 打分；公开 MovieLens 替代 YouTube 私有 watch/search/context 特征。",
    )
