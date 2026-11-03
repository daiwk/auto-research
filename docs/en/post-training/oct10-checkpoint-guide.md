# October 10 post-training algorithms: Real-checkpoint runs

<!-- source-sha256: 5b8ee2bbeaf2241688071b4ca597bb86b79070f777f8f9afa07f246b65028fae -->

[简体中文](../../post-training/oct10-checkpoint-guide.md)

These implementations do not return preset answers. The student samples, the teacher scores real token probabilities, and objectives update actual LoRA parameters. DIAL, Meta, and Semi-OPD use different distillation updates. GRPODropout uses external numeric verification rewards. RA and Co-RA combine teacher-distribution residuals with verifiable reward. Co-RA also updates the teacher LoRA, which guides the following round only.

## Environment and data

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[post-training-gpu]'
```

Prepare public causal-LM checkpoints with identical vocabularies and `q_proj` / `v_proj`. This A100 batch used Qwen3-4B-Instruct-2507 and public Qwen3-4B-Inst-MOPD. Compatible alternatives may be supplied; retain actual IDs and revisions.

Public GSM8K lines have `{"question": "...", "answer": "... #### 42"}`. Train and validation questions must not overlap. Only the evaluator sees validation answers, not the sampler. A small validation run establishes execution, not gains. Record the revisions actually downloaded rather than copying example revisions for other files.

## Run one objective

The following uses the pinned public revisions from this batch; substitute local paths:

```bash
PYTHONPATH=src python scripts/run_oct10_post_training.py \
  --objective dial-opd \
  --student-path checkpoints/qwen3-4b \
  --student-id Qwen/Qwen3-4B-Instruct-2507 \
  --student-revision cdbee75f17c01a7cc42f958dc650907174af0554 \
  --teacher-path checkpoints/qwen3-4b-mopd \
  --teacher-id Siye01/Qwen3-4B-Inst-MOPD \
  --teacher-revision b61a9f00b77302b6e947af1215b7cb994b884c4a \
  --train-path data/gsm8k/train.jsonl \
  --validation-path data/gsm8k/validation.jsonl \
  --dataset-revision 3101c7d5072418e28b9008a6636bde82a006892c \
  --output-dir runs/dial-opd --device cuda \
  --seed 42 --steps 2 --group 2 --max-tokens 128
```

Other objectives: `meta-opd`, `semi-opd`, `grpo-dropout`, `residual-advantage`, and `co-ra`, plus the `opd` control. GRPO and Co-RA need enough generation tokens. Inspect real within-group reward variance; all success or all failure may give no sequence-reward gradient. Do not replace rewards with fabricated values to fix this.

## Sequential batch and outputs

`scripts/validate_oct10_post_training.sh` runs six objectives sequentially. Provide `STUDENT_PATH`, `TEACHER_PATH`, their IDs and revisions, `TRAIN_PATH`, `VALIDATION_PATH`, and `DATASET_REVISION` explicitly via the environment. Defaults are short-budget verification, not full experiments.

Each directory contains `report.json` and local `adapter.pt`. Inspect loss, real reward variance, effective gradient steps, student and teacher parameter changes, filtered responses, and final isolated validation. It does not push weights to GitHub, call online models automatically, or upload training data.

These objectives have standalone executable training entry points but are not integrated with unified evolve. A registered paper name is not multi-round integration.
