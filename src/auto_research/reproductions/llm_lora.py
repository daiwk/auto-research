from __future__ import annotations

import random


def require_llm_backend():
    try:
        import torch
        from torch import nn
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError as exc:
        raise RuntimeError("This reproduction needs `pip install -e '.[plum]'`.") from exc
    return torch, nn, AutoModelForCausalLM, AutoTokenizer


def device_for(torch):
    return torch.device("mps" if torch.backends.mps.is_available() else "cpu")


def inject_lora(model, rank: int = 4, alpha: float = 8.0):
    torch, nn, _, _ = require_llm_backend()

    class LoRALinear(nn.Module):
        def __init__(self, base):
            super().__init__()
            self.base = base
            self.down = nn.Linear(base.in_features, rank, bias=False)
            self.up = nn.Linear(rank, base.out_features, bias=False)
            nn.init.normal_(self.down.weight, std=0.02)
            nn.init.zeros_(self.up.weight)
            self.down.to(device=base.weight.device, dtype=base.weight.dtype)
            self.up.to(device=base.weight.device, dtype=base.weight.dtype)
            self.scale = alpha / rank

        def forward(self, values):
            return self.base(values) + self.up(self.down(values)) * self.scale

    for parameter in model.parameters():
        parameter.requires_grad = False
    replacements = []
    for name, module in model.named_modules():
        if name.rsplit(".", 1)[-1] in {"q_proj", "v_proj", "q", "v"} and isinstance(module, nn.Linear):
            replacements.append((name, module))
    for name, module in replacements:
        parent_name, child = name.rsplit(".", 1)
        parent = model.get_submodule(parent_name)
        setattr(parent, child, LoRALinear(module))
    return sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)


def load_lora_lm(model_name: str, seed: int):
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    torch.manual_seed(seed)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "left"
    model = AutoModelForCausalLM.from_pretrained(model_name)
    trainable = inject_lora(model)
    model.to(device_for(torch))
    return model, tokenizer, trainable


def lora_sft(model, tokenizer, examples, steps: int, batch_size: int, learning_rate: float, seed: int):
    torch, _, _, _ = require_llm_backend()
    device = next(model.parameters()).device
    rows = []
    for prompt, completion in examples:
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        completion_ids = tokenizer(completion + tokenizer.eos_token, add_special_tokens=False)["input_ids"]
        prompt_ids = prompt_ids[-(128 - len(completion_ids)) :]
        rows.append((prompt_ids + completion_ids, [-100] * len(prompt_ids) + completion_ids))
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=learning_rate)
    rng = random.Random(seed)
    losses = []
    model.train()
    for _ in range(steps):
        batch = [rows[rng.randrange(len(rows))] for _ in range(batch_size)]
        width = max(len(row[0]) for row in batch)
        input_ids, masks, labels = [], [], []
        for ids, target in batch:
            padding = width - len(ids)
            input_ids.append([tokenizer.pad_token_id] * padding + ids)
            masks.append([0] * padding + [1] * len(ids))
            labels.append([-100] * padding + target)
        output = model(
            input_ids=torch.tensor(input_ids, device=device),
            attention_mask=torch.tensor(masks, device=device),
            labels=torch.tensor(labels, device=device),
        )
        optimizer.zero_grad(set_to_none=True)
        output.loss.backward()
        torch.nn.utils.clip_grad_norm_([p for p in model.parameters() if p.requires_grad], 1.0)
        optimizer.step()
        losses.append(float(output.loss.detach().cpu()))
    return {"initial": sum(losses[: min(10, len(losses))]) / min(10, len(losses)), "final": sum(losses[-min(10, len(losses)) :]) / min(10, len(losses))}


def encode_texts(model, tokenizer, texts, batch_size: int = 16, maximum_length: int = 128):
    torch, _, _, _ = require_llm_backend()
    device = next(model.parameters()).device
    vectors = []
    model.eval()
    with torch.inference_mode():
        for start in range(0, len(texts), batch_size):
            encoded = tokenizer(
                texts[start : start + batch_size], padding=True, truncation=True,
                max_length=maximum_length, return_tensors="pt",
            ).to(device)
            output = model(**encoded, output_hidden_states=True, return_dict=True)
            hidden = output.hidden_states[-1]
            weights = encoded["attention_mask"].unsqueeze(-1)
            vectors.append(((hidden * weights).sum(1) / weights.sum(1).clamp_min(1)).cpu().float())
    return torch.cat(vectors).numpy()
