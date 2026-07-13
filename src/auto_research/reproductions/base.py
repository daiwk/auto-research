from __future__ import annotations

from dataclasses import dataclass
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


@dataclass(frozen=True)
class ReproductionAdapter:
    """Everything unique to one paper, behind a stable runner interface."""

    key: str
    paper: PaperMetadata
    run: RunFunction
    render: RenderFunction
