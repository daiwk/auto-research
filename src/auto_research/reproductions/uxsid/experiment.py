"""Real semantic encoding and chronological public-data UxSID training.

MovieLens replaces private advertising data. It cannot reproduce KuaiRec-Big
long-history conclusions, CTR/CTCVR or the production A/B result.
"""
from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path

import numpy as np
import torch
from torch.nn import functional as F

from auto_research.datasets import MOVIELENS_SHA256, MOVIELENS_URL, movielens_100k
from auto_research.oct12_public_sources import checkpoint_source
from auto_research.reproductions.forte.experiment import binary_metrics, parameter_digest
from .model import ResidualKmeansFSQ, SemanticMemoryCache, UxSID, objective

ENCODER_ID = "Qwen/Qwen2.5-0.5B-Instruct"
ENCODER_REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"


def chronological_data(root: Path, *, max_users=None, max_history=256):
    if max_history < 1:
        raise ValueError("history budget must be positive")
    histories = defaultdict(list)
    for row in movielens_100k(root):
        histories[row[0]].append(row)
    selected = sorted(histories)[:max_users]
    splits = {name: [] for name in ("train", "validation", "test")}
    for user in selected:
        events = sorted(histories[user], key=lambda r: (r[3], r[1]))
        if len(events) < 4:
            continue
        previous = []
        for index, (_, item, rating, timestamp) in enumerate(events):
            if previous:
                split = "test" if index == len(events) - 1 else "validation" if index == len(events) - 2 else "train"
                splits[split].append({"user": user, "item": item, "label": float(rating >= 4),
                                      "timestamp": timestamp, "history": previous[-max_history:]})
            previous = previous + [item]
    train_times = [r["timestamp"] for r in splits["train"]]
    if not train_times:
        raise ValueError("public data produced no training history")
    low, high = min(train_times), max(train_times)
    for rows in splits.values():
        for row in rows:
            row["context"] = (row["timestamp"] - low) / max(1, high - low)
    source = root / "ml-100k/u.data"
    metadata = {"public_id": "MovieLens-100K", "revision": MOVIELENS_SHA256,
                "source": MOVIELENS_URL, "ratings_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "split": "per-user chronological leave-last-two; all observed earlier ratings form history",
                "target": "observed rating >=4, not private advertising CTR/CTCVR",
                "max_users": max_users, "max_history": max_history,
                "counts": {name: len(rows) for name, rows in splits.items()},
                "split_sha256": {name: hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
                                 for name, rows in splits.items()}}
    return splits, metadata


def public_item_texts(root: Path):
    genres = [row.split("|")[0] for row in (root / "ml-100k/u.genre").read_text().splitlines() if row]
    records = {}
    for line in (root / "ml-100k/u.item").read_text(encoding="latin-1").splitlines():
        row = line.split("|")
        categories = [genre for genre, active in zip(genres, row[5:]) if active == "1"]
        records[int(row[0])] = f"Movie: {row[1]}. Genres: {', '.join(categories)}."
    return records


def encode_attributes(texts, *, encoder_id=ENCODER_ID, encoder_revision=ENCODER_REVISION,
                      encoder_path=None, device="cpu", batch_size=32):
    from transformers import AutoModel, AutoTokenizer

    source, kwargs, provenance = checkpoint_source(encoder_id, encoder_revision, encoder_path)
    tokenizer = AutoTokenizer.from_pretrained(source, trust_remote_code=False, **kwargs)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModel.from_pretrained(source, trust_remote_code=False,
                                     torch_dtype=torch.float32 if device == "cpu" else torch.bfloat16,
                                     attn_implementation="eager", **kwargs).to(device).eval()
    model.requires_grad_(False)
    identities = sorted(texts)
    vectors = []
    with torch.no_grad():
        for offset in range(0, len(identities), batch_size):
            batch = tokenizer([texts[item] for item in identities[offset:offset + batch_size]],
                              return_tensors="pt", padding=True, truncation=True, max_length=128).to(device)
            hidden = model(**batch, use_cache=False).last_hidden_state.float()
            # Attribute-only frozen encoder. No interaction or target labels.
            pooled = (hidden * batch.attention_mask[..., None]).sum(1) / batch.attention_mask.sum(1, keepdim=True)
            vectors.append(F.normalize(pooled, dim=-1).cpu())
    del model
    if device.startswith("cuda"):
        torch.cuda.empty_cache()
    matrix = torch.cat(vectors)
    return identities, matrix, {"public_id": encoder_id, "revision": encoder_revision,
                                "verified_mirror": provenance,
                                "attributes_sha256": hashlib.sha256(json.dumps(texts, sort_keys=True).encode()).hexdigest(),
                                "embedding_sha256": hashlib.sha256(matrix.numpy().tobytes()).hexdigest(),
                                "pooling": "attention-mask mean of final hidden state; no labels",
                                "modality": "public movie title + genre text; no private video frames"}


