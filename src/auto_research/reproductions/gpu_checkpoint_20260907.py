"""Real-checkpoint validation shared by BeaconKV and KVMem."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics


def _layers(cache):
    if hasattr(cache, "layers"):
        return [(layer.keys, layer.values) for layer in cache.layers]
    if hasattr(cache, "key_cache"):
        return list(zip(cache.key_cache, cache.value_cache))
    return list(cache)


def _attend(query, keys, values, indices, torch):
    weights = torch.softmax(keys[indices].float() @ query.float() / keys.shape[-1] ** 0.5, dim=0)
    return weights @ values[indices].float()


def run(method: str, *, output: Path, model_id: str, revision: str, sequence_length: int,
        retained_tokens: int, seed: int, local_files_only: bool):
    import torch
    from huggingface_hub import model_info, snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from .beaconkv.model import beacon_retained_indices
    from .kvmem.model import select_workspace_blocks

    torch.manual_seed(seed)
    resolved_revision = revision if local_files_only else model_info(model_id, revision=revision).sha
    checkpoint_source = (
        snapshot_download(model_id, revision=resolved_revision, local_files_only=True)
        if local_files_only else model_id
    )
    tokenizer = AutoTokenizer.from_pretrained(
        checkpoint_source,
        revision=None if local_files_only else resolved_revision,
        local_files_only=local_files_only,
    )
    model = AutoModelForCausalLM.from_pretrained(
        checkpoint_source,
        revision=None if local_files_only else resolved_revision,
        dtype=torch.bfloat16,
        local_files_only=local_files_only,
    ).cuda().eval()
    corpus = "To be, or not to be, that is the question. " * 9000
    token_ids = tokenizer(corpus, return_tensors="pt", add_special_tokens=False).input_ids[0][:sequence_length][None].cuda()
    torch.cuda.reset_peak_memory_stats()
    with torch.inference_mode():
        result = model(token_ids, use_cache=True, output_hidden_states=True)
    layers = _layers(result.past_key_values)
    records = []
    for layer_index in sorted({0, len(layers) // 2, len(layers) - 1}):
        layer = model.model.layers[layer_index]
        hidden = result.hidden_states[layer_index]
        q_heads = model.config.num_attention_heads
        kv_heads = model.config.num_key_value_heads
        head_dim = layer.self_attn.head_dim
        with torch.inference_mode():
            normalized_hidden = layer.input_layernorm(hidden)
            queries = (
                layer.self_attn.q_proj(normalized_hidden)[0]
                .view(sequence_length, q_heads, head_dim)
                .transpose(0, 1)
            )
        queries = queries.view(kv_heads, q_heads // kv_heads, sequence_length, head_dim).mean(1)
        keys, values = layers[layer_index][0][0], layers[layer_index][1][0]
        for head in range(kv_heads):
            query = queries[head, -1]
            if method == "beaconkv":
                chosen = beacon_retained_indices(
                    keys[head], queries[head], retained_tokens,
                    beacon_count=8, recent_tokens=min(128, retained_tokens // 2),
                )
                extra = {"beacon_count": 8}
            else:
                chosen, blocks, _ = select_workspace_blocks(
                    keys[head], query, block_size=32,
                    selected_blocks=max(1, retained_tokens // 32),
                )
                chosen = chosen[:retained_tokens]
                extra = {"materialized_blocks": int(len(blocks)), "virtualization_tiers": 3}
            recent = torch.arange(sequence_length - retained_tokens, sequence_length, device=keys.device)
            full = _attend(query, keys[head], values[head], torch.arange(sequence_length, device=keys.device), torch)
            records.append({
                "layer": layer_index,
                "head": head,
                "baseline_attention_cosine": float(torch.nn.functional.cosine_similarity(full, _attend(query, keys[head], values[head], recent, torch), dim=0)),
                "method_attention_cosine": float(torch.nn.functional.cosine_similarity(full, _attend(query, keys[head], values[head], chosen, torch), dim=0)),
                "retained_tokens": int(len(chosen)),
                **extra,
            })
    mean = lambda key: statistics.fmean(row[key] for row in records)
    payload = {
        "schema_version": 3,
        "method": f"{method}-real-checkpoint",
        "dataset": {"name": "fixed public-domain long-context probe", "revision": "public-domain-long-context-v1", "examples": 1, "sequence_length": sequence_length},
        "checkpoint": {"model_id": model_id, "revision": resolved_revision},
        "setup": {"seed": seed, "retained_tokens": retained_tokens},
        "metrics": {"baseline_attention_cosine_mean": mean("baseline_attention_cosine"), "method_attention_cosine_mean": mean("method_attention_cosine"), "retained_tokens": retained_tokens, "evaluated_head_layers": len(records), "peak_gpu_memory_mb": torch.cuda.max_memory_allocated() / 1024 ** 2},
        "records": records,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Real Qwen checkpoint query/KV tensors and fixed public-domain text; mechanism diagnostic, not the full paper serving matrix.",
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return payload


def main(method: str) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model-id", default="Qwen/Qwen3-4B-Instruct-2507")
    parser.add_argument("--revision", default="main")
    parser.add_argument("--sequence-length", type=int, default=1024)
    parser.add_argument("--retained-tokens", type=int, default=256)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--local-files-only", action="store_true")
    args = parser.parse_args()
    metrics = run(method, **vars(args))["metrics"]
    print(json.dumps(metrics, indent=2))
    return 0
