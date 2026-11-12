# OpenMLE-fast task

Task ID: `state-wise-power-consumption-in-india@1`

Native metric: `PowerConsumptionForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (1319 bytes)
- `data/sample_submission.csv` (38954 bytes); columns: ["Date", "State", "Usage"]
- `data/test.csv` (50297 bytes); columns: ["Date", "State", "Region", "latitude", "longitude"]
- `data/train.csv` (923029 bytes); columns: ["Date", "State", "Region", "latitude", "longitude", "Usage"]

## Public description

Competition: India State Daily Power Forecasting (2019–2020)

Problem statement
Participants must forecast daily electricity consumption (in Mega Units, MU) for every Indian state/UT over the final 28 calendar days in the dataset. You are given a multi-series panel of historical daily usage along with simple geographic metadata. Predict a complete panel of State × Date values for the holdout window.

Files in this directory (relative paths):
- train.csv: Long-format historical panel with columns:
  - Date (string, DD/MM/YYYY HH:MM:SS)
  - State (string)
  - Region (string: NR/WR/SR/ER/NER)
  - latitude (float)
  - longitude (float)
  - Usage (float, target)
- test.csv: Same schema as train.csv except without the Usage column. It contains the final 28 calendar days for all states.
- sample_submission.csv: Example of a valid submission for all rows in test.csv.

Target and horizon
- Target: Usage (MU) for each State × Date pair
- Forecast horizon: 28 consecutive calendar days at the end of the timeline

Evaluation metric
- Weighted Mean Absolute Percentage Error (wMAPE)
  wMAPE = sum_i |y_i − yhat_i| / sum_i y_i  (lower is better)

Submission format
- CSV with columns and order: Date, State, Usage
- Rows must match test.csv exactly by the (Date, State) keys with no duplicates or missing values.
