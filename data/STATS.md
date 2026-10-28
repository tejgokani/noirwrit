# Corpus stats

| Set | Books | Words | Tokens | Paragraphs passing sanity filter |
|---|---|---|---|---|
| general | 185 | 16,158,324 | 21,456,416 | 99.74% |
| crime | 76 | 6,416,901 | 8,513,410 | 99.81% |
| noir | 2 | 242,017 | 336,019 | 99.71% |
| **total** | 263 | 22,817,242 | 30,305,845 | 99.76% |

The sanity filter is in `noirwrit/corpus/clean.py` (`paragraph_passes`): mostly letters, at least 97% ASCII, and a plausible English stopword rate.
Books under 97% are dropped whole. In kept books, failing paragraphs are removed, so the training text itself is 100% passing; the column shows the rate before that step.
