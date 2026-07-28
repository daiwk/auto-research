from pathlib import Path

from ..classic_multitask import run_multitask_reproduction


def reproduce(dataset_dir: Path, seed: int = 42):
    return run_multitask_reproduction(
        dataset_dir,
        seed,
        paper={
            "arxiv_id": "1804.07931",
            "title": "Entire Space Multi-Task Model",
            "url": "https://arxiv.org/abs/1804.07931",
            "organization": "Alibaba",
        },
        baseline_kind="clicked-cvr",
        method_kind="esmm",
        baseline_name="clicked-space CVR tower",
        method_name="ESMM pCTR × pCVR entire-space objective",
        paper_results={"offline": "ESMM improves AUC and calibration on the public Ali-CCP sample and industrial traffic logs."},
        scope="实际执行共享输入上的 CTR/CVR 双塔、pCTCVR=pCTR×pCVR 与 entire-space 联合损失；MovieLens rating 阈值构造 click/conversion 标签替代淘宝私有漏斗。",
    )
