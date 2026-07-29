from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_penelope(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="penelope",
        architecture="penelope",
        paper_results={
            "claim": "competitive structured-reasoning accuracy with lower measured latency",
            "latent_recurrence_localized": True,
        },
        scope=(
            "真实在 micro decoder 中只对一个中间边界执行两步 GRU latent refinement，"
            "下层前缀不重复计算；WikiText-2 同预算训练不等同于论文结构推理 benchmark "
            "和完整 CoT-to-latent curriculum。"
        ),
    )
