# OpenMLE-fast task

Task ID: `movielens-100k-dataset@1`

Native metric: `MovieLensRatingPredictionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2994 bytes)
- `data/items.csv` (143763 bytes); columns: ["item_id", "title", "release_date", "release_year", "genre_unknown", "genre_Action", "genre_Adventure", "genre_Animation", "genre_Children_s", "genre_Comedy", "genre_Crime", "genre_Documentary", "genre_Drama", "genre_Fantasy", "genre_Film_Noir", "genre_Horror", "genre_Musical", "genre_Mystery", "genre_Romance", "genre_Sci_Fi", "genre_Thriller", "genre_War", "genre_Western"]
- `data/sample_submission.csv` (320015 bytes); columns: ["row_id", "rating"]
- `data/test.csv` (495959 bytes); columns: ["row_id", "user_id", "item_id", "timestamp"]
- `data/train.csv` (2292179 bytes); columns: ["row_id", "user_id", "item_id", "rating", "timestamp"]
- `data/users.csv` (23606 bytes); columns: ["user_id", "age", "gender", "occupation", "zip"]

## Public description

```
description.txt (40 lines)
items.csv (1683 lines)
sample_submission.csv (20001 lines)
test.csv (20001 lines)
train.csv (80001 lines)
users.csv (944 lines)```

-> items.csv has 1682 rows and 23 columns.
Here is some information about the columns:
genre_Action (int64) has 2 unique values: [0, 1]
genre_Adventure (int64) has 2 unique values: [0, 1]
genre_Animation (int64) has 2 unique values: [1, 0]
genre_Children_s (int64) has 2 unique values: [1, 0]
genre_Comedy (int64) has 2 unique values: [1, 0]
genre_Crime (int64) has 2 unique values: [0, 1]
genre_Documentary (int64) has 2 unique values: [0, 1]
genre_Drama (int64) has 2 unique values: [0, 1]
genre_Fantasy (int64) has 2 unique values: [0, 1]
genre_Film_Noir (int64) has 2 unique values: [0, 1]
genre_Horror (int64) has 2 unique values: [0, 1]
genre_Musical (int64) has 2 unique values: [0, 1]
genre_Mystery (int64) has 2 unique values: [0, 1]
genre_Romance (int64) has 2 unique values: [0, 1]
genre_Sci_Fi (int64) has 2 unique values: [0, 1]
genre_Thriller (int64) has 2 unique values: [0, 1]
genre_War (int64) has 2 unique values: [0, 1]
genre_Western (int64) has 2 unique values: [0, 1]
genre_unknown (int64) has 2 unique values: [0, 1]
item_id (int64) has range: 1.00 - 1682.00, 0 nan values
release_date (object) has 240 unique values. Some example values: ['01-Jan-1995', '01-Jan-1994', '01-Jan-1993', '01-Jan-1997']
release_year (float64) has range: 1922.00 - 1998.00, 1 nan values
title (object) has 1664 unique values. Some example values: ['Kull the Conqueror (1997)', 'Body Snatchers (1993)', 'Hurricane Streets (1998)', 'Chasing Amy (1997)']

-> sample_submission.csv has 20000 rows and 2 columns.
Here is some information about the columns:
rating (float64) has range: 1.00 - 5.00, 0 nan values
row_id (int64) has range: 80000.00 - 99999.00, 0 nan values

-> test.csv has 20000 rows and 4 columns.
Here is some information about the columns:
item_id (int64) has range: 1.00 - 1680.00, 0 nan values
row_id (int64) has range: 80000.00 - 99999.00, 0 nan values
timestamp (int64) has range: 889237269.00 - 893286638.00, 0 nan values
user_id (int64) has range: 1.00 - 942.00, 0 nan values

-> train.csv has 80000 rows and 5 columns.
Here is some information about the columns:
item_id (int64) has range: 1.00 - 1682.00, 0 nan values
rating (float64) has 5 unique values: [4.0, 3.0, 5.0, 2.0, 1.0]
row_id (int64) has range: 0.00 - 79999.00, 0 nan values
timestamp (int64) has range: 874724710.00 - 889237269.00, 0 nan values
user_id (int64) has range: 1.00 - 943.00, 0 nan values

-> users.csv has 943 rows and 5 columns.
Here is some information about the columns:
age (int64) has range: 7.00 - 73.00, 0 nan values
gender (object) has 2 unique values: ['M', 'F']
occupation (object) has 21 unique values. Some example values: ['student', 'other', 'educator', 'administrator']
user_id (int64) has range: 1.00 - 943.00, 0 nan values
zip (object) has 795 unique values. Some example values: ['55414', '55105', '20009', '10003']
