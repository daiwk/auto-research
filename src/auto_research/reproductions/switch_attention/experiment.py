from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="switch-attention",
        architecture="switch_attention",
        paper_results={"retrieval_vs_swa_relative_percent": 27.5, "long_context_vs_static_hybrid_percent": 6.3, "decode_speedup_32k_x": 4.0, "paper_full_attention_rate": 0.13},
        scope="实际共享 Q/K/V 计算 full 与 16-token sliding-window attention，并以逐 token、逐层可学习 router 融合，已接入 evolve；小模型 soft routing 替代论文 STE 与 branch-selective decode kernel。",
    )
