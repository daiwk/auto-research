"""Bounded actual-cache attention diagnostic; no training or large download."""

from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import time
from typing import Any

import torch
from torch import Tensor

from .cache import PNMixCache, PNMixConfig, reference_attention


# Public-domain original text, not benchmark questions/answers or a trained-policy fixture.
PUBLIC_TEXT = (
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer "
    "The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles "
    "And by opposing end them. To die, to sleep; No more; and by a sleep to say we end "
    "The heart-ache and the thousand natural shocks That flesh is heir to. "
)
PUBLIC_TEXT_SOURCE = "https://www.gutenberg.org/ebooks/1524"


def component_device(requested: str | None = None) -> str:
    """Honor the shared runtime without selecting an unsupported MPS backend.

    PN-Mix's packing/reference path is advertised for CPU/CUDA only. Auto uses
    CUDA if available, otherwise CPU even on a Mac with an MPS device. Explicit
    MPS fails before any experiment rather than silently changing the backend.
    """
    from auto_research import runtime

    choice = (requested or os.environ.get(runtime.DEVICE_ENV, "auto")).strip().lower()
    if choice == "auto":
        choice = "cuda" if torch.cuda.is_available() else "cpu"
    if choice == "mps":
        raise ValueError("PN-Mix does not support MPS; choose cpu, cuda, or auto")
    return str(runtime.device_for(torch, choice))


def apply_rope(states: Tensor, positions: Tensor, *, pair_layout: str) -> Tensor:
    """Standard RoPE with explicit pair layout, used only by the initialized probe."""
    half = states.shape[-1] // 2
    frequencies = 1 / (10000 ** (torch.arange(half, device=states.device).float() / half))
    angles = positions.float().unsqueeze(-1) * frequencies
    cos, sin = angles.cos()[None, None], angles.sin()[None, None]
    if pair_layout == "adjacent":
        pair = states.float().reshape(*states.shape[:-1], half, 2)
        left, right = pair.unbind(-1)
        return (
            torch.stack((left * cos - right * sin, left * sin + right * cos), -1)
            .flatten(-2)
            .to(states.dtype)
        )
    if pair_layout == "split":
        left, right = states.float().chunk(2, -1)
        return torch.cat((left * cos - right * sin, left * sin + right * cos), -1).to(states.dtype)
    raise ValueError("unknown pair layout")


