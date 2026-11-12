# OpenMLE-fast task

Task ID: `customer-feedback-and-satisfaction@1`

Native metric: `CustomerSatisfactionMAEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1564 bytes)
- `data/sample_submission.csv` (82388 bytes); columns: ["CustomerID", "SatisfactionScore"]
- `data/test.csv` (257552 bytes); columns: ["CustomerID", "Age", "Gender", "Country", "Income", "ProductQuality", "ServiceQuality", "PurchaseFrequency"]
- `data/train.csv` (1212486 bytes); columns: ["CustomerID", "Age", "Gender", "Country", "Income", "ProductQuality", "ServiceQuality", "PurchaseFrequency", "SatisfactionScore"]

## Public description

```
description.txt (54 lines)
sample_submission.csv (7690 lines)
test.csv (7690 lines)
train.csv (30756 lines)```

-> sample_submission.csv has 7689 rows and 2 columns.
Here is some information about the columns:
CustomerID (int64) has range: 5.00 - 38440.00, 0 nan values
SatisfactionScore (float64) has 1 unique values: [50.0]

-> test.csv has 7689 rows and 8 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 69.00, 0 nan values
Country (object) has 5 unique values: ['UK', 'Germany', 'Canada', 'USA', 'France']
CustomerID (int64) has range: 5.00 - 38440.00, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Income (int64) has range: 30007.00 - 119990.00, 0 nan values
ProductQuality (int64) has range: 1.00 - 10.00, 0 nan values
PurchaseFrequency (int64) has range: 1.00 - 20.00, 0 nan values
ServiceQuality (int64) has range: 1.00 - 10.00, 0 nan values

-> train.csv has 30755 rows and 9 columns.
Here is some information about the columns:
Age (int64) has range: 18.00 - 69.00, 0 nan values
Country (object) has 5 unique values: ['UK', 'USA', 'France', 'Germany', 'Canada']
CustomerID (int64) has range: 1.00 - 38444.00, 0 nan values
Gender (object) has 2 unique values: ['Male', 'Female']
Income (int64) has range: 30001.00 - 119999.00, 0 nan values
ProductQuality (int64) has range: 1.00 - 10.00, 0 nan values
PurchaseFrequency (int64) has range: 1.00 - 20.00, 0 nan values
SatisfactionScore (float64) has range: 4.28 - 100.00, 0 nan values
ServiceQuality (int64) has range: 1.00 - 10.00, 0 nan values
