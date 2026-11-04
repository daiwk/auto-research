"""Publish the bounded Nov4 bulletin delivery, without an exhaustive-window claim."""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from curate_nov04b_components import AUDIT, COMPONENTS, catalogue, validate_raw  # noqa: E402

BATCH='2026-11-04-new-bulletin-components'
REFERENCES={'multi-layer-indexer','rsi-dojo'}
CATEGORIES={'cs.AI','cs.CL','cs.CV','cs.IR','cs.LG','cs.RO','cs.SD','eess.AS'}


def write(path,payload):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(directory):
    if (AUDIT/'task-scope.json').exists():
        raise ValueError('accepted scope is immutable; refuse a second publication')
    ledger_path=ROOT/'docs/paper-discovery-ledger.json'
    ledger=json.loads(ledger_path.read_text())
    if any(batch['batch']==BATCH for batch in ledger['batches']):
        raise ValueError('batch already exists')
    capture=json.loads((directory/'capture.json').read_text())
    direct=json.loads((directory/'bulletins-direct.json').read_text())
    query=[row for row in capture if row['kind']=='arxiv']
    for pages in (direct,query):
        if len(pages)!=8 or {p['source'] for p in pages}!=CATEGORIES:
            raise ValueError('eight distinct category receipts required for each URL route')
        if any(p.get('status')!='retrieved' or p.get('parse_complete') is not True
               or p.get('announced_on')!='2026-11-04'
               or not p.get('expected_entries')==p.get('parsed_entries')==len(p['records']) for p in pages):
            raise ValueError('actual Nov4 bulletin parse/counts required')
    direct_ids={p['source']:[r['arxiv_id'] for r in p['records']] for p in direct}
    query_ids={p['source']:[r['arxiv_id'] for r in p['records']] for p in query}
    if direct_ids!=query_ids:
        raise ValueError('direct and parameterized routes disagree; do not invent a merged date')
    frozen=json.loads((AUDIT/'frozen-sources.json').read_text())
    for device in ('cpu','cuda'):
        validate_raw(json.loads((AUDIT/f'raw-{device}.json').read_text()),device,frozen)
    selected={key:spec for key,(_,spec) in catalogue().items()}
    for path in (ROOT/'src/auto_research/paper_specs/catalog').glob('*/*.json'):
        spec=json.loads(path.read_text())
        if spec['key'] in REFERENCES:selected[spec['key']]=spec
    if set(selected)!=set(COMPONENTS)|REFERENCES:
        raise ValueError('fixed fourteen selected papers required')
    baseline_path=ROOT/'docs/research-audits/nov04-components/source-coverage.json'
    baseline=json.loads(baseline_path.read_text())
    baseline_time=max(datetime.fromisoformat(row['checked_at'].replace('Z','+00:00')) for row in baseline['retrieval_receipts'])
    observed={r['arxiv_id'].split('v')[0] for page in direct for r in page['records']}
    new_section={r['arxiv_id'].split('v')[0] for page in direct for r in page['records'] if r['entry_kind']=='new'}
    rows=[]
    for key,spec in sorted(selected.items()):
        identity=spec['paper_url'].split('/')[-1].split('v')[0]
        if identity not in observed or spec.get('review_done') is not True:
            raise ValueError('selected identity must be in the actual bulletin and reviewed')
        component=key in COMPONENTS
        if (spec.get('full_experiment_status')!='not_reproduced_high_cost'
                or spec.get('full_experiment_review_done') is not True
                or spec.get('promotion_eligible') is not False or spec.get('evolve_integrated') is not False):
            raise ValueError('explicit high-cost terminal/no-capability boundary required')
        if not component and (spec.get('local_operator') is not None or spec.get('requires_gpu_validation')):
            raise ValueError('reference-only paper cannot become a pretend implementation')
        row={field:spec[field] for field in ('domain','key','title','paper_url','detail_path','published','published_at',
                                            'first_author','first_author_affiliation','priority','cost_assessment','implementation_status')}
        row.update(id=identity,doc=spec['detail_path'],catalog_key=key,catalog_detail=spec['detail_path'],
                   track={'foundation-models':'foundation-model','agent-research':'agent'}.get(spec['domain'],spec['domain']),
                   intake_class=('late_announced_historical_backfill' if key=='rsi-dojo' else
                                 'newly_crosslisted_first_collection' if identity not in new_section else
                                 'newly_announced_first_collection'),
                   status='implemented' if component else 'deferred',
                   resolution='bounded_l1_component_accepted' if component else 'not_reproduced_high_cost',
                   component_implemented=component,component_accepted=component,review_done=True,
                   first_publication_after_previous_capture=datetime.fromisoformat(spec['published_at'].replace('Z','+00:00'))>baseline_time,
                   full_experiment_status='not_reproduced_high_cost',full_experiment_review_done=True,
                   requires_gpu_validation=bool(spec.get('requires_gpu_validation')),
                   gpu_validation_passed=bool(spec.get('gpu_validation_passed')),
                   automatic_retry=False,automatic_implementation_queue=False,promotion_eligible=False,evolve_integrated=False,
                   verified_priority_organizations=[],
                   full_text_review={'scope':'defining method, resource/cost, author affiliation/code and original figure; not every appendix/reference claim','full_article_read':False},
                   source_provenance=[{'source_kind':'reviewed-fixed-primary-paper','source_url':spec.get('reviewed_version_url',spec['paper_url'])}])
        if component:
            device=COMPONENTS[key][1]
            row['component_evidence']=(Path('docs')/Path(spec['detail_path']).parent/f'metrics/component-{device}-seeds42-44.json').as_posix()
        else:
            if not spec.get('deferral_reason'):
                raise ValueError('reference-only high-cost closure requires an explicit reason')
            row['reason']=spec['deferral_reason']
        rows.append(row)
    official=[]
    for name in ['Google','Meta','Google DeepMind']:
        pages=[p for p in capture if p['kind']=='official' and p['source']==name]
        complete=all(p['status']=='retrieved' for p in pages)
        official.append({'organization':name,'attempted_pages':len(pages),'retrieved_pages':sum(p['status']=='retrieved' for p in pages),
                         'delta_known':False,'new_directory_urls':None,
                         'status':'bounded_retrieved_inventory_not_full_identity_review' if complete else 'source_unavailable_not_zero_delta'})
    counts={'selected_papers':14,'component_implementations':12,'cuda_validated_components':6,'cpu_only_components':6,
            'reference_only_high_cost_review_done':2,'newly_announced_first_collections':13,
            'new_section_first_collections':12,'crosslisted_first_collections':1,'late_announced_backfills':1,
            'selected_first_publications_after_previous_capture':sum(r['first_publication_after_previous_capture'] for r in rows),
            'category_entries_including_crosslists_and_replacements':sum(len(p['records']) for p in direct),
            'unique_bulletin_identities':len(observed),'full_capability_reproductions':0}
    common={'schema_version':1,'batch':BATCH,'selected_scope_complete':True,'delivery_status':'bounded_scope_complete',
            'all_sources_exhaustive':False,'review_watermark_advanced':False,
            'review_watermark':{'before':'2026-10-15','after':'2026-10-15'},'counts':counts}
    scope=common|{'fixed_component_keys':sorted(COMPONENTS),'reference_only_keys':sorted(REFERENCES),'papers':rows}
    coverage=common|{'checked_on':'2026-11-04','actual_announced_on':'2026-11-04',
                     'baseline':'docs/research-audits/nov04-components/source-coverage.json','baseline_sha256':sha(baseline_path),
                     'baseline_last_checked_at':baseline_time.isoformat(),'full_bulletin_full_text_review_complete':False,
                     'raw_capture_sha256':sha(directory/'capture.json'),'direct_capture_sha256':sha(directory/'bulletins-direct.json'),
                     'bulletin_ids_by_category':direct_ids,'direct_and_parameterized_identities_equal':True,
                     'retrieval_receipts':[{k:v for k,v in p.items() if k!='records'} for p in capture+direct],
                     'official_directory_status':official,
                     'limitations':[f'Fourteen selected full-text method reviews are not all {len(observed)} bulletin identities reviewed.',
                         'November4 announcement/first collection is not original publication today or after the previous capture; v1 timestamps are separate.',
                         'Google/Meta directory timeouts are unknown deltas, not zero new papers; official GitHub/search are bounded supplementary channels.',
                         'Meta² is a method name, not a verified Meta company affiliation. None of this selected cohort is advertised as Google/Meta.',
                         'L1 tensors, state and arithmetic are not complete model capability, production lift, measured serving acceleration or executable Evolve integration.',
                         'High-cost complete experiments are reviewDONE/not reproduced; no automatic retry queue. Global review watermark remains October15.']}
    minimal=[{**{k:v for k,v in page.items() if k!='records'},
              'records':[{k:r[k] for k in ('arxiv_id','title','authors','entry_kind')} for r in page['records']]} for page in direct]
    batch=common|{'date':'2026-11-04','source_artifact':'research-audits/nov04-bulletin-components/README.md','candidates':rows}
    updated=deepcopy(ledger);updated['batches'].append(batch)
    for name,payload in [('source-coverage.json',coverage),('task-scope.json',scope),('bulletin-records.json',minimal)]:
        write(AUDIT/name,payload)
    write(ledger_path,updated)
    print(json.dumps(counts))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture_directory',type=Path)
    args=parser.parse_args()
    record(args.capture_directory)
