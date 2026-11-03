# Structured decisions / System One

<!-- source-sha256: e43d24bea9804e233460e724df4706142bf6331b35f4cc525de179086cb4002d -->

[简体中文](../../system-one/README.md)

Jev is TypeSafe AI's first **System One** model. Given a `state` and typed questions, it returns machine-consumable decisions rather than natural-language answers. This repository separates three evidence layers so community hypotheses are not treated as official facts.

Structured decisions form a research domain alongside foundation models, post-training, and agents. The focus is typed, calibrated, directly executable decisions over dynamic candidates, rating scales, or Boolean propositions. Jev is the product entry point; GLiClass, calibration work, and open implementations supply a publicly verifiable research lineage.

[Jev-DLC dual-channel continual adaptation](../../system-one/2610.31521-jev-dlc/README-en.md) maintains semantic counts, PA-I corrections, and reliability state above a frozen external scorer. It commits each decision before receiving feedback. The local CPU component verifies temporal ordering and independent equations, without loading Jev or reproducing the costly full 27B experiments.

The October 26 announcement added [EditJev image-edit routing](../../foundation-models/2610.32635-editjev/README-en.md): a preference head, request-normalized pairwise loss, and speed routing, verified as an L1 component on A100. It generates no images and does not give test quality to the router. [PathJev pathology decisions](../../foundation-models/2610.32478-pathjev/README-en.md) are a reference only; long multiseed training is not reproduced due to cost (review DONE). These papers do not disclose TypeSafe Jev's internals.

The [Jev Portuguese retrieval interface](../../foundation-models/2610.23346-jev-portuguese-ir/README-en.md) separates ordinal qrel judgments from independent Noul probability reranking, preserving exact batch coverage, linear nDCG/MRR, and κ/τ-b. Local work checks the offline protocol and recomputes published confusion matrices; it does not call Jev or reproduce costly full API experiments.

[System One multimodal reranking](../../multimodal-models/2610.28435-system-one-rerank/README-en.md) reads candidate-letter logits under one image–text prompt and ranks choices in one actual VLM forward pass. The interface was verified with a small public VLM on A100. It is not TypeSafe Jev or the paper's 27B result; full evaluation is not reproduced due to cost.

| Layer | Repository support | Evidence boundary |
|---|---|---|
| Official contract | Choice, Score, Noul structures and optional TypeSafe HTTP provider | Public API only. Jev weights, data, and architecture are not published in this snapshot. |
| Reproducible experiments | Dynamic scorer, proper scoring, temperature calibration, and three-seed Banking77 | Independent auditable baselines, not Jev's internal model |
| Open ecosystem | 48 community implementations, evaluations, and indexes | Separate trained checkpoints, inference decoders, diffusion, and explanatory material; cataloged does not mean integrated |

## Run

The local backend needs neither a key nor a GPU:

```bash
auto-research system-one-eval \
  --backend local \
  --architecture rival_attention \
  --objective hybrid \
  --seeds 42,43,44
```

The online comparison runs only with an explicitly configured `TYPESAFE_API_KEY`, which is not saved in results:

```bash
TYPESAFE_API_KEY=... auto-research system-one-eval --backend typesafe
```

All three open backends use audited immutable revisions. The audited NanoJev and Nimble paths use CUDA. Laya also supports CPU, although formal evidence was rechecked on A100:

```bash
pip install -e '.[system-one-gpu]'
auto-research system-one-eval \
  --backend nanojev --device cuda:0 --precision bf16 \
  --maximum-eval-examples 100
```

Offline Nimble is Qwen3.5-9B LoRA and needs both the adapter and a pinned base snapshot. Laya is a 421M ModernBERT typed-decision head:

```bash
auto-research system-one-eval --backend nimble --dataset public-jsonl \
  --public-data data/system-one/system-one-public-v1.jsonl \
  --checkpoint-dir /checkpoints/nimble --base-model-dir /checkpoints/qwen3.5-9b \
  --offline --device cuda:0

auto-research system-one-eval --backend laya --dataset public-jsonl \
  --public-data data/system-one/system-one-public-v1.jsonl \
  --checkpoint-dir /checkpoints/laya --offline --device cuda:0
```

Without `--checkpoint-dir`, NanoJev downloads a pinned `C-Tianyu/NanoJev` commit. Offline mode requires the downloaded directory. The provider runs the authors' actual 0.6B checkpoint without gold answers or autoregressive output tokens.

## Executable contracts

### Cross-language recomputation and request independence

- [Prism-1](../../foundation-models/2610.22066-prism-1/README-en.md): Independent option blocks, shared positions, and yes/no odds. A tiny Transformer verified independent-forward equivalence and invariance to irrelevant options on A100. L1 only; no 8B/12B training, Jev internals, or Evolve integration.
- [Jev regional language transfer](../../system-one/2610.14112-regional-transfer/README-en.md): Uses fixed public author predictions to recompute calibration, risk–coverage, and a validation-selected confidence cascade. No paid service or training on Jev output.
- [Retrieval request-independence audit](../../system-one/2610.14631-request-audit/README-en.md): Separates interventions on questions, evidence, and candidates to detect unexpected probability or decision changes. Runs paired external-prediction analysis, not a full seven-checkpoint experiment.
- [Selective Reasoning](../../system-one/2610.19644-selective-reasoning/README-en.md): Recomputes nine groups of statistics from a pinned public release and exposes controller interfaces for start, read, and stop. Historical recomputation is not local capability; costly full online LLM experiments are not reproduced.

