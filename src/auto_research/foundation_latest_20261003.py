"""Foundation-model mechanisms selected from the 2026-10-03 intake."""

from __future__ import annotations


def llm2jev_distribution(option_log_probs, *, temperature: float = 1.0):
    """Turn bracketed-option token likelihoods into a Jev distribution."""
    import torch

    if temperature <= 0 or option_log_probs.ndim != 2:
        raise ValueError("option_log_probs must be [options, option_tokens]")
    return torch.softmax(option_log_probs.sum(-1) / temperature, dim=0)


def llm2jev_objective(decision_logits, target, auxiliary_logits, base_logits, *, kl_weight: float):
    """Listwise decision loss with the paper's base-model KL anchor."""
    import torch.nn.functional as F

    listwise = F.cross_entropy(decision_logits[None], target.reshape(1))
    base = F.softmax(base_logits.detach(), dim=-1)
    anchor = F.kl_div(F.log_softmax(auxiliary_logits, dim=-1), base, reduction="batchmean")
    return listwise + kl_weight * anchor


def dense_caption_distillation(student_embeddings, caption_teacher_embeddings):
    """Omni-Embed-Mini cosine distillation into the frozen text geometry."""
    import torch.nn.functional as F

    student = F.normalize(student_embeddings, dim=-1)
    teacher = F.normalize(caption_teacher_embeddings.detach(), dim=-1)
    return (1 - (student * teacher).sum(-1)).mean()


def mwop_masks(attention_importance, visual_ffn_importance, text_ffn_importance, *, keep: int):
    """Create separate modality-path and modality-FFN masks for MWOP."""
    import torch

    if attention_importance.ndim != 2 or attention_importance.shape[-1] != 3:
        raise ValueError("attention importance must be [heads, V2V/T2V/T2T]")
    if keep <= 0:
        raise ValueError("keep must be positive")

    def mask(values):
        result = torch.zeros_like(values, dtype=torch.bool)
        count = min(keep, values.numel())
        result.flatten()[torch.topk(values.flatten(), count).indices] = True
        return result

    return mask(attention_importance), mask(visual_ffn_importance), mask(text_ffn_importance)


def af_muon_vocab_direction(gradient, *, cap: float):
    """Support-aware finite-cap direction for a tied vocabulary table."""
    import torch

    if gradient.ndim != 2 or cap <= 0:
        raise ValueError("expected a vocabulary matrix and a positive cap")
    active = gradient.norm(dim=1) > 0
    direction = torch.zeros_like(gradient)
    if active.any():
        rows = gradient[active]
        direction[active] = rows / rows.norm(dim=1, keepdim=True).clamp_min(1e-12)
        direction[active] *= rows.norm(dim=1, keepdim=True).clamp(max=cap)
    return direction


def rea_select_context(instructions, episodes, relevance, *, episode_budget: int):
    """Keep persistent instructions and retrieve only useful episodic turns."""
    import torch

    if len(episodes) != len(relevance) or episode_budget < 0:
        raise ValueError("invalid episodic inputs")
    count = min(episode_budget, len(episodes))
    selected = torch.topk(torch.as_tensor(relevance), count).indices.tolist() if count else []
    return tuple(instructions), tuple(episodes[index] for index in selected)


def hawk_draft_target(target_hidden_states, layer_weights, shifted_target_logits):
    """Mix informative target layers and expose shifted-trajectory supervision."""
    import torch

    weights = torch.softmax(layer_weights, dim=0)
    hidden = sum(weights[index] * state for index, state in enumerate(target_hidden_states))
    return hidden, shifted_target_logits.detach()


def ireko_nested_subnetwork(weight, projection, *, width: int):
    """Expose a nested post-hoc subnetwork without discarding the projection."""
    if width <= 0 or width > projection.shape[1]:
        raise ValueError("invalid requested width")
    basis = projection[:, :width]
    return basis.transpose(-1, -2) @ weight @ basis, basis
