"""LiSA's bounded CPU policy-memory kernel (Eq.1–2 and Appendix C.4).

LLM policy induction, Gemini embeddings and final guardrail inference are
external inputs, not replaced by local heuristics. The diagnostic uses explicit
synthetic embeddings/policy drafts and measures no safety capability.
"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, replace
import hashlib
import math
from typing import Callable

import numpy as np

REQUIRES_GPU_VALIDATION = False


def _text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("nonempty text required")
    return value


def _label(value):
    if type(value) is not int or value not in (0, 1):
        raise ValueError("0=allow or 1=refuse required")
    return value


def _vector(value):
    raw = tuple(value)
    if (not raw or any(isinstance(x, bool) or not isinstance(x, (int, float))
                       or not math.isfinite(x) for x in raw)):
        raise ValueError("finite nonzero embedding required")
    norm = math.sqrt(math.fsum(x * x for x in raw))
    if norm == 0 or not math.isfinite(norm):
        raise ValueError("finite nonzero embedding required")
    return tuple(float(x / norm) for x in raw)


def _cosine(left, right):
    if len(left) != len(right):
        raise ValueError("embedding dimensions must agree")
    return math.fsum(a * b for a, b in zip(left, right, strict=True))


def beta_lower(support: int, contradiction: int, delta: float = .05) -> float:
    """Exact Beta(1+s,1+c) lower quantile, not empirical accuracy or a proxy CI."""
    if (any(type(x) is not int or x < 0 for x in (support, contradiction))
            or isinstance(delta, bool) or not 0 < delta < 1):
        raise ValueError("nonnegative integer evidence and a probability required")
    from scipy.special import betaincinv

    return float(betaincinv(1 + support, 1 + contradiction, delta))


def _clusters(vectors):
    """Average-linkage cosine clustering at distance <0.20, no cluster count."""
    if not vectors:
        return ()
    if len({len(v) for v in vectors}) != 1:
        raise ValueError("embedding dimensions must agree")
    if len(vectors) == 1:
        return ((0,),)
    from scipy.cluster.hierarchy import fcluster, linkage
    from scipy.spatial.distance import pdist

    distances = np.clip(pdist(np.asarray(vectors), metric="cosine"), 0, 2)
    labels = fcluster(linkage(distances, method="average"),
                      t=np.nextafter(.20, -np.inf), criterion="distance")
    groups = {}
    for i, label in enumerate(labels):
        groups.setdefault(int(label), []).append(i)
    return tuple(sorted((tuple(indices) for indices in groups.values()), key=lambda x: x[0]))


@dataclass(frozen=True)
class Report:
    identity: str
    scenario_group: str
    domain: str
    summary: str
    corrected_label: int
    embedding: tuple[float, ...]
    attributes: tuple[tuple[str, str], ...] = ()

    def __post_init__(self):
        for value in (self.identity, self.scenario_group, self.domain, self.summary):
            _text(value)
        _label(self.corrected_label)
        object.__setattr__(self, "embedding", _vector(self.embedding))
        attributes = tuple(self.attributes)
        if (any(not isinstance(p, tuple) or len(p) != 2 for p in attributes)
                or len({p[0] for p in attributes}) != len(attributes)):
            raise ValueError("distinct canonical attribute/value pairs required")
        for key, value in attributes:
            _text(key)
            _text(value)
        object.__setattr__(self, "attributes", tuple(sorted(attributes)))


@dataclass(frozen=True)
class Draft:
    """One external Template2 synthesis result; at most three per daily group."""
    identity: str
    title: str
    description: str
    content: str
    recommended_label: int | None
    rule_type: str
    embedding: tuple[float, ...]

    def __post_init__(self):
        for value in (self.identity, self.title, self.description, self.content, self.rule_type):
            _text(value)
        object.__setattr__(self, "embedding", _vector(self.embedding))

    def statement(self, label: int):
        _label(label)
        return (f"Title: {self.title}\nDescription: {self.description}\nContent: {self.content}\n"
                f"Recommended label: {label}\nRule type: {self.rule_type}")


@dataclass(frozen=True)
class Policy:
    identity: str
    statement: str
    label: int
    embedding: tuple[float, ...]
    support: int
    contradiction: int
    report_ids: tuple[str, ...]
    label_histogram: tuple[int, int]
    local: bool = False
    conflict_score: float = 0.
    near_conflict: bool = False

    def __post_init__(self):
        _text(self.identity)
        _text(self.statement)
        _label(self.label)
        object.__setattr__(self, "embedding", _vector(self.embedding))
        if (any(type(x) is not int or x < 0 for x in (self.support, self.contradiction))
                or len(self.label_histogram) != 2
                or any(type(x) is not int or x < 0 for x in self.label_histogram)
                or type(self.local) is not bool or type(self.near_conflict) is not bool
                or not 0 <= self.conflict_score <= .5):
            raise ValueError("valid counts, two-label histogram and conflict metadata required")
        if not self.report_ids or any(not isinstance(x, str) or not x for x in self.report_ids):
            raise ValueError("source report provenance required")

    @property
    def confidence(self):
        return beta_lower(self.support, self.contradiction)


class Memory:
    """Deterministic memory-side procedure, not a semantic classifier.

    Only externally reported adaptation failures enter refresh. The evaluator
    supplies held-out scenario-group identities solely as a leakage barrier;
    no held-out labels or answers enter memory or the final prompt.
    """
    def __init__(self, *, heldout_groups=()):
        self.heldout_groups = frozenset(_text(x) for x in heldout_groups)
        self.day = -1
        self._reports = {}
        self._raw = {}
        self._runtime = {}
        self._feedback_ids = set()
        self._last_surfaced = frozenset()
        self.broad = ()
        self.local = ()

    def refresh(self, day: int, reports: tuple[Report, ...], drafts: tuple[Draft, ...], *,
                embed_local: Callable[[str], tuple[float, ...]] | None = None):
        if type(day) is not int or day <= self.day or len(drafts) > 3:
            raise ValueError("increasing refresh day and <=3 externally induced items required")
        if any(not isinstance(r, Report) for r in reports) or any(not isinstance(x, Draft) for x in drafts):
            raise ValueError("typed failure reports and induced drafts required")
        if (len({r.identity for r in reports}) != len(reports)
                or any(r.identity in self._reports for r in reports)
                or len({d.identity for d in drafts}) != len(drafts)
                or any(d.identity in self._raw for d in drafts)):
            raise ValueError("new unique report/draft identities required")
        if any(r.scenario_group in self.heldout_groups for r in reports):
            raise ValueError("held-out scenario cannot enter adaptation")
        if drafts and not reports:
            raise ValueError("policy induction requires a nonempty daily failure group")
        histogram = tuple(sum(r.corrected_label == y for r in reports) for y in (0, 1))
        raw = dict(self._raw)
        for draft in drafts:
            label = draft.recommended_label
            if type(label) is not int or label not in (0, 1):
                if histogram[0] == histogram[1]:
                    raise ValueError("invalid synthesis label with tied group has no majority; retry upstream")
                label = int(histogram[1] > histogram[0])
            raw[draft.identity] = Policy(draft.identity, draft.statement(label), label, draft.embedding,
                                        histogram[label], histogram[1 - label],
                                        tuple(sorted(r.identity for r in reports)), histogram)
        history = dict(self._reports) | {r.identity: r for r in reports}
        local = self._local_rules(history, embed_local)
        candidates = tuple(raw[k] for k in sorted(raw))
        broad = []
        for indices in _clusters([c.embedding for c in candidates]):
            members = [candidates[i] for i in indices]
            center = _vector(np.asarray([c.embedding for c in members]).mean(axis=0).tolist())
            representative = min(members, key=lambda c: (-_cosine(c.embedding, center), c.identity))
            runtime = self._runtime.get(representative.statement, (0, 0))
            broad.append(replace(representative,
                support=sum(c.support for c in members) + runtime[0],
                contradiction=sum(c.contradiction for c in members) + runtime[1],
                report_ids=tuple(sorted({i for c in members for i in c.report_ids})),
                label_histogram=tuple(sum(c.label_histogram[y] for c in members) for y in (0, 1)),
                near_conflict=any(_cosine(representative.embedding, c.embedding) >= .85 for c in local)))
        self.day, self._reports, self._raw = day, history, raw
        self.broad, self.local = tuple(broad), tuple(local)
        self._last_surfaced = frozenset()
        self._runtime = {c.statement: self._runtime[c.statement] for c in broad
                         if c.statement in self._runtime}

    @staticmethod
    def _local_rules(history, embed_local):
        result = []
        for domain in sorted({r.domain for r in history.values()}):
            rows = sorted((r for r in history.values() if r.domain == domain), key=lambda r: r.identity)
            for indices in _clusters([r.embedding for r in rows]):
                members = [rows[i] for i in indices]
                labels = Counter(r.corrected_label for r in members)
                if len(members) < 2 or len(labels) != 2:
                    continue
                if embed_local is None:
                    raise ValueError("mixed-label regions require explicit local-text embedding provider")
                pivots = []
                for key in sorted({k for r in members for k, _ in r.attributes}):
                    values = [{dict(r.attributes).get(key) for r in members if r.corrected_label == y}
                              for y in (0, 1)]
                    if all(len(v) == 1 and None not in v for v in values) and values[0] != values[1]:
                        pivots.append(f"{key}: allow={next(iter(values[0]))}; refuse={next(iter(values[1]))}")
                ids = tuple(r.identity for r in members)
                region = "; ".join(f"{r.identity}[{r.corrected_label}]: {r.summary}; {dict(r.attributes)}"
                                   for r in members)
                for label in (0, 1):
                    text = (f"Local boundary in {domain}; recommended label={label}. "
                            f"Region: {region}. Differing common attributes: {'; '.join(pivots) or 'none recorded'}. "
                            "This is a narrow conflict cue, not a global rule.")
                    key = "local-" + hashlib.sha256(text.encode()).hexdigest()[:16]
                    result.append(Policy(key, text, label, _vector(embed_local(text)),
                                         labels[label], labels[1 - label], ids,
                                         (labels[0], labels[1]), True,
                                         1 - max(labels.values()) / len(members)))
        return result

    def retrieve(self, embedding, *, tau_allow: float = .55, tau_refuse: float = .55):
        if any(isinstance(t, bool) or not isinstance(t, (int, float)) or not 0 <= t <= 1
               for t in (tau_allow, tau_refuse)):
            raise ValueError("finite probability thresholds required")
        query = _vector(embedding)
        rank = lambda rows: tuple(sorted(rows, key=lambda c: (-_cosine(query, c.embedding), c.identity))[:2])
        # Retrieve at most two from each channel BEFORE filtering broad memory.
        candidates = rank(self.broad)
        broad = tuple(c for c in candidates if c.confidence >= (tau_allow, tau_refuse)[c.label])
        local = rank(self.local)  # No Beta gate on narrow mixed-label cues.
        self._last_surfaced = frozenset(c.identity for c in broad)
        return {"broad": broad, "local": local, "base_fallback": not broad and not local,
                "broad_candidate_ids": tuple(c.identity for c in candidates)}

    def feedback(self, identity: str, surfaced: tuple[str, ...], reported_label: int, *, split="adaptation"):
        _text(identity)
        _label(reported_label)
        known = {p.identity: p for p in self.broad}
        if split != "adaptation" or identity in self._feedback_ids or len(set(surfaced)) != len(surfaced):
            raise ValueError("unique adaptation-only feedback required")
        if any(i not in known for i in surfaced):
            raise ValueError("feedback must name currently surfaced broad policies")
        if not set(surfaced) <= self._last_surfaced:
            raise ValueError("feedback cannot update broad memory not surfaced at inference")
        changed = []
        for policy in self.broad:
            if policy.identity not in surfaced:
                changed.append(policy)
                continue
            matched = policy.label == reported_label
            old = self._runtime.get(policy.statement, (0, 0))
            self._runtime[policy.statement] = old[0] + int(matched), old[1] + int(not matched)
            changed.append(replace(policy, support=policy.support + int(matched),
                                   contradiction=policy.contradiction + int(not matched)))
        self.broad = tuple(changed)
        self._feedback_ids.add(identity)


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    if type(seed) is not int or device != "cpu":
        raise ValueError("integer seed and CPU-only component required")
    memory = Memory(heldout_groups=("held-out",))
    reports = (Report("public", "g1", "privacy", "A public lecture", 0, (1., .01),
                      (("event", "public"),)),
               Report("private", "g2", "privacy", "A private meeting", 1, (1., -.01),
                      (("event", "private"),)))
    draft = Draft("broad", "Information sharing", "Broad abstraction", "Prefer privacy", 1,
                  "broad", (1., 0.))
    memory.refresh(0, reports, (draft,), embed_local=lambda _: (1., 0.))
    context = memory.retrieve((1., 0.))
    return {"seed": seed, "device": "cpu", "diagnostic_only": True,
            "evaluation_tier": "l1_mechanism",
            "metrics": {"confidence_one_support": beta_lower(1, 0),
                        "confidence_five_support": beta_lower(5, 0),
                        "local_rules_retrieved": len(context["local"]),
                        "conflict_score": memory.local[0].conflict_score},
            "checks": {"exact_beta_evidence_volume": beta_lower(1, 0) < .55 <= beta_lower(5, 0),
                       "weak_broad_not_surfaced": not context["broad"],
                       "local_rules_are_not_confidence_gated": len(context["local"]) == 2,
                       "nonempty_local_context_prevents_base_fallback": not context["base_fallback"],
                       "synthetic_inputs_not_model_capability": True}}
