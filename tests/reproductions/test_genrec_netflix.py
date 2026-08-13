import numpy as np

from auto_research.reproductions.genrec_netflix.data import (
    GenRecData,
    training_rows,
    verbalize,
)
from auto_research.reproductions.registry import get_adapter


def _data() -> GenRecData:
    return GenRecData(
        train=((0, 1, 2, 3, 4),),
        validation=(5,),
        test=(6,),
        item_texts=tuple(f"Title: movie {index}. Genres: genre {index % 2}." for index in range(7)),
        item_genres=tuple((f"genre {index % 2}",) for index in range(7)),
        popularity=np.ones(7, dtype=np.float32),
    )


def test_netflix_genrec_does_not_replace_jd_genrec():
    jd = get_adapter("genrec")
    netflix = get_adapter("genrec-netflix")
    assert jd.paper.arxiv_id == "2604.14878"
    assert netflix.paper.arxiv_id == "2608.10257"
    assert netflix.paper.organization == "Netflix"
    assert netflix.paper.has_online_ab


def test_genrec_training_rows_and_prompt_use_real_item_text():
    data = _data()
    rows = training_rows(data, maximum_history=3)
    assert rows == [((0, 1, 2), 3), ((1, 2, 3), 4)]
    prompt = verbalize((0, 1, 2), data, maximum_events=2)
    assert "Title: movie 1" in prompt
    assert "Genres: genre 0" in prompt
    assert "Title: movie 0" not in prompt
