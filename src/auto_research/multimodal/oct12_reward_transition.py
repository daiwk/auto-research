"""Actual VLM transition SFT and frozen-layer reward probing, Oct-12 batch.

The image enters the VLM processor and visual encoder, not an image-class
scorer. Reward features mean-pool RESPONSE tokens from intermediate language
layers, never prompt or image tokens. Dataset fields containing gold metadata
are available to training/evaluation only, never forwarded to generation.
"""
from __future__ import annotations

import hashlib
import io
import json
import random
import re
from collections import Counter
from pathlib import Path
from typing import Any

import torch
from torch import Tensor, nn
from torch.nn import functional as F
from auto_research.oct12_public_sources import (
    checkpoint_source, read_jsonl_mirror, recorded_verified_files, verified_image_path,
)

VLM_CHECKPOINT = "HuggingFaceTB/SmolVLM-256M-Instruct"
VLM_REVISION = "7e3e67edbbed1bf9888184d9df282b700a323964"
WOVEN_REVISION = "9ebd698c8500f4d4729ffe39bd78f4fd694904aa"
COCO_DATASET = "lmms-lab-encoder/COCO-Caption2017"
COCO_REVISION = "3bdd5827e243cc3084ac69a1111e69c3ab9193ff"


def group_split(rows: list[dict], group_key: str, seed: int) -> tuple[dict, dict]:
    """Split GROUPS, not questions/perturbations; exact assignment is audited."""
    groups = sorted({str(row[group_key]) for row in rows})
    if len(groups) < 5:
        raise ValueError("need at least five distinct public source groups")
    random.Random(seed).shuffle(groups)
    n_train = max(1, min(len(groups) - 2, int(len(groups) * 0.6)))
    n_val = max(1, min(len(groups) - n_train - 1, int(len(groups) * 0.2)))
    buckets = {"train": set(groups[:n_train]), "validation": set(groups[n_train:n_train + n_val]),
               "test": set(groups[n_train + n_val:])}
    split = {name: [r for r in rows if str(r[group_key]) in keys] for name, keys in buckets.items()}
    metadata = {"group_key": group_key, "source_groups_disjoint": True,
                "official_test": False, "seed": seed, "split_counts": {}, "group_sha256": {},
                "item_sha256": {}}
    for name, items in split.items():
        ids = sorted(str(r.get("id", r[group_key])) for r in items)
        metadata["split_counts"][name] = {"examples": len(items), "groups": len(buckets[name])}
        metadata["group_sha256"][name] = hashlib.sha256("\n".join(sorted(buckets[name])).encode()).hexdigest()
        metadata["item_sha256"][name] = hashlib.sha256("\n".join(ids).encode()).hexdigest()
    return split, metadata


def woven_prompt(row: dict, rotation: int = 0) -> tuple[list[dict], str]:
    """Project only observed question/options/images; exclude gold flags."""
    if len(row["options"]) != 4 or row["answer"] not in "ABCD":
        raise ValueError("WOVEN requires exactly four labeled options")
    rotation %= 4
    original = row["options"]
    options = original[rotation:] + original[:rotation]
    answer = None
    lines = []
    for label, option in zip("ABCD", options):
        lines.append(f"{label}. {option['content']}")
        if option["label"] == row["answer"]:
            answer = label
    if answer is None:
        raise ValueError("correct letter is absent from options")
    text = row["question"] + "\n" + "\n".join(lines) + "\nAnswer with one option letter."
    content = []
    for i, piece in enumerate(re.split(r"<image_(\d+)>", text)):
        if i % 2:
            index = int(piece) - 1
            if not 0 <= index < len(row["images"]):
                raise ValueError("unresolved image reference")
            content.append({"type": "image", "image": row["images"][index]})
        elif piece:
            content.append({"type": "text", "text": piece})
    if not any(c["type"] == "image" for c in content):
        raise ValueError("transition supervision must contain actual visual input")
    return [{"role": "user", "content": content}], answer


