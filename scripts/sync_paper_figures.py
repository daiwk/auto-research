#!/usr/bin/env python3
"""Download one important original-paper figure for every reproduction page.

The script prefers arXiv's HTML representation because it preserves the
figure/caption relationship.  Older papers fall back to ar5iv and, finally,
to a caption-aware crop from the arXiv PDF.  Generated sections are delimited
by stable comments so a later refresh is deterministic.

Install the maintainer dependencies with:

    python -m pip install -e '.[paper-figures]'

Examples:

    python scripts/sync_paper_figures.py --only 2507.15551
    python scripts/sync_paper_figures.py --workers 3
"""

from __future__ import annotations

import argparse
import concurrent.futures
import io
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from PIL import Image, ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True


ROOT = Path(__file__).resolve().parents[1]
DOC_ROOTS = (
    ROOT / "docs" / "reproductions",
    ROOT / "docs" / "post-training",
    ROOT / "docs" / "agent-research",
    ROOT / "docs" / "foundation-models",
    ROOT / "docs" / "multimodal-models",
    ROOT / "docs" / "evolution",
)
TMP = ROOT / "tmp" / "paper-figures"
MANIFEST = ROOT / "docs" / "paper-figures-manifest.json"
START = "<!-- paper-figure:start -->"
END = "<!-- paper-figure:end -->"
USER_AGENT = "auto-research-paper-figure-sync/1.0 (https://github.com/daiwk/auto-research)"

MANUAL_PDFS = {
    "kdd2018-mmoe-mmoe": (
        "https://raw.githubusercontent.com/tangxyw/RecSysPapers/main/"
        "Multi-Task/%5B2018%5D%5BGoogle%5D%5BMMOE%5D%20Modeling%20Task%20"
        "Relationships%20in%20Multi-task%20Learning%20with%20Multi-gate%20"
        "Mixture-of-Experts.pdf"
    ),
    "recsys2016-youtube-dnn-youtube-dnn": (
        "https://research.google.com/pubs/archive/45530.pdf"
    ),
    "recsys2020-ple-ple": (
        "https://raw.githubusercontent.com/tangxyw/RecSysPapers/main/"
        "Multi-Task/%5B2020%5D%5BTencent%5D%5BPLE%5D%20Progressive%20"
        "Layered%20Extraction%20%28PLE%29%20-%20A%20Novel%20Multi-Task%20"
        "Learning%20%28MTL%29%20Model%20for%20Personalized%20Recommendations.pdf"
    ),
}
MANUAL_FIGURE_NUMBERS = {
    "kdd2018-mmoe-mmoe": "1",
    "recsys2016-youtube-dnn-youtube-dnn": "3",
    "recsys2020-ple-ple": "1",
}
FIGURE_OVERRIDES = {
    "2610.22075-rr-vlm": "1",
    "2610.21412-jev-agent-harness": "8",
    "2610.20782-memory-mosaics-plus": "2",
    "2610.21323-adaloop-vision": "1",
    "2610.22369-softcache": "1",
    "2610.20904-egojepa": "2",
    "2610.21500-remote-kv-tiers": "1",
    "2610.21018-rshd": "2",
    "2610.21281-diviner": "3",
    "2610.21555-muon-paired-budget": "3",
    "2610.22124-probe": "1",
    "2610.22319-gemini-minecraft": "2",
    "2610.22196-hy-memory": "1",
    "2610.21055-athanor": "2",
    "2610.22230-hardware-diversity": "3",
    "2610.22290-elite-replay": "2",
    "2610.22353-mirror-moe": "4",
    "2610.13025-evo2": "2",
    "2610.13092-jev-workflow": "2",
    "2610.13194-janus": "2",
    "2610.13348-t2mem": "1",
    "2610.13889-rated": "3",
    "2610.13912-rsi-anything": "2",
    "2610.13481-branch-opd": "2",
    "2610.13257-cast-opd": "1",
    "2610.13285-boundary-evo": "2",
    "2610.13521-road-mopd": "2",
    "2610.13630-msar": "2",
    "2610.13735-orthros": "1",
    "2610.13767-dualquant": "1",
    "2610.12417-woven": "2",
    "2610.12707-umrm": "2",
    "2610.11794-memento3": "2",
    "2610.11251-vcola": "5",
    "2610.12102-data-space-iteration": "1",
    "2610.12367-sguid": "1",
    "2610.12327-sparse-decoding": "2",
    "2610.11332-recal": "3",
    "2610.12060-vimod": "4",
    "2610.01834-jev-lookahead": "1",
    "2610.02001-mingbird": "1",
    "2609.31045-kuafu": "2",
    "2609.00986-tgr": "1",
    "2609.00444-gapo": "2",
    "2604.18146-marc": "5",
    "2008.13535-dcn-v2": "2",
    "2205.08084-m6rec": "3",
    "2308.00352-metagpt": "1",
    "2310.04406-lats": "1",
    "2403.07691-orpo": "2",
    "2407.16741-openhands": "2",
    "2502.10157-sessionrec": "2",
    "2502.16982-muon": "2",
    "2512.24880-mhc": "1",
    "2606.13392-minimax-sparse-attention": "1",
    "2607.28895-snaplgr": "1",
    "2606.06970-ssrlive": "2",
    "2605.27043-causal-representation": "1",
    "2605.16479-policy-facet": "2",
    "2602.09386-smes": "2",
    "2601.20215-easq": "1",
    "2601.02955-harmonrank": "3",
}
CAPTION_OVERRIDES = {
    "2112.09332-webgpt": "demonstration interface",
}

