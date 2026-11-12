# OpenMLE-fast task

Task ID: `bank-marketing-dataset@1`

Native metric: `BankMarketingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2618 bytes)
- `data/sample_submission.csv` (90435 bytes); columns: ["id", "y"]
- `data/test.csv` (733346 bytes); columns: ["id", "age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month", "campaign", "pdays", "previous", "poutcome"]
- `data/train.csv` (2993584 bytes); columns: ["id", "age", "job", "marital", "education", "default", "balance", "housing", "loan", "contact", "day", "month", "campaign", "pdays", "previous", "poutcome", "y"]

## Public description

```
description.txt (34 lines)
sample_submission.csv (9044 lines)
test.csv (9044 lines)
train.csv (36169 lines)```

-> sample_submission.csv has 9043 rows and 2 columns.
Here is some information about the columns:
id (int64) has range: 36169.00 - 45211.00, 0 nan values
y (float64) has 1 unique values: [0.5]

-> test.csv has 9043 rows and 16 columns.
Here is some information about the columns:
age (int64) has range: 18.00 - 93.00, 0 nan values
balance (int64) has range: -3058.00 - 98417.00, 0 nan values
campaign (int64) has range: 1.00 - 55.00, 0 nan values
contact (object) has 3 unique values: ['unknown', 'cellular', 'telephone']
day (int64) has range: 1.00 - 31.00, 0 nan values
default (object) has 2 unique values: ['no', 'yes']
education (object) has 4 unique values: ['primary', 'secondary', 'tertiary', 'unknown']
housing (object) has 2 unique values: ['yes', 'no']
id (int64) has range: 36169.00 - 45211.00, 0 nan values
job (object) has 12 unique values. Some example values: ['management', 'blue-collar', 'technician', 'admin.']
loan (object) has 2 unique values: ['yes', 'no']
marital (object) has 3 unique values: ['married', 'single', 'divorced']
month (object) has 12 unique values. Some example values: ['may', 'jul', 'aug', 'jun']
pdays (int64) has range: -1.00 - 838.00, 0 nan values
poutcome (object) has 4 unique values: ['unknown', 'success', 'failure', 'other']
previous (int64) has range: 0.00 - 37.00, 0 nan values

-> train.csv has 36168 rows and 17 columns.
Here is some information about the columns:
age (int64) has range: 18.00 - 95.00, 0 nan values
balance (int64) has range: -8019.00 - 102127.00, 0 nan values
campaign (int64) has range: 1.00 - 63.00, 0 nan values
contact (object) has 3 unique values: ['telephone', 'cellular', 'unknown']
day (int64) has range: 1.00 - 31.00, 0 nan values
default (object) has 2 unique values: ['no', 'yes']
education (object) has 4 unique values: ['secondary', 'tertiary', 'primary', 'unknown']
housing (object) has 2 unique values: ['no', 'yes']
id (int64) has range: 1.00 - 36168.00, 0 nan values
job (object) has 12 unique values. Some example values: ['blue-collar', 'management', 'technician', 'admin.']
loan (object) has 2 unique values: ['no', 'yes']
marital (object) has 3 unique values: ['divorced', 'single', 'married']
month (object) has 12 unique values. Some example values: ['may', 'jul', 'aug', 'jun']
pdays (int64) has range: -1.00 - 871.00, 0 nan values
poutcome (object) has 4 unique values: ['unknown', 'failure', 'other', 'success']
previous (int64) has range: 0.00 - 275.00, 0 nan values
y (int64) has 2 unique values: [0, 1]
