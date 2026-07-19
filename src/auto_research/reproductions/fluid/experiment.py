from pathlib import Path

from ..industrial_2026 import base_scores, evaluate, gain, load_industrial_data
from .model import build_lucid, lucid_score, train_prefix_tables


def reproduce_fluid(dataset_dir: Path, seed: int = 42) -> dict:
    data = load_industrial_data(dataset_dir)
    fused, slice_prefix, room_prefix, all_slices = build_lucid(data, seed)
    slice_tables = train_prefix_tables(data, slice_prefix)
    room_tables = train_prefix_tables(data, room_prefix)

    def slice_only(history):
        return lucid_score(data, fused, slice_prefix, room_prefix, slice_tables, room_tables, history, False)

    def fluid(history):
        return lucid_score(data, fused, slice_prefix, room_prefix, slice_tables, room_tables, history, True)

    baseline = evaluate(data, lambda history: base_scores(data, history))
    stages = {
        "stage_0_id_checkpoint": evaluate(data, lambda history: base_scores(data, history), target_split="validation"),
        "stage_1_slice_add_on": evaluate(data, lambda history: 0.65 * base_scores(data, history) + 0.35 * slice_only(history), target_split="validation"),
        "stage_2_item_id_phase_out": evaluate(data, slice_only, target_split="validation"),
        "stage_3_room_add_on": evaluate(data, fluid, target_split="validation"),
        "candidate_item_id_in_final_model": False,
        "rq_levels": slice_prefix.shape[1],
        "slice_views_per_item": all_slices.shape[1],
        "prefix_table_sizes": [int(slice_prefix[:, level].max()) + 1 for level in range(slice_prefix.shape[1])],
        "separate_slice_and_room_tables": True,
    }
    method = evaluate(data, fluid)
    return {
        "paper": {"arxiv_id": "2605.21832", "title": "FLUID: From Ephemeral IDs to Multimodal Semantic Codes for Industrial-Scale Livestreaming Recommendation", "url": "https://arxiv.org/abs/2605.21832", "organization": "TikTok / ByteDance"},
        "dataset": {"name": "MovieLens 100K", "users": len(data.sequences.train), "items": data.item_count},
        "setup": {"adapter": "fluid", "same_split_and_candidates": True, "seed": seed},
        "baseline": {"name": "ID ranker", **baseline},
        "method": {"name": "FLUID ID-free late fusion", **method},
        "relative": gain(method, baseline),
        "stages": stages,
        "paper_results": {"Quality Watch Duration": 0.55, "Cold-Start Room Views": 2.05, "Active Hours": 0.05},
        "scope": "实际执行 cross-domain content/collaborative fusion、slice-level residual K-means、room-level逐层多数投票、prefix n-gram 索引、slice/room 独立行为表、late fusion 与三阶段 item-ID phase-out；最终候选打分不读取 item ID transition/popularity。MovieLens genre/协同表征和扰动 slice 替代 SigLIP2+Qwen3 直播视觉、ASR/OCR 与真实 2 分钟切片。",
    }
