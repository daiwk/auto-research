# Native validation after five-line clarification: core execution, zero submissions

<!-- source-sha256: 1857921c0b58b74d94ad09cc27c413a736d0e35e9a2fed6ecc18d319e9f4c63e -->

[简体中文](../../../../reproductions/2609.01642-skilldreamer/metrics/validation-no-submit-5c07ef42.md)

On 2026-10-14, the sole seed-42 probe ran on a real NVIDIA A100 with algorithm source `701f45007be75cf6153f98812ef94e087c94a8f0` and runner `5c07ef42bbb008e7adc3fc03fd5e85695c2bcc86`. It reused Qwen2.5-7B-Instruct `bb46c15ee4bb56c5b63245ef50fd7637234d6f75`, MiniLM `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`, and eight validation IDs. The model saw questions only; no gold/scorer or 16 evaluation IDs. The same dual 600-second hard limits, 240 calls, 256 tokens per call, eight actions, and top-k 3 applied, without retries or expansion.

Exit code was 0; launcher time 401.4411 seconds (runner 400.5552), 159 calls, and 19,369 tokens. PSG and HSR each ran on seven items, with 65 real CSI calls, seven gallery-loading episodes, and nine post-load fresh-action queries. There were 56 **environment step calls**, not successful tool calls: 48 of 54 calculator attempts succeeded, six errored, and two calls requested unknown tools. **Zero finish calls and zero submissions**: no passing receipt, improvement or task-success claim, or external accuracy scoring.

The [diagnostic artifact](../../../../reproductions/2609.01642-skilldreamer/metrics/public-a100-validation-no-submit-5c07ef42.json) records sources, budget, and raw SHA values. The [final](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/seed42.json), [partial](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/seed42.partial.json), [159-call trace](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/seed42.trace.jsonl), and [CPU replay/classification](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/submission-analysis.json) are unchanged; [sanitized exit](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/exit.sanitized.json) records the original exit SHA. The 0f/d860 result and 0.5B three-seed failures are not attributed to this source.

| Validation ID | Calls / tokens | CSI | Skills loaded | env.step | Calculator success / error | Unknown tools | Repeated successful expressions | Finish |
| --- | --- | ---: | --- | ---: | --- | ---: | ---: | ---: |
| 13 | 1 / 208 | 0 | None (PSG failure retained) | 0 | 0 / 0 | 0 | 0 | 0 |
| 1 | 28 / 3198 | 9 | scheduling | 8 | 1 / 6 | 1 | 0 | 0 |
| 4 | 17 / 2321 | 9 | rates | 8 | 7 / 0 | 1 | 4 | 0 |
| 6 | 27 / 2932 | 9 | arithmetic | 8 | 8 / 0 | 0 | 3 | 0 |
| 23 | 19 / 2481 | 10 | money, arithmetic | 8 | 8 / 0 | 0 | 7 | 0 |
| 21 | 16 / 2167 | 9 | rates | 8 | 8 / 0 | 0 | 6 | 0 |
| 14 | 25 / 3257 | 10 | money, arithmetic | 8 | 8 / 0 | 0 | 4 | 0 |
| 15 | 26 / 2805 | 9 | rates | 8 | 8 / 0 | 0 | 4 | 0 |

117 runtime calls divide into nine loads, 56 env.step calls, and 52 schema failures. All seven executed items exhausted eight actions without submission. The 28 repeats are an auditable lower bound: same AST as a prior successful expression whose result was already in the current observation history. Gold was not used.

## Two kinds of evidence for zero finish

**Policy stalling and noncompliant choices.** ID 21/call 100 computed `5 * 2 * 5` and received `Calculator result: 50`. The actual call 101 prompt included it, yet SUBGOAL repeated the distance calculation and NEXT/JSON called the same expression again. The pattern continued. None of the 65 valid CSI NEXT lines mentioned finish/submit. A self-reported unresolved subgoal is not a missing result; the API preserved feedback. Other items also repeated successful expressions or moved from a computed total back to local steps. Without a scorer, this does not establish answer correctness.

ID 1/call 20 requested `assess_capability`; ID 4/call 38 requested `load_skill`. The environment returned `Invalid action schema` without correction. Six calculator errors involved natural-language equations, statements, or unsupported operators. These are real requests and tool errors, not implicit successful execution.

**Unequal API descriptions.** The frozen `execute_agent` gives the baseline a generic `SYSTEM_PROMPT` specifying calculator, finish, and arithmetic-only expressions. The skill `capability_context` only gave JSON examples for calculator/finish, without equivalent semantics or explicitly explaining that five-line CSI and skill-ID loading are not extra tools. This disparity is visible in source and prompts; **its causal effect on zero finish was not isolated**. Keep the 28 repeated successful computations distinct from the description gap, without attributing everything to prompting or model capability.

## Independent CPU replay and follow-up limits

The public artifact includes exact frozen [701f algorithm](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/frozen-source/skill_probe_701f/skilldreamer/algorithm.py) and [environment](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-no-submit-5c07ef42/frozen-source/skill_probe_701f/state_opd/environment.py). `tests/test_skilldreamer_native_no_submit.py` imports those sources in an isolated namespace and replays responses from seven episodes, checking each complete prompt and returned field without newer prompts, fresh model outputs, or CUDA.

The follow-up changes API descriptions only: calculator and finish are the only tools; calculator returns a value without submitting; explicit finish submits and stops; capability assessment is five lines rather than a tool; executor loads skill_id and shows actual gallery content before requerying. No `load_skill` or `assess_capability` tool, problem numbers, gold, ID-specific answers/skill judgments, forced finish, or automatic policy adjustment based on the 28 repeats. Parser, gallery, executor, and action budget remain unchanged. **The added API wording was not GPU-tested and cannot rebind this record or establish causal or capability improvement.**
