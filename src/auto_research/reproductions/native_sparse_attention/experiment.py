from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="native-sparse-attention",
        architecture="native_sparse_attention",
        paper_results={
            "quality": "27B-scale evaluations match or exceed full attention",
            "efficiency": "paper reports substantial decoding speedups at 64K context",
        },
        scope=(
            "本地实际训练压缩、query-selected fine block 与滑窗三分支，并学习逐 "
            "query/head 融合门；PyTorch 参考核只报告 attention-edge proxy，"
            "不复刻论文的 Triton 加速结论。"
        ),
    )