# Some papers have no parseable Figure caption.  These bounded, reviewed crops
# preserve an important original passage (MRKL) or the official public abstract
# when the proceedings full text cannot be fetched automatically (Pin-SCALE).
SPECIAL_CROPS = {
    "2610.22075-rr-vlm": {
        "pdf_url": "https://arxiv.org/pdf/2610.22075v1",
        "page": 1,
        "rect": (105, 79, 508, 303),
        "label": "Figure 1",
        "caption": "原始 VLM 与 prune-then-loop retrofit 架构对比，完整保留连续剪枝、prelude、adapter、共享循环核心、coda 和展开路径。",
    },
    "2610.21281-diviner": {
        "pdf_url": "https://arxiv.org/pdf/2610.21281v1",
        "page": 5,
        "rect": (50, 318, 562, 539),
        "label": "Figure 3",
        "caption": "Diviner 的 Encode、Execute、Evaluate、Adapt 四阶段生命周期；保留证据关联、隔离工作者和回放后经负责人批准的更新。",
    },
    "2610.21412-jev-agent-harness": {
        "pdf_url": "https://arxiv.org/pdf/2610.21412v1",
        "page": 24,
        "rect": (302, 227, 528, 468),
        "label": "Figure 8",
        "caption": "JEVAGENTHARNESS 的 typed decision 路由、System-1/System-2 分工与逐调用成本账本；图为原论文集成架构，不是本地官方框架验收。",
    },
    "2610.20782-memory-mosaics-plus": {
        "pdf_url": "https://arxiv.org/pdf/2610.20782v1",
        "page": 5,
        "rect": (105, 500, 508, 662),
        "label": "Figure 2",
        "caption": "对比 basic、现代混合、Memory Mosaics+ 和 two-stage 架构；短期窗口、长期记忆与目标/相关任务分离为原论文结构。",
    },
    "2610.21323-adaloop-vision": {
        "pdf_url": "https://arxiv.org/pdf/2610.21323v1",
        "page": 1,
        "rect": (105, 79, 507, 202),
        "label": "Figure 1",
        "caption": "普通 VLM 一次视觉编码与 AdaLoop 问题条件视觉循环的结构对比；完整保留左右两条路径。",
    },
    "2610.22369-softcache": {
        "pdf_url": "https://arxiv.org/pdf/2610.22369v1",
        "page": 1,
        "rect": (303, 80, 507, 248),
        "label": "Figure 1",
        "caption": "固定网格上的 hard caching 与按缓存 headroom 跳步的 SoftCache 对比，保留 off-grid landing 放大示意；不是本地质量或速度结果。",
    },
    "2610.21555-muon-paired-budget": {
        "pdf_url": "https://arxiv.org/pdf/2610.21555v1",
        "page": 5,
        "rect": (113, 88, 500, 340),
        "label": "Figure 3",
        "caption": "冻结23候选池的validation-AUC regret曲线及预算检查点；作者结果，不是本地新训练曲线。",
    },
    "2610.22330-langdit": {
        "pdf_url": "https://arxiv.org/pdf/2610.22330v1",
        "page": 5,
        "rect": (65, 110, 525, 580),
        "label": "Figure 3",
        "caption": "完整保留 denoising Transformer、likelihood shortcut 和训练/推理 self-conditioning 两分支；原自动裁剪遗漏了上半部分。",
    },
    "2610.21138-clean-rm": {
        "pdf_url": "https://arxiv.org/pdf/2610.21138v1",
        "page": 2,
        "rect": (65, 55, 548, 187),
        "label": "Figure 1",
        "caption": "完整保留两侧案例：明确指令与模糊指令产生不同的样本级反馈噪声；不是本地模型输出。",
    },
    "2610.21267-tracer": {
        "pdf_url": "https://arxiv.org/pdf/2610.21267v1",
        "page": 3,
        "rect": (40, 40, 555, 218),
        "label": "Figure 2",
        "caption": "完整执行前缀树示意：同一工具在不同完整前缀下拥有不同后继与转移频率；不是本地能力评测轨迹。",
    },
    "2610.19844-smrc-pmrc": {
        "pdf_url": "https://arxiv.org/pdf/2610.19844v1",
        "page": 4,
        "rect": (100, 75, 512, 245),
        "label": "Algorithm 2",
        "caption": "多阶段 SMRC：投影内动量、子空间外残差与换基前参数边界修正。",
    },
    "autoformbench": {
        "pdf_url": "https://raw.githubusercontent.com/facebookresearch/autoformbench/af1aa38fd44e019e566bce0b5a168609a886d8e6/paper.pdf",
        "page": 3,
        "rect": (65, 200, 548, 391),
        "label": "Figure 2",
        "caption": "AutoformBench 原论文评测协议：隔离 Lean 工作区、工具反馈与 clean-room 独立验证；图中原文访问条件不同于公开 source-free 发布。",
    },
    "2610.12102-data-space-iteration": {
        "pdf_url": "https://arxiv.org/pdf/2610.12102",
        "page": 0,
        "rect": (106, 439, 508, 601),
        "label": "Figure 1",
        "caption": "概率流空间的离散时间迭代与共享生成器的数据空间循环对比；为原论文方法图，非本地生成结果。",
    },
    "2610.12375-ontrack": {
        "pdf_url": "https://arxiv.org/pdf/2610.12375",
        "page": 4,
        "rect": (50, 54, 302, 289),
        "label": "Figure 3",
        "caption": "玩具轨迹的代价矩阵与最优传输对齐：无关的天气工具调用无法匹配参考步骤，产生接近 1 的泄漏质量。",
    },
    "2610.12444-adamw4bit": {
        "pdf_url": "https://arxiv.org/pdf/2610.12444",
        "page": 20,
        "rect": (105, 78, 508, 236),
        "label": "Figure 7",
        "caption": "2.7B 预训练的验证损失对照与 LM-head 随机舍入切换；为原论文结果，非本地 WikiText 短跑。",
    },
    "2610.11575-elastic-expert-routing": {
        "pdf_url": "https://arxiv.org/pdf/2610.11575",
        "page": 0,
        "rect": (303, 217, 530, 473),
        "label": "Figure 1",
        "caption": "固定 top-k 的硬截断与 Elastic Expert Routing 的离散高斯预算及平滑监督对比。",
    },
    "2609.26355-pact": {
        "pdf_url": "https://arxiv.org/pdf/2609.26355",
        "page": 6,
        "rect": (70, 72, 540, 355),
        "label": "Figure 2",
        "caption": "PPO 的独立更新与 PACT 的 Actor-then-Critic、IS 校正流程对比。",
    },
    "2609.10750-skill-retention": {
        "pdf_url": "https://arxiv.org/pdf/2609.10750",
        "page": 4,
        "rect": (42, 45, 555, 474),
        "label": "Table 1–3",
        "caption": (
            "真实任务、合成任务与 OOD rings 上的遗忘对照，以及 anchor/LwF/EWC/"
            "L2-init 等缓解方法比较。"
        ),
    },
    "2609.11677-ecdysis": {
        "pdf_url": "https://arxiv.org/pdf/2609.11677",
        "page": 3,
        "rect": (294, 35, 588, 451),
        "label": "Algorithm 1",
        "caption": "Ecdysis 的批级失败聚合、FDCR 诊断与 harness 接纳循环。",
    },
    "mlsys2026-prompts": {
        "pdf_url": "https://storage.googleapis.com/gweb-research2023-media/pubtools/1038279.pdf",
        "page": 2,
        "rect": (55, 55, 557, 735),
        "label": "Figure 2",
        "caption": "PROMPTS Coordinator、Analyzer、Proposal 与 Sharding Memory 的整体工作流。",
    },
    "2608.06291-bakron": {
        "pdf_url": "https://arxiv.org/pdf/2608.06291",
        "page": 6,
        "rect": (78, 64, 536, 666),
        "label": "Algorithm 5–6",
        "caption": (
            "BaKron recursive divide-and-conquer algorithm and the final algorithm "
            "that combines recursion with parallel anti-diagonal processing."
        ),
    },
    "2205.00445-mrkl": {
        "pdf_url": "https://arxiv.org/pdf/2205.00445",
        "page": 3,
        "rect": (96, 96, 518, 574),
        "label": "方法定义（第 4 页）",
        "caption": (
            "MRKL architecture definition: an extensible set of neural or symbolic "
            "experts and a router that sends each natural-language input to the "
            "best module."
        ),
    },
    "sigir2026-pin-scale-pin-scale": {
        "pdf_url": "https://sigir2026.org/SIGIR2026_program.pdf",
        "page": 95,
        "rect": (302, 344, 565, 608),
        "label": "官方摘要 P074",
        "caption": (
            "Official SIGIR 2026 abstract of the Pin-SCALE framework, including "
            "cascading pooling, engagement-aware tokenization and multi-view "
            "contrastive learning."
        ),
    },
}

