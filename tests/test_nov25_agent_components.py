"""Finite CPU controls, not model capability or native-paper benchmarks."""

from concurrent.futures import ThreadPoolExecutor
import inspect
import random

import pytest

from auto_research.agent_research.agent_kernel import AgentKernel, Claim
from auto_research.agent_research.agent_kernel import diagnostic as kernel_diagnostic
from auto_research.agent_research.cape import (
    Action, CapeCompiler, Effect, Policy, catalog_retry, execute, exhaustive_oracle,
)
from auto_research.agent_research.cape import diagnostic as cape_diagnostic


def test_kernel_failure_cascade_and_sibling_preservation(tmp_path):
    k = AgentKernel(tmp_path / "dag.sqlite")
    for node in ("a", "b", "c"):
        k.fork(node, node)
    k.fork("join", "join", depends_on=("c", "a", "b"))
    claims = {c.node_id: c for c in k.claim_ready(3)}
    assert not k.claim_ready()
    k.finish(claims["b"], output="B")
    k.finish(claims["c"], output="C")
    before = {n: k.fetch(n) for n in ("b", "c")}
    k.finish(claims["a"], error="transient")
    assert k.fetch("join")["state"] == "unreachable"
    assert k.retry("a")
    assert all(k.fetch(n) == before[n] for n in before)
    claim = k.claim_ready()[0]
    assert claim.node_id == "a"
    k.finish(claim, output="A")
    join = k.claim_ready()[0]
    assert join.parent_outputs == (("c", "C"), ("a", "A"), ("b", "B"))
    assert join.prompt.endswith("</predecessor_outputs>\n\njoin")
    k.finish(join, output="joined")
    assert len(k.query("complete")) == 4
    assert not k.retry("b")
    k.close()


def test_kernel_reopen_revokes_stale_claim_and_keeps_completed(tmp_path):
    path = tmp_path / "durable.sqlite"
    old = AgentKernel(path)
    old.fork("done", "done")
    old.finish(old.claim_ready()[0], output="preserved")
    old.fork("work", "work", depends_on=("done",))
    stale = old.claim_ready()[0]
    new = AgentKernel(path, recover_running=True)
    assert new.fetch("done")["output"] == "preserved"
    assert not old.finish(stale, output="late-corrupt-output")
    fresh = new.claim_ready()[0]
    assert fresh.generation > stale.generation
    assert new.finish(fresh, output="fresh")
    assert not new.finish(fresh, output="double-commit")
    assert new.fetch("work")["output"] == "fresh"
    old.close()
    new.close()


def test_kernel_two_failed_parents_wait_and_cancel(tmp_path):
    k = AgentKernel(tmp_path / "two.sqlite")
    k.fork("a", "a")
    k.fork("b", "b")
    k.fork("join", "join", depends_on=("a", "b"))
    for c in k.claim_ready(2):
        k.finish(c, error="failed")
    k.retry("a")
    c = k.claim_ready()[0]
    k.finish(c, output="A")
    assert not k.claim_ready()  # b is still failed, join must not run
    k.retry("b")
    c = k.claim_ready()[0]
    assert k.cancel("b")
    assert not k.finish(c, output="late")
    assert k.fetch("join")["state"] == "unreachable"
    k.close()


def test_kernel_fork_is_nonblocking_and_claim_is_atomic(tmp_path):
    k = AgentKernel(tmp_path / "atomic.sqlite")
    k.fork("a", "task")
    with ThreadPoolExecutor(max_workers=2) as pool:
        claims = list(pool.map(lambda _: k.claim_ready(), range(2)))
    assert sum(map(len, claims)) == 1
    assert k.fetch("a")["state"] == "running"
    # A new fork remains available while another node is running.
    k.fork("b", "other")
    assert k.fetch("b")["state"] == "waiting"
    k.close()


def test_kernel_budget_and_external_side_effect_negative_control(tmp_path):
    k = AgentKernel(tmp_path / "budget.sqlite")
    k.fork("effect", "external write", retry_budget=2)
    effects = []
    def executor(claim):
        effects.append("external mutation")
        raise RuntimeError("exception AFTER mutation")
    k.run(executor)
    assert len(effects) == 2  # deliberately NOT an exactly-once guarantee
    assert k.fetch("effect")["state"] == "failed"
    assert k.fetch("effect")["attempts"] == 2
    k.close()


def test_kernel_dependency_and_context_admission(tmp_path):
    k = AgentKernel(tmp_path / "bound.sqlite", max_context_chars=2)
    with pytest.raises(KeyError):
        k.fork("missing", "task", depends_on=("absent",))
    with pytest.raises(ValueError):
        k.fork("self", "task", depends_on=("self",))
    k.fork("p", "parent")
    k.finish(k.claim_ready()[0], output="long parent")
    k.fork("c", "child", depends_on=("p",))
    with pytest.raises(ValueError, match="character bound"):
        k.claim_ready()
    assert k.fetch("c")["state"] == "waiting"
    k.close()


def family(seed=42, count=4):
    rng = random.Random(seed)
    hs = tuple(f"h{i}" for i in range(count))
    actions = tuple(Action(f"p{i}", True) for i in range(count)) + (
        Action("separate", False), Action("partial", False))
    table = {}
    for a in actions:
        for i, h in enumerate(hs):
            observation = h if a.name == "separate" else (
                str(i % 2) if a.name == "partial" else "error")
            table[a.name, h] = Effect(observation, a.name == f"p{i}")
    order = list(actions)
    rng.shuffle(order)
    return hs, tuple(order), table


