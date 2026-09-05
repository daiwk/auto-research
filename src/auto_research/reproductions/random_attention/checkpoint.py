"""Real-checkpoint equal-budget Random Attention validation."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import statistics
import time

from .model import random_retained_indices, recent_retained_indices


@dataclass(frozen=True)
class Config:
    output: Path
    model_id: str = "Qwen/Qwen2.5-0.5B-Instruct"
    revision: str = "main"
    dataset_id: str = "Salesforce/wikitext"
    dataset_revision: str = "main"
    examples: int = 3
    sequence_length: int = 2048
    prompt_tokens: int = 256
    retention_ratio: float = 0.5
    seed: int = 42


def _layers(cache):
    if hasattr(cache, "layers"):
        return [(x.keys, x.values) for x in cache.layers]
    if hasattr(cache, "key_cache"):
        return list(zip(cache.key_cache, cache.value_cache))
    return list(cache)


def _output(query, keys, values, indices, torch):
    scores = keys[indices].float() @ query.float() / keys.shape[-1] ** 0.5
    return torch.softmax(scores, 0) @ values[indices].float()


def run(config: Config):
    import torch
    from datasets import load_dataset
    from huggingface_hub import dataset_info, model_info
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.manual_seed(config.seed)
    model_revision = model_info(config.model_id, revision=config.revision).sha
    data_revision = dataset_info(config.dataset_id, revision=config.dataset_revision).sha
    tokenizer = AutoTokenizer.from_pretrained(config.model_id, revision=model_revision)
    model = AutoModelForCausalLM.from_pretrained(
        config.model_id, revision=model_revision, torch_dtype=torch.bfloat16
    ).cuda().eval()
    corpus = "\n".join(x["text"] for x in load_dataset(
        config.dataset_id, "wikitext-2-raw-v1", revision=data_revision, split="test"
    ) if x["text"].strip())
    token_ids = tokenizer(corpus, return_tensors="pt", add_special_tokens=False).input_ids[0]
    budget = round(config.sequence_length * config.retention_ratio)
    records=[]
    torch.cuda.reset_peak_memory_stats()
    for example in range(config.examples):
        ids=token_ids[example*config.sequence_length:(example+1)*config.sequence_length][None].cuda()
        with torch.inference_mode(): out=model(ids,use_cache=True)
        layers=_layers(out.past_key_values)
        for layer in sorted({0,len(layers)//2,len(layers)-1}):
            keys,values=layers[layer][0][0],layers[layer][1][0]
            heads=keys.shape[0]
            start=time.perf_counter(); recent=recent_retained_indices(len(keys[0]),budget,prompt_tokens=config.prompt_tokens,heads=heads,device=keys.device); torch.cuda.synchronize(); recent_time=time.perf_counter()-start
            start=time.perf_counter(); random=random_retained_indices(len(keys[0]),budget,prompt_tokens=config.prompt_tokens,heads=heads,seed=config.seed+example*100+layer,device=keys.device); torch.cuda.synchronize(); random_time=time.perf_counter()-start
            full=[]; base=[]; method=[]
            for head in range(heads):
                q=keys[head,-1]
                all_idx=torch.arange(keys.shape[-2],device=keys.device)
                full.append(_output(q,keys[head],values[head],all_idx,torch))
                base.append(_output(q,keys[head],values[head],recent[head],torch))
                method.append(_output(q,keys[head],values[head],random[head],torch))
            full,base,method=map(torch.stack,(full,base,method))
            records.append({"baseline_attention_cosine":float(torch.nn.functional.cosine_similarity(full.flatten(),base.flatten(),dim=0)),"random_attention_cosine":float(torch.nn.functional.cosine_similarity(full.flatten(),method.flatten(),dim=0)),"baseline_selection_seconds":recent_time,"random_selection_seconds":random_time,"independent_head_patterns":int(torch.unique(random,dim=0).shape[0])})
    mean=lambda k:statistics.fmean(r[k] for r in records)
    payload={"schema_version":3,"method":"random-attention-real-checkpoint","dataset":{"name":config.dataset_id,"config":"wikitext-2-raw-v1","revision":data_revision,"examples":config.examples,"sequence_length":config.sequence_length},"checkpoint":{"model_id":config.model_id,"revision":model_revision},"setup":{"seed":config.seed,"prompt_tokens":config.prompt_tokens,"retained_tokens":budget},"metrics":{"baseline_attention_cosine_mean":mean("baseline_attention_cosine"),"random_attention_cosine_mean":mean("random_attention_cosine"),"baseline_selection_seconds_mean":mean("baseline_selection_seconds"),"random_selection_seconds_mean":mean("random_selection_seconds"),"independent_head_patterns_mean":mean("independent_head_patterns"),"retained_tokens":budget,"peak_gpu_memory_mb":torch.cuda.max_memory_allocated()/1024**2},"records":records,"created_at":datetime.now(timezone.utc).isoformat(),"scope":"Real Qwen KV tensors and public WikiText-2; reconstruction/selection diagnostic, not the paper's vLLM throughput matrix."}
    config.output.parent.mkdir(parents=True,exist_ok=True); config.output.write_text(json.dumps(payload,indent=2)+"\n"); return payload


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True); p.add_argument("--model-id",default=Config.model_id); p.add_argument("--revision",default="main"); p.add_argument("--dataset-id",default=Config.dataset_id); p.add_argument("--dataset-revision",default="main"); p.add_argument("--examples",type=int,default=3); p.add_argument("--sequence-length",type=int,default=2048); p.add_argument("--prompt-tokens",type=int,default=256); p.add_argument("--retention-ratio",type=float,default=.5); p.add_argument("--seed",type=int,default=42)
    print(json.dumps(run(Config(**vars(p.parse_args())))["metrics"],indent=2)); return 0


if __name__ == "__main__": raise SystemExit(main())
