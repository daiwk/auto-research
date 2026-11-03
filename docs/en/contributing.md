# Keeping Chinese and English documentation in sync

[English home](index.md) · [Paper catalog](papers/index.md)

## What to update in one pull request

- New catalog papers, including review-only entries, and edits to existing Chinese paper write-ups need a companion English `README-en.md` beside `README.md`.
- Keep the paper information, method, reported results, local implementation and evaluation limits in both languages. Reuse the same images and evidence files. Explicitly distinguish paper results from local diagnostics and high-cost experiments that were not reproduced.
- If you edit the project README, site home, or installation guide, review its corresponding English page as well:

  | Chinese source | English page |
  | --- | --- |
  | Root `README.md` | Root `README.en.md` |
  | `docs/index.md` | `docs/en/index.md` |
  | Root `readme_setup.md` | `docs/en/setup.md` |

## Mark a translation as reviewed

Put a single `<!-- source-sha256: <64 lowercase hexadecimal characters> -->` comment near the top of the English page. After reviewing the English against the final Chinese text, obtain the digest of the **Chinese source file** with `shasum -a 256 path/to/README.md` (or `sha256sum` on Linux). Review even changes that do not alter the English meaning, such as a typo correction, before refreshing the digest. The digest detects source drift; it does not verify translation quality.

Link back to the Chinese page (for papers, `[简体中文](README.md)`). The site automatically links Chinese paper pages to their English siblings. Older pages without English can be translated incrementally; they are marked as untranslated in the catalog until a companion is added.

## Regenerate and check

Run the existing research manifest generator first if paper metadata changed, then:

```bash
python scripts/english_docs.py --write
python scripts/english_docs.py
mkdocs build --strict
```

To reproduce the pull-request gate locally, pass the full base commit SHA to `python scripts/english_docs.py --base <base-sha>`. The gate checks all existing pairs for drift and requires English for newly added catalog entries or edited Chinese paper pages. The English catalog is generated from the same manifest as the Chinese site; do not edit its rows by hand.

This workflow covers the public entry pages and paper write-ups. Existing learning cards, audit records and other specialist guides may still be Chinese-only.
