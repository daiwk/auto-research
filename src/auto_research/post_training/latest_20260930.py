"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.roft_retrospection_loss import roft_retrospection_loss
from auto_research.post_training.mechanisms.lspd_objective import lspd_objective
from auto_research.post_training.mechanisms.dr_opd_token_weights import dr_opd_token_weights
from auto_research.post_training.mechanisms.dr_opd_reverse_kl import dr_opd_reverse_kl
from auto_research.post_training.mechanisms.sipo_token_advantage import sipo_token_advantage
from auto_research.post_training.mechanisms.token_policy_gradient_loss import (
    token_policy_gradient_loss,
)
from auto_research.post_training.mechanisms.replay_item import LSPDReplayBuffer, ReplayItem
from auto_research.post_training.mechanisms.roft_family import update_latest
