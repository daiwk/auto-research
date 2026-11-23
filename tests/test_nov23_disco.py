from dataclasses import FrozenInstanceError, asdict
import itertools
import json
import math
from hashlib import sha256
from pathlib import Path

import pytest

from auto_research.foundation_models.disco import (
    Disco, diagnostic, exact_null_calibration, log_p_to_e, weighted_ebh,
)


def test_p_to_e_formula_endpoints_and_log_scale():
    assert math.exp(log_p_to_e(.01)) == pytest.approx(5.)
    assert log_p_to_e(1.) == pytest.approx(math.log(.5))
    assert log_p_to_e(0.) == math.inf
    assert math.isfinite(log_p_to_e(1e-300))


def test_weighted_ebh_uses_largest_satisfying_rank_not_first_failure():
    # At alpha=1, rank1 fails (2.5<3), while rank2 satisfies 2*2>=3.
    assert weighted_ebh({"a": 2.5, "b": 2., "c": 0.}, alpha=1.) == ("a", "b")
    assert weighted_ebh({"a": 100., "b": 4., "c": 1.}, alpha=.1) == ("a",)
    assert weighted_ebh({"a": math.inf}, alpha=0.) == ()
    assert weighted_ebh({}, alpha=.1) == ()
    assert weighted_ebh({"a": 2., "b": 2.}, alpha=1.) == ("a", "b")
    with pytest.raises(ValueError):
        weighted_ebh({"a": 1., "b": 1.}, k_bar=1)


def test_exact_null_moments_include_survival_conditioning_and_first_exit():
    calibration = exact_null_calibration(((.01, .01), (1., .99)), e_max=3., n_max=2)
    assert calibration.exit_probabilities == pytest.approx((.01, .01))
    assert calibration.active_means == pytest.approx((.5, .2725))
    assert calibration.epsilon == pytest.approx(.5)
    assert calibration.exact_path_enumeration


def test_coarse_selector_view_hides_exact_evidence_and_is_immutable():
    a, b = Disco(), Disco()
    a.observe("h", .04)
    b.observe("h", .0625)
    assert a.selector_view() == b.selector_view()
    view = a.selector_view()[0]
    assert set(asdict(view)) == {"name", "updates", "bin_history", "frozen"}
    with pytest.raises(FrozenInstanceError):
        view.updates = 100
    assert view.bin_history == ("A",)


def test_freezing_is_inclusive_at_exit_and_at_round_limit():
    state = Disco(e_max=5., n_max=2)
    state.observe("exit", .01)
    state.observe("limit", 1.)
    state.observe("limit", 1.)
    assert all(row.frozen for row in state.selector_view())
    assert state.selector_view()[0].bin_history == ("H",)
    assert state.selector_view()[1].bin_history == ("A", "A")
    for name in ("exit", "limit"):
        with pytest.raises(ValueError):
            state.observe(name, .01)
    below = Disco(e_max=5.)
    below.observe("below", .01000001)
    assert not below.selector_view()[0].frozen


def test_invalid_selector_does_not_trigger_external_provider_call():
    state = Disco(e_max=5.)
    state.observe("h", .01)
    provider_calls = []
    with pytest.raises(ValueError):
        state.run(lambda _: "h", lambda *args: provider_calls.append(args))
    assert provider_calls == []


def test_query_budget_uses_actual_partial_final_batch():
    state = Disco(query_budget=5, batch_size=3, n_max=2)
    allocations = []

    def provider(name, batch):
        allocations.append(batch)
        return 1.

    state.run(lambda _: "h", provider)
    assert allocations == [3, 2] and state.queries_used == 5
    with pytest.raises(ValueError):
        state.observe("another", .01)
    with pytest.raises(ValueError):
        Disco(batch_size=3).observe("h", .01, queries=1)


def test_pre_hoc_uses_deterministic_upper_count_and_corrected_alpha():
    calibration = exact_null_calibration(((.01, .01), (1., .99)), e_max=3., n_max=2)
    state = Disco(e_max=3., n_max=2, query_budget=2)
    state.observe("h", 1.)
    result = state.finish(calibration, alpha=.1)
    certificate = result["certificate"]
    assert certificate["epsilon"] == pytest.approx(.5)
    assert certificate["delta"] == pytest.approx(.02)  # K_bar=2, not K_obs=1.
    assert certificate["alpha_star"] == pytest.approx(.16)
    assert certificate["bound"] == pytest.approx(.1)
    assert not certificate["conditional_on_no_null_exit"]


def test_post_hoc_is_explicitly_conditional_not_alpha_minus_delta():
    calibration = exact_null_calibration(((.01, .01), (1., .99)), e_max=3., n_max=2)
    state = Disco(e_max=3., n_max=2, query_budget=3)
    state.observe("exit", .01)
    state.observe("active", 1.)
    state.observe("active", 1.)
    result = state.finish(calibration, alpha=.1, mode="post_hoc")
    certificate = result["certificate"]
    assert certificate["epsilon"] == pytest.approx(.2725 / 2)
    assert certificate["delta"] == pytest.approx(.02)
    assert certificate["alpha_star"] == pytest.approx(.1 / (.2725 / 2))
    assert certificate["bound"] == pytest.approx(.1)
    assert certificate["conditional_on_no_null_exit"]
    with pytest.raises(ValueError):
        state.observe("future", .01)
    with pytest.raises(ValueError):
        state.finish(calibration)
    provider_calls = []
    with pytest.raises(ValueError):
        state.run(lambda _: "future", lambda *args: provider_calls.append(args))
    assert provider_calls == []


