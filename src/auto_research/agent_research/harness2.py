"""Harness²'s bounded, answer-free recursion controller (CPU mechanism, not an LLM).

The executor/editor/selector/reflection callbacks are trusted integration points.
This module neither starts a model service nor executes candidate file contents.
The source implementation at google-research/harness2 is pinned in UPSTREAM_COMMIT.
Callbacks receive explicit immutable public inputs; this is not a security sandbox
for malicious callbacks or a guarantee about a callback's external/network access.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path, PurePosixPath
import random
import re
from typing import Callable, Sequence, TypeVar

UPSTREAM_COMMIT = "1cfe254e8d25b15f37048c3730134686abe60335"
PROTOCOL = "harness2-answer-free-controller-v1"
_FORBIDDEN = re.compile(
    r"(?:gold[_ -]?(?:answer|plan)|answer[_ -]?key|reference[_ -]?answer|"
    r"rubrics?(?:\.json)?|grader[_ -]?(?:score|verdict)|grading[_ -]?criteria)", re.I)
_ROOTS = {"systemprompt.md", "guardrails.md", "memory.md", "tools.md"}
_T = TypeVar("_T")


def fingerprint(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def _text(value: str, field: str, *, empty: bool = False) -> None:
    if type(value) is not str or (not empty and not value.strip()):
        raise ValueError(f"nonempty string required for {field}")
    if _FORBIDDEN.search(value):
        raise ValueError(f"privileged evaluation material rejected in {field}")


def _pairs(values: tuple[tuple[str, str], ...], *, surface: bool) -> None:
    if type(values) is not tuple or any(type(v) is not tuple or len(v) != 2 for v in values):
        raise ValueError("immutable (path, text) pairs required")
    paths = []
    for path, text in values:
        _text(path, "path")
        _text(text, path, empty=True)
        p = PurePosixPath(path)
        if p.is_absolute() or ".." in p.parts or "\\" in path or p.as_posix() != path:
            raise ValueError("relative canonical paths required")
        if surface and path not in _ROOTS and not re.fullmatch(
                r"(?:scripts/[a-z0-9_-]+\.py|skills/[a-z0-9_-]+/SKILL\.md|"
                r"sub_agents/[a-z0-9_-]+\.md|plugin/[a-z0-9_-]+\.ts)", path):
            raise ValueError("file is outside the eight-component editable surface")
        paths.append(path)
    if len(set(paths)) != len(paths):
        raise ValueError("duplicate file path")


@dataclass(frozen=True)
class Harness:
    files: tuple[tuple[str, str], ...]

    def __post_init__(self):
        _pairs(self.files, surface=True)
        tree = dict(self.files)
        if not tree.get("systemprompt.md", "").strip():
            raise ValueError("a nonempty system prompt is required")
        always = tree["systemprompt.md"] + tree.get("guardrails.md", "")
        if "{{" in always or "{%" in always:
            raise ValueError("unresolved runtime template in always-on text")
        for name in tree:
            if name.startswith("skills/"):
                skill = name.split("/")[1]
                if skill not in always:
                    raise ValueError("skill needs an always-on trigger")
                if not re.search(r"(?m)^description:\s*\S", tree[name]):
                    raise ValueError("skill needs description frontmatter")
        for text in tree.values():
            for script in re.findall(r"scripts/[a-z0-9_-]+\.py", text):
                if script not in tree:
                    raise ValueError("referenced helper must travel with the harness")

    def mapping(self) -> dict[str, str]:
        return dict(self.files)

    @property
    def sha256(self) -> str:
        return fingerprint(dict(self.files))


@dataclass(frozen=True)
class PublicTask:
    task_id: str
    domain: str
    prompt: str
    sources: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        for key in ("task_id", "domain", "prompt"):
            _text(getattr(self, key), key)
        _pairs(self.sources, surface=False)


@dataclass(frozen=True)
class ExecutionConfig:
    model_revision: str
    environment_revision: str
    seed: int
    improvement_revision: str
    initial_harness_sha256: str

    def __post_init__(self):
        _text(self.model_revision, "model revision")
        _text(self.environment_revision, "environment revision")
        _text(self.improvement_revision, "editor/selector/reflection revision")
        if type(self.seed) is not int:
            raise ValueError("integer seed required")
        if (type(self.initial_harness_sha256) is not str or
                re.fullmatch(r"[a-f0-9]{64}", self.initial_harness_sha256) is None):
            raise ValueError("initial harness SHA256 required")


@dataclass(frozen=True)
class Execution:
    trajectory: str
    deliverable: str
    ok: bool = True
    error: str = ""

    def __post_init__(self):
        for name in ("trajectory", "deliverable", "error"):
            _text(getattr(self, name), name, empty=True)
        if type(self.ok) is not bool:
            raise ValueError("boolean execution status required")


@dataclass(frozen=True)
class Evidence:
    label: str
    harness: Harness
    execution: Execution


@dataclass(frozen=True)
class Lesson:
    cue: str
    lesson: str
    evidence_pairs: tuple[tuple[str, str], ...]
    confidence: str = "observed behavior only; transfer not established"

    def __post_init__(self):
        for name in ("cue", "lesson", "confidence"):
            _text(getattr(self, name), name)
        if (type(self.evidence_pairs) is not tuple or not self.evidence_pairs or
                any(type(p) is not tuple or len(p) != 2 or
                    any(type(v) is not str or not v for v in p) for p in self.evidence_pairs)):
            raise ValueError("lesson needs explicit execution contrast pairs")


@dataclass(frozen=True)
class LibraryEntry:
    task_id: str
    domain: str
    task_index: int
    adopted: Harness
    lesson: Lesson
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class EditContext:
    task: PublicTask
    current: Harness
    references: tuple[Evidence, ...]
    pool: tuple[Evidence, ...]
    library: tuple[LibraryEntry, ...]
    stage: str
    index: int
    decisions: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Edit:
    harness: Harness
    notes: str
    supports: tuple[str, ...]


@dataclass(frozen=True)
class StageRecord:
    label: str
    context: EditContext
    edit: Edit
    attempts: int
    fell_back: bool = False
    errors: tuple[str, ...] = ()


@dataclass(frozen=True)
class SelectionContext:
    """Only public request/source + anonymous final deliverables, never harnesses."""
    task: PublicTask
    candidates: tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class ReflectionContext:
    task: PublicTask
    base: Harness
    adopted: Evidence
    evidence: tuple[Evidence, ...]
    stages: tuple[StageRecord, ...]
    library: tuple[LibraryEntry, ...]


@dataclass(frozen=True)
class RunResult:
    task: PublicTask
    config: ExecutionConfig
    mode: str
    k: int
    evidence: tuple[Evidence, ...]
    stages: tuple[StageRecord, ...]
    finals: tuple[str, ...]
    adopted: str | None
    selection_error: str
    lesson_retained: bool
    reflection_error: str
    library_entries_seen: int
    diagnostic_only: bool = True
    promotion_eligible: bool = False
    evolve_integrated: bool = False

    def summary(self) -> dict:
        return {"task_id": self.task.task_id, "domain": self.task.domain,
            "mode": self.mode, "k": self.k, "rollouts": len(self.evidence),
            "improvement_stages": len(self.stages),
            "editor_attempts": sum(s.attempts for s in self.stages),
            "stage_fallbacks": sum(s.fell_back for s in self.stages),
            "failed_rollouts": sum(not e.execution.ok for e in self.evidence),
            "finals": list(self.finals), "adopted": self.adopted,
            "selection_error": self.selection_error, "lesson_retained": self.lesson_retained,
            "reflection_error": self.reflection_error,
            "library_entries_seen": self.library_entries_seen,
            "diagnostic_only": True, "promotion_eligible": False, "evolve_integrated": False}


def _validate_lesson(lesson: Lesson, evidence: Sequence[Evidence]) -> None:
    if not isinstance(lesson, Lesson):
        raise ValueError("reflection must return a Lesson or None")
    pool = {e.label: e for e in evidence}
    for left, right in lesson.evidence_pairs:
        if left == right or left not in pool or right not in pool:
            raise ValueError("unknown or identical evidence contrast")
        a, b = pool[left], pool[right]
        if not a.execution.ok or not b.execution.ok or a.harness.sha256 == b.harness.sha256:
            raise ValueError("lesson requires two successful, different harness executions")
        if (a.execution.trajectory, a.execution.deliverable) == (b.execution.trajectory, b.execution.deliverable):
            raise ValueError("no observed execution contrast; adoption is not lesson evidence")


class EvidenceLibrary:
    """One explicit run namespace; same-domain earlier tasks only, tamper checked.

    The full adopted tree and cited execution contrasts persist. Writes refuse a
    changed snapshot, so simultaneous same-namespace writers fail rather than
    silently lose an update. Run different domains/namespaces separately.
    """

    def __init__(self, path: Path, namespace: str):
        self.path = Path(path)
        _text(namespace, "library namespace")
        self.namespace = namespace

    def _read(self) -> dict:
        if not self.path.exists():
            return {"protocol": PROTOCOL, "namespace": self.namespace, "entries": []}
        obj = json.loads(self.path.read_text(encoding="utf-8"))
        if (obj.get("protocol") != PROTOCOL or obj.get("namespace") != self.namespace or
                type(obj.get("entries")) is not list):
            raise ValueError("incompatible library namespace or protocol")
        for item in obj["entries"]:
            if set(item) != {"entry", "sha256"} or fingerprint(item["entry"]) != item["sha256"]:
                raise ValueError("library entry integrity failure")
            _decode_entry(item["entry"])
        return obj

    def before(self, task: PublicTask, task_index: int) -> tuple[tuple[LibraryEntry, ...], str]:
        if type(task_index) is not int or task_index < 0:
            raise ValueError("nonnegative stream index required")
        obj = self._read()
        entries = tuple(_decode_entry(i["entry"]) for i in obj["entries"])
        relevant = tuple(e for e in entries if e.domain == task.domain)
        if any(e.task_id == task.task_id or e.task_index >= task_index for e in relevant):
            raise ValueError("current/future or repeated task in library; use chronological stream")
        return tuple(sorted(relevant, key=lambda e: e.task_index)), fingerprint(obj)

    def append(self, entry: LibraryEntry, snapshot: str) -> None:
        _validate_lesson(entry.lesson, entry.evidence)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock = self.path.with_name(self.path.name + ".lock")
        with lock.open("x", encoding="utf-8"):
            try:
                obj = self._read()
                if fingerprint(obj) != snapshot:
                    raise ValueError("library changed while task was executing")
                self.before(PublicTask(entry.task_id, entry.domain, "library append"), entry.task_index)
                data = asdict(entry)
                obj["entries"].append({"entry": data, "sha256": fingerprint(data)})
                temporary = self.path.with_name(self.path.name + ".tmp")
                try:
                    temporary.write_text(json.dumps(obj, ensure_ascii=False, indent=2,
                                                    allow_nan=False) + "\n", encoding="utf-8")
                    temporary.replace(self.path)
                finally:
                    temporary.unlink(missing_ok=True)
            finally:
                lock.unlink(missing_ok=True)


def _decode_entry(data: dict) -> LibraryEntry:
    try:
        task = PublicTask(data["task_id"], data["domain"], "stored public task")
        if type(data["task_index"]) is not int or data["task_index"] < 0:
            raise ValueError("invalid library task index")
        adopted = Harness(tuple(tuple(p) for p in data["adopted"]["files"]))
        lesson = Lesson(**{**data["lesson"], "evidence_pairs":
                          tuple(tuple(p) for p in data["lesson"]["evidence_pairs"])})
        evidence = tuple(Evidence(e["label"], Harness(tuple(tuple(p) for p in e["harness"]["files"])),
                                  Execution(**e["execution"])) for e in data["evidence"])
        if len({e.label for e in evidence}) != len(evidence):
            raise ValueError("duplicate persisted execution labels")
        _validate_lesson(lesson, evidence)
        return LibraryEntry(task.task_id, task.domain, data["task_index"], adopted, lesson, evidence)
    except (KeyError, TypeError) as exc:
        raise ValueError("malformed library entry") from exc


def _map(fn: Callable[[_T], object], items: Sequence[_T], workers: int) -> list:
    if workers == 1 or len(items) < 2:
        return [fn(item) for item in items]
    with ThreadPoolExecutor(max_workers=min(workers, len(items))) as pool:
        return list(pool.map(fn, items))


class Harness2:
    """Inject real callbacks; preserve the published width/depth and budget identities."""

    def __init__(self, *, executor: Callable, editor: Callable, selector: Callable,
                 reflector: Callable, config: ExecutionConfig, k: int = 1,
                 mode: str = "parallel", workers: int = 1):
        if type(k) is not int or not 1 <= k <= 16:
            raise ValueError("local controller budget must be 1..16")
        if mode not in {"parallel", "sequential"}:
            raise ValueError("exactly parallel and sequential modes are supported")
        if type(workers) is not int or not 1 <= workers <= 8:
            raise ValueError("workers must be 1..8")
        if not isinstance(config, ExecutionConfig) or not all(
                callable(f) for f in (executor, editor, selector, reflector)):
            raise ValueError("execution config and explicit callbacks required")
        self.executor, self.editor, self.selector, self.reflector = executor, editor, selector, reflector
        self.config, self.k, self.mode, self.workers = config, k, mode, workers

    @property
    def namespace(self) -> str:
        return fingerprint({"protocol": PROTOCOL, "config": asdict(self.config),
                            "k": self.k, "mode": self.mode})

    def _execute(self, task: PublicTask, item: tuple[str, Harness]) -> Evidence:
        label, harness = item
        try:
            output = self.executor(task, harness, self.config)
            if not isinstance(output, Execution):
                raise ValueError("executor must return an Execution")
        except Exception as exc:
            output = Execution("", "", False, f"{type(exc).__name__}: execution failed")
        return Evidence(label, harness, output)

    def _edit(self, label: str, context: EditContext) -> StageRecord:
        errors = []
        for attempt in (1, 2):
            try:
                edit = self.editor(context)
                if not isinstance(edit, Edit) or not isinstance(edit.harness, Harness):
                    raise ValueError("editor must return an Edit with validated Harness")
                _text(edit.notes, "edit notes")
                known = {e.label for e in context.references + context.pool}
                if (type(edit.supports) is not tuple or not edit.supports or
                        any(type(p) is not str or p not in known for p in edit.supports)):
                    raise ValueError("edits must cite visible execution evidence")
                return StageRecord(label, context, edit, attempt, errors=tuple(errors))
            except Exception as exc:
                errors.append(f"{type(exc).__name__}: invalid or failed edit")
        return StageRecord(label, context, Edit(context.current,
            "Invalid proposal; preserved current harness, not a successful edit.", ()),
            2, True, tuple(errors))

    def run(self, task: PublicTask, base: Harness, *, library: EvidenceLibrary | None = None,
            task_index: int = 0) -> RunResult:
        if not isinstance(task, PublicTask) or not isinstance(base, Harness):
            raise ValueError("explicit public task and validated harness required")
        if base.sha256 != self.config.initial_harness_sha256:
            raise ValueError("initial harness differs from frozen execution config")
        if library is not None and library.namespace != self.namespace:
            raise ValueError("library must be scoped to model/environment/seed/mode/budget")
        prior, snapshot = library.before(task, task_index) if library else ((), "")
        # All probes get the same frozen config and public input. The stream
        # resets to base; earlier adopted execution harnesses are not inherited.
        references = tuple(_map(lambda item: self._execute(task, item),
                                [(f"base{i}", base) for i in range(1, self.k + 1)], self.workers))
        evidence, stages, finals = list(references), [], []
        current, history = base, ()
        rounds = (1,) if self.mode == "parallel" else range(1, self.k + 1)
        for index in rounds:
            indices = range(1, self.k + 1) if self.mode == "parallel" else (index,)
            specs = [(f"{scope}{i}", scope, i) for i in indices for scope in ("invariant", "domain")]
            decisions = tuple((s.label, s.edit.notes) for s in stages)
            proposed = _map(lambda s: self._edit(s[0], EditContext(task, current, references,
                history, prior, s[1], s[2], decisions)), specs, self.workers)
            stages.extend(proposed)
            probes = tuple(_map(lambda s: self._execute(task, (s.label, s.edit.harness)), proposed, self.workers))
            evidence.extend(probes)
            pool = history + probes
            composition_indices = range(1, self.k + 1) if self.mode == "parallel" else (index,)
            decisions = tuple((s.label, s.edit.notes) for s in stages)
            composed = _map(lambda i: self._edit(f"compose{i}", EditContext(task, current,
                references, pool, prior, "compose", i, decisions)), tuple(composition_indices), self.workers)
            stages.extend(composed)
            outputs = tuple(_map(lambda s: self._execute(task, (s.label, s.edit.harness)), composed, self.workers))
            evidence.extend(outputs)
            finals.extend(e.label for e in outputs)
            if self.mode == "sequential":
                current = composed[0].edit.harness
                history = pool + outputs
        if len(evidence) != 4*self.k or len(stages) != 3*self.k:
            raise AssertionError("Harness² budget identity violated")
        labels = [e.label for e in evidence]
        if len(set(labels)) != len(labels):
            raise AssertionError("duplicate execution labels")
        available = [e for e in evidence if e.label in finals and e.execution.ok and e.execution.deliverable.strip()]
        adopted, selection_error = None, ""
        if not available:
            selection_error = "No final deliverable; base and proposals are not selection candidates."
        elif self.k == 1:
            adopted = available[0]
        else:
            # A task/run-stable permutation; no origin harness or rollout labels
            # are visible to the selector. It cannot synthesize a new output.
            shuffled = sorted(available, key=lambda e: e.label)
            random.Random(fingerprint({"task": task.task_id, "namespace": self.namespace})).shuffle(shuffled)
            id_map = {f"candidate-{i}": e for i, e in enumerate(shuffled)}
            context = SelectionContext(task, tuple((key, e.execution.deliverable) for key, e in id_map.items()))
            try:
                choice = self.selector(context)
                if type(choice) is not str or choice not in id_map:
                    raise ValueError("selector must choose an existing anonymous candidate")
                adopted = id_map[choice]
            except Exception:
                # Same deterministic finals-only fallback as upstream. This is
                # recorded as a selection failure, never a positive judgment.
                adopted = sorted(available, key=lambda e: e.label)[0]
                selection_error = "Selector failed; deterministic existing-final fallback, not quality evidence."
        retained, reflection_error = False, ""
        if adopted is not None:
            try:
                lesson = self.reflector(ReflectionContext(task, base, adopted, tuple(evidence), tuple(stages), prior))
                if lesson is not None:
                    _validate_lesson(lesson, evidence)
                    if library is not None:
                        cited = {label for pair in lesson.evidence_pairs for label in pair}
                        entry = LibraryEntry(task.task_id, task.domain, task_index, adopted.harness,
                                             lesson, tuple(e for e in evidence if e.label in cited))
                        library.append(entry, snapshot)
                        retained = True
            except Exception as exc:
                reflection_error = f"{type(exc).__name__}: reflection not retained"
        return RunResult(task, self.config, self.mode, self.k, tuple(evidence), tuple(stages),
            tuple(finals), adopted.label if adopted else None, selection_error,
            retained, reflection_error, len(prior))
