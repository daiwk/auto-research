#!/usr/bin/env python3
"""Validate actual teacher/fake/generator evidence before a sanitized receipt."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['scripts/run_data_space_iteration.py',
           'src/auto_research/foundation/data_space_iteration.py',
           'src/auto_research/multimodal/data.py']


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def summarize(report):
    protocol, dataset = report.get('protocol', {}), report.get('dataset', {})
    if (report.get('paper_id') != '2610.12102' or report.get('diagnostic_only') is not True
            or protocol.get('test_read') is not False or dataset.get('test_read') is not False
            or dataset.get('split_source') != 'official_train_only'
            or protocol.get('inception_fid_evaluated') is not False):
        raise ValueError('train-only actual DMD diagnostic, not paper FID, required')
    required = {'teacher_trained': True, 'teacher_frozen_during_dmd': True,
        'generator_refinements': 4, 'fake_updates_per_generator': 4, 'dmd_beta': [2.5, 1.],
        'dmd_weight': 1., 'adam_betas': [0., .95], 'ema_decay': .9999, 'evaluation_uses_ema': True}
    if any(protocol.get(key) != value for key, value in required.items()):
        raise ValueError('defining shared-generator alternating-DMD/EMA protocol missing')
    if len(dataset.get('revision', {})) != 5 or any('test' in key for key in dataset['revision']):
        raise ValueError('all five fixed official train-file hashes required')
    rows = report.get('rows', [])
    pairs, metrics = {}, {}
    for row in rows:
        seed, recipe = row['seed'], row['recipe']
        if recipe not in ('flow-renoise', 'data-space') or (seed, recipe) in pairs:
            raise ValueError('duplicate or unknown paired recipe')
        teacher = row['teacher']
        if (teacher['steps'] < 10 or not teacher.get('checkpoint_sha256')
                or not finite(teacher['validation_velocity_mse_before'])
                or not finite(teacher['validation_velocity_mse_after'])
                or teacher['validation_velocity_mse_before'] == teacher['validation_velocity_mse_after']):
            raise ValueError('real teacher training and measured held-out flow loss required')
        steps, trace = row['generator_steps'], row['trace']
        if (steps < 4 or row['fake_steps'] != 4 * steps or len(trace) != steps
                or row.get('generator_parameter_changed') is not True
                or row.get('fake_parameter_changed') is not True):
            raise ValueError('actual generator and fourfold fake updates required')
        for index, event in enumerate(trace):
            if (event['refinement'] != index % 4 or len(event['fake_losses']) != 4
                    or len(event['fake_gradient_norms']) != 4
                    or not all(finite(x) for x in [*event['fake_losses'], *event['fake_gradient_norms'],
                            event['generator_loss'], event['generator_gradient_norm']])):
                raise ValueError('invalid actual prefix/fake-update or finite-gradient trace')
        if not any(event['generator_gradient_norm'] > 0 for event in trace):
            raise ValueError('no generator gradient observed')
        evaluation = row['evaluation']
        if [x['nfe'] for x in evaluation] != [1, 2, 3, 4]:
            raise ValueError('evaluate all four EMA generation prefixes')
        if any(not finite(x['pixel_feature_frechet_distance'])
               or x['pixel_feature_frechet_distance'] < 0 for x in evaluation):
            raise ValueError('invalid finite pixel-feature distance')
        pairs[seed, recipe] = row
        metrics[f'{recipe}_seed{seed}'] = {'teacher_validation_velocity_mse_before': teacher['validation_velocity_mse_before'],
            'teacher_validation_velocity_mse_after': teacher['validation_velocity_mse_after'],
            'teacher_pixel_feature_frechet_distance': teacher['pixel_feature_frechet_distance'],
            'generator_steps': steps, 'fake_steps': 4 * steps,
            **{f'pixel_feature_frechet_nfe{x["nfe"]}': x['pixel_feature_frechet_distance'] for x in evaluation}}
    seeds = sorted({seed for seed, _ in pairs})
    if not seeds or len(pairs) != 2 * len(seeds):
        raise ValueError('both matched recipes required for every seed; do not drop failed seeds')
    for seed in seeds:
        a, b = (pairs[seed, recipe] for recipe in ('flow-renoise', 'data-space'))
        if a['teacher'] != b['teacher'] or a['generator_steps'] != b['generator_steps']:
            raise ValueError('paired frozen teacher and training budgets differ')
    return metrics, seeds


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    args = parser.parse_args()
    report = json.loads(args.input.read_text())
    metrics, seeds = summarize(report)
    commit = subprocess.check_output(['git', 'rev-parse', args.source_commit], cwd=ROOT, text=True).strip()
    hashes = {s: hashlib.sha256(subprocess.check_output(['git', 'show', f'{commit}:{s}'], cwd=ROOT)).hexdigest()
              for s in SOURCES}
    metric_path = 'docs/foundation-models/2610.12102-data-space-iteration/metrics/cifar10-a100.json'
    receipt_path = 'docs/gpu-validations/data-space-iteration-a100-20261011.json'
    limitations = ['small from-scratch two-scale U-Net, not SongUNet-55M or ImageNet SiT-XL/2',
        'pixel average-pool feature Frechet distance is not Inception FID; no paper-number comparison',
        'bounded teacher and distillation budgets; retain every negative recipe/seed',
        'EMA decay retained at 0.9999; short training EMA can stay close to initialization',
        'core-mechanism GPU diagnostic, not formal image-generation quality improvement']
    dataset = {'id': 'CIFAR-10', 'revision': report['dataset']['revision'],
               'split_provenance': report['dataset']}
    checkpoint = {**report['checkpoint'], 'revision': {str(row['seed']): row['teacher']['checkpoint_sha256']
        for row in report['rows'] if row['recipe'] == 'data-space'}}
    metric = {'schema_version': 2, 'manifest_ref': 'foundation-models:data-space-iteration',
        'method': 'data-space-iteration', 'dataset': 'CIFAR-10', 'seeds': seeds, 'metrics': metrics,
        'evaluation_protocol': {'tier': 'l1_mechanism', 'diagnostic_only': True,
            'formal_comparison': False, 'test_read': False, 'seeds': seeds,
            'claim_policy': 'real alternating DMD mechanism, no benchmark improvement claim'},
        'runtime_details': report, 'limitations': limitations,
        'provenance': {'original_code_commit': commit, 'artifact_path': metric_path,
            'executed_source_sha256': hashes, 'dataset_fingerprint': hashlib.sha256(
                json.dumps(report['dataset'], sort_keys=True).encode()).hexdigest()}}
    one = report['rows'][0]
    command = ['python', 'scripts/run_data_space_iteration.py', '--data', 'data/cifar10', '--offline',
        '--output', 'runs/data-space-cifar.json', '--seeds', ','.join(map(str, seeds)),
        '--train-examples', str(report['dataset']['train_examples']),
        '--validation-examples', str(report['dataset']['validation_examples']),
        '--teacher-steps', str(one['teacher']['steps']), '--distill-steps', str(one['generator_steps']),
        '--width', str(report['checkpoint']['width']), '--depth', str(report['checkpoint']['depth'])]
    receipt = {'schema_version': 1, 'adapter_key': 'data-space-iteration', 'validated_at': '2026-10-11',
        'accelerator': {'vendor': 'NVIDIA', 'model': report['accelerator']}, 'command': command,
        'dataset': dataset, 'checkpoint': checkpoint, 'result': 'passed', 'metrics': metrics,
        'evaluation_tier': 'l1_mechanism', 'limitations': limitations, 'seeds': seeds,
        'executed_source_sha256': hashes, 'provenance': {'commit': commit, 'artifact_path': receipt_path,
            'metrics_artifact': metric_path, 'checkpoint_committed': False}}
    for relative, payload in ((metric_path, metric), (receipt_path, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
