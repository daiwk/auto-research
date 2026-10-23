"""PLE fixed-release offline scoring/provenance protocol, not a task runner.

Independent implementation of paper 2610.30537v1 Eq.1/2 and documented
canonical artifact rules at google-research/ple 70ed96281d87380926a0d7c08e21799fd5edee63
(Apache-2.0). No commands, containers, graders, models, filesystem or network.
"""
from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import math
import random
import re
import statistics


UPSTREAM_REVISION = "70ed96281d87380926a0d7c08e21799fd5edee63"
DATASET_REVISION = "535cf0a8af68126e3f00a1441cf736754a0cda4b"
DEV_MANIFEST_SOURCE_SHA256 = "c36cab6f0f3a1ab613e5b507e13dad80f56d3eec370019969965f5a32edaed1e"
_ROOT_ALIAS = re.compile(r"(dev[-_]?)?artifacts?", re.IGNORECASE)


def _number(value, *, minimum: float = 0.0, maximum: float = 1.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("finite numeric value required; booleans are not scores")
    number = float(value)
    if not math.isfinite(number) or not minimum <= number <= maximum:
        raise ValueError("numeric value outside its finite allowed range")
    return number


def design_item_score(passed: Sequence[bool], hard: Sequence[bool], objective: float,
                      naive_objective: float = 0.0) -> float:
    """Paper Eq.1/2 only, not the special site/MEP graders or a physics judge."""
    if (not passed or len(passed) != len(hard)
            or any(type(x) is not bool for x in tuple(passed)+tuple(hard))):
        raise ValueError("nonempty aligned boolean verdict/hard-constraint vectors required")
    objective = _number(objective)
    baseline = _number(naive_objective)
    if baseline == 1:
        raise ValueError("naive objective must be below one for normalization")
    p = sum(passed)/len(passed)
    gate = all(ok for ok, is_hard in zip(passed, hard) if is_hard)
    normalized = min(1.0, max(0.0, (objective-baseline)/(1-baseline)))
    return 0.4*p + 0.6*int(gate)*normalized


def rubric_score(passed: Sequence[bool], weights: Sequence[float]) -> float:
    """Given evaluator verdicts, compute the paper's weighted binary rubric."""
    if not passed or len(passed) != len(weights) or any(type(x) is not bool for x in passed):
        raise ValueError("aligned nonempty boolean rubric verdicts and weights required")
    positive = [_number(w, maximum=math.inf) for w in weights]
    if any(w <= 0 for w in positive):
        raise ValueError("rubric weights must be positive")
    # Scale before summing: finite individual weights can overflow in aggregate.
    largest = max(positive)
    scaled = [weight/largest for weight in positive]
    return math.fsum(w for ok, w in zip(passed, scaled) if ok)/math.fsum(scaled)


def dev_set_digest(data: Mapping) -> str:
    """Hash parsed config, not raw YAML; matches fixed upstream canonical JSON."""
    if not isinstance(data, Mapping):
        raise ValueError("parsed dev-set mapping required")
    try:
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"),
                               ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("dev-set data must be finite JSON-compatible values") from error
    return hashlib.sha256(canonical.encode()).hexdigest()


def _path_problem(path: str) -> str | None:
    if not isinstance(path, str) or not path:
        return "empty/non-string path"
    try:
        encoded = path.encode("utf-8")
    except UnicodeEncodeError:
        return "non-UTF-8 path"
    if "\ufffd" in path:
        return "non-UTF-8 path"
    if path.count("/") > 64 or len(encoded) > 1024 or any(len(x.encode()) > 255 for x in path.split("/")):
        return "path size/depth limit"
    if any(x in ("", ".", "..") for x in path.split("/")):
        return "empty/dot/traversal segment"
    if "\\" in path or any(ord(x) < 32 or ord(x) == 127 for x in path):
        return "backslash/control character"
    return None


@dataclass(frozen=True)
class DevTask:
    task_id: str
    deliverables: tuple[str, ...]
    final_message: bool
    grading: str

    def covers(self, relative_path: str) -> bool:
        absolute = "/"+relative_path
        return any(absolute == d or (d.endswith("/") and absolute.startswith(d))
                   for d in self.deliverables)


def dev_tasks(data: Mapping) -> tuple[DevTask, ...]:
    """Project task metadata only; never load task instructions, rubrics or gold."""
    dev_set_digest(data)
    result, seen = [], set()
    rows = data.get("tasks")
    if not isinstance(rows, list) or any(not isinstance(row, Mapping) for row in rows):
        raise ValueError("task rows must be a list of mappings")
    for row in rows:
        task_id = row.get("id")
        if (not isinstance(task_id, str) or _path_problem(task_id) or "/" in task_id
                or task_id in seen):
            raise ValueError("unique single-segment task IDs required")
        deliverables = row.get("deliverables")
        if (not isinstance(deliverables, list) or not deliverables
                or any(not isinstance(d, str) or not d.startswith("/")
                       or _path_problem(d[1:].rstrip("/")) for d in deliverables)):
            raise ValueError("canonical absolute deliverable paths required")
        grading = row.get("grading", "checks")
        final = row.get("final_message", grading == "rubric")
        if grading not in {"checks", "rubric", "checks-judge"} or type(final) is not bool:
            raise ValueError("known grading kind and boolean final_message required")
        result.append(DevTask(task_id, tuple(deliverables), final, grading))
        seen.add(task_id)
    if not result:
        raise ValueError("nonempty task manifest required")
    return tuple(result)


@dataclass(frozen=True)
class FileEntry:
    path: str
    data: bytes
    mode: str = "100644"

    def __post_init__(self):
        if not isinstance(self.data, bytes) or not isinstance(self.path, str) or not isinstance(self.mode, str):
            raise ValueError("entries require actual bytes, not paths or file callbacks")


def git_blob_id(data: bytes) -> str:
    if not isinstance(data, bytes):
        raise ValueError("Git blob input must be bytes")
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()


def harness_digest(entries: Sequence[FileEntry]) -> str:
    """Fixed upstream mode/blob/path SHA256, excluding artifact aliases and .env."""
    selected, seen = [], set()
    for entry in entries:
        if _path_problem(entry.path) or entry.path in seen:
            raise ValueError("canonical unique harness paths required")
        seen.add(entry.path)
        parts = entry.path.split("/")
        excluded = (_ROOT_ALIAS.fullmatch(parts[0]) or entry.path == ".env"
                    or parts[0] == ".git" or (len(parts) >= 3 and parts[0] == "runs" and parts[2] == "artifacts"))
        if excluded:
            continue
        if entry.mode not in {"100644", "100755", "100664"}:
            raise ValueError("only regular-file harness entries supported locally")
        selected.append((entry.path.encode(), entry.mode, git_blob_id(entry.data)))
    digest = hashlib.sha256()
    for path, mode, blob in sorted(selected):
        digest.update(mode.encode()+b" "+blob.encode()+b" "+path+b"\n")
    return digest.hexdigest()


def audit_artifacts(tasks: Sequence[DevTask], entries: Sequence[FileEntry], *,
                    manifest: Mapping | None, expected_dev_digest: str,
                    expected_harness_digest: str) -> dict:
    """Canonical-layout subset of release review rules, using immutable bytes.

    Missing/stale manifest is a provenance warning, not a server refusal.
    No fallback folder aliases, git-index/LFS-attribute inspection, deleted-file
    replay or grading is implemented. Caller scores only externally graded data.
    """
    ids = [task.task_id for task in tasks]
    if not tasks or len(set(ids)) != len(ids):
        raise ValueError("unique nonempty tasks required")
    groups = {task_id: [] for task_id in ids}
    total_bytes, total_files = 0, 0
    refusals, warnings = [], []
    for entry in entries:
        if not entry.path.startswith("artifacts/"):
            warnings.append("outside canonical artifacts layout: ignored")
            continue
        total_bytes += len(entry.data)
        total_files += 1
        parts = entry.path.split("/")
        if len(parts) >= 2 and parts[1] in groups:
            groups[parts[1]].append(entry)
    if total_bytes > 512 << 20 or total_files > 10000:
        refusals.append("whole artifact folder size/file limit")
    task_results = {}
    for task in tasks:
        reasons, notes, files, names = [], [], {}, set()
        message = None
        auxiliary_bytes = 0
        group = groups[task.task_id]
        prefix = f"artifacts/{task.task_id}/"
        for entry in group:
            relative = entry.path[len(prefix):] if entry.path.startswith(prefix) else ""
            parts = relative.split("/")
            if any(p in {".git", ".gitignore", ".gitattributes", ".gitmodules", ".DS_Store",
                         "Thumbs.db", "desktop.ini", "__MACOSX"} or p.startswith("._") for p in parts):
                notes.append("git/OS metadata: ignored")
                continue
            problem = _path_problem(relative)
            if problem:
                reasons.append(problem)
                continue
            if entry.mode not in {"100644", "100755", "100664"}:
                reasons.append("symlink/submodule/non-regular artifact")
                continue
            if relative.startswith("files/"):
                container = relative[6:]
                problem = _path_problem(container)
                if problem:
                    reasons.append(problem)
                    continue
                if container.casefold() in names:
                    reasons.append("duplicate/case-colliding deliverable")
                names.add(container.casefold())
                if len(entry.data) > 95 << 20:
                    reasons.append("deliverable file size limit")
                if entry.data.startswith(b"version https://git-lfs.github.com/spec/"):
                    reasons.append("Git LFS pointer, not deliverable bytes")
                if task.covers(container):
                    files[container] = git_blob_id(entry.data)
                else:
                    notes.append("outside declared deliverables: ignored")
            elif relative == "final_message.md":
                if message is not None:
                    reasons.append("duplicate final message")
                message = entry.data
                if len(message) > 1 << 20:
                    notes.append("final message exceeds1MiB; official grading truncates it")
            elif relative in {"trajectory.json", "deleted.txt"}:
                if relative == "trajectory.json" and len(entry.data) > 32 << 20:
                    notes.append("oversize trajectory: ignored")
                else:
                    auxiliary_bytes += len(entry.data)
            elif relative not in {"trajectory.json", "deleted.txt", ".gitignore", ".gitattributes", ".gitmodules"}:
                notes.append("unrecognized task artifact: ignored")
        folders = {"/".join(path.split("/")[:i]) for path in files for i in range(1, len(path.split("/")))}
        spellings = {}
        for path in set(files) | folders:
            spellings.setdefault(path.casefold(), set()).add(path)
        if any(len(paths) > 1 for paths in spellings.values()):
            reasons.append("case-colliding file/folder path")
        if set(files) & folders:
            reasons.append("path is both file and folder")
        file_sizes = {entry.path[len(prefix)+6:]: len(entry.data)
                      for entry in group if entry.path.startswith(prefix+"files/")}
        task_bytes = sum(file_sizes[path] for path in files)+len(message or b"")+auxiliary_bytes
        if len(files) > 2000 or task_bytes > 256 << 20:
            reasons.append("task folder size/file limit")
        if task.final_message and not message:
            notes.append("grader reads final_message.md but message is missing/empty")
        usable = bool(files or (task.final_message and message)) and not reasons
        if not usable and not reasons:
            reasons.append("no usable declared deliverable/final message")
        task_results[task.task_id] = {"usable": bool(usable), "reasons": reasons, "warnings": notes,
                                      "files": files, "final_message_blob": git_blob_id(message) if message else None}
    if not any(row["usable"] for row in task_results.values()):
        refusals.append("no dev task has usable artifacts")
    provenance = {"manifest": "missing", "dev_set": "unknown", "harness": "unknown", "edited_tasks": []}
    if (not isinstance(manifest, Mapping) or not isinstance(manifest.get("tasks"), Mapping)):
        warnings.append("missing/invalid manifest: provenance cannot be established")
    else:
        provenance["manifest"] = "ok"
        if manifest.get("format") != 1:
            warnings.append("manifest format differs from fixed release")
        provenance["dev_set"] = "same" if manifest.get("dev_set") == expected_dev_digest else "other"
        recorded = manifest.get("harness", {})
        recorded = recorded.get("tree") if isinstance(recorded, Mapping) else None
        provenance["harness"] = "unknown" if not recorded else ("same" if recorded == expected_harness_digest else "changed")
        for task_id, result in task_results.items():
            if not result["usable"]:
                continue
            record = manifest["tasks"].get(task_id)
            if not isinstance(record, Mapping):
                warnings.append(f"{task_id}: absent from manifest")
                continue
            # Local claimed reward is deliberately not consumed as a grade.
            expected_files = record.get("files", {})
            if (expected_files != result["files"]
                    or (record.get("final_message") and record["final_message"] != result["final_message_blob"])):
                provenance["edited_tasks"].append(task_id)
            if record.get("dev_set", expected_dev_digest) != expected_dev_digest:
                provenance["dev_set"] = "other"
            if record.get("tree", recorded) != recorded:
                provenance["harness"] = "changed"
        if provenance["dev_set"] == "other":
            warnings.append("manifest dev-set fingerprint differs")
        if provenance["harness"] != "same":
            warnings.append("manifest cannot tie artifacts to this harness snapshot")
        if provenance["edited_tasks"]:
            warnings.append("artifact blobs differ from their export manifest")
    return {"refused": bool(refusals), "refusals": refusals, "warnings": warnings,
            "tasks": task_results, "provenance": provenance, "grades_computed": False,
            "layout": "canonical-only", "upstream_revision": UPSTREAM_REVISION}


def aggregate_three_runs(task_ids: Sequence[str], runs: Sequence[Mapping[str, float]]) -> dict:
    """Mean over full task set and exactly three runs; absent results score zero."""
    if (not task_ids or any(not isinstance(x, str) or not x for x in task_ids)
            or len(set(task_ids)) != len(task_ids) or len(runs) != 3):
        raise ValueError("unique task IDs and exactly three complete run records required")
    ids = set(task_ids)
    means, missing = [], []
    for run in runs:
        if not isinstance(run, Mapping) or not set(run) <= ids:
            raise ValueError("each run must map only declared task IDs to external scores")
        scores = [_number(run[task_id]) if task_id in run else 0.0 for task_id in task_ids]
        means.append(sum(scores)/len(task_ids))
        missing.append([task_id for task_id in task_ids if task_id not in run])
    return {"run_means": means, "mean": statistics.mean(means),
            "population_std": statistics.pstdev(means), "sample_std": statistics.stdev(means),
            "missing_tasks_per_run": missing, "task_count": len(task_ids), "run_count": 3,
            "std_note": "both conventions reported; public rules do not specify ddof",
            "scores_source": "external evaluator, never manifest claimed reward"}


def reproduction_check(committed: Sequence[float], live: Sequence[float]) -> dict:
    if not committed or len(committed) != len(live):
        raise ValueError("aligned nonempty reproduction-sample scores required")
    gap = statistics.mean([_number(x) for x in committed])-statistics.mean([_number(x) for x in live])
    return {"mean_gap": gap, "flag_for_human_review": bool(gap > 0.25),
            "automatic_disqualification": False}


def diagnostic(seed: int = 42) -> dict:
    """Synthetic contracts only; no engineering designs or agent capability score."""
    data = {"tasks": [{"id": "design", "deliverables": ["/output/"], "final_message": False},
                       {"id": "memo", "deliverables": ["/output/"], "final_message": True}]}
    tasks = dev_tasks(data)
    payload = random.Random(seed).randbytes(16)
    entry = FileEntry("artifacts/design/files/output/design.csv", payload)
    harness = harness_digest([FileEntry("serve.py", b"not executed")])
    manifest = {"format": 1, "dev_set": dev_set_digest(data), "harness": {"tree": harness},
                "tasks": {"design": {"files": {"output/design.csv": git_blob_id(payload)}, "reward": 1.0}}}
    audit = audit_artifacts(tasks, [entry], manifest=manifest,
                            expected_dev_digest=dev_set_digest(data), expected_harness_digest=harness)
    aggregate = aggregate_three_runs(["design", "memo"], [{"design": 1.0}, {"memo": 1.0}, {}])
    hard_cap = design_item_score([True, False], [False, True], 1.0)
    checks = {"declared_deliverable_usable": audit["tasks"]["design"]["usable"],
              "missing_task_not_usable": not audit["tasks"]["memo"]["usable"],
              "manifest_reward_not_a_grade": not audit["grades_computed"],
              "hard_constraint_gate_caps_score": abs(hard_cap-0.2) < 1e-12,
              "full_task_denominator_and_three_runs": abs(aggregate["mean"]-1/3) < 1e-12,
              "blob_provenance_consistent": not audit["provenance"]["edited_tasks"],
              "strict_reproduction_threshold": not reproduction_check([0.5], [0.25])["flag_for_human_review"]}
    return {"seed": seed, "checks": {key: bool(value) for key, value in checks.items()},
            "metrics": {"contract_cases": float(len(checks)), "model_calls": 0.0,
                        "container_runs": 0.0, "external_commands": 0.0},
            "evaluation_tier": "l1_mechanism", "diagnostic_only": True,
            "promotion_eligible": False, "evolve_integrated": False,
            "requires_gpu_validation": False, "full_experiment_status": "not_reproduced_high_cost",
            "upstream_revision": UPSTREAM_REVISION}
