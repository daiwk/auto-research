from dataclasses import asdict
import os
from pathlib import Path
import sqlite3
import subprocess
import sys

import pytest

from auto_research.agent_research.logact import DurableLogAct, RecoveryRequired, diagnostic


def create(tmp_path, *, quorum=2):
    return DurableLogAct(tmp_path / "bus.sqlite", bus_id="test-bus", voters=("rule", "review"), quorum=quorum)


def approve(log, identity="one", *, replay_contract="at-most-once"):
    log.propose(identity, "append", {"text": "effect"}, replay_contract=replay_contract)
    log.vote(identity, "rule", True)
    assert log.vote(identity, "review", True) == "commit"


def test_durable_intention_and_quorum_precede_actual_file_effect(tmp_path):
    log = create(tmp_path)
    log.propose("one", "append", {"text": "effect"})
    output = tmp_path / "output.txt"

    def effect(view, _):
        # A separate DB connection observes the committed intention/votes/decision.
        with sqlite3.connect(log.path) as db:
            assert db.execute("SELECT decision FROM intents WHERE id='one'").fetchone()[0] == "commit"
            assert db.execute("SELECT count(*) FROM votes WHERE intent_id='one' AND approved=1").fetchone()[0] == 2
            assert db.execute("SELECT kind FROM entries ORDER BY position").fetchall()[-2:] == [("commit",), ("started",)]
        output.write_text(view.arguments["text"])
        return {"done": True}

    with pytest.raises(PermissionError):
        log.execute("one", effect)
    assert not output.exists()
    assert log.vote("one", "rule", True) is None
    with pytest.raises(PermissionError):
        log.execute("one", effect)
    assert not output.exists()
    log.vote("one", "review", True)
    assert log.execute("one", effect) == {"done": True}
    assert output.read_text() == "effect"
    reopened = create(tmp_path)
    assert reopened.execute("one", lambda *_: pytest.fail("duplicate commit executed twice")) == {"done": True}


def test_rejection_and_duplicate_votes_cannot_satisfy_quorum(tmp_path):
    log = create(tmp_path)
    log.propose("one", "delete", {})
    assert log.vote("one", "rule", True) is None
    assert log.vote("one", "rule", True) is None
    assert [e["kind"] for e in log.entries()].count("vote") == 1
    with pytest.raises(ValueError, match="changed"):
        log.vote("one", "rule", False)
    assert log.vote("one", "review", False) == "abort"
    with pytest.raises(PermissionError):
        log.execute("one", lambda *_: pytest.fail("aborted action executed"))
    # Abort terminates the flight, so a new action can be proposed.
    log.propose("two", "safe", {})


def test_or_quorum_accepts_one_approval_without_overriding_logged_decision(tmp_path):
    log = create(tmp_path, quorum=1)
    log.propose("one", "allowed", {})
    assert log.vote("one", "rule", False) is None
    assert log.vote("one", "review", True) == "commit"
    assert log.execute("one", lambda *_: "ok") == "ok"


def test_one_flight_and_immutable_intention_identity(tmp_path):
    log = create(tmp_path)
    original = log.propose("one", "write", {"x": 1})
    assert log.propose("one", "write", {"x": 1}) == original
    with pytest.raises(ValueError, match="rebound"):
        log.propose("one", "write", {"x": 2})
    with pytest.raises(RuntimeError, match="in-flight"):
        log.propose("two", "other", {})
    with pytest.raises(ValueError, match="configured"):
        log.vote("one", "not-a-voter", True)


def test_failed_non_idempotent_effect_never_automatically_replayed(tmp_path):
    log = create(tmp_path)
    approve(log)
    output = tmp_path / "effect.txt"

    def fail_after_effect(*_):
        with output.open("a") as handle:
            handle.write("side effect\n")
        raise RuntimeError("failed after effect")

    with pytest.raises(RuntimeError, match="failed after effect"):
        log.execute("one", fail_after_effect)
    reopened = create(tmp_path)
    for recover in (False, True):
        with pytest.raises(RecoveryRequired):
            reopened.execute("one", fail_after_effect, recover=recover)
    assert output.read_text().count("side effect") == 1
    with pytest.raises(RuntimeError, match="in-flight"):
        reopened.propose("two", "other", {})
    assert [e["kind"] for e in reopened.entries()] == ["intent", "vote", "vote", "commit", "started", "failed"]


