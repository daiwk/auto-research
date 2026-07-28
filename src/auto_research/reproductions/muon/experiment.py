from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="muon",
        architecture="llama_modern",
        optimizer="muon",
        paper_results={
            "efficiency": "paper reports about 2x computational efficiency",
            "scale": "Moonlight 3B/16B MoE was trained on 5.7T tokens",
        },
        scope=(
            "本地对隐藏层二维矩阵执行 momentum + quintic Newton-Schulz "
            "正交更新，embedding、norm、bias 和输出参数保留 AdamW；"
            "这是单机参考实现，不声称分布式吞吐复现。"
        ),
    )
