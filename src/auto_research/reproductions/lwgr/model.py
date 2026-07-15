from __future__ import annotations

import random
import time
from dataclasses import dataclass

import numpy as np

from ..llm_lora import device_for, require_llm_backend


@dataclass(frozen=True)
class LWGRConfig:
    dimensions: int = 48
    sequence_length: int = 12
    parallel_codebooks: int = 3
    codewords: int = 8
    batch_size: int = 8
    temperature: float = 0.2
    margin: float = 1e-4
    constraint: float = 1e-4
    lambda_initial: float = 0.05
    lambda_lr: float = 5e-4
    learning_rate: float = 8e-4


def load_knowledge_llm(model_name: str, titles, config: LWGRConfig):
    torch, _, AutoModelForCausalLM, AutoTokenizer = require_llm_backend()
    tokenizer = AutoTokenizer.from_pretrained(model_name, local_files_only=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(model_name, local_files_only=True)
    for parameter in model.parameters():
        parameter.requires_grad_(False)
    device = device_for(torch)
    model.to(device).eval()
    embedding = model.get_input_embeddings()
    vectors = []
    with torch.inference_mode():
        for start in range(0, len(titles), 64):
            encoded = tokenizer(
                list(titles[start : start + 64]),
                padding=True,
                truncation=True,
                max_length=16,
                return_tensors="pt",
            ).to(device)
            values = embedding(encoded["input_ids"])
            weights = encoded["attention_mask"].unsqueeze(-1)
            vectors.append((values * weights).sum(1) / weights.sum(1).clamp_min(1))
    return model, torch.cat(vectors).detach(), device


def build_gr(item_count: int, code_sizes: tuple[int, ...], config: LWGRConfig):
    torch, nn, _, _ = require_llm_backend()

    class GenerativeRecommender(nn.Module):
        def __init__(self):
            super().__init__()
            self.item = nn.Embedding(item_count, config.dimensions)
            self.encoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.code_embeddings = nn.ModuleList(
                [nn.Embedding(size, config.dimensions) for size in code_sizes]
            )
            self.bos = nn.Parameter(torch.zeros(config.dimensions))
            self.decoder = nn.GRU(config.dimensions, config.dimensions, batch_first=True)
            self.heads = nn.ModuleList(
                [nn.Linear(config.dimensions, size) for size in code_sizes]
            )
            self.world_projection = None
            self.cross_attention = nn.MultiheadAttention(
                config.dimensions, 4, batch_first=True
            )

        def encode(self, histories):
            _, state = self.encoder(self.item(histories))
            return state.squeeze(0)

        def fuse(self, context, world=None):
            if world is None:
                return context
            projected = self.world_projection(world)
            attended, _ = self.cross_attention(
                context.unsqueeze(1), projected, projected, need_weights=False
            )
            return context + attended.squeeze(1)

        def decode(self, context, codes):
            batch = codes.shape[0]
            previous = [self.bos.expand(batch, 1, -1)]
            for level in range(1, codes.shape[1]):
                previous.append(
                    self.code_embeddings[level - 1](codes[:, level - 1]).unsqueeze(1)
                )
            hidden, _ = self.decoder(torch.cat(previous, 1), context.unsqueeze(0))
            return [head(hidden[:, level]) for level, head in enumerate(self.heads)]

        def forward(self, histories, codes, world=None):
            return self.decode(self.fuse(self.encode(histories), world), codes)

    return GenerativeRecommender()


def build_lwgr(gr, llm, title_embeddings, config: LWGRConfig):
    torch, nn, _, _ = require_llm_backend()
    llm_dimensions = title_embeddings.shape[1]
    sub_dimensions = config.dimensions // config.parallel_codebooks

    class ParallelInstructions(nn.Module):
        def __init__(self):
            super().__init__()
            self.codebooks = nn.Parameter(
                torch.randn(
                    config.parallel_codebooks, config.codewords, sub_dimensions
                )
                * 0.02
            )
            self.projections = nn.ModuleList(
                [nn.Linear(sub_dimensions, llm_dimensions) for _ in range(config.parallel_codebooks)]
            )

        def forward(self, context):
            subspaces = context.view(
                len(context), config.parallel_codebooks, sub_dimensions
            )
            distance = -(
                (subspaces[:, :, None] - self.codebooks[None]) ** 2
            ).sum(-1)
            probability = torch.softmax(distance / config.temperature, -1)
            hard = torch.nn.functional.one_hot(
                probability.argmax(-1), config.codewords
            ).to(probability.dtype)
            straight_through = hard - probability.detach() + probability
            selected = torch.einsum(
                "bkv,kvd->bkd", straight_through, self.codebooks
            )
            return torch.stack(
                [self.projections[index](selected[:, index]) for index in range(config.parallel_codebooks)],
                1,
            ), probability

    class LWGR(nn.Module):
        def __init__(self):
            super().__init__()
            self.gr = gr
            self.llm = llm
            self.instructions = ParallelInstructions()
            self.register_buffer("title_embeddings", title_embeddings)
            self.gr.world_projection = nn.Linear(llm_dimensions, config.dimensions)

        def world_knowledge(self, histories):
            context = self.gr.encode(histories)
            instructions, probability = self.instructions(context)
            text = self.title_embeddings[histories[:, -6:]]
            self.llm.eval()
            output = self.llm(
                inputs_embeds=torch.cat((instructions, text), 1),
                output_hidden_states=True,
                use_cache=False,
                return_dict=True,
            )
            return output.hidden_states[-1], probability

        def forward(self, histories, codes):
            world, probability = self.world_knowledge(histories)
            return self.gr(histories, codes, world), probability

        def state(self, histories):
            world, _ = self.world_knowledge(histories)
            return self.gr.fuse(self.gr.encode(histories), world)

    return LWGR()


def train_reference(codes, item_count, rows, config, steps, seed, device):
    torch, _, _, _ = require_llm_backend()
    torch.manual_seed(seed)
    sizes = tuple(int(codes[:, level].max()) + 1 for level in range(codes.shape[1]))
    model = build_gr(item_count, sizes, config).to(device)
    code_tensor = torch.tensor(codes, dtype=torch.long, device=device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=config.learning_rate)
    rng = random.Random(seed)
    losses = []
    started = time.perf_counter()
    for _ in range(steps):
        histories, targets = _batch(rows, config, rng, device, torch)
        target_codes = code_tensor[targets]
        loss = _rec_loss(model(histories, target_codes), target_codes, torch)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return model, _training(losses, started, steps)


def train_policy(
    reference,
    llm,
    title_embeddings,
    codes,
    rows,
    config,
    steps,
    seed,
    constrained,
):
    torch, _, _, _ = require_llm_backend()
    torch.manual_seed(seed)
    device = next(reference.parameters()).device
    sizes = tuple(int(codes[:, level].max()) + 1 for level in range(codes.shape[1]))
    gr = build_gr(len(codes), sizes, config).to(device)
    compatible = {
        key: value
        for key, value in reference.state_dict().items()
        if key in gr.state_dict() and gr.state_dict()[key].shape == value.shape
    }
    gr.load_state_dict(compatible, strict=False)
    model = build_lwgr(gr, llm, title_embeddings, config).to(device)
    code_tensor = torch.tensor(codes, dtype=torch.long, device=device)
    trainable = [parameter for parameter in model.parameters() if parameter.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=config.learning_rate)
    rng = random.Random(seed)
    multiplier = config.lambda_initial
    losses, constraints, multipliers, entropies = [], [], [], []
    started = time.perf_counter()
    reference.eval()
    for _ in range(steps):
        histories, targets = _batch(rows, config, rng, device, torch)
        target_codes = code_tensor[targets]
        logits, probability = model(histories, target_codes)
        rec_loss = _rec_loss(logits, target_codes, torch)
        policy_score = _path_score(logits, target_codes, torch)
        with torch.no_grad():
            reference_score = _path_score(
                reference(histories, target_codes), target_codes, torch
            )
        degradation = torch.relu(
            reference_score - policy_score - config.margin
        ).mean()
        loss = rec_loss
        if constrained:
            loss = loss + multiplier * (degradation - config.constraint)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(trainable, 1.0)
        optimizer.step()
        if constrained:
            multiplier = max(
                0.0,
                multiplier
                + config.lambda_lr * (float(degradation.detach().cpu()) - config.constraint),
            )
        entropy = -(probability * probability.clamp_min(1e-8).log()).sum(-1).mean()
        losses.append(float(rec_loss.detach().cpu()))
        constraints.append(float(degradation.detach().cpu()))
        multipliers.append(multiplier)
        entropies.append(float(entropy.detach().cpu()))
    metrics = _training(losses, started, steps)
    metrics.update(
        {
            "mean_degradation_constraint": float(np.mean(constraints)),
            "final_lagrange_multiplier": multiplier,
            "mean_codebook_entropy": float(np.mean(entropies)),
            "constrained": constrained,
        }
    )
    return model, metrics


def score_catalog(model, history, codes, config, reference=False, chunk=512):
    torch, _, _, _ = require_llm_backend()
    device = next(model.parameters()).device
    histories = _histories([history], config.sequence_length, device, torch)
    code_tensor = torch.tensor(codes, dtype=torch.long, device=device)
    model.eval()
    values = []
    with torch.inference_mode():
        if reference:
            context = model.encode(histories)
            decoder = model
        else:
            context = model.state(histories)
            decoder = model.gr
        for start in range(0, len(codes), chunk):
            candidate = code_tensor[start : start + chunk]
            logits = decoder.decode(context.expand(len(candidate), -1), candidate)
            values.append(_path_score(logits, candidate, torch).cpu().numpy())
    return np.concatenate(values)


def _batch(rows, config, rng, device, torch):
    selected = [rows[rng.randrange(len(rows))] for _ in range(config.batch_size)]
    histories = _histories([row[0] for row in selected], config.sequence_length, device, torch)
    targets = torch.tensor([row[1] for row in selected], device=device)
    return histories, targets


def _histories(histories, length, device, torch):
    output = []
    for history in histories:
        recent = tuple(history[-length:])
        padding = recent[0] if recent else 0
        output.append((padding,) * (length - len(recent)) + recent)
    return torch.tensor(output, dtype=torch.long, device=device)


def _rec_loss(logits, codes, torch):
    return sum(
        torch.nn.functional.cross_entropy(logits[level], codes[:, level])
        for level in range(codes.shape[1])
    ) / codes.shape[1]


def _path_score(logits, codes, torch):
    score = torch.zeros(len(codes), device=codes.device)
    for level in range(codes.shape[1]):
        score += torch.log_softmax(logits[level], -1).gather(
            1, codes[:, level : level + 1]
        ).squeeze(1)
    return score / codes.shape[1]


def _training(losses, started, steps):
    window = min(10, len(losses))
    return {
        "steps": steps,
        "initial_loss": float(np.mean(losses[:window])),
        "final_loss": float(np.mean(losses[-window:])),
        "seconds": time.perf_counter() - started,
    }
