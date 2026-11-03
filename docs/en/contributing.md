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

In each English paper write-up, link back to the adjacent `README.md` with the label “简体中文”. The site automatically links Chinese paper pages to their English siblings. For a non-paper page, link back to the corresponding Chinese source.

Use the repository's portable math delimiters in both languages: single dollar signs for inline math and double dollar signs on their own lines for display math.

## Regenerate and check

Run the existing research manifest generator first if paper metadata changed, then:

```bash
python scripts/english_docs.py --write
python scripts/english_docs.py
mkdocs build --strict
```

To reproduce the pull-request gate locally, pass the full base commit SHA to `python scripts/english_docs.py --base <base-sha>`. The gate checks all existing pairs for drift and requires English for newly added catalog entries or edited Chinese paper pages. The English catalog is generated from the same manifest as the Chinese site; do not edit its rows by hand.

New non-paper site pages also need English in the same pull request. Place the English counterpart under `docs/en/` at the same path relative to the documentation root (for example, `docs/architecture.md` pairs with `docs/en/architecture.md`). Existing pairs are checked for drift and the site adds a link from the Chinese page. The installation guide is the existing exception: `readme_setup.md` pairs with `docs/en/setup.md`.

The [coverage report](coverage.md) tracks the entire Chinese site, including learning and audit pages. A catalog link to a Chinese-only paper does not count as a translation. The full-site check is `python scripts/english_docs.py --require-complete`; use `--list-untranslated` to diagnose missing counterparts.

For generated collections, translate the underlying text fields rather than editing every repeated output. Keep source IDs, evidence files, formulas, and experiment values shared. Also check interactive labels (such as search and pagination) in the rendered English page.

The grouped English catalogs use the canonical classifications and reviewed English write-ups. Learning questions, topic introductions, self-tests, and cross-paper deep dives use reviewed overlays under `docs/en/learning/translations/`. Each overlay entry uses a stable source unit ID, a source fingerprint, and the exact translated prose fields. Review affected text against the source before updating the fingerprint. The learning generator rejects incomplete, duplicate, or stale overlays.

```bash
python scripts/generate_learning_cards.py --require-questions --require-deep-dives
python scripts/english_docs.py --write --write-browse --write-learning
python scripts/english_docs.py
```
