# Website Tour

<!-- source-sha256: 16a4f4e98177caf2ec792cfdd90a12c9b194fd47d6c2d412e46ec35f110e8258 -->

[简体中文](../../../assets/media/README.md)

[Project entry](../../project-readme.md) · [Pausable MP4](../../../assets/media/site-tour.mp4) · [Animated WebP](../../../assets/media/site-tour.webp)

The tour uses actual site screens with chapter captions, not fabricated UI or simulated results. It covers the home page, library, topic catalogs, four-level Q&A, explanations and sources, recent questions, and public experiment dashboard. Each silent loop lasts under a minute. The README uses WebP by default and shows a still poster when reduced motion is preferred. The MP4 can be paused or viewed by segment. See the [media receipt](../../../assets/media/site-tour.json) for date, timing, dimensions, frame count, and hashes.

## Update the tour

1. Pass question coverage checks and build the site. Open actual pages and capture each interaction state.
2. Write storyboard JSON with source commit, capture date, image paths, and each segment's title, caption, and duration.
3. Generate and convert the video using FFmpeg, ImageMagick, libwebp, and Python Pillow:

```bash
python scripts/create_site_tour.py /path/to/storyboard.json --output docs/assets/media
```

macOS defaults to `Heiti-SC-Medium`. On other systems, use `magick -list font` to find a Chinese font and pass `--font`. The script encodes the MP4 from real screens, samples at chapter boundaries for WebP, and checks equal MP4/WebP duration, multiple frames, and WebP under 8 MiB. It also emits a reduced-motion poster. Temporary PNGs and encoding lists are cleaned up; MP4, WebP, poster, and receipt remain.

Scene fields are `file`, `title`, `caption`, and `seconds`. Root fields are `recorded`, `source_commit`, and `scenes`. Total duration must be positive and at most 60 seconds.
