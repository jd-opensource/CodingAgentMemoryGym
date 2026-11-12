# OpenMLE-fast task

Task ID: `solargeneration@1`

Native metric: `SolarACPowerRMSMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2397 bytes)
- `data/sample_submission.csv` (330737 bytes); columns: ["id", "AC Power in Watts"]
- `data/test.csv` (1300066 bytes); columns: ["id", "MODULE_TEMP", "Amb_Temp", "WIND_Speed", "IRR (W/m2)"]
- `data/train.csv` (6029630 bytes); columns: ["id", "MODULE_TEMP", "Amb_Temp", "WIND_Speed", "IRR (W/m2)", "AC Power in Watts"]

## Public description

Competition: Solar Plant AC Power Prediction

Problem statement
Predict instantaneous AC power output (Watts) at a 350 kWp ground-mounted photovoltaic plant using only exogenous on-site sensor readings. Participants must learn the nonlinear mapping from irradiance and thermal/wind conditions to AC power across the full operating range, including low-light and near-peak regimes.

Files provided
- train.csv: Training set with feature columns and the target.
- test.csv: Test set with the same feature columns (no target).
- sample_submission.csv: Example submission file with the expected column names and format.

Columns
- id: Unique identifier for each row.
- Features (provided in both train.csv and test.csv):
  - MODULE_TEMP
  - Amb_Temp
  - WIND_Speed
  - IRR (W/m2)
- Target (only in train.csv; must be predicted for test.csv):
  - AC Power in Watts

Important notes
- Only exogenous sensor features are included. Electrical current measurements (e.g., DC Current in Amps, AC Ir/Iy/Ib in Amps) are intentionally excluded to prevent target leakage. The goal is to learn power output from environmental and module conditions available prior to power computation.
- The data covers the full dynamic range of generation; expect nonlinearities (e.g., temperature effects, inverter clipping/derating-like behavior).

Evaluation metric
- Root Mean Squared Error (RMSE) on AC Power in Watts.
- Definition: RMSE = sqrt(mean((y_pred - y_true)^2)). Lower is better.
- Submissions are evaluated by matching on id and computing RMSE over all test rows. Predictions must be finite numeric values.

Train/test split policy (for your reference)
- A deterministic split is applied with stratification over irradiance quantiles to align irradiance distributions between train and test, preserving difficulty at high-power extremes.

Submission format
- CSV with exactly two columns in this order: id, AC Power in Watts
- id must exactly match the ids in test.csv (order need not match).
- Do not include any extra columns.

Modeling guidance (non-binding)
- Baselines: linear or polynomial regression on exogenous features, gradient boosting trees, or shallow neural networks.
- Feature ideas: interactions between irradiance and temperatures, temperature derating shapes, wind-speed cooling effects, nonlinear basis expansions, monotonicity constraints.

Good luck and build robust, physics-aware models!
