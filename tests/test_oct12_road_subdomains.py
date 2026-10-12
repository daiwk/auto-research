import hashlib
import json

import pytest

from auto_research.post_training.oct10_checkpoint import load_public_rows
from auto_research.public_holdout import validate_holdout

from scripts.prepare_oct12_road_subdomains import domain, prepare


def test_domain_depends_on_question_not_gold():
    assert domain('How much money did she earn?')=='monetary-arithmetic'
    assert domain('How many apples are in the basket?')=='nonmonetary-arithmetic'


def test_transform_keeps_labels_partitions_and_public_identity(tmp_path):
    source=tmp_path/'source'
    source.mkdir()
    files={}
    questions={'train':['How many apples?','How many dollars?'],
               'validation':['How many pears?','What is the price?']}
    for split,values in questions.items():
        raw=''.join(json.dumps({'question':q,'answer':'#### 3'})+'\n' for q in values).encode()
        (source/f'{split}.jsonl').write_bytes(raw)
        files[split]=hashlib.sha256(raw).hexdigest()
    manifest={'source_id':'openai/grade-school-math','source_revision':'a'*40,
              'source_split':'train','test_opened':False,'source_sha256':'b'*64,
              'partition':'test fixture normalized question partition','counts':{'train':2,'validation':2},
              'partition_sha256':files}
    (source/'split.json').write_text(json.dumps(manifest))
    result=prepare(source,tmp_path/'output')
    assert result['source_revision']==manifest['source_revision']
    assert result['original_partition_sha256']==files and result['test_opened'] is False
    rows=[json.loads(line) for line in (tmp_path/'output/train.jsonl').read_text().splitlines()]
    assert [row['question'] for row in rows]==questions['train']
    assert [row['answer'] for row in rows]==['#### 3','#### 3']
    assert len({row['domain'] for row in rows})==2


@pytest.mark.parametrize('separator', ['\u0085','\u2028','\u2029','\n','\r','\r\n',
                                       '\v','\f','\x1c','\x1d','\x1e'])
def test_unicode_line_separators_preserve_text_and_load_as_exact_jsonl_records(tmp_path,separator):
    source=tmp_path/'source'
    source.mkdir()
    originals={
        'train':[{'question':'How many apples'+separator+'in basket?','answer':'work'+separator+'#### 3'},
                 {'question':'How many dollars'+separator+'paid?','answer':'账单'+separator+'#### 5'}],
        'validation':[{'question':'How many pears'+separator+'on table?','answer':'steps'+separator+'#### 7'},
                      {'question':'What is the price'+separator+'of tea?','answer':'成本'+separator+'#### 9'}],
    }
    digests={}
    for split,rows in originals.items():
        raw=''.join(json.dumps(row,ensure_ascii=False)+'\n' for row in rows).encode('utf-8')
        (source/f'{split}.jsonl').write_bytes(raw)
        digests[split]=hashlib.sha256(raw).hexdigest()
    manifest={'source_id':'openai/grade-school-math','source_revision':'a'*40,
              'source_split':'train','test_opened':False,'source_sha256':'b'*64,
              'partition':'unit fixture question partition','counts':{'train':2,'validation':2},
              'partition_sha256':digests}
    (source/'split.json').write_text(json.dumps(manifest),encoding='utf-8')
    output=tmp_path/'fresh'
    result=prepare(source,output)
    assert result['counts']=={'train':2,'validation':2}
    assert result['original_partition_sha256']==digests
    assert 'ensure_ascii=True' in result['jsonl_serialization']
    for split,original_rows in originals.items():
        path=output/f'{split}.jsonl'
        raw=path.read_bytes()
        assert raw.isascii() and len(raw.split(b'\n'))==3
        actual_rows=load_public_rows(path)  # Existing shared loader, not a patched fixture.
        assert len(actual_rows)==len(original_rows)==2
        assert [{key:row[key] for key in ('question','answer')} for row in actual_rows]==original_rows
        assert result['partition_sha256'][split]==hashlib.sha256(raw).hexdigest()
    assert validate_holdout(output/'split.json',output/'train.jsonl',output/'validation.jsonl',
                            dataset_revision='a'*40)['verified']
