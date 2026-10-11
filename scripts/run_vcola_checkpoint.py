#!/usr/bin/env python3
"""Real frozen Qwen3.5 visual compression on official CIFAR TRAIN holdout.

Restricted first-token object classification is an L1 mechanism diagnostic,
not MME/MMBench or full generated-answer accuracy. No gold goes into the model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from PIL import Image
import torch

from auto_research.multimodal.data import CIFAR10_LABELS, CIFAR10_URL, _md5, _read_cifar_batches
from auto_research.multimodal.vcola_checkpoint import Qwen35VCoLA

CHECKPOINT_ID = 'Qwen/Qwen3.5-9B'
CHECKPOINT_REVISION = 'c202236235762e1c871ad0ccb60c8ee5ba337b9a'
TRAIN_MD5 = (
    'c99cafc152244af753f735de768cd75f', 'd4bba439e000b95fd0a9bffe97cbabec',
    '54ebc095f3ab1f0389bbae665268c751', '634d18415352ddfa80567beed471001a',
    '482c414d41f54cd18b22e5b47cb7c3cb',
)


def load_image_holdout(directory, seed, examples):
    files = [Path(directory) / 'cifar-10-batches-py' / f'data_batch_{i}' for i in range(1, 6)]
    if examples < 1 or examples > 100:
        raise ValueError('bounded public-image diagnostic must use 1..100 cases')
    for path, digest in zip(files, TRAIN_MD5, strict=True):
        if _md5(path) != digest:
            raise ValueError('CIFAR train archive checksum mismatch')
    images, labels = _read_cifar_batches(files)  # never open test_batch
    # Last 100 official-training examples per class are a fixed validation pool.
    # This frozen-checkpoint experiment performs no fitting or parameter selection.
    pools = [np.flatnonzero(labels == label)[-100:] for label in range(10)]
    rng = np.random.default_rng(seed)
    chosen = [int(rng.choice(pools[i % 10])) for i in range(examples)]
    if len(set(chosen)) != len(chosen):
        raise ValueError('duplicate validation selections; choose another fixed sampling seed')
    metadata = {'id': 'CIFAR-10', 'source': CIFAR10_URL,
        'revision': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files},
        'split': 'fixed_official_train_only_class_tail_holdout', 'test_read': False,
        'selected_indices_sha256': hashlib.sha256(np.asarray(chosen, dtype='<i8').tobytes()).hexdigest(),
        'sampling_seed': seed, 'examples': len(chosen)}
    return [(idx, Image.fromarray(images[idx].transpose(1, 2, 0)), int(labels[idx])) for idx in chosen], metadata


def class_prompt():
    choices = '\n'.join(f'{chr(65 + i)}. {name}' for i, name in enumerate(CIFAR10_LABELS))
    return 'What main object is shown in this image?\n' + choices + '\nAnswer with one letter A through J only.'


def run(args):
    import transformers
    from transformers import AutoProcessor, Qwen3_5ForConditionalGeneration
    if not torch.cuda.is_available():
        raise RuntimeError('the actual Qwen3.5 checkpoint diagnostic requires CUDA')
    if args.checkpoint_revision != CHECKPOINT_REVISION:
        raise ValueError('checkpoint must remain on audited official revision')
    root = Path(args.checkpoint)
    processor = AutoProcessor.from_pretrained(root, local_files_only=True)
    model = Qwen3_5ForConditionalGeneration.from_pretrained(root, local_files_only=True,
        dtype=torch.bfloat16, attn_implementation='sdpa').to('cuda').eval()
    backend = Qwen35VCoLA(model)
    rows, datasets = [], []
    choice_ids = [processor.tokenizer.encode(chr(65 + i), add_special_tokens=False) for i in range(10)]
    if any(len(ids) != 1 for ids in choice_ids) or len({ids[0] for ids in choice_ids}) != 10:
        raise ValueError('restricted first-token scoring requires ten distinct single-token letters')
    letter_ids = torch.tensor([ids[0] for ids in choice_ids], device='cuda')
    for seed in [int(x) for x in args.seeds.split(',')]:
        images, metadata = load_image_holdout(args.data, seed, args.examples)
        datasets.append(metadata)
        for example, image, gold in images:
            message = [{'role': 'user', 'content': [{'type': 'image'}, {'type': 'text', 'text': class_prompt()}]}]
            prompt = processor.apply_chat_template(message, tokenize=False,
                add_generation_prompt=True, enable_thinking=False)
            batch = processor(text=prompt, images=[image], return_tensors='pt',
                min_pixels=224 * 224, max_pixels=224 * 224)
            batch = {key: value.to('cuda') for key, value in batch.items()}
            with torch.no_grad():
                # Full official original path provides baseline and a numerical
                # equivalence gate before claims about intervention behavior.
                original = model(**batch, use_cache=False, logits_to_keep=1).logits[:, -1].float()
                prefix = backend.prepare(batch)
                unmodified, sanity = backend.forward(prefix, collect_scores=True)
            error = float((original - unmodified).norm() / original.norm().clamp_min(1e-12))
            if not math.isfinite(error) or error > .01:
                raise RuntimeError(f'original checkpoint baseline forward mismatch ({error})')
            baseline_choices = original[0, letter_ids].log_softmax(-1)
            for recipe, rate, exit_layer in (('dense', 1., None), ('vcola-50-exit24', .5, 24),
                                             ('vcola-25-exit24', .25, 24)):
                logits, details = (original, sanity) if recipe == 'dense' else backend.forward(
                    prefix, remain_rate=rate, exit_layer=exit_layer)
                choice_lp = logits[0, letter_ids].log_softmax(-1)
                predicted = int(choice_lp.argmax())
                choice_kl = float((baseline_choices.exp() * (baseline_choices - choice_lp)).sum())
                row = {'sampling_seed': seed, 'example_id': example, 'recipe': recipe,
                    'restricted_first_token_correct': predicted == gold,
                    'restricted_choice_probability_mass': float(logits[0].softmax(-1)[letter_ids].sum()),
                    'restricted_choice_kl_to_dense': choice_kl, 'dense_backend_relative_error': error,
                    'forward': details}
                rows.append(row)
                print(json.dumps(row), flush=True)
    files = ['config.json', 'model.safetensors.index.json', 'tokenizer.json', 'tokenizer_config.json',
             'preprocessor_config.json', 'video_preprocessor_config.json', 'chat_template.jinja']
    return {'schema_version': 1, 'adapter_key': 'vcola', 'diagnostic_only': True,
        'evaluation_tier': 'l1_core_mechanism', 'rows': rows, 'datasets': datasets,
        'checkpoint': {'id': CHECKPOINT_ID, 'revision': CHECKPOINT_REVISION,
            'configuration_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                                     for name in files if (root / name).exists()}},
        'protocol': {'transformers_version': transformers.__version__,
            'first_layer_real_delta_state_capture': True, 'state_scores_not_feature_proxy': True,
            'query_probe_window': [0, 4], 'uniqueness_weight': .1, 'merge_temperature': 1.,
            'exit_layer': 24, 'text_original_mrope_preserved': True,
            'position_choice': 'original_max_score_chunk_member',
            'no_cache_reference_backend': True, 'prefill_speedup_claim': False,
            'full_generated_answer_accuracy': False, 'inference_gold_read': False,
            'restricted_first_token_only': True, 'test_read': False,
            'sampling_seeds_not_training_replicates': True},
        'accelerator': torch.cuda.get_device_name()}


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--checkpoint', type=Path, required=True)
    p.add_argument('--checkpoint-revision', default=CHECKPOINT_REVISION)
    p.add_argument('--data', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--examples', type=int, default=4)
    p.add_argument('--seeds', default='42')
    args = p.parse_args()
    report = run(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + '\n')


if __name__ == '__main__':
    main()
