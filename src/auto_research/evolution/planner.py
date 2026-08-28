from __future__ import annotations

from dataclasses import replace
import random

from ..post_training.models import ALGORITHMS as POST_TRAINING_ALGORITHMS
from .models import Genome, PaperInspiration
from .compatibility import compatible_architectures


def allowed_architectures(model: str, direction: str, papers: list[PaperInspiration]) -> list[str]:
    def compatible(values: list[str]) -> list[str]:
        return compatible_architectures(model, list(dict.fromkeys(values)))

    if model == "genrec":
        defaults = [
            "context:full", "context:longer-compressed",
            "head:semantic-catalog", "head:hybrid-catalog",
            "reward:novelty", "reward:content-discovery",
            "distillation:popularity-teacher",
            "distillation:semantic-teacher",
        ]
        mapped = [
            paper.architecture for paper in papers
            if paper.architecture and paper.architecture.split(":", 1)[0]
            in {"context", "head", "reward", "distillation"}
        ]
        return compatible([*mapped, *defaults])
    if model == "reasoning-checkpoint":
        return compatible(["reasoning:1", "reasoning:2", "reasoning:4", "reasoning:8"])
    if model == "vlm-checkpoint":
        return compatible([
            "checkpoint_vlm:direct",
            "checkpoint_vlm:context-first",
            "checkpoint_vlm:elimination",
            "checkpoint_vlm:no-hint",
        ])
    if model == "micro-vlm":
        values = [
            "micro_vlm_linear", "micro_vlm_mlp", "micro_vlm_query",
            "micro_vlm_qformer", "micro_vlm_gated", "micro_vlm_pixelshuffle",
            "objective:siglip2", "objective:gas-nep",
        ]
        text = direction.lower()
        priorities = {
            "micro_vlm_query": ("query", "q-former", "查询", "视觉查询"),
            "micro_vlm_mlp": ("mlp", "projector", "投影", "llava"),
            "micro_vlm_qformer": ("blip-2", "blip2", "q-former", "qformer"),
            "micro_vlm_gated": ("gated projector", "门控投影"),
            "micro_vlm_pixelshuffle": ("smolvlm", "pixel shuffle", "像素重排", "token 压缩"),
        }
        for architecture, terms in priorities.items():
            if any(term in text for term in terms):
                values.remove(architecture)
                values.insert(0, architecture)
        return compatible(values)
    if model == "post-training":
        installed = list(POST_TRAINING_ALGORITHMS)
        mapped = [paper.architecture for paper in papers if paper.architecture in installed]
        requested = [
            value for value in installed
            if value.replace("-", " ") in direction.lower().replace("-", " ")
        ]
        if "reco" in direction.lower() and "reco-grpo" not in requested:
            requested.insert(0, "reco-grpo")
        return compatible([*requested, *mapped, *installed])
    if model == "agent":
        operators = [paper.architecture for paper in papers if paper.architecture and ":" in paper.architecture]
        operators = list(dict.fromkeys([
            *operators,
            "reflection:reflexion", "verifier:public-evidence",
            "context:compressed",
        ]))
        if operators:
            text = direction.lower().replace("_", "-")
            compact_text = text.replace("-", "").replace(" ", "")
            requested = [
                operator for operator in operators
                if operator.split(":", 1)[1]
                .replace("_", "")
                .replace("-", "")
                .replace(" ", "") in compact_text
            ]
            # Put one operator from each axis first so a small first generation is
            # still a fair component ablation rather than four planner variants.
            interleaved = []
            for component in (
                "memory:", "planner:", "tool:", "critic:", "policy:",
                "recovery:", "reflection:", "verifier:", "context:",
            ):
                match = next(
                    (
                        value for value in operators
                        if value.startswith(component) and value not in requested
                    ),
                    None,
                )
                if match:
                    interleaved.append(match)
            return compatible([*requested, *interleaved, *operators])
        return compatible([
            "memory:u-mem", "memory:legomem", "planner:react", "planner:rewoo",
            "planner:tree-of-thoughts", "planner:lats", "tool:toolformer",
            "tool:memtool", "critic:self-refine", "recovery:reflexion",
            "planner:metagpt", "planner:swe-agent", "planner:openhands",
            "critic:critic", "policy:agent-lightning",
            "reflection:reflexion", "verifier:public-evidence",
            "context:compressed",
            "tool:mrkl", "planner:hugginggpt",
            "memory:generative-agents", "memory:memgpt",
            "tool:webgpt", "planner:saycan", "tool:pal", "planner:art",
            "critic:seed", "critic:cast", "planner:turn-opd",
            "tool:search-r1", "critic:ragen",
            "critic:loop", "planner:webagent-r1", "tool:mua-rl",
            "memory:voyager", "planner:autogen", "planner:pearl",
            "memory:hiskill", "memory:unimem",
            "tool:cam-df", "memory:skillrise",
            "critic:tapo", "critic:grsd",
            "critic:envace",
            "critic:agent-opsd", "critic:ocsd",
            "memory:vermem", "memory:coevo-mem",
        ])
    if model == "micro-llm":
        values = [
            "gpt_baseline", "gpt_gqa", "llama_modern", "llama_gqa",
            "parallel_gelu", "parallel_swiglu", "llama_gqa_parallel",
            "hyper_connections", "mhc", "qkv_depthwise_conv",
            "mobius_rope", "naju", "adadsf",
            "engram", "looped_latent_attention", "gaugequant", "penelope",
            "switch_transformer", "mamba", "switch_attention",
            "native_sparse_attention", "gated_attention",
            "nsa_gated_attention", "wide_dynamic_width", "retoken", "optimizer:muon",
            "block_attnres", "rd_attnres",
            "olm_composable",
            "macro", "hilp",
            "rope", "alibi", "gqa", "hymba", "moba", "blt",
        ]
        text = direction.lower().replace("-", "")
        priority_terms = {
            "engram": ("engram", "conditional memory", "条件记忆", "查表记忆"),
            "looped_latent_attention": (
                "looped latent attention", "lla", "kv compression",
                "kv 压缩", "循环注意力",
            ),
            "gaugequant": ("gaugequant", "quantization", "量化", "w4a4"),
            "penelope": (
                "penelope", "latent recurrence", "latent reasoning",
                "局部循环", "隐式推理",
            ),
            "switch_transformer": ("switch transformer", "sparse moe", "稀疏 moe"),
            "mamba": ("mamba", "selective ssm", "选择性状态空间"),
            "switch_attention": ("switch attention", "swiattn", "动态注意力路由"),
            "native_sparse_attention": (
                "native sparse attention", "nsa", "原生稀疏注意力",
            ),
            "gated_attention": (
                "gated attention", "attention gate", "门控注意力",
            ),
            "optimizer:muon": ("muon", "正交优化器"),
            "wide_dynamic_width": (
                "wide", "dynamic width", "token-level width", "动态宽度", "宽度剪枝",
            ),
            "retoken": (
                "retoken", "retrieval token", "value cache retrieval",
                "检索 token", "视觉缓存检索",
            ),
            "rd_attnres": (
                "rd-attnres", "role decoupled", "qk v route", "残差路由", "角色解耦",
            ),
            "olm_composable": (
                "openlanguagemodel", "open language model", "olm",
                "composable", "可组合", "预训练基础设施",
            ),
            "rope": ("rope", "rotary", "旋转位置"),
            "alibi": ("alibi", "linear bias", "长度外推"),
            "gqa": ("gqa", "grouped query", "分组查询"),
            "hymba": ("hymba", "hybrid head", "混合头"),
            "moba": ("moba", "mixture of block", "块路由"),
            "blt": ("byte latent", "blt", "字节 patch"),
            "macro": ("macro", "markov route", "层路由", "跳层", "重复层"),
            "hilp": ("hilp", "hierarchical latent", "分层 latent", "层级隐变量"),
        }
        for architecture, terms in priority_terms.items():
            if any(term in text for term in terms):
                values.remove(architecture)
                values.insert(0, architecture)
        if (
            any(term in text for term in ("native sparse attention", "nsa", "原生稀疏注意力"))
            and any(term in text for term in ("gated attention", "attention gate", "门控注意力"))
        ):
            values.remove("nsa_gated_attention")
            values.insert(0, "nsa_gated_attention")
        if any(term in text for term in ("adadsf", "adaptive depth", "动态深度", "深度稀疏")):
            values.remove("adadsf")
            values.insert(0, "adadsf")
        return compatible(values)
    text = direction.lower()
    requested = []
    if "longer" in text or "长序列" in text or "long sequence" in text:
        requested.append("longer")
    if "unimixer" in text or "高效 transformer" in text or "efficient transformer" in text:
        requested.append("unimixer")
    for paper in papers:
        if paper.architecture in {"longer", "unimixer"} and paper.architecture not in requested:
            requested.append(paper.architecture)
    if model == "hyformer":
        values = ["hyformer"]
        if "longer" in requested: values.append("hyformer_longer")
        if "unimixer" in requested: values.append("hyformer_unimixer")
        if set(requested) >= {"longer", "unimixer"}: values.append("hyformer_longer_unimixer")
        return compatible(values)
    values = ["rankmixer_dense"]
    if "longer" in requested: values.append("rankmixer_longer")
    if "unimixer" in requested: values.append("rankmixer_unimixer")
    if set(requested) >= {"longer", "unimixer"}: values.append("rankmixer_longer_unimixer")
    direct_terms = {
        "rankmixer_whale": ("whale", "wukong", "hstu"),
        "rankmixer_tmallgs": ("tmallgs", "天猫", "field-wise"),
        "rankmixer_long_history": (
            "long-history",
            "long history",
            "长历史",
            "缓存",
        ),
        "rankmixer_ramp": ("ramp", "隐私", "特征受限", "feature availability"),
        "rankmixer_kgd": ("kgd", "knowledge geometry", "知识几何", "可刷新预训练", "bmtp"),
        "rankmixer_tokenminds": ("tokenminds", "user token", "用户 token", "sid 用户"),
        "rankmixer_ha_moe": ("ha-moe", "heterogeneous moe", "异构 moe", "异构门控"),
        "rankmixer_dual_sid": ("dual sid", "dual-purpose", "双用途 sid"),
        "rankmixer_mfli": ("mfli", "learnable index", "可学习索引", "多切面"),
        "rankmixer_kunlun": ("kunlun", "gdpa", "昆仑"),
        "rankmixer_ultra_hstu": ("ultra-hstu", "ultra hstu", "semi-local", "半局部"),
        "rankmixer_dceo": ("dceo", "causal effect", "因果效果", "长期价值"),
        "rankmixer_transretrieval": ("transretrieval", "norm-aware", "目标压缩", "跨域召回"),
    }
    for architecture, terms in direct_terms.items():
        if any(term in text for term in terms):
            if architecture in values:
                values.remove(architecture)
            values.insert(0, architecture)
    mapping = {
        p.architecture: p.architecture for p in papers
        if p.architecture
        and p.architecture not in {"longer", "unimixer"}
        and (not text or p.architecture.replace("_", "") in text.replace("-", "").replace("_", "") or p.title.lower().split(":", 1)[0] in text)
    }
    values.extend(mapping.values())
    return compatible(values)


