# OpenMLE-fast task

Task ID: `hr-jobs-emails@1`

Native metric: `LocalPartEmailSenderTypeMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (970 bytes)
- `data/sample_submission.csv` (299501 bytes); columns: ["id", "label"]
- `data/test.csv` (254376 bytes); columns: ["id", "local_part"]
- `data/train.csv` (1822713 bytes); columns: ["id", "local_part", "label"]

## Public description

```
description.txt (48 lines)
sample_submission.csv (15880 lines)
test.csv (15880 lines)
train.csv (63516 lines)```

-> sample_submission.csv has 15879 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 7.00 - 79393.00, 0 nan values
label (object) has 5 unique values: ['isp_hosted', 'free_personal', 'corporate_org', 'education', 'government']

-> test.csv has 15879 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 7.00 - 79393.00, 0 nan values
local_part (object) has 12888 unique values. Some example values: ['mail', 'ali', 'abudhabi', 'ceo']

-> train.csv has 63515 rows and 3 columns.
Here is some information about the columns:
id (int64) has range: 0.00 - 79391.00, 0 nan values
label (object) has 5 unique values: ['free_personal', 'corporate_org', 'isp_hosted', 'education', 'government']
local_part (object) has 45787 unique values. Some example values: ['info', 'hr', 'sales', 'jobs']
