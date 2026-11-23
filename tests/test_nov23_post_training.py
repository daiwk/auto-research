import math
import random
import hashlib
import json
from pathlib import Path

import pytest

from auto_research.post_training import dwe, retokenization_update as retok


class FixedRandom(random.Random):
    def __init__(self, value):
        super().__init__(0)
        self.value = value

    def random(self):
        return self.value


@pytest.mark.parametrize("reverse", [False, True])
def test_kl_gradient_matches_finite_difference(reverse):
    logits, teacher = (.4, -.7, 1.1), (-.2, .5, -.3)

    def loss(z):
        p, q = dwe.softmax(z), dwe.softmax(teacher)
        a, b = (p, q) if reverse else (q, p)
        return math.fsum(x*math.log(x/y) for x, y in zip(a, b, strict=True))

    analytic = dwe.kl_logit_gradient(logits, teacher, reverse=reverse)
    for i, target in enumerate(analytic):
        plus, minus = list(logits), list(logits)
        plus[i] += 1e-6
        minus[i] -= 1e-6
        assert (loss(plus)-loss(minus))/2e-6 == pytest.approx(target, abs=1e-9)
    assert math.fsum(analytic) == pytest.approx(0., abs=1e-14)


def test_dwe_exact_shared_quantile_integral_and_sparse_chain_rule():
    g = (.4, -.1, -.3, .2, -.2)
    order = (3, 1, 4, 0, 2)
    expected = dwe.exact_quantile_expectation(g, order)
    assert expected == pytest.approx(g, abs=1e-14)
    w, h = ((1., 2.), (3., 1.), (-2., 4.), (5., 6.), (0., 1.)), (2., -3.)
    dh, dw = dwe.sparse_backward(w, h, tuple(enumerate(expected)))
    assert dh == pytest.approx(tuple(sum(w[i][j]*g[i] for i in range(5)) for j in range(2)))
    assert dict(dw)[2] == pytest.approx((g[2]*h[0], g[2]*h[1]))


@pytest.mark.parametrize("draw", [0., .4, math.nextafter(1., 0.)])
def test_dwe_strata_share_quantile_and_never_select_zero_mass(draw):
    sparse = dwe.paired_gradient((.4, 0., -.4, .1, -.1), (0, 1, 2, 3, 4), 8, rng=FixedRandom(draw))
    assert 1 not in dict(sparse)
    assert len(sparse) <= 16
    assert sum(value for _, value in sparse) == pytest.approx(0., abs=1e-14)


def test_principal_order_uses_centered_geometry_and_fixed_ties():
    weights = ((2., 0.), (-2., 0.), (0., 0.), (1., 0.))
    assert dwe.principal_order(weights) == (1, 2, 3, 0)
    assert dwe.principal_order(tuple((a+100, b-20) for a, b in weights)) == (1, 2, 3, 0)
    assert dwe.principal_order(((1., 1.),)*3) == (0, 1, 2)


@pytest.mark.parametrize("g,order,k", [((1., -.5), (0, 1), 2), ((1., -1.), (0, 0), 2), ((math.nan, 0.), (0, 1), 2), ((1., -1.), (0, 1), 0), ((1., -1.), (0, 1), True)])
def test_dwe_invalid_inputs_rejected(g, order, k):
    with pytest.raises(ValueError):
        dwe.paired_gradient(g, order, k, rng=random.Random(0))


def test_retokenization_full_gradient_is_not_sampled_logit_only():
    p = {"aa": .1, "ab": .2, "ba": .3, "bb": .4}
    coarse, fine = retok.PrefixPolicy(p, 2), retok.PrefixPolicy(p, 1)
    assert coarse.string_distribution() == pytest.approx(p)
    assert fine.string_distribution() == pytest.approx(p)
    coarse_before, unvisited = coarse.logits[""], fine.logits["b"]
    update = coarse.full_gradient_step("ab", (.2,))[""]
    assert update == pytest.approx((-.02, .16, -.06, -.08))
    assert coarse.logits[""][0] != coarse_before[0]  # unsampled logit DOES move
    fine.full_gradient_step("ab", (.1, .3))
    assert fine.logits["b"] == unvisited
    c, f = coarse.string_distribution(), fine.string_distribution()
    assert math.log(c["ba"]/c["bb"])-math.log(p["ba"]/p["bb"]) == pytest.approx(-.2*(.3-.4))
    assert f["ba"]/f["bb"] == pytest.approx(p["ba"]/p["bb"])


