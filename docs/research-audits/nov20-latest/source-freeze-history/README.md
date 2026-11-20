# 冻结前交叉审查记录

[English](../../../en/research-audits/nov20-latest/source-freeze-history/README.md)

`71aca03f-unexecuted.json` 绑定提交 `71aca03fe0e77cd9a3f2dcad24dde77f76eb9d74`。这是实际产生的早期源码冻结快照；**尚未用于统一CPU或CUDA实跑**，不是失败GPU实验，也不是最终验收版本。

随后独立代码审查发现 VisAlloc 的半精度统计合同不完整：fp16/bfloat16输入可能在quantile报错，有限极端fp16 logits可能在JSD路径产生NaN。固定上游在统计前提升到float32。HiSA也发现无符号整数位置相减回绕，可能把未来键当作过去键；修复为先检查uint64范围、再使用非负int64位置。两项均先修复并补入实际诊断负控，再创建新提交和新的冻结证明。已有独立CPU记录保留原始源码hash，不冒充修复后的运行。

最终执行版本是 `15c4e1d105fe68c7556734ad50ad6022061dd11a`，统一9个CPU/4个A100组件的三种子运行已完成，见父目录的 `frozen-sources.json` 与 `raw-cpu.json` / `raw-cuda.json`。

旧快照只为保留审查轨迹，不应被自动重跑或作为最终GPU验收依据。
