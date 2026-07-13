from __future__ import annotations

from ..base import PaperMetadata, ReproductionAdapter
from ..registry import register
from .experiment import reproduce_sis
from .report import render

ADAPTER = register(
    ReproductionAdapter(
        key="sis",
        paper=PaperMetadata(
            arxiv_id="2607.04728",
            title="Turning Off-Policy Tokens On-Policy: A Plug-in Approach for Improving LLM Alignment",
            url="https://arxiv.org/abs/2607.04728",
            track="llm",
        ),
        run=reproduce_sis,
        render=render,
    )
)
