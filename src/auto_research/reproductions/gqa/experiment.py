from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction
def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(dataset_dir, seed, key="gqa", architecture="gqa", paper_results={"uptraining_compute_percent": 5.0}, scope="实际让 4 个 query heads 分组共享 2 个 K/V heads，并报告 KV cache 缩减；从头小模型训练替代论文从 MHA checkpoint 的 5% compute uptraining。")
