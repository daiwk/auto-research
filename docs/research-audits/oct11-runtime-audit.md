# 10 月 11 日运行失败与证据修正

本页保留不成功或资格不足的运行，不将其伪装成通过的 GPU 回执。

| 方法 | 观察 | 处理及结论边界 |
|---|---|---|
| VFold，4 个校准问题 | BF16 logits 相对误差 0.0211506，超过运行器固定 0.02 门槛 | 拒绝。改用 32 个训练问题校准，误差降为 0.0172934；并非精确数值保持 |
| VFold，旧 Cache 接口 | `lazy_initialization` 的参数个数与本地版本不同，解码失败 | 按绑定接口签名适配；新旧接口都有真实小 Qwen 回归，A100 后续完整解码通过 |
| OPD 表征诊断 | 远端 `hidden_states` 是最终 Tensor，不是逐层 tuple；旧代码误遍历 batch 维后 shape 失败 | 不 reshape 掩盖问题。显式 hook embedding/中间层/final norm，实际采集 37 个位置；A100 完成 |
| ZCPO，最早 8 步 | 同奖励组全部跳过，未更新参数；旧执行把官方 test 传到名为 validation 的参数，旧报告仍写 `test_read=false` | 旧声明错误，撤销资格；不是训练成功或独立验证。后续使用官方 train 派生 holdout；保留首次无有效组事实 |
| ZCPO，24 步旧报告 | 9 个有效组、非零参数更新；执行发生在 split-manifest 校验加入之前 | 不改写旧运行成新源码。按当前可追溯提交和 manifest 重跑，旧值只作诊断记录 |
| ReCal，旧四题对照 | ReCal 在 SFT 后 1.0、OPD 后 0.75；对照 OPD 后 1.0 | 明确保留负结果，不能声称方法提高能力。旧报告同样需补执行前 split-manifest 校验，另行重跑 |
| ReCal / ZCPO，当前源码重跑 | 执行前核验 train-only holdout manifest；ReCal 负结果、ZCPO 9 个有效组及 0.625 验证 EM 均与前次一致 | 新回执绑定实际执行提交；旧报告不覆盖或改写 |
| Option-Channel，早期证据等级 | 原生合成安全探针误写 `diagnostic_only=false` | 修正为 L1 机制诊断并在 A100 重跑；ASR 与无分母结果不变，不升级为 Agent 能力或生产安全证据 |
| SparseDecoding，首次 Triton 编译 | JIT 局部作用域未正确绑定 `tl`，A100 编译失败 | 移到惰性导入的独立 Triton 模块；四种 N:M 实际 kernel 的数值回归通过 |
| SparseDecoding，128-token 首轮 | 稠密和两种稀疏配方共 12 个验证回答均截断、数值评分均为 0 | 不作质量结论。补 EOS/截断标记、去掉预算末尾无用 forward、用训练输入预热，并固定源码后扩大为 512 token |
| SparseDecoding，512-token 对照 | 稠密 4/4 正常结束且匹配；固定文本稀疏匹配 2/4、解码校准稀疏 1/4，两者均截断 3/4；稀疏吞吐更慢 | 保留负结果与截断；只证明 decoding-only 校准、真实 bitmask kernel 路径执行，不声称论文精度收益、加速或 Evolve 能力提升 |
| PIVOT，公开依赖下载 | A100 的 Hugging Face 请求连接超时；改用已有同词表 4B checkpoint 的尝试也在官方 Banking77 下载阶段连接重置 | 尚未执行三配方 GPU 训练，不能生成通过回执。源码/数据隔离/路由测试不替代 GPU 验证；公开数据或权重同步需遵守单独授权范围 |

成功运行的回执仅证明对应命令按限定协议执行，不证明论文所有实验、统计收益或 Evolve 已完成。整批任务状态见[完整范围](oct11-implementation-scope.md)。
