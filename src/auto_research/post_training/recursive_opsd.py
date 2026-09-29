"""Recursive gold-conditioned on-policy distillation with verified self-refinement.

This module implements the DCE/SRCL *mechanism* of arXiv:2609.30652. The
public GSM8K runner is a bounded diagnostic, not the paper's OpenThoughts and
AIME/HMMT result. Gold is used only by the detached teacher and verifier; the
student rollout and SRCL rewrite prompt never contain it.
"""

from __future__ import annotations

from contextlib import nullcontext
from dataclasses import dataclass
import re

from .local_lora import disabled_adapters
from .token_ids import token_ids


_REFLECTION = re.compile(
    r"\b(?:wait|actually|correction|double[ -]?check|start over|let me reconsider)\b",
    re.IGNORECASE,
)
_DEPENDENT = re.compile(
    r"\b(?:as shown above|as mentioned earlier|from the previous solution)\b",
    re.IGNORECASE,
)
_ANSWER = re.compile(r"(?:Answer\s*[:=]|####)\s*([-+]?\d[\d,]*(?:\.\d+)?)", re.I)
_BOX = re.compile(r"\\boxed\{([^{}]+)\}")


def numeric_answer(text: str) -> str | None:
    """Extract the final visible numerical answer; never infer it from a prompt."""
    boxes = _BOX.findall(text)
    matches = _ANSWER.findall(text)
    candidate = (boxes or matches or [None])[-1]
    if candidate is None:
        return None
    try:
        from decimal import Decimal

        return str(Decimal(candidate.strip().replace(",", "")).normalize())
    except Exception:
        return None


def accept_refinement(
    source: str, rewrite: str, gold: str, *, source_tokens: int,
    rewrite_tokens: int, ended: bool,
) -> bool:
    """A deliberately conservative public-task version of SRCL's four gates."""
    if not ended or not rewrite.strip() or not (0 < rewrite_tokens < source_tokens):
        return False
    if _REFLECTION.search(rewrite) or _DEPENDENT.search(rewrite):
        return False
    answer = numeric_answer(rewrite)
    verified = numeric_answer(f"Answer: {gold}")
    return answer is not None and answer == verified


def teacher_prompt(problem: str, gold_solution: str) -> list[dict[str, str]]:
    """DCE: keep the privileged solution in the assistant turn, not user input."""
    return [
        {"role": "user", "content": f"Solve this problem. End with Answer: <number>.\n{problem}"},
        {"role": "assistant", "content": (
            f"A verified solution is: {gold_solution}\n"
            "Now solve this problem using your own approach.\n"
        )},
    ]


def student_prompt(problem: str) -> list[dict[str, str]]:
    return [{"role": "user", "content": f"Solve this problem. End with Answer: <number>.\n{problem}"}]


def refinement_prompt(problem: str, source: str) -> list[dict[str, str]]:
    return [{"role": "user", "content": (
        f"Problem: {problem}\nYour previous response: {source}\n"
        "Rewrite it as a shorter, self-contained solution without reflection or detours. "
        "End with Answer: <number>."
    )}]


def forward_kl(student_logits, teacher_logits, mask=None):
    """Mean tokenwise KL(q_teacher || p_student); q never receives gradients."""
    import torch

    if student_logits.shape != teacher_logits.shape or student_logits.ndim != 3:
        raise ValueError("student and teacher logits must have identical [batch, token, vocab] shape")
    log_student = torch.log_softmax(student_logits.float(), dim=-1)
    log_teacher = torch.log_softmax(teacher_logits.detach().float(), dim=-1)
    teacher = log_teacher.exp()
    per_token = torch.sum(teacher * (log_teacher - log_student), dim=-1)
    if mask is None:
        return per_token.mean()
    mask = mask.to(device=per_token.device, dtype=per_token.dtype)
    if mask.shape != per_token.shape or not bool(mask.any()):
        raise ValueError("mask must select at least one aligned response token")
    return (per_token * mask).sum() / mask.sum()


def _prompt_ids(tokenizer, messages, *, assistant_prefill: bool = False):
    if assistant_prefill:
        # The verified solution and transition already occupy the assistant turn.
        # Continue the same turn so each scored response prefix has the paper's
        # assistant-side ordering. No new user/assistant separator is inserted.
        prefix = tokenizer.apply_chat_template(
            messages[:1], tokenize=False, add_generation_prompt=True,
            enable_thinking=False,
        ) + messages[1]["content"]
        encoded = tokenizer.encode(prefix, add_special_tokens=False)
        return token_ids(encoded)
    encoded = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, enable_thinking=False,
    )
    return token_ids(encoded)


