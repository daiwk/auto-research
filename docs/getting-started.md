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

顶部“学习卡片”栏目以逐篇论文问答为主体，按“主题 → 子主题 → 具体问题”组织。每篇至少覆盖基础理解、核心机制、方法对比、实现细节四层，各至少一问；也可以持续追加。先读问题，再展开答案与教学例子。子主题问题库、[全部论文问答](learning/all.md)和[最近新增问题](learning/recent.md)使用同一份问答来源，新增内容同时进入三个入口。专题串读保留跨论文讲解，单独维护。

侧栏主题默认折叠，进入当前子主题时展开。问题按每批 12 个展示，可组合主题、子主题、学习层次与关键词筛选；筛选条件保存在网址中。点击论文标题可集中查看这一篇的所有问答，默认按四层顺序排列。问题深链会解除冲突筛选并展开答案。原来的主题导读和阅读路线保留为可选展开区。实验验证和未复现边界从“实现解读”进入查阅。

新增论文时，同步统一 manifest、论文正文、`docs/learning/topics/*.json` 的归属，以及 `docs/learning/questions/*.json` 的逐篇问答。问题必须针对定义性机制，答案直接解释，附具体教学例子；不能用通用“解决什么问题”加摘要摘录充数。`source_sections` 引用本篇 README 的实际标题，问题 `id` 保持稳定，`added` 使用真实加入日期。补充旧论文的新问题会进入最近新增；修改原有答案不自动改写加入日期。未分主题的记录保留在[待归类](learning/inbox.md)，发布检查仍要求每篇都有问答。

问答 JSON 中每题必须有 `level`，取值为 `basics`、`mechanism`、`comparison`、`implementation`。下面仅展示一题的字段；实际每篇四层必须齐全，再按需要追加同层问题：

```json
{"schema_version": 1, "papers": {"recommendation:example": {"questions": [{
  "id": "mechanism", "level": "mechanism", "question": "选中块的索引不可导，连续gate为什么还能被训练？",
  "answer": "解释梯度经过的连续路径，以及离散选择仍然存在的限制。",
  "example": "给出帮助理解的教学场景，不冒充论文实验。",
  "source_sections": ["背景与主要改动", "核心公式"], "added": "2026-10-27"
}]}}}
```

也可以手动生成并检查：

```bash
python scripts/generate_learning_cards.py --require-questions
python scripts/generate_learning_cards.py --check --require-questions
```

第一个命令更新全部问答、最近新增、子主题问题库和汇总页标记区域；第二个验证生成一致性。缺少任一学习层次、非法层次、重复问题ID、无效来源标题、空答案或例子、重复论文归属都会导致失败。编辑问答和主题的 JSON 来源，不直接修改生成页面。对比题需说明真实机制/假设差异；没有测量时不编造性能排名。实现题明确原方法的关键条件与本地证据范围。生成器不会自动拼接通用问题来通过检查。

本地 MkDocs 与 CI 使用同一生成器，并强制完整问答覆盖。折叠导航来自主题 JSON，单篇问题不挤入侧栏。学习内容直接在本站阅读，博客草稿不再作为交付流程。
