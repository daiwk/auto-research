"""Compatibility imports; implementations live in stable mechanisms modules."""

from __future__ import annotations

from auto_research.mechanisms.stacktok_select import (
    _softmax,
    persistent_recurrent_memory,
    register_chunk,
    stacktok_select,
)
from auto_research.mechanisms.echo_candidates import echo_candidates
from auto_research.mechanisms.echo_lossless_verify import echo_lossless_verify
from auto_research.mechanisms.videomm_select import videomm_select
from auto_research.mechanisms.reproducible_reduce import reproducible_reduce
from auto_research.mechanisms.echo_cuda_kernel import echo_cuda_kernel
from auto_research.mechanisms.videomm_cuda_kernel import videomm_cuda_kernel
