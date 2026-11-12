# OpenMLE-fast task

Task ID: `air-passengers-forecast-dataset@2`

Native metric: `AirPassengersForecastMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (915 bytes)
- `data/sample_submission.csv` (899 bytes); columns: ["Month", "P10", "P50", "P90"]
- `data/test.csv` (198 bytes); columns: ["Month"]
- `data/train.csv` (1457 bytes); columns: ["Month", "Passengers"]

## Public description

AirPassengers Probabilistic Forecast (P10/P50/P90) Challenge

Public files
- train.csv: Historical monthly demand with columns [Month, Passengers].
- test.csv: Future months to forecast with column [Month].
- sample_submission.csv: Example submission with columns [Month, P10, P50, P90].

Task
Predict P10 (10th), P50 (50th), and P90 (90th) percentiles for each Month in test.csv.

Submission format
- CSV with columns exactly: Month, P10, P50, P90.
- The set of Month values must match those in test.csv (order is flexible).
- Quantiles must be ordered per row: P10 <= P50 <= P90.

Evaluation
- Mean pinball loss averaged over q in {0.1, 0.5, 0.9} and across all test rows. Lower is better.
- For quantile level q in (0,1): pinball_q(y, yhat) = max(q*(y - yhat), (q-1)*(y - yhat)).

Notes
- Do not include any paths in CSVs; keep only the specified columns.
- Use only the provided time series (no external data).
