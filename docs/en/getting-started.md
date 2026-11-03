# Local documentation preview and deployment

<!-- source-sha256: 71f1c3cdf23db63ab9edbb877f08ee235eb98a529ad73e9030bb39635ebfb099 -->

[简体中文](../getting-started.md) · [Project installation and demos](setup.md)

## Start the documentation site

```bash
python3 -m venv .venv-docs
.venv-docs/bin/pip install -r requirements-docs.txt
.venv-docs/bin/mkdocs serve
```

Open `http://127.0.0.1:8000` to preview the site. Pages reload automatically when you edit Markdown.

## Strict build

```bash
.venv-docs/bin/mkdocs build --strict
```

Strict mode fails the build for missing pages, configuration errors, and incompatible extensions. A separate test checks math delimiters and braces:

```bash
PYTHONPATH=src .venv/bin/pytest -q tests/test_docs_math.py
```

## GitHub Pages

After a merge into `main`, GitHub Actions builds and publishes the site at `https://daiwk.github.io/auto-research/`. Pull requests run the strict build but do not publish. To set up Pages for the first time, select **GitHub Actions** under **Settings → Pages → Build and deployment**.

## Add paper documentation

Keep the paper write-up in `docs/reproductions/<arxiv-id>-<adapter>/README.md`. Markdown that passes the strict build and math tests is published directly; there is no separate copy of the Chinese page to maintain for the website. Maintain the English companion according to the [bilingual contribution guide](contributing.md).

## Learning cards

The Learning Cards section is organized as topic → subtopic → individual question. A paper needs at least one question at each of four levels: fundamentals, core mechanism, method comparison, and implementation details. You can continue adding questions. Read the question first, then expand the answer and teaching example. The subtopic question banks, [all paper questions (Chinese)](../learning/all.md), and [recent additions (Chinese)](../learning/recent.md) use the same source, so new content appears in all three. [Topic deep dives (Chinese)](../learning/deep-dives/index.md) use the same taxonomy. Each card compares representative papers, explains their trade-offs, and contains at least three cross-paper questions.

Topics are collapsed by default in the sidebar and expand when you enter the current subtopic. Questions appear 12 at a time. You can combine topic, subtopic, level, and keyword filters; the filters are stored in the URL. Click a paper's title to see all its questions in the four-level order. A question deep link clears conflicting filters and expands the answer. The original topic introductions and reading paths remain available in optional expandable sections. Use the implementation write-up to check experimental validation and what was not reproduced.

When adding a paper, update the shared manifest, the write-up, its classification in `docs/learning/topics/*.json`, and its questions in `docs/learning/questions/*.json`. Questions must focus on defining mechanisms, with direct answers and concrete teaching examples. Do not pad the bank with generic questions such as “What problem does this solve?” followed by abstract excerpts. `source_sections` must name actual headings in the paper's README. Keep question `id` values stable and set `added` to the true date of addition. New questions for old papers appear in recent additions; editing an answer does not change its original date. Preview unclassified entries in the [inbox (Chinese)](../learning/inbox.md). Before publication, finish the classification, per-paper questions, and corresponding deep-dive updates.

In the question JSON, each entry must have a `level` of `basics`, `mechanism`, `comparison`, or `implementation`. The following example shows the fields for one question; in practice, cover all four levels for each paper before adding more at the same level. The Chinese `source_sections` values illustrate the actual heading names the generator checks. The example asks why a continuous gate can be trained even when the index of a selected block is not differentiable; the answer should explain the continuous gradient path and the remaining limits of discrete selection, with a teaching example rather than a claimed experiment.

```json
{"schema_version": 1, "papers": {"recommendation:example": {"questions": [{
  "id": "mechanism", "level": "mechanism", "question": "选中块的索引不可导，连续gate为什么还能被训练？",
  "answer": "解释梯度经过的连续路径，以及离散选择仍然存在的限制。",
  "example": "给出帮助理解的教学场景，不冒充论文实验。",
  "source_sections": ["背景与主要改动", "核心公式"], "added": "2026-10-27"
}]}}}
```

The hand-authored sources for deep dives are in `docs/learning/deep-dives/*.json`. Each card must include at least three representative papers, two sections of analysis, and three cross-paper questions. Comparison rows refer to actual headings in each paper's README. `reviewed_papers` is a snapshot of the papers whose abstracts and classifications were checked for the topic, not a claim that every paper received an equally thorough reading. The complete catalog and the selection for focused comparison are shown separately.

When adding a paper, check whether it introduces a new approach or changes an existing trade-off. Revise the comparison, analysis, or questions when necessary. Append an entry to `updates` with the date, the papers involved, and an explanation of what changed, then update `reviewed_papers` and `updated`. If the conclusion still holds, explain how the new paper adds to the existing distinction. Keep old question IDs and historical updates; adding a paper to a list is not sufficient. A missing card, member, or update entry, or an inconsistent date, blocks publication. The date of the corresponding update cannot be earlier than the date the paper first joined the question bank. Each update's `source_revisions` records SHA-256 hashes for the relevant paper READMEs. When an old write-up or its implementation limits change, review it and append an update rather than reusing a stale snapshot.

After reviewing the topic, inspect the current source fingerprints without writing any files. Put the keys and values for the papers involved in the new update's `source_revisions` and preserve the fingerprints on historical entries:

```bash
python scripts/generate_learning_cards.py --show-deep-dive-sources recommendation/history-ranking-backbones
```

Then generate the pages and check them:

```bash
python scripts/generate_learning_cards.py --require-questions --require-deep-dives
python scripts/generate_learning_cards.py --check --require-questions --require-deep-dives
```

The first command updates the all-questions page, recent additions, subtopic banks, and designated sections of the overview. The second verifies that the generated pages match their sources. Missing or invalid levels, duplicate question IDs, invalid source headings, empty answers or examples, and duplicate paper assignments all cause failures. Edit the question and topic JSON, not the generated pages. Comparisons should explain real differences in mechanisms or assumptions; do not invent a performance ranking without measurements. Implementation questions should state key requirements of the original method and the scope of local evidence. The generator does not synthesize generic questions to pass the checks.

Local MkDocs and CI use the same generator, enforcing complete question and deep-dive coverage. Collapsible navigation comes from the topic JSON; individual questions are not added to the sidebar. Readers use the learning content on the site itself, so blog drafts are no longer part of the publishing workflow.
