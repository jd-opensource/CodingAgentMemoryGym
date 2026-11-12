# OpenMLE-fast task

Task ID: `global-health-data-analysis-1990-2019@1`

Native metric: `SuicideRateForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (390 bytes)
- `data/sample_submission.csv` (21980 bytes); columns: ["row_id", "suicide_rate"]
- `data/test.csv` (118327 bytes); columns: ["Indicator", "continent", "Code", "country", "Year", "sex", "row_id"]
- `data/train.csv` (703164 bytes); columns: ["Indicator", "continent", "Code", "country", "Year", "sex", "suicide_rate", "row_id"]

## Public description

Global Suicide Rate Forecasting by Sex (2017–2019)

Files under public/:
- train.csv: Training data (2000–2016) with columns including row_id, Code, country, Year, sex, and target suicide_rate.
- test.csv: Test data (2017–2019) without target, with columns including row_id, Code, country, Year, sex.
- sample_submission.csv: Submission template with columns row_id and suicide_rate.
