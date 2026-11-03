# October 14 MBS and SOAR failure diagnostics: evidence boundaries

<!-- source-sha256: d7356b940726b48edb1b1ccf88dea66c39bb275c172669040699512270769eef -->

[简体中文](../../research-audits/oct14-mbs-soar-diagnostic-review.md)

This audit first examined existing raw runs without changing them. The subsequent changes only improve local diagnostic records and remove ambiguity in SOAR's slash placeholder. No CUDA run or download was initiated in that step, and rewards, parsers, gates, and sampling budgets were unchanged. CPU fixtures are not capability evidence. Earlier failures remain intact, with no fabricated responses or rejection reasons.

## Executed bounded MBS seed 42

- Execution source: `0f5dca9f7f0319c6e3bb57aa578cfe26499a6e7e`; all 52 launch source SHAs match this revision. Unchanged budget: 16 training candidates, group 4, cap 1,024, at most four hard roots, depth 1, two decomposition and two synthesis retries, and two teacher attempts.
- Raw failure: `.cache/oct14-post-training/mbs-bounded-raw-attempt02/evidence/failure.json`, SHA256 `adcca5400a7e38042407eba85ffac4a8d44ada3493fce8c06ca3b09c94d69df0`. Exit 1, 348.2407392859459s, 36,129 actual generated tokens including 1,541 existing validation-baseline tokens. “Train-only” limits candidate construction/calibration, not whether the original invocation evaluated validation.
- Hard roots were training indices 4, 7, and 8, each with zero successes across four actual untruncated rollouts. Passing hardness is not independent teacher verification or Goldilocks success.
- Construction recorded root 4 hardness, root 7 hardness/failed verification, and root 8 hardness/failed verification. Root 4 formed no usable tree. The run paid one batch each for student and teacher effectivity baselines and two construction-teacher calls. With no scaffold/effectivity audit, control flow and costs narrow root 4 to failure to form at least two verified children; without original responses, JSON, fields, truncation, and independent-solution failures cannot be distinguished. This is inference from code and costs, not preserved per-rejection traces. No target-policy-Goldilocks audit exists; do not claim all three roots failed Goldilocks.
- `paired_rl_root_indices=[]`; neither method nor control entered RLVR. This failure is not a passed receipt.

Gold scope in the original MBS source: `CheckpointConstruction.verify` sends only questions to independent solvers; answers stay in the external scorer. Effectivity allows independent child worked examples, never the parent answer or complete parent plan in the evaluated policy. `teacher_json` contexts for decomposition, synthesis, scaffolding, and blueprints can see training parent/candidate answers and traces. Do not claim all teachers or generation calls are gold-free.

## Executed SOAR 7B format probe

- Execution source `57b2314db1d5b8a8ebeb0aa7fbb6b7fee523df55`; all 54 recorded source SHAs match. Fixed `Qwen/Qwen2.5-7B-Instruct` revision `bb46c15ee4bb56c5b63245ef50fd7637234d6f75` and `Elliotes/EcoAgent` revision `bc5db40a20b254c5249401d2220ea71b06c86a5c`. Two attempts on each of the first four questions in the separate catalog training QA.
- Raw `.cache/oct14-post-training/soar-format-raw-attempt02/evidence/diagnosis.json`, SHA256 `22d58ccfac06e99547d9f50391f8920b5eb7539cb37355670ec6a614bc0b6d9b`. Probe exit 0 means the diagnostic executed, but result is `no-format-signal`, whole-method GPU validation=false. Outer 34.612656300887465s, inner 32.17066810838878s, 433 actual generated tokens.
- All eight first turns `invalid`, `truncated=false`; lengths 51, 48, 23, 107, 50, 49, 51, and 54. Search=0, format=0, source-match=0. No LoRA/optimizer updates, assessment, or validation/test data read.
- The old SYSTEM required think then search or source+answer. It used placeholder `<information_source>internal/external</information_source>`, while the parser accepts exact `internal` or `external`. CPU counterexamples reject literal slash copying and accept each separate template. This static ambiguity is not the established cause of the eight real failures.
- The old probe stored only response-text SHAs, lengths, and truncation flags, not text or token IDs; runtime did not print individual responses. Do not quote or reverse hashes or claim the model copied the slash, omitted tags, or used wrong capitalization.

## Local diagnostics, not retroactive evidence

The SOAR SYSTEM lists two legal final-answer templates without changing think/search/source/answer semantics, parser, reward, or budget. The format probe records actual policy text, token IDs, SHA, and truncation. It registers incomplete episodes at start and retains returned turns on errors without inventing final answers, reward, or completed state. Run only on the fixed training prefix and do not add train gold or tool answers as examples.

MBS records actual calibration, effectivity, construction-teacher, and question-only verification responses with roles, input-gold scopes, original token IDs, SHAs, truncation, and external verdicts. Each construction continue branch records its rejection reason without additional samples. Failure/interruption payloads retain observed traces. Local responses can include training construction answers and must not be copied into sanitized GPU receipts.

New source at this initial checkpoint had not run on GPU. Later probes require a separately frozen source, immutable attempt directory, original budget, and explicit authorization. Do not rebind old failures or claim passed GPU gates from CPU fixtures.

