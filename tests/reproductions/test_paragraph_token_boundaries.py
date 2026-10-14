"""Exact-token CPU boundary contracts, not GPU or reasoning evidence."""
from pathlib import Path

import pytest

from auto_research.reproductions.progressive_contraction.algorithm import paragraph_prefixes


class FusedTokenizerFixture:
    eos_token_id=99
    pieces={1:"First step",2:".\n\n",3:"Second step",4:".\n\n",5:"Final answer",
            6:"\n\n\n\n",7:"\n\n",99:"<eos>"}
    def decode(self,tokens,*,skip_special_tokens,clean_up_tokenization_spaces):
        assert clean_up_tokenization_spaces is False
        return "".join(self.pieces[t] for t in tokens if not (skip_special_tokens and t==99))
    def __call__(self,*args,**kwargs):
        raise AssertionError("prefixes must never be re-tokenized")


def test_period_fused_paragraph_boundaries_map_to_exact_original_token_prefixes():
    tokens=(1,2,3,4,5,99)
    cuts=paragraph_prefixes(tokens,(7,),tokenizer=FusedTokenizerFixture(),limit=16)
    assert cuts==[2,4]
    assert [tokens[:cut] for cut in cuts]==[(1,2),(1,2,3,4)]


def test_repeated_newlines_are_deduplicated_and_limit_is_applied_after_mapping():
    tokenizer=FusedTokenizerFixture()
    tokens=(1,6,3,4,5,99)
    assert paragraph_prefixes(tokens,tokenizer=tokenizer,limit=16)==[2,4]
    assert paragraph_prefixes(tokens,tokenizer=tokenizer,limit=1)==[2]
    assert paragraph_prefixes((1,7,3,7,5),tokenizer=tokenizer,limit=16)==[2,4]


def test_trailing_paragraph_delimiter_without_a_following_paragraph_is_not_a_cut():
    tokenizer=FusedTokenizerFixture()
    assert paragraph_prefixes((1,2,99),tokenizer=tokenizer,limit=16)==[]
    assert paragraph_prefixes((1,2),tokenizer=tokenizer,limit=16)==[]


def test_original_tuple_delimiter_fixture_path_remains_compatible():
    assert paragraph_prefixes((1,9,9,2,9,9,3),(9,9),limit=3)==[3,6]


def test_invalid_boundary_budget_is_rejected():
    with pytest.raises(ValueError):
        paragraph_prefixes((1,2,3),tokenizer=FusedTokenizerFixture(),limit=0)


def test_fixed_public_qwen_tokenizer_period_fusion_when_cpu_cache_is_available():
    directory=Path(__file__).resolve().parents[2]/".cache/oct14-skill-public-transfer"
    if not (directory/"tokenizer.json").is_file():
        pytest.skip("fixed public tokenizer cache absent; deterministic fusion contracts still run")
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(directory,local_files_only=True)
    text="First step.\n\nSecond step.\n\nFinal \\boxed{2}"
    tokens=tuple(tokenizer(text,add_special_tokens=False).input_ids)
    assert tokens[:6]==(5338,3019,382,15666,3019,382)
    cuts=paragraph_prefixes(tokens,tokenizer=tokenizer,limit=16)
    assert cuts==[3,6]
    assert all(tokens[:cut][-1]==382 for cut in cuts)
