# 2026-10-19: Targeted components and source-difference audit

<!-- source-sha256: e74b0b17c146d1285fa8c8e496c3b9265cde232f7760654f1f2ed29b1c47c078 -->

[简体中文](../../../research-audits/oct19-components/README.md)

This batch covers **nine papers: seven low-cost components or protocols and two high-cost documentation entries**. One historical gap was found in Google's official catalog and eight candidates came from the overlapping October 16 announcement. **These are not nine papers newly published October 19.**

All seven components passed acceptance: **three CUDA items ran on one A100 with three seeds each, and four CPU items ran with the same three seeds** (42, 43, and 44). These are operator and protocol diagnostics, not seven full reproductions.

The review watermark stays **2026-10-15**; this batch does not advance it, and `all_sources_exhaustive=false`. Component implementation, GPU verification, and source coverage are separate. See [source-coverage.json](../../../research-audits/oct19-components/source-coverage.json) for per-source receipts, SHA256, catalog decisions, and the nine-paper scope.

## Fixed scope

| Priority | Paper / arXiv v1 date | Local scope | Acceptance |
| --- | --- | --- | --- |
| P0 | [SKILL.state](../../../agent-research/2608.26263-skill-state/README-en.md), 2026-08-26 | CPU: explicit state, JSON merge patch, and execution loop retaining only the latest observation | [Three-seed CPU artifact](../../../agent-research/2608.26263-skill-state/metrics/component-cpu-seeds42-44.json) passed |
| P1 | [AlphaDiana](../../../agent-research/2610.20675-alpha-diana/README-en.md), 2026-10-14 | CPU: stable sample identity, retry/failure accounting, and shared-memory session policy | [Three-seed CPU artifact](../../../agent-research/2610.20675-alpha-diana/metrics/component-cpu-seeds42-44.json) passed |
| P1 | [AgentPerturb](../../../agent-research/2610.21624-agent-perturb/README-en.md), 2026-10-15 | CPU: one-target perturbations, independent verification, paired coverage, and bounds for unknown scores | [Three-seed CPU artifact](../../../agent-research/2610.21624-agent-perturb/metrics/component-cpu-seeds42-44.json) passed |
| P1 | [DIVERGE](../../../post-training/2610.22324-diverge-ideation/README-en.md), 2026-10-15 | CPU: set-level diversity and quality reward protocol | [Three-seed CPU artifact](../../../post-training/2610.22324-diverge-ideation/metrics/component-cpu-seeds42-44.json) passed |
| P1 | [FPOT](../../../foundation-models/2610.21257-fpot/README-en.md), 2026-10-15 | CUDA: fractional power-of-two weight quantization | [Three-seed A100 artifact](../../../foundation-models/2610.21257-fpot/metrics/component-cuda-seeds42-44.json) and [GPU receipt](../../../gpu-validations/fpot-a100-20261019.json) passed |
| P1 | [LAMP](../../../foundation-models/2610.22182-lamp/README-en.md), 2026-10-15 | CUDA: adaptive cross-layer prediction mixing on frozen features | [Three-seed A100 artifact](../../../foundation-models/2610.22182-lamp/metrics/component-cuda-seeds42-44.json) and [GPU receipt](../../../gpu-validations/lamp-a100-20261019.json) passed |
| P1 | [KnowGPO](../../../post-training/2610.22331-knowgpo/README-en.md), 2026-10-15 | CUDA: knowledge-grouped advantage and objective | [Three-seed A100 artifact](../../../post-training/2610.22331-knowgpo/metrics/component-cuda-seeds42-44.json) and [GPU receipt](../../../gpu-validations/knowgpo-a100-20261019.json) passed |
| P1 | [AutoSFT](../../../agent-research/2610.22194-auto-sft/README-en.md), 2026-10-15 | Method and cost notes only; no placeholder adapter | Full experiment too expensive, not reproduced (review DONE) |
| P1 | [Gen4P](../../../foundation-models/2610.22371-gen4p/README-en.md), 2026-10-15 | Method and cost notes only; no placeholder adapter | Full experiment too expensive, not reproduced (review DONE) |

SKILL.state v1 appeared August 26. This batch checked a later revision's explicit-state mechanism; neither a new catalog URL nor a revision is a first release. The other eight v1 dates are October 14–15, from overlap in the October 16 announcement. This fixes the batch scope without claiming that all remaining candidates have received full-text review.

## Actual retrieval time and original receipts

Retrieval ran **2026-10-19 03:34:14–03:36:45 (Asia/Shanghai)**. The receipts retain corresponding UTC timestamps `2026-10-18T19:34:14.229591+00:00` through `2026-10-18T19:36:45.590972+00:00`. Retrieval, announcement, and v1 dates are distinct; do not conflate them with first publication.

Sources are the actual `retrieval.json` and three Google, Meta, and DeepMind difference JSON files. The committed coverage file retains URLs, original fetch times, content SHA256, and counts for 49 pages rather than duplicating a 2.7 MB abstract corpus. Hashes fingerprint retrieved content; they are neither permanent mirrors nor proof of exhaustive source coverage.

### Latest announcements in six arXiv categories

