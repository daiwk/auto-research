from ..historical_b07 import build_adapter
from ..registry import register
from .experiment import reproduce


ADAPTER = register(build_adapter('autonomy-heads', reproduce))
