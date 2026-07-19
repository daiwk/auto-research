from __future__ import annotations

import collections
import math

from auto_research.evolution.llm_model import MicroLMConfig, build_micro_lm


def build_recipient(vocab_size: int):
    config = MicroLMConfig(
        vocab_size=vocab_size, dimensions=64, layers=2, heads=4,
        sequence_length=48, expansion=3,
    )
    return build_micro_lm("llama_modern", config), config


def frequent_ngrams(tokens, capacity: int = 192):
    counts = collections.Counter()
    values = [int(value) for value in tokens]
    for order in (2, 3, 4):
        counts.update(tuple(values[index : index + order]) for index in range(len(values) - order + 1))
    return tuple(key for key, _ in counts.most_common(capacity))


def build_frozen_bank(teacher, keys, torch):
    device = next(teacher.parameters()).device
    rows = []
    teacher.eval()
    with torch.inference_mode():
        for key in keys:
            tokens = torch.tensor(key, dtype=torch.long, device=device)[None]
            rows.append(teacher.hidden(tokens)[0, -1].detach().cpu())
    return torch.stack(rows)


def memory_injector(keys, bank, dimensions: int, hash_buckets: int, exact: bool, torch):
    nn = torch.nn

    class ConditionalMemory(nn.Module):
        def __init__(self):
            super().__init__()
            self.key_to_index = {tuple(key): index for index, key in enumerate(keys)}
            self.exact = exact
            self.bank = nn.Embedding.from_pretrained(bank, freeze=True)
            self.hash_memory = nn.Embedding(hash_buckets, dimensions)
            self.memory_key = nn.Linear(dimensions, dimensions, bias=False)
            self.memory_value = nn.Linear(dimensions, dimensions, bias=False)
            self.hash_key = nn.Linear(dimensions, dimensions, bias=False)
            self.hash_value = nn.Linear(dimensions, dimensions, bias=False)
            self.query_norm = nn.RMSNorm(dimensions)
            self.key_norm = nn.RMSNorm(dimensions)
            self.short_conv = nn.Conv1d(dimensions, dimensions, 3, padding=1, groups=dimensions)
            self.last_hit_rate = 0.0

        def _lookup(self, tokens):
            batch, length = tokens.shape
            indices = torch.zeros((batch, length), dtype=torch.long, device=tokens.device)
            mask = torch.zeros((batch, length), dtype=torch.bool, device=tokens.device)
            rows = tokens.detach().cpu().tolist()
            if self.exact:
                for row_index, row in enumerate(rows):
                    for position in range(length):
                        for order in (4, 3, 2):
                            if position + 1 < order:
                                continue
                            key = tuple(row[position - order + 1 : position + 1])
                            found = self.key_to_index.get(key)
                            if found is not None:
                                indices[row_index, position] = found
                                mask[row_index, position] = True
                                break
            hashed = tokens.remainder(hash_buckets)
            for shift, prime in ((1, 257), (2, 65537)):
                shifted = torch.roll(tokens, shift, dims=1)
                shifted[:, :shift] = 0
                hashed = (hashed * prime + shifted).remainder(hash_buckets)
            return indices, mask, hashed

        def forward(self, tokens, hidden):
            indices, mask, hashed = self._lookup(tokens)
            exact_values = self.bank(indices)
            hash_values = self.hash_memory(hashed)
            key = torch.where(
                mask.unsqueeze(-1), self.memory_key(exact_values), self.hash_key(hash_values)
            )
            value = torch.where(
                mask.unsqueeze(-1), self.memory_value(exact_values), self.hash_value(hash_values)
            )
            gate = torch.sigmoid(
                (self.query_norm(hidden) * self.key_norm(key)).sum(-1, keepdim=True)
                / math.sqrt(hidden.shape[-1])
            )
            update = gate * value
            convolved = self.short_conv(update.transpose(1, 2)).transpose(1, 2)
            self.last_hit_rate = float(mask.float().mean().detach().cpu())
            return hidden + update + convolved

    return ConditionalMemory()
