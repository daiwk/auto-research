from ..historical_b01_b03_metadata import build_adapter
from ..registry import register
from .experiment import reproduce
from .report import render


ADAPTER = register(build_adapter('tubifm', reproduce, render))
