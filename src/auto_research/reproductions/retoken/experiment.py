from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_retoken(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir,
        seed,
        key="retoken",
        architecture="retoken",
        paper_results={
            "visual_haystacks_qwen3vl_8b_points": 13.4,
            "visual_haystacks_internvl35_points": 12.4,
            "lvbench_zero_shot_points": 8.0,
            "added_retrieval_tokens": 1,
        },
        scope=(
            "实际训练单个 retrieval target 与 value-space projection，并在每个因果查询上"
            "稀疏选择已可见 value cache；WikiText-2 用于验证梯度、稀疏率与语言建模质量，"
            "不冒充 MIRAGE、Visual Haystacks 或长视频 VLM 复现。"
        ),
    )
