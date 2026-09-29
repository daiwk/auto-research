"""Public MRQA answer scoring and strict equal-token input controls."""

from __future__ import annotations

from collections import Counter
import re
import string
from collections.abc import Sequence

import torch
from torch import Tensor


def _tokens(text: str) -> list[str]:
    normalized = text.lower().translate(str.maketrans("", "", string.punctuation))
    normalized = re.sub(r"\b(a|an|the)\b", " ", normalized)
    return normalized.split()


def exact_match(prediction: str, references: Sequence[str]) -> float:
    if not references:
        raise ValueError("MRQA scoring requires at least one reference")
    normalized = _tokens(prediction)
    return float(any(normalized == _tokens(reference) for reference in references))


def token_f1(prediction: str, references: Sequence[str]) -> float:
    if not references:
        raise ValueError("MRQA scoring requires at least one reference")
    predicted = _tokens(prediction)
    scores = []
    for reference in references:
        expected = _tokens(reference)
        if not predicted or not expected:
            scores.append(float(predicted == expected))
            continue
        overlap = sum((Counter(predicted) & Counter(expected)).values())
        scores.append(2 * overlap / (len(predicted) + len(expected)))
    return max(scores)


def same_token_budget(raw_ids: Tensor, *, item_count: int,
                      tokens_per_item: int) -> tuple[Tensor, Tensor]:
    """Head/tail raw-text controls have the same count as cached item slots."""
    if raw_ids.ndim != 1 or item_count < 1 or tokens_per_item < 1:
        raise ValueError("expected raw IDs and a positive cache budget")
    budget = item_count * tokens_per_item
    if raw_ids.numel() < budget:
        raise ValueError("raw context shorter than compressed token budget")
    return raw_ids[:budget], raw_ids[-budget:]


def raw_context_qa_loss(decoder: torch.nn.Module, context_ids: Tensor,
                        question_ids: Tensor, answer_ids: Tensor) -> Tensor:
    """Train an independent raw-token control without exposing answer in the prefix."""
    if any(value.ndim != 1 or not value.numel()
           for value in (context_ids, question_ids, answer_ids)):
        raise ValueError("raw context, question and answer must be nonempty token vectors")
    source = torch.cat((context_ids, question_ids))
    tokens = torch.cat((source, answer_ids))
    labels = torch.cat((torch.full_like(source, -100), answer_ids))
    return decoder(input_ids=tokens[None], labels=labels[None], return_dict=True).loss


def greedy_answer(decoder: torch.nn.Module, prefix: Tensor, *,
                  eos_token_id: int, max_tokens: int) -> Tensor:
    """Decode only from source/prompt prefix; no gold answer enters the model."""
    if prefix.ndim != 2 or not prefix.numel() or max_tokens < 1:
        raise ValueError("expected [tokens,width] prefix and positive max_tokens")
    sequence = prefix
    tokens: list[int] = []
    embedding = decoder.get_input_embeddings()
    with torch.no_grad():
        for _ in range(max_tokens):
            output = decoder(inputs_embeds=sequence.unsqueeze(0), return_dict=True)
            token = int(output.logits[0, -1].argmax().item())
            if token == eos_token_id:
                break
            tokens.append(token)
            next_embedding = embedding(torch.tensor([token], device=sequence.device))
            sequence = torch.cat((sequence, next_embedding), dim=0)
    return torch.tensor(tokens, dtype=torch.long, device=prefix.device)
