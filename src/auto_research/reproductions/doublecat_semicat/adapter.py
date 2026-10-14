"""Explicit doublecat-semicat checkpoint/mechanism binding; never a fixture fallback."""
from pathlib import Path
import json

from auto_research.foundation_models.oct13_runtime import execute
from auto_research.paper_specs.runtime import adapter_from_spec
from auto_research.reproductions.registry import register


def reproduce(dataset_dir: Path, seed: int = 42) -> dict:
    return execute("doublecat-semicat", "run_doublecat_semicat.py", dataset_dir, seed)


def render(result: dict) -> str:
    return "# On the Design Space of Continuous Diffusion Language Models\n\n> 小规模核心机制诊断；不能据此宣称原文能力或效率提升。\n\n" + "执行结果：\n\n```json\n" + json.dumps(result, ensure_ascii=False, indent=2) + "\n```\n"


ADAPTER = register(adapter_from_spec(key="doublecat-semicat", run=reproduce, render=render))
