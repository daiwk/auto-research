# Continuously maintained topic deep dives

<!-- source-sha256: 352886a8fc241546cb1b019bac9a73e5dd8b35ff75899558a63e5fa6c7de1266 -->

[简体中文](../../design/topic-deep-dives.md)

The two earlier reading essays move out of site navigation. The existing six themes and 31 subtopics each get one deep dive. Paper-by-paper questions remain separate. Deep dives compare mechanisms and trade-offs and ask cross-paper questions.

## Content and navigation

Each card starts from a shared question and compares at least three representative papers. The table gives mechanisms and trade-offs, with actual local README sections and original links. Include at least two analytical sections and three cross-paper questions. Each question has a direct answer, a teaching example, and at least two sources from the topic. Without a common measured protocol, compare mechanisms, assumptions, and applications, not performance. The full topic catalog is collapsed by default and is distinct from the representative comparison.

The sidebar nests deep dives under six themes. The index initially shows six collapsed groups. Question banks and deep dives cross-link, and learning home offers both. Keep Material typography and colors, with two-column topic cards and a comparison table. On mobile, use one column and stack each paper's source, mechanism, and trade-off instead of requiring sideways scrolling.

## Incremental updates

Author content lives in `docs/learning/deep-dives/*.json`. Rendering does not call a model or fabricate summaries and questions. `reviewed_papers` is a snapshot of identities checked for summary and classification and must equal topic membership; it is not a claim of full reading. Append `updates` chronologically, cover affected papers, match the latest date to `updated`, and do not predate a paper's first question.

Each update pins relevant README SHA256s. Changes to earlier sources or implementation limits need review and a new update. For new papers, check whether existing distinctions still hold; adjust comparisons, analysis, or Q&A as needed and record why. Preserve question IDs and history. Generation requires a card for every topic and a corresponding update for each new paper.

## Acceptance

Validate all 31 cards, membership and update coverage, representative papers and source headings, cross-paper question counts, and stable IDs. Test rejection of a new paper without its update and acceptance with a complete update, without writing generated files on failure. Run targeted doc tests, generation checks, and strict build. Verify desktop/mobile navigation, comparison tables, and expanded answers.
