# Harness² and the Google/Meta historical screening gap

<!-- source-sha256: ec57c1ec19f97935e3ae832bad1a2111c78de4f086505325fe75ebf3b1052750 -->

[简体中文](../../../research-audits/harness2-priority-repair/scope.md)

This round starts with the user-nominated Harness² and fixes a screening bug: discovery records outside the review window were treated as if the methods had already been reviewed. The work is delivered in one MR without advancing a cutoff that has not been fully verified.

## Accepted scope

1. Read the Harness² paper and the pinned official implementation. Preserve two-level recursion and selection without gold answers.
2. Implement a low-cost, CPU-runnable core and tests. Distinguish the L1 mechanism diagnostic from real model capabilities.
3. Add a dedicated Chinese paper page, complete provenance metadata, original figures, classifications, measured metrics, and a rerunnable command.
4. Mark the full model/API benchmark as “not reproduced due to cost (review DONE).” Do not download large resources or start paid evaluations.
5. Fix discovery deduplication, priority-institution classification, and the review-write gate. Add a Harness² regression.
6. Reconcile saved official Google/Meta historical records individually and recheck recent official catalogs. Distinguish existing entries, historical omissions, out-of-scope items, and unverified items. Record the actual scope without claiming exhaustive coverage of all sources.
7. Run the relevant quality gates, check the MR branch, diff and CI, and remove disposable artifacts from this round.

## Resource and evidence constraints

- The Harness² core orchestration does not require CUDA. Any newly added CUDA implementation must run on a single A100 or A30.
- Checking discovery and dates is not a method review; a catalog entry is not an implementation; a multiseed diagnostic is not a capability comparison.
- Keep frozen review snapshots and append new dispositions to the discovery ledger. Do not automatically retry cost-based closures.
- Do not change runtime model defaults, use DeepXiv, or regenerate `uv.lock`.

## Completion record

See the report and machine-readable review artifacts in this directory for per-item outcomes, actual tests, and exceptions.
