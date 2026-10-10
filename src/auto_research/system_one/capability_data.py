"""Auditable public dataset adapters for the thirteen Jev capability tasks.

Normalization uses only question/option text. Rationales, corrected-label
annotations and explanations never enter the provider-facing state.
"""
from __future__ import annotations

from dataclasses import asdict
import hashlib
import json
from pathlib import Path
import random
import re

from .capability_bench import CapabilityItem


DATASETS = {
    "mmlu-pro": "TIGER-Lab/MMLU-Pro",
    "mmlu-redux": "edinburgh-dawg/mmlu-redux-2.0",
    "mmlu": "cais/mmlu",
    "gpqa-diamond": "Idavidrein/gpqa",
    "c-eval": "ceval/ceval-exam",
    "hellaswag": "Rowan/hellaswag",
    "winogrande": "allenai/winogrande",
    "truthfulqa": "truthfulqa/truthful_qa",
    "arc-challenge": "allenai/ai2_arc",
    "mathqa": "allenai/math_qa",
    "aqua-rat": "deepmind/aqua_rat",
    "mmlu-prox": "li-lab/MMLU-ProX",
    "mmmlu": "openai/MMMLU",
}


class ExcludedItem(ValueError):
    """An upstream item has no usable unique reference; count rather than guess."""


def _choices(values):
    if not 2 <= len(values) <= 26:
        raise ValueError("expected 2–26 text options")
    if any(not isinstance(value, str) or not value.strip() for value in values):
        raise ValueError("empty/non-text option")
    return {chr(65 + i): value for i, value in enumerate(values)}


def normalize_item(benchmark, row, *, config="default", language="en", index=0, seed=42):
    """Parse an official schema without silently translating or relabeling it."""
    if benchmark not in DATASETS:
        raise ValueError("unknown benchmark")
    if not language or language == "default":
        raise ValueError("explicit language required, particularly for multilingual tasks")
    question = row.get("question", row.get("Question", ""))
    if benchmark in {"mmlu", "mmlu-redux"}:
        values, target = row["choices"], row["answer"]
        if benchmark == "mmlu-redux":
            error = row.get("error_type", "ok")
            if error == "wrong_groundtruth":
                corrected = row.get("correct_answer")
                if str(corrected) not in {"0", "1", "2", "3"}:
                    raise ExcludedItem("non-index corrected reference")
                target = int(corrected)
            elif error != "ok":
                raise ExcludedItem("ambiguous/no-correct-answer Redux annotation")
        options = _choices(values)
        target = chr(65 + int(target))
    elif benchmark == "mmlu-pro":
        options = _choices(row["options"])
        target = str(row["answer"])
    elif benchmark == "mmlu-prox":
        options = _choices([row[f"option_{i}"] for i in range(10)])
        target = str(row["answer"])
    elif benchmark == "mmmlu":
        options = {letter: row[letter] for letter in "ABCD"}
        target = str(row["Answer"])
    elif benchmark == "gpqa-diamond":
        question = row["Question"]
        values = [(row["Correct Answer"], True)] + [
            (row[f"Incorrect Answer {i}"], False) for i in range(1, 4)
        ]
        # Stable, reference-independent permutation: correct is not always A.
        digest = hashlib.sha256(f"{seed}:{config}:{index}".encode()).digest()
        random.Random(int.from_bytes(digest[:8], "big")).shuffle(values)
        options = _choices([text for text, _ in values])
        target = chr(65 + next(i for i, (_, correct) in enumerate(values) if correct))
    elif benchmark == "c-eval":
        options = {letter: row[letter] for letter in "ABCD"}
        target = str(row.get("answer", ""))
        if not target:
            raise ExcludedItem("C-Eval test reference is not publicly labeled")
    elif benchmark == "hellaswag":
        question = row["ctx"]
        options = _choices(row["endings"])
        target = chr(65 + int(row["label"]))
    elif benchmark == "winogrande":
        question = row["sentence"]
        options = _choices([row["option1"], row["option2"]])
        target = chr(64 + int(row["answer"]))
    elif benchmark == "truthfulqa":
        labels = row["mc1_targets"]["labels"]
        if labels.count(1) != 1:
            raise ExcludedItem("MC1 requires exactly one correct answer")
        options = _choices(row["mc1_targets"]["choices"])
        target = chr(65 + labels.index(1))
    elif benchmark == "arc-challenge":
        labels, texts = row["choices"]["label"], row["choices"]["text"]
        if len(set(labels)) != len(labels) or len(labels) != len(texts):
            raise ValueError("malformed ARC labels")
        options = dict(zip(map(str, labels), texts))
        target = str(row["answerKey"])
    elif benchmark == "mathqa":
        question = row["Problem"]
        raw = row["options"]
        matches = list(re.finditer(r"(?:^|,\s*)([a-e])\s*\)\s*", raw))
        if [m.group(1) for m in matches] != list("abcde"):
            raise ValueError("MathQA option delimiter mismatch")
        options = {m.group(1).upper(): raw[m.end():matches[i + 1].start()
                   if i + 1 < len(matches) else len(raw)].strip()
                   for i, m in enumerate(matches)}
        target = str(row["correct"]).upper()
    else:  # AQuA-RAT raw/json options include A) prefix.
        values = row["options"]
        if any(not value.startswith(f"{chr(65 + i)})") for i, value in enumerate(values)):
            raise ValueError("AQuA option prefix mismatch")
        options = _choices([value[2:].strip() for value in values])
        target = str(row["correct"])
    identifier = f"{benchmark}:{config}:{language}:{index}"
    return CapabilityItem(identifier, benchmark, question, options, target, language)


