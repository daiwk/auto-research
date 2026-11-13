<!-- source-sha256: 4c886f50855975e0f983bd52a5c78544a63480b791bdcaf8177be0afd1a4ceb0 -->
# November 13: closing 24 historical COLM leads

[简体中文](../../../research-audits/nov13-colm-remaining/README.md)

This round reviews the **24 outstanding identities** in the preceding real-source snapshot: 23 papers are catalogued with 20 L1 mechanism kernels and three L0 interfaces; one is explicitly excluded based on its contribution scope. These are not 24 newly published papers or an exhaustive Google/Meta historical census.

## Delivery

| Domain | Local components / interfaces |
| --- | --- |
| Foundation models | Rosetta unification scores; LIDAS layer/AdamW-state growth; Thinking-to-Recall offline conditional analysis; latent-generalization set metrics; LLM stochasticity tests; ECG representations/loss; ContinuousBench protocol; QE length units; CuE cultural directions; constrained-beam extraction probabilities; StoryScope core-feature gating |
| Agents | Blocksworld optimality; SGP clarification costs/selection; MT-PingEval private views; PolicyBank structured memory; Co-Director factored UCB; Instruct-to-Act annotations/losses |
| Post-training | Social Meta-Learning successful student-token SFT; MAPLE nonprivate donation selection; Behavioral Canaries paired log-probability audit; RLMF metacognitive feedback/advantages |
| Multimodal | AVMeme Exam shortcut-controlled multiple-choice protocol; MMEB-V3 ranking and mixed-pool OmniSET protocol |

The [fixed-scope register](../../../research-audits/nov13-colm-remaining/task-scope.json) records paper metadata, method/cost locations, code availability and dispositions. [Foundation](../../../research-audits/nov13-colm-remaining/foundation-review.json), [agent](../../../research-audits/nov13-colm-remaining/agent-review.json) and [evaluation/post-training](../../../research-audits/nov13-colm-remaining/evaluation-review.json) reviews retain source hashes and inspected sections. First-author affiliation grouping is separate from Google/Meta coauthor priority.

`2601.16355`, **Identity, Cooperation and Framing Effects within Groups of Real and Simulated Humans**, is an empirical simulation of U.S. partisan social behavior. The review did not establish a new independently specified algorithm or released public benchmark, so it receives a sourceful scope exclusion. This neither dismisses its scientific value because of GPU cost nor invents a general-agent implementation.

## Actual validation and evidence boundaries

Sources were frozen at `1b7fe8699efd48e6421b01f6df756d6e4086eb52` before seeds 42/43/44 executed:

- 23 CPU components: approximately 4.13 seconds total.
- Seven CUDA components on one **NVIDIA A100-SXM4-80GB**: approximately 1.47 seconds total.
- CUDA scope: LIDAS, ECG, CuE, Social Meta-Learning, Instruct-to-Act, Behavioral Canaries and RLMF only. No large model, full-dataset inference or long training ran.

The [frozen-source proof](../../../research-audits/nov13-colm-remaining/frozen-sources.json), [raw CPU report](../../../research-audits/nov13-colm-remaining/raw-cpu.json), [raw CUDA report](../../../research-audits/nov13-colm-remaining/raw-cuda.json), per-paper three-seed artifacts and seven sanitized GPU receipts form an offline-verifiable chain:

```bash
PYTHONPATH=src:scripts python scripts/curate_nov13_colm_evidence.py --check
PYTHONPATH=src python scripts/validate_gpu_evidence.py
```

These commands verify evidence rather than rerunning GPUs. Three small-tensor/fixture seeds are not a formal model comparison. Passing control/scoring checks establishes no cultural, reasoning, tool-use, privacy or model-quality improvement. Every entry retains `diagnostic_only=true`, `promotion_eligible=false` and `evolve_integrated=false`. PolicyBank and the two multimodal benchmark protocols remain **L0**, not capability implementations.

No complete model campaign ran. Twenty-two papers have original model/data/matrix scale evidence and are **not reproduced due to high cost (review DONE)**. Latent Generalization's private Gemini SFT/teacher/RL dependency is separately marked `not_reproduced_private_dependency`, without invented public-GPU hours. Dataset access conditions, unconfirmed code releases and media licenses remain explicit. No checkpoints were loaded or trials launched merely to estimate cost, and nothing enters an automatic retry queue.

## Learning material and bilingual coverage

Each of the 23 papers has a Chinese explanation, individually reviewed English version and original paper figure. Four levels per paper produce **92 independently authored questions and reviewed English counterparts**. Topic cards add 23 source-bound comparisons with explicit methodological limits. Scoring protocols, paper-reported results and local diagnostics remain distinct; perfect fixtures are not capability claims.

## Historical reconciliation and coverage

The [current reconciliation](../../../research-audits/nov13-colm-remaining/historical-source-reconciliation.json) closes the captured 28 identities as **27 catalogued, one substantively reviewed exclusion, zero requiring review**. This closes captured identities, not unavailable official pages. **Four source exceptions** remain visible; zero outstanding identities does not conceal uncovered sources.

The [preceding snapshot](../../../research-audits/nov13-history-repair/historical-source-reconciliation.json) remains unchanged and honestly shows the earlier 24 pending reviews. No new date-window scan occurred; the review watermark remains **2026-11-09**.

Requested PR #250 was already merged when this work began and cannot receive additional commits. Local completion and publication target are recorded separately; no claim is made that these commits were appended to a merged PR.
