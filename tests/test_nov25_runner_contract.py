"""Validate every diagnostic interface before source freeze and device runs."""
import pytest

from run_nov25_latest_components import config, load_component, validate_diagnostic


@pytest.mark.parametrize("key",sorted(config()["components"]))
def test_actual_cpu_diagnostic_matches_unified_evidence_contract(key):
    item=config()["components"][key]
    module=load_component("auto_research."+item["module"][:-3].replace("/","."))
    assert module.REQUIRES_GPU_VALIDATION is item["cuda"]
    row=module.diagnostic(42,device="cpu")
    validate_diagnostic(row,42,key)
