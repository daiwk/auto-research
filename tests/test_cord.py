import pytest
import torch

from auto_research.post_training.cord import (
    accumulate_gradients,
    combine_gradients,
    diagnostic,
    objective_gradients,
)


def vector(values):
    return torch.tensor(values, dtype=torch.float64)


@pytest.mark.parametrize("protect", ["first", "second"])
@pytest.mark.parametrize("gate", ["conflict-only", "always", "none"])
def test_closed_form_protects_selected_weighted_objective(protect, gate):
    first, second = vector([2., 1.]), vector([-3., 1.])
    result, audit = combine_gradients(first, second, weight=.2, protect=protect, gate=gate)
    a, b = (first, .2 * second) if protect == "first" else (.2 * second, first)
    expected = a + b if gate == "none" else a + b - a.dot(b) / a.dot(a) * a
    torch.testing.assert_close(result, expected)
    torch.testing.assert_close(audit["protected"], a)
    if gate != "none":
        assert abs(float(a.dot(result) - a.dot(a))) < 1e-12
        assert abs(float(a.dot(audit["candidate_after"]))) < 1e-12
    assert audit["guarantee_before_optimizer_only"] is True


def test_aligned_gate_zero_protected_and_zero_weight_are_distinct():
    first, second = vector([1., 2.]), vector([2., 4.])
    conflict, _ = combine_gradients(first, second)
    always, _ = combine_gradients(first, second, gate="always")
    torch.testing.assert_close(conflict, first + second)
    torch.testing.assert_close(always, first)
    for protect in ("first", "second"):
        zero_weight, _ = combine_gradients(first, second, weight=0, protect=protect, gate="always")
        torch.testing.assert_close(zero_weight, first)
    zero_protected, audit = combine_gradients(first * 0, second)
    torch.testing.assert_close(zero_protected, second)
    assert audit["projected"] is False


def test_projection_is_once_after_fixed_weight_accumulation():
    a = [vector([1., 0.]), vector([0., 1.])]
    b = [vector([-2., 1.]), vector([1., -2.])]
    actual, _ = accumulate_gradients(a, b, (.5, .5))
    wrong = sum(.5 * combine_gradients(x, y)[0] for x, y in zip(a, b))
    torch.testing.assert_close(actual, vector([.5, .5]))
    assert not torch.allclose(actual, wrong)
    split, _ = accumulate_gradients([a[0], a[0], a[1]], [b[0], b[0], b[1]], (.2, .3, .5))
    torch.testing.assert_close(split, actual)


def test_scalar_autograd_preserves_unused_parameters():
    p = torch.nn.Parameter(vector([1., 2.]))
    unused = torch.nn.Parameter(vector([3.]))
    got = objective_gradients((p.square()).sum(), [p, unused])
    torch.testing.assert_close(got, vector([2., 4., 0.]))


def test_fp16_micro_accumulation_promotes_before_overflow():
    first = [torch.tensor([40000., 0.], dtype=torch.float16) for _ in range(2)]
    second = [torch.tensor([0., 1.], dtype=torch.float16) for _ in range(2)]
    result, audit = accumulate_gradients(first, second, (1., 1.))
    assert result.dtype == torch.float32
    assert bool(torch.isfinite(result).all())
    torch.testing.assert_close(audit["first_accumulated"], torch.tensor([80000., 0.]))
    torch.testing.assert_close(audit["second_accumulated"], torch.tensor([0., 2.]))
    torch.testing.assert_close(result, torch.tensor([80000., 2.]))


def test_bf16_micro_accumulation_retains_small_increments():
    first = [torch.tensor([x, 0.], dtype=torch.bfloat16) for x in (256., 1., 1.)]
    second = [torch.zeros(2, dtype=torch.bfloat16) for _ in first]
    result, audit = accumulate_gradients(first, second, (1., 1., 1.))
    assert result.dtype == torch.float32
    torch.testing.assert_close(audit["first_accumulated"], torch.tensor([258., 0.]))
    torch.testing.assert_close(result, torch.tensor([258., 0.]))
    # The old bf16 accumulator lost each unit increment at this magnitude.
    rounded = sum(first, torch.zeros_like(first[0])).float()
    assert not torch.equal(result, rounded)


@pytest.mark.parametrize("options", [{"weight": -1}, {"weight": float("nan")}, {"weight": True}, {"gate": "automatic"}, {"protect": "both"}])
def test_invalid_options(options):
    with pytest.raises(ValueError):
        combine_gradients(vector([1., 2.]), vector([2., 1.]), **options)


def test_invalid_gradient_inputs_and_weights():
    with pytest.raises(ValueError):
        combine_gradients(vector([1., 2.]), vector([float("nan"), 1.]))
    with pytest.raises(ValueError):
        accumulate_gradients([vector([1.])], [vector([2.])], (0.,))
    with pytest.raises(ValueError):
        accumulate_gradients([vector([1.])], [vector([2., 3.])], (1.,))


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_diagnostic_uses_real_neural_gradients_and_three_updates(seed):
    result = diagnostic(seed)
    assert result["metrics"]["optimizer_updates"] == 3
    assert result["metrics"]["student_parameter_delta"] > 0
    assert all(result["checks"].values())
    assert all(torch.isfinite(torch.tensor(v)) for v in result["metrics"].values())
