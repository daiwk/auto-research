# October 11 real-checkpoint diagnostics

<!-- source-sha256: d4d37e1d7edc89cdfb488b1545abe2a4e4b5ac91f291a6cb64df21cfb16cd354 -->

[简体中文](../../post-training/oct11-checkpoint-guide.md)

These entry points execute real models. Short runs do not establish the paper's gains. Use a Linux NVIDIA GPU; the verified device was A100. Supply local paths without host identity or SSH configuration.

```bash
python -m pip install -e '.[post-training-gpu]'
python scripts/split_public_training_jsonl.py --help
python scripts/run_vfold_checkpoint.py --help
python scripts/run_recal_checkpoint.py --help
python scripts/run_zcpo_checkpoint.py --help
python scripts/run_opd_learning_signals.py --help
python scripts/prepare_pivot_banking77.py --help
python scripts/run_pivot_checkpoint.py --help
python scripts/run_sguid_checkpoint.py --help
python scripts/run_memento3_checkpoint.py --help
python scripts/run_vcola_checkpoint.py --help
python scripts/run_data_space_iteration.py --help
```

## Public checkpoints and data

The base is `Qwen/Qwen3-4B-Instruct-2507` at `cdbee75f17c01a7cc42f958dc650907174af0554`. OPD also requires the same-vocabulary `Siye01/Qwen3-4B-Inst-MOPD` teacher at `b61a9f00b77302b6e947af1215b7cb994b884c4a`. Use `--checkpoint-path` or OPD's `--student-path/--teacher-path` after downloading locally, and pass IDs and revisions. The runner does not download or upload private data.

GSM8K uses `openai/grade-school-math` revision `3101c7d5072418e28b9008a6636bde82a006892c`. Pass only official **train** JSONL to the splitter. Deterministic SHA-256 hashing of normalized questions yields a 90%/10% holdout with train, validation, and split.json. Do not use official test as validation. `--split-manifest` verifies source split, revision, partition hashes, counts, and nonoverlap. Legacy entry points without a manifest do not claim test isolation.

## Complete example with replaceable paths

```bash
python scripts/run_zcpo_checkpoint.py \
  --checkpoint-path checkpoints/qwen3-4b \
  --checkpoint-id Qwen/Qwen3-4B-Instruct-2507 \
  --checkpoint-revision cdbee75f17c01a7cc42f958dc650907174af0554 \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --train-path data/gsm8k-holdout/train.jsonl \
  --validation-path data/gsm8k-holdout/validation.jsonl \
  --split-manifest data/gsm8k-holdout/split.json \
  --steps 24 --group 4 --max-tokens 256 --validation-examples 8 \
  --seed 42 --device cuda --output runs/zcpo-42.json
```

Other papers' full argv is in their GPU receipts' `command` fields. Replace `checkpoints/*` with local public snapshots. Receipts store commands, revisions, executing commits, and source hashes, not weights.

## Interpretation

PIVOT uses separate official Banking77 train-only 385/77 partitions and Qwen2.5-0.5B / 7B. Do not substitute GSM8K paths. Its GPU receipt records commands for all three recipes and pinned checkpoints. All three scored 0% on eight questions; this real mechanism diagnostic retains that result.

## Other domains

- [SGUID](../../post-training/2610.12367-sguid/README-en.md): Actual Qwen3.5-9B text path with thinking toggle and a GSM8K train-derived holdout. A100 round one completed; round two failed persistence filtering and recovered exactly. No passing receipt or two-round acceptance. Check actual rendered prefixes, not just accepted parameters.
- [Memento3](../../agent-research/2610.11794-memento3/README-en.md): A public 7B generated world model interacts with real FrozenLake through a bounded AST interpreter. The run falsified the model and failed the task, not successful ARC/Pong reproduction.
- [V-CoLA](../../multimodal-models/2610.11251-vcola/README-en.md): Real 9B multimodal checkpoint and CIFAR-10 train-only images. Exercises state contribution, visual merging, and exit; constrained first-letter diagnosis is not full generation accuracy.
- [Data-Space Iteration](../../foundation-models/2610.12102-data-space-iteration/README-en.md): Trains a small UNet teacher from scratch on public CIFAR-10 train images and runs two DMD recipes. Three-seed results are mixed; pooled pixel distance is not paper FID.

Image entry points need the five official CIFAR-10 `data_batch_*` training files with verified MD5s. Do not substitute test for validation. Methods have their own budget and evaluation contracts; do not rank short diagnostics across domains.

Install extras independently. The micro-LLM `llm-evolution` extra is not a checkpoint environment:

```bash
# Real sparse CUDA kernels (Linux NVIDIA)
python -m pip install -e '.[sparse-decoding-gpu]'
# V-CoLA image processor and Qwen3.5 multimodal runtime
python -m pip install -e '.[multimodal]'
# Train the image teacher and DMD from scratch, with SciPy Fréchet diagnostic
python -m pip install -e '.[data-space-gpu]'
# Pinned Memento3 environment; post-training-gpu provides model dependencies
python -m pip install -e '.[post-training-gpu]' 'gymnasium==1.1.1'
# Option-Channel uses the public Laya checkpoint
python -m pip install -e '.[system-one-gpu]'
```

Results verify real forward/backward passes, parameter or cache changes, and data isolation. A single seed and a few validation questions do not establish stable gains. LoRA displacement is not full-parameter displacement; persistent cache size is not end-to-end peak memory or latency. Mark evolve integration only when the controller can execute and evaluate the operator. This batch did not promote named papers except the ZIP/ZE optimizers.
