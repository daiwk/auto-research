"""CausalArmor Eq. 2/5/6: bounded LOO attribution and fail-closed intervention.

No tool is executed here. Scoring is a proxy likelihood, not a proof of causality
or a validated injection classifier. Sanitizer/agent callbacks remain explicit.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import math
from pathlib import Path
import re
from typing import Callable, Protocol

PROTOCOL = "causal-armor-loo-component-v1"


@dataclass(frozen=True)
class Turn:
    role: str
    content: str
    untrusted: bool = False

    def __post_init__(self):
        if self.role not in {"user", "system", "assistant", "tool"}:
            raise ValueError("unsupported role")
        if not isinstance(self.content, str):
            raise ValueError("text content required")
        if self.untrusted and self.role != "tool":
            raise ValueError("this bounded protocol treats tool outputs as untrusted spans")


class Scorer(Protocol):
    def score_batch(self, contexts: tuple[tuple[Turn, ...], ...], action: str
                    ) -> tuple[tuple[float, ...], int]: ...


@dataclass(frozen=True)
class Attribution:
    user_influence: float
    span_influences: tuple[tuple[int, float], ...]
    flagged_indices: tuple[int, ...]
    action_tokens: int
    scoring_contexts: int


def attribute(turns: tuple[Turn, ...], action: str, scorer: Scorer, *, tau: float = 0
              ) -> Attribution:
    """One batch: full, user-removed, then one untrusted-turn removal per span."""
    users = [i for i, turn in enumerate(turns) if turn.role == "user"]
    spans = [i for i, turn in enumerate(turns) if turn.untrusted]
    if len(users) != 1 or not action or not math.isfinite(tau) or len(spans) > 8:
        raise ValueError("one user, nonempty action, finite tau and <=8 spans required")
    contexts = (turns, tuple(t for i, t in enumerate(turns) if i != users[0])) + tuple(
        tuple(t for j, t in enumerate(turns) if j != i) for i in spans)
    scores, tokens = scorer.score_batch(contexts, action)
    if len(scores) != len(contexts) or tokens < 1 or any(not math.isfinite(x) for x in scores):
        raise ValueError("scorer must return finite summed action log-likelihoods")
    delta_user = (scores[0] - scores[1]) / tokens
    influences = tuple((i, (scores[0] - score) / tokens)
                       for i, score in zip(spans, scores[2:], strict=True))
    flagged = tuple(i for i, influence in influences if influence > delta_user - tau)
    return Attribution(delta_user, influences, flagged, tokens, len(contexts))


@dataclass(frozen=True)
class Intervention:
    status: str
    proposed_action: str
    action: str | None
    turns: tuple[Turn, ...]
    attribution: Attribution | None
    sanitizer_observed: bool
    regeneration_observed: bool


def guard(turns: tuple[Turn, ...], action: str, scorer: Scorer, *, privileged: bool,
          tau: float = 0,
          sanitizer: Callable[[str, str, str], str] | None = None,
          regenerate: Callable[[tuple[Turn, ...]], str] | None = None) -> Intervention:
    """Flagged action is withheld if either model callback is not supplied.

    Replacing post-hit assistant messages is deliberately conservative: this
    bounded format does not expose hidden CoT or parse mixed tool-call messages.
    """
    if not privileged or not any(t.untrusted for t in turns):
        return Intervention("not_checked", action, action, turns, None, False, False)
    result = attribute(turns, action, scorer, tau=tau)
    if not result.flagged_indices:
        return Intervention("not_flagged", action, action, turns, result, False, False)
    if sanitizer is None or regenerate is None:
        return Intervention("intervention_required", action, None, turns, result, False, False)
    user = next(t.content for t in turns if t.role == "user")
    sanitized = list(turns)
    for i in result.flagged_indices:
        text = sanitizer(user, action, turns[i].content)
        if not isinstance(text, str):
            raise ValueError("sanitizer must return text")
        sanitized[i] = replace(turns[i], content=text)
    first = min(result.flagged_indices)
    for i in range(first + 1, len(sanitized)):
        if sanitized[i].role == "assistant":
            sanitized[i] = replace(sanitized[i], content="[Reasoning redacted for security]")
    updated = tuple(sanitized)
    new_action = regenerate(updated)
    if not isinstance(new_action, str) or not new_action.strip():
        raise ValueError("regeneration must return a nonempty proposed action")
    return Intervention("regenerated_not_executed", action, new_action, updated, result, True, True)


def render_context(turns: tuple[Turn, ...]) -> str:
    """Explicit text protocol shared by all ablations; no tokenizer chat fallback."""
    return "\n".join(f"[{t.role}]\n{t.content}" for t in turns) + "\n[assistant action]\n"


class CachedLikelihoodScorer:
    """Real causal-LM teacher-forced likelihood; no download or generation.

    Fixed target tokenization across every ablation. Prefix tokens are never
    truncated silently. A single batch has <=10 contexts, each <=512 tokens.
    This backend is optional and lazily imports torch/transformers.
    """
    def __init__(self, checkpoint: str, *, revision: str, device: str = "cpu",
                 max_context_tokens: int = 384):
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            raise ValueError("exact public model revision required")
        if not Path(checkpoint).is_dir() or not 32 <= max_context_tokens <= 512:
            raise ValueError("existing local checkpoint and <=512 context cap required")
        if device not in {"cpu", "cuda"}:
            raise ValueError("device must be cpu or cuda")
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if device == "cuda" and not torch.cuda.is_available():
            raise RuntimeError("CUDA requested but not available")
        self.torch, self.device, self.max_context_tokens = torch, device, max_context_tokens
        self.tokenizer = AutoTokenizer.from_pretrained(
            checkpoint, revision=revision, local_files_only=True, trust_remote_code=False)
        self.model = AutoModelForCausalLM.from_pretrained(
            checkpoint, revision=revision, local_files_only=True, trust_remote_code=False,
            torch_dtype=torch.float32 if device == "cpu" else torch.bfloat16).to(device).eval()
        self.accelerator = torch.cuda.get_device_name() if device == "cuda" else "cpu"
        self.calls = 0

    def score_batch(self, contexts, action):
        if not 1 <= len(contexts) <= 10:
            raise ValueError("<=10 bounded LOO contexts required")
        target = self.tokenizer.encode(action, add_special_tokens=False)
        if not 1 <= len(target) <= 48:
            raise ValueError("action target must contain 1..48 tokens")
        prefixes = [self.tokenizer.encode(render_context(c), add_special_tokens=True)
                    for c in contexts]
        if any(not p or len(p) > self.max_context_tokens for p in prefixes):
            raise ValueError("context budget exceeded; no silent truncation")
        sequences = [p + target for p in prefixes]
        width = max(map(len, sequences))
        pad = self.tokenizer.pad_token_id
        if pad is None:
            pad = self.tokenizer.eos_token_id
        if pad is None:
            raise ValueError("model tokenizer requires a pad or eos token")
        ids = self.torch.tensor([s + [pad] * (width - len(s)) for s in sequences],
                                device=self.device)
        mask = self.torch.tensor([[1] * len(s) + [0] * (width - len(s)) for s in sequences],
                                 device=self.device)
        self.calls += 1
        with self.torch.inference_mode():
            logits = self.model(input_ids=ids, attention_mask=mask).logits
            scores = []
            for row, prefix in enumerate(prefixes):
                start = len(prefix) - 1
                log_probs = logits[row, start:start + len(target)].float().log_softmax(-1)
                target_ids = self.torch.tensor(target, device=self.device)
                scores.append(float(log_probs.gather(1, target_ids[:, None]).sum().item()))
        return tuple(scores), len(target)
