from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from ..latest_20260809_common import reproduce_llm_ts_prior, render_latest

ADAPTER = register(ReproductionAdapter(
    key="llm-ts-prior", paper=PaperMetadata(
        arxiv_id="2608.03382", title="LLM-Derived Priors for Thompson Sampling in Cold-Start Comment Recommendation",
        url="https://arxiv.org/abs/2608.03382", track="recommendation",
        organization="NAVER WEBTOON", published="2026-08-04",
        topics=("llm-recommendation", "bandit", "cold-start", "comment-ranking"),
        online_ab=(
            OnlineABEvidence("WEBTOON comment recommendation", "Gender-prior overall CTR", 1.48, "four-week A/B/C; about 595K users per arm", significance="p=0.144, not significant"),
            OnlineABEvidence("WEBTOON 10-49 exposure bucket", "Gender-prior CTR", 9.51, "A/B/C cold-start subgroup", significance="p<0.001"),
            OnlineABEvidence("WEBTOON overall", "Content-prior CTR", -5.68, "four-week A/B/C", significance="p<0.001"),
        )), run=reproduce_llm_ts_prior, render=render_latest,
    fidelity=ReproductionFidelity.CORE_MECHANISM,
    omitted_core_components=("production prompts and service calibration", "WEBTOON private comment inventory"),
))