POSITIVE = {
    "architecture": 24,
    "framework": 22,
    "overview": 19,
    "pipeline": 18,
    "workflow": 18,
    "diagram": 16,
    "system": 12,
    "structure": 12,
    "implementation": 11,
    "proposed": 10,
    "model": 9,
    "network": 9,
    "method": 8,
    "approach": 7,
    "training": 5,
    "agent": 3,
}
NEGATIVE = {
    "result": -15,
    "performance": -14,
    "comparison": -13,
    "ablation": -18,
    "accuracy": -12,
    "distribution": -9,
    "case study": -8,
    "example": -5,
    "visualization": -5,
}


@dataclass
class Paper:
    page: Path
    paper_url: str
    arxiv_id: str
    title: str


@dataclass
class FigureResult:
    page: str
    paper_url: str
    arxiv_id: str
    figure: str
    original_caption: str
    source_url: str
    extraction: str
    asset: str
    width: int
    height: int
    score: int
    error: str = ""


def fetch(url: str, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == attempts - 1:
                raise
            time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"unable to fetch {url}")


def normalize_arxiv_id(value: str) -> str:
    value = value.split("/")[-1].removesuffix(".pdf")
    return re.sub(r"v\d+$", "", value)


def discover() -> list[Paper]:
    papers: list[Paper] = []
    for root in DOC_ROOTS:
        for page in sorted(root.glob("*/README.md")):
            text = page.read_text(encoding="utf-8")
            if "## 论文信息" not in text:
                continue
            link = re.search(
                r"\|\s*论文链接\s*\|\s*\[[^\]]+\]\((https?://[^)]+)\)", text
            )
            if not link:
                continue
            paper_url = link.group(1)
            arxiv = re.search(r"arxiv\.org/(?:abs|pdf)/([^)/\s]+)", paper_url)
            title = text.splitlines()[0].removeprefix("#").strip()
            papers.append(
                Paper(
                    page=page,
                    paper_url=paper_url,
                    arxiv_id=normalize_arxiv_id(arxiv.group(1)) if arxiv else "",
                    title=title,
                )
            )
    return papers


