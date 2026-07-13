# Paper reproductions

每篇论文拥有独立目录，方法说明、实验设置和已确认结果不会与其他论文混写。

2026 年至今的 Google/Meta + 线上 A/B 严格筛选过程见 [selection report](2026-google-meta-online-ab-selection.md)。

| Track | Paper | Adapter | Results |
|---|---|---|---|
| LLM | SIS · arXiv 2607.04728 | `sis` | [结论](2607.04728-sis/README.md) |
| Recommendation | MDCNS · arXiv 2605.19651 | `mdcns` | [结论](2605.19651-mdcns/README.md) |
| Recommendation | CMSL · arXiv 2606.28533 | `cmsl` | [结论](2606.28533-cmsl/README.md) |
| Recommendation | G2Rec · arXiv 2606.20554 | `g2rec` | [结论](2606.20554-g2rec/README.md) |
| Recommendation | Cluster GOOBS · arXiv 2607.00448 | `cluster-goobs` | [结论](2607.00448-cluster-goobs/README.md) |
| Recommendation | LLaTTE · arXiv 2601.20083 | `llatte` | [结论](2601.20083-llatte/README.md) |
| Recommendation | Self-Evolving RecSys · arXiv 2602.10226 | `self-evolving-rec` | [结论](2602.10226-self-evolving-rec/README.md) |
| Recommendation | Memento · arXiv 2605.24051 | `memento` | [结论](2605.24051-memento/README.md) |

运行产生的原始结果位于：

```text
runs/reproductions/<arxiv-id>-<adapter>/<timestamp>/
├── report.md
└── result.json
```

`runs/` 不进入 Git。经过复核、需要长期保留的结论，再写入对应论文目录的 `README.md`。
