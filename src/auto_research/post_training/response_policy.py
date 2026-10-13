"""Verified local-checkpoint response likelihoods shared by OPD and proximal RL.

Generation receives messages only. Public reference labels belong to callers'
external training verifiers, never this policy. No silent prompt truncation.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

import torch

from auto_research.oct12_public_sources import checkpoint_source
from .oct10_checkpoint import install_lora


@dataclass(frozen=True)
class GeneratedResponse:
    tokens: tuple[int, ...]
    text: str
    truncated: bool


class ResponsePolicy:
    def __init__(self, *, public_id, revision, checkpoint_path: Path, device="cpu", seed=42,
                 context_limit=4096):
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if context_limit < 2:
            raise ValueError("context budget must allow prompt and response")
        if device.startswith("cuda") and not torch.cuda.is_available():
            raise RuntimeError("CUDA required; no implicit CPU receipt fallback")
        torch.manual_seed(seed)
        source, kwargs, provenance = checkpoint_source(public_id, revision, checkpoint_path)
        self.tokenizer = AutoTokenizer.from_pretrained(source, trust_remote_code=False, **kwargs)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(
            source, trust_remote_code=False, use_safetensors=True,
            torch_dtype=torch.float32 if device == "cpu" else torch.bfloat16,
            attn_implementation="eager", **kwargs).to(device).eval()
        self.model.requires_grad_(False)
        self.device, self.context_limit = device, context_limit
        self.provenance = {"public_id": public_id, "revision": revision, "verified_mirror": provenance}
        self.vocabulary_sha256 = hashlib.sha256(json.dumps(self.tokenizer.get_vocab(), sort_keys=True).encode()).hexdigest()
        self.optimizer = None

    def prompt_ids(self, messages):
        if not messages:
            raise ValueError("a public prompt is required")
        if getattr(self.tokenizer, "chat_template", None):
            text = self.tokenizer.apply_chat_template(list(messages), tokenize=False, add_generation_prompt=True)
        else:
            text = "\n".join(f"{message['role']}: {message['content']}" for message in messages) + "\nassistant:"
        ids = self.tokenizer(text, add_special_tokens=False, return_tensors="pt").input_ids.to(self.device)
        if ids.shape[1] >= self.context_limit:
            raise ValueError("complete history exceeds context budget; it is not silently truncated")
        return ids

    def generate(self, messages, *, samples=1, max_tokens=512, sample=True):
        if min(samples, max_tokens) < 1:
            raise ValueError("positive response sampling budget required")
        prompt = self.prompt_ids(messages)
        budget = min(max_tokens, self.context_limit - prompt.shape[1])
        self.model.eval()
        with torch.no_grad():
            output = self.model.generate(prompt, attention_mask=torch.ones_like(prompt),
                max_new_tokens=budget, do_sample=sample, num_return_sequences=samples,
                **({"temperature": 1., "top_p": 1., "top_k": 0} if sample else {}),
                pad_token_id=self.tokenizer.pad_token_id, use_cache=True)
        responses = []
        for row in output:
            tokens = row[prompt.shape[1]:]
            eos = torch.where(tokens == self.tokenizer.eos_token_id)[0]
            if len(eos):
                tokens = tokens[:int(eos[0]) + 1]
            values = tuple(map(int, tokens.cpu().tolist()))
            responses.append(GeneratedResponse(values, self.tokenizer.decode(tokens, skip_special_tokens=True),
                                                not len(eos) and len(values) >= budget))
        return responses

    def token_statistics(self, messages, tokens, *, entropy=False):
        if not tokens:
            raise ValueError("empty response cannot be scored")
        prompt = self.prompt_ids(messages)[0]
        response = torch.tensor(tokens, device=self.device)
        if len(prompt) + len(response) > self.context_limit:
            raise ValueError("same-prefix response exceeds context budget")
        ids = torch.cat((prompt, response))[None]
        logits = self.model(ids, attention_mask=torch.ones_like(ids), use_cache=False).logits[
            0, len(prompt) - 1:-1].float()
        log_probabilities = logits.log_softmax(-1)
        selected = log_probabilities.gather(-1, response[:, None])[:, 0]
        full_entropy = -(log_probabilities.exp() * log_probabilities).sum(-1) if entropy else None
        return selected, full_entropy

    def trainable_digest(self):
        digest = hashlib.sha256()
        for name, value in self.model.named_parameters():
            if value.requires_grad:
                digest.update(name.encode())
                digest.update(value.detach().float().cpu().contiguous().numpy().tobytes())
        return digest.hexdigest()

    def prepare_lora(self, *, rank=8, learning_rate=1e-5):
        if self.optimizer is not None:
            raise ValueError("LoRA optimizer already initialized")
        count = install_lora(self.model, rank=rank)
        self.model.config.use_cache = False
        self.model.gradient_checkpointing_enable(gradient_checkpointing_kwargs={"use_reentrant": False})
        self.optimizer = torch.optim.AdamW([p for p in self.model.parameters() if p.requires_grad], lr=learning_rate)
        return count

    def update(self, summed_response_losses, supervised_tokens):
        if self.optimizer is None or supervised_tokens < 1:
            raise ValueError("trainable policy and actual supervised response tokens required")
        self.model.train()
        self.optimizer.zero_grad(set_to_none=True)
        total_loss = 0.
        for loss in summed_response_losses:
            scaled = loss / supervised_tokens
            scaled.backward()
            total_loss += float(scaled.detach())
        torch.nn.utils.clip_grad_norm_([p for p in self.model.parameters() if p.requires_grad], 1.)
        self.optimizer.step()
        self.model.eval()
        return total_loss
