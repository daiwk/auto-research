import pytest

from auto_research.dependency_guard import (
    assert_torch_plan_is_safe,
    planned_distribution_version,
)


def _report(*packages):
    return {
        "install": [
            {"metadata": {"name": name, "version": version}} for name, version in packages
        ]
    }


def test_guard_allows_unchanged_or_new_torch_install():
    same = _report(("torch", "2.8.0"), ("transformers", "5.0.0"))
    assert planned_distribution_version(same, "torch") == "2.8.0"
    assert_torch_plan_is_safe("2.8.0", same, allow_torch_change=False)
    assert_torch_plan_is_safe(None, same, allow_torch_change=False)


def test_guard_rejects_silent_torch_replacement():
    report = _report(("Torch", "2.8.0"))
    with pytest.raises(RuntimeError, match="Refusing to replace"):
        assert_torch_plan_is_safe("2.7.0+vendor", report, allow_torch_change=False)
    assert_torch_plan_is_safe("2.7.0+vendor", report, allow_torch_change=True)


def test_guard_accepts_plan_that_does_not_touch_torch():
    report = _report(("transformers", "5.0.0"))
    assert planned_distribution_version(report, "torch") is None
    assert_torch_plan_is_safe("2.7.0+vendor", report, allow_torch_change=False)
