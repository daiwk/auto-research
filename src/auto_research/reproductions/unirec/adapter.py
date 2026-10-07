from auto_research.reproductions.mechanisms.unirec_scores import make_adapter
from ..registry import register

ADAPTER = register(make_adapter("unirec"))
