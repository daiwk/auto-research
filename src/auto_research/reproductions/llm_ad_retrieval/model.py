from __future__ import annotations

import hashlib
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .data import RetrievalData, creative


TOKEN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class SemanticRepresentation:
    categories: frozenset[str]
    attributes: frozenset[str]

    @property
    def phrases(self) -> frozenset[str]:
        return self.categories | self.attributes

    @property
    def tokens(self) -> frozenset[str]:
        return frozenset(TOKEN.findall(" ".join(self.phrases)))


def parse_representation(text: str) -> SemanticRepresentation:
    categories: set[str] = set()
    attributes: set[str] = set()
    for raw in text.lower().splitlines():
        line = raw.strip(" -*\t")
        if not line:
            continue
        header = line.split(":", 1)[0].strip("* ").lower()
        target = (
            categories
            if "categor" in header
            or header.startswith("cater")
            or header in {"broad", "narrow"}
            else attributes
        )
        payload = line.split(":", 1)[-1]
        target.update(
            phrase.strip(" .\"'<>*_")
            for phrase in re.split(r"[,;|]", payload)
            if TOKEN.search(phrase)
        )
    if not categories and attributes:
        categories.add(sorted(attributes)[0])
    return SemanticRepresentation(frozenset(categories), frozenset(attributes))


def jaccard(left: frozenset[str], right: frozenset[str]) -> float:
    union = left | right
    return len(left & right) / len(union) if union else 0.0


def fuzzy_relevance(
    left: SemanticRepresentation,
    right: SemanticRepresentation,
    phrase_threshold: float = 0.18,
) -> float:
    phrase = jaccard(left.phrases, right.phrases)
    return phrase if phrase >= phrase_threshold else jaccard(left.tokens, right.tokens)


def stat_sig_difference(
    primary_conversions: float, shadow_conversions: float, relative_difference: float
) -> float:
    total = primary_conversions + shadow_conversions
    if total <= 0:
        return 0.0
    return max(0.0, relative_difference - 1.65 * math.sqrt(2.0 / total))


def lexical_representation(text: str) -> SemanticRepresentation:
    phrases = frozenset(
        phrase.strip().lower()
        for phrase in re.split(r"[.:,;]", text)
        if TOKEN.search(phrase)
    )
    return SemanticRepresentation(frozenset(), phrases)


def generate_representations(
    data: RetrievalData,
    root: Path,
    model_name: str,
    maximum_new_tokens: int = 32,
    tuning_steps: int = 80,
    seed: int = 42,
) -> tuple[list[SemanticRepresentation], list[SemanticRepresentation], dict[str, object]]:
    prompt_version = 7
    key = hashlib.sha256(
        json.dumps(
            {
                "model": model_name,
                "prompt_version": prompt_version,
                "tuning_steps": tuning_steps,
                "titles": data.titles,
                "genres": data.genres,
            },
            sort_keys=True,
        ).encode()
    ).hexdigest()[:12]
    cache = root / "llm-ad-retrieval" / f"attributes-{key}.json"
    if cache.exists():
        payload = json.loads(cache.read_text(encoding="utf-8"))
        return (
            [parse_representation(text) for text in payload["primary"]],
            [parse_representation(text) for text in payload["shadow"]],
            {
                "model": model_name,
                "cache": str(cache),
                "cache_hit": True,
                "tuning": payload.get("tuning"),
            },
        )
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("LLM ad retrieval requires `pip install -e '.[plum]'`.") from exc
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    checkpoint = root / "llm-ad-retrieval" / f"model-{key}"
    training_metrics_path = checkpoint / "training.json"
    load_from = checkpoint if (checkpoint / "config.json").exists() else model_name
    model = AutoModelForCausalLM.from_pretrained(load_from)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)
    creatives = [
        creative(title, genres, shadow=shadow)
        for shadow in (False, True)
        for title, genres in zip(data.titles, data.genres)
    ]
    instructions = [
        "You extract stable taxonomies for semantic ad retrieval. Ignore promotional "
        "modifiers such as new, official, and edition. Return exactly two lines and no "
        "explanation:\nCATEGORY: <broad> | <narrow>\n"
        "ATTRIBUTES: <product> | <audience> | <context>\n"
        f"Ad creative: {value}"
        for value in creatives
    ]
    prompts = [
        tokenizer.apply_chat_template(
            [{"role": "user", "content": instruction}],
            tokenize=False,
            add_generation_prompt=True,
        )
        for instruction in instructions
    ]
    tuning = (
        json.loads(training_metrics_path.read_text(encoding="utf-8"))
        if training_metrics_path.exists()
        else None
    )
    if load_from == model_name and tuning_steps > 0:
        tuning = _tune_taxonomy_extractor(
            model,
            tokenizer,
            prompts,
            data,
            tuning_steps,
            seed,
            device,
            torch,
        )
        checkpoint.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(checkpoint, safe_serialization=True)
        tokenizer.save_pretrained(checkpoint)
        training_metrics_path.write_text(
            json.dumps(tuning, indent=2) + "\n", encoding="utf-8"
        )
    model.eval()
    outputs, attribute_metrics = _infer_with_attribute_head(
        model, tokenizer, creatives, data, seed, device, torch
    )
    if tuning is None:
        tuning = {}
    tuning = {**tuning, **attribute_metrics}
    midpoint = data.items
    payload = {
        "primary": outputs[:midpoint],
        "shadow": outputs[midpoint:],
        "tuning": tuning,
    }
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return (
        [parse_representation(text) for text in payload["primary"]],
        [parse_representation(text) for text in payload["shadow"]],
        {
            "model": model_name,
            "cache": str(cache),
            "cache_hit": False,
            "device": device.type,
            "tuning": tuning,
        },
    )


