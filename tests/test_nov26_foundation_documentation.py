from hashlib import sha256
import json
from pathlib import Path
import re

from english_learning_sources import question_units

ROOT=Path(__file__).resolve().parents[1]
AUDIT=ROOT/'docs/research-audits/nov26-latest'


def test_foundation_authored_metadata_figures_and_bilingual_contract():
    specs=json.loads((AUDIT/'paper-proposals-foundation.json').read_text())['papers']
    assert {p['key'] for p in specs} == {'rap','duomi','jepa-eu'}
    for p in specs:
        directory=ROOT/'docs'/p['detail_path']
        cn=directory.read_text()
        en=directory.with_name('README-en.md').read_text()
        assert '<!-- source-sha256: '+sha256(directory.read_bytes()).hexdigest()+' -->' in en
        assert '[简体中文](README.md)' in en
        for token in ['## 论文信息','论文链接','公司 / 作者机构','首次公开日期','原作者开源代码',
                      '本地 adapter / 稳定键','本地复现代码目录','<!-- paper-figure:start -->',
                      '### 原论文关键图','图片来自[原论文]','版权归原作者所有','<!-- paper-figure:end -->']:
            assert token in cn
        provenance=json.loads((directory.parent/'assets/provenance.json').read_text())
        image=directory.parent/'assets/paper-figure-01.png'
        assert image.stat().st_size > 5000
        assert sha256(image.read_bytes()).hexdigest() == provenance['image_sha256']
        assert provenance['source_pdf_sha256'] == p['method_source_sha256']
        assert provenance['visually_reviewed'] and not provenance['scientific_content_modified']
        assert not p['automatic_retry']
        if p['key']=='rap':
            assert not p['full_experiment_review_done']
            assert p['full_experiment_status']=='not_run_scope_limited'
            assert p['review_resolution']=='component_scope_complete'
            assert '不是高成本延期' in cn
        else:
            assert p['full_experiment_review_done']
            assert '成本过高，不复现（审查 DONE）' in cn
        assert not p['evolve_integrated'] and not p['promotion_eligible']
        if p['key']=='jepa-eu':
            assert p['adapter'] is p['local_operator'] is p['local_command'] is None
            assert p['implementation_status']=='deferred_high_cost'
            assert not (directory.parent/'metrics').exists()


def test_foundation_authored_questions_and_peer_source_fingerprints():
    bundle=json.loads((AUDIT/'foundation-authored-bundle.json').read_text())
    papers=bundle['papers']
    units=question_units({k:v['questions'] for k,v in papers.items()})
    assert set(units)==set(bundle['english_question_units'])
    specs={p['domain']+':'+p['key']:p for p in json.loads((AUDIT/'paper-proposals-foundation.json').read_text())['papers']}
    manifest={p['domain']+':'+p['key']:p for p in json.loads((ROOT/'docs/research-manifest.json').read_text())['papers']}
    for identity,paper in papers.items():
        assert {q['level'] for q in paper['questions']} == {'basics','mechanism','comparison','implementation'}
        text=(ROOT/'docs'/specs[identity]['detail_path']).read_text()
        headings=set(re.findall(r'^#{1,6}\s+(.+)$',text,re.M))
        for q in paper['questions']:
            assert set(q['source_sections']) <= headings
            uid=f"qa/{identity}/{q['id']}"
            row=bundle['english_question_units'][uid]
            assert row['reviewed'] and row['source_sha256']==units[uid].source_sha256
            assert set(row['fields']) == {'question','answer','example'}
    proposals=json.loads((AUDIT/'deep-dive-proposals-foundation.json').read_text())['proposals']
    for p in proposals:
        assert p['update']['source_revisions']==p['source_revisions']
        for identity,digest in p['source_revisions'].items():
            record=specs.get(identity,manifest.get(identity))
            assert sha256((ROOT/'docs'/record['detail_path']).read_bytes()).hexdigest()==digest
