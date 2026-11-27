from hashlib import sha256
import json
from pathlib import Path
import re

import pytest

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/research-audits/nov27-latest'


def load(path):
    return json.loads(path.read_text())


@pytest.mark.parametrize('key',['compaction-authorization','budgeted-submapl'])
def test_nov27_agent_metadata_translation_figure_and_scope(key):
    spec=load(AUDIT/'paper-proposals-agent.json')['papers']['agent-research:'+key]
    path=ROOT/'docs'/spec['detail_path'];cn=path.read_text();en=path.with_name('README-en.md').read_text()
    for label in ['论文链接','公司/机构/学校','首次公开日期','原作者开源代码','本地 Adapter / 方法','本地复现代码目录']:
        assert label in cn
    assert spec['published_at'].replace('T',' ').replace('Z',' UTC') in cn
    assert spec['discovered_on']=='2026-11-27' and spec['published'] in {'2026-11-24','2026-11-25'}
    assert '<!-- source-sha256: '+sha256(path.read_bytes()).hexdigest()+' -->' in en
    assert '[简体中文](README.md)' in en
    for value in [cn,en]:assert '图片来自[原论文]' in value and '版权归原作者所有' in value
    prov=load(path.parent/'assets/provenance.json')
    assert prov['visually_reviewed'] and prov['caption_preserved']
    assert prov['source_sha256']==spec['method_source_sha256']
    assert prov['asset_sha256']==sha256((path.parent/'assets/paper-figure-01.png').read_bytes()).hexdigest()
    assert spec['evaluation_tier']=='l1_mechanism' and spec['diagnostic_only']
    assert spec['adapter'] is None and not spec['requires_gpu_validation'] and spec['gpu_validation_artifact'] is None
    assert not spec['automatic_retry'] and not spec['promotion_eligible'] and not spec['evolve_integrated']
    if key=='budgeted-submapl':
        assert spec['full_experiment_status']=='not_run_scope_limited' and spec['full_experiment_review_done'] is False
        assert '成本过高' not in spec['deferral_reason'] and spec['announced_on']=='2026-11-26'
    else:
        assert spec['code'] and spec['full_experiment_status']=='not_reproduced_high_cost'
        assert spec['announced_on'] is None


def test_nov27_agent_authored_qa_and_deep_fingerprints():
    specs=load(AUDIT/'paper-proposals-agent.json')['papers'];bundle=load(AUDIT/'agent-authored-bundle.json')
    count=0
    for identity,row in bundle['papers'].items():
        cn=(ROOT/'docs'/specs[identity]['detail_path']).read_text();heads=set(re.findall(r'^#{2,6}\s+(.+)$',cn,re.M))
        assert {q['level'] for q in row['questions']}=={'basics','mechanism','comparison','implementation'}
        for q in row['questions']:
            assert q['added']=='2026-11-27' and set(q['source_sections'])<=heads
            unit=bundle['english_question_units'][f"qa/{identity}/{q['id']}"]
            expected=sha256(json.dumps(q,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            assert unit['reviewed'] and unit['source_sha256']==expected
            assert set(unit['fields'])=={'question','answer','example'}
            assert not re.search(r'[\u3400-\u9fff]',''.join(unit['fields'].values()))
            count+=1
    assert count==8
    peers={'agent-research:runtime-tickets':'agent-research/2611.03772-runtime-tickets/README.md',
           'agent-research:ooas':'agent-research/2611.30405-ooas/README.md'}
    paths=peers|{i:p['detail_path'] for i,p in specs.items()}
    topics=load(ROOT/'docs/learning/topics/agent-research.json')['topics']
    for row in load(AUDIT/'deep-dive-proposals-agent.json')['proposals']:
        members=next(t for t in topics if t['id']==row['target_card'].split('/')[1])['papers']
        assert set(row['source_revisions'])-{row['paper']}<=set(members)
        for identity,digest in row['source_revisions'].items():
            assert sha256((ROOT/'docs'/paths[identity]).read_bytes()).hexdigest()==digest
        assert row['update']['source_revisions']==row['source_revisions']
        assert not re.search(r'[\u3400-\u9fff]',json.dumps(row['english'],ensure_ascii=False))