def decode_image(value: Any):
    from PIL import Image
    if isinstance(value, Image.Image):
        return value.convert("RGB")
    if isinstance(value, dict):
        if value.get("bytes"):
            return Image.open(io.BytesIO(value["bytes"])).convert("RGB")
        if value.get("path"):
            return Image.open(value["path"]).convert("RGB")
    raise ValueError("public row contains no decoded/embedded image")


def load_woven(dataset_dir: Path, maximum: int = 96):
    from auto_research.oct12_public_sources import managed_stream, public_parquet_rows
    if maximum < 5:
        raise ValueError("maximum must allow a grouped mini-suite")
    if (Path(dataset_dir) / "woven.jsonl").exists():
        rows, manifest = read_jsonl_mirror(dataset_dir, "woven.jsonl", "MLL-Lab/WOVEN", WOVEN_REVISION, "train")
        result = []
        for row in rows[:maximum]:
            row["images"] = [decode_image({"path": str(verified_image_path(x, dataset_dir, manifest))}) for x in row["images"]]
            result.append(row)
        return result
    dataset = public_parquet_rows("MLL-Lab/WOVEN", WOVEN_REVISION, "train",
                                  data_files="train/questions-*.parquet", cache_dir=dataset_dir)
    rows = []
    with managed_stream(dataset) as iterator:
        for row in iterator:
            row = dict(row)
            row["images"] = [decode_image(x) for x in row["images"]]
            rows.append(row)
            if len(rows) >= maximum:
                break
    return rows


def load_coco(dataset_dir: Path, maximum: int = 80):
    if (Path(dataset_dir) / "coco.jsonl").exists():
        rows, manifest = read_jsonl_mirror(dataset_dir, "coco.jsonl", COCO_DATASET, COCO_REVISION, "val")
        for row in rows[:maximum]:
            row["image"] = decode_image({"path": str(verified_image_path(row["image"], dataset_dir, manifest))})
        return rows[:maximum]
    from auto_research.oct12_public_sources import managed_stream, public_parquet_rows
    dataset = public_parquet_rows(COCO_DATASET, COCO_REVISION, "val", cache_dir=dataset_dir)
    rows = []
    with managed_stream(dataset) as iterator:
        for row in iterator:
            references = row["answer"]
            if not isinstance(references, list) or not references:
                raise ValueError("caption row must carry public reference captions")
            rows.append({"id": str(row["id"]), "image": decode_image(row["image"]),
                         "caption": references[0], "references": references})
            if len(rows) >= maximum:
                break
    return rows


def load_vlm(device: str, checkpoint: str = VLM_CHECKPOINT, revision: str = VLM_REVISION,
             checkpoint_path: Path | None = None):
    from transformers import AutoModelForImageTextToText, AutoProcessor
    source, source_args, _ = checkpoint_source(checkpoint, revision, checkpoint_path)
    processor = AutoProcessor.from_pretrained(source, **source_args)
    # Fixed dtype ensures the cached-feature head is not dependent on ambient AMP.
    model = AutoModelForImageTextToText.from_pretrained(
        source, **source_args, torch_dtype=torch.float32, attn_implementation="eager"
    ).to(device).eval()
    model.requires_grad_(False)
    return model, processor


def encode_prefix(processor, messages: list[dict], device: str) -> dict[str, Tensor]:
    images = [part["image"] for m in messages for part in m["content"] if part["type"] == "image"]
    # The template sees image placeholders; the processor receives the actual PIL
    # images in the identical reading order, including repeated references.
    clean = [{"role": m["role"], "content": [
        {"type": "image"} if c["type"] == "image" else {"type": "text", "text": c["text"]}
        for c in m["content"]]} for m in messages]
    text = processor.apply_chat_template(clean, tokenize=False, add_generation_prompt=True)
    inputs = processor(text=[text], images=[images], return_tensors="pt")
    return {name: value.to(device) for name, value in inputs.items()}


