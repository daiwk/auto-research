<!-- source-sha256: 10a030b1ec9e52a309b3ce4c11be621dba5bd955350a1032084242ef8527a98f -->
# Pre-execution review and source freeze

[简体中文](../../../../research-audits/nov20-latest/source-freeze-history/README.md)

`71aca03f-unexecuted.json` binds commit `71aca03fe0e77cd9a3f2dcad24dde77f76eb9d74`. This is an actual early source snapshot, **not yet used for the unified CPU or CUDA run**. It is neither a failed GPU experiment nor the final accepted version.

Independent review subsequently found an incomplete VisAlloc half-precision contract: fp16/bfloat16 inputs could fail at quantile, and finite extreme fp16 logits could yield NaN on the JSD path. The fixed upstream implementation promotes these statistics to float32. HiSA also had unsigned-position subtraction wraparound that could admit future keys; the fix validates uint64 range before using nonnegative int64 positions. Both fixes and actual diagnostic negative controls precede the new commit and source proof. Earlier independent CPU records keep their actual hashes rather than being relabeled as post-fix runs.

The final executed version is `15c4e1d105fe68c7556734ad50ad6022061dd11a`. Unified three-seed runs of9 CPU and4 A100 components are complete; see the parent directory's `frozen-sources.json`, `raw-cpu.json` and `raw-cuda.json`.

The old snapshot preserves the review trail only. It must not be retried automatically or used as final GPU evidence.