## October 14: new b908 response diagnostics

Both actual runs used `b90862754bf51b1beeb5add3f7dc2a51ca00ace4`; 54 source files matched Git and CPU independently verified response hashes and token lengths. No historical responses were backfilled.

- MBS stayed within the original budget: exit 1 in 343.03794s; failure SHA `a86f6e78c3a9c2c4abd1dbcfcf9c520db64d9bfd7d339c5d367ae20001916a0a`. Root 4 passed independent solving, but each decomposition verified only one child. A second child lacked quantities/relations; independent answers 104, 2p, or 2 differed from proposed answers. Roots 7/8 were also solved incorrectly by the teacher. All eight rejections were untruncated and numerically unequal, with no evidence of rejecting an equivalent numeric notation. No qualified descendants or RL updates; no passing receipt.
- SOAR original train-only probe exit 0 in 35.97100s; diagnosis SHA `29f7478df63701917e2f5370ca502712c7f320a17d7abd8b29250217025a8b1f`. Three valid traces, two source matches, and three real retrievals. Two samples on one question received different source rewards that become equal without the source term. Accuracy and optimizer updates both zero. Format signal only, not whole-method acceptance or capability gain. Full training and ablation were run separately.

MBS §3.3 and Appendix E require self-contained children, correct worked solutions, and concise final answers. The previous prompt already asked for self-containment. The revision operationalizes it: include all quantities, units, time ranges, relations, and assumptions in question, without relying on parent/siblings or answer/trace fields; trace explains the solution and answer is a single number. This neither recreates the unpublished production wrapper nor guarantees arithmetic correctness. Independent verification still reads question alone; do not add parent context, change JSON schema/verifier/retries/budget, or inject training numbers, answers, or examples. Freeze and rerun new prompts on GPU; do not rebind b908.

## Actual 5c self-containment rerun

`5c863ab8`, unchanged budget: exit 1, 322.58302s, failure SHA `6597edd5e23e3c776d20bba3fdb631205e32a61e5f978ab47ee7fa3c69eee0b6`. Same three hard roots, empty paired roots, zero RL updates. Root 4 emitted two invalid JSON object arrays: unescaped newline inside a string and a malformed string array. The parser could extract only partial objects, not a valid two-child array. Other roots failed independent verification. No auto-repair or acceptance of fragments.

The next change clarifies JSON escaping and object-array type in the same generic child instruction. Parser, schema, sampling, retries, and budget remain unchanged. CPU regressions reject invalid arrays without repairing them. This is interface clarification, not better math or guaranteed synthesis. Freeze source and run separately; do not mark the 5c failure passed.

## 773 negative result and a new optional grammar path

`773da4e3` failed in 330.631s with 35,413 generated tokens, two invalid outer JSON payloads, empty paired roots, and zero RL updates. Three separate sanitized failures stay on the paper page, without repairing outputs or overwriting raw data.

Appendix E describes serialization enforcement without releasing the wrapper. Local `f92413aa` supplies **explicitly optional** XGrammar token-level JSON Schema generation, not a recreation. It constrains construction teacher fields, types, and the existing two-child requirement, without forcing numeric answers or true booleans. Independent solving, student sampling, effectivity/novelty/Goldilocks, and RL gates remain unchanged. Missing dependencies or compile failures do not fall back.

A100 preparation verified 54 source files and original public resources byte-for-byte. Five schemas compiled on CPU under XGrammar 0.2.8 with the actual Qwen tokenizer/vocab 152064, without model loading or CUDA initialization. One same-budget seed-42 GPU attempt was registered independently as attempt06, capped at 1,800s with no added retry. Only actual outputs and complete core execution establish passing; CPU compilation/tests and legal formats do not establish math or GPU acceptance.

Attempt06 exited 1 at 374.2966s and 36,728 tokens. Both proposals were valid two-child JSON, but all four children failed both independent checks. No descendants or RL updates. The [separate failure record](../../reproductions/2610.12659-magicbeanstalk/metrics/public-a100-schema-failed-seed42-f92413aa.json) binds nine raw/source/dependency artifacts and is not a passed receipt.

Actual XGrammar CPU matching then showed `sort_keys=True` serialized answer→question→trace, accepting answer-first and rejecting question-first. New `ce4a4a34` uses explicit question→trace→answer order and binds that order in the compiled cache and audit SHA. All five schemas compiled using the actual tokenizer, accepting question-first and rejecting answer-first. Default non-schema path, budget, verification, and RL are unchanged. This verifies a structural issue, not the cause of all underspecification/math failures. Run attempt07 independently at the same budget without rebinding old failures.

Attempt07 exited 1 at 351.71331s, 36,425 tokens, and 86 actual responses. Both proposals were legal two-child JSON. Of 12 independent checks, only the training root and one child passed. Construction 450 tokens, verification 2,757, validation 1,541, calibration 29,408, student effectivity 1,231, and teacher effectivity 1,038 match total usage. No valid descendants, `paired_rl_root_indices=[]`, and zero RL updates. These adjacent failures cannot attribute mathematical changes to field order. Structure was fixed; content quality gate failed. Keep attempt07 and the four earlier failure records independently, without another blind retry.
