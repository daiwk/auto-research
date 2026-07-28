from pathlib import Path

from ..classic_multitask import run_multitask_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_multitask_reproduction(
        dataset_dir,
        seed,
        paper={
            "arxiv_id": "recsys2020-ple",
            "title": "Progressive Layered Extraction",
            "url": "https://doi.org/10.1145/3383313.3412236",
            "organization": "Tencent",
        },
        baseline_kind="mmoe",
        method_kind="ple",
        baseline_name="MMoE shared experts",
        method_name="PLE shared + task-specific extraction",
        paper_results={"offline": "PLE outperforms strong multitask baselines on public and Tencent Video tasks."},
        scope="实际训练共享 expert、任务专属 expert、任务 gate 和独立 head 的 CGC/PLE 核心层；小规模公开数据替代腾讯视频多行为日志。",
    )
