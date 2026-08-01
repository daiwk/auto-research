from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_wide(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="wide", architecture="wide_dynamic_width",
        paper_results={
            "target_sparsity_percent": 50.0,
            "prefill_kernel_speedup_x": 1.98,
            "decode_kernel_speedup_x": 4.95,
            "prefill_end_to_end_speedup_x": 1.68,
            "decode_end_to_end_speedup_x": 1.55,
        },
        scope="实际训练逐 token attention-head group 与 FFN-channel group router，并以 straight-through Top-K mask 保持 50% 动态宽度；本地 PyTorch dense kernel 不宣称获得论文定制 kernel 加速。",
    )
