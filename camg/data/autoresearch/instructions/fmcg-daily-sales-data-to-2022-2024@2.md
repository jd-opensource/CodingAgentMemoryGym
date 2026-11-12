# OpenMLE-fast task

Task ID: `fmcg-daily-sales-data-to-2022-2024@2`

Native metric: `FMCGForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3125 bytes)
- `data/sample_submission.csv` (118620 bytes); columns: ["sku", "week", "channel", "region", "target_next_week"]
- `data/test.csv` (396539 bytes); columns: ["sku", "brand", "segment", "category", "week", "channel", "region", "units_sold", "stock_available", "promotion_flag", "price_unit", "delivery_days", "is_holiday_peak", "week_number", "month", "year", "is_holiday_week", "is_summer", "is_winter", "sku_age", "lifecycle_stage", "lag_1", "lag_2", "rolling_mean_4", "rolling_std_4", "momentum"]
- `data/train.csv` (5463746 bytes); columns: ["sku", "brand", "segment", "category", "week", "channel", "region", "units_sold", "stock_available", "promotion_flag", "price_unit", "delivery_days", "is_holiday_peak", "week_number", "month", "year", "is_holiday_week", "is_summer", "is_winter", "sku_age", "lifecycle_stage", "lag_1", "lag_2", "rolling_mean_4", "rolling_std_4", "momentum", "target_next_week"]

## Public description

Title: Weekly Hierarchical FMCG Forecasting (2022–2024)

Problem statement
- You are given a weekly retail panel for fast-moving consumer goods (FMCG) across SKUs, sales channels, and regions from 2022–2024. For each SKU × channel × region and week t, predict next-week units_sold (the column target_next_week for week t).
- Predictions are evaluated at multiple aggregation levels to reward models that are both locally accurate and globally coherent.

Files provided
- train.csv: Weekly panel with features and labels up to the start of the public test window. Contains target_next_week (label), units_sold, engineered covariates, and product hierarchy columns (brand, segment, category).
- test.csv: Same schema as train.csv but without target_next_week for the final 8 weeks. Predict target_next_week for every row in test.csv.
- sample_submission.csv: Correct submission structure with randomly generated placeholder values.

Prediction target and IDs
- Target to predict: target_next_week.
- The ID for each required prediction is the tuple (sku, week, channel, region). Your submission must contain every row from test.csv with exactly these four ID columns and a single target column named target_next_week.

Evaluation metric
- Weighted, hierarchical RMSSE (WRMSSE) across node sets:
  1) Bottom: sku × channel × region
  2) brand × channel × region
  3) segment × channel × region
  4) category × channel × region
  5) Global total
- For each node, we aggregate weekly predictions and actuals across all constituent series for each week in the test window, then compute RMSSE using the in-sample scale from the training window:
  RMSSE(node) = sqrt( MSE_test(node) / scale_train(node) )
  where MSE_test(node) is the mean squared error across all test weeks for that node, and scale_train(node) = mean( diff(y_train(node))^2 ) computed from the training weekly units_sold aggregated to that node. A small epsilon is used if the denominator is zero/undefined to ensure numerical stability.
- Node weights are proportional to the node’s total units_sold over the training window, normalized to sum to 1. The final score is the weighted average of RMSSE over all nodes. Lower is better.

Train/test split
- The test window is the last 8 unique weeks in the dataset (out-of-time). All earlier weeks form the training set. The split is deterministic and consistent across all SKUs/channels/regions.

Submission format
- CSV with exactly these columns in this order and no extras: sku, week, channel, region, target_next_week
- Values must be finite real numbers (no NaN/Inf). Any missing or duplicate keys will invalidate the submission.

Guidance (non-exhaustive)
- Data processing and feature engineering: you may use provided covariates (lags, rolling stats, calendar, price/promo/stock/delivery) and engineer additional features using only past information.
- Modeling: per-series statistical models (ARIMA/ETS), global tree-based models (LightGBM/XGBoost/CatBoost), or sequence models (TFT/N-BEATS) are viable. Post-hoc reconciliation (bottom-up, MinT, top-down) can improve hierarchical coherence.
