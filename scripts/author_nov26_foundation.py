"""Author only the three accepted Nov26 foundation papers and review bundles.

No shared catalog, registry, learning bank or formal experiment metrics are edited.
Figures are unmodified fixed-v1 PDF page rasters reviewed by the authoring agent.
"""
from hashlib import sha256
import json
from pathlib import Path

from english_learning_sources import question_units

ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / 'docs/research-audits/nov26-latest'
CACHE = ROOT / '.cache/nov26-latest/foundation-primary'
DATE = '2026-11-26'
SECTIONS = ['背景与主要改动','核心公式','同主题比较与边界','数据协议与代码映射','高成本完整实验']

CONTENT = {
 'rap': {
  'id':'2611.34298','title':'RAP: Radial-Angular Random Projection for Hyperbolic Representations',
  'author':'Jiahong Liu','affiliation':'The Chinese University of Hong Kong',
  'institutions':'The Chinese University of Hong Kong；Yale University；The Hong Kong University of Science and Technology (Guangzhou)',
  'published':'2026-11-25T12:50:23Z','code':'https://github.com/HUBERILT/RAP',
  'code_status':'作者固定 v1 直接链接公开 Python 仓库，GitHub API 已确认 public；git ls-remote 核验 HEAD。未声明许可证，按论文公式独立实现，未复制源码。',
  'revision':'91afe946876ead00008465c6c75dcd0f94f5b5ff','page':4,'figure':'Figure 1',
  'figure_caption':'Three hyperbolic random projection paradigms, including RAP radial-angular separation.',
  'sections':['3','4.1–4.4','5','Appendix A–E','Appendix F.7–F.8'],
  'peer':'hvmap','peer_path':'foundation-models/2611.01514-hvmap/README.md','card':'foundation-models/context-and-state',
  'position':'RAP在同一双曲空间中压缩维度，保持每点到指定原点的半径，只随机投影并归一化角方向；不拟合数据。',
  'tradeoff':'HVMap学习异构编码器空间的配对映射并联合原生/映射分数；RAP不对齐不同编码器，也不能把不同曲率或原点的向量直接混用。二者解决的不是同一检索瓶颈，现有L1不支持语义检索收益比较。',
  'en_position':'RAP reduces dimension within a hyperbolic geometry, preserving distance to a designated origin and projecting only the normalized angular direction without fitting data.',
  'en_tradeoff':'HVMap learns paired mappings between heterogeneous encoder spaces and combines native/mapped scores. RAP does not align encoders or permit mixing arbitrary curvatures or origins. Their L1 components do not establish comparative semantic retrieval gains.',
  'mechanism':'普通空间坐标投影会同时改变径向深度与角相似度。RAP拆开这两者：到所选原点的半径不变，角向量乘一次高斯矩阵后归一化，再提升回目标 Lorentz 双曲面。它不是对原始坐标做普通欧氏 JL；保证仍受半径上界、点间分离和 arcosh 条件数限制。',
  'en_mechanism':'A spatial-coordinate sketch perturbs both radial depth and angular similarity. RAP separates them: keep radius, apply a Gaussian sketch to the unit direction, normalize, and lift to the target Lorentz hyperboloid. This is not ordinary Euclidean JL on the input coordinates. The finite-set guarantee still depends on bounded radii, pairwise separation and arcosh conditioning.',
  'formula':r'''For $P_{ij}\sim\mathcal N(0,1/k)$, $r_x=d_c(o,x)$ and $u_x\in S^{d-1}$:

$$
\widetilde u_x=\frac{Pu_x}{\|Pu_x\|_2},\qquad
\Pi_{RAP}(x)=\frac1{\sqrt c}\left(\cosh(\sqrt c\,r_x),\sinh(\sqrt c\,r_x)\widetilde u_x\right).
$$

$$
\cosh(\sqrt c\,d_c(x,y))=\cosh(\sqrt c\,r_x)\cosh(\sqrt c\,r_y)-\sinh(\sqrt c\,r_x)\sinh(\sqrt c\,r_y)\langle u_x,u_y\rangle.
$$''',
  'formula_note':'对应 Eq11–12。非原点方向若落入投影核则不可归一化，必须拒绝；原点映射为目标原点。同射线距离精确保留；任意角度的距离并非无损。',
  'en_formula_note':'These are Eq.11–12. Reject a non-origin direction in the projection kernel; map the origin to the target origin. Same-ray distances are exact, but arbitrary pairwise distances are not lossless.',
  'results':'作者 Table1 的 broad-radius、n=512、k=32：平均相对距离失真 RAP 0.040，fully-hyperbolic 与 half-space 均约 0.077。Appendix F.7 的冻结视觉语言特征检索在 k=64 为18.31，对照15.24，未压缩31.44；所以相对压缩对照改善不等于超越未压缩表示。生产线上 A/B：未报告。',
  'en_results':'In Table1, broad-radius n=512/k=32 gives mean relative distance distortion 0.040 for RAP versus about 0.077 for fully-hyperbolic and half-space projections. Appendix F.7 reports frozen-feature retrieval at k=64:18.31 versus15.24 for the strongest compressed comparator, below the uncompressed31.44. Improvement over compression baselines is not improvement over the original representation. No production A/B is reported.',
  'local':'`polar_to_lorentz`、`lorentz_to_polar`、`project_rap`、`pairwise_distance`真实执行极坐标分解、Eq11–12及双曲距离；另有原点 tangent 与 spatial 两对照。128个32维随机点压到8维，固定种子共享源点与投影矩阵，仅作机制诊断，和作者每方法独立随机投影协议不同。无WordNet、冻结视觉语言特征或百万点压力测试。',
  'en_local':'The component implements polar conversion, Eq.11–12, hyperbolic distances, and canonical-origin tangent/spatial comparators. It compresses128 synthetic32-dimensional points to8 dimensions. Source points and the projection matrix are paired locally, unlike the paper\'s independent per-method projection matrices. No WordNet, frozen vision-language features or million-point stress test is run.',
  'checks':'检查半径、目标双曲面、同射线距离和原点不变；负控拒绝非单位方向、非双曲面、非有限数、非法曲率和非原点投影核。失真是描述性标量，不把某个seed的优劣断言为能力收益。正式冻结三seed指标由统一runner另行验收，本文不引用早期preflight冒充正式结果。',
  'en_checks':'Checks cover radii, the target hyperboloid, same-ray distance and origin preservation. Invalid directions, manifolds, finite values, curvature or non-origin projection kernels fail. Distortion is descriptive, not a capability claim. The integration owner separately collects frozen three-seed evidence; early preflight is not formal paper metrics.',
  'cost':'核心合成/WordNet投影可负担，Appendix E明确为CPU无拟合任务。百万4096维点压力测试作者单A40约11秒、峰值15.8GiB，不能据此认定高成本。完整矩阵另含五种冻结视觉语言backbone、75个backbone–dataset cells和3375次压缩评测，未报告特征文件体积、公开获取路径或总体时长；作者仓库只提供NumPy核心和256点demo。没有充分依据把全论文定为高成本。本轮授权范围止于小型CPU L1，不额外获取这些资源或执行完整矩阵；不把未承接写成硬件不可行。',
  'en_cost':'Core synthetic/WordNet projection is affordable and Appendix E explicitly describes CPU workloads without fitting. The million4096-dimensional-point stress test takes about11seconds and15.8GiB on one A40 in the paper; that is not evidence of prohibitive cost. The complete matrix also includes five frozen vision-language backbones,75 backbone–dataset cells and3375 compressed evaluations,but feature-file sizes,release paths and total runtime are not reported. The author repository exposes only the NumPy core and a256-point demo. There is insufficient evidence to label the whole paper high-cost. The accepted scope ends at bounded CPU L1; not undertaking the complete matrix is not a hardware-infeasibility claim.',
  'qa':[
   ('radius-not-all-distances','basics','保持半径是否表示所有距离都不变？','不是。半径只固定每点到选定原点的距离，角向随机投影仍改变不同射线间距离。','教学例：两个半径同为1的点可夹角90度；投影后夹角变为60度时，两半径不变而点间距离改变。','Does preserving radius preserve every distance?','No. It fixes distance to the selected origin, while angular projection can change distances between rays.','Illustration:two radius-one points can change angle from90 to60degrees with unchanged radii but changed mutual distance.'),
   ('normalize-before-lift','mechanism','为何不能直接把Pu作为目标空间坐标？','Pu一般不是单位方向；必须先除以其范数，再按原半径用cosh/sinh提升，否则径向深度漂移。','教学例：Pu长度为2时直接代入空间分量会偏离原半径；除以2恢复角方向，非原点且Pu=0必须报错。','Why not use Pu directly as target spatial coordinates?','Pu need not be unit length. Normalize it, then lift with the original radius using cosh/sinh; otherwise radial depth drifts.','Illustration:a sketch of norm2 must be divided by2 before lifting; a zero sketch of a non-origin point must fail.'),
   ('not-cross-encoder-alignment','comparison','RAP能替代HVMap把不同编码器的向量库对齐吗？','不能。RAP压缩同一已定义双曲空间；HVMap从配对表示学习异构空间映射。保持原点半径不提供跨编码器语义对应。','教学例：编码器A与B把同一物体置于不同方向，即使两边半径都保持，角向量也不会自动对齐。','Can RAP replace HVMap for cross-encoder alignment?','No. RAP compresses one defined hyperbolic space; HVMap learns paired mappings between heterogeneous spaces. Radial preservation provides no semantic correspondence.','Illustration:if two encoders place an object in different directions, preserving their radii does not align those directions.'),
   ('diagnostic-not-retrieval','implementation','怎样检验实现没有偷换成欧氏距离压缩？','同时检查输出在目标双曲面、每点半径不变及同射线距离；用双曲距离而非输出坐标欧氏距离计失真。','教学例：把r和Pu直接拼接可能通过shape测试，却无法通过Lorentz约束；本地负控会拒绝非法输入。','How do we exclude a Euclidean-compression substitution?','Check the target hyperboloid, per-point radii and same-ray distances, and measure distortion with hyperbolic rather than ambient Euclidean distances.','Illustration:concatenating r and Pu can pass shape checks but fails the Lorentz constraint.')],
 },
 'duomi': {
  'id':'2611.33952','title':'DuoMI: Dual Mutual Information Regularization for Expert Reuse in Looped Transformers',
  'author':'Xinlai Kang','affiliation':'Huawei Foundation Model Lab','institutions':'Huawei Foundation Model Lab',
  'published':'2026-11-25T08:13:44Z','code':None,'revision':None,
  'code_status':'固定 v1 全文、PDF链接与摘要未找到作者专用公开源码；本轮有界标题/作者搜索也未找到，未找到/尚未发布，不将MindSpeed-LLM依赖当成DuoMI代码。',
  'page':5,'figure':'Figure 2','figure_caption':'Two rounds share expert FFNs while attention, routers and normalization remain independent.',
  'sections':['3.1–3.4','Algorithm 1','4','Appendix A','Appendix B.1–B.2'],
  'peer':'echomoe','peer_path':'foundation-models/2611.22215-echomoe/README.md','card':'foundation-models/compression-and-cache',
  'position':'DuoMI按相同token在两轮的全部expert软路由计算两种互信息：聚合使用对齐与逐token变化区间，训练时约束共享expert池的实际复用。',
  'tradeoff':'EchoMoE复用跨层激活参考并压缩通信变化量；DuoMI共享expert参数并约束路由。前者的reference不是后者的expert池，减少通信和改变专家复用不是可交换收益；小张量反传不代表语言模型提升。',
  'en_position':'DuoMI regulates realized expert reuse using aggregate alignment and a token-level change band computed from all-expert soft routing at aligned positions in two rounds.',
  'en_tradeoff':'EchoMoE reuses activation references and compresses communication deltas; DuoMI shares expert parameters and regularizes routing. A reference is not an expert pool. Communication reduction and routing reuse are different benefits, and tensor gradients establish no language-model gain.',
  'mechanism':'两次调用共享expert FFN，但attention、router与normalization独立。仅看总体expert使用分布会漏掉每个token全部换expert的情况；仅看逐token变化又可能允许两轮偏好不同子池。DuoMI分别限制聚合round–expert依赖和token条件下的round–expert依赖，训练使用全部expert的softmax而非无梯度的硬Top-k集合。',
  'en_mechanism':'The two invocations share expert FFNs but have independent attention, routers and normalization. Aggregate usage can agree while every token replaces its experts. Token-level change alone can still permit round-specific subpools. DuoMI separately controls aggregate and conditional round–expert dependence using differentiable all-expert softmax distributions, not hard Top-k membership.',
  'formula':r'''For aligned valid positions, $p_{i,r}=\operatorname{softmax}(z_{i,r}/\tau)$ and base-two JSD:

$$
G_{b,j}=\operatorname{JSD}_2(\overline p_1,\overline p_2),\qquad
D_{b,j}=\frac1{N_b}\sum_i\operatorname{JSD}_2(p_{i,1},p_{i,2}),\quad 0\le G\le D\le1.
$$

$$
\Phi_{b,j}=\lambda_G[G_{b,j}-g_{max}]_+^2+\lambda_L[d_{min}-D_{b,j}]_+^2+\lambda_U[D_{b,j}-d_{max}]_+^2.
$$

$$
L=L_{base}+\frac{w_t}{BM}\sum_b\sum_j\Phi_{b,j}.
$$''',
  'formula_note':'每组8条序列；先逐group、逐pool计算阈值罚项，再平均。默认tau=1、g_max=.02 bits、D区间[.05,.30] bits、三个权重均.1。D是平均JSD，soft D不是Top-k替换比例；只有均匀硬Top-k分布才有D=1−retention。基础语言、负载均衡与z-loss保持原配置。',
  'en_formula_note':'Each group has eight sequences. Apply thresholds per group and pool before averaging. Defaults:tau=1,g_max=.02bits,D-band[.05,.30]bits,and weights.1. Soft D is not the Top-k replacement fraction; D=1-retention holds only for uniform hard Top-k distributions. The language, load-balancing and z-loss objectives retain their baseline coefficients.',
  'results':'作者Table1在同一looped OLMoE骨干15项下游任务的平均分由50.08升至51.82（+1.74个百分点）；9项改善、部分任务下降。未共享expert的OLMoE参考为51.15。结论只覆盖该骨干，不等于所有loop/MoE结构都获益。生产线上 A/B：未报告。',
  'en_results':'Table1 reports a15-task average rising from50.08 to51.82(+1.74percentage points) on one looped OLMoE backbone; nine tasks improve and some regress. The unshared OLMoE reference is51.15. This is not evidence that every looped/MoE architecture benefits. No production A/B is reported.',
  'local':'`PairedSharedExperts`确实用两个独立router/LayerNorm读取连续状态，两轮调用同一GELU FFN expert池，稀疏Top-k派发和原加权不受正则改变。`duomi_penalty`读取派发前logits，valid token对齐，按8序列分组并真实反传。仅FFN耦合组件，无attention/因果语言模型、全局负载均衡、expert parallel或MindSpeed集成，不能称完整looped Transformer。',
  'en_local':'PairedSharedExperts uses distinct routers/LayerNorms on successive states and invokes the same GELU FFN expert pool twice. Sparse Top-k dispatch and its weighting are unchanged by regularization. The penalty uses aligned pre-dispatch logits and eight-sequence groups with real backpropagation. This is only a coupled FFN component: no attention, causal LM, global balancing, expert parallelism or MindSpeed integration.',
  'checks':'本地默认诊断为激活下界梯度而显式使用D区间[.5,.8]，不是调参求能力收益；库默认保留论文[.05,.30]。检查两router与共享expert非零梯度、实际更新、G≤D和派发不变；负控验证总体分布相同但逐token完全互换、group平均后阈值错误及padding排除。统一runner负责正式冻结结果，早期preflight不写成paper metrics。',
  'en_checks':'The diagnostic explicitly uses a[.5,.8]D-band to activate lower-bound gradients, not to tune capability; library defaults retain[.05,.30]. Checks cover gradients into both routers/shared experts, updates,G<=D and unchanged dispatch. Negative controls cover aggregate cancellation with token swapping, threshold-before-group-averaging and excluded padding. Formal frozen evidence belongs to the common runner, not early preflight.',
  'cost':'Appendix B给出4.5B独立可训练参数、1.3B active/token、16层64 experts/Top8、FineWeb-Edu sample-100BT，50000步×512序列×4096=104857600000 token positions；多对照/阈值重训。该完整训练矩阵明显超单A100/A30或Mac有界预算；成本来自配置估计，论文未给本地可用的完整时长，不编造GPU小时。',
  'en_cost':'Appendix B specifies4.5B unique trainable parameters,1.3B active/token,16layers,64experts/Top8,and FineWeb-Edu sample-100BT:50000updates x512sequences x4096=104857600000token positions, plus comparator/threshold retraining. The complete matrix exceeds a bounded single-A100/A30-or-Mac budget. This is configuration-based, not an invented GPU-hour measurement.',
  'qa':[
   ('aggregate-not-token-agreement','basics','两轮总体expert使用相同，是否每个token都复用expert？','不一定。不同token的变化可互相抵消，使聚合G=0但逐token D>0。','教学例：第一轮x选A、y选B，第二轮交换；两轮总体各一半A/B，但每个token都换了expert。','Does identical aggregate usage mean per-token reuse?','No. Token changes can cancel, yielding G=0 with D>0.','Illustration:x choosesA and y choosesB, then they swap; aggregate usage stays halfA/halfB while both tokens change.'),
   ('group-before-hinge','mechanism','为何不能先跨所有group平均G/D再计算阈值罚项？','平方hinge非线性；一组越界不能被另一组抵消。必须每组每pool先计算Phi再平均。','教学例：两组分别偏好相反子池，池化后G为0，但两组自身G都大，正确实现仍有罚项。','Why not average G/D globally before thresholding?','Squared hinges are nonlinear. One group\'s violation must not be canceled by another; compute Phi per group/pool first.','Illustration:opposite subgroup preferences cancel after pooling while each group still violates the marginal bound.'),
   ('reuse-not-communication','comparison','DuoMI和EchoMoE里的跨层复用是同一种东西吗？','不是。DuoMI约束共享FFN池的router选择；EchoMoE复用激活reference并压缩差值通信。','教学例：同一个expert可被两轮选择，但两轮激活差值仍很大；专家复用率不能替代通信字节测量。','Is cross-layer reuse the same in DuoMI and EchoMoE?','No. DuoMI regulates shared-FFN routing; EchoMoE reuses activation references and compresses communication deltas.','Illustration:the same expert may process very different activations in two rounds, so expert retention cannot substitute for communication bytes.'),
   ('real-coupled-gradients','implementation','只给任意两组logits算JSD算完成DuoMI L1吗？','不够。本地需实际两router依次读取状态并调用同一expert池，证明组化正则能反传到两router且不改变硬派发。','教学例：独立优化两个logits数组无法证明共享FFN的耦合；本地检查第二轮loss通过第一轮状态回到共享参数。','Are arbitrary paired-logit JSD arrays sufficient for this L1?','No. Run successive routers with a real shared expert pool, backpropagate the grouped penalty to both routers, and verify unchanged hard dispatch.','Illustration:optimizing two isolated arrays cannot establish shared-FFN coupling; the second round must depend on the first round\'s state.')],
 },
 'jepa-eu': {
  'id':'2611.34830','title':'Not all world models can doubt: how training objective and architecture shape epistemic uncertainty in JEPA and RSSM world models',
  'author':'Simon Baur','affiliation':'Fraunhofer Heinrich-Hertz-Institut','institutions':'Fraunhofer Heinrich-Hertz-Institut, Berlin, Germany',
  'published':'2026-11-25T18:11:49Z','code':None,'revision':None,
  'code_status':'固定 v1 PDF/HTML/摘要未找到专属作者实现链接；有界精确标题/作者入口搜索未找到可核实公开源码，未找到/尚未发布。引用的LeWorldModel与Dreamer代码不等于本文实验实现。',
  'page':5,'figure':'Figure 4','figure_caption':'Persistence and entity pixel/gradient share influence uncertainty sensitivity.',
  'sections':['3–6','Appendix A','Appendix B','Appendix C','Tables 1–11','Figure 14'],
  'peer':'jepa-prediction-planning','peer_path':'foundation-models/2610.19375-jepa-prediction-planning/README.md','card':'multimodal-models/world-state-actions',
  'position':'JEPA EU沿模拟器状态到像素、encoder、预测特征及post-hoc uncertainty逐层追踪扰动，区分RSSM的GRU时间平均与重建目标实体像素权重。',
  'tradeoff':'预测—规划评测拆表示误差、预测误差和环境成功；JEPA EU分析不确定性在何层丢失。低一步误差、敏感uncertainty及更好规划是不同证据。观测posterior head可恢复当前帧异常信号，但不能用于没有未来观察的imagined rollout。',
  'en_position':'JEPA EU traces simulator-state perturbations through pixels, encoder, predictor features and post-hoc uncertainty, separating recurrent averaging from reconstruction-based entity weighting.',
  'en_tradeoff':'Prediction-planning evaluation separates representation error, prediction error and execution. JEPA EU asks where uncertainty loses a perturbation. Low error, responsive uncertainty and planning success are different evidence. A posterior head observes the current frame and cannot replace a prior head in imagined rollout.',
  'mechanism':'冻结LeWM与DreamerV3后，在预测头最后线性层前的特征上拟合last-layer Laplace，并用五头ensemble对照。对物理状态做标准差尺度扰动再由模拟器重渲染，追踪各层相对位移；延长扰动持续K帧可分离GRU平均效应，按实体重建梯度与像素面积分析小物体效应。此处是实证诊断，不是已完成移除重建项/改变gate的因果消融，也不证明所有RSSM或JEPA都如此。',
  'en_mechanism':'After freezing LeWM/DreamerV3, fit last-layer Laplace on predictor features and compare five-head ensembles. Perturb simulator coordinates in training-standard-deviation units and re-render frames, tracing stage-wise displacement. Vary persistence K to examine recurrent averaging and inspect entity reconstruction gradients/pixel areas. This is an empirical diagnosis, not a completed causal ablation removing reconstruction or changing gates, nor a universal claim about JEPA/RSSM.',
  'formula':r'''For frozen predictor feature $\psi$:

$$
\Lambda=\sigma^{-2}\sum_n\psi_n\psi_n^\top+\tau^{-2}I,\qquad s^2(\psi)=\psi^\top\Lambda^{-1}\psi.
$$

$$
x'=x+\epsilon\sigma_i e_i,\qquad
\rho_y=\mathbb E_x\frac{\|y(x')-y(x)\|}{\epsilon\|y(x)\|},\quad \kappa=\rho_{s^2}.
$$''',
  'formula_note':'Laplace只依赖输入特征：若扰动在前面被消掉，换最后读出也看不见。RSSM GRU把单帧扰动按gate缩放，持续扰动才累积；重建目标按像素贡献优化。posterior需观察帧，不可当作规划时可用的prior特征。',
  'en_formula_note':'A Laplace readout only sees its feature: a perturbation erased upstream cannot be recovered by changing that readout. The RSSM GRU admits a one-frame change through its gate and accumulates persistent changes; reconstruction allocates signal by pixels. The observation-dependent posterior feature is unavailable during imagination.',
  'results':'作者Table1中PushT的unfamiliar-state AUROC，body为LeWM .96 / Dreamer .73、object为.98 / .80；Finger等部分格子Dreamer更高。物理shift并非始终JEPA领先，Scene/Cube double也有失败。只比较一种LeWM和一种Dreamer类RSSM，bootstrap是固定模型的评测波动，不是多模型训练seed收益。生产线上 A/B：未报告。',
  'en_results':'Table1 gives PushT unfamiliar-state AUROC:body .96/.73 and object .98/.80 for LeWM/Dreamer; Dreamer leads some cells such as Finger. JEPA does not consistently win physical shifts, and Scene/Cube-double expose failures. One instance per paradigm is studied; fixed-model bootstrap variation is not training-seed variance. No production A/B is reported.',
  'local':'没有本地模型实现、adapter、operator、运行命令、metrics或GPU回执。没有以通用Laplace公式或手工异常数组冒充本文多环境比较。这里只交付固定v1原文审查、图源与教学问答。',
  'en_local':'No local model,adapter,operator,command,metrics or GPU receipt is provided. A generic Laplace calculation or hand-written anomaly array is not passed off as the multi-environment comparison. The delivery is fixed-v1 review,figure provenance and teaching questions only.',
  'checks':'本地未执行训练、五项任务或控制成功率测量。阅读时保留negative cells、prior/posterior区别，以及论文将来才建议开展的因果消融；不把相关性回归当作已实施架构干预。',
  'en_checks':'No training,five-task evaluation or control-success measurement is executed locally. The review retains negative cells,the prior/posterior distinction,and causal interventions proposed only as future work; regression associations are not presented as implemented architecture interventions.',
  'cost':'两模型在10视觉控制环境分别训练/冻结；LeWM ViT-Tiny224输入、6层预测器、特征2048，未有官方checkpoint时100 epochs；Dreamer small为64输入、GRU512、32×32分类状态，100 epochs。CEM每次300候选×30迭代，每格200episodes×3seeds、多个lambda与两种困难场景；另有五头ensemble。作者只给post-hoc head计时用单H200，未报全训练GPU小时或完整数据规模。按多环境训练与长rollout矩阵判断明显超本轮单A100/A30或Mac边界，不下载模型/数据，不以昂贵探跑估价。',
  'en_cost':'Two models are trained/frozen across10 visual-control environments. LeWM uses224-pixel ViT-Tiny,a six-layer predictor and2048-dimensional features,with100epochs where no official checkpoint exists. Dreamer-small uses64-pixel input,GRU512 and32x32 categorical state,also100epochs. CEM uses300candidates x30iterations,200episodes x3seeds per cell,multiple lambdas/two hard settings,and five-head ensembles. Only post-hoc head timing is attributed to one H200; total training hours and full data scale are not reported. The matrix exceeds this run\'s bounded single-A100/A30-or-Mac scope; no expensive probe or download is launched.',
  'qa':[
   ('feature-limits-uncertainty','basics','最后一层贝叶斯不确定性能看见任何输入异常吗？','不能。它只读冻结特征；若前面的表示已把异常抹平，最后一层估计器也无法恢复该差异。','教学例：正常与异常帧被映射到同一psi时，二者s²严格相同，即使原始像素差异很大。','Can last-layer Bayesian uncertainty detect every anomaly?','No. It only reads frozen features; an upstream-erased difference cannot be recovered at the last layer.','Illustration:normal and anomalous frames mapped to the same psi have exactly the same s-squared despite different pixels.'),
   ('persistence-not-stronger-head','mechanism','为什么把同一扰动持续多帧能检验RSSM的时间平均？','GRU单步只接纳gate比例的新状态，持续K帧逐步累积；这改变进入feature的信号，不是换更强uncertainty head。','教学例：固定gate=.25的线性近似在1帧保留.25，持续4帧保留1−.75⁴≈.684；只是说明机制，不是本地世界模型实测。','Why test the same perturbation over multiple frames?','A gated recurrent state admits only part of a new input per step,accumulating it over K frames. This changes the feature signal rather than the uncertainty estimator.','Illustration:a fixed .25gate retains .25 after one step and1-.75^4,about.684,after four; this is illustrative,not a measured local world model.'),
   ('uncertainty-not-planning-proof','comparison','比预测—规划评测多得到一个uncertainty指标，能跳过实际规划吗？','不能。误差、不确定性与成功率不同。JEPA EU还需真实CEM评估，并且posterior读出虽可检测当前异常，却依赖不可用于想象未来的观察。','教学例：用真实下一帧的posterior把异常检出率提高，并不表示planner在执行前就拥有该信号。','Does adding uncertainty remove the need for real planning evaluation?','No. Error,uncertainty and success differ. JEPA EU also evaluates CEM; a posterior readout can detect observed anomalies but requires observations absent in imagined futures.','Illustration:detecting an anomaly with the actual next-frame posterior does not make that signal available before the action.'),
   ('no-generic-laplace-substitute','implementation','本地只算Laplace二次型能声称复现本文结论吗？','不能。核心证据来自真实训练世界模型、可重渲染模拟器、逐层扰动追踪及五任务配对评测；完整矩阵已按成本终态不复现。','教学例：手工设正常psi=0、异常psi=1会保证分数不同，但那是把答案写进表示，无法证明JEPA优于RSSM。','Can a local Laplace quadratic form reproduce this conclusion?','No. The evidence requires trained world models,simulator re-rendering,stage traces and paired five-task evaluation. The complete matrix is terminally cost-deferred.','Illustration:assigning psi=0 to normal inputs and1 to anomalies builds the answer into features and proves no JEPA-over-RSSM claim.')],
 },
}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def dump(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def main():
    specs,papers,english,proposals,accepted=[],{},{},[],[]
    AUDIT.mkdir(parents=True,exist_ok=True)
    for key,c in CONTENT.items():
        identity='foundation-models:'+key
        directory=ROOT/'docs/foundation-models'/f"{c['id']}-{key}"
        source=f"https://arxiv.org/pdf/{c['id']}v1"
        abstract=f"https://arxiv.org/abs/{c['id']}v1"
        pdf=CACHE/f"{c['id']}v1.pdf"
        review_only=key=='jepa-eu'
        scope_limited=key=='rap'
        sections=SECTIONS[:-1]+['完整实验与成本边界'] if scope_limited else SECTIONS
        cost_heading='完整实验与成本边界' if scope_limited else '高成本完整实验'
        disposition_cn=('本轮组件范围完成，完整矩阵未执行；不是高成本延期。`full_experiment_status: not_run_scope_limited`，`full_experiment_review_done: false`；`review_done: true`只说明本轮组件/选题范围闭环。未实测完整数据集效果，不自动扩展、重试或进入Evolve。' if scope_limited else '**成本过高，不复现（审查 DONE）**，指完整论文实验矩阵；局部CPU组件与完整矩阵分开。终态 `not_reproduced_high_cost`，不下载大资源、不试训估价、不自动重试、不进入自动实现队列或Evolve；不让完整实验延期阻塞本轮审查闭环。')
        disposition_en=('The component scope is complete; the complete matrix was not run,not classified as prohibitively costly. Status:`not_run_scope_limited`; full_experiment_review_done:false. Review_done:true closes only this run\'s component/intake scope. No full-dataset outcome,automatic scope expansion,retry or Evolve claim.' if scope_limited else '**Too costly; not reproduced (review DONE).** This terminal decision applies to the complete paper matrix, distinct from bounded CPU components. Resolution:`not_reproduced_high_cost`. No large-resource download,trial training,automatic retry,implementation queue or Evolve promotion; full experiments do not block review closure.')
        code_path=None if review_only else f'src/auto_research/foundation_models/{key}.py'
        command=None if review_only else f"PYTHONPATH=src python -c 'from auto_research.foundation_models.{key} import diagnostic; print(diagnostic(42))'"
        code_label='未找到 / 尚未发布' if c['code'] is None else f"[作者仓库]({c['code']})；HEAD `{c['revision']}`"
        local_label='无；高成本 review-only，不提供本地实现' if review_only else f'`{code_path}`'
        status='review-only / deferred_high_cost' if review_only else 'CPU-only component_only / l1_mechanism'
        mermaid={'rap':'X[Canonical Lorentz points] --> R[Separate radius and unit direction]\n R --> P[Gaussian angular sketch and normalize]\n P --> L[Lift with unchanged radius]',
                 'duomi':'X[Input states] --> A[Router one and shared experts]\n A --> B[Updated states]\n B --> C[Router two and same experts]\n A --> D[Aligned all-expert logits]\n C --> D\n D --> E[Per-group G and D hinges then average]',
                 'jepa-eu':'X[Controlled simulator state perturbation] --> R[Re-render]\n R --> E[Encoder]\n E --> P[Prior predictor features or observed posterior control]\n P --> U[Laplace or ensemble]\n U --> T[Five separately evaluated tasks]'}[key]
        figure=f"<!-- paper-figure:start -->\n### 原论文关键图\n\n![原论文 {c['figure']}，固定 v1 第 {c['page']} 页，保留完整图注](assets/paper-figure-01.png)\n\n图片来自[原论文]({source}#page={c['page']})；未经科学内容编辑的整页栅格，含 {c['figure']} 完整图注，2026-11-26 已目视核对。版权归原作者所有；图中方法/结果不是本地测量。[来源与 SHA256](assets/provenance.json)。\n<!-- paper-figure:end -->"
        cn=f"""# {c['title']}

[English](README-en.md)

## 论文信息

| 字段 | 内容 |
| --- | --- |
| 论文链接 | [固定 v1]({abstract})；[原文 PDF]({source}) |
| 公司 / 作者机构 | {c['institutions']}；一作 {c['author']}：{c['affiliation']} |
| 首次公开日期 | `{c['published']}`（arXiv v1）；本轮发现/审查日 2026-11-26，不混作首发时间 |
| arXiv 公告日期 | `2026-11-26`；已核本轮官方 cs.LG new / cs.AI cross-list 公告，不改写 v1 首发时间 |
| 原作者开源代码 | {code_label}。{c['code_status']} |
| 本地 adapter / 稳定键 | `{key}`；`adapter: null`；不接入 Evolve |
| 本地复现代码目录 | {local_label} |
| 实现状态 | {status}；没有CUDA承诺或能力提升声明 |

## 原始论文总结

### 背景与主要改动

{c['mechanism']}

```mermaid
flowchart LR
 {mermaid}
```

{figure}

### 核心公式

{c['formula']}

{c['formula_note']}

### 论文离线与线上效果

{c['results']}

### 同主题比较与边界

{c['position']} [已审读的对照：{c['peer']}](../{Path(c['peer_path']).parent.name}/README.md)。{c['tradeoff']} 对照README的SHA256记录于本轮deep-dive提案。

## 本地复现

### 数据协议与代码映射

{c['local']}

{('无运行命令。' if review_only else '```bash'+chr(10)+command+chr(10)+'python -m pytest tests/test_nov26_foundation_components.py -q'+chr(10)+'```')}

### 结果与负控

{c['checks']}

### {cost_heading}

{c['cost']}

{disposition_cn}
"""
        (directory/'README.md').write_text(cn)
        en_code='Not found / not released after fixed-v1 and bounded author/title checks.' if c['code'] is None else f"[Author repository]({c['code']}), HEAD `{c['revision']}`; public Python repository verified, no declared license. Independently implemented from the formulas; upstream source was not copied."
        en=f"""# {c['title']}

<!-- source-sha256: {digest(directory/'README.md')} -->
[简体中文](README.md)

## Paper information

| Field | Content |
| --- | --- |
| Paper | [Fixed v1]({abstract}); [PDF]({source}) |
| Institutions | {c['institutions']}; first author {c['author']}: {c['affiliation']} |
| Original publication | `{c['published']}`; reviewed on 2026-11-26, not a new publication date |
| arXiv announcement | `2026-11-26`, verified in the official cs.LG new / cs.AI cross-list bulletin; distinct from the v1 submission timestamp |
| Author code | {en_code} |
| Local adapter / key | `{key}`; adapter null; no Evolve integration |
| Local reproduction code | {'None: high-cost review only.' if review_only else '`'+code_path+'`'} |
| Status | {status}; no CUDA path or capability claim |

## Original paper

### Background and method

{c['en_mechanism']}

```mermaid
flowchart LR
 {mermaid}
```

<!-- paper-figure:start -->
### Original paper figure

![{c['figure']}, fixed-v1 PDF page {c['page']}, complete caption retained](assets/paper-figure-01.png)

Unmodified full-page raster from the [paper]({source}#page={c['page']}), visually reviewed on2026-11-26. Copyright belongs to the original authors. This is the paper's method/results, not a local measurement. [Provenance and SHA256](assets/provenance.json).
<!-- paper-figure:end -->

### Core equations

{c['formula']}

{c['en_formula_note']}

### Reported results

{c['en_results']}

### Comparison and limits

{c['en_position']} [Reviewed peer:{c['peer']}](../{Path(c['peer_path']).parent.name}/README-en.md). {c['en_tradeoff']} The peer source fingerprint is recorded in the deep-dive proposal.

## Local reproduction

### Data and code contract

{c['en_local']}

{('No local command.' if review_only else '```bash'+chr(10)+command+chr(10)+'python -m pytest tests/test_nov26_foundation_components.py -q'+chr(10)+'```')}

### Evidence and negative controls

{c['en_checks']}

### {'Full experiments and cost boundary' if scope_limited else 'High-cost full experiments'}

{c['en_cost']}

{disposition_en}
"""
        (directory/'README-en.md').write_text(en)
        asset=directory/'assets/paper-figure-01.png'
        dump(directory/'assets/provenance.json',{'schema_version':1,'paper_url':abstract,'source_url':source+f"#page={c['page']}",
             'source_pdf_sha256':digest(pdf),'source_sha256':digest(pdf),'page':c['page'],'pdf_page':c['page'],'figure':c['figure'],
             'caption':c['figure_caption'],'image_sha256':digest(asset),'asset_sha256':digest(asset),'retrieved_on':DATE,
             'reviewed_version':'v1','visually_reviewed':True,'visually_reviewed_on':DATE,'scientific_content_modified':False,
             'render_dpi':120,'extraction':'Unmodified full PDF page raster including complete figure caption; pdftoppm at120dpi; visually reviewed.',
             'copyright':'Copyright belongs to the original authors.'})
        cost={'source':source,'sections':c['sections'],'available_resource':'one A100 or A30, or local Mac',
              'paper_configuration':c['cost'],'estimated_cost_basis':'Published configuration and scope estimate; no full local run,model/data download or costly probe.',
              'decision':'组件范围完成；完整矩阵未执行，未认定高成本，不自动扩scope或重试' if scope_limited else '成本过高，不复现（审查 DONE）；完整矩阵终态，无自动重试'}
        spec={'domain':'foundation-models','key':key,'title':c['title'],'paper_url':abstract,'reviewed_version_url':source,'reviewed_version':'v1',
              'published':'2026-11-25','published_at':c['published'],'announced_on':'2026-11-26','detail_path':f'foundation-models/{c["id"]}-{key}/README.md',
              'topic':[{'rap':'表征压缩与几何','duomi':'条件计算与专家路由','jepa-eu':'JEPA与世界模型'}[key]],
              'first_author':c['author'],'first_author_affiliation':c['affiliation'],'affiliation_evidence':'Fixed-v1 first-page byline and author superscripts.',
              'verified_priority_organizations':[],'code':c['code'],'code_status':c['code_status'],'code_license':None,'upstream_revision':c['revision'],
              'method_source_sha256':digest(pdf),'adapter':None,'priority':'P1','intake_class':'new_first_release_in_window',
              'implementation_status':'deferred_high_cost' if review_only else 'component_only','evaluation_tier':'paper_reported_only' if review_only else 'l1_mechanism',
              'diagnostic_only':True,'promotion_eligible':False,'evolve_integrated':False,
              'local_operator':None if review_only else f'auto_research.foundation_models.{key}.diagnostic','local_command':command,
              'requires_gpu_validation':False,'gpu_validation_passed':False,'gpu_validation_artifact':None,'full_experiment_status':'not_run_scope_limited' if scope_limited else 'not_reproduced_high_cost',
              'full_experiment_review_done':not scope_limited,'review_done':True,'review_resolution':'component_scope_complete' if scope_limited else 'not_reproduced_high_cost','automatic_retry':False,
              'automatic_implementation_queue':False,'cost_assessment':cost,'summary':c['position']+' '+c['tradeoff']}
        if review_only:spec['deferral_reason']='成本过高，不复现（审查 DONE）；多环境世界模型训练和长CEM rollout矩阵，review-only无本地执行。'
        specs.append(spec)
        questions,translations=[],{}
        for qid,level,q,a,example,eq,ea,ee in c['qa']:
            questions.append({'id':qid,'level':level,'question':q,'answer':a,'example':example,'source_sections':sections,'added':DATE})
            translations[qid]={'question':eq,'answer':ea,'example':ee}
        papers[identity]={'questions':questions}
        units=question_units({identity:questions})
        for q in questions:
            uid=f"qa/{identity}/{q['id']}"
            english[uid]={'source_sha256':units[uid].source_sha256,'reviewed':True,'fields':translations[q['id']]}
        peer='foundation-models:'+c['peer']
        pair=[identity,peer]
        revisions={identity:digest(directory/'README.md'),peer:digest(ROOT/'docs'/c['peer_path'])}
        compare=questions[2]
        proposals.append({'paper':identity,'target_card':c['card'],'source_revisions':revisions,
                          'comparison':{'position':c['position'],'tradeoff':c['tradeoff'],'sections':sections[:3]},
                          'analysis':{'title':c['title'],'body':c['tradeoff']+' '+c['formula_note'],'papers':pair},
                          'question':{'id':'nov26-'+key,'question':compare['question'],'answer':compare['answer'],'example':compare['example'],'papers':pair},
                          'update':{'date':DATE,'papers':pair,'source_revisions':revisions,'summary':c['tradeoff']+(' 本轮组件范围闭环；完整矩阵未执行且未认定高成本。' if scope_limited else ' 完整矩阵高成本终态，不以L1或审查充当能力证据。')},
                          'english':{'comparison':{'position':c['en_position'],'tradeoff':c['en_tradeoff']},
                                     'analysis':{'title':c['title'],'body':c['en_tradeoff']+' '+c['en_formula_note']},
                                     'question':translations[compare['id']],'update':c['en_tradeoff']+(' The component scope is complete; the full matrix was not run and is not labeled high-cost.' if scope_limited else ' Complete matrices are terminally cost-deferred; L1 or review is not capability evidence.')}})
        accepted.append({'arxiv_id':c['id'],'identity':identity,'key':key,'domain':'foundation-models','title':c['title'],
                         'first_author':c['author'],'first_author_affiliation':c['affiliation'],'first_published_at':c['published'],
                         'announced_on':'2026-11-26','intake_class':'new_first_release_in_window','reviewed_version':'v1',
                         'reviewed_source_url':source,'source_sha256':digest(pdf),'sections_read':c['sections'],'scope':spec['summary'],
                         'source_revisions':revisions,'cost_basis':cost,'implementation_status':spec['implementation_status'],
                         'evaluation_tier':spec['evaluation_tier'],'local_detail_path':spec['detail_path'],'requires_gpu_validation':False,
                         'gpu_validation_passed':False,'code_url':c['code'],'upstream_revision':c['revision'],
                         'full_experiment_status':spec['full_experiment_status'],'full_experiment_review_done':spec['full_experiment_review_done'],'review_resolution':spec['review_resolution'],'review_done':True,
                         'automatic_retry':False,'automatic_implementation_queue':False})
    dump(AUDIT/'paper-proposals-foundation.json',{'schema_version':1,'date':DATE,'papers':specs})
    dump(AUDIT/'foundation-authored-bundle.json',{'schema_version':1,'date':DATE,'papers':papers,'english_question_units':english})
    dump(AUDIT/'deep-dive-proposals-foundation.json',{'schema_version':1,'reviewed_on':DATE,'integration_owner':'root','proposals':proposals})
    dump(AUDIT/'foundation-review.json',{'schema_version':1,'reviewed_on':DATE,'accepted':accepted,'preflight_before_implementation':True,
         'available_resource':'one A100 or A30, or local Mac','watermark_change_claimed':False,'large_downloads_authorized_or_needed':False,
         'scope':'Finite Nov25 first-release selection:two CPU L1 components and one terminal high-cost review-only paper. Not exhaustive coverage.'})


if __name__=='__main__':
    main()
