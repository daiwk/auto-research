"""Task-level KV reference backend: WikiText next-token likelihood/accuracy.

The backing cache deliberately remains complete. Workspace selection changes
the actual attention used for decoding, but this Python evaluator does NOT
claim end-to-end KV memory savings or reproduce a production serving system.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import random
import time

from .beaconkv.model import beacon_retained_indices
from .kvmem.model import select_workspace_blocks


@contextmanager
def attention_workspace(method, budget):
    import torch
    import transformers.models.qwen3.modeling_qwen3 as qwen

    original = qwen.eager_attention_forward
    anchors = {}

    def attention(module, query, key, value, attention_mask, **kwargs):
        if query.shape[-2] > 1:
            # Preserve real per-head prefill queries, never averaged GQA heads.
            anchors[module.layer_idx] = query.detach()[:, :, ::max(1, query.shape[-2] // 32)]
        if method == "full" or query.shape[-2] != 1 or key.shape[-2] <= budget:
            return original(module, query, key, value, attention_mask, **kwargs)
        group = query.shape[1] // key.shape[1]
        retained_keys, retained_values = [], []
        for head in range(key.shape[1]):
            keys = key[0, head]
            if method == "recent":
                chosen = torch.arange(len(keys) - budget, len(keys), device=keys.device)
            elif method == "beaconkv":
                historical = anchors[module.layer_idx][0, head * group:(head + 1) * group]
                chosen = beacon_retained_indices(keys, historical.reshape(-1, keys.shape[-1]),
                                                  budget, beacon_count=8,
                                                  recent_tokens=min(128, budget // 2))
            elif method == "kvmem":
                # Evaluate each query head and union its candidates. Rank union
                # by max per-query similarity instead of collapsing GQA queries.
                candidates = []
                for q in query[0, head * group:(head + 1) * group, 0]:
                    selected, _, _ = select_workspace_blocks(keys, q, block_size=32,
                                                             selected_blocks=max(1, budget // 32))
                    candidates.append(selected)
                union = torch.unique(torch.cat(candidates))
                scores = torch.nn.functional.normalize(keys[union].float(), dim=-1) @ torch.nn.functional.normalize(
                    query[0, head * group:(head + 1) * group, 0].float(), dim=-1).T
                chosen = union[scores.max(-1).values.topk(min(budget, len(union))).indices].sort().values
                # Preserve an exact matched token budget even for short blocks.
                if len(chosen) < budget:
                    missing = torch.ones(len(keys), dtype=torch.bool, device=keys.device)
                    missing[chosen] = False
                    chosen = torch.cat((chosen, torch.arange(len(keys), device=keys.device)[missing][-budget + len(chosen):])).sort().values
            else:
                raise ValueError(f"unknown KV method: {method}")
            retained_keys.append(keys[chosen])
            retained_values.append(value[0, head, chosen])
        # One autoregressive query may attend to all retained past positions;
        # original RoPE positions stay in the cached keys.
        return original(module, query, torch.stack(retained_keys)[None],
                        torch.stack(retained_values)[None], None, **kwargs)

    qwen.eager_attention_forward = attention
    try:
        yield
    finally:
        qwen.eager_attention_forward = original


def run(output, seed=42, context_tokens=2048, target_tokens=32, examples=6, budget=512, dataset_file=None):
    import torch
    from datasets import load_dataset
    from huggingface_hub import snapshot_download
    from transformers import AutoModelForCausalLM, AutoTokenizer

    from ..agent_research.coskill_checkpoint import MODEL, REVISION

    if not 32 <= budget < context_tokens or target_tokens < 1 or examples < 2:
        raise ValueError("require 32 <= budget < context and multiple examples")
    torch.manual_seed(seed)
    dataset_id = "Salesforce/wikitext"
    if dataset_file:
        payload = json.loads(Path(dataset_file).read_text())
        corpus, dataset_revision = payload["text"], payload["revision"]
        if (payload["id"] != dataset_id or payload["config"] != "wikitext-2-raw-v1"
                or payload["split"] != "test"
                or hashlib.sha256(corpus.encode()).hexdigest() != payload["sha256"]):
            raise ValueError("invalid public WikiText dataset identity/checksum")
    else:
        dataset_revision = "b08601e04326c79dfdd32d625aee71d232d685c3"
        dataset = load_dataset(dataset_id, "wikitext-2-raw-v1", split="test", revision=dataset_revision)
        corpus = "\n".join(row["text"] for row in dataset)
    checkpoint = snapshot_download(MODEL, revision=REVISION, local_files_only=True)
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, local_files_only=True)
    model = AutoModelForCausalLM.from_pretrained(checkpoint, local_files_only=True,
                                                torch_dtype=torch.bfloat16, attn_implementation="eager").cuda().eval()
    tokens = tokenizer(corpus, add_special_tokens=False).input_ids
    width = context_tokens + target_tokens
    if len(tokens) < examples * width:
        raise ValueError("not enough non-overlapping evaluation text")
    rows = []
    # Warm up model kernels outside timed records; rotate method order to avoid
    # attributing first-run initialization or thermal drift to one backend.
    with torch.inference_mode():
        warmup = model(torch.tensor(tokens[:64], device="cuda")[None], use_cache=True)
        del warmup
    torch.cuda.synchronize()
    rng = random.Random(seed)
    for example in range(examples):
        ids = torch.tensor(tokens[example * width:(example + 1) * width], device="cuda")[None]
        methods = ["full", "recent", "beaconkv", "kvmem"]
        rng.shuffle(methods)
        for order, method in enumerate(methods):
            torch.cuda.synchronize()
            torch.cuda.reset_peak_memory_stats()
            started = time.monotonic()
            losses, correct = [], 0
            with torch.inference_mode(), attention_workspace(method, budget):
                prediction = model(ids[:, :context_tokens], use_cache=True)
                cache = prediction.past_key_values
                logits = prediction.logits[:, -1]
                del prediction
                torch.cuda.synchronize()
                prefill_seconds = time.monotonic() - started
                for index in range(target_tokens):
                    target = ids[:, context_tokens + index]
                    losses.append(float(torch.nn.functional.cross_entropy(logits.float(), target)))
                    correct += int((logits.argmax(-1) == target).sum())
                    if index + 1 < target_tokens:
                        prediction = model(target[:, None], past_key_values=cache, use_cache=True,
                                           cache_position=torch.tensor([context_tokens + index], device="cuda"))
                        logits, cache = prediction.logits[:, -1], prediction.past_key_values
                        del prediction
                torch.cuda.synchronize()
                elapsed = time.monotonic() - started
                rows.append({"example": example, "method": method,
                             "execution_order": order,
                             "context_tokens": context_tokens, "workspace_budget": None if method == "full" else budget,
                             "tokens": target_tokens, "nll": sum(losses) / len(losses),
                             "next_token_accuracy": correct / target_tokens,
                             "prefill_seconds": prefill_seconds, "total_seconds": elapsed,
                             "peak_allocated_bytes": torch.cuda.max_memory_allocated()})
                print(json.dumps(rows[-1]), flush=True)
            del cache, logits
            torch.cuda.empty_cache()
    result = {"schema_version": 1, "seed": seed, "records": rows,
              "checkpoint": {"model_id": MODEL, "revision": REVISION},
              "dataset": {"id": dataset_id, "config": "wikitext-2-raw-v1", "split": "test",
                          "revision": dataset_revision, "text_sha256": hashlib.sha256(corpus.encode()).hexdigest()},
              "accelerator": torch.cuda.get_device_name(),
              "scope": "task-level next-token reference evaluation; full backing cache, no memory-saving claim"}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--context-tokens", type=int, default=2048)
    parser.add_argument("--examples", type=int, default=6)
    parser.add_argument("--dataset-file", type=Path)
    args = parser.parse_args()
    run(**vars(args))
