from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed,
        key="open-language-model",
        architecture="olm_composable",
        baseline_architecture="llama_modern",
        paper_results={
            "preset_count": 27,
            "model_families": 9,
            "four_gpu_weak_scaling_efficiency_percent": 90.6,
        },
        scope=(
            "本地以普通 PyTorch module 组合 Block/Residual/Repeat/Parallel 风格 decoder，"
            "同一模型可在 CPU、MPS、CUDA runtime 运行，并进入统一 micro-LLM evolve。"
            "未复制上游完整 27 presets 或四卡 348M 训练。"
        ),
    )


__all__ = ["reproduce"]
