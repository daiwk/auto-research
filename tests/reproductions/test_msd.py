from auto_research.reproductions.msd.model import item_prompt
from auto_research.reproductions.llm_rec_data import TextCTRData


def test_msd_item_prompt_contains_text_and_genre():
    data = TextCTRData((), (), ("Movie",), (("Drama",),), 0)
    prompt = item_prompt(data, 0)
    assert "Movie" in prompt and "Drama" in prompt and "rationale" in prompt
