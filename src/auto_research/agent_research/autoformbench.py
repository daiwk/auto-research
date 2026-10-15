"""Pinned, evaluation-only AutoformBench task and result interfaces.

This module does not solve a theorem, run Lean, or execute Harbor.  Official
leaderboard CSVs are source-present reports, not results of the public
source-free task release.  No torch, model provider, or training dependency is
imported here.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass
from decimal import Decimal, InvalidOperation
import csv
import hashlib
import io
import json
from pathlib import Path
import re
from types import MappingProxyType
from typing import Mapping, Sequence
from urllib.request import urlopen


REPOSITORY = "https://github.com/facebookresearch/autoformbench"
REVISION = "af1aa38fd44e019e566bce0b5a168609a886d8e6"
RAW_ROOT = f"https://raw.githubusercontent.com/facebookresearch/autoformbench/{REVISION}"
LEAN_VERSION = "v4.32.2"
MATHLIB_REVISION = "905b95818eb32af7874a58b427f50c1711a5e96c"
HARBOR_VERSION = "0.22.0"
TASK_SCHEMA_VERSION = "1.4"
OFFICIAL_TASK_COUNT = 341
OFFICIAL_BUDGET_USD = Decimal("200")
MAX_FILE_BYTES = 1024 * 1024
MANIFEST_FIELDS = ("problem_id", "book", "target_count", "target_declarations")
SOURCE_FIELDS = ("book", "title", "authors", "url")
RESULT_FIELDS = (
    "problem_id", "textbook", "target_theorem", "passed", "input_tokens",
    "cached_read_tokens", "cache_write_tokens", "output_tokens", "cost_usd",
    "turns", "compactions", "added_code_loc", "end_reason",
)
COUNT_FIELDS = (
    "input_tokens", "cached_read_tokens", "cache_write_tokens", "output_tokens",
    "turns", "compactions", "added_code_loc",
)
FILE_HASHES = MappingProxyType({
    "MANIFEST.csv": "8fcde3381403e456b42639ab040a2cc47cb02369bddfedc345fa7d42cd8af674",
    "SOURCES.csv": "854135c5c49acc2506a38a08dfbd5f205f71a5e26f40f0d38b865aedf60e73c8",
    "leaderboard_data/deepseek-v4.1-flash.csv": "3a1dff2ae51ddfa19cd8fec259401eed80fe05e3e2a2d4c0688cf22db9f321af",
    "leaderboard_data/fable-5.csv": "1782cb70e5ace247ef68544ce8b4eaabe3bc0bee5a3f0adcf2330a5e4e43ab86",
    "leaderboard_data/gemini-3.7-flash.csv": "b9cf19baf50d7e412542e9f7461d7056f78fa53e2292bc24d0891ad4fab00d2d",
    "leaderboard_data/gpt-5.6-sol.csv": "8c27c44596ae0bd37dda27ddde1cbd01ba6ba001cdb6841cf3bcca05809abb6e",
    "leaderboard_data/gpt-6-astra.csv": "64a2174e047eac29468a7925768f1671f9c9ab8fd59d4547f78b1d80ff340bd5",
    "leaderboard_data/kimi-k3.csv": "3a24b1722663fd1968a140f3f9433d2677c7e81cb3379497cc9d85f9b701c401",
    "leaderboard_data/opus-4.8.csv": "a8134523cb7a96dbea01156dd190c8589f0d45448d2f9599305442243a8e5bb5",
    "leaderboard_data/opus-5.csv": "bfcfa3893a4040f61ed8924df850b921bb406480f107e9cf438e9b7cd5c9b8cc",
    "leaderboard_data/sonnet-5.csv": "f323d879c43e681b488b391b23231dccaf3614f19f43e933d29234f9ee132cfb",
})
OFFICIAL_MODELS = tuple(path.split("/")[1][:-4] for path in FILE_HASHES if "/" in path)
REASONING_EFFORT = MappingProxyType({
    "gpt-6-astra": "max", "gpt-5.6-sol": "xhigh", "opus-5": "max", "fable-5": "max",
    "deepseek-v4.1-flash": "max", "kimi-k3": "max", "gemini-3.7-flash": "high",
    "sonnet-5": "high", "opus-4.8": "high",
})
_ID = re.compile(r"^[A-Za-z0-9_-]+$")


class ProtocolError(ValueError):
    """Input identities, conditions, or outcomes do not match the protocol."""


def _canonical_hash(value: object) -> str:
    contents = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(contents.encode("utf-8")).hexdigest()


def _rows(data: bytes, fields: Sequence[str]) -> list[dict[str, str]]:
    try:
        reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""), strict=True)
        if tuple(reader.fieldnames or ()) != tuple(fields):
            raise ProtocolError(f"CSV columns must be exactly {tuple(fields)}")
        rows = list(reader)
    except (UnicodeDecodeError, csv.Error) as error:
        raise ProtocolError(f"invalid UTF-8 CSV: {error}") from error
    if not rows or any(None in row or any(row.get(key) is None for key in fields) for row in rows):
        raise ProtocolError("CSV is empty or has malformed row lengths")
    return rows


def _nonnegative_int(value: str, label: str) -> int:
    if not re.fullmatch(r"0|[1-9][0-9]*", value):
        raise ProtocolError(f"{label} must be a non-negative integer")
    return int(value)


def _decimal(value: str, label: str) -> Decimal:
    try:
        number = Decimal(value)
    except InvalidOperation as error:
        raise ProtocolError(f"{label} must be a finite non-negative number") from error
    if not number.is_finite() or number < 0:
        raise ProtocolError(f"{label} must be a finite non-negative number")
    return number


@dataclass(frozen=True)
class Source:
    book: str
    title: str
    authors: str
    url: str


@dataclass(frozen=True)
class Task:
    problem_id: str
    book: str
    target_declarations: tuple[str, ...]
    manifest_row_sha256: str


@dataclass(frozen=True)
class Release:
    tasks: tuple[Task, ...]
    sources: Mapping[str, Source]
    manifest_sha256: str
    sources_sha256: str
    revision: str = REVISION

    @property
    def by_id(self) -> dict[str, Task]:
        return {task.problem_id: task for task in self.tasks}

    @property
    def pinned(self) -> bool:
        return (
            self.revision == REVISION and len(self.tasks) == OFFICIAL_TASK_COUNT
            and self.manifest_sha256 == FILE_HASHES["MANIFEST.csv"]
            and self.sources_sha256 == FILE_HASHES["SOURCES.csv"]
        )


def _parse_release(manifest: bytes, sources: bytes) -> Release:
    source_index = {}
    for row in _rows(sources, SOURCE_FIELDS):
        book = row["book"]
        if not _ID.fullmatch(book) or book in source_index:
            raise ProtocolError(f"invalid or duplicate source book: {book!r}")
        if not row["title"] or not row["authors"] or not row["url"].startswith(("https://", "http://")):
            raise ProtocolError(f"incomplete source metadata: {book}")
        source_index[book] = Source(**row)
    tasks = []
    seen = set()
    for row in _rows(manifest, MANIFEST_FIELDS):
        problem_id = row["problem_id"]
        if not _ID.fullmatch(problem_id) or problem_id in seen:
            raise ProtocolError(f"invalid or duplicate task ID: {problem_id!r}")
        if row["book"] not in source_index:
            raise ProtocolError(f"unknown source book: {row['book']}")
        count = _nonnegative_int(row["target_count"], "target_count")
        targets = tuple(row["target_declarations"].split(";"))
        if not count or count != len(targets) or len(set(targets)) != count or any(
            not target or target != target.strip() for target in targets
        ):
            raise ProtocolError(f"invalid target declarations: {problem_id}")
        tasks.append(Task(problem_id, row["book"], targets, _canonical_hash(row)))
        seen.add(problem_id)
    if {task.book for task in tasks} != set(source_index):
        raise ProtocolError("manifest and source-book coverage differ")
    return Release(
        tuple(tasks), MappingProxyType(source_index),
        hashlib.sha256(manifest).hexdigest(), hashlib.sha256(sources).hexdigest(),
    )


def _verified_bytes(path: Path, relative: str) -> bytes:
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ProtocolError(f"expected a regular file of at most {MAX_FILE_BYTES} bytes: {path}")
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != FILE_HASHES[relative]:
        raise ProtocolError(f"pinned {REVISION} content hash mismatch: {relative}")
    return data


def load_release(directory: Path, *, revision: str = REVISION) -> Release:
    """Load exactly the audited revision; no network or workspace code runs."""
    if revision != REVISION:
        raise ProtocolError(f"unsupported release revision: {revision}")
    release = _parse_release(
        _verified_bytes(directory / "MANIFEST.csv", "MANIFEST.csv"),
        _verified_bytes(directory / "SOURCES.csv", "SOURCES.csv"),
    )
    if not release.pinned:
        raise ProtocolError("official release must contain exactly 341 tasks")
    return release


def fetch_release(directory: Path, *, models: Sequence[str] = ()) -> dict:
    """Explicitly fetch small pinned CSVs only; never textbooks or Lean images."""
    if len(set(models)) != len(models) or any(model not in OFFICIAL_MODELS for model in models):
        raise ProtocolError("models must be distinct pinned official leaderboard names")
    files = ["MANIFEST.csv", "SOURCES.csv", *(f"leaderboard_data/{model}.csv" for model in models)]
    for relative in files:
        path = directory / relative
        if path.exists() or path.is_symlink():
            _verified_bytes(path, relative)
            continue
        with urlopen(f"{RAW_ROOT}/{relative}", timeout=30) as response:
            data = response.read(MAX_FILE_BYTES + 1)
        if len(data) > MAX_FILE_BYTES or hashlib.sha256(data).hexdigest() != FILE_HASHES[relative]:
            raise ProtocolError(f"download size/hash mismatch: {relative}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
    return {"revision": REVISION, "files": {name: FILE_HASHES[name] for name in files},
            "evaluation_only": True, "models_downloaded": False, "textbooks_downloaded": False}


def select_tasks(
    release: Release, *, task_ids: Sequence[str] = (), books: Sequence[str] = (),
    limit: int | None = None,
) -> tuple[Task, ...]:
    """Deterministic manifest order; unknown/duplicate filters never disappear."""
    if len(set(task_ids)) != len(task_ids) or len(set(books)) != len(books):
        raise ProtocolError("duplicate task/book filter")
    unknown = set(task_ids) - release.by_id.keys()
    unknown_books = set(books) - release.sources.keys()
    if unknown or unknown_books:
        raise ProtocolError(f"unknown tasks/books: {sorted(unknown)} / {sorted(unknown_books)}")
    if limit is not None and (isinstance(limit, bool) or not isinstance(limit, int) or limit < 1):
        raise ProtocolError("limit must be a positive integer")
    tasks = tuple(task for task in release.tasks if (
        (not task_ids or task.problem_id in task_ids) and (not books or task.book in books)
    ))
    if not tasks:
        raise ProtocolError("task/book filters have an empty intersection")
    return tasks[:limit] if limit is not None else tasks


def task_view(release: Release, tasks: Sequence[Task]) -> dict:
    """Export public metadata and canonical file URLs, not proofs or source text."""
    if not tasks or len({task.problem_id for task in tasks}) != len(tasks) or any(
        release.by_id.get(task.problem_id) != task for task in tasks
    ):
        raise ProtocolError("selection must contain distinct canonical tasks")
    payload = {
        "schema_version": 1, "benchmark": "Meta AutoformBench", "revision": release.revision,
        "manifest_sha256": release.manifest_sha256, "sources_sha256": release.sources_sha256,
        "source_condition": "source-free", "evaluation_only": True,
        "training_use_allowed": False, "contains_gold_proofs": False,
        "lean_version": LEAN_VERSION, "mathlib_revision": MATHLIB_REVISION,
        "inventory_only": True, "execution_performed": False,
        "tasks": [{
            **asdict(task), "target_declarations": list(task.target_declarations),
            "source_citation": asdict(release.sources[task.book]),
            "canonical_workspace_url": f"{REPOSITORY}/tree/{release.revision}/workspaces/{task.problem_id}",
        } for task in tasks],
    }
    payload["selection_sha256"] = _canonical_hash(payload)
    return payload


def harbor_plan(
    release: Release, tasks: Sequence[Task], *, repository_dir: Path,
    agent: str = "nop", model: str | None = None,
) -> dict:
    """Produce real upstream CLI argument vectors; deliberately do not execute."""
    if not release.pinned:
        raise ProtocolError("Harbor plans require the pinned official manifest")
    view = task_view(release, tasks)
    if not agent or agent.startswith("-") or any(character.isspace() for character in agent):
        raise ProtocolError("agent must be one non-option name")
    if agent != "nop" and (not model or model.startswith("-")):
        raise ProtocolError("a real agent requires an explicit provider/model")
    if agent == "nop" and model:
        raise ProtocolError("nop baseline does not take a model")
    commands = []
    for task in tasks:
        problem_id = task.problem_id
        run = ["uvx", "--offline", "--from", f"harbor=={HARBOR_VERSION}", "harbor", "run",
               "-p", f"harbor/tasks/{problem_id}", "--agent", agent,
               "--n-attempts", "1", "--n-concurrent", "1"]
        if model:
            run.extend(["--model", model])
        commands.append({"problem_id": problem_id, "steps": [
            ["python3", "harbor/export.py", "--problem", problem_id],
            ["python3", "harbor/export.py", "--check", "--problem", problem_id], run,
        ]})
    return {
        "schema_version": 1, "kind": "execution_plan_only", "execution_performed": False,
        "revision": REVISION, "selection_sha256": view["selection_sha256"],
        "source_condition": "source-free", "training_use_allowed": False,
        "working_directory": str(repository_dir),
        "preflight_revision_command": ["git", "rev-parse", "HEAD"],
        "preflight_expected_revision": REVISION,
        "environment": {"HARBOR_TELEMETRY": "0", "UV_OFFLINE": "1"},
        "harbor_version": HARBOR_VERSION, "task_schema_version": TASK_SCHEMA_VERSION,
        "agent": agent, "model": model, "attempts": 1, "concurrency": 1,
        "agent_timeout_sec_from_upstream": 86400, "verifier_timeout_sec_from_upstream": 6000,
        "cpus": 4, "memory_mb": 16384, "storage_mb": 51200, "gpus": 0,
        "network_mode": "no-network", "commands": commands,
        "prerequisites": [
            "A clean complete checkout at the exact revision, not only the downloaded CSVs",
            "Harbor 0.22.0 and both official Lean/Mathlib verifier images already installed",
            "Publishable evaluations must pin image digests; local image tags are not immutable",
            "Apply a separate explicit cost gate before running a real agent; no USD cap is enforced by this plan",
        ],
        "claim_boundary": "nop must yield zero on pristine sorry; a plan is not a verifier run or model score",
    }


def _parse_leaderboard(release: Release, data: bytes) -> tuple[dict, ...]:
    """Validate task-level CSV structure; called before any aggregation."""
    tasks = release.by_id
    seen = set()
    parsed = []
    for row in _rows(data, RESULT_FIELDS):
        problem_id = row["problem_id"]
        if problem_id not in tasks or problem_id in seen:
            raise ProtocolError(f"unknown or duplicate result task: {problem_id}")
        task = tasks[problem_id]
        if row["textbook"] != task.book or row["target_theorem"] not in task.target_declarations:
            raise ProtocolError(f"book/target does not match canonical task: {problem_id}")
        if row["passed"] not in {"true", "false"}:
            raise ProtocolError(f"passed must be true/false: {problem_id}")
        passed = row["passed"] == "true"
        if row["end_reason"] not in {"success", "model_gave_up", "budget_consumed"} or (
            passed != (row["end_reason"] == "success")
        ):
            raise ProtocolError(f"success and stopping reason disagree: {problem_id}")
        counts = {key: _nonnegative_int(row[key], key) for key in COUNT_FIELDS}
        cost = _decimal(row["cost_usd"], "cost_usd")
        parsed.append({"problem_id": problem_id, "book": task.book,
                       "target_theorem": row["target_theorem"], "passed": passed,
                       **counts, "cost_usd": str(cost), "end_reason": row["end_reason"]})
        seen.add(problem_id)
    missing = tasks.keys() - seen
    if missing:
        raise ProtocolError(f"missing result tasks: {sorted(missing)}")
    return tuple(parsed)


def import_official_results(
    release: Release, csv_path: Path, *, model: str,
    source_condition: str, budget_usd: Decimal = OFFICIAL_BUDGET_USD,
) -> dict:
    """Import existing source-present outcomes; never create local capability scores."""
    if not release.pinned or model not in OFFICIAL_MODELS:
        raise ProtocolError("official result import requires a pinned release and known model")
    budget_usd = _decimal(str(budget_usd), "nominal budget")
    if source_condition != "source-present" or budget_usd != OFFICIAL_BUDGET_USD:
        raise ProtocolError("official CSV condition is source-present with nominal USD 200/task")
    relative = f"leaderboard_data/{model}.csv"
    rows = _parse_leaderboard(release, _verified_bytes(csv_path, relative))
    solved = sum(row["passed"] for row in rows)
    costs = [Decimal(row["cost_usd"]) for row in rows]
    over_budget = [row["problem_id"] for row in rows if Decimal(row["cost_usd"]) > budget_usd]
    by_book = {}
    for book in release.sources:
        cohort = [row for row in rows if row["book"] == book]
        by_book[book] = {"tasks": len(cohort), "solved": sum(row["passed"] for row in cohort)}
    return {
        "schema_version": 1, "kind": "imported_official_reference_results",
        "benchmark": "Meta AutoformBench", "model": model, "revision": REVISION,
        "source_csv_url": f"{RAW_ROOT}/{relative}", "source_csv_sha256": FILE_HASHES[relative],
        "manifest_sha256": release.manifest_sha256, "sources_sha256": release.sources_sha256,
        "source_condition": "source-present", "nominal_budget_usd_per_task": str(budget_usd),
        "scaffold": "paper common multi-turn formalization harness",
        "reasoning_effort": REASONING_EFFORT[model],
        "reasoning_effort_is_cross_provider_matched_compute": False,
        "explicit_token_or_turn_limit_in_csv": None,
        "tool_access": ["filesystem", "Lean execution", "Loogle/Mathlib search"],
        "stopping_policy": "submit_report or budget; paper persistence intervention applies",
        "exact_trajectories_available": False, "evaluation_only": True,
        "diagnostic_only": True, "promotion_eligible": False,
        "local_execution_performed": False, "local_capability_score": None,
        "metrics": {"tasks": len(rows), "solved": solved, "solve_rate": solved / len(rows),
                    "observed_cost_usd_total": str(sum(costs)), "observed_cost_usd_max": str(max(costs)),
                    "input_tokens_total": sum(row["input_tokens"] for row in rows),
                    "output_tokens_total": sum(row["output_tokens"] for row in rows),
                    "turns_total": sum(row["turns"] for row in rows)},
        "by_book": by_book, "end_reasons": dict(Counter(row["end_reason"] for row in rows)),
        "budget_audit": {"observed_rows_above_nominal_cap": len(over_budget),
                         "task_ids": over_budget, "strict_cap_compliant": not over_budget,
                         "overrun_reason": "not inferable from the public CSV" if over_budget else None},
        "claim_boundary": "existing source-present reports; not a local source-free Lean evaluation",
    }


def validate_comparison(
    reports: Sequence[dict], *, source_condition: str, budget_usd: Decimal,
    strict_budget: bool = True,
) -> None:
    """Reject mixed task universes, source access, nominal budgets or overrun claims."""
    if not reports:
        raise ProtocolError("comparison has no reports")
    budget_usd = _decimal(str(budget_usd), "comparison budget")
    if budget_usd <= 0:
        raise ProtocolError("comparison budget must be finite and positive")
    models = [report.get("model") for report in reports]
    if any(not model for model in models) or len(models) != len(set(models)):
        raise ProtocolError("comparison model identities are missing or duplicated")
    required = ("revision", "manifest_sha256", "sources_sha256", "scaffold", "tool_access", "stopping_policy")
    for report in reports:
        nominal_budget = _decimal(str(report.get("nominal_budget_usd_per_task")), "nominal budget")
        if report.get("source_condition") != source_condition or nominal_budget != budget_usd:
            raise ProtocolError("source condition or nominal budget mismatch")
        if any(report.get(field) != reports[0].get(field) for field in required) or (
            report.get("metrics", {}).get("tasks") != OFFICIAL_TASK_COUNT
        ):
            raise ProtocolError("task universe, scaffold, tools or stopping policy mismatch")
        if strict_budget and not report.get("budget_audit", {}).get("strict_cap_compliant", False):
            raise ProtocolError("observed costs exceed the requested strict budget; preserve the anomaly")


def read_verifier_verdict(path: Path, *, expected_problem_id: str) -> dict:
    """Read an actual upstream verifier verdict, without replacing the verifier.

    An infrastructure error has no numerical reward.  Parsing a file alone is
    not proof of the verifier/image provenance, and cannot create a benchmark
    score.  A future execution bridge must separately attest those artifacts.
    """
    if not _ID.fullmatch(expected_problem_id):
        raise ProtocolError("invalid expected problem ID")
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise ProtocolError("verdict must be a regular JSON file of at most 1 MiB")
    data = path.read_bytes()
    verdict = json.loads(data)
    if not isinstance(verdict, dict) or not {
        "problem_id", "status", "accepted", "reason", "comparator_exit_code"
    } <= verdict.keys():
        raise ProtocolError("verifier verdict must contain the upstream verdict fields")
    if verdict.get("problem_id") != expected_problem_id:
        raise ProtocolError("verifier task ID mismatch")
    status = verdict.get("status")
    expected_accepted = {"accepted": True, "rejected": False, "error": None}
    if status not in expected_accepted or verdict.get("accepted") is not expected_accepted[status]:
        raise ProtocolError("verifier status/accepted mismatch")
    if not isinstance(verdict.get("reason"), str) or not verdict["reason"]:
        raise ProtocolError("verifier reason is missing")
    exit_code = verdict.get("comparator_exit_code")
    if exit_code is not None and (isinstance(exit_code, bool) or not isinstance(exit_code, int)):
        raise ProtocolError("invalid comparator exit code")
    if status == "accepted" and exit_code != 0:
        raise ProtocolError("accepted proof requires comparator exit code zero")
    return {"problem_id": expected_problem_id, "status": status,
            "reward": None if status == "error" else int(status == "accepted"),
            "reason": verdict["reason"], "verdict_sha256": hashlib.sha256(data).hexdigest(),
            "verifier_provenance_attested": False, "local_capability_score": None}
