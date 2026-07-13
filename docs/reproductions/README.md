# Paper reproductions

每篇论文拥有独立目录，方法说明、实验设置和已确认结果不会与其他论文混写。

| Track | Paper | Adapter | Results |
|---|---|---|---|
| LLM | SIS · arXiv 2607.04728 | `sis` | [结论](2607.04728-sis/README.md) |
| Recommendation | MDCNS · arXiv 2605.19651 | `mdcns` | [结论](2605.19651-mdcns/README.md) |

运行产生的原始结果位于：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── report.md
└── result.json
```

`runs/` 不进入 Git。经过复核、需要长期保留的结论，再写入对应论文目录的 `README.md`。
