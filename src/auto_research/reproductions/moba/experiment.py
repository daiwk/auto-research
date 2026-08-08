from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction
def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(dataset_dir, seed, key="moba", architecture="moba", paper_results={"context_tokens": 1000000}, scope="实际将历史划分为 8-token blocks，以 query 对 block key centroid 的相似度选择 top-2 causal blocks，再在命中块内执行精确 attention；PyTorch reference 未复刻百万上下文 fused kernel。")
