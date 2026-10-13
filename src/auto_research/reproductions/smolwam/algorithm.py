"""Contract for the real upstream network, its readout and training curriculum."""
from __future__ import annotations

RELEASED_BLOCKS = (0, 1, 2, 19, 20, 21, 22, 23, 24, 25, 26, 27)


def assert_release(config):
    model = config["model"]
    if (tuple(model["trunk_blocks"]) != RELEASED_BLOCKS or model["n_bidir"] != 6
            or model["ctx_pad_to"] != 512 or tuple(model["slot_tokens"]) != (196, 0, 28, 0, 0)):
        raise ValueError("real 12-block Cosmos trunk, six VL layers and compact 1008-token interface required")


def clean_estimate(noisy, velocity, tau):
    return noisy - tau * velocity


def curriculum_layout(step: int, total_steps: int = 5000, teacher_fraction: float = 0.2):
    if not 0 < teacher_fraction < 1 or total_steps < 2:
        raise ValueError("both pruning-recovery and compact-layout phases required")
    return (196, 196, 196, 196, 196) if step < int(total_steps * teacher_fraction) else (196, 0, 28, 0, 0)


def distillation_loss(actions, demo_actions, teacher_actions, future, demo_future, teacher_future):
    return ((actions - demo_actions).abs().mean() + (actions - teacher_actions).abs().mean()
            + (future - demo_future).abs().mean() + (future - teacher_future).abs().mean())