def append_response(processor, prefix: dict[str, Tensor], response: str,
                    *, eos: bool = False) -> tuple[dict[str, Tensor], Tensor]:
    ids = processor.tokenizer(response, add_special_tokens=False, return_tensors="pt").input_ids
    if eos:
        ids = torch.cat([ids, torch.tensor([[processor.tokenizer.eos_token_id]])], dim=1)
    if not ids.shape[1]:
        raise ValueError("empty response cannot be pooled/scored")
    ids = ids.to(prefix["input_ids"].device)
    inputs = dict(prefix)
    start = prefix["input_ids"].shape[1]
    inputs["input_ids"] = torch.cat([prefix["input_ids"], ids], dim=1)
    inputs["attention_mask"] = torch.cat([prefix["attention_mask"], torch.ones_like(ids)], dim=1)
    response_mask = torch.zeros_like(inputs["attention_mask"], dtype=torch.bool)
    response_mask[:, start:] = True
    return inputs, response_mask


def mean_response_states(states: Tensor, mask: Tensor) -> Tensor:
    if states.shape[:2] != mask.shape or not mask.any(dim=1).all():
        raise ValueError("response mask must align with hidden states and be nonempty")
    return (states.float() * mask[..., None]).sum(1) / mask.sum(1, keepdim=True)


@torch.no_grad()
def response_features(model, processor, messages, response: str, layers: list[int], device: str):
    model.eval()
    prefix = encode_prefix(processor, messages, device)
    inputs, mask = append_response(processor, prefix, response)
    output = model(**inputs, output_hidden_states=True, use_cache=False, return_dict=True)
    states = output.hidden_states
    if states is None:
        raise ValueError("checkpoint did not expose intermediate language hidden states")
    if any(layer <= 0 or layer >= len(states) - 1 for layer in layers):
        raise ValueError("probe layers must be intermediate (exclude embedding and final layer)")
    return {layer: mean_response_states(states[layer], mask).squeeze(0).detach().cpu()
            for layer in layers}


class LoRALinear(nn.Module):
    def __init__(self, base: nn.Linear, rank: int = 16, alpha: float = 4, dropout: float = .05):
        super().__init__()
        self.base = base.requires_grad_(False)
        self.a = nn.Parameter(torch.empty(rank, base.in_features, device=base.weight.device))
        self.b = nn.Parameter(torch.zeros(base.out_features, rank, device=base.weight.device))
        nn.init.kaiming_uniform_(self.a, a=5 ** .5)
        self.scaling = alpha / rank
        self.dropout = nn.Dropout(dropout)

    def forward(self, x: Tensor) -> Tensor:
        return self.base(x) + F.linear(F.linear(self.dropout(x), self.a), self.b) * self.scaling


def install_language_lora(model, rank: int = 16) -> list[str]:
    model.requires_grad_(False)
    selected = [(name, module) for name, module in model.named_modules()
                if isinstance(module, nn.Linear) and "text_model" in name
                and name.rsplit(".", 1)[-1] in {"q_proj", "k_proj", "v_proj", "o_proj"}]
    if not selected:
        raise ValueError("supported language q/k/v/o projections were not found")
    for name, module in selected:
        parent, child = name.rsplit(".", 1)
        setattr(model.get_submodule(parent), child, LoRALinear(module, rank))
    return [name for name, _ in selected]


def sft_response_loss(model, processor, messages, answer: str, device: str) -> Tensor:
    prefix = encode_prefix(processor, messages, device)
    inputs, mask = append_response(processor, prefix, answer, eos=True)
    labels = inputs["input_ids"].clone().masked_fill(~mask, -100)
    return model(**inputs, labels=labels, use_cache=False).loss


@torch.no_grad()
def choice_prediction(model, processor, messages, device: str) -> str:
    # Autoregressive likelihood, not a learned image-class scorer. Candidate
    # strings contain letters only; the unknown answer is never a prompt input.
    prefix = encode_prefix(processor, messages, device)
    scores = []
    for choice in "ABCD":
        inputs, mask = append_response(processor, prefix, choice)
        logits = model(**inputs, use_cache=False).logits[:, :-1].float()
        labels = inputs["input_ids"][:, 1:]
        token_scores = logits.log_softmax(-1).gather(-1, labels[..., None]).squeeze(-1)
        scores.append(float(token_scores[mask[:, 1:]].mean()))
    return "ABCD"[max(range(4), key=scores.__getitem__)]