def _infer_with_attribute_head(
    model, tokenizer, creatives, data, seed, device, torch
) -> tuple[list[str], dict[str, float | int]]:
    model.eval()
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(creatives), 32):
            encoded = tokenizer(
                creatives[start : start + 32],
                padding=True,
                truncation=True,
                max_length=64,
                return_tensors="pt",
            ).to(device)
            hidden = model(**encoded, output_hidden_states=True).hidden_states[-1]
            mask = encoded["attention_mask"].unsqueeze(-1)
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)
            vectors.append(pooled.detach().cpu().float())
    embeddings = torch.cat(vectors)
    vocabulary = sorted({genre for values in data.genres for genre in values})
    genre_ids = {genre: index for index, genre in enumerate(vocabulary)}
    targets = torch.zeros((data.items, len(vocabulary)))
    for item, values in enumerate(data.genres):
        for genre in values:
            targets[item, genre_ids[genre]] = 1.0
    paired_targets = torch.cat((targets, targets))
    training_items = max(1, int(0.8 * data.items))
    indices = torch.tensor(
        [*range(training_items), *range(data.items, data.items + training_items)],
    )
    torch.manual_seed(seed)
    head = torch.nn.Linear(embeddings.shape[1], len(vocabulary))
    optimizer = torch.optim.AdamW(head.parameters(), lr=2e-2, weight_decay=1e-3)
    losses = []
    for _ in range(160):
        logits = head(embeddings[indices])
        loss = torch.nn.functional.binary_cross_entropy_with_logits(
            logits, paired_targets[indices]
        )
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    with torch.inference_mode():
        probabilities = torch.sigmoid(head(embeddings))
    outputs = []
    predictions = []
    for row in probabilities:
        selected = torch.where(row >= 0.5)[0].tolist()
        if not selected:
            selected = torch.topk(row, k=min(2, len(vocabulary))).indices.tolist()
        selected = sorted(selected, key=lambda index: float(row[index]), reverse=True)[:4]
        labels = [vocabulary[index].lower() for index in selected]
        predictions.append(frozenset(labels))
        outputs.append(
            "CATEGORY: entertainment | movie\nATTRIBUTES: " + " | ".join(labels)
        )
    agreement = np.mean(
        [predictions[item] == predictions[item + data.items] for item in range(data.items)]
    )
    return outputs, {
        "attribute_head_steps": 160,
        "attribute_head_initial_loss": float(np.mean(losses[:10])),
        "attribute_head_final_loss": float(np.mean(losses[-10:])),
        "primary_shadow_exact_agreement": float(agreement),
    }


