from dataclasses import fields, replace
import importlib.util
import itertools
import math
from pathlib import Path
import random

import numpy as np
import pytest

from auto_research.agent_research import memprice as mp, scope_replay as scope, tokenworth as tw

ROOT = Path(__file__).resolve().parents[2]


def item(key, sizes=(8, 6, 4, 2, 0), utilities=(1., .8, .6, .3, 0.)):
    return mp.Item(key, tuple(mp.Representation(level, size, utility)
        for level, (size, utility) in enumerate(zip(sizes, utilities))))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_memprice_exact_independent_exhaustive_reference(seed):
    rng = random.Random(seed)
    for _ in range(15):
        items = tuple(item(str(i), utilities=tuple(sorted([rng.random() for _ in range(4)], reverse=True))+(0.,))
                      for i in range(rng.randrange(1, 5)))
        budget, price = rng.randrange(1, 22), rng.random()*2
        path, size, objective = mp.allocate(items, capacity=budget, price=price)
        reference = max(sum(o.utility-price*o.tokens/budget for o in options)
            for options in itertools.product(*(i.options for i in items))
            if sum(o.tokens for o in options) <= budget)
        assert objective == pytest.approx(reference, abs=1e-12)
        assert size <= budget and len(path) == len(items)


def test_memprice_pressure_refresh_irreversibility_and_monotonic_repair():
    allocator = mp.MemPrice(8, target=.1, c=100)
    first = allocator.step((item("one"),))
    second = allocator.step((item("one"),))
    assert first.tokens == 8 and second.tokens == 0
    assert allocator.step((item("one"),)).tokens == 0
    queue, clock = allocator.queue, allocator.round
    allocator.refresh()
    assert allocator.queue == queue and allocator.round == clock
    # Refresh permits archived detail again, but only subject to hard capacity.
    assert mp.allocate((item("one"),), capacity=8, price=0., minimum_levels=allocator.levels)[1] == 8
    bad_order = item("repair", utilities=(.2, .8, .1, .5, 0.))
    path, _, _ = mp.allocate((bad_order,), capacity=2, price=0.)
    assert path[0][1].utility == .1


@pytest.mark.parametrize("mutation", ["duplicate", "nan", "size", "delete", "levels", "budget"])
def test_memprice_rejects_invalid_inputs(mutation):
    data, budget = (item("x"),), 8
    if mutation == "duplicate":
        data *= 2
    elif mutation == "nan":
        data = (item("x", utilities=(math.nan, .8, .6, .3, 0.)),)
    elif mutation == "size":
        data = (item("x", sizes=(1, 6, 4, 2, 0)),)
    elif mutation == "delete":
        data = (item("x", utilities=(1., .8, .6, .3, .1)),)
    elif mutation == "levels":
        data = (mp.Item("x", (mp.Representation(4, 0, 0.),)*2),)
    else:
        budget = True
    with pytest.raises(ValueError):
        mp.allocate(data, capacity=budget, price=0.)


def stateful_api(name, state, *args):
    if name == "append":
        args[0].append(args[1])
        return args[0]
    if name == "read":
        return tuple(args[0])
    if name == "raise":
        state["errors"] = state.get("errors", 0)+1
        raise KeyError("expected")
    raise ValueError("unknown API")


def stateful_program(call, state):
    assert state["left"] is state["right"]
    returned = call("append", state["left"], state["increment"])
    assert returned is state["right"]
    assert call("read", state["right"]) == tuple(state["left"])
    try:
        call("raise")
    except KeyError:
        assert state["errors"] == 1
    call("read", state["left"])


def witness():
    shared = [1]
    return scope.record(stateful_program, source="original", instance="dev-1",
        state={"left": shared, "right": shared, "increment": 4}, api=stateful_api,
        native_grader=lambda s: s["left"] == [1, 4] and s["errors"] == 1)


