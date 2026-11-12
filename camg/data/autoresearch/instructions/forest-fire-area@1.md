# OpenMLE-fast task

Task ID: `forest-fire-area@1`

Native metric: `ForestFireAreaMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2243 bytes)
- `data/sample_submission.csv` (734 bytes); columns: ["row_id", "area"]
- `data/test.csv` (5414 bytes); columns: ["row_id", "X", "Y", "month", "day", "FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain"]
- `data/train.csv` (22058 bytes); columns: ["X", "Y", "month", "day", "FFMC", "DMC", "DC", "ISI", "temp", "RH", "wind", "rain", "area"]

## Public description

Forest Fire Burnt Area Prediction

Problem statement:
Predict the burnt area (in hectares) of a forest fire incident in Montesinho Natural Park using tabular spatial, temporal, and meteorological features recorded at the time of the incident.

Data description:
- Each row is a single fire incident.
- Features: X, Y (spatial grid coordinates), month, day (categorical strings), FFMC, DMC, DC, ISI (fire weather indices), temp (°C), RH (%), wind (km/h), rain (mm).
- Target: area (hectares), a non-negative continuous value with many zeros and a heavy-tailed positive distribution.

Files provided:
- train.csv: Full feature set plus the target column area. Participants train their models on this file.
- test.csv: Full feature set without the target. Includes a row_id column to link predictions to test rows.
- sample_submission.csv: A valid example submission with columns [row_id, area].

Task:
- Train your model on train.csv to predict area for each row in test.csv.
- Create a submission CSV with columns [row_id, area], one row per test example.

Evaluation metric:
- Root Mean Squared Logarithmic Error (RMSLE) computed on area+1.
- Definition: For each test row i with true value y_i and prediction p_i, we compute log(1 + y_i) and log(1 + max(p_i, 0)). RMSLE is the square root of the mean squared difference of these log-transformed values.
- Rationale: RMSLE treats proportional errors fairly, handles zero labels gracefully, and reduces the dominance of extreme outliers—well-suited to this dataset’s zero-inflation and heavy tail.

Split strategy and challenge:
- The organizer provides a single fixed train/test split with stratification on whether area > 0 to preserve the ratio of zero vs. positive cases in both sets. This ensures a realistic and challenging evaluation that balances common small/no-burn events and rare large burns.

Notes for modeling:
- Consider robust preprocessing: encode month/day (e.g., one-hot or cyclic), scale continuous features, and exploit interactions among fire weather indices.
- Optional: Train on log1p(area) and invert for predictions; the leaderboard uses RMSLE on the original scale.
- Ensure predictions are non-negative; negative values will be clipped to zero during scoring.
