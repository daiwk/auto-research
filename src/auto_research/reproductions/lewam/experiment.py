from __future__ import annotations
import json
from pathlib import Path
from .external import execute


def reproduce_lewam(dataset_dir: Path, seed: int) -> dict:
    return execute(json.loads((dataset_dir / "lewam.json").read_text()), seed, "lewam")


def render(result: dict) -> str:
    if result.get("phase") == "train":
        return ("# LeWAM 真实联合训练诊断\n\n实际公共视觉轨迹、action flow/latent MSE/SIGReg；"
                "非完整50epoch或正式能力比较。\n\n" + f"结果：`{result['variants']}`\n\n"
                "validation选checkpoint；新训练candidate的闭环尚未在本阶段评测。\n")
    return ("# LeWAM 实际机器人闭环\n\n原作者固定 checkpoint；目标/起点来自训练轨迹，"
            "不是独立留出能力比较。\n\n" + f"结果：`{result['variants']}`\n\n"
            "未重训原版 50-epoch JEPA；不能宣称 full_pipeline。\n")
