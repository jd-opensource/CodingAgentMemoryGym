# OpenMLE-fast task

Task ID: `online-shoppers-purchasing-intention-dataset@1`

Native metric: `OnlineShoppersPurchasingIntentionMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2921 bytes)
- `data/sample_submission.csv` (97253 bytes); columns: ["SessionID", "Revenue"]
- `data/test.csv` (330883 bytes); columns: ["Administrative", "Administrative_Duration", "Informational", "Informational_Duration", "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend", "SessionID"]
- `data/train.csv` (787993 bytes); columns: ["Administrative", "Administrative_Duration", "Informational", "Informational_Duration", "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend", "Revenue", "SessionID"]

## Public description

```
description.txt (40 lines)
sample_submission.csv (3700 lines)
test.csv (3700 lines)
train.csv (8632 lines)```

-> sample_submission.csv has 3699 rows and 2 columns.
Here is some information about the columns:
Revenue (float64) has range: 0.00 - 1.00, 0 nan values
SessionID (object) has 3699 unique values. Some example values: ['S01306', 'S09980', 'S11543', 'S07565']

-> test.csv has 3699 rows and 17 columns.
Here is some information about the columns:
Administrative (int64) has range: 0.00 - 27.00, 0 nan values
Administrative_Duration (float64) has range: 0.00 - 3398.75, 0 nan values
BounceRates (float64) has range: 0.00 - 0.20, 0 nan values
Browser (int64) has range: 1.00 - 13.00, 0 nan values
ExitRates (float64) has range: 0.00 - 0.20, 0 nan values
Informational (int64) has range: 0.00 - 24.00, 0 nan values
Informational_Duration (float64) has range: 0.00 - 2549.38, 0 nan values
Month (object) has 10 unique values. Some example values: ['May', 'Nov', 'Mar', 'Dec']
OperatingSystems (int64) has 8 unique values: [4, 3, 2, 1, 8, 7, 6, 5]
ProductRelated (int64) has range: 0.00 - 705.00, 0 nan values
ProductRelated_Duration (float64) has range: 0.00 - 63973.52, 0 nan values
Region (int64) has 9 unique values: [1, 3, 2, 7, 8, 5, 9, 4, 6]
SessionID (object) has 3699 unique values. Some example values: ['S01306', 'S09980', 'S11543', 'S07565']
SpecialDay (float64) has 6 unique values: [0.0, 1.0, 0.2, 0.8, 0.6, 0.4]
TrafficType (int64) has range: 1.00 - 20.00, 0 nan values
VisitorType (object) has 3 unique values: ['Returning_Visitor', 'New_Visitor', 'Other']
Weekend (bool) is 23.93% True, 76.07% False

-> train.csv has 8631 rows and 18 columns.
Here is some information about the columns:
Administrative (int64) has range: 0.00 - 26.00, 0 nan values
Administrative_Duration (float64) has range: 0.00 - 2720.50, 0 nan values
BounceRates (float64) has range: 0.00 - 0.20, 0 nan values
Browser (int64) has range: 1.00 - 13.00, 0 nan values
ExitRates (float64) has range: 0.00 - 0.20, 0 nan values
Informational (int64) has range: 0.00 - 14.00, 0 nan values
Informational_Duration (float64) has range: 0.00 - 2256.92, 0 nan values
Month (object) has 10 unique values. Some example values: ['May', 'Nov', 'Mar', 'Dec']
OperatingSystems (int64) has 8 unique values: [2, 3, 1, 4, 8, 7, 6, 5]
ProductRelated (int64) has range: 0.00 - 686.00, 0 nan values
ProductRelated_Duration (float64) has range: 0.00 - 29970.47, 0 nan values
Region (int64) has 9 unique values: [1, 3, 9, 4, 5, 7, 8, 6, 2]
Revenue (int64) has 2 unique values: [1, 0]
SessionID (object) has 8631 unique values. Some example values: ['S10287', 'S12234', 'S04506', 'S09695']
SpecialDay (float64) has 6 unique values: [0.0, 0.4, 0.6, 0.8, 0.2, 1.0]
TrafficType (int64) has range: 1.00 - 20.00, 0 nan values
VisitorType (object) has 3 unique values: ['New_Visitor', 'Returning_Visitor', 'Other']
Weekend (bool) is 22.98% True, 77.02% False
