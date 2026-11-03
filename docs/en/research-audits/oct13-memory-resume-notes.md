# NEAR / Beyond: resuming public retrieval GPU verification

<!-- source-sha256: d0b9960983a6d4da2ee53ad3d4bb7c0ebca2e11353b96e3d4564ea179cf23b5d -->

[简体中文](../../research-audits/oct13-memory-resume-notes.md)

These notes preserve the 2026-10-13 pause. **Unstarted GPU runs and unknown resource status belong to that historical checkpoint and do not count as acceptance.**
The user explicitly resumed work on 2026-10-14. See [GPU TODO](../../research-audits/oct13-gpu-todo.md) for the latest continuation state.
The commands below were not executed during the pause. Recheck actual file integrity before resuming.

No hostnames, usernames, SSH aliases, drivers, or build strings are stored here. Unknown states are marked explicitly. No receipts were added at the pause; actual GPU evidence after resumption is linked separately below. Preparation does not count as GPU completion.

## Work completed after resumption on 2026-10-14

After the user restored network authorization, the execution environment reverified byte-level SHAs for all six MiniLM files and provenance, and the `277383467`-byte LongMemEval original and raw-only provenance. Earlier failures and source snapshots were not overwritten.

The independent overlay `/tmp/oct14-memory-overlay-4496283a` installed and verified transformers 4.57.3, huggingface-hub 0.36.0, tokenizers 0.22.2, safetensors 0.8.0, and tqdm 4.69.0. Installs used target/no-deps/ignore-installed. Shared Torch file origins matched before and after, so the shared runtime was unchanged. An actual offline MiniLM CPU forward returned finite values, not CUDA completion.

The run used frozen source `34148c2e29c01e9be7e4d5b8cbd09fd0f6016902`, tar SHA `062bac1d086553e360b69206ad252243619d166175b0fa366919d6d9e1310df7`, and a new immutable directory `/tmp/auto-research-oct14-34148c2e`. Eleven critical files matched commit bytes. Eight sequential NVIDIA A30 runs exited 0: NEAR and Beyond each ran 100 shared-bank queries on seeds 42/43/44, plus 30 strict bank-disjoint queries on seed 42. All used `--diagnostic-only`, max_length 128, batch 16, and adapter_epochs 2. No concurrent CUDA.

LongMemEval source came from official evaluation instances, but the local split is a nonofficial diagnostic, not the official test score. Three seeds share the same split and final ranking metrics, not independent data repetitions. Strict30 uses only 27/1/2, not pooled with shared100's 60/20/20. None is promotion-eligible. Beyond shared seed 43 and strict seed 42 both selected epoch 0; retain the negative result that trained candidates were not selected.

Raw JSON returned to `.cache/oct14-memory-raw-34148c2e`; all eight raw byte SHAs match context. See [execution context](../../research-audits/oct14-memory-execution-context-34148c2e.json), [NEAR summary](../../reproductions/2610.13314-near/metrics/a30-diagnostics-34148c2e.json), [Beyond summary](../../reproductions/2610.13277-beyond-final-embedding/metrics/a30-diagnostics-34148c2e.json), and [NEAR receipt](../../gpu-validations/oct13-near-a30.json) / [Beyond receipt](../../gpu-validations/oct13-beyond-final-embedding-a30.json). Raw evaluation tiers stay unchanged; curation explicitly labels L1 mechanism diagnostics. Later receipt path/spec binding changed metadata only; the binding commit was not the execution source.

Execution context `jobs[].command` preserves exact restart parameters, including argv, seed, timeout, exit, and output SHA. Reruns need fresh output/log paths. The following pause checkpoint is historical and no longer describes current resources.

## Historical pause state on 2026-10-13

| Item | Observed state in this round | What it does not establish |
| --- | --- | --- |
| Read-only accelerator query | NVIDIA A30, 24 GiB; no retrieval or training CUDA job launched | GPU experiments or performance verification complete |
| Shared Python | Python 3.11.10 and Torch import available; shared Python/Torch unchanged | All model dependencies compatible |
| MiniLM | Transfer of seven specified public files eventually exited 0 | Per-file remote SHA-256 verification, not yet done |
| Full LongMemEval raw JSON | Transfer exited 255; no file or partial temporary files may remain, state unknown | Complete original data available |
| LongMemEval raw-only provenance | Transfer exited 255; remote state unknown | Complete provenance available |
| Independent overlay | Creation connection exited 255; creation or partial creation unknown | Overlay initialized |
| Transformers and dependencies | **No network pip install command was submitted** | Small dependencies installed |
| NEAR seeds 42/43/44 | **None started**, no result JSON | Success, failure, negative results, or three-seed comparison |
| Beyond seeds 42/43/44 | **None started**, no result JSON | Adapter training, updates, or three-seed comparison complete |

