# System One shared evaluation protocol

<!-- source-sha256: 0652f80e9d938e274d78a6cc8e8745852ba6628474b17fa62b320118d3828c40 -->

[简体中文](../../system-one/benchmark.md)

Protocol ID: `foundation.banking77.system_one.v1`.

- Data: PolyAI Banking77 (CC BY 4.0). Train on official train; split official test by fixed even/odd indices into validation and test.
- Candidates: every example gets all 77 intents. Gold labels must not narrow the set.
- Selection: architecture, objective, learning rate, and temperature use validation only. Test is reserved for final reporting.
- Seeds: 42, 43, 44.
- Primary metric: accuracy. Calibration: NLL, Brier, ECE. Decision metrics: coverage and selective accuracy.
- Online Jev requests can incur costs. They do not run by default and are not presented as local reproductions.
- NanoJev uses a pinned public checkpoint. A one-seed smoke test is not multiseed evidence and stays separate from local training-from-scratch baselines.

## Public protocol across decision types

`system-one-public` reads Nimble-compatible, human-labeled JSONL for Choice, Noul, and Score. Formal v1 contains 200 fixed public human-labeled examples. See the [manifest](https://github.com/daiwk/auto-research/blob/main/data/system-one/system-one-public-v1.manifest.json) for sources and licenses.

| Split | Count | Source | Use |
|---|---:|---|---|
| Calibration | 60 | BoolQ, HelpSteer2, PubMedQA | Select backend, temperature, and thresholds |
| Test | 60 | Different IDs from the same sources | Report once after selecting the winner |
| OOD | 80 | ARC-Challenge, TruthfulQA | Cross-source stress test; Choice only |

The fixed slice uses the first 40 examples from each source, chosen before any model runs. It covers three decision types but does not represent the full datasets or official leaderboards. The manifest records each API URL, configuration, license, response SHA256, and converted-suite SHA256. The builder downloads public data; evaluation and Evolve use committed JSONL by default without changing samples online.

- `input` contains state and question only; `reference.target` never enters a provider request.
- v1 uses explicit calibration/test/OOD fields and unique IDs. The old format retains family splits.
- Calibration selects backend, temperature, and confidence threshold; test/OOD report only the selected winner.
- Run a fixed checkpoint once rather than repeating seeds to imply independent runs.
- Shared metrics are accuracy, NLL, multiclass Brier, ECE, coverage, and selective accuracy. Score adds MAE. Reports include slices by primitive and domain, plus worst-group accuracy.

The protocol can assess interoperability, calibration, and OOD behavior of open implementations. Their training domains differ, so a small suite is not a general-capability ranking.

### Actual multi-round A100 validation (2026-09-26)

On pinned v1 with SHA256 `387638878933f8b6293b240a1daf5017fb317bd3c226e511c4e72cf3af46140d`, open Nimble and Laya checkpoints entered 2 rounds and 5 trials of System One Evolve. NanoJev was not provided. The controller selected only on 60 calibration examples and retained initial Nimble configuration `g0-t0`; no variant beat the baseline. On the 60 isolated test examples, accuracy was `0.7333`, coverage `0.6167`, selective accuracy `0.8649`. On 80 cross-source OOD examples, accuracy was `0.7625` and coverage `0.7500`. This is executable evidence for a fixed checkpoint and seed, not a statistically significant gain or full-dataset ranking.

See the [sanitized A100 receipt](../../gpu-validations/system-one-formal-evolve-a100-20260926.json). Raw predictions, checkpoints, and outputs with absolute paths are not committed.

This is public-data L2 evaluation under a shared typed-decision contract, not proof of Jev training reproduction or product performance.

- [Three-seed metrics](../../system-one/metrics/banking77-local-seeds42-44.json)
- [Readable report](banking77-local-report.md)
- [NanoJev A100 checkpoint receipt](../../gpu-validations/nanojev-checkpoint-a100-20260921.json)
- [Laya A100 checkpoint receipt](../../gpu-validations/laya-checkpoint-a100-20260921.json)
- [Nimble A100 checkpoint receipt](../../gpu-validations/nimble-checkpoint-a100-20260921.json)
