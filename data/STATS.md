# Corpus stats

| Set | Books | Words | Tokens | Paragraphs passing sanity filter |
|---|---|---|---|---|
| general | 341 | 30,275,577 | 40,811,041 | 99.76% |
| crime | 1,429 | 101,376,894 | 138,436,148 | 99.71% |
| noir | 58 | 3,004,949 | 4,206,957 | 99.52% |
| **total** | 1,828 | 134,657,420 | 183,454,146 | 99.71% |

The sanity filter is in `noirwrit/corpus/clean.py` (`paragraph_passes`): mostly letters, at least 97% ASCII, and a plausible English stopword rate.
Books under 97% are dropped whole. In kept books, failing paragraphs are removed, so the training text itself is 100% passing; the column shows the rate before that step.