def propose(parent: Genome, generation: int, index: int, architectures: list[str], rng: random.Random, model: str = "rankmixer"):
    if model == "reasoning-checkpoint":
        return _propose_reasoning(parent, generation, index, architectures, rng)
    if model == "post-training":
        return _propose_post_training(parent, generation, index, architectures, rng)
    if model == "agent":
        return _propose_agent(parent, generation, index, architectures, rng)
    if model == "genrec":
        return _propose_genrec(parent, generation, index, architectures, rng)
    if model == "micro-llm":
        return _propose_llm(parent, generation, index, architectures, rng)
    if model == "micro-vlm":
        return _propose_multimodal(parent, generation, index, architectures, rng)
    if model == "vlm-checkpoint":
        return _propose_checkpoint_vlm(parent, generation, index, architectures, rng)
    architecture = architectures[(index + generation - 1) % len(architectures)] if generation == 1 else rng.choice(architectures)
    genome = replace(parent, architecture=architecture)
    changes = [f"结构假设：{architecture}"]
    if generation == 1:
        if architecture == "rankmixer_dceo":
            gains = (0.10, 0.20, 0.35, 0.50, 0.75)
            temperatures = (0.75, 1.0, 1.25, 1.5)
            genome = replace(
                genome,
                dceo_causal_gain=gains[index % len(gains)],
                dceo_temperature=temperatures[index % len(temperatures)],
            )
            changes.append(
                "DCEO validation 搜索："
                f"gain={genome.dceo_causal_gain}, temperature={genome.dceo_temperature}"
            )
        changes.append("公平结构消融：保持基线超参数不变")
        return genome, "；".join(changes)
    if architecture == "rankmixer_dceo" and (generation + index) % 2 == 0:
        genome = replace(
            genome,
            dceo_causal_gain=rng.choice((0.10, 0.20, 0.35, 0.50, 0.75)),
            dceo_temperature=rng.choice((0.75, 1.0, 1.25, 1.5)),
        )
        changes.append(
            "DCEO 因果融合变异："
            f"gain={genome.dceo_causal_gain}, temperature={genome.dceo_temperature}"
        )
    knobs = (
        ("dimensions", [32, 64, 96, 128]), ("layers", [1, 2, 3, 4]),
        ("learning_rate", [1e-4, 3e-4, 6e-4, 1e-3]),
        ("optimizer", ["adamw", "adam", "adagrad"]), ("batch_size", [24, 32, 48, 64]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    genome = replace(genome, **{name: value})
    changes.append(f"控制变量：{name}={value}")
    return genome, "；".join(changes)


def _propose_llm(parent, generation, index, architectures, rng):
    if generation == 1:
        architecture = architectures[index % len(architectures)]
        if architecture.startswith("optimizer:"):
            optimizer = architecture.split(":", 1)[1]
            return replace(parent, optimizer=optimizer), (
                f"优化器研究：{optimizer}；保持结构、数据配方和训练预算不变"
            )
        return replace(parent, architecture=architecture), (
            f"结构研究：{architecture}；保持数据配方、训练预算和后训练方法不变"
        )
    if generation == 2:
        recipes = (
            ("wikitext", 0.0), ("mixed_narrative", 0.10),
            ("mixed_narrative", 0.20), ("mixed_narrative", 0.35),
            ("curriculum", 0.20), ("curriculum", 0.35),
        )
        recipe, ratio = recipes[index % len(recipes)]
        return replace(parent, data_recipe=recipe, data_mix_ratio=ratio), (
            f"数据研究：recipe={recipe}, narrative_ratio={ratio}；冻结冠军结构与训练参数"
        )
    if generation == 3:
        methods = (
            ("none", 0.0, 0),
            ("sft", 0.0, 24),
            ("sft_low_lr", 0.0, 24),
            ("neftune", 5.0, 24),
            ("dynamic_rubric", 0.0, 24),
            ("off_context_grpo", 0.0, 24),
            ("neftune", 10.0, 24),
            ("neftune", 15.0, 24),
        )
        method, alpha, steps = methods[index % len(methods)]
        return replace(parent, post_training=method, neftune_alpha=alpha, post_steps=steps), (
            f"后训练研究：method={method}, neftune_alpha={alpha}, post_steps={steps}；冻结结构和预训练数据配方"
        )
    knobs = (
        ("dimensions", [256, 384, 512]), ("layers", [4, 6, 8]),
        ("learning_rate", [1e-4, 3e-4, 6e-4]),
        ("optimizer", ["adamw", "muon", "adam", "adagrad"]),
        ("batch_size", [2, 4, 8]), ("sequence_length", [64, 128, 256]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    return replace(parent, **{name: value}), f"联合优化：{name}={value}"


def _propose_multimodal(parent, generation, index, architectures, rng):
    if generation == 1:
        architecture = architectures[index % len(architectures)]
        if architecture.startswith("objective:"):
            objective = architecture.split(":", 1)[1]
            return replace(parent, multimodal_objective=objective), (
                f"多模态训练目标消融：{objective}；保持 connector、图像、问题与预算不变"
            )
        return replace(parent, architecture=architecture), (
            f"多模态 connector 消融：{architecture}；保持图像、问题、预算与模型宽度不变"
        )
    knobs = (
        ("dimensions", [64, 96, 128, 192]),
        ("learning_rate", [1e-3, 3e-3, 6e-3]),
        ("batch_size", [8, 16, 32]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    return replace(parent, **{name: value}), (
        f"围绕冠军 connector 调整 {name}={value}；继续保留打乱图和空白图对照"
    )


def _propose_checkpoint_vlm(parent, generation, index, architectures, rng):
    if generation == 1:
        candidate = architectures[index % len(architectures)].split(":", 1)[1]
        if candidate == "no-hint":
            return replace(parent, checkpoint_use_hint=False), (
                "真实 checkpoint 输入消融：移除 ScienceQA hint；其余推理参数保持基线"
            )
        return replace(parent, checkpoint_prompt_style=candidate), (
            f"真实 checkpoint 提示模板消融：{candidate}；保持图像和解码预算不变"
        )
    knobs = (
        ("checkpoint_max_new_tokens", [4, 8, 16]),
        ("checkpoint_image_size", [0, 384, 512]),
        ("checkpoint_use_hint", [True, False]),
        ("checkpoint_prompt_style", ["direct", "context-first", "elimination"]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    return replace(parent, **{name: value}), (
        f"围绕冠军 checkpoint 推理配方调整 {name}={value}；不修改模型权重"
    )


def _propose_reasoning(parent, generation, index, architectures, rng):
    if generation == 1:
        samples = int(architectures[index % len(architectures)].split(":", 1)[1])
        return replace(
            parent, reasoning_samples=samples, reasoning_stop_consensus=1.0,
        ), f"同 checkpoint 推理预算消融：samples={samples}；不使用 gold answer 选样"
    knobs = (
        ("reasoning_samples", [2, 4, 8]),
        ("reasoning_max_new_tokens", [48, 96, 160]),
        ("reasoning_stop_consensus", [0.5, 0.67, 0.75, 1.0]),
    )
    name, values = knobs[(generation + index) % len(knobs)]
    value = rng.choice(values)
    return replace(parent, **{name: value}), (
        f"围绕冠军调整 {name}={value}；准确率、token、延迟和调用数共同记录"
    )


def _propose_post_training(parent, generation, index, algorithms, rng):
    if generation == 1:
        method = algorithms[index % len(algorithms)]
        return replace(
            parent,
            architecture="candidate-policy",
            post_training=method,
            post_steps=max(parent.post_steps, 40),
        ), f"后训练 objective 消融：{method}；冻结数据、特征和训练预算"
    knobs = (
        ("post_data_recipe", ["base", "hard-half", "curriculum"]),
        ("post_teacher", ["auto", "cached", "online"]),
        ("post_rollout", ["on-policy", "replay", "mixed"]),
        ("gradient_accumulation", [1, 2, 4]),
        ("mixed_precision", ["no", "bf16", "fp16"]),
        ("learning_rate", [0.02, 0.04, 0.08, 0.12]),
        ("group_size", [2, 4, 6]),
        ("post_steps", [40, 80, 120]),
    )
    name, values = knobs[index % len(knobs)]
    # A five-candidate round exposes data, teacher, rollout and system axes.
    value = values[1 + ((generation + index) % (len(values) - 1))]
    method = rng.choice(algorithms)
    return replace(
        parent,
        architecture="candidate-policy",
        post_training=method,
        **{name: value},
    ), (
        f"组合优化：objective={method}, {name}={value}；保留 data/teacher/rollout/"
        "gradient-accumulation/precision 的父代组合"
    )


def _propose_agent(parent, generation, index, operators, rng):
    values = {
        "memory": ["none"],
        "planner": ["fast"],
        "tool": ["direct"],
        "critic": ["none"],
        "policy": ["heuristic", "replay-policy", "pairwise-policy"],
        "recovery": ["none", "retry", "rollback"],
        "reflection": ["none", "reflexion"],
        "verifier": ["none", "public-evidence"],
        "context": ["full", "compressed"],
    }
    for operator in operators:
        if ":" not in operator:
            continue
        component, value = operator.split(":", 1)
        if component in values and value not in values[component]:
            values[component].append(value)
    if generation == 1:
        operator = operators[index % len(operators)]
        component, value = operator.split(":", 1)
        field = {
            "memory": "agent_memory", "planner": "agent_planner",
            "tool": "agent_tool_policy", "critic": "agent_critic",
            "policy": "agent_policy", "recovery": "agent_failure_recovery",
            "reflection": "agent_reflection", "verifier": "agent_verifier",
            "context": "agent_context_compression",
        }[component]
        return replace(parent, architecture="composable-agent", **{field: value}), (
            f"论文算子单组件消融：{operator}；其余组件保持基线"
        )
    return replace(
        parent,
        architecture="composable-agent",
        agent_memory=rng.choice(values["memory"]),
        agent_planner=rng.choice(values["planner"]),
        agent_tool_policy=rng.choice(values["tool"]),
        agent_critic=rng.choice(values["critic"]),
        agent_policy=rng.choice(values["policy"]),
        agent_failure_recovery=rng.choice(values["recovery"]),
        agent_reflection=rng.choice(values["reflection"]),
        agent_verifier=rng.choice(values["verifier"]),
        agent_context_compression=rng.choice(values["context"]),
        memory_size=rng.choice((8, 16, 24, 48)),
    ), (
        "论文检索约束下的 Agent 组合 genome：搜索 memory / planner / tool / "
        "critic / policy / recovery / reflection / verifier / context / capacity"
    )


def _propose_genrec(parent, generation, index, operators, rng):
    fields = {
        "context": "genrec_context",
        "head": "genrec_head",
        "reward": "genrec_reward",
        "distillation": "genrec_distillation",
    }
    values = {
        "context": ["recent", "full", "longer-compressed"],
        "head": ["id-catalog", "semantic-catalog", "hybrid-catalog"],
        "reward": ["uniform", "novelty", "content-discovery"],
        "distillation": ["none", "popularity-teacher", "semantic-teacher"],
    }
    if generation == 1:
        operator = operators[index % len(operators)]
        component, value = operator.split(":", 1)
        return replace(
            parent, architecture="genrec-catalog", **{fields[component]: value},
        ), f"生成式推荐单轴消融：{operator}；其余 catalog 训练条件保持基线"
    genome = replace(
        parent,
        architecture="genrec-catalog",
        genrec_context=rng.choice(values["context"]),
        genrec_head=rng.choice(values["head"]),
        genrec_reward=rng.choice(values["reward"]),
        genrec_distillation=rng.choice(values["distillation"]),
    )
    if generation >= 3:
        field, choices = rng.choice((
            ("dimensions", (32, 64, 96)),
            ("sequence_length", (8, 12, 24)),
            ("learning_rate", (1e-3, 3e-3, 1e-2)),
        ))
        genome = replace(genome, **{field: rng.choice(choices)})
    return genome, (
        "围绕冠军组合 context / catalog head / reward / distillation；"
        "validation 仅以全目录排序指标晋级"
    )


def round_record(generation, parent, trials, champion):
    ranked = sorted(trials, key=lambda trial: trial.fitness, reverse=True)
    return {
        "generation": generation, "parent": parent.trial_id,
        "hypotheses": [{"trial_id": t.trial_id, "rationale": t.rationale, "architecture": t.genome.architecture} for t in trials],
        "observations": [{"trial_id": t.trial_id, "fitness": t.fitness, "status": t.status,
                          "validation": t.validation} for t in ranked],
        "decision": f"下一轮围绕 {champion.trial_id} / {champion.genome.architecture} 继续搜索",
        "improved": champion.fitness > parent.fitness,
    }
