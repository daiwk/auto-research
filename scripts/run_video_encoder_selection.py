#!/usr/bin/env python3
"""Frozen SmolVLM video features + Appendix-I conditional selector, L1 only.

No downloads, training, language-model generation, QA answers or learned
refinement. Uniform external quotas and an explicit scene proxy are not SITE.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import time

import torch
from torch.nn import functional as F

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from auto_research.foundation_models.video_encoder_selection import select_source_tokens  # noqa: E402

SOURCES = ["scripts/run_video_encoder_selection.py",
           "src/auto_research/foundation_models/video_encoder_selection.py"]
PROTOCOL = "video-encoder-conditional-selection-smolvlm-l1-v1"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_manifest(path: Path, max_examples: int) -> tuple[dict, list[dict]]:
    payload = json.loads(path.read_text())
    if set(payload) != {"dataset_id", "dataset_revision", "examples"}:
        raise ValueError("manifest allows only dataset_id, dataset_revision, examples; no answers")
    if not payload["dataset_id"] or not payload["dataset_revision"]:
        raise ValueError("public dataset identity and revision required")
    examples = payload["examples"]
    if not isinstance(examples, list) or not examples or len(examples) > max_examples:
        raise ValueError("manifest must fit the explicit small example budget")
    ids = []
    for row in examples:
        if set(row) - {"id", "video", "question", "fragments", "source_url"}:
            raise ValueError("example contains unsupported fields (answers/gold are forbidden)")
        if any(not isinstance(row.get(key), str) or not row[key].strip()
               for key in ("id", "video", "question", "source_url")):
            raise ValueError("each example requires id, video, question and public source_url")
        fragments = row.get("fragments", [])
        if not isinstance(fragments, list) or len(fragments) > 8 or any(
            not isinstance(fragment, str) or not fragment.strip() for fragment in fragments
        ):
            raise ValueError("at most eight nonempty question/option fragments allowed")
        video = Path(row["video"])
        row["video"] = video if video.is_absolute() else path.parent / video
        ids.append(row["id"])
    if len(set(ids)) != len(ids):
        raise ValueError("example IDs must be unique")
    return payload, examples


def decode_frames(path: Path, count: int):
    """Small-file uniform sampling; timestamps/indices retain original identity."""
    import av
    if not path.is_file() or path.stat().st_size > 16 * 1024 * 1024:
        raise ValueError("local video missing or exceeds the 16 MiB per-video cost gate")
    with av.open(str(path)) as container:
        stream = container.streams.video[0]
        if stream.width * stream.height > 1920 * 1080:
            raise ValueError("video resolution exceeds the 1080p diagnostic cost gate")
        if stream.duration is not None and float(stream.duration * stream.time_base) > 30:
            raise ValueError("video exceeds the 30-second diagnostic cost gate")
        metadata = []
        for index, frame in enumerate(container.decode(stream)):
            if index >= 1000:
                raise ValueError("video exceeds the 1000-decoded-frame cost gate")
            timestamp = float(frame.time) if frame.time is not None else float(index)
            metadata.append((index, timestamp))
    if len(metadata) < count:
        raise ValueError("not enough distinct source frames; repeated frames are not fabricated")
    chosen = [round(index * (len(metadata) - 1) / (count - 1)) for index in range(count)] if count > 1 else [0]
    # Two passes bound resident image memory to the selected frames, not every
    # decoded frame of a highly compressed video.
    frames = []
    with av.open(str(path)) as container:
        for index, frame in enumerate(container.decode(container.streams.video[0])):
            if index in chosen:
                frames.append((frame.to_image().convert("RGB"), *metadata[index]))
            if index >= chosen[-1]:
                break
    if len(frames) != count:
        raise ValueError("video decode changed between metadata and sampled-frame pass")
    if any(frames[index + 1][2] <= frames[index][2] for index in range(len(frames) - 1)):
        raise ValueError("video lacks strictly increasing source timestamps")
    return frames


class FrozenSmolVLMFeatures:
    def __init__(self, checkpoint: Path, device: str):
        from transformers import AutoModelForImageTextToText, AutoProcessor
        self.processor = AutoProcessor.from_pretrained(str(checkpoint), local_files_only=True)
        self.model = AutoModelForImageTextToText.from_pretrained(
            str(checkpoint), local_files_only=True, dtype=torch.float32,
            attn_implementation="eager").to(device).eval()
        if self.model.config.model_type not in ("smolvlm", "idefics3"):
            raise ValueError("only the explicit SmolVLM/Idefics3 backend is supported")
        for parameter in self.model.parameters():
            parameter.requires_grad_(False)
        self.device = device

    @torch.no_grad()
    def extract(self, frames, question: str, fragments: list[str]):
        import numpy as np
        from PIL import Image
        backbone = self.model.model
        config = self.model.config
        image_size = config.vision_config.image_size
        scale = config.scale_factor
        width = image_size // config.vision_config.patch_size // scale
        preprocessor = self.processor.image_processor
        mean = torch.tensor(preprocessor.image_mean, device=self.device)[:, None, None]
        std = torch.tensor(preprocessor.image_std, device=self.device)[:, None, None]
        features, intermediates, positions = [], [], []
        for image, _, timestamp in frames:
            # Explicit square resize is a documented bounded preprocessing
            # choice; it avoids multi-crop source ambiguities and huge images.
            image = image.resize((image_size, image_size), Image.Resampling.BICUBIC)
            pixels = torch.tensor(np.asarray(image).copy(), device=self.device).permute(2, 0, 1).float() / 255
            pixels = ((pixels - mean) / std)[None]
            visual = backbone.vision_model(pixel_values=pixels).last_hidden_state
            projected = backbone.connector(visual)[0]
            aligned_intermediate = backbone.connector.pixel_shuffle(visual, scale)[0]
            if projected.shape[0] != width * width:
                raise ValueError("projected token count does not match the source grid")
            features.append(projected)
            intermediates.append(aligned_intermediate)
            positions.append([[timestamp, (row + .5) / width, (column + .5) / width]
                              for row in range(width) for column in range(width)])
        questions = []
        for text in [question, *fragments]:
            ids = self.processor.tokenizer(text, add_special_tokens=False, return_tensors="pt")["input_ids"]
            if not 0 < ids.numel() <= 256:
                raise ValueError("question fragment must contain 1–256 input tokens; no silent truncation")
            questions.append(self.model.get_input_embeddings()(ids.to(self.device))[0].mean(dim=0))
        return (torch.stack(features), torch.stack(questions),
                torch.tensor(positions, device=self.device, dtype=torch.float64),
                {"connector_input": torch.stack(intermediates)})


def evaluate_features(features, questions, positions, streams, budget: int) -> dict:
    frames, tokens, _ = features.shape
    if not 0 < budget <= frames * tokens:
        raise ValueError("budget must fit the real source candidate pool")
    # This is an explicit external diagnostic budget profile, NOT SITE.
    quotas = torch.tensor([budget // frames + (frame < budget % frames) for frame in range(frames)],
                          device=features.device, dtype=torch.long)
    pooled = F.normalize(features.double().mean(dim=1), dim=-1)
    scene = (pooled[:-1] * pooled[1:]).sum(dim=-1).clamp(-1, 1)
    started = time.perf_counter()
    selected = select_source_tokens(features, questions, positions, quotas, scene, streams=streams)
    elapsed = time.perf_counter() - started
    independent = select_source_tokens(features, questions, positions, quotas, -torch.ones_like(scene), streams=streams)
    dense = features.flatten(0, 1)
    source_positions = positions.flatten(0, 1)
    embedding_error = float((selected.embeddings - dense[selected.indices]).abs().max())
    position_error = float((selected.positions - source_positions[selected.indices]).abs().max())
    stream_error = max((float((selected.streams[name] - value.flatten(0, 1)[selected.indices]).abs().max())
                        for name, value in streams.items()), default=0.)
    gain_sum = sum(len(move["indices"]) * move["score_per_token"] for move in selected.trace)
    gain_error = abs(selected.objective - gain_sum)
    actual_quotas = torch.bincount(selected.indices // tokens, minlength=frames)
    if (len(selected.indices) != budget or len(set(selected.indices.tolist())) != budget
            or not torch.equal(actual_quotas, quotas) or max(embedding_error, position_error, stream_error) != 0
            or gain_error > 1e-7):
        raise RuntimeError("source alignment, exact budget or independent objective identity failed")
    return {"metrics": {
        "candidate_tokens": frames * tokens, "selected_tokens": budget,
        "source_frames": frames, "tokens_per_frame": tokens,
        "compression_ratio": budget / (frames * tokens),
        "source_embedding_max_error": embedding_error, "source_position_max_error": position_error,
        "source_stream_max_error": stream_error, "objective_trace_absolute_error": gain_error,
        "correspondence_edges": len(selected.edges),
        "selected_correspondence_pairs": sum(edge.first in selected.indices.tolist() and edge.second in selected.indices.tolist()
                                              for edge in selected.edges),
        "pair_moves": sum(len(move["indices"]) == 2 for move in selected.trace),
        "correspondence_ablation_mask_difference": len(set(selected.indices.tolist()) ^ set(independent.indices.tolist())),
        "selected_question_relevance_mean": float(selected.relevance.flatten()[selected.indices].mean()),
        "objective": selected.objective, "selector_seconds": elapsed,
    }, "quotas": quotas.tolist(), "actual_quotas": actual_quotas.tolist(),
        "selected_source_indices": selected.indices.tolist(), "selected_source_positions": selected.positions.tolist(),
        "correspondence_disabled_indices": independent.indices.tolist(),
        "scene_similarities": scene.tolist(), "trace": list(selected.trace)}


def run_cases(examples, feature_loader, *, frames: int, budget: int, checkpoint_save) -> list[dict]:
    """Persist every success/failure immediately; no failed-example omission."""
    rows = []
    for example in examples:
        try:
            decoded = decode_frames(example["video"], frames)
            extracted = feature_loader.extract(decoded, example["question"], example.get("fragments", []))
            result = evaluate_features(*extracted, budget)
            row = {"id": example["id"], "status": "passed", "video_sha256": sha256(example["video"]),
                   "source_frame_indices": [frame[1] for frame in decoded],
                   "source_timestamps": [frame[2] for frame in decoded], **result}
        except Exception as exc:
            row = {"id": example["id"], "status": "failed", "error_type": type(exc).__name__, "error": str(exc)}
        rows.append(row)
        checkpoint_save(rows)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--checkpoint-id", required=True)
    parser.add_argument("--checkpoint-revision", required=True)
    parser.add_argument("--source-commit", help="explicit frozen 40-hex commit for a source-only execution directory")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--device", choices=("cpu", "cuda"), default="cpu")
    parser.add_argument("--frames", type=int, default=4)
    parser.add_argument("--budget", type=int, default=32)
    parser.add_argument("--max-examples", type=int, default=4)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if not 1 <= args.frames <= 8 or not 1 <= args.max_examples <= 4 or not 1 <= args.budget <= 64:
        parser.error("bounded L1 recipe requires 1–8 frames, 1–4 examples and budget 1–64")
    if not re.fullmatch(r"[0-9a-f]{40}", args.checkpoint_revision):
        parser.error("immutable public checkpoint commit required")
    if args.source_commit is not None and not re.fullmatch(r"[0-9a-f]{40}", args.source_commit):
        parser.error("source commit must be a full 40-hex commit")
    if args.device == "cuda" and not torch.cuda.is_available():
        parser.error("CUDA explicitly requested but unavailable; no CPU fallback")
    args.output_dir.mkdir(parents=True, exist_ok=False)
    report = {"schema_version": 1, "adapter_key": "video-encoder-selection", "protocol_id": PROTOCOL,
              "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
              "promotion_eligible": False, "evolve_integrated": False, "seed": args.seed,
              "created_at": datetime.now(timezone.utc).isoformat(), "device": args.device,
              "accelerator": {"vendor": "NVIDIA", "model": torch.cuda.get_device_name(0)} if args.device == "cuda" else {"model": "CPU"},
              "checkpoint": {"id": args.checkpoint_id, "revision": args.checkpoint_revision},
              "code_revision": args.source_commit or subprocess.check_output(
                  ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "executed_source_sha256": {source: sha256(ROOT / source) for source in SOURCES},
              "protocol": {"frozen_real_image_encoder": True, "independent_frame_encoding": True,
                           "question_input_embedding_mean": True, "inference_gold_read": False,
                           "test_read": False, "training_steps": 0, "refiner_enabled": False,
                           "quota_source": "external_uniform_not_SITE",
                           "scene_statistic": "explicit_mean_pooled_visual_cosine_proxy",
                           "full_SITE_selection_reproduced": False, "video_QA_capability_evaluated": False,
                           "frame_preprocessing": "single_square_bicubic_resize_model_native_image_size",
                           "budget": args.budget, "frames": args.frames}, "rows": [], "status": "running"}
    output = args.output_dir / "result.json"

    def save(rows):
        report["rows"] = rows
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n")

    save([])
    try:
        payload, examples = load_manifest(args.manifest, args.max_examples)
        report["dataset"] = {"id": payload["dataset_id"], "revision": payload["dataset_revision"],
                             "manifest_sha256": sha256(args.manifest), "examples": len(examples)}
        files = sorted(path for path in args.checkpoint.rglob("*") if path.is_file()
                       and path.suffix in {".json", ".safetensors", ".bin", ".model"})
        if not files or sum(path.stat().st_size for path in files) > 2 * 1024**3:
            raise ValueError("checkpoint missing or exceeds 2 GiB bounded cost gate; no download is attempted")
        content = {str(path.relative_to(args.checkpoint)): sha256(path) for path in files}
        report["checkpoint"]["content_sha256"] = hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()
        report["checkpoint"]["files_sha256"] = content
        torch.manual_seed(args.seed)
        loader = FrozenSmolVLMFeatures(args.checkpoint, args.device)
        rows = run_cases(examples, loader, frames=args.frames, budget=args.budget, checkpoint_save=save)
        report["status"] = "passed" if all(row["status"] == "passed" for row in rows) else "failed"
    except Exception as exc:
        report["status"] = "failed"
        report["failure"] = {"error_type": type(exc).__name__, "error": str(exc)}
    save(report["rows"])
    print(json.dumps({"status": report["status"], "completed_cases": len(report["rows"]), "output": str(output)}))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
