from __future__ import annotations

from pathlib import Path


UPSTREAM_URL = "https://github.com/salmon1802/UniRank"
SUPPORTED_UPSTREAM_DATASETS = (
    "QK_Video_Action",
    "KuaiRand_Video_Action",
    "TencentGR_10M_Action",
    "Taobao_Action",
    "MerRec_Action",
)
SUPPORTED_UPSTREAM_MODELS = (
    "HiFormer", "RankMixer", "INFNet", "LONGER", "OneTrans",
    "Zenith", "HyFormer", "MixFormer", "TokenMixer", "EST",
    "HeMix", "UniMixer", "TokenFormer", "UltraHSTU", "SSR",
)


def protocol_manifest() -> dict:
    return {
        "name": "UniRank chronological pointwise autoregressive protocol",
        "version": "2607.19987-v2",
        "paper": "https://arxiv.org/abs/2607.19987",
        "upstream": UPSTREAM_URL,
        "split": "per-user chronological 80/10/10 in upstream",
        "metrics": ("global AUC", "binary logloss"),
        "local_compatibility": (
            "MovieLens leave-two-out remains fixed; validation/test targets are "
            "evaluated chronologically against deterministic unseen negatives."
        ),
    }


def upstream_command(
    checkout: Path,
    experiment_id: str,
    *,
    gpu: str = "0",
) -> tuple[str, ...]:
    """Return the auditable command for a full upstream UniRank experiment."""
    runner = checkout / "run_expid.py"
    if not runner.exists():
        raise ValueError(
            f"{checkout} is not a UniRank checkout; clone {UPSTREAM_URL} first"
        )
    return (
        "python", str(runner), "--expid", experiment_id,
        "--gpu", gpu,
    )
