"""Actual SmolVLM crop-conditioned on-policy self-distillation smoke.

Requires verified public training pixels and actual positive boxes. Never
manufactures a crop/answer from a held-out test or injects a gold completion.
"""
from __future__ import annotations

import argparse
import copy
from collections import Counter
import json
from pathlib import Path

import torch
from torch.nn import functional as F

from auto_research.multimodal.cv_opd import (
    VisionPolicy, ema_update, intersection_over_union, negative_crop, objective, sampled_training_rollouts, verify_answer,
)
from auto_research.post_training.local_lora import attach_lora
from auto_research.foundation_models.oct13_runtime import check_checkpoint_identity, check_dataset_identity

COCO_CLASSES = ("person", "cat", "dog", "car", "bus", "bird", "horse", "bicycle")
COCO_QUESTION = "Name the main object in this picture. Reply with one COCO category name and no other words."


def load_rows(path: Path, manifest: dict) -> list[dict]:
    if manifest.get("public_id") != "COCO2017/train2017" or manifest.get("source_split") != "train2017":
        raise ValueError("CV diagnostic must identify the original COCO train2017 source split")
    if path.name not in manifest["files"]:
        raise ValueError("CV records JSONL must be hashed in the verified dataset manifest")
    rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
    if not rows or any(row.get("split") not in ("train", "validation", "test")
                       or not row.get("verified") or not row.get("bbox")
                       or not row.get("question") or not (row.get("answer") or row.get("answers")) for row in rows):
        raise ValueError("verified image/question/answer/bbox with explicit train/validation/test split required")
    if any(len(row["bbox"]) != 4 for row in rows):
        raise ValueError("bbox must be pixel xyxy, four coordinates")
    if manifest.get("rows") is not None and manifest["rows"] != len(rows):
        raise ValueError("CV row count differs from the verified dataset manifest")
    for row in rows:
        row["references"] = row.get("answers", [row.get("answer")])
        if (not isinstance(row["references"], list) or not row["references"]
                or any(not isinstance(reference, str) or not reference.strip() for reference in row["references"])):
            raise ValueError("CV verifier references must be nonempty strings")
        image = Path(row["image"])
        image_path = image if image.is_absolute() else path.parent / image
        try:
            relative = image_path.resolve().relative_to(path.parent.resolve()).as_posix()
        except ValueError as error:
            raise ValueError("CV images must remain inside the verified dataset mirror") from error
        if relative not in manifest["files"]:
            raise ValueError("every CV image must be hashed in the verified dataset manifest")
        row["image"] = str(image_path)
    image_ids = {}
    for row in rows:
        relative = Path(row["image"]).resolve().relative_to(path.parent.resolve()).as_posix()
        identities = (("path", relative), ("sha256", manifest["files"][relative]),
                      ("source_id", str(row.get("image_id", row.get("id", relative)))))
        for identity in identities:
            if identity in image_ids and image_ids[identity] != row["split"]:
                raise ValueError("same source image cannot cross the training/held-out boundary")
            image_ids[identity] = row["split"]
    return rows


