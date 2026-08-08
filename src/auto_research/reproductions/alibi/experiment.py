from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction
def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(dataset_dir, seed, key="alibi", architecture="alibi", paper_results={"training_time_percent": -11.0, "memory_percent": -11.0}, scope="实际移除位置 embedding，并对各 attention head 加不同斜率的因果距离线性 bias；WikiText-2 小模型未复跑论文 WikiText-103 1.3B 参数实验。")
