"""Pinned local causal-LM inference; never called by the online serving path."""

from __future__ import annotations


MODEL_ID = "Qwen/Qwen2.5-7B-Instruct"
REVISION = "bb46c15ee4bb56c5b63245ef50fd7637234d6f75"


class LocalGenerator:
    def __init__(self, *, model_id: str = MODEL_ID, revision: str = REVISION,
                 device: str = "cpu", max_new_tokens: int = 192,
                 model_path: str | None = None):
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if device not in {"cpu", "cuda", "cuda:0"}:
            raise ValueError("music rationale generation supports CPU or CUDA:0")
        if device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA was requested but no CUDA device is available")
        self.torch = torch
        self.device = device
        self.max_new_tokens = max_new_tokens
        source = model_path or model_id
        kwargs = {"local_files_only": True}
        if model_path is None:
            kwargs["revision"] = revision
        self.tokenizer = AutoTokenizer.from_pretrained(source, **kwargs)
        # BF16 avoids doubling a 7B checkpoint to ~28 GB on CPU. CPU kernels
        # are slower, but this is an offline cache-generation path.
        dtype = torch.bfloat16
        self.model = AutoModelForCausalLM.from_pretrained(
            source, dtype=dtype, **kwargs,
        ).to(device).eval()

    def __call__(self, prompt: str) -> str:
        encoded = self.tokenizer.apply_chat_template(
            [{"role": "system", "content": "Return compact valid JSON; no markdown."},
             {"role": "user", "content": prompt}],
            add_generation_prompt=True, return_tensors="pt",
        )
        tokens = (encoded["input_ids"] if hasattr(encoded, "keys") else encoded).to(self.device)
        with self.torch.inference_mode():
            result = self.model.generate(
                tokens, max_new_tokens=self.max_new_tokens, do_sample=False,
                attention_mask=self.torch.ones_like(tokens),
                pad_token_id=self.tokenizer.eos_token_id,
            )
        return self.tokenizer.decode(result[0, tokens.shape[1]:], skip_special_tokens=True)
