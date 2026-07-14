from __future__ import annotations

import random
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..llm_rec_data import TextCTRData, binary_auc


@dataclass(frozen=True)
class KARConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"
    dimensions: int = 48
    experts: int = 4
    maximum_users: int = 80
    batch_size: int = 64
    steps: int = 120
    learning_rate: float = 8e-4
    maximum_train: int = 5000
    maximum_test: int = 1000


def require_backend():
    try:
        import torch
        from torch import nn
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("KAR requires `pip install -e '.[plum]'`.") from exc
    return torch, nn, AutoModelForCausalLM, AutoTokenizer


def build_knowledge(
    data: TextCTRData, root: Path, config: KARConfig
) -> tuple[np.ndarray, np.ndarray, dict[str, int]]:
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_backend()
    slug = config.model_name.rsplit("/", 1)[-1].lower()
    cache = root / "kar" / f"{slug}-u{config.maximum_users}.npz"
    if cache.exists():
        payload = np.load(cache)
        return payload["users"], payload["items"], {"generated_prompts": int(payload["generated_prompts"])}
    needed_users = sorted({row.user for row in (*data.train, *data.test)})
    needed_items = sorted(
        {row.candidate for row in (*data.train, *data.test)}
        | {item for row in (*data.train, *data.test) for item in row.history[-8:]}
    )
    latest_history: dict[int, tuple[int, ...]] = {}
    for row in data.train:
        latest_history[row.user] = row.history
    user_prompts = [
        "Infer this user's durable movie preferences in one short sentence. History: "
        + "; ".join(data.titles[item] for item in latest_history[user][-8:])
        for user in needed_users
    ]
    item_prompts = [
        "State useful factual recommendation knowledge about this movie in one short sentence: "
        + data.titles[item] + ". Genres: " + ", ".join(data.genres[item])
        for item in needed_items
    ]
    tokenizer = AutoTokenizer.from_pretrained(config.model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(config.model_name)
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).eval()
    generated = _generate(model, tokenizer, [*user_prompts, *item_prompts], device, torch)
    vectors = _encode(model, tokenizer, generated, device, torch)
    hidden = vectors.shape[1]
    users = np.zeros((data.users, hidden), dtype=np.float32)
    items = np.zeros((len(data.titles), hidden), dtype=np.float32)
    for index, user in enumerate(needed_users):
        users[user] = vectors[index]
    offset = len(needed_users)
    for index, item in enumerate(needed_items):
        items[item] = vectors[offset + index]
    cache.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(cache, users=users, items=items, generated_prompts=len(generated))
    return users, items, {"generated_prompts": len(generated)}


def _generate(model, tokenizer, prompts, device, torch):
    texts = []
    with torch.inference_mode():
        for start in range(0, len(prompts), 16):
            batch = prompts[start:start + 16]
            encoded = tokenizer(batch, padding=True, truncation=True, max_length=96, return_tensors="pt").to(device)
            outputs = model.generate(
                **encoded, max_new_tokens=24, do_sample=False,
                pad_token_id=tokenizer.pad_token_id,
            )
            new_tokens = outputs[:, encoded["input_ids"].shape[1]:]
            decoded = tokenizer.batch_decode(new_tokens, skip_special_tokens=True)
            texts.extend(text if text.strip() else prompt for text, prompt in zip(decoded, batch))
    return texts


def _encode(model, tokenizer, texts, device, torch):
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(texts), 32):
            encoded = tokenizer(texts[start:start + 32], padding=True, truncation=True, max_length=64, return_tensors="pt").to(device)
            output = model(**encoded, output_hidden_states=True, return_dict=True)
            hidden = output.hidden_states[-1]
            weights = encoded["attention_mask"].unsqueeze(-1)
            pooled = (hidden * weights).sum(1) / weights.sum(1).clamp_min(1)
            vectors.append(pooled.cpu().float().numpy())
    return np.concatenate(vectors).astype(np.float32)


def build_ranker(data, user_knowledge, item_knowledge, config: KARConfig, use_knowledge: bool):
    torch, nn, _, _ = require_backend()
    knowledge_dimensions = user_knowledge.shape[1]

    class HybridExpert(nn.Module):
        def __init__(self):
            super().__init__()
            self.experts = nn.ModuleList(
                nn.Sequential(nn.Linear(knowledge_dimensions, 2 * config.dimensions), nn.GELU(), nn.Linear(2 * config.dimensions, config.dimensions))
                for _ in range(config.experts)
            )
            self.gate = nn.Linear(config.dimensions, config.experts)

        def forward(self, knowledge, identity):
            weights = torch.softmax(self.gate(identity), dim=-1)
            values = torch.stack([expert(knowledge) for expert in self.experts], dim=1)
            return (values * weights.unsqueeze(-1)).sum(1)

    class KARRanker(nn.Module):
        def __init__(self):
            super().__init__()
            self.user = nn.Embedding(data.users, config.dimensions)
            self.item = nn.Embedding(len(data.titles), config.dimensions)
            self.register_buffer("user_knowledge", torch.tensor(user_knowledge))
            self.register_buffer("item_knowledge", torch.tensor(item_knowledge))
            self.user_adapter = HybridExpert()
            self.item_adapter = HybridExpert()
            if not use_knowledge:
                for parameter in (*self.user_adapter.parameters(), *self.item_adapter.parameters()):
                    parameter.requires_grad = False
            self.score = nn.Sequential(
                nn.Linear(3 * config.dimensions, 2 * config.dimensions), nn.GELU(),
                nn.Linear(2 * config.dimensions, 1),
            )

        def forward(self, users, items):
            user = self.user(users)
            item = self.item(items)
            if use_knowledge:
                user = user + self.user_adapter(self.user_knowledge[users], user)
                item = item + self.item_adapter(self.item_knowledge[items], item)
            return self.score(torch.cat((user, item, user * item), dim=-1)).squeeze(-1)

    return KARRanker()


def train_and_evaluate(model, train, test, config: KARConfig, seed: int):
    torch, _, _, _ = require_backend()
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device).train()
    parameters = [value for value in model.parameters() if value.requires_grad]
    optimizer = torch.optim.AdamW(parameters, lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(config.steps):
        batch = [train[rng.randrange(len(train))] for _ in range(config.batch_size)]
        users = torch.tensor([row.user for row in batch], device=device)
        items = torch.tensor([row.candidate for row in batch], device=device)
        labels = torch.tensor([row.label for row in batch], device=device, dtype=torch.float32)
        loss = torch.nn.functional.binary_cross_entropy_with_logits(model(users, items), labels)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(parameters, 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    labels, scores = [], []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(test), config.batch_size):
            batch = test[start:start + config.batch_size]
            users = torch.tensor([row.user for row in batch], device=device)
            items = torch.tensor([row.candidate for row in batch], device=device)
            scores.extend(torch.sigmoid(model(users, items)).cpu().tolist())
            labels.extend(row.label for row in batch)
    return {
        "auc": binary_auc(labels, scores), "examples": len(test),
        "initial_loss": float(np.mean(losses[:20])), "final_loss": float(np.mean(losses[-20:])),
        "seconds": time.perf_counter() - started,
        "trainable_parameters": sum(value.numel() for value in parameters), "device": device.type,
    }
