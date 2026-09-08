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
    from transformers.models.qwen3.modeling_qwen3 import apply_rotary_pos_emb

    from .beaconkv.model import beacon_retained_indices
    from .kvmem.model import select_workspace_blocks

    if method not in {"beaconkv", "kvmem"}:
        raise ValueError(f"Unsupported method: {method}")
    if not 0 < retained_tokens <= sequence_length:
        raise ValueError("Require 0 < retained_tokens <= sequence_length")
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
        attn_implementation="eager",
    ).cuda().eval()
    if model.config.model_type != "qwen3":
        raise ValueError("This attention parity probe supports Qwen3 only")
    corpus = "To be, or not to be, that is the question. " * 9000
    token_ids = tokenizer(corpus, return_tensors="pt", add_special_tokens=False).input_ids[0][:sequence_length][None].cuda()
    layer_indices = sorted({0, len(model.model.layers) // 2, len(model.model.layers) - 1})
    hidden_by_layer = {}
    positions_by_layer = {}
    outputs_by_layer = {}
    hooks = []
    for layer_index in layer_indices:
        def capture_input(_module, args, kwargs, *, index=layer_index):
            hidden_by_layer[index] = kwargs["hidden_states"].detach()
            positions_by_layer[index] = kwargs["position_embeddings"]

        def capture_output(_module, args, *, index=layer_index):
            outputs_by_layer[index] = args[0].detach()

        attention = model.model.layers[layer_index].self_attn
        hooks.append(attention.register_forward_pre_hook(capture_input, with_kwargs=True))
        hooks.append(attention.o_proj.register_forward_pre_hook(capture_output))
    torch.cuda.reset_peak_memory_stats()
    try:
        with torch.inference_mode():
            result = model(token_ids, use_cache=True)
    finally:
        for hook in hooks:
            hook.remove()
    sequence_length = token_ids.shape[-1]
    layers = _layers(result.past_key_values)
    records = []
    for layer_index in layer_indices:
        layer = model.model.layers[layer_index]
        hidden = hidden_by_layer[layer_index]
        q_heads = model.config.num_attention_heads
        kv_heads = model.config.num_key_value_heads
        head_dim = layer.self_attn.head_dim
        with torch.inference_mode():
            projected_queries = layer.self_attn.q_proj(hidden)
            queries = layer.self_attn.q_norm(
                projected_queries.reshape(1, sequence_length, q_heads, head_dim)
            ).transpose(1, 2)
            cos, sin = positions_by_layer[layer_index]
            queries, _ = apply_rotary_pos_emb(queries, queries, cos, sin)
            queries = queries[0]
        keys, values = layers[layer_index][0][0], layers[layer_index][1][0]
        actual = outputs_by_layer[layer_index].reshape(1, sequence_length, q_heads, head_dim)[0, -1]
        for head in range(q_heads):
            kv_head = head // (q_heads // kv_heads)
            head_keys, head_values = keys[kv_head], values[kv_head]
            query = queries[head, -1]
            if method == "beaconkv":
                chosen = beacon_retained_indices(
                    head_keys, queries[head], retained_tokens,
                    beacon_count=8, recent_tokens=min(128, retained_tokens // 2),
                )
                extra = {"beacon_count": 8}
            else:
                chosen, blocks, _ = select_workspace_blocks(
                    head_keys, query, block_size=32,
                    selected_blocks=max(1, retained_tokens // 32),
                )
                chosen = chosen[:retained_tokens]
                extra = {"materialized_blocks": int(len(blocks))}
            recent = torch.arange(sequence_length - retained_tokens, sequence_length, device=keys.device)
            full = _attend(query, head_keys, head_values, torch.arange(sequence_length, device=keys.device), torch)
            parity_error = float((full - actual[head].float()).abs().max())
            if not torch.allclose(full, actual[head].float(), atol=0.02, rtol=0.02):
                raise AssertionError(f"Full attention parity failed at layer {layer_index}, head {head}: {parity_error}")
            records.append({
                "layer": layer_index,
                "head": head,
                "kv_head": kv_head,
                "full_attention_max_abs_error": parity_error,
                "baseline_attention_cosine": float(torch.nn.functional.cosine_similarity(full, _attend(query, head_keys, head_values, recent, torch), dim=0)),
                "method_attention_cosine": float(torch.nn.functional.cosine_similarity(full, _attend(query, head_keys, head_values, chosen, torch), dim=0)),
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