def export_dataset(benchmark, config, language, revision, output, *, split="test", limit=None):
    """Download a user-selected immutable dataset revision; no remote Python code."""
    if not re.fullmatch(r"[0-9a-f]{40}", revision):
        raise ValueError("dataset revision must be an immutable 40-character commit")
    if split not in {"test", "validation"}:
        raise ValueError("use the official labeled evaluation split, not training data")
    if limit is not None and limit < 1:
        raise ValueError("limit must be positive")
    from datasets import load_dataset

    source = load_dataset(DATASETS[benchmark], config, split=split, revision=revision)
    rows, excluded = [], []
    for i, row in enumerate(source):
        if limit is not None and len(rows) >= limit:
            break
        try:
            rows.append(asdict(normalize_item(benchmark, row, config=config,
                                              language=language, index=i)))
        except ExcludedItem as exc:
            excluded.append({"index": i, "reason": str(exc)})
    if not rows:
        raise ValueError("dataset has no publicly labeled usable evaluation items")
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    output.write_text(text, encoding="utf-8")
    metadata = {"dataset_id": DATASETS[benchmark], "revision": revision,
                "benchmark": benchmark, "config": config, "language": language,
                "source_split": split, "selection": "first eligible rows" if limit else "all",
                "examples": len(rows), "excluded": excluded, "limit": limit,
                "sha256": hashlib.sha256(text.encode()).hexdigest()}
    output.with_suffix(output.suffix + ".source.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return metadata


def load_capability_data(paths):
    items, sources = [], []
    for value in paths:
        path = Path(value)
        source = json.loads(path.with_suffix(path.suffix + ".source.json").read_text())
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != source["sha256"]:
            raise ValueError("capability data does not match its source receipt")
        if source["dataset_id"] != DATASETS.get(source["benchmark"]) or not re.fullmatch(
                r"[0-9a-f]{40}", source["revision"]):
            raise ValueError("invalid dataset provenance")
        loaded = [CapabilityItem(**json.loads(line)) for line in raw.decode().splitlines() if line]
        if len(loaded) != source["examples"] or any(
            item.benchmark != source["benchmark"] or item.language != source["language"]
            for item in loaded
        ):
            raise ValueError("source receipt does not describe normalized data")
        items.extend(loaded)
        sources.append(source)
    return items, sources
