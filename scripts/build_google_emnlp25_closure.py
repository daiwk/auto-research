"""Close exactly the 25 approved historical leads, without inventing new papers."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'scripts'))
from auto_research.paper_specs.catalog import catalog_records  # noqa: E402
from curate_oct21_component_evidence import require, write  # noqa: E402

BATCH = '2026-10-25-google-emnlp25-closure'
AUDIT_REL = Path('docs/research-audits/google-emnlp25-closure')
INPUT_REL = Path('docs/research-audits/oct25-priority-components/google-emnlp-title-identity-audit.json')
DECISIONS = {'component_only', 'not_reproduced_high_cost', 'not_selected', 'duplicate', 'archived_source_exception'}


def catalogue():
    return {r['key']: r for r in catalog_records()}


def approved_input(root=ROOT):
    raw = (root/INPUT_REL).read_bytes()
    payload = json.loads(raw)
    rows = payload['historical_metadata_leads']
    require(len(rows) == len({r['id'] for r in rows}) == 25, 'exact 25 unique approved input identities required')
    require(all(r['accepted_for_implementation'] is False for r in rows), 'input must remain the original unaccepted snapshot')
    return {r['id']: r for r in rows}, hashlib.sha256(raw).hexdigest()


def bind_priorities(rows, catalog):
    for row in rows:
        if row['decision'] in {'component_only', 'not_reproduced_high_cost'}:
            row['priority'] = catalog[row['catalog_key']]['priority']
            row['priority_basis'] = '采用已核查catalog优先级；优先级不等于实现或能力验收'
        else:
            row['priority'] = 'P1'
            row['priority_basis'] = '本轮明确批准的历史线索审查优先级；不代表通过收录门槛或接收实现'


def validate_reviews(rows, catalog, root=ROOT):
    original, _ = approved_input(root)
    require(len(rows) == 25 and {r['id'] for r in rows} == set(original), 'review must cover exactly the 25 approved identities')
    for row in rows:
        decision = row['decision']
        require(row.get('priority') in {'P0', 'P1', 'P2'}, 'explicit review priority required')
        require(decision in DECISIONS and row.get('reason') and row.get('sources') and row.get('method_review'),
                f"{row['id']}: explicit method, primary sources and disposition required")
        require(row.get('review_done') is True or decision == 'archived_source_exception', 'unread items cannot silently count as reviewed')
        require(row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False,
                'no automatic retries or implementation queue')
        require(row.get('paper_url') == f"https://arxiv.org/abs/{row['id']}v1", 'canonical v1 identity required')
        if decision != 'archived_source_exception':
            require(row.get('title') and row.get('first_author') and row.get('first_author_affiliation'), 'verified identity/institution required')
            published = datetime.fromisoformat(row['published_at'].replace('Z', '+00:00'))
            require(published.tzinfo is not None, 'exact original publication UTC timestamp required')
        if decision in {'component_only', 'not_reproduced_high_cost'}:
            require(row.get('cost_assessment'), 'cost gate required before implementation or deferral')
            item = catalog[row['catalog_key']]
            require(row['priority'] == item['priority'], 'catalog/review priority binding')
            require(item['paper_url'] == row['paper_url'] and item['domain'] == row['domain']
                and item['published_at'] == row['published_at']
                and all(item[f] == row[f] for f in ('title', 'first_author', 'first_author_affiliation')),
                'catalog/review identity binding')
            require(item.get('adapter') is None and item.get('promotion_eligible') is False
                and item.get('evolve_integrated') is False and item.get('automatic_retry') is False
                and item.get('automatic_implementation_queue') is False, 'catalog non-promotion boundary')
            require(item['detail_path'] == f"{row['domain']}/{row['id']}-{row['catalog_key']}/README.md", 'canonical detail path required')
            if decision == 'component_only':
                require(row.get('accepted_for_implementation') is True and row.get('implemented') is True
                    and item.get('implementation_status') == 'component_only' and item.get('local_operator')
                    and item.get('local_command') and item.get('evaluation_tier') == 'l1_mechanism'
                    and item.get('diagnostic_only') is True, 'implemented L1 component entry required')
            else:
                require(row.get('accepted_for_implementation') is False and row.get('implemented') is False
                    and item.get('implementation_status') == 'deferred_high_cost' and not item.get('local_operator')
                    and not item.get('local_command') and not item.get('requires_gpu_validation')
                    and '不复现（审查 DONE）' in item.get('deferral_reason', ''), 'terminal high-cost review only')
        else:
            require(row.get('accepted_for_implementation') is False and row.get('implemented') is False,
                    'not-selected/exception/duplicate cannot count as new implementation')


def build(review_paths, root=ROOT):
    ledger_path = root/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    require(not any(b['batch'] == BATCH for b in ledger['batches']), 'batch already exists; refuse accepted-state overwrite')
    inputs, input_hash = approved_input(root)
    rows = []
    for path in review_paths:
        payload = json.loads(path.read_text())
        rows.extend(payload if isinstance(payload, list) else payload['reviews'] if 'reviews' in payload else payload['records'])
    rows.sort(key=lambda r: r['id'])
    catalog = catalogue()
    bind_priorities(rows, catalog)
    validate_reviews(rows, catalog, root)
    counts = dict(Counter(row['decision'] for row in rows))
    components = [r for r in rows if r['decision'] == 'component_only']
    gpu_count = sum(catalog[r['catalog_key']].get('requires_gpu_validation') is True for r in components)
    for row in rows:
        row['original_lead_title'] = inputs[row['id']]['title']
        if row['decision'] == 'component_only':
            row.update(component_implemented=False, component_accepted=False,
                       implementation_status='component_validation_pending')
    counts.update(reviewed_input_identities=25, components_pending_verification=len(components),
        components_accepted=0, gpu_components_pending=gpu_count, new_first_publications=0,
        capability_reproductions_claimed=0)
    common = {'schema_version': 1, 'batch': BATCH, 'date': '2026-10-25',
        'scope_kind': 'explicitly-approved-historical-google-conference-leads', 'selected_scope_complete': False,
        'delivery_status': 'pending_component_verification', 'review_scope_closed': True,
        'all_sources_exhaustive': False, 'review_watermark_advanced': False,
        'review_watermark': {'before': '2026-10-15', 'after': '2026-10-15'}}
    scope = {**common, 'input_artifact': INPUT_REL.as_posix(), 'input_sha256': input_hash,
        'fixed_input_identities': sorted(inputs), 'fixed_component_keys': sorted(r['catalog_key'] for r in components),
        'counts': counts, 'papers': rows,
        'limitations': ['Exactly the approved25 historical identities, not allGoogle publications or the four prior unresolved event-page links.',
            'High-cost review DONE does not mean implemented; accepted L1 components require separate frozen-source execution.',
            'Source exceptions, if any, are explicit archived dispositions, not successful full-text reviews.',
            'No pretrained capability comparison or evolve promotion; global review watermark is unchanged.']}
    candidates = []
    for original in rows:
        row = deepcopy(original)
        decision = row['decision']
        if decision in {'component_only', 'not_reproduced_high_cost'}:
            item = catalog[row['catalog_key']]
            row.update(key=row['catalog_key'], doc=item['detail_path'], detail_path=item['detail_path'],
                       catalog_detail=item['detail_path'])
        if decision == 'component_only':
            row.update(status='accepted-unimplemented', implementation_status='component_validation_pending',
                component_implemented=False, component_accepted=False, resolution='component_pending_verification')
        elif decision == 'not_reproduced_high_cost':
            row.update(status='deferred', implementation_status='deferred_high_cost', resolution='not_reproduced_high_cost')
        else:
            row.update(status='rejected', implementation_status='not_implemented', resolution=decision)
        row.update(review_artifact='research-audits/google-emnlp25-closure/task-scope.json',
                   promotion_eligible=False, evolve_integrated=False)
        candidates.append(row)
    batch = {**common, 'source_artifact': 'research-audits/google-emnlp25-closure/README.md',
        'counts': counts, 'candidates': candidates}
    updated = deepcopy(ledger)
    updated['batches'].append(batch)
    for path, value in ((root/AUDIT_REL/'task-scope.json', scope), (root/AUDIT_REL/'review-decisions.json', rows),
                        (ledger_path, updated)):
        write(path, value)
    return counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reviews', type=Path, nargs='+', required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.reviews), ensure_ascii=False))
