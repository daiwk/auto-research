from pathlib import Path

from ..llm_evolve_2026_common import run_llm_evolve_reproduction


def reproduce_engram(dataset_dir: Path, seed: int = 42):
    return run_llm_evolve_reproduction(
        dataset_dir, seed, key="engram", architecture="engram",
        paper_results={"mmlu_points": 3.4, "bbh_points": 5.0, "humaneval_points": 3.0, "runtime_overhead_percent": 3.0},
        scope="真实执行 O(1) hashed trigram memory table、门控注入与端到端训练，并注册为 evolve 架构；WikiText-2 64d 小模型不等同于论文大规模 Engram-27B/MoE 预训练。",
    )
