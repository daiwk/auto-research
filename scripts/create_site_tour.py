"""Turn captured site states into a short MP4, then an animated README WebP.

Requires ffmpeg/ffprobe, ImageMagick and libwebp's img2webp/cwebp. Capturing
the real browser states is deliberately separate from this media conversion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.DEVNULL)


def create(storyboard: Path, output: Path, font: str) -> dict:
    from PIL import Image

    data = json.loads(storyboard.read_text())
    scenes = data["scenes"]
    duration = sum(scene["seconds"] for scene in scenes)
    if not scenes or not 0 < duration <= 60 or any(scene["seconds"] <= 0 for scene in scenes):
        raise ValueError("The complete demo must be between zero and 60 seconds")
    for scene in scenes:
        source = storyboard.parent / scene["file"]
        if not source.is_file() or not scene["title"] or not scene["caption"]:
            raise ValueError("Each scene needs a real capture and two caption lines")
    for tool in ("ffmpeg", "ffprobe", "magick", "img2webp", "cwebp"):
        if not shutil.which(tool):
            raise RuntimeError(f"Missing media tool: {tool}")
    output.mkdir(parents=True, exist_ok=True)
    movie, animation = output / "site-tour.mp4", output / "site-tour.webp"
    with tempfile.TemporaryDirectory(prefix="auto-research-site-tour-") as temporary:
        work = Path(temporary)
        concat = []
        for index, scene in enumerate(scenes):
            source = storyboard.parent / scene["file"]
            shot, caption, frame = (work / f"{name}-{index}.png" for name in ("shot", "caption", "frame"))
            run(["magick", str(source), "-resize", "1080x608", "-background", "#ffffff",
                 "-gravity", "center", "-extent", "1080x608", str(shot)])
            run(["magick", "-size", "1080x92", "xc:#24335d", "-font", font,
                 "-gravity", "NorthWest", "-fill", "#ffffff", "-pointsize", "25",
                 "-annotate", "+24+12", scene["title"], "-fill", "#e2e8f0", "-pointsize", "18",
                 "-annotate", "+24+51", scene["caption"], str(caption)])
            run(["magick", str(shot), str(caption), "-append", str(frame)])
            concat.extend([f"file '{frame}'", f"duration {scene['seconds']}"])
        concat.append(f"file '{frame}'")
        listing = work / "frames.ffconcat"
        listing.write_text("\n".join(concat) + "\n")
        run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error", "-f", "concat",
             "-safe", "0", "-i", str(listing), "-t", str(duration), "-vf",
             f"fps=12,tpad=stop_mode=clone:stop_duration={duration},format=yuv420p",
             "-c:v", "libx264", "-crf", "18", "-preset", "slow", "-movflags", "+faststart", str(movie)])
        probe = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(movie),
        ]))
        movie_duration = float(probe["format"]["duration"])
        if abs(movie_duration - duration) > 0.2:
            raise RuntimeError(f"MP4 duration mismatch: expected {duration}, got {movie_duration}")
        # Convert the encoded video itself, sampling its real scene boundaries.
        command = ["img2webp", "-loop", "0", "-mixed", "-q", "78", "-m", "5"]
        elapsed = 0
        first = None
        for index, scene in enumerate(scenes):
            frame = work / f"video-frame-{index}.png"
            run(["ffmpeg", "-nostdin", "-y", "-hide_banner", "-loglevel", "error", "-ss", str(elapsed),
                 "-i", str(movie), "-frames:v", "1", str(frame)])
            command.extend(["-d", str(round(scene["seconds"] * 1000)), str(frame)])
            first = first or frame
            elapsed += scene["seconds"]
        run([*command, "-o", str(animation)])
        run(["cwebp", "-quiet", "-q", "80", str(first), "-o", str(output / "site-tour-poster.webp")])
    with Image.open(animation) as image:
        milliseconds = 0
        for index in range(image.n_frames):
            image.seek(index)
            image.load()
            milliseconds += image.info["duration"]
        width, height = image.size
        frames = image.n_frames
    if abs(movie_duration - duration) > 0.2 or milliseconds != round(duration * 1000) or frames < 2:
        raise RuntimeError("Encoded duration or animated frame verification failed")
    if animation.stat().st_size > 8 * 1024 * 1024:
        raise RuntimeError("README animation exceeds the 8 MiB size budget")
    receipt = {
        "recorded": data["recorded"], "source_commit": data["source_commit"],
        "capture_kind": "actual browser states; captions added during video editing",
        "mp4_seconds": movie_duration, "webp_milliseconds": milliseconds,
        "webp_frames": frames, "width": width, "height": height,
        "scenes": [{key: scene[key] for key in ("title", "caption", "seconds")} for scene in scenes],
        "assets": {path.name: {"bytes": path.stat().st_size,
                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
                   for path in (movie, animation, output / "site-tour-poster.webp")},
    }
    (output / "site-tour.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n")
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("storyboard", type=Path)
    parser.add_argument("--output", type=Path, default=Path("docs/assets/media"))
    parser.add_argument("--font", default="Heiti-SC-Medium", help="Installed font supporting Chinese")
    args = parser.parse_args()
    print(json.dumps(create(args.storyboard, args.output, args.font), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
