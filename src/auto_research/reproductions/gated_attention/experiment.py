from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="gated-attention",
        architecture="gated_attention",
        paper_results={
            "stability": "better training stability and learning-rate tolerance",
            "long_context": "attention sink is mitigated in extrapolation tests",
        },
        scope=(
            "本地在每个 attention head 的 SDPA 输出后执行 query-dependent "
            "sigmoid gate，并记录 gate mean/sparsity；缩小模型与训练预算后，"
            "不外推论文的大规模稳定性结论。"
        ),
    )
