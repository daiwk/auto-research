from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="switch-transformer",
        architecture="switch_transformer",
        paper_results={"pretraining_speedup_x": 7.0, "maximum_reported_parameters": "1.6T", "active_experts_per_token": 1},
        scope="实际执行 4-expert top-1 token routing、稀疏 dispatch 和 load-balancing auxiliary loss，并接入 micro-LLM evolve；未复刻跨设备 all-to-all 与万亿参数规模。",
    )