def test_small_exact_all_null_adaptive_pool_has_bounded_fdr():
    # Four exact independent null paths, not a real-model capability experiment.
    law = ((.0001, .0001), (1., .9999))
    calibration = exact_null_calibration(law, e_max=2., n_max=1)
    fdr = 0.
    observed_counts = set()
    for (p0, mass0), (p1, mass1) in itertools.product(law, repeat=2):
        state = Disco(e_max=2., n_max=1, query_budget=2)

        def selector(views):
            if not views:
                return "h0"
            if len(views) == 1 and views[0].bin_history[-1] == "H":
                return "h1"
            return None

        state.run(selector, lambda name, _: p0 if name == "h0" else p1)
        result = state.finish(calibration, alpha=.2)
        observed_counts.add(result["hypotheses"])
        fdr += mass0 * mass1 * bool(result["rejected"])
    assert observed_counts == {1, 2}
    assert 0 < fdr <= .2


def test_infinite_log_evidence_and_empty_pool_are_well_defined():
    calibration = exact_null_calibration(((1., 1.),), e_max=5., n_max=1)
    state = Disco(e_max=5., n_max=1)
    state.observe("h", 0.)
    assert state.finish(calibration)["rejected"] == ["h"]
    empty = Disco(e_max=5., n_max=1).finish(calibration, mode="post_hoc")
    assert empty["rejected"] == [] and empty["certificate"]["epsilon"] == 0.


@pytest.mark.parametrize("kwargs", [{"kappa": 0.}, {"kappa": 1.}, {"e_max": 1.},
    {"n_max": True}, {"query_budget": 0}, {"batch_size": 0}, {"kappa": math.nan}])
def test_invalid_configuration_rejected(kwargs):
    with pytest.raises(ValueError):
        Disco(**kwargs)


@pytest.mark.parametrize("p", [-.1, 1.1, math.nan, math.inf, True, None])
def test_invalid_p_does_not_mutate_state(p):
    state = Disco()
    with pytest.raises(ValueError):
        state.observe("h", p)
    assert state.selector_view() == () and state.queries_used == 0


@pytest.mark.parametrize("pmf", [((.01, .5), (1., .5)), ((.5, .2),),
    ((0., .01), (1., .99)), ((1., -1.),), ()])
def test_invalid_null_law_rejected(pmf):
    with pytest.raises(ValueError):
        exact_null_calibration(pmf)


def test_exact_enumeration_budget_and_calibration_mismatch_fail_closed():
    with pytest.raises(ValueError):
        exact_null_calibration(((.5, .5), (1., .5)), n_max=20, max_paths=100)
    wrong = exact_null_calibration(((1., 1.),), e_max=5.)
    with pytest.raises(ValueError):
        Disco().finish(wrong)


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_contract(seed):
    result = diagnostic(seed)
    assert result["evaluation_tier"] == "l1_mechanism" and result["diagnostic_only"]
    assert result["checks"] == result["controls"] and all(result["checks"].values())
    assert all(math.isfinite(value) for value in result["metrics"].values())
    with pytest.raises(ValueError):
        diagnostic(seed, "cuda")


def test_paper_metadata_and_reviewed_bilingual_source_are_complete():
    root = Path(__file__).resolve().parents[1]
    directory = root / "docs/foundation-models/2611.27104-disco"
    cn = (directory / "README.md").read_bytes()
    en = (directory / "README-en.md").read_text()
    assert f"<!-- source-sha256: {sha256(cn).hexdigest()} -->" in en
    for text in (cn.decode(), en):
        for fact in ("https://arxiv.org/abs/2611.27104v1", "Google DeepMind",
                     "2026-11-20T04:25:13Z", "https://github.com/google-deepmind/disco",
                     "HTTP404", "`disco`", "`adapter: null`",
                     "src/auto_research/foundation_models/disco.py"):
            assert fact in text
        assert "paper-figure:start" in text and "```mermaid" in text


def test_paper_figure_and_authored_learning_sources_are_fingerprinted():
    root = Path(__file__).resolve().parents[1]
    directory = root / "docs/foundation-models/2611.27104-disco"
    provenance = json.loads((directory / "assets/provenance.json").read_text())
    image = (directory / "assets/paper-figure-01.png").read_bytes()
    assert image.startswith(b"\x89PNG\r\n\x1a\n")
    assert provenance["asset_sha256"] == sha256(image).hexdigest()
    assert provenance["visually_reviewed"] and not provenance["scientific_content_modified"]
    audit = root / "docs/research-audits/nov23-latest"
    bundle = json.loads((audit / "foundation-authored-bundle.json").read_text())
    questions = bundle["papers"]["foundation-models:disco"]["questions"]
    assert {q["level"] for q in questions} == {"basics", "mechanism", "comparison", "implementation"}
    cn = (directory / "README.md").read_text()
    for question in questions:
        assert question["added"] == "2026-11-23" and question["example"]
        assert all("### " + heading in cn for heading in question["source_sections"])
    proposal = json.loads((audit / "deep-dive-proposals-foundation.json").read_text())["proposals"][0]
    assert proposal["source_revisions"]["foundation-models:disco"] == sha256((directory / "README.md").read_bytes()).hexdigest()
    peer = root / "docs/foundation-models/2611.26413-e-rwsc/README.md"
    assert proposal["source_revisions"]["foundation-models:e-rwsc"] == sha256(peer.read_bytes()).hexdigest()
