# Historical review and current implementation status

<!-- source-sha256: 6b6ef3ac8f7ebaed8df402b2b31cda84f8ab4e06c8dd800e7d1a224dbd06be53 -->

[简体中文](../../../research-audits/oct12-review-closure/implementation-status.md)

This page reconciles the current manifest with the frozen review register. Later implementation work does not change the historical review decisions. Catalog registration, a runnable implementation, GPU execution, and a capability comparison are separate facts.

| Current status of accepted candidates | Count |
| --- | ---: |
| Present in the catalog | 26 |
| Not yet present in the catalog | 494 |

A catalog entry does not establish a full reproduction or a capability gain. A GPU receipt confirms execution; it does not replace fair baselines, isolated splits, sufficient budgets, or review of the results.

See the [machine-readable reconciliation](../../../research-audits/oct12-review-closure/implementation-status.json) for per-paper fields. The current review cutoff comes from the [unified status](../../../paper-discovery-watermark.json). This page does not reinstate the retired exhaustive-source cutoff.

Regenerate with: `python scripts/reconcile_discovery_implementation.py`.
