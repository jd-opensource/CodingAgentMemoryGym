# OpenMLE-fast task

Task ID: `u-s-airline-traffic-data@1`

Native metric: `USAirlineTrafficRMSLEMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (791 bytes)
- `data/sample_submission.csv` (10281 bytes); columns: ["id", "target"]
- `data/test.csv` (8865 bytes); columns: ["id", "Year", "Month", "Series"]
- `data/train.csv` (28603 bytes); columns: ["Year", "Month", "Dom_Pax", "Int_Pax", "Pax", "Dom_Flt", "Int_Flt", "Flt", "Dom_RPM", "Int_RPM", "RPM", "Dom_ASM", "Int_ASM", "ASM", "Dom_LF", "Int_LF", "LF"]

## Public description

Competition: U.S. Airline Multi-Target Hierarchical Forecasting (2022-01 to 2023-09)

Files provided (under public/):
- train.csv: Monthly training data from 2003-01 to 2021-12 with columns Year, Month, and 15 target series.
- test.csv: Forecasting grid for 2022-01 to 2023-09 (21 months × 15 series). Columns: id, Year, Month, Series.
- sample_submission.csv: Example submission with correct structure (columns: id, target).
- description.txt: This file.

Target and submission format:
- Submit a CSV with two columns and a header: id, target.
- The id values must exactly match those in test.csv (one id per Series-month pair).

Evaluation metric:
- RMSLE computed over all rows: sqrt(mean((log1p(y) - log1p(y_hat))^2)).
- Predictions are clipped at zero during scoring. Lower is better.