These interfaces are not registered as trainable Evolve operators. Author predictions and protocol tests are not new local model capabilities.

The [13-task capability evaluation](../../system-one/2610.11978-jev-capability/README-en.md) covers knowledge, reasoning, and multilingual behavior with official schemas, pinned revisions, language macro averages, and explicit gaps. Open NanoJev ran the full ARC-Challenge test split. Its results are reported separately from closed Jev, not as official reproduction.

- `Choice`: 2–255 dynamic candidates, selected item, full probabilities, and confidence.
- `Score`: ordinal rubric scores with probabilities for every level.
- `Noul`: probability that a statement is true.
- Questions share one state but are evaluated independently.

Code: `src/auto_research/system_one/`. The HTTP provider validates HTTPS, question IDs, and probability sums. The local provider does not read gold answers or generate a text answer in place of a decision.

## Evolve

`system-one` is integrated into the multi-round controller. NanoJev, Nimble, and Laya operators are exposed and actually executed only when the user supplies checkpoint paths. Four trainable local operators are available:

- `system-one:bilinear-ce`
- `system-one:rival-ce`
- `system-one:rival-brier`
- `system-one:rival-hybrid`

```bash
auto-research evolve \
  --model system-one \
  --dataset banking77 \
  --direction "Compare dynamic candidate interaction architectures and calibration objectives" \
  --generations 3 --population 4 --seeds 42,43,44
```

Open checkpoints can jointly search backend, temperature, and selective-confidence threshold on one human-labeled Choice/Noul/Score JSONL:

```bash
auto-research evolve --model system-one --dataset system-one-public \
  --direction "Compare open System One checkpoints, calibration temperature, and abstention thresholds" \
  --system-one-public-data data/system-one/system-one-public-v1.jsonl \
  --system-one-nimble-checkpoint /checkpoints/nimble \
  --system-one-nimble-base /checkpoints/qwen3.5-9b \
  --system-one-laya-checkpoint /checkpoints/laya \
  --offline --device cuda:0
```

Public v1 contains 200 fixed human-labeled examples: 60 calibration, 60 test, and 80 from independent OOD sources. Select only on calibration; report test/OOD after the winner is fixed. This tests contracts, calibration, and cross-source behavior, not general product performance. See [source and license manifest](https://github.com/daiwk/auto-research/blob/main/data/system-one/system-one-public-v1.manifest.json) for response and suite hashes. Rebuild with `python scripts/build_system_one_public_suite.py --output data/system-one/system-one-public-v1.jsonl`. Local Banking77 training uses separate protocol `foundation.banking77.system_one.v1`.

Three-seed local baseline: accuracy `0.1353±0.0475`, Brier `0.9749±0.0004`, ECE `0.1048±0.0508`. See [per-seed metrics](../../system-one/metrics/banking77-local-seeds42-44.json). This small baseline uses 800 sample updates; it is not Jev performance and should not be compared directly with full GLiClass checkpoints.

NanoJev's real A100 smoke uses 12 validation and 12 held-out test examples. Test accuracy is `0.1667`, NLL `3.9825`, Brier `0.9745`, ECE `0.1397`, and schema validity `1.0`. This is small-sample OOD interoperability from a game/decision checkpoint to Banking77, not a stable capability ranking. See the [GPU receipt](../../gpu-validations/nanojev-checkpoint-a100-20260921.json).

Pinned Laya ran a mixed Choice/Noul/Score protocol on A100. See its [receipt](../../gpu-validations/laya-checkpoint-a100-20260921.json) for results and data hash. Qwen3.5-9B plus Nimble LoRA also ran on A100 under the same protocol; see the [Nimble receipt](../../gpu-validations/nimble-checkpoint-a100-20260921.json).

The public typed protocol is Nimble-compatible. Every record separates `input` from `reference`. The loader rejects target/answer/label/gold fields in input. Formal v1 checks explicit calibration/test/OOD splits and unique IDs; older records split by source family. This permits reporting accuracy, NLL, Brier, ECE, coverage, selective accuracy, Score MAE, and type/domain slices without exposing answers to models.

## Further reading

- [Chinese-Jev: Chinese candidates, probabilistic supervision, and RLCD](../../foundation-models/2609.36965-chinese-jev/README-en.md)
- [Methods index](catalog.md)
- [By institution](catalog/by-organization.md) · [By topic](catalog/by-topic.md) · [By year](catalog/by-year.md)
- [Jev and open implementations](implementations.md)
- [48-entry community snapshot](implementation-tracker.md), including P0/P1 candidates
- [Paper lineage and gaps](lineage.md)
- [Evaluation protocol](benchmark.md)
- [TypeSafe introduction](https://docs.typesafe.ai/introduction)
- [TypeSafe Choice contract](https://docs.typesafe.ai/primitives/choice)
