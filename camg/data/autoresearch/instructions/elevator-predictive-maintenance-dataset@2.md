# OpenMLE-fast task

Task ID: `elevator-predictive-maintenance-dataset@2`

Native metric: `ElevatorVibrationForecastingMetrics` (lower is better).

Create `/workspace/submission.csv` with the same row count and required columns as `data/sample_submission.csv`. Training labels are in `data/train.csv`; test features are in `data/test.csv`. Evaluation runs across an isolated boundary.

## Policy actions

You have one global budget of 30 ordinary actions. Every `shell_command`, `apply_patch`, and `submit` consumes one action, including rejected or failed actions. A compound shell command is one policy action, while every managed Python start is counted separately. Use only one action per response.

- `shell_command {"command":"...","workdir":".","timeout_ms":20000}`
- `apply_patch` followed by one `*** Begin Patch` / `*** End Patch` envelope
- `submit {}` grades `submission.csv` exactly once and always terminates

`TASK.md` and `data/` are read-only. Network, package installation, GPU access, and host paths are unavailable. The shell-action wall limit is 20 seconds and the managed-runtime aggregate limit inside one shell action is 15 seconds.

## Public files

- `data/description.txt` (3297 bytes)
- `data/sample_submission.csv` (1336853 bytes); columns: ["ID", "q0.1", "q0.5", "q0.9"]
- `data/test.csv` (1524482 bytes); columns: ["ID", "revolutions", "humidity", "x1", "x2", "x3", "x4", "x5"]
- `data/train.csv` (6641287 bytes); columns: ["ID", "revolutions", "humidity", "vibration", "x1", "x2", "x3", "x4", "x5"]
- `data/unlabeled.csv` (174762 bytes); columns: ["ID", "revolutions", "humidity", "vibration", "x1", "x2", "x3", "x4", "x5"]

## Public description

Elevator Door Vibration: Probabilistic Forecasting Challenge

Problem statement
- You are given time-ordered sensor readings from an elevator door system sampled at 4 Hz during evening operation. Your task is to predict uncertainty-aware targets: the conditional 10th, 50th, and 90th percentiles of the absolute vibration for each record in the test set.
- This is a probabilistic regression problem. Accurate and calibrated predictive intervals are crucial for maintenance planning (e.g., forecasting elevated vibration risk).

Data description
- Train data: tabular time series rows with columns [ID, revolutions, humidity, x1, x2, x3, x4, x5, vibration].
  - ID is a monotonically increasing index and reflects time order. Do not use it as a predictive feature unless you explicitly want to model position in time.
  - vibration is the supervised target in train data.
- Test data: same columns as train but without the vibration column.
- Optional unlabeled data: rows with missing vibration are provided separately to enable unsupervised or semi-supervised feature learning. They are not scored.

Files provided
- train.csv: Labeled training set.
- test.csv: Unlabeled test set (evaluation set).
- unlabeled.csv: Additional rows with missing target that you may use for representation learning or pretraining (optional).
- sample_submission.csv: Format illustration with valid but naive quantile predictions.

Rules and guidance
- Respect time order. Any feature engineering that uses information from the future relative to a row (e.g., forward-looking rolling stats) constitutes leakage. Use only past and present information when constructing features for each training/test row.
- You may build arbitrary models (e.g., gradient-boosted trees with quantile loss, quantile random forests, probabilistic neural nets, etc.).

Evaluation
- Submissions must contain exactly the following columns:
  - ID: integer identifier of each test row
  - q0.1, q0.5, q0.9: the predicted 10th, 50th (median), and 90th percentiles of vibration for that row
- Scoring uses the mean Pinball Loss across the three quantiles and averaged over all test rows. For a given quantile q in (0, 1), with ground truth y and prediction y_hat, the pinball loss is:
  - pinball_q(y, y_hat) = (y - y_hat) * q if y >= y_hat, else (y_hat - y) * (1 - q)
- The final score is the simple mean of pinball losses for q ∈ {0.1, 0.5, 0.9} across all rows. Lower is better.

Train/test split policy
- The split is chronological on the labeled rows to mimic real-world deployment: the earliest ~80% labeled rows are used for training and the most recent ~20% labeled rows form the test set. Rows with missing vibration are excluded from both train and test and provided as unlabeled.csv.

Submission format
- CSV with columns: ID, q0.1, q0.5, q0.9
- The set of IDs in your submission must match those in test.csv exactly; duplicates or missing IDs are not allowed.

Tips
- Consider lagged features and rolling statistics computed from historical values only.
- Consider modeling heteroskedasticity explicitly; prediction intervals should be wider in high-variance regimes and narrower in stable ones.
- Calibrate your quantile predictions to be well-ordered (q0.1 ≤ q0.5 ≤ q0.9) and reliable under temporal distribution shift.
