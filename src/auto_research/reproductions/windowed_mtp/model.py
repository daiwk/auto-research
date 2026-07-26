from __future__ import annotations

import math
import time


def build_mtp_head(target, *, heads: int = 4):
    import torch
    from torch import nn

    dimensions = target.token.embedding_dim
    vocab_size = target.token.num_embeddings
    head_dim = dimensions // heads

    class MTPHead(nn.Module):
        def __init__(self):
            super().__init__()
            self.token = nn.Embedding.from_pretrained(
                target.token.weight.detach().clone(), freeze=True
            )
            self.norm = nn.RMSNorm(dimensions)
            self.q = nn.Linear(dimensions, dimensions, bias=False)
            self.k = nn.Linear(dimensions, dimensions, bias=False)
            self.v = nn.Linear(dimensions, dimensions, bias=False)
            self.output = nn.Linear(dimensions, dimensions, bias=False)
            self.vocab = nn.Linear(dimensions, vocab_size, bias=False)
            self.vocab.weight = self.token.weight
            self.heads = heads
            self.head_dim = head_dim

        def key_indices(self, length: int, *, window: int | None, sink: int, device):
            if window is None or length <= window + sink:
                return torch.arange(length, device=device)
            recent_start = max(sink, length - window)
            return torch.cat((
                torch.arange(min(sink, length), device=device),
                torch.arange(recent_start, length, device=device),
            ))

        def forward(self, tokens, *, window: int | None = None, sink: int = 0):
            values = self.norm(self.token(tokens))
            indices = self.key_indices(
                values.shape[1], window=window, sink=sink, device=values.device
            )
            keys = values.index_select(1, indices)
            batch = values.shape[0]
            query = self.q(values[:, -1:]).view(
                batch, 1, self.heads, self.head_dim
            ).transpose(1, 2)
            key = self.k(keys).view(
                batch, len(indices), self.heads, self.head_dim
            ).transpose(1, 2)
            value = self.v(keys).view(
                batch, len(indices), self.heads, self.head_dim
            ).transpose(1, 2)
            attention = torch.softmax(
                torch.matmul(query, key.transpose(-2, -1))
                / math.sqrt(self.head_dim),
                dim=-1,
            )
            mixed = torch.matmul(attention, value)
            mixed = mixed.transpose(1, 2).reshape(batch, 1, -1)
            return self.vocab(self.output(mixed[:, 0]))

    return MTPHead()


def train_mtp_head(
    draft,
    tokens,
    *,
    steps: int,
    batch_size: int,
    context: int,
    learning_rate: float,
    seed: int,
    torch,
) -> dict:
    import numpy as np

    device = next(draft.parameters()).device
    draft.train()
    optimizer = torch.optim.AdamW(
        [parameter for parameter in draft.parameters() if parameter.requires_grad],
        lr=learning_rate,
    )
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(steps):
        starts = rng.integers(0, len(tokens) - context - 1, size=batch_size)
        rows = np.stack([tokens[start : start + context + 1] for start in starts])
        batch = torch.tensor(rows, dtype=torch.long, device=device)
        logits = draft(batch[:, :-1])
        loss = torch.nn.functional.cross_entropy(logits, batch[:, -1])
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(draft.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach().cpu()))
    return {
        "initial_loss": float(np.mean(losses[:5])),
        "final_loss": float(np.mean(losses[-5:])),
        "parameters": sum(
            parameter.numel()
            for parameter in draft.parameters()
            if parameter.requires_grad
        ),
    }


def _next_target(target, tokens, torch):
    return int(target(tokens)[0, -1].argmax().item())


def dense_greedy(target, prompt, *, new_tokens: int, torch) -> list[int]:
    output = prompt.clone()
    with torch.inference_mode():
        for _ in range(new_tokens):
            token = _next_target(target, output, torch)
            output = torch.cat((
                output,
                torch.tensor([[token]], dtype=torch.long, device=output.device),
            ), dim=1)
    return output[0, -new_tokens:].tolist()


def speculative_greedy(
    target,
    draft,
    prompt,
    *,
    new_tokens: int,
    gamma: int,
    window: int | None,
    sink: int,
    torch,
) -> dict:
    """Greedy speculative decoding; target verification makes output exact."""
    output = prompt.clone()
    accepted, proposed, rounds = 0, 0, 0
    with torch.inference_mode():
        while output.shape[1] < prompt.shape[1] + new_tokens:
            rounds += 1
            proposal_context = output
            proposals = []
            for _ in range(min(gamma, prompt.shape[1] + new_tokens - output.shape[1])):
                token = int(
                    draft(proposal_context, window=window, sink=sink)
                    .argmax(dim=-1)
                    .item()
                )
                proposals.append(token)
                proposal_context = torch.cat((
                    proposal_context,
                    torch.tensor(
                        [[token]], dtype=torch.long, device=output.device
                    ),
                ), dim=1)
            for proposal in proposals:
                target_token = _next_target(target, output, torch)
                proposed += 1
                if proposal == target_token:
                    accepted += 1
                    chosen = proposal
                else:
                    chosen = target_token
                output = torch.cat((
                    output,
                    torch.tensor(
                        [[chosen]], dtype=torch.long, device=output.device
                    ),
                ), dim=1)
                if proposal != target_token:
                    break
    return {
        "tokens": output[0, -new_tokens:].tolist(),
        "acceptance_rate": accepted / max(proposed, 1),
        "mean_accepted_per_round": accepted / max(rounds, 1),
        "rounds": rounds,
    }


def benchmark_draft_attention(
    draft,
    *,
    contexts: tuple[int, ...],
    window: int,
    sink: int,
    repeats: int,
    seed: int,
    torch,
) -> list[dict]:
    device = next(draft.parameters()).device
    generator = torch.Generator(device="cpu").manual_seed(seed)
    rows = []

    def synchronize():
        if device.type == "cuda":
            torch.cuda.synchronize()
        elif device.type == "mps":
            torch.mps.synchronize()

    draft.eval()
    with torch.inference_mode():
        for context in contexts:
            tokens = torch.randint(
                0,
                draft.token.num_embeddings,
                (1, context),
                generator=generator,
            ).to(device)
            for mode in (None, window):
                for _ in range(3):
                    draft(tokens, window=mode, sink=sink)
                synchronize()
                start = time.perf_counter()
                for _ in range(repeats):
                    draft(tokens, window=mode, sink=sink)
                synchronize()
                elapsed = 1000 * (time.perf_counter() - start) / repeats
                key_count = (
                    context
                    if mode is None
                    else min(context, window + sink)
                )
                rows.append({
                    "context": context,
                    "mode": "native" if mode is None else "windowed",
                    "milliseconds": elapsed,
                    "key_count": key_count,
                    "kv_read_reduction_percent": 100
                    * (context - key_count)
                    / context,
                })
    return rows
