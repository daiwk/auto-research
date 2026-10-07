"""Pinned, frozen checkpoints for program search and failure-recovery experiments."""

from __future__ import annotations

from pathlib import Path
import time

from .frugalevo import Completion


SMALL_MODEL = "Qwen/Qwen3-4B-Instruct-2507"
SMALL_REVISION = "cdbee75f17c01a7cc42f958dc650907174af0554"
LARGE_MODEL = "Qwen/Qwen2.5-7B-Instruct"
LARGE_REVISION = "bb46c15ee4bb56c5b63245ef50fd7637234d6f75"


class FrozenGenerator:
    requires_gpu_validation = True
    gpu_validation_artifact = "docs/gpu-validations/oct07-agent-search-a100.json"

    def __init__(self, model_id: str, revision: str, *, path: Path | None = None,
                 token_weight: float = 1.0):
        import torch
        from huggingface_hub import snapshot_download
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if token_weight <= 0:
            raise ValueError("token weight must be positive")
        if not torch.cuda.is_available():
            raise RuntimeError("this validation runner requires a real CUDA device")
        source = str(path) if path else snapshot_download(model_id, revision=revision, local_files_only=True)
        self.torch, self.weight = torch, token_weight
        self.model_id, self.revision = model_id, revision
        self.tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=True, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(
            source, local_files_only=True, trust_remote_code=False, torch_dtype=torch.bfloat16,
            attn_implementation="sdpa",
        ).cuda().eval().requires_grad_(False)
        self.calls = []

    def _tokens(self, prompt):
        rendered = self.tokenizer.apply_chat_template(
            [{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
        return self.tokenizer(rendered, return_tensors="pt")

    def upper_cost(self, prompt, max_tokens):
        return (self._tokens(prompt).input_ids.shape[-1] + max_tokens) * self.weight

    def generate(self, prompt, max_tokens, seed):
        torch = self.torch
        inputs = self._tokens(prompt).to("cuda")
        length = int(inputs.input_ids.shape[-1])
        if length + max_tokens > self.model.config.max_position_embeddings:
            raise ValueError("prompt exceeds checkpoint context; no silent truncation")
        torch.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        started = time.monotonic()
        with torch.inference_mode():
            outputs = self.model.generate(
                **inputs, do_sample=True, temperature=0.7, top_p=0.95,
                max_new_tokens=max_tokens, pad_token_id=self.tokenizer.eos_token_id,
            )
        torch.cuda.synchronize()
        ids = outputs[0, length:]
        result = Completion(self.tokenizer.decode(ids, skip_special_tokens=True), length,
                            int(ids.numel()), (length + int(ids.numel())) * self.weight)
        self.calls.append({"seed": seed, "input_tokens": length, "output_tokens": int(ids.numel()),
                           "elapsed_seconds": time.monotonic() - started})
        return result

    def provenance(self):
        return {"model_id": self.model_id, "revision": self.revision,
                "token_weight": self.weight, "cost_unit": "weighted input+output tokens; not USD",
                "cached_input_tokens": 0, "prefix_kv_cache_implemented": False}
