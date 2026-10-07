from auto_research.reproductions.mechanisms.rptune_family import make_adapter
from ..registry import register

ADAPTER = register(make_adapter("rptune"))
