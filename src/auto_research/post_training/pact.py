"""Token-level PACT actor-then-critic update on sampled completions.

This is a small-model mechanism implementation, not the paper's distributed
Qwen training recipe. The critic target uses the paper's practical one-token
importance ratio, not the full continuation product.
"""

from __future__ import annotations


def build_critic(vocabulary: int, dimensions: int = 64):
    from torch import nn

    class PrefixCritic(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(vocabulary, dimensions)
            self.recurrent = nn.GRU(dimensions, dimensions, batch_first=True)
            self.value = nn.Linear(dimensions, 1)

        def forward(self, tokens):
            states, _ = self.recurrent(self.embedding(tokens))
            return self.value(states).squeeze(-1)

    return PrefixCritic()


def _rollout_tensors(tokenizer, prompt, sequence, device):
    import torch

    if not sequence:
        raise ValueError("PACT requires a nonempty sampled token sequence")
    prefix = [tokenizer.bos_id, *tokenizer.encode(prompt), tokenizer.sep_id]
    tokens = torch.tensor([[*prefix, *sequence]], dtype=torch.long, device=device)
    return tokens[:, :-1], tokens[:, 1:], len(prefix) - 1


def _token_logprobs(policy, inputs, targets, start):
    logits, _ = policy(inputs)
    return logits.log_softmax(-1).gather(-1, targets.unsqueeze(-1)).squeeze(-1)[0, start:]


def pact_step(
    policy, critic, tokenizer, prompt, token_sequences, rewards,
    actor_optimizer, critic_optimizer, device, *, ratio_max=6.0,
):
    """Run one PACT iteration; rewards must come from an external verifier.

    The actor uses clipped token-policy ratios. Only after that update do we
    recompute log-probabilities for critic one-step importance targets.
    """
    import torch
    from torch.nn import functional as functional

    if not token_sequences or len(token_sequences) != len(rewards):
        raise ValueError("PACT requires a reward for each sampled completion")
    rows = []
    with torch.no_grad():
        for sequence, reward in zip(token_sequences, rewards, strict=True):
            inputs, targets, start = _rollout_tensors(tokenizer, prompt, sequence, device)
            old = _token_logprobs(policy, inputs, targets, start).detach()
            values = critic(inputs)[0, start:].sigmoid().detach()
            rows.append((inputs, targets, start, old, values, float(reward)))

    # Freeze the rollout critic and behavior policy while updating the actor.
    actor_losses = []
    for inputs, targets, start, old, values, reward in rows:
        logps = _token_logprobs(policy, inputs, targets, start)
        advantage = reward - values
        ratio = (logps - old).exp()
        surrogate = torch.minimum(
            ratio * advantage, ratio.clamp(0.8, 1.2) * advantage,
        )
        actor_losses.append(-surrogate.mean())
    actor_loss = torch.stack(actor_losses).mean()
    actor_optimizer.zero_grad(set_to_none=True)
    actor_loss.backward()
    torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
    actor_optimizer.step()

    # The paper's practical target is rho_t * R, where rho_t compares the
    # updated actor with the *rollout* actor at that token. It may exceed 1,
    # so BCE is written as softplus(logit) - target*logit rather than the
    # library BCE function, which assumes target is in [0, 1].
    critic_losses, accepted, total, ratios = [], 0, 0, []
    for inputs, targets, start, old, _, reward in rows:
        with torch.no_grad():
            new = _token_logprobs(policy, inputs, targets, start)
            rho = (new - old).exp()
            mask = (rho >= 0) & (rho <= ratio_max)
            target = rho * reward
        logits = critic(inputs)[0, start:]
        if mask.any():
            critic_losses.append((functional.softplus(logits) - target * logits)[mask].sum())
            accepted += int(mask.sum().item())
        total += mask.numel()
        ratios.append(rho.mean())
    if accepted:
        critic_loss = torch.stack(critic_losses).sum() / accepted
        critic_optimizer.zero_grad(set_to_none=True)
        critic_loss.backward()
        torch.nn.utils.clip_grad_norm_(critic.parameters(), 1.0)
        critic_optimizer.step()
        critic_loss_value = float(critic_loss.detach().cpu())
    else:
        critic_loss_value = 0.0
    return float(actor_loss.detach().cpu()), {
        "critic_loss": critic_loss_value,
        "critic_accepted_fraction": accepted / total,
        "post_actor_ratio_mean": float(torch.stack(ratios).mean().cpu()),
        "critic_target": "post-actor current-token IS * verifier reward",
        "update_order": "actor-then-critic",
    }
