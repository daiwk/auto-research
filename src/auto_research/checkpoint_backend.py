"""Pinned Hugging Face causal-LM inference shared by reasoning and post-training."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import time

from .runtime import device_for


SMOLLM2_135M_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"
SMOLLM2_135M_REVISION = "12fd25f77366fa6b3b4b768ec3050bf629380bac"


@dataclass(frozen=True)
class GenerationBatch:
    texts: tuple[str, ...]
    generated_tokens: tuple[int, ...]
    latency_seconds: float


class HFCausalLMBackend:
    def __init__(
        self,
        model_id: str = SMOLLM2_135M_ID,
        revision: str = SMOLLM2_135M_REVISION,
        checkpoint_path: Path | None = None,
        *,
        offline: bool = False,
    ):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        self.torch = torch
        self.model_id = model_id
        self.revision = revision
        source = str(checkpoint_path) if checkpoint_path else model_id
        kwargs = {"local_files_only": offline or checkpoint_path is not None, "trust_remote_code": False}
        if checkpoint_path is None:
            kwargs["revision"] = revision
        self.tokenizer = AutoTokenizer.from_pretrained(source, **kwargs)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.device = device_for(torch)
        self.dtype = (
            torch.bfloat16
            if self.device.type == "cuda" and torch.cuda.is_bf16_supported()
            else torch.float32
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            source, torch_dtype=self.dtype, **kwargs
        ).to(self.device)
        self.model.eval()

    def generate(
        self, prompt: str, *, samples: int, max_new_tokens: int,
        seed: int, temperature: float = 0.7,
    ) -> GenerationBatch:
        torch = self.torch
        inputs = self.tokenizer(prompt, return_tensors="pt")
        inputs = {key: value.to(self.device) for key, value in inputs.items()}
        generator = torch.Generator(device=self.device).manual_seed(seed)
        started = time.perf_counter()
        generation_kwargs = {
            "do_sample": samples > 1,
            "num_return_sequences": samples,
            "max_new_tokens": max_new_tokens,
            "pad_token_id": self.tokenizer.pad_token_id,
            "generator": generator,
        }
        if samples > 1:
            generation_kwargs["temperature"] = temperature
        with torch.inference_mode():
            output = self.model.generate(**inputs, **generation_kwargs)
        if self.device.type == "cuda":
            torch.cuda.synchronize(self.device)
        latency = time.perf_counter() - started
        prompt_tokens = inputs["input_ids"].shape[1]
        texts = tuple(
            self.tokenizer.decode(row[prompt_tokens:], skip_special_tokens=True)
            for row in output
        )
        lengths = tuple(
            int((row[prompt_tokens:] != self.tokenizer.pad_token_id).sum()) for row in output
        )
        return GenerationBatch(texts, lengths, latency)

    def provenance(self) -> dict:
        return {
            "model_id": self.model_id,
            "revision": self.revision,
            "device": self.device.type,
            "dtype": str(self.dtype).replace("torch.", ""),
        }
