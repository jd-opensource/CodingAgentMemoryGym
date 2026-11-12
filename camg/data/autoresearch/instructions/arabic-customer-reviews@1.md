# OpenMLE-fast task

Task ID: `arabic-customer-reviews@1`

Native metric: `ArabicCustomerReviewsMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1260 bytes)
- `data/sample_submission.csv` (246980 bytes); columns: ["review_id", "rating"]
- `data/test.csv` (1074337 bytes); columns: ["review_id", "review_description"]
- `data/train.csv` (3593971 bytes); columns: ["review_id", "review_description", "rating"]

## Public description

```
description.txt (32 lines)
sample_submission.csv (10013 lines)
test.csv (10296 lines)
train.csv (30427 lines)```

-> sample_submission.csv has 10012 rows and 2 columns.
Here is some information about the columns:
rating (object) has 3 unique values: ['positive', 'negative', 'neutral']
review_id (object) has 10012 unique values. Some example values: ['R59fd412da50016', 'R71e8d58aa60001', 'R99b42a3a030001', 'Re8b74b36be0001']

-> test.csv has 10012 rows and 2 columns.
Here is some information about the columns:
review_description (object) has 9006 unique values. Some example values: ['ممتاز', 'رائع', 'جيد جدا', 'جيد']
review_id (object) has 10012 unique values. Some example values: ['R59fd412da50016', 'R71e8d58aa60001', 'R99b42a3a030001', 'Re8b74b36be0001']

-> train.csv has 30034 rows and 3 columns.
Here is some information about the columns:
rating (object) has 3 unique values: ['positive', 'negative', 'neutral']
review_description (object) has 29997 unique values. Some example values: ['ممتاز جدا جدا جدا جدا جدا', 'جيد جيدا', 'كفو', 'ابو كلب']
review_id (object) has 30034 unique values. Some example values: ['R9b515a29080001', 'R58ff352a7f0001', 'Rc7e8ab4be70001', 'R8c7c2c70160001']
