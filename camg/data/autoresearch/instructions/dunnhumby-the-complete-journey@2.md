# OpenMLE-fast task

Task ID: `dunnhumby-the-complete-journey@2`

Native metric: `HouseholdWeeklySpendMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2491 bytes)
- `data/sample_submission.csv` (372859 bytes); columns: ["row_id", "weekly_spend"]
- `data/test.csv` (207476 bytes); columns: ["row_id", "household_key", "week"]
- `data/train.csv` (2262341 bytes); columns: ["row_id", "household_key", "week", "weekly_spend"]

## Public description

Title: Household Weekly Spend Forecasting with Marketing Effects

Background
Retailers strive to forecast household-level spend to personalize offers and measure marketing effectiveness. This competition provides two years of retail data and challenges you to forecast weekly spend at the household level in a strictly time-aware setup.

Problem Statement
Given historical household purchasing behavior and time-aware context, predict the weekly spend (sum of sales value, clipped to non-negative) for each household during a held-out future period. The task is a regression-style time series forecasting problem at the household–week granularity.

Final Data Files
- train.csv: Training index and targets. Columns: row_id, household_key, week, weekly_spend.
- test.csv: Test index without targets. Columns: row_id, household_key, week.
- sample_submission.csv: Example submission. Columns: row_id, weekly_spend.

Your objective is to build features from the provided retail tables and train models that predict weekly_spend for the rows specified in test.csv.

Train/Test Split
A time-aware split is used. Training covers earlier weeks; the test set covers later weeks so that learned signals must come from prior history.

Submission Format
Submit a CSV file with the following columns:
- row_id: The identifier matching rows in test.csv.
- weekly_spend: Your predicted non-negative weekly spend (float). Predictions will be evaluated after clipping to the non-negative range.

Evaluation Metric
Submissions are evaluated using SMAPE (Symmetric Mean Absolute Percentage Error), computed per row and averaged across all rows:
SMAPE = mean_i [ 2 * |y_pred_i - y_true_i| / (|y_pred_i| + |y_true_i|) ] * 100
Handling details:
- If both y_pred and y_true are 0 for a row, its SMAPE contribution is defined as 0.
- Denominators are stabilized with a small epsilon to avoid division by zero.
- Predictions are clipped to be non-negative before evaluation.

Notes and Guidance
- Leakage control is essential. Ensure any features used to predict a week come only from prior weeks.
- Make use of behavioral lags, moving averages, basket intensity, price/discount summaries, category mix features, and marketing exposure signals.
- The data scale is sufficient to train modern ML models. Strong baselines include gradient boosting and time-aware models with engineered features.
- All test households appear in the training period at least once to ensure solvability.

Good luck and happy modeling!
