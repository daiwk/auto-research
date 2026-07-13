# Architecture and extension guide

## Stable core

```text
CLI
 └── reproductions.registry
      └── one adapter per paper
           ├── algorithm.py / model.py
           ├── experiment.py
           ├── report.py
           └── adapter.py
```

通用层只负责 adapter 发现、数据缓存、运行目录和 JSON/Markdown 持久化。论文特有逻辑不能写回 `cli.py`、`reporting.py` 或兼容文件 `paper_methods.py`。

## Add a paper

1. 创建 `src/auto_research/reproductions/<key>/`。
2. 将论文公式或网络放在 `algorithm.py`/`model.py`，数据切分和对照实验放在 `experiment.py`。
3. 在 `report.py` 中渲染该论文真正需要的指标。
4. 在 `adapter.py` 构造并 `register(ReproductionAdapter(...))`；registry 会自动发现它。
5. 在 `tests/reproductions/<key>/` 增加算法单测、最小端到端测试。
6. 在 `docs/reproductions/<arxiv-id>-<key>/README.md` 记录经复核的长期结论。

新论文不需要修改 CLI 分支、公共报告渲染器或其他论文目录。

## Artifact contract

每次运行写入不可变目录：

```text
runs/reproductions/<arxiv-id>-<key>/<timestamp>/report.md
runs/reproductions/<arxiv-id>-<key>/<timestamp>/result.json
```

`result.json` 是机器可读事实来源，`report.md` 由论文自己的 renderer 生成。不要把临时运行结果提交 Git；只将复核后的结论摘录到对应论文文档。
