from auto_research.reproductions.mechanisms.gese_candidate_scores import make_adapter
from auto_research.reproductions.registry import register

ADAPTER = register(make_adapter("gese"))
