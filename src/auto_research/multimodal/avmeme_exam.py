"""AVMeme Exam evaluation contracts, without media or a multimodal model.

Question/choice shuffling, text-shortcut filtering, visual-shortcut masking and
multi-axis scoring follow fixed v1. Media processing/upload is a caller duty.
Evaluator keys never enter the predictor's typed request. This is not a sandbox.
"""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Callable, Sequence
from dataclasses import dataclass
import random
import re

REQUIRES_GPU_VALIDATION = False
QUESTION_TYPES = ("Audio Analysis", "Language Analysis", "Contextual Inference", "Emotion Analysis",
                  "Humor & Popularity", "Usage & Application", "World Knowledge")


@dataclass(frozen=True)
class Item:
    identity: str
    question: str
    choices: tuple[str, ...]
    solution: str
    question_type: str
    sound_category: str
    language: str
    text_cheat: bool
    visual_cheat: bool

    def __post_init__(self):
        if any(not isinstance(x, str) or not x.strip() for x in (
                self.identity, self.question, self.solution, self.sound_category, self.language)):
            raise ValueError("explicit item, question, solution and analysis labels required")
        if (not isinstance(self.choices, tuple) or not 2 <= len(self.choices) <= 26
                or any(not isinstance(x, str) or not x.strip() for x in self.choices)
                or len(set(self.choices)) != len(self.choices) or self.solution not in self.choices):
            raise ValueError("unique choices and an exact matching evaluator solution required")
        if self.question_type not in QUESTION_TYPES:
            raise ValueError("one of the seven published question types required")
        if type(self.text_cheat) is not bool or type(self.visual_cheat) is not bool:
            raise ValueError("explicit externally verified shortcut flags required")


@dataclass(frozen=True)
class ActorRequest:
    """No ID/title, source URL, transcript, summary, analysis labels or gold."""

    question: str
    labeled_choices: tuple[tuple[str, str], ...]
    audio_upload_name: str = "clip.wav"
    video_upload_name: str | None = None
    audio_sample_rate: int = 16000
    audio_channels: int = 1
    video_fps: int = 1
    video_height: int = 360
    maximum_clip_seconds: int = 30


@dataclass(frozen=True)
class ScoringKey:
    identity: str
    answer_letter: str
    question_type: str
    sound_category: str
    language: str


def prepare(item: Item, rng: random.Random, *, split: str, mode: str) -> tuple[ActorRequest, ScoringKey] | None:
    if not isinstance(item, Item) or split not in ("meme-full", "meme-main"):
        raise ValueError("typed item and an explicit published split required")
    if mode not in ("audio", "audio_visual") or not isinstance(rng, random.Random):
        raise ValueError("audio/audio_visual mode and explicit RNG required")
    if split == "meme-main" and item.text_cheat:
        return None
    choices = list(item.choices)
    rng.shuffle(choices)
    labeled = tuple((chr(65 + index), choice) for index, choice in enumerate(choices))
    request = ActorRequest(item.question, labeled,
                           video_upload_name="clip.mp4" if mode == "audio_visual" and not item.visual_cheat else None)
    key = ScoringKey(item.identity, chr(65 + choices.index(item.solution)), item.question_type,
                     item.sound_category, item.language)
    return request, key


def parse_letter(response: str | None, choice_count: int) -> str | None:
    """Strict local parser, not an invented paper-specific answer-extraction LM.

    Accept A or (A) only; free text, multiple letters and out-of-range answers
    count incorrect. This conservative convention is explicit, not claimed to
    reproduce every upstream backend's output parser.
    """
    if not isinstance(response, str):
        return None
    match = re.fullmatch(r"\s*(?:([A-Z])|\(([A-Z])\))\s*", response)
    letter = next((value for value in match.groups() if value), None) if match else None
    return letter if letter is not None and ord(letter) - 65 < choice_count else None


