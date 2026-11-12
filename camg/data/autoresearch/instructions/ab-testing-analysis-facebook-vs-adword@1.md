# OpenMLE-fast task

Task ID: `ab-testing-analysis-facebook-vs-adword@1`

Native metric: `AdEfficiencyAucMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2340 bytes)
- `data/sample_submission.csv` (1574 bytes); columns: ["row_id", "is_fb_better"]
- `data/test.csv` (11298 bytes); columns: ["row_id", "date_year", "date_month", "date_dayof_week", "facebook_ad_views", "facebook_ad_clicks", "facebook_cost_per_ad", "facebook_ctr", "facebook_cost_per_click", "adword_ad_views", "adword_ad_clicks", "adword_cost_per_ad", "adword_ctr", "adword_cost_per_click"]
- `data/train.csv` (46919 bytes); columns: ["row_id", "date_year", "date_month", "date_dayof_week", "facebook_ad_views", "facebook_ad_clicks", "facebook_cost_per_ad", "facebook_ctr", "facebook_cost_per_click", "adword_ad_views", "adword_ad_clicks", "adword_cost_per_ad", "adword_ctr", "adword_cost_per_click", "is_fb_better"]

## Public description

```
description.txt (41 lines)
sample_submission.csv (198 lines)
test.csv (198 lines)
train.csv (803 lines)```

-> sample_submission.csv has 197 rows and 2 columns.
Here is some information about the columns:
is_fb_better (float64) has 1 unique values: [0.5]
row_id (int64) has range: 1.00 - 992.00, 0 nan values

-> test.csv has 197 rows and 14 columns.
Here is some information about the columns:
adword_ad_clicks (int64) has range: 31.00 - 89.00, 0 nan values
adword_ad_views (int64) has range: 3715.00 - 5750.00, 0 nan values
adword_cost_per_ad (int64) has range: 50.00 - 200.00, 0 nan values
adword_cost_per_click (float64) has range: 0.64 - 6.00, 0 nan values
adword_ctr (float64) has range: 0.62 - 2.37, 0 nan values
date_dayof_week (int64) has 7 unique values: [4, 3, 6, 1, 2, 0, 5]
date_month (int64) has range: 1.00 - 12.00, 0 nan values
date_year (int64) has 4 unique values: [2021, 2022, 2023, 2024]
facebook_ad_clicks (int64) has range: 16.00 - 73.00, 0 nan values
facebook_ad_views (int64) has range: 1054.00 - 3311.00, 0 nan values
facebook_cost_per_ad (int64) has range: 60.00 - 249.00, 0 nan values
facebook_cost_per_click (float64) has range: 0.96 - 14.24, 0 nan values
facebook_ctr (float64) has range: 0.49 - 6.30, 0 nan values
row_id (int64) has range: 1.00 - 992.00, 0 nan values

-> train.csv has 802 rows and 15 columns.
Here is some information about the columns:
adword_ad_clicks (int64) has range: 31.00 - 89.00, 0 nan values
adword_ad_views (int64) has range: 3718.00 - 5754.00, 0 nan values
adword_cost_per_ad (int64) has range: 50.00 - 200.00, 0 nan values
adword_cost_per_click (float64) has range: 0.58 - 6.19, 0 nan values
adword_ctr (float64) has range: 0.54 - 2.33, 0 nan values
date_dayof_week (int64) has 7 unique values: [2, 5, 6, 0, 1, 4, 3]
date_month (int64) has range: 1.00 - 12.00, 0 nan values
date_year (int64) has 4 unique values: [2021, 2022, 2023, 2024]
facebook_ad_clicks (int64) has range: 15.00 - 73.00, 0 nan values
facebook_ad_views (int64) has range: 1050.00 - 3320.00, 0 nan values
facebook_cost_per_ad (int64) has range: 60.00 - 250.00, 0 nan values
facebook_cost_per_click (float64) has range: 0.96 - 16.53, 0 nan values
facebook_ctr (float64) has range: 0.49 - 6.86, 0 nan values
is_fb_better (int64) has 2 unique values: [1, 0]
row_id (int64) has range: 0.00 - 999.00, 0 nan values