def _public_bytes(tokens: int) -> tuple[list[int], dict[str, str]]:
    content = (PUBLIC_TEXT * (tokens // len(PUBLIC_TEXT) + 2)).encode("utf-8")[:tokens]
    return list(content), {
        "dataset": "public-domain-Hamlet-byte-diagnostic",
        "revision": "sha256:" + hashlib.sha256(content).hexdigest(),
        "source_url": PUBLIC_TEXT_SOURCE,
        "split": "fixed-input-mechanism-diagnostic-no-task-labels",
    }


def initialized_states(
    tokens: int, *, seed: int, device: str, dtype: torch.dtype, pair_layout: str
) -> tuple[Tensor, Tensor, Tensor, dict[str, Any]]:
    """A genuinely executed, random-initialized embedding -> RoPE/GQA network.

    This is *not* a pretrained Llama checkpoint, language benchmark, or surrogate
    scoring formula. The cache algorithm is unmodified; only its input network is tiny.
    """
    ids, dataset = _public_bytes(tokens)
    with torch.random.fork_rng(devices=[torch.device(device)] if device.startswith("cuda") else []):
        torch.manual_seed(seed)
        network = torch.nn.ModuleDict(
            {
                "embedding": torch.nn.Embedding(256, 128),
                "query": torch.nn.Linear(128, 128, bias=False),
                "key": torch.nn.Linear(128, 64, bias=False),
                "value": torch.nn.Linear(128, 64, bias=False),
            }
        ).to(device=device, dtype=dtype)
        with torch.no_grad():
            hidden = network["embedding"](torch.tensor(ids, device=device)[None])
            query = network["query"](hidden).reshape(1, tokens, 4, 32).transpose(1, 2)
            key = network["key"](hidden).reshape(1, tokens, 2, 32).transpose(1, 2)
            value = network["value"](hidden).reshape(1, tokens, 2, 32).transpose(1, 2)
            positions = torch.arange(tokens, device=device)
            query = apply_rope(query, positions, pair_layout=pair_layout)
            key = apply_rope(key, positions, pair_layout=pair_layout)
    return (
        query,
        key,
        value,
        {
            "dataset": dataset,
            "checkpoint": {
                "id": "random-initialized-single-layer-RoPE-GQA",
                "revision": "pn-mix-reference-rope-v1",
                "initialization_seed": seed,
                "pretrained": False,
            },
        },
    )


def checkpoint_states(
    checkpoint: Path, *, model_id: str, revision: str, tokens: int, device: str, dtype: torch.dtype
) -> tuple[Tensor, Tensor, Tensor, dict[str, Any]]:
    """Extract actual first-layer post-RoPE states from an offline Llama/SmolLM2 model.

    The checkpoint must already exist locally, and its public ID plus immutable
    revision must be supplied separately, so reports never contain private paths.
    This function never downloads models or data and does not run a full benchmark.
    """
    import re
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if (
        not checkpoint.is_dir()
        or "/" not in model_id
        or not re.fullmatch(r"[0-9a-f]{40}", revision)
    ):
        raise ValueError(
            "existing local checkpoint, public model ID and immutable 40-hex revision required"
        )
    # Cheap config-only gate *before* opening any weight shard. This deliberately
    # overestimates untied embedding/output weights and accepts only small models.
    configuration = json.loads((checkpoint / "config.json").read_text(encoding="utf-8"))
    if configuration.get("model_type") != "llama":
        raise ValueError("checkpoint extraction is explicitly limited to Llama/SmolLM2")
    hidden = int(configuration["hidden_size"])
    layers = int(configuration["num_hidden_layers"])
    heads = int(configuration["num_attention_heads"])
    kv_heads = int(configuration.get("num_key_value_heads", heads))
    head_dim = int(configuration.get("head_dim", hidden // heads))
    intermediate = int(configuration["intermediate_size"])
    vocabulary = int(configuration["vocab_size"])
    if min(hidden, layers, heads, kv_heads, head_dim, intermediate, vocabulary) <= 0:
        raise ValueError("invalid checkpoint dimensions")
    estimate = 2 * vocabulary * hidden + layers * (
        2 * hidden * heads * head_dim
        + 2 * hidden * kv_heads * head_dim
        + 3 * hidden * intermediate
        + 2 * hidden
    )
    if estimate > 500_000_000:
        raise ValueError(
            "checkpoint exceeds the 500M conservative parameter cost gate; no weights loaded"
        )
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
    encoded = tokenizer(
        PUBLIC_TEXT * (tokens // 20 + 2),
        return_tensors="pt",
        truncation=True,
        max_length=tokens,
        add_special_tokens=False,
    )
    ids = encoded["input_ids"].to(device)
    if ids.shape[-1] != tokens:
        raise ValueError("public diagnostic text did not supply the requested token count")
    model = (
        AutoModelForCausalLM.from_pretrained(
            checkpoint, local_files_only=True, dtype=dtype, attn_implementation="eager"
        )
        .to(device)
        .eval()
    )
    if model.config.model_type != "llama":
        raise ValueError("checkpoint extraction is explicitly limited to Llama/SmolLM2")
    layer = model.model.layers[0]
    attention = layer.self_attn
    with torch.no_grad():
        hidden = layer.input_layernorm(model.model.embed_tokens(ids))
        dim = attention.head_dim
        qheads, kheads = model.config.num_attention_heads, model.config.num_key_value_heads
        query = attention.q_proj(hidden).reshape(1, tokens, qheads, dim).transpose(1, 2)
        key = attention.k_proj(hidden).reshape(1, tokens, kheads, dim).transpose(1, 2)
        value = attention.v_proj(hidden).reshape(1, tokens, kheads, dim).transpose(1, 2)
        positions = torch.arange(tokens, device=device)[None]
        cos, sin = model.model.rotary_emb(hidden, positions)

        # Llama pairs the first/second halves, not adjacent memory channels.
        def rotate_half(x):
            left, right = x.chunk(2, -1)
            return torch.cat((-right, left), -1)

        query = query * cos[:, None] + rotate_half(query) * sin[:, None]
        key = key * cos[:, None] + rotate_half(key) * sin[:, None]
    token_hash = hashlib.sha256(ids.cpu().numpy().tobytes()).hexdigest()
    return (
        query,
        key,
        value,
        {
            "dataset": {
                "dataset": "public-domain-Hamlet-checkpoint-token-diagnostic",
                "revision": "sha256:" + token_hash,
                "source_url": PUBLIC_TEXT_SOURCE,
                "split": "fixed-input-mechanism-diagnostic-no-task-labels",
            },
            "checkpoint": {
                "id": model_id,
                "revision": revision,
                "pretrained": True,
                "checkpoint_revision_source": "caller-declared-public-revision-offline-no-network-resolution",
                "conservative_parameter_estimate": estimate,
                "captured_layer": 0,
                "model_type": "llama",
                "pair_layout": "split",
            },
        },
    )


def run_diagnostic(
    *,
    seed: int = 42,
    device: str = "cpu",
    prefill_tokens: int = 384,
    decode_tokens: int = 64,
    config: PNMixConfig | None = None,
    checkpoint: Path | None = None,
    checkpoint_id: str | None = None,
    checkpoint_revision: str | None = None,
) -> dict[str, Any]:
    """Execute online appends and actual attention; bounded to <= 2048 tokens."""
    config = config or PNMixConfig()
    if prefill_tokens < 1 or decode_tokens < 1 or prefill_tokens + decode_tokens > 2048:
        raise ValueError("require a nonempty prefill/decode and at most 2048 diagnostic tokens")
    device = component_device(device)
    dtype = torch.float16 if device.startswith("cuda") else torch.float32
    start = time.perf_counter()
    if device.startswith("cuda"):
        torch.cuda.reset_peak_memory_stats(device)
    tokens = prefill_tokens + decode_tokens
    if checkpoint is None:
        query, key, value, provenance = initialized_states(
            tokens, seed=seed, device=device, dtype=dtype, pair_layout=config.pair_layout
        )
    else:
        if config.pair_layout != "split":
            raise ValueError("Llama checkpoint states require pair_layout=split")
        query, key, value, provenance = checkpoint_states(
            checkpoint,
            model_id=checkpoint_id or "",
            revision=checkpoint_revision or "",
            tokens=tokens,
            device=device,
            dtype=dtype,
        )
    with torch.no_grad():
        cache = PNMixCache.from_prefill(
            query[..., :prefill_tokens, :],
            key[..., :prefill_tokens, :],
            value[..., :prefill_tokens, :],
            config,
        )
        cache.attention(query[..., :prefill_tokens, :])
        initial_mask = cache.high_pair_mask.clone()
        outputs = []
        for index in range(prefill_tokens, tokens):
            cache.append(key[..., index : index + 1, :], value[..., index : index + 1, :])
            output, _ = cache.attention(query[..., index : index + 1, :])
            outputs.append(output)
        # Compare identical final cache lengths; the explicit causal mask keeps future tokens invisible.
        reference, original_probs = reference_attention(query[..., prefill_tokens:, :], key, value)
        actual, quantized_probs = cache.attention(query[..., prefill_tokens:, :])
        replay_difference = (actual.float() - torch.cat(outputs, -2).float()).abs().max()
        reconstructed_key, reconstructed_value = cache.materialize()
        kl = (
            (
                original_probs
                * (original_probs.clamp_min(1e-30).log() - quantized_probs.clamp_min(1e-30).log())
            )
            .sum(-1)
            .mean()
        )
        metrics = {
            "key_mse": float((key.float() - reconstructed_key.float()).square().mean()),
            "value_mse": float((value.float() - reconstructed_value.float()).square().mean()),
            "attention_kl": float(kl),
            "attention_output_mse": float((actual.float() - reference.float()).square().mean()),
            "attention_output_cosine": float(
                torch.nn.functional.cosine_similarity(
                    actual.float(), reference.float(), dim=-1
                ).mean()
            ),
            "sink_key_max_error": float(
                (
                    reconstructed_key[..., : config.sink_tokens, :]
                    - key[..., : config.sink_tokens, :]
                )
                .abs()
                .max()
            )
            if config.sink_tokens
            else 0.0,
            "saliency_computations": cache.saliency_computations,
            "mask_unchanged_after_decode": bool(torch.equal(initial_mask, cache.high_pair_mask)),
            "actual_attention_calls": decode_tokens + 2,
            "online_vs_final_cache_attention_max_delta": float(replay_difference),
            **cache.storage(),
        }
    if metrics["quantized_tokens"] == 0:
        raise ValueError(
            "diagnostic did not flush a quantized page; increase tokens or reduce group/residual"
        )
    if not metrics["mask_unchanged_after_decode"] or not all(
        math_is_finite(value) for value in metrics.values()
    ):
        raise RuntimeError("nonfinite diagnostic or mutated prefill selection")
    if device.startswith("cuda"):
        torch.cuda.synchronize(device)
    return {
        "schema_version": 2,
        "paper": "pn-mix",
        "arxiv_id": "2610.19605",
        "seed": seed,
        "diagnostic_only": True,
        "evaluation_tier": "l1_mechanism",
        "evidence_scope": "actual_packed_cache_and_attention_component_not_language_capability",
        "protocol": {
            "prefill_tokens": prefill_tokens,
            "decode_tokens": decode_tokens,
            "config": asdict(config),
            "input_precision": str(dtype),
            "saliency_source": "prefill_only",
            "fused_kernel": False,
            "evolve_eligible": False,
        },
        **provenance,
        "metrics": metrics,
        "runtime": {
            "device_kind": "cuda" if device.startswith("cuda") else "cpu",
            "accelerator_model": torch.cuda.get_device_name(device)
            if device.startswith("cuda")
            else None,
            "elapsed_seconds": time.perf_counter() - start,
            "peak_allocated_bytes": torch.cuda.max_memory_allocated(device)
            if device.startswith("cuda")
            else None,
        },
        "full_experiment": {
            "status": "not_reproduced_high_cost",
            "review_done": True,
            "reason": "8B-32B multi-model, up-to-32K-output multi-task sweeps exceed this component-only budget",
        },
    }


def math_is_finite(value: Any) -> bool:
    import math

    return not isinstance(value, (float, int)) or math.isfinite(value)


def reproduce(_dataset_dir: Path, seed: int = 42) -> dict[str, Any]:
    return run_diagnostic(seed=seed, device=component_device())


def render(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    return (
        "# PN-Mix：L1 缓存机制诊断\n\n"
        "量化 K/V 已实际进入 attention；不代表语言任务、吞吐或完整论文效果复现。\n\n"
        f"- seed：{result['seed']}\n"
        f"- attention KL：{metrics['attention_kl']:.6g}\n"
        f"- attention output MSE：{metrics['attention_output_mse']:.6g}\n"
        f"- 量化 token：{metrics['quantized_tokens']}\n"
        "- 完整高成本实验：不复现（审查 DONE）；无自动 Evolve 晋级。\n"
    )
