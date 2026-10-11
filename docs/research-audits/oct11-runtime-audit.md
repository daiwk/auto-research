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
| PIVOT，授权同步后真实三臂 | 官方固定版本 0.5B 学生 / 7B 教师、共享 SFT→OPD warmup 后三臂各 8 步均真实更新；8 题验证三臂准确率全部为 0%，PIVOT 有混合 OPD/GRPO 路由 | 只证明训练和路由机制执行；不把参数位移或奖励异质性当作能力收益，负结果完整保留 |
| Memento3，真实冻结 7B | 初始观察接受 1 个生成模型；第一次真实动作即失配，修复失败，最终有效模型 0、任务未完成 | 记录 `falsified_generated_model`。GPU 通过只指安全解释/验证/失配链真实执行，明确 `capability_passed=false`；不添加手写导航 fallback |
| SGUID，首轮 4B probe | 8 步有真实梯度与参数更新，但技能支持信号全部非正，持久性筛选无可选技能；同时发现 Instruct-2507 的模板并不支持 thinking 切换 | 保留失败结果，不降低 h/阈值。旧运行不能充当 thinking 协议或两轮自蒸馏通过；需核验模板实际行为而非只记录请求参数 |
| Data-Space，公开依赖与缓存 | 首次缺少 SciPy；曾误把存在但为空的 CIFAR 目录当作缓存；官方远端下载很慢 | 补依赖到本轮临时目录；在用户授权后仅同步 5 份公开训练文件并逐份核对官方 MD5，未同步或读取 test |
| Data-Space，首次实际 backward | 从冻结 teacher deepcopy 的 student/fake 继承了 `requires_grad=False`，真实 backward 失败 | 拒绝生成通过证据。修正参数训练状态并新增实际训练→冻结→DMD backward 回归，再按冻结源码重新实跑；不能用单测代替 GPU 验证 |

成功运行的回执仅证明对应命令按限定协议执行，不证明论文所有实验、统计收益或 Evolve 已完成。整批任务状态见[完整范围](oct11-implementation-scope.md)。

## 新增数据角色与源码人工核验

- SGUID 的 gold 仅用于训练 rollout verifier、训练技能整理及外部验证评分；student、语义检索和评估生成不读 gold。模板现在核对实际渲染前缀，不能只凭 `enable_thinking` 参数被接受就宣称切换生效。
- V-CoLA 使用公开类别定义，不向模型提供图片正确类别；在真实 logits 生成后由外部 scorer 评分。4 张图片的受限字母结果不是完整生成准确率，也不参与压缩率择优。
- Data-Space 的训练/留出从官方训练集固定划分；teacher/fake/generator 的更新、冻结和参数摘要分别核验，不以 iteration 计数当作执行证据。
- Memento3 的运行模型只看公开 grid 与实际交互历史；生成 Python 由有界 AST 解释器处理，未调用 `exec/eval`，不输入隐藏环境转移或 gold plan。单测手写模型不进入运行时 fallback。

`fidelity-source-inventory.json` 是上述角色核验后的 AST 辅助清单，不是语义正确性或能力通过证书。实际 9B 四份权重的 SHA-256 已独立匹配 Hugging Face 固定官方 revision；执行源码摘要也与相应不可变提交和远端文件核对。