def title_terms(title: str) -> set[str]:
    ignored = {
        "with",
        "from",
        "using",
        "based",
        "towards",
        "large",
        "language",
        "model",
        "models",
        "recommendation",
        "system",
        "systems",
    }
    return {
        token.lower()
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]+", title)
        if len(token) >= 4 and token.lower() not in ignored
    }


def caption_score(caption: str, index: int, title: str = "") -> int:
    lowered = " ".join(caption.lower().split())
    score = max(0, 10 - index)
    for needle, weight in POSITIVE.items():
        if needle in lowered:
            score += weight
    for needle, weight in NEGATIVE.items():
        if needle in lowered:
            score += weight
    for term in title_terms(title):
        if term in lowered:
            score += 22
    if index == 1:
        score += 7
    return score


def figure_number(caption: str, fallback: int) -> str:
    match = re.search(r"\b(?:figure|fig\.?)\s*([0-9]+[a-z]?)", caption, re.I)
    return f"Figure {match.group(1)}" if match else f"Figure {fallback}"


def html_candidates(arxiv_id: str) -> Iterable[tuple[str, bytes]]:
    for url in (
        f"https://arxiv.org/html/{arxiv_id}",
        f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}",
    ):
        try:
            yield url, fetch(url)
        except Exception:
            continue


