"""Bounded CPU slice of Agent-Kernel (arXiv:2611.31727v1).

This is an orchestration component, not an LLM policy or an exactly-once tool
boundary. Executors receive task text and actual predecessor output, never a
reference answer. SQLite state is durable; external side effects are not rolled
back. One scheduler owns a buffer at a time; reopening explicitly revokes old
running claims rather than trusting late completions from the previous owner.
"""

from __future__ import annotations

from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from dataclasses import dataclass
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
from typing import Callable
import uuid


REQUIRES_GPU_VALIDATION = False

TERMINAL = frozenset({"complete", "failed", "cancelled", "unreachable"})
STATES = frozenset({"pending", "waiting", "running"}) | TERMINAL


@dataclass(frozen=True)
class Claim:
    node_id: str
    generation: int
    owner: str
    task: str
    role: str
    prompt: str
    parent_outputs: tuple[tuple[str, str], ...]


class AgentKernel:
    """SQLite SAB, dependency cascades and the five verbs on small DAGs.

    ``fork`` returns immediately without waiting for execution. ``run`` is an
    optional bounded concurrent driver; it may itself be started on a caller's
    background thread. Raw parent text is inherited in declared order. The
    character cap is a local admission bound, NOT a model token-budget policy.
    """

    def __init__(self, path: str | Path, *, recover_running: bool = False,
                 max_context_chars: int = 100_000):
        if max_context_chars <= 0:
            raise ValueError("context bound must be positive")
        self.owner = uuid.uuid4().hex
        self.max_context_chars = max_context_chars
        self._lock = threading.RLock()
        self.db = sqlite3.connect(str(path), check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS nodes (
                id TEXT PRIMARY KEY, task TEXT NOT NULL, role TEXT NOT NULL,
                state TEXT NOT NULL, generation INTEGER NOT NULL DEFAULT 0,
                owner TEXT, output TEXT, attempts INTEGER NOT NULL DEFAULT 0,
                retry_budget INTEGER NOT NULL, history TEXT NOT NULL DEFAULT '[]'
            );
            CREATE TABLE IF NOT EXISTS edges (
                parent TEXT NOT NULL REFERENCES nodes(id),
                child TEXT NOT NULL REFERENCES nodes(id), position INTEGER NOT NULL,
                PRIMARY KEY(parent,child)
            );
        """)
        if recover_running:
            # An explicit single-owner handover: old claims cannot commit later.
            with self._lock, self.db:
                self.db.execute("UPDATE nodes SET state='waiting', owner=NULL, "
                                "generation=generation+1 WHERE state='running'")

    def close(self) -> None:
        with self._lock:
            self.db.close()

    def _record(self, node_id: str) -> dict:
        row = self.db.execute("SELECT * FROM nodes WHERE id=?", (node_id,)).fetchone()
        if row is None:
            raise KeyError(node_id)
        out = dict(row)
        out["history"] = json.loads(out["history"])
        out["depends_on"] = [r[0] for r in self.db.execute(
            "SELECT parent FROM edges WHERE child=? ORDER BY position", (node_id,))]
        return out

    def fetch(self, node_id: str) -> dict:
        with self._lock:
            return self._record(node_id)

    def query(self, state: str | None = None) -> list[dict]:
        if state is not None and state not in STATES:
            raise ValueError("unknown state")
        with self._lock:
            rows = self.db.execute("SELECT id FROM nodes ORDER BY rowid").fetchall()
            records = [self._record(row[0]) for row in rows]
            return [r for r in records if state is None or r["state"] == state]

    def fork(self, node_id: str, task: str, *, role: str = "worker",
             depends_on: tuple[str, ...] = (), retry_budget: int = 3) -> str:
        if not node_id or not isinstance(task, str) or retry_budget < 1:
            raise ValueError("invalid node")
        if len(set(depends_on)) != len(depends_on) or node_id in depends_on:
            raise ValueError("duplicate/self dependency")
        with self._lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            parents = [self._record(p) for p in depends_on]
            # Edges point only to previously created nodes, hence remain acyclic.
            self.db.execute("INSERT INTO nodes(id,task,role,state,retry_budget) "
                            "VALUES(?,?,?,'pending',?)", (node_id, task, role, retry_budget))
            self.db.executemany("INSERT INTO edges VALUES(?,?,?)", [
                (p, node_id, i) for i, p in enumerate(depends_on)])
            state = "unreachable" if any(p["state"] in
                {"failed", "cancelled", "unreachable"} for p in parents) else "waiting"
            self.db.execute("UPDATE nodes SET state=? WHERE id=?", (state, node_id))
        return node_id

    def _descendants(self, node_id: str) -> list[str]:
        return [r[0] for r in self.db.execute("""
            WITH RECURSIVE d(id) AS (
                SELECT child FROM edges WHERE parent=?
                UNION SELECT e.child FROM edges e JOIN d ON e.parent=d.id
            ) SELECT id FROM d
        """, (node_id,))]

    def _cascade_failure(self, node_id: str) -> None:
        for descendant in self._descendants(node_id):
            self.db.execute("UPDATE nodes SET state='unreachable', owner=NULL, "
                "generation=generation+1 WHERE id=? AND state NOT IN "
                "('complete','failed','cancelled','unreachable')", (descendant,))

    def retry(self, node_id: str) -> bool:
        """SGR itself has no retry-budget policy; the driver enforces it."""
        with self._lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            if self._record(node_id)["state"] != "failed":
                return False
            for descendant in self._descendants(node_id):
                self.db.execute("UPDATE nodes SET state='waiting', owner=NULL, "
                    "generation=generation+1 WHERE id=? AND state='unreachable'", (descendant,))
            self.db.execute("UPDATE nodes SET state='waiting', owner=NULL, "
                            "generation=generation+1 WHERE id=?", (node_id,))
        return True

    def cancel(self, node_id: str) -> bool:
        with self._lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            if self._record(node_id)["state"] in TERMINAL:
                return False
            self.db.execute("UPDATE nodes SET state='cancelled', owner=NULL, "
                            "generation=generation+1 WHERE id=?", (node_id,))
            self._cascade_failure(node_id)
        return True

    def claim_ready(self, limit: int = 1) -> list[Claim]:
        if limit < 1:
            return []
        claims = []
        with self._lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            for row in self.db.execute("SELECT id FROM nodes WHERE state='waiting' "
                                       "ORDER BY rowid").fetchall():
                record = self._record(row[0])
                parents = [self._record(p) for p in record["depends_on"]]
                if not all(p["state"] == "complete" for p in parents):
                    continue
                outputs = tuple((p["id"], p["output"] or "") for p in parents)
                context = "\n".join(f"<from id={p!r}>{text}</from>" for p, text in outputs if text)
                if context:
                    context = "<predecessor_outputs>\n" + context + "\n</predecessor_outputs>\n\n"
                if len(context) > self.max_context_chars:
                    raise ValueError("raw predecessor context exceeds local character bound")
                generation = record["generation"] + 1
                history = record["history"] + [{"event": "start", "generation": generation}]
                self.db.execute("UPDATE nodes SET state='running', generation=?, owner=?, "
                    "attempts=attempts+1, history=? WHERE id=?", (
                    generation, self.owner, json.dumps(history), record["id"]))
                claims.append(Claim(record["id"], generation, self.owner, record["task"],
                                    record["role"], context + record["task"], outputs))
                if len(claims) == limit:
                    break
        return claims

    def finish(self, claim: Claim, *, output: str | None = None,
               error: str | None = None) -> bool:
        if (output is None) == (error is None):
            raise ValueError("provide exactly one output or error")
        if output is not None and not isinstance(output, str):
            raise TypeError("executor output must be text")
        with self._lock, self.db:
            self.db.execute("BEGIN IMMEDIATE")
            record = self._record(claim.node_id)
            if (record["state"], record["generation"], record["owner"]) != (
                    "running", claim.generation, claim.owner):
                return False
            state = "failed" if error is not None else "complete"
            history = record["history"] + [{"event": state, "error": error}]
            self.db.execute("UPDATE nodes SET state=?,output=?,owner=NULL,history=? WHERE id=?",
                            (state, output, json.dumps(history), claim.node_id))
            if error is not None:
                self._cascade_failure(claim.node_id)
        return True

    def run(self, executor: Callable[[Claim], str], *, workers: int = 3,
            auto_retry: bool = True) -> list[dict]:
        if workers < 1:
            raise ValueError("workers must be positive")
        with ThreadPoolExecutor(max_workers=workers) as pool:
            active = {}
            while True:
                if auto_retry:
                    for row in self.query("failed"):
                        if row["attempts"] < row["retry_budget"]:
                            self.retry(row["id"])
                for claim in self.claim_ready(workers - len(active)):
                    active[pool.submit(executor, claim)] = claim
                if not active:
                    return self.query()
                done, _ = wait(active, return_when=FIRST_COMPLETED)
                for future in done:
                    claim = active.pop(future)
                    try:
                        self.finish(claim, output=future.result())
                    except Exception as exc:  # an exception is a signal, not a semantic judge
                        self.finish(claim, error=f"{type(exc).__name__}: {exc}")


def diagnostic(seed: int = 42, device: str = "cpu") -> dict:
    """Small deterministic failure-injection control; no task capability score."""
    if type(seed) is not int or seed < 0 or device != "cpu":
        raise ValueError("nonnegative integer seed and CPU-only device required")
    import random
    names = ["a", "b", "c"]
    random.Random(seed).shuffle(names)
    with tempfile.TemporaryDirectory() as tmp:
        kernel = AgentKernel(Path(tmp) / "sab.sqlite")
        for name in names:
            kernel.fork(name, name.upper())
        kernel.fork("join", "join", depends_on=("a", "b", "c"))
        seen = {}
        def executor(claim: Claim) -> str:
            seen[claim.node_id] = seen.get(claim.node_id, 0) + 1
            if claim.node_id == "a" and seen["a"] == 1:
                raise RuntimeError("controlled transient exception")
            return "|".join(text for _, text in claim.parent_outputs) if claim.parent_outputs else claim.task
        rows = kernel.run(executor)
        result = {"diagnostic_only": True, "seed": seed, "nodes_complete": sum(
            r["state"] == "complete" for r in rows), "executor_calls": sum(seen.values()),
            "preserved_sibling_calls": seen["b"] + seen["c"],
            "parent_text_order_correct": kernel.fetch("join")["output"] == "A|B|C"}
        kernel.close()
        reopened = AgentKernel(Path(tmp) / "sab.sqlite", recover_running=True)
        result["durable_complete_nodes"] = len(reopened.query("complete"))
        reopened.close()
        result["evaluation_tier"] = "l1_mechanism"
        result["checks"] = {
            "transient_failure_recovery_completes_graph": result["nodes_complete"] == 4,
            "completed_siblings_are_not_reexecuted": result["preserved_sibling_calls"] == 2,
            "actual_parent_text_keeps_declared_order": result["parent_text_order_correct"],
            "reopened_sqlite_preserves_complete_nodes": result["durable_complete_nodes"] == 4,
        }
        result["metrics"] = {key: result[key] for key in (
            "nodes_complete", "executor_calls", "preserved_sibling_calls", "durable_complete_nodes")}
        return result
