# OpenMLE-fast task

Task ID: `online-shoppers@1`

Native metric: `OnlineShoppersMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2879 bytes)
- `data/sample_submission.csv` (127891 bytes); columns: ["SessionID", "Revenue"]
- `data/test.csv` (411405 bytes); columns: ["SessionID", "Administrative", "Administrative_Duration", "Informational", "Informational_Duration", "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend"]
- `data/train.csv` (662401 bytes); columns: ["SessionID", "Administrative", "Administrative_Duration", "Informational", "Informational_Duration", "ProductRelated", "ProductRelated_Duration", "BounceRates", "ExitRates", "SpecialDay", "Month", "OperatingSystems", "Browser", "Region", "TrafficType", "VisitorType", "Weekend", "Revenue"]

## Public description

```
description.txt (45 lines)
sample_submission.csv (4689 lines)
test.csv (4689 lines)
train.csv (7518 lines)```

-> sample_submission.csv has 4688 rows and 2 columns.
Here is some information about the columns:
Revenue (float64) has range: 0.00 - 1.00, 0 nan values
SessionID (object) has 4688 unique values. Some example values: ['S012205', 'S005379', 'S005380', 'S005383']

-> test.csv has 4688 rows and 17 columns.
Here is some information about the columns:
Administrative (int64) has range: 0.00 - 27.00, 0 nan values
Administrative_Duration (float64) has range: 0.00 - 3398.75, 0 nan values
BounceRates (float64) has range: 0.00 - 0.20, 0 nan values
Browser (int64) has range: 1.00 - 13.00, 0 nan values
ExitRates (float64) has range: 0.00 - 0.20, 0 nan values
Informational (int64) has range: 0.00 - 14.00, 0 nan values
Informational_Duration (float64) has range: 0.00 - 2549.38, 0 nan values
Month (object) has 2 unique values: ['Nov', 'Dec']
OperatingSystems (int64) has 8 unique values: [3, 2, 1, 4, 6, 8, 5, 7]
ProductRelated (int64) has range: 0.00 - 584.00, 0 nan values
ProductRelated_Duration (float64) has range: 0.00 - 63973.52, 0 nan values
Region (int64) has 9 unique values: [4, 1, 6, 2, 9, 7, 5, 3, 8]
SessionID (object) has 4688 unique values. Some example values: ['S012205', 'S005379', 'S005380', 'S005383']
SpecialDay (float64) has 1 unique values: [0.0]
TrafficType (int64) has range: 1.00 - 20.00, 0 nan values
VisitorType (object) has 3 unique values: ['New_Visitor', 'Returning_Visitor', 'Other']
Weekend (int64) has 2 unique values: [1, 0]

-> train.csv has 7517 rows and 18 columns.
Here is some information about the columns:
Administrative (int64) has range: 0.00 - 24.00, 0 nan values
Administrative_Duration (float64) has range: 0.00 - 2720.50, 0 nan values
BounceRates (float64) has range: 0.00 - 0.20, 0 nan values
Browser (int64) has range: 1.00 - 13.00, 0 nan values
ExitRates (float64) has range: 0.00 - 0.20, 0 nan values
Informational (int64) has range: 0.00 - 24.00, 0 nan values
Informational_Duration (float64) has range: 0.00 - 2252.03, 0 nan values
Month (object) has 8 unique values: ['Feb', 'Mar', 'May', 'Oct', 'June', 'Jul', 'Aug', 'Sep']
OperatingSystems (int64) has 8 unique values: [1, 2, 4, 3, 7, 6, 8, 5]
ProductRelated (int64) has range: 0.00 - 705.00, 0 nan values
ProductRelated_Duration (float64) has range: 0.00 - 43171.23, 0 nan values
Region (int64) has 9 unique values: [1, 9, 2, 3, 4, 5, 6, 7, 8]
Revenue (int64) has 2 unique values: [0, 1]
SessionID (object) has 7517 unique values. Some example values: ['S007894', 'S000001', 'S000002', 'S000003']
SpecialDay (float64) has 6 unique values: [0.0, 0.4, 0.8, 1.0, 0.2, 0.6]
TrafficType (int64) has range: 1.00 - 20.00, 0 nan values
VisitorType (object) has 3 unique values: ['Returning_Visitor', 'New_Visitor', 'Other']
Weekend (int64) has 2 unique values: [0, 1]