def choose_html_figure(
    arxiv_id: str,
    title: str,
    preferred_figure: str = "",
    preferred_caption: str = "",
) -> tuple[bytes, str, str, str, int] | None:
    for page_url, body in html_candidates(arxiv_id):
        soup = BeautifulSoup(body, "html.parser")
        ranked: list[tuple[int, int, str, str]] = []
        for index, figure in enumerate(soup.find_all("figure"), start=1):
            caption_node = figure.find("figcaption")
            caption = (
                " ".join(caption_node.get_text(" ", strip=True).split())
                if caption_node
                else ""
            )
            numbered = re.match(r"^(?:Figure|Fig\.)\s*([0-9]+[a-z]?)", caption, re.I)
            if preferred_caption:
                if preferred_caption.lower() not in caption.lower():
                    continue
            elif preferred_figure:
                if not numbered or numbered.group(1).lower() != preferred_figure.lower():
                    continue
            elif caption and not numbered:
                continue
            images = figure.find_all("img")
            for image in images:
                src = image.get("src")
                if not src:
                    continue
                ranked.append(
                    (
                        caption_score(caption, index, title),
                        index,
                        caption,
                        urllib.parse.urljoin(page_url, src),
                    )
                )
        for score, index, caption, image_url in sorted(
            ranked, key=lambda item: (-item[0], item[1])
        ):
            try:
                image_bytes = fetch(image_url)
                with Image.open(io.BytesIO(image_bytes)) as image:
                    if image.width < 400 or image.height < 140:
                        continue
                return (
                    image_bytes,
                    caption,
                    figure_number(caption, index),
                    image_url,
                    score,
                )
            except Exception:
                continue
    return None


def find_pdf_caption(page, index: int, title: str) -> list[tuple[int, object, str]]:
    candidates = []
    for block in page.get_text("blocks"):
        rect = block[:4]
        text = " ".join(str(block[4]).split())
        if not re.match(r"^(?:Figure|Fig\.)\s*\d+", text, re.I):
            continue
        candidates.append((caption_score(text, index, title), rect, text))
    return candidates


