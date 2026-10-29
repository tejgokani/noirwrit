# Quality gates

Model: `noirwrit-base-q8_0.gguf`. Run 2026-10-29 on this Mac.

## 12-chapter book

"Dead Man's Photograph": 18,931 words written in 150 s.

| Page size | Pages | TOC entries | TOC page numbers match chapter openers | Pages with page numbers | Pages with running header | Glyphs outside the page |
|---|---|---|---|---|---|---|
| A4 (8.27 x 11.69 in) | 39 | 12 | yes | 36 | 24 | 0 |
| Letter (8.5 x 11.0 in) | 39 | 12 | yes | 36 | 24 | 0 |
| A5 (5.83 x 8.27 in) | 63 | 12 | yes | 60 | 48 | 0 |
| 6x9 (6.0 x 9.0 in) | 60 | 12 | yes | 57 | 45 | 0 |

EPUB: epubcheck passed (Messages: 0 fatals / 0 errors / 0 warnings / 0 infos).

## Novelty

Two stories from the same prompt (a fog-bound port city, victim a pawnbroker): whole-chapter cosine 0.61, closest-passage cosine 0.51 (threshold 0.85), 5-gram overlap 2.2%, embedder `hashing`. Pass.

**Overall: all gates pass.**

PDFs and the EPUB are in `artifacts/gates/` (not committed).
