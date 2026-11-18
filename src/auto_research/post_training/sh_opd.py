"""SH-OPD v1 Algorithm 1; shared batch horizons, no STOPD debiasing."""

import torch
from ._nov18_contracts import mask, receipt, scalar, seeded, tensor

REQUIRES_GPU_VALIDATION = True


def horizon_distribution(base, maximum, alpha):
    if (
        type(base) is not int
        or type(maximum) is not int
        or base < 1
        or maximum < base
        or maximum % base
    ):
        raise ValueError("positive integral maximum/base required")
    a = scalar(alpha, "alpha", lower=0)
    k = maximum // base
    survival = torch.arange(1, k + 1, dtype=torch.float64).pow(-a)
    pmf = survival - torch.cat([survival[1:], torch.zeros(1, dtype=torch.float64)])
    return torch.arange(1, k + 1) * base, pmf


def sample_batch_horizon(base, maximum, alpha, *, generator):
    horizons, pmf = horizon_distribution(base, maximum, alpha)
    return int(horizons[torch.multinomial(pmf, 1, generator=generator)].item())


def generate_batch(prompts, generate, *, horizon):
    """Pass the cap to generation itself; never generate full then truncate.

    Callback contract: generate(prompt, max_new_tokens=H) returns response tokens.
    EOS handling belongs to the actual generator, not this adapter.
    """
    if type(horizon) is not int or horizon < 1 or not prompts:
        raise ValueError("nonempty prompts and positive horizon required")
    responses = [tuple(generate(p, max_new_tokens=horizon)) for p in prompts]
    if any(not r or len(r) > horizon for r in responses):
        raise ValueError("generator violated the shared horizon contract")
    return responses


def token_mean(token_losses, token_mask):
    tensor(token_losses, "losses", ndim=2)
    mask(token_mask, token_losses)
    return token_losses[token_mask].mean()


def implicit_block_weights(base, maximum, alpha):
    _, p = horizon_distribution(base, maximum, alpha)
    return torch.flip(torch.cumsum(torch.flip(p / torch.arange(1, len(p) + 1), [0]), 0), [0])


def diagnostic(seed, device="cpu"):
    g = seeded(seed, device)
    horizons, p = horizon_distribution(2, 8, 0.5)
    _, full = horizon_distribution(2, 8, 0)
    values = torch.randn(2, 4, generator=g, dtype=torch.float64).to(device).requires_grad_()
    m = torch.tensor([[True, True, False, False], [True] * 4], device=device)
    out = token_mean(values, m)
    out.backward()
    h = sample_batch_horizon(2, 8, 0.5, generator=g)
    calls = []

    def fake(prompt, max_new_tokens):
        calls.append(max_new_tokens)
        return [prompt] * max_new_tokens

    generate_batch([1, 2], fake, horizon=h)
    weights = implicit_block_weights(2, 8, 0.5)
    return receipt(
        seed,
        "l1_mechanism",
        {
            "pmf_normalized": bool(torch.allclose(p.sum(), torch.tensor(1.0, dtype=p.dtype))),
            "alpha_zero_is_full_opd": full.tolist() == [0.0, 0.0, 0.0, 1.0],
            "true_shared_generation_cap": calls == [h, h],
            "token_not_sequence_mean": bool(
                torch.allclose(out.detach(), values.detach()[m].sum() / 6)
            ),
            "padding_zero_gradient": bool((values.grad[~m] == 0).all()),
            "implicit_early_weight_not_debiased": bool(weights[0] > weights[-1]),
        },
        {"expected_horizon": float((horizons * p).sum()), "sampled_horizon": h, "loss": out.item()},
    )