def choose_local_pdf_figure(
    pdf_path: Path,
    source_url: str,
    title: str,
    preferred_figure: str = "",
) -> tuple[bytes, str, str, str, int] | None:
    import fitz

    document = fitz.open(pdf_path)
    ranked = []
    for page_index, page in enumerate(document):
        for score, rect, caption in find_pdf_caption(page, page_index + 1, title):
            if preferred_figure:
                match = re.match(r"^(?:Figure|Fig\.)\s*([0-9]+[a-z]?)", caption, re.I)
                if not match or match.group(1).lower() != preferred_figure.lower():
                    continue
            ranked.append((score, page_index, rect, caption))
    for score, page_index, raw_rect, caption in sorted(ranked, reverse=True):
        page = document[page_index]
        caption_rect = fitz.Rect(raw_rect)
        page_rect = page.rect
        if caption_rect.width < page_rect.width * 0.62:
            pad = page_rect.width * 0.035
            left = max(page_rect.x0, caption_rect.x0 - pad)
            right = min(page_rect.x1, caption_rect.x1 + pad)
        else:
            left, right = page_rect.x0, page_rect.x1

        # Most scholarly captions sit immediately below their figure.  This
        # bounded crop intentionally includes the caption as provenance.
        top = max(page_rect.y0, caption_rect.y0 - page_rect.height * 0.47)
        bottom = min(page_rect.y1, caption_rect.y1 + 10)
        clip = fitz.Rect(left, top, right, bottom)
        pixmap = page.get_pixmap(matrix=fitz.Matrix(2.2, 2.2), clip=clip, alpha=False)
        if pixmap.width < 500 or pixmap.height < 180:
            continue
        return (
            pixmap.tobytes("png"),
            caption,
            figure_number(caption, 1),
            f"{source_url}#page={page_index + 1}",
            score,
        )
    return None


def choose_pdf_figure(
    arxiv_id: str, title: str, preferred_figure: str = "",
) -> tuple[bytes, str, str, str, int] | None:
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
    pdf_path = TMP / f"{arxiv_id}.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    if not pdf_path.exists():
        pdf_path.write_bytes(fetch(pdf_url))
    return choose_local_pdf_figure(pdf_path, pdf_url, title, preferred_figure)


def choose_special_crop(
    slug: str,
) -> tuple[bytes, str, str, str, int] | None:
    import fitz

    spec = SPECIAL_CROPS.get(slug)
    if not spec:
        return None
    pdf_path = TMP / f"{slug}.pdf"
    # Reuse a cached canonical arXiv PDF before downloading the same public
    # document under its slug, especially for image-heavy papers.
    identifier = re.match(r"^(\d{4}\.\d{4,5})(?:-|$)", slug)
    canonical_pdf = TMP / f"{identifier.group(1)}.pdf" if identifier else None
    if not pdf_path.exists() and canonical_pdf is not None and canonical_pdf.exists():
        pdf_path = canonical_pdf
    if not pdf_path.exists():
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(fetch(str(spec["pdf_url"])))
    document = fitz.open(pdf_path)
    page = document[int(spec["page"])]
    clip = fitz.Rect(spec["rect"])
    pixmap = page.get_pixmap(matrix=fitz.Matrix(2.3, 2.3), clip=clip, alpha=False)
    return (
        pixmap.tobytes("png"),
        str(spec["caption"]),
        str(spec["label"]),
        f"{spec['pdf_url']}#page={int(spec['page']) + 1}",
        100,
    )


def choose_manual_pdf(
    slug: str, title: str,
) -> tuple[bytes, str, str, str, int] | None:
    url = MANUAL_PDFS.get(slug)
    if not url:
        return None
    pdf_path = TMP / f"{slug}.pdf"
    if not pdf_path.exists():
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_bytes(fetch(url))
    return choose_local_pdf_figure(
        pdf_path, url, title, MANUAL_FIGURE_NUMBERS.get(slug, "")
    )


def save_png(image_bytes: bytes, target: Path) -> tuple[int, int]:
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(io.BytesIO(image_bytes)) as source:
        image = source.convert("RGB")
        if image.width > 1800:
            height = round(image.height * 1800 / image.width)
            image = image.resize((1800, height), Image.Resampling.LANCZOS)
        image.save(target, "PNG", optimize=True)
        return image.width, image.height


