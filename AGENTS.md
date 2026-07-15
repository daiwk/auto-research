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
