from __future__ import annotations

from auto_research.reproductions.music_rationales.data import Artist, MusicData
from auto_research.reproductions.music_rationales.experiment import reproduce
from auto_research.reproductions.music_rationales.pipeline import (
    annotate_baseline, generate_profile, serve,
)


def fixture_data() -> MusicData:
    artists = {
        1: Artist(1, "Seed Band", ("jazz", "soul")),
        2: Artist(2, "New Band", ("jazz", "funk")),
        3: Artist(3, "Bad Band", ("metal",)),
        4: Artist(4, "Other Band", ("jazz",)),
    }
    return MusicData(artists, {1: frozenset({1}), 2: frozenset({1, 2, 3, 4})},
                     {1: frozenset({2}), 2: frozenset()},
                     {1: frozenset({4}), 2: frozenset()}, 5)


def test_entity_novelty_and_rationale_grounding():
    data = fixture_data()
    generated = ('[{"artist_id": 2, "rationale": "New Band shares jazz with Seed Band"},'
                 '{"artist_id": 3, "rationale": "Bad Band shares jazz with Seed Band"},'
                 '{"artist_id": 999, "rationale": "invented jazz artist"}]')
    profile, stats = generate_profile(data, 1, lambda _: generated)
    assert [row.artist_id for row in profile.nominations] == [2]
    assert stats["rejected"]["unsupported_rationale"] == 1
    assert stats["rejected"]["invalid_entity"] == 1


def test_live_path_uses_cache_or_cf_without_model():
    data = fixture_data()
    assert serve(data, 1, {})[0].artist_id in {2, 3, 4}
    profile, _ = generate_profile(
        data, 1, lambda _: '[{"artist_id":2,"rationale":"jazz like Seed Band"}]')
    assert serve(data, 1, {1: profile})[0].artist_id == 2
    assert {row.artist_id for row in serve(data, 1, {1: profile})} == {2, 3, 4}
    assert [row.artist_id for row in annotate_baseline(data, 1, {1: profile})] == [
        row.artist_id for row in annotate_baseline(data, 1, {})
    ]
    assert annotate_baseline(data, 1, {1: profile})[0].rationale == "jazz like Seed Band"


def test_invalid_split_fails_before_loading_data_or_model(tmp_path):
    import pytest

    with pytest.raises(ValueError, match="validation or test"):
        reproduce(tmp_path, split="train")
