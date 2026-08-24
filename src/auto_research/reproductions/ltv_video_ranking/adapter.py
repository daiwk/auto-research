from ..historical_b04_b06_metadata import build_adapter
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(build_adapter('ltv-video-ranking', reproduce, render))
