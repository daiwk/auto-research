from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class PaperMetadata:
    arxiv_id: str
    title: str
    url: str
    track: str
    code_url: str | None = None

    def to_dict(self) -> dict[str, str]:
        values = {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "url": self.url,
            "track": self.track,
        }
        if self.code_url:
            values["code"] = self.code_url
        return values


RunFunction = Callable[[Path, int], dict[str, Any]]
RenderFunction = Callable[[dict[str, Any]], str]


class ReproductionFidelity(str, Enum):
    FULL_PIPELINE = "full_pipeline"
    CORE_MECHANISM = "core_mechanism"
    CONCEPT_DEMO = "concept_demo"

    @property
    def label(self) -> str:
        return {
            self.FULL_PIPELINE: "完整核心链路复现",
            self.CORE_MECHANISM: "核心机制复现",
            self.CONCEPT_DEMO: "概念验证（非论文复现）",
        }[self]

    @property
    def description(self) -> str:
        return {
            self.FULL_PIPELINE: "论文的核心模型、训练阶段和推理路径均实际执行，仅缩小公开数据与模型规模。",
            self.CORE_MECHANISM: "论文中心算法被实际执行，但生产模型、私有特征或基础设施未复刻。",
            self.CONCEPT_DEMO: "至少一个决定论文结论的核心模型或训练阶段被代理替代，结果不得视为论文复现。",
        }[self]


@dataclass(frozen=True)
class ReproductionAdapter:
    """Everything unique to one paper, behind a stable runner interface."""

    key: str
    paper: PaperMetadata
    run: RunFunction
    render: RenderFunction
    fidelity: ReproductionFidelity = ReproductionFidelity.CONCEPT_DEMO
    omitted_core_components: tuple[str, ...] = ()
