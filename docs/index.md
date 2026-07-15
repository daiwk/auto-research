# Auto Research 论文复现库

这个站点汇总仓库内所有论文的背景、核心改动、架构图、公式、论文线上/离线结果和本地公开数据复现结论。

## 从这里开始

- [论文复现总览](reproductions/README.md)：查看全部 adapter、保真度和本地结论。
- [按公司浏览](reproductions/catalog/by-company.md)：Google、Meta、Pinterest、字节、阿里、腾讯、快手等。
- [按主题浏览](reproductions/catalog/by-topic.md)：LLM+推荐、生成式召回、排序、强化学习和 serving。
- [按月份浏览](reproductions/catalog/by-month.md)：按论文发布时间查找。
- [本地预览与发布](getting-started.md)：启动文档站或检查公式渲染。

## 阅读约定

每篇文档明确区分三类数字：原论文离线指标、原论文线上 A/B、本地公开数据实验。论文的线上提升不会被写成本地复现提升；本地负结果也会完整保留。

公式统一使用 `$...$` 和 `$$...$$`，由 MathJax 渲染；架构图使用 Mermaid。较宽的公式、表格和图在移动端可以横向滚动。
