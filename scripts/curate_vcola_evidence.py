#!/usr/bin/env python3
"""Reject proxy/token-label evidence before curating actual frozen V-CoLA runs."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ['scripts/run_vcola_checkpoint.py', 'src/auto_research/multimodal/vcola.py',
           'src/auto_research/multimodal/vcola_checkpoint.py', 'src/auto_research/multimodal/data.py']
REVISION = 'c202236235762e1c871ad0ccb60c8ee5ba337b9a'
RECIPES = ('dense', 'vcola-50-exit24', 'vcola-25-exit24')


def finite(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def summarize(report):
    protocol = report.get('protocol', {})
    required = {'first_layer_real_delta_state_capture': True, 'state_scores_not_feature_proxy': True,
        'query_probe_window': [0, 4], 'uniqueness_weight': .1, 'merge_temperature': 1.,
        'exit_layer': 24, 'text_original_mrope_preserved': True,
        'no_cache_reference_backend': True, 'prefill_speedup_claim': False,
        'full_generated_answer_accuracy': False, 'inference_gold_read': False,
        'restricted_first_token_only': True, 'test_read': False,
        'sampling_seeds_not_training_replicates': True}
    if (report.get('adapter_key') != 'vcola' or report.get('diagnostic_only') is not True
            or report.get('evaluation_tier') != 'l1_core_mechanism'
            or any(protocol.get(key) != value for key, value in required.items())):
        raise ValueError('actual delta-state, bounded first-token diagnostic protocol required')
    checkpoint = report.get('checkpoint', {})
    if checkpoint.get('id') != 'Qwen/Qwen3.5-9B' or checkpoint.get('revision') != REVISION:
        raise ValueError('fixed official original Qwen3.5-9B required')
    datasets = report.get('datasets', [])
    seeds = [d['sampling_seed'] for d in datasets]
    if not seeds or len(set(seeds)) != len(seeds):
        raise ValueError('unique explicit sampling seeds required')
    for dataset in datasets:
        if (dataset.get('id') != 'CIFAR-10' or dataset.get('test_read') is not False
                or dataset.get('split') != 'fixed_official_train_only_class_tail_holdout'
                or len(dataset.get('revision', {})) != 5
                or set(dataset['revision']) != {f'data_batch_{i}' for i in range(1, 6)}
                or not dataset.get('selected_indices_sha256') or dataset.get('examples', 0) < 1):
            raise ValueError('checksummed official train-only image holdout required')
    groups = {}
    for row in report.get('rows', []):
        key = row['sampling_seed'], row['example_id']
        if row['sampling_seed'] not in seeds or row['recipe'] not in RECIPES:
            raise ValueError('unknown sampling seed/recipe')
        group = groups.setdefault(key, {})
        if row['recipe'] in group:
            raise ValueError('duplicate image/recipe')
        if (type(row.get('restricted_first_token_correct')) is not bool
                or not finite(row.get('dense_backend_relative_error'))
                or not 0 <= row['dense_backend_relative_error'] <= .01
                or not finite(row.get('restricted_choice_probability_mass'))
                or not 0 <= row['restricted_choice_probability_mass'] <= 1
                or not finite(row.get('restricted_choice_kl_to_dense'))
                or row['restricted_choice_kl_to_dense'] < -1e-6):
            raise ValueError('invalid actual first-token/parity evidence')
        forward = row['forward']
        if (forward.get('cache_used') is not False
                or forward.get('original_text_positions_preserved') is not True
                or not finite(forward.get('recurrence_relative_error'))
                or not 0 <= forward['recurrence_relative_error'] <= .03
                or not all(finite(forward.get(k)) for k in ('importance_mean', 'uniqueness_mean', 'score_std'))):
            raise ValueError('missing actual state replay equivalence')
        layers = forward['layers']
        if (len(layers) <= 24 or [layer['layer'] for layer in layers] != list(range(1, len(layers) + 1))
                or layers[0]['visual_tokens'] < 4):
            raise ValueError('all actual original checkpoint layers required')
        text = layers[0]['sequence_tokens'] - layers[0]['visual_tokens']
        if text < 1 or any(layer['sequence_tokens'] != text + layer['visual_tokens'] for layer in layers):
            raise ValueError('text token preservation or physical sequence-length evidence invalid')
        original_visual = layers[0]['visual_tokens']
        if row['recipe'] == 'dense':
            if forward.get('merge') is not None or any(x['visual_tokens'] != original_visual for x in layers):
                raise ValueError('dense matched baseline changed')
        else:
            rate = .5 if row['recipe'] == RECIPES[1] else .25
            merged = max(1, round(original_visual * rate))
            merge = forward.get('merge', {})
            if (merge.get('original_visual_tokens') != original_visual
                    or merge.get('merged_visual_tokens') != merged
                    or len(merge.get('chunk_sizes', [])) != merged
                    or any(x < 1 for x in merge['chunk_sizes'])
                    or sum(merge['chunk_sizes']) != original_visual
                    or any(x['visual_tokens'] != merged for x in layers[1:24])
                    or any(x['visual_tokens'] != 0 for x in layers[24:])):
                raise ValueError('actual layer-one adaptive merge/layer-24 early-exit missing')
        group[row['recipe']] = row
    for dataset in datasets:
        selected = [group for (seed, _), group in groups.items() if seed == dataset['sampling_seed']]
        if len(selected) != dataset['examples'] or any(set(g) != set(RECIPES) for g in selected):
            raise ValueError('every image needs all matched recipes; do not omit failed cases')
    metrics = {}
    for seed in seeds:
        for recipe in RECIPES:
            rows = [g[recipe] for (s, _), g in groups.items() if s == seed]
            metrics[f'{recipe}_sampling_seed{seed}'] = {
                'evaluated_images': len(rows),
                'restricted_first_token_accuracy': sum(r['restricted_first_token_correct'] for r in rows) / len(rows),
                'restricted_choice_probability_mass_mean': sum(r['restricted_choice_probability_mass'] for r in rows) / len(rows),
                'restricted_choice_kl_to_dense_mean': sum(r['restricted_choice_kl_to_dense'] for r in rows) / len(rows),
                'dense_backend_relative_error_max': max(r['dense_backend_relative_error'] for r in rows),
                'state_replay_relative_error_max': max(r['forward']['recurrence_relative_error'] for r in rows),
                'original_visual_tokens_mean': sum(r['forward']['layers'][0]['visual_tokens'] for r in rows) / len(rows),
                'layer2_visual_tokens_mean': sum(r['forward']['layers'][1]['visual_tokens'] for r in rows) / len(rows),
                'layer25_visual_tokens_mean': sum(r['forward']['layers'][24]['visual_tokens'] for r in rows) / len(rows)}
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
    metric_path = 'docs/multimodal-models/2610.11251-vcola/metrics/cifar10-a100.json'
    receipt_path = 'docs/gpu-validations/vcola-a100-20261011.json'
    limitations = ['frozen original 9B checkpoint; train-only CIFAR object diagnostic, not MME/MMBench',
        'restricted first-token answer letter, not full generated-answer accuracy',
        'sampling seeds are not independent training replicates; no statistical capability claim',
        'exact state replay, real visual merge and early exit; no feature-similarity proxy',
        'no-cache sequential reference backend; no optimized latency/speedup claim',
        'main Equation 7 query probes; Appendix A says keys, discrepancy explicitly documented',
        'merged visual mRoPE uses original maximum-score member; text mRoPE stays unchanged']
    metric = {'schema_version': 2, 'manifest_ref': 'multimodal-models:vcola', 'method': 'vcola',
        'dataset': 'CIFAR-10', 'seeds': seeds, 'metrics': metrics,
        'evaluation_protocol': {'tier': 'l1_mechanism', 'diagnostic_only': True,
            'formal_comparison': False, 'test_read': False, 'seeds': seeds,
            'claim_policy': 'actual frozen-checkpoint state/compression mechanism, no quality/speedup claim'},
        'runtime_details': report, 'limitations': limitations,
        'provenance': {'original_code_commit': commit, 'artifact_path': metric_path,
                       'executed_source_sha256': hashes}}
    receipt = {'schema_version': 1, 'adapter_key': 'vcola', 'validated_at': '2026-10-11',
        'accelerator': {'vendor': 'NVIDIA', 'model': report['accelerator']},
        'command': ['python', 'scripts/run_vcola_checkpoint.py', '--checkpoint', 'checkpoints/qwen3.5-9b',
            '--checkpoint-revision', REVISION, '--data', 'data/cifar10', '--output', 'runs/vcola-cifar.json',
            '--seeds', ','.join(map(str, seeds)), '--examples', str(report['datasets'][0]['examples'])],
        'dataset': {'id': 'CIFAR-10', 'revision': report['datasets'][0]['revision'],
                    'split_provenance': report['datasets']},
        'checkpoint': report['checkpoint'], 'result': 'passed', 'metrics': metrics,
        'evaluation_tier': 'l1_mechanism', 'limitations': limitations, 'seeds': seeds,
        'executed_source_sha256': hashes,
        'provenance': {'commit': commit, 'artifact_path': receipt_path, 'metrics_artifact': metric_path,
                       'checkpoint_committed': False}}
    for relative, payload in ((metric_path, metric), (receipt_path, receipt)):
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
