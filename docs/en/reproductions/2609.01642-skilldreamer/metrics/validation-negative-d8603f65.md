# Negative 7B diagnostic on eight fixed validation items

<!-- source-sha256: 37494b41ba72b4e1d9a7442a863b089cd0963065b35677670bc9deaf30dab4e5 -->

[简体中文](../../../../reproductions/2609.01642-skilldreamer/metrics/validation-negative-d8603f65.md)

On 2026-10-14, the pinned Qwen2.5-7B-Instruct revision `bb46c15ee4bb56c5b63245ef50fd7637234d6f75` ran a seed-42 question-only format probe on a real NVIDIA A100. The algorithm source was `0f5dca9f` and the independent probe source was `d8603f65`. Budget: 600-second hard limit, 240 calls, 256 tokens per call, 8 tool actions, and top-k 3. Only fixed validation IDs `13/1/4/6/23/21/14/15` were used, with no gold or scorer and none of the 16 evaluation IDs.

The run took 596.9424 seconds, 210 calls, and 29,194 generated tokens, completing all eight call flows. This is not a passing mechanism check. PSG/HSR ran on seven items; real CSI and gallery loading occurred twice each, with zero tool actions or submitted answers. Retained as a **negative validation diagnostic** with no passing receipt, no promotion, and no capability comparison.

See the [sanitized artifact](../../../../reproductions/2609.01642-skilldreamer/metrics/public-a100-validation-negative-d8603f65.json) for metrics, provenance, and per-item classification. The [final](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-negative-d8603f65/seed42.json), [partial](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-negative-d8603f65/seed42.partial.json), [210-call trace](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-negative-d8603f65/seed42.trace.jsonl), and [CPU classification](../../../../reproductions/2609.01642-skilldreamer/metrics/raw/validation-negative-d8603f65/trace-analysis.json) are byte-for-byte copies with SHA-256 values in the artifact. Model responses are not gold answers.

## Failure classification

| Validation ID | Calls / tokens | Runtime calls | Missing/invalid JSON | CSI row order/absence | Invalid decision | Empty fields | Requery after valid load |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 13 | 1 / 208 | 0 | PSG JSON syntax error | 0 | 0 | 0 | 0 |
| 1 | 30 / 4309 | 24 | 5 | 18 | 1 | 0 | 0 |
| 4 | 30 / 4153 | 24 | 0 | 13 | 8 | 2 | 1 |
| 6 | 30 / 3353 | 24 | 7 | 9 | 7 | 0 | 1 |
| 23 | 30 / 3920 | 24 | 0 | 4 | 14 | 6 | 0 |
| 21 | 30 / 3939 | 24 | 0 | 4 | 18 | 2 | 0 |
| 14 | 30 / 5194 | 24 | 0 | 12 | 12 | 0 | 0 |
| 15 | 29 / 4118 | 24 | 0 | 19 | 5 | 0 | 0 |

The execution-order categories are mutually exclusive. Of 168 runtime CSI calls, 12 had no valid action JSON, 79 missing or misordered rows, 65 invalid first DECISION words, 10 empty fields, and two actual loads. All seven items exhausted 24 runtime calls instead of finishing normally.

After ID 4 loaded rates at global call 51, calls 52–61 had five missing-line and five invalid-decision failures. ID 6 loaded arithmetic at call 90. The original enum gate rejected call 91's `DECISION: Load the arithmetic skill.` All eleven post-load responses had fewer than 256 visible tokens, so truncation does not explain them. Longest input was 822 tokens, below 2,048. Forty-one visible outputs reached 256 (33 pseudo guidance and eight CSI); the trace has no per-call token IDs or stop reasons, so none are invented.

## Distinguish prompt ambiguity from parser failure

Lines 126–131 of the frozen `algorithm.py` request five labels and mention MATCH/PARTIAL_MATCH, but do not specify five nonempty `LABEL: value` lines or all four supported DECISION first words. Lines 134–146 enforce order, colons, nonempty values, and `MATCH/PARTIAL_MATCH/NO_MATCH/NO_CAPABILITY_GAP`. This is an **underspecified prompt contract**, not a confirmed parser bug.

Two five-line responses with valid action JSON but invalid enum values were ID 4/call 54 (`DECISION: Use the rates skill to calculate the reduced hourly wage.`) and ID 6/call 91 (`DECISION: Load the arithmetic skill.`). Two responses with legal `DECISION: MATCH` and calculator JSON (ID 4/call 55 and ID 15/call 196) lacked the fifth NEXT line. The CSI line contract, not JSON parsing, rejected them. No fully valid CSI response was rejected by action JSON parsing.

Requerying after first load is explicit in `execute_agent`: the model sees real gallery content before producing a fresh action. Every environment step, including finish, counts. Zero actions and answer=null show no tool entry was reached. No actual unknown-tool execution or tool RuntimeError occurred.

Later prompt clarification only adds nonempty colon lines, the complete enum, and JSON placement. Parser, enums, PSG/HSR/CSI, autocorrection/fallback, gold roles, IDs, and budgets are unchanged. Templates do not inject answers or skill judgments. CPU fixtures verify strict rejection and post-load calculator/finish access, not model capability. See [core execution without submissions](validation-no-submit-5c07ef42.md) for the separate 701f/5c07 measurement at the same budget. **This negative result remains bound to 0f/d860**, not the clarified prompt. Original 0.5B three-seed failures remain recorded.
