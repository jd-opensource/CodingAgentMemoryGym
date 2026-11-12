# OpenMLE-fast task

Task ID: `sachin-odi@1`

Native metric: `SachinODIScoreBandMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1512 bytes)
- `data/sample_submission.csv` (1114 bytes); columns: ["id", "score_band"]
- `data/test.csv` (3045 bytes); columns: ["id", "Opp", "Ground", "Date", "Inns"]
- `data/train.csv` (10911 bytes); columns: ["Opp", "Ground", "Date", "Inns", "score_band"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (91 lines)
test.csv (91 lines)
train.csv (363 lines)```

-> sample_submission.csv has 90 rows and 2 columns.
Here is some information about the columns:
id (object) has 90 unique values. Some example values: ['id_000000', 'id_000001', 'id_000002', 'id_000003']
score_band (object) has 5 unique values: ['<10', '25-49', '10-24', '100+', '50-99']

-> test.csv has 90 rows and 5 columns.
Here is some information about the columns:
Date (object) has 90 unique values. Some example values: ['26 Nov 2006', '29 Nov 2006', '3 Dec 2006', '21 Jan 2007']
Ground (object) has 46 unique values. Some example values: ['Nagpur', 'Brisbane', 'Colombo (RPS)', 'Dhaka']
Inns (int64) has 2 unique values: [2, 1]
Opp (object) has 11 unique values. Some example values: ['Australia', 'Sri Lanka', 'South Africa', 'England']
id (object) has 90 unique values. Some example values: ['id_000000', 'id_000001', 'id_000002', 'id_000003']

-> train.csv has 362 rows and 5 columns.
Here is some information about the columns:
Date (object) has 362 unique values. Some example values: ['22 Nov 2006', '18 Dec 1989', '1 Mar 1990', '6 Mar 1990']
Ground (object) has 86 unique values. Some example values: ['Sharjah', 'Colombo (RPS)', 'Toronto', 'Dhaka']
Inns (int64) has 2 unique values: [2, 1]
Opp (object) has 13 unique values. Some example values: ['Pakistan', 'Sri Lanka', 'Australia', 'South Africa']
score_band (object) has 5 unique values: ['<10', '25-49', '10-24', '50-99', '100+']
