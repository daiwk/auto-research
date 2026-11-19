<!-- source-sha256: cdc3514a366c2aec50d71baeac20318abf01a60d16cfe8203ebc4ddea5c71d2a -->
# November19 paper scan and delivery

[简体中文](../../../research-audits/nov19-latest/README.md)

23 items: 21 first releases from November18, Meta AVM first published November17 and announced today, and historical November2 Google SearchInject newly observed in the directory. 18 bounded components/interfaces and5 review-only high-cost papers;7 CUDA components actually ran on an A100 with seeds42/43/44. 92 individually reviewed bilingual questions and23 same-topic deep-dive updates.

## Scope and evidence

This is finite selection, not all-source or institution-wide exhaustion.2781overlapping metadata identities and1082current bulletin identities are neither a count of new papers nor an implementation backlog. The global review watermark is unchanged. Publication, announcement, directory observation and repository pushes remain separate events.

Google/Meta were prioritized. Meta MLE Agents includes verified production A/B and the adverse latency guardrail. The complete8M-video AVM campaign is not reproduced. SearchInject measures exposure, not attack-success reduction. CWM has Brown/AMI and NYU/AMI bylines, not an inferred Meta affiliation; X-split leaves institution unspecified rather than guessing Yandex.

All local evidence is L0/L1diagnostic, not model capability, online lift or Evolve promotion. High-cost full experiments are explicitly not reproduced, review DONE, without automatic retries. Independent review caught masked exponential overflow in ECA/MRPD; the fix and extreme-value negative controls precede the frozen run.

A final cross-topic review added Jeveration, EgoJev and JEPA Dots. EgoJev's explicit-probability CPU postprocessing has its own frozen execution group. The completed17-component primary group and7 A100 measurements remain unchanged, not overwritten or presented as new runs. The added full generation/robotics training campaigns are review-only and not reproduced.

[Coverage](../../../research-audits/nov19-latest/source-coverage.json) · [Priority source review](../../../research-audits/nov19-latest/priority-primary-selection.json) · [Delivery ledger](../../../research-audits/nov19-latest/task-scope.json) · [Cost preflight](../../../research-audits/nov19-latest/preflight.json) · [Actual CUDA run](../../../research-audits/nov19-latest/raw-cuda.json)

## Complete list

| Domain | Paper | First publication | Local delivery |
| --- | --- | --- | --- |
| agent-research | [Agentic Harness Engineering Beta: Requirement-Centered Evolution of Agent Harnesses](../../../agent-research/2611.24924-ahe-beta/README-en.md) | 2026-11-18 | l0_interface |
| agent-research | [Can Programs Replace LLM Judges? Executable Program Judges for Scalable and Efficient Relevance Labeling](../../../agent-research/2611.24849-execjudges/README-en.md) | 2026-11-18 | l0_interface |
| agent-research | [Kaer: Security-Aware Replanning for Multi-Agent Systems](../../../agent-research/2611.24839-kaer/README-en.md) | 2026-11-18 | l1_mechanism |
| agent-research | [RSIBench-Infra: Can Agents Optimize Their Own Training and Inference Infrastructure at Production Scale?](../../../agent-research/2611.24395-rsibench-infra/README-en.md) | 2026-11-18 | Review only; full campaign not reproduced |
| agent-research | [Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates](../../../agent-research/2611.23651-safe-personal-rsi/README-en.md) | 2026-11-18 | l1_mechanism |
| agent-research | [SearchInject: Retrieval Exposure Control for Indirect Prompt Injection in Language-Model Search](../../../agent-research/2611.02643-searchinject/README-en.md) | 2026-11-02 | l1_mechanism |
| agent-research | [Reducing Inference Cost of Coding Agents with Timeout Cascades](../../../agent-research/2611.24324-timeout-cascades/README-en.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [Counterfactual World Models: JEPAs That Reason About "What If"](../../../foundation-models/2611.24778-counterfactual-wm/README-en.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [Kernel Ridge Attention: Nonlinear Memory with Selective Forgetting](../../../foundation-models/2611.23896-kernel-ridge-attention/README-en.md) | 2026-11-18 | l1_mechanism |
| foundation-models | [LoopCache: Accelerating Long-Context Self-Speculative Decoding for Looped Transformers](../../../foundation-models/2611.24301-loopcache-interface/README-en.md) | 2026-11-18 | l0_interface |
| foundation-models | [NarrowSpec: Draft Hidden Width Need Not Match the Target in Speculative Decoding](../../../foundation-models/2611.23835-narrow-spec/README-en.md) | 2026-11-18 | l1_mechanism |
| multimodal-models | [Autoregressive View Model](../../../multimodal-models/2611.23417-autoregressive-view-model/README-en.md) | 2026-11-17 | Review only; full campaign not reproduced |
| multimodal-models | [JEPA Dots: Dual-Latent World Model for Language-Guided Robot Control](../../../multimodal-models/2611.24062-jepa-dots/README-en.md) | 2026-11-18 | Review only; full campaign not reproduced |
| post-training | [How Reward Gain Imbalance Shapes Ranking: Rethinking Rubric-Based Reward Aggregation](../../../post-training/2611.24005-dcc-aggregation/README-en.md) | 2026-11-18 | l1_mechanism |
| post-training | [Evidence-Based Credit Assignment for Search-Augmented Language Models](../../../post-training/2611.23824-eca-credit/README-en.md) | 2026-11-18 | l1_mechanism |
| post-training | [HINT-WAM: Hindsight-Informed Training for World Action Models](../../../post-training/2611.24789-hint-wam/README-en.md) | 2026-11-18 | Review only; full campaign not reproduced |
| post-training | [Beyond Replacement: Levenshtein Editing for Diffusion Language Models](../../../post-training/2611.23750-led-edits/README-en.md) | 2026-11-18 | l1_mechanism |
| post-training | [Replay, Don't Resample: Off-Policy Consolidation of Long-Horizon RL Experts](../../../post-training/2611.24059-mrpd-replay/README-en.md) | 2026-11-18 | l1_mechanism |
| recommendation | [MARS Technical Report](../../../recommendation-components/2611.24006-mars-fapo/README-en.md) | 2026-11-18 | l1_mechanism |
| recommendation | [MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems](../../../recommendation-components/2611.23910-mle-agents/README-en.md) | 2026-11-18 | l0_interface |
| recommendation | [X-split Argus: Learning Reusable History Tokens for Efficient CTR Prediction](../../../recommendation-components/2611.24283-xsplit-argus/README-en.md) | 2026-11-18 | l1_mechanism |
| system-one | [EgoJev: Finding Evidence in Egocentric Video by Reading VLM Decisions](../../../system-one/2611.24616-egojev/README-en.md) | 2026-11-18 | l1_mechanism |
| system-one | [Jeveration: System One Models Now Generate](../../../system-one/2611.24738-jeveration/README-en.md) | 2026-11-18 | Review only; full campaign not reproduced |
