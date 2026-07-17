from __future__ import annotations

from auto_research.runtime import device_for

import random
import time

import numpy as np

from ..llm_lora import inject_lora, require_llm_backend


def train_llm_semantics(data, model_name: str, item_steps: int, user_steps: int, seed: int):
    torch, nn, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    trainable = inject_lora(model, rank=4, alpha=8.0)
    device = device_for(torch)
    model.to(device)
    item_texts = [
        f"Item: {title}. Categories: {', '.join(genres)}"
        for title, genres in zip(data.titles, data.genres)
    ]
    cooccurrences = [
        (left, right)
        for sequence in data.sequences
        for left, right in zip(sequence[:-2], sequence[1:-1])
    ]
    rng = random.Random(seed)
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=5e-4)
    item_losses = []
    started = time.perf_counter()
    model.train()
    for _ in range(item_steps):
        pairs = [cooccurrences[rng.randrange(len(cooccurrences))] for _ in range(8)]
        left = _encode(model, tokenizer, [item_texts[a] for a, _ in pairs], device, torch, grad=True)
        right = _encode(model, tokenizer, [item_texts[b] for _, b in pairs], device, torch, grad=True)
        logits = torch.nn.functional.normalize(left, dim=-1) @ torch.nn.functional.normalize(right, dim=-1).T / 0.07
        labels = torch.arange(len(pairs), device=device)
        loss = (torch.nn.functional.cross_entropy(logits, labels) + torch.nn.functional.cross_entropy(logits.T, labels)) / 2
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        optimizer.step()
        item_losses.append(float(loss.detach().cpu()))
    item_vectors = _encode_batches(model, tokenizer, item_texts, device, torch)
    category_count = max(2, len({genres[0] if genres else "unknown" for genres in data.genres}))
    category_names = {name: index for index, name in enumerate(sorted({genres[0] if genres else "unknown" for genres in data.genres}))}
    category_head = nn.Linear(item_vectors.shape[1], category_count).to(device)
    optimizer = torch.optim.AdamW(
        [p for p in model.parameters() if p.requires_grad] + list(category_head.parameters()), lr=3e-4
    )
    user_prompts = []
    for sequence in data.sequences:
        history = "; ".join(data.titles[item] for item in sequence[-8:-2])
        user_prompts.append(f"User history: {history}. Future interest:")
    user_losses = []
    target_items = [sequence[-2] for sequence in data.sequences]
    for _ in range(user_steps):
        indices = [rng.randrange(data.user_count) for _ in range(8)]
        states = _encode(model, tokenizer, [user_prompts[i] for i in indices], device, torch, grad=True)
        targets = torch.tensor(item_vectors[[target_items[i] for i in indices]], device=device)
        categories = torch.tensor(
            [category_names[data.genres[target_items[i]][0] if data.genres[target_items[i]] else "unknown"] for i in indices],
            device=device,
        )
        alignment = 1.0 - torch.nn.functional.cosine_similarity(states, targets).mean()
        category = torch.nn.functional.cross_entropy(category_head(states), categories)
        loss = alignment + category
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(
            [p for p in model.parameters() if p.requires_grad] + list(category_head.parameters()), 1.0
        )
        optimizer.step()
        user_losses.append(float(loss.detach().cpu()))
    item_vectors = _encode_batches(model, tokenizer, item_texts, device, torch)
    user_vectors = _encode_batches(model, tokenizer, user_prompts, device, torch)
    item_codes, item_rqvae = train_rqvae(item_vectors, 3, 16, 100, seed)
    user_codes, user_rqvae = train_rqvae(user_vectors, 2, 16, 100, seed + 17)
    return item_vectors, user_vectors, item_codes, user_codes, {
        "model": model_name,
        "lora_trainable_parameters": trainable,
        "item_contrastive_initial": _edge(item_losses, True),
        "item_contrastive_final": _edge(item_losses, False),
        "user_supervision_initial": _edge(user_losses, True),
        "user_supervision_final": _edge(user_losses, False),
        "seconds": time.perf_counter() - started,
        "device": device.type,
        "item_rqvae": item_rqvae,
        "user_rqvae": user_rqvae,
    }