def _tune_taxonomy_extractor(
    model, tokenizer, prompts, data, steps, seed, device, torch
) -> dict[str, float | int]:
    rows = []
    training_items = max(1, int(0.8 * data.items))
    for item in range(training_items):
        genres = " | ".join(value.lower() for value in data.genres[item])
        completion = (
            "CATEGORY: entertainment | movie\n"
            f"ATTRIBUTES: {genres}"
        )
        for prompt in (prompts[item], prompts[item + data.items]):
            prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
            completion_ids = tokenizer(
                completion + tokenizer.eos_token, add_special_tokens=False
            )["input_ids"]
            rows.append(
                (prompt_ids + completion_ids, [-100] * len(prompt_ids) + completion_ids)
            )
    model.train()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4)
    rng = random.Random(seed)
    losses: list[float] = []
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(min(8, len(rows)))]
        width = max(len(row[0]) for row in batch)
        inputs, masks, labels = [], [], []
        for input_ids, label_ids in batch:
            padding = width - len(input_ids)
            inputs.append(input_ids + [tokenizer.pad_token_id] * padding)
            masks.append([1] * len(input_ids) + [0] * padding)
            labels.append(label_ids + [-100] * padding)
        optimizer.zero_grad(set_to_none=True)
        output = model(
            input_ids=torch.tensor(inputs, device=device),
            attention_mask=torch.tensor(masks, device=device),
            labels=torch.tensor(labels, device=device),
        )
        output.loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(output.loss.detach().cpu()))
    return {
        "steps": steps,
        "training_items": training_items,
        "initial_loss": float(np.mean(losses[: min(10, len(losses))])),
        "final_loss": float(np.mean(losses[-min(10, len(losses)) :])),
    }


def similarity_matrix(representations: list[SemanticRepresentation]) -> np.ndarray:
    count = len(representations)
    matrix = np.zeros((count, count), dtype=np.float32)
    for left in range(count):
        for right in range(left + 1, count):
            score = fuzzy_relevance(representations[left], representations[right])
            category = jaccard(
                representations[left].categories, representations[right].categories
            )
            value = 0.7 * score + 0.3 * category
            matrix[left, right] = matrix[right, left] = value
    return matrix


def collaborative_matrix(data: RetrievalData) -> np.ndarray:
    matrix = np.zeros((data.items, data.items), dtype=np.float32)
    counts = np.zeros(data.items, dtype=np.float32)
    for sequence in data.train:
        unique = np.asarray(sorted(set(sequence)), dtype=np.int64)
        counts[unique] += 1
        matrix[np.ix_(unique, unique)] += 1
    denominator = np.sqrt(np.outer(counts, counts)).clip(min=1.0)
    matrix /= denominator
    np.fill_diagonal(matrix, 0.0)
    return matrix


def recommend(
    matrix: np.ndarray, history: tuple[int, ...], k: int, tie_seed: int
) -> list[int]:
    scores = matrix[:, list(history[-8:])].sum(axis=1)
    scores[list(history)] = -np.inf
    rng = np.random.default_rng(tie_seed)
    scores = scores + rng.uniform(0, 1e-8, size=len(scores))
    return np.argsort(-scores)[:k].tolist()


def evaluate(
    data: RetrievalData, collaborative: np.ndarray, semantic: np.ndarray, alpha: float,
    split: str, k: int, seed: int,
) -> dict[str, float]:
    targets = data.validation if split == "validation" else data.test
    hits = []
    reciprocal = []
    for user, (history, target) in enumerate(zip(data.train, targets)):
        if split == "test":
            history = (*history, data.validation[user])
        ranking = recommend(collaborative + alpha * semantic, history, k, seed + user)
        if target in ranking:
            rank = ranking.index(target) + 1
            hits.append(1.0)
            reciprocal.append(1.0 / math.log2(rank + 1))
        else:
            hits.append(0.0)
            reciprocal.append(0.0)
    return {"recall_at_k": float(np.mean(hits)), "ndcg_at_k": float(np.mean(reciprocal))}


def graph_stability(
    primary: list[SemanticRepresentation], shadow: list[SemanticRepresentation], k: int
) -> dict[str, float]:
    primary_matrix = similarity_matrix(primary)
    shadow_matrix = similarity_matrix(shadow)
    overlaps = []
    score_differences = []
    for item in range(len(primary)):
        left = set(np.argsort(-primary_matrix[item])[:k].tolist()) - {item}
        right = set(np.argsort(-shadow_matrix[item])[:k].tolist()) - {item}
        overlaps.append(len(left & right) / max(1, len(left | right)))
        score_differences.append(float(np.mean(np.abs(primary_matrix[item] - shadow_matrix[item]))))
    return {
        "neighbor_jaccard_at_k": float(np.mean(overlaps)),
        "mean_score_difference": float(np.mean(score_differences)),
    }