def test_symmetric_exception_is_not_hidden_by_universal_impossibility_claim():
    p, scalar = {"aa": .25, "ab": .25, "ba": .25, "bb": .25}, .4
    coarse, fine = retok.PrefixPolicy(p, 2), retok.PrefixPolicy(p, 1)
    coarse.full_gradient_step("ab", (scalar,))
    fine.full_gradient_step("ab", (math.log((math.exp(scalar)+1)/2), scalar))
    assert coarse.string_distribution() == pytest.approx(fine.string_distribution(), abs=1e-14)


def test_update_geometry_reference_and_ratio_of_means():
    assert retok.normalized_distance((1., 0.), (1., 0.)) == 0
    assert retok.normalized_distance((1., 0.), (-1., 0.)) == 2
    assert retok.normalized_distance((1e308, 1e308), (-1e308, -1e308)) == 2
    assert retok.normalized_distance((1., 0.), (0., 1.)) == pytest.approx(math.sqrt(2))
    a, b, c = ((1., 0.), (1., 0.)), ((0., 1.), (-1., 0.)), ((-1., 0.), (1., 1.))
    expected = sum(retok.normalized_distance(x, y) for x, y in zip(a, b))/sum(retok.normalized_distance(x, y) for x, y in zip(a, c))
    assert retok.displacement_ratio(a, b, c) == pytest.approx(expected)
    with pytest.raises(ValueError):
        retok.displacement_ratio(a, b, a)
    with pytest.raises(ValueError):
        retok.normalized_distance((0.,), (0.,))


@pytest.mark.parametrize("p,block", [({"aa": .5, "ab": .5}, 1), ({"aa": .1, "ab": .2, "ba": .3, "bb": .3}, 1), ({"aa": 0., "ab": .3, "ba": .3, "bb": .4}, 1), ({"aa": .25, "ab": .25, "ba": .25, "bb": .25}, 3)])
def test_retokenization_invalid_distributions_rejected(p, block):
    with pytest.raises(ValueError):
        retok.PrefixPolicy(p, block)


@pytest.mark.parametrize("module", [dwe, retok])
@pytest.mark.parametrize("seed", [42, 43, 44])
def test_cpu_diagnostic_contract(module, seed):
    result = module.diagnostic(seed)
    assert result["diagnostic_only"] is True and result["evaluation_tier"] == "l1_mechanism"
    assert result["checks"] and all(type(x) is bool and x for x in result["checks"].values())
    assert all(type(x) in (int, float) and math.isfinite(x) for x in result["metrics"].values())
    with pytest.raises(ValueError):
        module.diagnostic(seed, "cuda")


def test_authored_paper_metadata_figures_and_translation_provenance():
    root = Path(__file__).resolve().parents[1]
    proposals = json.loads((root/"docs/research-audits/nov23-latest/paper-proposals-post.json").read_text())["papers"]
    assert set(proposals) == {"post-training:dwe", "post-training:retokenization-update", "post-training:ctrl"}
    for spec in proposals.values():
        directory = root/"docs"/Path(spec["detail_path"]).parent
        source = (directory/"README.md").read_bytes()
        translation = (directory/"README-en.md").read_text()
        assert f"<!-- source-sha256: {hashlib.sha256(source).hexdigest()} -->" in translation
        assert "[简体中文](README.md)" in translation
        assert "原作者开源代码" in source.decode() and "本地复现代码" in source.decode()
        assert spec["adapter"] is None and not spec["requires_gpu_validation"]
        assert spec["full_experiment_review_done"] and not spec["automatic_retry"]
        provenance = json.loads((directory/"assets/provenance.json").read_text())
        assert provenance["visually_reviewed"] and not provenance["scientific_content_modified"]
        assert hashlib.sha256((directory/"assets/paper-figure-01.png").read_bytes()).hexdigest() == provenance["image_sha256"]
    assert proposals["post-training:retokenization-update"]["first_author_affiliation"] == "University of Maine at Presque Isle"
    assert proposals["post-training:ctrl"]["component_implemented"] is False
