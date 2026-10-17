"""Prune-then-loop language-core surgery and staged recovery interfaces.

No pretrained TinyLLaVA weights or full 60B-token recovery are loaded.
"""
from __future__ import annotations

import copy
import math

import torch
from torch import Tensor, nn
from torch.nn import functional as F


class RetrofittedRecurrentVLM(nn.Module):
    def __init__(self, width: int = 16, heads: int = 4, vocabulary: int = 23,
                 original_depth: int = 6, prune_start: int = 1, prune_count: int = 2,
                 prelude: int = 1, core: int = 2, coda: int = 1):
        super().__init__()
        if (min(width, heads, vocabulary, original_depth, prune_count, prelude, core, coda) < 1
                or width % heads or prune_start < 0 or prune_start + prune_count > original_depth
                or prune_start != prelude
                or prelude + core + coda != original_depth - prune_count):
            raise ValueError("invalid surgery dimensions or retained layer allocation")
        self.width = width
        original = nn.ModuleList(nn.TransformerEncoderLayer(width, heads, 2 * width, dropout=0.,
                                                           batch_first=True, norm_first=True)
                                 for _ in range(original_depth))
        kept = [layer for index, layer in enumerate(original)
                if not prune_start <= index < prune_start + prune_count]
        self.teacher_layers = copy.deepcopy(original)
        for parameter in self.teacher_layers.parameters():
            parameter.requires_grad_(False)
        self.prelude = nn.ModuleList(kept[:prelude])
        self.core = nn.ModuleList(kept[prelude:prelude + core])
        self.coda = nn.ModuleList(kept[prelude + core:])
        self.adapter = nn.Linear(2 * width, width, bias=False)
        self.embedding = nn.Embedding(vocabulary, width)
        self.projector = nn.Linear(width, width)
        self.output = nn.Linear(width, vocabulary, bias=False)
        self.teacher_embedding = copy.deepcopy(self.embedding)
        self.teacher_projector = copy.deepcopy(self.projector)
        self.teacher_output = copy.deepcopy(self.output)
        for name, parameter in self.named_parameters():
            if name.startswith("teacher_"):
                parameter.requires_grad_(False)

    @staticmethod
    def apply_layers(x: Tensor, layers: nn.ModuleList) -> Tensor:
        mask = torch.ones(x.shape[1], x.shape[1], device=x.device, dtype=torch.bool).triu(1)
        for layer in layers:
            x = layer(x, src_mask=mask)
        return x

    def forward(self, tokens: Tensor, visual_tokens: Tensor, iterations: int = 3,
                initial_state: Tensor | None = None) -> Tensor:
        if iterations < 1 or tokens.ndim != 2 or visual_tokens.ndim != 3:
            raise ValueError("positive depth, token ids and visual token embeddings required")
        x = torch.cat((self.projector(visual_tokens), self.embedding(tokens)), 1)
        context = self.apply_layers(x, self.prelude)
        state = torch.randn_like(context) * .02 if initial_state is None else initial_state
        if state.shape != context.shape:
            raise ValueError("initial recurrent state must match the retained context")
        for _ in range(iterations):
            state = self.apply_layers(self.adapter(torch.cat((state, context), -1)), self.core)
        return self.output(self.apply_layers(state, self.coda))

    @torch.no_grad()
    def teacher_logits(self, tokens: Tensor, visual_tokens: Tensor) -> Tensor:
        hidden = torch.cat((self.teacher_projector(visual_tokens), self.teacher_embedding(tokens)), 1)
        return self.teacher_output(self.apply_layers(hidden, self.teacher_layers))

    def configure_stage(self, stage: int) -> None:
        if stage not in (0, 1, 2):
            raise ValueError("recovery stage must be 0, 1 or 2")
        for name, parameter in self.named_parameters():
            parameter.requires_grad_(not name.startswith("teacher_")
                                     and (stage == 2 or ((name.startswith("projector.")) == (stage == 1))))


def recovery_loss(student: Tensor, teacher: Tensor, labels: Tensor,
                  temperature: float = 2., weight: float = .5) -> Tensor:
    if (student.shape != teacher.shape or student.shape[:-1] != labels.shape
            or not math.isfinite(temperature) or temperature <= 0 or not 0 <= weight <= 1):
        raise ValueError("matching logits/labels and valid distillation settings required")
    ce = F.cross_entropy(student.flatten(0, -2), labels.flatten())
    teacher_probability = (teacher.detach() / temperature).softmax(-1)
    kl = F.kl_div((student / temperature).log_softmax(-1), teacher_probability, reduction="none").sum(-1).mean()
    return (1 - weight) * ce + weight * temperature ** 2 * kl