def _score_response(model, prompt_ids, response_ids, *, device):
    """Score exactly the response positions, including the first response token."""
    import torch

    if not prompt_ids or not response_ids:
        raise ValueError("prompt and response must contain tokens")
    inputs = torch.tensor([prompt_ids + response_ids], device=device)
    logits = model(input_ids=inputs, use_cache=False).logits
    start = len(prompt_ids) - 1
    return logits[:, start:start + len(response_ids), :]


def srcl_cross_entropy(model, prompt_ids, response_ids, *, device):
    import torch
    import torch.nn.functional as F

    logits = _score_response(model, prompt_ids, response_ids, device=device)
    labels = torch.tensor(response_ids, device=device)
    return F.cross_entropy(logits[0].float(), labels)


@dataclass(frozen=True)
class StepResult:
    guidance_loss: float
    refinement_loss: float | None
    refinement_accepted: bool
    rollout_tokens: int
    teacher_mode: str


def train_round(
    model, tokenizer, optimizer, *, problem: str, gold_solution: str,
    max_new_tokens: int = 128, lambda_guidance: float = 1.0,
    lambda_srcl: float = 1.0, teacher_mode: str = "dynamic",
) -> StepResult:
    """One genuine parameter-update round; next call uses the updated teacher.

    `teacher_mode='frozen'` is a reference-model OPSD control for PEFT models:
    it disables the trainable adapter only on the detached teacher pass.
    """
    import torch

    if teacher_mode not in {"dynamic", "frozen"}:
        raise ValueError("teacher_mode must be dynamic or frozen")
    if max_new_tokens < 2 or min(lambda_guidance, lambda_srcl) < 0:
        raise ValueError("invalid generation budget or loss weight")
    device = next(model.parameters()).device
    student_ids = _prompt_ids(tokenizer, student_prompt(problem))
    teacher_ids = _prompt_ids(tokenizer, teacher_prompt(problem, gold_solution), assistant_prefill=True)
    model.eval()
    with torch.no_grad():
        generated = model.generate(
            input_ids=torch.tensor([student_ids], device=device),
            attention_mask=torch.ones((1, len(student_ids)), device=device),
            max_new_tokens=max_new_tokens, do_sample=True, temperature=1.1,
            top_p=0.95, top_k=20, pad_token_id=tokenizer.eos_token_id,
        )[0, len(student_ids):].tolist()
    if not generated:
        raise RuntimeError("student produced no on-policy response")
    source = tokenizer.decode(generated, skip_special_tokens=True)
    accepted = False
    rewritten = []
    if lambda_srcl > 0:
        rewrite_ids = _prompt_ids(tokenizer, refinement_prompt(problem, source))
        with torch.no_grad():
            rewritten = model.generate(
                input_ids=torch.tensor([rewrite_ids], device=device),
                attention_mask=torch.ones((1, len(rewrite_ids)), device=device),
                max_new_tokens=max_new_tokens, do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )[0, len(rewrite_ids):].tolist()
        rewrite = tokenizer.decode(rewritten, skip_special_tokens=True)
        accepted = accept_refinement(
            source, rewrite, gold_solution, source_tokens=len(generated),
            rewrite_tokens=len(rewritten), ended=bool(rewritten and rewritten[-1] == tokenizer.eos_token_id),
        )
    model.train()
    # Teacher scores exactly the *pre-update* current weights on the same
    # on-policy tokens, and is detached even in dynamic mode.
    context = disabled_adapters(model) if teacher_mode == "frozen" else nullcontext()
    with torch.no_grad(), context:
        teacher_logits = _score_response(model, teacher_ids, generated, device=device)
    student_logits = _score_response(model, student_ids, generated, device=device)
    guidance = forward_kl(student_logits, teacher_logits)
    refinement = None
    if accepted:
        refinement = srcl_cross_entropy(model, student_ids, rewritten, device=device)
    total = lambda_guidance * guidance
    if refinement is not None:
        total = total + lambda_srcl * refinement
    if not total.requires_grad:
        raise ValueError("at least one positive loss weight is required")
    optimizer.zero_grad(set_to_none=True)
    total.backward()
    torch.nn.utils.clip_grad_norm_(
        (parameter for parameter in model.parameters() if parameter.requires_grad), 0.1,
    )
    optimizer.step()
    return StepResult(
        guidance_loss=float(guidance.detach()),
        refinement_loss=float(refinement.detach()) if refinement is not None else None,
        refinement_accepted=accepted,
        rollout_tokens=len(generated), teacher_mode=teacher_mode,
    )