def chinese_description(caption: str) -> str:
    lower = caption.lower()
    if "pipeline" in lower or "workflow" in lower:
        return "展示原论文的整体流程、关键阶段及其数据流向。"
    if "architecture" in lower or "framework" in lower or "structure" in lower:
        return "展示原论文提出的核心架构、主要模块及其连接关系。"
    if "training" in lower:
        return "展示原论文的训练流程与关键优化环节。"
    return "展示原论文方法的总体设计和关键组成。"


def update_page(paper: Paper, result: FigureResult) -> None:
    text = paper.page.read_text(encoding="utf-8")
    description = chinese_description(result.original_caption)
    reviewed_descriptions = {
        "2610.22130-drop-kv": "RULER 准确率随序列长度与 KV cache 预算的变化；这是原论文评测曲线，不是架构图或本地测量。",
        "2610.22245-disagreement-routing": "三个 benchmark 的准确率—路由预算曲线及其与最优路由的差距；这是原论文结果，不是本地合成探针能力。",
        "2610.22353-mirror-moe": "训练中的专家抑制、有效专家数及最小混合比 ξ 的变化；这是原论文训练诊断，不是本地预训练结果。",
    }
    description = reviewed_descriptions.get(paper.page.parent.name, description)
    if paper.page.parent.name in (
        "2610.21138-clean-rm", "2610.21267-tracer", "2610.21281-diviner",
        "2610.21412-jev-agent-harness", "2610.20782-memory-mosaics-plus",
        "2610.21323-adaloop-vision", "2610.22369-softcache", "2610.22075-rr-vlm",
    ):
        description = str(SPECIAL_CROPS[paper.page.parent.name]["caption"])
    if paper.page.parent.name == "2610.12375-ontrack":
        description = str(SPECIAL_CROPS[paper.page.parent.name]["caption"])
    if paper.page.parent.name == "2610.12327-sparse-decoding":
        description = "对比固定文本校准与排除 prefill 的自回归校准，以及传统稀疏 SpMM 和逐 token bitmask SpMV。图中加速与 OBS 后端属于原论文；本地为 Wanda 替代后端和独立 kernel。"
    if paper.page.parent.name == "2610.11794-memento3":
        description = "观察失配、反思、规则修正、编译与双重验证构成冻结 LLM 的世界模型学习闭环；图中由镜像假设修正为徽章顺时针旋转规则。为原论文示例，不是本地成功轨迹。"
    block = (
        f"{START}\n"
        f"### 原论文关键图\n\n"
        f"[![{paper.title} 原论文 {result.figure}](assets/paper-figure-01.png)]"
        f"({result.source_url})\n\n"
        f"> **原论文 {result.figure}（关键图）**：{description}"
        f"图片来自[原论文]({paper.paper_url})，版权归原作者所有；点击图片可查看来源。\n"
        f"{END}"
    )
    if START in text and END in text:
        text = re.sub(
            rf"{re.escape(START)}.*?{re.escape(END)}", block, text, flags=re.S
        )
    else:
        marker = "### 核心公式"
        if marker not in text:
            raise ValueError("missing 核心公式 section")
        text = text.replace(marker, f"{block}\n\n{marker}", 1)
    paper.page.write_text(text, encoding="utf-8")


