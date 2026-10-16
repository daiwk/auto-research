# 首次 A100 组件执行失败记录

- 设备：真实 NVIDIA A100；本记录不是 passed GPU receipt。
- 执行源码 checkpoint：`a6ac6598`。
- 已观察错误：`RuntimeError: waypoint-opd has no actual policy gradient`（旧 runner 的 `run_seed` 非零梯度断言）。
- 该轮没有产生可接受的后训练六项通过证据；原始日志由批次执行方保留，不以本次修正覆盖。
- 首次错误未附 seed、step 或 gate 数值；因此不能仅凭该异常断言当时每个 gate 都为零。

## 原因分析与边界

旧 tiny-teacher 的 reward 只取决于首个 sampled byte 的 parity，却乘整条 continuation 的长度平均 logp。除了长度缩放，它还加入了 reward 无关 action 的 Monte Carlo 噪声。每次只有4个样本、共两次独立更新，使 early/late shifts 的方向一致性极弱；此前 CPU 的 gate 均值有0.005量级、学生参数变化有 $10^{-7}$ 量级。这解释了跨设备采样流下失去可测策略梯度的风险，不是声称原论文 Waypoint gate 有错。

修正预算预先固定：8个 teacher RL updates，每 update 64个真实单 action rollout，REINFORCE 与首 action reward 对齐，始终保存0/4/8快照，不根据 reward、gate 或 student gradient 择优、不 retry。原 Waypoint 组件公式、gate 阈值和 student 非零梯度门槛全部保留。新配置仍只是 byte-parity 机制诊断，不代表文本质量、数学能力或论文训练复现。