def _batch(rows, sid_by_item, *, device, max_history):
    history = torch.zeros((len(rows), max_history), dtype=torch.long)
    for index, row in enumerate(rows):
        values = row["history"][-max_history:]
        history[index, -len(values):] = torch.tensor(values)
    tensors = {"users": torch.tensor([r["user"] for r in rows]),
               "targets": torch.tensor([r["item"] for r in rows]),
               "history_ids": history, "valid": history > 0,
               "context": torch.tensor([r["context"] for r in rows], dtype=torch.float32),
               "sid_ids": torch.tensor([sid_by_item[r["item"]] for r in rows])}
    labels = torch.tensor([r["label"] for r in rows])
    return {key: value.to(device) for key, value in tensors.items()}, labels.to(device)


def _evaluate(model, rows, sid_by_item, *, device, batch_size, max_history):
    model.eval()
    labels, probabilities = [], []
    with torch.no_grad():
        for offset in range(0, len(rows), batch_size):
            features, targets = _batch(rows[offset:offset + batch_size], sid_by_item,
                                      device=device, max_history=max_history)
            logits, _ = model(**features)
            labels.extend(targets.cpu().tolist())
            probabilities.extend(logits.sigmoid().cpu().tolist())
    return {**binary_metrics(np.array(labels), np.array(probabilities)), "examples": len(labels)}


