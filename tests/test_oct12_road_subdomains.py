import hashlib
import json

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