def woven_accuracy(model, processor, rows, device: str, rotations: int = 1) -> dict:
    model.eval()
    correct, counts = 0, Counter()
    groups = {}
    for row in rows:
        for rotation in range(rotations):
            messages, answer = woven_prompt(row, rotation)
            predicted = choice_prediction(model, processor, messages, device)
            correct += int(predicted == answer)
            counts[predicted] += 1
            key = row["reasoning_type"]
            hit, total = groups.get(key, (0, 0))
            groups[key] = (hit + int(predicted == answer), total + 1)
    n = len(rows) * rotations
    return {"accuracy": correct / n, "examples": len(rows), "scored_permutations": n,
            "answer_counts": dict(counts), "by_reasoning_type": {
                key: {"accuracy": hit / total, "count": total} for key, (hit, total) in groups.items()}}


def run_woven(dataset_dir: Path, seed: int = 42, *, device: str = "cpu", maximum: int = 96,
              steps: int = 24, rank: int = 16, evaluation_rotations: int = 1,
              checkpoint: str = VLM_CHECKPOINT, checkpoint_revision: str = VLM_REVISION,
              checkpoint_path: Path | None = None) -> dict:
    if steps < 1 or evaluation_rotations not in {1, 4}:
        raise ValueError("positive SFT steps; evaluation rotations must be 1 or 4")
    torch.manual_seed(seed)
    rows = load_woven(dataset_dir, maximum)
    split, protocol = group_split(rows, "source_id", seed)
    model, processor = load_vlm(device, checkpoint, checkpoint_revision, checkpoint_path)
    modules = install_language_lora(model, rank)
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-4)
    rng, losses, permutation_counts = random.Random(seed), [], Counter()
    model.train()
    for step in range(steps):
        row = split["train"][rng.randrange(len(split["train"]))]
        rotation = step % 4
        permutation_counts[rotation] += 1
        messages, answer = woven_prompt(row, rotation)
        optimizer.zero_grad(set_to_none=True)
        loss = sft_response_loss(model, processor, messages, answer, device)
        loss.backward()
        torch.nn.utils.clip_grad_norm_((p for p in model.parameters() if p.requires_grad), 1.0)
        optimizer.step()
        losses.append(float(loss.detach()))
    # No test is read until the fixed training budget is complete. Baseline is
    # obtained from the same immutable frozen backbone with LoRA B disabled.
    trained_b = {name: module.b.detach().clone() for name, module in model.named_modules()
                 if isinstance(module, LoRALinear)}
    model.eval()
    method_val = woven_accuracy(model, processor, split["validation"], device, evaluation_rotations)
    method_test = woven_accuracy(model, processor, split["test"], device, evaluation_rotations)
    with torch.no_grad():
        for module in model.modules():
            if isinstance(module, LoRALinear):
                module.b.zero_()
    baseline_val = woven_accuracy(model, processor, split["validation"], device, evaluation_rotations)
    baseline_test = woven_accuracy(model, processor, split["test"], device, evaluation_rotations)
    with torch.no_grad():
        for name, module in model.named_modules():
            if isinstance(module, LoRALinear):
                module.b.copy_(trained_b[name])
    return {"paper": {"key": "woven"}, "seed": seed,
            "dataset": {"name": "MLL-Lab/WOVEN", "revision": WOVEN_REVISION,
                        "source_split": "train (only released split)", **protocol,
                        "offline_source_verification": recorded_verified_files(dataset_dir)
                            if (Path(dataset_dir) / "woven.jsonl").exists() else None},
            "checkpoint": {"name": checkpoint, "revision": checkpoint_revision,
                           "offline_source_verification": recorded_verified_files(checkpoint_path)},
            "evaluation_tier": "L1", "fidelity": "core_mechanism", "diagnostic_only": True,
            "baseline": {"name": "frozen base VLM", **baseline_test},
            "method": {"name": "visual-transition response-token LoRA SFT", **method_test},
            "validation": {"baseline": baseline_val, "method": method_val},
            "stages": {"actual_image_encoder_input": True, "steps": steps, "lora_rank": rank,
                       "lora_alpha": 4, "lora_dropout": .05, "lora_modules": modules,
                       "option_permutation_counts": dict(permutation_counts),
                       "train_loss_first_last": [losses[0], losses[-1]],
                       "grpo_executed": False, "external_benchmark_transfer_executed": False},
            "scope": "真实公开 transition 图像→VLM→response-only SFT；仅官方 train 的 source_id 分组 mini-suite，不等于官方 test；未运行 GRPO 或26项迁移。"}