def test_scope_full_trace_mutation_alias_exception_and_binding():
    tape = witness()
    result = scope.certify(stateful_program, tape, candidate_source="revision", instance="dev-1")
    assert result.status == "certified" and result.matched_events == 4
    assert tape.initial["nodes"][1][1] == [["int", 1]]  # historical snapshot not mutated
    with pytest.raises(ValueError, match="different recorded instance"):
        scope.certify(stateful_program, tape, candidate_source="revision", instance="heldout-1")
    graph = scope.Graph()
    shared = []
    shared.append(shared)
    snapshot = graph.snapshot(({"a": shared, "b": shared},))
    restored, = scope.Graph().restore(snapshot)
    assert restored["a"] is restored["b"] and restored["a"][0] is restored["a"]


@pytest.mark.parametrize("kind", ["arguments", "state", "alias", "extra", "short", "caught_extra", "final_state"])
def test_scope_divergence_must_not_certify(kind):
    def changed(call, state):
        if kind == "arguments":
            return call("append", state["left"], 99)
        if kind == "state":
            state["increment"] = 5
        if kind == "alias":
            state["right"] = list(state["left"])
        if kind == "short":
            return
        stateful_program(call, state)
        if kind == "final_state":
            state["left"].clear()
        if kind in {"extra", "caught_extra"}:
            try:
                call("read", state["left"])
            except scope.Diverged:
                if kind != "caught_extra":
                    raise
    assert scope.certify(changed, witness(), candidate_source=kind, instance="dev-1").status == "diverged"


def test_scope_unsupported_objects_and_accepted_program_not_replay_gated():
    with pytest.raises(scope.Unavailable):
        scope.Graph().snapshot((np.array([1]),))
    def unsupported(call, state):
        call("read", np.array([1]))
    assert scope.certify(unsupported, witness(), candidate_source="array", instance="dev-1").status == "unavailable"
    with pytest.raises(ValueError, match="native-graded"):
        scope.record(lambda _call, _state: None, source="bad", instance="dev", state={},
                     api=stateful_api, native_grader=lambda _: False)
    accepted = scope.AcceptedPrograms("initial")
    assert accepted.observe("original", success=True, witness=witness())
    assert not accepted.observe("failed-new", success=False)
    assert accepted.accepted_source == "original" and len(accepted.witnesses) == 1
    assert accepted.observe("unsupported-but-native-success", success=True)
    assert accepted.accepted_source == "unsupported-but-native-success" and len(accepted.witnesses) == 1
    selected = scope.witness_subset((witness(),)*7, seed=42)
    assert len(selected) == 3


def test_scope_dictionary_insertion_order_is_observable_not_normalized_away():
    def api(name, state, argument):
        return next(iter(argument))
    def original(call, state):
        state["out"] = call("first", {"a": 1, "b": 2})
    def reordered(call, state):
        state["out"] = call("first", {"b": 2, "a": 1})
    tape = scope.record(original, source="original", instance="ordered-dict", state={},
                        api=api, native_grader=lambda state: state["out"] == "a")
    assert scope.certify(original, tape, candidate_source="same", instance="ordered-dict").status == "certified"
    assert scope.certify(reordered, tape, candidate_source="reordered", instance="ordered-dict").status == "diverged"


def test_scope_signed_zero_and_tuple_alias_are_behavior_relevant():
    def api(name, state, *arguments):
        if name == "sign":
            return math.copysign(1., arguments[0])
        return arguments[0] is arguments[1]
    def positive(call, state):
        state["out"] = call("sign", 0.)
    def negative(call, state):
        state["out"] = call("sign", -0.)
    tape = scope.record(positive, source="positive", instance="signed-zero", state={},
                        api=api, native_grader=lambda state: state["out"] == 1.)
    assert scope.certify(negative, tape, candidate_source="negative", instance="signed-zero").status == "diverged"
    def alias(call, state):
        value = tuple([1, 2])
        state["out"] = call("identity", value, value)
    def separate(call, state):
        state["out"] = call("identity", tuple([1, 2]), tuple([1, 2]))
    tape = scope.record(alias, source="alias", instance="tuple-alias", state={},
                        api=api, native_grader=lambda state: state["out"] is True)
    assert scope.certify(alias, tape, candidate_source="same", instance="tuple-alias").status == "certified"
    assert scope.certify(separate, tape, candidate_source="separate", instance="tuple-alias").status == "diverged"
    mutable = []
    value = (mutable,)
    mutable.append(value)
    restored, = scope.Graph().restore(scope.Graph().snapshot((value,)))
    assert restored[0][0] is restored


