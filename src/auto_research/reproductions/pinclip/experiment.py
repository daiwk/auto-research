from pathlib import Path

from ..p1_2026_common import run_p1
from .model import build_pinclip_scorer


def reproduce_pinclip(dataset_dir: Path, seed: int = 42):
    return run_p1(
        key="pinclip", dataset_dir=dataset_dir,
        build_method=build_pinclip_scorer,
        baseline_name="raw genre/content similarity",
        method_name="PinCLIP neighbor-aligned representation",
        paper_results={"organic_fresh_repin_percent": 15.0, "new_ads_click_percent": 8.7, "offline_retrieval_percent": 20.0},
        scope="真实以共现图邻居为正样本学习内容/图 canonical contrastive alignment，并重点报告 fresh cohort；MovieLens genre 代理图文输入，未训练 Pinterest VLM/Hybrid ViT。",
    )
