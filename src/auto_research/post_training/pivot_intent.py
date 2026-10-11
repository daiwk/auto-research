"""PIVOT's structured intent protocol; references never enter prompt generation."""
from __future__ import annotations

import csv
import hashlib
import io
import random
import re


def _matches(text, labels):
    found = []
    for label in labels:
        for match in re.finditer(r"(?<!\w)" + re.escape(label) + r"(?!\w)", text):
            found.append((match.start(), label))
    return [label for _, label in sorted(found)]


def intent_prediction(response, labels):
    text = response.replace("**", "")
    marker = re.search(r"Intent Category\s*:", text, flags=re.I)
    if marker is None:
        return None
    found = _matches(text[marker.end():], labels)
    return found[0] if found else None


def intent_reward(response, gold, labels):
    if gold not in labels:
        raise ValueError("training reference must be a known intent")
    text = response.replace("**", "")
    prediction = intent_prediction(text, labels)
    candidates = re.search(r"Candidates\s*:(.*?)Reasoning\s*:", text, flags=re.I | re.S)
    listed = _matches(candidates.group(1), labels) if candidates else []
    ordered = re.search(r"Analysis\s*:\s*\S.*?Candidates\s*:\s*\S.*?Reasoning\s*:\s*\S.*?Intent Category\s*:",
                        text, flags=re.I | re.S)
    correctness = 1.0 if prediction == gold else -1.0
    alignment = .5 if prediction is not None and prediction in listed else -.5
    format_reward = .1 if ordered else 0.0
    return correctness + alignment + format_reward, {
        "correct": prediction == gold, "prediction": prediction,
        "candidate_aligned": alignment > 0, "formatted": bool(ordered),
    }


def intent_prompt(question, labels, *, definitions=None):
    if not question.strip() or not labels or len(set(labels)) != len(labels):
        raise ValueError("nonempty question and unique label set required")
    if definitions is not None and (set(definitions) != set(labels) or not all(definitions.values())):
        raise ValueError("definitions must cover the whole label set")
    categories = "\n".join(f"- {label}: {definitions[label]}" if definitions else f"- {label}" for label in labels)
    return (
        "Classify the banking customer query into exactly one of these intent categories.\n"
        + categories + "\nAnalyze the action and object, list 3-5 exact candidate labels, compare and rule out alternatives.\n"
        "Respond with Analysis:, Candidates:, Reasoning:, and Intent Category: (one exact label).\n"
        "Customer query:\n" + question
    )


def banking_holdout(source_csv, labels, *, seed=42, shots=5, validation_per_class=1):
    """Use train.csv ONLY, class-balanced and normalized-query-disjoint."""
    if min(shots, validation_per_class) < 1:
        raise ValueError("positive split budgets required")
    groups = {label: [] for label in labels}
    seen = {}
    for row in csv.DictReader(io.StringIO(source_csv)):
        question, label = row["text"], row["category"]
        normalized = " ".join(question.split())
        if not normalized or label not in groups:
            raise ValueError("invalid official intent row")
        if normalized in seen:
            if seen[normalized] != label:
                raise ValueError("conflicting labels for normalized query")
            continue
        seen[normalized] = label
        groups[label].append({"question": question, "answer": label})
    rng = random.Random(seed)
    train, valid = [], []
    for label in labels:
        rows = groups[label]
        if len(rows) < shots + validation_per_class:
            raise ValueError("insufficient unique examples for intent")
        rng.shuffle(rows)
        train.extend(rows[:shots])
        valid.extend(rows[shots:shots + validation_per_class])
    rng.shuffle(train)
    rng.shuffle(valid)
    return train, valid, {
        "algorithm": "class-balanced train-only shuffle, normalized-query deduplication",
        "seed": seed, "shots": shots, "validation_per_class": validation_per_class,
        "labels": labels, "source_sha256": hashlib.sha256(source_csv.encode()).hexdigest(),
    }