def run_uxsid(root: Path, seed: int, *, device="cpu", encoder_path=None,
              encoder_id=ENCODER_ID, encoder_revision=ENCODER_REVISION,
              epochs=3, batch_size=256, dimension=32, anchors=8, codebook_size=64,
              max_users=None, max_history=256, learning_rate=1e-3):
    if min(epochs, batch_size, dimension, anchors) < 1:
        raise ValueError("positive training budget required")
    if device.startswith("cuda") and not torch.cuda.is_available():
        raise RuntimeError("requested CUDA unavailable; no implicit CPU validation fallback")
    torch.manual_seed(seed)
    splits, data = chronological_data(root, max_users=max_users, max_history=max_history)
    identities, vectors, encoder = encode_attributes(public_item_texts(root), encoder_id=encoder_id,
                                                     encoder_revision=encoder_revision,
                                                     encoder_path=encoder_path, device=device)
    train_items = set(r["item"] for r in splits["train"])
    train_indices = [i for i, item in enumerate(identities) if item in train_items]
    quantizer = ResidualKmeansFSQ(codebook_size=codebook_size).fit(vectors[train_indices], seed=seed)
    quantized = quantizer.encode(vectors)
    sid_by_item = dict(zip(identities, quantized.first_ids.tolist()))
    shape = dict(items=max(identities) + 1, users=max(r["user"] for r in splits["train"]) + 1,
                 sid_count=codebook_size, dimension=dimension, anchors=anchors)
    torch.manual_seed(seed)
    initial = UxSID(**shape).state_dict()
    results = {}
    models = {}
    for variant in ("global-only", "agnostic", "ungated", "uxsid"):
        torch.manual_seed(seed)
        model = UxSID(**shape, variant=variant).to(device)
        model.load_state_dict(initial)
        before = parameter_digest(model)
        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        rng = np.random.default_rng(seed)
        best_auc, best_state, history = -float("inf"), None, []
        for epoch in range(epochs):
            model.train()
            order = rng.permutation(len(splits["train"]))
            losses = []
            for offset in range(0, len(order), batch_size):
                rows = [splits["train"][int(i)] for i in order[offset:offset + batch_size]]
                features, labels = _batch(rows, sid_by_item, device=device, max_history=max_history)
                optimizer.zero_grad(set_to_none=True)
                logits, regularizer = model(**features)
                loss = objective(logits, labels, regularizer)
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.)
                optimizer.step()
                losses.append(float(loss.detach()))
            validation = _evaluate(model, splits["validation"], sid_by_item, device=device,
                                   batch_size=batch_size, max_history=max_history)
            history.append({"epoch": epoch + 1, "train_loss": float(np.mean(losses)), "validation": validation})
            if validation["roc_auc"] > best_auc:
                best_auc = validation["roc_auc"]
                best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
        model.load_state_dict(best_state)
        model.eval()
        results[variant] = {"training": history, "selected_validation_auc": best_auc,
                            "parameters_changed": before != parameter_digest(model)}
        models[variant] = model
    selected = max(results, key=lambda variant: results[variant]["selected_validation_auc"])
    # No test labels were read during variant/epoch selection.
    for variant, model in models.items():
        results[variant]["test"] = _evaluate(model, splits["test"], sid_by_item, device=device,
                                             batch_size=batch_size, max_history=max_history)
    example, _ = _batch(splits["test"][:1], sid_by_item, device=device, max_history=max_history)
    model = models["uxsid"]
    cache = SemanticMemoryCache()
    cached = cache.get(model, user=example["users"][0], sid=example["sid_ids"][0],
                       history_ids=example["history_ids"], valid=example["valid"], model_revision=parameter_digest(model))
    direct = model.memory(example["history_ids"], example["valid"], example["sid_ids"])[0]
    return {"method": "uxsid", "seed": seed, "device": device, "diagnostic_only": True,
            "evaluation_tier": "l2_public_dataset", "dataset": data, "checkpoint": encoder,
            "protocol": {"epochs": epochs, "batch_size": batch_size, "dimension": dimension,
                         "anchors": anchors, "learning_rate": learning_rate,
                         "semantic_quantizer_fit": "training item attributes only",
                         "hybrid_quantizer": "2 residual k-means stages + 7-level scalar residual",
                         "label_access_in_encoder": False, "test_selection": False},
            "quantization": {"mse": quantized.reconstruction_mse,
                             "occupied_first_codes": len(set(sid_by_item.values()))},
            "variants": results, "validation_selected_variant": selected,
            "cache": {"offline_online_max_abs_error": float((cached - direct).detach().abs().max()),
                      "target_item_free_memory": True,
                      "production_latency_measured": False},
            "limitations": ["MovieLens observed-rating diagnostic, not KuaiRec-Big/XLong or production CTR.",
                            "Public text-only frozen encoder replaces private multimodal semantic attributes.",
                            "No production KV server, ultra-long-history scaling or online A/B measured."]}


def render(result):
    lines = ["# UxSID 公开数据结构诊断", "", "仅验证公开评分预测和语义分组记忆，不验证原论文线上收益。", "",
             "| 结构 | Validation AUC | Test AUC | Test PR-AUC |", "| --- | ---: | ---: | ---: |"]
    for variant, row in result["variants"].items():
        lines.append(f"| {variant} | {row['selected_validation_auc']:.6f} | {row['test']['roc_auc']:.6f} | {row['test']['pr_auc']:.6f} |")
    lines.extend(["", f"仅由 validation 选择：{result['validation_selected_variant']}。",
                  f"缓存/直接计算最大误差：{result['cache']['offline_online_max_abs_error']:.3g}。", ""])
    return "\n".join(lines)
