# 2026-10-07 paper batch: implementation and evidence plan

<!-- source-sha256: 7602a32fca0dc10fa2f22c0a6b7d65639640aab0a3c7896d24a684d0fa450683 -->

[简体中文](../../design/oct07-research-batch.md)

Authorized scope: scan October 1–7, 2026; review the previous round's 48 Agent titles; prioritize FrugalEvo and Sentry; assess Dynamic Expert Pruning, RC-OPD, Recursive Harness Self-Improvement, Pivot-SD, and KV². Include candidates in the same PR only when their defining algorithms can be preserved and verified.

## Non-negotiable boundaries

- Do not use DeepXiv for discovery. Until organization-specific cross-checks are closed, keep the complete review watermark at 2026-10-02. Count search hits, first discoveries, and papers first released this week separately.
- At revision `83064d18a99f47a0a8032049eaa2e1e4085351ad`, the Sentry authors' repository contained only descriptions and the paper, with code marked forthcoming. This is an independent implementation, not a port of released code.
- Check FrugalEvo against author revision `82f7b739110944bf3e8737db303a302a568e7327`, paper §2, and Appendix A. Generate actual programs; do not substitute preset candidates for LLM search.
- CUDA paths require A100/A30 execution and sanitized receipts. Label CPU unit tests, synthetic tool environments, and actual public-task runs separately.
- Record exact blockers for missing weights, data, or defining algorithm details. Do not mark blocked candidates complete.

## FrugalEvo

Implement cold start, one strong-model call producing multiple strategies, weak-model trial and ranking per strategy, feedback retries with the parent fixed, re-anchoring after improvements, island MAP-Elites, and cost curves. The static prefix precedes dynamic feedback; count observed input and output tokens, with no fictional discounts for cache misses.

The first run uses public Circle Packing with 26 circles. Run generated Python in an isolated subprocess and score with a trusted external geometric verifier. The sandbox has no network, workspace or model-cache mounts; it has a read-only runtime and CPU, memory, output, and time limits. Fail closed when unavailable; do not fall back to bare `exec`. Public checkpoints replace the paper's API models, and budgets are in local token-cost units, not dollars. The paper's results tables are not reproduced.

## Sentry

The runtime receives only public reasoning, actions, observations, and action-validity signals. Invalid actions trigger hard repair. An LLM diagnoses behavior from a recent window and retrieves at most five experiences by failure class, tag overlap, and recency, aiming for no more than two primary tags. After soft repair, a reward-blind model examines up to ten steps for local recovery; only verified recovery can create an experience. Hard repairs never enter the soft playbook.

Compare held-out runs with a frozen playbook. The policy, detector, and verifier cannot receive final answers, reference plans, or success labels. Keep verifier errors and failed recoveries as failures, not self-reported completions.

## Delivery checklist

- [ ] Close all four official-source discovery tracks. Query results and the audit of 48 older titles were saved, but some queries were truncated and Google/Meta access was incomplete; the complete watermark remains 2026-10-02.
- [x] FrugalEvo implementation, negative tests, and actual dual-model A100 runs with three seeds and budget controls.
- [x] Sentry implementation, isolation tests, and held-out A100 runs with a real checkpoint and three seeds.
- [x] Full-text and feasibility decisions on the other five candidates. Missing requirements are documented in the scan; none are registered as implemented.
- [x] Chinese detail pages, original figures, metadata, RSI overview, discovery ledger, and roadmap.
- [x] Full local suite (1,271 passed), relevant generators and quality gates, strict docs build, and GPU receipts.
- [x] Opened [PR #194](https://github.com/daiwk/auto-research/pull/194) and verified its branch diff and remote HEAD.
- [ ] Remote CI fully green; use checks on the latest PR commit.

See the [scan report](../recent-paper-scan-20261007.md) for outcomes and open work. Neither real-model experiment showed improvement; retain the negative results and do not promote through Evolve. The newly discovered Google TEE-FL and Airbnb SIFT also remained unimplemented.
