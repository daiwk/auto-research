"""Bounded single-host durable LogAct protocol (arXiv:2604.07988v1).

Independent SQLite implementation of intention -> votes -> commit/abort ->
execution/result. It is not distributed consensus, an LLM agent, a sandbox, or
an exactly-once wrapper for arbitrary external effects. Recovery is conservative:
an uncertain non-idempotent action is never automatically re-executed.
"""
from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import random
import sqlite3
import tempfile
from typing import Callable

UPSTREAM_REVISION = "db395449fb2dbb534c8eec848900252ac8324ab2"


def _text(value: str) -> str:
    if type(value) is not str or not value.strip():
        raise ValueError("nonempty plain string required")
    return value


def _json(value) -> str:
    try:
        return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)
    except (TypeError, ValueError) as error:
        raise ValueError("finite JSON-compatible value required") from error


class RecoveryRequired(RuntimeError):
    """The effect may have occurred; a replay needs an explicit safe contract."""


@dataclass(frozen=True, slots=True)
class IntentView:
    intent_id: str
    operation: str
    arguments_json: str

    @property
    def arguments(self) -> dict:
        """A fresh public-action copy, never a private evaluation context."""
        return json.loads(self.arguments_json)


class DurableLogAct:
    """One logical agent on one POSIX host, with an immutable voter policy.

    A per-database OS lock fences concurrent local executors. SQLite FULL/WAL
    protects committed records against process restart, not disk loss or a
    malicious process with filesystem access. Voter names identify trusted
    integrations; they are not authenticated network identities. The executor
    callback is trusted and receives only an IntentView and a stable effect key.
    """

    def __init__(self, path: Path, *, bus_id: str, voters: tuple[str, ...], quorum: int):
        if (type(voters) is not tuple or not voters or len(set(voters)) != len(voters)
                or any(type(v) is not str or not v.strip() for v in voters)
                or type(quorum) is not int or not 1 <= quorum <= len(voters)):
            raise ValueError("unique named voters and a positive reachable quorum required")
        _text(bus_id)
        if str(path) == ":memory:":
            raise ValueError("durable on-disk database required")
        self.path = Path(path).resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.bus_id, self.voters, self.quorum = bus_id, tuple(sorted(voters)), quorum
        with self._transaction() as db:
            db.execute("CREATE TABLE IF NOT EXISTS metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.execute("CREATE TABLE IF NOT EXISTS intents (id TEXT PRIMARY KEY, operation TEXT NOT NULL, "
                       "arguments TEXT NOT NULL, replay_contract TEXT NOT NULL, decision TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS votes (intent_id TEXT NOT NULL REFERENCES intents(id), "
                       "voter TEXT NOT NULL, approved INTEGER NOT NULL, PRIMARY KEY(intent_id,voter))")
            db.execute("CREATE TABLE IF NOT EXISTS executions (intent_id TEXT PRIMARY KEY REFERENCES intents(id), "
                       "status TEXT NOT NULL, attempt INTEGER NOT NULL, result TEXT)")
            db.execute("CREATE TABLE IF NOT EXISTS entries (position INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "kind TEXT NOT NULL, intent_id TEXT NOT NULL, payload TEXT NOT NULL)")
            policy = _json({"bus_id": bus_id, "voters": self.voters, "quorum": quorum})
            existing = db.execute("SELECT value FROM metadata WHERE key='policy'").fetchone()
            if existing is None:
                db.execute("INSERT INTO metadata VALUES ('policy',?)", (policy,))
            elif existing[0] != policy:
                raise ValueError("reopening cannot silently change bus identity or voter policy")

    @contextmanager
    def _transaction(self):
        db = sqlite3.connect(self.path, timeout=5, isolation_level=None)
        db.row_factory = sqlite3.Row
        try:
            db.execute("PRAGMA journal_mode=WAL")
            db.execute("PRAGMA synchronous=FULL")
            db.execute("PRAGMA foreign_keys=ON")
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except BaseException:
            db.rollback()
            raise
        finally:
            db.close()

    @contextmanager
    def _executor_lock(self):
        # Only protects this database on this host. No distributed lease claim.
        import fcntl
        with self.path.with_suffix(self.path.suffix + ".executor.lock").open("a+b") as handle:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as error:
                raise RuntimeError("another local executor is active") from error
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _append(db, kind: str, intent_id: str, payload) -> None:
        db.execute("INSERT INTO entries(kind,intent_id,payload) VALUES (?,?,?)",
                   (kind, intent_id, _json(payload)))

    @staticmethod
    def _intent(db, intent_id: str):
        row = db.execute("SELECT * FROM intents WHERE id=?", (intent_id,)).fetchone()
        if row is None:
            raise KeyError(intent_id)
        return row

    def propose(self, intent_id: str, operation: str, arguments: dict, *,
                replay_contract: str = "at-most-once") -> IntentView:
        for value in (intent_id, operation):
            _text(value)
        if type(arguments) is not dict or replay_contract not in {"at-most-once", "idempotent"}:
            raise ValueError("public JSON arguments and an explicit supported replay contract required")
        encoded = _json(arguments)
        with self._transaction() as db:
            row = db.execute("SELECT * FROM intents WHERE id=?", (intent_id,)).fetchone()
            if row is not None:
                if (row["operation"], row["arguments"], row["replay_contract"]) != (operation, encoded, replay_contract):
                    raise ValueError("an intention identity cannot be rebound to a different action")
            else:
                pending = db.execute("SELECT i.id FROM intents i LEFT JOIN executions e ON i.id=e.intent_id "
                                     "WHERE i.decision IS NULL OR (i.decision='commit' "
                                     "AND (e.status IS NULL OR e.status!='succeeded')) LIMIT 1").fetchone()
                if pending:
                    raise RuntimeError("one in-flight intention allowed; resolve the prior intention first")
                db.execute("INSERT INTO intents VALUES (?,?,?,?,NULL)", (intent_id, operation, encoded, replay_contract))
                self._append(db, "intent", intent_id, {"operation": operation, "arguments": arguments,
                                                       "replay_contract": replay_contract})
        return IntentView(intent_id, operation, encoded)

    def vote(self, intent_id: str, voter: str, approved: bool) -> str | None:
        if voter not in self.voters or type(approved) is not bool:
            raise ValueError("vote must come from a configured voter with an explicit boolean")
        with self._transaction() as db:
            intent = self._intent(db, intent_id)
            prior = db.execute("SELECT approved FROM votes WHERE intent_id=? AND voter=?", (intent_id, voter)).fetchone()
            if prior:
                if bool(prior[0]) != approved:
                    raise ValueError("a recorded voter decision cannot be changed")
                return intent["decision"]
            if intent["decision"] is not None:
                raise RuntimeError("the logged decision is terminal")
            db.execute("INSERT INTO votes VALUES (?,?,?)", (intent_id, voter, int(approved)))
            self._append(db, "vote", intent_id, {"voter": voter, "approved": approved})
            total, yes = db.execute("SELECT count(*),sum(approved) FROM votes WHERE intent_id=?", (intent_id,)).fetchone()
            decision = ("commit" if yes >= self.quorum else
                        "abort" if yes + len(self.voters) - total < self.quorum else None)
            if decision is not None:
                db.execute("UPDATE intents SET decision=? WHERE id=?", (decision, intent_id))
                self._append(db, decision, intent_id, {"quorum": self.quorum})
            return decision

    def execute(self, intent_id: str, executor: Callable, *, recover: bool = False):
        """Run only durable commits; replay uncertain effects only when declared safe.

        ``idempotent`` is an external executor/API contract, not inferred from
        code. The stable key must actually deduplicate the effect, or repeated
        invocations must be intrinsically idempotent. A result cache alone cannot
        close the crash-after-effect/before-result window.
        """
        if type(recover) is not bool:
            raise ValueError("recover must be explicit boolean")
        with self._executor_lock():
            with self._transaction() as db:
                intent = self._intent(db, intent_id)
                if intent["decision"] != "commit":
                    raise PermissionError("an uncommitted or aborted intention must not execute")
                execution = db.execute("SELECT * FROM executions WHERE intent_id=?", (intent_id,)).fetchone()
                if execution and execution["status"] == "succeeded":
                    return json.loads(execution["result"])
                if execution and (not recover or intent["replay_contract"] != "idempotent"):
                    raise RecoveryRequired("uncertain prior effect: require explicit recovery and an idempotent executor")
                attempt = 1 if execution is None else execution["attempt"] + 1
                if execution:
                    self._append(db, "recovery", intent_id, {"attempt": attempt, "contract": "idempotent"})
                    db.execute("UPDATE executions SET status='running',attempt=? WHERE intent_id=?", (attempt, intent_id))
                else:
                    db.execute("INSERT INTO executions VALUES (?,'running',?,NULL)", (intent_id, attempt))
                self._append(db, "started", intent_id, {"attempt": attempt})
                view = IntentView(intent_id, intent["operation"], intent["arguments"])
                effect_key = hashlib.sha256(_json([self.bus_id, intent_id, intent["operation"], intent["arguments"]]).encode()).hexdigest()
            try:
                result = _json(executor(view, effect_key))
            except Exception as error:
                with self._transaction() as db:
                    db.execute("UPDATE executions SET status='uncertain' WHERE intent_id=?", (intent_id,))
                    self._append(db, "failed", intent_id, {"attempt": attempt, "error_type": type(error).__name__})
                raise
            with self._transaction() as db:
                db.execute("UPDATE executions SET status='succeeded',result=? WHERE intent_id=?", (result, intent_id))
                self._append(db, "result", intent_id, {"attempt": attempt, "value": json.loads(result)})
            return json.loads(result)

    def entries(self) -> tuple[dict, ...]:
        """Operator/auditor view; do not expose private evaluation data to actors."""
        with self._transaction() as db:
            return tuple({"position": row["position"], "kind": row["kind"], "intent_id": row["intent_id"],
                          "payload": json.loads(row["payload"])} for row in db.execute("SELECT * FROM entries ORDER BY position"))


def diagnostic(seed: int = 42) -> dict:
    """Real SQLite/file effects, scripted callbacks and zero model calls."""
    with tempfile.TemporaryDirectory(prefix="logact-diagnostic-") as directory:
        path = Path(directory) / "bus.sqlite"
        log = DurableLogAct(path, bus_id=f"generated-{seed}", voters=("rules", "review"), quorum=2)
        amount = random.Random(seed).randint(1, 9)
        log.propose("add", "add", {"amount": amount}, replay_contract="idempotent")
        calls = []
        effect = Path(directory) / "effect.txt"
        external_database = Path(directory) / "external.sqlite"

        def executor(view, key):
            calls.append(key)
            assert any(e["kind"] == "commit" for e in log.entries())
            with sqlite3.connect(external_database) as db:
                db.execute("CREATE TABLE IF NOT EXISTS effects (key TEXT PRIMARY KEY, amount INTEGER NOT NULL)")
                db.execute("INSERT OR IGNORE INTO effects VALUES (?,?)", (key, amount))
            # The file operation is also intrinsically idempotent: same contents.
            effect.write_text(str(amount))
            if len(calls) == 1:
                raise RuntimeError("simulated failure after real effect, before logged result")
            return {"written": int(effect.read_text())}

        blocked = False
        try:
            log.execute("add", executor)
        except PermissionError:
            blocked = True
        log.vote("add", "rules", True)
        incomplete = False
        try:
            log.execute("add", executor)
        except PermissionError:
            incomplete = True
        log.vote("add", "review", True)
        try:
            log.execute("add", executor)
        except RuntimeError:
            pass
        reopened = DurableLogAct(path, bus_id=f"generated-{seed}", voters=("rules", "review"), quorum=2)
        requires_recovery = False
        try:
            reopened.execute("add", executor)
        except RecoveryRequired:
            requires_recovery = True
        result = reopened.execute("add", executor, recover=True)
        cached = reopened.execute("add", executor)
        reopened.propose("denied", "delete", {})
        reopened.vote("denied", "rules", False)
        rejected = False
        try:
            reopened.execute("denied", lambda *_: calls.append("UNSAFE"))
        except PermissionError:
            rejected = True
        kinds = [e["kind"] for e in reopened.entries()]
        with sqlite3.connect(external_database) as db:
            distinct_effects = db.execute("SELECT count(*) FROM effects").fetchone()[0]
        checks = {"uncommitted_blocked": blocked, "incomplete_quorum_blocked": incomplete,
                  "commit_before_real_effect": kinds.index("commit") < kinds.index("started"),
                  "uncertain_effect_requires_explicit_recovery": requires_recovery,
                  "idempotent_retry_and_cached_result": len(calls) == 2 and distinct_effects == 1 and result == cached,
                  "durable_reopen_result": result == {"written": amount}, "rejected_action_never_executed": rejected and "UNSAFE" not in calls}
        return {"seed": seed, "metrics": {"actual_llm_calls": 0, "executor_invocations": len(calls),
                "distinct_effects": distinct_effects, "recovery_entries": kinds.count("recovery"),
                "log_entries": len(kinds)}, "checks": checks}
