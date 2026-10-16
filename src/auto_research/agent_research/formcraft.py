"""Independent CPU sequence-domain FormCraft mechanism, not upstream code.

The public composer sees training examples and callable operation IDs only.
Reference goals and held-out inputs remain exclusively in the evaluator.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import itertools
import json
from pathlib import Path
import random
from typing import Callable, Sequence

SequenceValue = tuple[int, ...]
TYPE = "sequence[int] -> sequence[int]"


@dataclass(frozen=True)
class Capability:
    identity: str
    kind: str
    body: tuple[str, ...]
    signature: str = TYPE


def _identity(kind: str, body: tuple[str, ...], signature: str = TYPE) -> str:
    return hashlib.sha256(json.dumps([kind, body, signature], separators=(",", ":")).encode()).hexdigest()


class Library:
    """Content-addressed operations with separate formation and admission."""

    def __init__(self) -> None:
        self.records: dict[str, Capability] = {}
        self.failures: list[dict] = []
        for bit in ("0", "1"):
            cap = self.primitive(bit)
            self.records[cap.identity] = cap

    @staticmethod
    def primitive(bit: str) -> Capability:
        if bit not in {"0", "1"}:
            raise ValueError("unsupported primitive")
        body = (bit,)
        return Capability(_identity("append", body), "append", body)

    def form(self, operations: Sequence[str]) -> Capability:
        body = tuple(operations)
        if not body or any(operation not in self.records for operation in body):
            raise ValueError("formation requires existing public operations")
        return Capability(_identity("compose", body), "compose", body)

    def invoke(self, identity: str, value: SequenceValue) -> SequenceValue:
        if not isinstance(value, tuple) or any(type(item) is not int for item in value):
            raise ValueError("public input must be a tuple of integers")
        return self.evaluate(self.records[identity], value)

    def evaluate(self, capability: Capability, value: SequenceValue) -> SequenceValue:
        def run(cap: Capability, current: SequenceValue, ancestry: frozenset[str]) -> SequenceValue:
            if cap.identity in ancestry or len(ancestry) > 128:
                raise ValueError("cyclic or excessive composition depth")
            if cap.signature != TYPE or cap.identity != _identity(cap.kind, cap.body, cap.signature):
                raise ValueError("invalid capability identity or type")
            if cap.kind == "append" and cap.body in {("0",), ("1",)}:
                return (*current, int(cap.body[0]))
            if cap.kind != "compose" or not cap.body:
                raise ValueError("unsupported capability")
            for operation in cap.body:
                current = run(self.records[operation], current, ancestry | {cap.identity})
            return current
        return run(capability, value, frozenset())

    def admit(self, candidate: Capability, holdouts: Sequence[SequenceValue],
              oracle: Callable[[SequenceValue], SequenceValue]) -> bool:
        """Independent verifier: failures persist; no failed candidate promoted."""
        if not holdouts:
            raise ValueError("admission requires nonempty independent holdouts")
        try:
            passed = all(self.evaluate(candidate, value) == oracle(value) for value in holdouts)
        except (KeyError, ValueError, RecursionError) as error:
            self.failures.append({"identity": candidate.identity, "accepted": False,
                                  "reason": str(error)})
            return False
        if passed:
            self.records[candidate.identity] = candidate
        else:
            self.failures.append({"identity": candidate.identity, "accepted": False,
                                  "reason": "holdout_semantic_mismatch"})
        return passed

    def save(self, path: Path) -> None:
        payload = {"schema_version": 1, "records": [asdict(cap) for cap in self.records.values()],
                   "failures": self.failures}
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True, indent=2)

    @classmethod
    def load(cls, path: Path) -> Library:
        payload = json.loads(path.read_text())
        if payload.get("schema_version") != 1:
            raise ValueError("unsupported library version")
        library = cls()
        library.records.clear()
        for row in payload["records"]:
            cap = Capability(row["identity"], row["kind"], tuple(row["body"]), row["signature"])
            if cap.identity in library.records:
                raise ValueError("duplicate capability")
            library.records[cap.identity] = cap
        for cap in library.records.values():
            library.evaluate(cap, ())  # validates identities, parents and acyclicity
        library.failures = payload["failures"]
        return library


def compose_from_examples(library: Library, public_ids: Sequence[str],
                          examples: Sequence[tuple[SequenceValue, SequenceValue]],
                          *, max_depth: int, candidate_limit: int = 20000) -> tuple[Capability | None, int]:
    """Bounded enumerative synthesis; no oracle, goal recipe or holdout access."""
    if not examples or max_depth < 1 or candidate_limit < 1:
        raise ValueError("nonempty examples and positive bounds required")
    if len(set(public_ids)) != len(public_ids) or any(key not in library.records for key in public_ids):
        raise ValueError("invalid public operation pool")
    attempts = 0
    for depth in range(1, max_depth + 1):
        for operations in itertools.product(public_ids, repeat=depth):
            attempts += 1
            if attempts > candidate_limit:
                return None, candidate_limit
            candidate = library.form(operations)
            if all(library.evaluate(candidate, value) == expected for value, expected in examples):
                # Direct reuse preserves the stored operation's identity.
                return (library.records[operations[0]] if depth == 1 else candidate), attempts
    return None, attempts


def run_sequence_study(*, snapshot_path: Path, seed: int = 42, goals: int = 12,
                       holdout_count: int = 128) -> dict:
    """Fixed local D01-D12 protocol; not the author's undistributed task copy.

    Acquisition selects using four training examples, then admits via separate
    random inputs. The final library is saved without overwrite, destroyed in
    memory, and cold-loaded. Both final views use that identical persisted
    snapshot and differ only in exposed public operations. This measures search,
    not an LLM; the evaluator alone retains the reference recipes and test data.
    """
    if not 1 <= goals <= 12 or holdout_count < 1:
        raise ValueError("study supports 1..12 goals and positive holdouts")
    snapshot_path = Path(snapshot_path)
    if snapshot_path.exists() or snapshot_path.is_symlink():
        raise FileExistsError("library snapshot must be a new immutable path")
    library = Library()
    primitive_ids = tuple(library.records)
    rng = random.Random(seed)
    suffix = tuple(rng.randrange(2) for _ in range(goals))
    rows, acquisition, plans = [], [], []
    for depth in range(1, goals + 1):
        pattern = suffix[:depth]
        # The evaluator alone owns this reference; the composer gets examples.
        oracle = lambda value, tail=pattern: (*value, *tail)
        training = [tuple(rng.randrange(-9, 10) for _ in range(length)) for length in (0, 2, 4, 7)]
        holdout_rng = random.Random(seed * 1000 + depth)
        holdouts = []
        while len(holdouts) < holdout_count:
            value = tuple(holdout_rng.randrange(-100, 101)
                          for _ in range(holdout_rng.randrange(1, 20)))
            if value not in training and value not in holdouts:
                holdouts.append(value)
        examples = [(value, oracle(value)) for value in training]
        candidate, attempts = compose_from_examples(library, tuple(library.records), examples, max_depth=2)
        accepted = candidate is not None and library.admit(candidate, holdouts, oracle)
        acquisition.append({"goal": f"D{depth:02d}", "attempts": attempts, "accepted": accepted})
        if not accepted:
            rows.append({"goal": f"D{depth:02d}", "status": "acquisition_failed"})
            if candidate is None:
                library.failures.append({"goal": f"D{depth:02d}", "accepted": False,
                                         "reason": "acquisition_search_budget_or_depth_exhausted"})
            continue
        plans.append((depth, pattern, training, holdouts, examples))

    # Persistence is part of the measured path, not just a unit-tested helper.
    expected_ids = tuple(library.records)
    expected_failures = list(library.failures)
    library.save(snapshot_path)
    snapshot_sha256 = hashlib.sha256(snapshot_path.read_bytes()).hexdigest()
    del library
    library = Library.load(snapshot_path)
    if tuple(library.records) != expected_ids or library.failures != expected_failures:
        raise ValueError("cold-loaded library differs from the saved admitted snapshot")
    snapshot = {"path": f"{snapshot_path.parent.name}/{snapshot_path.name}",
                "sha256": snapshot_sha256, "records": len(library.records),
                "cold_loaded": True, "same_snapshot_for_both_views": True}
    for depth, pattern, training, holdouts, examples in plans:
        oracle = lambda value, tail=pattern: (*value, *tail)
        # Final paired evaluation is isolated from acquisition/admission.
        test_rng = random.Random(seed * 10000 + depth)
        test_inputs = []
        while len(test_inputs) < holdout_count:
            value = tuple(test_rng.randrange(-1000, 1001) for _ in range(test_rng.randrange(1, 25)))
            if value not in training and value not in holdouts:
                test_inputs.append(value)
        for view, pool, bound in (("expanded", primitive_ids, depth),
                                  ("first_class", tuple(library.records), 1)):
            selected, work = compose_from_examples(library, pool, examples, max_depth=bound)
            success = selected is not None and all(library.evaluate(selected, value) == oracle(value)
                                                   for value in test_inputs)
            rows.append({"goal": f"D{depth:02d}", "view": view, "candidate_attempts": work,
                         "holdout_pass": success, "holdout_examples": len(test_inputs),
                         "split": "isolated_final_test",
                         "library_snapshot_sha256": snapshot_sha256,
                         "cold_loaded_library": True,
                         "selected_identity": selected.identity if selected else None})
    expanded = sum(row["candidate_attempts"] for row in rows if row.get("view") == "expanded")
    first_class = sum(row["candidate_attempts"] for row in rows if row.get("view") == "first_class")
    if hashlib.sha256(snapshot_path.read_bytes()).hexdigest() != snapshot_sha256:
        raise ValueError("immutable library snapshot changed during paired evaluation")
    return {"schema_version": 1, "method": "formcraft", "seed": seed,
            "dataset": "local-fixed-sequence-D01-D12-v1", "evaluation_tier": "l1_mechanism",
            "diagnostic_only": True, "promotion_eligible": False,
            "paper_exact_replication": False, "model_calls": 0,
            "metrics": {"goals_admitted": sum(row["accepted"] for row in acquisition),
                        "library_records": len(library.records), "expanded_candidate_attempts": expanded,
                        "first_class_candidate_attempts": first_class,
                        "all_paired_holdouts_pass": len(rows) == 2 * goals and
                            all(row.get("holdout_pass", False) for row in rows)},
            "library_snapshot": snapshot,
            "acquisition": acquisition, "paired_results": rows,
            "failures": library.failures}