def train_rqvae(features, levels: int, codebook_size: int, steps: int, seed: int):
    torch, nn, _, _ = require_llm_backend()
    torch.manual_seed(seed)
    device = device_for(torch)
    normalized = np.asarray(features, dtype=np.float32)
    normalized = normalized / np.maximum(
        np.linalg.norm(normalized, axis=1, keepdims=True), 1e-6
    )
    values = torch.tensor(normalized, dtype=torch.float32, device=device)
    latent_size = 48

    class RQVAE(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = nn.Sequential(
                nn.Linear(features.shape[1], 128), nn.GELU(), nn.Linear(128, latent_size)
            )
            self.decoder = nn.Sequential(
                nn.Linear(latent_size, 128), nn.GELU(), nn.Linear(128, features.shape[1])
            )
            self.codebooks = nn.ParameterList(
                [nn.Parameter(torch.randn(codebook_size, latent_size) * 0.02) for _ in range(levels)]
            )

        def quantize(self, latent):
            residual = latent
            quantized = torch.zeros_like(latent)
            losses, codes = [], []
            for codebook in self.codebooks:
                distances = torch.cdist(residual, codebook)
                code = distances.argmin(-1)
                selected = codebook[code]
                usage = torch.softmax(-distances / 0.1, dim=-1).mean(dim=0)
                losses.append(
                    torch.nn.functional.mse_loss(selected, residual.detach())
                    + 0.25 * torch.nn.functional.mse_loss(selected.detach(), residual)
                    + 0.001 * (usage * usage.clamp_min(1e-8).log()).sum()
                )
                quantized = quantized + selected
                residual = residual - selected
                codes.append(code)
            straight_through = latent + (quantized - latent).detach()
            return straight_through, torch.stack(losses).sum(), torch.stack(codes, dim=1)

    model = RQVAE().to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)
    rng = random.Random(seed)
    pretrain_losses = []
    model.train()
    for _ in range(40):
        indices = [rng.randrange(len(values)) for _ in range(min(256, len(values)))]
        batch = values[indices]
        reconstruction = torch.nn.functional.mse_loss(
            model.decoder(model.encoder(batch)), batch
        )
        optimizer.zero_grad(set_to_none=True)
        reconstruction.backward()
        optimizer.step()
        pretrain_losses.append(float(reconstruction.detach().cpu()))
    _initialize_codebooks(model, values, seed, torch)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4)
    losses = []
    for _ in range(steps):
        indices = [rng.randrange(len(values)) for _ in range(min(256, len(values)))]
        batch = values[indices]
        latent = model.encoder(batch)
        quantized, rq_loss, _ = model.quantize(latent)
        reconstruction = torch.nn.functional.mse_loss(model.decoder(quantized), batch)
        loss = reconstruction + rq_loss
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    model.eval()
    with torch.inference_mode():
        _, _, codes = model.quantize(model.encoder(values))
    encoded = codes.cpu().numpy().astype(np.int64)
    return encoded, {
        "levels": levels,
        "codebook_size": codebook_size,
        "steps": steps,
        "autoencoder_pretrain_steps": 40,
        "autoencoder_final_loss": _edge(pretrain_losses, False),
        "initial_loss": _edge(losses, True),
        "final_loss": _edge(losses, False),
        "unique_codes": len({tuple(row) for row in encoded.tolist()}),
    }


def _initialize_codebooks(model, values, seed, torch):
    with torch.no_grad():
        residual = model.encoder(values).cpu().numpy()
    rng = np.random.default_rng(seed)
    for codebook in model.codebooks:
        centers = residual[rng.choice(len(residual), size=len(codebook), replace=False)].copy()
        for _ in range(12):
            distances = ((residual[:, None] - centers[None]) ** 2).sum(-1)
            labels = distances.argmin(-1)
            for cluster in range(len(centers)):
                members = residual[labels == cluster]
                if len(members):
                    centers[cluster] = members.mean(0)
        labels = ((residual[:, None] - centers[None]) ** 2).sum(-1).argmin(-1)
        codebook.data.copy_(
            torch.tensor(centers, dtype=codebook.dtype, device=codebook.device)
        )
        residual = residual - centers[labels]


def _encode(model, tokenizer, texts, device, torch, grad):
    encoded = tokenizer(texts, padding=True, truncation=True, max_length=48, return_tensors="pt").to(device)
    context = torch.enable_grad() if grad else torch.inference_mode()
    with context:
        output = model(**encoded, output_hidden_states=True, return_dict=True, use_cache=False)
        hidden = output.hidden_states[-1]
        weights = encoded["attention_mask"].unsqueeze(-1)
        return (hidden * weights).sum(1) / weights.sum(1).clamp_min(1)


def _encode_batches(model, tokenizer, texts, device, torch):
    model.eval()
    rows = []
    for start in range(0, len(texts), 32):
        rows.append(_encode(model, tokenizer, texts[start : start + 32], device, torch, grad=False).cpu().float())
    model.train()
    return torch.cat(rows).numpy()


def _edge(values, first):
    if not values:
        return None
    width = min(5, len(values))
    return float(np.mean(values[:width] if first else values[-width:]))
