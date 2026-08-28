# Project agent requirements

## GPT-5.6 SOL restrictions

- When the active model is GPT-5.6 SOL and the user asks any question or requests any work about this repository, **never invoke the Superpowers plugin or any skill provided by that plugin**.
- This prohibition includes, but is not limited to, `using-superpowers`, `brainstorming`, and any other current or future Superpowers-provided skill.
- This is a mandatory project-level user requirement. It takes precedence over generic instructions that would otherwise require or recommend a Superpowers skill.

## Paper reproduction documentation

- Every paper reproduction README must include a clearly labeled paper-information block near the top.
- The block must list the paper link, company or author institution, exact original publication date, whether the original authors released source code (including its link when available), the local adapter key, and the local reproduction-code directory.
- An absent upstream repository must be written explicitly as not found/not released; never omit the field.
- New or updated reproductions must keep this metadata complete and covered by documentation tests.

## GPU validation gate

- Any new or materially upgraded implementation whose advertised path requires CUDA must be executed on a real NVIDIA A100 or A30 before its MR is declared complete.
- The adapter must set `requires_gpu_validation=True` and point `gpu_validation_artifact` at a committed sanitized receipt accepted by `scripts/validate_gpu_evidence.py`.
- Receipts must include the public dataset/checkpoint revision, command, seed, metrics, accelerator model and commit, while excluding hostnames, SSH aliases, usernames, driver/build strings and checkpoints.
