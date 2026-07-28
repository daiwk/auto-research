from pathlib import Path
from ..foundational_ranking import run_foundational_reproduction

def reproduce(dataset_dir: Path, seed: int = 42):
    return run_foundational_reproduction(
        dataset_dir, seed,
        paper={"arxiv_id": "2604.19269", "title": "CS3: Efficient Online Capability Synergy for Two-Tower Recommendation", "url": "https://arxiv.org/abs/2604.19269", "organization": "Kuaishou"},
        baseline_kind="two-tower", method_kind="cs3",
        baseline_name="isolated two-tower dot product", method_name="CAS + CTS + cascade sharing",
        paper_results={"revenue_gain_percent": [8.356, 1.366, 2.177], "daily_active_users": "400M+"},
        scope="实际训练 cycle-adaptive self-revision gate、cross-tower 显式同步和 cascade teacher 辅助损失；未复刻快手在线 EMA cache。",
    )
