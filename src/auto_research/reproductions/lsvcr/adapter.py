from ..base import OnlineABEvidence, PaperMetadata, ReproductionAdapter, ReproductionFidelity
from ..registry import register
from .experiment import reproduce_lsvcr
from .report import render_report


register(ReproductionAdapter(
    key="lsvcr",
    paper=PaperMetadata(
        arxiv_id="2403.13574", title="A Large Language Model Enhanced Sequential Recommender for Joint Video and Comment Recommendation",
        url="https://arxiv.org/abs/2403.13574", code_url="https://github.com/RUCAIBox/LSVCR", track="recommendation",
        organization="Kuaishou", published="2024-03", topics=("LLM recommendation", "comment recommendation", "preference alignment"),
        online_ab=(
            OnlineABEvidence("Kuaishou video", "Watch Time", 0.3649, "20K users, 2 weeks"),
            OnlineABEvidence("Kuaishou comments", "Watch Time", 4.1264, "20K users, 2 weeks"),
        ),
    ), run=reproduce_lsvcr, render=render_report,
    fidelity=ReproductionFidelity.FULL_PIPELINE,
    omitted_core_components=("ChatGLM3 scale", "Kuaishou private video/comment logs"),
))
