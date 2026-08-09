# Archived migration scripts

这里保存已经完成使命、仅用于追溯历史批次的日期型脚本。它们不是当前维护入口，也不在
CI 中执行。新增论文和目录更新请使用：

```bash
auto-research-maintain manifest
auto-research-maintain catalogs
auto-research-maintain audit
auto-research-maintain sync-readme
```

不要再新增 `generate_YYYYMMDD_*` 或 `run_YYYYMMDD_*`；可重复的能力应进入 CLI、adapter
或通用生成器。
