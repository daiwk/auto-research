"""Offline source accounting for two recent overlaps and a Google historical backfill."""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from build_oct23_source_audit import directory_deltas, identity, require, timestamp, validate_capture, write

ROOT = Path(__file__).resolve().parents[1]
BATCH = '2026-10-25-priority-backfill-components'
AUDIT_REL = Path('docs/research-audits/oct25-priority-components')
SELECTED = {'minimal-edit-opd': ('post-training', '2610.30231'),
            'inside-jepa': ('foundation-models', '2610.31194'),
            'group-dpo': ('post-training', '2604.15602')}
PRIORITY_ORGS = {'minimal-edit-opd': ['Meta'], 'group-dpo': ['Google', 'Google DeepMind']}


def build_reports(receipts, baseline, supplied, catalog, raw_sha256, additional):
    pages = validate_capture(receipts)
    versions = {p['source']: [r['id'] for r in p['records']] for p in pages}
    require(versions == baseline['bulletin_ids_by_category'], 'unchanged Oct23 category versions/order required')
    observed = {}
    for page in pages:
        for item in page['records']:
            row = observed.setdefault(identity(item['id']), {'versions': set(), 'categories': set(), 'kinds': set()})
            row['versions'].add(item['id'])
            row['categories'].add(page['source'])
            row['kinds'].add(item['entry_kind'])
    previous_end = max(baseline['retrieval_receipts'], key=lambda r: timestamp(r['checked_at']))['checked_at']
    selected = []
    for key, (domain, paper_id) in SELECTED.items():
        item = catalog[key]
        historical = key == 'group-dpo'
        require(item['domain'] == domain and item['paper_url'] == f'https://arxiv.org/abs/{paper_id}v1', 'catalog exact identity')
        require(timestamp(item['published_at']) <= timestamp(previous_end), 'no new-first-publication claim')
        require(historical or paper_id in observed, 'recent selected paper must be in actual bulletin')
        evidence = observed.get(paper_id, {'versions': [], 'categories': [], 'kinds': []})
        selected.append({'id': paper_id, 'key': key, 'domain': domain, 'title': item['title'],
            'paper_url': item['paper_url'], 'detail_path': item['detail_path'], 'priority': item['priority'],
            'first_author': item['first_author'], 'first_author_affiliation': item['first_author_affiliation'],
            'verified_priority_organizations': PRIORITY_ORGS.get(key, []), 'original_published_at': item['published_at'],
            'intake_class': 'historical-official-conference-backfill' if historical else 'same-announcement-overlap-backfill',
            'first_publication_after_baseline_capture': False, 'observed_versions': sorted(evidence['versions']),
            'bulletin_categories': sorted(evidence['categories']), 'bulletin_entry_kinds': sorted(evidence['kinds']),
            'status': 'accepted-unimplemented', 'implementation_status': 'component_validation_pending',
            'delivery_status': 'pending_component_verification', 'component_implemented': False, 'component_accepted': False,
            'review_done': False, 'full_experiment_review_done': True, 'full_experiment_status': item['full_experiment_status'],
            'cost_assessment': item['cost_assessment'], 'requires_gpu_validation': True,
            'automatic_retry': False, 'automatic_implementation_queue': False, 'promotion_eligible': False, 'evolve_integrated': False})
    deltas = directory_deltas(receipts, supplied)
    counts = {'selected_papers': 3, 'components_pending_verification': 3, 'recent_overlap_backfills': 2,
        'historical_official_source_backfills': 1, 'new_first_publications_after_previous_capture': 0,
        'category_entries_including_crosslists_and_replacements': sum(len(p['records']) for p in pages),
        'unique_bulletin_identities': len(observed), 'snapshot_added_base_identities_not_new_paper_count': 0,
        'snapshot_added_version_strings_not_revision_count': 0,
        'section_entry_counts': dict(Counter(r['entry_kind'] for p in pages for r in p['records'])),
        'official_directory_delta_unknown': sum(not d['delta_known'] for d in deltas)}
    common = {'schema_version': 1, 'batch': BATCH, 'delivery_status': 'pending_component_verification',
        'all_sources_exhaustive': False, 'review_watermark_advanced': False}
    scope = {**common, 'fixed_component_keys': sorted(SELECTED), 'reference_only_keys': [],
        'selected_scope_complete': False, 'papers': selected, 'additional_dispositions': additional}
    coverage = {**common, 'checked_on': '2026-10-25', 'scope_kind': 'priority-fulltext-and-conference-backfill',
        'actual_announced_on': '2026-10-23', 'new_announcement_batch_available': False,
        'raw_capture_sha256': raw_sha256, 'baseline': '../oct24-overlap-components/source-coverage.json',
        'baseline_raw_sha256': baseline['raw_capture_sha256'], 'baseline_last_checked_at': previous_end,
        'all_eight_bulletins_complete': True, 'full_bulletin_full_text_review_complete': False,
        'review_watermark': {'before': '2026-10-15', 'after': '2026-10-15'}, 'counts': counts,
        'bulletin_ids_by_category': versions, 'retrieval_receipts': [{k: v for k, v in r.items() if k != 'records'} for r in receipts],
        'official_directory_deltas': deltas, 'additional_dispositions': additional,
        'limitations': ['No new Oct25 arXiv bulletin or new first publication is claimed; the actual eight pages still show Oct23.',
            'Two papers are recent overlap backfills; GroupDPO is an April historical backfill from an independently checked Google conference page.',
            'Directory retrieval failures remain unknown/null, not zero additions or a finding that an organization has no new papers.',
            'A bounded DeepMind directory comparison and selected author-affiliation checks are not institutional or all-web exhaustiveness.',
            'L1 component acceptance is separate from high-cost full experiment review DONE/not reproduced; no capability or evolve promotion.',
            'Global review watermark remains 2026-10-15; this fixed delivery does not close a whole-window review.']}
    candidates = [{**row, 'doc': row['detail_path'], 'catalog_key': row['key'], 'catalog_detail': row['detail_path'],
        'track': 'foundation-model' if row['domain'] == 'foundation-models' else 'post-training',
        'resolution': 'component_pending_verification', 'review_artifact': 'research-audits/oct25-priority-components/task-scope.json',
        'full_text_review': {'scope': 'defining-method-resource-and-affiliation-review', 'full_article_read': False},
        'source_provenance': [{'source_url': row['paper_url'], 'source_kind': 'primary-method-resource-affiliation-review',
                               'organization': row['first_author_affiliation']}],
        'reason': '固定补漏范围，等待冻结CPU/A100验收；完整高成本实验不复现，不提前声明能力。'} for row in selected]
    batch = {**common, 'date': '2026-10-25', 'scope_kind': coverage['scope_kind'],
        'source_artifact': 'research-audits/oct25-priority-components/README.md', 'selected_scope_complete': False,
        'counts': counts, 'additional_dispositions': additional, 'candidates': candidates}
    return coverage, scope, batch


