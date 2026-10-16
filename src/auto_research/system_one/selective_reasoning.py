"""Pinned CPU statistical replay and gold-free start/read/stop interfaces.

The public release contains pre-scored measurements, not online model traces.
Only the reviewed, hash-pinned recompute.py is executable through this module.
"""
from __future__ import annotations

from dataclasses import dataclass
import csv
import hashlib
import io
import json
import math
from pathlib import Path, PurePosixPath
import subprocess
import sys
from types import MappingProxyType
import urllib.request
import zipfile


UPSTREAM = "https://github.com/binzheng-joey/selective-reasoning"
REVISION = "26795854fe148e7a4caa37ef6cc051431b8b8790"
RELEASE = "v1.0"
ARCHIVES = MappingProxyType({
    "coling2027-data.zip": ("1f82d594eb67556cec89cac810a9852f3d90e44a3b12bf51c732946ce54448ac", 2_843_249),
    "coling2027-software.zip": ("11819e28329d28f6e89f70c3b2d0fd532ea11b7341e97f3d9f8cf590d9c4b3a8", 216_170),
})
REPLAY_PREFIX = "coling2027-paper/reproducibility/"
EXTRACT = MappingProxyType({
    "coling2027-data.zip": tuple(REPLAY_PREFIX + "data/" + name for name in (
        "manifest.json", "metadata.json", "records.csv", "expected.json",
    )),
    "coling2027-software.zip": (REPLAY_PREFIX + "recompute.py", REPLAY_PREFIX + "README.md"),
})
SERIES_COUNT = 9
MEASUREMENT_COUNT = 29_808
NUMERIC_CHECK_COUNT = 16_888


class ProtocolError(ValueError):
    pass


def _archive_bytes(directory: Path, name: str) -> bytes:
    path = directory / name
    expected, size = ARCHIVES[name]
    if path.is_symlink() or not path.is_file() or path.stat().st_size != size:
        raise ProtocolError(f"missing or unexpected-sized fixed release archive: {name}")
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ProtocolError(f"fixed release archive hash mismatch: {name}")
    return raw


