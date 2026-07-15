from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.sigma.data import TASKS


def test_sigma_adapter_has_two_week_online_ab():
    adapter = get_adapter("sigma")
    assert adapter.paper.has_online_ab
    assert {row.lift_percent for row in adapter.paper.online_ab} == {2.8, 7.84}


def test_sigma_keeps_all_seven_instruction_tasks():
    assert set(TASKS) == {
        "JustForYou", "Query", "Category", "Longtail", "Discover", "Season", "Holiday"
    }
