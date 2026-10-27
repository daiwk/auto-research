"""Keep the public README demo playable, bounded and tied to its receipt."""

import hashlib
import json
from pathlib import Path
import re

from PIL import Image


MEDIA = Path(__file__).parents[1] / "docs/assets/media"


def test_published_demo_matches_receipt_and_stays_under_one_minute():
    receipt = json.loads((MEDIA / "site-tour.json").read_text())
    assert re.fullmatch(r"[0-9a-f]{40}", receipt["source_commit"])
    assert 0 < receipt["mp4_seconds"] <= 60
    assert len(receipt["scenes"]) >= 6
    assert sum(scene["seconds"] for scene in receipt["scenes"]) == receipt["mp4_seconds"]
    for name, expected in receipt["assets"].items():
        artifact = MEDIA / name
        assert artifact.stat().st_size == expected["bytes"]
        assert hashlib.sha256(artifact.read_bytes()).hexdigest() == expected["sha256"]
    assert b"ftyp" in (MEDIA / "site-tour.mp4").read_bytes()[:32]

    with Image.open(MEDIA / "site-tour.webp") as animation:
        assert animation.is_animated
        assert animation.n_frames == receipt["webp_frames"]
        assert animation.size == (receipt["width"], receipt["height"])
        duration = 0
        for index in range(animation.n_frames):
            animation.seek(index)
            animation.load()
            duration += animation.info["duration"]
    assert duration == receipt["webp_milliseconds"] == round(receipt["mp4_seconds"] * 1000)
    assert (MEDIA / "site-tour.webp").stat().st_size <= 8 * 1024 * 1024
    with Image.open(MEDIA / "site-tour-poster.webp") as poster:
        assert not getattr(poster, "is_animated", False)
        assert poster.size == (receipt["width"], receipt["height"])