| Category | Announcement date | new | cross-list | replacement | Parsed / expected |
| --- | --- | ---: | ---: | ---: | ---: |
| [cs.AI](https://arxiv.org/list/cs.AI/new?show=2000) | 2026-10-16 | 132 | 154 | 167 | 453 / 453 |
| [cs.CL](https://arxiv.org/list/cs.CL/new?show=2000) | 2026-10-16 | 105 | 72 | 90 | 267 / 267 |
| [cs.IR](https://arxiv.org/list/cs.IR/new?show=2000) | 2026-10-16 | 8 | 6 | 12 | 26 / 26 |
| [cs.LG](https://arxiv.org/list/cs.LG/new?show=2000) | 2026-10-16 | 166 | 140 | 161 | 467 / 467 |
| [cs.CV](https://arxiv.org/list/cs.CV/new?show=2000) | 2026-10-16 | 135 | 30 | 88 | 253 / 253 |
| [cs.RO](https://arxiv.org/list/cs.RO/new?show=2000) | 2026-10-16 | 89 | 13 | 47 | 149 / 149 |

All six pages were retrieved and their parsed counts matched. October 16 remains the latest announcement. Categories overlap, so 1,615 category records are not 1,615 independent papers; replacements are not automatically new methods. Complete parsing verifies receipt counts, not full-text review.

### Priority Google and Meta sources

| Official catalog | Successful / attempted pages | Unique URLs | October 15 baseline | URL difference |
| --- | ---: | ---: | ---: | ---: |
| [Google Research](https://research.google/pubs/?category=2026&sort=-publication__year) | 28 / 28 | 417 | 412 | 5 |
| [Meta AI](https://ai.meta.com/results/?content_types%5B0%5D=publication&page=1) | 6 / 6 | 144 | 144 | 0 |
| [Google DeepMind](https://deepmind.google/research/publications/) | 9 / 9 | 265 | 265 | 0 |

The baselines are the three official-source audits in `oct15-review-closure/`. Prior catalog presence does not establish implementation. No catalog difference does not mean a company published nothing elsewhere on the web, in repositories, or through model releases.

## Decisions on the five Google URL differences

| Catalog difference | Decision | Reason |
| --- | --- | --- |
| [SKILL.state](https://research.google/pubs/skillstate-scalable-long-horizon-agent-skills/) | Included as a historical P0 gap closure | v1 is 2026-08-26; the explicit-state component has independent value and is inexpensive to execute. |
| [Differential Observability…-2](https://research.google/pubs/differential-observability-detecting-silent-state-divergence-in-ebpf-based-cloud-networks-2/) | Duplicate URL, not a new paper | The same title's [unsuffixed URL](https://research.google/pubs/differential-observability-detecting-silent-state-divergence-in-ebpf-based-cloud-networks/) is in the baseline; the `-2` URL is not new method evidence. |
| [Regression Test Selection…-4](https://research.google/pubs/regression-test-selection-at-scale-4/) | Duplicate URL, not a new paper | The same title's [`-2` URL](https://research.google/pubs/regression-test-selection-at-scale-2/) is in the baseline; `-4` is not a new identity. |
| [The AI Divide…](https://research.google/pubs/the-ai-divide-bridging-the-implementation-gap-in-state-and-territorial-public-health-departments-2/) | Out of scope, not implemented | Public-health implementation and policy research, not a standalone ML or agent algorithm in scope. |
| [Uniform Laws of Large Numbers…](https://research.google/pubs/uniform-laws-of-large-numbers-in-product-spaces/) | Out of scope, not implemented | Probability and statistical learning theory, outside this batch's executable model, training, or agent scope. |

Thus **five new catalog URLs yield one historical gap closure, two duplicates, and two out-of-scope studies**, not five new same-day algorithms.

## Acceptance status and limits

All four CPU and three A100 components completed acceptance with seeds 42, 43, and 44. The initial source is pinned at `8c963f810e45ce3886e43b1b5da39980e41c95c0`. AlphaDiana's cost check for missing records was subsequently fixed and both Agent protocols reran at `39e912c1124c49b7d3a85957909fb143d8c9ba3c`. Unchanged GPU sources and actual runs remain tied to the first commit. Actual metrics and GPU receipts are linked above. [Frozen-source proof](../../../research-audits/oct19-components/frozen-sources.json) supports offline shallow-clone verification without relying on the old branch staying available. GPU claims cover these small operators only, not full checkpoints, real-task capability, or end-to-end speed.

All nine **full experiments** are marked `not_reproduced_high_cost` under the cost gate. Review is DONE, not a TODO blocking the watermark, and the two documentation entries have no algorithm adapter. Keep diagnostic boundaries: constructed traces are not official benchmarks, operator checks are not capability reproduction, and neither justifies Evolve promotion.

## Label and status recount

New static-fidelity inventory hits consist of two output-type checks, two transfers of actor-generated answers to independent graders, and one runtime version counter. None reads gold: references stay on the grading side, and the counter is not action or capability evidence. Behavioral tests cover private-field isolation, failure accounting, and non-execution of invalid patches. The static inventory itself is not a semantic passing certificate.

## Coverage not claimed

- This is not full-text closure of all candidates from six announcements. Only the nine component/documentation decisions above were closed.
- Other institutional sites, author repositories, model or benchmark releases, and unlisted sources were not exhausted. Lack of A/B wording in an abstract was not used to reject an industrial paper.
- Priority Google/Meta catalog checks do not replace full-text checks of online experiments, deployment, and cost.
- Missing catalog dates were not used to guess first releases, and high-cost non-reproduction was not recorded as completed implementation.
- The review watermark remains October 15. It can advance only with independent coverage closure, not because this batch's components passed.
