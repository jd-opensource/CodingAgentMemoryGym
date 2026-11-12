# OpenMLE-fast task

Task ID: `tsla-stock-data@1`

Native metric: `TeslaNextDayUpMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2933 bytes)
- `data/sample_submission.csv` (2156 bytes); columns: ["date", "prob_up"]
- `data/test.csv` (8764 bytes); columns: ["date", "adj_open", "adj_high", "adj_low", "adj_close", "adj_volume", "raw_close", "adj_change_percent", "adj_avg_vol_20d", "raw_open", "raw_high", "raw_low", "raw_volume", "raw_change_percent", "raw_avg_vol_20d"]
- `data/train.csv` (461626 bytes); columns: ["date", "adj_open", "adj_high", "adj_low", "adj_close", "adj_volume", "raw_close", "adj_change_percent", "adj_avg_vol_20d", "raw_open", "raw_high", "raw_low", "raw_volume", "raw_change_percent", "raw_avg_vol_20d", "target_up"]

## Public description

TSLA Next-Day Direction Probability Forecasting

Problem statement
Participants are asked to predict, for each trading date in the test set, the probability that Tesla’s split-adjusted closing price on the next trading day will be higher than on the current day. For a date t, the target is y_t = 1 if close_adj(t+1) > close_adj(t), else 0. Submit calibrated probabilities P(up on t+1).

Data description
- Train data: A single table providing daily features from 2010-06-29 through 2023-12-31 (chronologically ordered). It includes both split-adjusted and raw-scale OHLCV (open, high, low, close, volume) features merged by date, plus any derived columns present in the source files. A target column named target_up is provided for supervised learning.
- Test data: A single table providing daily features for 2024 trading dates available in the dataset (chronologically ordered) with the same columns as the train data except the target. Only dates for which the next trading day exists are included, ensuring labels are well-defined for evaluation.
- Date column: All rows include a date column that uniquely identifies each trading day.

Final data files
- train.csv: Feature table with target_up.
- test.csv: Feature table (no labels).
- sample_submission.csv: Example submission with columns: date, prob_up.

Submission format
- A CSV with the following columns:
  - date: trading date matching the test set exactly and in the same order.
  - prob_up: predicted probability that close_adj(t+1) > close_adj(t), a finite number in [0, 1].
- The number of rows must equal the number of rows in test.csv; each test date must appear exactly once and in the same order.

Evaluation metric
- Binary log loss (cross-entropy). For each test date i with true label y_i ∈ {0,1} and prediction p_i ∈ [0,1], the score is:
  LogLoss = - (1/N) * Σ_i [ y_i * log(p_i) + (1 - y_i) * log(1 - p_i) ]. Lower is better.
- This is a proper scoring rule that rewards well-calibrated probabilities and penalizes overconfidence. It is robust to class imbalance without ad-hoc weighting.

Guidance and expectations
- Avoid leakage: compute any rolling/aggregated features using only past information up to and including day t to predict y_t. Respect chronology in any preprocessing or model selection.
- Feature engineering: robust return, volatility, trend, and volume/liquidity features are encouraged. Both split-adjusted and raw-scale columns are provided to help models remain stable across stock splits and regime changes.
- Modeling: fit probabilistic classifiers (e.g., logistic regression with regularization, tree-based ensembles, gradient boosting, calibrated models, or temporal sequence models). Evaluate generalization on the held-out 2024 test period via the defined metric.
- Nonstationarity: expect regime shifts and volatility clustering. Proper time-series validation (e.g., rolling windows) is recommended during development.
