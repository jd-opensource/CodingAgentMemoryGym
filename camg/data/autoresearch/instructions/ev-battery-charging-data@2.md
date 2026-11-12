# OpenMLE-fast task

Task ID: `ev-battery-charging-data@2`

Native metric: `EVBatteryDegradationMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2342 bytes)
- `data/sample_submission.csv` (6721 bytes); columns: ["SessionID", "Degradation Rate (%)"]
- `data/test.csv` (41652 bytes); columns: ["SessionID", "SOC (%)", "Voltage (V)", "Current (A)", "Battery Temp (°C)", "Ambient Temp (°C)", "Charging Duration (min)", "Charging Mode", "Battery Type", "Charging Cycles", "EV Model"]
- `data/train.csv` (109770 bytes); columns: ["SessionID", "SOC (%)", "Voltage (V)", "Current (A)", "Battery Temp (°C)", "Ambient Temp (°C)", "Charging Duration (min)", "Charging Mode", "Battery Type", "Charging Cycles", "EV Model", "Degradation Rate (%)"]

## Public description

Title: EV Battery Session Degradation Prediction (Regression)

Problem statement
Predict the Degradation Rate (%) for each electric vehicle (EV) charging session using session context and planned charging conditions. Accurate prediction enables optimized charging strategies and improved battery longevity.

Files provided
- train.csv: Labeled training data.
- test.csv: Unlabeled test data to score.
- sample_submission.csv: Example of the required submission format.

Target and input features
- Target (to predict):
  - Degradation Rate (%)
- Inputs (columns present in both train.csv and test.csv):
  - SessionID: Unique integer identifier for each session
  - SOC (%)
  - Voltage (V)
  - Current (A)
  - Battery Temp (°C)
  - Ambient Temp (°C)
  - Charging Duration (min)
  - Charging Mode (categorical: Fast, Normal, Slow)
  - Battery Type (categorical: Li-ion, LiFePO4)
  - Charging Cycles
  - EV Model (categorical: Model A, Model B, Model C)

Notes
- Columns that could cause leakage or redundancy have been removed from the competition files.
- Categorical features are not pre-encoded; participants should perform their own preprocessing/encoding.

Submission format
- A single CSV with exactly these two columns and header row:
  - SessionID
  - Degradation Rate (%)
- Each SessionID from test.csv must appear exactly once. Order does not matter.

Evaluation
- Metric: Root Mean Squared Error (RMSE) on Degradation Rate (%).
  - RMSE = sqrt(mean((y_true − y_pred)^2)) computed over all test rows.
  - Ties are broken by smaller RMSE.
  - Predictions must be numeric and finite (no NaN/Inf).

Guidance and baseline ideas
- Recommended preprocessing: handle missing values (if any), encode categoricals (e.g., one-hot), and scale numeric features if your model benefits from it.
- Useful engineered features can include: temperature delta (Battery − Ambient), interaction terms (e.g., Duration × Temp, SOC × Current), and nonlinear transforms for temperature.
- Models such as gradient boosting, random forests, kernel methods, and regularized linear models are well-suited. Cross-validation is encouraged for robust model selection.

Final deliverable
- Submit a CSV named however you like that follows the described submission format. Your score is computed using RMSE against the hidden labels corresponding to test.csv.
