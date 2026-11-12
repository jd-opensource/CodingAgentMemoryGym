# OpenMLE-fast task

Task ID: `ev-battery-charging-data@1`

Native metric: `EVBatteryChargingMetrics` (higher is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2863 bytes)
- `data/sample_submission.csv` (1129 bytes); columns: ["row_id", "Optimal Charging Duration Class"]
- `data/test.csv` (24094 bytes); columns: ["row_id", "SOC (%)", "Voltage (V)", "Current (A)", "Battery Temp (°C)", "Ambient Temp (°C)", "Charging Cycles", "Charging Mode", "Battery Type", "EV Model"]
- `data/train.csv` (94736 bytes); columns: ["SOC (%)", "Voltage (V)", "Current (A)", "Battery Temp (°C)", "Ambient Temp (°C)", "Charging Cycles", "Charging Mode", "Battery Type", "EV Model", "Optimal Charging Duration Class"]

## Public description

EV Battery Optimal Charging Duration Classification

Problem statement:
- Predict the optimal charging duration class for an EV battery charging session. The target is a 3-class label: 0=Short (≤40 minutes), 1=Medium (≤80 minutes), 2=Long (>80 minutes).

Data description:
- Each row represents one charging session with mixed numerical and categorical features.
- Input features provided in the competition files:
  - Numerical: SOC (%), Voltage (V), Current (A), Battery Temp (°C), Ambient Temp (°C), Charging Cycles
  - Categorical: Charging Mode, Battery Type, EV Model
- Target column (in train.csv only): Optimal Charging Duration Class
- Notes:
  - Some original dataset columns that directly or indirectly encode duration (e.g., Charging Duration (min), Degradation Rate (%), Efficiency (%)) are excluded from the provided train/test files to prevent leakage.
  - No missing values are expected; duplicates are removed before splitting.

Files provided to participants:
- train.csv: Training data including all input features and the target column.
- test.csv: Test data with the same input features and an identifier column named row_id. The target labels are hidden.
- sample_submission.csv: Example submission file containing row_id and a placeholder Optimal Charging Duration Class for each test row.

Task guidance:
- Build an ML model to classify sessions into the three duration classes using the provided features.
- Recommended processing steps include:
  - Handling duplicates (already removed in the provided files)
  - Encoding categorical features (e.g., one-hot or target encoding with care to avoid leakage)
  - Scaling numerical features (standardization or robust scaling)
  - Feature engineering (e.g., interaction terms like Current×SOC, temperature delta: Battery Temp−Ambient Temp)
  - Model training and evaluation with cross-validation and proper regularization

Evaluation metric:
- Primary metric: Macro F1 score on the test set.
  - Macro F1 computes the F1 score per class (0, 1, 2) and averages them equally, promoting balanced performance across classes.
  - This metric is robust and fair under class imbalance.

Submission format:
- A CSV file with exactly two columns:
  - row_id: Integer identifier matching those in test.csv
  - Optimal Charging Duration Class: Predicted class labels in {0, 1, 2}
- The submission must contain exactly one row per test example, with no missing or duplicated row_id values.

Train/test split:
- A single deterministic stratified split is used to maintain class proportions across train and test.
- The split ratio is 80% train, 20% test.

Final data files:
- train.csv
- test.csv
- sample_submission.csv

Good luck! Build robust, leakage-free models that generalize across battery types, EV models, and charging modes while handling non-linear relationships and class imbalance.