def build(directory, additional_path, root=ROOT):
    ledger_path = root/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    require(not any(b['batch'] == BATCH for b in ledger['batches']), 'batch already exists; refuse accepted-state overwrite')
    raw = (directory/'retrieval.json').read_bytes()
    baseline = json.loads((root/'docs/research-audits/oct24-overlap-components/source-coverage.json').read_text())
    supplied = [json.loads((directory/f'{name}-delta.json').read_text()) for name in ('google', 'meta', 'google-deepmind')]
    catalog = {key: json.loads((root/f'src/auto_research/paper_specs/catalog/{domain}/{key}.json').read_text())
               for key, (domain, _) in SELECTED.items()}
    additional = json.loads(additional_path.read_text())
    coverage, scope, batch = build_reports(json.loads(raw), baseline, supplied, catalog, hashlib.sha256(raw).hexdigest(), additional)
    updated = deepcopy(ledger)
    updated['batches'].append(batch)
    for path, value in ((root/AUDIT_REL/'source-coverage.json', coverage), (root/AUDIT_REL/'task-scope.json', scope), (ledger_path, updated)):
        write(path, value)
    return coverage['counts']


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('capture_directory', type=Path)
    parser.add_argument('--additional-dispositions', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.capture_directory, args.additional_dispositions), ensure_ascii=False))