def evaluate(policy, rows, maximum_tokens: int) -> dict:
    from PIL import Image

    correct, total, lengths = 0, 0, []
    for row in rows:
        image = Image.open(row["image"]).convert("RGB")
        tokens = policy.rollout(image, row["question"], maximum_tokens)
        response = policy.processor.tokenizer.decode(tokens, skip_special_tokens=True)
        correct += verify_answer(response, row["references"])
        total += 1
        lengths.append(len(tokens))
    return {"accuracy": correct / total if total else None, "examples": total,
            "mean_generated_tokens": sum(lengths) / total if total else 0.}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--checkpoint", type=Path, required=True)
    p.add_argument("--checkpoint-id", required=True)
    p.add_argument("--checkpoint-revision", required=True)
    p.add_argument("--records", type=Path, required=True)
    p.add_argument("--dataset-id", required=True)
    p.add_argument("--dataset-revision", required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--device", default="cuda")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--steps", type=int, default=3)
    p.add_argument("--rollouts", type=int, default=8)
    p.add_argument("--max-new-tokens", type=int, default=16)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--contrastive-weight", type=float, default=.1)
    args = p.parse_args()
    if min(args.steps, args.rollouts, args.max_new_tokens, args.batch_size) < 1:
        p.error("positive training/rollout budgets required")
    checkpoint_manifest = check_checkpoint_identity(args.checkpoint, args.checkpoint_id, args.checkpoint_revision)
    dataset_manifest = check_dataset_identity(args.records.parent, args.dataset_id, args.dataset_revision,
                                             (args.records.name,))
    rows = load_rows(args.records, dataset_manifest)
    train = [row for row in rows if row["split"] == "train"]
    validation = [row for row in rows if row["split"] == "validation"]
    if not train:
        p.error("at least one public TRAIN row required")
    if any(row["question"] != COCO_QUESTION or len(row["references"]) != 1
           or row["references"][0] not in COCO_CLASSES for row in rows):
        p.error("this diagnostic requires the fixed label-free COCO question and exact category labels")
    label_counts = Counter(row["references"][0] for row in train)
    if len(label_counts) < 2:
        p.error("constant-label training is not a valid multiclass visual diagnostic")
    torch.manual_seed(args.seed)
    # Metadata/provenance validation and CLI help do not require the optional
    # vision runtime. Resolve it only when actually decoding pixels/loading VLMs.
    from PIL import Image
    from transformers import AutoModelForImageTextToText, AutoProcessor

    processor = AutoProcessor.from_pretrained(args.checkpoint, local_files_only=True)
    model = AutoModelForImageTextToText.from_pretrained(
        args.checkpoint, local_files_only=True, dtype=torch.bfloat16 if args.device == "cuda" else torch.float32,
        attn_implementation="eager").to(args.device)
    if model.config.model_type not in ("smolvlm", "idefics3"):
        p.error("this backend is verified for SmolVLM/Idefics3, not an untested Qwen3.5 claim")
    model.requires_grad_(False)
    attach_lora(model.model.text_model, rank=8, alpha=16.)
    teacher = copy.deepcopy(model).requires_grad_(False).eval()
    policy, teacher_policy = VisionPolicy(model, processor, args.device), VisionPolicy(teacher, processor, args.device)
    parameters = [value for value in model.parameters() if value.requires_grad]
    before = torch.cat([value.detach().flatten() for value in parameters]).clone()
    optimizer = torch.optim.AdamW(parameters, lr=2e-6, weight_decay=0.)
    baseline = evaluate(policy, validation, args.max_new_tokens)
    generator = torch.Generator().manual_seed(args.seed)
    history, updates, crop_failures, rollout_attempts = [], 0, [], []
    for step in range(args.steps):
        trajectories, correctness, sample_ids, crops = [], [], [], []
        for sample in range(args.batch_size):
            row = train[(step * args.batch_size + sample) % len(train)]
            image = Image.open(row["image"]).convert("RGB")
            box = tuple(int(round(coordinate)) for coordinate in row["bbox"])
            try:
                negative = negative_crop(image.size, box, generator=generator)
            except ValueError as error:
                crop_failures.append({"id": str(row.get("id", "unknown")), "reason": str(error)})
                continue
            rollouts, rewards = sampled_training_rollouts(policy, image, row["question"], row["references"],
                                                          args.rollouts, args.max_new_tokens)
            rollout_attempts.append({"step": step, "id": str(row.get("id", "unknown")),
                                     "rollouts": len(rollouts), "correct_rollouts": sum(rewards),
                                     "generated_tokens": sum(len(tokens) for tokens in rollouts),
                                     "retained": any(rewards)})
            if not any(rewards):
                continue  # NEVER insert the reference answer to bypass Eq. 13.
            positive_image, negative_image = image.crop(box), image.crop(negative)
            crops.append({"positive": list(box), "negative": list(negative),
                          "iou": intersection_over_union(box, negative), "correct_rollouts": sum(rewards)})
            for tokens, reward in zip(rollouts, rewards, strict=True):
                if not len(tokens):
                    continue
                model.train()
                student_logits = policy.trajectory_logits(image, row["question"], tokens)
                with torch.no_grad():
                    positive_logits = teacher_policy.trajectory_logits(positive_image, row["question"], tokens)
                    negative_logits = teacher_policy.trajectory_logits(negative_image, row["question"], tokens)
                trajectories.append((student_logits, positive_logits, negative_logits))
                correctness.append(reward)
                sample_ids.append(sample)
        if not trajectories:
            history.append({"step": step, "updated": False, "retained_samples": 0})
            continue
        length = max(len(item[0]) for item in trajectories)
        padded = [torch.stack([F.pad(item[branch], (0, 0, 0, length - len(item[branch])))
                               for item in trajectories]) for branch in range(3)]
        mask = torch.stack([torch.arange(length, device=args.device) < len(item[0]) for item in trajectories])
        optimizer.zero_grad()
        loss, parts = objective(*padded, mask, torch.tensor(correctness, device=args.device),
                                torch.tensor(sample_ids, device=args.device),
                                contrastive_weight=args.contrastive_weight)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.)
        optimizer.step()
        ema_update(teacher, model, .05)
        updates += 1
        history.append({"step": step, "updated": True, "loss": float(loss.detach()),
                        **{name: float(parts[name]) for name in ("opd", "cdl", "batch_mean", "retained_samples",
                                                                  "retained_rollouts", "gated_tokens", "valid_tokens")},
                        "crops": crops})
        print(json.dumps(history[-1]), flush=True)
    final_validation = evaluate(policy, validation, args.max_new_tokens)
    # No structural/hyperparameter selection reads test rows.
    test = [row for row in rows if row["split"] == "test"]
    final_test = evaluate(policy, test, args.max_new_tokens)
    delta = float((torch.cat([value.detach().flatten() for value in parameters]) - before).norm())
    report = {"paper": "2610.13264", "seed": args.seed, "diagnostic_only": True,
              "promotion_eligible": False, "fidelity": "core_mechanism", "evaluation_tier": "l1_mechanism",
              "checkpoint": {"id": args.checkpoint_id, "revision": args.checkpoint_revision,
                             "file_sha256": checkpoint_manifest["files"]},
              "dataset": {"id": args.dataset_id, "revision": args.dataset_revision,
                          "records_sha256": dataset_manifest["files"][args.records.name],
                          "source_split": dataset_manifest["source_split"],
                          "local_holdout_is_not_official_test": True,
                          "all_input_hashes_verified": True,
                          "input_file_sha256": dataset_manifest["files"]},
              "baseline_validation": baseline, "final_validation": final_validation, "final_test": final_test,
              "history": history, "optimizer_updates": updates, "parameter_delta_l2": delta,
              "crop_failures": crop_failures, "rollouts_per_sample": args.rollouts,
              "rollout_attempts": rollout_attempts,
              "total_training_rollout_tokens": sum(row["generated_tokens"] for row in rollout_attempts),
              "task_protocol": {"id": "coco-train2017-main-object-multiclass-v1",
                                "training_class_counts": dict(label_counts),
                                "gold_in_policy_prompt": False, "bbox_in_full_image_student_prompt": False,
                                "positive_negative_teacher_same_question": True,
                                "verifier": "exact category after case/punctuation/whitespace and leading a/an normalization"},
              "successful_parameter_update": updates > 0 and delta > 0,
              "objective_normalization": "Appendix A.3 Algorithm 1",
              "test_isolated_from_selection": True,
              "limitations": ["SmolVLM-256M + low-rank language updates, not Qwen3.5-4B full paper training",
                               "tiny public multiclass main-object subset, not fine-grained visual reasoning benchmark",
                               "strict external normalized category-name verifier, not the GPT-OSS-120B judge",
                               "no matched Vision-OPD training-budget capability comparison",
                               "zero accepted rollouts remains a failed zero-update run"]}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False))


if __name__ == "__main__":
    main()
