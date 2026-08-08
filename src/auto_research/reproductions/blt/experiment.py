from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction
def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(dataset_dir, seed, key="blt", architecture="blt", paper_results={"tokenizer_free": True, "dynamic_entropy_patching": True}, scope="实际执行可学习 surprisal boundary、相邻低熵位置 latent patch 共享并展开回原目标；当前 evaluator 的 512-symbol tokenizer 只近似 byte alphabet，未复刻 8B BLT 与完整 local encoder/decoder。")
