import itertools
import hashlib
import json
import math
from pathlib import Path

import pytest

from auto_research.agent_research import ooas, transport_safe_audit as audit


def test_ftrl_kkt_uniform_translation_and_not_softmax():
    assert ooas.ftrl_distribution((0., 0., 0.), 3., 6.) == pytest.approx((1/3,)*3)
    scores = (-2., 1., 4.)
    p = ooas.ftrl_distribution(scores, 2., 5.)
    kkt = [g+2/math.sqrt(x)+5/x for g, x in zip(scores, p)]
    assert max(kkt)-min(kkt) < 1e-10
    assert p == pytest.approx(ooas.ftrl_distribution(tuple(x+100 for x in scores), 2., 5.))
    assert p[2] > p[1] > p[0] > 0
    assert p[2]/p[1] != pytest.approx(math.exp(3))


def test_regularizer_and_potential_duality():
    assert ooas.regularizer((.5, .5), 2, 6) == pytest.approx(0)
    p = ooas.ftrl_distribution((1., -1.), 2., 6.)
    optimum = ooas.potential((1., -1.), 2., 6.)
    assert optimum == pytest.approx(p[0]-p[1]-ooas.regularizer(p, 2., 6.))
    for x in (.1, .3, .5, .7, .9):
        assert optimum >= 2*x-1-ooas.regularizer((x, 1-x), 2., 6.)-1e-12


def test_shared_noise_constant_arm_event_not_product_of_marginals():
    path = ((.3, .7), (.8, .2))
    rho = ooas.constant_arm_probabilities(path)
    assert rho == pytest.approx((.3, .2))
    assert rho[0] != pytest.approx(.3*.8)
    hints = ((.1, .2), (.3, .4))
    actual = ((.8, .5), (.9, .6))
    truth = tuple(sum(row[k]-hint[k] for row, hint in zip(actual, hints)) for k in (0, 1))
    # Analytic partition: armk wins both turns with probability rho_k.
    for k in (0, 1):
        reward = sum(row[k] for row in actual)
        mass, correction, residual, probability = ooas.aggregate_residual(hints, path, (k, k), reward)
        assert rho[k]*correction[k] == pytest.approx(truth[k])
        assert correction[1-k] == 0
        assert residual == pytest.approx(truth[k]) and probability == pytest.approx(rho)
        assert mass == pytest.approx((.4, .6))
    assert ooas.aggregate_residual(hints, path, (0, 1), 1.4)[1] == (0., 0.)


def test_task_state_provisional_hints_and_length_bound():
    learner = ooas.OptimisticSteering(2, 2, seed=3, alpha=2.)
    with pytest.raises(ValueError):
        learner.choose((.2, .8))
    learner.begin(noise=(1., 1.))
    with pytest.raises(ValueError):
        learner.begin()
    _, p0 = learner.choose((.2, .8))
    _, p1 = learner.choose((.8, .2))
    assert p0 == pytest.approx(ooas.ftrl_distribution((.2, .8), 2., 12.))
    assert p1 == pytest.approx(ooas.ftrl_distribution((1.8, 1.2), 2., 12.))
    with pytest.raises(ValueError):
        learner.choose((.5, .5))
    with pytest.raises(ValueError):
        learner.finish(3)
    assert learner._active  # failed validation does not lose pending task.
    learner.finish(1.)
    with pytest.raises(ValueError):
        learner.finish(1.)


def test_adaptive_signed_gap_is_not_clipped_and_restart_is_strict():
    def prepare():
        result = ooas.OptimisticSteering(2, 1)
        result.begin(noise=(.1, 2.))
        result.choose((0., 0.))
        return result
    trial = prepare()
    gap = trial.finish(1.)["gap"]
    assert gap > 0
    learner = prepare()
    learner.signed_gap = learner.threshold-gap/2
    previous = learner.threshold
    assert learner.finish(1.)["restart"]
    assert learner.threshold == 2*previous and learner.score == (0., 0.) and learner.signed_gap == 0
    control = ooas.OptimisticSteering(3, 4, seed=42)
    control.begin()
    chosen = [control.choose(hint)[0] for hint in ((.8, .2, .4), (.7, .3, .5), (.9, .1, .4))]
    trace = control.finish(sum((.9, .1, .5)[k] for k in chosen))
    assert trace["gap"] < 0 and control.signed_gap == trace["gap"]


