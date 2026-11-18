from dataclasses import asdict, replace
import random

import pytest

from auto_research.multimodal.avmeme_exam import Item, evaluate, parse_letter, prepare, diagnostic


def item(**kwargs):
    return replace(Item("q", "What is heard?", ("one", "two", "three"), "two", "Audio Analysis",
                        "sound effect", "N/A", False, False), **kwargs)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_shuffling_keeps_evaluator_key_but_actor_receives_no_gold_or_metadata(seed):
    request, key = prepare(item(), random.Random(seed), split="meme-main", mode="audio_visual")
    assert dict(request.labeled_choices)[key.answer_letter] == "two"
    assert set(asdict(request)) == {"question", "labeled_choices", "audio_upload_name", "video_upload_name",
                                   "audio_sample_rate", "audio_channels", "video_fps", "video_height", "maximum_clip_seconds"}
    assert request.audio_upload_name == "clip.wav" and request.video_upload_name == "clip.mp4"
    assert request.audio_sample_rate == 16000 and request.audio_channels == request.video_fps == 1
    assert request.video_height == 360 and request.maximum_clip_seconds == 30


def test_main_filters_only_flagged_text_shortcuts_and_full_retains_them():
    shortcut = item(text_cheat=True)
    assert prepare(shortcut, random.Random(1), split="meme-main", mode="audio") is None
    assert prepare(shortcut, random.Random(1), split="meme-full", mode="audio") is not None


@pytest.mark.parametrize("mode,cheat,video", [("audio", False, None), ("audio_visual", True, None),
                                            ("audio_visual", False, "clip.mp4")])
def test_visual_policy_applies_before_predictor(mode, cheat, video):
    request, _ = prepare(item(visual_cheat=cheat), random.Random(1), split="meme-main", mode=mode)
    assert request.video_upload_name == video


@pytest.mark.parametrize("response,expected", [(" A ", "A"), ("(B)", "B"), ("a", None),
                                               ("A or B", None), ("Answer: B", None), ("Z", None), (None, None)])
def test_conservative_local_parser_is_not_a_semantic_judge(response, expected):
    assert parse_letter(response, 3) == expected


def test_predictor_only_receives_actor_request_and_unanswered_counts_in_denominator():
    seen = []

    def predictor(request):
        seen.append(asdict(request))
        return None

    result = evaluate([item(), item(identity="other", language="en", question_type="World Knowledge")], predictor, seed=42)
    assert result["examples"] == 2 and result["micro_accuracy"] == result["parsed_fraction"] == 0
    assert result["by_axis"]["language"]["en"] == {"examples": 1, "accuracy": 0}
    assert not any("solution" in row or "question_type" in row for row in seen)
    assert result["media_processed"] is False and result["model_capability_established"] is False


@pytest.mark.parametrize("change", [{"choices": ("same", "same")}, {"solution": "missing"},
                                    {"text_cheat": 1}, {"visual_cheat": None}, {"question_type": "invented"}])
def test_malformed_inputs_rejected(change):
    with pytest.raises(ValueError):
        item(**change)


def test_duplicate_and_empty_evaluation_do_not_create_scores():
    with pytest.raises(ValueError, match="unique"):
        evaluate([item(), item()], lambda request: "A", seed=42)
    with pytest.raises(ValueError, match="no eligible"):
        evaluate([item(text_cheat=True)], lambda request: "A", seed=42)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_interface_diagnostics(seed):
    assert all(diagnostic(seed)["checks"].values())
    assert diagnostic(seed)["evaluation_tier"] == "l0_interface"
    with pytest.raises(ValueError, match="CPU"):
        diagnostic(seed, "cuda")
