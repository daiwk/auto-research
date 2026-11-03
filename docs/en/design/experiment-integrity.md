# Experiment integrity and execution contracts (MR-A)

<!-- source-sha256: 08cea645d05790052ceb6ea4eb2cc76f36ed773469a5ec642eacce82c82c01e9 -->

[简体中文](../../design/experiment-integrity.md)

This work covers evidence promotion, resume and caching, negative-result memory, and timeouts/GPU concurrency. It does not change paper algorithms, relabel historical diagnostics as capability evaluations, or delete old data.

## Statistical summaries are not capability evidence

`evidence_policy.assess_evidence` is shared by reproduction reports, three-seed aggregation, and the public dashboard. Three distinct seeds are necessary but never promote L0/L1 runs, concept demos, gold-derived candidates, or results explicitly marked `diagnostic_only / promotion_eligible=False`. Mixed inputs inherit their weakest evidence.

A formal comparison requires this `comparison_contract` from the actual experiment, not inference from a filename or documentation:

| Field | Source |
|---|---|
| `protocol_id` | Versioned evaluation protocol actually run |
| `dataset_revision` | Public data revision or content hash |
| `split_revision` | Actual train/validation/test split version or hash |
| `baseline` | Frozen baseline executed under the same protocol |
| `code_revision` | Implementation version or content hash |
| `test_isolated` | Explicit guarantee that test did not select architecture, parameters, or candidates |

Aggregation checks seed alignment, duplicates, failures, and conflicting protocols. A formal comparison does not establish improvement: assess significance, effect size, and fidelity separately. Evolve applies the same diagnostic exclusions when selecting on validation, but small-seed exploration is not a formal conclusion.

Historical metrics and claims remain untouched. The dashboard reapplies the current policy: missing contracts are marked as not meeting the formal-comparison protocol, without inventing revisions or erasing actual measurements. An old JSON `formal_comparison` value does not override the policy.

## ExperimentSpec and resume

`experiment_contract.py` records versioned parameters and hashes of inputs and implementation. File identity uses contents, not mtime or directory names, and is not capped at the first 10,000 files. The initial read can be costly for large checkpoints; this is the price of safe resumption, not training budget.

`result.json` stores `experiment_spec`; only identical code/data content can resume. Generations may increase, and output/resume locations, workers, CPU threads, GPU slots, per-task VRAM, and negative-result destinations may change. Decreasing generations or changing data, seeds, steps, population, architecture selection conditions, checkpoint, device, or timeout/retry budget requires a new run. Legacy runs without fingerprints remain readable but cannot continue selecting champions.

The full candidate plan and parents are saved before each generation. Resume executes only incomplete trials. Each generation uses a deterministic independent random stream, so completion order cannot break ties. A resume directory rejects concurrent writes. Final test has a hard timeout too; failures report an error and retain validation traces.

Three-seed `state.json` binds parameters, inputs, and code instead of caching by method and seed only. Prepare public inputs first; changed directory contents invalidate reuse rather than mixing datasets. Topic research trial caches also bind data and implementation; external commands must explicitly declare revisions.

## Scope of negative results

New records bind ExperimentSpec, full genome, and comparator, not only architecture names. One failed learning rate does not ban other rates; changes in code, data, or baseline reopen exploration. Transient runtime failures use bounded retries, not permanent exclusions. Old entries remain for audit but cannot auto-exclude methods without fine-grained identity.

## Execution and resource control

Baselines, single- and multi-worker trials, retries, and final test run in spawned subprocesses. Time includes startup, evaluation, and all retries. Reclaim the process at timeout and its process group where supported. Injected evaluators must serialize under spawn, not rely on parent memory side effects. Receive results promptly through pipes so large results cannot fill queues while the parent waits for process exit.

Resolve `auto` to the real device before limiting concurrency by GPU slots and free memory on the selected CUDA device. If one task cannot fit, report an error. Other users can still change free VRAM; slots are this controller's cap.

Run CUDA verification:

```bash
python scripts/validate_mra_gpu.py --data data --output runs/mra-gpu --commit <tested-commit>
```

The script runs actual RankMixer training, validation/test on public MovieLens, CUDA parameter updates, one- and two-slot concurrency, and timeout cleanup. This is a scheduling/device smoke, not paper effectiveness. The receipt stores only metrics, public data hash, random initialization, accelerator model, source revision, and command, excluding machine paths and identities.

On 2026-10-07 the NVIDIA A100 run passed. Its [sanitized receipt](../../gpu-validations/experiment-integrity-a100-20261007.json) records three real training trials, observed concurrency of one/two CUDA jobs in one/two slots, and cleanup after about 12 seconds. Single-seed, three-step test NDCG was 0; no improvement claim is supported.

## Scope and remaining MR

MR-A regressions are centered in `tests/test_experiment_integrity.py`, alongside impacted contracts and all quality gates. MR-B addresses lazy registries, minimal install, scan checkpoints/coverage, unified paper specs, and migration out of dated batches. This does not claim MR-B completion or rerunning every paper.
