# 论文目录

同一批 adapter 提供三种阅读入口，避免按单一维度反复移动代码和打断复现命令：

- [按公司](by-company.md)：适合追踪各工业团队的技术路线；
- [按主题](by-topic.md)：适合横向比较生成式推荐、LLM 适配、排序和 serving；
- [按时间](by-month.md)：适合查看技术演进和后续增量更新。

物理代码目录保持 `src/auto_research/reproductions/<adapter>/`，物理论文档保持 `<arxiv-id>-<adapter>/`；分类入口不改变物理路径。新增工业论文需在 `PaperMetadata` 写入公司、月份、主题和量化线上 A/B 证据，且必须 `paper.has_online_ab == true`；无线上 A/B 的经典论文只有用户明确点名时才能作为具名例外。

## 更新契约

新增 adapter 必须在同一个 PR 中完成以下更新：

1. 根 `README.md` 的能力表；
2. `docs/reproductions/README.md` 的完整审计表；
3. 本目录的公司、月份、主题三个入口；
4. 独立论文 README，顶部统一列出论文链接、公司/机构、arXiv v1 日期、原作者是否开源、Adapter 和本地代码位置，并包含原始论文总结、Mermaid 架构、核心公式、论文离线与线上效果、本地复现和边界；
5. `metrics/*.json` 稳定指标。概念验证也必须写入，但要设置 `diagnostic_only: true`。

新增或核实元数据后运行 `PYTHONPATH=src python scripts/sync_reproduction_metadata.py` 同步所有单篇 README。`tests/reproductions/test_documentation_catalog.py` 会把代码 registry 与上述文档逐项比对；漏任一入口、论文信息字段、断链、缺章节或缺 metrics 都会使测试失败。
