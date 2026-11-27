from hashlib import sha256
import json
from pathlib import Path
import re

from english_learning_sources import question_units

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/research-audits/nov27-latest'


def load(p):return json.loads(p.read_text())


def test_foundation_metadata_bilingual_figures_and_cost():
    papers=load(AUDIT/'paper-proposals-foundation.json')['papers']
    assert {p['key'] for p in papers}=={'integral-deltanet','deco-attention'}
    for p in papers:
        source=ROOT/'docs'/p['detail_path'];cn=source.read_text();en=source.with_name('README-en.md').read_text()
        assert '<!-- source-sha256: '+sha256(source.read_bytes()).hexdigest()+' -->' in en
        assert '[简体中文](README.md)' in en
        for token in ['## 论文信息','论文链接','公司 / 作者机构','首次公开日期','原作者开源代码',
                      '本地 adapter / 稳定键','本地复现代码目录','### 原论文关键图','图片来自[原论文]',
                      '版权归原作者所有','成本过高，不复现（审查 DONE）']:
            assert token in cn
        assert p['published']=='2026-11-24' and p['announced_on'] is None
        assert p['intake_class']=='overlap_backfill_newly_reviewed'
        assert p['full_experiment_status']=='not_reproduced_high_cost' and not p['automatic_retry']
        assert p['requires_gpu_validation'] is False and p['adapter'] is None
        provenance=load(source.parent/'assets/provenance.json')
        assert provenance['source_pdf_sha256']==p['method_source_sha256']
        assert sha256((source.parent/'assets/paper-figure-01.png').read_bytes()).hexdigest()==provenance['image_sha256']
        assert provenance['visually_reviewed'] and not provenance['scientific_content_modified']
        if p['key']=='deco-attention':
            assert p['code'] is None and 'native_fp4_kernel_calls' in cn
            assert 'CPU' in cn and 'I-ExpCast' in cn


def test_foundation_qa_fingerprints_headings_and_actual_topic_peers():
    bundle=load(AUDIT/'foundation-authored-bundle.json')
    questions={k:v['questions'] for k,v in bundle['papers'].items()}
    units=question_units(questions)
    assert len(units)==8 and set(units)==set(bundle['english_question_units'])
    manifest={p['domain']+':'+p['key']:p for p in load(ROOT/'docs/research-manifest.json')['papers']}
    specs={p['domain']+':'+p['key']:p for p in load(AUDIT/'paper-proposals-foundation.json')['papers']}
    manifest.update(specs)
    topics={}
    for path in (ROOT/'docs/learning/topics').glob('*.json'):
        for t in load(path)['topics']:topics[path.stem+'/'+t['id']]=set(t['papers'])
    for identity,qs in questions.items():
        text=(ROOT/'docs'/specs[identity]['detail_path']).read_text()
        headings=set(re.findall(r'^#{1,6}\s+(.+)$',text,re.M))
        assert {q['level'] for q in qs}=={'basics','mechanism','comparison','implementation'}
        for q in qs:
            assert set(q['source_sections'])<=headings
            unit=f"qa/{identity}/{q['id']}";row=bundle['english_question_units'][unit]
            assert row['source_sha256']==units[unit].source_sha256 and row['reviewed']
    for proposal in load(AUDIT/'deep-dive-proposals-foundation.json')['proposals']:
        peers=set(proposal['source_revisions'])-{proposal['paper']}
        assert peers<=topics[proposal['target_card']]
        for identity,digest in proposal['source_revisions'].items():
            assert sha256((ROOT/'docs'/manifest[identity]['detail_path']).read_bytes()).hexdigest()==digest
