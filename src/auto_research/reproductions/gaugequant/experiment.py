from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_gaugequant(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="gaugequant", architecture="gaugequant",
        paper_results={"llama2_7b_w4a4_ppl_baseline": 8.22, "llama2_7b_w4a4_ppl_gaugequant": 6.73},
        scope="真实学习 Householder 参数化的正交 gauge basis，以 LogSumExp outlier 正则训练并执行 W4A4 STE fake quantization；该参数化兼容 CPU/MPS/CUDA，未复刻 LLaMA-2 7B 全量训练或特定 GPU int4 kernel。",
    )