def process(paper: Paper, refresh: bool) -> FigureResult:
    slug = paper.page.parent.name
    if not paper.arxiv_id and slug not in MANUAL_PDFS and slug not in SPECIAL_CROPS:
        return FigureResult(
            page=str(paper.page.relative_to(ROOT)),
            paper_url=paper.paper_url,
            arxiv_id="",
            figure="",
            original_caption="",
            source_url="",
            extraction="unsupported",
            asset="",
            width=0,
            height=0,
            score=0,
            error="non-arXiv source requires a manual figure mapping",
        )
    target = paper.page.parent / "assets" / "paper-figure-01.png"
    page_text = paper.page.read_text(encoding="utf-8")
    if target.exists() and not refresh and START in page_text:
        with Image.open(target) as image:
            width, height = image.size
        block_match = re.search(
            rf"{re.escape(START)}(.*?){re.escape(END)}", page_text, re.S
        )
        block = block_match.group(1) if block_match else ""
        label_match = re.search(r"\*\*原论文 (.+?)（关键图）\*\*", block)
        source_match = re.search(
            r"\]\(assets/paper-figure-01\.png\)\]\((https?://[^)]+)\)", block
        )
        return FigureResult(
            page=str(paper.page.relative_to(ROOT)),
            paper_url=paper.paper_url,
            arxiv_id=paper.arxiv_id,
            figure=label_match.group(1) if label_match else "existing",
            original_caption="",
            source_url=source_match.group(1) if source_match else paper.paper_url,
            extraction="existing",
            asset=str(target.relative_to(ROOT)),
            width=width,
            height=height,
            score=0,
        )
    try:
        selected = choose_special_crop(slug)
        extraction = "reviewed-source-crop" if selected is not None else ""
        if selected is None and slug in {"2610.13285-boundary-evo", "2610.13521-road-mopd"}:
            # Reviewed original PDF Fig.2 is the method diagram. HTML numbering
            # differs; do not replace it with a high-scoring introductory plot.
            selected = choose_pdf_figure(paper.arxiv_id, paper.title, "2")
            extraction = "arxiv-pdf-crop"
        if selected is None and paper.arxiv_id:
            selected = choose_html_figure(
                paper.arxiv_id,
                paper.title,
                FIGURE_OVERRIDES.get(slug, ""),
                CAPTION_OVERRIDES.get(slug, ""),
            )
            extraction = "arxiv-html"
        if selected is None and paper.arxiv_id:
            selected = choose_pdf_figure(
                paper.arxiv_id, paper.title, FIGURE_OVERRIDES.get(slug, "")
            )
            extraction = "arxiv-pdf-crop"
        if selected is None:
            selected = choose_manual_pdf(slug, paper.title)
            extraction = "published-pdf-crop"
        if selected is None:
            raise RuntimeError("no suitable figure found")
        image_bytes, caption, label, source_url, score = selected
        width, height = save_png(image_bytes, target)
        result = FigureResult(
            page=str(paper.page.relative_to(ROOT)),
            paper_url=paper.paper_url,
            arxiv_id=paper.arxiv_id,
            figure=label,
            original_caption=caption,
            source_url=source_url,
            extraction=extraction,
            asset=str(target.relative_to(ROOT)),
            width=width,
            height=height,
            score=score,
        )
        update_page(paper, result)
        return result
    except Exception as exc:
        return FigureResult(
            page=str(paper.page.relative_to(ROOT)),
            paper_url=paper.paper_url,
            arxiv_id=paper.arxiv_id,
            figure="",
            original_caption="",
            source_url="",
            extraction="failed",
            asset="",
            width=0,
            height=0,
            score=0,
            error=f"{type(exc).__name__}: {exc}",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", action="append", default=[], help="arXiv id or slug substring")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--workers", type=int, default=3)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    papers = discover()
    if args.only:
        needles = tuple(args.only)
        papers = [
            paper
            for paper in papers
            if any(
                needle in paper.arxiv_id or needle in paper.page.parent.name
                for needle in needles
            )
        ]
    if args.limit:
        papers = papers[: args.limit]

    results: list[FigureResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = {pool.submit(process, paper, args.refresh): paper for paper in papers}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            status = "OK" if not result.error else "FAIL"
            print(f"[{status}] {result.page}: {result.extraction} {result.figure} {result.error}")

    results.sort(key=lambda item: item.page)
    existing = []
    if MANIFEST.exists() and args.only:
        existing = json.loads(MANIFEST.read_text(encoding="utf-8"))
        touched = {result.page for result in results}
        existing = [item for item in existing if item["page"] not in touched
                    and (ROOT / item["page"]).is_file()]
    MANIFEST.write_text(
        json.dumps(existing + [asdict(result) for result in results], ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    failures = sum(bool(result.error) for result in results)
    print(f"processed={len(results)} failures={failures} manifest={MANIFEST.relative_to(ROOT)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