def evaluate(items: Sequence[Item], predictor: Callable[[ActorRequest], str | None], *,
             seed: int, split: str = "meme-main", mode: str = "audio_visual") -> dict:
    """One fixed pass; no retries, no label-based selection, no media access."""
    if (type(seed) is not int or not callable(predictor) or isinstance(items, (str, bytes))
            or not isinstance(items, Sequence) or not all(isinstance(item, Item) for item in items)
            or len({item.identity for item in items}) != len(items)):
        raise ValueError("integer seed, predictor and unique typed evaluation items required")
    rng, rows = random.Random(seed), []
    axes = {name: defaultdict(list) for name in ("question_type", "sound_category", "language")}
    for item in items:
        prepared = prepare(item, rng, split=split, mode=mode)
        if prepared is None:
            continue
        request, key = prepared
        prediction = parse_letter(predictor(request), len(request.labeled_choices))
        correct = prediction == key.answer_letter
        rows.append({"id": key.identity, "correct": correct, "parsed": prediction is not None,
                     "visual_masked": mode == "audio_visual" and request.video_upload_name is None})
        for axis, values in axes.items():
            values[getattr(key, axis)].append(correct)
    if not rows:
        raise ValueError("no eligible evaluation rows; do not report a fabricated zero-sample score")
    return {"split": split, "mode": mode, "examples": len(rows), "filtered_examples": len(items) - len(rows),
            "micro_accuracy": sum(row["correct"] for row in rows) / len(rows),
            "parsed_fraction": sum(row["parsed"] for row in rows) / len(rows),
            "by_axis": {axis: {label: {"examples": len(values), "accuracy": sum(values) / len(values)}
                               for label, values in sorted(groups.items())} for axis, groups in axes.items()},
            "rows": rows, "aggregation_note": "Explicit micro accuracy and per-axis counts; no guessed seven-type macro AVG",
            "media_processed": False, "model_capability_established": False}


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("CPU-only benchmark protocol, no CUDA encoder or media pipeline")
    items = [Item("fixture-a", "Which event?", ("event one", "event two"), "event two",
                  "Audio Analysis", "sound effect", "N/A", False, True),
             Item("fixture-b", "Which intent?", ("intent one", "intent two"), "intent one",
                  "Contextual Inference", "speech", "en", False, False),
             Item("fixture-shortcut", "Which source?", ("source one", "source two"), "source one",
                  "World Knowledge", "song", "en", True, False)]
    visible = []

    def predictor(request):
        visible.append(request)
        return "A"  # Fixed uninformed output; never reads an evaluator key.

    main = evaluate(items, predictor, seed=seed)
    full = evaluate(items, lambda request: "A or B", seed=seed, split="meme-full")
    request, key = prepare(items[0], random.Random(seed), split="meme-main", mode="audio_visual")
    mapped = dict(request.labeled_choices)[key.answer_letter] == items[0].solution
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l0_interface",
            "metrics": {"eligible_fixture_items": main["examples"], "filtered_shortcut_items": main["filtered_examples"],
                        "visual_masked_items": sum(row["visual_masked"] for row in main["rows"]),
                        "invalid_response_items": len(full["rows"]) - sum(row["parsed"] for row in full["rows"])},
            "checks": {"main_excludes_text_shortcuts": main["examples"] == 2 and main["filtered_examples"] == 1,
                       "visual_shortcut_masked": visible[0].video_upload_name is None and visible[1].video_upload_name == "clip.mp4",
                       "shuffle_preserves_private_key_mapping": mapped,
                       "actor_fields_are_label_blind": not any(hasattr(visible[0], x) for x in (
                           "solution", "answer_letter", "identity", "summary", "transcription", "name", "language")),
                       "invalid_outputs_are_not_guessed": full["parsed_fraction"] == full["micro_accuracy"] == 0,
                       "analysis_counts_preserved": main["by_axis"]["language"]["en"]["examples"] == 1}}
