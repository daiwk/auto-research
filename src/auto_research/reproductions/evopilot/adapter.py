from auto_research.reproductions.mechanisms.comparison_protocol import make_evopilot_adapter
from ..registry import register


ADAPTER = register(make_evopilot_adapter())
