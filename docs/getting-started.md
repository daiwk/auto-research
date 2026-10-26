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

## 学习卡片

顶部“学习卡片”栏目汇总精选主题卡和[全部论文小卡片](learning/all.md)。精选卡围绕一个问题比较多篇论文，可独立维护；单篇小卡片从统一论文 manifest 和对应正文生成，保留原论文证据、本地结果与适用边界。学习卡片直接在本站阅读，博客草稿不再作为交付流程。

新增论文后，同步 `docs/research-manifest.json` 和论文正文即可；文档构建会自动为它生成小卡片，无需另外维护卡片或追踪文件。也可以手动生成并检查，提前预览结果：

```bash
python scripts/generate_learning_cards.py
python scripts/generate_learning_cards.py --check
```

第一个命令更新 `docs/learning/all.md`，第二个检查生成内容与源文件一致，发现遗漏或过期卡片时返回失败。

本地 `mkdocs serve`、`mkdocs build` 和 CI 均会在构建前调用同一生成器，自动更新小卡片汇总。CI 使用最新来源生成后再严格构建，新论文会随下一次站点发布进入学习卡片栏目。