@pytest.mark.parametrize("call", [
    lambda: ooas.ftrl_distribution((1.,), 1, 1),
    lambda: ooas.ftrl_distribution((1., 2.), 0, 1),
    lambda: ooas.ftrl_distribution((1e308, -1e308), 1, 1),
    lambda: ooas.constant_arm_probabilities(((0., 1.),)),
    lambda: ooas.aggregate_residual(((.1, .2),), ((.5, .5),), (True,), 1),
    lambda: ooas.aggregate_residual(((.1, 1.2),), ((.5, .5),), (0,), 1),
    lambda: ooas.OptimisticSteering(2, 0),
])
def test_ooas_bad_inputs_fail_closed(call):
    with pytest.raises(ValueError):
        call()


def test_aipw_exact_design_enumeration_and_no_clipping():
    predictions = (audit.CrossFitPrediction(.2, "a", frozenset({"b"})),
                   audit.CrossFitPrediction(.9, "b", frozenset({"a"})))
    expectation = 0
    for flags in itertools.product((0, 1), repeat=2):
        probability = math.prod((.25 if flag else .75) for flag in flags)
        labels = tuple(y if flag else None for y, flag in zip((0, 1), flags))
        expectation += probability*audit.aipw_estimate(predictions, (.25, .25), labels, positivity_floor=.1)
    assert expectation == pytest.approx(.5)
    high = audit.aipw_estimate((audit.CrossFitPrediction(0., "a", frozenset()),), (.1,), (1,), positivity_floor=.1)
    assert high == 10.  # clipping this to1 would break design-unbiasedness.
    with pytest.raises(ValueError):
        audit.CrossFitPrediction(.5, "a", frozenset({"a"}))


def test_allocation_kkt_budget_floor_cap_and_zero_variance_strata():
    prediction, weights = (.0, .1, .5, .9), (.1, .2, .5, .2)
    p = audit.bounded_allocation(prediction, weights, mean_budget=.4, positivity_floor=.1)
    assert p[0] == .1 and min(p) >= .1 and max(p) <= 1
    assert sum(x*w for x, w in zip(p, weights)) == pytest.approx(.4)
    assert p[1] == pytest.approx(p[3])
    assert p[2] > p[1]
    assert audit.bounded_allocation((0., 1.), (.5, .5), mean_budget=.1, positivity_floor=.1) == (.1, .1)
    with pytest.raises(ValueError):
        audit.bounded_allocation((0., 1.), (.5, .5), mean_budget=.2, positivity_floor=.1)


def test_eprocess_matches_direct_products_and_requires_plan_before_label():
    process = audit.HedgedAuditProcess(audit.FrozenTarget("stable"), (.2, .5, .8), (.05, .1), positivity_floor=.2)
    labels = (1, 0, 1, 1)
    with pytest.raises(ValueError):
        process.observe(1)
    for label in labels:
        assert process.plan(.3, 1., target_identity="stable")
        with pytest.raises(ValueError):
            process.plan(.3, 1., target_identity="stable")
        process.observe(label)
    for theta, log_e in zip(process.theta, process.log_evalues()):
        direct = sum(math.prod(1+sign*lam*(label-theta) for label in labels)
                     for lam in (.05, .1) for sign in (1, -1))/4
        assert math.exp(log_e) == pytest.approx(direct)
    assert process.count == 4
    with pytest.raises(ValueError):
        process.plan(.3, 1., target_identity="updated-agent")


def test_unobserved_labels_cannot_enter_eprocess_and_still_increment_count():
    process = audit.HedgedAuditProcess(audit.FrozenTarget("stable"), (.5,), (.05,), positivity_floor=.1, seed=0)
    assert not process.plan(.4, .1, target_identity="stable")
    with pytest.raises(ValueError):
        process.observe(1)
    process.observe(None)
    assert process.count == 1 and math.isfinite(process.log_evalues()[0])


def test_log_space_handles_long_stream_without_product_overflow():
    process = audit.HedgedAuditProcess(audit.FrozenTarget("stable"), (0., .5, 1.), (.5,), positivity_floor=.6)
    for _ in range(2000):
        process.plan(.5, 1., target_identity="stable")
        process.observe(1)
    assert all(math.isfinite(x) for x in process.log_evalues())
    assert process.log_evalues()[0] > 700
    assert 0. not in process.accepted_grid()


