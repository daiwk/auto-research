"""CV-OPD crop/teacher/JSD/CDL/DAG contracts from arXiv:2610.13264.

The default normalization follows Appendix A.3 Algorithm 1 (Top-K+tail main
loss, full-vocabulary margin loss averaged over above-batch-mean gate tokens).
All sample rollouts are retained when ANY rollout is correct; gold answers
remain exclusively inside the external verifier, never checkpoint inputs.
"""
from __future__ import annotations

import math
import re

import torch
from torch import Tensor
from torch.nn import functional as F


def intersection_over_union(a: tuple, b: tuple) -> float:
    intersection = max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))
    area_a, area_b = (a[2] - a[0]) * (a[3] - a[1]), (b[2] - b[0]) * (b[3] - b[1])
    return intersection / (area_a + area_b - intersection)


def negative_crop(image_size: tuple[int, int], positive: tuple[int, int, int, int],
                  *, maximum_iou: float = .1, generator: torch.Generator | None = None) -> tuple:
    width, height = image_size
    x0, y0, x1, y1 = positive
    if not (0 <= x0 < x1 <= width and 0 <= y0 < y1 <= height and 0 <= maximum_iou < 1):
        raise ValueError("valid pixel-coordinate bbox and IoU threshold required")
    crop_width, crop_height = x1 - x0, y1 - y0
    for _ in range(1024):
        x = int(torch.randint(width - crop_width + 1, (), generator=generator))
        y = int(torch.randint(height - crop_height + 1, (), generator=generator))
        box = (x, y, x + crop_width, y + crop_height)
        if intersection_over_union(positive, box) <= maximum_iou:
            return box
    # A bounded deterministic search can still find valid edge placements.
    for x in (0, width - crop_width):
        for y in (0, height - crop_height):
            box = (x, y, x + crop_width, y + crop_height)
            if intersection_over_union(positive, box) <= maximum_iou:
                return box
    raise ValueError("no same-size negative crop satisfies the IoU bound")


def jsd(log_p: Tensor, log_q: Tensor) -> Tensor:
    if log_p.shape != log_q.shape:
        raise ValueError("JSD distributions must be vocabulary-aligned")
    mixture = torch.logaddexp(log_p, log_q) - math.log(2)
    return .5 * ((log_p.exp() * (log_p - mixture)).sum(-1)
                 + (log_q.exp() * (log_q - mixture)).sum(-1))


def topk_tail(log_p: Tensor, log_q: Tensor, k: int) -> tuple[Tensor, Tensor]:
    """Student-aligned Top-K support, with the ENTIRE omitted mass in one bin."""
    if not 0 < k < log_p.shape[-1]:
        raise ValueError("Top-K must leave a nonempty vocabulary tail")
    indices = log_p.detach().topk(k, -1).indices
    outputs = []
    for log_prob in (log_p, log_q):
        selected = log_prob.gather(-1, indices)
        mass = selected.logsumexp(-1, keepdim=True).clamp_max(-1e-7)
        tail = (-mass.expm1()).log()
        outputs.append(torch.cat((selected, tail), -1))
    return tuple(outputs)


def objective(student_logits: Tensor, positive_logits: Tensor, negative_logits: Tensor,
              mask: Tensor, correct: Tensor, sample_ids: Tensor, *, topk: int = 100,
              margin: float = .1, contrastive_weight: float = .1) -> tuple[Tensor, dict]:
    if (student_logits.shape != positive_logits.shape or student_logits.shape != negative_logits.shape
            or mask.shape != student_logits.shape[:-1] or mask.ndim != 2
            or correct.shape != sample_ids.shape or len(correct) != len(mask)):
        raise ValueError("aligned rollout-token-vocabulary logits/mask and rollout sample IDs required")
    if not 0 < margin < math.log(2) or contrastive_weight < 0:
        raise ValueError("CDL margin must be in (0,ln2), weight nonnegative")
    sample_retained = torch.zeros(int(sample_ids.max()) + 1, dtype=torch.bool, device=mask.device)
    for sample in sample_ids.unique():
        sample_retained[sample] = correct[sample_ids == sample].any()
    valid = mask.bool() & sample_retained[sample_ids, None]
    log_student = student_logits.float().log_softmax(-1)
    log_positive = positive_logits.detach().float().log_softmax(-1)
    log_negative = negative_logits.detach().float().log_softmax(-1)
    positive = jsd(log_student, log_positive)
    negative = jsd(log_student, log_negative)
    batch_mean = positive.detach()[valid].mean() if valid.any() else positive.detach().new_zeros(())
    gate = valid & (positive.detach() > batch_mean)
    aligned_student, aligned_positive = topk_tail(log_student, log_positive, min(topk, log_student.shape[-1] - 1))
    primary = jsd(aligned_student, aligned_positive)
    per_rollout = valid.sum(-1).clamp_min(1).reciprocal().float()
    weights = valid * per_rollout[:, None]
    opd = (primary * weights).sum() / weights.sum().clamp_min(1)
    hinge = F.relu(margin + positive - negative)
    cdl = (hinge * gate).sum() / gate.sum().clamp_min(1)
    loss = opd + contrastive_weight * cdl
    return loss, {"opd": opd.detach(), "cdl": cdl.detach(), "batch_mean": batch_mean,
                  "retained_samples": sample_retained.sum(), "retained_rollouts": valid.any(-1).sum(),
                  "gated_tokens": gate.sum(), "valid_tokens": valid.sum(),
                  "sample_gate": sample_retained, "token_gate": gate}