def replay(policy, hs, table, calls):
    outcomes = [execute(policy, lambda a, h=h: table[a, h], call_limit=calls) for h in hs]
    return frozenset(h for h, (ok, _) in zip(hs, outcomes) if ok), sum(n for _, n in outcomes)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cape_certificates_bounds_and_coverage(seed):
    hs, actions, table = family(seed)
    compiler = CapeCompiler(hs, actions, lambda a, h: table[a, h],
                            catalog_retry(("p3", "p0", "p1")))
    policy = compiler.compile(max_queries=len(table))
    successes, calls = replay(policy, hs, table, 3)
    oracle = exhaustive_oracle(hs, actions, table, compiler.required, 3)
    assert compiler.certified
    assert (len(successes), -calls) == oracle
    assert compiler.required <= successes
    assert len(set(compiler.query_log)) == len(compiler.query_log) <= len(table)
    assert all(tuple(s["lower"]) <= oracle <= tuple(s["upper"]) for s in compiler.snapshots)
    assert [s["lower"] for s in compiler.snapshots] == sorted(s["lower"] for s in compiler.snapshots)
    assert [s["upper"] for s in compiler.snapshots] == sorted(
        (s["upper"] for s in compiler.snapshots), reverse=True)


@pytest.mark.parametrize("allowance", range(0, 25))
def test_cape_anytime_initial_coverage(allowance):
    hs, actions, table = family()
    initial = catalog_retry(("p3", "p0", "p1"))
    required, _ = replay(initial, hs, table, 3)
    compiler = CapeCompiler(hs, actions, lambda a, h: table[a, h], initial)
    policy = compiler.compile(max_queries=allowance)
    actual, _ = replay(policy, hs, table, 3)
    assert required <= actual
    assert len(compiler.query_log) <= allowance


def test_cape_local_closure_and_observation_only_deployment():
    hs, actions, table = family()
    compiler = CapeCompiler(hs, actions, lambda a, h: table[a, h], catalog_retry(("p3", "p0", "p1")))
    policy = compiler.compile(max_queries=len(table))
    # Local closure needs effects only on V, even if a global search eventually
    # acquires the complete row to prove a better root policy's optimality.
    local = CapeCompiler(hs, actions, lambda a, h: table[a, h], Policy())
    local._limit = 3
    for h in hs[:3]:
        local._acquire("separate", h)
    probe = next(a for a in actions if a.name == "separate")
    assert local._closed(probe, frozenset(hs[:3]))
    assert not local._closed(probe, frozenset(hs))
    assert ("separate", "h3") not in local.effects
    assert not any("configuration" in p for p in inspect.signature(execute).parameters)
    assert set(Policy.__dataclass_fields__) == {"action", "branches", "default"}
    assert set(Claim.__dataclass_fields__) == {
        "node_id", "generation", "owner", "task", "role", "prompt", "parent_outputs"}
    seen = []
    def unknown_tool(action):
        seen.append(action)
        return Effect("unseen deployment response", False)
    assert execute(policy, unknown_tool, call_limit=3)[0] is False
    assert len(seen) <= 3


@pytest.mark.parametrize("seed", range(8))
def test_cape_random_finite_tables_against_independent_oracle(seed):
    rng = random.Random(seed)
    hs = tuple(f"h{i}" for i in range(4))
    actions = tuple(Action(f"p{i}", True) for i in range(4)) + (Action("q", False),)
    table = {(a.name, h): Effect(str(rng.randrange(3)), a.program and rng.random() < 0.4)
             for a in actions for h in hs}
    compiler = CapeCompiler(hs, actions, lambda a, h: table[a, h], catalog_retry(("p0", "p1")))
    policy = compiler.compile(max_queries=len(table))
    success, calls = replay(policy, hs, table, 3)
    optimum = exhaustive_oracle(hs, actions, table, compiler.required, 3)
    assert compiler.certified
    assert (len(success), -calls) == optimum
    assert all(s["lower"] <= optimum <= s["upper"] for s in compiler.snapshots)


def test_cape_invalid_model_and_scope():
    with pytest.raises(ValueError, match="eight"):
        CapeCompiler(tuple(map(str, range(9))), (Action("p", True),), None, Policy())
    compiler = CapeCompiler(("h",), (Action("q", False), Action("p", True)),
                            lambda a, h: Effect("wrong", True), Policy("q"))
    with pytest.raises(ValueError, match="probe cannot commit"):
        compiler.compile(max_queries=2)


def test_cape_eight_configuration_boundary():
    hs, actions, table = family(count=8)
    compiler = CapeCompiler(hs, actions, lambda a, h: table[a, h],
                            catalog_retry(("p0", "p1")), call_limit=2)
    policy = compiler.compile(max_queries=len(table))
    success, calls = replay(policy, hs, table, 2)
    assert compiler.certified
    assert (len(success), -calls) == exhaustive_oracle(hs, actions, table, compiler.required, 2)
    assert len(success) == 8 and calls == 16


def test_diagnostics_are_explicitly_non_capability():
    for seed in (42, 43, 44):
        k, c = kernel_diagnostic(seed), cape_diagnostic(seed)
        assert k["diagnostic_only"] and c["diagnostic_only"]
        assert k["nodes_complete"] == k["durable_complete_nodes"] == 4
        assert k["executor_calls"] == 5 and k["parent_text_order_correct"]
        assert c["runtime_certificate"] and c["oracle_agreement"]


def test_unified_runner_contract_is_explicitly_cpu_only():
    from auto_research.agent_research import agent_kernel, cape
    for module in (agent_kernel, cape):
        assert module.REQUIRES_GPU_VALIDATION is False
        with pytest.raises(ValueError, match="CPU-only"):
            module.diagnostic(42, device="cuda")