Owned transfers and environment preparation ended: three failed operations exited 255, and MiniLM exited 0. Stop requests for the MiniLM transfer and children reported no such process; checking exact owned commands locally found no survivors. Other task connections were not stopped. Transferred resources, partial files, and checkpoints were not deleted.

## Frozen source and integrity

Source snapshot: `/tmp/auto-research-oct13-ccad3e67`.

The lead agent used `git archive` from `ccad3e679787f6f5383b8bd3dd1c7b58e7c8c5d0`. Read-only checks matched all **ten execution-related files** below against local `git show <commit>:<path>` bytes using SHA-256. This verifies files, not a remote `.git` directory or root provenance statement.

| File (relative to snapshot root) | Verified SHA-256 |
| --- | --- |
| `scripts/run_oct13_memory.py` | `1b2750f16e3bb82d4960f1767c8505826df92d92088ecb5437762c093559e616` |
| `src/auto_research/reproductions/near/__init__.py` | `e7526576c299eded95c33b11c8c535d972ae4e44052d240d29f9e14f3eb18703` |
| `src/auto_research/reproductions/near/adapter.py` | `2c44b4430af86b7b570bb55b8d366b684ae517530aa589ebe8339f2b4db28b3d` |
| `src/auto_research/reproductions/near/algorithm.py` | `2058bdd67dd04dabe2482a60c234a61bcb90ad132a7e43cf40d85ef3fedd1906` |
| `src/auto_research/reproductions/near/data.py` | `795416bdffeb25880aeaf85b4bfd6480b8677b45cddabe37ba2e49d7bf544eb8` |
| `src/auto_research/reproductions/near/experiment.py` | `dff15dd41eb74a102265b473f92b8885bab033be91f1ad7b0a8a4d8579607ea7` |
| `src/auto_research/reproductions/beyond_final_embedding/__init__.py` | `b61e251f3e7f6fbb26021eb9ad3996c8f8ca233175dc19b86796b695ecc44a43` |
| `src/auto_research/reproductions/beyond_final_embedding/adapter.py` | `3b58025b770656c4a5c2b647854a43977ce67a335abf9fda2d278ef9cd79bce9` |
| `src/auto_research/reproductions/beyond_final_embedding/algorithm.py` | `25ddc0d5276ca7f16d416410942a71beef721491633e0103d9b8f88a4f671622` |
| `src/auto_research/reproductions/beyond_final_embedding/experiment.py` | `9defb1afee9b3acf3818fd9fd76b5f357e707da900ecd74da27b9c34e3193665` |

Recheck these files before resuming. Report needed algorithm/runner fixes, have the lead agent commit a new snapshot, and rerun. Do not hot-patch the original snapshot or fabricate successful JSON.

## Only public resources authorized for synchronization

### MiniLM

