import math

import pytest

from run_nov26_latest_components import config, load_component, validate_diagnostic


@pytest.mark.parametrize("key", ["rap", "duomi", "briar", "feast", "home", "dualpm", "onequery", "camar"])
def test_actual_component_contract_before_execution_freeze(key):
    module_name = "auto_research."+config()["components"][key]["module"].removesuffix(".py").replace("/", ".")
    module = load_component(module_name)
    assert module.REQUIRES_GPU_VALIDATION is config()["components"][key]["cuda"]
    row = module.diagnostic(42, device="cpu")
    validate_diagnostic(row, 42, key)
    assert all(type(flag) is bool for flag in row["checks"].values())
    assert all(math.isfinite(value) for value in row["metrics"].values())
