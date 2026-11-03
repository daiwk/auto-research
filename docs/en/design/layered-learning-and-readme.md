# Layered questions, site tour, and project entry points

<!-- source-sha256: c55e8f23a5422cfa0ce847af5b651ef54cde44432981e55359b535246247fb2e -->

[简体中文](../../design/layered-learning-and-readme.md)

This work has three complete deliverables. A subset of papers or a sample tour does not constitute full completion.

## Layered questions

The baseline was 1,034 paper/resource entries with 1,042 questions, including 1,030 entries with only one question. Add all four levels to each entry: `basics`, `mechanism`, `comparison`, and `implementation`. Every level needs at least one question; each question keeps a direct answer, teaching example, and actual source sections. Preserve IDs and dates. Mechanism comparisons do not invent experimental winners, and implementation questions distinguish paper methods from local evidence.

Show levels in reading order with filters that can combine theme, subtopic, paper, and keywords. A question deep link clears conflicting filters and opens the answer. Global, recent, and subtopic lists use one source. Publication requires all four distinct levels; four same-level questions or automatic summaries cannot pass.

## README

The main README retains project scope, live CI, site capabilities, a tour, minimal installation and commands, navigation, and contribution links. Split installation/data/platform examples, evolution and external experiments, and historical delivery into `readme_*.md` files, preserving commands and evidence links. The mirror script synchronizes these sources, site links, and media paths. CI, commit history, and delivery records show maintenance status; do not invent cadences or roadmap promises.

## Tour

Record actual site operation in at most 60 seconds. Retain MP4 and embed animated WebP in the root README. Cover paper search, themes, four question levels, answers/examples/sources, recent additions, and the public experiment dashboard. Use the final build's footage. Captions describe actual interactions without staging fake clicks. Check duration, frame count, clarity, size, and media links in GitHub and on the site.

## Verification and delivery

- Check complete four-level coverage, unchanged old IDs/dates, valid source headings, and duplicate/template content.
- Run targeted pytest, generation consistency, README sync, and strict site build. Check filters, deep links, and mobile layout in a browser.
- Verify split README links and actual WebP playback and duration.
- Publish only after applicable CI; verify deployed counts, assets, and interactions, retain receipts, and clean temporary build and encoding outputs.
