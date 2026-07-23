from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

import numpy as np

from ..datasets import alpaca_instructions, gsm8k, tiny_shakespeare, wikitext_2


@dataclass(frozen=True)
class PreferenceExample:
    candidates: tuple[np.ndarray, ...]
    response_starts: tuple[int, ...]
    rubrics: np.ndarray
    gold: int = 0


@dataclass(frozen=True)
class ReasoningExample:
    candidates: tuple[np.ndarray, ...]
    response_starts: tuple[int, ...]
    gold: int


@dataclass(frozen=True)
class LLMEvolutionData:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray
    narrative: np.ndarray
    instruction_train: tuple[tuple[np.ndarray, int], ...]
    instruction_validation: tuple[tuple[np.ndarray, int], ...]
    preference_train: tuple[PreferenceExample, ...]
    preference_validation: tuple[PreferenceExample, ...]
    reasoning_train: tuple[ReasoningExample, ...]
    reasoning_validation: tuple[ReasoningExample, ...]
    vocab_size: int
    tokenizer_path: Path


def load_llm_evolution_data(
    root: Path,
    allow_network: bool,
    vocab_size: int = 4096,
    maximum_train_tokens: int | None = None,
    maximum_eval_tokens: int | None = 100_000,
    benchmark_suite: str = "core",
) -> LLMEvolutionData:
    try:
        from tokenizers import Tokenizer
        from tokenizers.decoders import ByteLevel as ByteLevelDecoder
        from tokenizers.models import BPE
        from tokenizers.pre_tokenizers import ByteLevel
        from tokenizers.trainers import BpeTrainer
    except ImportError as exc:
        raise RuntimeError("LLM evolution requires pip install -e '.[llm-evolution]'") from exc

    wiki = wikitext_2(root, allow_network)
    narrative = tiny_shakespeare(root, allow_network)
    cache = root / "llm-evolution"
    tokenizer_path = cache / f"wikitext-narrative-bpe-{vocab_size}.json"
    if tokenizer_path.exists():
        tokenizer = Tokenizer.from_file(str(tokenizer_path))
    else:
        cache.mkdir(parents=True, exist_ok=True)
        tokenizer = Tokenizer(BPE(unk_token="<unk>"))
        tokenizer.pre_tokenizer = ByteLevel(add_prefix_space=False)
        tokenizer.decoder = ByteLevelDecoder()
        trainer = BpeTrainer(
            vocab_size=vocab_size,
            min_frequency=2,
            special_tokens=["<pad>", "<unk>", "<bos>", "<eos>"],
        )
        tokenizer.train_from_iterator((wiki["train"], narrative), trainer=trainer)
        tokenizer.save(str(tokenizer_path))

    def encode(text: str, limit: int | None) -> np.ndarray:
        values = np.asarray(tokenizer.encode(text).ids, dtype=np.int64)
        return values if limit is None else values[:limit]

    instructions = alpaca_instructions(root, allow_network)
    examples = []
    for row in instructions[:384]:
        prompt = f"Instruction: {row['instruction']}\n"
        if row["input"]:
            prompt += f"Input: {row['input']}\n"
        prompt += "Response:"
        prompt_ids = tokenizer.encode(prompt).ids
        full = np.asarray(
            [tokenizer.token_to_id("<bos>"), *prompt_ids, *tokenizer.encode(" " + row["output"]).ids, tokenizer.token_to_id("<eos>")],
            dtype=np.int64,
        )
        examples.append((full, 1 + len(prompt_ids)))
    preferences = tuple(
        _preference_example(row, tokenizer) for row in instructions[:320]
    )
    reasoning_train: tuple[ReasoningExample, ...] = ()
    reasoning_validation: tuple[ReasoningExample, ...] = ()
    if benchmark_suite == "public":
        math_rows = gsm8k(root, allow_network)
        rng = np.random.default_rng(202607)
        reasoning_train = tuple(
            example
            for row in math_rows["train"][:256]
            if (example := _reasoning_example(row, tokenizer, rng)) is not None
        )
        reasoning_validation = tuple(
            example
            for row in math_rows["test"][:64]
            if (example := _reasoning_example(row, tokenizer, rng)) is not None
        )
    return LLMEvolutionData(
        train=encode(wiki["train"], maximum_train_tokens),
        validation=encode(wiki["validation"], maximum_eval_tokens),
        test=encode(wiki["test"], maximum_eval_tokens),
        narrative=encode(narrative, maximum_train_tokens),
        instruction_train=tuple(examples[:320]),
        instruction_validation=tuple(examples[320:384]),
        preference_train=preferences[:256],
        preference_validation=preferences[256:320],
        reasoning_train=reasoning_train,
        reasoning_validation=reasoning_validation,
        vocab_size=tokenizer.get_vocab_size(),
        tokenizer_path=tokenizer_path,
    )


def _preference_example(row, tokenizer) -> PreferenceExample:
    prompt = f"Instruction: {row['instruction']}\n"
    if row["input"]:
        prompt += f"Input: {row['input']}\n"
    prompt += "Response:"
    words = row["output"].split()
    candidates = (
        row["output"],
        " ".join(words[: max(1, len(words) // 4)]),
        " ".join(words[::2] + words[1::2]),
    )
    encoded, starts, rubrics = [], [], []
    prompt_ids = tokenizer.encode(prompt).ids
    for response in candidates:
        response_ids = tokenizer.encode(" " + response).ids
        encoded.append(
            np.asarray(
                [
                    tokenizer.token_to_id("<bos>"),
                    *prompt_ids,
                    *response_ids,
                    tokenizer.token_to_id("<eos>"),
                ],
                dtype=np.int64,
            )
        )
        starts.append(1 + len(prompt_ids))
        response_words = response.split()
        rubrics.append(
            [
                min(len(response_words) / 32.0, 1.0),
                len(set(response_words)) / max(len(response_words), 1),
                float(any(mark in response for mark in (".", ":", "\n", "- "))),
                min(len(response_ids) / 64.0, 1.0),
            ]
        )
    return PreferenceExample(
        tuple(encoded),
        tuple(starts),
        np.asarray(rubrics, dtype=np.float32),
    )


def _reasoning_example(row, tokenizer, rng) -> ReasoningExample | None:
    match = re.search(r"####\s*(-?[\d,]+(?:\.\d+)?)", row["answer"])
    if not match:
        return None
    gold = float(match.group(1).replace(",", ""))
    scale = max(1.0, abs(gold) * 0.08)
    values = [gold, *(gold + offset * scale for offset in (-3, -2, -1, 1, 2, 3, 5))]
    order = rng.permutation(len(values))
    prompt = f"Question: {row['question']}\nAnswer:"
    prompt_ids = tokenizer.encode(prompt).ids
    encoded, starts = [], []
    for index in order:
        text = f" {values[int(index)]:g}"
        encoded.append(
            np.asarray(
                [
                    tokenizer.token_to_id("<bos>"),
                    *prompt_ids,
                    *tokenizer.encode(text).ids,
                    tokenizer.token_to_id("<eos>"),
                ],
                dtype=np.int64,
            )
        )
        starts.append(1 + len(prompt_ids))
    gold_index = int(np.flatnonzero(order == 0)[0])
    return ReasoningExample(tuple(encoded), tuple(starts), gold_index)
