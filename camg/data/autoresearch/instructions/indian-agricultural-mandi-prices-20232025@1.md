# OpenMLE-fast task

Task ID: `indian-agricultural-mandi-prices-20232025@1`

Native metric: `IndianMandiPriceForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2312 bytes)
- `data/sample_submission.csv` (116098 bytes); columns: ["row_id", "Modal_Price"]
- `data/test.csv` (324391 bytes); columns: ["row_id", "STATE", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Price Date"]
- `data/train.csv` (59274157 bytes); columns: ["STATE", "District Name", "Market Name", "Commodity", "Variety", "Grade", "Min_Price", "Max_Price", "Modal_Price", "Price Date"]

## Public description

```
description.txt (37 lines)
sample_submission.csv (5000 lines)
test.csv (5000 lines)
train.csv (732394 lines)```

-> sample_submission.csv has 4999 rows and 2 columns.
Here is some information about the columns:
Modal_Price (float64) has range: 9.84 - 84712.72, 0 nan values
row_id (int64) has range: 0.00 - 4998.00, 0 nan values

-> test.csv has 4999 rows and 8 columns.
Here is some information about the columns:
Commodity (object) has 5 unique values: ['Onion', 'Potato', 'Tomato', 'Wheat', 'Rice']
District Name (object) has 370 unique values. Some example values: ['nashik', 'ahmednagar', 'shajapur', 'pune']
Grade (object) has 7 unique values: ['FAQ', 'Non-FAQ', 'Local', 'Large', 'Ref grade-1', 'Medium', 'Ref grade-2']
Market Name (object) has 1549 unique values. Some example values: ['Indore', 'Shajapur', 'Ratlam', 'Pratapgarh']
Price Date (object) has 566 unique values. Some example values: ['2025-06-11', '2025-06-10', '2024-02-06', '2025-06-06']
STATE (object) has 29 unique values. Some example values: ['Uttar Pradesh', 'Madhya Pradesh', 'Maharashtra', 'Tamilnadu']
Variety (object) has 86 unique values. Some example values: ['Other', 'Local', 'Red', 'Potato']
row_id (int64) has range: 0.00 - 4998.00, 0 nan values

-> train.csv has 732393 rows and 10 columns.
Here is some information about the columns:
Commodity (object) has 5 unique values: ['Onion', 'Potato', 'Tomato', 'Wheat', 'Rice']
District Name (object) has 373 unique values. Some example values: ['bulandshahar', 'kottayam', 'nashik', 'pune']
Grade (object) has 7 unique values: ['FAQ', 'Non-FAQ', 'Local', 'Medium', 'Large', 'Ref grade-1', 'Ref grade-2']
Market Name (object) has 1598 unique values. Some example values: ['Pratapgarh', 'Durgapur', 'Ahmedabad(Chimanbhai Patal Market Vasana)', 'Asansol']
Max_Price (float64) has range: 0.00 - 480000.00, 0 nan values
Min_Price (float64) has range: 0.00 - 420000.00, 0 nan values
Modal_Price (float64) has range: 0.00 - 460000.00, 0 nan values
Price Date (object) has 736 unique values. Some example values: ['2023-06-12', '2023-06-14', '2023-06-19', '2023-06-20']
STATE (object) has 29 unique values. Some example values: ['Uttar Pradesh', 'Tamilnadu', 'Haryana', 'Madhya Pradesh']
Variety (object) has 94 unique values. Some example values: ['Other', 'Red', 'Desi', 'Potato']
