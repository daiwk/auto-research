"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.post_training.mechanisms.oasis_select_scaffold import oasis_select_scaffold
from auto_research.post_training.mechanisms.oasis_forward_kl import oasis_forward_kl
from auto_research.post_training.mechanisms.graft_peer_objective import graft_peer_objective
from auto_research.post_training.mechanisms.ride_target import ride_loss, ride_target
from auto_research.post_training.mechanisms.pr_opd_alignment import pr_opd_alignment
