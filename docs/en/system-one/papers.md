# Jev-related papers and method lineage (legacy entry point)

<!-- source-sha256: 1d5695421587b7f1d42f2f37c0e6c070f5b87af169044a846c1388ca510d9d19 -->

[简体中文](../../system-one/papers.md)

The complete classification has moved to the [structured decision methods index](catalog.md) and [paper lineage and gaps](lineage.md). This page keeps the previous URL working.

There is no public Jev technical paper at the time of this report. Its internal architecture cannot be inferred from the product name. The verifiable **adjacent methods** below inform the repository's independent baselines and evaluation dimensions.

| Research direction | Paper | Mechanism usable in this repository | Status |
|---|---|---|---|
| Classification with dynamic candidates | [GLiClass](../../foundation-models/2508.07662-gliclass/README-en.md) | Single-pass encoding and interaction between the text and candidate labels | Local scorer operator |
| Calibration-aware rewards | [RLCR](../../post-training/2507.16806-rlcr/README-en.md) | Correctness plus a proper scoring rule | Brier / hybrid objective |
| Decision-token calibration | [Calibration-Aware RL](../../post-training/2601.13284-calibration-aware-rl/README-en.md) | Apply a calibration objective directly to the decision probabilities | ECE/Brier and validation-set temperature calibration |

These mappings explain where the research dimensions come from. They do not imply that Jev uses the same architecture.