- Local mirror: `.cache/oct12-public/checkpoints/minilm/`.
- Public ID：`sentence-transformers/all-MiniLM-L6-v2`。
- Pinned revision: `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.
- Destination: `/tmp/auto-research-oct13-ccad3e67/public/minilm/`.
- Sync only the six files below and `provenance.json`; exclude `.cache/huggingface/`, locks, and other local files.

| File | Bytes | Verified local SHA-256 |
| --- | ---: | --- |
| `model.safetensors` | 90,868,376 | `53aa51172d142c89d9012cce15ae4d6cc0ca6895895114379cacb4fab128d9db` |
| `config.json` | 612 | `953f9c0d463486b10a6871cc2fd59f223b2c70184f49815e7efbcab5d8908b41` |
| `tokenizer.json` | 466,247 | `be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037` |
| `tokenizer_config.json` | 350 | `acb92769e8195aabd29b7b2137a9e6d6e25c476a4f15aa4355c233426c61576b` |
| `special_tokens_map.json` | 112 | `303df45a03609e4ead04bc3dc1536d0ab19b5358db685b6f3da123d05ec200e3` |
| `vocab.txt` | 231,508 | `07eced375cec144d27c900241f3e339478dec958f92fddbc551f295c992038a3` |

### LongMemEval

- Local original: `.cache/oct12-public/longmemeval/longmemeval_s_cleaned.json`.
- Public ID：`xiaowu0162/longmemeval-cleaned`。
- Pinned revision: `98d7416c24c778c2fee6e6f3006e7a073259d48f`.
- bytes：`277383467`。
- SHA256：`d6f21ea9d60a0d56f34a05b609c79c88a451d2ae03597821ea3d5a9678c3a442`。
- Destination: `/tmp/auto-research-oct13-ccad3e67/public/longmemeval/longmemeval_s_cleaned.json`.
- Raw-only provenance: `.cache/oct13-a30-memory-transfer/longmemeval-provenance.json`, destined for `provenance.json` in the same directory.

Existing `.cache/oct12-public/longmemeval/provenance.json` describes two earlier transformed samples, not the full raw dataset. The new raw-only record contains public ID, pinned revision, full original hash, and a no-transformation statement. The old record was unchanged and `t2mem-first2.jsonl` was not transferred.

### Resume transfer (do not run now)

Create destination directories in an authorized session and preserve any partial files. Supply the authorized target through `APPROVED_TARGET`; do not record it here.

```bash
mkdir -p /tmp/auto-research-oct13-ccad3e67/public/minilm
mkdir -p /tmp/auto-research-oct13-ccad3e67/public/longmemeval
```

Sync serially from the local repository. Reuse MiniLM files if complete and matching hashes. A failed transfer does not establish that a full file is available.

```bash
: "${APPROVED_TARGET:?Supply an authorized connection target}"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct12-public/checkpoints/minilm/config.json \
  .cache/oct12-public/checkpoints/minilm/model.safetensors \
  .cache/oct12-public/checkpoints/minilm/tokenizer.json \
  .cache/oct12-public/checkpoints/minilm/tokenizer_config.json \
  .cache/oct12-public/checkpoints/minilm/special_tokens_map.json \
  .cache/oct12-public/checkpoints/minilm/vocab.txt \
  .cache/oct12-public/checkpoints/minilm/provenance.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/minilm/"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct12-public/longmemeval/longmemeval_s_cleaned.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/longmemeval/"
rsync --archive --compress --partial --progress --timeout=60 \
  .cache/oct13-a30-memory-transfer/longmemeval-provenance.json \
  "${APPROVED_TARGET}:/tmp/auto-research-oct13-ccad3e67/public/longmemeval/provenance.json"
```

On resumption, read both public provenance records on the execution side, stream SHA-256 for each actual file, and check model ID/revision against the pinned values. Stop if files are missing or hashes differ rather than substituting a smaller temporary sample.

## Isolated dependency plan (not installed at the historical checkpoint)

Read-only module probing confirmed missing `transformers`, `huggingface_hub`, `tokenizers`, `safetensors`, and `tqdm`.

Specs were located for `numpy`, `regex`, `requests`, `packaging`, `filelock`, and `yaml`, but imports and versions were not checked individually, so compatibility was unknown. No `sklearn` spec; these implementations use their own NumPy clustering/indexing and do not require it.

The lead agent checked the official Transformers 4.57.3 dependency contract and recommended the pinned small set below. This was not a completed install at the checkpoint:

```text
transformers==4.57.3
huggingface-hub==0.36.0
tokenizers==0.22.2
safetensors==0.8.0
tqdm==4.69.0
```

Do not copy local Transformers 5.14.1 or upgrade shared Torch to accommodate it.

Planned overlay: `/tmp/oct13-memory-overlay-ccad3e67`. First inspect it read-only. If partially created, preserve it and choose a fresh directory; do not clear or overwrite unknown contents. This example creates it only when absent:

```bash
OVERLAY=/tmp/oct13-memory-overlay-ccad3e67
if [ ! -e "$OVERLAY" ]; then
  /usr/bin/python -m venv --system-site-packages --symlinks "$OVERLAY"
