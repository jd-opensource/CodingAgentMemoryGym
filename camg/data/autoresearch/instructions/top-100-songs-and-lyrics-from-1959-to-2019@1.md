# OpenMLE-fast task

Task ID: `top-100-songs-and-lyrics-from-1959-to-2019@1`

Native metric: `LyricsToYearClassificationMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (657 bytes)
- `data/sample_submission.csv` (34433 bytes); columns: ["id", "year"]
- `data/test.csv` (9572606 bytes); columns: ["id", "lyrics", "title", "artist", "album", "writers", "featured_artists", "verbs", "nouns", "adverbs", "corpus", "word_counts", "unique_word_counts"]
- `data/train.csv` (21249949 bytes); columns: ["id", "lyrics", "title", "artist", "album", "writers", "featured_artists", "verbs", "nouns", "adverbs", "corpus", "word_counts", "unique_word_counts", "year"]

## Public description

Competition: Lyrics-to-Year Classification (1959–2019)

Problem statement
- Given the lyrics and limited metadata of a song that ranked in the US Top 100, predict the year (1959–2019).

Files
- train.csv: training set with input features and ground-truth label.
- test.csv: test set with the same input features but no labels.
- sample_submission.csv: a valid example submission with randomized labels.

Submission format
- CSV file with columns: id, year
- id must match exactly the ids in test.csv (order is irrelevant).
- year must be an integer within [1959, 2019].

Evaluation metric
- Macro F1 score over the year classes present in the test set.