def fetch_release(directory: Path) -> dict:
    """Download only the two fixed ~3 MB public archives, never model weights."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    for name, (digest, size) in ARCHIVES.items():
        path = directory / name
        if path.exists() or path.is_symlink():
            _archive_bytes(directory, name)
            continue
        url = f"{UPSTREAM}/releases/download/{RELEASE}/{name}"
        request = urllib.request.Request(url, headers={"User-Agent": "auto-research-selective-replay/1.0"})
        with urllib.request.urlopen(request, timeout=25) as response:
            raw = response.read(size + 1)
        if len(raw) != size or hashlib.sha256(raw).hexdigest() != digest:
            raise ProtocolError("upstream release byte count/hash mismatch")
        with path.open("xb") as handle:
            handle.write(raw)
    return {"release": RELEASE, "revision": REVISION,
            "archives": {name: digest for name, (digest, _) in ARCHIVES.items()},
            "model_or_benchmark_downloaded": False}


def extract_release(archive_directory: Path, destination: Path) -> dict:
    """Allowlist only the six reviewed CPU files; never extract historical jobs."""
    destination = Path(destination)
    if destination.exists() or destination.is_symlink():
        raise ProtocolError("choose a new immutable extraction directory")
    files = {}
    for name in ARCHIVES:
        archive = zipfile.ZipFile(io.BytesIO(_archive_bytes(Path(archive_directory), name)))
        members = archive.infolist()
        names = [member.filename for member in members]
        if len(names) != len(set(names)):
            raise ProtocolError("duplicate archive member")
        for relative in EXTRACT[name]:
            member = archive.getinfo(relative)
            path = PurePosixPath(relative)
            if path.is_absolute() or ".." in path.parts or member.file_size > 5_000_000:
                raise ProtocolError("unsafe or oversized release member")
            if member.is_dir() or (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ProtocolError("release member must be a regular file")
            files[relative] = archive.read(member)
    destination.mkdir(parents=True)
    hashes = {}
    for relative, raw in files.items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            handle.write(raw)
        hashes[relative] = hashlib.sha256(raw).hexdigest()
    return hashes


def _load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def validate_replay_inputs(directory: Path) -> dict:
    """Check fixed measurement identity before executing the reviewed script."""
    data = directory / REPLAY_PREFIX / "data"
    manifest = _load_json(data / "manifest.json")
    if manifest.get("schema_version") != 1 or len(manifest.get("series", ())) != SERIES_COUNT:
        raise ProtocolError("unexpected upstream series inventory")
    for name, digest in manifest["files"].items():
        if name not in {"metadata.json", "records.csv", "expected.json"}:
            raise ProtocolError("unexpected upstream manifest input")
        if hashlib.sha256((data / name).read_bytes()).hexdigest() != digest:
            raise ProtocolError(f"changed upstream measurement input: {name}")
    with (data / "records.csv").open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        expected_fields = ["series", "question_id", "method", "repeat", "accuracy", "pipeline_seconds",
                           "physical_output_tokens", "generation_tokens", "full_reads", "trigger_calls",
                           "input_tokens", "cached_input_tokens", "reasoning_rate", "early_stop_rate",
                           "invalid_rate", "budget_hit_rate"]
        if reader.fieldnames != expected_fields:
            raise ProtocolError("released statistical records must match the fixed numeric schema")
        count = sum(1 for _ in reader)
    if count != MEASUREMENT_COUNT:
        raise ProtocolError("unexpected upstream measurement count")
    return {"series_count": len(manifest["series"]), "measurement_rows": count,
            "bootstrap_draws": manifest["bootstrap_draws"], "bootstrap_seed": manifest["seed"],
            "series_ids": [series["id"] for series in manifest["series"]]}


def replay_official(archive_directory: Path, output: Path, *, maximum_seconds: int = 180) -> dict:
    """Run unmodified upstream statistics; never import a score as local capability."""
    if not isinstance(maximum_seconds, int) or not 1 <= maximum_seconds <= 180:
        raise ProtocolError("CPU replay budget must be 1..180 seconds")
    output = Path(output)
    if output.exists() or output.is_symlink():
        raise ProtocolError("choose a new immutable output directory")
    # Authenticate both archives before creating any output or running code.
    for name in ARCHIVES:
        _archive_bytes(Path(archive_directory), name)
    hashes = extract_release(Path(archive_directory), output / "source")
    inventory = validate_replay_inputs(output / "source")
    replay = output / "source" / REPLAY_PREFIX
    command = [sys.executable, "-I", str(replay / "recompute.py"), "--data", str(replay / "data"),
               "--output", str(output / "statistics"), "--check"]
    try:
        process = subprocess.run(command, check=True, capture_output=True, text=True,
                                 timeout=maximum_seconds)
        computed = _load_json(output / "statistics/summary.json")
        checks = computed.get("checks", {})
        numeric = sum(row.get("numeric_values_checked", 0) for row in checks.values())
        if set(checks) != set(inventory["series_ids"]) or numeric != NUMERIC_CHECK_COUNT or any(
            row.get("state") != "passed" for row in checks.values()
        ):
            raise ProtocolError("upstream fixed-check inventory does not match")
        artifact = {
            "schema_version": 2, "paper": "selective-reasoning", "upstream_revision": REVISION,
            "upstream_release": RELEASE, "source": UPSTREAM, "source_sha256": hashes,
            "archive_sha256": {name: digest for name, (digest, _) in ARCHIVES.items()},
            "evidence_kind": "official_measurement_recomputation", "evaluation_tier": "l0_interface",
            "diagnostic_only": True, "promotion_eligible": False,
            "local_capability_score": None, "model_inference_performed": False,
            "raw_trace_or_prefix_relations_verified": False,
            "full_experiment_status": "not_reproduced_high_cost",
            "metrics": {**inventory, "numeric_values_checked": numeric, "all_fixed_checks_passed": True},
            "official_reference_statistics": computed,
            "command": "python -I <pinned-release>/recompute.py --data <release-data> --output <statistics> --check",
            "stdout": process.stdout.replace(str(output), "<run>"),
        }
    except (subprocess.SubprocessError, ProtocolError, OSError, ValueError) as error:
        with (output / "failure.json").open("x", encoding="utf-8") as handle:
            json.dump({"status": "failed", "error_type": type(error).__name__,
                       "diagnostic_only": True, "promotion_eligible": False}, handle, indent=2)
        raise
    with (output / "result.json").open("x", encoding="utf-8") as handle:
        json.dump(artifact, handle, indent=2, ensure_ascii=False, allow_nan=False)
        handle.write("\n")
    return artifact


def _probabilities(values: tuple[float, ...]) -> tuple[float, ...]:
    p = tuple(float(value) for value in values)
    if len(p) < 2 or not all(math.isfinite(v) and 0 <= v <= 1 for v in p):
        raise ProtocolError("reader must provide >=2 finite candidate probabilities")
    if not math.isclose(sum(p), 1.0, abs_tol=1e-6):
        raise ProtocolError("candidate probabilities must sum to one")
    return p


def entropy_certainty(probabilities: tuple[float, ...]) -> float:
    p = _probabilities(probabilities)
    return 1 + sum(v * math.log(v) for v in p if v > 0) / math.log(len(p))


@dataclass(frozen=True)
class LinearGate:
    """Frozen standardized logistic gate; fitting is external train/dev only."""

    coefficients: tuple[float, ...]
    intercept: float
    means: tuple[float, ...]
    scales: tuple[float, ...]

    def __post_init__(self):
        if not self.coefficients or not (len(self.coefficients) == len(self.means) == len(self.scales)):
            raise ProtocolError("gate parameter dimensions must match")
        if not all(math.isfinite(x) for x in (*self.coefficients, self.intercept, *self.means, *self.scales)):
            raise ProtocolError("gate parameters must be finite")
        if any(x <= 0 for x in self.scales):
            raise ProtocolError("gate scales must be positive")

    def probability(self, features: tuple[float, ...]) -> float:
        if len(features) != len(self.coefficients) or not all(math.isfinite(v) for v in features):
            raise ProtocolError("public gate features must match frozen coefficients")
        score = self.intercept + sum(c * (v - m) / s for c, v, m, s in zip(
            self.coefficients, features, self.means, self.scales, strict=True
        ))
        return 1 / (1 + math.exp(-score)) if score >= 0 else math.exp(score) / (1 + math.exp(score))


@dataclass(frozen=True)
class PublicDecision:
    """Only solver-visible inputs; no dictionary passthrough or gold fields."""

    question: str
    candidates: tuple[str, ...]
    reasoning_prefix: str = ""

    @classmethod
    def from_mapping(cls, mapping: dict):
        allowed = {"question", "candidates", "reasoning_prefix"}
        if set(mapping) - allowed or not {"question", "candidates"} <= set(mapping):
            raise ProtocolError("only public question/candidates/reasoning_prefix are permitted")
        if not isinstance(mapping["question"], str) or not isinstance(mapping.get("reasoning_prefix", ""), str):
            raise ProtocolError("question and prefix must be text")
        candidates = mapping["candidates"]
        if not isinstance(candidates, (list, tuple)) or len(candidates) < 2 or any(
            not isinstance(candidate, str) or not candidate for candidate in candidates
        ):
            raise ProtocolError("at least two nonempty described candidates are required")
        return cls(mapping["question"], tuple(candidates), mapping.get("reasoning_prefix", ""))


@dataclass(frozen=True)
class SelectiveController:
    """An executable decision interface, not a replacement for the trained reader.

    Caller supplies a true reader's probabilities and frozen gate features.
    No correctness indicator or benchmark answer is accepted by this interface.
    """

    benefit_gate: LinearGate
    trigger_gate: LinearGate
    benefit_threshold: float
    trigger_threshold: float
    certainty_threshold: float = 0.70
    minimum_sentence_gap: int = 1
    token_budget: int = 1024

    def __post_init__(self):
        if not all(math.isfinite(v) and 0 <= v <= 1 for v in (
            self.benefit_threshold, self.trigger_threshold, self.certainty_threshold
        )) or self.minimum_sentence_gap < 1 or self.token_budget < 1:
            raise ProtocolError("invalid frozen controller thresholds/budgets")

    def start(self, probabilities: tuple[float, ...], features: tuple[float, ...]) -> dict:
        p = _probabilities(probabilities)
        reason = self.benefit_gate.probability(features) >= self.benefit_threshold
        return {"action": "reason" if reason else "answer", "candidate_index": None if reason else max(
            range(len(p)), key=p.__getitem__), "certainty": entropy_certainty(p)}

    def request_read(self, features: tuple[float, ...], *, sentences_since_read: int) -> bool:
        if sentences_since_read < 0:
            raise ProtocolError("sentence count cannot be negative")
        return (sentences_since_read >= self.minimum_sentence_gap and
                self.trigger_gate.probability(features) >= self.trigger_threshold)

    def accept_read(self, probabilities: tuple[float, ...], *, generated_tokens: int) -> dict:
        if generated_tokens < 0:
            raise ProtocolError("token count cannot be negative")
        p = _probabilities(probabilities)
        certainty = entropy_certainty(p)
        accepted, budget_hit = certainty >= self.certainty_threshold, generated_tokens >= self.token_budget
        answer = accepted or budget_hit
        return {"action": "answer" if answer else "continue", "candidate_index": max(
            range(len(p)), key=p.__getitem__) if answer else None,
            "certainty": certainty, "entropy_accepted": accepted, "budget_forced": budget_hit and not accepted}