def test_rank_sets_use_strict_interval_separation_and_preserve_ties():
    assert audit.robust_rank_sets({"a": (.5, .7), "b": (.3, .5)}) == {"a": (1, 2), "b": (1, 2)}
    assert audit.robust_rank_sets({"a": (.6, .7), "b": (.3, .5), "c": (.3, .5)}) == {"a": (1, 1), "b": (2, 3), "c": (2, 3)}
    assert audit.support_outer_set(.445, .2) == (.445, .645)
    with pytest.raises(ValueError):
        audit.support_outer_set(.9, .2)


@pytest.mark.parametrize("call", [
    lambda: audit.FrozenTarget("x", agent_frozen=False),
    lambda: audit.FrozenTarget("x", independently_drawn_tasks=False),
    lambda: audit.HedgedAuditProcess(audit.FrozenTarget("x"), (.5,), (.1,), positivity_floor=.1),
    lambda: audit.HedgedAuditProcess(audit.FrozenTarget("x"), (.5, .5), (.01,), positivity_floor=.1),
    lambda: audit.transport_bias(.5, .5, .5, .8, .8),
    lambda: audit.aipw_estimate((audit.CrossFitPrediction(.5, "a", frozenset()),), (.01,), (1,), positivity_floor=.1),
    lambda: audit.aipw_estimate((audit.CrossFitPrediction(.5, "a", frozenset()),), (.5,), (True,), positivity_floor=.1),
])
def test_audit_invalid_contracts_rejected(call):
    with pytest.raises(ValueError):
        call()


@pytest.mark.parametrize("module", [ooas, audit])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_bounded_cpu_diagnostic_contract(module, seed):
    result = module.diagnostic(seed, "cpu")
    assert module.REQUIRES_GPU_VALIDATION is False
    assert result["diagnostic_only"] and result["evaluation_tier"] == "l1_mechanism"
    assert all(type(x) is bool and x for x in result["checks"].values())
    assert all(type(x) in (int, float) and math.isfinite(x) for x in result["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")


def test_agent_paper_metadata_translation_figures_and_four_level_questions():
    root = Path(__file__).resolve().parents[1]
    audit_path = root/"docs/research-audits/nov24-latest"
    proposals = json.loads((audit_path/"paper-proposals-agent.json").read_text())["papers"]
    bundle = json.loads((audit_path/"agent-authored-bundle.json").read_text())
    assert set(proposals) == {"agent-research:ooas", "agent-research:transport-safe-audit", "agent-research:morse"}
    assert len(bundle["english_question_units"]) == 12
    for identity, spec in proposals.items():
        page = root/"docs"/spec["detail_path"]
        source = page.read_bytes()
        source_text = source.decode()
        translation = page.with_name("README-en.md").read_text()
        assert f"<!-- source-sha256: {hashlib.sha256(source).hexdigest()} -->" in translation
        assert "[简体中文](README.md)" in translation
        assert all(name in source_text for name in ("论文链接", "公司/机构/学校", "首次公开日期", "原作者开源代码", "本地 Adapter", "本地复现代码目录"))
        assert spec["published"] == "2026-11-23" and spec["discovered_on"] == "2026-11-24"
        assert spec["announced_on"] is None and spec["adapter"] is None
        assert spec["requires_gpu_validation"] is False and spec["automatic_retry"] is False
        questions = bundle["papers"][identity]["questions"]
        assert {row["level"] for row in questions} == {"basics", "mechanism", "comparison", "implementation"}
        for row in questions:
            assert all(f"### {heading}" in source_text for heading in row["source_sections"])
            assert f"qa/{identity}/{row['id']}" in bundle["english_question_units"]
        provenance = json.loads((page.parent/"assets/provenance.json").read_text())["figures"][0]
        assert provenance["visual_review_done"] and provenance["caption_included"]
        assert provenance["scientific_content_modified"] is False
        assert hashlib.sha256((page.parent/"assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["image_sha256"]
    assert proposals["agent-research:morse"]["component_implemented"] is False
    assert proposals["agent-research:morse"]["local_operator"] is None