def test_tokenworth_logistic_newton_independent_stationarity_and_bounds():
    rng = np.random.default_rng(42)
    x = rng.normal(size=(40, 4))
    labels = np.where(x[:, 1] > 0, 1., -1.)
    updated = tw.fit_base(x, labels)
    assert tw.logistic_loss(updated, x, labels) < tw.logistic_loss(tw.PRIOR, x, labels)
    assert np.all(updated >= 0) and np.all(updated <= [2., 1., 1., 1.])
    assert np.array_equal(tw.vector("A memory"), tw.vector("A memory"))
    assert np.linalg.norm(tw.vector("A memory")) == pytest.approx(1.)
    assert not tw.vector("").any()


def test_tokenworth_krr_scalar_reference_and_finite_difference_agop():
    x = np.array([[.1, .3], [.5, -.4], [1., .2]])
    y = np.array([1., -.8, .2])
    rfm = tw.ResidualRFM(2)
    rfm.metric = np.array([.7, 1.3])
    rfm.fit(x, y)
    gram = np.array([[math.exp(-math.sqrt(sum(rfm.metric[k]*(a[k]-b[k])**2
        for k in range(2)))) for b in x] for a in x])
    alpha = np.linalg.solve(gram+.01*np.eye(3), y)
    assert np.max(np.abs(rfm.coefficients-alpha)) < 1e-12
    q = np.array([[.2, -.1], [.7, .8]])
    finite = np.zeros_like(q)
    for i in range(2):
        step = np.zeros_like(q)
        step[:, i] = 1e-6
        finite[:, i] = (rfm.predict(q+step)-rfm.predict(q-step))/(2e-6)
    assert np.max(np.abs(finite-rfm.gradients(q))) < 1e-6
    original = rfm.metric.copy()
    expected = np.clip(.75*original+.25*np.mean(finite**2, axis=0), .05, 8.)
    expected /= expected.mean()
    rfm.adapt(q, x, y)
    assert rfm.metric == pytest.approx(expected, abs=1e-7)
    assert rfm.fits == 2 and not np.array_equal(original, rfm.metric)


def test_tokenworth_gates_self_eviction_positive_ratio_and_nearest_fallback():
    a, b = tw.Memory("a", "same", 0), tw.Memory("b", "same", 1)
    retained, reason = tw.admission_decision((a,), b, ("q",), score=lambda q, m: 1., capacity=1)
    assert reason == "reject" and retained == (a,)
    a.utility = 0.
    retained, reason = tw.admission_decision((a,), b, ("q",),
        score=lambda q, m: -.8 if m.key == "a" else -.6, capacity=1)
    assert reason == "replace_nearest" and retained == (b,)
    novel = tw.Memory("novel", "completely different 12345", 1)
    retained, reason = tw.admission_decision((a,), novel, ("q",),
        score=lambda q, m: 1. if m.key == "a" else -1., capacity=1)
    assert reason == "candidate_self_evicted" and retained == (a,)
    retained, reason = tw.admission_decision((a,), b, ("q1", "q2", "q3"),
        score=lambda q, m: -1. if m.key == "a" else (3. if q == "q1" else -.1), capacity=1)
    # Positive mean beats the best, but 1/3 positive probes fails rho >= .45;
    # fallback replacement still applies because the nearest utility is low.
    assert reason == "replace_nearest"
    a.utility = 1.
    retained, reason = tw.admission_decision((a,), b, ("q1", "q2", "q3"),
        score=lambda q, m: -1. if m.key == "a" else (3. if q == "q1" else -.1), capacity=1)
    assert reason == "reject" and retained == (a,)  # rho+, not relative win ratio
    best = tw.Memory("best", "same", 0)
    retained, reason = tw.admission_decision((a, best), b, ("q",),
        score=lambda q, m: {"a": 1., "best": 2., "b": 1.5}[m.key], capacity=2)
    assert reason == "reject" and retained == (a, best)  # compare best, not nearest


