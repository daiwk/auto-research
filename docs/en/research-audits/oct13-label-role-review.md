# 2026-10-13: Label access and state counter roles

<!-- source-sha256: 84c06147b7dcee1374076398c035c5684244b297db0b8636055051a4b3a231a8 -->

[简体中文](../../research-audits/oct13-label-role-review.md)

This manual source-role review is not capability acceptance. It checks answer flow, generation messages, objectives, and counters across 14 added or changed AST inventory files. GPU status is tracked [separately](oct13-gpu-todo.md).

| Source / role | Label boundary | Counts and limits |
|---|---|---|
| `oct13_common.evaluate`, State `evaluate` | Model receives questions only; answers go to external scorer | Preserve accuracy=0; real updates are not capability gains |
| Difficulty curriculum `run` | Current policy rolls out questions only; verifier correctness controls difficulty | Validation selects stages; zero effective updates do not advance. Length reward is not correctness |
| MagicBeanStalk construction and verification | Offline teacher can see training problem/trace. Independent re-solving sees only question; student scaffold excludes parent answer and full plan | Teacher effectivity/novelty is not formal proof; rejections and recalibration count toward cost |
| Progressive contraction | Question-only teacher and continuations; answers verify; verified teacher tokens are train SFT targets | Separate profiling cost from reduced exposure, not total-compute savings |
| SynthSelf | Training-only aligner/self-builder uses train answers for rewriting; evaluated student sees only question | Target NLL is not a generation hint; Eq. 6 failure remains failed, not promoted |
| UPTURN | Answers produce training labels, rescue rewards, and external evaluation only; inference gate and cut head do not read answers | Encoder/token costs reflect calls; new rounds concatenate original tokens rather than re-encoding |
| SOAR | Policy/internal recall/retriever have no gold; `final.answer` is submitted by the model; row.answer only feeds reward and scorer | External corpus must be independent public knowledge, not an answer store. Actual trajectory cost is recorded |
| SkillDreamer | Input is question and generic skills; references stay in separate scorer; PSG/HSR/CSI take no reference | Calls and tokens come from model.generate. Skill loads are not success |
| Beyond / ReplaySSM | Search and refresh counts describe executed paths only | They do not alone establish retrieval success, kernel bandwidth, or task capability |

Behavior tests cover question-only generation, scaffold leakage rejection, exact prefixes, zero-advantage rejection, and cost accounting. The AST inventory does not cover dynamic keys or full-program taint propagation. It is not a semantic proof.

Network pauses do not relax CUDA gates for new or changed paths. Missing or stale receipts remain open.

After the October 14 diagnostic changes, another item-by-item comparison found only moved line numbers for ten MBS checkpoint entries and four SOAR entries, with unchanged expressions and enclosing functions. Saved MBS model outputs diagnose training construction only. Independent validation sees only questions and the trace labels train-side answer visibility. SOAR traces exclude scorer gold; source-template clarification does not change parsing or reward. The reviewed inventory still covers 140 files. CPU tests for gold isolation and interruption traces passed. Neither the syntax inventory nor those tests substitute for semantic proof or GPU receipts.
