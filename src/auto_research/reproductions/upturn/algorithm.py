"""UPTURN Eqs5-10 and Appendix C head architecture."""
from __future__ import annotations

import re
import torch
from torch import nn

INSTRUCTION = "Resolve this concisely."


class PositionHead(nn.Module):
    def __init__(self, hidden_size, width=128):
        super().__init__()
        self.network = nn.Sequential(nn.LayerNorm(hidden_size), nn.Linear(hidden_size, width),
                                     nn.GELU(), nn.Linear(width, 1))

    def forward(self, causal_features):
        return self.network(causal_features.detach()).squeeze(-1)


class CorrectnessGate(nn.Module):
    def __init__(self, hidden_size, width=64):
        super().__init__()
        self.network = nn.Sequential(nn.LayerNorm(hidden_size), nn.Linear(hidden_size, width),
                                     nn.GELU(), nn.Linear(width, 1))

    def forward(self, final_box_feature):
        return self.network(final_box_feature.detach()).squeeze(-1)


def intervention_messages(question_messages, retained_prefix):
    if retained_prefix.count("<think>") > retained_prefix.count("</think>"):
        retained_prefix += "</think>"
    return tuple(question_messages) + ({"role": "assistant", "content": retained_prefix},
                                      {"role": "user", "content": INSTRUCTION})


def remaining_response_budget(max_tokens, cut):
    if not 0 <= cut < max_tokens:
        raise ValueError("cut must retain fewer tokens than the original response budget")
    return max_tokens-cut


def boxed_token_position(tokens, tokenizer):
    """Map the LAST parseable box to ORIGINAL tokens without re-tokenizing."""
    text = tokenizer.decode(tokens, skip_special_tokens=True)
    matches = list(re.finditer(r"\\boxed\{([^{}]+)\}", text))
    if not matches:
        return None
    character = matches[-1].start()
    for index in range(len(tokens)):
        if len(tokenizer.decode(tokens[:index+1], skip_special_tokens=True)) > character:
            return index
    return None


def position_loss(logits, selected, old_log_probs, rescue_rewards, *, epsilon=.2, entropy_beta=.001):
    if len(selected) < 2 or len(selected) != len(set(selected)):
        raise ValueError("sample at least two different cuts without replacement")
    if len(rescue_rewards) != len(selected) or old_log_probs.shape != (len(selected),):
        raise ValueError("cut probabilities and actual rescue rewards must align")
    log_probs = logits.log_softmax(-1)
    values = log_probs[torch.as_tensor(selected, device=logits.device)]
    rewards = torch.as_tensor(rescue_rewards, device=logits.device, dtype=logits.dtype)
    advantages = (rewards-rewards.mean()).detach()  # no std normalization, Eq8
    ratio = (values-old_log_probs.detach()).exp()
    surrogate = torch.minimum(ratio*advantages, ratio.clamp(1-epsilon,1+epsilon)*advantages)
    entropy = -(log_probs.exp()*log_probs).sum()
    return -surrogate.mean()-entropy_beta*entropy, {
        "advantages": advantages.tolist(), "rescue_rewards": rewards.tolist(),
        "entropy": float(entropy.detach()), "nonzero_rescue_advantage": bool(advantages.abs().sum())}


def calibrated_gate(logit, *, temperature=1.38, parseable=True):
    if temperature <= 0:
        raise ValueError("positive calibration temperature required")
    return torch.sigmoid(logit/temperature) if parseable else logit.new_zeros(())