def test_tokenworth_selected_only_feedback_chronology_windows_and_no_gold():
    controller = tw.TokenWorth(capacity=2, dimension=16, base_interval=2,
                              krr_interval=2, agop_interval=4, warmup=2)
    view = controller.begin("public task")
    assert not {"gold", "answer", "reward", "reference"} & {field.name for field in fields(view)}
    with pytest.raises(ValueError, match="previous"):
        controller.begin("future task")
    with pytest.raises(ValueError):
        controller.finish(False, new_memory=("x", "private reference"))
    controller.finish(True, new_memory=("a", "public successful trajectory"))
    assert controller.feedback == 0
    for index in range(8):
        controller.begin(f"public trajectory {index}")
        controller.finish(index % 2 == 0)
    memory = controller.bank["a"]
    assert controller.feedback == 8 == memory.hits+memory.misses
    assert memory.hits == memory.misses == 4 and memory.utility == pytest.approx(.2)
    assert controller.rfm.fits == 6 and np.mean(controller.rfm.metric) == pytest.approx(1.)
    with pytest.raises(ValueError):
        controller.finish(True)


def test_tokenworth_default_schedule_uses_feedback_not_tasks_and_bounded_fifos():
    controller = tw.TokenWorth(dimension=8)
    controller.begin("cold start")
    controller.finish(True, new_memory=("only", "public complete action"))
    for t in range(270):
        controller.begin(f"public {t % 3}")
        controller.finish(t % 3 == 0)
        if t == 3:
            assert controller.rfm.fits == 0  # warmup does not trigger off-schedule fit
    assert len(controller.base) == len(controller.slow) == 256
    assert len(controller.fast) == 128 and controller.feedback == 270
    assert controller.rfm.fits == 6  # scheduled 50...250 plus 200 AGOP refit


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_tokenworth_rejects_nonfinite_learning_inputs(bad):
    with pytest.raises(ValueError):
        tw.fit_base([[1., bad, .5, .3]], [1.])
    with pytest.raises(ValueError):
        tw.ResidualRFM(2).fit([[1., bad]], [1.])
    with pytest.raises(ValueError):
        tw.laplacian([[1., 2.]], [[1., 2.]], [1., bad])


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_runner_mechanisms_and_controls(seed):
    spec = importlib.util.spec_from_file_location("oct20_agent_runner", ROOT/"scripts/run_oct20_agent_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = {key: function(seed) for key, function in module.FUNCTIONS.items()}
    assert rows["memprice"]["metrics"]["maximum_objective_reference_error"] < 1e-10
    assert rows["memprice"]["metrics"]["greedy_negative_control_gap"] > 0
    assert rows["scope-replay"]["metrics"]["false_certificates_under_faults"] == 0
    assert rows["scope-replay"]["metrics"]["broken_replay_negative_control_failures"] > 0
    assert rows["tokenworth"]["metrics"]["maximum_kernel_reference_error"] < 1e-10
    assert rows["tokenworth"]["metrics"]["gradient_finite_difference_error"] < 1e-5
    assert rows["tokenworth"]["metrics"]["fit_updates"] > 0
    for row in rows.values():
        assert len(row["fixture_sha256"]) == 64
        assert all(type(v) in (int, float, bool) and math.isfinite(v) for v in row["metrics"].values())
