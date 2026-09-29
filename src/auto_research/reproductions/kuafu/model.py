"""Core KuaFu mechanisms.

This module does not contain a surrogate judge or pretend that a fixture is the
paper's industrial four-stage experiment. The caller supplies real model
embeddings, gold-free source-text judgments, and a public-data training loop.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
import math

import torch
from torch import Tensor, nn


def cosine_residual_scale(step: int, total_steps: int) -> float:
    """Anneal the uncached high-width residual away before final inference."""
    if total_steps < 1 or not 0 <= step < total_steps:
        raise ValueError("residual schedule step must be inside total_steps")
    if total_steps == 1:
        return 0.0
    return 0.5 * (1.0 + math.cos(math.pi * step / (total_steps - 1)))


class TwoAxisProjector(nn.Module):
    """Compress m memory states to k low-width states before decoder injection.

    During training, ``restore`` includes the paper's pooled high-width
    residual. The compact cache contains only low-width states; callers must
    not claim the training residual is recoverable from that cache alone.
    """

    def __init__(self, width: int, low_width: int, memory_tokens: int, output_tokens: int):
        super().__init__()
        if not (0 < low_width < width and 0 < output_tokens <= memory_tokens):
            raise ValueError("compression requires low_width < width and k <= m")
        self.down = nn.Linear(width, low_width)
        self.mix = nn.Parameter(torch.full((output_tokens, memory_tokens), 1 / memory_tokens))
        self.up = nn.Linear(low_width, width)
        self.memory_tokens = memory_tokens
        self.output_tokens = output_tokens

    def compress(self, memory_states: Tensor) -> Tensor:
        if memory_states.ndim != 3 or memory_states.shape[-2] != self.memory_tokens:
            raise ValueError("memory states must have shape [items, m, d]")
        low = self.down(memory_states)
        return torch.einsum("km,bmd->bkd", self.mix, low)

    def restore(self, compact: Tensor, memory_states: Tensor | None = None,
                residual_scale: float = 1.0) -> Tensor:
        if compact.shape[-2] != self.output_tokens:
            raise ValueError("invalid compact token count")
        restored = self.up(compact)
        if memory_states is not None:
            if memory_states.shape[-2] != self.memory_tokens:
                raise ValueError("invalid memory token count")
            pooled = memory_states.mean(dim=-2, keepdim=True)
            restored = restored + residual_scale * pooled
        return restored


class KuafuSystem(nn.Module):
    """Independent item LM encoding followed by chronological decoder injection.

    ``encoder`` and ``decoder`` must be causal language models with a common
    hidden width. Production uses separate Qwen3 backbones; tests can inject
    a small causal LM without changing the compression algorithm.
    """

    def __init__(self, encoder: nn.Module, decoder: nn.Module,
                 projector: TwoAxisProjector):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.projector = projector
        embedding_weight = encoder.get_input_embeddings().weight
        self.memory_embeddings = nn.Parameter(
            torch.randn(projector.memory_tokens, projector.down.in_features,
                        device=embedding_weight.device, dtype=embedding_weight.dtype) * 0.02
        )
        self._original_trainable = {
            name: tuple(parameter.requires_grad for parameter in module.parameters())
            for name, module in (("encoder", encoder), ("projector", projector),
                                 ("decoder", decoder))
        }

    def set_stage(self, stage: str) -> None:
        active = {
            "reconstruction": (True, False, False),
            "compressed_qa": (True, True, False),
            "co_training": (True, True, True),
            "hallucination_rl": (False, False, True),
        }
        if stage not in active:
            raise ValueError(f"unknown KuaFu stage: {stage}")
        for name, enabled in zip(("encoder", "projector", "decoder"), active[stage]):
            module = getattr(self, name)
            module.train(enabled)
            for parameter, original in zip(module.parameters(), self._original_trainable[name]):
                parameter.requires_grad_(enabled and original)
        self.memory_embeddings.requires_grad_(stage != "hallucination_rl")

    def encode_item(self, item_ids: Tensor, *, projected: bool,
                    residual_scale: float = 1.0) -> Tensor:
        if item_ids.ndim != 1 or item_ids.numel() == 0:
            raise ValueError("item_ids must be one nonempty token sequence")
        token_embeddings = self.encoder.get_input_embeddings()(item_ids)
        inputs = torch.cat((token_embeddings, self.memory_embeddings), dim=0).unsqueeze(0)
        output = self.encoder(
            inputs_embeds=inputs, output_hidden_states=True, return_dict=True
        )
        states = output.hidden_states
        last_hidden = states if isinstance(states, Tensor) else states[-1]
        memory = last_hidden[:, -self.projector.memory_tokens:, :]
        if not projected:
            return memory[0]
        compact = self.projector.compress(memory)
        return self.projector.restore(compact, memory, residual_scale)[0]

    def context_embeddings(self, items: Sequence[Tensor], prompt_ids: Tensor,
                           *, residual_scale: float = 0.0) -> Tensor:
        if not items or not prompt_ids.numel():
            raise ValueError("items and question must be nonempty")
        device = self.memory_embeddings.device
        projected_items = [
            self.encode_item(item.to(device), projected=True,
                             residual_scale=residual_scale)
            for item in items
        ]
        prompt = self.decoder.get_input_embeddings()(prompt_ids.to(device))
        return torch.cat((*projected_items, prompt), dim=0)

    def completion_logprobs(self, prefix: Tensor, completion_ids: Tensor) -> Tensor:
        """Differentiable token log probabilities for sampled on-policy answers."""
        if prefix.ndim != 2 or completion_ids.ndim != 1 or not completion_ids.numel():
            raise ValueError("expected [prefix,d] and a nonempty completion")
        tokens = completion_ids.to(prefix.device)
        embeddings = self.decoder.get_input_embeddings()(tokens)
        sequence = torch.cat((prefix, embeddings), dim=0).unsqueeze(0)
        logits = self.decoder(inputs_embeds=sequence, return_dict=True).logits[0]
        positions = logits[prefix.shape[0] - 1:prefix.shape[0] - 1 + len(tokens)]
        return positions.log_softmax(dim=-1).gather(-1, tokens[:, None]).squeeze(-1)

    def sequence_loss(self, items: Sequence[Tensor], *, prompt_ids: Tensor,
                      target_ids: Tensor, projected: bool,
                      residual_scale: float = 1.0) -> Tensor:
        if not items or not target_ids.numel():
            raise ValueError("sequence and target must be nonempty")
        device = self.memory_embeddings.device
        # No cross-item encoder context: each call sees only one item's tokens.
        compressed = [
            self.encode_item(item.to(device), projected=projected,
                             residual_scale=residual_scale)
            for item in items
        ]
        decoder_embedding = self.decoder.get_input_embeddings()
        prompt = decoder_embedding(prompt_ids.to(device))
        target = decoder_embedding(target_ids.to(device))
        inputs = torch.cat((*compressed, prompt, target), dim=0).unsqueeze(0)
        prefix_length = inputs.shape[1] - target.shape[0]
        labels = torch.cat((
            torch.full((prefix_length,), -100, dtype=torch.long, device=device),
            target_ids.to(device),
        )).unsqueeze(0)
        return self.decoder(inputs_embeds=inputs, labels=labels, return_dict=True).loss


def cache_item_embeddings(
    user_histories: Sequence[Sequence[Hashable]],
    encode_item: Callable[[Hashable], Tensor],
) -> list[list[Tensor]]:
    """Encode each unique item once; never let user context enter encoding."""
    cache: dict[Hashable, Tensor] = {}
    outputs = []
    for history in user_histories:
        row = []
        for item in history:
            if item not in cache:
                cache[item] = encode_item(item)
            row.append(cache[item])
        outputs.append(row)
    return outputs


def sample_completion_group(
    system: KuafuSystem, prefix: Tensor, *, group_size: int, max_tokens: int,
    eos_token_id: int, generator: torch.Generator, temperature: float = 1.0,
) -> tuple[list[Tensor], list[bool]]:
    """Autoregressive policy rollouts; never inject a gold answer into input."""
    if group_size < 2 or max_tokens < 1 or temperature <= 0:
        raise ValueError("group_size >= 2, max_tokens >= 1, temperature > 0 required")
    outputs: list[Tensor] = []
    truncated: list[bool] = []
    decoder_embeddings = system.decoder.get_input_embeddings()
    with torch.no_grad():
        for _ in range(group_size):
            sequence = prefix.detach()
            sampled: list[int] = []
            complete = False
            for _step in range(max_tokens):
                logits = system.decoder(
                    inputs_embeds=sequence.unsqueeze(0), return_dict=True
                ).logits[0, -1]
                probabilities = torch.softmax(logits.float() / temperature, dim=-1)
                token = int(torch.multinomial(probabilities.cpu(), 1,
                                              generator=generator).item())
                sampled.append(token)
                if token == eos_token_id:
                    complete = True
                    break
                embedding = decoder_embeddings(
                    torch.tensor([token], device=sequence.device)
                )
                sequence = torch.cat((sequence, embedding), dim=0)
            outputs.append(torch.tensor(sampled, dtype=torch.long, device=prefix.device))
            truncated.append(not complete)
    return outputs, truncated


def configure_training_stage(
    stage: str, compressor: nn.Module, projector: nn.Module, decoder: nn.Module
) -> None:
    """The exact trainable C/P/D sets in KuaFu Table 1."""
    trainable = {
        "reconstruction": (True, False, False),
        "compressed_qa": (True, True, False),
        "co_training": (True, True, True),
        "hallucination_rl": (False, False, True),
    }
    try:
        flags = trainable[stage]
    except KeyError as exc:
        raise ValueError(f"unknown KuaFu stage: {stage}") from exc
    for module, active in zip((compressor, projector, decoder), flags):
        module.train(active)
        for parameter in module.parameters():
            parameter.requires_grad_(active)


_ERROR_WEIGHTS = {
    "fabrication": 0.45,
    "date_misattribution": 0.24,
    "broken_logic": 0.24,
    "missed_detection": 0.07,
}


def hallucination_reward(errors: dict[str, bool], completeness: str,
                         bonuses: dict[str, float] | None = None) -> float:
    """Source-grounded judge outputs -> paper's four weighted penalties.

    The paper does not specify numerical completeness bonuses. These are
    caller-configurable and default to an explicit ordinal scale; they are
    *not* reported as an author-provided value.
    """
    unknown = set(errors) - _ERROR_WEIGHTS.keys()
    if unknown:
        raise ValueError(f"unknown hallucination categories: {sorted(unknown)}")
    reward_bonus = bonuses or {"complete": 1.0, "partial": 0.5, "missing": 0.0}
    if completeness not in reward_bonus:
        raise ValueError(f"unknown completeness: {completeness}")
    return reward_bonus[completeness] - sum(
        weight for name, weight in _ERROR_WEIGHTS.items() if errors.get(name, False)
    )


def dapo_objective(
    new_logprobs: Tensor, old_logprobs: Tensor, rewards: Tensor,
    *, token_mask: Tensor, truncated: Tensor, clip_low: float = 0.2,
    clip_high: float = 0.28,
) -> Tensor:
    """Token-ratio, asymmetric-clip DAPO with group-mean advantage, no KL.

    One call represents one prompt group. Truncated completions are dropped
    rather than assigned zero reward. Reward judging must use uncompressed
    source text and not hold-out gold answers visible to the policy.
    """
    if new_logprobs.shape != old_logprobs.shape or new_logprobs.shape != token_mask.shape:
        raise ValueError("logprobs and token mask must have identical shape")
    if new_logprobs.ndim != 2 or rewards.shape != new_logprobs.shape[:1]:
        raise ValueError("expected [responses,tokens] and one reward per response")
    if truncated.shape != rewards.shape:
        raise ValueError("truncation mask must have one value per response")
    valid = ~truncated.bool()
    if not valid.any():
        raise ValueError("DAPO needs at least one non-truncated response")
    # Group baseline includes sampled responses; exclusion applies to loss.
    advantages = rewards - rewards.mean()
    ratio = torch.exp(new_logprobs - old_logprobs.detach())
    clipped = torch.clamp(ratio, 1 - clip_low, 1 + clip_high)
    surrogate = torch.minimum(ratio * advantages[:, None], clipped * advantages[:, None])
    weights = token_mask.to(surrogate.dtype) * valid[:, None].to(surrogate.dtype)
    return -(surrogate * weights).sum() / weights.sum().clamp_min(1)
