from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable


@dataclass(frozen=True)
class OnlineABEvidence:
    product: str
    metric: str
    lift_percent: float
    traffic: str
    source_url: str | None = None
    source_location: str | None = None
    experiment_duration: str | None = None
    significance: str | None = None
    retrieved_at: str | None = None

    def to_dict(self) -> dict[str, str | float]:
        values = {
            "product": self.product,
            "metric": self.metric,
            "lift_percent": self.lift_percent,
            "traffic": self.traffic,
        }
        for key in (
            "source_url", "source_location", "experiment_duration",
            "significance", "retrieved_at",
        ):
            value = getattr(self, key)
            if value:
                values[key] = value
        return values


@dataclass(frozen=True)
class PaperMetadata:
    arxiv_id: str
    title: str
    url: str
    track: str
    code_url: str | None = None
    organization: str | None = None
    published: str | None = None
    publication_label: str | None = None
    publication_source: str | None = None
    topics: tuple[str, ...] = ()
    online_ab: tuple[OnlineABEvidence, ...] = ()
    selection_exception: str | None = None

    def to_dict(self) -> dict[str, Any]:
        values = {
            "arxiv_id": self.arxiv_id,
            "title": self.title,
            "url": self.url,
            "track": self.track,
        }
        if self.code_url:
            values["code"] = self.code_url
        if self.organization:
            values["organization"] = self.organization
        if self.published:
            values["published"] = self.published
        if self.publication_label:
            values["publication_label"] = self.publication_label
        if self.publication_source:
            values["publication_source"] = self.publication_source
        if self.topics:
            values["topics"] = list(self.topics)
        if self.online_ab:
            values["online_ab"] = [entry.to_dict() for entry in self.online_ab]
        if self.selection_exception:
            values["selection_exception"] = self.selection_exception
        return values

    @property
    def has_online_ab(self) -> bool:
        return bool(self.online_ab)

    def validate_catalog_entry(self) -> None:
        """Enforce online A/B evidence for newly catalogued industrial papers."""
        catalogued = bool(self.organization or self.published or self.topics)
        if (
            self.track == "recommendation"
            and catalogued
            and not self.online_ab
            and not self.selection_exception
        ):
            raise ValueError(
                f"catalogued paper {self.arxiv_id} has no quantified online A/B evidence; "
                "only an explicit user-requested classic exception may bypass this gate"
            )


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


class EvaluationTier(str, Enum):
    """How much empirical evidence a local reproduction actually executes."""

    CONTRACT = "l0_contract"
    MECHANISM = "l1_mechanism"
    PUBLIC_DATASET = "l2_public_dataset"
    PAPER_PIPELINE = "l3_paper_pipeline"

    @property
    def label(self) -> str:
        return {
            self.CONTRACT: "L0 接口/张量验证",
            self.MECHANISM: "L1 核心机制 mini-suite",
            self.PUBLIC_DATASET: "L2 公开数据集训练",
            self.PAPER_PIPELINE: "L3 接近论文训练链路",
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
    evaluation_tier: EvaluationTier = EvaluationTier.PUBLIC_DATASET
    datasets: tuple[str, ...] = ()
    baseline: str | None = None
    metrics: tuple[str, ...] = ()
    default_seeds: tuple[int, ...] = (42,)
    budget: str = "paper-specific"
    device_capabilities: tuple[str, ...] = ("cpu",)
    infer_device_capabilities: bool = True
