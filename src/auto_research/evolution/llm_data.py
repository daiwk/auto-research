from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from ..datasets import alpaca_instructions, tiny_shakespeare, wikitext_2


@dataclass(frozen=True)
class LLMEvolutionData:
    train: np.ndarray
    validation: np.ndarray
    test: np.ndarray
    narrative: np.ndarray
    instruction_train: tuple[tuple[np.ndarray, int], ...]
    instruction_validation: tuple[tuple[np.ndarray, int], ...]
    vocab_size: int
    tokenizer_path: Path


def load_llm_evolution_data(
    root: Path,
    allow_network: bool,
    vocab_size: int = 4096,
    maximum_train_tokens: int | None = None,
    maximum_eval_tokens: int | None = 100_000,
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
    return LLMEvolutionData(
        train=encode(wiki["train"], maximum_train_tokens),
        validation=encode(wiki["validation"], maximum_eval_tokens),
        test=encode(wiki["test"], maximum_eval_tokens),
        narrative=encode(narrative, maximum_train_tokens),
        instruction_train=tuple(examples[:320]),
        instruction_validation=tuple(examples[320:384]),
        vocab_size=tokenizer.get_vocab_size(),
        tokenizer_path=tokenizer_path,
    )
