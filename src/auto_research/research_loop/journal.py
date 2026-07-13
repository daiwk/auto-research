from __future__ import annotations

import datetime as dt
import json
import os
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class ResearchStage(str, Enum):
    DISCOVERY = "discovery"
    IMPLEMENTATION = "implementation"
    EXPERIMENT = "experiment"
    REPORTING = "reporting"
    COMPLETE = "complete"


@dataclass(frozen=True)
class ResearchEvent:
    run_id: str
    stage: str
    event: str
    timestamp: str
    payload: dict[str, Any]


class ResearchJournal:
    """Append-only, machine-readable record of the research workflow."""

    def __init__(self, path: Path, run_id: str):
        self.path = path
        self.run_id = run_id
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(
        self, stage: ResearchStage, event: str, **payload: Any
    ) -> ResearchEvent:
        entry = ResearchEvent(
            run_id=self.run_id,
            stage=stage.value,
            event=event,
            timestamp=dt.datetime.now(dt.timezone.utc).isoformat(),
            payload=payload,
        )
        line = json.dumps(asdict(entry), ensure_ascii=False, sort_keys=True)
        descriptor = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o644)
        try:
            os.write(descriptor, (line + "\n").encode("utf-8"))
        finally:
            os.close(descriptor)
        return entry
