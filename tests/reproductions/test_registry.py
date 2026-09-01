import json

from auto_research.reproductions.registry import get_adapter, list_adapters
from auto_research.reproductions.base import ReproductionFidelity
from auto_research.reproductions.reporting import write_reproduction_result


def test_builtin_adapters_are_discoverable():
    assert {adapter.key for adapter in list_adapters()} == {
        "bahe",
        "memory-layer",
        "scalr",
        "hill-index",
        "semantic-native-longseq",
        "friend-gnn",
        "argus",
        "akt-rec",
        "adadsf",
        "beque",
        "barge",
        "cluster-goobs",
        "cobra",
        "cmsl",
        "din",
        "cross-domain-kd",
        "danet",
        "degre",
        "g2rec",
        "genrank",
        "grc",
        "gr4ad",
        "hstu",
        "harness-lm",
        "hyformer",
        "kar",
        "learn",
        "leadre",
        "llatte",
        "llm-ad-retrieval",
        "longer",
        "lsvcr",
        "lum",
        "lwgr",
        "m6rec",
        "mdcns",
        "mesh",
        "memento",
        "mobius-rope",
        "mbgr",
        "mixformer",
        "mm-llm",
        "msd",
        "notellm",
        "naju",
        "nontp",
        "onerec",
        "onerec-v2",
        "onetrans",
        "pinfm",
        "pinrec",
        "pinterest-ads-llm",
        "pinequalizer",
        "plum",
        "precise",
        "prompt-generation",
        "proximity-features",
        "rankmixer",
        "rec-distill",
        "s-grec",
        "sam",
        "self-evolving-rec",
        "sessionrec",
        "sasrec",
        "seral",
        "saviorrec",
        "sigma",
        "sis",
        "tiger",
        "transact-v2",
        "univa",
        "growthgr",
        "fluid",
        "gzip-sparse-attention",
        "memory-grafting",
        "mhc",
        "conv-llm",
        "ppl-factory",
        "recap",
        "uame",
        "slimper",
        "recgpt-v3",
        "recgpt-mobile",
        "sort-gen",
        "tsgr",
        "whale",
        "windowed-mtp",
        "ramp",
        "tmallgs",
        "long-history-transformer",
        "downstream-rewards",
        "dynamic-rubric",
        "off-context-grpo",
        "nova",
        "evorec",
        "tokenmixer-large",
        "msn",
        "idproxy",
        "glide",
        "genrec",
        "genrec-netflix",
        "rankgraph2",
        "solaris",
        "minimax-sparse-attention",
        "onemall",
        "dos",
        "mdl",
        "hisac",
        "pinclip",
        "pin-scale",
        "causal-retrieval",
        "podcast-mtl",
        "engram",
        "looped-latent-attention",
        "gaugequant",
        "wide-deep",
        "dcn-v2",
        "dien",
        "bst",
        "cs3",
        "cq-sid",
        "switch-transformer",
        "mamba",
        "switch-attention",
        "deepfm",
        "youtube-dnn",
        "esmm",
        "mmoe",
        "ple",
        "mosaic",
        "unir2",
        "core-relevance",
        "data-orchestra",
        "mim",
        "filterllm",
        "fuxi-alpha",
        "recgpt-v2",
        "higr",
        "drl-put",
        "adaf2m2",
        "mgoe",
        "click-a-buy-b",
        "native-sparse-attention",
        "gated-attention",
        "muon",
        "reco-reward",
        "twice",
        "swag-bid",
        "youtube-freshness",
        "melo",
        "penelope",
        "oxygenrec-v2",
        "asarl",
        "ccformer",
        "open-web-ufm",
        "rocs",
        "wide",
        "retoken",
        "gryphon-v2",
        "degr",
        "rd-attnres",
        "dme",
        "steps",
        "spear",
        "open-language-model",
        "glorank",
        "dual-rerank",
        "oneranker",
        "radar",
        "dualgr",
        "mpformer",
        "hap",
        "onepiece",
        "intsr",
        "cdm",
        "cwm",
        "rope",
        "alibi",
        "gqa",
        "hymba",
        "moba",
        "blt",
        "doremi",
        "data-mixing-laws",
        "twin-v2",
        "sim",
        "crsd",
        "clip",
        "blip2",
        "llava",
        "siglip2",
        "smolvlm",
        "speculative-decoding",
        "awq",
        "medusa",
        "hrpo",
        "kgd",
        "llm-ts-prior",
        "twitch-mor",
        "qevict",
        "dblast",
        "hilp",
        "macro",
        "bakron",
        "tokenminds",
        "ha-moe",
        "dual-sid",
        "agentic-rec-tune",
        "mfli",
        "kunlun",
        "ultra-hstu",
        "metastrategy",
        "sona",
        "gas",
        "connectionmind",
        "dream",
        "dynamic-codebook",
        "netflix-mediafm",
        "ogr",
        "inthq",
        "pushdualgen",
        "recharness",
        "gala",
        "feedback-policy",
        "real-estate-rerank",
        "adaptive-ad-load",
        "guess-where-you-go",
        "genpage",
        "journeyformer",
        "l2rec",
        "qgs",
        "tubifm",
        "pearl-percentile",
        "dadf",
        "onemodel",
        "rare",
        "clockrope",
        "oneshot-index",
        "next-vlm",
        "prl-puts",
        "ektm",
        "adasid",
        "unirec-coa",
        "uniscale",
        "gatesid",
        "aigq",
        "safro",
        "sort-ranking",
        "quasid",
        "gpl-prerank",
        "ltv-video-ranking",
        "rgalign-rec",
        "linkedin-feed-sr",
        "cadet",
        "diffureason",
        "sarm",
        "ml-dcn",
        "rag-qac",
        "tcab",
        "olmpool-long-context",
        "distillcache",
        "autonomy-heads",
        "physics-mm-pretraining",
        "ttcd",
        "dart",
        "transmem",
        "c2kv",
        "tagr",
        "wemm-embedding",
        "dceo",
        "transretrieval",
        "vbvr-pro",
        "mllmclip",
        "pace-vlm",
        "twinkv",
    }
    assert get_adapter("sis").paper.arxiv_id == "2607.04728"
    assert get_adapter("plum").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("onerec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("g2rec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("mixformer").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("rankmixer").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("hyformer").paper.arxiv_id == "2601.12681"
    assert get_adapter("onetrans").paper.arxiv_id == "2510.26104"
    assert get_adapter("rec-distill").paper.arxiv_id == "2605.29755"
    assert get_adapter("din").paper.arxiv_id == "1706.06978"
    assert get_adapter("recgpt-v3").paper.has_online_ab
    assert get_adapter("recgpt-mobile").paper.has_online_ab
    assert get_adapter("sort-gen").paper.has_online_ab
    assert get_adapter("tsgr").paper.has_online_ab
    assert get_adapter("whale").paper.has_online_ab
    assert get_adapter("ramp").paper.code_url == "https://github.com/Ruixinhua/RAMP"
    assert get_adapter("tmallgs").paper.has_online_ab
    assert get_adapter("long-history-transformer").paper.has_online_ab
    assert get_adapter("downstream-rewards").paper.has_online_ab
    assert get_adapter("dynamic-rubric").paper.selection_exception
    assert get_adapter("off-context-grpo").paper.code_url == "https://github.com/AgPriyank/OC-GRPO"
    assert get_adapter("nova").paper.has_online_ab
    assert get_adapter("evorec").paper.has_online_ab
    assert get_adapter("tokenmixer-large").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert (
        get_adapter("minimax-sparse-attention").paper.code_url
        == "https://github.com/MiniMax-AI/MSA"
    )
    assert get_adapter("onemall").paper.has_online_ab
    assert get_adapter("pin-scale").paper.has_online_ab
    assert get_adapter("podcast-mtl").paper.has_online_ab
    assert get_adapter("engram").paper.code_url == "https://github.com/deepseek-ai/Engram"
    assert get_adapter("gaugequant").paper.code_url == "https://github.com/MPedraBento/gauge-quant"
    assert get_adapter("sasrec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("hstu").paper.arxiv_id == "2402.17152"
    assert get_adapter("deepfm").paper.selection_exception
    assert get_adapter("youtube-dnn").paper.selection_exception
    assert get_adapter("esmm").paper.selection_exception
    assert get_adapter("mmoe").paper.selection_exception
    assert get_adapter("ple").paper.selection_exception
    assert get_adapter("tiger").paper.arxiv_id == "2305.05065"
    assert get_adapter("pinfm").paper.arxiv_id == "2507.12704"
    assert get_adapter("transact-v2").paper.arxiv_id == "2506.02267"
    assert get_adapter("m6rec").paper.has_online_ab
    assert get_adapter("onerec-v2").paper.has_online_ab
    assert get_adapter("kar").paper.has_online_ab
    assert get_adapter("bahe").paper.has_online_ab
    assert get_adapter("beque").paper.has_online_ab
    assert get_adapter("genrank").paper.has_online_ab
    assert get_adapter("pinrec").paper.has_online_ab
    assert get_adapter("learn").paper.has_online_ab
    assert get_adapter("notellm").paper.has_online_ab
    assert get_adapter("univa").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("univa").paper.has_online_ab
    assert get_adapter("pinterest-ads-llm").paper.has_online_ab
    assert get_adapter("lwgr").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("sigma").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("s-grec").fidelity is ReproductionFidelity.FULL_PIPELINE
    assert get_adapter("s-grec").paper.has_online_ab
    assert get_adapter("nontp").paper.has_online_ab
    assert get_adapter("akt-rec").paper.has_online_ab
    assert get_adapter("ccformer").paper.has_online_ab
    assert get_adapter("open-web-ufm").paper.has_online_ab
    assert get_adapter("rocs").paper.has_online_ab
    assert get_adapter("wide").paper.code_url
    assert get_adapter("twin-v2").paper.has_online_ab
    assert get_adapter("sim").paper.has_online_ab
    assert get_adapter("crsd").paper.has_online_ab
    assert get_adapter("clip").paper.code_url == "https://github.com/openai/CLIP"
    assert get_adapter("awq").paper.code_url == "https://github.com/mit-han-lab/llm-awq"


def test_each_result_gets_an_isolated_artifact_directory(tmp_path):
    adapter = get_adapter("sis")
    result = {
        "paper": adapter.paper.to_dict(),
        "dataset": "fixture",
        "baseline": {
            "method": "is",
            "weight_variance": 1.0,
            "mean_abs_log_ratio": 1.0,
            "effective_sample_size": 1.0,
            "acceptance_rate": 0.0,
        },
        "method": {
            "method": "sis",
            "weight_variance": 0.5,
            "mean_abs_log_ratio": 0.5,
            "effective_sample_size": 2.0,
            "acceptance_rate": 0.5,
        },
        "variance_reduction_percent": 50.0,
    }
    report = write_reproduction_result(adapter, result, tmp_path, "fixed-run")
    assert report == tmp_path / "2607.04728-sis" / "fixed-run" / "report.md"
    assert json.loads((report.parent / "result.json").read_text())["dataset"] == "fixture"
    payload = json.loads((report.parent / "result.json").read_text())
    assert payload["reproduction_fidelity"]["level"] == "core_mechanism"
    assert "核心机制复现" in report.read_text()
