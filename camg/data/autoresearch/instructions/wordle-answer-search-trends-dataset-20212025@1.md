# OpenMLE-fast task

Task ID: `wordle-answer-search-trends-dataset-20212025@1`

Native metric: `WordleSearchUpliftMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1750 bytes)
- `data/sample_submission.csv` (6806 bytes); columns: ["id", "uplift_global"]
- `data/test.csv` (15008 bytes); columns: ["id", "date", "game", "word", "wordfreq_commonality", "subtlex_commonality", "trend_avg_200_global", "trend_avg_200_language"]
- `data/train.csv` (72184 bytes); columns: ["id", "date", "game", "word", "wordfreq_commonality", "subtlex_commonality", "trend_avg_200_global", "trend_avg_200_language", "uplift_global"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (295 lines)
test.csv (295 lines)
train.csv (1174 lines)```

-> sample_submission.csv has 294 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 1174.00 - 1467.00, 0 nan values
uplift_global (float64) has range: -87.82 - 120.00, 0 nan values

-> test.csv has 294 rows and 8 columns.
Here is some information about the columns:
date (object) has 294 unique values. Some example values: ['2025-06-24', '2024-09-04', '2024-09-05', '2024-09-06']
game (int64) has range: 1173.00 - 1466.00, 0 nan values
id (int64) has range: 1174.00 - 1467.00, 0 nan values
subtlex_commonality (float64) has range: 0.00 - 0.72, 0 nan values
trend_avg_200_global (float64) has range: 0.04 - 88.23, 0 nan values
trend_avg_200_language (float64) has range: 0.00 - 81.70, 1 nan values
word (object) has 294 unique values. Some example values: ['elite', 'stern', 'widen', 'rerun']
wordfreq_commonality (float64) has range: 0.00 - 0.02, 0 nan values

-> train.csv has 1173 rows and 9 columns.
Here is some information about the columns:
date (object) has 1173 unique values. Some example values: ['2024-09-03', '2021-06-19', '2021-06-20', '2021-06-21']
game (int64) has range: 0.00 - 1172.00, 0 nan values
id (int64) has range: 1.00 - 1173.00, 0 nan values
subtlex_commonality (float64) has range: 0.00 - 0.79, 0 nan values
trend_avg_200_global (float64) has range: 0.02 - 92.02, 0 nan values
trend_avg_200_language (float64) has range: 0.00 - 86.22, 8 nan values
uplift_global (float64) has range: -29.12 - 99.98, 0 nan values
word (object) has 1173 unique values. Some example values: ['faint', 'cigar', 'rebut', 'sissy']
wordfreq_commonality (float64) has range: 0.00 - 0.05, 0 nan values
