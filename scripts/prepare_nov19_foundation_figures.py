"""Extract fixed-v1 original-paper crops, with source/rectangle provenance."""

from hashlib import sha256
import json
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / ".cache/nov19-latest/foundation"
FIGURES = [
    (
        "2611.23896",
        "kernel-ridge-attention",
        "foundation-models",
        2,
        (100, 75, 520, 395),
        "Figure1: Kernel Ridge Attention mechanism",
    ),
    (
        "2611.23835",
        "narrow-spec",
        "foundation-models",
        3,
        (62, 200, 550, 442),
        "Figure1: DFlash decode iteration and draft width",
    ),
    (
        "2611.24301",
        "loopcache-interface",
        "foundation-models",
        6,
        (104, 48, 515, 294),
        "Figure6: LoopCache scheduling, draft update and shallow-layer decoupling",
    ),
    (
        "2611.24778",
        "counterfactual-wm",
        "foundation-models",
        1,
        (82, 365, 518, 775),
        "Figure1: Observed outcome and same-event counterfactual",
    ),
    (
        "2611.23417",
        "autoregressive-view-model",
        "multimodal-models",
        1,
        (66, 365, 547, 525),
        "Figure1: A scene as a stream of views",
    ),
]


def main():
    for aid, key, domain, page, bounds, caption in FIGURES:
        source = CACHE / (aid + "v1.pdf")
        doc = fitz.open(source)
        # Review the full page before admitting the crop.
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(1.3, 1.3)).save(CACHE / (aid + "-preview.png"))
        output = ROOT / f"docs/{domain}/{aid}-{key}/assets"
        output.mkdir(parents=True, exist_ok=True)
        asset = output / "paper-figure-01.png"
        doc[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(bounds)).save(asset)
        (output / "provenance.json").write_text(
            json.dumps(
                {
                    "source_url": f"https://arxiv.org/pdf/{aid}v1",
                    "paper_url": f"https://arxiv.org/abs/{aid}v1",
                    "reviewed_version": "v1",
                    "retrieved_on": "2026-11-19",
                    "page": page,
                    "crop_box_pdf_points": bounds,
                    "caption": caption,
                    "extraction": "Original PDF crop, no semantic editing",
                    "source_pdf_sha256": sha256(source.read_bytes()).hexdigest(),
                    "asset_sha256": sha256(asset.read_bytes()).hexdigest(),
                    "copyright": "Copyright retained by the original authors; research commentary, not a local result.",
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )


if __name__ == "__main__":
    main()
