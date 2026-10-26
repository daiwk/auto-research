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

顶部“学习卡片”栏目按“主题 → 子主题 → 论文卡片”组织。侧栏的主题默认折叠，进入当前子主题时自动展开；汇总页只展示主题入口，单篇论文放在子主题页，默认每次显示 12 张。可以在[全部论文小卡片](learning/all.md)跨主题搜索，按主题和子主题联动筛选；筛选条件保存在网址中，方便收藏。

每个子主题都有人工整理的导学卡：核心问题、机制、具体例子、适用边界、代表论文阅读顺序，以及可展开答案的自测题。精选慢读保留跨论文对比。单篇小卡片从统一 manifest 与正文摘录，论文结论和本地验证边界分别展示，成本过高而未复现的状态在折叠前也可见。

新增论文时，同步 `docs/research-manifest.json`、论文正文和 `docs/learning/topics/*.json` 中的归属。每条记录只分配一个主子主题，代表阅读顺序可以跨文档解释关联。未分配的新论文会自动进入[待归类](learning/inbox.md)，同时保留在全部搜索中；这用于暴露遗漏，不会自动猜测主题。实现新论文时，还要交付一张人工整理的学习卡（核心认识、例子、边界、自测），并补入相应主题的阅读入口，不能只以自动摘录代替。

也可以手动生成并检查：

```bash
python scripts/generate_learning_cards.py
python scripts/generate_learning_cards.py --check
```

第一个命令更新 `docs/learning/all.md`、主题与子主题页面、待归类页，以及汇总页中标记的主题区；精选正文和其他人工段落保持原样。第二个检查上述输出一致性，发现重复归属、无效代表论文、缺失导学内容或过期页面时返回失败。修改导学内容和论文归属请编辑 JSON 来源，不直接修改生成页面。

本地 `mkdocs serve`、`mkdocs build` 和 CI 均调用同一生成器。MkDocs hook 从同一主题来源生成折叠导航，不在侧栏枚举所有论文；新增子主题也无需手写第二份导航树。CI 使用最新来源生成后再严格构建，新论文会随下一次站点发布进入学习卡片栏目。学习卡片直接在本站阅读，博客草稿不再作为交付流程。