fi
SITE=$("$OVERLAY/bin/python" -c "import sysconfig; print(sysconfig.get_path('purelib'))")
case "$SITE" in
  "$OVERLAY"/*) ;;
  *) exit 1 ;;
esac
"$OVERLAY/bin/python" -m pip --isolated --disable-pip-version-check install \
  --no-deps --ignore-installed --no-cache-dir --upgrade --target "$SITE" \
  transformers==4.57.3 huggingface-hub==0.36.0 tokenizers==0.22.2 \
  safetensors==0.8.0 tqdm==4.69.0
"$OVERLAY/bin/python" -m pip --isolated --disable-pip-version-check list --path "$SITE"
```

Do not resolve/install dependencies automatically; avoid reinstalling Torch/Triton/NVIDIA packages or changing the inherited environment. Check Torch files against `/usr/bin/python` before and after; setup does not need CUDA initialization. Report any additional missing/incompatible dependency before installing a small pinned version only in the overlay.

## Fixed evaluation protocol

Six planned runs in order: NEAR 42/43/44, then Beyond 42/43/44. Each uses 100 queries, max length 128, batch 16, two adapter epochs, and explicit `query-disjoint-shared-bank`. Run only one CUDA process and reconfirm exclusive GPU authorization before resumption.

Local public raw loading and splitting was checked: 60 train, 20 validation, and 20 test, all answerable, with 2820/951/964 candidate session IDs and 4572 distinct memory texts across 100 queries. This is CPU data protocol checking, not model retrieval.

- Use fixed label-free hashes to split query IDs. Encoder and unlabeled memory bank may be shared.
- Relevance labels for the optional query adapter are training-loss only. Validation selects epoch/alpha or NEAR settings; test only scores the final choice.
- Keep gold answers hidden from models and preserve `shared_unlabelled_memory=true`, `unseen_bank_generalization=false`, `diagnostic_only=true`, and `promotion_eligible=false`.
- Scaled, nonofficial fixed-index diagnostics are not full LMEB, original backbone/HNSW, or unseen-bank generalization. Do not pool with strict bank-disjoint results.
- Preserve the earlier strict CPU negative result on 30 queries. It is not superseded by this TODO or future shared-bank results.

### Six sequential commands (do not run now)

Execute in the specified snapshot only after resources, dependencies, and source pass checks and the user explicitly resumes GPU work. Use new results and preserve raw failure logs.

```bash
SOURCE=/tmp/auto-research-oct13-ccad3e67
OVERLAY=/tmp/oct13-memory-overlay-ccad3e67
cd "$SOURCE"
export PYTHONPATH=src
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export CUDA_VISIBLE_DEVICES=0
RUN_ROOT=runs/memory-eval-resume
LOG_ROOT=logs/memory-eval-resume
mkdir -p "$RUN_ROOT" "$LOG_ROOT"
for paper in near beyond-final-embedding; do
  for seed in 42 43 44; do
    output="$RUN_ROOT/$paper-seed$seed.json"
    if [ -e "$output" ]; then
      printf 'Immutable result exists; verify before proceeding: %s\n' "$output"
      continue
    fi
    "$OVERLAY/bin/python" scripts/run_oct13_memory.py \
      --paper "$paper" \
      --raw-data public/longmemeval/longmemeval_s_cleaned.json \
      --model-dir public/minilm --device cuda --seed "$seed" \
      --max-queries 100 --max-length 128 --batch-size 16 --adapter-epochs 2 \
      --split-policy query-disjoint-shared-bank --output "$output" \
      >> "$LOG_ROOT/$paper-seed$seed.log" 2>&1
    status=$?
    printf '%s seed=%s exit=%s\n' "$paper" "$seed" "$status"
    if [ "$status" -ne 0 ]; then
      printf 'Keep failure logs; diagnose before proceeding and do not invent successful JSON.\n'
      break 2
    fi
  done
done
```

Check each real JSON for seed/device, 60/20/20 split, public revisions/hashes, validation-selected settings, test/baseline, and comparison contract. Beyond also needs real two-epoch loss and parameter-update evidence. Report poor, flat, epoch-0, and failed outcomes as observed. Retrieve raw JSON into a dedicated local directory; the lead agent curates formal metrics and sanitized receipts. These notes are not a receipt.

## Local retention and cleanup boundaries

Keep `.cache/oct13-a30-memory-transfer/longmemeval-provenance.json` as the public raw-only record and retain unknown/partial remote files for resumption. No shared cache was deleted and no other models, data, source, or local files were acquired or transferred. No global index, manifest, or generated content changes from these notes.
