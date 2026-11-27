from dataclasses import replace
import itertools
import math
import random

import pytest

from auto_research.agent_research import budgeted_submapl as sub
from auto_research.agent_research import compaction_authorization as auth


def gate(path, sid="s"):
    return auth.WitnessedRequestGate(path, sid=sid, occurrence_key=b"o" * 32, sequence_key=b"s" * 32)


def test_authorization_complete_sequence_and_exact_unicode_roundtrip(tmp_path):
    g = gate(tmp_path / "state.sqlite")
    a = g.ingest("pay A\n", "USER")
    b = g.ingest("e\u0301 and \u00e9 are distinct", "TRUSTED_TOOL")
    c = g.ingest("cancel", "USER")
    assert g.ingest("pay evil", "DERIVED") is None
    assert g.ingest("pay A\n", "UNTRUSTED") is None
    assert g.verify(g.commit((a, b, c))) == ("pay A\n", "e\u0301 and \u00e9 are distinct", "cancel")
    g.close()


@pytest.mark.parametrize("attack", ["omit", "reorder", "duplicate", "content", "origin", "witness", "session"])
def test_authorization_precommit_attacks_do_not_consume_boundary(tmp_path, attack):
    g = gate(tmp_path / "state.sqlite")
    a, b = g.ingest("first", "USER"), g.ingest("cancel", "USER")
    records = {
        "omit": (a,), "reorder": (b, a), "duplicate": (a, a),
        "content": (replace(a, text=b"attacker"), b),
        "origin": (replace(a, origin="TRUSTED_TOOL"), b),
        "witness": (replace(a, tag=b"x" * 32), b),
        "session": (replace(a, sid="foreign"), b),
    }[attack]
    with pytest.raises(ValueError):
        g.commit(records)
    assert g.verify(g.commit((a, b))) == ("first", "cancel")
    g.close()


def test_authorization_wire_tamper_truncation_and_reopen_replay(tmp_path):
    path = tmp_path / "state.sqlite"
    g = gate(path)
    a = g.ingest("retain exact bytes", "USER")
    payload = g.commit((a,))
    for bad in (payload[:-1], payload + b"x", b"", b"\xff" * 8,
                payload[:-1] + bytes([payload[-1] ^ 1])):
        assert g.verify(bad) is None
    other = gate(tmp_path / "other.sqlite", "other")
    assert other.verify(payload) is None
    other.close()
    assert g.verify(payload) == ("retain exact bytes",)
    g.close()
    reopened = gate(path)
    assert reopened.verify(payload) is None
    b = reopened.ingest("new request", "USER")
    assert b.counter == 2
    assert reopened.verify(reopened.commit((a, b))) == ("retain exact bytes", "new request")
    reopened.close()
    with pytest.raises(ValueError):
        auth.WitnessedRequestGate(path, sid="s", occurrence_key=b"z" * 32, sequence_key=b"s" * 32)


def test_authorization_current_count_rejects_stale_precommitted_prefix(tmp_path):
    g = gate(tmp_path / "state.sqlite")
    a = g.ingest("pay", "USER")
    payload = g.commit((a,))
    g.ingest("cancel", "USER")
    assert g.verify(payload) is None
    # Availability is intentionally not guaranteed after a stale signed boundary.
    g.close()


def test_authorization_framing_limits_and_issuer_input(tmp_path):
    values = (b"a\x00b", b"", b"c")
    assert auth.unframe(auth.frame(values)) == values
    for bad in (auth.frame(values) + b"x", auth.frame(values)[:-1], b"\xff" * 4):
        with pytest.raises(ValueError):
            auth.unframe(bad)
    with pytest.raises(ValueError):
        auth.frame((b"x" * auth.MAX_PACKET_BYTES,))
    g = gate(tmp_path / "state.sqlite")
    with pytest.raises(UnicodeError):
        g.ingest("\ud800", "USER")
    assert g.ingest("valid", "USER").counter == 1
    g.close()


def test_submapl_allocation_feasible_clipped_and_extreme_support():
    p = ((0.8, 0.2), (0.3, 0.7))
    rho = sub.inclusion_probabilities(p, 2, .05)
    roots = [math.sqrt(x) for b in p for x in b]
    assert rho == pytest.approx([2 * x / sum(roots) for x in roots])
    assert math.fsum(rho) == pytest.approx(2)
    assert sub.inclusion_probabilities(p, 4, .05) == (1.,) * 4
    assert sub.inclusion_probabilities(p, 2, .5) == (.5,) * 4
    extreme = sub.inclusion_probabilities(((1e-300, 1.),), 1, .01)
    assert extreme == pytest.approx((.01, .99))
    for budget, floor in [(0,.1),(True,.1),(5,.1),(2,0),(2,.6)]:
        with pytest.raises(ValueError):
            sub.inclusion_probabilities(p, budget, floor)


