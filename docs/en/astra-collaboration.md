# Project collaboration guide for GPT-6 Astra

<!-- source-sha256: 88137cfde494d25e99861cecf32bd360a0c53d95df02cb8f343610eadbeff3d4 -->

[简体中文](../astra-collaboration.md)

The root `AGENTS.md` describes how coding assistants work in this project. With GPT-6 Astra selected, the assistant should use existing context to finish the task, preserve research evidence, and verify in proportion to risk. There is no need to paste the workflow for every paper.

## Official guidance and scope

The [official OpenAI GPT-6 Astra guide](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-6-astra) was checked on 2026-09-08. This project adapted its instructions for persistence, skill conflicts, output style, parallel scope, and verification cost. The rules below are project engineering choices.

This adapts collaboration instructions only. It does not change experimental models or API providers. `AGENTS.md` cannot select the actual model, enable asynchronous tools, or change reasoning effort; the hosting application or API request controls those. Runtime integration changes require their own interface compatibility checks and verification.

## How to give a task

State the goal, scope, and acceptance result. The assistant can choose the implementation route from existing code. For example:

> Scan papers after the last audited window across existing domains, prioritizing Google and Meta. Use the existing evidence thresholds. Implement feasible items, update docs and evaluations, and submit one PR. Validate CUDA implementations on an existing A100 or A30 and report unfinished items.

> Fix overflow in the public dashboard table. All columns should be visible on desktop and readable on mobile. Check the rendered page and documentation build.

> Review whether the agent implementation reads gold answers. List file locations, impact, and recommended fixes.

The first two are implementation tasks; the third is review. “Continue” means resume the unfinished goal. Fold status requests and added constraints into the current task. Explicit decisions are needed for major scope or budget changes, not ordinary implementation details.

## What counts as done

| Work | Reviewable completion evidence |
|---|---|
| New paper | Primary evidence, correct metadata, actual algorithm, Chinese and English write-ups ([bilingual maintenance](contributing.md)), four levels of Q&A with illustrative examples, incremental analysis and update log for the relevant deep dive, experiments, and explicit fidelity tier |
| Evolve integration | The controller can execute candidates and produce evaluable results, with isolated data splits during selection |
| CUDA path | Actual A100/A30 execution and a sanitized receipt tied to the implementation commit |
| Documentation | Links and generated sources agree; relevant builds or page checks pass |
| PR submission | Accessible PR link, accurate scope, completed checks, and any remaining gates |

Mechanism counters, simulated trajectories, and gold-answer fixtures only demonstrate the corresponding diagnostics. Neither a success rate of 1 nor three seeds establishes real agent capability. CPU shape tests do not replace CUDA execution.

## Verification scope and resumption

Apply the mandatory cost gate from the root instructions first. Resources are one A100 or A30 or a local Mac, not multiple GPUs. When paper configuration, upstream requirements, or existing measurements establish high cost, mark **not reproduced due to cost (review DONE)**, record model/data scale and supporting evidence, and continue with feasible papers. Do not download large resources, launch trials, or repeatedly expand budgets to establish an already evident cost. Multiarms and multiseeds expected to take hours, severe local swap, and insufficient single-GPU memory all trigger the gate. An estimate is not a measurement. If a major cost uncertainty cannot be resolved with cheap read-only checks, mark not reproduced. Resume only when the user explicitly requests it after seeing the cost.

This also applies to previously authorized but unfinished expensive work. Deferred papers may remain cataloged and reviewed. Keep results and failures, but do not label them as completed implementations or executable Evolve operators. Do not block other deliveries, fabricate GPU receipts, or weaken algorithm requirements. The rule applies to all domains and coding models, not only Astra.

**High-cost non-reproduction is a terminal review decision, not a TODO waiting for compute.** Once the cost basis and decision are recorded, it does not block the batch or review cutoff and is not automatically queued again. The machine ledger retains `deferred` for compatibility; the catalog retains `deferred_high_cost`. New decisions can use `resolution: not_reproduced_high_cost`. None means implemented. No code, metrics, or GPU receipt is required for this disposition. Finish any outstanding searches or other candidate reviews without treating closed items as blockers.

For prose, check docs and links. For algorithms, check equations, data flow, and targeted tests. Shared executors, registries, or broad changes may require the full gates. Do not repeat a passed check without a new edit or finding. CI workflows define the actual commands.

For long tasks, retain completed and pending scope, branch and commit, artifacts, and pending checks. Verify actual state before resuming to avoid rerunning completed experiments. Parallel reads and independent checks can save time; subagents must follow the environment's authorization rules.

## How to evaluate these instructions

Observe the following scenarios in real future tasks and record what happens. This is an acceptance plan, not a completed model comparison.

| Scenario | Expected behavior |
|---|---|
| Explicit batch implementation request | Finish the batch or report actual blockers item by item; preserve reviewable code and evidence |
| Mid-task status request or “continue” | Answer with current status, resume unfinished work, and retain accepted constraints |
| A skill suggests another confirmation | Use existing authorization; if it truly blocks work, cite the exact file and clause |
| Prose-only update | Run relevant doc checks; do not retrain or rerun unrelated full tests |
| Only CPU tests passed for a GPU path | Run on actual hardware or leave the GPU gate explicitly unfinished |
| New paper exceeds reasonable single-GPU/Mac budget | Record cost and mark not reproduced; review DONE, no cutoff block, download, trial, or automatic reopening |
| Agent fixture returns gold answers | Keep the diagnostic label and expose the capability implementation gap |

Compare completion rate, extra confirmations, repeated checks, and evidence completeness before adjusting the rules. The GPT-5.6 SOL Superpowers restriction remains in the root instructions, with the scope defined there.
