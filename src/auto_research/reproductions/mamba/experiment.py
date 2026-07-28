from pathlib import Path
from ..llm_evolve_2026_common import run_llm_evolve_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="mamba", architecture="mamba",
        paper_results={"throughput_vs_transformer_x": 5.0, "maximum_model_size": "2.8B", "sequence_scaling": "linear"},
        scope="实际训练输入依赖 delta/B/C、causal depthwise convolution、selective recurrent scan 和门控输出，并接入 evolve；Python scan 替代官方并行 fused kernel。",
    )