EDIT_WORDS = {
    "red": "blue", "blue": "red", "green": "yellow", "yellow": "green",
    "black": "white", "white": "black", "brown": "gray", "gray": "brown",
    "one": "two", "two": "three", "three": "two", "four": "five", "five": "four",
    "small": "large", "large": "small", "left": "right", "right": "left",
    "above": "below", "below": "above", "front": "behind", "behind": "front",
}


def caption_negative(caption: str, other: str, rng: random.Random) -> tuple[str, str]:
    """Same-response perturbation mixture; record inapplicable edit fallbacks."""
    draw = rng.random()
    if draw < .15:
        return other, "cross_image"
    if draw < .65:
        spans = list(re.finditer(r"\b(" + "|".join(EDIT_WORDS) + r")\b", caption, re.I))
        if spans:
            span = rng.choice(spans)
            new = EDIT_WORDS[span.group().lower()]
            if span.group()[0].isupper():
                new = new.capitalize()
            return caption[:span.start()] + new + caption[span.end():], "near_one_span"
    if draw < .85:
        own, foreign = caption.split(), other.split()
        cut = max(1, len(own) // 2)
        negative = " ".join(own[:cut] + foreign[len(foreign) // 2:])
        if negative != caption:
            return negative, "splice"
    clauses = [p.strip() for p in re.split(r"[,;]", caption) if p.strip()]
    if len(clauses) > 1:
        shifted = clauses[1:] + clauses[:1]
        return ", ".join(shifted), "clause_shuffle"
    # No model-written negative: retain a recorded cross-image fallback.
    return other, "cross_image_fallback"


def in_batch_bt(head: nn.Module, positive: Tensor, negative: Tensor, beta: float = .1) -> Tensor:
    if positive.shape != negative.shape or positive.ndim != 2 or beta <= 0:
        raise ValueError("aligned feature matrices and positive beta required")
    plus, minus = head(positive).flatten(), head(negative).flatten()
    return F.softplus(-beta * (plus[:, None] - minus[None])).mean()


def train_reward_head(positive: Tensor, negative: Tensor, seed: int, steps: int = 200,
                      batch_size: int = 8, initial: nn.Linear | None = None) -> nn.Linear:
    torch.manual_seed(seed)
    head = nn.Linear(positive.shape[1], 1, bias=False)
    if initial is None:
        nn.init.zeros_(head.weight)
    else:
        head.load_state_dict(initial.state_dict())
    optimizer = torch.optim.AdamW(head.parameters(), lr=1e-3, weight_decay=.01)
    rng = torch.Generator().manual_seed(seed)
    for _ in range(steps):
        indices = torch.randint(len(positive), (min(batch_size, len(positive)),), generator=rng)
        optimizer.zero_grad(set_to_none=True)
        loss = in_batch_bt(head, positive[indices], negative[indices])
        loss.backward()
        optimizer.step()
    return head.eval()


@torch.no_grad()
def pair_accuracy(head: nn.Module, positive: Tensor, negative: Tensor) -> float:
    delta = (head(positive) - head(negative)).flatten()
    return float(((delta > 0).float() + .5 * (delta == 0).float()).mean())


def select_probe_layer(validation_accuracy: dict[int, float]) -> int:
    if not validation_accuracy:
        raise ValueError("empty validation layer sweep")
    # Explicit, deterministic tie breaking; this function has no test input.
    return max(sorted(validation_accuracy), key=validation_accuracy.__getitem__)


OBJECT_ALIASES = {
    "person": ("person", "people", "man", "woman", "men", "women", "boy", "girl", "child", "children"),
    "bicycle": ("bicycle", "bike", "bikes"), "motorcycle": ("motorcycle", "motorbike"),
    "car": ("car", "cars"), "bus": ("bus", "buses"), "train": ("train",),
    "truck": ("truck",), "boat": ("boat",), "airplane": ("airplane", "plane"),
    "bird": ("bird", "birds"), "cat": ("cat", "cats"), "dog": ("dog", "dogs"),
    "horse": ("horse", "horses"), "sheep": ("sheep",), "cow": ("cow", "cows"),
    "elephant": ("elephant",), "bear": ("bear",), "zebra": ("zebra",), "giraffe": ("giraffe",),
    "chair": ("chair", "chairs"), "couch": ("couch", "sofa"), "bed": ("bed",),
    "dining table": ("table", "dining table"), "toilet": ("toilet",), "tv": ("tv", "television"),
    "laptop": ("laptop",), "cell phone": ("phone", "cellphone", "cell phone"),
    "bottle": ("bottle",), "cup": ("cup",), "bowl": ("bowl",), "banana": ("banana",),
    "apple": ("apple",), "sandwich": ("sandwich",), "pizza": ("pizza",),
    "orange": ("orange",), "cake": ("cake",), "fork": ("fork",), "knife": ("knife",),
    "spoon": ("spoon",), "umbrella": ("umbrella",), "backpack": ("backpack",),
    "handbag": ("handbag", "purse"), "suitcase": ("suitcase",), "tie": ("tie",),
    "skis": ("skis",), "snowboard": ("snowboard",), "skateboard": ("skateboard",),
    "surfboard": ("surfboard",), "sports ball": ("ball", "sports ball"),
    "tennis racket": ("tennis racket",), "baseball bat": ("baseball bat",),
    "baseball glove": ("baseball glove",), "kite": ("kite",), "frisbee": ("frisbee",),
    "traffic light": ("traffic light",), "stop sign": ("stop sign",),
    "fire hydrant": ("fire hydrant",), "parking meter": ("parking meter",), "bench": ("bench",),
    "oven": ("oven",), "microwave": ("microwave",), "refrigerator": ("refrigerator", "fridge"),
    "sink": ("sink",), "toaster": ("toaster",), "scissors": ("scissors",), "clock": ("clock",),
    "book": ("book", "books"), "vase": ("vase",), "toothbrush": ("toothbrush",),
    "teddy bear": ("teddy bear",), "hair drier": ("hair drier", "hair dryer"),
    "keyboard": ("keyboard",), "mouse": ("mouse",), "remote": ("remote",),
    "wine glass": ("wine glass",), "hot dog": ("hot dog",), "broccoli": ("broccoli",),
    "carrot": ("carrot",), "donut": ("donut",), "potted plant": ("plant", "potted plant"),
}


def mentioned_objects(caption: str) -> set[str]:
    return {name for name, aliases in OBJECT_ALIASES.items()
            if any(re.search(r"\b" + re.escape(alias) + r"\b", caption.lower()) for alias in aliases)}


def verifier_score(candidate: str, allowed_objects: set[str]) -> float | None:
    """Caption-supported absent-object diagnostic, NOT official CHAIR.

    Object-free responses abstain, so empty captions do not mint successes.
    The verifier is outside the VLM: reference objects NEVER enter its prompt.
    """
    mentions = mentioned_objects(candidate)
    if not mentions:
        return None
    return 1 - len(mentions - allowed_objects) / len(mentions)


def mint_verified_pair(candidates: list[str], allowed_objects: set[str]):
    scored = [(candidate, verifier_score(candidate, allowed_objects)) for candidate in candidates]
    usable = [(candidate, score) for candidate, score in scored if score is not None]
    if len(usable) < 2:
        return None
    chosen, high = max(usable, key=lambda p: p[1])
    rejected, low = min(usable, key=lambda p: p[1])
    if high <= low:
        return None
    return chosen, rejected, high, low


def caption_messages(image) -> list[dict]:
    return [{"role": "user", "content": [{"type": "image", "image": image},
             {"type": "text", "text": "Describe the image accurately in one sentence."}]}]


@torch.no_grad()
def generate_candidates(model, processor, image, count: int, device: str) -> list[str]:
    prefix = encode_prefix(processor, caption_messages(image), device)
    results = []
    for _ in range(count):
        generated = model.generate(**prefix, max_new_tokens=48, do_sample=True,
                                    temperature=.8, top_p=.95)
        results.append(processor.tokenizer.decode(generated[0, prefix["input_ids"].shape[1]:],
                                                   skip_special_tokens=True).strip())
    return results


def run_umrm(dataset_dir: Path, seed: int = 42, *, device: str = "cpu", maximum: int = 80,
             steps: int = 200, layers: list[int] | None = None, bootstrap_prompts: int = 8,
             bootstrap_candidates: int = 4, checkpoint: str = VLM_CHECKPOINT,
             checkpoint_revision: str = VLM_REVISION, checkpoint_path: Path | None = None) -> dict:
    if steps < 1 or bootstrap_candidates < 2 or bootstrap_prompts < 1:
        raise ValueError("positive training/bootstrap budget and >=2 generated candidates required")
    torch.manual_seed(seed)
    rows = load_coco(dataset_dir, maximum)
    split, protocol = group_split(rows, "id", seed)
    model, processor = load_vlm(device, checkpoint, checkpoint_revision, checkpoint_path)
    depth = model.config.text_config.num_hidden_layers
    layers = layers or sorted({max(1, depth // 3), max(1, 2 * depth // 3), depth - 1})
    if any(layer <= 0 or layer >= depth for layer in layers):
        raise ValueError("only intermediate layers can be probed")
    rng, features, operator_counts = random.Random(seed), {}, Counter()
    # Each split supplies its own negative pool. TEST is not extracted until
    # validation has frozen the selected layer and all training is complete.
    def extract_split(name, requested_layers):
        positive, negative = {l: [] for l in requested_layers}, {l: [] for l in requested_layers}
        items = split[name]
        if len(items) < 2:
            raise ValueError("each split needs two images for cross-image negatives")
        for i, row in enumerate(items):
            other = items[(i + 1) % len(items)]["caption"]
            bad, operator = caption_negative(row["caption"], other, rng)
            operator_counts[f"{name}:{operator}"] += 1
            messages = caption_messages(row["image"])
            good_features = response_features(model, processor, messages, row["caption"], requested_layers, device)
            bad_features = response_features(model, processor, messages, bad, requested_layers, device)
            for layer in requested_layers:
                positive[layer].append(good_features[layer])
                negative[layer].append(bad_features[layer])
        return {layer: (torch.stack(positive[layer]), torch.stack(negative[layer])) for layer in requested_layers}
    for name in ("train", "validation"):
        features[name] = extract_split(name, layers)
    heads, validation = {}, {}
    for layer in layers:
        heads[layer] = train_reward_head(*features["train"][layer], seed, steps)
        validation[layer] = pair_accuracy(heads[layer], *features["validation"][layer])
    selected = select_probe_layer(validation)
    last_baseline = nn.Linear(features["train"][selected][0].shape[1], 1, bias=False)
    nn.init.zeros_(last_baseline.weight)
    bootstrap_plus, bootstrap_minus, mined, abstained = [], [], 0, 0
    for row in split["train"][:bootstrap_prompts]:
        candidates = generate_candidates(model, processor, row["image"], bootstrap_candidates, device)
        allowed = set().union(*(mentioned_objects(caption) for caption in row["references"]))
        pair = mint_verified_pair(candidates, allowed)
        if pair is None:
            abstained += 1
            continue
        chosen, rejected, _, _ = pair
        messages = caption_messages(row["image"])
        bootstrap_plus.append(response_features(model, processor, messages, chosen, [selected], device)[selected])
        bootstrap_minus.append(response_features(model, processor, messages, rejected, [selected], device)[selected])
        mined += 1
    verified = None
    if mined:
        verified = train_reward_head(torch.stack(bootstrap_plus), torch.stack(bootstrap_minus), seed + 1,
                                     steps, initial=heads[selected])
    features["test"] = extract_split("test", [selected])
    test_accuracy = pair_accuracy(heads[selected], *features["test"][selected])
    baseline_accuracy = pair_accuracy(last_baseline, *features["test"][selected])
    utility = {"probe": [], "verified": [], "random": []}
    # Fresh policy samples from isolated test images; gold is used by verifier
    # AFTER generation/scoring only. Preserve negative/no-pair outcomes.
    for row in split["test"][:bootstrap_prompts]:
        candidates = generate_candidates(model, processor, row["image"], bootstrap_candidates, device)
        allowed = set().union(*(mentioned_objects(caption) for caption in row["references"]))
        nonempty = [c for c in candidates if c]
        if not nonempty:
            continue
        candidate_features = torch.stack([response_features(model, processor, caption_messages(row["image"]),
                                           c, [selected], device)[selected] for c in nonempty])
        with torch.no_grad():
            probe_index = int(heads[selected](candidate_features).argmax())
            utility["probe"].append(verifier_score(nonempty[probe_index], allowed))
            utility["random"].append(verifier_score(rng.choice(nonempty), allowed))
            if verified is not None:
                verified_index = int(verified(candidate_features).argmax())
                utility["verified"].append(verifier_score(nonempty[verified_index], allowed))
    utility_summary = {name: {"scorable_picks": len([x for x in values if x is not None]),
        "mean_caption_supported_object_score": (sum(x for x in values if x is not None) /
            len([x for x in values if x is not None])) if any(x is not None for x in values) else None}
        for name, values in utility.items()}
    return {"paper": {"key": "umrm"}, "seed": seed,
            "dataset": {"name": COCO_DATASET, "revision": COCO_REVISION,
                        "source_split": "val; local grouped diagnostic split", **protocol,
                        "offline_source_verification": recorded_verified_files(dataset_dir)
                            if (Path(dataset_dir) / "coco.jsonl").exists() else None},
            "checkpoint": {"name": checkpoint, "revision": checkpoint_revision,
                           "offline_source_verification": recorded_verified_files(checkpoint_path)},
            "evaluation_tier": "L1", "fidelity": "core_mechanism", "diagnostic_only": True,
            "baseline": {"name": "zero bias-free reward head (ties count half)", "pair_accuracy": baseline_accuracy},
            "method": {"name": "frozen intermediate response-token linear probe", "pair_accuracy": test_accuracy},
            "validation": {"pair_accuracy_by_layer": validation, "selected_layer": selected},
            "stages": {"backbone_frozen": all(not p.requires_grad for p in model.parameters()),
                       "trainable_parameters_per_head": heads[selected].weight.numel(),
                       "response_only_mean_pooling": True, "in_batch_bt_beta": .1,
                       "in_batch_bt_microbatch": 8, "steps": steps, "negative_operators": dict(operator_counts),
                       "bootstrap": {"generated_candidates_per_prompt": bootstrap_candidates,
                         "training_prompts_attempted": min(bootstrap_prompts, len(split["train"])),
                         "verified_pairs": mined, "abstained_prompts": abstained,
                         "head_retrained": verified is not None,
                         "verifier": "caption-supported COCO object lexicon (not CHAIR)",
                         "test_best_of_n": utility_summary}},
            "scope": "真实冻结 VLM 中间层 reward probing；验证集选层、test 隔离、独立 verifier 对 policy 自生成候选挖 pair。小型 caption-supported verifier 非官方 CHAIR；未复刻Qwen3-VL32B、图像生成、DPO或原论文reward benchmarks。"}
