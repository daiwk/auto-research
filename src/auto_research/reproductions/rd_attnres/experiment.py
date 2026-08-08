from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_rd_attnres(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="rd-attnres",
        architecture="rd_attnres",
        baseline_architecture="block_attnres",
        paper_results={
            "120m_perplexity_percent": -2.97,
            "343m_perplexity_percent": -2.43,
            "paired_training_wins": 10,
            "paired_training_runs": 10,
        },
        scope=(
            "实际让每层读取全部历史 residual sources，并以匹配的 Block AttnRes "
            "共享路由为基线；实验组仅将 QK 与 V 的内容依赖深度路由解耦。"
            "WikiText-2 micro-LM 不冒充论文 120M/343M 规模训练。"
        ),
    )
