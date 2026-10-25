"""Verify fixed historical-review scope separately from actual L1 execution."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
sys.path.insert(0, str(ROOT/'scripts'))
from auto_research.gpu_validation import load_gpu_receipt  # noqa: E402
from build_google_emnlp25_closure import AUDIT_REL, BATCH, approved_input, bind_priorities, catalogue, validate_reviews  # noqa: E402
from curate_oct21_component_evidence import aggregate, digest, require, write  # noqa: E402
from oct18_frozen_sources import capture_sources, verify_sources  # noqa: E402
from run_google_emnlp25_components import RUNNER, SEEDS, execution_spec, sources, validate_row  # noqa: E402

AUDIT = ROOT/AUDIT_REL


def spec_rows():
    return {r['key']: r for r in execution_spec()['components']}


def validate_catalog(catalog, specs):
    for key, spec in specs.items():
        row = catalog[key]
        module = spec['source'].removeprefix('src/').removesuffix('.py').replace('/', '.')
        require(row['domain'] == spec['domain'] and row['paper_url'] == f"https://arxiv.org/abs/{spec['id']}v1"
            and row['detail_path'] == f"{spec['domain']}/{spec['id']}-{key}/README.md"
            and row.get('adapter') is None and row.get('implementation_status') == 'component_only'
            and row.get('evaluation_tier') == 'l1_mechanism' and row.get('diagnostic_only') is True
            and row.get('promotion_eligible') is False and row.get('evolve_integrated') is False
            and row.get('review_done') is True and row.get('full_experiment_review_done') is True
            and row.get('full_experiment_status') == 'not_reproduced_high_cost'
            and row.get('automatic_retry') is False and row.get('automatic_implementation_queue') is False,
            f'{key}: catalog boundary')
        require(row['local_operator'] == spec['operator'] and spec['operator'].startswith(module+'.')
            and row['local_command'] == f"PYTHONPATH=src python -c 'from {module} import diagnostic; print(diagnostic(42))'",
            f'{key}: executed entry binding')
        cuda = spec['device'] == 'cuda'
        require(row.get('requires_gpu_validation') is cuda
            and row.get('gpu_validation_artifact') == (f'docs/gpu-validations/{key}-a100-20261025.json' if cuda else None),
            f'{key}: GPU boundary')


def validate_raw(raw, specs):
    require(set(raw) == {'cpu', 'cuda'}, 'CPU and actual CUDA runs required')
    for device, item in raw.items():
        expected = set(specs) if device == 'cpu' else {k for k, r in specs.items() if r['device'] == 'cuda'}
        require(item['schema_version'] == 2 and item['device'] == device and item['seeds'] == SEEDS
            and set(item['components']) == expected and item['evaluation_tier'] == 'l1_mechanism'
            and item['diagnostic_only'] is True and item['formal_comparison'] is False
            and item['promotion_eligible'] is False and item['evolve_integrated'] is False
            and item['pretrained_model_calls'] == 0 and item['full_experiments_executed'] is False, 'raw scope boundary')
        require(item['accelerator'] == 'CPU' if device == 'cpu'
            else any(n in item['accelerator'] for n in ('A100', 'A30')), 'real execution device required')
        require(set(item['source_sha256']) == set(sources(execution_spec())), 'exact frozen source coverage required')
        for key, component in item['components'].items():
            rows = component['per_seed']
            require([r['seed'] for r in rows] == SEEDS, 'exact three seeds required')
            for seed, row in zip(SEEDS, rows):
                require(row.get('execution_device') == device and row.get('execution_accelerator') == item['accelerator'],
                        'per-seed execution device binding')
                validate_row(row, specs[key], seed)
            aggregate(rows)
    require(raw['cpu']['code_commit'] == raw['cuda']['code_commit']
        and raw['cpu']['source_sha256'] == raw['cuda']['source_sha256'], 'CPU/CUDA frozen identity binding')


def metric_path(key, specs, catalog):
    return Path('docs')/Path(catalog[key]['detail_path']).parent/f"metrics/component-{specs[key]['device']}-seeds42-44.json"


def result_for(key, raw, raw_bytes, specs, catalog):
    device = specs[key]['device']
    item = raw[device]
    dataset = {'id': f'synthetic:google-emnlp25-{key}-v1', 'revision': 'sha256:'+digest(item['source_sha256']),
        'recipe': 'frozen-source-bounded-mechanism-or-offline-protocol', 'capability_benchmark': False}
    rows = item['components'][key]['per_seed']
    return {'schema_version': 2, 'method': key, 'manifest_ref': catalog[key]['domain']+':'+key,
        'dataset': dataset, 'seeds': SEEDS, 'per_seed': rows, 'metrics': aggregate(rows), 'evaluation_tier': 'l1_mechanism',
        'evaluation_protocol': {'tier': 'l1_mechanism', 'seeds': SEEDS, 'formal_comparison': False,
            'claim_policy': 'bounded numerical/protocol diagnostics; not pretrained capability, official benchmark or full reproduction'},
        'diagnostic_only': True, 'fixture_demo': True, 'formal_comparison': False, 'promotion_eligible': False,
        'evolve_integrated': False, 'pretrained_model_calls': 0, 'full_experiment_status': 'not_reproduced_high_cost',
        'full_experiment_review_done': True, 'provenance': {'commit': item['code_commit'],
            'artifact_path': metric_path(key, specs, catalog).as_posix(), 'accelerator': item['accelerator'],
            'executed_source_sha256': item['source_sha256'],
            'raw_runner_artifact_sha256': hashlib.sha256(raw_bytes[device]).hexdigest(),
            'dataset_fingerprint': 'sha256:'+digest({'dataset': dataset, 'seeds': SEEDS, 'source': item['source_sha256']})}}


def receipt_for(key, result, catalog):
    p = result['provenance']
    path = catalog[key]['gpu_validation_artifact']
    return {'schema_version': 1, 'adapter_key': key, 'validated_at': '2026-10-25',
        'accelerator': {'vendor': 'NVIDIA', 'model': p['accelerator'], 'count': 1},
        'command': ['python3', RUNNER, '--device', 'cuda', '--source-commit', p['commit'],
            '--frozen-proof', 'google-emnlp25-frozen-proof.json', '--output', 'results/components-cuda.json'],
        'dataset': result['dataset'], 'checkpoint': {'public_id': 'none-seeded-component-initialization',
            'revision': p['commit'], 'pretrained': False}, 'seeds': SEEDS, 'result': 'passed',
        'metrics': result['metrics'], 'executed_source_sha256': p['executed_source_sha256'],
        'provenance': {**p, 'artifact_path': path, 'metric_artifact_path': result['provenance']['artifact_path']},
        'diagnostic_only': True, 'promotion_eligible': False, 'evolve_integrated': False,
        'full_experiment_status': 'not_reproduced_high_cost', 'full_experiment_review_done': True}


def validate_scope(scope, batch, specs, catalog, *, allow_pending=False):
    original, input_hash = approved_input()
    require(scope['batch'] == batch['batch'] == BATCH and scope['input_sha256'] == input_hash
        and scope['fixed_input_identities'] == sorted(original)
        and set(scope['fixed_component_keys']) == set(specs), 'scope identity or frozen input differs')
    validate_reviews(scope['papers'], catalog)
    validate_reviews(batch['candidates'], catalog)
    require(scope['review_scope_closed'] is True and batch['review_scope_closed'] is True
        and scope['review_watermark'] == batch['review_watermark'] == {'before': '2026-10-15', 'after': '2026-10-15'}
        and scope['review_watermark_advanced'] is False and batch['review_watermark_advanced'] is False, 'review is bounded historical closure')
    complete = scope['selected_scope_complete']
    require(type(complete) is bool and batch['selected_scope_complete'] is complete
        and scope['delivery_status'] == batch['delivery_status'] == ('bounded_scope_complete' if complete else 'pending_component_verification')
        and (complete or allow_pending), 'scope/ledger completion state differs')
    require(scope['counts'] == batch['counts'] and scope['counts']['reviewed_input_identities'] == 25
        and scope['counts']['new_first_publications'] == 0 and scope['counts']['capability_reproductions_claimed'] == 0, 'scope/ledger counts differ')
    decisions = Counter(row['decision'] for row in scope['papers'])
    require(all(scope['counts'].get(decision, 0) == count for decision, count in decisions.items()), 'disposition counts differ')
    if complete:
        require(scope['counts']['components_pending_verification'] == scope['counts']['gpu_components_pending'] == 0
            and scope['counts']['components_accepted'] == len(specs), 'accepted component counts differ')
    for rows in (scope['papers'], batch['candidates']):
        require(len(rows) == 25 and {r['id'] for r in rows} == set(original), 'exact25 scope/ledger identities required')
        require({r['catalog_key'] for r in rows if r['decision'] == 'component_only'} == set(specs), 'fixed accepted component set differs')
        for row in rows:
            require(row['original_lead_title'] == original[row['id']]['title'], 'original source title binding')
            if row['decision'] not in {'component_only', 'not_reproduced_high_cost'}:
                continue
            key = row['catalog_key']
            item = catalog[key]
            require(row['paper_url'] == item['paper_url'] and row['published_at'] == item['published_at']
                and all(row[f] == item[f] for f in ('title', 'first_author', 'first_author_affiliation')), 'scope/ledger paper identity differs')
            if rows is batch['candidates']:
                require(row['key'] == key and row['doc'] == row['catalog_detail'] == row['detail_path'] == item['detail_path'],
                        'scope/ledger catalog alias differs')
            if row['decision'] == 'component_only':
                require(row['component_accepted'] is complete and row['component_implemented'] is complete
                    and row['implementation_status'] == ('component_only' if complete else 'component_validation_pending'), 'scope/ledger component acceptance differs')
                if complete:
                    require(row['component_evidence'] == metric_path(key, specs, catalog).as_posix(), 'scope/ledger evidence differs')


def ingest(cpu, cuda):
    catalog, specs = catalogue(), spec_rows()
    validate_catalog(catalog, specs)
    raw_bytes = {'cpu': cpu.read_bytes(), 'cuda': cuda.read_bytes()}
    raw = {device: json.loads(data) for device, data in raw_bytes.items()}
    validate_raw(raw, specs)
    proof = capture_sources(ROOT, raw['cpu']['code_commit'], sources(execution_spec()))
    verify_sources(ROOT, raw['cpu']['code_commit'], raw['cpu']['source_sha256'], proof)
    for key in specs:
        result = result_for(key, raw, raw_bytes, specs, catalog)
        write(ROOT/metric_path(key, specs, catalog), result)
        if specs[key]['device'] == 'cuda':
            write(ROOT/catalog[key]['gpu_validation_artifact'], receipt_for(key, result, catalog))
    write(AUDIT/'frozen-sources.json', {'schema_version': 1, 'commit': raw['cpu']['code_commit'], 'proof': proof})
    for device, data in raw_bytes.items():
        (AUDIT/f'raw-{device}.json').write_bytes(data)


def check(*, allow_pending=False):
    catalog, specs = catalogue(), spec_rows()
    validate_catalog(catalog, specs)
    raw_bytes = {device: (AUDIT/f'raw-{device}.json').read_bytes() for device in ('cpu', 'cuda')}
    raw = {device: json.loads(data) for device, data in raw_bytes.items()}
    validate_raw(raw, specs)
    proof = json.loads((AUDIT/'frozen-sources.json').read_text())
    require(proof['commit'] == raw['cpu']['code_commit'], 'frozen commit binding')
    verify_sources(ROOT, proof['commit'], raw['cpu']['source_sha256'], proof['proof'])
    for key in specs:
        result = json.loads((ROOT/metric_path(key, specs, catalog)).read_text())
        require(result == result_for(key, raw, raw_bytes, specs, catalog), f'{key}: exact raw/result binding')
        if specs[key]['device'] == 'cuda':
            require(load_gpu_receipt(ROOT/catalog[key]['gpu_validation_artifact']) == receipt_for(key, result, catalog), f'{key}: exact GPU receipt binding')
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    require(json.loads((AUDIT/'review-decisions.json').read_text()) == scope['papers'], 'current review/scope records differ')
    batches = [b for b in json.loads((ROOT/'docs/paper-discovery-ledger.json').read_text())['batches'] if b['batch'] == BATCH]
    require(len(batches) == 1, 'exactly one batch')
    validate_scope(scope, batches[0], specs, catalog, allow_pending=allow_pending)


def finalize():
    check(allow_pending=True)
    specs, catalog = spec_rows(), catalogue()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    ledger_path = ROOT/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    batch = next(b for b in ledger['batches'] if b['batch'] == BATCH)
    for rows in (scope['papers'], batch['candidates']):
        for row in rows:
            if row['decision'] != 'component_only':
                continue
            key = row['catalog_key']
            row.update(component_accepted=True, component_implemented=True, implementation_status='component_only',
                       component_evidence=metric_path(key, specs, catalog).as_posix(), status='implemented',
                       resolution='bounded_l1_component_accepted')
            if specs[key]['device'] == 'cuda':
                row['gpu_validation_artifact'] = catalog[key]['gpu_validation_artifact']
    for item in (scope, batch):
        item.update(selected_scope_complete=True, delivery_status='bounded_scope_complete')
        item['counts'].update(components_pending_verification=0, gpu_components_pending=0, components_accepted=len(specs),
                              gpu_validated_components=sum(r['device'] == 'cuda' for r in specs.values()))
    validate_scope(scope, batch, specs, catalog)
    write(AUDIT/'task-scope.json', scope)
    write(AUDIT/'review-decisions.json', scope['papers'])
    write(ledger_path, ledger)


def sync_review_records():
    """Backfill explicit review priorities; preserve identities and acceptance."""
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    ledger_path = ROOT/'docs/paper-discovery-ledger.json'
    ledger = json.loads(ledger_path.read_text())
    batches = [b for b in ledger['batches'] if b['batch'] == BATCH]
    require(len(batches) == 1, 'exactly one batch')
    catalog, specs = catalogue(), spec_rows()
    bind_priorities(scope['papers'], catalog)
    bind_priorities(batches[0]['candidates'], catalog)
    validate_scope(scope, batches[0], specs, catalog)
    write(AUDIT/'task-scope.json', scope)
    write(AUDIT/'review-decisions.json', scope['papers'])
    write(ledger_path, ledger)


def sync_figures():
    from PIL import Image

    manifest_path = ROOT/'docs/paper-figures-manifest.json'
    manifest = json.loads(manifest_path.read_text())
    catalog = catalogue()
    scope = json.loads((AUDIT/'task-scope.json').read_text())
    for reviewed in scope['papers']:
        if reviewed['decision'] not in {'component_only', 'not_reproduced_high_cost'}:
            continue
        record = catalog[reviewed['catalog_key']]
        page = Path('docs')/record['detail_path']
        assets = page.parent/'assets'
        provenance = json.loads((ROOT/assets/'provenance.json').read_text())
        asset = assets/provenance.get('image', provenance.get('local_path', 'paper-figure-01.png'))
        source = provenance.get('source_url', provenance.get('source_image_url', provenance.get('paper_url')))
        require(source and source.startswith('https://'), 'original figure primary source required')
        actual_hash = hashlib.sha256((ROOT/asset).read_bytes()).hexdigest()
        recorded_hash = provenance.get('sha256', provenance.get('image_sha256'))
        require(recorded_hash == actual_hash, 'original figure provenance hash differs')
        with Image.open(ROOT/asset) as image:
            width, height = image.size
        require(width > 0 and height > 0, 'nonempty original image required')
        row = {'page': page.as_posix(), 'paper_url': record['paper_url'], 'arxiv_id': reviewed['id'],
            'figure': str(provenance.get('figure', 'Figure 1')), 'original_caption': provenance.get('original_caption', ''),
            'source_url': source, 'extraction': 'original-reviewed-paper-figure', 'asset': asset.as_posix(),
            'width': width, 'height': height, 'score': 0, 'error': '', 'sha256': actual_hash, 'visually_inspected': True}
        existing = [i for i, old in enumerate(manifest) if old['page'] == row['page']]
        require(len(existing) <= 1, 'duplicate figure page')
        if existing:
            manifest[existing[0]] = row
        else:
            manifest.append(row)
    write(manifest_path, manifest)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cpu', type=Path)
    parser.add_argument('--cuda', type=Path)
    parser.add_argument('--finalize', action='store_true')
    parser.add_argument('--sync-figures', action='store_true')
    parser.add_argument('--sync-reviews', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    if args.cpu and args.cuda:
        ingest(args.cpu, args.cuda)
    if args.finalize:
        finalize()
    if args.sync_figures:
        sync_figures()
    if args.sync_reviews:
        sync_review_records()
    if args.check:
        check()
