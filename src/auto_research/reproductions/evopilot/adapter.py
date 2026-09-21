from ..latest_20260921 import make_evopilot_adapter
from ..registry import register


ADAPTER = register(make_evopilot_adapter())
