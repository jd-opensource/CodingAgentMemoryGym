# OpenMLE-fast task

Task ID: `customer-satisfaction-10k@1`

Native metric: `CustomerSatisfactionMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (2240 bytes)
- `data/sample_submission.csv` (14184 bytes); columns: ["id", "overall"]
- `data/test.csv` (22119 bytes); columns: ["id", "food", "speed", "accurate"]
- `data/train.csv` (104796 bytes); columns: ["id", "food", "speed", "accurate", "overall"]

## Public description

Competition: Ordinal prediction of delivery satisfaction (1–5)

Problem statement:
Predict a customer’s overall delivery satisfaction rating (1–5) from other survey signals collected for a cafe’s delivery service. The target is ordinal: mispredicting by 1 point is less severe than mispredicting by 3–4 points, so the evaluation reflects distance on the 1–5 scale.

Files provided:
- train.csv: Labeled training data with columns [id, food, speed, accurate, overall].
- test.csv: Unlabeled test data with columns [id, food, speed, accurate].

Target to predict:
- overall: Integer rating in [1, 5], representing the overall delivery experience.

Features:
- food: Integer rating in [1, 5], food quality.
- speed: Integer rating in [1, 5], speed of delivery.
- accurate: Binary indicator in {0, 1}, whether the order was accurate.
- id: Row identifier (no predictive content; used to align submissions).

Data notes:
- Missing values may exist in features. Rows with missing target are excluded from train/test splits. Participants should handle feature missingness via imputation or modeling.
- Values are cleaned and cast to the expected types. Column names are standardized to [id, food, speed, accurate, overall].

Submission format:
- CSV with exactly two columns: [id, overall].
- id must match every id in test.csv exactly once (no extras, no duplicates). overall can be any numeric value; it will be clipped to [1, 5] during evaluation.

Evaluation metric:
- Mean Absolute Error (MAE) between submitted overall predictions and the true overall labels for test.csv.
- MAE is computed as the mean of |prediction − truth| across all test rows. Lower is better.

Rules and expectations:
- Build an ML pipeline that includes data processing (e.g., cleaning, imputation), feature engineering, model training, and careful evaluation.
- Exploit the ordinal nature of the target (e.g., ordinal regression, custom losses, monotonic constraints) for potential gains.
- Ensure robust handling of missing values and skewed class distribution.

Tip:
- A simple baseline is to use food and speed as main signals with accurate as an additional binary feature, but stronger models should calibrate ordinal predictions and handle noise.
