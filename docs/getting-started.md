# 本地预览与发布

## 启动文档站

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
.venv-docs/bin/mkdocs serve
```

打开 `http://127.0.0.1:8000` 即可预览。修改 Markdown 后页面会自动刷新。

## 严格构建

```bash
.venv-docs/bin/mkdocs build --strict
```

严格模式会把缺失页面、配置错误和不兼容扩展当作构建失败。公式分隔符与花括号还由测试单独检查：

```bash
PYTHONPATH=src .venv/bin/pytest -q tests/test_docs_math.py
```

## GitHub Pages

合入 `main` 后，GitHub Actions 自动构建并发布到 `https://daiwk.github.io/auto-research/`。Pull Request 只运行严格构建，不发布站点。仓库首次使用 Pages 时，需要在 GitHub 的 **Settings → Pages → Build and deployment** 中选择 **GitHub Actions**。

## 新增论文文档

继续把论文放在 `docs/reproductions/<arxiv-id>-<adapter>/README.md`。只要 Markdown 通过严格构建和公式测试，页面会自动进入站点；不需要维护另一份正文。
