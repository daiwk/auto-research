<!-- source-sha256: fbce43d521d6c0b0818c0868da0fb42fc54bbac60d2a90b65f138a8c0b7a1fdf -->

# Domain adapters for automated evolution

[简体中文](../evolution-domains.md) · [Automated research overview](auto-research.md)

## Paper operators added on 2026-08-29

- **Post-training:** `ttpo`, `weak-guide-rlvr`, `uc-mopd`, and `spear` are now objective, rollout, or reward candidates that can be inherited and combined.
- **Agents:** `swe-prime`, `harnesslens`, `covemem`, and `spt` are available in the policy, verifier, memory, and data/skill slots.
- **`friend-gnn` is not connected to the RankMixer genome.** A GNN over a friendship graph does not fit the current sequence-ranking slot. Forcing that mapping before a graph-model genome exists would make a false claim about composability.

These names refer to papers already implemented in the repository with public experiment artifacts. They are not architectures invented at runtime.

Auto Research is an extensible research protocol, not a single recommendation model. Any domain that supplies a research object, data, searchable changes, and an evaluator can reuse paper retrieval, parallel experiments, selection, and multi-round iteration.

!!! info "Finding a paper does not implement it"
    Online retrieval discovers evidence. Executable mutations must already be implemented and tested in the repository. The controller combines only allowlisted operators and parameters; it does not execute arbitrary code from paper text or model output. See the [guide to candidate sources](model-evolution.md#candidate-sources) for a complete example.

## Shared adapter contract

```mermaid
flowchart LR
    I["Topic / current system"] --> P["Paper evidence"]
    P --> H["Hypothesis + mutation"]
    H --> T["Trainer / executor"]
    T --> V["Validation evaluator"]
    V --> S["Selection + research memory"]
    S --> H
    S --> O["Isolated test + report"]
```

A domain adapter declares the following interfaces:

| Interface | Purpose |
|---|---|
| Research object | The model, agent policy, training recipe, or other system to optimize. |
| Evidence source | The scope of paper retrieval and the architectures or training methods eligible for adoption. |
| Mutation space | Changes to architecture, data, post-training, tool policies, and hyperparameters. |
| Trainer / executor | An isolated entry point for training or episode execution. |
| Validation evaluator | A fair metric that determines which candidates advance without accessing the final test set. |
| Artifact contract | Configuration, parent–child relationships, traces, metrics, and a report in Chinese. |

## Built-in domains

| Domain | Automated evolution implemented | Reusable paper components | Current status |
|---|---|---|---|
| Search, ads, recommendation, and LLM applications | RankMixer and HyFormer on MovieLens and public recommendation benchmarks. | Architectures such as LONGER, UniMixer, and RankMixer, plus industry paper adapters. | **Runnable** |
| Foundation models | micro-LLM search in rounds covering architecture, data recipes, and efficiency operators. | Mamba, Switch Transformer, sparse attention, conditional memory, quantization, and dynamic computation, among others. | **Runnable** |
| LLM post-training | A paper-constrained objective genome; multi-round search over algorithms, learning rate, group size, and training steps. | All current post-training adapters: PPO/DPO/GRPO, preference optimization, OPSD/OPCD/Lightning OPD, process rewards, and curriculum RL. | **Runnable** |
| Agents | A paper-constrained composable genome; per-round search over memory, planner, tool, critic, and capacity. | ReAct/LATS/ART, Voyager/AutoGen/PEARL, LOOP/WebAgent-R1/MUA-RL, Agentic RL/OPD, and software agents. | **Runnable** |

!!! note "Agent execution"
    Agent evolution can use a deterministic episode evaluator. With `swebench-local`, it can also create a temporary repository and perform real edits and tests. Paper retrieval maps only to audited operators; papers without a safe mapping remain evidence only.

## Audit of paper-to-evolution mappings

- **Post-training:** Every algorithm in `post_training.models.ALGORITHMS` has a paper mutation. Since OPSD and OPCD were added, tests have enforced coverage of the full set so a standalone reproduction cannot be completed without its corresponding genome mapping.
- **Agents:** Except for the `long-context` fairness baseline, all current paper methods map to a memory, planner, tool, or critic operator. This update fills the earlier gaps for Voyager, AutoGen, and PEARL and adds LOOP, WebAgent-R1, and MUA-RL. Search-R1 also moved from the generic tool fallback to an explicit operator.
- **Recommendation and foundation models:** Only architectures the current evaluator can score fairly are integrated. Methods requiring proprietary data protocols, serving latency targets, or a byte-level backend remain evidence only. Listing a method by name does not show that the controller can search its core mechanism.

## Composable research

Methods need not be tied to one domain. For example:

- Use LLM semantic features, generative retrieval, or post-training objectives as mutations in recommendation evolution.
- Search architecture, pretraining data recipes, and efficiency operators in foundation-model evolution, with the option to compose post-training algorithms across domains.
- Combine memory policies, planners, tool context, and critics in agent evolution.
- Implement the same adapter contract for a new domain without modifying the research loop's selection and reporting logic.

[Read the complete evolution protocol and commands](model-evolution.md)
