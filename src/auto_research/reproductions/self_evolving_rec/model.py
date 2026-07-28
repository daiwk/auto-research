from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Candidate:
    name: str
    optimizer: str
    gated: bool
    multi_objective_reward: bool
    learning_rate: float = 0.015


def candidate_space() -> tuple[Candidate, ...]:
    values = [Candidate("human_adagrad", "adagrad", False, False)]
    for optimizer in ("adagrad", "rmsprop"):
        for gated in (False, True):
            for reward in (False, True):
                for learning_rate in (0.008, 0.015, 0.03):
                    name = f"{optimizer}-gate{int(gated)}-reward{int(reward)}-lr{learning_rate:g}"
                    values.append(Candidate(name, optimizer, gated, reward, learning_rate))
    return tuple(values)


class EvolvingModel:
    def __init__(self, items: int, factors: int, seed: int, candidate: Candidate):
        rng = np.random.default_rng(seed)
        scale = 0.08 / math.sqrt(factors)
        self.context = rng.normal(0, scale, (items, factors))
        self.item = rng.normal(0, scale, (items, factors))
        self.gate = np.zeros(factors)
        self.candidate = candidate
        self.context_acc = np.zeros_like(self.context)
        self.item_acc = np.zeros_like(self.item)
        self.gate_acc = np.zeros_like(self.gate)

    def _gating(self) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-self.gate)) if self.candidate.gated else np.ones_like(self.gate)

    def scores(self, previous: int, candidates: np.ndarray) -> np.ndarray:
        return self.item[candidates] @ (self.context[previous] * self._gating())

    def update(self, previous: int, positive: int, negative: int, weight: float) -> None:
        user = self.context[previous].copy()
        pos = self.item[positive].copy()
        neg = self.item[negative].copy()
        gate = self._gating()
        representation = user * gate
        diff = float(representation @ (pos - neg))
        coefficient = weight / (1.0 + math.exp(min(30.0, diff)))
        reg = 0.002
        user_grad = coefficient * (pos - neg) * gate - reg * user
        pos_grad = coefficient * representation - reg * pos
        neg_grad = -coefficient * representation - reg * neg
        self._apply(self.context, self.context_acc, previous, user_grad)
        self._apply(self.item, self.item_acc, positive, pos_grad)
        self._apply(self.item, self.item_acc, negative, neg_grad)
        if self.candidate.gated:
            gate_grad = coefficient * user * (pos - neg) * gate * (1.0 - gate) - reg * self.gate
            self._apply_dense(self.gate, self.gate_acc, gate_grad)

    def _apply(self, parameter, accumulator, index: int, gradient: np.ndarray) -> None:
        if self.candidate.optimizer == "rmsprop":
            accumulator[index] = 0.95 * accumulator[index] + 0.05 * gradient**2
        else:
            accumulator[index] += gradient**2
        parameter[index] += self.candidate.learning_rate * gradient / np.sqrt(accumulator[index] + 1e-6)

    def _apply_dense(self, parameter, accumulator, gradient: np.ndarray) -> None:
        if self.candidate.optimizer == "rmsprop":
            accumulator[:] = 0.95 * accumulator + 0.05 * gradient**2
        else:
            accumulator[:] += gradient**2
        parameter += self.candidate.learning_rate * gradient / np.sqrt(accumulator + 1e-6)


def train_candidate(data, candidate: Candidate, seed: int, factors: int = 20, epochs: int = 3):
    rng = np.random.default_rng(seed)
    model = EvolvingModel(data.item_count, factors, seed, candidate)
    examples = []
    for sequence in data.train:
        denominator = max(1, len(sequence) - 1)
        for index, (previous, positive) in enumerate(zip(sequence, sequence[1:])):
            reward = 0.6 + 0.8 * (index / denominator) if candidate.multi_objective_reward else 1.0
            examples.append((previous, positive, reward))
    examples = np.asarray(examples, dtype=np.float64)
    for _ in range(epochs):
        rng.shuffle(examples)
        for previous, positive, reward in examples:
            negative = int(rng.integers(data.item_count))
            if negative == int(positive):
                negative = (negative + 1) % data.item_count
            model.update(int(previous), int(positive), negative, float(reward))
    return model


class LLMResearchAgent:
    """A constrained LLM agent: the LM reads the journal and ranks executable edits."""

    def __init__(self, model_name: str = "HuggingFaceTB/SmolLM2-135M-Instruct"):
        try:
            import torch
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError("Self-Evolving RecSys requires `pip install -e '.[plum]'`.") from exc
        from auto_research.runtime import device_for
        self.torch = torch
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        self.device = device_for(torch)
        self.model.to(self.device).eval()
        self.model_name = model_name

    @staticmethod
    def prompt(journal: list[dict]) -> str:
        observations = "\n".join(
            f"- {row['candidate']}: validation NDCG@10={row['validation_ndcg_at_10']:.6f}"
            for row in journal
        ) or "- no experiment has run yet"
        return (
            "You are a recommendation-model research agent. Read the experiment journal, "
            "then choose the most promising next executable configuration. Prefer a controlled "
            "change and do not repeat a tested configuration.\nJournal:\n"
            f"{observations}\nNext configuration: "
        )

    def propose(self, candidates: tuple[Candidate, ...], journal: list[dict]) -> tuple[Candidate, dict]:
        tried = {row["candidate"] for row in journal}
        available = [candidate for candidate in candidates if candidate.name not in tried]
        prompt = self.prompt(journal)
        continuations = [
            (
                f"{candidate.name}; optimizer={candidate.optimizer}; "
                f"gated={candidate.gated}; multi_objective_reward={candidate.multi_objective_reward}; "
                f"learning_rate={candidate.learning_rate}"
            )
            for candidate in available
        ]
        prompt_tokens = len(self.tokenizer(prompt, add_special_tokens=True)["input_ids"])
        score_rows = []
        for start in range(0, len(continuations), 4):
            texts = [prompt + value for value in continuations[start:start + 4]]
            encoded = self.tokenizer(
                texts, padding=True, truncation=True, max_length=512, return_tensors="pt"
            ).to(self.device)
            labels = encoded["input_ids"].clone()
            labels[:, :prompt_tokens] = -100
            labels[encoded["attention_mask"] == 0] = -100
            with self.torch.inference_mode():
                logits = self.model(**encoded).logits[:, :-1]
                targets = labels[:, 1:]
                loss = self.torch.nn.functional.cross_entropy(
                    logits.reshape(-1, logits.shape[-1]), targets.reshape(-1),
                    ignore_index=-100, reduction="none",
                ).reshape(targets.shape)
                valid = targets.ne(-100)
                score_rows.append(
                    ((loss * valid).sum(1) / valid.sum(1).clamp_min(1)).cpu()
                )
        scores = self.torch.cat(score_rows)
        index = int(scores.argmin().item())
        return available[index], {
            "prompt": prompt,
            "candidate_log_losses": {
                candidate.name: float(value)
                for candidate, value in zip(available, scores)
            },
        }
