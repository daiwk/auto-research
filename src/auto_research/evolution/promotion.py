from __future__ import annotations

import json
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any


@dataclass(frozen=True)
class CandidatePluginSpec:
    candidate_id: str
    provider: str
    origin: str
    paper_ids: tuple[str, ...]
    files: dict[str, str]
    verification_command: tuple[str, ...] = ()

    @classmethod
    def from_file(cls, path: Path) -> "CandidatePluginSpec":
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["paper_ids"] = tuple(payload.get("paper_ids", ()))
        payload["verification_command"] = tuple(payload.get("verification_command", ()))
        spec = cls(**payload)
        spec.validate()
        return spec

    def validate(self) -> None:
        if self.origin not in {"retrieved-paper", "generated-combination", "novel-proposal"}:
            raise ValueError(f"unsupported candidate origin: {self.origin}")
        if not self.candidate_id.replace("-", "").replace("_", "").isalnum():
            raise ValueError("candidate_id must contain only letters, digits, '-' and '_'")
        if not self.files:
            raise ValueError("candidate must contain at least one file")
        for name, content in self.files.items():
            relative = PurePosixPath(name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"unsafe candidate path: {name}")
            if relative.suffix not in {".py", ".json", ".md"}:
                raise ValueError(f"unsupported candidate file type: {name}")
            if len(content.encode()) > 1_000_000:
                raise ValueError(f"candidate file exceeds 1 MB: {name}")


class CandidatePromotionPipeline:
    """Auditable staging gate; promotion always requires explicit human approval."""

    def __init__(self, project_dir: Path, root: Path = Path(".auto-research/candidates")):
        self.project_dir = project_dir.resolve()
        self.root = (self.project_dir / root).resolve()

    def stage(self, spec: CandidatePluginSpec) -> Path:
        spec.validate()
        directory = self.root / spec.candidate_id
        if directory.exists():
            raise ValueError(f"candidate already exists: {directory}")
        directory.mkdir(parents=True)
        for name, content in spec.files.items():
            destination = directory / name
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(content, encoding="utf-8")
        (directory / "candidate.json").write_text(
            json.dumps(asdict(spec), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        return directory

    def verify(self, candidate_id: str, timeout_seconds: int = 300) -> dict[str, Any]:
        directory = self.root / candidate_id
        spec = CandidatePluginSpec.from_file(directory / "candidate.json")
        python_files = [str(item) for item in directory.rglob("*.py")]
        command = list(spec.verification_command) or [
            sys.executable, "-m", "py_compile", *python_files,
        ]
        cwd = directory if spec.verification_command else self.project_dir
        completed = subprocess.run(
            command, cwd=cwd, capture_output=True, text=True,
            timeout=timeout_seconds, check=False,
        )
        record = {
            "candidate_id": candidate_id,
            "command": command,
            "returncode": completed.returncode,
            "stdout": completed.stdout[-20_000:],
            "stderr": completed.stderr[-20_000:],
            "passed": completed.returncode == 0,
        }
        (directory / "verification.json").write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        return record

    def promote(self, candidate_id: str, destination: Path, *, approved: bool) -> Path:
        if not approved:
            raise ValueError("candidate promotion requires explicit --approve")
        directory = self.root / candidate_id
        verification = json.loads((directory / "verification.json").read_text(encoding="utf-8"))
        if not verification.get("passed"):
            raise ValueError("candidate has not passed verification")
        target = (self.project_dir / destination).resolve()
        if self.project_dir not in target.parents:
            raise ValueError("promotion destination must stay inside the repository")
        if target.exists():
            raise ValueError(f"promotion destination already exists: {target}")
        target.mkdir(parents=True)
        for item in directory.rglob("*"):
            if item.is_file() and item.name not in {"candidate.json", "verification.json"}:
                relative = item.relative_to(directory)
                output = target / relative
                output.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, output)
        return target
