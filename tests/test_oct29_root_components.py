import pytest
import torch

from auto_research.foundation_models.sleep_lti import diagnostic as sleep_diagnostic
from auto_research.foundation_models.sleep_lti import edit_distance, lti_reward
from auto_research.reproductions.kl_mopd import calibrate_weights, diagnostic, kl_mopd_loss


@pytest.mark.parametrize("seed", [42, 43, 44])
def test_real_diagnostics(seed):
    assert all(diagnostic(seed)["checks"].values())
    assert all(sleep_diagnostic(seed)["checks"].values())


def test_kl_calibration_zero_is_not_silently_uniform():
    x = torch.zeros(2, 3, 5, dtype=torch.float64)
    with pytest.raises(ValueError, match="positive"):
        calibrate_weights(x, torch.stack([x, x]), torch.ones(2, 3, dtype=torch.bool))


def test_kl_token_sum_not_length_average_and_padding_nan():
    x = torch.tensor([[[1., 2.], [1., 2.]]], requires_grad=True)
    q = torch.tensor([[[[3., 0.], [3., 0.]]], [[[0., 3.], [0., 3.]]]])
    a = torch.tensor([[.7, .7], [.3, .3]])
    mask = torch.ones(1, 2, dtype=torch.bool)
    full = kl_mopd_loss(x, q, mask, a)
    single = kl_mopd_loss(x[:, :1], q[:, :, :1], mask[:, :1], a[:, :1])
    torch.testing.assert_close(full, 2 * single)
    mask[:, 1] = False
    xn, qn = x.detach().clone(), q.clone()
    xn[:, 1], qn[:, :, 1] = float("nan"), float("nan")
    torch.testing.assert_close(kl_mopd_loss(xn, qn, mask, a), single)


def test_finite_large_discrepancies_normalize_without_overflow():
    x = torch.tensor([[[1e38, -1e38]]])
    teachers = torch.stack([-x, -x])
    alpha = calibrate_weights(x, teachers, torch.tensor([[True]]))["weights"]
    torch.testing.assert_close(alpha, torch.tensor([[.5], [.5]]))


def test_sleep_count_threshold_and_nonempty_tokens():
    assert edit_distance([1, 2], [1, 3, 2]) == 1
    assert lti_reward([1, 2], [1, 3, 2], semantic_match=1, gamma=.2, threshold=0)["reward"] == .2
    with pytest.raises(ValueError):
        edit_distance([], [])
    with pytest.raises(ValueError):
        lti_reward([1], [1], semantic_match=.7, gamma=.5, threshold=1)
