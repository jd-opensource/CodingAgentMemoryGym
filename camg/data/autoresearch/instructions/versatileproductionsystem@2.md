# OpenMLE-fast task

Task ID: `versatileproductionsystem@2`

Native metric: `VPSNextWeightForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2860 bytes)
- `data/sample_submission.csv` (37204 bytes); columns: ["row_id", "TargetWeight"]
- `data/test.csv` (101429 bytes); columns: ["row_id", "Timestamp", "CupState", "CurrentWeight", "EmergencyStop", "FanOn", "HeatCoverClosed", "HeaterOn", "HeatingTimePercent", "PotAvailable", "Produce", "ScaleCupDown", "ScaleCupUp", "SwitchToPot", "TrackSwitchAtCup", "TrackSwitchAtPot", "TurnScaleCup"]
- `data/train.csv` (513032 bytes); columns: ["row_id", "Timestamp", "CupState", "CurrentWeight", "EmergencyStop", "FanOn", "HeatCoverClosed", "HeaterOn", "HeatingTimePercent", "PotAvailable", "Produce", "ScaleCupDown", "ScaleCupUp", "SwitchToPot", "TrackSwitchAtCup", "TrackSwitchAtPot", "TurnScaleCup", "TargetWeight"]

## Public description

# VPS Short-Horizon Weight Forecasting Competition

Problem statement:
Predict the next-step cup weight in the Versatile Production System (VPS) production module. Given the current sensor and actuator readings at time t, forecast the cup’s CurrentWeight at time t+1. This short-horizon forecasting task models real industrial control needs for anticipative monitoring.

Data description:
- You are provided with supervised training data constructed from the VPS production module time series. Each training row contains features from time t and the regression target TargetWeight, which is the measured CurrentWeight at time t+1.
- The test set contains only features at time t; your task is to predict TargetWeight for each test row.

Final files provided:
- train.csv: Supervised pairs with features and the target column TargetWeight.
- test.csv: Feature-only rows matching the train feature schema and including a row_id.
- sample_submission.csv: A properly formatted example submission file with row_id and TargetWeight.

Columns:
- row_id: Unique integer identifier for each row (present in train.csv and test.csv; use it in your submission).
- TargetWeight: Regression target (present only in train.csv; in submissions, provide your predicted TargetWeight for each test row).
- Feature columns (present in both train.csv and test.csv):
  - Timestamp: Milliseconds since epoch.
  - CupState: Integer state of the cup handling.
  - CurrentWeight: Current cup weight at time t (note: the target is the next-step weight at time t+1).
  - EmergencyStop: Binary indicator (constant in this dataset).
  - FanOn: Binary indicator.
  - HeatCoverClosed: Binary indicator.
  - HeaterOn: Binary indicator.
  - HeatingTimePercent: Heating intensity percentage.
  - PotAvailable: Binary indicator.
  - Produce: Binary indicator.
  - ScaleCupDown: Binary indicator.
  - ScaleCupUp: Binary indicator.
  - SwitchToPot: Binary indicator.
  - TrackSwitchAtCup: Binary indicator.
  - TrackSwitchAtPot: Binary indicator.
  - TurnScaleCup: Binary indicator.

Modeling notes:
- The dynamics include nonlinear switching behavior and strong autoregressive signals. Approaches may range from feature-engineered regression to sequence models using sliding windows.
- The split preserves chronological order to avoid leakage. You may construct additional temporal features (e.g., rolling statistics) from the provided features.

Submission format:
- Create a CSV named submission.csv with exactly two columns: row_id and TargetWeight.
- row_id must match the values in test.csv; TargetWeight must be numeric predictions.

Evaluation metric:
- Mean Absolute Error (MAE) between your predicted TargetWeight and the ground truth for the corresponding row_id.
- MAE is robust and interpretable in physical units of weight.

Good luck, and enjoy modeling the VPS production dynamics!
