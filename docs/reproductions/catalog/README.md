# 论文目录

同一批 adapter 提供三种阅读入口，避免按单一维度反复移动代码和打断复现命令：

- [按公司](by-company.md)：适合追踪各工业团队的技术路线；
- [按主题](by-topic.md)：适合横向比较生成式推荐、LLM 适配、排序和 serving；
- [按时间](by-month.md)：适合查看技术演进和后续增量更新。

物理代码目录保持 `src/auto_research/reproductions/<adapter>/`，物理论文档保持 `<arxiv-id>-<adapter>/`；公司、月份、主题和量化线上 A/B 证据写入 `PaperMetadata`。自动选入的新工业论文必须 `paper.has_online_ab == true`；无线上 A/B 的经典论文只有用户明确点名时才能作为具名例外。