def test_crash_after_effect_before_result_recovers_only_with_real_durable_dedup(tmp_path):
    log = create(tmp_path)
    approve(log, replay_contract="idempotent")
    # Child is genuinely terminated after an external SQLite effect, with no
    # chance to record its successful LogAct result or cleanly close the log.
    code = r'''
import os,sqlite3,sys
from pathlib import Path
from auto_research.agent_research.logact import DurableLogAct
directory=Path(sys.argv[1])
log=DurableLogAct(directory/'bus.sqlite',bus_id='test-bus',voters=('rule','review'),quorum=2)
def external(view,key):
    with sqlite3.connect(directory/'external.sqlite') as db:
        db.execute('CREATE TABLE IF NOT EXISTS effects (key TEXT PRIMARY KEY, text TEXT NOT NULL)')
        db.execute('INSERT OR IGNORE INTO effects VALUES (?,?)',(key,view.arguments['text']))
    os._exit(17)
log.execute('one',external)
'''
    root = Path(__file__).resolve().parents[1]
    env = {**os.environ, "PYTHONPATH": str(root / "src")}
    child = subprocess.run([sys.executable, "-c", code, str(tmp_path)], env=env, check=False, timeout=15)
    assert child.returncode == 17
    reopened = create(tmp_path)
    assert [e["kind"] for e in reopened.entries()][-1] == "started"

    def redo(view, key):
        with sqlite3.connect(tmp_path / "external.sqlite") as db:
            db.execute("INSERT OR IGNORE INTO effects VALUES (?,?)", (key, view.arguments["text"]))
            return {"effects": db.execute("SELECT count(*) FROM effects").fetchone()[0]}

    with pytest.raises(RecoveryRequired):
        reopened.execute("one", redo)
    assert reopened.execute("one", redo, recover=True) == {"effects": 1}
    assert reopened.execute("one", lambda *_: pytest.fail("cached result must not execute")) == {"effects": 1}
    assert [e["kind"] for e in reopened.entries()][-3:] == ["recovery", "started", "result"]


def test_active_local_executor_cannot_be_replayed_concurrently(tmp_path):
    log = create(tmp_path)
    approve(log, replay_contract="idempotent")
    other = create(tmp_path)

    def effect(*_):
        with pytest.raises(RuntimeError, match="another local executor"):
            other.execute("one", lambda *_: pytest.fail("concurrent effect"), recover=True)
        return "done"

    assert log.execute("one", effect) == "done"


def test_public_executor_view_has_no_store_or_private_gold_context(tmp_path):
    log = create(tmp_path)
    approve(log)
    private_gold = {"oracle": "not in actor inputs"}

    def effect(view, key):
        assert set(asdict(view)) == {"intent_id", "operation", "arguments_json"}
        assert private_gold["oracle"] not in repr(view)
        with pytest.raises(AttributeError):
            object.__setattr__(view, "gold", private_gold)
        view.arguments["text"] = "mutated copy"
        assert view.arguments == {"text": "effect"}
        assert len(key) == 64
        return "done"

    log.execute("one", effect)
    assert private_gold["oracle"] not in repr(log.entries())


def test_reopen_cannot_change_policy_and_relative_paths_share_execution_lock(tmp_path):
    log = create(tmp_path)
    with pytest.raises(ValueError, match="cannot silently"):
        DurableLogAct(log.path, bus_id="other", voters=("rule", "review"), quorum=2)
    with pytest.raises(ValueError, match="cannot silently"):
        create(tmp_path, quorum=1)
    alias = tmp_path / "alias.sqlite"
    alias.symlink_to(log.path)
    other = DurableLogAct(alias, bus_id="test-bus", voters=("rule", "review"), quorum=2)
    assert other.path == log.path


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_seeded_diagnostic_performs_effect_and_is_not_llm_capability(seed):
    result = diagnostic(seed)
    assert all(value is True for value in result["checks"].values())
    assert result["metrics"]["actual_llm_calls"] == 0
    assert result["metrics"]["executor_invocations"] == 2
    assert result["metrics"]["distinct_effects"] == 1


def test_invalid_configuration_and_payload_rejected(tmp_path):
    with pytest.raises(ValueError, match="durable"):
        DurableLogAct(Path(":memory:"), bus_id="x", voters=("v",), quorum=1)
    with pytest.raises(ValueError, match="quorum"):
        DurableLogAct(tmp_path / "x", bus_id="x", voters=("v", "v"), quorum=1)
    log = create(tmp_path)
    with pytest.raises(ValueError, match="JSON"):
        log.propose("one", "write", {"bad": float("nan")})
