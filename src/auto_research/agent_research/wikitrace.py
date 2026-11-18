"""WikiTrace source-linked corpus protocol; no compiler LLM or task-solving actor."""
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from types import MappingProxyType

REQUIRES_GPU_VALIDATION = False


@dataclass(frozen=True)
class ToolStep:
    action: str
    observation: str

    def __post_init__(self):
        if not isinstance(self.action, str) or not isinstance(self.observation, str):
            raise ValueError("actions and public observations must be text")


@dataclass(frozen=True)
class SourceRun:
    identity: str
    task: str
    trajectory: tuple[ToolStep, ...]
    success: bool
    split: str = "train"

    def __post_init__(self):
        if (not self.identity or not isinstance(self.identity, str)
                or not isinstance(self.task, str) or not self.task
                or type(self.success) is not bool or self.split != "train"
                or not isinstance(self.trajectory, tuple)
                or not all(isinstance(step, ToolStep) for step in self.trajectory)):
            raise ValueError("identified training run with immutable observable steps required")

    @property
    def digest(self):
        return sha256(json.dumps(asdict(self), sort_keys=True, ensure_ascii=False).encode()).hexdigest()


@dataclass(frozen=True)
class Compilation:
    run_id: str
    title: str
    interpretation: str


@dataclass(frozen=True)
class Insight:
    identity: str
    run_id: str
    text: str
    applicability: str


class EvidenceLinkedCorpus:
    """Freeze externally compiled train evidence without merging or validating lessons.

    Compilation is an interpretation, not a verified explanation. Source outcomes
    may be false; contradictory insights are retained, rather than silently fixed.
    """
    def __init__(self, runs, compilations, insights):
        runs, compilations, insights = tuple(runs), tuple(compilations), tuple(insights)
        if (not all(isinstance(row, SourceRun) for row in runs)
                or not all(isinstance(row, Compilation) for row in compilations)
                or not all(isinstance(row, Insight) for row in insights)):
            raise ValueError("typed corpus records required")
        raw = {row.identity: row for row in runs}
        compiled = {row.run_id: row for row in compilations}
        lessons = {row.identity: row for row in insights}
        if (len(raw) != len(runs) or len(compiled) != len(compilations)
                or len(lessons) != len(insights) or set(raw) != set(compiled)):
            raise ValueError("unique runs, compilations and insight IDs with full source coverage required")
        counts = dict.fromkeys(raw, 0)
        for row in compilations:
            if not all(isinstance(x, str) and x for x in (row.run_id, row.title, row.interpretation)):
                raise ValueError("nonempty compilation fields required")
        for row in insights:
            if row.run_id not in raw or not all(isinstance(x, str) and x for x in (
                    row.identity, row.run_id, row.text, row.applicability)):
                raise ValueError("insights must link to a real training run")
            counts[row.run_id] += 1
        if any(value > 3 for value in counts.values()):
            raise ValueError("the paper extracts at most three insights per source run")
        self.runs = MappingProxyType(raw)
        self.compilations = MappingProxyType(compiled)
        self.insights = MappingProxyType(lessons)
        self.source_digests = MappingProxyType({key: row.digest for key, row in raw.items()})

    def actor_memory(self):
        """All insights are visible; no gold answer, task oracle or correctness claim."""
        return tuple(self.insights.values())

    def descend(self, insight_id: str):
        insight = self.insights[insight_id]
        raw = self.runs[insight.run_id]
        if raw.digest != self.source_digests[raw.identity]:
            raise ValueError("source trajectory integrity failure")
        return self.compilations[raw.identity], raw


def diagnostic(seed: int, device: str = "cpu") -> dict:
    if device != "cpu":
        raise ValueError("WikiTrace corpus protocol is CPU-only")
    run = SourceRun("run-0", "inspect lamp", (ToolStep("look", "lamp is off"),), False)
    compilation = Compilation("run-0", "failed lamp inspection", "Inspection did not turn it on.")
    insights = (Insight("a", "run-0", "Inspect before switching.", "lamp tasks"),
                Insight("b", "run-0", "Inspection may be insufficient.", "failed inspection"))
    corpus = EvidenceLinkedCorpus((run,), (compilation,), insights)
    before = run.digest
    recovered_compilation, recovered = corpus.descend("b")
    immutable = False
    try:
        corpus.runs["other"] = run
    except TypeError:
        immutable = True
    return {"seed": seed, "diagnostic_only": True, "evaluation_tier": "l1_mechanism",
            "metrics": {"source_runs": len(corpus.runs), "linked_insights": len(corpus.insights)},
            "checks": {"raw_source_unchanged": recovered.digest == before,
                       "failed_source_retained": recovered.success is False,
                       "exact_compilation_link": recovered_compilation == compilation,
                       "all_insights_retained": corpus.actor_memory() == insights,
                       "read_only_corpus": immutable}}
