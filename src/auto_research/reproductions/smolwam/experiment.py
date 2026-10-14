from __future__ import annotations
import json
from pathlib import Path
from ..lewam.external import execute


def reproduce_smolwam(dataset_dir: Path, seed: int) -> dict:
    return execute(json.loads((dataset_dir / "smolwam.json").read_text()), seed, "smolwam")


def render(result: dict) -> str:
    if result.get("phase") == "train":
        return ("# SmolWAM 真实teacher蒸馏与布局课程诊断\n\n实际28blockteacher目标与12blockstudent，"
                "两布局和四项L1更新；缩小步骤不等于原5000步效果复现。\n\n"
                + f"结果：`{result['variants']}`\n\n"
                "只按compact validation选checkpoint；新student闭环尚未在本阶段评测。\n")
    return ("# SmolWAM 真实 LIBERO 闭环\n\nNVIDIA 非商业权重许可；实际 Cosmos 12-block trunk，"
            "不是 VQA 代理。\n\n" + f"结果：`{result['variants']}`\n\n"
            "原始 teacher-target 缓存与 5000 步布局课程未重训；只声称发布策略推理核心复现。\n")
