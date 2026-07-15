import random

from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.pinterest_ads_llm.model import _response_group


def test_pinterest_ads_adapter_has_significant_online_roas():
    adapter = get_adapter("pinterest-ads-llm")
    assert adapter.paper.has_online_ab
    assert {row.lift_percent for row in adapter.paper.online_ab} == {4.94, 6.69}


def test_grpo_response_group_exercises_rank_and_format_rewards():
    class Row:
        target_advertiser = 0

    responses, rewards = _response_group(
        Row(), ("target", "a", "b", "c", "d", "e", "f"), random.Random(4), 4, 5
    )
    assert len(responses) == 4
    assert rewards[0] > rewards[1] > rewards[2] > rewards[3]
    assert all("</advertiser_names>" in response for response in responses)
