"""Lazy real-checkpoint teacher used by the CoBA-RL boundary curriculum."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ..runtime import device_for


QWEN25_TEACHER_ID = "Qwen/Qwen2.5-0.5B-Instruct"
QWEN25_TEACHER_REVISION = "7ae557604adf67be50417f59c2c2f167def9a775"


@dataclass(frozen=True)
class TeacherCompletion:
    text: str
    input_tokens: int
    output_tokens: int


class HFTeacherGenerator:
    """Load the public teacher only when a boundary example actually needs it."""

    def __init__(
        self,
        model_id: str,
        revision: str,
        checkpoint_path: Path | None,
        allow_network: bool,
        max_new_tokens: int,
    ):
        self.model_id = model_id
        self.requested_revision = revision
        self.checkpoint_path = checkpoint_path
        self.allow_network = allow_network
        self.max_new_tokens = max_new_tokens
        self.resolved_revision = revision
        self.device = "not_loaded"
        self._tokenizer: Any | None = None
        self._model: Any | None = None
        self._torch: Any | None = None

    def _load(self) -> None:
        if self._model is not None:
            return
        import torch
        from huggingface_hub import model_info
        from transformers import AutoModelForCausalLM, AutoTokenizer

        resolved = self.requested_revision
        if self.checkpoint_path is None and self.allow_network:
            resolved = model_info(self.model_id, revision=resolved).sha
        source = str(self.checkpoint_path or self.model_id)
        kwargs = {
            "revision": resolved,
            "local_files_only": self.checkpoint_path is not None or not self.allow_network,
            "trust_remote_code": False,
        }
        tokenizer = AutoTokenizer.from_pretrained(source, **kwargs)
        device = device_for(torch)
        dtype = torch.float32
        if device.type == "cuda":
            dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16
        elif device.type == "mps":
            dtype = torch.float16
        model = AutoModelForCausalLM.from_pretrained(
            source, dtype=dtype, **kwargs
        ).to(device).eval()
        self._torch, self._tokenizer, self._model = torch, tokenizer, model
        self.device = device.type
        self.resolved_revision = getattr(model.config, "_commit_hash", None) or resolved

    def complete(self, prompt: str) -> TeacherCompletion:
        self._load()
        torch, tokenizer, model = self._torch, self._tokenizer, self._model
        messages = [{
            "role": "user",
            "content": prompt + "\nReturn concise reasoning followed by Answer: <number>.",
        }]
        rendered = tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        inputs = tokenizer(rendered, return_tensors="pt").to(model.device)
        input_tokens = int(inputs["input_ids"].shape[-1])
        with torch.inference_mode():
            generated = model.generate(
                **inputs, do_sample=False, max_new_tokens=self.max_new_tokens
            )
        suffix = generated[0, input_tokens:]
        return TeacherCompletion(
            tokenizer.decode(suffix, skip_special_tokens=True).strip(),
            input_tokens,
            int(len(suffix)),
        )

    def provenance(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "requested_revision": self.requested_revision,
            "resolved_revision": self.resolved_revision,
            "checkpoint_path": (
                "local snapshot (not committed)" if self.checkpoint_path else None
            ),
            "device": self.device,
            "lazy_load": True,
        }
