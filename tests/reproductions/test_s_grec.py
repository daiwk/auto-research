import numpy as np

from auto_research.reproductions.registry import get_adapter
from auto_research.reproductions.s_grec.data import ASPECT_NAMES, ASPECT_VALUES


def test_s_grec_has_required_online_ab_and_three_offline_aspects():
    adapter = get_adapter("s-grec")
    assert adapter.paper.has_online_ab
    assert {entry.metric for entry in adapter.paper.online_ab} == {"GMV", "CTR"}
    assert ASPECT_NAMES == ("profile", "future", "novelty")
    assert [len(values) for values in ASPECT_VALUES] == [5, 3, 3]


def test_a2po_magnitude_rule_is_business_bounded():
    business = np.asarray([-2.0, -0.2, 0.3, 1.5])
    semantic = np.asarray([-0.5, 3.0, 0.1, -1.0])
    consistent = np.sign(business) == np.sign(semantic)
    coefficient = consistent * np.minimum(abs(business), abs(semantic)) / (
        np.maximum(abs(business), abs(semantic)) + 1e-8
    )
    contribution = coefficient * semantic
    assert np.all(abs(contribution) <= abs(business) + 1e-7)
    assert coefficient[1] == 0.0
    assert coefficient[3] == 0.0
