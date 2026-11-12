# OpenMLE-fast task

Task ID: `sipri-military-expenditure-database@2`

Native metric: `MilitaryExpenditureMovementMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3245 bytes)
- `data/sample_submission.csv` (16491 bytes); columns: ["row_id", "movement"]
- `data/test.csv` (176710 bytes); columns: ["row_id", "Country", "Global Region", "Sub-Region", "Year", "Value_t", "Value_t_1", "Value_t_2", "Log1p_Value_t", "Log1p_Value_t_1", "Log1p_Value_t_2", "LogDiff_t", "LogDiff_t_1", "CAGR2_Log", "Vol3_Log", "Vol3_Lvl", "Decade"]
- `data/train.csv` (1715551 bytes); columns: ["row_id", "Country", "Global Region", "Sub-Region", "Year", "Value_t", "Value_t_1", "Value_t_2", "Log1p_Value_t", "Log1p_Value_t_1", "Log1p_Value_t_2", "LogDiff_t", "LogDiff_t_1", "CAGR2_Log", "Vol3_Log", "Vol3_Lvl", "Decade", "movement"]

## Public description

```
description.txt (51 lines)
sample_submission.csv (768 lines)
test.csv (768 lines)
train.csv (7292 lines)```

-> sample_submission.csv has 767 rows and 2 columns.
Here is some information about the columns:
movement (object) has 4 unique values: ['decrease', 'stable', 'small_change', 'increase']
row_id (object) has 767 unique values. Some example values: ['test_000766', 'test_000000', 'test_000001', 'test_000002']

-> test.csv has 767 rows and 17 columns.
Here is some information about the columns:
CAGR2_Log (float64) has range: -3.02 - 1.12, 0 nan values
Country (object) has 155 unique values. Some example values: ['Albania', 'Algeria', 'Angola', 'Austria']
Decade (int64) has 2 unique values: [2010, 2020]
Global Region (object) has 5 unique values: ['Asia & Oceania', 'Europe', 'Africa', 'Americas', 'Middle East']
Log1p_Value_t (float64) has range: 0.00 - 13.73, 0 nan values
Log1p_Value_t_1 (float64) has range: 0.00 - 13.67, 0 nan values
Log1p_Value_t_2 (float64) has range: 0.00 - 13.60, 0 nan values
LogDiff_t (float64) has range: -5.01 - 1.79, 0 nan values
LogDiff_t_1 (float64) has range: -5.01 - 1.79, 0 nan values
Sub-Region (object) has 14 unique values. Some example values: ['sub-Saharan Africa', 'Western Europe', 'Central Europe', 'Central America and the Caribbean']
Value_t (float64) has range: 0.00 - 916014.70, 0 nan values
Value_t_1 (float64) has range: 0.00 - 860692.20, 0 nan values
Value_t_2 (float64) has range: 0.00 - 806230.20, 0 nan values
Vol3_Log (float64) has range: 0.00 - 2.64, 0 nan values
Vol3_Lvl (float64) has range: 0.00 - 44819.79, 0 nan values
Year (int64) has 5 unique values: [2019, 2020, 2021, 2022, 2023]
row_id (object) has 767 unique values. Some example values: ['test_000766', 'test_000000', 'test_000001', 'test_000002']

-> train.csv has 7291 rows and 18 columns.
Here is some information about the columns:
CAGR2_Log (float64) has range: -2.41 - 4.76, 0 nan values
Country (object) has 173 unique values. Some example values: ['Argentina', 'Australia', 'Belgium', 'Costa Rica']
Decade (int64) has 7 unique values: [1950, 1960, 1970, 1980, 1990, 2000, 2010]
Global Region (object) has 5 unique values: ['Americas', 'Asia & Oceania', 'Europe', 'Middle East', 'Africa']
Log1p_Value_t (float64) has range: 0.00 - 13.53, 0 nan values
Log1p_Value_t_1 (float64) has range: 0.00 - 13.53, 0 nan values
Log1p_Value_t_2 (float64) has range: 0.00 - 13.53, 0 nan values
LogDiff_t (float64) has range: -7.76 - 8.87, 0 nan values
LogDiff_t_1 (float64) has range: -4.75 - 8.96, 0 nan values
Sub-Region (object) has 14 unique values. Some example values: ['sub-Saharan Africa', 'Western Europe', 'Middle East', 'South America']
Value_t (float64) has range: 0.00 - 752288.00, 0 nan values
Value_t_1 (float64) has range: 0.00 - 752288.00, 0 nan values
Value_t_2 (float64) has range: 0.00 - 752288.00, 0 nan values
Vol3_Log (float64) has range: 0.00 - 4.36, 0 nan values
Vol3_Lvl (float64) has range: 0.00 - 47681.25, 0 nan values
Year (int64) has range: 1951.00 - 2018.00, 0 nan values
movement (object) has 4 unique values: ['stable', 'increase', 'small_change', 'decrease']
row_id (object) has 7291 unique values. Some example values: ['train_007290', 'train_000000', 'train_000001', 'train_000002']