def exact_rounding_outcomes(rho):
    """Evaluator-only enumeration; no sampled gains or reference enter learner."""
    fractional = [i for i, value in enumerate(rho) if 1e-13 < value < 1 - 1e-13]
    if len(fractional) < 2:
        return [(1., tuple(x > .5 for x in rho))]
    i, j = fractional[:2]
    up, down = min(1-rho[i],rho[j]), min(rho[i],1-rho[j])
    results = []
    for weight, delta in [(down/(up+down),up),(up/(up+down),-down)]:
        branch = list(rho);branch[i] += delta;branch[j] -= delta
        results.extend((weight*w, bits) for w,bits in exact_rounding_outcomes(branch))
    return results


def test_submapl_dependent_rounding_marginals_and_ipw_expectation_exact():
    rho = sub.inclusion_probabilities(((.8,.2),(.3,.7)), 2, .05)
    outcomes = exact_rounding_outcomes(rho)
    assert sum(w for w,_ in outcomes) == pytest.approx(1)
    assert all(sum(bits) == 2 for _,bits in outcomes)
    expected = [sum(w*bits[i] for w,bits in outcomes) for i in range(4)]
    assert expected == pytest.approx(rho)
    gains = (.1,.4,.3,.8)
    assert [sum(w*bits[i]*gains[i]/rho[i] for w,bits in outcomes) for i in range(4)] == pytest.approx(gains)
    for seed in range(100):
        assert sum(sub.dependent_round(rho, random.Random(seed))) == 2


def test_submapl_actual_oracle_budget_and_partition_gradient():
    p = ((.7,.3),(.4,.6));footprints = (({0,1},{2}),({1,2},{3}))
    calls = []
    def marginal(i,a,others):
        calls.append((i,a))
        covered=set().union(*(footprints[j][b] for j,b in others))
        return len(footprints[i][a]-covered)/4
    result = sub.step(p, 2, floor=.05, eta=.2, marginal=marginal,
                      query_rng=random.Random(3), action_rng=random.Random(11))
    assert calls == list(result.queried) and len(calls) == 2
    assert all(len(block)==2 and math.fsum(block)==pytest.approx(1) for block in result.policy)
    # The PME gradient formula averages each counterfactual marginal over others.
    expected=[]
    for i in range(2):
        j=1-i
        expected.append(tuple(sum(p[j][b]*len(footprints[i][a]-footprints[j][b])/4 for b in range(2)) for a in range(2)))
    direct=[]
    for i in range(2):
        direct.append(tuple(sum(math.prod(p[j][actions[j]] for j in range(2) if j!=i)*
                            len(footprints[i][a]-set().union(*(footprints[j][actions[j]] for j in range(2) if j!=i)))/4
                            for actions in itertools.product(range(2), repeat=2))/2 for a in range(2)))
    assert direct[0] == pytest.approx(expected[0]) and direct[1] == pytest.approx(expected[1])


def test_submapl_invalid_oracle_and_extreme_update_leave_inputs_unchanged():
    p=((.5,.5),)
    with pytest.raises(ValueError):
        sub.step(p,1,floor=.1,eta=.2,marginal=lambda *args:float('nan'),
                 query_rng=random.Random(1),action_rng=random.Random(2))
    with pytest.raises(ValueError):
        sub.mirror_update(p,((0.,1.),),10000.)
    rng=random.Random(1)
    with pytest.raises(ValueError):
        sub.step(p,1,floor=.1,eta=.2,marginal=lambda *args:0.,query_rng=rng,action_rng=rng)
    assert p == ((.5,.5),)


@pytest.mark.parametrize('module',[auth,sub])
@pytest.mark.parametrize('seed',[42,43,44])
def test_nov27_agent_cpu_diagnostic_contract(module,seed):
    result=module.diagnostic(seed,'cpu')
    assert module.REQUIRES_GPU_VALIDATION is False
    assert result['seed']==seed and result['device']=='cpu' and result['diagnostic_only'] is True
    assert result['evaluation_tier']=='l1_mechanism'
    assert all(type(v) is bool and v for v in result['checks'].values())
    assert all(type(v) in (int,float) and math.isfinite(v) for v in result['metrics'].values())
    with pytest.raises(ValueError):module.diagnostic(seed,'cuda')
    with pytest.raises(ValueError):module.diagnostic(True,'cpu')