def verify_answer(response: str, references: list[str]) -> bool:
    """External training/evaluation verifier; references never enter the VLM."""
    if not references or any(not isinstance(value, str) or not value.strip() for value in references):
        raise ValueError("nonempty string references required by the external verifier")

    def normalize(value: str) -> str:
        normalized = " ".join(re.sub(r"[^a-z0-9 ]+", " ", value.lower()).split())
        # Only a leading indefinite article is harmless. No substring match,
        # synonyms, plural conversion, negation removal or label-aware rewrite.
        return re.sub(r"^(?:a|an)\s+", "", normalized)

    normalized = normalize(response)
    expected = [normalize(reference) for reference in references]
    if all(reference in ("yes", "no") for reference in expected):
        decision = re.search(r"\b(yes|no)\b", normalized)
        return bool(decision and decision.group(1) in expected)
    return normalized in expected


def sampled_training_rollouts(policy, image, question: str, references: list[str],
                               count: int, maximum_tokens: int) -> tuple[list[Tensor], list[bool]]:
    """Trainer/verifier boundary: gold never appears in the policy call."""
    if count < 1:
        raise ValueError("positive rollout count required")
    tokens = [policy.rollout(image, question, maximum_tokens) for _ in range(count)]
    responses = [policy.processor.tokenizer.decode(row, skip_special_tokens=True) for row in tokens]
    return tokens, [verify_answer(response, references) for response in responses]


class VisionPolicy:
    """Real image-conditioned checkpoint rollout and identical-prefix logits."""
    def __init__(self, model, processor, device: str):
        self.model, self.processor, self.device = model, processor, device

    def prefix(self, image, question: str) -> dict:
        messages = [{"role": "user", "content": [{"type": "image"}, {"type": "text", "text": question}]}]
        prompt = self.processor.apply_chat_template(messages, add_generation_prompt=True)
        encoded = self.processor(text=prompt, images=[image], return_tensors="pt")
        return {key: value.to(self.device) for key, value in encoded.items()}

    @torch.no_grad()
    def rollout(self, image, question: str, maximum_tokens: int = 16) -> Tensor:
        self.model.eval()
        prefix = self.prefix(image, question)
        generated = self.model.generate(**prefix, do_sample=True, temperature=.7,
                                        max_new_tokens=maximum_tokens, use_cache=True,
                                        pad_token_id=self.processor.tokenizer.eos_token_id)
        tokens = generated[0, prefix["input_ids"].shape[1]:].detach()
        eos = (tokens == self.processor.tokenizer.eos_token_id).nonzero()
        return tokens[:int(eos[0]) + 1] if len(eos) else tokens

    def trajectory_logits(self, image, question: str, tokens: Tensor) -> Tensor:
        prefix = self.prefix(image, question)
        length = prefix["input_ids"].shape[1]
        prefix["input_ids"] = torch.cat((prefix["input_ids"], tokens[None]), -1)
        prefix["attention_mask"] = torch.cat((prefix["attention_mask"], torch.ones_like(tokens[None])), -1)
        # Same generated token IDs on each branch. Different crop image-token
        # counts are aligned by each branch's own prompt boundary, not index 0.
        output = self.model(**prefix, use_cache=False)
        return output.logits[0, length - 1:length + len(tokens) - 1]


@torch.no_grad()
def ema_update(teacher, student, rate: float = .05) -> None:
    if not 0 < rate <= 1:
        raise ValueError("EMA rate in (0,1] required")
    destination = dict(teacher.named_parameters())
    for name, parameter in student.named_parameters():
        if parameter.requires_grad:
            destination[name].lerp_(parameter.detach(), rate)
